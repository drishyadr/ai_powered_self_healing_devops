from fastapi import FastAPI
import subprocess

from prometheus import get_cpu_usage, get_memory_usage, get_pod_restarts
from db import get_db_connection, fetch_recent_metrics
from ml.anomaly_detector import AnomalyDetector
from ml.utils import decide_action, execute_action

app = FastAPI()

# ------------------- BASIC -------------------
@app.get("/")
def root():
    return {"status": "FastAPI running"}

# ------------------- METRIC COLLECTION -------------------
@app.get("/collect_metrics")
def collect_metrics():
    cpu_data = get_cpu_usage()
    mem_data = get_memory_usage()
    restart_data = get_pod_restarts()

    if not cpu_data:
        return {"error": "CPU metrics not available yet"}

    conn = get_db_connection()
    cursor = conn.cursor()

    for cpu in cpu_data:
        pod = cpu["metric"].get("pod")
        cpu_val = float(cpu["value"][1])

        mem_val = next(
            (float(m["value"][1]) for m in mem_data if m["metric"].get("pod") == pod),
            0
        )

        restart_val = next(
            (int(r["value"][1]) for r in restart_data if r["metric"].get("pod") == pod),
            0
        )

        cursor.execute("""
            INSERT INTO pod_metrics (pod_name, cpu_usage, memory_usage, restarts)
            VALUES (%s, %s, %s, %s)
        """, (pod, cpu_val, mem_val, restart_val))

    conn.commit()
    cursor.close()
    conn.close()

    return {"status": "metrics inserted"}

# ------------------- RULE-BASED HEALING -------------------
CPU_THRESHOLD = 300
RESTART_THRESHOLD = 5

SYSTEM_PODS = [
    "kube-apiserver",
    "kube-scheduler",
    "kube-controller-manager",
    "etcd",
    "prometheus",
    "storage-provisioner"
]

def is_system_pod(pod_name):
    return any(sys in pod_name for sys in SYSTEM_PODS)

def heal_pod(pod_name):
    subprocess.run(["kubectl", "delete", "pod", pod_name], check=False)
    return "Pod restarted"

@app.get("/detect_anomalies")
def detect_anomalies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM pod_metrics
        WHERE timestamp >= NOW() - INTERVAL 2 MINUTE
    """)
    pods = cursor.fetchall()

    actions = []

    for pod in pods:
        if pod["cpu_usage"] > CPU_THRESHOLD or pod["restarts"] > RESTART_THRESHOLD:
            if is_system_pod(pod["pod_name"]):
                action = "ALERT_ONLY"
            else:
                action = heal_pod(pod["pod_name"])

            actions.append({
                "pod": pod["pod_name"],
                "reason": "Rule-based threshold breach",
                "action": action
            })

    cursor.close()
    conn.close()
    return actions

# ------------------- ML-BASED PREDICTIVE HEALING -------------------
detector = None
ANOMALY_THRESHOLD = 0.0103

@app.get("/predict_anomalies")
def predict_anomalies():
    global detector

    if detector is None:
        detector = AnomalyDetector()

    df = fetch_recent_metrics(minutes=10)

    # 🚦 Guard: minimum data for LSTM
    if df.empty or len(df) < 35:
        return {
            "status": "not_enough_data",
            "rows_found": len(df),
            "required_min": 35
        }

    results = []
    handled_pods = set()  # 🔁 Prevent duplicate actions

    for metric in ["cpu_usage", "memory_usage", "restart_count"]:
        anomalies = detector.detect_metric(df, metric, ANOMALY_THRESHOLD)

        for _, row in anomalies.iterrows():
            pod_name = row["pod_name"]

            if pod_name in handled_pods:
                continue

            handled_pods.add(pod_name)

            recent = df[df["pod_name"] == pod_name].iloc[-1]

            if is_system_pod(pod_name):
                action = "ALERT_ONLY"
            else:
                action = decide_action(
                    recent["cpu_usage"],
                    recent["memory_usage"],
                    recent["restart_count"]
                )
                execute_action(action, pod_name)

            results.append({
                "pod": pod_name,
                "metric": metric,
                "score": float(row["anomaly_score"]),
                "action": action,
                "timestamp": str(row["timestamp"])
            })

    return {
        "total_anomalies": len(results),
        "details": results
    }

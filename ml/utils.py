import subprocess

def decide_action(cpu, memory, restarts):
    if restarts >= 3:
        return "RESTART_POD"
    if cpu > 0.85 or memory > 0.85:
        return "SCALE_DEPLOYMENT"
    return "ALERT_ONLY"


def execute_action(action, pod_name, namespace="default"):
    try:
        if action == "RESTART_POD":
            subprocess.run(
                ["kubectl", "delete", "pod", pod_name, "-n", namespace],
                check=False,
                capture_output=True,
                text=True
            )

        elif action == "SCALE_DEPLOYMENT":
            print(f"[INFO] Recommend scaling deployment for pod {pod_name}")

        else:
            print(f"[INFO] Alert only for pod {pod_name}")

    except FileNotFoundError:
        print("[WARN] kubectl not found — action simulated only")

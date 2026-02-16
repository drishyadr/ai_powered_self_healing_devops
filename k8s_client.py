from kubernetes import client, config

def get_k8s_clients():
    try:
        # This works when running from your laptop
        config.load_kube_config(config_file=r"C:\Users\drish\.kube\config")
    except Exception as e:
        print("Kube config load failed:", e)
        raise

    core_v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    return core_v1, apps_v1

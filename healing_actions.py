from k8s_client import get_k8s_clients

def restart_pod(pod_name, namespace="default"):
    core_v1, _ = get_k8s_clients()
    try:
        core_v1.delete_namespaced_pod(
            name=pod_name,
            namespace=namespace,
            grace_period_seconds=0
        )
        return f"Pod {pod_name} restarted"
    except Exception as e:
        return f"Failed to restart {pod_name}: {str(e)}"

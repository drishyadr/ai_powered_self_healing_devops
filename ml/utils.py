import subprocess

def decide_action(cpu, memory, restarts):
    if restarts >= 3:
        return "RESTART_POD"
    if cpu > 0.85 or memory > 0.85:
        return "SCALE_DEPLOYMENT"
    return "ALERT_ONLY"


SYSTEM_PODS = [
    "kube-apiserver",
    "kube-scheduler",
    "kube-controller-manager",
    "etcd",
    "prometheus",
    "storage-provisioner",
    "coredns",
    "kube-proxy"
]

def is_system_pod(pod_name):
    return any(sys in pod_name for sys in SYSTEM_PODS)


def execute_action(action, pod_name):
    if is_system_pod(pod_name):
        return "Protected system pod — alert only"

    if action == "RESTART_POD":
        return restart_pod(pod_name)

    elif action == "SCALE_DEPLOYMENT":
        deployment = pod_name.rsplit("-", 2)[0]
        return scale_deployment(deployment, replicas=3)

    else:
        return "Alert only — no action"


from k8s_client import get_k8s_clients

def restart_pod(pod_name):
    core_v1, _ = get_k8s_clients()
    try:
        pods = core_v1.list_pod_for_all_namespaces(field_selector=f"metadata.name={pod_name}")
        if not pods.items:
            return f"Pod {pod_name} not found"

        namespace = pods.items[0].metadata.namespace

        core_v1.delete_namespaced_pod(
            name=pod_name,
            namespace=namespace,
            grace_period_seconds=0
        )
        return f"Pod {pod_name} restarted in {namespace}"

    except Exception as e:
        return f"Restart failed: {str(e)}"


def scale_deployment(deployment_name, replicas):
    _, apps_v1 = get_k8s_clients()
    try:
        deployments = apps_v1.list_deployment_for_all_namespaces(
            field_selector=f"metadata.name={deployment_name}"
        )
        if not deployments.items:
            return f"Deployment {deployment_name} not found"

        namespace = deployments.items[0].metadata.namespace

        body = {"spec": {"replicas": replicas}}
        apps_v1.patch_namespaced_deployment_scale(
            name=deployment_name,
            namespace=namespace,
            body=body
        )

        return f"Scaled {deployment_name} to {replicas} in {namespace}"

    except Exception as e:
        return f"Scaling failed: {str(e)}"

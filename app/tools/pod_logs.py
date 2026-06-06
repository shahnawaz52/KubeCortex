from kubernetes import client, config
from kubernetes.client.rest import ApiException


def _decode_logs(logs: str | bytes | None) -> str:
    if logs is None:
        return ""
    if isinstance(logs, bytes):
        return logs.decode("utf-8", errors="replace")
    return logs

def get_pod_logs(namespace: str, pod: str, tail_lines: int = 50) -> dict:
    config.load_kube_config()
    v1 = client.CoreV1Api()
    logs = _decode_logs(
        v1.read_namespaced_pod_log(
            name=pod,
            namespace=namespace,
            tail_lines=tail_lines,
        )
    )

    try:
        previous_logs = _decode_logs(
            v1.read_namespaced_pod_log(
                name=pod,
                namespace=namespace,
                tail_lines=tail_lines,
                previous=True,
            )
        )
    except ApiException:
        previous_logs = ""
    
    return {
        "pod_name": pod,
        "namespace": namespace,
        "logs": logs,
        "log_lines": logs.splitlines(),
        "previous_logs": previous_logs,
        "previous_log_lines": previous_logs.splitlines(),
        "tail_lines": tail_lines,
    }

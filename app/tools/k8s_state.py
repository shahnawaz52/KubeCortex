from datetime import datetime, timezone
from kubernetes import client, config

def get_pod_state(namespace: str, pod: str) -> dict:
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pod_obj = v1.read_namespaced_pod(pod, namespace)
    container_statuses = []
    restart_count = 0
    for cs in (pod_obj.status.container_statuses or []):
        restart_count += cs.restart_count
        state = {}
        if cs.state.waiting:
            state = {
                "waiting":{
                    "reason": cs.state.waiting.reason
                    }
                }
        elif cs.state.running:
            state = {
                "running": {
                    "started_at": str(cs.state.running.started_at)
                    }
                }
        elif cs.state.terminated:
            state = {
                "terminated": {
                    "reason": cs.state.terminated.reason, "exit_code": cs.state.terminated.exit_code
                    }
                }
        container_statuses.append({
            "name": cs.name,
            "ready": cs.ready,
            "restart_count": cs.restart_count,
            "state": state,
        })
    conditions = [
        {"type": c.type, "status": c.status}
        for c in (pod_obj.status.conditions or [])
    ]
    events_api = v1.list_namespaced_event(namespace, field_selector=f"involvedObject.name={pod}")
    recent_events = [
        {
            "type": e.type,
            "reason": e.reason,
            "message": e.message,
            "count": e.count,
            "last_timestamp": str(e.last_timestamp),
        }
        for e in events_api.items[-5:]
    ]
    return {
        "pod_name": pod,
        "namespace": namespace,
        "phase": pod_obj.status.phase,
        "restart_count": restart_count,
        "container_statuses": container_statuses,
        "conditions": conditions,
        "recent_events": recent_events,
    }

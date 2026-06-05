def classify_incident(raw_alert: dict) -> tuple[str, str]:
    alerts = raw_alert.get("alerts", [])
    if not alerts:
        return "UnknownIncident", "No alerts were provided in the payload"

    first_alert = alerts[0]
    labels = first_alert.get("labels", {})
    annotations = first_alert.get("annotations", {})
    alert_name = labels.get("alertname", "UnknownAlert").lower()
    summary = annotations.get("summary", "No summary provided").strip()

    if "crash" in alert_name or "restart" in alert_name:
        return "CrashLoopBackOff", summary or "Pod is repeatedly crashing"

    if "rollout" in alert_name or "deployment" in alert_name:
        return "FailedRollout", summary or "Deployment rollout appears to be failing"

    if "memory" in alert_name or "oom" in alert_name:
        return "HighMemoryUsage", summary or "Workload is showing memory pressure"

    return "UnknownIncident", summary or "Unable to classify incident from alert payload"

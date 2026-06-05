from app.services.planner import classify_incident


def test_classify_crash_loop_backoff() -> None:
    raw_alert = {
        "alerts": [
            {
                "labels": {
                    "alertname": "PodCrashLooping",
                    "namespace": "default",
                    "pod": "demo-app-123",
                },
                "annotations": {
                    "summary": "Pod is restarting repeatedly",
                },
            }
        ]
    }

    incident_type, summary = classify_incident(raw_alert)

    assert incident_type == "CrashLoopBackOff"
    assert summary == "Pod is restarting repeatedly"


def test_classify_failed_rollout() -> None:
    raw_alert = {
        "alerts": [
            {
                "labels": {
                    "alertname": "DeploymentRolloutFailed",
                    "namespace": "default",
                    "deployment": "checkout-service",
                },
                "annotations": {
                    "summary": "Deployment rollout is failing",
                },
            }
        ]
    }

    incident_type, summary = classify_incident(raw_alert)

    assert incident_type == "FailedRollout"
    assert summary == "Deployment rollout is failing"


def test_classify_high_memory_usage() -> None:
    raw_alert = {
        "alerts": [
            {
                "labels": {
                    "alertname": "HighMemoryUsage",
                    "namespace": "default",
                    "pod": "payments-service",
                },
                "annotations": {
                    "summary": "Memory usage is above threshold",
                },
            }
        ]
    }

    incident_type, summary = classify_incident(raw_alert)

    assert incident_type == "HighMemoryUsage"
    assert summary == "Memory usage is above threshold"


def test_classify_unknown_incident() -> None:
    raw_alert = {
        "alerts": [
            {
                "labels": {
                    "alertname": "SomethingWeird",
                    "namespace": "default",
                },
                "annotations": {
                    "summary": "Unexpected alert",
                },
            }
        ]
    }

    incident_type, summary = classify_incident(raw_alert)

    assert incident_type == "UnknownIncident"
    assert summary == "Unexpected alert"


def test_classify_empty_alerts() -> None:
    raw_alert = {
        "alerts": []
    }

    incident_type, summary = classify_incident(raw_alert)

    assert incident_type == "UnknownIncident"
    assert summary == "No alerts were provided in the payload"
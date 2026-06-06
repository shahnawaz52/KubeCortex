from app.db.models import Incident, InvestigationStep
from app.db.session import SessionLocal
from app.services.planner import classify_incident
from app.tools.k8s_state import get_pod_state


def process_incident(incident_id: int) -> None:
    db = SessionLocal()
    incident = None

    try:
        incident = db.get(Incident, incident_id)
        if incident is None:
            return

        incident.status = "processing"
        db.commit()
        db.refresh(incident)

        incident_type, summary = classify_incident(incident.raw_alert)

        step = InvestigationStep(
            incident_id=incident.id,
            step_type="classification",
            status="completed",
            input_payload=incident.raw_alert,
            output_payload={
                "incident_type": incident_type,
                "summary": summary,
            },
        )
        db.add(step)

        incident.incident_type = incident_type
        incident.summary = summary
        incident.status = "classified"

        db.commit()
        db.refresh(incident)

        if incident_type == "CrashLoopBackOff":
            labels = incident.raw_alert.get("alerts",[{}])[0].get("labels",{})
            namespace = labels.get("namespace")
            pod = labels.get("pod")
            try:
                k8s_result = get_pod_state(namespace,pod)

                k8s_step = InvestigationStep(
                    incident_id=incident.id,
                    step_type="k8s_state",
                    status="completed",
                    input_payload={
                        "namespace": namespace,
                        "pod": pod,
                    },
                    output_payload=k8s_result,
                )
                db.add(k8s_step)
            except Exception as exc:
                k8s_step = InvestigationStep(
                    incident_id=incident.id,
                    step_type="k8s_state",
                    status="failed",
                    input_payload={
                        "namespace": namespace,
                        "pod": pod,
                    },
                    output_payload={
                        "error": str(exc),
                    },
                )
                db.add(k8s_step)

            db.commit()
            db.refresh(incident)

    except Exception as exc:
        db.rollback()
        if incident is not None:
            incident.status = "failed"
            incident.summary = f"Processing failed: {str(exc)}"
            db.commit()

    finally:
        db.close()

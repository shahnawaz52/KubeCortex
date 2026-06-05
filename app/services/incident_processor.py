from app.db.models import Incident, InvestigationStep
from app.db.session import SessionLocal
from app.services.planner import classify_incident


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

    except Exception as exc:
        db.rollback()
        if incident is not None:
            incident.status = "failed"
            incident.summary = f"Processing failed: {str(exc)}"
            db.commit()

    finally:
        db.close()

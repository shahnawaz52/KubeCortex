from app.db.models.incident import Incident
from app.db.session import SessionLocal
from app.services.planner import classify_incident


def process_incident(incident_id: int) -> None:
    db = SessionLocal()

    try:
        incident = db.get(Incident, incident_id)
        if incident is None:
            return

        incident.status = "processing"
        db.commit()
        db.refresh(incident)

        incident_type, summary = classify_incident(incident.raw_alert)

        incident.incident_type = incident_type
        incident.summary = summary
        incident.status = "classified"

        db.commit()
        db.refresh(incident)

    finally:
        db.close()

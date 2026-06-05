from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from redis.exceptions import RedisError

from app.db.dependencies import get_db
from app.db.models import Incident
from app.queue.redis_queue import enqueue_incident
from app.schemas.alert import AlertPayload

router = APIRouter()


@router.post("/alerts")
def create_alert(
    payload: AlertPayload,
    db: Session = Depends(get_db),
) -> dict[str, int | str]:
    try:
        incident = Incident(
            status="received",
            source=payload.source,
            raw_alert=payload.model_dump(),
            incident_type=None,
            summary=None,
        )
        db.add(incident)
        db.commit()
        db.refresh(incident)

        try:
            enqueue_incident(incident.id)
        except RedisError as exc:
            incident.status = "queued_failed"
            db.commit()
            db.refresh(incident)
            raise HTTPException(status_code=500, detail="Failed to enqueue incident") from exc

        return {
            "id": incident.id,
            "status": incident.status,
        }

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create incident") from exc

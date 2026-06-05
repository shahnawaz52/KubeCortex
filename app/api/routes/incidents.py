from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.db.models import Incident
from app.db.dependencies import get_db
from app.schemas.incident import IncidentResponse

router = APIRouter()


@router.get("/incidents", response_model=list[IncidentResponse])
def list_incidents(
    db: Session = Depends(get_db),
) -> list[IncidentResponse]:
    try:
        statement = (
            select(Incident)
            .options(selectinload(Incident.steps))
            .order_by(Incident.created_at.desc())
        )
        return list(db.scalars(statement).all())
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=500, detail="Failed to fetch incidents") from exc


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
) -> IncidentResponse:
    try:
        statement = (
            select(Incident)
            .options(selectinload(Incident.steps))
            .where(Incident.id == incident_id)
        )
        incident = db.scalar(statement)

        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")

        return incident

    except SQLAlchemyError as exc:
        raise HTTPException(status_code=500, detail="Failed to fetch incident") from exc
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict

class InvestigationStepResponse(BaseModel):
    id: int
    incident_id: int
    step_type: str
    status: str
    input_payload: dict[str, Any]
    output_payload: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentResponse(BaseModel):
    id: int
    status: str
    source: str
    raw_alert: dict[str, Any]
    incident_type: str | None
    summary: str | None
    created_at: datetime
    updated_at: datetime
    steps: list[InvestigationStepResponse] = []

    model_config = ConfigDict(from_attributes=True)

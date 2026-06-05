from typing import Any
from pydantic import BaseModel, Field

class AlertItem(BaseModel):
    labels: dict[str, str] = Field(default_factory=dict)
    annotations: dict[str, str] = Field(default_factory=dict)

class AlertPayload(BaseModel):
    alerts: list[AlertItem]
    source: str = "webhook"
    metadata: dict[str, Any] = Field(default_factory=dict)

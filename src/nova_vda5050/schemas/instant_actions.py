"""VDA5050 V3.0.0 InstantActions message."""

from __future__ import annotations

from pydantic import BaseModel, Field

from nova_vda5050.schemas import Action


class InstantActionsMessage(BaseModel):
    """VDA5050 V3.0.0 InstantActions — immediate actions sent to a robot."""

    # Header
    headerId: int
    timestamp: str
    version: str = "3.0.0"
    manufacturer: str
    serialNumber: str

    # Actions
    actions: list[Action] = Field(default_factory=list)

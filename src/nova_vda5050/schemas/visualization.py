"""VDA5050 V3.0.0 Visualization message."""

from __future__ import annotations

from pydantic import BaseModel, Field

from nova_vda5050.schemas import AgvPosition, Velocity


class VisualizationMessage(BaseModel):
    """VDA5050 V3.0.0 Visualization — high-rate position for map rendering."""

    # Header
    headerId: int
    timestamp: str
    version: str = "3.0.0"
    manufacturer: str
    serialNumber: str

    # Position
    agvPosition: AgvPosition | None = None
    velocity: Velocity | None = None

    # Order context
    orderId: str = ""
    orderUpdateId: int = 0
    lastNodeId: str = ""
    lastNodeSequenceId: int = 0

    # Driving
    driving: bool = False
    paused: bool = False

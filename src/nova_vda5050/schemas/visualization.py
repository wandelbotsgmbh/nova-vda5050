"""VDA5050 V3.0.0 Visualization message."""

from __future__ import annotations

from pydantic import BaseModel, Field

from nova_vda5050.schemas import (
    AgvPosition,
    IntermediatePath,
    MobileRobotPosition,
    PlannedPath,
    Velocity,
)


class VisualizationMessage(BaseModel):
    """VDA5050 V3.0.0 Visualization — high-rate position for map rendering."""

    # Header
    headerId: int
    timestamp: str
    version: str = "3.0.0"
    manufacturer: str
    serialNumber: str

    # V3 reference back to the state message this visualization relates to
    referenceStateHeaderId: int | None = None

    # Position — V3 uses mobileRobotPosition, keep agvPosition for compat
    mobileRobotPosition: MobileRobotPosition | None = None
    agvPosition: AgvPosition | None = None  # V2 compat
    velocity: Velocity | None = None

    # Path (V3)
    plannedPath: PlannedPath | None = None
    intermediatePath: IntermediatePath | None = None

    # Order context
    orderId: str = ""
    orderUpdateId: int = 0
    lastNodeId: str = ""
    lastNodeSequenceId: int = 0

    # Driving
    driving: bool = False
    paused: bool = False

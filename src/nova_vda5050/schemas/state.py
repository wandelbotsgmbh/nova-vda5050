"""VDA5050 V3.0.0 State message."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from nova_vda5050.schemas import (
    ActionState,
    AgvPosition,
    BatteryState,
    EdgeState,
    Error,
    Information,
    Load,
    NodeState,
    OperatingMode,
    SafetyState,
    Velocity,
)


class StateMessage(BaseModel):
    """VDA5050 V3.0.0 State Message."""

    # Header
    headerId: int
    timestamp: str
    version: str = "3.0.0"
    manufacturer: str
    serialNumber: str

    # Order
    orderId: str = ""
    orderUpdateId: int = 0
    lastNodeId: str = ""
    lastNodeSequenceId: int = 0

    # Driving
    driving: bool = False
    paused: bool = False
    newBaseRequest: bool = False

    # Position / velocity
    agvPosition: AgvPosition | None = None
    velocity: Velocity | None = None

    # Battery / safety
    batteryState: BatteryState = Field(default_factory=BatteryState)
    operatingMode: OperatingMode = OperatingMode.AUTOMATIC
    safetyState: SafetyState = Field(default_factory=SafetyState)

    # Order state
    nodeStates: list[NodeState] = Field(default_factory=list)
    edgeStates: list[EdgeState] = Field(default_factory=list)
    actionStates: list[ActionState] = Field(default_factory=list)

    # Errors / info
    errors: list[Error] = Field(default_factory=list)
    informations: list[Information] = Field(default_factory=list)

    # Loads
    loads: list[Load] = Field(default_factory=list)

    # Optional
    distanceSinceLastNode: float | None = None
    zoneSetId: str | None = None

    @classmethod
    def create_minimal(
        cls,
        header_id: int,
        manufacturer: str,
        serial_number: str,
        timestamp: str | None = None,
    ) -> StateMessage:
        return cls(
            headerId=header_id,
            timestamp=timestamp or datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            manufacturer=manufacturer,
            serialNumber=serial_number,
            agvPosition=AgvPosition(),
            velocity=Velocity(),
        )

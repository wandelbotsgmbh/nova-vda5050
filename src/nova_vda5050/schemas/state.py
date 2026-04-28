"""VDA5050 V3.0.0 State message."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from nova_vda5050.schemas import (
    ActionState,
    AgvPosition,
    BatteryState,
    EdgeRequest,
    EdgeState,
    Error,
    Information,
    IntermediatePath,
    Load,
    MapState,
    MobileRobotPosition,
    NodeState,
    OperatingMode,
    PlannedPath,
    PowerSupply,
    SafetyState,
    Velocity,
    ZoneRequest,
    ZoneSetState,
)


class StateMessage(BaseModel):
    """VDA5050 V3.0.0 State Message."""

    # Header
    headerId: int
    timestamp: str
    version: str = "3.0.0"
    manufacturer: str
    serialNumber: str

    # Maps and zone sets stored on the robot
    maps: list[MapState] = Field(default_factory=list)
    zoneSets: list[ZoneSetState] = Field(default_factory=list)

    # Order
    orderId: str = ""
    orderUpdateId: int = 0
    lastNodeId: str = ""
    lastNodeSequenceId: int = 0

    # Driving
    driving: bool = False
    paused: bool = False
    newBaseRequest: bool = False

    # Position / velocity — V3 uses mobileRobotPosition, keep agvPosition for compat
    mobileRobotPosition: MobileRobotPosition | None = None
    agvPosition: AgvPosition | None = None  # V2 compat, deprecated
    velocity: Velocity | None = None

    # Power — V3 uses powerSupply, keep batteryState for compat
    powerSupply: PowerSupply | None = None
    batteryState: BatteryState | None = None  # V2 compat, deprecated

    operatingMode: OperatingMode = OperatingMode.AUTOMATIC
    safetyState: SafetyState = Field(default_factory=SafetyState)

    # Order state
    nodeStates: list[NodeState] = Field(default_factory=list)
    edgeStates: list[EdgeState] = Field(default_factory=list)

    # Path planning (V3)
    plannedPath: PlannedPath | None = None
    intermediatePath: IntermediatePath | None = None

    # Action states — V3 splits into order/instant/zone
    actionStates: list[ActionState] = Field(default_factory=list)
    instantActionStates: list[ActionState] = Field(default_factory=list)
    zoneActionStates: list[ActionState] = Field(default_factory=list)

    # Requests (V3)
    zoneRequests: list[ZoneRequest] = Field(default_factory=list)
    edgeRequests: list[EdgeRequest] = Field(default_factory=list)

    # Errors / info — V3 uses 'information' (not 'informations')
    errors: list[Error] = Field(default_factory=list)
    information: list[Information] = Field(default_factory=list)
    informations: list[Information] | None = None  # V2 compat alias

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
            mobileRobotPosition=MobileRobotPosition(),
            agvPosition=AgvPosition(),
            powerSupply=PowerSupply(),
            batteryState=BatteryState(),
            velocity=Velocity(),
        )

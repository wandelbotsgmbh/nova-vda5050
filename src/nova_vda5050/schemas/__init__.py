"""Shared VDA5050 header fields and common sub-models."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────────────────────────────


class OperatingMode(str, Enum):
    STARTUP = "STARTUP"
    AUTOMATIC = "AUTOMATIC"
    SEMIAUTOMATIC = "SEMIAUTOMATIC"
    INTERVENED = "INTERVENED"
    MANUAL = "MANUAL"
    SERVICE = "SERVICE"
    TEACHIN = "TEACHIN"
    TEACH_IN = "TEACH_IN"  # V3 alias


class EStopState(str, Enum):
    AUTOACK = "AUTOACK"
    MANUAL = "MANUAL"
    REMOTE = "REMOTE"
    NONE = "NONE"


class InfoLevel(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"


class ErrorLevel(str, Enum):
    WARNING = "WARNING"
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"


class ActionStatus(str, Enum):
    WAITING = "WAITING"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    RETRIABLE = "RETRIABLE"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class BlockingType(str, Enum):
    NONE = "NONE"
    SOFT = "SOFT"
    SINGLE = "SINGLE"
    HARD = "HARD"


class ConnectionState(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    CONNECTIONBROKEN = "CONNECTIONBROKEN"


# ── Shared sub-models ────────────────────────────────────────────────────────


class Header(BaseModel):
    """VDA5050 message header — shared by all message types."""

    headerId: int = Field(description="Incrementing message header ID")
    timestamp: str = Field(description="ISO 8601 timestamp")
    version: str = Field(default="3.0.0", description="VDA5050 protocol version")
    manufacturer: str = Field(description="Robot manufacturer name")
    serialNumber: str = Field(description="Robot serial number")

    @classmethod
    def create(
        cls,
        header_id: int,
        manufacturer: str,
        serial_number: str,
        timestamp: str | None = None,
    ) -> Header:
        return cls(
            headerId=header_id,
            timestamp=timestamp or datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            manufacturer=manufacturer,
            serialNumber=serial_number,
        )


class AgvPosition(BaseModel):
    x: float = Field(default=0.0, description="X position in meters")
    y: float = Field(default=0.0, description="Y position in meters")
    theta: float = Field(default=0.0, description="Orientation in radians")
    mapId: str = Field(default="default", description="Map identifier")
    positionInitialized: bool = Field(default=True)
    deviationRange: float | None = Field(default=None)
    localizationScore: float | None = Field(default=None)
    mapDescription: str | None = Field(default=None)


class Velocity(BaseModel):
    vx: float = Field(default=0.0, description="Velocity in x direction (m/s)")
    vy: float = Field(default=0.0, description="Velocity in y direction (m/s)")
    omega: float = Field(default=0.0, description="Angular velocity (rad/s)")


class BatteryState(BaseModel):
    batteryCharge: float = Field(default=0.0, ge=0, le=100)
    batteryVoltage: float | None = Field(default=None)
    batteryHealth: float | None = Field(default=None, ge=0, le=100)
    charging: bool = Field(default=False)
    reach: int | None = Field(default=None)


class SafetyState(BaseModel):
    eStop: EStopState = Field(default=EStopState.NONE)
    fieldViolation: bool = Field(default=False)

    # V3 alias
    activeEmergencyStop: EStopState | None = Field(default=None)


# ── V3 position / power models ──────────────────────────────────────────────


class MobileRobotPosition(BaseModel):
    """V3 position model — replaces AgvPosition."""

    x: float = Field(default=0.0, description="X position in meters")
    y: float = Field(default=0.0, description="Y position in meters")
    theta: float = Field(default=0.0, description="Orientation in radians")
    mapId: str = Field(default="default", description="Map identifier")
    localized: bool = Field(default=True, description="True if position is trusted")
    localizationScore: float | None = Field(default=None, ge=0.0, le=1.0)
    deviationRange: float | None = Field(default=None, ge=0.0)


class PowerSupply(BaseModel):
    """V3 power supply — replaces BatteryState."""

    stateOfCharge: float = Field(default=0.0, ge=0, le=100, description="State of charge in %")
    batteryVoltage: float | None = Field(default=None)
    batteryCurrent: float | None = Field(default=None, description="Current in Ampere")
    batteryHealth: float | None = Field(default=None, ge=0, le=100)
    charging: bool = Field(default=False)
    range: float | None = Field(default=None, ge=0, description="Estimated reach in meters")


class MapState(BaseModel):
    """Map stored on the robot, reported in state."""

    mapId: str
    mapVersion: str
    mapStatus: str = Field(description="ENABLED or DISABLED")
    mapDescriptor: str | None = None


class ZoneSetState(BaseModel):
    """Zone set stored on the robot, reported in state."""

    zoneSetId: str
    mapId: str
    zoneSetStatus: str = Field(description="ENABLED or DISABLED")


class ControlPoint(BaseModel):
    x: float
    y: float
    weight: float | None = None


class Trajectory(BaseModel):
    degree: int | None = None
    knotVector: list[float] | None = None
    controlPoints: list[ControlPoint] = Field(default_factory=list)


class PlannedPath(BaseModel):
    trajectory: Trajectory
    traversedNodes: list[str] = Field(default_factory=list)


class IntermediatePathPoint(BaseModel):
    x: float
    y: float
    theta: float | None = None
    eta: str = Field(description="ISO 8601 ETA")


class IntermediatePath(BaseModel):
    polyline: list[IntermediatePathPoint] = Field(default_factory=list)


class ZoneRequestType(str, Enum):
    ACCESS = "ACCESS"
    REPLANNING = "REPLANNING"


class RequestStatus(str, Enum):
    REQUESTED = "REQUESTED"
    GRANTED = "GRANTED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


class ZoneRequest(BaseModel):
    requestId: str
    requestType: ZoneRequestType
    zoneId: str
    zoneSetId: str
    requestStatus: RequestStatus
    trajectory: Trajectory | None = None


class EdgeRequest(BaseModel):
    requestId: str
    requestType: str = "CORRIDOR"
    edgeId: str
    sequenceId: int
    requestStatus: RequestStatus


class ActionParameter(BaseModel):
    key: str = Field(description="Parameter key")
    value: Any = Field(description="Parameter value")


class Action(BaseModel):
    """VDA5050 action — used in orders and instant actions."""

    actionId: str = Field(description="Unique action identifier")
    actionType: str = Field(description="Action type identifier")
    blockingType: BlockingType = Field(default=BlockingType.NONE)
    actionDescription: str | None = Field(default=None)
    actionParameters: list[ActionParameter] = Field(default_factory=list)


class NodeState(BaseModel):
    nodeId: str
    sequenceId: int
    released: bool = True
    nodeDescription: str | None = None
    nodePosition: AgvPosition | None = None


class EdgeState(BaseModel):
    edgeId: str
    sequenceId: int
    released: bool = True
    edgeDescription: str | None = None
    trajectory: Any | None = None


class ActionState(BaseModel):
    actionId: str
    actionType: str
    actionStatus: ActionStatus
    actionDescription: str | None = None
    resultDescription: str | None = None


class ErrorReference(BaseModel):
    referenceKey: str
    referenceValue: str


class Error(BaseModel):
    errorType: str
    errorLevel: ErrorLevel
    errorDescription: str | None = None
    errorHint: str | None = None
    errorReferences: list[ErrorReference] = Field(default_factory=list)


class Information(BaseModel):
    infoType: str
    infoLevel: InfoLevel = InfoLevel.INFO
    infoDescription: str | None = None
    infoReferences: list[ErrorReference] = Field(default_factory=list)


class Load(BaseModel):
    loadId: str | None = None
    loadType: str | None = None
    loadPosition: str | None = None
    boundingBoxReference: Any | None = None
    loadDimensions: Any | None = None
    weight: float | None = None

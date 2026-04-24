"""Shared VDA5050 header fields and common sub-models."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────────────────────────────


class OperatingMode(str, Enum):
    AUTOMATIC = "AUTOMATIC"
    SEMIAUTOMATIC = "SEMIAUTOMATIC"
    MANUAL = "MANUAL"
    SERVICE = "SERVICE"
    TEACHIN = "TEACHIN"


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
    FATAL = "FATAL"


class ActionStatus(str, Enum):
    WAITING = "WAITING"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class BlockingType(str, Enum):
    NONE = "NONE"
    SOFT = "SOFT"
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

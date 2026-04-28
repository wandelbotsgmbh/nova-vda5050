"""VDA5050 V3.0.0 Zone Set message."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ZoneType(str, Enum):
    BLOCKED = "BLOCKED"
    LINE_GUIDED = "LINE_GUIDED"
    RELEASE = "RELEASE"
    COORDINATED_REPLANNING = "COORDINATED_REPLANNING"
    SPEED_LIMIT = "SPEED_LIMIT"
    ACTION = "ACTION"
    PRIORITY = "PRIORITY"
    PENALTY = "PENALTY"
    DIRECTED = "DIRECTED"
    BIDIRECTED = "BIDIRECTED"


class DirectionLimitation(str, Enum):
    SOFT = "SOFT"
    RESTRICTED = "RESTRICTED"
    STRICT = "STRICT"


class ZoneVertex(BaseModel):
    x: float = Field(description="X-coordinate in meters (project coordinate system)")
    y: float = Field(description="Y-coordinate in meters (project coordinate system)")


class ZoneAction(BaseModel):
    """Action within a zone — subset of VDA5050 Action without actionId."""

    actionType: str = Field(description="Action type identifier")
    blockingType: str = Field(default="NONE", description="NONE | SOFT | SINGLE | HARD")
    actionDescriptor: str | None = Field(default=None)
    actionParameters: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Array of {key, value} parameter objects",
    )


class Zone(BaseModel):
    """A single VDA5050 zone within a zone set."""

    zoneId: str = Field(description="Locally unique zone identifier within the zone set")
    zoneType: ZoneType = Field(description="Zone category")
    zoneDescriptor: str | None = Field(default=None, description="Human-readable descriptor")
    vertices: list[ZoneVertex] = Field(
        min_length=3,
        description="Polygon vertices defining the zone shape",
    )

    # SPEED_LIMIT
    maximumSpeed: float | None = Field(default=None, description="Max speed in m/s (SPEED_LIMIT)")

    # ACTION
    entryActions: list[ZoneAction] | None = Field(
        default=None, description="Actions on zone entry (ACTION type)"
    )
    duringActions: list[ZoneAction] | None = Field(
        default=None, description="Actions while in zone (ACTION type)"
    )
    exitActions: list[ZoneAction] | None = Field(
        default=None, description="Actions on zone exit (ACTION type)"
    )

    # PRIORITY
    priorityFactor: float | None = Field(
        default=None, ge=0.0, le=1.0, description="0.0=no preference, 1.0=max (PRIORITY)"
    )

    # PENALTY
    penaltyFactor: float | None = Field(
        default=None, ge=0.0, le=1.0, description="0.0=no penalty, 1.0=max (PENALTY)"
    )

    # DIRECTED / BIDIRECTED
    direction: float | None = Field(
        default=None, description="Direction of travel in radians (DIRECTED/BIDIRECTED)"
    )
    limitation: DirectionLimitation | None = Field(
        default=None, description="SOFT | RESTRICTED | STRICT (DIRECTED/BIDIRECTED)"
    )


class ZoneSet(BaseModel):
    """A named set of zones for a specific map."""

    mapId: str = Field(description="Globally unique map identifier")
    zoneSetId: str = Field(description="Globally unique zone set identifier")
    zoneSetDescriptor: str | None = Field(default=None, description="Human-readable name")
    zones: list[Zone] = Field(default_factory=list, description="Array of zone objects")


class ZoneSetMessage(BaseModel):
    """VDA5050 V3.0.0 Zone Set message — sent by fleet control to a robot."""

    # Header
    headerId: int
    timestamp: str
    version: str = "3.0.0"
    manufacturer: str
    serialNumber: str

    # Payload
    zoneSet: ZoneSet

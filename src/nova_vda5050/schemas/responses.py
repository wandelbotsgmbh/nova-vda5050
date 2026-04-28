"""VDA5050 V3.0.0 Responses message."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class GrantType(str, Enum):
    GRANTED = "GRANTED"
    QUEUED = "QUEUED"
    REVOKED = "REVOKED"
    REJECTED = "REJECTED"


class Response(BaseModel):
    """A single response to a robot's zone/resource request."""

    requestId: str = Field(
        description="Unique identifier within all active requests for this robot"
    )
    grantType: GrantType = Field(description="GRANTED | QUEUED | REVOKED | REJECTED")
    leaseExpiry: str | None = Field(
        default=None, description="ISO 8601 timestamp for lease expiration"
    )


class ResponsesMessage(BaseModel):
    """VDA5050 V3.0.0 Responses message — sent by fleet control to a robot."""

    # Header
    headerId: int
    timestamp: str
    version: str = "3.0.0"
    manufacturer: str
    serialNumber: str

    # Payload
    responses: list[Response] = Field(
        default_factory=list,
        description="Array of response objects for the robot's requests",
    )

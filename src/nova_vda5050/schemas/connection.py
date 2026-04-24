"""VDA5050 V3.0.0 Connection message."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from nova_vda5050.schemas import ConnectionState


class ConnectionMessage(BaseModel):
    """VDA5050 V3.0.0 Connection message — online/offline heartbeat."""

    # Header
    headerId: int
    timestamp: str
    version: str = "3.0.0"
    manufacturer: str
    serialNumber: str

    # Connection
    connectionState: ConnectionState

    @classmethod
    def online(
        cls,
        header_id: int,
        manufacturer: str,
        serial_number: str,
        timestamp: str | None = None,
    ) -> ConnectionMessage:
        return cls(
            headerId=header_id,
            timestamp=timestamp or datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            manufacturer=manufacturer,
            serialNumber=serial_number,
            connectionState=ConnectionState.ONLINE,
        )

    @classmethod
    def offline(
        cls,
        header_id: int,
        manufacturer: str,
        serial_number: str,
        timestamp: str | None = None,
    ) -> ConnectionMessage:
        return cls(
            headerId=header_id,
            timestamp=timestamp or datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            manufacturer=manufacturer,
            serialNumber=serial_number,
            connectionState=ConnectionState.OFFLINE,
        )

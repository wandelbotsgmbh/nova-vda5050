"""VDA5050 connection message helpers for Nova KV online/offline events."""

from __future__ import annotations

from nova_vda5050.schemas.connection import ConnectionMessage
from nova_vda5050.manufacturers import get_manufacturer


_header_counters: dict[str, int] = {}


def _next_header_id(key: str) -> int:
    _header_counters[key] = _header_counters.get(key, 0) + 1
    return _header_counters[key]


def robot_online(robot_model: str, robot_id: str) -> ConnectionMessage:
    """Create an ONLINE connection message for a Nova robot."""
    manufacturer = get_manufacturer(robot_model)
    return ConnectionMessage.online(
        header_id=_next_header_id(f"conn.{robot_id}"),
        manufacturer=manufacturer,
        serial_number=robot_id,
    )


def robot_offline(robot_model: str, robot_id: str) -> ConnectionMessage:
    """Create an OFFLINE connection message for a Nova robot."""
    manufacturer = get_manufacturer(robot_model)
    return ConnectionMessage.offline(
        header_id=_next_header_id(f"conn.{robot_id}"),
        manufacturer=manufacturer,
        serial_number=robot_id,
    )

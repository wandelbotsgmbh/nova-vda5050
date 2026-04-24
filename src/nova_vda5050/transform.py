"""Transform Nova telemetry dicts to VDA5050 state messages."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from nova_vda5050.schemas import (
    AgvPosition,
    BatteryState,
    EStopState,
    Information,
    InfoLevel,
    OperatingMode,
    SafetyState,
    Velocity,
)
from nova_vda5050.schemas.state import StateMessage
from nova_vda5050.schemas.visualization import VisualizationMessage


def _parse_operating_mode(mode: str | None) -> OperatingMode:
    if mode is None:
        return OperatingMode.AUTOMATIC
    mode_map = {
        "automatic": OperatingMode.AUTOMATIC,
        "auto": OperatingMode.AUTOMATIC,
        "semiautomatic": OperatingMode.SEMIAUTOMATIC,
        "semi": OperatingMode.SEMIAUTOMATIC,
        "manual": OperatingMode.MANUAL,
        "service": OperatingMode.SERVICE,
        "teachin": OperatingMode.TEACHIN,
        "teach": OperatingMode.TEACHIN,
    }
    return mode_map.get(mode.lower(), OperatingMode.AUTOMATIC)


def transform_telemetry_to_state(
    nova_telemetry: dict[str, Any],
    robot_id: str,
    manufacturer: str,
    header_id: int,
) -> StateMessage:
    """Transform Nova telemetry data to a VDA5050 StateMessage.

    Handles partial data gracefully — missing fields get sensible defaults.
    """
    timestamp = nova_telemetry.get("timestamp") or datetime.now(timezone.utc).isoformat(
        timespec="milliseconds"
    )

    # Position
    pos = nova_telemetry.get("position", {})
    agv_position = AgvPosition(
        x=pos.get("x", 0.0),
        y=pos.get("y", 0.0),
        theta=pos.get("theta", 0.0),
        mapId=pos.get("map_id", "default"),
        positionInitialized=bool(pos),
    )

    # Velocity
    vel = nova_telemetry.get("velocity", {})
    velocity = Velocity(
        vx=vel.get("vx", 0.0),
        vy=vel.get("vy", 0.0),
        omega=vel.get("omega", vel.get("vyaw", 0.0)),
    )

    # Battery
    bat = nova_telemetry.get("battery", {})
    battery = BatteryState(
        batteryCharge=bat.get("percentage", bat.get("level", 0.0)),
        batteryVoltage=bat.get("voltage"),
        charging=bat.get("charging", False),
    )

    # Status
    status = nova_telemetry.get("status", {})
    operating_mode = _parse_operating_mode(status.get("operating_mode"))
    driving = status.get("driving", False)
    paused = status.get("paused", False)

    # Safety
    safety = nova_telemetry.get("safety", {})
    estop_str = safety.get("estop", "NONE")
    try:
        estop = EStopState(estop_str.upper())
    except ValueError:
        estop = EStopState.NONE
    safety_state = SafetyState(
        eStop=estop,
        fieldViolation=safety.get("field_violation", False),
    )

    # Order info
    order = nova_telemetry.get("order", {})
    informations: list[Information] = []
    order_id = order.get("order_id", "")
    completion = order.get("completion_percentage")
    if order_id and completion is not None:
        informations.append(
            Information(
                infoType="orderProgress",
                infoLevel=InfoLevel.INFO,
                infoDescription=f"Order {completion:.0f}% complete",
            )
        )

    return StateMessage(
        headerId=header_id,
        timestamp=timestamp,
        version="3.0.0",
        manufacturer=manufacturer,
        serialNumber=robot_id,
        orderId=order_id,
        orderUpdateId=order.get("order_update_id", 0),
        lastNodeId=order.get("last_node_id", ""),
        lastNodeSequenceId=order.get("last_node_sequence_id", 0),
        driving=driving,
        paused=paused,
        newBaseRequest=False,
        agvPosition=agv_position,
        velocity=velocity,
        batteryState=battery,
        operatingMode=operating_mode,
        safetyState=safety_state,
        informations=informations,
    )


def transform_telemetry_to_visualization(
    nova_telemetry: dict[str, Any],
    robot_id: str,
    manufacturer: str,
    header_id: int,
) -> VisualizationMessage:
    """Transform Nova telemetry to a lightweight VDA5050 Visualization message."""
    timestamp = nova_telemetry.get("timestamp") or datetime.now(timezone.utc).isoformat(
        timespec="milliseconds"
    )

    pos = nova_telemetry.get("position", {})
    vel = nova_telemetry.get("velocity", {})
    status = nova_telemetry.get("status", {})

    return VisualizationMessage(
        headerId=header_id,
        timestamp=timestamp,
        manufacturer=manufacturer,
        serialNumber=robot_id,
        agvPosition=AgvPosition(
            x=pos.get("x", 0.0),
            y=pos.get("y", 0.0),
            theta=pos.get("theta", 0.0),
            mapId=pos.get("map_id", "default"),
            positionInitialized=bool(pos),
        ),
        velocity=Velocity(
            vx=vel.get("vx", 0.0),
            vy=vel.get("vy", 0.0),
            omega=vel.get("omega", vel.get("vyaw", 0.0)),
        ),
        driving=status.get("driving", False),
        paused=status.get("paused", False),
    )

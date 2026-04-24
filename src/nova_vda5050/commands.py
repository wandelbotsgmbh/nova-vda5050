"""Translate VDA5050 order/instantActions to Nova control commands."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from nova_vda5050.schemas.order import OrderMessage, Node
from nova_vda5050.schemas.instant_actions import InstantActionsMessage
from nova_vda5050.schemas import Action


def translate_instant_action_to_nova(action: Action) -> dict[str, Any] | None:
    """Translate a single VDA5050 instant action to a Nova control command.

    Returns a dict suitable for publishing to rt.v1.robot.{model}.{id}.control.cmd,
    or None if the action type is not recognized.
    """
    now = datetime.now(timezone.utc).isoformat()

    # Map VDA5050 action types to Nova command types
    action_type = action.actionType.lower()

    if action_type in ("stopdrive", "stop"):
        return {
            "type": "stop",
            "client_id": f"vda5050-{action.actionId}",
            "seq": 0,
            "timestamp": now,
        }

    if action_type in ("startcharging", "enable", "startpause"):
        nova_type = {
            "startcharging": "enable",
            "enable": "enable",
            "startpause": "stop",
        }[action_type]
        return {
            "type": nova_type,
            "client_id": f"vda5050-{action.actionId}",
            "seq": 0,
            "timestamp": now,
        }

    if action_type in ("cancelorder", "estop"):
        return {
            "type": "estop",
            "client_id": f"vda5050-{action.actionId}",
            "seq": 0,
            "timestamp": now,
        }

    # Unknown action type — let the connector decide
    return {
        "type": action_type,
        "client_id": f"vda5050-{action.actionId}",
        "seq": 0,
        "timestamp": now,
        "action_parameters": {p.key: p.value for p in action.actionParameters},
    }


def translate_instant_actions_to_nova(
    msg: InstantActionsMessage,
) -> list[dict[str, Any]]:
    """Translate all actions in an InstantActionsMessage to Nova commands."""
    results = []
    for action in msg.actions:
        cmd = translate_instant_action_to_nova(action)
        if cmd is not None:
            results.append(cmd)
    return results


def translate_order_to_nova(order: OrderMessage) -> list[dict[str, Any]]:
    """Translate a VDA5050 order to a sequence of Nova navigation commands.

    Each node with a position becomes a navigation waypoint command.
    """
    commands: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc).isoformat()

    for node in order.nodes:
        if node.nodePosition is None:
            continue

        # Create a navigate-to-waypoint command
        cmd: dict[str, Any] = {
            "type": "navigate",
            "client_id": f"vda5050-order-{order.orderId}",
            "seq": node.sequenceId,
            "timestamp": now,
            "target": {
                "x": node.nodePosition.x,
                "y": node.nodePosition.y,
                "theta": node.nodePosition.theta,
                "map_id": node.nodePosition.mapId,
            },
            "order_id": order.orderId,
            "node_id": node.nodeId,
        }
        commands.append(cmd)

        # Add any actions attached to this node
        for action in node.actions:
            action_cmd = translate_instant_action_to_nova(action)
            if action_cmd:
                action_cmd["order_id"] = order.orderId
                action_cmd["node_id"] = node.nodeId
                commands.append(action_cmd)

    return commands

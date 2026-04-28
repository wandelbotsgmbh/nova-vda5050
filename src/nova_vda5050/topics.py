"""Bidirectional NATS <-> VDA5050 MQTT topic mapper."""

from __future__ import annotations

from dataclasses import dataclass
from nova_vda5050.manufacturers import get_manufacturer


VDA5050_TOPIC_PREFIX = "vda5050/v3"
VDA5050_NATS_PREFIX = "vda5050.v3"

# VDA5050 message types
MESSAGE_TYPES = (
    "state",
    "visualization",
    "connection",
    "order",
    "instantActions",
    "factsheet",
    "zoneSet",
    "responses",
)

# Inbound = FMS -> Robot (order, instantActions, zoneSet, responses)
INBOUND_TYPES = {"order", "instantActions", "zoneSet", "responses"}
# Outbound = Robot -> FMS (state, visualization, connection, factsheet)
OUTBOUND_TYPES = {"state", "visualization", "connection", "factsheet"}


@dataclass(frozen=True)
class VDA5050Address:
    """Parsed VDA5050 topic address."""

    manufacturer: str
    serial_number: str
    message_type: str

    @property
    def mqtt_topic(self) -> str:
        return (
            f"{VDA5050_TOPIC_PREFIX}/{self.manufacturer}/{self.serial_number}/{self.message_type}"
        )

    @property
    def nats_subject(self) -> str:
        return f"{VDA5050_NATS_PREFIX}.{self.manufacturer}.{self.serial_number}.{self.message_type}"


@dataclass(frozen=True)
class NovaAddress:
    """Parsed Nova NATS subject address."""

    robot_model: str
    robot_id: str
    category: str  # "telemetry", "control", "graphnav"
    subcategory: str  # "state", "cmd", "evt", etc.


class TopicMapper:
    """Maps between Nova NATS subjects and VDA5050 topics.

    Nova format:  {prefix}.robot.{model}.{id}.telemetry.state
    VDA5050 format: vda5050.v3.{manufacturer}.{serial}.state
    """

    def __init__(self, nova_prefix: str = "rt.v1"):
        self.nova_prefix = nova_prefix.strip(".")

    # ── Nova -> VDA5050 ──────────────────────────────────────────────────

    def nova_to_vda5050(self, robot_model: str, robot_id: str, message_type: str) -> VDA5050Address:
        """Build a VDA5050 address from Nova robot identity."""
        manufacturer = get_manufacturer(robot_model)
        return VDA5050Address(
            manufacturer=manufacturer,
            serial_number=robot_id,
            message_type=message_type,
        )

    def nova_state_to_vda5050_nats(self, robot_model: str, robot_id: str) -> str:
        """Return the NATS subject for publishing VDA5050 state."""
        return self.nova_to_vda5050(robot_model, robot_id, "state").nats_subject

    def nova_state_to_vda5050_visualization_nats(self, robot_model: str, robot_id: str) -> str:
        return self.nova_to_vda5050(robot_model, robot_id, "visualization").nats_subject

    def nova_connection_nats(self, robot_model: str, robot_id: str) -> str:
        return self.nova_to_vda5050(robot_model, robot_id, "connection").nats_subject

    def nova_factsheet_nats(self, robot_model: str, robot_id: str) -> str:
        """Return the NATS subject for publishing VDA5050 factsheet."""
        return self.nova_to_vda5050(robot_model, robot_id, "factsheet").nats_subject

    # ── VDA5050 -> Nova ──────────────────────────────────────────────────

    def parse_vda5050_nats_subject(self, subject: str) -> VDA5050Address | None:
        """Parse a NATS subject in VDA5050 format."""
        if not subject.startswith(VDA5050_NATS_PREFIX + "."):
            return None
        rest = subject[len(VDA5050_NATS_PREFIX) + 1 :]
        parts = rest.split(".", 2)
        if len(parts) != 3:
            return None
        manufacturer, serial, msg_type = parts
        if msg_type not in MESSAGE_TYPES:
            return None
        return VDA5050Address(
            manufacturer=manufacturer,
            serial_number=serial,
            message_type=msg_type,
        )

    def parse_nova_subject(self, subject: str) -> NovaAddress | None:
        """Parse a Nova NATS subject."""
        prefix = self.nova_prefix + ".robot."
        if not subject.startswith(prefix):
            return None
        rest = subject[len(prefix) :]
        parts = rest.split(".")
        if len(parts) < 4:
            return None
        return NovaAddress(
            robot_model=parts[0],
            robot_id=parts[1],
            category=parts[2],
            subcategory=parts[3],
        )

    # ── Subscribe subjects ───────────────────────────────────────────────

    def vda5050_order_subscribe(self, manufacturer: str, serial: str) -> str:
        """NATS subject to subscribe for VDA5050 orders for a specific robot."""
        return f"{VDA5050_NATS_PREFIX}.{manufacturer}.{serial}.order"

    def vda5050_instant_actions_subscribe(self, manufacturer: str, serial: str) -> str:
        return f"{VDA5050_NATS_PREFIX}.{manufacturer}.{serial}.instantActions"

    def vda5050_zone_set_subject(self, manufacturer: str, serial: str) -> str:
        """NATS subject for publishing VDA5050 zone set to a robot."""
        return f"{VDA5050_NATS_PREFIX}.{manufacturer}.{serial}.zoneSet"

    def vda5050_responses_subject(self, manufacturer: str, serial: str) -> str:
        """NATS subject for publishing VDA5050 responses to a robot."""
        return f"{VDA5050_NATS_PREFIX}.{manufacturer}.{serial}.responses"

    def vda5050_inbound_wildcard(self) -> str:
        """Wildcard subject to receive all VDA5050 inbound messages."""
        return f"{VDA5050_NATS_PREFIX}.*.*.>"

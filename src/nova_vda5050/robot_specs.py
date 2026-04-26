"""Centralized robot specification registry and factsheet builder.

Physical constants sourced from public datasheets. Footprint polygons are
simple rectangles derived from length/width, centred on the robot origin.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from nova_vda5050.manufacturers import get_manufacturer
from nova_vda5050.schemas.factsheet import (
    ActionParameterDefinition,
    Envelope2d,
    FactsheetMessage,
    LoadSpecification,
    MaximumArrayLengths,
    MaximumStringLengths,
    MobileRobotActionDef,
    MobileRobotGeometry,
    PhysicalParameters,
    ProtocolFeatures,
    ProtocolLimits,
    Timing,
    TypeSpecification,
    Vertex2d,
)


# ── Robot specifications ─────────────────────────────────────────────────────
# Keys match the robot model strings used by Nova connectors.
# All dimensions in metres, speeds in m/s, accelerations in m/s².

ROBOT_SPECS: dict[str, dict[str, Any]] = {
    "spot": {
        "seriesName": "Spot",
        "seriesDescription": "Boston Dynamics Spot quadruped robot",
        "mobileRobotKinematics": "OMNIDIRECTIONAL",
        "mobileRobotClass": "CARRIER",
        "maximumLoadMass": 14.0,
        "localizationTypes": ["NATURAL", "SPOT"],
        "navigationTypes": ["FREELY_NAVIGATING"],
        "minimumSpeed": 0.0,
        "maximumSpeed": 1.6,
        "minimumAngularSpeed": 0.0,
        "maximumAngularSpeed": 1.5,
        "maximumAcceleration": 2.0,
        "maximumDeceleration": 2.0,
        "length": 1.1,
        "width": 0.5,
        "minimumHeight": 0.19,
        "maximumHeight": 0.61,
    },
    "g1": {
        "seriesName": "G1",
        "seriesDescription": "Unitree G1 humanoid robot",
        "mobileRobotKinematics": "OMNIDIRECTIONAL",
        "mobileRobotClass": "CARRIER",
        "maximumLoadMass": 3.0,
        "localizationTypes": ["NATURAL"],
        "navigationTypes": ["FREELY_NAVIGATING"],
        "minimumSpeed": 0.0,
        "maximumSpeed": 2.0,
        "minimumAngularSpeed": 0.0,
        "maximumAngularSpeed": 2.0,
        "maximumAcceleration": 1.5,
        "maximumDeceleration": 1.5,
        "length": 0.45,
        "width": 0.35,
        "minimumHeight": 0.7,
        "maximumHeight": 1.32,
    },
    "go2": {
        "seriesName": "Go2",
        "seriesDescription": "Unitree Go2 quadruped robot",
        "mobileRobotKinematics": "OMNIDIRECTIONAL",
        "mobileRobotClass": "CARRIER",
        "maximumLoadMass": 8.0,
        "localizationTypes": ["NATURAL"],
        "navigationTypes": ["FREELY_NAVIGATING"],
        "minimumSpeed": 0.0,
        "maximumSpeed": 3.5,
        "minimumAngularSpeed": 0.0,
        "maximumAngularSpeed": 2.5,
        "maximumAcceleration": 2.0,
        "maximumDeceleration": 2.0,
        "length": 0.70,
        "width": 0.31,
        "minimumHeight": 0.20,
        "maximumHeight": 0.40,
    },
    "b2": {
        "seriesName": "B2",
        "seriesDescription": "Unitree B2 industrial quadruped robot",
        "mobileRobotKinematics": "OMNIDIRECTIONAL",
        "mobileRobotClass": "CARRIER",
        "maximumLoadMass": 40.0,
        "localizationTypes": ["NATURAL"],
        "navigationTypes": ["FREELY_NAVIGATING"],
        "minimumSpeed": 0.0,
        "maximumSpeed": 3.0,
        "minimumAngularSpeed": 0.0,
        "maximumAngularSpeed": 2.0,
        "maximumAcceleration": 2.0,
        "maximumDeceleration": 2.0,
        "length": 1.0,
        "width": 0.48,
        "minimumHeight": 0.30,
        "maximumHeight": 0.53,
    },
    "h1": {
        "seriesName": "H1",
        "seriesDescription": "Unitree H1 humanoid robot",
        "mobileRobotKinematics": "OMNIDIRECTIONAL",
        "mobileRobotClass": "CARRIER",
        "maximumLoadMass": 30.0,
        "localizationTypes": ["NATURAL"],
        "navigationTypes": ["FREELY_NAVIGATING"],
        "minimumSpeed": 0.0,
        "maximumSpeed": 3.3,
        "minimumAngularSpeed": 0.0,
        "maximumAngularSpeed": 2.0,
        "maximumAcceleration": 2.0,
        "maximumDeceleration": 2.0,
        "length": 0.45,
        "width": 0.40,
        "minimumHeight": 1.0,
        "maximumHeight": 1.80,
    },
    "ur5e": {
        "seriesName": "UR5e",
        "seriesDescription": "Universal Robots UR5e collaborative arm (simulated)",
        "mobileRobotKinematics": "DIFFERENTIAL",
        "mobileRobotClass": "CARRIER",
        "maximumLoadMass": 5.0,
        "localizationTypes": ["NATURAL"],
        "navigationTypes": ["VIRTUAL_LINE_GUIDED"],
        "minimumSpeed": 0.0,
        "maximumSpeed": 0.0,
        "maximumAcceleration": 0.0,
        "maximumDeceleration": 0.0,
        "length": 0.4,
        "width": 0.4,
        "minimumHeight": 0.0,
        "maximumHeight": 0.9,
    },
    "tiago": {
        "seriesName": "TIAGo",
        "seriesDescription": "PAL Robotics TIAGo mobile manipulator (simulated)",
        "mobileRobotKinematics": "DIFFERENTIAL",
        "mobileRobotClass": "CARRIER",
        "maximumLoadMass": 5.0,
        "localizationTypes": ["NATURAL"],
        "navigationTypes": ["FREELY_NAVIGATING"],
        "minimumSpeed": 0.0,
        "maximumSpeed": 1.0,
        "minimumAngularSpeed": 0.0,
        "maximumAngularSpeed": 1.5,
        "maximumAcceleration": 1.0,
        "maximumDeceleration": 1.0,
        "length": 0.54,
        "width": 0.54,
        "minimumHeight": 1.10,
        "maximumHeight": 1.10,
    },
    "pidog": {
        "seriesName": "PiDog",
        "seriesDescription": "SunFounder PiDog robot dog on Raspberry Pi",
        "mobileRobotKinematics": "DIFFERENTIAL",
        "mobileRobotClass": "CARRIER",
        "maximumLoadMass": 0.0,
        "localizationTypes": ["NATURAL"],
        "navigationTypes": ["FREELY_NAVIGATING"],
        "minimumSpeed": 0.0,
        "maximumSpeed": 0.3,
        "minimumAngularSpeed": 0.0,
        "maximumAngularSpeed": 1.0,
        "maximumAcceleration": 0.5,
        "maximumDeceleration": 0.5,
        "length": 0.20,
        "width": 0.12,
        "minimumHeight": 0.08,
        "maximumHeight": 0.15,
    },
}


# ── Helpers ──────────────────────────────────────────────────────────────────


def _rect_footprint(length: float, width: float) -> list[Vertex2d]:
    """Return rectangular 2D envelope centred on origin."""
    hl, hw = length / 2, width / 2
    return [
        Vertex2d(x=hl, y=hw),
        Vertex2d(x=hl, y=-hw),
        Vertex2d(x=-hl, y=-hw),
        Vertex2d(x=-hl, y=hw),
    ]


_header_counters: dict[str, int] = {}


def _next_header_id(key: str) -> int:
    _header_counters[key] = _header_counters.get(key, 0) + 1
    return _header_counters[key]


def build_factsheet(
    robot_model: str,
    robot_id: str,
    supported_actions: list[MobileRobotActionDef] | None = None,
    *,
    simulated: bool = False,
    overrides: dict[str, Any] | None = None,
) -> FactsheetMessage:
    """Build a complete VDA5050 factsheet from the robot spec registry.

    Args:
        robot_model: Nova robot model key (e.g. "spot", "g1", "pidog").
        robot_id: Serial number / robot ID.
        supported_actions: List of action definitions. If ``None`` a minimal
            set (stop, enable, disable) is generated.
        overrides: Dict of spec key overrides merged on top of the registry
            defaults (useful for runtime-specific values).

    Returns:
        A fully populated ``FactsheetMessage`` ready for serialization.
    """
    spec = dict(ROBOT_SPECS.get(robot_model, {}))
    if overrides:
        spec.update(overrides)

    manufacturer = get_manufacturer(robot_model)
    header_id = _next_header_id(f"factsheet.{robot_id}")

    length = spec.get("length", 0.5)
    width = spec.get("width", 0.5)

    if supported_actions is None:
        supported_actions = [
            MobileRobotActionDef(
                actionType="stop",
                actionDescription="Emergency stop",
                actionScopes=["INSTANT"],
                blockingTypes=["HARD"],
                pauseAllowed="false",
                cancelAllowed="false",
            ),
            MobileRobotActionDef(
                actionType="enable",
                actionDescription="Enable robot",
                actionScopes=["INSTANT"],
                blockingTypes=["NONE"],
            ),
            MobileRobotActionDef(
                actionType="disable",
                actionDescription="Disable robot",
                actionScopes=["INSTANT"],
                blockingTypes=["HARD"],
            ),
        ]

    return FactsheetMessage(
        headerId=header_id,
        timestamp=datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        manufacturer=manufacturer,
        serialNumber=robot_id,
        typeSpecification=TypeSpecification(
            seriesName=spec.get("seriesName", robot_model),
            seriesDescription=spec.get("seriesDescription"),
            mobileRobotKinematics=spec.get("mobileRobotKinematics"),
            mobileRobotClass=spec.get("mobileRobotClass"),
            maximumLoadMass=spec.get("maximumLoadMass", 0.0),
            localizationTypes=spec.get("localizationTypes", []),
            navigationTypes=spec.get("navigationTypes", []),
        ),
        physicalParameters=PhysicalParameters(
            minimumSpeed=spec.get("minimumSpeed", 0.0),
            maximumSpeed=spec.get("maximumSpeed", 0.0),
            minimumAngularSpeed=spec.get("minimumAngularSpeed"),
            maximumAngularSpeed=spec.get("maximumAngularSpeed"),
            maximumAcceleration=spec.get("maximumAcceleration", 0.0),
            maximumDeceleration=spec.get("maximumDeceleration", 0.0),
            minimumHeight=spec.get("minimumHeight", 0.0),
            maximumHeight=spec.get("maximumHeight", 0.0),
            width=width,
            length=length,
        ),
        protocolLimits=ProtocolLimits(
            maximumStringLengths=MaximumStringLengths(
                maximumIdLength=256,
                maximumTopicSerialLength=256,
                maximumTopicElementLength=256,
            ),
            maximumArrayLengths=MaximumArrayLengths(
                instantActions=10,
            ),
            timing=Timing(
                minimumOrderInterval=0.5,
                minimumStateInterval=0.5,
                defaultStateInterval=1.0,
                visualizationInterval=0.2,
            ),
        ),
        protocolFeatures=ProtocolFeatures(
            mobileRobotActions=supported_actions,
        ),
        mobileRobotGeometry=MobileRobotGeometry(
            envelopes2d=[
                Envelope2d(
                    envelope2dId="footprint",
                    description=f"Rectangular footprint {length}m x {width}m",
                    vertices=_rect_footprint(length, width),
                ),
            ],
        ),
        loadSpecification=LoadSpecification(),
        nova={"simulated": simulated},
    )


def action_def(
    action_type: str,
    description: str = "",
    scopes: list[str] | None = None,
    blocking: list[str] | None = None,
    parameters: list[ActionParameterDefinition] | None = None,
    pause_allowed: str = "false",
    cancel_allowed: str = "true",
) -> MobileRobotActionDef:
    """Convenience builder for a single action definition."""
    return MobileRobotActionDef(
        actionType=action_type,
        actionDescription=description or None,
        actionScopes=scopes or ["INSTANT"],
        blockingTypes=blocking or ["NONE"],
        actionParameters=parameters or [],
        pauseAllowed=pause_allowed,
        cancelAllowed=cancel_allowed,
    )

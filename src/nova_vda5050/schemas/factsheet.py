"""VDA5050 V3.0.0 Factsheet message model.

The factsheet provides basic information about a specific mobile robot type
series, including physical parameters, protocol capabilities, supported
actions, geometry, and load specifications.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from nova_vda5050.schemas import Header


# ── Type specification ───────────────────────────────────────────────────────


class TypeSpecification(BaseModel):
    """General class and capabilities of the mobile robot."""

    seriesName: str = Field(description="Generalized series name")
    seriesDescription: str | None = Field(default=None)
    mobileRobotKinematics: str | None = Field(
        default=None,
        description="DIFFERENTIAL, OMNIDIRECTIONAL, THREE_WHEEL, etc.",
    )
    mobileRobotClass: str | None = Field(
        default=None,
        description="FORKLIFT, CONVEYOR, TUGGER, CARRIER, etc.",
    )
    maximumLoadMass: float = Field(default=0.0, ge=0, description="kg")
    localizationTypes: list[str] = Field(
        default_factory=list,
        description="NATURAL, REFLECTOR, RFID, DMC, SPOT, GRID, GPS",
    )
    navigationTypes: list[str] = Field(
        default_factory=list,
        description="PHYSICAL_LINE_GUIDED, VIRTUAL_LINE_GUIDED, FREELY_NAVIGATING",
    )
    supportedZones: list[str] = Field(default_factory=list)


# ── Physical parameters ─────────────────────────────────────────────────────


class PhysicalParameters(BaseModel):
    """Basic physical properties of the mobile robot."""

    minimumSpeed: float = Field(default=0.0, ge=0, description="m/s")
    maximumSpeed: float = Field(default=0.0, ge=0, description="m/s")
    minimumAngularSpeed: float | None = Field(default=None, ge=0, description="rad/s")
    maximumAngularSpeed: float | None = Field(default=None, ge=0, description="rad/s")
    maximumAcceleration: float = Field(default=0.0, ge=0, description="m/s^2")
    maximumDeceleration: float = Field(default=0.0, description="m/s^2")
    minimumHeight: float = Field(default=0.0, description="m")
    maximumHeight: float = Field(default=0.0, description="m")
    width: float = Field(default=0.0, description="m")
    length: float = Field(default=0.0, description="m")


# ── Protocol limits ──────────────────────────────────────────────────────────


class MaximumStringLengths(BaseModel):
    maximumMessageLength: int | None = Field(default=None, ge=0)
    maximumTopicSerialLength: int | None = Field(default=None, ge=0)
    maximumTopicElementLength: int | None = Field(default=None, ge=0)
    maximumIdLength: int | None = Field(default=None, ge=0)
    idNumericalOnly: bool | None = Field(default=None)
    maximumLoadIdLength: int | None = Field(default=None, ge=0)


class MaximumArrayLengths(BaseModel):
    order_nodes: int | None = Field(default=None, ge=0, alias="order.nodes")
    order_edges: int | None = Field(default=None, ge=0, alias="order.edges")
    node_actions: int | None = Field(default=None, ge=0, alias="node.actions")
    edge_actions: int | None = Field(default=None, ge=0, alias="edge.actions")
    actions_actionsParameters: int | None = Field(
        default=None, ge=0, alias="actions.actionsParameters"
    )
    instantActions: int | None = Field(default=None, ge=0)
    trajectory_knotVector: int | None = Field(default=None, ge=0, alias="trajectory.knotVector")
    trajectory_controlPoints: int | None = Field(
        default=None, ge=0, alias="trajectory.controlPoints"
    )
    zoneSet_zones: int | None = Field(default=None, ge=0, alias="zoneSet.zones")
    state_nodeStates: int | None = Field(default=None, ge=0, alias="state.nodeStates")
    state_edgeStates: int | None = Field(default=None, ge=0, alias="state.edgeStates")
    state_loads: int | None = Field(default=None, ge=0, alias="state.loads")
    state_actionStates: int | None = Field(default=None, ge=0, alias="state.actionStates")
    state_instantActionStates: int | None = Field(
        default=None, ge=0, alias="state.instantActionStates"
    )
    state_zoneActionStates: int | None = Field(default=None, ge=0, alias="state.zoneActionStates")
    state_errors: int | None = Field(default=None, ge=0, alias="state.errors")
    state_information: int | None = Field(default=None, ge=0, alias="state.information")
    error_errorReferences: int | None = Field(default=None, ge=0, alias="error.errorReferences")
    information_infoReferences: int | None = Field(
        default=None, ge=0, alias="information.infoReferences"
    )

    model_config = {"populate_by_name": True}


class Timing(BaseModel):
    minimumOrderInterval: float = Field(default=0.0, ge=0, description="s")
    minimumStateInterval: float = Field(default=0.0, ge=0, description="s")
    defaultStateInterval: float | None = Field(default=None, ge=0, description="s")
    visualizationInterval: float | None = Field(default=None, ge=0, description="s")


class ProtocolLimits(BaseModel):
    maximumStringLengths: MaximumStringLengths = Field(default_factory=MaximumStringLengths)
    maximumArrayLengths: MaximumArrayLengths = Field(default_factory=MaximumArrayLengths)
    timing: Timing = Field(default_factory=Timing)


# ── Protocol features ────────────────────────────────────────────────────────


class OptionalParameter(BaseModel):
    parameter: str = Field(description="Full dotted parameter name")
    support: str = Field(description="SUPPORTED or REQUIRED")
    description: str | None = Field(default=None)


class ActionParameterDefinition(BaseModel):
    """Definition of an action parameter in the factsheet."""

    key: str
    valueDataType: str = Field(description="BOOL, NUMBER, INTEGER, STRING, OBJECT, ARRAY")
    description: str | None = Field(default=None)
    isOptional: bool | None = Field(default=None)


class MobileRobotActionDef(BaseModel):
    """Definition of a supported action in the factsheet."""

    actionType: str
    actionDescription: str | None = Field(default=None)
    actionScopes: list[str] = Field(
        default_factory=list,
        description="INSTANT, NODE, EDGE, ZONE",
    )
    actionParameters: list[ActionParameterDefinition] = Field(default_factory=list)
    actionResult: str | None = Field(default=None)
    blockingTypes: list[str] = Field(default_factory=list)
    pauseAllowed: str = Field(default="false")
    cancelAllowed: str = Field(default="true")


class ProtocolFeatures(BaseModel):
    optionalParameters: list[OptionalParameter] = Field(default_factory=list)
    mobileRobotActions: list[MobileRobotActionDef] = Field(default_factory=list)


# ── Mobile robot geometry ────────────────────────────────────────────────────


class WheelPosition(BaseModel):
    x: float
    y: float
    theta: float | None = None


class WheelDefinition(BaseModel):
    type: str = Field(description="DRIVE, CASTER, FIXED, MECANUM")
    isActiveDriven: bool = False
    isActiveSteered: bool = False
    position: WheelPosition = Field(default_factory=WheelPosition)
    diameter: float = 0.0
    width: float = 0.0
    centerDisplacement: float | None = None
    constraints: str | None = None


class Vertex2d(BaseModel):
    x: float
    y: float


class Envelope2d(BaseModel):
    envelope2dId: str
    vertices: list[Vertex2d] = Field(default_factory=list)
    description: str | None = None


class Envelope3d(BaseModel):
    envelope3dId: str
    format: str = ""
    data: Any | None = None
    url: str | None = None
    description: str | None = None


class MobileRobotGeometry(BaseModel):
    wheelDefinitions: list[WheelDefinition] = Field(default_factory=list)
    envelopes2d: list[Envelope2d] = Field(default_factory=list)
    envelopes3d: list[Envelope3d] = Field(default_factory=list)


# ── Load specification ───────────────────────────────────────────────────────


class BoundingBoxReference(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    theta: float | None = None


class LoadDimensions(BaseModel):
    length: float = 0.0
    width: float = 0.0
    height: float | None = None


class LoadSet(BaseModel):
    setName: str
    loadType: str
    loadPositions: list[str] = Field(default_factory=list)
    boundingBoxReference: BoundingBoxReference | None = None
    loadDimensions: LoadDimensions | None = None
    maximumWeight: float | None = Field(default=None, ge=0)
    minimumLoadhandlingHeight: float | None = Field(default=None, ge=0)
    maximumLoadhandlingHeight: float | None = Field(default=None, ge=0)
    minimumLoadhandlingDepth: float | None = None
    maximumLoadhandlingDepth: float | None = None
    minimumLoadhandlingTilt: float | None = None
    maximumLoadhandlingTilt: float | None = None
    maximumSpeed: float | None = Field(default=None, ge=0)
    maximumAcceleration: float | None = Field(default=None, ge=0)
    maximumDeceleration: float | None = None
    pickTime: float | None = Field(default=None, ge=0)
    dropTime: float | None = Field(default=None, ge=0)
    description: str | None = None


class LoadSpecification(BaseModel):
    loadPositions: list[str] = Field(default_factory=list)
    loadSets: list[LoadSet] = Field(default_factory=list)


# ── Mobile robot configuration ───────────────────────────────────────────────


class VersionEntry(BaseModel):
    key: str
    value: str


class NetworkConfig(BaseModel):
    dnsServers: list[str] = Field(default_factory=list)
    ntpServers: list[str] = Field(default_factory=list)
    localIpAddress: str | None = None
    netmask: str | None = None
    defaultGateway: str | None = None


class BatteryCharging(BaseModel):
    criticalLowChargingLevel: float | None = Field(default=None, ge=0, le=100)
    minimumDesiredChargingLevel: float | None = Field(default=None, ge=0, le=100)
    maximumDesiredChargingLevel: float | None = Field(default=None, ge=0, le=100)
    minimumChargingTime: float | None = Field(default=None, ge=0, description="s")


class MobileRobotConfiguration(BaseModel):
    versions: list[VersionEntry] = Field(default_factory=list)
    network: NetworkConfig | None = None
    batteryCharging: BatteryCharging | None = None


# ── Top-level factsheet message ──────────────────────────────────────────────


class FactsheetMessage(Header):
    """VDA5050 V3.0.0 factsheet message — full robot self-description."""

    typeSpecification: TypeSpecification = Field(default_factory=TypeSpecification)
    physicalParameters: PhysicalParameters = Field(default_factory=PhysicalParameters)
    protocolLimits: ProtocolLimits = Field(default_factory=ProtocolLimits)
    protocolFeatures: ProtocolFeatures = Field(default_factory=ProtocolFeatures)
    mobileRobotGeometry: MobileRobotGeometry = Field(default_factory=MobileRobotGeometry)
    loadSpecification: LoadSpecification = Field(default_factory=LoadSpecification)
    mobileRobotConfiguration: MobileRobotConfiguration | None = Field(default=None)

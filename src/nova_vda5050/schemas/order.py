"""VDA5050 V3.0.0 Order message."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from nova_vda5050.schemas import Action, AgvPosition


class NodePosition(BaseModel):
    x: float
    y: float
    theta: float | None = None
    mapId: str = "default"
    allowedDeviationXY: float | None = None
    allowedDeviationTheta: float | None = None


class Node(BaseModel):
    nodeId: str
    sequenceId: int
    released: bool = True
    nodePosition: NodePosition | None = None
    nodeDescription: str | None = None
    actions: list[Action] = Field(default_factory=list)


class Edge(BaseModel):
    edgeId: str
    sequenceId: int
    released: bool = True
    startNodeId: str = ""
    endNodeId: str = ""
    edgeDescription: str | None = None
    maxSpeed: float | None = None
    maxHeight: float | None = None
    minHeight: float | None = None
    orientation: float | None = None
    direction: str | None = None
    rotationAllowed: bool | None = None
    maxRotationSpeed: float | None = None
    length: float | None = None
    trajectory: Any | None = None
    actions: list[Action] = Field(default_factory=list)


class OrderMessage(BaseModel):
    """VDA5050 V3.0.0 Order message — sent by fleet control to a robot."""

    # Header
    headerId: int
    timestamp: str
    version: str = "3.0.0"
    manufacturer: str
    serialNumber: str

    # Order
    orderId: str
    orderUpdateId: int = 0
    zoneSetId: str | None = None

    # Graph
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)

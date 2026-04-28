# nova-vda5050

VDA5050 V3.0.0 Python library for the Wandelbots Nova platform.

## Features

- **Pydantic models** for all VDA5050 V3.0.0 message types:
  - `StateMessage` — robot state with V3 fields (`mobileRobotPosition`, `powerSupply`, `instantActionStates`, `zoneRequests`, `edgeRequests`, `plannedPath`, `intermediatePath`, `maps`, `zoneSets`). V2 compat fields (`agvPosition`, `batteryState`) retained.
  - `OrderMessage` — orders with nodes, edges, zoneSetId
  - `InstantActionsMessage` — instant action dispatch
  - `ConnectionMessage` — online/offline/broken
  - `VisualizationMessage` — high-rate position with V3 `plannedPath`, `intermediatePath`, `referenceStateHeaderId`
  - `FactsheetMessage` — robot capabilities, physical specs, supported actions
  - `ZoneSetMessage` — zone sets with all 10 VDA5050 zone types (BLOCKED, LINE_GUIDED, RELEASE, COORDINATED_REPLANNING, SPEED_LIMIT, ACTION, PRIORITY, PENALTY, DIRECTED, BIDIRECTED)
  - `ResponsesMessage` — fleet control responses to robot zone/edge requests (GRANTED, QUEUED, REVOKED, REJECTED)
- **Vendored JSON schemas** from the official [VDA5050/VDA5050](https://github.com/VDA5050/VDA5050) repository (v3.0.0) for validation
- **Topic mapper** for bidirectional NATS ↔ VDA5050 MQTT topic translation (including `zoneSet` and `responses` subjects)
- **State transformer** to convert Nova telemetry dicts to VDA5050 StateMessage
- **Command translator** to convert VDA5050 orders/instantActions to Nova control commands
- **Manufacturer registry** mapping Nova robot models to VDA5050 manufacturer names
- **Robot specs** with `build_factsheet()` for 8 robot models (Spot, G1, Go2, B2, H1, UR5e, TIAGo, PiDog)

## Installation

```bash
pip install git+https://github.com/wandelbotsgmbh/nova-vda5050.git
```

## Usage

```python
from nova_vda5050 import (
    TopicMapper,
    StateMessage,
    ZoneSetMessage, ZoneSet, Zone, ZoneType,
    ResponsesMessage, Response, GrantType,
    build_factsheet,
    transform_telemetry_to_state,
    get_manufacturer,
)

# Map Nova subjects to VDA5050
mapper = TopicMapper("rt.v1")
subject = mapper.nova_state_to_vda5050_nats("spot", "spot-01")
# => "vda5050.v3.BostonDynamics.spot-01.state"

# Transform telemetry
state_msg = transform_telemetry_to_state(
    nova_telemetry={"position": {"x": 1.0, "y": 2.0}, "battery": {"percentage": 85}},
    robot_id="spot-01",
    manufacturer="BostonDynamics",
    header_id=1,
)

# Build a factsheet for a robot model
factsheet = build_factsheet("spot", "spot-01", simulated=False)

# Create a zone set
zone_set = ZoneSetMessage(
    headerId=1, timestamp="2025-01-01T00:00:00.000Z",
    manufacturer="BostonDynamics", serialNumber="spot-01",
    zoneSet=ZoneSet(
        mapId="default", zoneSetId="zs-1",
        zones=[Zone(zoneId="z1", zoneType=ZoneType.BLOCKED,
                    vertices=[{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}])]
    ),
)
```

## V3.0.0 Compliance Status

| Message Type | Pydantic Model | JSON Schema | Topic Helper |
|---|---|---|---|
| state | ✅ Full V3 | ✅ | ✅ |
| order | ✅ | ✅ | ✅ |
| instantActions | ✅ | ✅ | ✅ |
| connection | ✅ | ✅ | ✅ |
| visualization | ✅ Full V3 | ✅ | ✅ |
| factsheet | ✅ | ✅ | ✅ |
| zoneSet | ✅ | ✅ | ✅ |
| responses | ✅ | ✅ | ✅ |

### Known Gaps

- Connectors do not yet populate all V3 state fields (e.g., `instantActionStates`, `zoneRequests`, `maps`)
- `OrderMessage` does not model corridor/retriable semantics
- Connectors do not fully execute orders (factsheets may overstate capabilities)

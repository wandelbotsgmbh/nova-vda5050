# nova-vda5050

VDA5050 V3.0.0 Python library for the Wandelbots Nova platform.

## Features

- **Pydantic models** for all VDA5050 V3.0.0 message types (state, order, instantActions, connection, visualization, factsheet, responses, zoneSet)
- **Vendored JSON schemas** from the official [VDA5050/VDA5050](https://github.com/VDA5050/VDA5050) repository (v3.0.0) for validation
- **Topic mapper** for bidirectional NATS <-> VDA5050 MQTT topic translation
- **State transformer** to convert Nova telemetry dicts to VDA5050 StateMessage
- **Command translator** to convert VDA5050 orders/instantActions to Nova control commands
- **Manufacturer registry** mapping Nova robot models to VDA5050 manufacturer names

## Installation

```bash
pip install nova-vda5050 --index-url https://pypi.pkg.github.com/wandelbotsgmbh/
```

## Usage

```python
from nova_vda5050 import (
    TopicMapper,
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
```

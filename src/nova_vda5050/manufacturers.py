"""Manufacturer registry — maps Nova robot models to VDA5050 manufacturer names."""

from __future__ import annotations

# Model name (lowercase) -> VDA5050 manufacturer string
MANUFACTURERS: dict[str, str] = {
    # Boston Dynamics
    "spot": "BostonDynamics",
    # Unitree
    "g1": "Unitree",
    "go2": "Unitree",
    "b2": "Unitree",
    "h1": "Unitree",
    # Simulated / generic
    "ur5e": "UniversalRobots",
    "tiago": "PALRobotics",
    "pidog": "SunFounder",
}

# Default manufacturer for unknown models
DEFAULT_MANUFACTURER = "Wandelbots"


def get_manufacturer(robot_model: str) -> str:
    """Return the VDA5050 manufacturer name for a Nova robot model."""
    return MANUFACTURERS.get(robot_model.lower(), DEFAULT_MANUFACTURER)

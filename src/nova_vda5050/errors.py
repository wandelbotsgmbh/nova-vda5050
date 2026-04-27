"""VDA5050 error and safety helpers for Nova connectors."""

from __future__ import annotations

from nova_vda5050.schemas import (
    EStopState,
    Error,
    ErrorLevel,
    ErrorReference,
    OperatingMode,
    SafetyState,
)


# ── Common VDA5050 error type constants ─────────────────────────────────────

COMMUNICATION_LOST = "communicationLost"
HARDWARE_FAULT = "hardwareFault"
ROBOT_FELL = "robotFell"
BATTERY_READ_FAILED = "batteryReadFailed"
SENSOR_FAULT = "sensorFault"
LEASE_TIMEOUT = "leaseTimeout"
MOTOR_FAULT = "motorFault"
SOFTWARE_ERROR = "softwareError"
COMMAND_FAILED = "commandFailed"
ESTOP_ACTIVE = "estopActive"
CONNECTION_TIMEOUT = "connectionTimeout"


# ── Error builder ───────────────────────────────────────────────────────────


def make_error(
    error_type: str,
    level: ErrorLevel | str = ErrorLevel.WARNING,
    description: str | None = None,
    hint: str | None = None,
    references: dict[str, str] | None = None,
) -> Error:
    """Build a VDA5050 Error object.

    Args:
        error_type: VDA5050 error type string (use constants above).
        level: "WARNING" or "FATAL".
        description: Human-readable error description.
        hint: Hint for resolving the error.
        references: Key-value pairs for errorReferences.
    """
    if isinstance(level, str):
        level = ErrorLevel(level.upper())
    refs = [ErrorReference(referenceKey=k, referenceValue=v) for k, v in (references or {}).items()]
    return Error(
        errorType=error_type,
        errorLevel=level,
        errorDescription=description,
        errorHint=hint,
        errorReferences=refs,
    )


# ── Safety helpers ──────────────────────────────────────────────────────────


def map_estop(
    estop_active: bool,
    estop_type: str = "NONE",
    field_violation: bool = False,
) -> SafetyState:
    """Build a VDA5050 SafetyState.

    Args:
        estop_active: Whether e-stop is currently active.
        estop_type: One of "AUTOACK", "MANUAL", "REMOTE", "NONE".
            When estop_active is True and type is "NONE", defaults to "MANUAL".
        field_violation: Whether a protective field violation is active.
    """
    if estop_active:
        if estop_type.upper() == "NONE":
            estop_type = "MANUAL"
        try:
            estop = EStopState(estop_type.upper())
        except ValueError:
            estop = EStopState.MANUAL
    else:
        estop = EStopState.NONE
    return SafetyState(eStop=estop, fieldViolation=field_violation)


def map_operating_mode(mode: str | None) -> OperatingMode:
    """Map a connector-specific mode string to VDA5050 OperatingMode.

    Accepts various common aliases.
    """
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
        # Unitree DDS FSM aliases
        "zero_torque": OperatingMode.SERVICE,
        "damping": OperatingMode.SERVICE,
        "sit": OperatingMode.SEMIAUTOMATIC,
        "lock_standing": OperatingMode.SEMIAUTOMATIC,
        "standing": OperatingMode.SEMIAUTOMATIC,
        "start": OperatingMode.SEMIAUTOMATIC,
        "running": OperatingMode.AUTOMATIC,
        "run": OperatingMode.AUTOMATIC,
    }
    return mode_map.get(mode.lower().strip(), OperatingMode.AUTOMATIC)

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum


class NormalizationMode(str, Enum):
    ADDITIVE = "additive"
    LOG_VOLUME = "log_volume"
    RH_ENVELOPE = "rh_envelope"
    PRIME_FLUX = "prime_flux"
    BOX_PRIME_FLUX = "box_prime_flux"


@dataclass(frozen=True)
class NormalizedResidual:
    mode: NormalizationMode
    interval: tuple[int | float, int | float]
    center_u: float
    raw_residual: float
    scale: float
    value: float


class NormalizationError(RuntimeError):
    pass


def center_log_coordinate(a: int | float, b: int | float) -> float:
    if a <= 0 or b <= a:
        raise NormalizationError("requires 0 < a < b")
    return 0.5 * (math.log(a) + math.log(b))


def additive_scale(a: int | float, b: int | float) -> float:
    if b <= a:
        raise NormalizationError("requires b > a")
    return float(b - a)


def log_volume_scale(a: int | float, b: int | float) -> float:
    if a <= 0 or b <= a:
        raise NormalizationError("requires 0 < a < b")
    return math.log(b) - math.log(a)


def rh_envelope_scale(a: int | float, b: int | float) -> float:
    """Diagnostic RH-shaped envelope scale.

    This is a normalization diagnostic only. It is not a theorem claim.
    """
    u = center_log_coordinate(a, b)
    return math.exp(u / 2.0)


def prime_flux_scale(a: int | float, b: int | float) -> float:
    """Expected log-coordinate prime-flux scale e^u/u over one log-volume unit."""
    u = center_log_coordinate(a, b)
    if u <= 0:
        raise NormalizationError("center log-coordinate must be positive")
    return math.exp(u) / u


def box_prime_flux_scale(a: int | float, b: int | float) -> float:
    """Expected prime-flux scale over the whole log-width of the box.

    This multiplies the local log-coordinate flux e^u/u by the box width
    Delta u = log(b)-log(a). It is the preferred scale when comparing boxes
    with different log widths.
    """
    return prime_flux_scale(a, b) * log_volume_scale(a, b)


def normalization_scale(mode: NormalizationMode | str, a: int | float, b: int | float) -> float:
    mode = NormalizationMode(mode)
    if mode == NormalizationMode.ADDITIVE:
        return additive_scale(a, b)
    if mode == NormalizationMode.LOG_VOLUME:
        return log_volume_scale(a, b)
    if mode == NormalizationMode.RH_ENVELOPE:
        return rh_envelope_scale(a, b)
    if mode == NormalizationMode.PRIME_FLUX:
        return prime_flux_scale(a, b)
    if mode == NormalizationMode.BOX_PRIME_FLUX:
        return box_prime_flux_scale(a, b)
    raise NormalizationError(f"unsupported normalization mode: {mode}")


def normalize_residual(
    residual: float,
    a: int | float,
    b: int | float,
    mode: NormalizationMode | str,
) -> NormalizedResidual:
    mode = NormalizationMode(mode)
    scale = normalization_scale(mode, a, b)
    if scale == 0:
        raise NormalizationError("normalization scale is zero")
    return NormalizedResidual(
        mode=mode,
        interval=(a, b),
        center_u=center_log_coordinate(a, b),
        raw_residual=float(residual),
        scale=scale,
        value=float(residual) / scale,
    )


def normalize_all_modes(residual: float, a: int | float, b: int | float) -> list[NormalizedResidual]:
    return [normalize_residual(residual, a, b, mode) for mode in NormalizationMode]

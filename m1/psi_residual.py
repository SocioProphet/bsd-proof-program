from __future__ import annotations

import math
from dataclasses import dataclass

from m1.li_quadrature import QuadratureConfig, zero_channel_integral


@dataclass(frozen=True)
class ResidualResult:
    interval: tuple[int | float, int | float]
    psi_increment: float
    truncation_level: int
    channel_sum: float
    residual: float


# Infrastructure placeholder.
# Full Chebyshev psi implementation will later be replaced with a certified
# Mangoldt-sum engine or imported audited source.
def approximate_psi(x: int | float) -> float:
    return float(x)


def psi_increment(a: int | float, b: int | float) -> float:
    return approximate_psi(b) - approximate_psi(a)


def compute_residual(
    a: int | float,
    b: int | float,
    gammas: list[float],
    config: QuadratureConfig,
) -> ResidualResult:
    raw = psi_increment(a, b)

    channel_sum = 0.0
    for gamma in gammas:
        channel_sum += zero_channel_integral(a, b, gamma, config)

    residual = raw - channel_sum

    return ResidualResult(
        interval=(a, b),
        psi_increment=raw,
        truncation_level=len(gammas),
        channel_sum=channel_sum,
        residual=residual,
    )

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class QuadratureConfig:
    du: float = 0.0025
    max_frequency: float | None = None
    safety_factor: float = 1.0

    def validate(self) -> None:
        if self.du <= 0:
            raise ValueError("du must be positive")
        if self.max_frequency is not None:
            if self.max_frequency <= 0:
                raise ValueError("max_frequency must be positive")
            if self.du * self.max_frequency > self.safety_factor:
                raise ValueError(
                    "quadrature step violates oscillation-resolution condition: "
                    "du * gamma_N must be <= safety_factor"
                )


def trapezoid_integral(f: Callable[[float], float], u0: float, u1: float, config: QuadratureConfig) -> float:
    """Fixed-step trapezoid integration in log-coordinate u.

    The M1 production path uses a fixed-step rule so the run is replayable.
    Adaptive integrators may be used only as external correctness references.
    """
    config.validate()
    if u1 < u0:
        raise ValueError("u1 must be >= u0")
    if u1 == u0:
        return 0.0

    width = u1 - u0
    n = max(1, math.ceil(width / config.du))
    h = width / n
    acc = 0.5 * (f(u0) + f(u1))
    for i in range(1, n):
        acc += f(u0 + i * h)
    return acc * h


def oscillatory_li_kernel(u: float, gamma: float) -> float:
    """Real u-form oscillatory kernel used for zero-channel infrastructure.

    This is the replayable real-valued substrate. It deliberately avoids complex Ei
    and keeps branch behavior out of the implementation surface.
    """
    return math.exp(u / 2.0) * math.cos(gamma * u) / max(u, 1e-300)


def zero_channel_integral(a: int | float, b: int | float, gamma: float, config: QuadratureConfig) -> float:
    if a <= 1 or b <= a:
        raise ValueError("requires 1 < a < b")
    u0 = math.log(a)
    u1 = math.log(b)
    cfg = QuadratureConfig(du=config.du, max_frequency=gamma, safety_factor=config.safety_factor)
    return trapezoid_integral(lambda u: oscillatory_li_kernel(u, gamma), u0, u1, cfg)


def constant_integral_closed_form(a: int | float, b: int | float) -> float:
    """Closed form for integral of 1 du over [log(a),log(b)]."""
    if a <= 0 or b <= a:
        raise ValueError("requires 0 < a < b")
    return math.log(b) - math.log(a)

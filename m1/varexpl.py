from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VarianceExplanation:
    raw_variance: float
    residual_variance: float
    explained_fraction: float


class VarianceExplanationError(RuntimeError):
    pass


def variance(values: list[float]) -> float:
    if not values:
        raise VarianceExplanationError("empty sequence")

    mu = sum(values) / len(values)
    return sum((x - mu) ** 2 for x in values) / len(values)


def variance_explained(raw: list[float], residual: list[float]) -> VarianceExplanation:
    if len(raw) != len(residual):
        raise VarianceExplanationError("sequence length mismatch")

    raw_var = variance(raw)
    residual_var = variance(residual)

    if raw_var == 0:
        explained = 0.0
    else:
        explained = 1.0 - residual_var / raw_var

    return VarianceExplanation(
        raw_variance=raw_var,
        residual_variance=residual_var,
        explained_fraction=explained,
    )

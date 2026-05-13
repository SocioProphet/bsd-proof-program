from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class StationaritySummary:
    count: int
    mean: float
    variance: float
    lag1_autocorrelation: float
    energy: float


class StatisticsError(RuntimeError):
    pass



def mean(values: list[float]) -> float:
    if not values:
        raise StatisticsError("empty sequence")
    return sum(values) / len(values)



def variance(values: list[float]) -> float:
    if not values:
        raise StatisticsError("empty sequence")
    mu = mean(values)
    return sum((x - mu) ** 2 for x in values) / len(values)



def lag1_autocorrelation(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0

    mu = mean(values)
    denom = sum((x - mu) ** 2 for x in values)

    if denom == 0:
        return 0.0

    numer = sum(
        (values[i] - mu) * (values[i + 1] - mu)
        for i in range(len(values) - 1)
    )

    return numer / denom



def energy(values: list[float]) -> float:
    return math.sqrt(sum(x * x for x in values))



def summarize_stationarity(values: list[float]) -> StationaritySummary:
    return StationaritySummary(
        count=len(values),
        mean=mean(values),
        variance=variance(values),
        lag1_autocorrelation=lag1_autocorrelation(values),
        energy=energy(values),
    )



def aggregate_box_residuals(boxes: list[float], block_size: int) -> list[float]:
    if block_size <= 0:
        raise StatisticsError("block_size must be positive")

    out = []
    for i in range(0, len(boxes), block_size):
        chunk = boxes[i : i + block_size]
        if chunk:
            out.append(sum(chunk) / len(chunk))
    return out



def scaling_slope(xs: list[float], ys: list[float]) -> float:
    """Least-squares slope in log-log coordinates."""
    if len(xs) != len(ys) or len(xs) < 2:
        raise StatisticsError("need matching sequences with length >= 2")

    lx = [math.log(x) for x in xs]
    ly = [math.log(abs(y) + 1e-300) for y in ys]

    mx = mean(lx)
    my = mean(ly)

    denom = sum((x - mx) ** 2 for x in lx)
    if denom == 0:
        return 0.0

    numer = sum((lx[i] - mx) * (ly[i] - my) for i in range(len(lx)))

    return numer / denom

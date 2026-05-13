from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkInterval:
    name: str
    left: int
    right: int
    du: float


PRIMARY_A_INTERVALS = [
    BenchmarkInterval("I1", 10_000, 20_000, 0.0025),
    BenchmarkInterval("I2", 100_000, 110_000, 0.0025),
    BenchmarkInterval("I3", 1_000_000, 1_010_000, 0.0025),
]


def get_interval(name: str) -> BenchmarkInterval:
    for item in PRIMARY_A_INTERVALS:
        if item.name == name:
            return item
    raise KeyError(name)

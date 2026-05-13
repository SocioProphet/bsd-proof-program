from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path

from m1.benchmarks import BenchmarkInterval
from m1.li_quadrature import QuadratureConfig
from m1.normalization import NormalizationMode, normalize_residual
from m1.psi_residual import compute_residual
from m1.statistics import StationaritySummary, summarize_stationarity


@dataclass(frozen=True)
class SweepSpec:
    name: str
    intervals: list[BenchmarkInterval]
    truncation_levels: list[int]
    du_values: list[float]
    normalization_modes: list[NormalizationMode]


@dataclass(frozen=True)
class SweepObservation:
    interval_name: str
    left: int
    right: int
    truncation_level: int
    du: float
    normalization_mode: NormalizationMode
    raw_residual: float
    normalized_residual: float


@dataclass(frozen=True)
class SweepResult:
    spec_hash: str
    observations: list[SweepObservation]
    summaries: dict[str, StationaritySummary]


class ExperimentError(RuntimeError):
    pass


def canonical_hash(obj: object) -> str:
    text = json.dumps(obj, sort_keys=True, default=str)
    return sha256(text.encode("utf-8")).hexdigest()


def run_sweep(spec: SweepSpec, gammas: list[float]) -> SweepResult:
    if not spec.truncation_levels:
        raise ExperimentError("truncation_levels must not be empty")
    if not spec.du_values:
        raise ExperimentError("du_values must not be empty")
    if not spec.normalization_modes:
        raise ExperimentError("normalization_modes must not be empty")

    observations: list[SweepObservation] = []

    for interval in spec.intervals:
        for du in spec.du_values:
            for n in spec.truncation_levels:
                selected = gammas[:n]
                cfg = QuadratureConfig(du=du)
                residual = compute_residual(interval.left, interval.right, selected, cfg)

                for mode in spec.normalization_modes:
                    norm = normalize_residual(
                        residual.residual,
                        interval.left,
                        interval.right,
                        mode,
                    )
                    observations.append(
                        SweepObservation(
                            interval_name=interval.name,
                            left=interval.left,
                            right=interval.right,
                            truncation_level=n,
                            du=du,
                            normalization_mode=mode,
                            raw_residual=residual.residual,
                            normalized_residual=norm.value,
                        )
                    )

    summaries: dict[str, StationaritySummary] = {}
    for mode in spec.normalization_modes:
        vals = [
            obs.normalized_residual
            for obs in observations
            if obs.normalization_mode == mode
        ]
        summaries[str(mode.value)] = summarize_stationarity(vals)

    return SweepResult(
        spec_hash=canonical_hash(asdict(spec)),
        observations=observations,
        summaries=summaries,
    )


def write_sweep_result(path: str | Path, result: SweepResult) -> str:
    payload = asdict(result)
    digest = canonical_hash(payload)
    wrapped = {
        "result_sha256": digest,
        "payload": payload,
    }
    Path(path).write_text(json.dumps(wrapped, indent=2, sort_keys=True, default=str))
    return digest

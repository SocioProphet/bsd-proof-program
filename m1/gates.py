from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from m1.statistics import StationaritySummary


class GateStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True)
class GateResult:
    name: str
    status: GateStatus
    metric: float
    threshold: float
    rationale: str


class GateError(RuntimeError):
    pass



def stationarity_gate(summary: StationaritySummary, max_variance: float) -> GateResult:
    if max_variance < 0:
        raise GateError("max_variance must be nonnegative")

    status = GateStatus.PASS if summary.variance <= max_variance else GateStatus.FAIL
    return GateResult(
        name="stationarity",
        status=status,
        metric=summary.variance,
        threshold=max_variance,
        rationale="variance must remain below declared stationarity threshold",
    )



def autocorrelation_gate(summary: StationaritySummary, max_abs_lag1: float) -> GateResult:
    if max_abs_lag1 < 0:
        raise GateError("max_abs_lag1 must be nonnegative")

    metric = abs(summary.lag1_autocorrelation)
    status = GateStatus.PASS if metric <= max_abs_lag1 else GateStatus.FAIL
    return GateResult(
        name="lag1_autocorrelation",
        status=status,
        metric=metric,
        threshold=max_abs_lag1,
        rationale="absolute lag-1 autocorrelation must remain below threshold",
    )



def shuffled_collapse_gate(canonical_energy: float, shuffled_energy: float, min_ratio: float) -> GateResult:
    """Check that shuffled spectral controls do not preserve canonical energy.

    PASS here means the shuffled control energy is sufficiently smaller than the
    canonical energy under the chosen metric. This is an evidentiary gate only.
    """
    if canonical_energy <= 0:
        return GateResult(
            name="shuffled_collapse",
            status=GateStatus.INCONCLUSIVE,
            metric=0.0,
            threshold=min_ratio,
            rationale="canonical energy is zero, ratio undefined",
        )

    ratio = shuffled_energy / canonical_energy
    status = GateStatus.PASS if ratio <= min_ratio else GateStatus.FAIL
    return GateResult(
        name="shuffled_collapse",
        status=status,
        metric=ratio,
        threshold=min_ratio,
        rationale="shuffled control should collapse below declared canonical-energy ratio",
    )



def perturbation_robustness_gate(canonical_energy: float, perturbed_energy: float, max_relative_delta: float) -> GateResult:
    if canonical_energy <= 0:
        return GateResult(
            name="perturbation_robustness",
            status=GateStatus.INCONCLUSIVE,
            metric=0.0,
            threshold=max_relative_delta,
            rationale="canonical energy is zero, relative delta undefined",
        )

    delta = abs(perturbed_energy - canonical_energy) / canonical_energy
    status = GateStatus.PASS if delta <= max_relative_delta else GateStatus.FAIL
    return GateResult(
        name="perturbation_robustness",
        status=status,
        metric=delta,
        threshold=max_relative_delta,
        rationale="small spectral perturbation should preserve energy within threshold",
    )



def all_pass(results: list[GateResult]) -> bool:
    return bool(results) and all(x.status == GateStatus.PASS for x in results)

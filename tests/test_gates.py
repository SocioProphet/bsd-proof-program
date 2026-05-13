from m1.gates import (
    GateStatus,
    autocorrelation_gate,
    perturbation_robustness_gate,
    shuffled_collapse_gate,
    stationarity_gate,
)
from m1.statistics import StationaritySummary



def test_stationarity_gate_passes_under_threshold():
    summary = StationaritySummary(
        count=4,
        mean=0.0,
        variance=0.1,
        lag1_autocorrelation=0.0,
        energy=1.0,
    )

    result = stationarity_gate(summary, max_variance=0.2)

    assert result.status == GateStatus.PASS



def test_autocorrelation_gate_fails_above_threshold():
    summary = StationaritySummary(
        count=4,
        mean=0.0,
        variance=1.0,
        lag1_autocorrelation=0.9,
        energy=1.0,
    )

    result = autocorrelation_gate(summary, max_abs_lag1=0.2)

    assert result.status == GateStatus.FAIL



def test_shuffled_collapse_gate_passes_when_control_collapses():
    result = shuffled_collapse_gate(
        canonical_energy=10.0,
        shuffled_energy=2.0,
        min_ratio=0.25,
    )

    assert result.status == GateStatus.PASS



def test_perturbation_gate_passes_for_small_delta():
    result = perturbation_robustness_gate(
        canonical_energy=10.0,
        perturbed_energy=10.5,
        max_relative_delta=0.1,
    )

    assert result.status == GateStatus.PASS

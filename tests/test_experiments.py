from pathlib import Path

from m1.benchmarks import get_interval
from m1.experiments import SweepSpec, run_sweep, write_sweep_result
from m1.normalization import NormalizationMode



def test_sweep_runs(tmp_path: Path):
    spec = SweepSpec(
        name="smoke",
        intervals=[get_interval("I1")],
        truncation_levels=[1, 2],
        du_values=[0.0025],
        normalization_modes=[
            NormalizationMode.LOG_VOLUME,
            NormalizationMode.PRIME_FLUX,
        ],
    )

    gammas = [14.134725141734693790, 21.022039638771554993]

    result = run_sweep(spec, gammas)

    assert len(result.observations) > 0
    assert "log_volume" in result.summaries

    out = tmp_path / "result.json"

    digest = write_sweep_result(out, result)

    assert out.exists()
    assert len(digest) == 64

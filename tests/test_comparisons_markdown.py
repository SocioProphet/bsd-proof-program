from pathlib import Path

from m1.benchmarks import BenchmarkInterval
from m1.campaigns import CampaignKind, CampaignSpec, SpectralControl, run_campaign
from m1.comparisons import compare_perturbation_robustness, compare_shuffled_collapse, write_pair_report
from m1.experiments import SweepSpec
from m1.markdown import render_pair_report
from m1.normalization import NormalizationMode
from m1.perturbation import PerturbationSpec


GAMMAS = [
    14.134725141734693790,
    21.022039638771554993,
]



def _sweep():
    return SweepSpec(
        name="pair-smoke",
        intervals=[BenchmarkInterval("T", 10, 100, 0.01)],
        truncation_levels=[1, 2],
        du_values=[0.01],
        normalization_modes=[NormalizationMode.BOX_PRIME_FLUX],
    )



def test_pair_comparison_and_markdown(tmp_path: Path):
    canonical = run_campaign(
        CampaignSpec(
            name="canon",
            kind=CampaignKind.CANONICAL,
            sweep=_sweep(),
            spectral_control=SpectralControl.CANONICAL,
        ),
        GAMMAS,
    )
    shuffled = run_campaign(
        CampaignSpec(
            name="shuf",
            kind=CampaignKind.NULL_MODEL,
            sweep=_sweep(),
            spectral_control=SpectralControl.SHUFFLED,
            shuffle_seed=1,
        ),
        GAMMAS,
    )

    report = compare_shuffled_collapse(
        canonical,
        shuffled,
        summary_key="box_prime_flux",
        min_ratio=10.0,
    )

    out = tmp_path / "pair.json"
    digest = write_pair_report(out, report)
    md = render_pair_report(report)

    assert out.exists()
    assert len(digest) == 64
    assert "not a theorem claim" in md



def test_perturbation_comparison_runs():
    canonical = run_campaign(
        CampaignSpec(
            name="canon",
            kind=CampaignKind.CANONICAL,
            sweep=_sweep(),
        ),
        GAMMAS,
    )
    perturbed = run_campaign(
        CampaignSpec(
            name="perturb",
            kind=CampaignKind.PERTURBATION,
            sweep=_sweep(),
            spectral_control=SpectralControl.PERTURBED,
            perturbation=PerturbationSpec(epsilon=1e-6, seed=1),
        ),
        GAMMAS,
    )

    report = compare_perturbation_robustness(
        canonical,
        perturbed,
        summary_key="box_prime_flux",
        max_relative_delta=10.0,
    )

    assert report.comparison_kind == "perturbation_robustness"

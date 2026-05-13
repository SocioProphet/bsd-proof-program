from pathlib import Path

from m1.benchmarks import get_interval
from m1.campaigns import (
    CampaignKind,
    CampaignSpec,
    SpectralControl,
    run_campaign,
)
from m1.experiments import SweepSpec
from m1.gates import stationarity_gate
from m1.normalization import NormalizationMode
from m1.reports import build_campaign_report, write_campaign_report



def _sweep_spec():
    return SweepSpec(
        name="campaign-smoke",
        intervals=[get_interval("I1")],
        truncation_levels=[1],
        du_values=[0.0025],
        normalization_modes=[NormalizationMode.BOX_PRIME_FLUX],
    )



def test_canonical_campaign_runs():
    spec = CampaignSpec(
        name="canonical-smoke",
        kind=CampaignKind.CANONICAL,
        sweep=_sweep_spec(),
        spectral_control=SpectralControl.CANONICAL,
    )

    result = run_campaign(spec, [14.134725141734693790])

    assert result.spectral_control == SpectralControl.CANONICAL
    assert len(result.sweep_result.observations) == 1



def test_shuffled_campaign_runs():
    spec = CampaignSpec(
        name="shuffled-smoke",
        kind=CampaignKind.NULL_MODEL,
        sweep=_sweep_spec(),
        spectral_control=SpectralControl.SHUFFLED,
        shuffle_seed=1,
    )

    result = run_campaign(spec, [14.134725141734693790, 21.022039638771554993])

    assert result.spectral_control == SpectralControl.SHUFFLED



def test_campaign_report_writes(tmp_path: Path):
    spec = CampaignSpec(
        name="report-smoke",
        kind=CampaignKind.CANONICAL,
        sweep=_sweep_spec(),
    )

    result = run_campaign(spec, [14.134725141734693790])
    summary = result.sweep_result.summaries["box_prime_flux"]
    gate = stationarity_gate(summary, max_variance=1e30)
    report = build_campaign_report(result, [gate])

    out = tmp_path / "report.json"
    digest = write_campaign_report(out, report)

    assert out.exists()
    assert len(digest) == 64
    assert report.claim_status == "evidence_passed_no_theorem_claim"

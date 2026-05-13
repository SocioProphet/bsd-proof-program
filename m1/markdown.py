from __future__ import annotations

from m1.comparisons import PairComparisonReport
from m1.reports import CampaignReport


def render_campaign_report(report: CampaignReport) -> str:
    campaign = report.campaign_result.campaign
    lines = [
        f"# M1 Campaign Report: {campaign.name}",
        "",
        f"Claim status: `{report.claim_status}`",
        "",
        "## Campaign",
        "",
        f"- kind: `{campaign.kind.value}`",
        f"- spectral control: `{campaign.spectral_control.value}`",
        f"- spec hash: `{report.campaign_result.sweep_result.spec_hash}`",
        "",
        "## Summaries",
        "",
    ]

    for key, summary in report.campaign_result.sweep_result.summaries.items():
        lines.extend(
            [
                f"### {key}",
                "",
                f"- count: {summary.count}",
                f"- mean: {summary.mean}",
                f"- variance: {summary.variance}",
                f"- lag1_autocorrelation: {summary.lag1_autocorrelation}",
                f"- energy: {summary.energy}",
                "",
            ]
        )

    lines.extend(["## Gates", ""])
    if not report.gates:
        lines.append("No gates were applied.")
    else:
        for gate in report.gates:
            lines.extend(
                [
                    f"- `{gate.name}`: `{gate.status.value}`",
                    f"  - metric: {gate.metric}",
                    f"  - threshold: {gate.threshold}",
                    f"  - rationale: {gate.rationale}",
                ]
            )

    lines.extend(
        [
            "",
            "## Claim discipline",
            "",
            "This report is an evidentiary campaign artifact. It is not a theorem claim.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_pair_report(report: PairComparisonReport) -> str:
    lines = [
        f"# M1 Pair Comparison Report: {report.comparison_kind}",
        "",
        f"Claim status: `{report.claim_status}`",
        "",
        f"- summary key: `{report.summary_key}`",
        f"- canonical energy: {report.canonical_energy}",
        f"- control energy: {report.control_energy}",
        "",
        "## Gate",
        "",
        f"- `{report.gate.name}`: `{report.gate.status.value}`",
        f"  - metric: {report.gate.metric}",
        f"  - threshold: {report.gate.threshold}",
        f"  - rationale: {report.gate.rationale}",
        "",
        "## Claim discipline",
        "",
        "This comparison report is an evidentiary artifact. It is not a theorem claim.",
    ]
    return "\n".join(lines) + "\n"

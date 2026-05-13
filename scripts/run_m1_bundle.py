#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from m1.campaign_io import evaluate_gate_specs, load_campaign_envelope, load_gammas
from m1.campaigns import run_campaign
from m1.comparisons import (
    compare_perturbation_robustness,
    compare_shuffled_collapse,
    write_pair_report,
)
from m1.markdown import render_campaign_report, render_pair_report
from m1.provenance import build_provenance_record
from m1.reports import build_campaign_report, write_campaign_report



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run canonical/null/perturbation M1 campaign bundle."
    )
    parser.add_argument("--canonical-spec", required=True)
    parser.add_argument("--shuffled-spec", required=True)
    parser.add_argument("--perturbation-spec", required=True)
    parser.add_argument("--gammas", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--summary-key", default="box_prime_flux")
    parser.add_argument("--shuffled-min-ratio", type=float, default=0.75)
    parser.add_argument("--perturbation-max-relative-delta", type=float, default=0.25)
    return parser.parse_args()



def _run_one(spec_path: str, gammas: list[float], out_dir: Path, stem: str):
    envelope = load_campaign_envelope(spec_path)
    result = run_campaign(envelope.campaign, gammas)
    gates = evaluate_gate_specs(result, envelope.gates)
    provenance = build_provenance_record(
        parameters={
            "spec": str(Path(spec_path)),
            "campaign_name": envelope.campaign.name,
            "campaign_kind": envelope.campaign.kind.value,
            "spectral_control": envelope.campaign.spectral_control.value,
        },
        gammas=gammas,
        spectral_source=envelope.spectral_source,
    )
    report = build_campaign_report(result, gates, provenance=provenance)
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"
    digest = write_campaign_report(json_path, report)
    md_path.write_text(render_campaign_report(report))
    return report, digest



def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    gammas = load_gammas(args.gammas)

    canonical_report, canonical_digest = _run_one(
        args.canonical_spec,
        gammas,
        out_dir,
        "canonical_campaign_report",
    )
    shuffled_report, shuffled_digest = _run_one(
        args.shuffled_spec,
        gammas,
        out_dir,
        "shuffled_campaign_report",
    )
    perturbation_report, perturbation_digest = _run_one(
        args.perturbation_spec,
        gammas,
        out_dir,
        "perturbation_campaign_report",
    )

    shuffled_pair = compare_shuffled_collapse(
        canonical_report.campaign_result,
        shuffled_report.campaign_result,
        summary_key=args.summary_key,
        min_ratio=args.shuffled_min_ratio,
    )
    perturbation_pair = compare_perturbation_robustness(
        canonical_report.campaign_result,
        perturbation_report.campaign_result,
        summary_key=args.summary_key,
        max_relative_delta=args.perturbation_max_relative_delta,
    )

    shuffled_pair_digest = write_pair_report(out_dir / "canonical_vs_shuffled_pair.json", shuffled_pair)
    (out_dir / "canonical_vs_shuffled_pair.md").write_text(render_pair_report(shuffled_pair))

    perturbation_pair_digest = write_pair_report(out_dir / "canonical_vs_perturbation_pair.json", perturbation_pair)
    (out_dir / "canonical_vs_perturbation_pair.md").write_text(render_pair_report(perturbation_pair))

    print(f"canonical_report_sha256={canonical_digest}")
    print(f"shuffled_report_sha256={shuffled_digest}")
    print(f"perturbation_report_sha256={perturbation_digest}")
    print(f"canonical_vs_shuffled_pair_sha256={shuffled_pair_digest}")
    print(f"canonical_vs_perturbation_pair_sha256={perturbation_pair_digest}")
    print(f"canonical_claim_status={canonical_report.claim_status}")
    print(f"shuffled_pair_claim_status={shuffled_pair.claim_status}")
    print(f"perturbation_pair_claim_status={perturbation_pair.claim_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

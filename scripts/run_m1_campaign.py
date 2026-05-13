#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from m1.campaign_io import evaluate_gate_specs, load_campaign_envelope, load_gammas
from m1.campaigns import run_campaign
from m1.provenance import build_provenance_record
from m1.reports import build_campaign_report, write_campaign_report



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an M1 campaign spec against a gamma table and write a frozen report."
    )
    parser.add_argument(
        "--spec",
        required=True,
        help="Path to M1 campaign JSON spec.",
    )
    parser.add_argument(
        "--gammas",
        required=True,
        help="Path to newline-delimited gamma values.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output path for frozen campaign report JSON.",
    )
    return parser.parse_args()



def main() -> int:
    args = parse_args()

    envelope = load_campaign_envelope(args.spec)
    gammas = load_gammas(args.gammas)

    result = run_campaign(envelope.campaign, gammas)
    gates = evaluate_gate_specs(result, envelope.gates)

    provenance = build_provenance_record(
        parameters={
            "spec": str(Path(args.spec)),
            "campaign_name": envelope.campaign.name,
            "campaign_kind": envelope.campaign.kind.value,
            "spectral_control": envelope.campaign.spectral_control.value,
        },
        gammas=gammas,
        spectral_source=envelope.spectral_source,
    )

    report = build_campaign_report(result, gates, provenance=provenance)
    digest = write_campaign_report(args.out, report)

    print(f"report_sha256={digest}")
    print(f"claim_status={report.claim_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

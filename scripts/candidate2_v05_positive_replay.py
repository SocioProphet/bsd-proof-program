#!/usr/bin/env python3
"""Candidate 2 positive-path replay against restored BSD v0.5 baseline.

This is the first positive proof-apparatus replay after State A import. It checks
that the v0.5 executable baseline restores, freezes, preserves the documented
claim-tier split, preserves the audit correction, and emits digest-addressed
ledger events for the C5-facing row consistency channels available in the v0.5
baseline.

Boundary: this script validates the imported v0.5 baseline and its C5-facing
consistency record. It does not re-run independent four-descent/M6 gates and does
not promote any adapter claim.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "v0.5" / "bsd_dataset_v0_5.json"
VALIDATION = ROOT / "reports" / "v0.5" / "bsd_dataset_v0_5_validation.json"
OUT = ROOT / "reports" / "candidate2"
SEVEN = [41, 137, 257, 313, 353, 457, 761]
EXPECTED_SPLIT = {"H-E1-alg": 426, "H-E2": 182}
EXPECTED_TOTAL = 608
EXPECTED_FALSE_POSITIVES = [313, 353]
EXPECTED_RANK2 = [41, 137, 761]


def sha256_json(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_restored() -> None:
    if DATA.exists() and VALIDATION.exists():
        return
    subprocess.run(["python3", "scripts/restore_v0_5_payload.py"], cwd=ROOT, check=True)


def event(row: dict[str, Any], gate: str, payload: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    input_payload = {"gate": gate, "n": row["n"], "row": payload}
    output_payload = {"gate": gate, "n": row["n"], "result": result}
    return {
        "event_type": "candidate2_gate_replay",
        "gate": gate,
        "n": row["n"],
        "input_digest": "sha256:" + sha256_json(input_payload),
        "output_digest": "sha256:" + sha256_json(output_payload),
        "result": result,
    }


def main() -> int:
    ensure_restored()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
    rows = data["rows"]

    if data["total_rows"] != EXPECTED_TOTAL or len(rows) != EXPECTED_TOTAL:
        raise SystemExit(f"row-count mismatch: data={data.get('total_rows')} len={len(rows)}")
    if data["by_tier"] != EXPECTED_SPLIT:
        raise SystemExit(f"claim-tier mismatch: {data['by_tier']}")
    if validation.get("by_claim_tier") != EXPECTED_SPLIT:
        raise SystemExit(f"validation split mismatch: {validation.get('by_claim_tier')}")
    if validation.get("open_contradictions") != 0:
        raise SystemExit(f"open contradictions present: {validation.get('open_contradictions')}")
    if validation.get("audit_correction", {}).get("false_positives_caught") != EXPECTED_FALSE_POSITIVES:
        raise SystemExit("audit correction false-positive set mismatch")
    if validation.get("rank_2_unconditional_primes") != EXPECTED_RANK2:
        raise SystemExit("rank-2 unconditional prime set mismatch")

    by_tier = Counter(row["claim_tier"] for row in rows)
    root_numbers = Counter(str(row["root_number"]) for row in rows)
    tunnell_status = Counter(row["tunnell_status"] for row in rows)
    row_events = []

    for row in rows:
        row_events.append(event(row, "v0.5-claim-tier-consistency", {
            "claim_tier": row["claim_tier"],
            "alg_rank_method": row["alg_rank_method"],
            "alg_rank_exact_known": row["alg_rank_exact_known"],
            "BSD_used": row["BSD_used"],
            "sha_finite_assumed": row["sha_finite_assumed"],
        }, {
            "pass": row["claim_tier"] in {"H-E1-alg", "H-E2"},
            "claim_tier": row["claim_tier"],
        }))
        row_events.append(event(row, "v0.5-tunnell-root-consistency", {
            "root_number": row["root_number"],
            "tunnell_status": row["tunnell_status"],
            "n_mod_8": row["n_mod_8"],
            "congruent_status": row["congruent_status"],
        }, {
            "pass": row["tunnell_status"] in {"obstruction", "conditional_congruent"} and row["root_number"] in {-1, 1},
            "tunnell_status": row["tunnell_status"],
            "root_number": row["root_number"],
        }))
        row_events.append(event(row, "v0.5-nonclaim-discipline", {
            "BSD_used": row["BSD_used"],
            "parity_used": row["parity_used"],
            "sha_finite_assumed": row["sha_finite_assumed"],
            "claim_tier": row["claim_tier"],
        }, {
            "pass": row["sha_finite_assumed"] is False,
            "sha_finite_assumed": row["sha_finite_assumed"],
        }))

    failed = [e for e in row_events if not e["result"].get("pass")]
    if failed:
        raise SystemExit(f"candidate2 failed events: {failed[:5]}")

    seven_status = {}
    by_n = {int(row["n"]): row for row in rows}
    for n in SEVEN:
        row = by_n[n]
        seven_status[str(n)] = {
            "claim_tier": row["claim_tier"],
            "alg_rank_method": row["alg_rank_method"],
            "alg_rank_exact_known": row["alg_rank_exact_known"],
            "alg_rank_exact": row["alg_rank_exact"],
            "second_independent_point_certified": row["second_independent_point_certified"],
            "promoted_in_milestone": row["promoted_in_milestone"],
        }

    input_digests = {e["input_digest"] for e in row_events}
    output_digests = {e["output_digest"] for e in row_events}
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "state": "Candidate 2 positive replay",
        "scope_boundary": [
            "Validates v0.5 baseline consistency through controller-visible data.",
            "Does not re-attest inherited H-E1-alg classifications as controller-witnessed M6 evidence.",
            "Does not promote adapter claims."
        ],
        "source_files": {
            "data/v0.5/bsd_dataset_v0_5.json": sha256_file(DATA),
            "reports/v0.5/bsd_dataset_v0_5_validation.json": sha256_file(VALIDATION),
        },
        "total_rows": len(rows),
        "by_tier": dict(by_tier),
        "root_numbers": dict(root_numbers),
        "tunnell_status": dict(tunnell_status),
        "event_count": len(row_events),
        "distinct_input_digest_count": len(input_digests),
        "distinct_output_digest_count": len(output_digests),
        "failed_event_count": len(failed),
        "audit_correction": validation["audit_correction"],
        "seven_prime_status": seven_status,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "candidate2_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (OUT / "candidate2_ledger_events.jsonl").open("w", encoding="utf-8") as handle:
        for item in row_events:
            handle.write(json.dumps(item, sort_keys=True) + "\n")
    lines = [
        "# Candidate 2 Positive Replay Result",
        "",
        "Scope: v0.5 baseline consistency replay. No claim promotion.",
        "",
        f"- total_rows: {summary['total_rows']}",
        f"- H-E1-alg: {summary['by_tier'].get('H-E1-alg')}",
        f"- H-E2: {summary['by_tier'].get('H-E2')}",
        f"- event_count: {summary['event_count']}",
        f"- distinct_input_digest_count: {summary['distinct_input_digest_count']}",
        f"- distinct_output_digest_count: {summary['distinct_output_digest_count']}",
        f"- failed_event_count: {summary['failed_event_count']}",
        "",
        "## Seven-prime status",
        "",
    ]
    for n in SEVEN:
        lines.append(f"- {n}: {seven_status[str(n)]}")
    lines.extend(["", "## Audit correction", "", json.dumps(validation["audit_correction"], indent=2, sort_keys=True)])
    (OUT / "candidate2_result.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("candidate2_v05_positive_replay: PASS")
    print(f"total_rows={summary['total_rows']}")
    print(f"by_tier={summary['by_tier']}")
    print(f"event_count={summary['event_count']}")
    print(f"distinct_input_digest_count={summary['distinct_input_digest_count']}")
    print(f"distinct_output_digest_count={summary['distinct_output_digest_count']}")
    print(f"failed_event_count={summary['failed_event_count']}")
    print(f"seven_prime_status={json.dumps(seven_status, sort_keys=True)}")
    print(f"audit_correction={json.dumps(validation['audit_correction'], sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate and freeze the restored BSD v0.5 baseline.

State A only: verifies imported data and writes reproducible reports under
reports/v0.6/m6.0. It does not promote claims or perform descent.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_JSON = ROOT / "data" / "v0.5" / "bsd_dataset_v0_5.json"
DATA_CSV = ROOT / "data" / "v0.5" / "bsd_dataset_v0_5.csv"
VALIDATION = ROOT / "reports" / "v0.5" / "bsd_dataset_v0_5_validation.json"
OUT = ROOT / "reports" / "v0.6" / "m6.0"
EXPECTED_TOTAL = 608
EXPECTED_BY_TIER = {"H-E1-alg": 426, "H-E2": 182}
SEVEN_PRIMES = [41, 137, 257, 313, 353, 457, 761]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_payload_restored() -> None:
    if DATA_JSON.exists() and DATA_CSV.exists() and VALIDATION.exists():
        return
    restore = ROOT / "scripts" / "restore_v0_5_payload.py"
    if not restore.exists():
        raise SystemExit("v0.5 payload missing and restore script unavailable")
    import subprocess
    subprocess.run(["python3", str(restore)], cwd=ROOT, check=True)


def load_dataset() -> dict:
    ensure_payload_restored()
    return json.loads(DATA_JSON.read_text(encoding="utf-8"))


def verify_csv_rows() -> int:
    with DATA_CSV.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def main() -> int:
    data = load_dataset()
    rows = data.get("rows", [])
    by_tier = data.get("by_tier", {})
    if data.get("total_rows") != EXPECTED_TOTAL:
        raise SystemExit(f"expected total_rows {EXPECTED_TOTAL}, got {data.get('total_rows')}")
    if len(rows) != EXPECTED_TOTAL:
        raise SystemExit(f"expected {EXPECTED_TOTAL} rows, got {len(rows)}")
    if by_tier != EXPECTED_BY_TIER:
        raise SystemExit(f"expected by_tier {EXPECTED_BY_TIER}, got {by_tier}")
    csv_rows = verify_csv_rows()
    if csv_rows != EXPECTED_TOTAL:
        raise SystemExit(f"expected CSV rows {EXPECTED_TOTAL}, got {csv_rows}")

    by_n = {int(row["n"]): row for row in rows}
    seven_prime_status = {}
    for n in SEVEN_PRIMES:
        row = by_n.get(n)
        if row is None:
            raise SystemExit(f"seven-prime row missing: {n}")
        seven_prime_status[str(n)] = {
            "claim_tier": row.get("claim_tier"),
            "alg_rank_method": row.get("alg_rank_method"),
            "alg_rank_exact_known": row.get("alg_rank_exact_known"),
            "alg_rank_exact": row.get("alg_rank_exact"),
            "second_independent_point_certified": row.get("second_independent_point_certified"),
            "promoted_in_milestone": row.get("promoted_in_milestone"),
        }

    files = [DATA_JSON, DATA_CSV, VALIDATION]
    manifest_lines = []
    for path in files:
        manifest_lines.append(f"{sha256_file(path)}  {path.relative_to(ROOT)}")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "MANIFEST_v0_5.sha256").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    ingest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "state": "State A infrastructure validation only",
        "total_rows": EXPECTED_TOTAL,
        "by_tier": by_tier,
        "csv_rows": csv_rows,
        "seven_prime_status": seven_prime_status,
        "files": {str(path.relative_to(ROOT)): sha256_file(path) for path in files},
    }
    (OUT / "v0_5_ingest_report.json").write_text(json.dumps(ingest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    claim_manifest = [
        "# v0.5 Claim Manifest",
        "",
        "State A infrastructure validation only.",
        "No M6 execution is claimed.",
        "No gate is marked pass.",
        "No claim is promoted.",
        "",
        f"- total_rows: {EXPECTED_TOTAL}",
        f"- H-E1-alg: {by_tier.get('H-E1-alg')}",
        f"- H-E2: {by_tier.get('H-E2')}",
        "",
        "## Seven-prime status",
        "",
    ]
    for n in SEVEN_PRIMES:
        claim_manifest.append(f"- {n}: {seven_prime_status[str(n)]}")
    (OUT / "v0_5_claim_manifest.md").write_text("\n".join(claim_manifest) + "\n", encoding="utf-8")
    (OUT / ".completed").write_text("completed\n", encoding="utf-8")
    print("m6_0_freeze_v0_5: PASS")
    print(f"total_rows={EXPECTED_TOTAL}")
    print(f"by_tier={by_tier}")
    print(f"seven_prime_status={json.dumps(seven_prime_status, sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

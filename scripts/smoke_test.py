#!/usr/bin/env python3
"""Smoke test for the State A BSD v0.5 payload import."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_JSON = ROOT / "data" / "v0.5" / "bsd_dataset_v0_5.json"
VALIDATION = ROOT / "reports" / "v0.5" / "bsd_dataset_v0_5_validation.json"
ADAPTER = ROOT / "proof-adapter.json"


def ensure_payload() -> None:
    if DATA_JSON.exists() and VALIDATION.exists():
        return
    subprocess.run(["python3", "scripts/restore_v0_5_payload.py"], cwd=ROOT, check=True)


def main() -> int:
    ensure_payload()
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
    assert data["total_rows"] == 608
    assert data["by_tier"] == {"H-E1-alg": 426, "H-E2": 182}
    claims = {claim["claim_id"]: claim for claim in adapter["claims"]}
    m6 = claims["BSD-M6-002-four-descent-named-primes"]
    assert m6["state"] == "draft"
    assert m6["severity"] == "E7"
    for gate in adapter["gates"]:
        assert gate["status"] != "pass", gate
    print("smoke_test.py: PASS")
    print("total_rows=608")
    print("by_tier={'H-E1-alg': 426, 'H-E2': 182}")
    print("state_a_adapter_posture=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Pre-flight tests for M6 target extraction.

These tests are intentionally strict. They should pass before M6.1 runs and
fail loudly if the v0.3.1-normalized baseline, audit-correction block, or
M6 target row state has not been imported correctly.
"""

import json
from pathlib import Path


TARGETS = {257, 313, 353, 457}
RANK_2_UNCONDITIONAL = {41, 137, 761}
RANK_1_UNCONDITIONAL_SET = {
    5,
    7,
    13,
    23,
    29,
    31,
    71,
    109,
    149,
    151,
    239,
    509,
    709,
    751,
}


DATASET = Path("data/v0.3.1/bsd_dataset_v0_3_1.json")
VALIDATION = Path("reports/v0.3.1/bsd_dataset_v0_3_1_validation.json")


def _rows():
    return json.loads(DATASET.read_text())


def test_baseline_row_count():
    rows = _rows()
    assert len(rows) == 608


def test_targets_present_and_unresolved():
    rows = _rows()
    by_n = {r["n"]: r for r in rows}
    for n in TARGETS:
        assert n in by_n, f"target {n} missing from baseline"
        r = by_n[n]
        assert r.get("evidence_class") == "E1", (
            f"target {n} expected E1, got {r.get('evidence_class')}"
        )
        assert r.get("certified_status") == "congruent_unconditional", (
            f"target {n} should be explicit-point E1 before M6; got {r.get('certified_status')}"
        )
        assert r.get("explicit_point_x") is not None, (
            f"target {n} should carry M4 explicit point"
        )
        assert r.get("explicit_point_y") is not None, (
            f"target {n} should carry M4 explicit point"
        )
        assert r.get("rank_lower_bound") == 1, (
            f"target {n} should inherit rank lower bound 1"
        )
        assert r.get("rank_upper_bound") is None, (
            f"target {n} should remain exact-rank unresolved before M6"
        )


def test_rank_2_reference_set_present():
    rows = _rows()
    by_n = {r["n"]: r for r in rows}
    for n in RANK_2_UNCONDITIONAL:
        assert n in by_n
        assert by_n[n].get("evidence_class") == "E1"
        assert by_n[n].get("explicit_point_x") is not None


def test_rank_1_reference_set_present():
    rows = _rows()
    by_n = {r["n"]: r for r in rows}
    missing = sorted(n for n in RANK_1_UNCONDITIONAL_SET if n not in by_n)
    assert not missing, f"rank-1 reference rows missing from baseline: {missing}"


def test_audit_correction_present():
    val = json.loads(VALIDATION.read_text())
    assert "audit_correction" in val, "v0.3.1 must carry audit_correction"
    ac = val["audit_correction"]
    fp = ac.get("false_positives_caught", [])
    assert 313 in fp, "p=313 false positive must be carried forward"
    assert 353 in fp, "p=353 false positive must be carried forward"


def test_no_v0_6_files_yet():
    assert not Path("data/v0.6").exists(), (
        "M6 promotion files must not exist before M6.0 runs"
    )
    reports = Path("reports/v0.6")
    assert not reports.exists() or not list(reports.glob("m6.*")), (
        "M6 stage outputs must not exist before M6.0 runs"
    )

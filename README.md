# BSD Program — M6 Pre-Execution Scaffolding (v0.3.2)

This is the **authoritative SocioProphet BSD Proof Program repository**.

Current authoritative repository:

```text
SocioProphet/bsd-proof-program
```

The uploaded handoff archive is:

```text
bsd-m6-scaffolding-v0.3.2.zip
sha256: 41990051925e4b04e22e0b50f7be01cd8a6c5b87894ee354a1bc696112a5ad1e
size:   575491 bytes
```

This branch is the GitOps import lane for the v0.3.2 M6 pre-execution scaffolding baseline.

Pre-execution scaffolding for **Milestone 6 (M6): four-descent on unresolved prime rows {257, 313, 353, 457}** of the BSD program.

This tranche contains type contracts, runbooks, tests, audit documentation, and canonical inherited v0.5 data. **No mathematics is performed here.** The actual M6 descent execution (M6.3 onward) requires PARI/Cremona/Magma engines and runs in a separate environment.

---

## Status

| Tranche | Status | Mathematics added |
|---|---|---|
| v0.5 inherited | Canonical baseline | existing |
| v0.3.2 handoff | M6 pre-execution scaffolding | none — documentation, schema, tests |
| v0.6.0 next | M6.0 → M6.8 execution | TBD per outcome |

---

## Local verification already performed from uploaded archive

The uploaded archive was extracted and tested before repo sync planning.

```bash
python3 scripts/smoke_test.py
python3 -m py_compile m6/models/m6_v0_6_models.py m6/scripts/m6_0_freeze_v0_5.py scripts/smoke_test.py tests/test_m6_targets.py
pytest -q tests/test_m6_targets.py
python3 -m m6.scripts.m6_0_freeze_v0_5
```

Observed local results:

```text
smoke_test.py: PASS
py_compile: PASS
pytest tests/test_m6_targets.py: 66 passed in 0.26s
m6_0_freeze_v0_5: PASS
```

M6.0 freeze emitted:

```text
reports/v0.6/m6.0/MANIFEST_v0_5.sha256
reports/v0.6/m6.0/v0_5_ingest_report.json
reports/v0.6/m6.0/v0_5_claim_manifest.md
reports/v0.6/m6.0/.completed
```

Generated M6.0 outputs are not part of the initial handoff baseline unless explicitly committed in a post-freeze tranche.

---

## Required repository layout after full import

```text
.
├── README.md
├── AGENTS.md
├── RELEASE_NOTES_v0_3_2.md
├── PROGRAM_LOG.md
├── HANDOFF_VERIFICATION.md
├── INTEGRITY.sha256
├── Makefile
├── requirements.txt
├── pyproject.toml
├── .github/workflows/validate.yml
├── data/v0.5/
├── docs/audit/
├── docs/runbooks/
├── docs/specs/
├── m6/models/
├── m6/scripts/
├── reports/v0.5/
├── scripts/
└── tests/
```

The archive root `bsd-m6-scaffolding-v0.3.2/` should not remain nested after import; its contents should become repo-root contents.

---

## What v0.3.2 delivers

### Pydantic type contract

`m6/models/m6_v0_6_models.py` is the type contract for v0.6 row certificates. It enforces design invariants including:

- M6 targets are exactly `{257, 313, 353, 457}`.
- Each target is prime and congruent to 1 modulo 8.
- Canonical rationals have `gcd = 1` and positive denominator.
- Known points are recomputed on-curve.
- Torsion images are stored as evaluated integers, not symbolic placeholders.
- Torsion orbits are recomputed from descent images.
- p=313 and p=353 M5.1 candidates must classify as `torsion_translate`.
- M6 exact-rank promotion cannot use BSD, parity, or Sha-finiteness.
- `claim_tier` is locked at `H-E1-alg` for unconditional M6 outputs.
- `row_hash` is SHA-256 of canonical JSON of all other fields.

### M6.0 hash-freeze script

`m6/scripts/m6_0_freeze_v0_5.py` is the executable M6.0 runbook. It:

- verifies all v0.5 inputs exist and are readable;
- hashes each input file in file-name-sorted SHA-256 order;
- verifies dataset structure: 608 rows, by-tier counts `{H-E1-alg: 426, H-E2: 182}`;
- hashes the `audit_correction` block;
- verifies the four M6 target P1 points are on-curve with correct descent images;
- confirms no v0.6 files exist before freeze;
- writes the M6.0 manifest artifacts under `reports/v0.6/m6.0/`.

### Pre-flight tests

`tests/test_m6_targets.py` is the pytest suite that must pass before M6.1 starts. It tests:

- v0.5 dataset wrapper structure and canonical counts;
- M6 target rows in expected state;
- rank-2 and rank-1 unconditional sets;
- M5.1 false-positive arithmetic and torsion-orbit membership;
- descent-image arithmetic against the spec table;
- no v0.6 leakage from earlier partial runs.

---

## What this tranche does not do

- no descent computation;
- no second-point search extension;
- no dataset promotion;
- no M6.7 validation gate execution;
- no final M6.8 report;
- no change to the v0.5 row state;
- no new mathematical claim.

M6.3 onward requires PARI/GP, Cremona/mwrank, Magma, or equivalent reviewed engine surfaces and is outside this sync tranche.

---

## Dependencies

```text
python >= 3.10
pydantic >= 2.0
pytest >= 7.0
```

CI system tools:

```text
pdftotext / poppler-utils
sha256sum
```

Network access is not required for v0.3.2 validation.

---

## GitOps status

The GitHub connector can update UTF-8 files and issue/PR metadata. It cannot directly push local binary/PDF/archive bytes from `/mnt/data` into GitHub as native binary paths. Full path-preserving import of all extracted archive files, including PDFs and the large canonical JSON dataset, should be completed by a normal git push from a local checkout or another binary-capable GitHub path.

See:

```text
IMPORT_STATUS.md
LOCAL_SYNC_COMMANDS.md
```

for the execution status and exact local commands for the final binary-capable push if needed.

---

## Tracker

Authoritative import tracker:

```text
https://github.com/SocioProphet/bsd-proof-program/issues/1
```

# BSD v0.3.2 Import Status

Branch: `m6-scaffolding-v0.3.2-sync`  
Tracker: #1  
Authoritative repo: `SocioProphet/bsd-proof-program`

## Source archive

```text
file:   bsd-m6-scaffolding-v0.3.2.zip
sha256: 41990051925e4b04e22e0b50f7be01cd8a6c5b87894ee354a1bc696112a5ad1e
size:   575491 bytes
```

## Local validation performed from uploaded archive

The archive was extracted under `/tmp/bsd_sync/bsd-m6-scaffolding-v0.3.2` and validated before sync planning.

```text
python3 scripts/smoke_test.py                    PASS
python3 -m py_compile ...                        PASS
pytest -q tests/test_m6_targets.py               66 passed in 0.26s
python3 -m m6.scripts.m6_0_freeze_v0_5            PASS
```

M6.0 freeze emitted:

```text
reports/v0.6/m6.0/MANIFEST_v0_5.sha256
reports/v0.6/m6.0/v0_5_ingest_report.json
reports/v0.6/m6.0/v0_5_claim_manifest.md
reports/v0.6/m6.0/.completed
```

Those generated outputs are validation products and should not be committed as part of the initial v0.3.2 handoff baseline unless explicitly promoted in a post-freeze tranche.

## Current sync state

The repository has been marked as the authoritative BSD Program repo and tracker #1 records the import plan.

This branch currently contains the authoritative README/import-control material. Full byte-for-byte archive expansion still needs a binary-capable git push because the GitHub connector path available in this session can update UTF-8 files and metadata, but cannot directly push native local binary/PDF/archive bytes from `/mnt/data` into GitHub with preserved paths.

## Required final import state

The archive root `bsd-m6-scaffolding-v0.3.2/` must be flattened into repo root. Required paths include:

```text
.github/workflows/validate.yml
.gitignore
AGENTS.md
HANDOFF_VERIFICATION.md
INTEGRITY.sha256
Makefile
PROGRAM_LOG.md
README.md
RELEASE_NOTES_v0_3_2.md
data/v0.5/bsd_dataset_v0_5.csv
data/v0.5/bsd_dataset_v0_5.json
data/v0.5/second_gen_extended_search.json
data/v0.5/second_generator_search.json
data/v0.5/workstream_h_308_vec_results.json
data/v0.5/workstream_h_53_rows_consolidated.json
data/v0.5/workstream_h_second_generators.json
docs/audit/53_rows_resolution.md
docs/audit/BSD_53_Rows_Resolution.pdf
docs/audit/PROJECT_AUDIT_FINDINGS.md
docs/runbooks/M6_0_FIRST_ACTION_RUNBOOK.md
docs/specs/BSD_Program_Lane_v0_2.pdf
docs/specs/BSD_Program_Lane_v0_2_0.pdf
docs/specs/BSD_Program_Lane_v0_2_1.pdf
docs/specs/M6_FOUR_DESCENT_SPEC_v0_3.pdf
docs/specs/M6_FOUR_DESCENT_SPEC_v0_3_1.md
m6/__init__.py
m6/models/__init__.py
m6/models/m6_v0_6_models.py
m6/scripts/__init__.py
m6/scripts/m6_0_freeze_v0_5.py
pyproject.toml
reports/v0.5/bsd_dataset_v0_5_validation.json
requirements.txt
scripts/smoke_test.py
tests/__init__.py
tests/test_m6_targets.py
```

## Claim boundary

This sync is baseline capture only. It adds no M6 descent execution and no new mathematical result. M6.1 may only start after full import and validation are observed.

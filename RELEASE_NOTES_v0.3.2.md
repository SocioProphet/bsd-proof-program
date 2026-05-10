# Release Notes — v0.3.2

## Status

Pre-execution scaffolding for M6 four-descent execution. No new mathematics. No row-state changes. No promotions.

## Inherits from v0.3.1-normalized

- 608 rows, 307 E1, 301 E2.
- v0.3.1 downstream-count warning for later v0.4/v0.5 aggregate summaries.
- M6 target identities `{257, 313, 353, 457}` remain unchanged.
- Failed M3 L-value and pairwise-Hilbert descent engines remain quarantined.

## Adds

- `docs/specs/M6_FOUR_DESCENT_SPEC_v0_3_1.md` — load-bearing tightenings to the M6 v0.3 spec.
- `m6/models/m6_v0_6_models.py` — Pydantic v0.6 row certificate model.
- `docs/runbooks/M6_0_FIRST_ACTION_RUNBOOK.md` — line-by-line procedure for M6.0 hash-freeze.
- `tests/test_m6_targets.py` — pre-flight tests asserting baseline state for M6.1.

## Does not add

- M6.0 outputs.
- M6.1 target extractor output.
- Any `data/v0.6/` dataset file.
- Any new claim about any row.

## Open items for v0.3.3

1. Reconcile downstream count check: determine whether the later `426 E1 / 182 E2` split re-derives cleanly from the corrected `307 E1 / 301 E2` baseline plus the actual M5 promotion set.
2. Decide whether the M6 inherited slot name remains `v0_5_inherited` permanently or is renamed after M6.
3. Import or regenerate full binary PDF specs if GitHub connector-only text import is insufficient.

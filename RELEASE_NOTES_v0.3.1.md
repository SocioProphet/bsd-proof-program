# Release Notes — v0.3.1-normalized

Milestone 4 resolved all 53 squarefree `n <= 1000` in the `(Tunnell satisfied, root_number = +1)` cell by explicit non-torsion rational points.

## Normalized dataset transition

Raw M4 reported `E1=300`, `E2=308`, but that omitted the seven v0.2 explicit-point rows. v0.3.1 is the corrected baseline:

- E1: 254 -> 307
- E2: 354 -> 301
- Total rows: 608
- Contradictions: 0

## Downstream tranche implication

Any downstream tranche quoting v0.4/v0.5 aggregate counts must re-derive its count pedigree from the corrected v0.3.1 baseline. In particular, the later `426 E1 / 182 E2` split is not trusted until it is reconciled against `307 E1 / 301 E2` plus the actual M5 promotion set. M6 target selection is unaffected because M6 is keyed to the row identities `{257, 313, 353, 457}`, not to the aggregate v0.5 count.

## Boundary

This release does not prove BSD. It promotes specific congruent-number rows by explicit rational points and preserves conditional labels where proof dependencies remain.

## Validation

```bash
python3 scripts/build_v0_3_1.py
python3 tests/test_bsd_dataset_v0_3_1.py
```

# Release Notes — v0.3.1-normalized

Milestone 4 resolved all 53 squarefree `n <= 1000` in the `(Tunnell satisfied, root_number = +1)` cell by explicit non-torsion rational points.

## Normalized dataset transition

Raw M4 reported `E1=300`, `E2=308`, but that omitted the seven v0.2 explicit-point rows. v0.3.1 is the corrected baseline:

- E1: 254 -> 307
- E2: 354 -> 301
- Total rows: 608
- Contradictions: 0

## Boundary

This release does not prove BSD. It promotes specific congruent-number rows by explicit rational points and preserves conditional labels where proof dependencies remain.

## Validation

```bash
python3 scripts/build_v0_3_1.py
python3 tests/test_bsd_dataset_v0_3_1.py
```

# BSD Proof Program

Evidence-gated BSD research-program lane for the congruent-number elliptic-curve family

```text
E_n : y^2 = x^3 - n^2 x,   n squarefree, 1 <= n <= 1000.
```

This repository is a research-program archive and reproducibility surface. It is not a proof of BSD, not a Clay-prize submission, and not an ECC/key-breaking project.

## Canonical baseline

Current canonical dataset target: `data/v0.3.1/bsd_dataset_v0_3_1.{json,csv}`.

The v0.3.1 normalization preserves the Milestone 2 explicit-point rows and the Milestone 4 explicit-point rows:

| class | count | meaning |
|---|---:|---|
| E1 | 307 | theorem-grade rows: 247 Tunnell obstructions + 60 explicit congruent points |
| E2 | 301 | conditional rows: Tunnell equality still conditional on weak BSD unless independently certified |
| total | 608 | squarefree `n <= 1000` |
| contradictions | 0 | no Tunnell/root-number structural contradiction |

## What Milestone 4 proves

Milestone 4 resolves all 53 rows in the `(Tunnell satisfied, root_number = +1)` cell by explicit non-torsion rational points. Each point is verified on the curve and converts to a rational right triangle of area `n`. Hence all 53 are unconditionally congruent numbers.

The exact-rank-2 statement for the seven primes `{41, 137, 257, 313, 353, 457, 761}` remains parity-conditional / Sha-finiteness-conditional until a second independent generator, 4-descent certificate, or equivalent closure is added.

## Important correction from raw Milestone 4

The raw Milestone 4 ledger reported `E1=300`, `E2=308`. That drops the seven v0.2 explicit-point rows `{5,6,7,14,15,21,22}`. The normalized ledger is:

```text
E1 = 247 + 7 + 53 = 307
E2 = 608 - 307 = 301
```

See `docs/patch-notes/v0_3_1_normalization_notes.md`.

## Validate

After importing the full local seed/data artifacts, run:

```bash
python3 tests/test_bsd_dataset_v0_3_1.py
```

Expected output:

```text
v0.3.1 dataset integrity passed: 608 rows, E1=307, E2=301, all explicit points/triangles verified
```

## Repository layout

```text
data/v0.3.1/                      normalized canonical dataset
data/v0.3.0-raw/                  raw Milestone 4 import, retained for provenance
reports/v0.3.1/                   validation and Workstream H search report
docs/specs/                       v0.1 and v0.2 program specifications
docs/milestones/                  M3 snapshot and original M4 resolution document
docs/patch-notes/                 v0.3.1 normalization note
scripts/                          normalization and Workstream H scripts
tests/                            dataset-integrity tests
```

## Next work

1. Close the seven-prime exact-rank target by 4-descent, Heegner-point methods, or explicit second generators.
2. Extend Workstream H to the remaining 301 E2 rows.
3. Add exact Selmer/descent machinery after replacing the failed pairwise Hilbert-symbol test with joint square-class enumeration.
4. Keep the failed M3 L-value and 2-descent engines quarantined until validation passes.

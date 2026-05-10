# BSD Program Lane — Program Log

Continuous document. Markdown source is the source of truth; PDFs in `docs/` are snapshots or historical program specifications.

## Quick-reference state

| Item | Value |
|---|---|
| Canonical repo baseline | v0.3.1-normalized |
| Canonical dataset | `data/v0.3.1/bsd_dataset_v0_3_1.{json,csv}` |
| Squarefree rows | 608, for `1 <= n <= 1000` |
| Theorem-grade rows (E1) | 307 = 247 Tunnell obstructions + 60 explicit congruent points |
| Conditional rows (E2) | 301 |
| Open contradictions | 0 |
| Last milestone | Milestone 4 normalized import |

## Changelog

### v0.3.1 — Normalized Milestone 4 baseline

Status: canonical repository baseline.

Milestone 4 correctly resolved all 53 rows in the `(Tunnell satisfied, root_number = +1)` cell by explicit non-torsion rational points. The raw Milestone 4 count ledger accidentally reverted to the v0.1 baseline and dropped the seven v0.2 explicit-point rows. This normalization preserves both the v0.2 and M4 explicit-point promotions.

Correct count transition:

```text
v0.2:     E1=254, E2=354
M4 adds:  +53 E1 promotions
v0.3.1:  E1=307, E2=301
```

Validation: `tests/test_bsd_dataset_v0_3_1.py` verifies 608 rows, E1/E2 counts, all explicit points on-curve, and all triangles Pythagorean with area `n`.

### Milestone 4 — Resolution of the 53 interesting rows

Status: mathematically accepted; raw count ledger corrected by v0.3.1.

All 53 squarefree `n <= 1000` in the `(Tunnell satisfied, root_number = +1)` cell have explicit non-torsion rational points on `E_n`. Search bounds: `D <= 50`, `|c| <= 500000`. Workstream H report retained at `reports/v0.3.1/workstream_h_53_rows_consolidated.json`.

The exact-rank-2 statement for the seven primes `{41,137,257,313,353,457,761}` remains parity-conditional / Sha-finiteness-conditional.

### Milestone 3 — EC-MIRROR-001 + 2-descent attempt

Status: partial; engines built but validation failed; results not promoted.

Reusable correct components:

- CM formula for `a_p(E_1)`, validated against direct point count.
- Quadratic twist formula `a_p(E_n) = (n/p) a_p(E_1)`, validated by direct point count.
- Hilbert symbol primitives at `{infinity, 2, odd p}`.
- Engine architecture and validation harnesses.

Known failures:

- L-value engine returned nonzero values for known rank-2 cases `E_34`, `E_41`.
- Pairwise Hilbert-symbol descent test was necessary but not sufficient; replacement must use joint square-class enumeration.

### v0.2 — Workstream D foundational + small Heegner bridge

- Root number `epsilon(E_n)` computed via Birch–Stephens (`n mod 8`) formula.
- Tunnell/root-number grid had zero contradictions across 608 rows.
- Seven explicit non-torsion points attached for `n in {5,6,7,14,15,21,22}`.
- Counts: 247 noncongruent unconditional, 7 explicit congruent, 301 parity-conditional congruent, 53 even-rank-or-rank-0 conditional.

### v0.1 — Tunnell engine + first dataset

- Tunnell ternary-form engine implemented and validated against Koblitz's table for squarefree `n <= 50`.
- Dataset for squarefree `n <= 1000`: 608 rows.
- Initial counts: 247 obstruction (E1 noncongruent), 361 conditional-congruent (E2).

## Cross-validation grids

### Tunnell × root number

|                          | epsilon = +1 | epsilon = -1 |
|--------------------------|-------------:|-------------:|
| Tunnell obstruction      | 247          | 0            |
| Tunnell satisfied        | 53           | 308          |

The zero cell remains empty.

## Active workstreams

- A — Formal Foundation Layer: stable.
- B — Congruent-Number Laboratory: dataset at `N=1000` normalized.
- C — Descent and Selmer Machinery: experimental engine quarantined; joint square-class replacement pending.
- D — Analytic Rank and L-Function Layer: root-number layer stable; L-value engine quarantined.
- E — BSD Leading-Term Layer: spec-stable, not executed.
- F — Obstruction Discipline: continuously active.
- G — Function-Field Shadows: planned.
- H — Heegner / Kolyvagin / point-search lane: M4 resolved 53 rows; remaining 301 E2 rows pending.
- I — Statistical Baseline: planned.

## Reproducibility

```bash
python3 tests/test_bsd_dataset_v0_3_1.py
```

Historical raw Milestone 4 data is retained under `data/v0.3.0-raw/`. Canonical consumers should use `data/v0.3.1/`.

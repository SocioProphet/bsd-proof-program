# BSD Program Lane v0.2.1 — Capture Manifest

Status: capture manifest for uploaded tranche artifacts. This file records the exact files received in chat, their SHA-256 digests, their sizes, the tranche claims, and the remaining import boundary.

This capture is additive. It does not revise the M6 v0.3.2 pre-execution scaffolding baseline and does not perform any descent or BSD proof computation.

## Source artifacts received

| File | Size bytes | SHA-256 | Capture status |
|---|---:|---|---|
| `BSD_Program_Lane_v0_2_1.pdf` | 24368 | `9a058d3f464654fee3e49c00ce89b23adf0ec90680975d980440ae522f414896` | native PDF received in chat; hash recorded here; binary-native repo import still requires binary-capable path |
| `bsd_registry_v021_stats.json` | 2871 | `4cc847a7122c60f6e0e5237d43c03e4c1040efb5fdedc5eafda18e1d27bf57ef` | small UTF-8 stats JSON captured in this branch as `reports/v0.2.1/bsd_registry_v021_stats.json` |
| `bsd_registry_v021.csv` | 126548 | `5cc476c1c1d6649858fc0b0a0de5433ee82df47f1dc672039ecd56e296a4346c` | native CSV received in chat; hash/schema/row count recorded here; full path-preserving import remains pending |
| `bsd_registry_v021.json` | 1230392 | `afe0f920625b882a36bf35d5a1490d6b24dc557484a4f860ac03ca9aba5324f4` | native full JSON received in chat; hash/schema/row count recorded here; full path-preserving import remains pending |

## Tranche identity

```text
lane: BSD Program Lane
version: v0.2.1
family: congruent_number
equation: y^2 = x^3 - n^2 x
N_0: 1000
schema_version: v0.2.1
```

Working-draft boundary from the PDF: no theorem of the Birch and Swinnerton-Dyer conjecture is claimed. This tranche populates Lane L1 for the congruent-number family with `N_0 = 1000`, runs the C5 five-fold consistency gate at every row, and leaves L4/L5 closed for later tranches.

## Executive result captured

The uploaded v0.2.1 document reports:

- L1 closes for `n <= 1000`.
- Corrected C5 gate passes `1000 / 1000` rows.
- There are `608` squarefree rows and `392` non-squarefree rows.
- Tunnell + Coates-Wiles separate rows into `432` with `L(E_n, 1) != 0` and `568` with `L(E_n, 1) = 0`.
- Root-number distribution is `503` with `epsilon = +1` and `497` with `epsilon = -1`.
- First 50 squarefree congruent numbers match OEIS A003273 restricted to squarefree entries.
- `53` squarefree rows with `(epsilon = +1, L = 0)` are flagged as rank-at-least-2 candidates for v0.2.2.
- The smallest five rank-at-least-2 candidates are `34, 41, 65, 137, 138`.
- A v0.2.1.0 buggy implementation produced `203` C5 failures; the v0.2.1.1 corrected implementation restored `1000 / 1000` C5 pass.

## Stats JSON aggregate

The received `bsd_registry_v021_stats.json` reports:

```json
{
  "N_0": 1000,
  "total_rows": 1000,
  "squarefree_count": 608,
  "non_squarefree_count": 392,
  "L_nonzero_count": 432,
  "L_zero_count": 568,
  "eps_plus_count": 503,
  "eps_minus_count": 497,
  "c5_pass_count": 1000,
  "c5_fail_count": 0,
  "rank_geq_2_candidate_count": 53,
  "squarefree_congruent_count_under_N0": 361
}
```

## CSV registry verification

The received CSV has:

```text
rows including header: 1001
data rows: 1000
columns: 26
```

Header:

```text
n,squarefree_part,is_squarefree,j_invariant,discriminant,conductor,bad_primes,root_number,tunnell_label,A_n,B_n,A_minus_2B,goldfeld_prediction,tamagawa_at_2,a_3,a_5,a_7,a_11,a_13,a_17,a_19,c5_hasse_ok,c5_tunnell_eps_ok,c5_cm_inert_ok,c5_all_pass,c5_flags
```

First data row, compact:

```text
n=1, squarefree_part=1, is_squarefree=True, j_invariant=1728, discriminant=64, conductor=32, bad_primes=2, root_number=1, tunnell_label=L_nonzero, A_n=2, B_n=2, A_minus_2B=-2
```

## Full JSON registry verification

The received full JSON has:

```text
schema_version: v0.2.1
family: congruent_number
equation: y^2 = x^3 - n^2 x
N_0: 1000
row_count: 1000
len(rows): 1000
```

First row compact verification:

```text
n=1
is_squarefree=true
j_invariant=1728
cm_by=Z[i]
root_number=1
tunnell_status=["L_nonzero", 2, 2, -2]
conductor=32
c5_gate.all_pass=true
```

## Rank-at-least-2 candidates

Captured from the stats JSON:

```text
34, 41, 65, 137, 138, 145, 154, 161, 194, 210, 219, 226, 257, 265, 291, 299, 313, 323, 330, 353, 371, 386, 395, 410, 426, 434, 442, 457, 465, 505, 514, 546, 561, 602, 609, 651, 658, 674, 689, 721, 723, 731, 761, 777, 793, 866, 889, 890, 905, 915, 985, 987, 995
```

Count: `53`.

## First 50 squarefree congruent numbers under N0

Captured from the stats JSON:

```text
5, 6, 7, 13, 14, 15, 21, 22, 23, 29, 30, 31, 34, 37, 38, 39, 41, 46, 47, 53, 55, 61, 62, 65, 69, 70, 71, 77, 78, 79, 85, 86, 87, 93, 94, 95, 101, 102, 103, 109, 110, 111, 118, 119, 127, 133, 134, 137, 138, 141
```

## Claim boundary

This capture records the uploaded v0.2.1 tranche and its registry outputs. It does not certify BSD for any curve. It does not verify analytic-rank-equals-algebraic-rank for any individual `n`. It does not produce Heegner points. It does not certify BSD-II leading-term formulas. It records the uploaded tranche statement that the `432` squarefree `L != 0` rows are rigorously rank 0 by prior-art Tunnell + Coates-Wiles in the CM congruent-number family, while the `568` `L = 0` squarefree rows remain conditional/predictive as stated in the tranche.

## Remaining import boundary

The available GitHub connector path can reliably add UTF-8 text files and tracker metadata. It cannot directly push native local binary/PDF bytes from `/mnt/data` as repository-native files. The small stats JSON has been captured as UTF-8. The PDF, CSV, and full JSON are hash-locked here and available from the chat upload context; full path-preserving raw import should be completed by a binary-capable git checkout or another file-upload lane.

Recommended final native paths:

```text
reports/v0.2.1/BSD_Program_Lane_v0_2_1.pdf
data/v0.2.1/bsd_registry_v021.csv
data/v0.2.1/bsd_registry_v021.json
reports/v0.2.1/bsd_registry_v021_stats.json
reports/v0.2.1/ARTIFACTS.sha256
```

## Next admissible tranche

Per the uploaded document, the next admissible tranche is v0.2.2: L4 chi_p certificate execution on the rank-0 sub-population. L5 remains closed until v0.2.3; L2/L3 open later by gate sequencing.

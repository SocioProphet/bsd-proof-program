# Claim Boundary

This repository is an internal research-program lane toward BSD for the congruent-number family. It is not a proof of BSD, not a Clay-prize submission, and not an ECC/key-breaking project.

## Current canonical state

- Baseline family: `E_n: y^2 = x^3 - n^2 x`, squarefree `1 <= n <= 1000`.
- Canonical dataset: `data/v0.3.1/bsd_dataset_v0_3_1.{json,csv}`.
- E1 theorem-grade rows: 307.
- E2 conditional rows: 301.
- Open contradictions: 0.

## Promoted theorem-grade content

1. Tunnell-obstruction rows are noncongruent by the unconditional direction of Tunnell's theorem and the congruent-number correspondence.
2. The 7 v0.2 explicit-point rows `{5,6,7,14,15,21,22}` are congruent by explicit rational right triangles / non-torsion rational points.
3. The 53 Milestone 4 rows in the `(Tunnell satisfied, root_number = +1)` cell are congruent because explicit non-torsion rational points are exhibited and verified.

## Conditional content

1. Tunnell equality implying congruence remains conditional on weak BSD unless an explicit point or independent theorem-grade certificate is attached.
2. Exact rank-2 claims for `{41,137,257,313,353,457,761}` remain parity-conditional / Sha-finiteness-conditional until a second generator, 4-descent certificate, or equivalent independent proof is added.
3. The 301 remaining E2 rows are not theorem-grade congruent rows in this repository baseline.

## Quarantined / experimental content

1. Milestone 3 L-value engine output is not dataset-grade.
2. Milestone 3 pairwise-Hilbert 2-descent output is not dataset-grade.
3. Any file marked `_EXPERIMENTAL` cannot promote a claim.

## Required promotion rule

No result may move from E2/E4/E5 to E1 without an explicit theorem-grade certificate and a validation test.

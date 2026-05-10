# v0.2.1 Registry Construction — Operator Log

Status: historical tranche capture / operator report. This document records the reported v0.2.1 registry-construction pass for the congruent-number family. It is not itself the executable registry artifact, and it does not supersede the v0.3.1-normalized baseline.

## Scope

Registry construction for the congruent-number family

```text
E_n : y^2 = x^3 - n^2 x
```

with `n <= 1000`, including execution of the five-fold consistency gate at every row.

## Reported execution sequence

1. Computational engine was built for row-level registry construction.
2. Initial C5 gate fired 203 mismatches.
3. All 203 mismatches were of one type and were diagnosed as formula bugs, not as mathematical contradictions.
4. Root-number bug was identified using `n=3` as a sanity witness: `n=3` is prime, `n mod 8 = 3`, noncongruent/rank 0, and must have `epsilon(E_n)=+1` in this family. The incorrect complex local-epsilon/Jacobi-symbol formula produced the wrong sign.
5. Root-number computation was reverted to the simple Birch--Stephens `n mod 8` rule for this family.
6. The even-`n` Tunnell formula was also corrected.
7. After formula correction, the C5 gate passed `1000/1000`.
8. Sanity checks were reported as passing against the known congruent-number sequence and LMFDB rank-at-least-2 candidates.

## C5 diagnostic lesson

The initial 203 mismatches are retained as evidence that the consistency gate is doing useful work. The gate caught implementation-level formula defects before they could become dataset claims.

The correct interpretation is:

```text
C5 mismatch spike -> formula implementation fault -> corrected formulas -> C5 pass
```

not:

```text
C5 mismatch spike -> parity contradiction / BSD anomaly
```

## Formula discipline retained

For the congruent-number family, root-number implementation should be based on the Birch--Stephens residue rule:

```text
epsilon(E_n) = +1  for n mod 8 in {1, 2, 3}
epsilon(E_n) = -1  for n mod 8 in {5, 6, 7}
```

For squarefree `n`, residues `{0,4}` do not occur.

Tunnell counts must use the family-specific odd/even forms as fixed in the v0.2 launch specification and Tunnell engine implementation.

## Claim boundary

The reported `1000/1000` gate pass is a registry-engine validation statement, not a proof of BSD. It validates internal consistency of the row registry under the corrected formulas.

## Relationship to v0.3.1-normalized

This tranche is lower in the historical version chain than the current canonical v0.3.1-normalized baseline. The current repo baseline remains:

```text
608 squarefree rows for n <= 1000
E1 = 307
E2 = 301
open contradictions = 0
```

The v0.2.1 operator report is preserved because its bug-and-fix cycle explains why C5 exists and why formula provenance must be explicit.

## Follow-up requirements

1. Attach the executable v0.2.1 registry engine or regenerate it from source.
2. Store the C5 pre-fix mismatch report if available.
3. Store the post-fix `1000/1000` C5 pass report if available.
4. Cite OEIS/LMFDB sanity sources explicitly in a later evidence appendix.
5. Ensure downstream v0.4/v0.5 aggregate counts are recomputed from the v0.3.1-normalized baseline before publication.

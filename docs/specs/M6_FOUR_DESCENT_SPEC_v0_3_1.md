# M6 Four-Descent Specification v0.3.1

Delta document against `M6_FOUR_DESCENT_SPEC_v0_3`. This file applies load-bearing schema tightenings and documentation corrections needed before M6 execution. It does not change row identities, mathematical claims, or promotion gates.

## Status

Pre-execution specification patch. No new mathematics. No v0.6 row emission. No promotion.

## Canonical inheritance

M6 remains keyed to the four prime rows:

```text
{257, 313, 353, 457}
```

The corrected baseline for pre-execution work is v0.3.1-normalized:

```text
608 rows; E1=307; E2=301; contradictions=0.
```

The older M6 field name `v0_5_inherited` is retained as a contract slot name. It refers to the M6 inheritance block, not necessarily to a filename. The block must carry the v0.3.1 baseline hashes and the audit-correction hash.

## 1. Engine-runs / four-descent consistency rule

When `four_descent.attempted == true`, all of the following are mandatory:

1. `four_descent.engine_runs` is non-empty.
2. At least one `engine_runs[*].role == "four_descent"`.
3. `four_descent.primary_engine` is non-null.
4. Exactly one `engine_runs` entry has `role == "four_descent"` and `engine_id == four_descent.primary_engine`.
5. That entry is the primary four-descent source for the row-level outcome.

Failure of any condition makes the row certificate invalid.

## 2. Points-discovered schema reference

`points_discovered` is a list of descent-by-product point certificates. Each element must conform to the §13 descent-by-product schema:

```text
x: rational string
 y: rational string
 source: bounded_search | heegner | four_descent | imported_certificate | manual_review
 on_curve_verified: bool
 torsion_excluded: bool
 independence_status: independent | dependent | not_checked | not_applicable
 verification_notes: string | null
```

A point certificate cannot promote a row unless `on_curve_verified == true` and `torsion_excluded == true`.

## 3. Engine-runs non-empty when four-descent attempted

This is separate from the primary-engine consistency rule. A row may not mark `four_descent.attempted == true` unless an auditable engine-run record exists.

Minimum engine-run fields:

```text
engine_id
engine_name
engine_version
role
status
started_at
completed_at
input_hash
output_hash
log_hash
```

Allowed role values:

```text
four_descent
point_search
independence_check
curve_verification
audit
```

Allowed status values:

```text
success
inconclusive
error
invalidated
```

## 4. Row hash field

Every emitted M6 row certificate must include:

```text
row_hash: sha256(canonical_json(row_without_row_hash))
```

Canonical JSON means:

1. UTF-8.
2. `sort_keys=True`.
3. compact separators `(',', ':')`.
4. no omission of null fields unless the model contract explicitly excludes them.

The writer must compute the hash at write time. The validator must recompute and reject mismatches.

## 5. Singular-engine reference fix in promotion logic

Any reference to “the engine” in §15 promotion logic must be read as “the selected primary four-descent engine run.” If more than one four-descent engine contributes, one must be selected as primary and the others must be represented as corroborating or conflicting evidence.

## 6. Symmetric corroboration rule

Rank-2 and rank-1 closure paths require symmetric corroboration discipline:

- Rank-2 via independent points: verify both points on curve, exclude torsion, and verify independence or provide a cited independence certificate.
- Rank-1 exact via four-descent: verify the descent upper bound and ensure that the explicit point supplies the matching lower bound.
- Conflicts between point-search and descent output produce `rank_still_1_or_2`, `engine_inconclusive`, or `certificate_invalid`; they do not promote.

## 7. Citation note for `e2_rational_dimension`

The field `e2_rational_dimension` is grounded in the full rational 2-torsion of the congruent-number curve family:

```text
E_n(Q)[2] = {O, (0,0), (n,0), (-n,0)} ~= (Z/2Z)^2.
```

The schema should cite the rational torsion structure and the standard torsion classification boundary. In documentation, cite Mazur's torsion theorem and the explicit factorization `x(x-n)(x+n)` for the family.

## 8. Non-effect on M6 target selection

This patch does not alter the target set `{257, 313, 353, 457}`. It only tightens the row-certificate contract that later M6 stages must satisfy.

## 9. Open downstream count audit

The v0.3.1 normalization changes the baseline used by later v0.4/v0.5 aggregate summaries. Any downstream quotation of the `426 E1 / 182 E2` split must be re-derived from the corrected `307 E1 / 301 E2` baseline. M6 is unaffected because M6 operates by target row identity.

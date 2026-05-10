# Workstream H — E1 Certificate Tiering and Reclassification Gate (H-v0.4.2)

Status: audit execution protocol. No row promotes by prose.

This file captures the H-v0.4.2 patch stream for Workstream H. It separates explicit point evidence, algebraic rank-one certification, and analytic/BSD rank-one certification.

## Governing principle

```text
No row promotes by prose.
Every row promotes only across a tier boundary after the required certificates and contradiction checks for that boundary pass.
```

Given only thread-level evidence, the 126 asserted rows remain provisional `H-E1-point_candidate` until the row manifest and row-level certificates are available.

## Tiers

### H-E1-point

Explicit rational point found and verified exactly.

Required:

```yaml
point_certificate.on_curve_verified_exactly: true
point_certificate.non_torsion_verified: true
point_certificate.triangle_reconstructed: true
```

This proves algebraic rank at least 1.

### H-E1-alg

Explicit point plus theorem-grade algebraic upper bound proves Mordell-Weil rank exactly 1.

Required:

```yaml
algebraic_rank_certificate.upper_bound_value: 1
algebraic_rank_certificate.theorem_source: populated
algebraic_rank_certificate.algebraic_rank_status: exactly_1
```

Valid methods include validated 2-Selmer, Monsky, Heath-Brown where row-level hypotheses apply, database-backed certified rank, or other theorem-grade method.

### H-E1-BSD

BSD-rank-one route certified.

Required route A:

```yaml
analytic_rank_certificate.analytic_rank_status: exactly_1
analytic_rank_certificate.interval_excludes_zero: true
```

or route B:

```yaml
analytic_rank_certificate.method: p_converse
analytic_rank_certificate.theorem_hypotheses_logged: true
```

Root number `epsilon = -1` alone certifies only odd analytic rank, not analytic rank exactly 1.

## Schema refinements

### Analytic rank certificate

```yaml
analytic_rank_certificate:
  analytic_rank_status: exactly_1 | not_certified | higher_rank_possible
  method: rigorous_L_derivative | dokchitser_interval | p_converse | parity_only | not_run
  root_number_epsilon: -1 | 1 | unknown
  parity_information:
    analytic_rank_forced_odd: boolean
    analytic_rank_forced_even: boolean
    sufficient_for_exact_rank_1: false
  L_value_or_derivative_interval: string
  error_bound: string
  interval_excludes_zero: boolean
  theorem_hypotheses_logged: boolean
```

`parity_only` means root-number / functional-equation parity was recorded but is insufficient for analytic rank exactly 1.

### Curve consistency

```yaml
curve_consistency:
  conductor: string
  root_number_epsilon: -1 | 1 | unknown
  database_source_kind: lmfdb | cremona_tables | computed_locally | none
  database_version: string | null
  fetched_at: ISO8601 | null
  query_or_script_hash: string | null
  database_match: boolean
  local_factor_check: boolean
```

Free-text source labels such as `online` or `standard tables` are forbidden.

## Duplicate witness policy

```yaml
duplicate_policy:
  equivalence_key:
    - squarefree_n
    - curve_model

  canonical_witness_rule:
    primary: lowest_canonical_height
    tie_break_1: lexicographically_smallest_point_coordinates
    tie_break_2: earliest_source_run_timestamp
    tie_break_3: lowest_artifact_hash_lexicographic

  supplementary_witnesses:
    retained: true
    count_for_promotion: false
    superseded_by: canonical_row_id
    may_be_cited_as_redundant_verification: true

  independence_check:
    required_when_multiple_witnesses_exist: true
    method: height_pairing | saturation | declared_other
    result: dependent | independent | unresolved

  rank_implication:
    if_independent_lower_bound_at_least_2:
      remove_from_E1_stream: true
      route_to: rank_ge_2_or_M4_stream
```

If multiple point certificates exist for the same squarefree `n` and curve model, retain the lowest-height point as canonical and archive the others as supplementary witnesses. If multiple witnesses are independent, the row leaves the E1 stream.

## Parity consistency check

```yaml
contradiction_checks:
  parity_consistency:
    status: pass | fail | unknown
    root_number_epsilon: -1 | 1 | unknown
    analytic_rank_status: exactly_1 | not_certified | higher_rank_possible
    method: rigorous_L_derivative | dokchitser_interval | p_converse | parity_only | not_run
    rule_applied: string
```

Rules:

- `analytic_rank_status: exactly_1` requires `root_number_epsilon: -1`.
- `root_number_epsilon: -1` with `method: parity_only` records odd analytic rank only.
- `root_number_epsilon: +1` is inconsistent with analytic rank exactly 1.
- Unknown root number blocks `H-E1-BSD` unless the analytic certificate supplies a theorem-grade route that implies the correct parity.

## Route-other discipline

```yaml
bsd_chain_status:
  status: H-E1-point | H-E1-alg | H-E1-BSD
  route: explicit_point_only | selmer_cap | analytic_rank_1_GZK | p_converse | other
  sha_claim: none | finite | two_part_finite | conditional
  notes: string

  route_other_justification:
    required_when: route == "other"
    theorem_source: string
    hypotheses_logged: boolean
    reviewer_validated: boolean
    reviewer_id: string
    reviewer_notes_hash: string
```

`route: other` cannot promote a row unless the justification block is fully populated and reviewer validated.

## next_required_certificates

The field is list-valued:

```yaml
next_required_certificates:
  values:
    - point_recheck
    - selmer_cap
    - four_descent
    - rigorous_L_derivative
    - p_converse_hypotheses
    - database_consistency
    - duplicate_resolution
  priority_order:
    - duplicate_resolution
    - point_recheck
    - database_consistency
    - selmer_cap
    - four_descent
    - rigorous_L_derivative
    - p_converse_hypotheses
  blocking:
    - duplicate_resolution
    - point_recheck
```

A blocking certificate must be resolved before downstream certificates are interpreted.

## Tier-boundary execution order

```text
1. Freeze manifest.
2. Resolve duplicates.
3. Run exact point audit.
4. Run point-level contradiction sweep.
5. Promote passing rows to H-E1-point.
6. Populate algebraic certificates.
7. Run algebraic-level contradiction sweep.
8. Promote passing rows to H-E1-alg.
9. Populate analytic / converse certificates.
10. Run analytic-level contradiction sweep.
11. Promote passing rows to H-E1-BSD.
12. Emit final dashboard.
```

This avoids promote-then-demote drift.

## Minimum manifest payload

```yaml
row_id: string
n: integer
curve_model: "E_n: y^2 = x^3 - n^2 x"

point:
  x: rational
  y: rational
  source_run_id: string
  search_height_bound: string | integer
  artifact_hash: string

optional_existing_certificates:
  root_number_epsilon: -1 | 1 | unknown
  conductor: string | null
  database_source_kind: lmfdb | cremona_tables | computed_locally | none
  database_version: string | null
  fetched_at: string | null
  query_or_script_hash: string | null

  algebraic_upper_bound:
    method: two_selmer | monsky | heath_brown | four_descent | database | other | none
    upper_bound_value: integer | null
    certificate_hash: string | null
    theorem_source: string | null

  analytic_certificate:
    method: rigorous_L_derivative | dokchitser_interval | p_converse | parity_only | not_run
    analytic_rank_status: exactly_1 | not_certified | higher_rank_possible
    interval: string | null
    error_bound: string | null
    theorem_hypotheses_hash: string | null
```

Without that manifest, the only honest state is:

```yaml
total_promoted_rows_referenced: 126
status: H-E1-point_candidate
row_level_citable: false
```

## Current thread-level classification

```yaml
retiering_status_from_thread_only:
  total_promoted_rows_referenced: 126
  H-E1-point_candidate: 126
  H-E1-point_citable_row_level: unknown_until_manifest_audit
  H-E1-alg: unknown
  H-E1-BSD: unknown
  H-recheck: unknown

  known_holdouts:
    - n: 157
      status: holdout_tail
      included_in_126: false
```

No row receives `H-E1-alg` or `H-E1-BSD` from thread evidence alone.

## Final dashboard shape

```yaml
summary:
  total_rows: integer
  H-E1-point: integer
  H-E1-alg: integer
  H-E1-BSD: integer
  H-recheck: integer
  point_failures: integer
  missing_algebraic_upper_bound: integer
  parity_only_rows: integer
  analytic_rank_certified_rows: integer
  p_converse_candidate_rows: integer
  contradiction_count: integer
  rows_ready_for_citation: list[row_id]
  rows_needing_certificate: list[row_id]
  rows_demoted_or_recheck: list[row_id]
```

## Citation rule

- `H-E1-point` rows may be cited as explicit non-torsion point rows.
- `H-E1-alg` rows may be cited as unconditional Mordell-Weil rank-one rows.
- `H-E1-BSD` rows may be cited only according to the exact theorem route logged in `bsd_chain_status`.

## Next action

The next unit is certification, not new search:

```yaml
current_patch: H-v0.4.2
status: promoted
next_action_type: execution
next_action: run the 126-row re-tiering audit against the manifest
new_search_allowed_before_audit: false
```

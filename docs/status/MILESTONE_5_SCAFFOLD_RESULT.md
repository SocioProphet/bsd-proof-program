# Milestone 5 Scaffold Result

Date: 2026-05-11
PR: #11
Merge commit: `e874e65780c7b81c3abd0335808d134ce72a7039`

## Result

Milestone 5 scaffold is merged.

The scaffold installs the first controller-routed research surface after proof-apparatus validation. It is deliberately fail-closed: scaffold only, no rank exactness, no second independent point certification, no four-descent execution, no BSD-I/BSD-II/Sha claim, and no adapter claim promotion.

## Added artifacts

- `data/milestone5/m5_four_prime_baseline.json`
- `schemas/milestone5_orbit_candidate.schema.json`
- `scripts/milestone5_orbit_scaffold.py`
- `.github/workflows/milestone-5-orbit-scaffold.yml`
- `proof-adapter.json` claim `BSD-M5-004-orbit-membership-scaffold`

## Observed validation

Both required checks passed on PR #11:

- `Milestone 5 orbit scaffold`: success
- `Proof apparatus continuous validation`: success

The scaffold workflow printed:

```text
milestone5_orbit_scaffold: PASS
target_count=4
event_count=4
distinct_input_digest_count=4
distinct_output_digest_count=4
all_p1_on_curve=True
```

## Target classification

| n | target_class | P1 on curve | requires fresh search/descent | requires orbit-membership filter | second independent point certified | claim promotion allowed |
|---:|---|---|---|---|---|---|
| 257 | no_second_generator_found | true | true | false | false | false |
| 313 | historical_false_positive_requires_orbit_filter | true | false | true | false | false |
| 353 | historical_false_positive_requires_orbit_filter | true | false | true | false | false |
| 457 | no_second_generator_found | true | true | false | false | false |

## Boundary

The scaffold validates inherited P1 points and installs the orbit-membership-aware candidate discipline.

It does not:

- certify rank exactness;
- certify a second independent point;
- run four-descent;
- prove BSD-I;
- prove BSD-II;
- prove Tate-Shafarevich finiteness;
- mark any gate as `pass` in `proof-adapter.json`;
- promote any claim.

## Next executable research step

The next Milestone 5 step is to implement the first controller-routed candidate runner that consumes candidate records conforming to `schemas/milestone5_orbit_candidate.schema.json` and enforces:

- candidate on-curve verification;
- descent-image recording;
- torsion-orbit membership check against P1;
- independence decision only after orbit filtering;
- input/output SHA-256 digests for every checked candidate;
- typed no-result output when search bounds are exhausted.

The first target split remains:

```text
257, 457: extended search / four-descent / Heegner route
313, 353: re-search with orbit-membership filter before independence interpretation
```

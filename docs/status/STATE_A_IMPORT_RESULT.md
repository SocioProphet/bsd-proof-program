# State A Import Result

Date: 2026-05-11
PR: #8
Merge commit: `5e9f86feaeac45c4552904bc1da55305a0855d63`

## Result

State A import is complete.

The BSD v0.5 executable baseline payload was imported through a deterministic packed-text restore path.

## Source payload

```text
source upload: bsd v05 payload.zip
source upload sha256: 666ad565251701b23779c84005de0511eb018b7649bb46635cd9b8775cb0c607
packed tar.gz sha256: 8dd75bf39599d727f1568bfd2d4c998e968b4612242cc53086616dfd9153721a
```

## Imported State A machinery

- `payloads/v0.5/bsd_v05_required_manifest.json`
- `payloads/v0.5/bsd_v05_required_text.tar.gz.b64.part00` through `part04`
- `scripts/restore_v0_5_payload.py`
- `scripts/smoke_test.py`
- `m6/scripts/m6_0_freeze_v0_5.py`
- `.github/workflows/validate-state-a-v05.yml`

## Restored executable baseline

The restore script materializes:

```text
data/v0.5/bsd_dataset_v0_5.csv
data/v0.5/bsd_dataset_v0_5.json
reports/v0.5/bsd_dataset_v0_5_validation.json
```

## Observed validation

PR #8 observed both required checks green:

- `Validate State A v0.5 payload`: success
- `Proof apparatus continuous validation`: success

The State A payload workflow verified:

```text
restore_v0_5_payload: restored_or_checked=3
smoke_test.py: PASS
m6_0_freeze_v0_5: PASS
total_rows=608
by_tier={'H-E1-alg': 426, 'H-E2': 182}
```

## Seven-prime baseline status

The freeze validator printed:

| n | claim_tier | alg_rank_method | alg_rank_exact_known | alg_rank_exact | second_independent_point_certified | promoted_in_milestone |
|---:|---|---|---|---:|---|---:|
| 41 | H-E1-alg | two_indep_points_HB_selmer4 | true | 2 | true | 4 |
| 137 | H-E1-alg | two_indep_points_HB_selmer4 | true | 2 | true | 4 |
| 257 | H-E1-alg | explicit_point_HB_selmer4 | false | null | false | 4 |
| 313 | H-E1-alg | explicit_point_HB_selmer4 | false | null | false | 4 |
| 353 | H-E1-alg | explicit_point_HB_selmer4 | false | null | false | 4 |
| 457 | H-E1-alg | explicit_point_HB_selmer4 | false | null | false | 4 |
| 761 | H-E1-alg | two_indep_points_HB_selmer4 | true | 2 | true | 4 |

## Claim boundary

This import is State A infrastructure only.

It does not claim M6 execution, does not mark gates as passed, does not promote claims, and leaves `BSD-M6-002-four-descent-named-primes` at `draft` / `E7`.

The imported `H-E1-alg` classifications remain inherited evidence until re-attested by controller-routed gates.

## Next step

Candidate 2 is unblocked.

The next work item is to run the positive-path C5 replay against the restored v0.5 baseline and record the result as a proof-apparatus validation artifact.

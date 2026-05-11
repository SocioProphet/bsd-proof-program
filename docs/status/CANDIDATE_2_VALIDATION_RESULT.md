# Candidate 2 Validation Result

Date: 2026-05-11
PR: #9
Merge commit: `cab93b8ad5f9433839c9f7a37e217f475d2ee877`

## Result

Candidate 2 passed and is merged.

Candidate 2 ran a positive-path replay against the restored BSD v0.5 baseline. It validated the controller-visible v0.5 baseline and emitted digest-addressed row-level ledger events.

## Observed checks

Both required workflows passed on PR #9:

- `Candidate 2 C5 replay`: success
- `Proof apparatus continuous validation`: success

The replay restored the State A v0.5 payload, verified restored hashes, ran the positive replay, printed artifacts to the job log, and uploaded `candidate-2-c5-replay-artifacts`.

## Positive replay output

Observed from the PR #9 replay log:

```text
candidate2_v05_positive_replay: PASS
total_rows=608
by_tier={'H-E1-alg': 426, 'H-E2': 182}
event_count=1824
distinct_input_digest_count=1824
distinct_output_digest_count=1824
failed_event_count=0
```

## Source file hashes

```text
data/v0.5/bsd_dataset_v0_5.json      5b2d5b2b1c71dfc873d4dcc5a019b08411803b33b6c094662fd102dd2bfc18d3
reports/v0.5/bsd_dataset_v0_5_validation.json  aa79f6fbbcfaee4ac024c48ef6d4b90197835bc9be8f02eb5ca1d1d6f5eaf61c
```

## Seven-prime status

| n | claim_tier | alg_rank_method | exact rank known | exact rank | second independent point certified | promoted in milestone |
|---:|---|---|---|---:|---|---:|
| 41 | H-E1-alg | two_indep_points_HB_selmer4 | true | 2 | true | 4 |
| 137 | H-E1-alg | two_indep_points_HB_selmer4 | true | 2 | true | 4 |
| 257 | H-E1-alg | explicit_point_HB_selmer4 | false | null | false | 4 |
| 313 | H-E1-alg | explicit_point_HB_selmer4 | false | null | false | 4 |
| 353 | H-E1-alg | explicit_point_HB_selmer4 | false | null | false | 4 |
| 457 | H-E1-alg | explicit_point_HB_selmer4 | false | null | false | 4 |
| 761 | H-E1-alg | two_indep_points_HB_selmer4 | true | 2 | true | 4 |

## Audit correction preserved

Candidate 2 preserved the v0.5 audit correction:

```text
previous claim: 5 of 7 M4 primes have rank = 2 unconditional (set was {41, 137, 313, 353, 761})
corrected claim: 3 of 7 M4 primes have rank = 2 unconditional (set is {41, 137, 761})
false positives caught: [313, 353]
```

Cause:

```text
Q's descent image was different from P1's, but Q was in P1's torsion orbit.
At p=313, Q = P1 + (0,0). At p=353, Q = P1 + (-353,0).
Naive descent-image comparison missed this; orbit-membership testing catches it.
```

## Boundary

Candidate 2 validates:

- State A payload reproducibility;
- v0.5 row-count and claim-tier split;
- row-level controller-visible consistency channels;
- digest-addressed event generation;
- preservation of the v0.5 audit correction;
- seven-prime status readout;
- SocioSphere proof-apparatus controller validation on a positive BSD replay PR.

Candidate 2 does **not** validate:

- inherited `H-E1-alg` classifications as controller-witnessed M6 evidence;
- four-descent execution;
- independence proofs for 257, 313, 353, or 457;
- any claim promotion in `proof-adapter.json`;
- BSD-I, BSD-II, or Tate-Shafarevich finiteness.

Those remain future controller-routed gates.

## Next step

SocioSphere proof-apparatus validation issue #320 can close with the precise scope boundary above.

After closure, branch protection should require proof-apparatus validation on claim-bearing branches. The first post-validation research program should be Milestone 5, focused on controller-routed re-attestation/fresh search for the four-prime cohort:

```text
{257, 313, 353, 457}
```

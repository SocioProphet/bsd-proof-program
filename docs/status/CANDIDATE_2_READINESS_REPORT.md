# Candidate 2 Readiness Report

Status date: 2026-05-11

Candidate 2 is not ready to run yet.

The SocioSphere proof-apparatus controller has been validated for the adapter-boundary negative path. It correctly materialized BSD PR heads, rejected unsupported M6 self-promotion, rejected an undeclared non-claim reference, and produced inspectable failure artifacts.

Verified negative PRs:

| PR | Purpose | Result |
|---|---|---|
| #5 | Unsupported M6 self-promotion | Failed as expected: invalid state |
| #6 | Undeclared non-claim reference | Failed as expected: undeclared non-claim |

## Branch inventory checked

Visible branches:

- `main`
- `m6-scaffolding-v0.3.2-sync`
- `capture/v0.3.1-normalized-baseline`
- `capture-bsd-v0.2.1-l1-registry`
- `negative/bsd-m6-self-promotion-test`
- `negative/bsd-m6-undeclared-nonclaim-test`

Findings:

- `m6-scaffolding-v0.3.2-sync` contains import-control documentation only.
- `capture/v0.3.1-normalized-baseline` contains partial M6 text/code assets: model code, tests, specs, and runbooks.
- `capture-bsd-v0.2.1-l1-registry` contains v0.2.1 capture/report material.
- No visible branch contains the full v0.5 data payload required for Candidate 2.

## Partial material present

The partial branch includes useful M6 material such as:

- `m6/models/m6_v0_6_models.py`
- `tests/test_m6_targets.py`
- `docs/specs/M6_FOUR_DESCENT_SPEC_v0_3_1.md`
- `docs/runbooks/M6_0_FIRST_ACTION_RUNBOOK.md`

However, the test file depends on data files that are not visible on that branch.

## Missing material blocking Candidate 2

Candidate 2 still requires the missing v0.5 payload, including:

- `data/v0.5/bsd_dataset_v0_5.csv`
- `data/v0.5/bsd_dataset_v0_5.json`
- `reports/v0.5/bsd_dataset_v0_5_validation.json`
- `m6/scripts/m6_0_freeze_v0_5.py`
- `scripts/smoke_test.py`

The expected imported baseline is:

```text
608 rows
H-E1-alg: 426
H-E2: 182
```

## Current conclusion

The controller is ready for Candidate 2. The BSD repository payload is not.

The next required action is issue #7: land the missing State A v0.5/v0.3.2 import, then run the freeze check, then run Candidate 2.

# M1 Infrastructure Lane

This document tracks the analytic infrastructure lane for residual analysis, benchmark generation, and replayable campaign adjudication.

The M1 lane is intentionally separated from the M6 BSD certificate lane.

## Scope

M1 is infrastructure and experiment doctrine only.

It does not prove RH, BSD, P vs NP, or any other open problem. It provides a no-leakage residual-analysis framework for testing whether log-coordinate and spectral normalizations produce stable arithmetic residual structure under canonical and null spectral controls.

## Implemented components

- segmented sieve oracle (`m1/sieve.py`)
- G0 zero-table provenance validator (`m1/zero_table.py`)
- fixed-step real-u quadrature substrate (`m1/li_quadrature.py`)
- Chebyshev psi / von Mangoldt engine (`m1/chebyshev.py`)
- psi residual machinery (`m1/psi_residual.py`)
- frozen benchmark manifest writer (`m1/manifest.py`)
- benchmark interval catalog (`m1/benchmarks.py`)
- residual normalization geometries (`m1/normalization.py`)
- stationarity and scaling statistics (`m1/statistics.py`)
- variance-explanation metrics (`m1/varexpl.py`)
- spectral perturbation controls (`m1/perturbation.py`)
- sweep engine (`m1/experiments.py`)
- provenance ledger utilities (`m1/provenance.py`)
- evidentiary gates (`m1/gates.py`)
- campaign runner model (`m1/campaigns.py`)
- campaign JSON IO (`m1/campaign_io.py`)
- stable JSON serialization (`m1/serialization.py`)
- frozen campaign reports (`m1/reports.py`)
- CLI campaign runner (`scripts/run_m1_campaign.py`)

## Versioned campaign specs

- `m1/campaign_specs/m1_primary_a_canonical.json`
- `m1/campaign_specs/m1_primary_a_shuffled_null.json`
- `m1/campaign_specs/m1_primary_a_perturbation.json`

These specs require an external newline-delimited gamma table supplied to the CLI runner. They are not self-contained numerical claims.

## Claim discipline

Campaign reports classify outcomes as one of:

- `no_adjudication`
- `inconclusive`
- `evidence_passed_no_theorem_claim`
- `evidence_failed_no_theorem_claim`

Passing gates never promote a result into a theorem claim.

## Key invariants

- fail-closed zero-table validation
- cross-source zero verification
- hardcoded fixture checks for gamma_1, gamma_50, gamma_100, gamma_200
- oracle/model separation
- frozen-manifest evaluation discipline
- no silent truncation when a gamma table is shorter than requested N
- RH-envelope normalization remains diagnostic only
- box prime-flux normalization is used when comparing boxes with different log widths
- campaign reports are hash-bound and replayable

## Current limitations

- CI status is not yet confirmed on GitHub.
- Campaign gates currently use declared thresholds; no statistical significance doctrine is frozen yet.
- Canonical campaign specs are executable definitions, not validated empirical results.
- The current Chebyshev psi engine favors auditability over speed.
- Shuffled-collapse and perturbation-robustness gates are implemented, but paired canonical-vs-null comparison campaigns still need a higher-level comparator.

## Next tranche

- add paired campaign comparison reports
- add CLI support for canonical/null/perturbation bundles
- freeze first small gamma fixture under `tests/fixtures/`
- add CI workflow if absent
- add markdown report rendering for campaign summaries

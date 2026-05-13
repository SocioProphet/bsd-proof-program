# M1 Infrastructure Lane

This document tracks the analytic infrastructure lane for residual-analysis and benchmark generation.

The M1 lane is intentionally separated from the M6 BSD certificate lane.

Implemented components:

- segmented sieve oracle (`m1/sieve.py`)
- G0 zero-table provenance validator (`m1/zero_table.py`)
- infrastructure regression tests (`tests/test_m1_infrastructure.py`)

Pending components:

- Li quadrature
- psi residual machinery
- box manifest writer
- end-to-end integration harness

The current tranche is infrastructure only.

No theorem claims are introduced by this lane.

Key invariants:

- fail-closed provenance validation
- cross-source zero verification
- hardcoded fixture checks for gamma_1, gamma_50, gamma_100, gamma_200
- oracle/model separation
- frozen-manifest evaluation discipline

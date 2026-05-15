# Dependencies

## Upstream

| Repository | Commit SHA | Cited content |
|---|---|---|
| `SocioProphet/Heller-Godel` | `988307215ad38ccb16514311222184a1b757752b` | Framework objects (`HG-*`) from `docs/framework-core/`; PFK operational substrate from `proof_fabric_kernel/` |

## Cited objects

### Framework-grade (HG-*)

| Identifier | Role | Notes |
|---|---|---|
| `HG-FND-*` | Foundational vocabulary | typing and claim-boundary vocabulary only |
| `HG-MTH-005` | Universal Bridge formal specification | method-grade shared-missing-machinery diagnosis; does not transfer proofs |
| `HG-MTH-009` | Universal Bridge: arithmetic-geometric / BSD domain extension | reserved upstream; not yet drafted |

### PFK operational substrate

| Identifier | Role | BSD use |
|---|---|---|
| `PFK-OP-001` | Event ingestion family | future receipt emission |
| `PFK-OP-030` | Calibration operator family | numerical baselines for congruent-number family and rank/check artifacts |
| `PFK-OP-050` | PrimeStatsProtocol family | descriptive-grade empirical surveys, if any |

### PFK schemas

| Identifier | Canonical path | BSD use |
|---|---|---|
| `PFK-SCHEMA-001` | `proof_fabric_kernel/schemas/claim_ledger_row.schema.json` | future workstream claim ledgers |
| `PFK-SCHEMA-002` | `proof_fabric_kernel/schemas/event_ir.schema.json` | operator invocation receipts |
| `PFK-SCHEMA-003` | `proof_fabric_kernel/schemas/proof_artifact.schema.json` | proof-step envelopes |
| `PFK-SCHEMA-004` | `proof_fabric_kernel/schemas/calibration_bundle.schema.json` | numerical baseline checks |

### PFK anti-seed

| Identifier | Applies because |
|---|---|
| `A-PFK-OP-001` | operator invocation is not evidence; congruent-number calibration is not BSD progress |
| `A-PFK-PROTOCOL-001` | null passage is not theorem-grade |
| `A-PFK-PROTOCOL-002` | window-shopping prevention for rank-distribution or Tunnell-checkable surveys |
| `A-PFK-SCHEMA-001` | schema validity is not content validity |
| `A-PFK-SCHEMA-002` | schema-version drift; pin is not floating |
| `A-PFK-VAL-001` | validator green is not audit completion |

### Framework anti-seed

| Identifier | Failure mode |
|---|---|
| `A-MTH-001` | Universal Bridge does not transfer proofs |
| `A-MTH-003` | Catalan / mu2 fixture is not Clay progress |

## Citation form

```text
[HG-MTH-005 @ 988307215ad38ccb16514311222184a1b757752b]
[HG-MTH-009 @ 988307215ad38ccb16514311222184a1b757752b]  # reserved, not yet drafted
[PFK-SCHEMA-001 @ 988307215ad38ccb16514311222184a1b757752b]
[A-PFK-OP-001 @ 988307215ad38ccb16514311222184a1b757752b]
```

## Forbidden edges

- `bsd-proof-program` -> any other Clay-program repo (no horizontal dependencies).
- `bsd-proof-program` -> Heller-Godel-other-than-pinned-commit (no floating references).
- `bsd-proof-program` -> Universal Bridge material as proof transfer.

## Scope discipline

This dependency declaration does not change M6 discipline:

- no BSD proof claim;
- no rank computation claim;
- no row promotion;
- no parity theorem use for M6 promotion;
- no finite-Sha assumption;
- no use of BSD, parity, or Sha-finiteness for `H-E1-alg` exact-rank promotion.

The current M6 boundary remains authoritative: exact-rank promotion cannot set `bsd_used = true`, `parity_used = true`, or `sha_finite_assumed = true`.

## Schema source

PFK schemas live canonically at `SocioProphet/Heller-Godel/proof_fabric_kernel/schemas/` at the pinned commit. This repository consumes them through `HELLER_GODEL_ROOT` in dependency validation workflows.

Local schema material, if any, is non-authoritative unless explicitly declared generated/cache-only. It must not shadow canonical PFK schema names.

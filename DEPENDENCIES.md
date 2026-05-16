# Dependencies

## Upstream

This repository consumes from two upstream framework repositories. Both pins are required for citation-surface validation.

| Repository | Commit SHA | Role |
|---|---|---|
| `SocioProphet/Heller-Godel` | `e385bad859c49604cff5a3f4945b33079d54af82` | Framework core; framework objects (`HG-*`); PFK operational substrate (`PFK-*`); framework anti-seed (`A-HG-*`, `A-PFK-*`) |
| `SocioProphet/Heller-Dirac` | `e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993` | Co-foundational spectral / Hopf / time / field scaffold; spectral-triple vocabulary (`HD-*`); Heller-Dirac anti-seed (`A-HD-*`) |

Both pins are not floating. Re-pinning requires an explicit dependency PR.

## Cited objects

### From Heller-Godel @ `e385bad859c49604cff5a3f4945b33079d54af82`

#### Framework-grade (HG-*)

| Identifier | Role | Status |
|---|---|---|
| `HG-FND-*` | Foundational vocabulary | active |
| `HG-MTH-005` | Universal Bridge formal specification | active |
| `HG-MTH-009` | Universal Bridge: BSD arithmetic-geometric domain extension | active |

#### PFK operational substrate

| Identifier | Role | BSD use |
|---|---|---|
| `PFK-OP-001` | Event ingestion family | future receipt emission |
| `PFK-OP-030` | Calibration operator family | numerical baselines for congruent-number family and rank/check artifacts |
| `PFK-OP-050` | PrimeStatsProtocol family | descriptive-grade empirical surveys, if any |
| `PFK-SCHEMA-001..004` | standard schemas | claim ledgers, Event-IR, proof artifacts, calibration bundles |

#### Framework anti-seed

| Identifier | Applies because |
|---|---|
| `A-HG-MTH-001` | Universal Bridge does not transfer proofs |
| `A-HG-MTH-003` | Catalan / mu2 fixture is not Clay progress |
| `A-HG-MTH-004` | Standard Conjectures / Bloch-Kato-style apparatus cited diagnostically are not assumed |
| `A-HG-MTH-006` | component apparatus diagnostic is not Clay-grade resolution |
| `A-HG-MTH-007` | BSD-rank and BSD-strong have distinct structural status |

#### PFK anti-seed

| Identifier | Applies because |
|---|---|
| `A-PFK-OP-001` | operator invocation is not evidence; congruent-number calibration is not BSD progress |
| `A-PFK-PROTOCOL-001` | null passage is not theorem-grade |
| `A-PFK-PROTOCOL-002` | window-shopping prevention for rank-distribution or Tunnell-checkable surveys |
| `A-PFK-SCHEMA-001` | schema validity is not content validity |
| `A-PFK-SCHEMA-002` | schema-version drift; pins are not floating |
| `A-PFK-VAL-001` | validator green is not audit completion |

### From Heller-Dirac @ `e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993`

#### Foundational (HD-FND-* / HD-EX-*)

| Identifier | Role in BSD citation |
|---|---|
| `HD-FND-001` | spectral triple definition for Bost-Connes / endomotive spectral context |
| `HD-FND-007` | Tomita-Takesaki modular operator and modular flow |
| `HD-EX-001` | circle spectral triple fixture, basic spectral building block |

#### Heller-Dirac anti-seed (A-HD-*)

| Identifier | Applies because |
|---|---|
| `A-HD-NC-001` | Bost-Connes / endomotive reformulation is not proof |
| `A-HD-SP-001` | analog spectral data is not target spectral data |
| `A-HD-FT-001` | axiomatic / KMS structure is not constructive realization |
| `A-HD-TM-001` | modular flow is not automatically physical or arithmetic time |
| `A-HD-FND-001` | HD-FND identifiers are reference surface, not reproof |

## Citation form

```text
[HG-MTH-005 @ e385bad859c49604cff5a3f4945b33079d54af82]
[HG-MTH-009 @ e385bad859c49604cff5a3f4945b33079d54af82]
[PFK-SCHEMA-001 @ e385bad859c49604cff5a3f4945b33079d54af82]
[A-HG-MTH-007 @ e385bad859c49604cff5a3f4945b33079d54af82]
[HD-FND-001 @ e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993]
[HD-FND-007 @ e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993]
[HD-EX-001 @ e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993]
[A-HD-NC-001 @ e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993]
[A-HD-SP-001 @ e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993]
[A-HD-FT-001 @ e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993]
[A-HD-TM-001 @ e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993]
[A-HD-FND-001 @ e1d7c863f4e0fc6e5e2ab485370cc75b2dba3993]
```

## Forbidden edges

- `bsd-proof-program` -> any other Clay-program repo.
- `bsd-proof-program` -> Heller-Godel-other-than-pinned-commit.
- `bsd-proof-program` -> Heller-Dirac-other-than-pinned-commit.
- `bsd-proof-program` -> noncommutative-geometric methodology beyond the HG-MTH-009 Component 2 diagnostic frame.

## Scope discipline

This dependency declaration does not change M6 discipline:

- no BSD proof claim;
- no rank computation claim;
- no row promotion;
- no parity theorem use for M6 promotion;
- no finite-Sha assumption;
- no use of BSD, parity, or Sha-finiteness for `H-E1-alg` exact-rank promotion.

BSD-rank and BSD-strong are distinct surfaces. Workstream artifacts must declare which surface they address.

## Schema-version pinning policy

Both upstream pins are fixed. Re-pinning either upstream requires a dedicated migration PR and validation of all affected citations.

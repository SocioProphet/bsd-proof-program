# Workstream C — Tunnell-Checkable Cases

Spec citation: `[BSD-LANE-V0.1-SKELETON @ a01376090792b12f54fd51caa9e077c9894276e6]`  
Bridge citation: `[HG-MTH-009 @ e385bad859c49604cff5a3f4945b33079d54af82]:Components 1+3`  
Framework citation: `[HG-MTH-005 @ e385bad859c49604cff5a3f4945b33079d54af82]`  
PFK citation: `[PFK-SCHEMA-004 @ e385bad859c49604cff5a3f4945b33079d54af82]`  
Boundary anti-seed: `[A-HG-MTH-007 @ e385bad859c49604cff5a3f4945b33079d54af82]`, `[A-PFK-OP-001 @ e385bad859c49604cff5a3f4945b33079d54af82]`

## Status

Workstream skeleton. No apparatus implemented yet.

## Purpose

Control congruent-number family fixtures, including curves of the form:

```text
E_n: y^2 = x^3 - n^2 x
```

## Bridge positioning

Component scope: Component 1 (Selmer / Sha) plus Component 3 (modularity / p-adic L-functions) in restricted-rank fixture regimes.

This workstream is the natural location for Tunnell-checkable and congruent-number-family apparatus. Per `[A-HG-MTH-007 @ e385bad859c49604cff5a3f4945b33079d54af82]`, restricted-rank fixture work is not full BSD-rank or BSD-strong apparatus.

## Promotion gate status

| Gate | Status |
|---|---|
| Gate 0 — spec accepted | pending PR merge |
| Gate 1 — apparatus implemented | pending |
| Gate 2 — fixture validated | pending |
| Gate 3 — descriptive-grade claim | pending |
| Gate 4 — methodology-grade claim | pending |
| Gate 5 — theorem-grade artifact | pending |

## Boundary

Tunnell-checkable fixture work is not BSD proof. Conditional results must declare all assumptions explicitly. No artifact in this workstream may assume Sha finiteness or use BSD/parity/Sha-finiteness for `H-E1-alg` exact-rank promotion.

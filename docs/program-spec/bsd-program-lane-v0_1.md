# BSD Program Lane v0.1 — Specification Skeleton

Source reference: `BSD_Program_Lane_v0.1.pdf` (Drive, May 9, 2026).  
Status: structural skeleton only; full PDF text not imported by this PR.  
Claim level: program specification / no theorem claim.

## Import discipline

This file records the BSD Program Lane v0.1 structure known from the program review context. It does not claim to be a byte-faithful or full-text import of the Drive PDF.

A future source-import PR with Drive/PDF access should replace this skeleton with full extracted markdown, preserving the workstream and claim-boundary structure below.

## Scope

The BSD program is scoped to disciplined evidence handling around the Birch and Swinnerton-Dyer program, including congruent-number family fixtures and M6 exact-rank promotion constraints.

This skeleton does not claim:

- a BSD proof;
- a rank computation;
- a row promotion;
- finite Sha;
- parity theorem applicability to M6 rows;
- any theorem-grade BSD artifact.

## Workstreams A-F

### Workstream A — Foundational typing

Defines the BSD claim surface, coefficient fields, elliptic-curve object model, and claim-boundary vocabulary.

### Workstream B — Mordell-Weil and Tate-Shafarevich structure

Records the structural relationship between Mordell-Weil rank, Selmer groups, descent data, and Tate-Shafarevich obstructions without assuming finite Sha unless explicitly allowed by a theorem.

### Workstream C — Tunnell-checkable cases

Controls congruent-number family fixtures, including elliptic curves of the form:

```text
E_n: y^2 = x^3 - n^2 x
```

Fixture-grade work remains fixture-grade unless upgraded by a theorem-grade artifact.

### Workstream D — p-adic and Iwasawa-theoretic apparatus

Records p-adic L-function, Iwasawa-theoretic, and related arithmetic apparatus boundaries. No p-adic evidence is theorem-grade without explicit theorem/citation.

### Workstream E — Empirical surveys

Controls descriptive-grade surveys such as rank-distribution or Tunnell-checkable computations. Any empirical claim must declare distribution, tranche, nulls, and reporting policy.

### Workstream F — Promotion gates and audit

Defines promotion gates, audit requirements, anti-seed cross-references, and rollback discipline.

## Evidence classes E0-E7

The full v0.1 PDF should define the canonical evidence classes. Until full source import, this skeleton only reserves the class range:

```text
E0, E1, E2, E3, E4, E5, E6, E7
```

No downstream PR should cite the detailed contents of a class until the full v0.1 spec text is imported or the class is independently defined in repo.

## Promotion gates

The full v0.1 PDF should define the canonical promotion gates. Until full source import, this skeleton reserves:

| Gate | Status |
|---|---|
| Gate 0 | workstream specification accepted |
| Gate 1 | workstream apparatus implemented |
| Gate 2 | fixture validated |
| Gate 3 | first descriptive-grade claim |
| Gate 4 | first methodology-grade claim |
| Gate 5 | theorem-grade artifact |

## Anti-seed cross-references

- `[A-MTH-001 @ 988307215ad38ccb16514311222184a1b757752b]` — Universal Bridge does not transfer proofs.
- `[A-MTH-003 @ 988307215ad38ccb16514311222184a1b757752b]` — fixture-grade work is not Clay progress.
- `[A-PFK-OP-001 @ 988307215ad38ccb16514311222184a1b757752b]` — operator invocation is not evidence.
- `[A-PFK-SCHEMA-001 @ 988307215ad38ccb16514311222184a1b757752b]` — schema validity is not content validity.

## Citation form

```text
[BSD-LANE-V0.1-SKELETON @ <this-merge-sha>]
```

This skeleton is citable as a structural scaffold only, not as the full Drive PDF import.

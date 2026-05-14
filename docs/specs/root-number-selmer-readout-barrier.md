# Root Number / Selmer Readout-Basis Barrier

Status: **barrier reference / context only / no row promotion**.  
Canonical pattern owner: `SocioProphet/systems-learning-loops`.  
Canonical pattern path:

```text
kb/patterns/coordinate-basis-vs-readout-basis-involution.md
```

## Purpose

This note attaches the coordinate-basis vs readout-basis involution pattern to the BSD proof program without changing any M6 row state or promotion rule.

The local barrier statement is:

```text
The root number epsilon is a global involution/sign on the L-function side.
It is not, by itself, a readout basis for Selmer or Mordell-Weil rank.
```

## Local interpretation

The functional-equation sign `epsilon` gives a global parity-shaped involution on the `L(E, s)` side. That sign is structurally important, but any method that tries to read off rank from `epsilon` alone is still operating in a coordinate/global-sign basis.

The readout-basis problem is the arithmetic alignment problem:

```text
L-function sign / analytic symmetry
-> Selmer / Tate-module / Mordell-Weil direction
```

That alignment is not supplied by the sign alone. It is part of the hard BSD structure.

## M6 guardrail

This note does not alter M6 promotion logic. In particular, exact-rank promotion remains forbidden from using:

```text
bsd_used = true
parity_used = true
sha_finite_assumed = true
```

The existing `H-E1-alg` boundary remains intact.

## Canonical KB backlink

The reusable cross-repo pattern is not duplicated here. Use:

```text
SocioProphet/systems-learning-loops/kb/patterns/coordinate-basis-vs-readout-basis-involution.md
```

## Nonclaims

This note does not claim:

- a BSD proof;
- a rank computation;
- a row promotion;
- parity theorem applicability to M6 rows;
- finite Sha;
- that the Part B cipher experiment measures elliptic curves or Selmer groups.

It is a barrier note only: involution is not selectivity, and root-number sign is not Selmer readout alignment.

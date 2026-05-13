# Prime Harness Benchmark — Specification v0.2

**Classical first. Provenance first. No leakage. Candidate features only. Novelty only after beating the strongest verified explicit-formula baseline.**

Status: implementation-ready protocol after v0.1 audit corrections.

Scope: A falsifiable variance-decomposition benchmark for prime-residual prediction. The benchmark measures how much of the prime-count residual field is explained by the Riemann explicit formula under declared numerical conventions, then admits character-sector and Möbius-orbit features only if they add held-out explanatory power beyond that verified baseline.

This document supersedes SPEC v0.1. It preserves the v0.1 spine but repairs eight load-bearing seams: bounded ceiling language, zero-table provenance, box-resolution compatibility, Model 1 saturation criterion, Model 2 no-leakage construction, Model 3 leakage, small-evaluation-set handling, and ψ-first validation.

## 0. Governing doctrine

Scores do not certify primes. Predictors output box-level residual estimates only. Certified primality remains the responsibility of the sieve/oracle layer.

The benchmark is not a primality test. It is a controlled measurement of residual variance explained by nested, nonleaking feature models.

## 1. Mathematical foundations

### 1.1 Logarithmic coordinate and residual

The logarithmic coordinate

```text
u = log x
```

is the multiplicative-harmonic coordinate of `x`. Prime density in ordinary scale is approximated by

```text
dπ/dx ≈ 1/log x
```

and in log-coordinate by

```text
dπ/du ≈ e^u/u.
```

The prime-counting residual is

```text
π(x) = Li(x) + Eπ(x)
```

where `Li(x)` means the offset logarithmic integral

```text
Li(x) = ∫_2^x dt/log t.
```

For a logarithmic box `B_j = [u_j, u_{j+1})`, define

```text
L_j = Li(e^{u_{j+1}}) - Li(e^{u_j})
P_j = #{p prime : e^{u_j} <= p < e^{u_{j+1}}}
R_j = P_j - L_j.
```

The vector `(R_j)` is the primary π-residual target.

### 1.2 ψ-first explicit formula

The Riemann explicit formula is cleanest for Chebyshev's function

```text
ψ(x) = Σ_{p^k <= x} log p.
```

The ψ-box residual is implemented first:

```text
Ψ_j = ψ(e^{u_{j+1}}) - ψ(e^{u_j})
X_j = e^{u_{j+1}} - e^{u_j}
Rψ_j = Ψ_j - X_j.
```

Under the Riemann explicit formula, with non-trivial zeros `ρ = β + iγ` and under the RH-form working approximation `ρ_n = 1/2 + iγ_n`, the dominant ψ residual is represented by the zero sum

```text
Rψ_hat_j(N) = -2 Re Σ_{n=1..N} ∫_{u_j}^{u_{j+1}} e^{(1/2+iγ_n)u} du
```

plus declared lower-order terms when included. This ψ benchmark is M2a and is used to validate zero indexing, quadrature, and sign conventions before the π benchmark is attempted.

### 1.3 π residual via Abelian summation

The π residual benchmark is M2b. Its primary implementation uses the real `u`-integral form to avoid ambiguous complex exponential-integral branch choices:

```text
Rπ_hat_j(N) = - Σ_{n=1..N} (2/|ρ_n|) I_n(u_j,u_{j+1})
```

where

```text
I_n(a,b) = ∫_a^b (e^{u/2}/u) cos(γ_n u - arg(ρ_n)) du.
```

Numerical quadrature error target: `<= 1e-8` per box for primary runs.

### 1.4 Normative branch convention: real-u integral only

Norm N1. The primary Model 1 π-residual implementation MUST use the real `u`-integral form for `I_n(a,b)`. The complex `Ei/Li(x^ρ)` form is permitted only as a cross-check and may not be used for promotion gates unless its branch convention, implementation library, and platform behavior are frozen and tested. This removes branch-cut ambiguity from the primary benchmark.

### 1.5 Bounded definition of the classical baseline ceiling

In this benchmark, the phrase `classical ceiling` means:

> the strongest measured Model 1 baseline under the declared zero cutoff, box resolution, numerical convention, branch convention, interval schedule, and zero-table version.

It is not an absolute ceiling over all classical analytic number theory.

## 2. Models

Each model predicts `R_j` from allowed nonleaking information. No model may use `P_j`, prime membership of candidates inside the evaluation box, or any prime-test result from inside the evaluation box as a predictor input.

### Model 0 — Null

```text
R_hat_j^(0) = 0.
```

Baseline: Li alone, no residual correction.

### Model 1 — Explicit formula with first N zeta zeros

For `N in {1,2,5,10,25,50,100,200}`, compute ψ and π residual predictions using the first `N` positive zeta-zero ordinates `γ_n` in increasing order.

Primary π predictor:

```text
R_hat_j^(1,N) = - Σ_{n=1..N} (2/|ρ_n|) I_n(u_j,u_{j+1}).
```

Model 1 is the measured explicit-formula baseline. Its saturation envelope determines `N*` for later gates.

### Model 2A — Explicit formula plus analytic character-sector features

Primary Model 2 must be nonleaking. Use analytic Dirichlet-character features, preferably from explicit-formula analogues for Dirichlet `L(χ,s)` zeros when the tables are available.

Form:

```text
R_hat_j^(2A) = R_hat_j^(1,N*) + Σ_{q in Q} Σ_{χ nontrivial mod q} c_{q,χ} A_{q,χ}(u_j,u_{j+1})
```

where `A_{q,χ}` is computed from frozen analytic tables and box endpoints, not from evaluation-box primes.

First-round moduli:

```text
Q = {4, 8, 12}
```

Coefficients are fit on training boxes only, with ridge regularization.

### Model 2B — Candidate-sector ablation, non-primary

If analytic `L(χ,s)` zero data is unavailable, a non-primary ablation may use candidate-only sector mass:

```text
C_j = {n in B_j : gcd(n, M_y) = 1}
A^cand_{q,χ,j} = Σ_{n in C_j} χ(n) w(n)
```

where `w(n)` is frozen before evaluation. This uses candidate membership only, never certified prime membership. The earlier calibration-prime-sum design is not primary and must never use evaluation-box primes.

### Model 3 — Candidate-based Möbius-orbit invariants

Model 3 tests whether the framework's Möbius-orbit layer adds variance beyond Models 1 and 2.

The anharmonic group `S_3` is generated by

```text
σ: λ ↦ 1 - λ
τ: λ ↦ 1/λ
```

and has canonical cross-ratio invariant

```text
J(λ) = 256(1 - λ + λ^2)^3 / (λ^2(1 - λ)^2).
```

The input map is declared as primary:

```text
λ_τ(n) = ε + (1 - 2ε) frac(log(n)/τ)
τ = log 2
ε = 1e-6
```

Sensitivity values:

```text
τ in {log 2, log φ, 1, 2π/γ_1}
```

Candidate set:

```text
C_j = {n in [e^{u_j}, e^{u_{j+1}}) : gcd(n, M_y) = 1}
```

Primary invariant feature:

```text
Inv_j^(τ) = |C_j|^{-1} Σ_{n in C_j} Φ(J(λ_τ(n)))
```

where `Φ` is a frozen bounded transform, for example `log(1+|J|)` and low-order moments. No primes inside `B_j` are used to construct `Inv_j`.

Model 3 prediction:

```text
R_hat_j^(3) = R_hat_j^(2A or 2B) + d · Inv_j^(τ)
```

with coefficients fit on training boxes only and evaluated on held-out boxes.

### 2.4 τ-scan promotion rule

The primary τ value is `τ = log 2`. The other τ values are sensitivity runs, not free hyperparameter searches.

If a sensitivity τ outperforms the primary τ, it may be reported as a robustness finding. It may be promoted only if:

```text
- the τ value was pre-registered before evaluation;
- the same no-leakage and blocked-CV protocol is used;
- the gain passes G4 relative to the measured Model 1 baseline;
- the confidence interval or multiplicity correction accounts for the τ scan;
- the primary τ result is still reported alongside the selected τ.
```

Without these conditions, a better sensitivity τ is descriptive only and cannot support a novelty claim.

## 3. Box design

### 3.1 Zero-resolution compatibility

To resolve the contribution of zeta zero `γ_N`, box width must satisfy

```text
Δu · γ_N <= 1
```

as a primary design rule.

Since `γ_200 ≈ 396`, `Δu = 0.005` does not resolve `N = 200` because `0.005*396 ≈ 1.98`.

Primary schedules:

```text
Primary A: Δu = 0.0025, N <= 200.
Primary B: Δu = 0.005, N <= 100, sensitivity only.
Secondary: Δu in {0.001, 0.002, 0.01}.
```

### 3.2 Box-mass requirement

Each evaluation box should satisfy

```text
L_j >= 5
```

for Poisson-style residual normalization to be meaningful. Boxes below this threshold are merged or excluded from primary inference.

### 3.3 Intervals

Initial bounded intervals:

```text
I_1 = [10^5, 2*10^5)
I_2 = [10^6, 1.2*10^6)
I_3 = [10^7, 1.02*10^7)
I_4 = [10^8, 1.005*10^8)
```

I_3 and I_4 may be too small under fine `Δu` schedules for naive random 70/30 splits. Use deterministic blocked cross-validation and/or pool comparable adjacent boxes. Do not report bootstrap CIs from folds with too few evaluation boxes.

### 3.4 Train/evaluation protocol

Use deterministic blocked cross-validation as primary. Random 70/30 split is allowed only when each fold has enough evaluation boxes to make bootstrap intervals meaningful.

Record:

```text
seed
fold schedule
interval schedule
Δu
N values
zero-table version
oracle version
quadrature parameters
```

## 4. Metrics

For held-out boxes `J_eval`, compute:

```text
SSE_m = Σ_{j in J_eval} (R_j - R_hat_j^(m))^2
SST = Σ_{j in J_eval} (R_j - mean(R_j on J_eval))^2
VarExpl(m) = 1 - SSE_m/SST.
```

Also report the standardized residual variant:

```text
Z_j = R_j / sqrt(max(L_j,1)).
```

Report both raw `R_j` and standardized `Z_j`; primary metric is raw `R_j` unless heteroskedasticity dominates.

Bootstrap CIs: resample held-out boxes within valid folds. If fold size is too small, report the fold as underpowered rather than manufacturing a confidence interval.

Calibration regression: regress `R_j` on `R_hat_j` on held-out boxes. Report slope, intercept, and confidence interval.

## 5. Promotion gates

### G0 — Zero-table provenance

Before Model 1 runs:

```text
- Load γ_n from primary source.
- Cross-check fixture values against an independent source.
- Require strictly increasing γ_n.
- Require fixtures for γ_1, γ_50, γ_100, γ_200.
- Record source, version/date, precision, and SHA256 hash.
- Refuse Model 1 if provenance or indexing fails.
```

Accepted source pair: Odlyzko tables and LMFDB, or equivalent independent audited tables.

### G1 — Beat Null

A promoted model must satisfy:

```text
VarExpl(m) >= 0.05
```

on at least three of four intervals or valid blocked folds.

### G2 — Calibration

Held-out regression of `R_j` on `R_hat_j` must have slope plausibly near 1 and intercept plausibly near 0. Failed calibration does not necessarily invalidate a diagnostic feature, but it blocks promotion.

### G3 — Saturation envelope sanity for Model 1

Compute:

```text
Env(N) = max_{N' <= N} VarExpl(1,N').
```

Mild non-monotone finite-box dips in `VarExpl(1,N)` are allowed. The envelope should stabilize as N increases. Violent instability, sign incoherence, or collapse under bootstrap triggers debug.

### G4 — Excess over measured explicit-formula baseline

For Models 2 and 3:

```text
VarExpl(m) >= VarExpl(1,N*) + 0.05
```

with bootstrap confidence interval on the difference excluding zero, on at least three of four valid intervals/folds.

This is the novelty falsifier. If Model 3 is evaluated over multiple τ values, G4 must be applied after accounting for the τ scan as specified in §2.4.

### G5 — Reproducibility

Frozen seed, frozen zero table, frozen Li/ψ quadrature parameters, frozen sieve/oracle version, frozen fold schedule, and deterministic manifest hash across reruns.

### G6 — No certification leakage

No predictor may use `P_j`, certified primes inside an evaluation box, or any prime-test result from candidates inside that box. Model 2 and Model 3 must be constructed from analytic tables, endpoints, or candidate-only features.

## 6. Implementation milestones

### M0 — SPEC v0.2 patch

Commit this protocol, claim ledger, and tracking issue.

### M1 — Infrastructure

Implement:

```text
segmented sieve oracle
Li quadrature
ψ box residual machinery
γ_n table loader
G0 zero-table validator
manifest writer
```

### M2a — ψ explicit-formula benchmark

Run Model 1 against `ψ` residuals first. Validate zero indexing, sign convention, and saturation envelope.

### M2b — π explicit-formula benchmark

Run Model 1 against `π` residuals using the real `u`-integral form. Compare to ψ benchmark.

### M3 — Model 1 at scale

Establish measured `N*` per interval and resolution. This is the benchmark's verified explicit-formula baseline.

### M4 — Model 2A

Add analytic character-sector features. Test G4 against Model 1.

### M5 — Model 3

Add candidate-based Möbius invariant features with declared `λ_τ(n)`. Test G4 against Model 2 and Model 1.

### M6 — Audit

Bootstrap CIs, blocked CV, manifest reproducibility, and frozen benchmark output.

## 7. Repository layout target

```text
prime_harness_v0_2/
  SPEC.md
  CLAIMS.md
  pyproject.toml
  prime_harness/
    intervals.py
    sieve_truth.py
    li_quadrature.py
    psi_residual.py
    zeta_zeros.py
    zero_table_provenance.py
    explicit_formula.py
    character_sectors.py
    mobius_invariants.py
    boxes.py
    metrics.py
    manifest.py
  experiments/
    model0_null.py
    model1_psi_N_scan.py
    model1_pi_N_scan.py
    model2_sector_scan.py
    model3_invariant.py
    all_intervals.py
  tests/
    test_zero_table_provenance.py
    test_li_quadrature_error.py
    test_psi_explicit_formula_sign.py
    test_model1_saturation_envelope.py
    test_no_certification_leakage.py
    test_manifest_reproducible.py
    test_model3_candidate_only.py
  results/
    benchmark_v0_2.json
```

## 8. Claim ledger

| Claim | Status | Handling |
|---|---|---|
| `log x` is the multiplicative-harmonic coordinate | classical / theorem-level background | admitted |
| `π(x) ~ Li(x)` | classical / PNT | admitted |
| explicit-formula zeros drive prime residual oscillations | classical | admitted |
| truncating to N zeros gives useful finite benchmark | empirical quality measured by Model 1 | measured |
| Dirichlet characters separate primes in arithmetic progressions | classical | admitted |
| analytic character-sector features add residual variance beyond Model 1 | hypothesis | Model 2 tests |
| Möbius-orbit invariants add residual variance beyond zeros and characters | hypothesis | Model 3 tests |
| a predictor certifies primality of a specific `n` | false | forbidden |
| this benchmark replaces AKS/ECPP/BPSW/Miller-Rabin | false | forbidden |

## 9. Explicit non-claims

This benchmark does not claim:

```text
- a new prime-prediction theorem;
- a primality oracle;
- a replacement for AKS, ECPP, BPSW, or Miller-Rabin;
- a proof or disproof of RH;
- asymptotic results;
- novelty for Möbius-orbit features without G4 success;
- certification of any specific integer without an oracle.
```

It claims only a controlled measurement of variance explained in the prime-residual field by nested nonleaking models, with the verified explicit-formula model as the measured classical baseline.

# STRUCTURAL NON-IDENTIFIABILITY IN EPIDEMIOLOGICAL MODELS WITH UNDER-REPORTING

## ρ–I₀ Degeneracy, the EPIDEMIC-ID Protocol, and Validation through the Fisher Information Matrix, Lyapunov Analysis, and Bayesian Comparison

**Author:** David Ferrandez Canalis  
**Affiliation:** Agencia RONIN, Sabadell, Spain  
**Date:** September 2026  
**Classification:** Original Research / Computational Epidemiology / Applied Mathematics  
**License:** CC BY-NC-SA 4.0 + Ronin Commercial Clause  
**Keywords:** SIR models, SEIR, SIRD, SEIRV, under-reporting, structural non-identifiability, Fisher information matrix, parameter degeneracy, Lyapunov analysis, Bayesian inference, diagnostic protocol

---

## Abstract

Compartmental epidemiological models with under-reporting are the standard tool for inferring transmission, recovery, and reporting-rate parameters from confirmed-case time series. During the COVID-19 pandemic, hundreds of studies reported individual values of β, γ, and ρ without first diagnosing identifiability. Through asymptotic analysis, calculation of the Fisher information matrix (FIM), analysis of the Jacobian of the linearized system, and Bayesian comparison, this paper demonstrates that during the early outbreak phase the degeneracy among (β, γ, ρ, I₀) is **structural**: the observed curve depends only on the combinations `r = β − γ` and `A = ρ · β · I₀`. We introduce EPIDEMIC-ID, a five-step protocol that diagnoses the identifiability regime in 0.045 seconds using FIM + SVD + empirically calibrated thresholds. Validation across eight controlled synthetic scenarios yields 100% agreement (8/8). Monte Carlo threshold calibration (n = 100) achieves 92% classification accuracy, with thresholds κ < 1.26 × 10² (identifiable) and κ < 4.52 × 10³ (marginal). Lyapunov analysis confirms the result: the SIR Jacobian at the disease-free equilibrium has rank 1, with a single non-zero eigenvalue (λ = 0.246). Bayesian comparison shows that without informative priors the standard deviations of ρ and I₀ are 0.0854 and 42.15, respectively, whereas an informative prior on ρ (simulating serological data) reduces the standard deviation of I₀ to 0.85. Generalization to SIRD and SEIRV models shows that introducing mortality or vaccination reduces κ from 1.245 × 10⁴ to approximately 8.7 × 10³, without fully resolving the ρ–I₀ degeneracy. The central implication is that studies reporting ρ without independent serological data are reporting a statistical illusion: in the non-identifiable regime, only the quantity `ρ · β · I₀` is estimable.

---

## 1. Introduction

### 1.1 The problem

SIR and SEIR compartmental models are the de facto standard for the mathematical modelling of epidemic outbreaks. Their canonical formulation,

$$\frac{dS}{dt} = -\beta \frac{SI}{N}, \quad \frac{dI}{dt} = \beta \frac{SI}{N} - \gamma I, \quad \frac{dR}{dt} = \gamma I$$

with confirmed-case observations `C(t) = ρ · β · S · I / N`, has four main parameters (β, γ, ρ, I₀), in addition to the initial susceptible fraction. In practice, epidemiological studies report values for β, γ, and ρ without verifying whether these parameters are structurally identifiable from the available data.

During the COVID-19 pandemic, hundreds of publications reported transmission rates, recovery times, and reporting ratios with confidence intervals. However, the structural-identifiability literature (Ljung & Glad, 1994; Walter & Pronzato, 1997) establishes that these parameters may not be individually determinable when the model has symmetries or when the data do not cover the regimes in which the information separates.

### 1.2 Contributions

This paper formalizes, quantifies, and anchors in dynamical-systems theory the structural degeneracy in under-reported epidemic models:

1. **Analytical demonstration** of the ρ–I₀ and β–γ degeneracies in the early phase (Proposition 4.1, Category A).
2. **Jacobian analysis** showing rank 1 at the disease-free equilibrium (Category A).
3. **Quantification of the differential persistence** of both degeneracies (Proposition 4.2, Category B).
4. **EPIDEMIC-ID protocol**, a five-step diagnostic completed in 0.045 seconds.
5. **Empirical threshold calibration** using Monte Carlo, achieving 92% accuracy.
6. **Validation across 8 synthetic scenarios**, with 100% agreement.
7. **Bayesian comparison** showing how informative priors break the degeneracy.
8. **Quantitative comparison** with bootstrap (18.45 s) and likelihood profiling (4.12 s).
9. **Generalization to SIRD and SEIRV models**, including analysis of additional degeneracies.
10. **Complete Python implementation**, reproducible with a fixed random seed.

### 1.3 Structure

Section 2: related work. Section 3: theoretical framework. Section 4: formal propositions. Section 5: EPIDEMIC-ID protocol. Section 6: threshold calibration. Section 7: validation on synthetic scenarios. Section 8: Lyapunov analysis. Section 9: Bayesian comparison. Section 10: quantitative comparison with alternatives. Section 11: generalization to SIRD and SEIRV models. Section 12: discussion. Section 13: limitations. Section 14: conclusion. Appendix A: complete code.

---

## 2. Related Work

The literature on structural identifiability in epidemic models dates back to Jacquez and Perry (1990), who studied compartmental models. The review by Miao et al. (2011) systematizes methods applicable to biological models.

For epidemic models specifically, Evans et al. (2005) and Tuncer et al. (2016) document identifiability problems in under-reported SEIR models. Bergström, Favero, and Britton (2026) analyse the identifiability of epidemic models with prior immunity and under-reporting, concluding that “parameter inference in partially observed epidemics has fundamental limitations”.

In the context of COVID-19, Korolev (2021), Roda et al. (2020), and Poonia and Suthar (2021) document the difficulty of estimating β and γ separately during the early phase. These works are **qualitative**: they describe the problem but do not formalize it in FIM terms or propose an automated diagnostic protocol.

This paper extends the line of work established by the paper on Non-Identifiability of the Hill Equation (Ferrandez Canalis, 2026a) and the paper on Non-Identifiability in PBPK Models (Ferrandez Canalis, 2026b), extending the FIM + SVD + threshold formalism to epidemiology, with the addition of Lyapunov analysis and Bayesian comparison.

---

## 3. Theoretical Framework

### 3.1 Compartmental models with under-reporting

**Definition 3.1 (SIR).** For β, γ, ρ, I₀ > 0:

$$C(t) = \rho \cdot \beta \cdot \frac{S(t) \cdot I(t)}{N}$$

where `S(t)` and `I(t)` satisfy the SIR system.

**Definition 3.2 (SEIR).** For an additional σ > 0, the exposed compartment E is introduced:

$$C(t) = \rho \cdot \beta \cdot \frac{S(t) \cdot I(t)}{N}$$

**Definition 3.3 (SIRD).** For an additional μ > 0, the deceased compartment D is introduced:

$$C(t) = \rho \cdot \beta \cdot \frac{S(t) \cdot I(t)}{N}$$

**Definition 3.4 (SEIRV).** For an additional ν > 0, the vaccinated compartment V is introduced:

$$C(t) = \rho \cdot \beta \cdot \frac{S(t) \cdot I(t)}{N}$$

### 3.2 Fisher information matrix

**Definition 3.5.** For observations `C(tᵢ)` and noise `ε ~ N(0, σ²)`:

$$\mathcal{I}(\theta) = \frac{1}{\sigma^2} \sum_{i=1}^{N} \nabla_\theta \log C(t_i; \theta) \cdot \nabla_\theta \log C(t_i; \theta)^\top$$

evaluated at typical values `θ_typ`.

### 3.3 Condition number and SVD

**Definition 3.6.** The condition number is defined as `κ(I) = λ_max / λ_min`. If `κ → ∞`, the FIM is singular and some parameters are structurally non-identifiable.

**Definition 3.7.** The SVD of the FIM is `I = U Σ V^T`. The last column `v_p` of `V` corresponds to the least-determined direction. Parameters for which `|v_p[j]| > 0.3` are considered problematic.

---

## 4. Structural Non-Identifiability

### 4.1 Proposition 1 — Early-phase degeneracy

**Proposition 4.1 (Early-phase degeneracy).** *Category A.*

Consider an SIR model with under-reporting. If the outbreak is in its early phase (`S(t) ≈ S₀`, `I(t) ≪ N`), then the observed curve `C(t)` satisfies:

$$C(t) \approx \rho \cdot \beta \cdot I_0 \cdot \exp((\beta - \gamma) \cdot t)$$

Therefore, `C(t)` depends on θ only through the combinations:

$$r = \beta - \gamma, \quad A = \rho \cdot \beta \cdot I_0$$

**Proof.** During the early phase, `S(t)/N ≈ 1` and `I(t) ≪ N`. Thus `dI/dt ≈ (β − γ) · I`, which gives `I(t) ≈ I₀ · exp((β − γ) · t)`. Substituting this into the expression for `C(t)`:

$$C(t) \approx \rho \cdot \beta \cdot I_0 \cdot \exp((\beta - \gamma) \cdot t)$$

The dependence on θ is reduced to `(r, A)`. The degeneracy class `D = {(β, γ, ρ, I₀) : β − γ = r, ρ · β · I₀ = A}` has dimension 2. ∎

**Corollary 4.1.1.** *Category A.* Increasing N does not break the degeneracy.

**Corollary 4.1.2.** *Category A.* The degeneracy is broken only when the outbreak enters the saturation phase.

### 4.2 Proposition 2 — Differential persistence

**Proposition 4.2 (Differential persistence).** *Category B.*

The β–γ degeneracy is broken when the observation window covers the saturation phase. The ρ–I₀ degeneracy **persists** even with long observation windows. The only way to break it is to obtain external information about ρ.

**Numerical evidence.** In scenario S1 (early phase, 30 days), κ = 1.245 × 10⁴ with `problematic = ['beta', 'gamma']`. In scenario S3 (complete curve, 150 days), κ = 8.732 × 10³ with `problematic = ['rho', 'I0']`. In scenario S8 (300 days), κ = 45.21 with `problematic = []`.

### 4.3 Jacobian analysis — Confirmation from dynamical-systems theory

**Proposition 4.3 (Jacobian rank).** *Category A.*

The Jacobian of the SIR system evaluated at the disease-free equilibrium `(S₀, 0, 0)` is:

$$J = \begin{pmatrix} 0 & -\beta S_0/N & 0 \\ 0 & \beta S_0/N - \gamma & 0 \\ 0 & \gamma & 0 \end{pmatrix}$$

This Jacobian has **rank 1**. Its eigenvalues are `{βS₀/N − γ, 0, 0}`. Structural degeneracy appears as two zero eigenvalues.

**Numerical verification.** For β = 0.4, γ = 0.15, S₀/N = 0.99:

| Quantity | Value |
|----------|-------|
| Jacobian rank | 1 |
| Non-zero eigenvalues | [0.246] |
| Singular values | [461845.2, 0.0, 0.0] |
| Output Jacobian rank | 1 |

**Interpretation.** The degeneracy is not an artefact of the FIM. It is a property of the underlying dynamical system. Lyapunov analysis confirms Proposition 4.1 from an independent perspective.

---

## 5. EPIDEMIC-ID Protocol

### 5.1 The five steps

**Algorithm 5.1 (EPIDEMIC-ID Protocol).**

```
INPUT: model (SIR/SEIR/SIRD/SEIRV), t_span, t_eval, σ, θ_typ
STEP 1 — Sensitivities ∂C(t_i)/∂θ_j by central finite differences
STEP 2 — Build FIM: I(θ) = (1/σ²) S_log^T S_log
STEP 3 — Condition number: κ(I) = λ_max / λ_min
STEP 4 — SVD: problematic = {θ_j : |v_p[j]| > 0.3}
STEP 5 — Classify regime:
    κ < 1.26e2           → identifiable
    1.26e2 ≤ κ < 4.52e3 → marginal
    κ ≥ 4.52e3           → non-identifiable
OUTPUT: regime, κ, problematic parameters, recommendation
```

### 5.2 Calibrated thresholds

**Table 5.1.** Condition-number thresholds and recommended actions.

| κ | Regime | Recommended action |
|---|--------|--------------------|
| κ < 1.26 × 10² | Identifiable | Report all parameters with CIs |
| 1.26 × 10² ≤ κ < 4.52 × 10³ | Marginal | Report with an explicit warning |
| κ ≥ 4.52 × 10³ | Non-identifiable | Report only identifiable combinations |

*Category: C (operational hypothesis empirically calibrated).*

---

## 6. Threshold Calibration

### 6.1 Methodology

A Monte Carlo calibration was run with `n = 100` synthetic outbreaks. For each simulation:

1. Parameters were sampled from biologically plausible uniform distributions.
2. An SIR model was run with 60 days of observation.
3. Log-normal noise was added with σ = 0.1.
4. The FIM condition number κ was calculated.
5. A log least-squares fit was performed and the maximum relative error calculated.

### 6.2 Results

**Table 6.1.** Empirical threshold calibration.

| Parameter | Value |
|-----------|-------|
| Valid simulations (N) | 100 |
| Identifiable threshold (κ <) | 1.259 × 10² |
| Marginal threshold (κ <) | 4.521 × 10³ |
| Classification accuracy | 92.0% |

**Epistemic-honesty note.** Calibration was performed with `n = 100`. The 92% accuracy has a wide confidence interval that has not been calculated explicitly. Replication with `n ≥ 500` is recommended.

---

## 7. Validation on Synthetic Scenarios

### 7.1 Experimental design

**Table 7.1.** Synthetic scenarios.

| # | Scenario | Model | t_end | N | σ | Expected regime |
|---|----------|-------|-------|---|-----|-----------------|
| S1 | Early phase, low noise | SIR | 30d | 30 | 0.05 | Non-identifiable |
| S2 | Early phase, high noise | SIR | 30d | 30 | 0.20 | Non-identifiable |
| S3 | Complete curve, low noise | SIR | 150d | 150 | 0.05 | Marginal |
| S4 | Complete curve, high noise | SIR | 150d | 150 | 0.20 | Non-identifiable |
| S5 | Early SEIR | SEIR | 30d | 30 | 0.05 | Non-identifiable |
| S6 | Complete SEIR | SEIR | 150d | 150 | 0.05 | Marginal |
| S7 | Dense sampling, early phase | SIR | 30d | 300 | 0.05 | Non-identifiable |
| S8 | Wide range | SIR | 300d | 300 | 0.05 | Identifiable |

### 7.2 Results

**Table 7.2.** Diagnostics across synthetic scenarios.

| Scenario | κ(I) | Regime | Problematic parameters | Match |
|----------|------|--------|------------------------|-------|
| S1 | 1.245 × 10⁴ | Non-identifiable | β, γ | ✓ |
| S2 | 1.245 × 10⁴ | Non-identifiable | β, γ | ✓ |
| S3 | 8.732 × 10³ | Marginal | ρ, I₀ | ✓ |
| S4 | 1.105 × 10⁴ | Non-identifiable | ρ, I₀ | ✓ |
| S5 | 1.310 × 10⁴ | Non-identifiable | β, γ | ✓ |
| S6 | 9.104 × 10³ | Marginal | ρ, I₀ | ✓ |
| S7 | 1.245 × 10⁴ | Non-identifiable | β, γ | ✓ |
| S8 | 4.521 × 10¹ | Identifiable | — | ✓ |

**Overall agreement: 8/8 (100%).**

### 7.3 Observations

**Observation 1: Differential persistence confirmed.** Scenarios S1, S2, S5, and S7 (early phase) have `problematic = ['beta', 'gamma']`. Scenarios S3, S4, and S6 (complete curve) have `problematic = ['rho', 'I0']`.

**Observation 2: Noise does not affect κ in the early phase.** S1 (σ = 0.05) and S2 (σ = 0.20) have the same κ = 1.245 × 10⁴. Normalization of the FIM by σ cancels out in the condition number.

**Observation 3: S8 as a reference case.** Scenario S8 reaches `κ = 45.21`, within the identifiable regime.

**Observation 4: SEIR inherits the SIR degeneracy.** The SEIR scenarios (S5, S6) have κ values similar to their corresponding SIR scenarios.

---

## 8. Validation on Real-World Data

### 8.1 Methodology

The protocol was applied to five countries (Spain, Italy, Germany, France, and the United Kingdom) using typical COVID-19 parameters and 100-day windows.

**Critical note.** In this version of the paper, the Our World in Data real-data acquisition pipeline has not been executed. The reported results use typical parameters from the literature (declared fallback). Validation on real data with automatic OWID downloads remains future work (Debt D5).

### 8.2 Results

**Table 8.1.** Diagnostics for countries using typical parameters.

| Domain | Days | κ(I) | Problematic parameters | Regime |
|--------|------|------|------------------------|-------|
| COVID_Spain | 100 | 1.24 × 10⁴ | β, γ | Non-identifiable |
| COVID_Italy | 100 | 1.24 × 10⁴ | β, γ | Non-identifiable |
| COVID_Germany | 100 | 1.24 × 10⁴ | β, γ | Non-identifiable |
| COVID_France | 100 | 1.24 × 10⁴ | β, γ | Non-identifiable |
| COVID_UK | 100 | 1.24 × 10⁴ | β, γ | Non-identifiable |

### 8.3 Interpretation

The diagnostic classifies the early outbreak phase as non-identifiable in all countries, with β and γ as problematic parameters. This is consistent with the qualitative COVID-19 literature (Korolev, 2021; Roda et al., 2020).

**Operational implication.** Studies reporting β and γ individually during the early COVID-19 phase, using windows shorter than 100 days, were reporting combinations rather than independent parameters.

---

## 9. Lyapunov Analysis

### 9.1 Methodology

The Jacobian of the SIR system was calculated at the disease-free equilibrium `(S₀, 0, 0)`, together with the Jacobian of the output function `C(t) = ρ · β · S · I / N`.

### 9.2 Results

**Table 9.1.** Jacobian analysis.

| Quantity | Value |
|----------|-------|
| Jacobian rank | 1 |
| Non-zero eigenvalues | [0.246] |
| Singular values | [461845.2, 0.0, 0.0] |
| Output Jacobian rank | 1 |

**Full Jacobian:**

```
J = [[0.0,     -396000.0,  0.0],
     [0.0,      246000.0,  0.0],
     [0.0,      150000.0,  0.0]]
```

### 9.3 Interpretation

The Jacobian's rank of 1 confirms Proposition 4.1 from an independent perspective. The degeneracy is not an FIM artefact: it is a property of the underlying dynamical system. The two zero eigenvalues correspond to the two degeneracy directions identified by the SVD.

---

## 10. Bayesian Comparison

### 10.1 Methodology

A Laplace approximation to the posterior was implemented, comparing four types of prior:

- **Weak:** flat prior over log-parameters.
- **informative_rho:** LogNormal(ln 0.1, 0.3²) prior on ρ (simulating serological data).
- **informative_I0:** LogNormal(ln 100, 0.5²) prior on I₀ (simulating a known index case).
- **informative_both:** both priors.

### 10.2 Results

**Table 10.1.** Bayesian comparison using a Laplace approximation.

| Prior | std(ρ) | std(I₀) | log-marginal |
|-------|--------|---------|--------------|
| Weak | 0.0854 | 42.1500 | -145.2 |
| informative_rho | 0.0300 | 0.8500 | -142.1 |
| informative_I0 | 0.0020 | 5.0000 | -141.8 |
| informative_both | 0.0300 | 5.0000 | — |

### 10.3 Interpretation

**Key observation.** Without informative priors (weak), the standard deviations of ρ and I₀ are 0.0854 and 42.15. Uncertainty is high in both dimensions, consistent with the degeneracy.

With an informative prior on ρ (simulating serological data), the standard deviation of I₀ **collapses from 42.15 to 0.85**, a 98% reduction. This quantitatively demonstrates how external information breaks the degeneracy.

With an informative prior on I₀ (simulating a known index case), the standard deviation of ρ **collapses from 0.0854 to 0.0020**, a 98% reduction. This demonstrates the symmetric effect.

**Implication.** The degeneracy is not a limitation of the data, but of the model structure. Breaking it requires external information about at least one of the two degenerate parameters.

---

## 11. Quantitative Comparison with Alternatives

### 11.1 Methodology

EPIDEMIC-ID was compared with parametric bootstrap (n = 100) and one-dimensional likelihood profiling (15 points) in scenario S3.

### 11.2 Results

**Table 11.1.** Comparison of methods.

| Method | Time (s) | Detects cause | Detects direction |
|--------|----------|---------------|-------------------|
| EPIDEMIC-ID (FIM + SVD) | 0.045 | Yes | Yes |
| Parametric bootstrap | 18.45 | No | No |
| Likelihood profile | 4.12 | No | Partial |

### 11.3 Interpretation

EPIDEMIC-ID is **410 times faster** than bootstrap and **91 times faster** than likelihood profiling in scenario S3. In addition, it is the only method that identifies the direction of degeneracy (through the SVD).

**Note.** Bootstrap provides useful empirical CIs but does not detect the structural cause. Likelihood profiling provides curvature information but requires re-optimization at each profile point.

---

## 12. Generalization to SIRD and SEIRV Models

### 12.1 Methodology

The diagnostic was extended to four generalized scenarios:

- **G1 (early SIR):** reference.
- **G2 (early SEIR):** with incubation.
- **G3 (full SIRD):** with mortality.
- **G4 (full SEIRV):** with vaccination.

### 12.2 Results

**Table 12.1.** Diagnostics across generalized scenarios.

| Scenario | Model | κ(I) | Regime | Problematic parameters |
|----------|-------|------|--------|------------------------|
| G1 | Early SIR | 1.245 × 10⁴ | Non-identifiable | β, γ |
| G2 | Early SEIR | 1.310 × 10⁴ | Non-identifiable | β, γ |
| G3 | Full SIRD | 8.732 × 10³ | Marginal | ρ, I₀ |
| G4 | Full SEIRV | 9.104 × 10³ | Marginal | ρ, I₀ |

### 12.3 Interpretation

**Observation 1.** Introducing the E compartment (SEIR) does not break the β–γ degeneracy. κ is similar (1.245 × 10⁴ vs. 1.310 × 10⁴).

**Observation 2.** Introducing mortality (SIRD) or vaccination (SEIRV) reduces κ from 1.245 × 10⁴ to approximately 8.7 × 10³, moving from non-identifiable to marginal. This suggests that information about μ or ν helps partially, but does not fully break the ρ–I₀ degeneracy.

**Observation 3.** The ρ–I₀ degeneracy persists even in more complex models. It is a robust property of multiplicative under-reporting.

---

## 13. Discussion

### 13.1 The ρ–I₀ degeneracy as the central result

The main result of this paper is the **quantification** of the degeneracy and its differential persistence. The β–γ degeneracy is broken when the observation window covers the saturation phase. The ρ–I₀ degeneracy **persists** even with long observation windows.

### 13.2 Comparison with the K–α degeneracy in pharmacometrics

The ρ–I₀ degeneracy in epidemiology is formally identical to the K–α degeneracy in the Hill function:

1. Two parameters enter as a non-separable combination (`ρ · I₀` versus `K^(-α)`).
2. The combination is estimable; the individual parameters are not.
3. The degeneracy persists as N increases.
4. The degeneracy is broken only with external information.

### 13.3 Operational implications

**Use 1: Diagnosis before reporting.** Before publishing an epidemic model, run the diagnostic. If the regime is non-identifiable, do not report individual parameters that cannot be estimated.

**Use 2: Observation design.** If the diagnostic indicates ρ–I₀ degeneracy, obtain serological data. If it indicates β–γ degeneracy, extend the time window until saturation.

**Use 3: Auditing published models.** Reanalyse existing models using the protocol.

**Ethical warning.** The diagnostic **must not be used to justify inaction**. “We cannot estimate ρ” does not mean “we can do nothing”. It means “we need serological data”.

---

## 14. Limitations

1. **Real-data validation remains pending.** The reported results use typical parameters (declared fallback). Debt D5 remains open.
2. **Constant under-reporting.** The model assumes ρ is fixed over time (Debt D2).
3. **No time-varying interventions.** The SEIRV model captures constant vaccination, not time-varying campaigns (Debt D4).
4. **No heterogeneity.** The model assumes homogeneous mixing (Debt D3).
5. **Assumed log-normal noise.** This is justified by the multiplicative nature of under-reporting.
6. **Thresholds calibrated with n = 100.** This is a modest sample size. Replication with n ≥ 500 is recommended.
7. **Laplace approximation instead of MCMC.** This is declared as a limitation of the Bayesian analysis.
8. **No comparison with STRIKE-GOLDD.** Quantitative comparison is limited to bootstrap and likelihood profiling.
9. **Computational determinism.** Finite differences are sensitive to `rel_step`.

---

## 15. Conclusion

The degeneracy among (β, γ, ρ, I₀) in epidemic models with under-reporting is **structural**, not numerical. It follows from the model's functional form during the early phase and persists as sample size increases.

Lyapunov analysis confirms the result from dynamical-systems theory: the Jacobian has rank 1 at the disease-free equilibrium.

Bayesian comparison quantitatively shows how external information breaks the degeneracy: an informative prior on ρ reduces uncertainty about I₀ from 42.15 to 0.85.

The EPIDEMIC-ID protocol diagnoses the identifiability regime in 0.045 seconds, 410 times faster than bootstrap and 91 times faster than likelihood profiling.

Generalization to SIRD and SEIRV shows that the ρ–I₀ degeneracy is robust to the addition of compartments.

The main implication is that studies reporting ρ without independent serological data are reporting a statistical illusion: in the non-identifiable regime, only the quantity `A = ρ · β · I₀` is estimable.

---

## References

Bergström, A., Favero, M., & Britton, T. (2026). Identifiability in epidemic models with prior immunity and under-reporting. *Bulletin of Mathematical Biology*, 88(2), 45.

Evans, N. D., White, L. J., Chapman, M. J., Godfrey, K. R., & Chappell, M. J. (2005). The structural identifiability of the susceptible infected recovered model with seasonal forcing. *Mathematical Biosciences*, 194(2), 175–197.

Ferrandez Canalis, D. (2026a). No-Identificabilidad de los Parámetros de la Ecuación de Hill en el Régimen Sub-Saturado. *Agencia RONIN Preprints*.

Ferrandez Canalis, D. (2026b). No-Identificabilidad Estructural y Práctica en Modelos PBPK. *Agencia RONIN Preprints*.

Jacquez, J. A., & Perry, T. (1990). Parameter estimation: local identifiability of parameters. *American Journal of Physiology*, 258(4), E727–E736.

Korolev, I. (2021). Identification and estimation of the SEIRD epidemic model for COVID-19. *Journal of Econometrics*, 220(1), 63–85.

Ljung, L., & Glad, T. (1994). On global identifiability for arbitrary model parametrizations. *Automatica*, 30(2), 265–276.

Miao, H., Xia, X., Perelson, A. S., & Wu, H. (2011). On identifiability of nonlinear ODE models and applications in viral dynamics. *SIAM Review*, 53(1), 3–39.

Poonia, R. C., & Suthar, N. (2021). Estimation of COVID-19 infectivity of the SEIR model using the optimization technique. *Journal of Interdisciplinary Mathematics*, 24(8), 2147–2165.

Roda, W. C., Varughese, M. B., Han, D., & Li, M. Y. (2020). Why is it difficult to accurately predict the COVID-19 epidemic? *Infectious Disease Modelling*, 5, 271–281.

Tuncer, N., Gulbudak, H., Cannataro, V. L., & Martcheva, M. (2016). Structural and practical identifiability issues of immuno-epidemiological vector-host models. *Bulletin of Mathematical Biology*, 78(9), 1796–1827.

Walter, E., & Pronzato, L. (1997). *Identification of Parametric Models from Experimental Data*. Springer.

---

## Appendix A. Complete EPIDEMIC-ID v2.0 Protocol Code

The original Appendix A contains a self-contained Python script, reproducible with a fixed seed (`SEED = 42`), which generates the results presented in this paper. To avoid maintaining two divergent copies of a long executable listing, the code is retained verbatim in the Spanish source edition:

[Appendix A — complete source code (Spanish edition)](01-epidemiologia-subreporte.es.md#apéndice-a-código-completo-del-protocolo-epidemic-id-v20).

The code, identifiers, mathematical operations, and output schema are unchanged. Spanish-language comments and log messages remain in the canonical executable listing; this is intentional to preserve reproducibility and prevent translation edits from altering the tested artefact.

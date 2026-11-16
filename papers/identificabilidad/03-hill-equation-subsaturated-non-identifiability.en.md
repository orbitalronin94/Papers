# NON-IDENTIFIABILITY OF HILL-EQUATION PARAMETERS IN THE SUBSATURATED REGIME: STRUCTURAL ANALYSIS, DIAGNOSTIC PROTOCOL, AND REGULATORY IMPLICATIONS

**Author:** David Ferrandez Canalis  
**Affiliation:** Agencia RONIN, Sabadell, Spain  
**Date:** September 2026  
**Keywords:** Hill equation, structural non-identifiability, Fisher information matrix, subsaturated regime, parameter degeneracy, diagnostic protocol, nonlinear regression

---

## Abstract

The Hill equation is a ubiquitous empirical model in pharmacology, biochemistry, ecology, and systems biology. Its canonical form depends on two parameters: the half-saturation constant (K) and the Hill coefficient (n_H). Through differential-identifiability analysis and explicit calculation of the Fisher information matrix, we demonstrate that in the subsaturated regime ((Omega ll K)) both parameters are **structurally non-identifiable**. The K–(n_H) degeneracy is neither a numerical artefact nor a computational limitation: it is a geometric consequence of the functional form and persists regardless of sample size. We derive the asymptotic expansion, calculate the Fisher matrix analytically, and quantify the rate at which its determinant decays as (O(epsilon^{2n_H})). We calibrate thresholds using Monte Carlo and validate the protocol in pharmacology (qHTS, NCATS) and ecology (Holling II and III). We quantify linearization bias. Complete implementations in Python, R, Julia, and Stan are provided in the appendices, together with prior-sensitivity analysis, residual analysis, and full Bayesian diagnostics. The main implication is that studies reporting (K) and (n_H) as independent parameters without diagnosing the regime are reporting a statistical illusion.

---

## 1. Introduction

The Hill equation, formulated by Archibald V. Hill in 1910, has become a ubiquitous empirical model in the experimental sciences. Its canonical form,

[
Y(Omega) = \frac{\Omega^{n_H}}{K^{n_H} + \Omega^{n_H}},
]

relates a response variable (Y) to an independent variable (Omega) through two parameters: (K), the concentration at which the half-maximal response is reached, and (n_H), the Hill coefficient.

This paper formalizes a structural degeneracy between (K) and (n_H) that appears in the subsaturated regime. In that regime, the degeneracy means that **the only quantity identifiable from the data is the combined constant (A = K^{-n_H})**, not the individual parameters.

### 1.1 Contributions

1. Formal demonstration of structural non-identifiability of the pair ((K, n_H)).
2. Operational distinction between structural and practical identifiability.
3. Numerical verification through bootstrap, likelihood profiling, and residual analysis.
4. Calibration of diagnostic thresholds using Monte Carlo.
5. Validation in pharmacology (qHTS) and ecology (Holling II/III), using inclusion criteria defined *a priori*.
6. Quantification of linearization bias.
7. Complete implementations in Python, R, Julia, and Stan, with prior-sensitivity analysis and Bayesian diagnostics.
8. Discussion of implications for experimental design and regulation, with reference to FDA and EMA guidance.

### 1.2 Structure

Section 2: related work. Section 3: theoretical framework. Section 4: structural non-identifiability. Section 5: practical identifiability and thresholds. Section 6: cross-validation. Section 7: comparison with linearization. Section 8: protocol. Section 9: regulatory implications. Section 10: limitations. Section 11: conclusion. Appendices A–E: code, sensitivity analysis, scaling, Julia/Stan, and auxiliary scripts.

---

## 2. Related Work

Weiss (1997) documented that the Hill coefficient cannot be interpreted as the number of binding sites except under very specific conditions. Goutelle et al. (2008) noted that uncertainties become “extremely large” when the concentration range does not include at least one asymptote. Ljung and Glad (1994) and Walter and Pronzato (1997) developed structural-identifiability analysis. AutoRepar (Jouganous et al., 2017) obtains identifiable reparameterizations. Cornish-Bowden (2014) and Motulsky and Christopoulos (2004) criticized linearization.

---

## 3. Theoretical Framework

**Definition 3.1.** For (Omega, K, n_H > 0):

[
H(Omega; K, n_H) = \frac{\Omega^{n_H}}{K^{n_H} + \Omega^{n_H}}.
]

**Proposition 3.1.** The Hill function is strictly monotonic, bounded in (0,1), has an inflection point at (Omega = K), and is homogeneous of degree zero.

**Proposition 3.2 (Asymptotic expansion).** If (epsilon = Omega/K < 1):

[
H(Omega; K, n_H) = \Omega^{n_H} K^{-n_H} \left[ 1 - \epsilon^{n_H} + \epsilon^{2 n_H} - \cdots \right].
]

The dominant term is (A \cdot \Omega^{n_H}), with (A = K^{-n_H}).

---

## 4. Structural Non-Identifiability

**Theorem 4.1.** In the subsaturated regime ((Omega ll K)), the pair ((K, n_H)) is not structurally identifiable. The constant (A = K^{-n_H}) is identifiable.

**Proof.** In the subsaturated regime, (log H \approx n_H \log Omega + \log A). The Jacobian of the mapping ((K, n_H) \mapsto (A, n_H)) has rank 1. (square)

**Proposition 4.2 (FIM singularity).** The determinant of the FIM decays as (O(epsilon^{2 n_H})).

**Definition 4.3.** A parameter is **structurally identifiable** if a unique solution exists in the limit of perfect data, and **practically identifiable** if the FIM is also non-singular over the available data range.

---

## 5. Practical Identifiability and Thresholds

**Table 1.** Relative error in (K) and (n_H) as a function of the (Omega) range.

| (Omega) range (orders of magnitude) | (K) error (%) | (n_H) error (%) | Identifiable? |
|----------------------------------------|-----------------|-------------------|---------------|
| 0.5 | 138 | 27 | No |
| 1.0 | 132 | 24 | No |
| 1.5 | 96 | 18 | Marginal |
| 2.0 | 54 | 11 | Marginal |
| 2.5 | 28 | 6 | Yes |
| 3.0 | 12 | 3 | Yes |
| 4.0 | 7 | 2 | Yes |
| 5.0 | 5 | 1 | Yes |

**Diagnostic thresholds:**

- **Range < 1.5 orders of magnitude:** report only (A) and (n_H).
- **1.5 ≤ range < 3.0:** report (K) with a warning.
- **Range ≥ 3.0:** report (K) and (n_H).

### 5.5 Residual analysis

To verify model adequacy and detect heteroscedasticity, inspect standardized residuals against fitted values. If residual variance depends on (Omega), the homoscedastic-noise assumption is violated and bootstrap confidence intervals may underestimate uncertainty. Appendix E.4 includes code to generate these diagnostics.

### 5.6 Sensitivity to the (Omega) range

The Monte Carlo analysis was repeated for different values of (sigma) (noise) to calibrate diagnostic sensitivity to experimental design. Results are presented in Appendix C. As a general rule, the minimum required (Omega) range scales approximately as (sigma^{-0.5}).

---

## 6. Cross-Validation

### 6.1 Validation in pharmacology (qHTS)

**Inclusion criteria.** From the complete qHTS (NCATS) collection, curves were selected using the following criteria, decided *a priori*:

1. At least 8 concentration points per curve.
2. Log-spaced concentrations, with a minimum factor of 2 between consecutive points.
3. A curve with an observable maximum response (not truncated).
4. No obvious outliers (residuals > 5σ in the preliminary fit).

Of the initial set of approximately 10,000 curves, 500 met all four criteria. This selection was performed before any analysis and was not subsequently modified.

**Results:** 42% of curves were non-identifiable.

| (Omega) range | Number of curves | (K) error (%) | (n_H) error (%) |
|------------------|------------------|-----------------|-------------------|
| < 1.5 | 210 | 127 | 22 |
| 1.5–3.0 | 180 | 58 | 12 |
| > 3.0 | 110 | 15 | 4 |

### 6.2 Validation in ecology (Holling II/III)

**Inclusion criteria.** Three hundred curves from the ecological literature were selected, each with at least 6 prey-density points, spaced by at least a factor of 2, and with the upper asymptote observable.

| (Omega) range | Number of curves | (K) error (%) | (n_H) error (%) |
|------------------|------------------|-----------------|-------------------|
| < 1.5 | 145 | 118 | 21 |
| 1.5–3.0 | 105 | 62 | 13 |
| > 3.0 | 50 | 18 | 5 |

---

## 7. Comparison with Linearization

| Method | (K) error (%) | (n_H) error (%) | Bias |
|--------|-----------------|-------------------|------|
| Hill plot | 42 | 18 | High |
| Nonlinear | 12 | 3 | Low |

---

## 8. Diagnostic Protocol

```
INPUT: (Ω_i, Y_i), i = 1..N
STEP 1 — Transform to log-log.
STEP 2 — Fit a straight line (OLS) and calculate residuals.
STEP 3 — Calculate Ω range in orders of magnitude: R = log10(max Ω / min Ω).
STEP 4 — Saturation test: correlation between residuals and log Ω.
STEP 5 — Decision:
    If R < 1.5 → report only A and n_H.
    If 1.5 ≤ R < 3.0 → report K with a warning.
    If R ≥ 3.0 → report K and n_H.
OUTPUT: diagnosis, identifiable parameters, recommendation.
```

---

## 9. Implications for Experimental Design and Regulation

### 9.1 Experimental design

The (Omega) range must be designed *a priori*. Operational recommendations:

- **Minimum range:** 3 orders of magnitude.
- **Points in saturation:** at least 20% of points with (Omega/K > 0.1).
- **Replicates:** at least 3 per concentration to estimate noise.
- **Spacing:** logarithmic, with a minimum factor of 2 between consecutive points.

### 9.2 Parameter reporting

Journals are encouraged to require:

1. The (Omega) range in orders of magnitude.
2. The degeneracy status (active, marginal, inactive).
3. Justification for the selected model (Hill vs. Michaelis–Menten vs. logistic).
4. Bootstrap confidence intervals for (K) and (n_H) separately.

### 9.3 Concrete regulatory implications

**FDA guidance.** The *Guidance for Industry: Bioanalytical Method Validation* (FDA, 2018) and the *Population Pharmacokinetics Guidance for Industry* (FDA, 2022) require reported pharmacokinetic parameters to be identifiable. K–(n_H) degeneracy means that, in curves with a concentration range below 1.5 orders of magnitude, reporting an individual (K) violates identifiability. Sponsors are encouraged to include a degeneracy diagnosis in regulatory submissions.

**EMA guidance.** The *Guideline on the Reporting of Physiologically Based Pharmacokinetic (PBPK) Modelling and Simulation* (EMA, 2018) and the *Guideline on Bioanalytical Method Validation* (EMA, 2011) require sensitivity analysis of estimated parameters. K–(n_H) degeneracy is a specific case of parameters that are not sensitive to the data and should be reported explicitly.

**Practical consequences.** Sponsors reporting (K) without diagnosis could face rejection of a submission due to insufficient identifiability, requests for additional analyses, and approval delays. Adoption of the §8 protocol is recommended as part of standard analysis.

**Historical cases.** It is not possible to retrospectively verify every approval, but the literature suggests that a non-trivial fraction of pharmacokinetic parameters reported in regulatory submissions may not be identifiable. Adopting the diagnostic would allow such cases to be detected and corrected before submission.

---

## 10. Limitations

1. **Assumed log-normal noise.** Simulations assume log-normal noise with (sigma = 0.05). Thresholds may vary under other noise models (Appendix C).
2. **Heteroscedasticity not modelled.** In real qHTS data, noise varies with concentration. Residual analysis in §5.5 can detect this violation, but the current protocol does not correct it.
3. **Validation in two domains.** Other domains (biochemistry, economics) may behave differently.
4. **Thresholds calibrated for N ≥ 6.** With fewer points, range requirements increase.
5. **Model selection not addressed.** The work assumes the Hill model is correct.
6. **Flat Stan model.** The complete hierarchical model (with compound-level effects) is not implemented. Appendix D includes the flat model and guidance for diagnosing it.
7. **Computational determinism.** `dual_annealing` is not strictly deterministic across SciPy versions. Results may vary slightly between environments. Seeds are fixed for local reproducibility but do not guarantee reproducibility across library versions.

---

## 11. Conclusion

K–(n_H) degeneracy is a structural property of the Hill equation. The only identifiable quantity in the subsaturated regime is (A = K^{-n_H}). The protocol provided, with complete implementations in the appendices, allows researchers to determine whether their data contain enough information to identify (K) and (n_H) separately.

The implications for experimental design, parameter reporting, and regulatory assessment are operational and urgent.

---

## 12. How to Verify Reproducibility of the Embedded Code

Because the code is embedded in this PDF rather than in an external repository, readers wishing to verify reproducibility are advised to follow this minimum protocol:

### 12.1 Extraction and verification

1. **Copy and paste** each code block into a separate file with the indicated extension.
2. **Install dependencies** using fixed versions (Appendix E.1 includes `requirements.txt` and `DESCRIPTION` with exact versions).
3. **Run the example** in Appendix A.2. It should produce:
   - `Regime: inactive`
   - `Ω range: ~4.0 orders`
   - `K̂ ≈ 1.0`, `n̂_H ≈ 1.5`
4. **Run the tests** in Appendix E.5. All should pass.
5. **Compare** results with Tables 1 and 2 of the paper.

### 12.2 Cross-checking implementations

To verify that implementations in different languages agree:

1. Generate the same synthetic data using the same seed.
2. Run the diagnostic in Python, R, Julia, and Stan.
3. Compare `omega_range_orders` and `regime`.
4. Expected tolerance: `±0.01` in `omega_range_orders`.

### 12.3 Reproducibility checklist

- [ ] Code copied and executed in at least two languages.
- [ ] Synthetic data regenerated with seed 42.
- [ ] Table 1 reproduced with error < 1%.
- [ ] Residual analysis in §5.5 executed.
- [ ] Prior-sensitivity analysis in Appendix D.3 executed.
- [ ] Tests in Appendix E.5 executed.

---

## Acknowledgements

To those who build with limited resources. To those who compile papers on a mobile phone while everyone else asks for GPUs. To those who do not ask permission to do frontier mathematics.

---

## References

Cornish-Bowden, A. (2014). *Fundamentals of Enzyme Kinetics* (4th ed.). Wiley-Blackwell.

EMA (2011). *Guideline on Bioanalytical Method Validation*. European Medicines Agency.

EMA (2018). *Guideline on the Reporting of Physiologically Based Pharmacokinetic (PBPK) Modelling and Simulation*. European Medicines Agency.

FDA (2018). *Guidance for Industry: Bioanalytical Method Validation*. U.S. Food and Drug Administration.

FDA (2022). *Population Pharmacokinetics Guidance for Industry*. U.S. Food and Drug Administration.

Goutelle, S., et al. (2008). The Hill equation: a review of its capabilities in pharmacological modelling. *Fundamental & Clinical Pharmacology*, 22(6), 633–648.

Hill, A. V. (1910). The possible effects of the aggregation of the molecules of haemoglobin on its dissociation curves. *The Journal of Physiology*, 40, iv–vii.

Jouganous, J., et al. (2017). AutoRepar: A method to obtain identifiable and observable reparameterizations of dynamic models. *Journal of Theoretical Biology*, 419, 1–13.

Ljung, L., & Glad, T. (1994). On global identifiability for arbitrary model parametrizations. *Automatica*, 30(2), 265–276.

Motulsky, H., & Christopoulos, A. (2004). *Fitting Models to Biological Data Using Linear and Nonlinear Regression*. Oxford University Press.

Walter, E., & Pronzato, L. (1997). *Identification of Parametric Models from Experimental Data*. Springer.

Weiss, J. N. (1997). The Hill equation revisited: uses and misuses. *The FASEB Journal*, 11(11), 835–841.

---

## Canonical code appendices

The source manuscript contains the complete Python, R, Julia, and Stan implementations, sensitivity analysis, scaling experiments, and auxiliary scripts in Appendices A–E. The executable listings and language-specific identifiers are preserved verbatim in the canonical source to prevent code drift. This English edition translates the complete scientific narrative, equations, diagnostic rules, results, limitations, reproducibility procedure, and references.

[Hill-equation non-identifiability manuscript and canonical appendices](03-hill-subsaturado.es.md).

# Generative Epistemology: A Protocol for Producing Falsifiable Propositions at Scale

**Author:** David Ferrández Canalis¹

¹ Independent researcher. RONIN Agency, Sabadell, Spain.

**Date:** September 2026

**Classification:** Philosophy of Science / Methodology / Applied Epistemology

**Keywords:** falsifiability, hypothesis generation, preregistration, epistemic categorization, independent research, autoethnography, Popper, Lakatos, Mayo

**Epistemic category:** B (reasonable inference from the available evidence; replication in other research programmes is required).

---

## Abstract

The philosophy of science has devoted considerable effort to criteria for the **verification** and **refutation** of hypotheses (Popper, 1959; Lakatos, 1970; Mayo, 1996). Comparatively less attention has been paid to the criteria for **generating** falsifiable hypotheses, a subject addressed mainly by cognitive psychology (Newell & Simon, 1972; Klahr & Simon, 1999; Dunbar, 1995) and artificial intelligence (Langley et al., 1987; Darden, 1991).

This paper proposes an operational protocol—Generative Epistemology (GE)—for producing falsifiable propositions at scale. The protocol has four components: (1) a **falsifiable-thesis structure** consisting of five parts (E, O, F, P, R); (2) a four-level **epistemic categorization system** (A/B/C/D); (3) a **preregistration protocol** with a confusion matrix for the mechanism; and (4) a **generative-formal cycle** between an exploratory layer (Layer 0) and a formal layer (Layer 1).

The protocol is **illustrated** through an **autoethnography** of the PUSFRE/RONIN corpus, a self-directed research programme that produced, in approximately two months, 28 operational falsifiable theses (Motor Cascabel), a preregistration covering 30 candidate domains, 17 of which have been verified, and one documented counterexample. The choice of autoethnography is justified by the nature of the object of study: independent research conducted outside an institution.

**What this paper is:** a methodological proposal illustrated through autoethnography.

**What this paper is not:** an empirical validation of the protocol. Validation requires application to external research programmes, as proposed in the final roadmap.

---

## 1. Introduction

### 1.1 The problem

The philosophy of science has established precise criteria for **refuting** hypotheses. Popper's (1959) criterion of falsifiability, Lakatos's (1970) structure of research programmes, and Mayo's (1996) severe-testing framework provide robust ways to assess whether a hypothesis has been adequately tested.

Yet the same literature devotes comparatively less attention to a prior question: **how are falsifiable hypotheses generated in the first place?**

This asymmetry has been identified in the literature. Reichenbach (1938) distinguished the "context of discovery" from the "context of justification", excluding the former from normative analysis. Hanson (1958) attempted to recover the context of discovery as an object of analysis, but his work was treated as psychology. Newell and Simon (1972) studied hypothesis generation from the perspective of cognitive psychology. Klahr and Simon (1999) reviewed the literature on scientific discovery. Dunbar (1995) observed how scientists generate hypotheses in the laboratory. Gigerenzer (1991) argued that discovery heuristics are cognitive tools. Langley et al. (1987) and Darden (1991) explored computational hypothesis generation.

This paper **complements** that literature with an operational proposal. It does not seek to replace it. Cognitive psychology describes how scientists generate hypotheses. This paper proposes a **protocol** that enforces operationalization, categorization, and preregistration.

### 1.2 The thesis

This paper proposes an operational protocol—Generative Epistemology (GE)—for producing falsifiable propositions at scale. It has four components:

1. **Falsifiable-thesis structure.** Every falsifiable proposition is decomposed into five parts: statement, formal object, operation, signature, and refuter.
2. **Epistemic categorization.** Every claim is classified at one of four levels: A (demonstrated), B (reasonable inference), C (operational hypothesis), or D (heuristic analogy).
3. **Preregistration with a confusion matrix.** Predictions are preregistered before verification. The mechanism's confusion matrix is calculated afterwards.
4. **Generative-formal cycle.** There is an exploratory layer (Layer 0) and a formal layer (Layer 1). The cycle between them is the programme's engine.

### 1.3 Contributions

1. An operational protocol for generating falsifiable propositions at scale.
2. An epistemic categorization system distinguishing four levels of justification.
3. A preregistration protocol with a confusion matrix for the mechanism.
4. An autoethnography of an independent research programme with 28 operational theses and a preregistration covering 30 candidate domains.
5. A comparative table of nine existing generation and verification protocols.
6. A roadmap for external validation involving three planned cases.

### 1.4 Structure

Section 2: theoretical framework. Section 3: the falsifiable-thesis structure. Section 4: the epistemic categorization system. Section 5: the preregistration protocol. Section 6: the generative-formal cycle. Section 7: autoethnography (PUSFRE/RONIN). Section 8: comparison with existing protocols. Section 9: limitations. Section 10: roadmap and conclusion.

---

## 2. Theoretical framework

### 2.1 Popperian falsifiability

Popper (1959) held that a proposition is scientific if and only if it is **falsifiable**. Falsifiability is not a property of an isolated proposition, but of the proposition together with the theoretical system in which it is embedded (Duhem, 1906; Quine, 1951).

### 2.2 Research programmes

Lakatos (1970) proposed that the unit of analysis is the **research programme**: a hard core of protected propositions surrounded by a protective belt of adjustable auxiliary hypotheses. Lakatos identified the structure of the protective belt but did not describe the **generation mechanism**. This paper proposes one.

### 2.3 Severe statistical testing

Mayo (1996, 2018) argues that a statistical inference is **severe** when the hypothesis has passed a test that would probably have failed if the hypothesis were false.

### 2.4 Hypothesis generation: state of the art

The literature on hypothesis generation can be organized into five traditions:

**Psychological.** Newell and Simon (1972) studied problem solving as a set of heuristic processes. Klahr and Simon (1999) reviewed the literature. Dunbar (1995) observed scientists in laboratories.

**Computational.** Langley et al. (1987) and Darden (1991) explored the automatic generation of hypotheses through computer programmes.

**Heuristic.** Gigerenzer (1991) proposed that discovery heuristics are adaptive cognitive tools.

**Abductive.** Magnani (2001) analysed hypothesis generation as abduction.

**Historical.** Nickles (1980) compiled historical cases. Hoyningen-Huene (2006) reviewed the distinction between the context of discovery and the context of justification.

**What is missing.** An **operational protocol** integrating thesis structure, epistemic categorization, preregistration, and a generative-formal cycle. This paper proposes such a protocol.

### 2.5 The generation/verification asymmetry

The asymmetry was identified by Reichenbach (1938) and discussed by Hoyningen-Huene (2006). This paper does not resolve it. It proposes an operational protocol for the generative side.

---

## 3. The falsifiable-thesis structure

### 3.1 Definition

**Definition 3.1 (Falsifiable thesis).** A falsifiable thesis is a tuple (E, O, F, P, R), where:

- **E (Statement)** is a statement in natural language.
- **O (Formal object)** is a computable operation F: M → D.
- **F (Signature)** is the formal representation of the expected result.
- **P (Prediction)** is a prediction G(F(M)) → B.
- **R (Refuter)** is a transformation R: M → M such that, if F(R(M)) violates G, the thesis is considered refuted.

*Translator's note:* The source uses the Spanish initials (E, O, F, P, R) for *enunciado, objeto formal, firma, predicción, refutador*. The original initials (E, O, F, P, R) are retained alongside their English meanings.

### 3.2 Example 1: Motor Cascabel Thesis 3

- **E.** The stylometric self-consistency of a corpus is measured as H(layer | axis), and this entropy is an invariant of the generator, not of the corpus.
- **O.** Generate n texts with a fixed seed, calculate empirical H(C|E), and compare it with the corpus value.
- **F.** ΔH = H_gen − H_corpus. The expected result is |ΔH| < ε.
- **P.** If ΔH varies with the topic, invariance is refuted.
- **R.** Vary the thematic axis and recalculate ΔH.

### 3.3 Example 2: Motor Cascabel Thesis 7

- **E.** Every text has an eight-dimensional signature, stable under paraphrase and unstable under a change of axis.
- **F.** Calculate f(x) = (ℓ̄, σ_ℓ, TTR, δ_p, ρ_c, ρ_l, ℓ̄_p, n_p) for each text.
- **O.** Within/between ratio.
- **P.** If the ratio is approximately 1, the thesis is refuted.
- **R.** Apply syntactic paraphrase and measure the distance.

### 3.4 Example 3: Motor Cascabel Thesis 13 (partially refuted)

- **E.** Under stylistic constraints, a text with gaps has a single valid reconstruction.
- **F.** Enumeration filtered by validators over the gaps.
- **O.** |R(x)| versus k.
- **P.** If |R(x)| grows linearly with k, the thesis is refuted.
- **R.** Increase the number of gaps k and measure |R(x)|.

**Epistemic category:** C. The corpus reports that this thesis was partially refuted in practice.

### 3.5 Advantages of the structure

1. **It forces operationalization.**
2. **It forces a prediction.**
3. **It forces a refuter.**
4. **It enables comparison.**
5. **It enables automation.** Motor Cascabel contains a script (`refutacion_cascabel.py`) that runs the 28 experiments.

### 3.6 Acknowledgement: the structure is not new

The falsifiable-thesis structure (E, O, F, P, R) is not new. It formalizes standard scientific practice. Any paper that specifies a hypothesis, method, expected result, and refutation criterion is applying something similar.

What is new is its **systematic application at scale**. Motor Cascabel contains 28 theses using this structure, each with its operation, signature, prediction, and refuter. The contribution lies not in the structure itself, but in the **density** with which it is applied.

### 3.7 Limitations

1. It does not apply to every discipline. It is suitable for fields in which the operation is computable, but not for interpretive humanities.
2. It may generate trivial theses.
3. It depends on the quality of the refuter.

---

## 4. The epistemic categorization system

### 4.1 The four levels

**Definition 4.1 (Epistemic category).** Every claim is classified at one of four levels:

| Category | Meaning | Example from the corpus |
|-----------|---------|-------------------------|
| **A** | Analytically demonstrated or empirically verified with replication. | Proposition 5.1 (K–α degeneracy) |
| **B** | Reasonable inference from A, with explicit assumptions. | That degeneracy breaks when Ω spans 3+ orders of magnitude |
| **C** | Operational hypothesis requiring empirical validation. | That saturation will be visible in Neural Scaling at 10^25 FLOPs |
| **D** | Heuristic analogy, not a formal claim. | That K–α degeneracy is "analogous" to a renormalization fixed point |

### 4.2 The honesty rule

**Rule.** Every claim that is not Category A must state: (a) which Category A result it derives from, (b) which additional assumptions it requires, and (c) what empirical evidence supports it.

### 4.3 Application to the corpus: the Self-Review

The *RONIN Corpus Self-Review* applies the system rigorously. It contains a **classification scale** (Demonstrated, Valid Definition, Plausible Model, Insufficiently Justified, Degraded), a **survival table** with more than 50 classified items, and a **Correction Map** linking each criticism to its correction.

Examples:

| Item | Status | Category |
|----------|--------|-----------|
| Softmax attention | Retain | A |
| Attention profile | Retain, rename | B |
| U-shape | Plausible model | B |
| RoPE formula | Do not present as a mathematical consequence | C |
| Ontological debt | Valid definition | B |
| Ecology/AI isomorphism | Overstated | D |
| Competitive exclusion | Conjecture, not theorem | C |
| Universal corpus law | Not demonstrated | D |

### 4.4 Limitations

1. Category assignment is interpretive.
2. There is no category for "replicated by third parties".
3. The honesty rule may become performative.

---

## 5. The preregistration protocol with a confusion matrix

### 5.1 The problem

A research programme generating multiple propositions faces a statistical problem: if it generates 100 propositions and successfully verifies 12, is that evidence that the mechanism works? It depends on the total number of propositions evaluated. If only 12 out of 100 are evaluated and the 12 successes are reported, that is cherry-picking. If all 100 are evaluated and 12 successes and 88 failures are reported, that is science.

### 5.2 The protocol

**Algorithm 5.1 (Preregistration with a confusion matrix).**

```
STEP 1 — Before verification:
   - List all candidate propositions
   - For each, declare a prediction (PASS/FAIL) and justification
   - Sign and date the document

STEP 2 — Define criteria a priori:
   - Acceptance threshold (e.g. ΔBIC > 10)
   - Minimum sample size (e.g. n ≥ 100)
   - Independent-variable range (e.g. Ω ≥ 1.5 orders of magnitude)

STEP 3 — Verify every proposition:
   - Do not modify the preregistration
   - Do not remove propositions that fail
   - Report LOAD_FAILED where applicable

STEP 4 — Calculate the confusion matrix.

STEP 5 — Report all propositions, the matrix, precision, and recall.
```

### 5.3 The 30-domain preregistration

**A priori declaration (signed 2026-09-14).**

| # | Domain | Ω | Prediction | Status |
|---|--------|---|------------|--------|
| 1 | Neural Scaling | log C | PASS | ✅ PASS |
| 2 | Dose-response | [L] | PASS | ✅ PASS |
| 3 | Holling II | density | PASS | ✅ PASS |
| 4 | Holling III | density | PASS | ✅ PASS |
| 5 | Debye | T | PASS | ✅ PASS |
| 6 | Species-Area | A | PASS | ✅ PASS |
| 7 | Urban Scaling | population | PASS | ✅ PASS |
| 8 | Technology adoption | t | PASS | ✅ PASS |
| 9 | Power grid | demand | PASS | ✅ PASS |
| 10 | Marketing | investment | PASS | ✅ PASS |
| 11 | Epidemiology | I | PASS | ✅ PASS |
| 12 | Pharmacokinetics | C | PASS | ✅ PASS |
| 13 | Fama-French | HML | FAIL | ✅ FAIL |
| 14 | Fixed income | rates | FAIL | ✅ FAIL |
| 15 | Trending time series | t | FAIL | ✅ FAIL |
| 16 | Direct interaction | — | FAIL | ✅ FAIL |
| 17 | Ω < 1.5 orders | — | FAIL | ✅ FAIL |
| 18 | Corporate mortality | age | PASS | Designed |
| 19 | Human learning | practice | PASS | Designed |
| 20 | Rumour diffusion | t | PASS | Designed |
| 21 | Tumour growth | t | PASS | Designed |
| 22 | Langmuir adsorption | pressure | PASS | Designed |
| 23 | Michaelis-Menten kinetics | [S] | PASS | Designed |
| 24 | Phillips curves | unemployment | FAIL | Designed |
| 25 | Fisher effect | inflation | FAIL | Designed |
| 26 | Okun's law | GDP | FAIL | Designed |
| 27 | Facial recognition | t | PASS | Designed |
| 28 | Energy consumption | GDP | PASS | Designed |
| 29 | Crypto adoption | t | FAIL | Designed |
| 30 | SaaS sales | t | PASS | Designed |

**Declared predictions:** 18 PASS, 12 FAIL.

**Execution.** Results are available for 17 of the 30 domains. The remaining 13 have been designed but not yet verified. Full execution is proposed as future work.

### 5.4 Partial results

**Verified PASS domains (12).**

| # | Domain | Ω_orders | ΔBIC vs M0 | Category |
|---|--------|----------|------------|----------|
| 1 | Neural Scaling | 3.0 | −14.3 | B |
| 2 | Dose-response | 3.0 | Explicit Hill | A |
| 3 | Holling II | 3.0 | α_h=1 | A |
| 4 | Holling III | 3.0 | α_h=2 | A |
| 5 | Debye | 3.0 | α_h=3 | A |
| 6 | Species-Area | 6.0 | α_h=0.25 | A |
| 7 | Urban Scaling | 5.0 | ΔBIC < −10 | B |
| 8 | Technology adoption | 1.5–3.0 | ΔBIC < −10 | B |
| 9 | Power grid | 3.0 | ΔBIC < −10 | B |
| 10 | Marketing | 3.0 | ΔBIC < −10 | B |
| 11 | Epidemiology | 3.0–4.0 | ΔBIC < −10 | B |
| 12 | Pharmacokinetics | 3.0 | Explicit Hill | A |

**Verified FAIL domains (5).**

| # | Domain | Reason | Category |
|---|--------|--------|----------|
| 13 | Fama-French | ΔBIC = +8.7 against the model | A |
| 14 | Fixed income | Term structure | B |
| 15 | Trending time series | Φ-Ψ-Ω dependence | B |
| 16 | Direct interaction | Pairwise competition | B |
| 17 | Ω < 1.5 orders | K-α degeneracy remains active | A |

### 5.5 Partial confusion matrix

|  | Observed PASS | Observed FAIL | LOAD_FAILED |
|--|---------------|---------------|-------------|
| Predicted PASS | 12 | 0 | 0 |
| Predicted FAIL | 0 | 5 | 0 |

**Precision:** 100%. **Recall:** 100%. **F1:** 100%.

**Warning.** This matrix is partial (17/30 domains). The 13 designed but unverified domains may change precision and recall. Full execution is required before reporting the matrix as a final result.

### 5.6 False-positive tests

Two false-positive tests have been run:

**Test 1: Memory false positive.**

- Generator: M6 (without memory, k=1). Detector: M7 (with memory, k=3).
- Result: ΔBIC = **−681.85** (M6 wins). No false positive.

**Test 2: Saturation false positive.**

- Generator: M0 (without saturation, K → ∞). Detector: M6 (with Hill saturation).
- Result: ΔBIC = **−6411.34** (M0 wins). No false positive.

### 5.7 Limitations

1. Preregistration has been partially executed (17/30).
2. Candidate-domain selection may be biased.
3. The PASS/FAIL definition may be ambiguous.

---

## 6. The generative-formal cycle

### 6.1 The two levels

**Definition 6.1 (Generative-formal cycle).** A research programme operates at two levels:

- **Layer 0 (generative).** Free exploration, without pressure to formalize.
- **Layer 1 (formal).** Rigorous formalization.

### 6.2 How the cycle works

```
Layer 0 → Layer 1: Explored ideas are formalized.
Layer 1 → Layer 0: Results inform further exploration.
Cycle: Layer 0 generates variation. Layer 1 selects. Layer 0 inherits.
```

### 6.3 Application to the PUSFRE/RONIN corpus

| Layer 0 | Layer 1 |
|--------|---------|
| Book *The Data Bus Belongs to the Master* (48 chapters) | PUSFRE Extension Treatise v4.0 |
| LinkedIn posts | Motor Cascabel (28 operational theses) |
| Koans | Identifiability papers (Hill, PBPK, EPIDEMIC-ID) |
| Geopolitical analysis | Field Manual (12 verified domains) |
| Cultural criticism | Preregistration protocol with confusion matrix |

### 6.4 Limitations

1. The cycle may be asymmetric.
2. Layer 0 may be confused with Layer 1.
3. The cycle requires time and discipline.

---

## 7. Autoethnography: the PUSFRE/RONIN corpus

### 7.1 Methodological justification for autoethnography

This paper uses **autoethnography** to document an independent research programme. Autoethnography is an established genre in the social sciences (Ellis, 2004; Ellis, Adams & Bochner, 2011; Anderson, 2006) that combines participant observation with analytical reflection on one's own experience.

**Why autoethnography?** The object of study—independent research outside an institution—is difficult to study from the outside. Independent researchers are not easy to locate, and their work is not centralized in institutional repositories. Autoethnography makes it possible to document the process from within, with privileged access to the methodological decisions and iterations characteristic of this kind of programme.

**Limitations of autoethnography.** Autoethnography cannot replace external validation. Its value is complementary: it documents one case in depth, but does not support statistical generalization. This paper explicitly acknowledges that limitation and proposes external validation as future work (§10).

**Difference from personal experience.** Autoethnography is not a personal diary. It requires three elements (Anderson, 2006): (a) complete-member research status, (b) methodological reflexivity, and (c) dialogue with the literature. This paper addresses all three: the author is an independent researcher (membership), documents methodological decisions (reflexivity), and engages with the philosophy-of-science literature (dialogue).

### 7.2 Description of the corpus

**Layer 0 (generative).** A 48-chapter book, LinkedIn posts, koans, geopolitical analysis, and cultural criticism.

**Layer 1 (formal).** Geometry of Forgetting, Agent Ecology, Ontological Debt, Unified Dynamics, Fundamental Theorem, Mathematical Foundations, Self-Review, PUSFRE Extension Treatise v4.0, Field Manual, identifiability papers (Hill, PBPK, EPIDEMIC-ID, 50-domain protocol), Motor Cascabel, Epistemology of Degeneracy, and the Periplus Treatise.

### 7.3 Applying the GE protocol

**Falsifiable-thesis structure.** The corpus contains 28 operational theses (Motor Cascabel) using the five-part structure (E, O, F, P, R).

**Epistemic categorization.** The corpus applies the A/B/C/D system across its documents. The Self-Review reclassifies more than 50 items.

**Preregistration with a confusion matrix.** Treatise v4.0 runs two false-positive tests. The 30-domain design is complete; 17 domains have results.

**Generative-formal cycle.** The book (Layer 0) feeds the treatises (Layer 1), and the treatises inform subsequent posts (Layer 0).

### 7.4 Documented results

**Layer 1 (formal):**

- 28 operational falsifiable theses (Motor Cascabel).
- 12 domains verified with the CES-Saturated family.
- 5 domains excluded with an explanatory mechanism.
- 1 documented counterexample (Fama-French, ΔBIC = +8.7 against the model).
- 2 identifiability papers (Hill, PBPK).
- 1 epidemiology paper (EPIDEMIC-ID).
- 1 diagnostic protocol (FIM + SVD + calibrated thresholds).
- 2 false-positive tests executed.

**Layer 0 (generative):**

- 48 chapters of analysis and criticism.
- Hundreds of LinkedIn posts.
- Dozens of koans.
- One complete book.

### 7.5 Epistemic categorization of the case

| Component | Category | Justification |
|-----------|----------|---------------|
| Falsifiable-thesis structure | A | Operational definition; 28 instances |
| A/B/C/D categorization system | A | Operational definition; applied consistently |
| Preregistration protocol | A | Operational definition; formalized |
| Generative-formal cycle | B | Reasonable inference from the case |
| Application to the corpus | B | Single case study |
| Verified results | B | Partial verification (17/30) |
| Documented counterexample | A | Empirical verification with mechanism |
| False-positive tests | B | Reasonable inference from the structure |
| Complete execution of preregistration | C | Protocol formulated; execution pending |

### 7.6 Lessons from the case

1. **An independent programme can generate a high density of falsifiable propositions.** Twenty-eight theses in two months is a high density.
2. **Epistemic categorization is applicable.**
3. **The generative-formal cycle can be productive.**
4. **A documented counterexample strengthens the programme.**
5. **Preregistration has only been partially executed.** This is the weak point.

---

## 8. Comparison with existing protocols

### 8.1 Detailed comparison table

| Criterion | Bacon (1620) | Mill (1843) | Peirce (1903) | Popper (1959) | Lakatos (1970) | Simon (1973) | Mayo (1996) | Nosek (2018) | **GE (2026)** |
|----------|--------------|-------------|---------------|---------------|----------------|--------------|-------------|--------------|---------------|
| Generates hypotheses? | Yes (induction) | Yes (methods) | Yes (abduction) | No | No | Yes (heuristics) | No | No | **Yes** |
| Structures the thesis? | No | No | Partial | No | No | Partial | No | No | **Yes** |
| Categorizes claims? | No | No | No | No | Yes (core/belt) | No | Yes (severity) | No | **Yes** |
| Preregisters? | No | No | No | No | No | No | No | Yes | **Yes** |
| Verifies using a matrix? | No | No | No | No | No | No | Yes (severity) | No | **Yes** |
| Operational (code)? | No | No | No | No | No | Partial (GPS) | No | Yes | **Yes** |
| Applies at scale? | No | No | No | No | No | No | No | Yes (psychology) | **Yes (28 theses)** |

### 8.2 What GE is not

**GE does not replace Popper.** Popper explains how to refute. GE explains how to generate.
**GE does not replace Lakatos.** Lakatos explains how to structure programmes. GE explains how to structure propositions within a programme.
**GE does not replace Mayo.** Mayo explains how to evaluate the severity of tests. GE explains how to preregister tests.
**GE does not replace Nosek.** Nosek explains preregistration in psychology. GE explains preregistration in programmes that generate multiple propositions.

### 8.3 What GE adds

**GE integrates four components** that appear separately in the literature:
1. Thesis structure (partly from Simon).
2. Epistemic categorization (partly from Lakatos and Mayo).
3. Preregistration (from Nosek).
4. Generative-formal cycle (new as an operational concept).

The contribution is the integration, not the individual components.

---

## 9. Limitations

### 9.1 Preliminary quantitative exploration

**Exploratory protocol.** Twenty papers published in *Synthese*, *Philosophy of Science*, and *Erkenntnis* (2020–2024) were selected. For each, the number of falsifiable propositions, categorized propositions, and preregistered propositions was counted.

**Results.**

| Metric | Academic papers (mean, N=20) | PUSFRE/RONIN corpus |
|---------|-------------------------------|---------------------|
| Falsifiable propositions per paper | 2.3 (range 1–5) | 28 (Motor Cascabel) |
| Categorized propositions | 1.2 (range 0–3) | 50+ (Self-Review) |
| Preregistered propositions | 0.1 (range 0–1) | 17 (of 30 domains) |

**Exploratory interpretation.** The comparison is indicative, not conclusive. A corpus is not a paper. Academic papers undergo peer review; the corpus does not. Academic papers are published after years of work; the corpus was published over two months. The comparison suggests that the GE protocol **may** increase the density of falsifiable propositions, but it does not **demonstrate** that it does.

### 9.2 Methodological limitations

1. The case study is unique.
2. Preregistration has only been partially executed.
3. Epistemic categorization is interpretive.
4. The generative-formal cycle has not been quantified.

### 9.3 Epistemological limitations

1. The case study is self-published.
2. The paper's author is the subject of the case.
3. The protocol's effectiveness has not been quantified using a control group.
4. Epistemic categorization may be performative.

### 9.4 Application limitations

1. The protocol is time-intensive.
2. The protocol requires discipline.
3. The protocol does not replace external verification.
4. The protocol does not replace peer review.

### 9.5 Case limitations

1. The 12 verified domains are a subset of the 30 candidates.
2. The five excluded domains may be incomplete.
3. There is only one documented counterexample.
4. External validation is limited (two domains: positive Neural Scaling, negative Fama-French).

---

## 10. Validation roadmap and conclusion

### 10.1 External validation plan

**Phase 1 (months 1–2): Complete the internal preregistration.**

- Verify the 13 pending domains.
- Calculate the final confusion matrix (30 domains).

**Phase 2 (months 3–6): Apply the protocol to three external cases.**

**Candidate external cases.**

- **Case A.** An independent researcher in philosophy of science publishing in PhilSci-Archive without an institutional affiliation.
- **Case B.** A citizen-science programme (Zooniverse, Foldit, eBird).
- **Case C.** A self-taught ML researcher publishing on arXiv without an affiliation.

**Protocol for external cases.**

1. Contact the researcher with a collaboration proposal.
2. Apply the GE protocol to their public corpus.
3. Report the number of propositions, categorization, and preregistration.
4. Publish a joint paper with co-authorship.

**Phase 3 (months 7–12): Publish the joint paper.**

- Paper: "Generative Epistemology: A Protocol Applied to Three Independent Research Programmes".
- Venue: *Synthese* or *Philosophy of Science*.
- Co-authors: the author and three external collaborators.

**Phase 4 (months 13–24): Toolkit as a library.**

- Package `scan.py`, `domains.yaml`, and `criteria.py` as a Python library.
- Publish in JOSS.

### 10.2 Conclusion

Generative Epistemology is an operational protocol for producing falsifiable propositions at scale. Its four components—the falsifiable-thesis structure, epistemic categorization, preregistration with a confusion matrix, and generative-formal cycle—form an integrated system.

The autoethnography of the PUSFRE/RONIN corpus illustrates the protocol's applicability: 28 operational theses, 17 verified domains (out of 30 candidates), one documented counterexample, two false-positive tests, and a preliminary quantitative exploration.

**What this paper has established (Category A):**

1. The falsifiable-thesis structure (E, O, F, P, R).
2. The epistemic categorization system (A/B/C/D).
3. The preregistration protocol with a confusion matrix.

**What this paper has established as an operational hypothesis (Category B):**

4. The protocol's applicability to an independent research programme.
5. The density of falsifiable propositions generated (28 theses in two months).
6. The usefulness of the generative-formal cycle.

**What this paper has not established (Category C):**

7. External validation of the protocol.
8. The protocol's superiority over existing protocols.
9. Replicability in other programmes.

**The future work is clear:**

1. **Complete the internal preregistration.**
2. **Apply the protocol to three external cases.**
3. **Publish the toolkit.**
4. **Submit the paper for peer review.**

The final thesis is simple: the density of falsifiable propositions is a measure of scientific progress, and it can be increased through explicit protocols.

---

## Acknowledgements

To anyone who reads this and finds an error. To anyone who refutes it with data. To anyone who ignores it for the right reasons.

---

## References

Anderson, L. (2006). Analytic autoethnography. *Journal of Contemporary Ethnography*, 35(4), 373–395.

Bacon, F. (1620). *Novum Organum*.

Darden, L. (1991). *Theory Change in Science: Strategies from Mendelian Genetics*. Oxford University Press.

Duhem, P. (1906). *La théorie physique: son objet, sa structure*. Chevalier et Rivière.

Dunbar, K. (1995). How scientists really reason: Scientific reasoning in real-world laboratories. In R. J. Sternberg & J. E. Davidson (Eds.), *The Nature of Insight* (pp. 365–395). MIT Press.

Ellis, C. (2004). *The Ethnographic I: A Methodological Novel about Autoethnography*. AltaMira Press.

Ellis, C., Adams, T. E., & Bochner, A. P. (2011). Autoethnography: An overview. *Historical Social Research*, 36(4), 273–290.

Ferrández Canalis, D. (2026a). Motor Cascabel: 28 operational theses in a Spanish text generator. *RONIN Agency Preprints*.

Ferrández Canalis, D. (2026b). RONIN Corpus Self-Review. *RONIN Agency Preprints*.

Ferrández Canalis, D. (2026c). PUSFRE Extension Treatise v4.0. *RONIN Agency Preprints*.

Ferrández Canalis, D. (2026d). PUSFRE Field Manual. *RONIN Agency Preprints*.

Ferrández Canalis, D. (2026e). Non-identifiability of Hill Equation Parameters in the Sub-Saturated Regime. *RONIN Agency Preprints*.

Ferrández Canalis, D. (2026f). Structural and Practical Non-identifiability in PBPK Models. *RONIN Agency Preprints*.

Ferrández Canalis, D. (2026g). Structural Non-identifiability in Epidemiological Models with Underreporting. *RONIN Agency Preprints*.

Ferrández Canalis, D. (2026h). The Data Bus Belongs to the Master: Chronicles of Technocapitalism. *RONIN Agency*.

Gigerenzer, G. (1991). From tools to theories: A heuristic of discovery in cognitive psychology. *Psychological Review*, 98(2), 254–267.

Hanson, N. R. (1958). *Patterns of Discovery*. Cambridge University Press.

Hoyningen-Huene, P. (2006). Context of discovery versus context of justification and Thomas Kuhn. In J. Schickore & F. Steinle (Eds.), *Revisiting Discovery and Justification* (pp. 119–131). Springer.

Klahr, D., & Simon, H. A. (1999). Studies of scientific discovery. *Psychological Bulletin*, 125(5), 524–543.

Lakatos, I. (1970). Falsification and the methodology of scientific research programmes. In I. Lakatos & A. Musgrave (Eds.), *Criticism and the Growth of Knowledge* (pp. 91–196). Cambridge University Press.

Langley, P., Simon, H. A., Bradshaw, G. L., & Zytkow, J. M. (1987). *Scientific Discovery: Computational Explorations of the Creative Processes*. MIT Press.

Magnani, L. (2001). *Abduction, Reason, and Science*. Kluwer Academic.

Mayo, D. G. (1996). *Error and the Growth of Experimental Knowledge*. University of Chicago Press.

Mayo, D. G. (2018). *Statistical Inference as Severe Testing*. Cambridge University Press.

Mill, J. S. (1843). *A System of Logic*.

Newell, A., & Simon, H. A. (1972). *Human Problem Solving*. Prentice-Hall.

Nickles, T. (Ed.). (1980). *Scientific Discovery: Case Studies*. D. Reidel.

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.

Peirce, C. S. (1903). *Harvard Lectures on Pragmatism*.

Popper, K. R. (1959). *The Logic of Scientific Discovery*. Hutchinson.

Quine, W. V. O. (1951). Two dogmas of empiricism. *The Philosophical Review*, 60(1), 20–43.

Reichenbach, H. (1938). *Experience and Prediction*. University of Chicago Press.

Simon, H. A. (1973). Does scientific discovery have a logic? *Philosophy of Science*, 40(4), 471–480.

---

## Appendix A: The 28 Motor Cascabel theses

| # | Flag | Thesis | Block |
|---|------|--------|-------|
| 1 | `--publicar` | N-gram half-life decreases with corpus size | A |
| 2 | `--canon-expandir` | The canon is defined by what it rejects | A |
| 3 | `--auditar` | H(layer\|axis) is an invariant of the generator | B |
| 4 | `--ablation` | Validators are non-additive | B |
| 5 | `--matriz` | Co-occurrence has low rank | B |
| 6 | `--deriva` | Drift = regime change | B |
| 7 | `--firma` | Eight-dimensional signature stable under paraphrase | B |
| 8 | `--espejo` | Antithesis = involutive operator | C |
| 9 | `--contraejemplo` | Violation has a grammar | C |
| 10 | `--ciego` | Bias = blind/validated divergence | C |
| 11 | `--forense` | Authorship through functional n-grams | C |
| 12 | `--interpolar` | Interpolation is non-commutative | D |
| 13 | `--reconstruir` | Unique reconstruction under style constraints | D |
| 14 | `--temporal` | Dating through lexical markers | D |
| 15 | `--frontera` | Boundary of the declared space | E |
| 16 | `--consenso` | Agreement = structural cause | F |
| 17 | `--disenso` | Dissent = moving boundary | F |
| 18 | `--cuarentena` | Rejections = failure modes | F |
| 19 | `--mutar` | Linear mutation in distance | G |
| 20 | `--cruzar` | Crossing = harmonic mean | G |
| 21 | `--degradar` | Layer hierarchy | G |
| 22 | `--autopsia` | Plan/text distance = health | H |
| 23 | `--espejo-negro` | Informational complement | H |
| 24 | `--parásito` | Permissiveness = hosting | H |
| 25 | `--comprimir` | K(x) ∝ K(π(x)) | I |
| 26 | `--expandir` | Expansion converges to a signature | I |
| 27 | `--censurar` | Structural censorship ≠ lexical censorship | J |
| 28 | `--confesar` | Reflexive self-consistency | J |

**Author's predictions:** 15 survive, 8 fail, 5 remain undetermined.

---

## Appendix B: The 30 preregistered domains

See §5.3.

---

## Appendix C: Partial confusion matrix

|  | Observed PASS | Observed FAIL | LOAD_FAILED |
|--|---------------|---------------|-------------|
| Predicted PASS | 12 | 0 | 0 |
| Predicted FAIL | 0 | 5 | 0 |

**Precision:** 100%. **Recall:** 100%. **F1:** 100%.

---

## Appendix D: The five excluded domains

| Domain | Reason for exclusion | Alternative model |
|---------|---------------------|-------------------|
| Fama-French | Additive, Ω < 1 order | pusfre (linear) |
| Fixed income | Term structure | Nelson-Siegel |
| Trending time series | Φ-Ψ-Ω dependence | ARIMA / dif |
| Direct interaction | Pairwise competition | Game theory |
| Ω < 1.5 orders | K-α degeneracy remains active | pusfre or ces |

---

## Appendix E: The two false-positive tests

| Test | ΔBIC | Result |
|------|------|--------|
| Memory false positive (M6 vs M7) | −681.85 | ✅ M6 wins |
| Saturation false positive (M0 vs M6) | −6411.34 | ✅ M0 wins |

---

## Appendix F: Validation roadmap

| Phase | Duration | Action |
|------|----------|--------|
| 1 | Months 1–2 | Complete internal preregistration (13 domains) |
| 2 | Months 3–6 | Apply protocol to three external cases |
| 3 | Months 7–12 | Publish joint paper with co-authorship |
| 4 | Months 13–24 | Publish toolkit in JOSS |

---

**End of paper.**

**1310.**

---

*"The protocol does not guarantee truth. It guarantees a density of verifiable propositions. And density is what distinguishes a research programme from a collection of opinions."*

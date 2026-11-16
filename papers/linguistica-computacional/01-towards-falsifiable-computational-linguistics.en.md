# TOWARDS A FALSIFIABLE COMPUTATIONAL LINGUISTICS: TWENTY-EIGHT OPERABLE THESES IN A SPANISH TEXT GENERATOR

**Author:** David Ferrández Canalis¹  
¹ Independent researcher. Contact: correspondence through the project repository.

**Date:** September 2026  
**Classification:** JEL Z13, C88, C63 · ACM I.2.7, J.5 · MSC 68T50, 62P99  
**Keywords:** computational stylometry, text generation, falsifiability, negative corpus, authorship, compression, conditional entropy

---

## Abstract

We present **MOTOR CASCABEL v0.1.0**, a Spanish text-generation system built around **twenty-eight falsifiable theses** about language, each implemented as a computable operation. Unlike conventional generators, which are evaluated by the quality of their output, this system is evaluated by the **refutability of its internal claims**. Each instrument returns a measurement together with an explicit prediction about its behaviour under perturbation; its scientific value lies in being capable of contradiction. The preprint formalizes the twenty-eight theses across four layers (formal, operational, predictive, and refutational), groups them into ten thematic blocks, and proposes a reproducible empirical-validation protocol. Implications for computational stylometry, authorship theory, and the epistemology of generative systems are discussed.

---

## 1. Introduction

Computational linguistics has historically privileged the **predictive capacity** of its models — which word comes next, which label applies, which translation is most likely — over the **falsifiability of their assumptions**. A language model can set benchmark records without any of its internal hypotheses being refutable in the Popperian sense.

This preprint describes a system that reverses that hierarchy. MOTOR CASCABEL v0.1.0 does not aim to generate the best possible text. It aims to **generate text that allows its own claims about text to be refuted**. Each of its twenty-eight additions is a thesis with: (1) a natural-language statement; (2) a formal object amenable to computation; (3) an operation that executes it; (4) a falsifiable prediction; and (5) a statement of novelty relative to the state of the art.

The system inherits a stable core from v0.0.2: an embedded corpus of nineteen posts, a bootstrap mechanism over an external corpus of forty-eight chapters, three independent validators (stylometric, anti-repetition, and anti-tic), and a scheduler of combinations without repetition. Version v0.1.0 adds the twenty-eight instruments without modifying that core. The design principle is that **an addition must not alter existing guarantees**; it may only increase the number of refutable claims made by the system.

### 1.1 Motivation

Three observations motivate this work.

**First.** Classical stylometry (Mosteller & Wallace, 1964; Burrows, 2002) has produced robust authorship-attribution techniques, but has rarely formalized **which properties of a text remain invariant under which transformations**. The notion of a “stylometric signature” has been used operationally but not algebraically. Thesis 7 proposes a validity criterion: a signature is valid if stable under paraphrase and unstable under a change of topic.

**Second.** Generative systems are evaluated by their **acceptance space**, not their **rejection space**. Computational linguistics has extensively studied which texts a model produces, but barely studied which texts it **does not** produce and why. Theses 2, 9, 18, and 23 treat the negative corpus — rejected material — as a primary object.

**Third.** The humanities' notion of “style” and computing's notion of “distribution” have not been reconciled. Theses 3, 5, 6, and 12 propose measuring style through thermodynamic-like quantities (conditional entropy, matrix rank, regime change, and mixture non-commutativity) that are **operable without semantic interpretation**.

### 1.2 Contributions

This preprint contributes a formal framework (§2) for expressing linguistic theses as computable operations with falsifiable predictions; twenty-eight theses (§4), grouped into ten blocks; a reproducible empirical-validation protocol (§5) for the public engine; and a limitations discussion (§7) separating what the system measures from what it claims.

### 1.3 Non-contributions

The system **does not learn**. It does not modify its weights through experience and does not improve with use. This is a design decision, not a deficiency. A learning system shifts its own claims without declaring it; a non-learning system can be refuted at every instant.

---

## 2. Formal Framework

### 2.1 Notation

Let G be a text generator. Let L(G) be the set of texts accepted by G. Let f: Text → ℝᵈ be a **signature** assigning each text a vector of d dimensions. Let π ∈ Π be a **composition plan** specifying structural constraints. Let V = {v₁, v₂, v₃} be the validators, with vᵢ: Text → {⊤, ⊥}.

### 2.2 Falsifiable thesis

**Definition 2.1.** A **falsifiable thesis** is a tuple (A, O, P, R), where A is a natural-language statement; O is a computable operation O: G → D, with D a measurable domain; P is a prediction P: O(G) → B, where B is a Boolean or interval; and R is a **refuter**, a transformation R: G → G such that if O(R(G)) violates P, the thesis is considered refuted.

### 2.3 Invariants

A strong claim in v0.1.0 is that **certain generator properties are invariant under corpus transformations**.

**Definition 2.2.** Let T be a transformation over corpora. A property φ is T-invariant if φ(G(C)) = φ(G(T(C))) for every corpus C.

Theses 3, 6, and 7 make invariance claims under specific transformations: topic change, paraphrase, and corpus-size change.

### 2.4 Falsifiability and normal science

The system distinguishes three regimes: **validated** (all three validators accept the text), **blind** (validators are disabled), and **negative** (validators reject the text). Their coexistence allows theses 4, 10, 16, 17, and 18 to measure **the contribution of each validator separately**.

---

## 3. Brief State of the Art

### 3.1 Stylometry

The tradition initiated by Mosteller & Wallace (1964) and continued by Burrows (2002) established **Burrows's Delta** and its variants as a de facto standard for authorship attribution. These methods work, but rarely formulate refutable predictions about their own behaviour under transformation. Thesis 7 proposes a signature-validity criterion that does.

### 3.2 Distributional semantics

The distributional hypothesis (Harris, 1954) and its computational implementations (Deerwester et al., 1990; Landauer & Dumais, 1997) show that co-occurrence captures semantic structure. Thesis 5 differs by applying it **to style**, not content.

### 3.3 Information theory

The connection between style and compression has received little attention. Thesis 25 proposes that the minimum description length of a text is proportional to the complexity of its plan, not to its length.

### 3.4 Generative systems

Neural language models (Brown et al., 2020, and successors) have dominated text generation. The difference here is not architectural but **epistemic**: neural models do not declare their theses; this system declares twenty-eight and offers a protocol to refute them.

---

## 4. The Twenty-Eight Theses

Each thesis is presented through a statement, formal object, operation, signature, and falsifiable prediction. Its thematic block and CLI flag are indicated.

### Block A — Persistence and Memory

**Thesis 1 — Accretion and half-life (—publicar).** A generator's corpus grows by accretion, while the half-life of an n-gram decreases as corpus size increases. For corpus Cₜ, the half-life τ(g) of n-gram g is the difference between its last and first cycle of appearance. The hypothesis is τ(g) ∝ |Cₜ|⁻ᵅ, α > 0. The engine serializes accepted posts with signature, plan, and date, then recalculates the n-gram index. The signature is the log–log curve of τ against corpus size, with slope −α. **Refuter:** α ≤ 0.

**Thesis 2 — Negative canon (—canon-expandir).** A voice's canon is defined by what it has rejected, not what it has accepted. Let R be rejected texts with reason m(r) among stylometric, repetition, and tic failures; the negative canon K⁻ stores each reason with f(r). Rejections are stored and become negative constraints when the canon expands. The signature is a histogram of rejection reasons by stylometric signature. **Refuter:** two different generators produce the same K⁻.

### Block B — Measurement

**Thesis 3 — Invariant conditional entropy (—auditar).** Stylistic self-consistency is measured as H(layer | axis), which is claimed to be a generator invariant rather than a corpus invariant. The engine generates n texts with a fixed seed, estimates H(C|E), and compares it with the corpus value. Signature: ΔH = H_gen − H_corpus, expected |ΔH| < ε. **Refuter:** ΔH varies with topic.

**Thesis 4 — Validator non-additivity (—ablation).** The sum of validators' marginal contributions differs from their joint contribution. Acceptance A(S) for validator subset S is measured across all 2³ = 8 subsets. Signature: the full ablation table and second-/third-order interactions. **Refuter:** interaction is zero and validators behave independently.

**Thesis 5 — Low discourse-matrix rank (—matriz).** The term co-occurrence matrix of a stylistic corpus has low rank, and that rank is the discourse's effective dimension. Mᵢⱼ = PMI(tᵢ,tⱼ); the engine builds the matrix and applies truncated SVD. Signature: singular-value spectrum and elbow k*. **Refuter:** power-law decay without an elbow.

**Thesis 6 — Drift as regime change (—deriva).** Stylistic drift is a regime change detectable by CUSUM over mean sentence length. Sₜ = max(0, Sₜ₋₁ + (ℓₜ − ℓ̄)); a change point occurs when Sₜ exceeds h. The engine orders texts by cycle and detects change points. Signature: change-point list, expected to align with axis changes. **Refuter:** no correlation between change points and the plan.

**Thesis 7 — Signature stable under paraphrase (—firma).** Every text has an eight-dimensional signature, stable under paraphrase and unstable under an axis change. The signature comprises mean and standard deviation of sentence length, type-token ratio, punctuation and lexical measures, paragraph length, and paragraph count. The engine compares within-axis and between-axis distances. Signature: within/between ratio. **Refuter:** ratio approximately 1.

### Block C — Inversion and Falsification

**Thesis 8 — Antithesis as an involution (—espejo).** There exists an operator E such that E² = id, f(E(x)) ≈ f(x), and polarity reverses. The operation structurally negates assertions while preserving length and rhythm. Signature: polarity measured through negation and antonyms. **Refuter:** signature is not preserved.

**Thesis 9 — Grammar of violation (—contraejemplo).** Texts violating a validator form a structured corpus, not noise. Nᵥ = {x : V(x) = ⊥}; the engine forces a validator violation, generates n examples, and analyses their mean signature. **Refuter:** the negative-corpus signature is indistinguishable from randomness.

**Thesis 10 — Bias as divergence (—ciego).** A generator's intrinsic bias is the difference between blind and validated distributions: bias(G) = D_KL(p_blind || p_validated). The engine generates n texts with and without validators and compares signatures. **Refuter:** divergence does not change when the axis changes.

**Thesis 11 — Authorship through functional n-grams (—forense).** Authorship is attributed through functional n-grams (articles, prepositions, auxiliaries), with accuracy independent of topic. Compare classification using functional n-grams F(x) against content n-grams C(x). **Refuter:** F does not outperform C.

### Block D — Interpolation and Reconstruction

**Thesis 12 — Non-commutativity of mixing (—interpolar).** Voice interpolation is neither commutative nor associative. In general I(A,B,α) ≠ I(B,A,α). The engine generates against target signature αf(A)+(1−α)f(B). Signature: difference between AB and BA fit errors. **Refuter:** difference is zero.

**Thesis 13 — Uniqueness under style constraints (—reconstruir).** A text with gaps has a unique valid reconstruction under stylistic constraints. R(x) is the set of reconstructions passing all three validators; the claim is |R(x)| = 1 for small k. The engine enumerates and filters completions. **Refuter:** |R(x)| grows linearly with k.

**Thesis 14 — Implicit dating (—temporal).** A corpus has an implicit timeline detectable through lexical markers. T(x) is the inferred date, with |T(x)−T_real(x)| < δ claimed. A naive classifier estimates dates. **Refuter:** MAE exceeds δ_max.

### Block E — Boundary

**Thesis 15 — Measurable boundary of the declared space (—frontera).** A generator's declared space has a classifiable boundary. Generate n texts inside and n outside the declared space, then train a binary classifier. Signature: AUC. **Refuter:** AUC ≈ 0.5.

### Block F — Cross-Validation

**Thesis 16 — Consensus as a structural signal (—consenso).** Agreement between two validators in rejecting a text indicates a structural rather than superficial cause. Compare structural-violation rates in intersections of rejection sets against their symmetric differences. **Refuter:** rates are equal.

**Thesis 17 — Dissent as a moving boundary (—disenso).** Validator disagreement defines a moving epistemic boundary as a function of layer temperature. D = Rᵢ △ Rⱼ; measure |D| by layer, axis, and temperature. **Refuter:** |D| is constant.

**Thesis 18 — Quarantine as laboratory (—cuarentena).** Rejected texts form a negative corpus with stable failure modes. Accumulate rejections, cluster by signature, and assess centroids, cluster sizes, and resampling stability. **Refuter:** clusters do not stabilize.

### Block G — Metamorphosis

**Thesis 19 — Linearity of mutation (—mutar).** Mutating one plan variable produces stylometric distance linear in that variable: ||f(xπ)−f(xπ′)|| = a|Δvar|+b. Sweep variables and measure distances; signature is linear-fit R². **Refuter:** R² < 0.5.

**Thesis 20 — Crossover as harmonic mean (—cruzar).** Crossing two plans produces a signature closer to the harmonic than arithmetic mean: f(crossover(A,B)) ≈ 2/(1/f(A)+1/f(B)). Cross plans and compare fit errors. **Refuter:** arithmetic mean fits better.

**Thesis 21 — Layer hierarchy (—degradar).** Progressive degradation reveals a hierarchy between structural and decorative layers. Apply successive degradations Dₖ(x) and measure signature distance. **Refuter:** collapse point k* does not depend on layer.

### Block H — Self-Reference

**Thesis 22 — Autopsy as fidelity (—autopsia).** Distance between expected plan signature and generated-text signature indicates generator health: Δ(π,x)=||f_expected(π)−f(x)||. Measure its distribution. **Refuter:** Δ is constant.

**Thesis 23 — Informative complement (—espejo-negro).** The closest text in signature that the generator rejects is informative about the generator. Search rejected texts for N(x)=argmin d(f(y),f(x)), subject to y∉L(G). **Refuter:** no such N(x) exists.

**Thesis 24 — Permissiveness as hosting (—parasito).** A text's ability to host another without violating constraints measures stylistic permissiveness. Valid insertion is tested for |y|/|x| < ρ, with ρ expected to depend on layer. **Refuter:** ρ is constant.

### Block I — Compression

**Thesis 25 — Plan complexity (—comprimir).** Minimum description length of a text is proportional to plan complexity: K(x) ≈ K(π(x))+c. Compare zlib(text) with zlib(plan). **Refuter:** ratio depends on text length.

**Thesis 26 — Convergence of expansion (—expandir).** Expansion of a compressed text converges to the original signature in k* steps: ||f(Eₖ(x))−f(x)||→0. Expand paragraph by paragraph and measure the convergence curve. **Refuter:** no elbow appears.

### Block J — Operational Ethics

**Thesis 27 — Differentiable censorship (—censurar).** Structural censorship is distinguishable from lexical censorship through stylometric signature: f(C_lex(x)) ≠ f(C_struct(x)). Apply both and compare. **Refuter:** signatures are indistinguishable.

**Thesis 28 — Reflexive self-consistency (—confesar).** A generator can produce a text declaring its own constraints without violating them. The generated confession must belong to L(G) and mention its plan; all three validators check it. **Refuter:** success rate is zero.

---

## 5. Empirical-Validation Protocol

### 5.1 Reproducibility

The engine is a single Python file with no external dependencies. Each thesis can be run from the command line. The seed is explicit and outputs are JSON.

### 5.2 Standard test suite

The canonical CLI battery invokes all thesis flags by block: publication and negative-canon expansion (A); audit, ablation, matrix, drift, and signature (B); mirror, counterexample, blind, and forensic modes (C); interpolation, reconstruction, and temporal analysis (D); boundary (E); consensus, dissent, and quarantine (F); mutation, crossover, and degradation (G); autopsy, black mirror, and parasite (H); compression and expansion (I); and lexical/structural censorship and confession (J). Exact commands are retained in the source manuscript.

### 5.3 Acceptance criteria

| Block | Criterion |
|---|---|
| A | α > 0.1 with p < 0.05 |
| B | |ΔH| < 0.1; non-zero interaction; visible elbow; t* correlated |
| C | E² = id and ||f(E(x))−f(x)|| < 0.05; AUC > 0.7 |
| D | commutative difference > 0.01; |R(x)| = 1 in 90% |
| E | AUC > 0.85 |
| F | significant interaction; correlation > 0.4 |
| G | R² > 0.5; harmonic mean wins in > 60% |
| H | bimodal Δ distribution |
| I | stable ratio; visible elbow |
| J | distance above threshold; success rate > 0.8 |

### 5.4 Publication of refutations

The project commits to publishing any refutation of any of the twenty-eight theses. A refuted thesis is not deleted: it is marked refuted with its date and the experiment is documented.

---

## 6. Consolidated Predictions

| # | Prediction | Expected magnitude | Refuter |
|---|---|---|---|
| 1 | α > 0 | 0.1–0.5 | Corpus does not erode |
| 2 | K⁻ distinguishable | AUC > 0.7 | Negative canon indistinguishable |
| 3 | Bounded ΔH | < 0.1 | Topic-dependent drift |
| 4 | Non-zero interaction | |I| > 0.05 | Additive validators |
| 5 | Low rank | Elbow < 20 | Flat spectrum |
| 6 | Change points | Correlation > 0.4 | Noise |
| 7 | Discriminative signature | Within/between < 0.5 | Indistinguishability |
| 8 | Involution | E² = id | Not involutive |
| 9 | Structured violation | Non-random signature | Noise |
| 10 | Measurable bias | D_KL > 0.1 | No bias |
| 11 | Functional > content | Δ > 0.05 | Content performs better |
| 12 | Non-commutativity | Δ > 0.01 | Commutative result |
| 13 | Uniqueness | |R| = 1 in 90% | Multiple reconstructions |
| 14 | Dating | MAE < 2 years | Random performance |
| 15 | Boundary | AUC > 0.85 | No boundary |
| 16 | Structural consensus | Rate > 0.7 | Superficial agreement |
| 17 | Moving dissent | corr > 0.4 | Rigid disagreement |
| 18 | Stable modes | Stable k | Unstable clusters |
| 19 | Linearity | R² > 0.5 | Non-linearity |
| 20 | Harmonic mean wins | > 60% | Arithmetic mean wins |
| 21 | Hierarchy | Layer-dependent k* | Uniform collapse |
| 22 | Bimodality | Two modes | Unimodal distribution |
| 23 | Complement | Small distance | Distant rejected text |
| 24 | Permissiveness | Variable ρ | Constant ρ |
| 25 | Stable ratio | Approximately 1 | Variable ratio |
| 26 | Convergence | Clear elbow | No elbow |
| 27 | Differentiable censorship | Distance > 0.1 | Indistinguishable |
| 28 | Self-consistency | Rate > 0.8 | Failure |

---

## 7. Limitations

### 7.1 System limitations

The assembler produces texts shorter than the corpus. The stylometric validator is statistical and does not understand meaning. The tic validator is syntactic and does not understand synonymy. The forensic mode uses heuristics, not trained models. The archaeological mode fills gaps syntactically, not semantically. The system **does not learn**; this is a design decision.

### 7.2 Thesis limitations

The twenty-eight theses are **falsifiable**, not proven. Compression uses zlib, an **upper bound** on K(x). The plan space is discrete. The embedded corpus is finite (19 texts). Predictions are calibrated on a single language and register.

### 7.3 Epistemic stance

The system does not claim to be neutral. It does not claim to be complete.

---

## 8. Future Work

Immediate extensions include inter-annotator validation, multilingual extension, and a parallel corpus with explicit plans. Broader extensions include formalization of the negative corpus, connection to algorithmic information theory, longitudinal study, and systematic refutation. The project proposes a **Popperian agenda** for computational linguistics.

---

## 9. Conclusion

We have presented a generative system built around twenty-eight falsifiable theses about language, each implemented as a computable operation. The system does not aspire to generate the best text. It aspires to **be refuted precisely**.

The twenty-eight theses are not twenty-eight truths. They are twenty-eight **bets**.

---

## Acknowledgements

To whoever reads this and finds an error. To whoever refutes it with data. To whoever ignores it for the right reasons.

---

## References

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., … & Amodei, D. (2020). *Language models are few-shot learners*. Advances in Neural Information Processing Systems, 33, 1877–1901.

Burrows, J. (2002). *'Delta': a measure of stylistic difference and a guide to likely authorship*. Literary and Linguistic Computing, 17(3), 267–287.

Church, K. W., & Hanks, P. (1990). *Word association norms, mutual information, and lexicography*. Computational Linguistics, 16(1), 22–29.

Deerwester, S., Dumais, S. T., Furnas, G. W., Landauer, T. K., & Harshman, R. (1990). *Indexing by latent semantic analysis*. Journal of the American Society for Information Science, 41(6), 391–407.

Harris, Z. S. (1954). *Distributional structure*. Word, 10(2–3), 146–162.

Heaps, H. S. (1978). *Information retrieval: Computational and theoretical aspects*. Academic Press.

Holmes, D. I. (1998). *The evolution of stylometry in humanities scholarship*. Literary and Linguistic Computing, 13(3), 111–117.

Kolmogorov, A. N. (1965). *Three approaches to the quantitative definition of information*. Problems of Information Transmission, 1(1), 1–7.

Landauer, T. K., & Dumais, S. T. (1997). *A solution to Plato's problem: The latent semantic analysis theory of acquisition, induction, and representation of knowledge*. Psychological Review, 104(2), 211–240.

Mosteller, F., & Wallace, D. L. (1964). *Inference and disputed authorship: The Federalist*. Addison-Wesley.

Page, E. S. (1954). *Continuous inspection schemes*. Biometrika, 41(1/2), 100–115.

Popper, K. R. (1959). *The logic of scientific discovery*. Hutchinson.

Shannon, C. E. (1948). *A mathematical theory of communication*. Bell System Technical Journal, 27(3), 379–423.

Zipf, G. K. (1949). *Human behavior and the principle of least effort*. Addison-Wesley.

---

## Appendices and canonical implementation

The source manuscript contains the engine architecture, the full thesis-to-CLI map, formal glossary, complete Python implementation, embedded corpus, all 28 command-line instruments, and supporting code. The executable implementation is preserved verbatim in the Spanish source to avoid changing the Spanish-language corpus, CLI contract, metadata, identifiers, or runtime behaviour.

The English edition translates the complete research narrative, all twenty-eight thesis specifications, empirical protocol, acceptance criteria, consolidated predictions, limitations, future work, and references. The source appendices remain canonical for exact commands and executable code.

[Canonical Spanish manuscript with complete MOTOR CASCABEL v0.1.0 implementation](01-veintiocho-tesis-linguistica-computacional.es.md).

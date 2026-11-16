# Towards a Falsifiable Computational Linguistics: Twenty-Eight Operational Theses in a Spanish Text Generator

**Author:** David Ferrández Canalis¹

¹ Independent researcher. Contact: [correspondence through the project repository]

**Date:** September 2026

**Classification:** JEL Z13, C88, C63 · ACM I.2.7, J.5 · MSC 68T50, 62P99

**Keywords:** computational stylometry, text generation, falsifiability, negative corpus, authorship, compression, conditional entropy

---

## Abstract

We present **MOTOR CASCABEL v0.1.0**, a Spanish-language text-generation system built around **twenty-eight falsifiable theses** about language, each implemented as a computable operation. Unlike conventional generators, which are evaluated by the quality of their output, this system is evaluated by the **refutability of its internal claims**. Each instrument returns a measurement together with an explicit prediction about its behaviour under perturbation; its scientific value lies in being open to contradiction. This preprint formalizes the twenty-eight theses across four layers (formal, operational, predictive, and refutational), groups them into ten thematic blocks, and proposes a reproducible empirical-validation protocol. Implications for computational stylometry, authorship theory, and the epistemology of generative systems are discussed.

---

## 1. Introduction

Computational linguistics has historically prioritized the **predictive capacity** of its models—what word comes next, which label applies, which translation is most likely—over the **falsifiability of their assumptions**. A language model can set benchmark records without any of its internal hypotheses being refutable in the Popperian sense.

This preprint describes a system that reverses that hierarchy. MOTOR CASCABEL v0.1.0 does not aim to generate the best possible text. It aims to **generate text that makes it possible to refute its own claims about text**. Each of its twenty-eight additions is a thesis with:

1. A **natural-language statement**.
2. A **formal object** that can be computed.
3. An **operation** that executes it.
4. A **falsifiable prediction** whose violation would refute it.
5. **Novelty** relative to the state of the art.

The system inherits a stable core from its previous version (`v0.0.2`): an embedded corpus of nineteen posts, a bootstrap mechanism over an external corpus of forty-eight chapters, three independent validators (stylometric, anti-repetition, and anti-tic), and a scheduler of combinations without repetition. Version `v0.1.0` adds the twenty-eight instruments without modifying that core. The design principle is that **an addition must not alter existing guarantees**; it may only increase the number of refutable claims made by the system.

### 1.1 Motivation

Three observations motivate this work.

**First.** Classical stylometry (Mosteller & Wallace, 1964; Burrows, 2002) has produced a robust set of authorship-attribution techniques, but has rarely formalized **which properties of text remain invariant under which transformations**. The notion of a “stylometric signature” has been used operationally but not algebraically. Thesis 7 (the eight-dimensional signature) proposes a validity criterion: a signature is valid if it is stable under paraphrase and unstable under a change of topic.

**Second.** Generative systems are evaluated by their **acceptance space**, not their **rejection space**. Computational linguistics has extensively studied which texts a model produces, but has scarcely studied which texts it **does not** produce and why. Theses 2, 9, 18, and 23 propose treating the negative corpus—the rejected material—as a primary object.

**Third.** The humanities notion of “style” and the computational notion of “distribution” have not been reconciled. Theses 3, 5, 6, and 12 propose measuring style through thermodynamic-like quantities (conditional entropy, matrix rank, regime change, and non-commutativity of mixing) that are **operable without semantic interpretation**.

### 1.2 Contributions

This preprint contributes:

- A **formal framework** (§2) for expressing linguistic theses as computable operations with falsifiable predictions.
- **Twenty-eight theses** (§4), grouped into ten blocks, each with a statement, formal object, operation, signature, and prediction.
- A reproducible **empirical-validation protocol** (§5) for the public engine.
- A **discussion of limitations** (§7) separating what the system measures from what it claims.

### 1.3 Non-contributions

The system does **not** learn. It does not update its weights through experience. It does not improve with use. This is a design decision, not a deficiency. The rationale is that a learning system shifts its own claims without declaring that it has done so; a non-learning system can be refuted at any given moment.

---

## 2. Formal Framework

### 2.1 Notation

Let `G` be a text generator. Let `L(G)` be the set of texts accepted by `G`. Let `f: Text → ℝ^d` be a **signature** assigning a d-dimensional vector to each text. Let `π ∈ Π` be a **composition plan** specifying a text's structural constraints. Let `V = {v_1, v_2, v_3}` be the set of validators, with `v_i: Text → {⊤, ⊥}`.

### 2.2 Falsifiable thesis

**Definition 2.1.** A **falsifiable thesis** is a tuple `(A, O, P, R)`, where:

- `A` is a natural-language statement.
- `O` is a computable operation `O: G → D`, with `D` a measurable domain.
- `P` is a prediction `P: O(G) → B`, where `B` is a Boolean or an interval.
- `R` is a **refuter**: a transformation `R: G → G` such that, if `O(R(G))` violates `P`, the thesis is considered refuted.

### 2.3 Invariants

A strong thesis of `v0.1.0` is that **certain properties of the generator are invariant under corpus transformations**. Formally:

**Definition 2.2.** Let `T` be a transformation over corpora. A property `φ` is **T-invariant** if `φ(G(C)) = φ(G(T(C)))` for every corpus `C`.

Theses 3, 6, and 7 make invariance claims under specific transformations (`T = topic change`, `T = paraphrase`, and `T = corpus-size change`).

### 2.4 Falsifiability and normal science

The system distinguishes three regimes:

- **Validated regime:** all three validators accept the text.
- **Blind regime:** validators are disabled.
- **Negative regime:** validators reject the text.

The coexistence of these three regimes makes it possible for theses 4, 10, 16, 17, and 18 to measure **the contribution of each validator separately**.

---

## 3. Brief State of the Art

### 3.1 Stylometry

The tradition initiated by Mosteller & Wallace (1964) and continued by Burrows (2002) established **Burrows's Delta** and its variants as a de facto standard for authorship attribution. These methods work, but rarely formulate **refutable predictions** about their own behaviour under transformation. Thesis 7 proposes a signature-validity criterion that does.

### 3.2 Distributional semantics

The distributional hypothesis (Harris, 1954) and its computational implementations (Deerwester et al., 1990; Landauer & Dumais, 1997) have shown that co-occurrence captures semantic structure. Thesis 5 differs by applying it to **style**, not content.

### 3.3 Information theory

The connection between style and compression has received little attention. Thesis 25 proposes that the minimum description length of a text is proportional to the complexity of its composition plan, not to its length.

### 3.4 Generative systems

Neural language models (Brown et al., 2020, and successors) have dominated text generation. The difference in this work is not architectural but **epistemic**: neural models do not declare their theses; this system declares twenty-eight and provides a protocol for refuting them.

---

## 4. The Twenty-Eight Theses

Each thesis is presented in five parts: statement, formal object, operation, signature, and falsifiable prediction. Its block (A–J) and invoking CLI flag are indicated.

### Block A — Persistence and Memory

#### Thesis 1 — Accretion and half-life (`--publicar`)

**Statement.** A generator's corpus is an organism that grows by accretion; the half-life of an n-gram decreases as corpus size increases.

**Formal object.** Let `C_t` be the corpus after cycle `t`. The half-life of an n-gram `g` is `τ(g) = sup{ t : g ∈ C_t } − inf{ t : g ∈ C_t }`. The hypothesis is `τ(g) ∝ |C_t|^{−α}`, with `α > 0`.

**Operation.** Each accepted post is serialized to `publicados.json` with its signature, plan, and date. The n-gram index is recalculated and `τ(g)` is recorded for each n-gram.

**Signature.** The `τ` versus `|C|` curve on logarithmic-logarithmic axes. Slope `−α`.

**Falsifiable prediction.** If `α ≤ 0`, the thesis is refuted: the corpus does not erode; it accumulates.

#### Thesis 2 — Negative canon (`--canon-expandir`)

**Statement.** A voice's canon is defined by what it has rejected, not by what it has accepted.

**Formal object.** Let `R = {r_1, …, r_n}` be the set of rejected texts, with rejection reason `m(r) ∈ {est, rep, tic}`. The negative canon is `K⁻ = { (m, f(r)) : r ∈ R }`.

**Operation.** Each rejection is stored with its signature and reason. When the canon is expanded, `K⁻` acts as a negative constraint.

**Signature.** A histogram of rejection reasons by stylometric signature.

**Falsifiable prediction.** If two different generators produce the same `K⁻`, they do not have distinct voices.

### Block B — Measurement

#### Thesis 3 — Invariant conditional entropy (`--auditar`)

**Statement.** The stylometric self-consistency of a corpus is measured as `H(layer | axis)`, and this entropy is an invariant of the generator, not of the corpus.

**Formal object.** `H(C | E) = − Σ_{e,c} p(e,c) log p(c|e)`. The hypothesis is that `H(C|E)` remains constant under corpus variation if the generator is unchanged.

**Operation.** Generate `n` texts with a fixed seed, calculate empirical `H(C|E)`, and compare it with the corpus value.

**Signature.** `ΔH = H_gen − H_corpus`. Expected: `|ΔH| < ε`.

**Falsifiable prediction.** If `ΔH` varies with topic, the invariance claim is refuted.

#### Thesis 4 — Non-additivity of validators (`--ablation`)

**Statement.** The sum of validators' marginal contributions is not equal to their joint contribution.

**Formal object.** Let `A(S)` be the acceptance rate with validator subset `S ⊆ V`. The hypothesis is `A(V) ≠ A(∅) + Σ_i [A(V) − A(V∖{v_i})]`.

**Operation.** Run the generator with all `2³ = 8` validator subsets, generating `n` texts for each.

**Signature.** The 2³ table; second- and third-order interactions.

**Falsifiable prediction.** If the interaction is zero, the validators are independent.

#### Thesis 5 — Low rank of discourse (`--matriz`)

**Statement.** The term co-occurrence matrix in a style corpus has low rank, and that rank is the effective dimensionality of the discourse.

**Formal object.** `M_{ij} = PMI(t_i, t_j)`. The hypothesis is `rank(M) ≪ min(|V|, |V|)`.

**Operation.** Build `M` over the complete corpus and apply truncated SVD.

**Signature.** Singular-value spectrum, with an elbow at `k*`.

**Falsifiable prediction.** If the spectrum decays as a power law without an elbow, the thesis is refuted.

#### Thesis 6 — Drift as a regime change (`--deriva`)

**Statement.** Stylistic drift is a regime change detectable by CUSUM applied to mean sentence length.

**Formal object.** `S_t = max(0, S_{t−1} + (ℓ_t − ℓ̄))`. A change point occurs at `t*` when `S_{t*} > h`.

**Operation.** Order texts by cycle, calculate CUSUM, and detect change points.

**Signature.** The list `{t*}`. Alignment with changes of axis is expected.

**Falsifiable prediction.** If `t*` does not correlate with the plan, the thesis is refuted.

#### Thesis 7 — Signature stability under paraphrase (`--firma`)

**Statement.** Every text has an eight-dimensional signature that is stable under paraphrase and unstable under a change of axis.

**Formal object.** `f(x) = (ℓ̄, σ_ℓ, TTR, δ_p, ρ_c, ρ_l, ℓ̄_p, n_p)`. The hypotheses are `||f(x) − f(Π(x))|| < ε` and `||f(x) − f(x')|| > δ` when `axis(x) ≠ axis(x')`.

**Operation.** Calculate `f` for each text. Compare within-axis and between-axis distances.

**Signature.** The `within/between` ratio.

**Falsifiable prediction.** If the ratio is approximately 1, the thesis is refuted.

### Block C — Inversion and Falsification

#### Thesis 8 — Antithesis as an involution (`--espejo`)

**Statement.** There exists an operator `E` such that `E² = id`, `f(E(x)) ≈ f(x)`, and `polaridad(E(x)) = −polaridad(x)`.

**Formal object.** `E: Text → Text`, involutive, stylometrically neutral, and polarity-reversing.

**Operation.** Invert assertions through structural negation while preserving length and rhythm.

**Signature.** Polarity, measured through negation and antonym analysis.

**Falsifiable prediction.** If `E(x)` does not preserve the signature, the thesis is refuted.

#### Thesis 9 — Grammar of violation (`--contraejemplo`)

**Statement.** The set of texts that violate a validator is a structured corpus, not noise.

**Formal object.** `N_V = { x : V(x) = ⊥ }`. The hypothesis is that `N_V` admits a generative model with its own signature.

**Operation.** Force a validator violation, generate `n` violators, and analyse them.

**Signature.** Mean signature of `N_V`.

**Falsifiable prediction.** If the signature of `N_V` is indistinguishable from chance, the thesis is refuted.

#### Thesis 10 — Bias as divergence (`--ciego`)

**Statement.** A generator's intrinsic bias is the difference between its blind and validated distributions.

**Formal object.** `bias(G) = D_KL(p_ciego || p_validado)`.

**Operation.** Generate `n` texts with validators and `n` without them. Compare signatures.

**Signature.** Empirical `D_KL`.

**Falsifiable prediction.** If `D_KL` does not change when the axis varies, the thesis is refuted.

#### Thesis 11 — Authorship through functional n-grams (`--forense`)

**Statement.** Authorship is attributed through functional n-grams (articles, prepositions, auxiliaries), and the hit rate is independent of topic.

**Formal object.** `F(x)` = functional n-grams; `C(x)` = content n-grams. The hypothesis is `P(author | F(x)) > P(author | C(x))`.

**Operation.** Naive classification using `F` and using `C`; compare the results.

**Signature.** Confusion matrix and comparative accuracy.

**Falsifiable prediction.** If `F` does not outperform `C`, the thesis is refuted.

### Block D — Interpolation and Reconstruction

#### Thesis 12 — Non-commutativity of mixing (`--interpolar`)

**Statement.** Voice interpolation is neither commutative nor associative.

**Formal object.** In general, `I(A, B, α) ≠ I(B, A, α)`.

**Operation.** Generate with target signature `α·f(A) + (1−α)·f(B)`. Compare commutative errors.

**Signature.** Difference `|error(AB) − error(BA)|`.

**Falsifiable prediction.** If the difference is zero, the thesis is refuted.

#### Thesis 13 — Uniqueness under style constraints (`--reconstruir`)

**Statement.** Under stylistic constraints, a text with gaps has a unique valid reconstruction.

**Formal object.** Let `R(x)` be the set of reconstructions that pass all three validators. The hypothesis is `|R(x)| = 1` for small `k`.

**Operation.** Enumerate candidate completions and filter them through the validators.

**Signature.** `|R(x)|` versus `k`.

**Falsifiable prediction.** If `|R(x)|` grows linearly with `k`, the thesis is refuted.

#### Thesis 14 — Implicit dating (`--temporal`)

**Statement.** Every corpus has an implicit timeline detectable through lexical markers.

**Formal object.** Let `T(x)` be the inferred date. The hypothesis is `|T(x) − T_real(x)| < δ` for small `δ`.

**Operation.** A naive classifier uses temporal markers.

**Signature.** Dating MAE.

**Falsifiable prediction.** If `MAE > δ_max`, the thesis is refuted.

### Block E — Boundary

#### Thesis 15 — Measurable boundary of the declared space (`--frontera`)

**Statement.** A generator's declared space has a classifiable boundary.

**Formal object.** `S` is the declared space. `F` is the set of texts generated with plans outside `S`. The hypothesis is `AUC > 0.9` for a binary inside/outside classifier.

**Operation.** Generate `n` in-space and `n` out-of-space texts. Train a classifier.

**Signature.** `AUC`.

**Falsifiable prediction.** If `AUC ≈ 0.5`, the thesis is refuted.

### Block F — Cross-Validation

#### Thesis 16 — Consensus as a structural signal (`--consenso`)

**Statement.** Agreement between two validators in rejecting a text indicates a structural, not superficial, cause.

**Formal object.** `R_i` is the set rejected by `v_i`. The hypothesis is `x ∈ R_i ∩ R_j` implies a structural violation of the plan.

**Operation.** Record rejections by validator and analyse intersections.

**Signature.** Structural-violation rate in intersections versus the symmetric difference.

**Falsifiable prediction.** If the rates are equal, the thesis is refuted.

#### Thesis 17 — Dissent as a moving boundary (`--disenso`)

**Statement.** Dissent between validators defines a moving epistemic boundary, as a function of layer temperature.

**Formal object.** `D = R_i △ R_j`. The hypothesis is that `|D|` grows with `temperature(layer)`.

**Operation.** Measure `|D|` by layer, axis, and temperature.

**Signature.** Correlation between `|D|` and temperature.

**Falsifiable prediction.** If `|D|` is constant, the thesis is refuted.

#### Thesis 18 — Quarantine as a laboratory (`--cuarentena`)

**Statement.** Rejected texts form a negative corpus with stable failure modes.

**Formal object.** `Q = { (x, reason) : x rejected }`. The hypothesis is that `Q` admits clustering into `k` modes.

**Operation.** Accumulate rejections and cluster them by signature.

**Signature.** Centroids and cluster sizes; stability under resampling.

**Falsifiable prediction.** If the clusters do not stabilize, the thesis is refuted.

### Block G — Metamorphosis

#### Thesis 19 — Linearity of mutation (`--mutar`)

**Statement.** Mutating one plan variable produces a stylometric distance that is linear in that variable.

**Formal object.** `||f(x_π) − f(x_π')|| = a·|Δvar| + b`.

**Operation.** Sweep one variable at a time and measure distances.

**Signature.** `R²` of the linear fit.

**Falsifiable prediction.** If `R² < 0.5`, the thesis is refuted.

#### Thesis 20 — Crossing as a harmonic mean (`--cruzar`)

**Statement.** Crossing two plans produces a signature equal to the harmonic mean, not the arithmetic mean.

**Formal object.** `f(cross(A,B)) ≈ 2 / (1/f(A) + 1/f(B))`.

**Operation.** Cross plans and compare the fits.

**Signature.** Fit error for each mean.

**Falsifiable prediction.** If the arithmetic mean fits better, the thesis is refuted.

#### Thesis 21 — Layer hierarchy (`--degradar`)

**Statement.** Progressive degradation reveals a hierarchy between structural and decorative layers.

**Formal object.** `D_k(x)` with `k` degradations. The signature collapses at `k*`, which depends on the layer.

**Operation.** Apply successive degradations and measure the signature.

**Signature.** Curve `||f(D_k(x)) − f(x)||` versus `k`.

**Falsifiable prediction.** If `k*` does not depend on the layer, the thesis is refuted.

### Block H — Self-Reference

#### Thesis 22 — Autopsy as fidelity (`--autopsia`)

**Statement.** The distance between the plan's expected signature and the text's signature is an indicator of generator health.

**Formal object.** `Δ(π, x) = ||f_expected(π) − f(x)||`.

**Operation.** Measure `Δ` for every generated text.

**Signature.** Distribution of `Δ`.

**Falsifiable prediction.** If `Δ` is constant, the thesis is refuted.

#### Thesis 23 — Informational complement (`--espejo-negro`)

**Statement.** The closest text in signature space that the generator rejects is informative about the generator.

**Formal object.** `N(x) = argmin_y d(f(y), f(x))`, subject to `y ∉ L(G)`.

**Operation.** Search among rejected texts.

**Signature.** `d(f(x), f(N(x)))`.

**Falsifiable prediction.** If `N(x)` does not exist, the thesis is refuted.

#### Thesis 24 — Permissiveness as hosting capacity (`--parásito`)

**Statement.** A text's ability to host another text without violating constraints measures the permissiveness of its style.

**Formal object.** `H(x, y)` is valid for `|y|/|x| < ρ`. `ρ` depends on the layer.

**Operation.** Insert text and validate the result.

**Signature.** `ρ` by layer.

**Falsifiable prediction.** If `ρ` is constant, the thesis is refuted.

### Block I — Compression

#### Thesis 25 — Plan complexity (`--comprimir`)

**Statement.** The minimum description length of a text is proportional to the complexity of its plan.

**Formal object.** `K(x) ≈ K(π(x)) + c`. The hypothesis is `K(x) / K(π(x)) ≈ 1`.

**Operation.** Compare `zlib(text)` with `zlib(plan)`.

**Signature.** The ratio.

**Falsifiable prediction.** If the ratio depends on `|x|`, the thesis is refuted.

#### Thesis 26 — Convergence of expansion (`--expandir`)

**Statement.** Expanding a compressed text converges to the original signature after `k*` steps.

**Formal object.** `||f(E_k(x)) − f(x)|| → 0` as `k` increases.

**Operation.** Expand paragraph by paragraph and measure the signature.

**Signature.** Convergence curve.

**Falsifiable prediction.** If there is no elbow, the thesis is refuted.

### Block J — Operational Ethics

#### Thesis 27 — Differentiable censorship (`--censurar`)

**Statement.** Structural censorship can be distinguished from lexical censorship through its stylometric signature.

**Formal object.** `f(C_lex(x)) ≠ f(C_est(x))`.

**Operation.** Apply both types of censorship and compare signatures.

**Signature.** Signature distance.

**Falsifiable prediction.** If the signatures are indistinguishable, the thesis is refuted.

#### Thesis 28 — Reflexive self-consistency (`--confesar`)

**Statement.** A generator can produce a text that declares its own constraints without violating them.

**Formal object.** `CF(π) ∈ L(G)` and `CF(π)` mentions `π`.

**Operation.** Generate a text that states its plan and verify it with all three validators.

**Signature.** Success rate.

**Falsifiable prediction.** If the success rate is zero, the thesis is refuted.

---

## 5. Empirical Validation Protocol

### 5.1 Reproducibility

The engine is a single Python file with no external dependencies. Any researcher can run each thesis with a single command-line invocation. The seed is explicit and outputs are JSON.

### 5.2 Standard battery

```bash
# Block A
python cascabel.py --publicar --canon ./publicados.json --n 1000
python cascabel.py --canon-expandir --canon ./publicados.json

# Block B
python cascabel.py --auditar --n 1000 --semilla 42
python cascabel.py --ablation --n 500
python cascabel.py --matriz
python cascabel.py --deriva --n 500
python cascabel.py --firma --texto "..."

# Block C
python cascabel.py --espejo --texto "..."
python cascabel.py --contraejemplo --tic no_es_es --n 500
python cascabel.py --ciego --n 500
python cascabel.py --forense

# Block D
python cascabel.py --interpolar --peso 0.5
python cascabel.py --reconstruir "El ____ no es ____. Es ____."
python cascabel.py --temporal

# Block E
python cascabel.py --frontera --n 500

# Block F
python cascabel.py --consenso --n 1000
python cascabel.py --disenso --n 1000
python cascabel.py --cuarentena --n 1000

# Block G
python cascabel.py --mutar --variable capa
python cascabel.py --cruzar --plano-a ia|cto|tecnico --plano-b poder|inversor|juridico
python cascabel.py --degradar

# Block H
python cascabel.py --autopsia --n 200
python cascabel.py --espejo-negro
python cascabel.py --parasito

# Block I
python cascabel.py --comprimir
python cascabel.py --expandir

# Block J
python cascabel.py --censurar --tipo lexica
python cascabel.py --censurar --tipo estructural
python cascabel.py --confesar --combinacion ia|cto|tecnico
```

### 5.3 Acceptance criteria

| Block | Criterion |
|---|---|
| A | `α > 0.1` with `p < 0.05` |
| B | `|ΔH| < 0.1`; interaction ≠ 0; visible elbow; `t*` correlates |
| C | `E² = id` and `||f(E(x)) − f(x)|| < 0.05`; `AUC > 0.7` |
| D | commutative difference > 0.01; `|R(x)| = 1` in 90% |
| E | `AUC > 0.85` |
| F | significant interaction; correlation > 0.4 |
| G | `R² > 0.5`; harmonic mean wins in > 60% |
| H | bimodal distribution of `Δ` |
| I | stable ratio; visible elbow |
| J | distance > threshold; rate > 0.8 |

### 5.4 Publication of refutations

The project commits to publishing any refutation of any of the twenty-eight theses. A refuted thesis is not deleted: it is marked as `refuted:<date>` and the experiment is documented.

---

## 6. Consolidated Predictions

| # | Prediction | Expected magnitude | Refuter |
|---|---|---|---|
| 1 | `α > 0` | 0.1–0.5 | corpus without erosion |
| 2 | distinguishable `K⁻` | AUC > 0.7 | indistinct negative canon |
| 3 | bounded `ΔH` | < 0.1 | topic-driven drift |
| 4 | interaction ≠ 0 | |I| > 0.05 | additive validators |
| 5 | low rank | elbow < 20 | flat spectrum |
| 6 | change points | correlation > 0.4 | noise |
| 7 | discriminative signature | within/between < 0.5 | indistinguishability |
| 8 | involution | `E² = id` | not involutive |
| 9 | structured violation | non-random signature | noise |
| 10 | measurable bias | `D_KL > 0.1` | no bias |
| 11 | functional > content | Δ > 0.05 | content performs better |
| 12 | non-commutative | Δ > 0.01 | commutative |
| 13 | uniqueness | |R| = 1 in 90% | multiple solutions |
| 14 | dating | MAE < 2 years | chance |
| 15 | boundary | AUC > 0.85 | no boundary |
| 16 | structural consensus | rate > 0.7 | superficial cause |
| 17 | moving dissent | corr > 0.4 | rigid |
| 18 | stable modes | stable k | unstable |
| 19 | linearity | R² > 0.5 | non-linear |
| 20 | harmonic wins | > 60% | arithmetic |
| 21 | hierarchy | layer-specific k* | uniform |
| 22 | bimodality | two modes | unimodal |
| 23 | complement | small distance | distant |
| 24 | permissiveness | variable ρ | constant |
| 25 | stable ratio | ≈ 1 | variable |
| 26 | convergence | clear elbow | no elbow |
| 27 | distinguishable censorship | distance > 0.1 | indistinguishable |
| 28 | self-consistency | rate > 0.8 | failure |

---

## 7. Limitations

### 7.1 System limitations

- The assembler produces texts shorter than the corpus.
- The stylometric validator is statistical: it does not understand meaning.
- The tic validator is syntactic: it does not understand synonymy.
- The forensic mode uses heuristics, not trained models.
- The archaeological mode fills gaps syntactically, not semantically.
- The system **does not learn**. This is a design decision.

### 7.2 Limitations of the theses

- The twenty-eight theses are **falsifiable**, not demonstrated.
- Compression uses `zlib`, which is an **upper bound** on `K(x)`.
- The plan space is discrete.
- The embedded corpus is finite (19 texts).
- Predictions are calibrated on a single language and register.

### 7.3 Epistemic stance

- The system does not claim to be neutral.
- The system does not claim to be complete.

---

## 8. Future Work

### 8.1 Immediate extensions

- **Inter-annotator validation.**
- **Multilingual extension.**
- A **parallel corpus** with explicit plans.

### 8.2 Longer-term extensions

- **Formalization of the negative corpus.**
- **Connection to algorithmic information theory.**
- **Longitudinal study.**
- **Systematic refutation.**

### 8.3 Agenda

The project proposes a **Popperian agenda** for computational linguistics.

---

## 9. Conclusion

We have presented a generative system articulating twenty-eight falsifiable theses about language, each implemented as a computable operation. The system does not aspire to generate the best text. It aspires to **be refuted precisely**.

The twenty-eight theses are not twenty-eight truths. They are twenty-eight **wagers**.

---

## Acknowledgements

To whoever reads this and finds an error.  
To whoever refutes it with data.  
To whoever ignores it for the right reasons.

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

## Appendices

The Spanish source continues with Appendix A (engine architecture), Appendix B (thesis/flag map), Appendix C (formal glossary), Appendix D (complete engine code), and Appendix E (the empirical refutation protocol for all 28 theses, including its proposed runner). These materials are not reproduced in this main-text edition because the code and experiment definitions must remain synchronized with the source. Their translation and parity audit remain outstanding.

**Translation status:** Complete English translation of the main text (Abstract through References). Appendices A–E remain in the Spanish source and are not represented as translated.
# TESTING PROTOCOL 1310 — EXTENDED VERSION 1.0

**Operational manual for a typed, falsifiable, integrity-preserving, auditable testing system, with an extension for AI-assisted QA.**

**Pydantic v2 + mathematics + cybersecurity + 2025–2026 state of the art + multi-agent systems + semantic validation.**

---

## PART 0 — PRINCIPLE AND DECISION GUIDE

A test is not an opinion. It is **falsifiable testimony** about software behaviour. Each test becomes a typed object with a mandatory refuter, severity, cybersecurity standard, and 1310 seal. The system's **1310 Auditor** verifies integrity, executes, and reports.

**Without a refuter, there is no test. There is an illusion of coverage.**

**The 1310 seal is not decorative.** It certifies that the test has passed the falsifiability protocol: it has an explicit refuter, a failure condition, a preregistered hash, and an integrity audit. A test without the 1310 seal is a script that runs. A test with the 1310 seal is testimony that can be refuted.

**This protocol is designed so that an LLM can operate it unambiguously.** It is not a protocol for humans who write tests by hand. It is a protocol for humans who write **the contract**, and agents that generate, execute, and validate tests satisfying it.

### Decision tree: which level do I need?

**Question 1: Could failure of your software cause physical, financial, or legal harm?**
- **YES** → Full level. Banking, healthcare, automotive, defence, medical IoT.
- **NO** → Question 2.

**Question 2: Do you have regulatory requirements to audit (PCI DSS, GDPR, DORA, IEC 62304, ISO 26262)?**
- **YES** → Standard or Full, depending on criticality.
- **NO** → Question 3.

**Question 3: Does your team have fewer than 10 people and need to ship every week?**
- **YES** → Lite level.
- **NO** → Standard level.

**Operational rule:** if you are unsure between two levels, start with the lower one. You can always move up.

### Three operating levels

| Level | Audience | Includes | Does NOT include |
|---|---|---|---|
| **Lite** | Startups, teams of 1–10 | pytest plugin; refuter in docstring; automatic hash; generation cost | Roles, SBOM, SLSA, ML, HIL, regulatory audit |
| **Standard** | Mid-sized companies, B2B SaaS, teams of 10–50 | Lite + roles + standards + business report + basic ML + multi-agent support | SLSA 3+, HIL, TLPT, MC/DC |
| **Full** | Banking, healthcare, automotive, defence, regulated environments | Standard + SBOM + SLSA 3+ + MC/DC + HIL + TLPT + auditable segregation + full ML + semantic validation | Nothing; this is the complete protocol |

---

## PART 1 — HOW THE PROTOCOL WORKS

### 1.1 Lifecycle

The protocol has four phases, each with a purpose and an owner.

**Phase 1 — PROPOSED.** The Architect (or the developer, at Lite level) writes the test. They declare what it verifies, how it can be refuted, its severity, and which standard it contributes to.

**Phase 2 — PREREGISTERED.** The system calculates a SHA-256 hash of the test's **immutable identity** (not its state) and stores it. From this point on, the test cannot be modified without the hash no longer matching.

**Phase 3 — RUNNING.** The Executor (or CI/CD) runs the test. The result is recorded as `PASSED`, `FAILED`, `BLOCKED`, or `QUARANTINED`.

**Phase 4 — AUDITED.** The 1310 Auditor verifies that the hash matches, that the result is consistent, and that any failure has a documented root cause.

**Golden rule:** a test that has not passed through all four phases is not a test. It is a script.

### 1.2 The refuter, explained

The refuter is the most important part of the protocol. It answers the question: **what would have to happen for this test to cease to be valid?**

Without a refuter, a test is a tautology. It verifies what it verifies because it verifies it. It contributes no information.

**The problem with AI-generated tests:** empirical studies show that LLMs generate tests that compile and achieve reasonable coverage but **fail to detect bugs**, and frequently exhibit design smells that undermine their effectiveness. Used naively, these assistants tend to generate **tautological tests that restate implementation logic instead of challenging it**.

**Bad example (without a refuter):**
```python
def test_sum():
    assert 2 + 2 == 4
```

**Good example (with a refuter):**
```python
def test_transfer_does_not_allow_negative_balance():
    """
    REFUTER: If transferring €100 from an account with €50 and no active
    overdraft results in a balance >= 0 and the transfer completes.
    FAILURE_CONDITION: final_balance >= 0 and transfer.completed
    """
    account = Account(balance=50, overdraft_active=False)
    result = transfer(account, destination, 100)
    assert result.failed
    assert account.balance == 50
```

### 1.3 The Auditor, explained

The 1310 Auditor is not a judge. It is an **integrity verifier**.

Its functions are:

1. **Verify the hash.** Compare the current test hash with the preregistered one.
2. **Semantically validate the refuter.** Its mere existence is insufficient; it must genuinely be falsifiable.
3. **Decide whether a failure is significant.** Use execution history.
4. **Report.** Generate JSON containing suite status, business impact, and covered standards.

**The Auditor cannot validate a test that it proposed itself.**

---

## PART 2 — DATA MODEL (PYDANTIC V2)

The source implementation defines the protocol's typed data model in Pydantic v2. The model separates test identity from execution state and includes enumerations for test type, category, state, cybersecurity standard, severity, domain, role, protocol level, and supported LLM families.

### 2.1 Core enumerations

The test types include unit, integration, end-to-end, security, integrity, performance, property-based, contract, mutation, chaos, ML drift, ML fairness, ML explainability, ML robustness, and LLM hallucination, bias, and safety tests.

Test categories are A (critical), B (important), C (edge case), and D (exploratory). States include proposed, preregistered, running, passed, failed, blocked, skipped, quarantined, obsolete, tautological, and invalid-refuter.

The cybersecurity standards represented include NIST SP 800-218 and 800-218A, ISO 27001, OWASP ASVS and Top 10:2025, SLSA, PCI DSS, HIPAA, GDPR, SOC 2, NIST SP 800-53, ISO 26262, IEC 62304, ISO 21434, and DORA.

Roles are proposer, executor, Auditor, chronicler, LLM generator, and semantic validator. Protocol levels are Lite, Standard, and Full.

### 2.2 Test signature

The immutable test signature records line coverage, branch coverage, MC/DC coverage, mutation score, determinism, execution time, external dependencies, isolation, flakiness, and tautological integrity. The ten-dimensional vector is used for quantitative comparisons.

The integrity scale is explicit: 0.0 means tautological; 1.0 means falsifiable.

### 2.3 Immutable, versioned test

A test has an identifier, semantic version, optional parent test, and mandatory version-change rationale when it derives from a parent. It records type, category, domain, protocol level, statement, preconditions, steps, expected result, refuter, failure condition, severity, applicable standards, expected signature, risk references, SHA-256 hash, date, and the literal 1310 seal.

AI-generation metadata includes whether the test was generated by an LLM, the model, prompt version, generation cost, and input/output token counts. The refuter validator rejects generic wording that makes the claim non-falsifiable.

Execution state is stored separately and records the test ID and version, state, timestamp, observed signature, immutable hash, proposer, executor, and validator.

### 2.4 Cost of LLM generation

Generation cost is calculated from input/output token counts and model-specific prices per million tokens. The model supports single-prompt, multi-prompt, agentic, and hybrid strategies, and records the number of attempts.

The budget object sets a total limit and a per-test limit, tracks accumulated spending and number of generated tests, and determines whether a proposed generation cost is admissible.

### 2.5 Versioning generation prompts

Generation prompts are immutable, versioned objects with IDs, target model, SHA-256 hash, and quality metrics: tests generated, valid tests, tautological tests, and average cost per test. Prompt history selects the best prompt for a model and detects regressions against a configurable threshold.

### 2.6 Semantic validation of refuters

The semantic validator checks whether a refuter is genuinely falsifiable, using semantic entropy to detect tautologies. It distinguishes structural tautology (the refuter merely restates the implementation) from semantic tautology (the refuter is vacuously true), and returns falsifiability, semantic entropy, confidence, reason, and tautology type.

### 2.7 Multi-agent testing

The multi-agent system assigns explicit roles and permissions to agents. Its orchestration cycle is:

1. The LLM generator proposes tests.
2. The semantic validator checks the refuters.
3. The Auditor verifies integrity.
4. The Executor runs the tests.
5. If a test fails, the process returns to the generator with feedback.

The system limits the number of iterations and keeps role lookup explicit.

### 2.8 Execution history and flakiness

Execution history stores a rolling window of results (20 by default). It calculates success rate, flags flaky tests when the rate is between 5% and 95%, and determines whether a failure is significant. For a flaky test, significance requires the last three executions all to have failed.

---

## PART 3 — THE MATHEMATICS OF TESTING

### 3.1 Master fitness equation

The testing fitness model uses `φ`, `ψ`, `ω`, `α`, and `ε`, with an optional `k` parameter. Fitness is calculated as:

$$F = \phi \cdot \psi \cdot \omega^\alpha \cdot \varepsilon$$

### 3.2 The six reduction conditions (SRC)

The protocol defines six reduction conditions used to assess whether a test can be simplified without losing the property it is intended to verify. Their executable definitions and thresholds are maintained in the source implementation.

### 3.3 Property-Based Testing with adversarial refinement

**2026 state of the art:** PROBE introduces Adversarial Refinement: a Validator agent generates counter-implementations (semantically incorrect code that nevertheless satisfies the generated property) to expose gaps in the specification. PROBE increases mutation scores by 9.79% and identified 45 previously unknown bugs in leading libraries.

### 3.4 Mutation Testing with LLMs

**2025–2026 state of the art:** Firefly shows that even designs with 95% coverage can contain up to 28% undetected bugs. SMART shows that LLMs can generate high-quality mutants, with even 7B models matching GPT-4o.

### 3.5 Property-Based Testing for LLMs

The protocol treats property-based testing as a distinct testing strategy for LLM systems, rather than assuming that conventional example-based tests are sufficient.

### 3.6 Semantic entropy for test validation

**2026 state of the art:** VALTEST introduces a framework that uses semantic entropy to automatically validate test cases generated by LLMs. Results suggest semantic entropy is a reliable signal for identifying invalid tests. It is calculated by generating multiple answers to the same question and measuring uncertainty across semantic clusters.

---

## PART 4 — INTEGRITY AND CYBERSECURITY

### 4.1 Integrity chain

The protocol binds test identity, execution records, and build artifacts through cryptographic integrity. **2026 state of the art:** software supply-chain attacks more than doubled globally in 2025. SLSA provenance creates a cryptographic chain linking an artifact to its source commit.

### 4.2 OWASP Top 10:2025 — honest operational mapping

| OWASP category | Automatable | Tool | 1310 test |
|---|---|---|---|
| A01: Broken Access Control | Partial | ZAP, Burp | Integration + Security |
| A02: Security Misconfiguration | **Yes** | Checkov, Trivy | Integrity + IaC scan |
| A03: Supply Chain Failures | **Yes** | Syft, Snyk | Integrity + SBOM |
| A04: Cryptographic Failures | **Yes** | SAST | Unit + Security |
| A05: Injection (including Prompt Injection) | **Yes** | SQLMap, SAST | Unit + Property |
| A06: Insecure Design | **NO** (human required) | Manual + LLM | Threat model + E2E |
| A07: Authentication Failures | Partial | ZAP, custom | E2E + Security |
| A08: Data Integrity Failures | **Yes** | Sigstore | Integrity + Contract |
| A09: Logging Failures | **Yes** | Custom | Integration |
| A10: Mishandling Exceptional Conditions | **NO** (human required) | Custom | Integration + Chaos |

**Honesty rule:** A06 and A10 are not automatable. The protocol says so explicitly.

### 4.3 NIST SP 800-218A — AI SSDF Profile

The protocol maps AI-specific secure-development practices to the NIST SSDF profile and treats them as auditable requirements rather than generic claims of compliance.

### 4.4 Chaos Engineering for AI agents

**2026 state of the art:** AgentChaos proposes programmatic runtime fault injection for LLM APIs. The paper reports that only 14.4% of agents reach production with complete security and IT approval.

### 4.5 Continuous adversarial red teaming

Red teaming is treated as a continuous activity. Findings should generate regression tests, so that discovered attack paths become durable test cases rather than isolated reports.

### 4.6 Regulatory cycles

Regulatory requirements do not share one universal testing cadence.

**Rule:** a test declaring `PCI_DSS` as a standard must run at least quarterly. If it has not run for 90 days, the Auditor marks it `EXPIRED`.

---

## PART 5 — LORE AS A TYPE

### 5.1 The 1310 seal

**Hard rule:** Pydantic validates `seal: Literal[1310] = 1310`. A test without the seal cannot be instantiated. If an attempt is made to modify the seal, the hash changes and the test becomes `BLOCKED`.

### 5.2 Testing heteronyms

The protocol assigns named roles to different functions in the testing process. These are operational identities, not decorative character labels.

### 5.3 Visibility layers

The protocol distinguishes what each role may propose, execute, validate, and audit. Visibility and permissions are part of the control model.

---

## PART 6 — LIFECYCLE

A test marked **TAUTOLOGICAL** is not deleted. It is labelled and documented in the negative corpus as a failure by the Proposer. A **FAILED** test is also retained and labelled, with its failure documented.

---

## PART 7 — THE 1310 AUDITOR

### 7.1 Auditor with versioning, risk, and semantic validation

The Auditor combines immutable versioning, risk references, semantic refuter validation, execution history, and integrity checks. It does not treat the presence of a refuter field as proof that the refuter is meaningful.

### 7.2 Roles and separation of duties

The protocol explicitly separates proposer, executor, and validator roles.

**Rule for small teams:** if one user holds multiple roles, the system flags `SEPARATION_RISK` in the report.

**Multi-agent rule:** the `LLMGenerator` cannot be the same model as the `SemanticValidator`. If the Generator uses GPT-4, the Validator uses Claude or Gemini.

### 7.3 Execution-cost management

**1310 rule:** if a test costs more to run than the estimated bug it prevents, it should not run on every commit. It should run nightly or before release.

### 7.4 Emulation-escape metrics

The protocol records metrics for behaviour that escapes emulation, especially where simulated execution is used instead of hardware-in-the-loop or other higher-fidelity environments.

---

## PART 8 — LITE IMPLEMENTATION

### 8.1 Five-minute quickstart

The Lite implementation is intended to be deployable with minimal ceremony.

**That is all.** Five minutes. No Pydantic. No models. No manual SHA-256 handling.

### 8.2 LLM onboarding guide

The LLM receives the contract and the protocol rules, generates candidate tests, and supplies explicit refuters. The semantic validator and Auditor remain separate controls; the model must not be allowed to certify its own output.

---

## PART 9 — FULL IMPLEMENTATION

### 9.1 Complete architecture

The Full level uses all models defined in Part 2. The 1310 Auditor orchestrates:

1. **Preregistration** of every `ImmutableTest`.
2. **Semantic validation** of the refuter.
3. **Integrity verification** (SHA-256 hash).
4. **Execution** with a `TestState` record.
5. **Blocking decision** based on history, severity, and category.
6. **Reporting** with business impact, costs, and covered standards.

### 9.2 Anomaly management for regulated domains

Regulated environments require anomaly records with traceable causes, decisions, and corrective actions. An anomaly is not closed merely because a test has been rerun successfully.

### 9.3 Business reporting

**2026 state of the art:** teams adopting TDD report defect reductions between 40% and 90%. Organizations implementing test automation may reduce QA operating costs by 40% to 85%. These figures are contextual claims, not guarantees for an individual deployment.

---

## PART 10 — DOMAIN-SPECIFIC GUIDANCE

### 10.1 Cybersecurity

**Level:** Standard or Full.

**Frameworks:** Semgrep, CodeQL, SonarQube (SAST); ZAP and Burp Suite (DAST); Atheris and AFL++ (fuzzing); Snyk, Dependabot, and Trivy (SCA); Syft and CycloneDX (SBOM); slsa-github-generator and in-toto (SLSA provenance).

**Practices:** threat modelling before the first test; SAST/DAST on every commit; continuous adversarial red teaming; SBOM + SLSA 3+.

### 10.2 Banking and Financial Services

**Level:** Full.

**Frameworks:** Pact and PactFlow (contract testing); Hypothesis (financial PBT); Parasoft and Tricentis Tosca (compliance); JMeter, k6, and Gatling (performance); TIBER-EU (TLPT).

**Practices:** mandatory contract testing between services; financial PBT; TLPT every three years; DORA traceability; differentiated regulatory cycles.

### 10.3 IoT and Embedded Systems

**Level:** Standard or Full, depending on criticality.

**Frameworks:** Unity Test (C); Google Test (C++); Ceedling (embedded C); PlatformIO and ArduinoUnit (board automation); Renode and QEMU (simulation); LabVIEW and dSPACE (HIL); Otii and Joulescope (power profiling).

**Practices:** HIL → PIL → SIL → emulation fallback; escape metrics; power profiling as a non-functional test; network fuzzing.

### 10.4 Healthcare and Medical Devices

**Level:** Full.

**Frameworks:** Jira + Xray / TestRail (traceability); Greenlight Guru and MasterControl (QMS); pytest and JUnit (unit testing); Hypothesis (clinical PBT); ELK and Splunk (access auditing).

**Practices:** requirement-to-test traceability; root-cause anomaly management; IEC 62304 under 2026 review; human-in-the-loop.

### 10.5 Automotive

**Level:** Full.

**Frameworks:** Parasoft C/C++test (MC/DC); Floyd (Rust, open source); Reactis and Testwell CTC++ (coverage); CodeSonar (static analysis); dSPACE and Vector (MIL/SIL/PIL/HIL); CANoe and Vehicle Spy (bus).

**Practices:** MC/DC mandatory for ASIL C/D; ISO 21434 TARA; MIL/SIL/PIL/HIL. Open-source alternative: Floyd for Rust, extended LLVM-Cov for DO-178C.

### 10.6 Video Games

**Level:** Standard.

**Frameworks:** TITAN (LLM agents in MMORPGs); MIMIC (agent personalities); GameEval (browser games); Applitools (visual regression); RenderDoc and Unity Profiler (performance).

**Practices:** LLM agents as exploratory testers; bounded execution budget; Monte Carlo balance testing.

### 10.7 DevOps and Cloud

**Level:** Lite or Standard.

**Frameworks:** SonarQube (quality gate); Checkov, OPA, and Terratest (IaC); Trivy and Grype (containers); Syft and CycloneDX (SBOM); Prometheus, Grafana, and OpenTelemetry (observability); Flagger and Argo Rollouts (canary).

**Practices:** automated quality gates; ephemeral environments; shift-right with canary; observability as a test.

### 10.8 ML and LLM

**Level:** Standard or Full.

**Frameworks:** DeepEval, Promptfoo, and Giskard (LLM testing); Evidently and NannyML (drift); Fairlearn and AIF360 (fairness); SHAP and LIME (explainability); Great Expectations and Pandera (data validation).

**Practices:** continuous drift testing; fairness testing; LLM hallucination, bias, and safety testing; generative-model red teaming; monitored execution costs.

---

## PART 11 — DESIGN DECISIONS

1. **Frozen vs mutable:** immutable for identity, mutable for state; keep them separate.
2. **Who proposes tests:** anyone; only the Auditor validates. Roles are explicit.
3. **Signature:** SHA-256 + GPG/Sigstore; SLSA provenance for artifacts.
4. **Exploratory tests:** refuter optional; state `SKIPPED`.
5. **1310 seal:** **MANDATORY**. It certifies the falsifiability protocol.
6. **Failed tests:** retain them in the `NegativeCorpus`; they are the most valuable asset.
7. **Flakiness:** history + threshold; quarantine with a deadline.
8. **ML:** `TestML` extension.
9. **HIL:** fallback with an escape metric.
10. **ROI:** `BusinessReport` with transparent formulas.
11. **Versioning:** semantic; `parent_test` + `version_reason`.
12. **Risk:** FMEA/FTA mandatory for severity ≥ 9.
13. **Red teaming:** continuous; every finding generates a regression test.
14. **Cost:** monitored; distinguish commit tests from release tests.
15. **Regulatory cycles:** differentiated by standard.
16. **Onboarding:** five-minute quickstart + LLM guide.
17. **Scalability:** SQLite for history; circular buffer.
18. **Prioritization:** critical tests first; choose frameworks by layer, not fashion.
19. **Adoption:** phased roadmap.
20. **Generation cost:** `GenerationCost` + `GenerationBudget`.
21. **Prompt versioning:** `GenerationPrompt` + `PromptHistory`.
22. **Semantic validation:** `SemanticValidator` + `SemanticEntropy`.
23. **Multi-agent:** `MultiAgentSystem` with roles as agents.
24. **Tautology detection:** `TAUTOLOGICAL` state + tautology types.
25. **Model diversity:** Generator and Validator use different models.

### Adoption roadmap

| Phase | Duration | Implementation | Success metric |
|---|---|---|---|
| **Pilot** | 1–2 months | Lite in one team; refuters in docstrings | 20 tests with refuters |
| **Expansion** | 3–6 months | Standard in 2–3 teams; roles, history, business report, semantic validation | ROI > 1.0; flakiness < 5%; tautologies < 10% |
| **Scale** | 6–12 months | Full across the organization; SBOM, SLSA, ML, regulatory cycles, multi-agent | Regulatory audit passed |
| **Optimization** | 12+ months | Continuous red teaming; published experience paper | Documented success cases |

**The AI-assisted QA extension:** the protocol is designed so that an LLM can operate it unambiguously. The human defines the contract (refuter, severity, standard). The LLM generates the test. The Semantic Validator checks that the refuter is falsifiable. The Auditor checks integrity. The Executor runs it. The Chronicler documents it. Everything has a cost, version, and traceability.

**1310.**

*The one who designs the test also writes the pipeline. And the one who runs it does too. But the one who chooses the level decides which protocol is needed. And the one who validates the refuter decides whether the test is a test or an illusion.*

---

# APPENDIX A — DESIGN ALTERNATIVES REJECTED

### A.1 Optional 1310 seal at Lite level

**Considered:** allowing Lite level to omit the 1310 seal.

**Rejected:** the seal is not an ornament. It certifies that the test has passed through the falsifiability protocol. Without the seal, there is no test.

### A.2 Hashing the complete model

**Considered:** calculating SHA-256 over the complete object, including state.

**Rejected:** the hash would change on every execution. Alternative: separate `ImmutableTest` from `TestState`.

### A.3 Static flakiness history

**Considered:** declaring flakiness as a field of the test.

**Rejected:** flakiness is dynamic. Alternative: `ExecutionHistory` with a window of 20.

### A.4 ML tests outside the protocol

**Considered:** a separate system for ML.

**Rejected:** in banking, 40% of risk is model risk. Alternative: `TestType.ML_*`.

### A.5 Mandatory HIL for IoT

**Considered:** requiring HIL for every firmware test.

**Rejected:** hardware is expensive. Alternative: fallback + `EscapeMetric`.

### A.6 Full automation of OWASP Top 10

**Considered:** promising automated coverage of all ten categories.

**Rejected:** A06 and A10 are not automatable. Alternative: an honest table with “Automatable: Yes/Partial/NO”.

### A.7 Optional threat modelling

**Considered:** a recommendation rather than a requirement.

**Rejected:** without a threat model, a security test is a checklist.

### A.8 ROI without an explicit formula

**Considered:** ROI as an internally calculated number.

**Rejected:** it is not auditable. Alternative: an explicit `roi_formula` in the report.

### A.9 Overwriting versions

**Considered:** overwriting the previous test when it changes.

**Rejected:** traceability is lost. Alternative: semantic versioning with `parent_test`.

### A.10 A single level

**Considered:** one protocol without levels.

**Rejected:** a bank needs Full; a startup needs Lite. Alternative: three levels.

### A.11 The 1310 seal as a metaphor without a function

**Considered:** a decorative narrative element.

**Rejected:** if it certifies nothing, there is no reason to keep it. Alternative: `Literal[1310]` validated by Pydantic.

### A.12 Running every test on every commit

**Considered:** the complete suite on every commit.

**Rejected:** LLM tests cost money. Alternative: commit tests versus release tests.

### A.13 Annual red teaming

**Considered:** once a year.

**Rejected:** attackers do not wait. Alternative: `ContinuousRedTeaming`.

### A.14 Unified regulatory cycles

**Considered:** the same cycle for every standard.

**Rejected:** PCI DSS is quarterly, DORA triennial, IEC 62304 annual. Alternative: differentiated `RegulatoryCycle`.

### A.15 In-memory history

**Considered:** keeping suite history as in-memory JSON.

**Rejected:** 300,000 records in memory are unmanageable. Alternative: SQLite.

### A.16 One framework per layer

**Considered:** recommending a single framework for each layer.

**Rejected:** the choice depends on language and team. Alternative: a table of options.

### A.17 Optional refuter

**Considered:** allowing tests without a refuter.

**Rejected:** without a refuter, a test is a tautology. Alternative: mandatory at every level.

### A.18 Dynamically calculated seal

**Considered:** making the seal a function of the hash.

**Rejected:** the seal is not a hash. It is a constant certification.

### A.19 One Auditor without roles

**Considered:** a single “tester” role.

**Rejected:** separation of duties is required by PCI DSS, SOX, and DORA. Alternative: four roles.

### A.20 Extensive documentation as onboarding

**Considered:** using the complete manual for onboarding.

**Rejected:** a new developer will not read 40 pages. Alternative: a five-minute quickstart.

### A.21 Test generation without cost monitoring

**Considered:** generating tests without `GenerationCost`.

**Rejected:** a test suite using GPT-4 costs between $5 and $50 per run. Cost must be budgeted. Alternative: `GenerationCost` + `GenerationBudget`.

### A.22 Ignoring prompt versioning

**Considered:** not versioning generation prompts.

**Rejected:** if the prompt changes, the tests change. That is a protocol-version change. Alternative: `GenerationPrompt` + `PromptHistory`.

### A.23 Semantic validation using forbidden words only

**Considered:** relying on a validator that only detects forbidden words.

**Rejected:** an LLM can write “if the result is incorrect, it fails”. That is tautological but contains no forbidden words. Alternative: `SemanticValidator` with semantic entropy.

### A.24 One LLM agent for everything

**Considered:** one agent that generates, validates, and executes.

**Rejected:** an agent cannot validate its own output without bias. Alternative: `MultiAgentSystem` with separate roles and diverse models.

### A.25 Tautological tests treated as passed

**Considered:** a tautological test passes because its assertion is true.

**Rejected:** a tautological test verifies nothing. Alternative: a `TAUTOLOGICAL` state that does not count toward coverage.

---

## CLOSING

Testing Protocol 1310 formalizes every test as a typed object with a mandatory refuter, severity, cybersecurity standard, integrity signature, segregated roles, semantic validation, and the 1310 seal. The Auditor verifies. The system reports. And the suite grows through refutation, not accumulation.

**The 1310 seal is mandatory.** It certifies that a test has passed the falsifiability protocol. Without the seal, there is no test. There is a script.

**1310.**

*The one who designs the protocol also decides what to discard. And the reader of the appendix knows why.*

---

## Implementation listings and code parity

The Spanish source contains the complete Pydantic v2 models, executable examples, Lite and Full implementation snippets, and supporting implementation details. Those code blocks are deliberately not duplicated here: they remain the executable source of truth and must not drift between language editions. Comments and user-facing strings inside those code listings remain in Spanish and are not represented as translated.

**Translation status:** Complete translation of the protocol's explanatory text and design appendix. Embedded Python listings and their comments are retained in the Spanish source and remain untranslated.
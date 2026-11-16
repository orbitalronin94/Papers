# TESTING PROTOCOL 1310 — EXTENDED VERSION 1.0

**Operational manual for a typed, falsifiable, integrity-preserving, auditable testing system, with an extension for AI-assisted QA.**

**Pydantic v2 + mathematics + cybersecurity + 2025–2026 state of the art + multi-agent systems + semantic validation.**

## PART 0 — PRINCIPLE AND DECISION GUIDE

A test is not an opinion. It is a **falsifiable testimony** about software behaviour. Each test becomes a typed object with a mandatory refuter, severity, cybersecurity standard, and 1310 seal. The system, an **Auditor 1310**, verifies integrity, executes, and reports.

**Without a refuter, there is no test. There is an illusion of coverage.**

**The 1310 seal is not decorative.** It certifies that the test has passed the falsifiability protocol: it has an explicit refuter, a failure condition, a preregistered hash, and an integrity audit. A test without the 1310 seal is an executable script. A test with the 1310 seal is a statement that can be refuted.

**This protocol is designed so that an LLM can operate it unambiguously.** It is not a protocol for humans who write tests by hand. It is a protocol for humans who write **the contract**, and agents that generate, execute, and validate tests against it.

### Decision tree: which level do I need?

**Question 1: If your software fails, could it cause physical, financial, or legal harm?**
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
| **Lite** | Startups, teams of 1–10 | pytest plugin, refuter in docstring, automatic hash, generation cost | Roles, SBOM, SLSA, ML, HIL, regulatory audit |
| **Standard** | Mid-sized companies, B2B SaaS, teams of 10–50 | Lite + roles + standards + business report + basic ML + multi-agent | SLSA 3+, HIL, TLPT, MC/DC |
| **Full** | Banking, healthcare, automotive, defence, regulated environments | Standard + SBOM + SLSA 3+ + MC/DC + HIL + TLPT + auditable segregation + full ML + semantic validation | Nothing; this is the complete protocol |

## PART 1 — HOW THE PROTOCOL WORKS

### 1.1 The lifecycle

The protocol has four phases. Each has a purpose and an owner.

**Phase 1 — PROPOSED.** The Architect (or developer, in Lite) writes the test. They declare what it verifies, how it can be refuted, its severity, and which standard it contributes to.

**Phase 2 — PREREGISTERED.** The system calculates a SHA-256 hash of the test's **immutable identity** (not its state) and stores it. From this point on, the test cannot be modified without invalidating the hash.

**Phase 3 — RUNNING.** The Executor (or CI/CD) runs the test. The result is recorded as `PASSED`, `FAILED`, `BLOCKED`, or `QUARANTINED`.

**Phase 4 — AUDITED.** Auditor 1310 verifies that the hash matches, the result is consistent, and any failure has a documented root cause.

**Golden rule:** a test that has not passed through all four phases is not a test. It is a script.

### 1.2 The refuter, explained

The refuter is the most important part of the protocol. It answers the question: **what would have to happen for this test to become invalid?**

Without a refuter, a test is a tautology. It verifies what it verifies because it verifies it. It contributes no information.

**The problem with AI-generated tests:** empirical studies show that LLMs generate tests that compile and achieve reasonable coverage but **fail to detect bugs**, and frequently exhibit “design smells” that undermine their effectiveness. Used naively, these assistants tend to generate **tautological tests that restate implementation logic instead of challenging it**.

**Bad example (no refuter):**
```python
def test_addition():
    assert 2 + 2 == 4
```

**Good example (with a refuter):**
```python
def test_transfer_does_not_allow_negative_balance():
    """
    REFUTER: If transferring €100 from an account with €50 and no overdraft
    results in a balance >= 0 and the transfer completes.
    FAILURE_CONDITION: final_balance >= 0 and transfer.completed
    """
    account = Account(balance=50, overdraft_enabled=False)
    result = transfer(account, destination, 100)
    assert result.failed
    assert account.balance == 50
```

### 1.3 The Auditor, explained

Auditor 1310 is not a judge. It is an **integrity verifier**.

Its functions are:
1. **Verify the hash.** Compare the current test hash with the preregistered hash.
2. **Validate the refuter semantically.** It is not enough for one to exist; it must genuinely be falsifiable.
3. **Decide whether a failure is significant.** Use the execution history.
4. **Report.** Generate JSON with suite status, business impact, and covered standards.

**The Auditor cannot validate a test that it proposed itself.**

## PART 2 — DATA MODEL (PYDANTIC V2)

This part defines the typed data structures for test identity, state, signatures, security standards, roles, LLM generation, costs, prompts, semantic validation, multi-agent orchestration, and execution history.

The canonical Pydantic definitions are preserved unchanged in the Spanish source. Their identifiers and serialized field names are part of the proposed interface; translating them would silently change the API and invalidate compatibility. The source contains, in order:

- Base enumerations for test type, category, state, cybersecurity standard, severity, domain, role, protocol level, and LLM model.
- A test signature and immutable, versioned test object.
- Separate mutable execution state, preserving immutable test identity.
- LLM generation-cost accounting and budget enforcement.
- Versioned generation prompts and prompt-regression detection.
- Semantic refuter validation and classification of tautological tests.
- Multi-agent roles and orchestration.
- Execution history and flakiness detection.

**Versioning rule:** a test with `test_padre` does not replace its parent; it versions it. The parent is marked `OBSOLETO` and remains in the corpus for traceability.

### 2.4 LLM generation cost

**The problem:** generating 100 tests with GPT-4 costs money. Cost per test varies substantially by model and strategy. The source cites Sakura with Qwen3-Coder at **$0.07 per test**, approximately half the cost of Gemini CLI with Gemini 2.5 Pro; Devstral Small 2 matches the Flash-tier price at **$0.02 per test**. TestForge generates tests for a complete file at **$0.63 per file**. DiffTestGen costs **$0.041 per instance**, compared with $0.045 for Testora++. Claude Sonnet 4.5 with single prompting reduces cost from **$0.95 to $0.20 per instance**.

**1310 rule:** if the cost of generating a test exceeds the estimated cost of the bug it prevents, that model must not be used to generate the test. Use a cheaper model or write it by hand. The protocol distinguishes **low-cost generation tests** (Qwen3-Coder, Devstral) from **premium generation tests** (Claude Opus, GPT-4).

**A 100-case test suite using GPT-4 can cost between $5 and $50 per run.** The cost must be budgeted, not discovered after the fact.

### 2.5 Versioning generation prompts

**The problem:** if the Proposer's prompt changes, generated tests change. That is a protocol-version change, not a test change. The protocol must distinguish between them.

**2026 state of the art:** prompts are code — they need version control, testing, and gradual deployments just like software. Best practice includes versioning generation prompts alongside code. When test patterns change, prompts are updated accordingly.

**1310 rule:** a prompt change that reduces the validity rate by more than 5% is a regression. The previous prompt remains available as a fallback. A prompt is not updated in production without prior A/B testing.

### 2.6 Semantic validation of refuters

**The problem:** an LLM can write “REFUTER: if the result is incorrect, the test fails.” That is not a refuter. It is a tautology. The current validator only detects prohibited words (`depends`, `perhaps`). It does not detect semantic tautologies.

**2026 state of the art:** **VALTEST** uses **semantic entropy** to automatically validate LLM-generated test cases. It measures uncertainty in semantic parts of a test case and uses those signals to identify invalid tests before downstream use. Empirical studies show that LLMs generate oracles with an average mutation score of **43%**, similar to the **45%** achieved by human-designed oracles.

**Types of tautological tests the SemanticValidator must detect:**

| Type | Description | Example |
|---|---|---|
| **Vacuously true** | The refuter cannot be false under any circumstances | “If the result is incorrect, the test fails” |
| **Restatement** | The refuter uses the same logic as the implementation | `assert build_query(x) == build_query(x)` |
| **Mock passthrough** | The test checks that a mock returns what it was configured to return | `mock.return_value = 5; assert obj.method() == 5` |
| **Internal assertion** | The test checks internal state rather than behaviour | `assert obj._cache == {}` |
| **Useless snapshot** | The snapshot verifies nothing useful | `expect(foo()).toMatchSnapshot()` without review |

**1310 rule:** if the SemanticValidator detects a tautology, the test moves to state `TAUTOLOGICO`. It is not executed, does not count towards coverage, and does not block a release. It is, however, recorded in the negative corpus as a Proposer failure.

### 2.7 Multi-agent systems: roles as agents

**The problem:** an LLM can generate a test, but cannot validate it without bias. The separation of duties that is an organizational challenge in a human team is a natural architecture in a multi-agent system.

**2026 state of the art:** TestAgent proposes an LLM-based test-generation approach that addresses current limitations by emulating human testing practices through **multi-agent collaboration**. It designs three specialized agents. Recent research argues that multi-agent frameworks generate better unit tests than a single carefully crafted prompt by iteratively refining coverage and cross-checking oracles.

**Roles mapped to agents:**

| Human role | LLM agent | Function |
|---|---|---|
| Proposer | LLMGenerator | Generates tests from requirements and code |
| Validator | SemanticValidator | Checks whether refuters are falsifiable |
| Executor | Executor | Runs tests in CI/CD |
| Auditor | Auditor1310 | Verifies integrity, hashes, and roles |
| Chronicler | Chronicler | Documents results and maintains the negative corpus |

**1310 rule:** a test generated by `LLMGenerator` cannot be semantically validated by the same model. If the Generator uses GPT-4, the Validator uses Claude or Gemini. Model diversity is the independence safeguard.

### 2.8 Execution history and flakiness

The execution history is stored in SQLite (`.testing1310/historial.db`). The 20-run window is calculated with `ORDER BY timestamp DESC LIMIT 20`.

## PART 3 — THE MATHEMATICS OF TESTING

### 3.1 Master fitness equation

The protocol defines a fitness equation using `phi`, `psi`, `omega`, `alpha`, and `epsilon`. The canonical implementation is preserved in the source code.

### 3.2 The six reduction conditions (SCR)

The SCR model records six reduction conditions: static behaviour, epsilon equal to one, psi equal to one, alpha equal to one, phi equal to one, and the infinite-resource limit. Its `amputaciones()` method counts how many reductions apply.

### 3.3 Property-based testing with adversarial refinement

**2026 state of the art:** PROBE introduces Adversarial Refinement: a Validator agent generates counter-implementations (semantically incorrect code that satisfies the generated property) to expose gaps in the specification. PROBE increases mutation scores by 9.79% and identified 45 previously unknown bugs in major libraries.

### 3.4 Mutation testing with LLMs

**2025–2026 state of the art:** Firefly demonstrates that even designs with 95% coverage can leave up to 28% of bugs undetected. SMART demonstrates that LLMs can generate high-quality mutants, with even 7B models matching GPT-4o.

### 3.5 Property-based testing for LLMs

The protocol defines LLM properties using an invariant, a generation prompt, a bounded number of examples, a metric (hallucination, faithfulness, toxicity, bias, or answer relevance), a threshold, and a comparison direction.

### 3.6 Semantic entropy for test validation

**2026 state of the art:** VALTEST introduces a framework that uses semantic entropy to automatically validate LLM-generated test cases. Results suggest semantic entropy is a reliable signal for identifying invalid tests. It is calculated by generating multiple responses to the same question and measuring uncertainty across semantic clusters.

## PART 4 — INTEGRITY AND CYBERSECURITY

### 4.1 Integrity chain

The integrity object includes a SHA-256 hash, optional GPG signature, SBOM reference, SLSA level, provenance reference, and known vulnerabilities.

**2026 state of the art:** software supply-chain attacks more than doubled globally in 2025. SLSA provenance creates a cryptographic chain linking an artifact to its originating commit.

### 4.2 OWASP Top 10:2025 — operational mapping with epistemic honesty

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

**Honesty rule:** A06 and A10 are not automatable. The protocol states this explicitly.

### 4.3 NIST SP 800-218A — AI SSDF profile

The protocol represents SSDF practices by group (PO, PS, PW, RV), practice identifier, AI-profile flag, and evidence.

### 4.4 Chaos engineering for AI agents

**2026 state of the art:** AgentChaos proposes programmatic runtime fault injection for LLM APIs. The source reports that 14.4% of agents reach production with full security and IT approval.

### 4.5 Continuous adversarial red teaming

Each red-team exercise records its objective, type (TLPT, Vibe Red Teaming, or adversarial fuzzing), frequency, framework, findings, and associated regression test.

### 4.6 Regulatory cycles

**Rule:** a test that declares `PCI_DSS` as its standard must run at least quarterly. If it has not run for 90 days, the Auditor marks it as `CADUCADO`.

## PART 5 — LORE AS A TYPE

### 5.1 The 1310 seal

**Hard rule:** Pydantic validates `sello: Literal[1310] = 1310`. If a test has no seal, it cannot be instantiated. If an attempt is made to modify the seal, the hash changes and the test becomes `BLOCKED`.

### 5.2 Testing heteronyms

The protocol models the Architect, Executor, Auditor 1310, Chronicler, LLM Generator, and Semantic Validator as explicit roles with separate capabilities.

### 5.3 Visibility layers

Each testing layer records its level, name, visibility in CI and GitHub, and whether it includes 1310.

## PART 6 — LIFECYCLE

The lifecycle runs from **PROPOSED** to **GENERATED_BY_LLM** (when applicable), **PREREGISTERED**, and **RUNNING**, then branches into **PASSED**, **FAILED**, **BLOCKED**, **QUARANTINED**, or **TAUTOLOGICAL**.

A **TAUTOLOGICAL** test is not deleted. It is marked and documented in the negative corpus as a Proposer failure. A **FAILED** test is not deleted either; the failure is recorded.

## PART 7 — AUDITOR 1310

### 7.1 Auditor with versioning, risk, and semantic validation

Auditor 1310 orchestrates preregistration of every immutable test, semantic validation of the refuter, SHA-256 integrity verification, execution and recording of test state, blocking decisions based on history/severity/category, and reporting of business impact, costs, and covered standards.

### 7.2 Roles and separation of duties

**Rule for small teams:** if one user holds multiple roles, the system marks `RIESGO_SEGREGACION` in the report.

**Multi-agent rule:** `LLMGenerator` cannot be the same model as `SemanticValidator`. If the Generator uses GPT-4, the Validator uses Claude or Gemini.

### 7.3 Execution-cost management

**1310 rule:** if a test costs more to run than the estimated cost of the bug it prevents, it is not run on every commit. It runs nightly or before release.

### 7.4 Emulation escape metrics

The protocol records the origin level (emulation, SIL, PIL, HIL), bugs found, bugs escaping to HIL, and escape rate. HIL is justified when the escape rate exceeds 0.3.

## PART 8 — LITE IMPLEMENTATION

### 8.1 Five-minute quickstart

1. Install the plugin: `pip install testing1310`.
2. Activate Lite mode in `conftest.py`.
3. Write a test with an explicit refuter, failure condition, severity, and 1310 seal.
4. Run `pytest --testing1310`.
5. Read `.testing1310/reporte.json`.

**That is all.** Five minutes. No Pydantic, no models, no manual SHA-256.

### 8.2 LLM onboarding guide

An LLM operating as a 1310 testing agent must give every generated test:
1. An explicit refuter (what would have to happen for the test to fail).
2. A failure condition (the concrete assertion).
3. A severity (critical, high, medium, low, or info).
4. At least one cybersecurity standard if `type == SECURITY`.
5. A 1310 seal.

It must not generate tests without refuters, generic refuters, or tautological tests. If it cannot formulate a refuter that could be false, the test is not a test; it is a script.

If the SemanticValidator detects a tautological refuter, the test moves to `TAUTOLOGICO`. It does not count towards coverage or block a release, but remains recorded as a Proposer failure.

## PART 9 — FULL IMPLEMENTATION

### 9.1 Complete architecture

Full level uses all models defined in Part 2. Auditor 1310 orchestrates:
1. Preregistration of each `TestInmutable`.
2. Semantic validation of the refuter.
3. Integrity verification (SHA-256 hash).
4. Execution with `TestEstado` recording.
5. Blocking decisions based on history, severity, and category.
6. Reporting of business impact, costs, and covered standards.

### 9.2 Anomaly management for regulated domains

**Rule:** a failure in a regulated domain can only be closed when a root cause and corrective action are documented.

### 9.3 Business reporting

The business report records totals for passed, failed, blocked, tautological, and invalid-refuter tests; estimated bugs prevented; avoided production-bug cost; reduced mean repair time; OWASP and requirements coverage; estimated ROI; generation costs; and the assumptions/formulae used.

**2026 state of the art:** teams adopting TDD report defect reductions of 40%–90%. Organizations implementing test automation can reduce QA operating costs by 40%–85%.

## PART 10 — DOMAIN-SPECIFIC GUIDANCE

### 10.1 Cybersecurity

**Level:** Standard or Full.

**Frameworks:** Semgrep, CodeQL, SonarQube (SAST); ZAP, Burp Suite (DAST); Atheris, AFL++ (fuzzing); Snyk, Dependabot, Trivy (SCA); Syft, CycloneDX (SBOM); slsa-github-generator, in-toto (SLSA provenance).

**Practices:** threat modelling before the first test; SAST/DAST on every commit; continuous adversarial red teaming; SBOM + SLSA 3+.

### 10.2 Banking and financial services

**Level:** Full.

**Frameworks:** Pact, PactFlow (contract); Hypothesis (financial PBT); Parasoft, Tricentis Tosca (compliance); JMeter, k6, Gatling (performance); TIBER-EU (TLPT).

**Practices:** mandatory contract testing between services; financial PBT; triennial TLPT; DORA traceability; differentiated regulatory cycles.

### 10.3 IoT and embedded systems

**Level:** Standard or Full, depending on criticality.

**Frameworks:** Unity Test (C); Google Test (C++); Ceedling (embedded C); PlatformIO, ArduinoUnit (board automation); Renode, QEMU (simulation); LabVIEW, dSPACE (HIL); Otii, Joulescope (power profiling).

**Practices:** HIL → PIL → SIL → emulation fallback; escape metrics; power profiling as a non-functional test; network fuzzing.

### 10.4 Healthcare and medical devices

**Level:** Full.

**Frameworks:** Jira + Xray / TestRail (traceability); Greenlight Guru, MasterControl (QMS); pytest, JUnit (unit); Hypothesis (clinical PBT); ELK, Splunk (access auditing).

**Practices:** requirement-to-test traceability; anomaly management with root cause; IEC 62304 under 2026 review; human-in-the-loop.

### 10.5 Automotive

**Level:** Full.

**Frameworks:** Parasoft C/C++test (MC/DC); Floyd (Rust, open source); Reactis, Testwell CTC++ (coverage); CodeSonar (static analysis); dSPACE, Vector (MIL/SIL/PIL/HIL); CANoe, Vehicle Spy (bus).

**Practices:** MC/DC mandatory for ASIL C/D; ISO 21434 TARA; MIL/SIL/PIL/HIL. Open-source alternative: Floyd for Rust, extended LLVM-Cov for DO-178C.

### 10.6 Video games

**Level:** Standard.

**Frameworks:** TITAN (LLM agents in MMORPGs); MIMIC (agent personalities); GameEval (browser games); Applitools (visual regression); RenderDoc, Unity Profiler (performance).

**Practices:** LLM agents as exploratory testers; bounded execution budget; Monte Carlo balance testing.

### 10.7 DevOps and cloud

**Level:** Lite or Standard.

**Frameworks:** SonarQube (quality gate); Checkov, OPA, Terratest (IaC); Trivy, Grype (containers); Syft, CycloneDX (SBOM); Prometheus, Grafana, OpenTelemetry (observability); Flagger, Argo Rollouts (canary).

**Practices:** automated quality gates; ephemeral environments; shift-right with canary; observability as a test.

### 10.8 ML and LLMs

**Level:** Standard or Full.

**Frameworks:** DeepEval, Promptfoo, Giskard (LLM testing); Evidently, NannyML (drift); Fairlearn, AIF360 (fairness); SHAP, LIME (explainability); Great Expectations, Pandera (data validation).

**Practices:** continuous drift testing; fairness testing; hallucination, bias, and safety tests for LLMs; generative-model red teaming; execution-cost monitoring.

## PART 11 — DESIGN DECISIONS

1. **Frozen vs mutable:** immutable for identity; mutable for state. Keep them separate.
2. **Who proposes tests:** anyone. Only the Auditor validates. Roles are explicit.
3. **Signature:** SHA-256 + GPG/Sigstore. SLSA provenance for artifacts.
4. **Exploratory tests:** refuter optional. State `SKIPPED`.
5. **1310 seal:** **MANDATORY.** It certifies the falsifiable protocol.
6. **Failed tests:** `CorpusNegativo`. The most valuable asset.
7. **Flakiness:** history + threshold. Quarantine with a deadline.
8. **ML:** `TestML` extension.
9. **HIL:** fallback with escape metric.
10. **ROI:** `ReporteNegocio` with transparent formulae.
11. **Versioning:** semantic. `test_padre` + `motivo_version`.
12. **Risk:** FMEA/FTA mandatory for severity ≥ 9.
13. **Red teaming:** continuous. Every finding generates a regression test.
14. **Cost:** monitored. Commit tests vs release tests.
15. **Regulatory cycles:** differentiated by standard.
16. **Onboarding:** five-minute quickstart + LLM guide.
17. **Scalability:** SQLite for history. Circular buffer.
18. **Prioritization:** critical tests first. Frameworks by layer, not fashion.
19. **Adoption:** phased roadmap.
20. **Generation cost:** `CosteGeneracion` + `PresupuestoGeneracion`.
21. **Prompt versioning:** `PromptGeneracion` + `HistorialPrompts`.
22. **Semantic validation:** `ValidadorSemantico` + `EntropiaSemantica`.
23. **Multi-agent:** `SistemaMultiAgente` with roles as agents.
24. **Tautology detection:** `TAUTOLOGICO` state + tautology types.
25. **Model diversity:** Generator and Validator use different models.

### Adoption roadmap

| Phase | Duration | Implementation | Success metric |
|---|---|---|---|
| **Pilot** | 1–2 months | Lite level in one team; refuters in docstrings | 20 tests with refuters |
| **Expansion** | 3–6 months | Standard in 2–3 teams; roles, history, business report, semantic validation | ROI > 1.0; flakiness < 5%; tautologies < 10% |
| **Scale** | 6–12 months | Full across the organization; SBOM, SLSA, ML, regulatory cycles, multi-agent | Regulatory audit passed |
| **Optimization** | 12+ months | Continuous red teaming; published experience paper | Documented success cases |

**The AI-QA extension:** the protocol is designed so an LLM can operate it unambiguously. The human defines the contract (refuter, severity, standard). The LLM generates the test. The SemanticValidator checks that the refuter is falsifiable. The Auditor checks integrity. The Executor runs it. The Chronicler documents it. Everything has a cost, version, and traceability.

**1310.**

*The one who designs the test also writes the pipeline. And the one who runs it, too. But the one who chooses the level decides which protocol is needed. And the one who validates the refuter decides whether the test is a test or an illusion.*

## APPENDIX A — ALTERNATIVES REJECTED DURING DESIGN

The following alternatives were considered and rejected:

1. **Optional 1310 seal in Lite:** rejected because the seal certifies passage through the falsifiability protocol; without it, there is no test.
2. **Hashing the complete model:** rejected because the hash would change on every execution. The design separates `TestInmutable` from `TestEstado`.
3. **Static flakiness history:** rejected because flakiness is dynamic. Use `HistorialEjecuciones` with a 20-run window.
4. **ML tests outside the protocol:** rejected; ML tests are represented by `TipoTest.ML_*`.
5. **Mandatory HIL for IoT:** rejected because hardware is expensive. Use fallback levels and `MetricaEscape`.
6. **Full automation of OWASP Top 10:** rejected because A06 and A10 are not automatable. Use an honest Yes/Partial/NO table.
7. **Optional threat modelling:** rejected because a security test without a threat model is a checklist.
8. **ROI without an explicit formula:** rejected as unauditable. The report exposes `formula_roi`.
9. **Overwrite-based versioning:** rejected because it destroys traceability. Use semantic versioning with `test_padre`.
10. **A single protocol level:** rejected because a bank needs Full while a startup needs Lite. Use three levels.
11. **1310 as a metaphor without a function:** rejected; use `Literal[1310]` validated by Pydantic.
12. **Run every test on every commit:** rejected because LLM tests cost money. Separate commit tests from release tests.
13. **Annual red teaming:** rejected because attackers do not wait. Use `RedTeamingContinuo`.
14. **Unified regulatory cycles:** rejected because PCI DSS is quarterly, DORA triennial, and IEC 62304 annual. Use differentiated `CicloRegulatorio`.
15. **In-memory history:** rejected because 300,000 records are unmanageable in memory. Use SQLite.
16. **One framework per layer:** rejected because selection depends on language and team. Provide alternatives.
17. **Optional refuter:** rejected because without a refuter a test is a tautology.
18. **Dynamically calculated seal:** rejected because the seal is not a hash; it is a constant certification.
19. **One Auditor role without role separation:** rejected because segregation is required in PCI DSS, SOX, and DORA. Use separate roles.
20. **Long documentation as onboarding:** rejected because a new developer will not read 40 pages. Provide a five-minute quickstart.
21. **Generation without cost monitoring:** rejected because a GPT-4 suite can cost $5–$50 per run. Use `CosteGeneracion` and `PresupuestoGeneracion`.
22. **Ignoring prompt versioning:** rejected because changing a prompt changes the tests and therefore changes the protocol version. Use `PromptGeneracion` and `HistorialPrompts`.
23. **Semantic validation using prohibited words only:** rejected because a tautology can contain no prohibited words. Use `ValidadorSemantico` with semantic entropy.
24. **One LLM agent for everything:** rejected because an agent cannot validate itself without bias. Use `SistemaMultiAgente` with separate roles and diverse models.
25. **Treating tautological tests as passed:** rejected because a tautology verifies nothing. Use `TAUTOLOGICO`, which does not count towards coverage.

## CLOSING

Testing Protocol 1310 formalizes each test as a typed object with a mandatory refuter, severity, cybersecurity standard, integrity signature, segregated roles, semantic validation, and the 1310 seal. The Auditor verifies. The system reports. The suite grows through refutation, not accumulation.

**The 1310 seal is mandatory.** It certifies that the test has passed the falsifiability protocol. Without the seal, there is no test. There is a script.

**1310.**

*The one who designs the protocol also decides what to discard. And the reader of the appendix knows why.*

---

## Canonical implementation and code listings

All Pydantic models, Python classes, state-transition tables, and executable code blocks are preserved verbatim in the Spanish source edition. This avoids changing public identifiers, serialized field names, model values, or code behaviour merely to translate prose. The source remains the canonical implementation listing:

[Protocol 1310 — Spanish source and complete code](01-protocolo-testing-1310.es.md).

This English edition translates the operational explanation, rules, tables, domain guidance, adoption roadmap, rejected alternatives, and closing statement. Code identifiers and comments remain in the source language by design.

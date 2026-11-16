# Replication and raw-artifact audit protocol
## Operational plan for the five tiny-model manuscripts

**Version:** 0.1  
**Prepared:** 16 November 2026  
**Status:** Protocol proposal; no new experiment is claimed by this document.

This protocol turns the outstanding evidence gaps in the five manuscripts into a reproducible audit sequence. Its purpose is not to manufacture a stronger result. It is to establish exactly which claims can be reproduced from immutable workflow records and raw artifacts, which remain descriptive, and which must be withdrawn or narrowed.

## 1. Evidence states

Every numerical claim should carry one of these states:

| State | Meaning | Permitted wording |
|---|---|---|
| S0 — reported | Present in a manuscript, curated note, or console excerpt only | “The run record reports…” |
| S1 — source-traced | Linked to a workflow run, exact workflow revision, and source file | “The workflow record reports…” |
| S2 — artifact-verified | Artifact identity and archive checksum independently match the platform record | “The archived artifact was verified…” |
| S3 — independently recomputed | Raw payload extracted and metrics recomputed by a versioned script | “We recomputed…” |
| S4 — contamination-audited | Training, validation, and holdout inputs checked for exact and near-duplicate exposure | “The evaluated prompts were not found in the audited training material…” |
| S5 — independently replicated | A separately executed run reproduces the finding under a declared protocol | “The result was replicated…” |

A claim must never be described using a higher state than its weakest material dependency. Artifact checksum verification (S2) does not establish that the contents are correct, uncontaminated, or scientifically meaningful.

## 2. Immutable run manifest

Create one machine-readable record per training or evaluation run. Preserve the raw source fields; do not overwrite missing values with estimates.

Required fields:

- repository, workflow run ID, job ID, workflow path, workflow commit SHA;
- run creation, start, and completion timestamps;
- conclusion at run and job level;
- runner label and available CPU/memory metadata;
- parent checkpoint artifact ID, filename, SHA-256, and cumulative step count;
- resulting checkpoint filename, SHA-256, cumulative step count, parameter count;
- model/configuration hash, tokenizer hash, corpus-manifest hash;
- optimizer, scheduler, precision, context length, batch size, accumulation;
- exact processed-token accounting and its definition;
- training, validation, and holdout split identifiers;
- evaluation prompt-set hash, scorer commit/blob SHA, inference-script blob SHA;
- decoding strategy, seed, thread counts, generation limits, stop conditions;
- artifact IDs, names, sizes, platform-reported digests, and locally recomputed digests;
- stage-level status: training, checkpoint integrity, lineage, evaluation, upload.

Use null for unavailable fields. Do not infer EOS from output length or infer a successful checkpoint from a green workflow alone.

## 3. Raw artifact handling

For each evaluation artifact:

1. Retrieve the artifact using its immutable artifact ID.
2. Record the platform metadata before downloading.
3. Compute SHA-256 over the downloaded ZIP bytes and compare it with the platform digest where available.
4. Preserve the original ZIP unchanged.
5. Extract into a clean, run-specific directory.
6. Inventory every file, byte size, and SHA-256.
7. Identify the exact prompt JSON, output JSON, scorer, tokenizer, and inference configuration.
8. Validate JSON syntax, expected row count, unique prompt IDs, and required fields.
9. Recompute every published metric from raw outputs using a versioned script.
10. Save a machine-readable audit report with the source hashes and script revision.

A verified archive checksum proves byte identity relative to the platform metadata; it does not prove the archive's internal semantic validity.

## 4. Metric definitions

Metrics must be defined before inspecting checkpoint differences.

### 4.1 Output-shape metrics

- **Empty output:** after the declared normalization, the generated answer contains no non-whitespace content.
- **Generation-cap hit:** the generation record contains exactly the configured maximum number of generated token IDs. Label this a cap hit, not an EOS failure, unless an explicit stop-reason field confirms it.
- **EOS emitted:** count only when the raw generation record or instrumented decoder explicitly records the EOS token as emitted.
- **Distinct output rate:** number of exact distinct normalized output strings divided by the number of evaluated prompts. This is lexical uniqueness, not semantic diversity or correctness.
- **Latency:** report the timing boundary, warm-up policy, hardware allocation, and whether tokenization/loading are included.
- **Repetition:** publish the exact algorithm, denominator, normalization, and per-response values. Do not report an aggregate without its unit.

### 4.2 Correctness metrics

Exact match, normalized exact match, rubric-based scoring, and semantic similarity are different measures. Report them separately. For generated answers with multiple valid forms, exact match should be treated as a narrow diagnostic rather than a general correctness measure.

For human or model-assisted adjudication, publish the rubric, annotator procedure, disagreement resolution, and blind status. Never silently replace a failed exact-match score with a semantic score.

### 4.3 Longitudinal comparisons

Compare checkpoints only when prompt set, tokenizer, inference script, decoding, generation limits, and scoring definitions are identical or when differences are explicitly modeled. Show raw numerators and denominators alongside percentages. Do not interpret a difference as causal when training data, schedule, architecture, or evaluation protocol also changed.

## 5. Holdout contamination audit

For every holdout prompt and reference answer:

1. Search the exact training corpus and all derived shards for exact byte/string matches.
2. Search normalized text after documented Unicode, whitespace, and punctuation normalization.
3. Run a declared near-duplicate procedure (for example, MinHash or SimHash) with its parameters and thresholds recorded.
4. Check source-document provenance and corpus inclusion manifests.
5. Search synthetic-data generators and seed/configuration files for prompt templates or answer leakage.
6. Record matches, candidate matches, false-positive review, and unresolved items.
7. Keep the holdout sealed after audit; do not feed its prompts or answers back into training.

“No match found” must be bounded to the audited files, normalizations, and thresholds. It is not proof of universal non-exposure.

## 6. Priority audit queue

### P0 — HERETIC-RONIN 512k-token evaluation

Known source: workflow run [42358300901](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42358300901), job 128361091415.

Outstanding work:
- inspect the downloaded archive and internal manifest;
- recover paired pre/post raw 120-response JSON;
- independently recompute normalized exact-match 0/120;
- verify all 120 prompt IDs, six domain labels, and row pairing;
- record empty, malformed, truncated, duplicate, and cap-hit outputs;
- confirm that the procedural generator and its references were not included in training;
- distinguish the 512,000-token chunk from the separate ~500M-parameter pilot.

Until complete, the safe statement is: the workflow source defines a 120-item procedural diagnostic and reports 0/120 normalized exact matches; independent raw-output recomputation and leakage audit remain pending.

### P1 — MINIRONIN 810k and 910k termination evaluations

Known sources: [810k run 42662696404](https://github.com/orbitalronin94/MINIRONIN/actions/runs/42662696404) and [910k run 42842506942](https://github.com/orbitalronin94/MINIRONIN/actions/runs/42842506942).

Outstanding work:
- recover both raw JSON artifacts and verify archive digests;
- identify the exact inference workflow revision and tokenizer for each;
- establish whether the output records contain token IDs or only decoded text;
- verify the 128-token cap count and whether EOS was explicitly recorded;
- recompute distinct outputs and latency from raw records;
- check whether both checkpoints used the same prompt set and decoding protocol.

Until explicit EOS evidence is available, phrase the result as “100/100 generations reached the reported 128-token cap; the recorded evaluation reports zero EOS emissions,” not as a fully instrumented stop-reason result.

### P2 — RONINIA five-checkpoint series

Known checkpoints: 100k, 137.5k, 205k, 250k, and 330k; source runs are indexed in `evidence-ledger.md` and `workflow-audit.csv`.

The artifact archives, shared prompt/tokenizer/script hashes, seed, and decoding configuration have already been audited at a substantial level. Remaining work:
- run exact and near-duplicate contamination checks against every training corpus revision;
- inspect raw per-response records for explicit stop reasons;
- replace the preliminary adjacent-bigram repetition estimates with a versioned, tested scorer;
- publish per-checkpoint metric confidence intervals only where the sampling design justifies them;
- avoid interpreting exact-string uniqueness as semantic diversity.

### P3 — CPU throughput comparison

The 2-thread and 4-thread RONIN-IA observations are hypothesis-generating only. Before causal claims:
- verify runner image and allocated hardware;
- recover full manifests and exact token accounting;
- establish that all configuration variables except thread count match;
- run randomized paired repetitions (at least three per setting where feasible);
- report median, range, and raw timings;
- separate data preparation, training, checkpointing, and evaluation time.

### P4 — Workflow lineage and recovery case studies

For every selected success/failure case, reconstruct the stage graph from the exact workflow revision. Report training completion, checkpoint integrity, lineage verification, evaluation, and artifact upload as independent states. Validate recovery by loading the recovered checkpoint and comparing its hash and cumulative-step metadata, not by relying on log text alone.

## 7. Manuscript-specific claim guardrails

- **Paper 1 — Loss–Behavior Gap:** show loss and behavioral metrics side by side; do not claim a statistical relationship until comparable paired observations exist.
- **Paper 2 — Longitudinal Change:** treat the five RONINIA checkpoints as a descriptive series; avoid causal or semantic claims from lexical metrics.
- **Paper 3 — CPU-Constrained Training:** do not generalize from one hosted-runner comparison; report configuration and timing boundaries.
- **Paper 4 — Checkpoint Lineage:** distinguish a failed workflow from a failed training run, but verify checkpoint integrity before calling it recoverable.
- **Paper 5 — Corpus Scale Is Not Learning:** define corpus units, token exposure, scorer semantics, and holdout isolation; do not equate 0/120 exact match with zero learning.

## 8. Release checklist

Before submission or public claims of a result:

- [ ] Every number maps to a run, artifact, and source revision.
- [ ] Raw artifacts are preserved and checksummed.
- [ ] Scoring scripts are versioned and independently rerun.
- [ ] Numerators, denominators, and metric definitions are published.
- [ ] Holdout contamination checks and their limits are documented.
- [ ] Checkpoint parentage and hashes are verified.
- [ ] Failures, missing artifacts, and exclusions are disclosed.
- [ ] The abstract uses only claims supported by the evidence state.
- [ ] Reproduction instructions work from a clean environment.

## 9. Interpretation principle

The object of study is not merely a model checkpoint. It is the complete experimental chain: data, tokenizer, optimization, checkpoint lineage, inference, scoring, and artifact preservation. A result is only as interpretable as the weakest unverified link in that chain.

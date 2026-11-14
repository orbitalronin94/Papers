# Tiny-model research programme

Five connected working manuscripts reconstruct a series of small-language-model experiments conducted in **MINIRONIN, RONIN-IA, HERETIC-RONIN, and RONINIA**. The programme studies not only model outputs, but also the engineering and measurement chain that makes those outputs interpretable: corpus construction, tokenization, training traces, checkpoint ancestry, inference settings, holdout scoring, and workflow recovery.

> **Publication status:** exploratory research drafts, not peer-reviewed papers. All numerical results in this directory are provisional unless explicitly marked otherwise and must be traced to their raw artifacts before submission.

## At a glance

| Manuscript | Main question | Principal evidence | Current maturity |
|---|---|---|---|
| [01 — The Loss–Behavior Gap](01-loss-behavior-gap.md) | Does optimization loss predict useful generation behavior? | MINIRONIN termination results; RONINIA checkpoint holdouts | Exploratory; raw holdout audit required |
| [02 — Longitudinal Behavioral Change](02-longitudinal-behavior.md) | How do observable behaviors change across checkpoints? | RONINIA 100k–250k; MINIRONIN 810k–910k | Descriptive series; comparability checks pending |
| [03 — CPU-Constrained Training](03-cpu-constrained-training.md) | What governs throughput on low-cost CPU runners? | RONIN-IA thread comparison; MINIRONIN and HERETIC performance records | Preliminary benchmark; controlled reruns needed |
| [04 — Checkpoint Lineage and Failure-Tolerant Experimentation](04-checkpoint-lineage.md) | How should partial success and artifact provenance be reported? | RONINIA and MINIRONIN post-training failures | Case-study evidence; workflow commit audit pending |
| [05 — Corpus Scale Is Not Learning](05-heretic-corpus-and-learning.md) | What does corpus size tell us about actual learning? | HERETIC corpus manifest, token budget, 0/120 holdout | Evidence incomplete; scoring and exposure audit required |

The five papers are related, but each has a distinct contribution. Paper 1 concerns measurement validity; paper 2 treats checkpoints as a longitudinal series; paper 3 concerns compute economics; paper 4 concerns experimental provenance; paper 5 concerns data exposure and the interpretation of negative results.

## Manuscripts

1. **[The Loss–Behavior Gap in Tiny Language Models](01-loss-behavior-gap.md)** — argues for reporting optimization metrics separately from externally measured generation outcomes. It examines cases where loss and visible behavior may diverge, without treating either as a proxy for general intelligence.
2. **[Longitudinal Behavioral Change Across Tiny Language-Model Checkpoints](02-longitudinal-behavior.md)** — tracks termination, empty outputs, cap hits, repetition, and response diversity across checkpoints. Its central methodological point is that a final checkpoint alone can conceal reversals and trade-offs.
3. **[CPU-Constrained Training of Small Language Models](03-cpu-constrained-training.md)** — documents measured throughput and the practical costs of data preparation, training, checkpointing, and evaluation on hosted CPU infrastructure.
4. **[Checkpoint Lineage and Failure-Tolerant Experimentation](04-checkpoint-lineage.md)** — separates successful optimization, valid checkpoint creation, artifact upload, provenance verification, and overall workflow status.
5. **[Corpus Scale Is Not Learning](05-heretic-corpus-and-learning.md)** — reconstructs HERETIC-RONIN corpus composition and token exposure, and asks what a negative holdout can and cannot establish.

## Current evidence snapshot

The following is a navigation-level summary of the extraction ledger, **not a final statistical analysis**. See the [evidence ledger](evidence-ledger.md) for run IDs, checkpoint hashes, provenance notes, and unresolved checks; see the [experiment matrix](experiment-matrix.csv) for machine-readable rows.

### RONINIA: checkpoint holdouts

Five official 100-response holdouts now provide a raw-artifact-backed descriptive series:

| Cumulative checkpoint | Empty outputs | Reached generation cap | Distinct responses |
|---:|---:|---:|---:|
| 100k | 1 | 22 | 100 |
| 137.5k | 0 | 42 | 96 |
| 205k | 14 | 29 | 83 |
| 250k | 2 | 45 | 96 |
| 330k | 1 | 21 | 99 |

The five ZIP artifacts were recovered and their archive SHA-256 values verified against GitHub's artifact API. The counts shown were recomputed from each raw JSON using one versioned script. A provenance audit of all five exact workflow revisions has verified the same 100-question prompt SHA-256, 8k tokenizer SHA-256, inference-script blob SHA, deterministic seed (20261110), greedy decoding, two CPU threads, 32-token/128-byte generation limits, and disabled KV cache/RAG. The 205k, 250k, and 330k workflows omit the limit flags but use the same script revision whose defaults match the earlier workflows. This establishes protocol consistency and supports the descriptive counts, but it does not establish answer correctness or freedom from training-data leakage. A response being distinct does not imply that it is correct, useful, or non-repetitive. The JSON does not record a stop reason or EOS event; exactly 32 generated token IDs is therefore reported as a token-limit hit, not as an EOS measurement.

The 250k training record reports 9,757,440 parameters, 920,277,537 processed tokens, validation loss 0.4032951621, and checkpoint SHA-256 `95d89f3030d3611c2dc5df26b83fc44b6c4ac3b924bc3a0862149952de4d3e38`. The run reached its target and produced artifacts, while a later lineage-verification stage failed. This is a key example for Paper 4: a post-training workflow error must not erase a recoverable checkpoint, nor should it be hidden.

### MINIRONIN: persistent termination limitation

The 810k and 910k holdout records each contain 100 responses, all reaching the reported 128-token cap, with zero EOS emissions. The recorded distinct-response counts were 98 and 91 respectively; mean latency was 0.288 s and 0.424 s. These are descriptive observations only until the raw outputs, exact inference settings, and scoring implementation are checked. They are useful because they show why step count and output diversity cannot substitute for an explicit termination metric.

### RONIN-IA: expansion screening and CPU measurements

A 10× expansion experiment was screened on 64 identical MMLU-Pro question IDs and recorded 5/64 both before and after training (7.8125%; zero percentage-point change). The record labels this screening-only and G0 FAIL; it is not evidence of a validated benchmark gain. Two performance records report 100.9M parameters and 500 updates: 383.24 s at 167.0 tokens/s with two inter-op threads, versus 505.14 s at 126.7 tokens/s with four. Runner identity and all other settings must be confirmed before interpreting the difference as a thread effect.

### HERETIC-RONIN: corpus and token-budget reconstruction

One extracted training chunk contains 512,000 tokens across 50 optimizer steps (10,240 tokens per optimizer step), with mean loss/token 2.268838; the first and last 100 recorded values average 2.349176 and 2.191886. The associated holdout is reported as 0/120, with 20 examples in each of six domains. The corpus snapshot records 256,237 documents after deduplication and 680,665,972 bytes. These figures do not, by themselves, establish the amount of unique token exposure or explain the holdout outcome. The exact rubric, raw outputs, tokenizer, training ancestry, and corpus-license manifest remain part of the audit.

## Evidence files

- **[Evidence ledger](evidence-ledger.md)** — source run links, extracted facts, hashes, caveats, and pending verification tasks.
- **[Experiment matrix](experiment-matrix.csv)** — tabular snapshot with run/job identity, checkpoint and corpus metadata, plus holdout artifact and protocol provenance.
- **[Recomputed RONINIA metrics](roninia-checkpoint-metrics.csv)** — five-checkpoint raw-JSON metrics, including archive and checkpoint hashes.
- **[Per-domain RONINIA metrics](roninia-domain-metrics.csv)** — 65 checkpoint-by-domain rows for empty outputs, token-limit hits, exact uniqueness, length, and latency.
- **[Reproducible scorer](../../scripts/score_roninia_holdouts.py)** — dependency-free script for JSON/ZIP input, common-protocol checks, descriptive metrics, and explicit EOS limitations.
- **Five manuscripts** — separate working papers linked above.

## Reading the evidence: status vocabulary

Use these labels consistently in the manuscripts and future additions:

- **Verified from source:** directly supported by an accessible run log, artifact manifest, source file, or immutable hash.
- **Extracted / provisional:** transcribed from a run or curated record but not yet independently recomputed from raw artifacts.
- **Derived:** calculated from source data using a documented formula and denominator.
- **Hypothesis:** a proposed explanation that has not been isolated experimentally.
- **Unknown / pending:** information not yet recovered or not comparable across runs.
- **Failed stage:** a workflow stage returned an error. This label describes pipeline execution, not automatically the training result or model quality.

Do not upgrade a claim's status merely because the same number appears in more than one draft. The ledger is the single working index for evidence provenance; the raw run and artifact remain the authority.

## Reproducibility and audit protocol

Before any result is promoted into a paper's main findings, record or recover:

1. **Identity:** repository, workflow run ID, job ID, workflow file path, workflow commit SHA, and execution date.
2. **Model:** architecture/configuration, parameter count, tokenizer identity and vocabulary, context length, optimizer, schedule, batch size, gradient accumulation, precision, and random seeds.
3. **Data:** corpus manifest and hash, source-level license/permission, deduplication procedure, filtering, split policy, token count, and actual token exposure.
4. **Lineage:** parent checkpoint, cumulative and incremental steps, parent and child hashes, and the code revision used to load and save them.
5. **Evaluation:** exact checkpoint hash, prompt-set version/hash, prompt IDs, decoding settings, generation cap, inference implementation, scorer version, denominator, and raw per-prompt outputs.
6. **Execution:** runner/CPU details, thread settings, elapsed time, tokens/s definition, data-loading and tokenization time, checkpoint time, and workflow exit status.
7. **Failure handling:** preserve logs and artifacts from failed or partially completed runs; state which stage failed and whether a usable checkpoint or evaluation artifact survived.

### Minimum behavioral metrics

Where raw generations are available, report at least:

- empty-output rate;
- EOS emission rate and explicit termination status;
- generation-cap hit rate;
- output length distribution (not just its mean);
- exact-match and normalized-match scores where a task has a defensible answer key;
- distinct-output rate, with the definition of “distinct” stated;
- repetition metrics with a documented tokenizer, window, denominator, and aggregation;
- latency distribution and the inference configuration.

Never collapse these into a single unqualified “quality” score. Correctness, fluency, termination, diversity, and latency are separate dimensions.

## Cross-paper dependencies

- **Paper 1** depends on the validity of the loss records and the behavioral scoring protocol developed across Papers 2 and 5.
- **Paper 2** depends on checkpoint lineage from Paper 4 and strict evaluation comparability.
- **Paper 3** depends on normalized throughput definitions and runner/configuration metadata.
- **Paper 4** supplies the provenance standard required by every other paper.
- **Paper 5** depends on corpus manifests, tokenizer accounting, data-split integrity, and a defensible interpretation of the 0/120 result.

Paper 4 is therefore the methodological backbone; Papers 1, 2, 3, and 5 are complementary empirical studies.

## Known limitations

- The experiments are heterogeneous: model families, tokenizers, corpus mixtures, parameter counts, training regimes, and evaluation procedures differ.
- Most current comparisons are observational, not randomized controlled experiments.
- Several holdout summaries have not yet been recalculated from raw JSON.
- Some workflow logs show successful checkpoint creation followed by metadata or lineage errors; final job status alone is an insufficient summary.
- A reported corpus byte count is not a token count, and a token count is not a measure of unique or useful information.
- A small fixed holdout can be noisy and can be contaminated by training data unless prompt provenance and corpus overlap are audited.
- Benchmark screening scores must not be described as general capability measurements, especially when the evaluation is small or explicitly marked screening-only.
- No result in this programme currently justifies claims of general intelligence, reasoning ability, or broad superiority.

## Work plan

The next research pass prioritizes evidence recovery over rhetorical expansion:

1. Recover the raw JSON for each RONINIA and MINIRONIN holdout and recompute all metrics with one versioned scorer.
2. Verify prompt-set identity, decoding configuration, tokenizer, inference code, and checkpoint SHA across each checkpoint comparison.
3. Recover workflow YAML and commit SHAs for the principal training and holdout runs.
4. Reconstruct HERETIC's corpus manifest, license records, tokenizer output, unique-token exposure, and exact 0/120 scoring rubric.
5. Normalize CPU benchmark metadata and distinguish model compute from end-to-end pipeline time.
6. Add all failed, cancelled, and partially successful runs to the ledger so the evidence is not selected only for favorable outcomes.
7. Revise the five manuscripts only when the underlying ledger changes; keep all unresolved claims visibly provisional.

## Citation and claim discipline

Every empirical sentence in a manuscript should point to a reproducible source: a run, job log, artifact, code revision, corpus manifest, or immutable checkpoint hash. Where the source is unavailable, write that the result is reported or pending verification. Do not infer missing values, silently repair inconsistent records, or turn a failed workflow into either a model failure or a success without inspecting the stage that failed.

The guiding principle is simple: **the experiment is the complete chain from data to scored output, not merely the training loop.**


## Latest evidence extraction: RONINIA protocol audit

A deeper inspection of all five holdout workflow files and the inference script at each exact workflow commit has established that the 100k, 137.5k, 205k, 250k, and 330k evaluations used the same immutable 100-question file and the same tokenizer. The inference script is byte-identical across all five workflow revisions. Its common protocol is deterministic greedy decoding, seed `20261110`, two CPU threads, a maximum of 32 generated tokens and 128 output bytes, with KV cache and RAG disabled.

The uploaded artifacts are also now individually catalogued by GitHub artifact ID, archive SHA-256, and byte size, alongside the workflow run, job, commit, and workflow filename. The 330k holdout is now included: its Actions job succeeded, its artifact was recovered, and its raw response metrics were recomputed. These identifiers are in the [evidence ledger](evidence-ledger.md) and [experiment matrix](experiment-matrix.csv).

This materially improves the checkpoint-series design: differences in the outputs are less likely to be explained by an intentional change in the inference protocol. The next decisive step is a corpus-overlap audit and a rubric-based correctness evaluation. The current JSON schema does not record EOS stop reasons, and the workflow does not calculate answer correctness.


### New checkpoint: 330k after interrupted-run recovery

The RONINIA history now extends beyond 250k. A 250k-to-300k continuation was cancelled after uploading a partial checkpoint chain. A separate recovery workflow selected the latest valid checkpoint from that artifact, checked that optimizer state was present, reused the existing token cache without retokenizing, verified the corpus fingerprint and tokenizer, and continued to exactly 330k. The recovery job and final checkpoint-chain upload succeeded.

An official 100-question holdout was then run against the 330k checkpoint. Its job completed successfully and uploaded an immutable artifact. The workflow verifies the same holdout and tokenizer hashes as the earlier checkpoint evaluations; the inference script and generation defaults also match. The 330k JSON was recovered and rescored: 1 empty response, 21 outputs reaching the 32-token limit, 99 exact-distinct strings, mean generated length 19.88 tokens, and mean latency 0.323478 seconds.

This recovery sequence is particularly relevant to Paper 4: the cancelled 300k attempt, recoverable intermediate artifacts, successful 330k continuation, and successful 330k holdout must be represented as separate events rather than compressed into a single “training succeeded” label.


### What the raw JSON adds

Across the five holdouts, mean generated length ranges from 19.03 to 23.13 tokens, while mean per-response latency ranges from 0.141405 to 0.374886 seconds. The latency variation should be treated as runner/runtime variation unless runner conditions are controlled. The holdout contains 35 CI/CD prompts and 25 personality/troll prompts; the remaining 40 prompts span 11 other domains. It is therefore a project-specific mixed test set, not a general reasoning benchmark.

The output files include answer text, token IDs, and elapsed time, but no explicit termination reason. The generation loop does not append EOS to the token list and may also stop at the 128-byte limit. EOS emission cannot be reconstructed reliably. Rubrics are included, but no automatic correctness scores are produced. The recomputed counts measure output shape and diversity only.


The shared holdout contains 35 CI/CD prompts and 25 personality/troll prompts; the remaining 40 prompts span 11 other domains. It is a project-specific mixed evaluation, not a general reasoning benchmark. The output records include rubrics but no correctness score, and they do not preserve an explicit termination reason. Accordingly, the current longitudinal metrics describe output shape and exact-text diversity, not correctness or EOS behavior.


## New extraction: workflow-level evidence

The current pass extends the papers beyond output metrics into the execution record. Job-step summaries were recovered for the HERETIC 512k-token chunk, both RONIN-IA expansion runs, the RONINIA 205k→250k continuation, and the RONINIA recovery to 330k.

Three details now matter for interpretation:

1. **HERETIC's corpus gates were executed.** The job completed the signed global corpus audit, training authorization and holdout-isolation checks, exact train-only corpus SHA verification, checkpoint/paired-holdout recovery, the 50-optimizer-step chunk, and resumable checkpoint/holdout upload. This supports the integrity of the recorded procedure, but it does not by itself validate the 0/120 scoring rubric or prove the holdout is absent from every historical source.
2. **RONINIA's 250k training completed despite a failed verification step.** The exact 45,000-step training step succeeded, recoverable checkpoints were uploaded, and the final checkpoint/lineage upload succeeded. The step named “Verify cumulative 205000 checkpoint and write lineage” failed; the overall run conclusion was failure. The paper now distinguishes this partial workflow failure from a failed training run.
3. **The 330k recovery was a clean, separate continuation.** The recovery job downloaded checkpoints from the interrupted run, selected a valid state, reused and verified the existing token cache unchanged, continued to exactly 330,000, verified the final checkpoint and lineage, and uploaded the chain successfully.

The two RONIN-IA expansion executions both completed all job steps, including source partition checks, six-source assembly, function-preserving expansion, 500 training steps, MMLU-Pro screening, and artifact upload. They are separate workflow executions with different head commits and artifact digests, but share the same experiment name, base checkpoint, corpus digest, and nominal configuration. Until seed and output-level independence are established, report them as repeated executions of one experiment specification—not as independent replications.

## Updated research priorities

- RONINIA: run a corpus/token-cache leakage audit against the shared 100-prompt holdout; extract the exact 250k parent and training trace; add correctness scoring with a blind, documented rubric.
- HERETIC: recover the raw paired 120-prompt JSON and scorer from the retained artifact (6.0 GB compressed); establish the meaning of 0/120 and distinguish the 512k-token chunk from the separate 500-update pilot record.
- RONIN-IA: compare the two expansion artifacts at the report/config/seed level; retrieve exact runner identity and benchmark manifests for the two-thread/four-thread CPU comparison.
- MINIRONIN: recover the two termination holdout JSONs and exact inference scripts; reconstruct the Mamba checkpoint metadata failure from structured artifacts.
- Cross-project: build a failure-stage catalog and avoid pooling metrics across incompatible tokenizers, prompt sets, model families, and decoding limits.

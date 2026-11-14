# Longitudinal Behavioral Change Across Tiny Language-Model Checkpoints
## A checkpoint-series analysis of termination, repetition, truncation, and response diversity

**Status:** Research draft v0.1 — exploratory  
**Primary system:** RONINIA (~9.76M parameters in the 250k checkpoint metadata)  
**Comparator:** MINIRONIN  
**Claim policy:** Descriptive longitudinal analysis; no anthropomorphic interpretation.

### Abstract (provisional)
This study examines how observable generation properties vary across checkpoints in a small language model trained through sequential continuation runs. Rather than treating a final checkpoint as the sole experimental outcome, it treats the checkpoint series as a longitudinal record. Preliminary RONINIA holdouts at 100k, 137.5k, 205k, 250k, and 330k steps show non-monotonic changes in empty outputs, generations reaching the output cap, and response diversity. MINIRONIN provides a contrasting case in which termination failure persists across 810k and 910k-step evaluations. The paper proposes a reproducible checkpoint-level measurement protocol and identifies the controls needed to distinguish genuine behavioral change from evaluation and lineage artifacts.

### 1. Research questions
- How do termination, truncation, repetition, and diversity evolve across checkpoints?
- Are there change points or reversals in these trajectories?
- Do training continuation boundaries correspond to behavioral discontinuities?
- Can apparent improvement in one metric coincide with deterioration in another?

### 2. RONINIA preliminary series
| Checkpoint | Empty outputs | 32-token limit hits | Exact-distinct responses | Mean tokens | Mean latency (s) |
|---:|---:|---:|---:|---:|---:|
| 100,000 | 1 | 22 | 100 | 21.18 | 0.319804 |
| 137,500 | 0 | 42 | 96 | 22.69 | 0.374886 |
| 205,000 | 14 | 29 | 83 | 19.03 | 0.141405 |
| 250,000 | 2 | 45 | 96 | 23.13 | 0.274788 |
| 330,000 | 1 | 21 | 99 | 19.88 | 0.323478 |

The five rows are recomputed from the raw JSON inside the official ZIP artifacts; the archive SHA-256 values were checked against GitHub's artifact API. All five workflow revisions use the same prompt-set hash, tokenizer hash, inference-script blob, seed, greedy decoding, two threads, 32-token/128-byte limits, and disabled KV cache/RAG. “Distinct response” means exact textual uniqueness, without semantic deduplication. The common prompt file's absence from each training corpus remains to be verified. Per-domain counts and metrics are published in `roninia-domain-metrics.csv`.

The 205k and 250k evaluations also yielded preliminary adjacent-bigram repetition estimates of 0.96 and 1.83 per response respectively. The denominator and implementation require verification.

The 205k checkpoint's 14 empty outputs are distributed across calibration (1), CI/CD (5), contradiction (2), knowledge (1), logic (1), personality/troll (3), and reasoning (1). At 330k, the single empty response is in personality/troll. This localization is descriptive only: most domains contain just 2–6 prompts, so per-domain rates are unstable. CI/CD and personality/troll have larger denominators (35 and 25) and account for most token-limit hits across checkpoints.

### 3. MINIRONIN comparator
The 810k and 910k holdouts both report 100/100 outputs at the 128-token cap and 0/100 EOS emissions. The recorded mean latency changes from about 0.288 s to 0.424 s, while distinct outputs change from 98 to 91. The comparison is not controlled for all possible inference/runtime variables and must be presented as a case observation, not a causal effect of 100k additional steps.

### 4. Study design
Construct a checkpoint panel. Each row is one checkpoint × prompt set × decoding configuration. Do not merge evaluations with different prompt hashes or decoding settings.

For each checkpoint:
1. Verify lineage and checkpoint SHA-256.
2. Verify tokenizer and inference-code identity.
3. Run the same fixed prompt set under deterministic decoding.
4. Store raw output and token-level termination metadata.
5. Compute all metrics from raw outputs.
6. Repeat selected checkpoints to estimate runtime/inference nondeterminism.

Primary outcomes: empty-output rate, explicit stop-reason rate (when logged), token/byte-limit hit rates, exact and normalized unique-output rates, repeated n-gram rate. EOS rate is unavailable in the current RONINIA output schema. Secondary outcomes: response length, latency percentiles, exact-match or rubric-based task scores where suitable.

### 5. Analysis plan
- Plot each metric against cumulative optimizer steps.
- Show raw counts alongside rates and denominators.
- Use paired prompt-level transitions between adjacent checkpoints.
- Bootstrap over prompts for uncertainty intervals.
- Use change-point analysis only if the number and spacing of checkpoints justify it.
- Correct for multiple comparisons if many metrics/checkpoints are tested.
- Report all checkpoints, not only favorable segments.

### 6. Interpretation boundaries
A higher unique-output rate is not necessarily better; it may reflect instability or incoherence. A lower cap-hit rate may indicate better stopping or merely shorter generations. EOS emission is a formatting/termination property, not a direct measure of semantic competence. These metrics must not be combined into an unvalidated “intelligence” score.

### 7. Limitations and required evidence
- Raw JSON and archive hashes are now verified for the five RONINIA checkpoints; retain this scorer and artifact inventory.
- Recover the full 5k–330k checkpoint sequence, not just selected points; extract the 330k JSON and rescore all five holdouts.
- Audit prompt-set overlap with training data and earlier holdouts; the shared 100-question set includes 35 CI/CD and 25 personality/troll prompts, so it is a project-specific mixed holdout rather than a general reasoning benchmark.
- Re-run a subset with a common inference binary and tokenizer.
- Recover training logs, validation traces, and run configuration for every checkpoint.
- Document failed and missing evaluations.

### 8. Planned artifacts
The raw-JSON metric table is available in `roninia-checkpoint-metrics.csv`; the 65-row per-domain table is `roninia-domain-metrics.csv`; the reproducible scorer is `scripts/score_roninia_holdouts.py`. Remaining artifacts: `checkpoint_panel.csv`, `prompt_level_transitions.csv`, `metrics_definition.md`, `plot_longitudinal_metrics.py`, and immutable artifact manifest.

### References to add
Longitudinal evaluation, reliability of NLP benchmarks, bootstrap methods, and measurement theory. Cite exact repository runs and artifacts after re-audit.


### 9. Stop-reason and holdout-composition caveats

The current output schema stores generated token IDs and decoded answers but not a termination enum. The inference loop stops when EOS is predicted without appending EOS to the generated list; it can also stop when the next token would exceed 128 UTF-8 bytes. Therefore, this paper reports exact 32-token-limit hits, not EOS emissions. A byte-limit stop cannot be distinguished reliably from EOS from the stored JSON alone.

The common holdout is not domain-balanced: 35/100 prompts are labelled `ci_cd`, 25/100 `personality_troll`, and 40/100 span 11 other domains. Aggregate distinctness is sensitive to this mixture. Future reporting should include per-domain metrics and avoid interpreting the aggregate as general reasoning ability. No correctness score has yet been computed from the included rubrics.

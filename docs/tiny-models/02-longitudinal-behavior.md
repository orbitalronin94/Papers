# Longitudinal Behavioral Change Across Tiny Language-Model Checkpoints
## A checkpoint-series analysis of termination, repetition, truncation, and response diversity

**Status:** Research draft v0.1 — exploratory  
**Primary system:** RONINIA (~9.76M parameters in the 250k checkpoint metadata)  
**Comparator:** MINIRONIN  
**Claim policy:** Descriptive longitudinal analysis; no anthropomorphic interpretation.

### Abstract (provisional)
This study examines how observable generation properties vary across checkpoints in a small language model trained through sequential continuation runs. Rather than treating a final checkpoint as the sole experimental outcome, it treats the checkpoint series as a longitudinal record. Preliminary RONINIA holdouts at 100k, 137.5k, 205k, and 250k steps show non-monotonic changes in empty outputs, generations reaching the output cap, and response diversity. MINIRONIN provides a contrasting case in which termination failure persists across 810k and 910k-step evaluations. The paper proposes a reproducible checkpoint-level measurement protocol and identifies the controls needed to distinguish genuine behavioral change from evaluation and lineage artifacts.

### 1. Research questions
- How do termination, truncation, repetition, and diversity evolve across checkpoints?
- Are there change points or reversals in these trajectories?
- Do training continuation boundaries correspond to behavioral discontinuities?
- Can apparent improvement in one metric coincide with deterioration in another?

### 2. RONINIA preliminary series
| Checkpoint | Empty outputs | Cap-reaching outputs | Distinct responses |
|---:|---:|---:|---:|
| 100,000 | 1 | 22 | 100 |
| 137,500 | 0 | 42 | 96 |
| 205,000 | 14 | 29 | 83 |
| 250,000 | 2 | 45 | 96 |

These counts are preliminary extractions from 100-response holdouts. They must be recomputed from the raw JSON and tied to exact checkpoint hashes before use as final results. “Distinct response” currently means textual uniqueness; normalization rules must be specified.

The 205k and 250k evaluations also yielded preliminary adjacent-bigram repetition estimates of 0.96 and 1.83 per response respectively. The denominator and implementation require verification.

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

Primary outcomes: EOS rate, empty-output rate, cap-hit rate, normalized unique-output rate, repeated n-gram rate. Secondary outcomes: response length, latency percentiles, exact-match or rubric-based task scores where suitable.

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
- Verify all raw JSON files and their SHA-256 hashes.
- Recover the full 5k–250k checkpoint sequence, not just four selected points.
- Audit prompt-set overlap with training data and earlier holdouts.
- Re-run a subset with a common inference binary and tokenizer.
- Recover training logs, validation traces, and run configuration for every checkpoint.
- Document failed and missing evaluations.

### 8. Planned artifacts
`checkpoint_panel.csv`, `prompt_level_transitions.csv`, `metrics_definition.md`, `plot_longitudinal_metrics.py`, and immutable artifact manifest.

### References to add
Longitudinal evaluation, reliability of NLP benchmarks, bootstrap methods, and measurement theory. Cite exact repository runs and artifacts after re-audit.

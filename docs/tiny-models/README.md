# Tiny-model research programme

Five connected manuscripts are being developed from the MINIRONIN, RONIN-IA, HERETIC-RONIN, and RONINIA experiment histories. These are working drafts, not peer-reviewed publications.

## Manuscripts

1. [The Loss–Behavior Gap in Tiny Language Models](01-loss-behavior-gap.md) — training objectives versus externally measured generation behavior.
2. [Longitudinal Behavioral Change Across Tiny Language-Model Checkpoints](02-longitudinal-behavior.md) — checkpoint-level termination, repetition, truncation, and diversity.
3. [CPU-Constrained Training of Small Language Models](03-cpu-constrained-training.md) — throughput, parallelism, and workflow costs.
4. [Checkpoint Lineage and Failure-Tolerant Experimentation](04-checkpoint-lineage.md) — provenance, artifact integrity, and partial recovery.
5. [Corpus Scale Is Not Learning](05-heretic-corpus-and-learning.md) — HERETIC corpus composition, token budgets, and holdout outcomes.

## Evidence and status

- [Evidence ledger](evidence-ledger.md) records the currently extracted runs and the remaining verification work.
- Metrics labelled preliminary must be recomputed from raw artifacts before submission.
- No paper should claim causal effects from heterogeneous observational runs.
- Negative results are retained; failed jobs are not silently omitted.
- Every reported score must define its task, denominator, scorer, prompt-set identity, and checkpoint lineage.

## Working conventions

- Separate verified facts, derived metrics, hypotheses, and unknowns.
- Prefer immutable run IDs, artifact IDs, checkpoint hashes, and corpus hashes to mutable branch links.
- Keep raw generations and per-prompt scores whenever licensing and storage permit.
- Distinguish training loss, validation loss, and task-specific holdout performance.
- Do not equate diversity, EOS emission, or low loss with general intelligence.

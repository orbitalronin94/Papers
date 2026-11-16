# RONINIA holdout metrics: definitions and stop semantics

**Status:** source-audited metric dictionary; contamination status remains unresolved.  
**Scope:** the five recovered RONINIA 100-response evaluations at 100k, 137.5k, 205k, 250k, and 330k steps.

This note defines what the published descriptive columns mean. It deliberately separates directly observable output properties from hidden generation events and task correctness.

## Evaluation loop

The audited evaluator is `RONINIA/scripts/checkpoint_holdout.py` (blob `b83ceb712431b3ea20902708fb9ec8f3c243425a`). Its greedy generation loop runs for at most 32 iterations. On each iteration it:

1. predicts the next token with argmax;
2. stops immediately if the predicted ID is EOS, without appending it;
3. decodes the candidate token and stops if appending its UTF-8 bytes would exceed 128 bytes;
4. otherwise appends the token ID and bytes.

The output JSON stores appended token IDs, decoded answer text, and elapsed time. It does not store a stop-reason enum, a count of EOS predictions, or the byte-limit event.

## Metric dictionary

| Field | Operational definition | What it does not mean |
|---|---|---|
| `holdout_n` | Number of result rows; expected 100 | Benchmark breadth or representativeness |
| `empty_outputs` | Count whose decoded answer is empty after whitespace stripping | A failure category with known cause |
| `token_limit_hits_32` | Count with exactly 32 appended generated token IDs | EOS rate, semantic truncation, or general quality |
| `distinct_exact_answers` | Number of distinct answer strings under exact string equality | Semantic diversity, correctness, or usefulness |
| `mean_generated_tokens` | Arithmetic mean of appended token-ID counts | Model tokenization efficiency across other tokenizers |
| `mean_output_bytes` | Mean UTF-8 byte length of decoded answer strings | Number of characters or tokens |
| `mean_latency_seconds` | Arithmetic mean of per-prompt elapsed seconds | Stable hardware-independent throughput |
| `p50_latency_seconds` | Median per-prompt elapsed seconds | Tail latency |
| `p90_latency_seconds_nearest_rank` | Sorted latency at rank ceil(0.90 × n), one-indexed | A parametric confidence interval |
| `eos_emissions` | Unavailable; left blank/null in the CSV | Zero EOS events |

### Interpreting the 32-token count

Exactly 32 appended token IDs means all 32 loop iterations appended a token and the token-count loop was exhausted. It is therefore valid to call this an **exact 32-token-loop exhaustion**.

For outputs shorter than 32 tokens, the stored JSON cannot distinguish EOS termination from the 128-byte guard. It is invalid to infer EOS from a short answer or to infer its absence from a 32-token output. The current evaluator should be amended in future runs to store at least:

- `stop_reason`: `eos`, `max_new_tokens`, `max_new_bytes`, or `error`;
- `eos_predicted`: boolean;
- `generated_token_count` and `generated_utf8_bytes`;
- optionally the final candidate token ID when stopped by a byte guard.

Historical EOS counts cannot be reconstructed from the existing JSON.

## Current five-checkpoint descriptive values

| Steps | Empty | Exact 32-token-loop exhaustion | Exact-distinct answers |
|---:|---:|---:|---:|
| 100,000 | 1 | 22 | 100 |
| 137,500 | 0 | 42 | 96 |
| 205,000 | 14 | 29 | 83 |
| 250,000 | 2 | 45 | 96 |
| 330,000 | 1 | 21 | 99 |

All denominators are 100. The rows are repeated evaluations of the same fixed prompt set and generation protocol, not five independent benchmark samples. These are descriptive counts, not correctness scores.

## Holdout-separation status

The evaluation workflows verify the benchmark file SHA-256. That confirms the identity of the file evaluated, not its absence from training. The audited RONINIA token-cache preparation run 42890884432 applies scripts/prepare_corpus.py (blob `1e63690abd1be96a6974760dcb329234054ae510`) to the source corpus before tokenization. Its filter excludes selected path/metadata values but does not explicitly denylist the benchmark hash or prompt IDs; its exclusion vocabulary does not include `inference_only`. The later training continuation consumes this cache. No contamination finding is asserted. Raw corpus and source-shard scans remain required before holdout independence can be claimed.

See [the evidence ledger](evidence-ledger.md), [the replication and audit protocol](replication-and-audit-protocol.md), and [the longitudinal manuscript](02-longitudinal-behavior.md).

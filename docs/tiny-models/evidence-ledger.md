# Evidence ledger — tiny-model research programme

**Snapshot:** 14 November 2026  
**Status:** Active extraction; not a final dataset.  
**Repositories:** MINIRONIN, RONIN-IA, HERETIC-RONIN, RONINIA.

This ledger preserves source identifiers and the narrowest claim supported by the retrieved records. Figures remain provisional until raw artifacts, scoring scripts, and exact workflow commits have been cross-checked.

## A. RONINIA checkpoint holdouts

| Cumulative checkpoint | Empty outputs | At generation cap | Distinct responses | Source |
|---:|---:|---:|---:|---|
| 100k | 1 | 22 | 100 | [Run 43112010343](https://github.com/orbitalronin94/RONINIA/actions/runs/43112010343) |
| 137.5k | 0 | 42 | 96 | [Run 43166483341](https://github.com/orbitalronin94/RONINIA/actions/runs/43166483341) |
| 205k | 14 | 29 | 83 | [Run 43309180308](https://github.com/orbitalronin94/RONINIA/actions/runs/43309180308) |
| 250k | 2 | 45 | 96 | [Run 43378296219](https://github.com/orbitalronin94/RONINIA/actions/runs/43378296219) |

Each evaluation is reported as a 100-response holdout. Recompute from raw JSON before publication. Confirm identical prompt-set hashes, generation cap, tokenizer, decoding parameters, checkpoint hashes, and inference implementation. A preliminary adjacent-bigram repetition estimate for 205k/250k was 0.96/1.83 per response; its denominator and scorer still require audit.

The 250k checkpoint metadata recorded 9,757,440 parameters, 920,277,537 processed tokens, validation loss 0.4032951621, and checkpoint SHA-256 `95d89f3030d3611c2dc5df26b83fc44b6c4ac3b924bc3a0862149952de4d3e38`. Source training run: [43315959342](https://github.com/orbitalronin94/RONINIA/actions/runs/43315959342). That workflow reached 250k and uploaded the official holdout artifact, but its later lineage-verification stage failed with `AttributeError: 'NoneType' object has no attribute 'group'`.

## B. MINIRONIN termination behavior

| Checkpoint | Prompts | At 128-token cap | EOS emitted | Mean latency | Distinct responses |
|---:|---:|---:|---:|---:|---:|
| 810k | 100 | 100 | 0 | 0.288 s | 98 |
| 910k | 100 | 100 | 0 | 0.424 s | 91 |

Sources: [810k run 42662696404](https://github.com/orbitalronin94/MINIRONIN/actions/runs/42662696404); [910k run 42842506942](https://github.com/orbitalronin94/MINIRONIN/actions/runs/42842506942). Verify raw JSON and exact inference settings. The observations support persistent termination failure in these two evaluations, not a causal claim about additional training.

## C. RONIN-IA 10× expansion screening

Two workflow records, [42364113096](https://github.com/orbitalronin94/RONIN-IA/actions/runs/42364113096) and [42364138735](https://github.com/orbitalronin94/RONIN-IA/actions/runs/42364138735), identify the experiment `ronin-expand-10x-from-winning-10k-v1`.

Recorded values:
- Base checkpoint: 10,000 steps; SHA-256 `7a7fe93350b72ebc8d645900c2ae8be455a60334e04ac95176e09bab72f981ed`.
- Target parameter count: 100,900,160.
- Training: 500 steps.
- Corpus: 685,023,414 bytes; SHA-256 `0d92e66ee96931299b97da7bbbb47f3312b3333bcd081a355422ed0230960af7`.
- MMLU-Pro screening: 64 identical question IDs, 5/64 before and 5/64 after (7.8125%; 0.0 percentage-point change).
- Functional preservation before training passed; maximum absolute logit delta 1.430511474609375e-06.
- Report labels: SCREENING_ONLY; automatic promotion false; global G0 FAIL; benchmark holdout contamination PENDING.

Do not call these independent replications until run metadata and exact output files establish independence. Do not treat the screening score as a comprehensive benchmark result.

## D. HERETIC-RONIN 512k-token chunk

Source: [workflow run 42358300901](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42358300901), job 128361091415.

Recorded chunk:
- Micro-steps 2,600–4,600; 2,000 micro-steps.
- 50 optimizer steps; accumulation 40; micro-batch 2 sequences.
- Context 128; 10,240 tokens per optimizer step; 512,000 tokens in chunk.
- Mean loss/token 2.268838; first 100 mean 2.349176; last 100 mean 2.191886.
- Holdout before and after: 0/120, 20 items in each of six domains (mathematics, programming, logic, natural science, language, interdisciplinary).
- Corpus: 256,305 audited documents before deduplication; 68 duplicate records excluded; 256,237 after deduplication.
- Total bytes: 680,665,972.
- Sources: CoVoST2 CC0 (translation-only), Mathlib4 Apache-2.0, ScienceVerse per-document CC-BY/CC0, Spanish public-domain literature, one NASA NTRS item, nine owner-authorized Papers documents.
- Explicitly excluded: validation/test/holdout, 20,000 unreviewed open-source candidates, Drosophila procedural synthetic rows, and exact/SimHash near-duplicate endpoints in the signed audit plan.
- Elapsed time 17,105.51 s; checkpoint SHA-256 `c81edf6658ed208cf4848c831336d427df4464eb725d158fdf827b99910ba5a2`.

The holdout's 0/120 is meaningful only relative to its exact scoring rubric. Recover the raw outputs and scorer before interpreting it as task failure or general capability.

## E. CPU / throughput records

Source: curated engineering record in MINIRONIN, `data/curated/minironin-performance-engineering-v1.jsonl`.

| Experiment | Parameters | Updates | Wall time | Throughput |
|---|---:|---:|---:|---:|
| RONIN-IA, 2 inter-op threads | 100.9M | 500 | 383.24 s | 167.0 tokens/s |
| RONIN-IA, 4 inter-op threads | 100.9M | 500 | 505.14 s | 126.7 tokens/s |
| MINIRONIN Mamba | 49.1M | 1,000 | 1,166.33 s | 54.9 tokens/s |
| HERETIC pilot | ~500M | 50 | 13,096.33 s | 39.1 tokens/s |

The thread comparison is hypothesis-generating. Retrieve the exact manifests and repeat paired runs before causal interpretation. The HERETIC pilot and 512k-token chunk are distinct records and must not be conflated.

## F. Additional MINIRONIN Mamba continuation

A workflow log in [run 42475009211](https://github.com/orbitalronin94/MINIRONIN/actions/runs/42475009211) records cumulative steps 1,000–2,000, 1,000 additional optimizer steps, 1,166.33 s, and a step-2,000 checkpoint with SHA-256 `4015cf070de7ca58cc3302fa80754308c86ecfc736b78a52eda267dbb441b364`. Mean loss over the final 50 steps was 1.9871. The later workflow stage failed with `KeyError: 'index_sha256'`. Treat checkpoint completion and workflow status separately.

## G. Cross-cutting infrastructure observations

RONIN-IA and HERETIC-RONIN logs include Node.js DEP0005 warnings for deprecated `Buffer()` usage. These are action/runtime warnings, not evidence of a model-training defect. RONINIA's regex-related AttributeError and MINIRONIN's missing `index_sha256` KeyError are separate post-training metadata failures.

## H. Highest-priority missing evidence

1. Raw JSON and scorer code for all RONINIA 100-response holdouts.
2. Prompt-set hashes and leakage audit for all fixed holdouts.
3. Exact workflow YAML/commit for RONINIA 250k and its failed lineage stage.
4. Raw HERETIC 120-prompt holdout, scoring rubric, and full corpus manifest.
5. Original RONIN-IA thread benchmark manifests and runner metadata.
6. Complete RONIN-IA and HERETIC training traces, not only terminal summaries.
7. RONIN-IA expansion workflow independence: determine whether the two run records are separate replications or repeated execution of one experiment design.
8. Full checkpoint series between RONINIA 5k and 250k, including failed or missing evaluations.

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

Each evaluation is a 100-response holdout. A follow-up audit of all four workflow files and the inference script found a common prompt-set SHA-256, tokenizer SHA-256, inference-script blob SHA, deterministic seed, greedy decoding, and matching generation limits across the four checkpoints (details in Section I). This substantially strengthens protocol comparability. It does not validate the preliminary behavioral counts: recompute those from the raw JSON, audit the scoring definitions, and verify that the holdout was excluded from every training corpus. A preliminary adjacent-bigram repetition estimate for 205k/250k was 0.96/1.83 per response; its denominator and scorer still require audit.

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


## I. RONINIA official holdout provenance audit (new)

The four official holdout workflows were inspected at their exact workflow-head commits, and the referenced `scripts/checkpoint_holdout.py` file was fetched at each commit. The script blob SHA is identical in all four cases: `b83ceb712431b3ea20902708fb9ec8f3c243425a`.

### Shared evaluation protocol

| Field | Verified value |
|---|---|
| Prompt set | 100 questions; SHA-256 `3cd8c1eb3142ebf9c6cc17d2e19353be3472d61ac7b7cfb6de0cbb233cf4a535` |
| Tokenizer | 8k tokenizer; SHA-256 `605834d0d1deea545518be54ae0936060845107b906172f6628d0ff9520e57a4` |
| Inference script blob | `b83ceb712431b3ea20902708fb9ec8f3c243425a` |
| Random seed | `20261110` (Python, NumPy, and PyTorch) |
| Determinism | `torch.use_deterministic_algorithms(True)` |
| Decoding | Greedy argmax |
| CPU threads | 2 |
| Generation limit | 32 new tokens and 128 UTF-8 bytes |
| KV cache | Disabled |
| RAG | Disabled |
| Prompt wrapper | Same Spanish instruction prefix and `Respuesta:` suffix |

The 100k and 137.5k workflow files pass these generation limits explicitly. The 205k and 250k files omit those command-line flags, but their exact checked-out inference script has the same defaults (2 threads, 32 tokens, 128 bytes). The four workflows therefore converge on the same generation settings. This is stronger than assuming comparability from the run labels alone.

### Per-run immutable workflow and artifact records

| Checkpoint | Run / job | Workflow head commit | Workflow file | Artifact ID | Artifact size | Artifact archive SHA-256 |
|---:|---|---|---|---:|---:|---|
| 100k | [43112010343](https://github.com/orbitalronin94/RONINIA/actions/runs/43112010343) / 130830212601 | `01db5d205b0e24b492d76873c3cba7c28f571b9e` | `checkpoint-holdout-ronin-10m-100000.yml` | 13897325999 | 26,054 B | `799d5d7189e725c44afead7975a56ad1f2d9b2ae429f41924f9501b50e989868` |
| 137.5k | [43166483341](https://github.com/orbitalronin94/RONINIA/actions/runs/43166483341) / 131009439575 | `bc0a4fd6c7cc0aa0892559b31ac7cde9dfc03e3d` | `checkpoint-holdout-ronin-10m-137500.yml` | 13920058028 | 25,368 B | `f10b8d4f112f2598cd0851e2526ae71e785d145c95423fc39e372f9d94aeef5f` |
| 205k | [43309180308](https://github.com/orbitalronin94/RONINIA/actions/runs/43309180308) / 131500398462 | `62da7623310ec019a1c20e25685b5c4746ec84e9` | `official-holdout-205000.yml` | 13984838040 | 24,897 B | `df6db70c4971315e1a035dae28b61320c41f57a942f570fd94b9875561ad0127` |
| 250k | [43378296219](https://github.com/orbitalronin94/RONINIA/actions/runs/43378296219) / 131729865487 | `e6955017eebb58541f1429fa691c80bcd31e7392` | `official-holdout-250000.yml` | 14015746116 | 25,826 B | `47135395843ab0a0736aa9aabd6a58689ebea8bafbcfbdd5c8fa71c464bf9d3c` |

All four jobs are recorded by the Actions API as completed with conclusion `success`; each uploaded one non-expired holdout artifact. The artifact digests above are GitHub's archive-level SHA-256 values, not hashes of the JSON file inside each archive. Artifact IDs, archive digests, sizes, and run/job IDs make the uploaded packages individually identifiable.

### Checkpoint identity recovered from the workflow definitions

- 137.5k checkpoint SHA-256: `d2c30940ade76e82bc5e7569c96af6ac4337173d141f627410eb40847e245727`.
- 205k checkpoint SHA-256: `425b9a0939a1b387420061450a99728718eb2640dea3c05fd1692d9ea8a24fa9`.
- 250k checkpoint SHA-256: `95d89f3030d3611c2dc5df26b83fc44b6c4ac3b924bc3a0862149952de4d3e38`.
- 100k workflow verifies the exact checkpoint and writes its SHA into the output JSON; the value still needs to be extracted from the retained artifact.

### What this audit does and does not establish

It establishes a common prompt-file hash, tokenizer hash, inference-script blob, and generation protocol across the four holdouts. It does **not** establish that the holdout was never included in any training corpus, that the current preliminary empty/cap/distinct counts are correct, or that the model answers are accurate. The JSON artifacts must still be retrieved and scored with an audited script. The workflows include rubrics in the output records but do not calculate a correctness score.

The source benchmark is stored in MINIRONIN at `benchmarks/inference-holdout-v1.jsonl` and each RONINIA workflow downloads that exact file by URL and verifies its SHA-256. The next leakage audit must compare the 100 question IDs and normalized text against every corpus manifest and any synthetic-data generation source used in the relevant RONINIA training lineage.

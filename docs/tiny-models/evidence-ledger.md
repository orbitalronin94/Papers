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
| 330k | 1 | 21 | 99 | [Run 43490561981](https://github.com/orbitalronin94/RONINIA/actions/runs/43490561981) |

Each evaluation is a 100-response holdout. A follow-up audit of all four workflow files and the inference script found a common prompt-set SHA-256, tokenizer SHA-256, inference-script blob SHA, deterministic seed, greedy decoding, and matching generation limits across the five checkpoints (details in Section I). This substantially strengthens protocol comparability. The recomputed descriptive counts are now in Section K. They are not correctness scores; the output schema does not record the exact stop reason, and the holdout's exclusion from every training corpus still requires a leakage audit. A preliminary adjacent-bigram repetition estimate for 205k/250k was 0.96/1.83 per response; its denominator and scorer still require audit.

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

Completed in this extraction pass: all five RONINIA official holdout ZIPs and raw JSONs recovered; archive digests verified; a common-protocol scorer and aggregate/domain metrics committed; exact workflow commits and shared prompt/tokenizer hashes recorded; 330k recovery and holdout chain reconstructed.

Remaining priorities:
1. Prompt-set overlap and leakage audit against every RONINIA training corpus, token cache, and synthetic-data source.
2. Exact workflow YAML and logs for the 250k training run's regex-related lineage failure.
3. Raw HERETIC 120-prompt holdout, scoring rubric, and full corpus manifest.
4. Original RONIN-IA thread benchmark manifests and runner metadata.
5. Complete RONIN-IA and HERETIC training traces, not only terminal summaries.
6. RONIN-IA expansion workflow independence: determine whether the two run records are separate replications or repeated execution of one experiment design.
7. Full checkpoint series between RONINIA 5k and 330k, including failed, cancelled, or missing evaluations.


## I. RONINIA official holdout provenance audit (new)

The five official holdout workflows were inspected at their exact workflow-head commits, and the referenced `scripts/checkpoint_holdout.py` file was fetched at each commit. The script blob SHA is identical in all four cases: `b83ceb712431b3ea20902708fb9ec8f3c243425a`.

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

The 100k and 137.5k workflow files pass these generation limits explicitly. The 205k, 250k, and 330k files omit those command-line flags, but their exact checked-out inference script has the same defaults (2 threads, 32 tokens, 128 bytes). All five workflows therefore converge on the same generation settings. This is stronger than assuming comparability from the run labels alone.

### Per-run immutable workflow and artifact records

| Checkpoint | Run / job | Workflow head commit | Workflow file | Artifact ID | Artifact size | Artifact archive SHA-256 |
|---:|---|---|---|---:|---:|---|
| 100k | [43112010343](https://github.com/orbitalronin94/RONINIA/actions/runs/43112010343) / 130830212601 | `01db5d205b0e24b492d76873c3cba7c28f571b9e` | `checkpoint-holdout-ronin-10m-100000.yml` | 13897325999 | 26,054 B | `799d5d7189e725c44afead7975a56ad1f2d9b2ae429f41924f9501b50e989868` |
| 137.5k | [43166483341](https://github.com/orbitalronin94/RONINIA/actions/runs/43166483341) / 131009439575 | `bc0a4fd6c7cc0aa0892559b31ac7cde9dfc03e3d` | `checkpoint-holdout-ronin-10m-137500.yml` | 13920058028 | 25,368 B | `f10b8d4f112f2598cd0851e2526ae71e785d145c95423fc39e372f9d94aeef5f` |
| 205k | [43309180308](https://github.com/orbitalronin94/RONINIA/actions/runs/43309180308) / 131500398462 | `62da7623310ec019a1c20e25685b5c4746ec84e9` | `official-holdout-205000.yml` | 13984838040 | 24,897 B | `df6db70c4971315e1a035dae28b61320c41f57a942f570fd94b9875561ad0127` |
| 250k | [43378296219](https://github.com/orbitalronin94/RONINIA/actions/runs/43378296219) / 131729865487 | `e6955017eebb58541f1429fa691c80bcd31e7392` | `official-holdout-250000.yml` | 14015746116 | 25,826 B | `47135395843ab0a0736aa9aabd6a58689ebea8bafbcfbdd5c8fa71c464bf9d3c` |
| 330k | [43490561981](https://github.com/orbitalronin94/RONINIA/actions/runs/43490561981) / 132110319633 | `11b1d25b7755d5efd745d4eda00b7d9f36129cda` | `official-holdout-330000.yml` | 14068589478 | 25,444 B | `fb3106d6cb698321e363eb9c7ba88f155203062494270d4b99a4127498d220b8` |

All five jobs are recorded by the Actions API as completed with conclusion `success`; each uploaded one non-expired holdout artifact. The artifact digests above are GitHub's archive-level SHA-256 values, not hashes of the JSON file inside each archive. Artifact IDs, archive digests, sizes, and run/job IDs make the uploaded packages individually identifiable.

### Checkpoint identity recovered from the workflow definitions

- 137.5k checkpoint SHA-256: `d2c30940ade76e82bc5e7569c96af6ac4337173d141f627410eb40847e245727`.
- 205k checkpoint SHA-256: `425b9a0939a1b387420061450a99728718eb2640dea3c05fd1692d9ea8a24fa9`.
- 250k checkpoint SHA-256: `95d89f3030d3611c2dc5df26b83fc44b6c4ac3b924bc3a0862149952de4d3e38`.
- 100k workflow verifies the exact checkpoint and writes its SHA into the output JSON; the value still needs to be extracted from the retained artifact.

### What this audit does and does not establish

It establishes a common prompt-file hash, tokenizer hash, inference-script blob, and generation protocol across the four holdouts. It does **not** establish that the holdout was never included in any training corpus, that the current preliminary empty/cap/distinct counts are correct, or that the model answers are accurate. The JSON artifacts must still be retrieved and scored with an audited script. The workflows include rubrics in the output records but do not calculate a correctness score.

The source benchmark is stored in MINIRONIN at `benchmarks/inference-holdout-v1.jsonl` and each RONINIA workflow downloads that exact file by URL and verifies its SHA-256. The next leakage audit must compare the 100 question IDs and normalized text against every corpus manifest and any synthetic-data generation source used in the relevant RONINIA training lineage.


## J. RONINIA recovery continuation to 330k and new holdout

The 250k-to-300k continuation was interrupted, but its partial checkpoint artifact was retained and then recovered by a separate continuation workflow. The distinction matters: the cancelled run is not a successful 300k training result, while the later recovery run is a successful 330k continuation.

### Interrupted 250k → 300k attempt

- Source run: [43379873611](https://github.com/orbitalronin94/RONINIA/actions/runs/43379873611), job 131734887979.
- Workflow commit: `79349d170b739dd5da5b47b57306289228afa37b`.
- Final run conclusion: `cancelled`; the 50,000-step continuation step was cancelled.
- The job nevertheless uploaded a partial checkpoint artifact: ID 14038606072, 4,405,331,548 bytes, archive SHA-256 `ca4d66e2a0b4ceb406685c559dedd67a45e1c5ff36a7ae2ad30dcec6f67a20c9`.
- The later recovery workflow explicitly consumed this artifact and selected the latest valid checkpoint with optimizer state. Do not assume the partial artifact had reached 300k; the exact recovered parent step must be read from the lineage artifact.

### Successful recovery and continuation to 330k

- Recovery run: [43433905009](https://github.com/orbitalronin94/RONINIA/actions/runs/43433905009), job 131914009794; workflow commit `4b25c6adabf86418b6b2da00b5c9adde76226a1f`.
- The job recovered the partial checkpoint chain from run 43379873611, verified the checkpoint metadata and optimizer state, then downloaded and reused the existing full-corpus token cache without retokenization.
- It verified that the parent checkpoint's corpus fingerprint matched the token-cache manifest and that the tokenizer SHA matched `605834d0d1deea545518be54ae0936060845107b906172f6628d0ff9520e57a4`.
- Training reached exactly 330,000 cumulative steps; the workflow's final lineage-verification and final artifact-upload steps completed successfully.
- Training configuration recorded in the workflow: context 256, two threads, batch size 4, learning rate 0.000025, zero warmup, minimum-LR ratio 1.0, checkpoint every 1,000 steps, 32 evaluation batches, tokenization reused.
- Final checkpoint-chain artifact: ID 14069581635, 4,190,025,399 bytes, archive SHA-256 `8f899b247c8cbab0dfa5ffeeb7e05bc4a35b1d3a403a5ebccd478ba9afffdeba`.
- Intermediate recovery-checkpoint artifact: ID 14067728850, 4,297,455,312 bytes, archive SHA-256 `fc19d3b6fcb153da658387829587068be3be8a02ecace2464e62d604ddc920bb`.

### Official 330k holdout

- Holdout run: [43490561981](https://github.com/orbitalronin94/RONINIA/actions/runs/43490561981), job 132110319633; workflow commit `11b1d25b7755d5efd745d4eda00b7d9f36129cda`.
- Workflow verified the exact 330k checkpoint, the same 8k tokenizer SHA, and the same 100-question holdout SHA used by the earlier checkpoint evaluations.
- The holdout job completed successfully and uploaded artifact ID 14068589478 (25,444 bytes; archive SHA-256 `fb3106d6cb698321e363eb9c7ba88f155203062494270d4b99a4127498d220b8`).
- The exact inference-script blob is still `b83ceb712431b3ea20902708fb9ec8f3c243425a`; its defaults match the earlier protocol: seed 20261110, greedy decoding, two threads, 32 tokens, 128 bytes, no KV cache, no RAG.
- The raw JSON has now been recovered and rescored: 1 empty response, 21 outputs reaching the 32-token limit, 99 exact-distinct answer strings, mean generated length 19.88 tokens, and mean latency 0.323478 s. EOS emission and task-level correctness remain unscored because the JSON schema records neither an explicit stop reason nor an automatic rubric score.

The 330k holdout run is distinct from the registry-update workflow triggered by the same commit, which failed. That documentation/registry failure does not invalidate the independently successful holdout job or its uploaded artifact.


## K. Raw JSON recomputation of the five RONINIA holdouts

All five holdout ZIP artifacts were downloaded. Each local archive SHA-256 matched the digest returned by GitHub's Actions artifact API. The JSON inside each archive was then processed by the new repository script `scripts/score_roninia_holdouts.py`. The resulting table is committed as [roninia-checkpoint-metrics.csv](roninia-checkpoint-metrics.csv); per-domain detail is in [roninia-domain-metrics.csv](roninia-domain-metrics.csv). The scorer is [scripts/score_roninia_holdouts.py](../../scripts/score_roninia_holdouts.py), blob SHA-256 `d0401f48d0e2e6a8a3fa5f8eadae69a171a69873`.

| Checkpoint | Empty | Exactly 32 generated tokens | Exact-distinct answers | Mean generated tokens | Mean latency (s) | P90 latency (s) |
|---:|---:|---:|---:|---:|---:|---:|
| 100k | 1 | 22 | 100 | 21.18 | 0.319804 | 0.484661 |
| 137.5k | 0 | 42 | 96 | 22.69 | 0.374886 | 0.570726 |
| 205k | 14 | 29 | 83 | 19.03 | 0.141405 | 0.237574 |
| 250k | 2 | 45 | 96 | 23.13 | 0.274788 | 0.402664 |
| 330k | 1 | 21 | 99 | 19.88 | 0.323478 | 0.510915 |

The recomputed empty-output, token-limit, and exact-distinct counts match the previously extracted values. The table now has a raw-artifact basis rather than being only a transcription from logs.

### Metric definitions and limits

- **Empty:** `answer.strip()` is empty.
- **Exactly 32 generated tokens:** the number of recorded `generated_token_ids` equals the configured `max_new_tokens=32`. This is a token-limit hit, not a general stop-reason label.
- **Exact-distinct answers:** number of unique raw answer strings; no semantic similarity or paraphrase normalization is applied.
- **Mean generated tokens:** arithmetic mean of `len(generated_token_ids)`.
- **P90 latency:** nearest-rank 90th percentile over the 100 per-response `elapsed_seconds` values.
- **EOS emissions:** unavailable. The inference loop stops when EOS is predicted but does not append EOS to the generated IDs and the output schema does not save a `stop_reason`. A short output may also have stopped because the next token would exceed the 128-byte limit. EOS cannot be reconstructed reliably from this JSON.
- **Correctness:** not scored. Rubrics are present in the output records, but the workflow does not calculate an exact-match or rubric-based score.

### Holdout composition

The same 100-question file has the following domain distribution at every checkpoint: 35 `ci_cd`, 25 `personality_troll`, and 40 questions spread across 11 other domains (logic, mathematics, causality, probability, instruction following, contradiction, uncertainty, reasoning, knowledge, critical thinking, and calibration). This is a mixed project-specific holdout, not a pure general-reasoning benchmark. The high share of CI/CD and personality/troll prompts must be stated when interpreting aggregate response diversity or behavior.

### Interpretation

The series is genuinely non-monotonic on these descriptive metrics. The 205k checkpoint has the highest empty-output count and lowest exact-distinct count; 250k has the most 32-token-limit hits; 330k has fewer token-limit hits and 99 exact-distinct strings. None of these facts establishes better answer quality. Latency varies substantially across runs and should be treated as a runner/runtime measurement, not as a direct measure of model capability.

The next analysis must add per-domain behavior, inspect raw generations, audit prompt leakage against the full training corpus and synthetic sources, and define a correctness scorer before any quality trend is claimed.

# The Loss–Behavior Gap in Tiny Language Models
## A multi-run observational study of training objectives and externally measured generation behavior

**Status:** Research draft v0.1 — exploratory, not peer reviewed  
**Language:** English working manuscript; Spanish notes may be added  
**Evidence base:** MINIRONIN, RONIN-IA, HERETIC-RONIN, RONINIA  
**Claim policy:** No claim of reasoning, intelligence, or general capability is made.

### Abstract (provisional)
Training loss is a convenient optimization signal, but it is not itself a direct measurement of useful generation behavior. This paper investigates the gap between optimization traces and fixed-prompt behavioral evaluations in several resource-constrained language-model experiments. The available record includes byte-level and subword-tokenized systems, distinct model families, CPU-constrained training runs, and checkpoint-level holdouts. Raw-artifact-backed descriptive observations include persistent termination limitations in MINIRONIN and non-monotonic changes in empty outputs, token-limit hits, and exact-text diversity across five RONINIA checkpoints. These observations motivate a measurement framework that reports optimization, decoding, and behavioral outcomes separately. The current evidence is observational and heterogeneous; causal attribution to architecture, data, tokenizer, or training duration is not yet justified.

### 1. Research question
When, and to what extent, do training and validation loss trajectories predict externally observable generation behavior in small language models trained under constrained compute?

Subquestions:
1. Can lower training or validation loss coexist with persistent EOS failure, truncation, repetition, or empty generations?
2. Are checkpoint-level behavioral changes monotonic?
3. Which evaluation metrics are stable across tokenizer and decoding changes?
4. How much apparent progress is explained by prompt memorization, output-length changes, or decoding configuration?

### 2. Scope and terminology
“Tiny” is used descriptively for the experimental systems in this corpus, not as a universal parameter threshold. “Behavior” refers only to measurable properties of generated outputs under a specified prompt set and decoding configuration. “Holdout” means a prompt set not used for the relevant training run, subject to verification of contamination and lineage.

### 3. Preliminary evidence
#### 3.1 MINIRONIN
The 810k and 910k evaluations each contain 100 prompts. Both report 100 generations reaching the 128-token cap and zero emitted EOS tokens. Mean latency rises from approximately 0.288 s to 0.424 s; distinct textual responses fall from 98 to 91. These figures are descriptive and depend on the recorded inference setup. They do not establish that additional training caused degradation.

#### 3.2 RONINIA
Five official 100-response evaluations at 100k, 137.5k, 205k, 250k, and 330k have been recovered from ZIP artifacts whose archive SHA-256 values match GitHub's artifact API. A single scorer recomputed empty outputs (1, 0, 14, 2, 1), exact 32-token-limit hits (22, 42, 29, 45, 21), and exact-distinct answer strings (100, 96, 83, 96, 99). The five runs share the same prompt-set hash, tokenizer hash, inference-script blob, deterministic seed, greedy decoding, and generation limits. These are output-shape and lexical-uniqueness metrics, not correctness scores. The JSON schema does not record explicit EOS/stop reasons, and the holdout's absence from all training data has not yet been established. Adjacent-bigram repetition was previously estimated to rise from 0.96 to 1.83 per response between 205k and 250k; its implementation and denominator remain unaudited.

#### 3.3 RONIN-IA: parameter expansion without screening gain

Two workflow records for the experiment `ronin-expand-10x-from-winning-10k-v1` report the same base checkpoint (10,000 steps; SHA-256 `7a7fe93350b72ebc8d645900c2ae8be455a60334e04ac95176e09bab72f981ed`), target parameter count 100,900,160, 500 training steps, and a 685,023,414-byte corpus with SHA-256 `0d92e66ee96931299b97da7bbbb47f3312b3333bcd081a355422ed0230960af7`. The 64-question MMLU-Pro validation screening used identical question IDs before and after training: 5/64 correct in both cases (7.8125%; 0.0 percentage-point change). The report explicitly labels this SCREENING_ONLY, records automatic promotion as false, global G0 as FAIL, and benchmark holdout contamination as PENDING. Functional preservation before training passed with maximum absolute logit delta 1.4305e-6.

This is useful evidence that a 500-step continuation after a 10× parameter expansion did not improve this particular screening score. It is not evidence that the model's broader behavior was unchanged, nor a controlled test of parameter count alone. The two records should be treated as replicated workflow outputs only after verifying whether they are independent runs or repeated execution of the same experiment specification.

### 4. Proposed method
For every checkpoint, preserve:
- checkpoint SHA-256, parent checkpoint SHA-256, completed optimizer steps;
- parameter count, architecture/config hash, tokenizer hash and vocabulary;
- corpus manifest, document IDs, token count, deduplication and synthetic-data flags;
- training and validation loss with aggregation window;
- exact prompt-set hash, decoding parameters, stop conditions, inference implementation;
- per-prompt raw output, token count, latency, EOS status and error state.

Report at least:
- empty-output rate;
- EOS emission rate;
- maximum-length/truncation rate;
- unique-output rate and normalized distinct-n;
- repeated unigram/bigram rates with explicit denominator;
- latency distribution, not only mean;
- task-specific correctness only where independently adjudicated.

Use paired checkpoint comparisons on identical prompts and decoding settings. Report confidence intervals or bootstrap intervals, and retain per-item results. Avoid collapsing heterogeneous models into one aggregate score.

### 5. Threats to validity
- Holdout contamination and prompt reuse across training datasets.
- Different tokenizer vocabularies and token-to-character ratios.
- Different generation caps, stop-token definitions, and inference code.
- Temperature, sampling, KV-cache, and batching differences.
- Checkpoint lineage errors or artifact substitution.
- Small prompt sets and unstable metrics.
- Loss values not comparable across tokenizers, objectives, or data mixtures.
- The risk of selecting only interesting checkpoints after seeing results.

### 6. Current conclusion
The evidence supports a narrow claim: optimization traces and generation diagnostics measure different aspects of a model, and the latter can change non-monotonically across checkpoints. It does not yet support a causal account of why these changes occur or a universal relationship between loss and behavioral quality.

### 7. Required work before submission
1. Recompute all metrics from raw holdout JSONs using one audited script.
2. Verify prompt-set hashes and prove holdout separation from training corpora.
3. Recover matching training/validation traces for every evaluated checkpoint.
4. Normalize decoding conditions or stratify results where normalization is impossible.
5. Add RONIN-IA and HERETIC runs only after exact configurations are recovered.
6. Publish analysis code, raw metric tables, and a data dictionary.

### 8. Reproducibility package
Planned: `data/checkpoints.csv`, `data/holdout_metrics.csv`, `data/run_manifest.csv`, `src/score_holdout.py`, `src/paired_checkpoint_analysis.py`, and a README with exact artifact IDs and hashes.

### References to add
Primary sources must be cited by immutable GitHub run URLs, artifact IDs, and SHA-256 values. Methodological references on language-model evaluation, measurement validity, bootstrap uncertainty, and data contamination remain to be selected and verified.


### 3.4 RONINIA: optimization success, verification failure, and recovery

The 205k→250k continuation provides a direct example of why training status and workflow status must be separated. In [run 43315959342](https://github.com/orbitalronin94/RONINIA/actions/runs/43315959342), the exact 45,000-additional-step training action completed successfully. The job uploaded recoverable checkpoints even if later steps failed, then the “Verify cumulative 205000 checkpoint and write lineage” step failed. The subsequent final checkpoint/lineage upload succeeded, but the run's overall conclusion was failure. The 250k holdout later used the recorded checkpoint SHA-256, so the model state was evaluable despite the verification-stage defect.

A later recovery sequence reached 330k by recovering the latest valid checkpoint from an interrupted continuation, verifying the existing token cache without retokenization, continuing to exactly 330,000 steps, and successfully writing and uploading lineage. This makes the 250k and 330k observations usable only when their distinct ancestry and artifact states are preserved.

### 3.5 What the expansion screening adds—and does not add

The RONIN-IA 10× expansion case provides a different kind of negative result: the 64-question MMLU-Pro screening score remained 5/64 before and after 500 steps. The workflow's own status was SCREENING_ONLY and G0 FAIL, with automatic promotion disabled. This does not show that expansion is ineffective in general. It shows that this particular short continuation did not improve this small screening score, under the recorded experiment design.

The broader lesson is methodological: loss, output-shape metrics, screening accuracy, and workflow completion are separate observables. They should be reported side by side, not substituted for one another.

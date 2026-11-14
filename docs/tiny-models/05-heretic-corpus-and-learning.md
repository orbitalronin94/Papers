# Corpus Scale Is Not Learning
## A case study of data composition, token budgets, and behavioral evaluation in HERETIC-RONIN

**Status:** Research draft v0.1 — evidence incomplete  
**Primary system:** HERETIC-RONIN  
**Comparators:** MINIRONIN and RONINIA where compatible  
**Claim policy:** The title is a research hypothesis, not a pre-established conclusion.

### Abstract (provisional)
The amount of text presented to a language model is an incomplete description of its training experience. Corpus composition, deduplication, tokenization, sequence packing, optimization schedule, and evaluation design all influence what can be inferred from a run. This paper reconstructs HERETIC-RONIN experiments, including a reported pilot of approximately 500M parameters and a 512,000-token training chunk with a 0/120 holdout result. The currently available evidence is insufficient to attribute the outcome to corpus scale, synthetic-data composition, architecture, or optimization. The paper therefore proposes an audit framework linking corpus manifests to token exposure, checkpoint lineage, and fixed behavioral evaluations.

### 1. Research questions
1. Does increasing nominal corpus size increase unique, useful token exposure?
2. How do synthetic and non-synthetic sources differ in their effect on memorization and generalization?
3. Can a model achieve low training loss while failing a task-specific holdout?
4. Which corpus metadata are necessary to interpret a negative result?

### 2. Preliminary evidence and caveats
A previous extraction identified:
- a HERETIC pilot described as approximately 500M parameters, 50 updates, about 13,096 seconds, and 39.1 tokens/s in a performance record;
- a 512,000-token training chunk followed by a 120-prompt holdout reported as 0/120 on the target success measure.

These values require direct verification against original run logs, workflow configuration, dataset manifests, and raw holdout outputs. The phrase “0/120” is not interpretable until the scoring criterion is defined. It must not be paraphrased as “the model learned nothing.”

#### 2.1 HERETIC-RONIN: an audited 512,000-token chunk

A retrieved chunk record reports micro-steps 2,600–4,600, 2,000 micro-steps, 50 optimizer steps, gradient accumulation 40, micro-batch size 2 sequences, context length 128, 10,240 tokens per optimizer step, and 512,000 tokens in the chunk. Mean loss per token was 2.26884 (first 100 micro-steps: 2.34918; last 100: 2.19189). The recorded holdout remained 0/120 before and after the chunk, with 20 items each in mathematics, programming, logic, natural science, language, and interdisciplinary categories. The reported difference was 0.0 percentage points.

The same record gives a corpus audit: 256,305 documents before deduplication, 68 duplicate records excluded, and 256,237 audited documents after deduplication. Total source bytes were 680,665,972. Sources were CoVoST2 (CC0, translation-only), Mathlib4 (Apache-2.0), ScienceVerse (per-document CC-BY/CC0), Spanish public-domain literature, one NASA NTRS item, and nine owner-authorized Papers documents. The manifest explicitly excluded validation/test/holdout material, 20,000 unreviewed open-source candidates, Drosophila procedural synthetic rows, and exact/SimHash near-duplicate endpoints from the signed audit plan. The chunk took 17,105.51 seconds according to the record, and the checkpoint SHA-256 was `c81edf6658ed208cf4848c831336d427df4464eb725d158fdf827b99910ba5a2`.

This is a stronger and more precise case than a bare “large corpus” claim. However, the 0/120 metric remains uninterpretable beyond the recorded scoring rubric until the raw prompt/response JSON and scorer are recovered. The first/last loss windows are not an independent validation metric.

### 3. Corpus audit framework
For every corpus artifact, record:
- source URL and retrieval date;
- license and redistribution status;
- language and domain;
- document count and byte count;
- exact and near-duplicate policy;
- filtering and quality-control rules;
- synthetic versus externally sourced labels;
- tokenizer identity and vocabulary size;
- token count after tokenization;
- train/validation/holdout split procedure;
- manifest hash and artifact ID.

Distinguish raw bytes, documents, characters, tokenizer tokens, training examples, and optimizer-exposed tokens. “Corpus size” must name its unit.

### 4. Experimental design
Construct controlled arms where feasible:
- curated non-synthetic corpus;
- synthetic corpus;
- mixed corpus with documented proportions;
- deduplicated versus non-deduplicated variants;
- matched-token-budget comparisons.

Hold architecture, tokenizer, optimizer, schedule, and token budget constant when testing corpus composition. Use identical independent holdouts and report per-task metrics. If compute limits prevent full factorial experiments, label the work observational and state confounders.

### 5. Evaluation
A 120-item holdout should publish:
- exact prompt set and hash;
- task categories and scoring rubric;
- raw model outputs;
- scorer version and adjudication procedure;
- empty, malformed, truncated, and repeated output counts;
- exact-match and semantic scoring separately;
- uncertainty intervals and per-category breakdowns.

### 6. Current interpretation
The present record motivates the proposition that nominal corpus scale is not sufficient evidence of learning. It does not yet establish which data property explains HERETIC's reported holdout outcome. A negative result is scientifically useful only when the training and evaluation chain is auditable.

### 7. Required evidence
1. Locate all HERETIC training runs and exact workflow commits.
2. Recover the 512k chunk manifest and tokenizer metadata.
3. Recover raw 120-prompt holdout JSON and scoring code.
4. Verify parameter count, architecture, optimizer steps, and processed tokens.
5. Reconstruct corpus composition and synthetic/non-synthetic proportions.
6. Compare with MINIRONIN/RONINIA only after harmonizing metric definitions.

### 8. Planned artifacts
`heretic_runs.csv`, `corpus_manifest.csv`, `holdout_120_raw.json`, `score_holdout.py`, `data_card.md`, and a reproducibility README.

### References to add
Dataset documentation, data contamination and memorization studies, language-model scaling and data-quality literature, and primary repository artifacts. All citations and licenses must be checked before submission.

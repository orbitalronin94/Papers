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

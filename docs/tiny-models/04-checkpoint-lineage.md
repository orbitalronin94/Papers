# Checkpoint Lineage and Failure-Tolerant Experimentation
## Separating training completion, artifact integrity, and workflow success

**Status:** Research draft v0.1 — engineering case study  
**Claim policy:** Reconstructed from workflow logs; no inference about model quality from pipeline status.

### Abstract (provisional)
Long-running machine-learning experiments can produce valid checkpoints even when a workflow later fails during metadata verification or artifact finalization. This paper studies checkpoint lineage and failure handling in small-model experiments conducted through GitHub Actions. In a RONINIA continuation sequence, workflow logs show training reaching 250,000 cumulative steps, saving and hashing the checkpoint, and successfully uploading a holdout artifact, while a later lineage-verification step failed with an AttributeError caused by a failed regular-expression match. The case motivates a layered definition of experiment success and a failure-tolerant provenance protocol.

### 1. Research questions
- How should an experiment distinguish compute completion from workflow completion?
- What minimum metadata is required to prove checkpoint ancestry?
- How can partial results remain recoverable after post-training failures?
- Which workflow assertions prevent false success and false failure reports?

### 2. Case study: RONINIA 205k → 250k
The retrieved workflow log for run `43315959342` records:
- parent checkpoint at 205,000 steps;
- 45,000 additional training steps;
- cumulative 250,000 steps;
- parameter count 9,757,440;
- reported processed-token count 920,277,537;
- final checkpoint SHA-256 `95d89f3030d3611c2dc5df26b83fc44b6c4ac3b924bc3a0862149952de4d3e38`;
- validation loss 0.4032951621 at the 250k checkpoint;
- a subsequent lineage-verification failure: `AttributeError: 'NoneType' object has no attribute 'group'`.

A later official 250k holdout workflow successfully uploaded an artifact. This supports the distinction between training/holdout artifact availability and the earlier job's final status. The exact artifact IDs, source checkpoint, and parent hashes must be cross-checked in the final provenance table.

#### 2.1 A second failure mode: MINIRONIN Mamba metadata

A MINIRONIN continuation log records completion of 2,000 cumulative steps and a checkpoint with verified SHA-256, followed by a `KeyError: 'index_sha256'` during a later metadata stage. This is a separate failure signature from RONINIA's regex-related AttributeError. It supports classifying failures by stage and exception rather than treating all non-green workflows as failed training runs.

### 3. Proposed success model
Report at least four independent statuses:
1. **Training status:** planned optimizer steps reached or not.
2. **Checkpoint integrity:** file exists, loads, metadata matches, SHA-256 verified.
3. **Lineage status:** parent checkpoint and cumulative step count independently verified.
4. **Evaluation status:** holdout executed, prompt-set identity verified, outputs stored.

A single green/red workflow status is too coarse to represent these dimensions.

### 4. Provenance schema
Each checkpoint record should include:
- repository, workflow run ID, job ID, workflow file commit;
- parent artifact ID and parent checkpoint SHA-256;
- checkpoint filename, cumulative steps, steps this run;
- model/config hash, tokenizer hash, corpus manifest hash;
- parameter count, optimizer and scheduler state presence;
- checkpoint SHA-256 and artifact ID;
- validation metrics and their data split;
- evaluation run ID, prompt-set hash, decoding configuration;
- timestamps, runner image, software versions;
- explicit status fields and error stage.

### 5. Failure-tolerant workflow recommendations
- Upload recoverable checkpoints before nonessential post-processing.
- Verify checkpoints by loading metadata and checking hashes, not by parsing fragile log text.
- Store structured JSON manifests as primary evidence; treat console logs as secondary.
- Make each stage idempotent and independently rerunnable.
- Preserve partial outputs on failure.
- Use explicit state names such as TRAINED, CHECKPOINT_VERIFIED, LINEAGE_VERIFIED, HOLDOUT_COMPLETED.
- Fail loudly on missing parent hashes or mismatched cumulative steps.
- Never label an experiment “successful” solely because an artifact upload succeeded.

### 6. Limitations
The current case is one reconstructed workflow chain. It does not quantify how frequently this failure pattern occurs across all repositories. The regex failure mechanism is inferred from the exception and surrounding log, and should be confirmed against the exact workflow source at the relevant commit. The case does not show that every failed workflow contains a valid model checkpoint.

### 7. Required work
1. Retrieve workflow YAML at the exact commit for each cited run.
2. Inspect the failing regex and replace text parsing with structured manifests.
3. Audit all failed runs in MINIRONIN, RONIN-IA, HERETIC-RONIN, and RONINIA.
4. Build a dataset of failure stage, checkpoint recoverability, and artifact integrity.
5. Test recovery procedures with deliberately injected failures.
6. Publish a machine-readable provenance schema and validation script.

### 8. Planned artifacts
`workflow_failure_catalog.csv`, `checkpoint_lineage.jsonl`, `verify_checkpoint.py`, `schema/checkpoint_manifest.schema.json`, and workflow examples.

### References to add
ML experiment tracking, data provenance, workflow reliability, software supply-chain integrity, and GitHub Actions documentation. Cite exact workflow run and commit URLs.

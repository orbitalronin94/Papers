# Checkpoint Lineage and Failure-Tolerant Experimentation
## Separating training completion, artifact integrity, and workflow success

**Status:** Research draft v0.1 — engineering case study  
**Claim policy:** Reconstructed from workflow logs; no inference about model quality from pipeline status.

### Abstract (provisional)
Long-running machine-learning experiments can produce valid checkpoints even when a workflow later fails during metadata verification or artifact finalization. This paper studies checkpoint lineage and failure handling in small-model experiments conducted through GitHub Actions. In RONINIA, one continuation reached 250,000 steps and saved its checkpoint before a later lineage-verification stage failed with a regex-related AttributeError. A subsequent 250k-to-300k attempt was cancelled after uploading partial checkpoints; a recovery workflow selected the latest valid checkpoint, reused the existing token cache, and completed a verified continuation to 330,000 steps. A separate official 330k holdout job then completed and uploaded its evaluation artifact. A step-level audit confirms that the 45,000-step training action and final artifact upload succeeded even though the cumulative-checkpoint verification step failed; a later recovery job completed every substantive step to 330k. These events demonstrate why interrupted runs, recovered checkpoints, training completion, lineage verification, and evaluation completion must be recorded separately. The paper proposes a layered definition of experiment success and a failure-tolerant provenance protocol.

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
Primary evidence is the immutable workflow, job, commit, and artifact record. Supplementary context: [HELM](https://arxiv.org/abs/2211.09110) demonstrates the value of releasing raw prompts and completions alongside standardized evaluation. The [workflow-audit.csv](workflow-audit.csv) file provides the run-level index.


### 2.2 Recovery after a cancelled continuation: 250k → partial artifact → 330k

A later RONINIA sequence provides a stronger recovery case than the isolated post-training metadata errors:

1. **Interrupted attempt:** [run 43379873611](https://github.com/orbitalronin94/RONINIA/actions/runs/43379873611), job 131734887979, attempted 50,000 additional steps from the verified 250k parent toward 300k. The training step was cancelled. The workflow nevertheless uploaded a partial checkpoint artifact (artifact ID 14038606072; archive SHA-256 `ca4d66e2a0b4ceb406685c559dedd67a45e1c5ff36a7ae2ad30dcec6f67a20c9`). The cancelled run must not be described as having reached 300k.
2. **Recovery:** [run 43433905009](https://github.com/orbitalronin94/RONINIA/actions/runs/43433905009), job 131914009794, recovered that artifact and selected the latest valid checkpoint. Its workflow explicitly required optimizer state, checked the tokenizer and parameter count, and compared the parent checkpoint's corpus fingerprint with the existing token-cache manifest.
3. **Data pipeline reuse:** the recovery job downloaded the pre-existing full-corpus token cache unchanged. It verified the cache checksums and manifest and did not retokenize the corpus.
4. **Continuation:** training reached exactly 330,000 cumulative steps. The workflow then wrote structured lineage metadata and uploaded the final checkpoint chain (artifact ID 14069581635; archive SHA-256 `8f899b247c8cbab0dfa5ffeeb7e05bc4a35b1d3a403a5ebccd478ba9afffdeba`). The final checkpoint SHA-256 was recovered from the official holdout JSON: `2fba7ec4b909150be08a1777e6a13c9046b1a2f5a711dd61469e61e54de578c4`. The exact recovered parent step still needs to be extracted from the lineage JSON before publication.
5. **Evaluation:** [run 43490561981](https://github.com/orbitalronin94/RONINIA/actions/runs/43490561981), job 132110319633, verified the 330k checkpoint and the official prompt/tokenizer hashes, generated 100 responses, and uploaded holdout artifact ID 14068589478 (archive SHA-256 `fb3106d6cb698321e363eb9c7ba88f155203062494270d4b99a4127498d220b8`). The raw JSON was recovered and rescored: 1 empty response, 21 responses reaching the 32-token limit, and 99 exact-distinct answer strings. The archive SHA-256 matches the GitHub artifact digest. The output schema records no explicit stop reason or EOS event, and no correctness score is calculated.

The recovery workflow's recorded training configuration was context length 256, two threads, batch size 4, learning rate 2.5e-5, zero warmup, minimum-LR ratio 1.0, checkpoint interval 1,000, and 32 evaluation batches. The token cache, tokenizer, and corpus fingerprint were verified before continuation.

This case distinguishes at least four states that a single run conclusion cannot represent: (i) an interrupted run that emitted recoverable checkpoints, (ii) a successful recovery/continuation, (iii) a verified final checkpoint artifact, and (iv) a successful holdout job whose raw metrics still require analysis. The registry-update workflow triggered around the 330k documentation changes failed separately; that failure does not invalidate the independently successful training or holdout jobs.


### 9. Job-step audit: successful work inside failed workflows

The RONINIA 205k→250k job (run [43315959342](https://github.com/orbitalronin94/RONINIA/actions/runs/43315959342), job 131523907339) exposes the stage boundary precisely:

- Parent run/artifact verification, exact 205k checkpoint resolution, token-cache download and identity verification, and matching 256-token configuration all succeeded.
- The 45,000-step training action succeeded.
- The “Upload every recoverable checkpoint even if a later step fails” action succeeded.
- “Verify cumulative 205000 checkpoint and write lineage” failed.
- “Upload final checkpoint and complete recovery lineage” succeeded.

The overall workflow conclusion was failure. The record therefore contains successful optimization and checkpoint uploads alongside a failed verification stage. The failure should be preserved, not converted into either “training failed” or “workflow succeeded.”

By contrast, the later 330k recovery job (run [43433905009](https://github.com/orbitalronin94/RONINIA/actions/runs/43433905009), job 131914009794) completed every substantive step: recovering checkpoints from the interrupted run, selecting the latest valid state, downloading and verifying the existing token cache unchanged, continuing to exactly 330k, verifying the final checkpoint and lineage, and uploading the final chain. The official 330k holdout then verified the checkpoint SHA and produced its own artifact.

### 10. Artifact inventory and retention risk

The GitHub Actions artifact API reports these retained artifacts:

| Run | Artifact | ID | Size (bytes) | API SHA-256 |
|---|---|---:|---:|---|
| HERETIC 512k chunk | heretic-500m-accum40-micro-4600 | 13578607392 | 6,001,746,291 | 9ff1ac4a96df57cd721291c47acec0889638be5a38ea4fc7335737031fe37468 |
| RONIN-IA expansion A | ronin-expand-10x-from-10k-42364113096 | 13570749085 | 374,819,789 | f53659f166548e742f6feefbcf067c9af4be312969b264a35593ce66803897b4 |
| RONIN-IA expansion B | ronin-expand-10x-from-10k-42364138735 | 13571800501 | 374,819,541 | 49e7b3564797095b084b06492a550fca73b493664522ac0ea3bd15e9b459526c |
| RONINIA 250k checkpoint chain | ronin-10m-chain-250000-43315959342 | 14002902157 | 4,835,631,596 | 8742092f1f0fb08c0e3bfd2cd8ea64fdbb9df94404f37ffc4a78972807fa974e |
| RONINIA 330k checkpoint chain | ronin-10m-chain-330000-43433905009 | 14069581635 | 4,190,025,399 | 8f899b247c8cbab0dfa5ffeeb7e05bc4a35b1d3a403a5ebccd478ba9afffdeba |

Artifact digests are metadata returned by GitHub's artifact API; they are not interchangeable with the checkpoint SHA-256 inside an archive. The HERETIC artifact is approximately 6.0 GB, so raw holdout extraction and retention should be planned separately from full checkpoint downloads. Preserve both artifact-level and file-level hashes.

### 11. A provenance state machine

For future work, represent each run with separate fields rather than one success flag:

1. training_started
2. target_steps_reached
3. checkpoint_written
4. checkpoint_hash_verified
5. lineage_verified
6. artifact_uploaded
7. holdout_completed
8. holdout_scored
9. workflow_conclusion

This prevents a post-training parsing exception from erasing valid training evidence, and prevents a successfully uploaded artifact from being mistaken for a validated scientific result.

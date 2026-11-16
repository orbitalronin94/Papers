# Tiny MINIRONIN: an Integrated Architecture for Tokenization, Documentary Memory, and Evidence-Aware Training

**Type:** Technical design note and applied research proposal  
**Status:** Implementation proposal and validation protocol; no empirical improvement is claimed yet  
**Objective:** Improve the small MINIRONIN checkpoint without breaking compatibility, learned behavior, or holdout validity.

## Executive summary

MINIRONIN should not attempt to solve with its limited parameter budget what an external system can do better. The strategy is to divide the work into three coordinated layers:

1. **Parametric capacity:** the Transformer learns language, procedures, response formats, abstention, evidence use, and generalizable patterns.
2. **Literal documentary memory:** an external index preserves admitted libraries, original fragments, metadata, and provenance. It can be updated without retraining the model.
3. **Efficient interface:** a reversible tokenizer and context protocol reduce unhelpful bytes and provide the model with small, relevant, citable evidence.

The integration is called **MINIRONIN Integrated Evidence Stack (MIES)**. Its lexical subsystem is honestly named **BACKDOOR_BPE**: it is not a complete BPE tokenizer or a conventional linguistic tokenizer, but a deterministic table of frequent byte sequences that reuses already-reserved vocabulary rows.

The central decision is to preserve the byte path as a universal fallback. No optimization may prevent exact encoding and reconstruction of valid text.

## 1. Starting point and actual constraints

MINIRONIN's source configuration declares 23,000 vocabulary rows, a decoder-only Transformer, and shared input/output embeddings. The operational reference tokenizer uses 257 symbols: UTF-8 bytes 0–255 and EOS=256. Reserved rows exist, but they are not functional tokens until the encoder emits them and training and inference allow the model to predict them.

The operational checkpoint must be identified by SHA-256, configuration, step count, and active_vocabulary. Step count alone does not identify a model. This note does not change the catalogue or declare any checkpoint promoted.

**Consequences:**

- Keep IDs 0–256 unchanged. EOS remains 256.
- Add tokens only from 257 onward, append-only.
- Do not change the shape of token_embedding or lm_head: the model already has the rows configured.
- Do not treat reserved rows as free capacity: each token requires encoding, initialization, softmax exposure, and supervision.
- Record a tokenizer hash in every checkpoint. Two checkpoints with different tokenizers are not comparable as if they shared the same representation.
- Compare bits per byte (BPB) and task metrics, not only loss per token.

## 2. Overall design: three layers and one contract

~~~text
Admitted libraries + rights + provenance
                    |
                    v
       Canonical document manifest
          /                         \
         v                           v
 Active rows                      Literal RAG
 (supervision)                 (document index)
         \                           /
          \                         /
           v                       v
        Shared evidence contract
                    |
                    v
     Small context/prompt adapter
                    |
                    v
       MINIRONIN + BACKDOOR_BPE
                    |
                    v
       answer / citation / abstention
~~~

The canonical manifest is the single authority for admission. Training and retrieval are two projections of the same inventory, not two processes that independently rediscover documents.

### 2.1 Canonical manifest

Each document should have:

| Field | Purpose |
|---|---|
| document_id | Stable ID derived from source and content |
| source_id, project, relative_path | Reproducible provenance |
| revision or artifact_id | Exact source version |
| sha256 | Integrity of the original document |
| license, rights_status, redistribution | Usage and redistribution rights |
| admission_status | admitted, candidate, quarantine, or rejected |
| train_eligible | Explicit permission for training |
| retrieval_eligible | Explicit permission for RAG |
| epistemic_type | primary, verified, synthetic, self-authored, curated, or estimated |
| domain, language | Domain/language mixture and evaluation |
| provenance_ref | Source record, licence, or manifest |

Presence in a folder alone does not prove that a file has been admitted. For inherited corpora, the builder must validate the source manifest and rights record at document or library level. Documents without verified rights are excluded from both projections.

**Absolute exclusions:** holdouts, reserved validation data, private rubrics and expected answers, checkpoints, optimizer states, raw operational logs, secrets, credentials, and unauthorized personal data. A document excluded from training does not automatically enter RAG: each channel requires explicit permission.

### 2.2 Two outputs, one inventory

- **RAG projection:** original document fragments, document and fragment hashes, locator (page/section/line), epistemic labels, licence, and all duplicate provenances.
- **Training projection:** derived rows with source document ID and hash, evidence hash, task type, split, and generation/review label. Synthetic answers are never presented as primary citations.

A library update rebuilds both projections and produces a report of additions, removals, changes, duplicates, and exclusions. Neither projection is updated silently.

## 3. BACKDOOR_BPE: expanding the vocabulary without losing bytes

### 3.1 What to do

Create an initial table of 128–256 frequent byte sequences, selected exclusively from the admitted training split. Suggested range: IDs 257–512; ablation determines the final number.

Criteria:

- Sequences of 3–16 bytes, with a minimum frequency and presence across multiple documents.
- Measure actual marginal savings with the final tokenizer; do not select by raw frequency alone.
- Favor sequences common in Spanish and real domains without removing English or code coverage.
- Do not cross document boundaries, JSONL records, or fields.
- Do not learn candidates from validation, the documentary benchmark, or holdouts.
- Avoid control tokens in the first iteration. Optimize ordinary text first; task markers are a separate experiment.

The encoder applies deterministic longest-match, with ties broken by stable ID, and falls back to individual bytes when no match exists. The decoder expands each new token to its original byte sequence. Encoding must be lossless for Unicode, accents, line breaks, spaces, emoji, and code.

### 3.2 What not to do yet

- Do not duplicate tokens for digits 0–9: bytes already represent them.
- Do not add hundreds of morphemes or character classes at once.
- Do not create a second EOS or reassign 256.
- Do not interpret user-provided literal strings as control tokens.
- Do not call it pure BPE: it is a byte n-gram vocabulary with deterministic segmentation.

### 3.3 Initialization and training

Initialize each new row as the average of the embeddings for the bytes it represents. This is a geometric initialization, not a semantic guarantee. Keep the embedding and LM-head weights tied. When resuming an optimizer, zero the moments for new rows; do not alter the states of old rows.

Initial ablation:

A. bytes 0–256 (reference);  
B. bytes + 128 n-grams;  
C. bytes + 256 n-grams;  
D. best variant + EOS windows;  
E. best variant + evidence supervision.

Evaluate BPB, validation loss per byte, mean length, compression ratio, latency, and quality by domain. Exact reconstruction is a binary requirement.

## 4. RAG for a model that cannot interpret huge contexts

Recent evidence on SLMs warns that classical retrieval can degrade when too much semantic interpretation is delegated to the small model. MiniRAG proposes combining text and entities in a heterogeneous structure and using relations/topology to reduce this dependency. For MINIRONIN, the useful approach is an austere adaptation, not a heavy GraphRAG clone.

### 4.1 Three retrieval layers

1. **BM25/FTS5:** names, formulas, identifiers, citations, dates, and exact words.
2. **Compact multilingual vectors:** paraphrases and Spanish/English queries. Evaluate multilingual-e5-small against small alternatives; record version and licence.
3. **Lightweight structural links:** entities, aliases, document, section, bibliography, and explicit relations. Do not generate a speculative graph with an LLM; link only auditable metadata or relations.

Fuse rankings (RRF as baseline), limit duplicates by document, and reserve source diversity. A large reranker should not be a mandatory runtime dependency; it may be used offline to create labels or evaluate candidates, with provenance marked.

### 4.2 Context budget

The model has a finite context and a byte-based base tokenizer. Until the new tokenizer is measured, budget using actual token cost, not character count. Retrieve a few compact fragments (for example, 2–4), not entire libraries.

Each block includes citation ID, document, fragment, hash, locator, licence, and epistemic label. The prompt asks the model to:

- use a citation only if it supports the claim;
- distinguish evidence, inference, and prior knowledge;
- identify contradictions;
- state when evidence is not found;
- never invent titles, authors, pages, or citations.

The runtime must also work with BM25 and no vectors, so a small index remains usable on CPU and does not depend on downloading embeddings on every run.

## 5. Active rows: teaching the model to use evidence

Injecting documents into context is not enough. The model must learn the context-use protocol from short, varied, verifiable examples. Every derived row retains the ID and SHA of the supporting document.

| Family | Input | Target behavior |
|---|---|---|
| Supported answer | question + 1–3 fragments | concise answer + correct citation |
| Insufficient evidence | question + irrelevant fragments | explicit abstention |
| Conflict | two incompatible sources | expose contradiction and provenance |
| Literal copy | request for definition/quotation | copy exact span without changing numbers |
| Location | question about section/author/date | retrieve exact metadata or abstain |
| Comparison | two fragments | separate similarities and differences |
| Distractor | relevant evidence plus distractors | select only useful evidence |
| Unanswerable query | corpus lacks the answer | do not invent a completion |

### 5.1 Safe generation

- Prefer deterministic templates and controlled transformations for the first corpus.
- If a teacher model is used, store identifier, version, prompt, date, and original output; mark the row synthetic and review samples.
- Do not generate facts from vector similarity.
- Keep question, answer, evidence, and provenance in separate fields.
- Deduplicate by hash and similarity while retaining provenance.
- Avoid placing a synthetic paraphrase of the same document in both train and validation.

### 5.2 Training mixture

Do not replace the language corpus with QA rows. In a ~10M-parameter model, overspecialization can happen quickly. Keep most of the budget on admitted language/documents and reserve a small fraction for evidence use and abstention; increase that fraction only if task validation improves without degrading fluency or previously learned domains.

Measure text continuation, QA format, copying, correct citations, abstention, contradictions, and regressions in mathematics, science, literature, and behavior.

## 6. Integration and activation protocol

Activation must be transactional and reproducible:

1. Freeze the base checkpoint SHA, configuration, and holdout.
2. Build the canonical manifest; fail on sources without verified rights or admission.
3. Build literal RAG and validate counts, hashes, coverage, and exclusions.
4. Build active rows only from documents with train_eligible=true; record evidence hashes.
5. Build BACKDOOR_BPE only from train; generate deterministic vocabulary and hash.
6. Run round-trip, ID stability, document-boundary, EOS, Unicode, and active-vocabulary tests.
7. Initialize new rows and verify that rows 0–256 do not change.
8. Validate the RAG adapter with synthetic queries separate from the holdout.
9. Run short training without touching the base checkpoint; save checkpoint and manifest.
10. Check byte-only and RAG inference, loading, and rollback.
11. Only after every component is activated, run the real paired and reserved holdout.

No workflow should launch training or holdout as a side effect of building the index. RAG construction produces artifacts; evaluation and training are explicit, separate decisions.

## 7. Evaluation: how to demonstrate that it helps

### 7.1 Tokenizer

- Exact round-trip for Spanish/English/code/Unicode.
- Tokens per byte, compression ratio, and frequency of each new token.
- BPB and NLL normalized per byte.
- EOS errors and premature-termination rate.
- Greedy generation with the same checkpoint and limits.

### 7.2 Retrieval

With questions independent of the final index and labelled relevance:

- Recall@1/5/10, MRR, and nDCG;
- citation precision and evidence coverage;
- exact retrieval of names, numbers, formulas, and references;
- latency, RAM, index size, and update cost;
- metrics by language, domain, and epistemic type.

### 7.3 Answering

Compare the same checkpoint, decoder, and questions:

1. no RAG;
2. BM25;
3. BM25 + vectors;
4. hybrid + structural links;
5. best RAG + active rows.

Measure accuracy, evidence faithfulness, valid citations, abstention, contradictions, and language regression. Use blind rubric scoring. Do not declare victory because an answer is longer, text changed, or cosine similarity is high.

## 8. Recommended decisions

**Priority 0 — safety and reproducibility**
- single admission and rights manifest;
- holdout blocking in every builder;
- hashes for corpus, index, tokenizer, and checkpoint;
- compatibility and rollback tests.

**Priority 1 — likely highest return**
- hybrid BM25 + small multilingual vector retrieval;
- citations and abstention trained with active rows;
- byte tokenizer with 128–256 n-grams selected by measured savings;
- training windows that teach EOS.

**Priority 2 — after measurement**
- lightweight links between entities/documents;
- 256 versus 128 n-grams;
- small offline reranker;
- distillation of verified answers if a teacher and review are available.

**Do not prioritize now**
- MoE, dense graphs, multi-stage agents, hundreds of control tokens, large runtime rerankers, parameter expansion, or training on all documents without sampling.

The reason is simple: the model has limited attention and parameters. It should spend its budget learning how to behave, not indiscriminately memorizing every library.

## 9. External evidence and critical reading

1. **Lu et al. (ACL 2025), “Demystifying Small Language Models for Edge Deployment”.** A study of more than 60 public SLMs. It highlights in-context learning limits and opportunities in vocabulary/KV-cache compression, task routing, and hardware–model co-design. Relevant because MINIRONIN's bottleneck is not only weight size: context, tokenization, and evidence use matter too.  
   https://aclanthology.org/2025.acl-long.718/

2. **Fan et al. (ACL 2026), “MiniRAG: A Lightweight RAG system with Small Language Models”.** Proposes heterogeneous indexing of text and entities and lightweight topological retrieval. It is a direct reference for avoiding the demand that a small model perform complex semantic interpretation at every stage. Do not extrapolate its quantitative results to MINIRONIN: the models and benchmarks differ.  
   https://aclanthology.org/2026.acl-long.1721/

3. **Fan et al. (2025), “MiniRAG: Towards Extremely Simple Retrieval-Augmented Generation”.** Initial version of the work and open repository. Useful for studying a lightweight implementation, not for copying an entire architecture without measuring costs.  
   https://arxiv.org/abs/2501.06713  
   https://github.com/HKUDS/MiniRAG

4. **“State of the Art and Future Directions of Small Language Models: A Systematic Review” (2025).** A review of 70 studies focused on SLMs up to 7B. It summarizes multitask training, distillation, compression, and RAG. Its aggregate ranges are not predictions for a 10M model; they are a map, not a promise.  
   https://www.mdpi.com/2504-2289/9/7/189

5. **Nozaki et al. (COLING Industry Track 2025), “Efficient Vocabulary Reduction for Small Language Models”.** Evaluates vocabulary reduction as an embedding-compression lever. It finds that memory and speed can improve, although task performance may fall and some of the loss can be recovered through fine-tuning. In MINIRONIN, the 23,000 rows are already physically reserved: activating 128–256 IDs does not shrink the checkpoint; it can only reduce sequence length and change softmax cost. Do not confuse row activation with weight compression.  
   https://aclanthology.org/2025.coling-industry.64/

6. **Srivastava et al. (EMNLP 2025), “ThinkSLM: Towards Reasoning in Small Language Models”.** Its benchmark of 72 SLMs emphasizes training methods and data quality alongside scale. Its models range from hundreds of millions to several billion parameters, so it is not direct evidence for a 10M model; it informs ablation design, not promises.  
   https://aclanthology.org/2025.emnlp-main.1659/

7. **Asai et al. (Nature, 4 February 2026), “Synthesizing scientific literature with retrieval-augmented language models”.** OpenScholar combines a 45-million-paper store, specialized retrieval, reranking, iterative generation, citation verification, and synthetic data. The applicable lesson is to separate retrieval, attribution, and generation. Do not copy its cost: it uses an 8B generator, a 110M bi-encoder, and a 340M cross-encoder. It also uses ordinary format strings rather than new special tokens; for MINIRONIN this is another reason to test literal prompt markers first.  
   https://www.nature.com/articles/s41586-025-10072-4

## 10. Internal project references

- MINIRONIN/src/minironin/config.py: model dimensions and configured vocabulary.
- MINIRONIN/src/minironin/model.py: causal Transformer and shared embedding/output weights.
- MINIRONIN/scripts/train_seed_tournament.py: byte-level encoding and EOS reference.
- MINIRONIN/scripts/run_inference_holdout.py: byte-level inference and checkpoint validation.
- MINIRONIN/data/semantic/semantic-tokens.json: external conceptual vocabulary; not equivalent to LM tokenizer IDs.
- MINIRONIN/docs/RAG_VS_TRAINING.md: earlier baseline comparing training and RAG.

## Conclusion

### Implications specific to MINIRONIN's size

The ACL edge-SLM study covers 100M–5B models, and ThinkSLM evaluates much larger scales than 10M. MINIRONIN is below both ranges; their percentages should therefore not be imported as predictions. Their methodological criteria can be adopted:

- Data quality and selection before indiscriminate volume; control saturation and forgetting.
- Exact BM25 retrieval as a mandatory baseline; use vectors only if they improve recall and justify total latency/memory.
- Explicit structure and simple document links before a graph generated by a large model.
- Context/citation markers as literal text initially; convert them into IDs only if an ablation demonstrates improvement.
- Measure total system cost (generator + encoder + index + prompt), not checkpoint size alone.

The most sensible architecture for MINIRONIN is not a tiny model trying to swallow an infinite library. It is a small model with a more efficient text representation, verifiable literal memory, examples that teach it to use that memory, and an explicit abstention policy.

**Success means that the same checkpoint answers better with evidence, cites correctly, abstains when appropriate, and does not lose language capability—not that the index is huge or the vocabulary has many tokens.**

# Related literature and methodological anchors

This bibliography is a working map, not a claim that the five project papers reproduce the cited studies. Each reference is linked to its publisher, proceedings page, or primary preprint. The notes explain the narrow methodological connection.

## Evaluation breadth and metric separation

1. Liang, P. et al. (2022). [Holistic Evaluation of Language Models (HELM)](https://arxiv.org/abs/2211.09110). arXiv:2211.09110.
   - HELM motivates standardized scenarios and reporting multiple dimensions rather than a single aggregate score. It is directly relevant to Papers 1 and 2: empty outputs, token-limit hits, lexical uniqueness, latency, and task correctness should remain separate outcomes. Our five RONINIA holdouts are much narrower and must not be described as HELM-equivalent.
2. Yen, H. et al. (2024). [HELMET: How to Evaluate Long-Context Language Models Effectively and Thoroughly](https://arxiv.org/abs/2410.02694). arXiv:2410.02694.
   - The paper reports that benchmark coverage and metric reliability affect conclusions, and that task categories can show distinct trends. This supports per-domain reporting and cautions against treating a 100-item mixed holdout as a universal measure. Its long-context setting differs from the small-model experiments here.

## Data contamination and holdout validity

3. Li, Y., Guo, Y., Guerin, F., and Lin, C. (2024). [An Open-Source Data Contamination Report for Large Language Models](https://aclanthology.org/2024.findings-emnlp.30/). Findings of EMNLP 2024.
   - Establishes contamination analysis as part of trustworthy benchmark evaluation and provides an open-source overlap-analysis direction. Relevant to the planned RONINIA prompt/corpus/token-cache audit and the HERETIC holdout-isolation discussion.
4. Deng, C. et al. (2024). [Investigating Data Contamination in Modern Benchmarks for Large Language Models](https://aclanthology.org/2024.naacl-long.482/). NAACL 2024.
   - Introduces retrieval-based overlap investigation and a complementary test-set slot-guessing protocol. This supports treating exact string overlap as only one signal; paraphrase, templated synthetic examples, and answer-distribution artifacts may require separate checks.
5. Dong, Y. et al. (2024). [Generalization or Memorization: Data Contamination and Trustworthy Evaluation for Large Language Models](https://aclanthology.org/2024.findings-acl.716/). Findings of ACL 2024.
   - Offers a complementary output-distribution approach to contamination detection. It should be considered an auxiliary diagnostic, not a replacement for direct corpus and manifest inspection.

## Compute, data exposure, and scaling

6. Hoffmann, J. et al. (2022). [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556). arXiv:2203.15556; NeurIPS 2022 version: [proceedings paper](https://papers.neurips.cc/paper_files/paper/2022/hash/c1e2faff6f588870935f114ebe04a3e5-Abstract.html).
   - The Chinchilla study relates parameter count and training-token budget under a specified compute-optimal scaling analysis. It is background for Papers 3 and 5, but its conclusions should not be mechanically extrapolated to 10M–500M models, different architectures, tokenizers, or CI CPU constraints. The papers here should report actual processed tokens and compute rather than claim Chinchilla optimality from parameter count alone.
7. Sardana, N., Portes, J., Doubov, S., and Frankle, J. (2024). [Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws](https://arxiv.org/abs/2401.00448). arXiv:2401.00448.
   - Extends compute allocation by accounting for inference demand. Useful context for the practical trade-off between a small model trained longer and a larger model trained less, while remaining an external scaling study rather than evidence about these particular runs.

## CPU benchmarking and reproducibility

8. PyTorch documentation. [torch.set_num_threads](https://docs.pytorch.org/docs/stable/generated/torch.set_num_threads.html).
   - The API controls intra-op CPU parallelism and must be set before eager/JIT/autograd execution. The RONIN-IA records compare inter-op thread settings; a proper benchmark must also record intra-op settings and the order in which thread controls are applied. Do not conflate intra-op and inter-op threads.

## How these references are used

- **Paper 1:** HELM's multi-metric framing; contamination literature for validity threats.
- **Paper 2:** HELM/HELMET's scenario coverage and metric reliability; contamination literature for fixed holdout interpretation.
- **Paper 3:** PyTorch thread-control documentation and compute-scaling literature as background, not as a direct CPU benchmark.
- **Paper 4:** provenance and reproducibility remain primarily grounded in the project's own immutable run, job, and artifact records; this bibliography is supplementary.
- **Paper 5:** contamination methods and compute/token-budget literature; scaling-law claims remain bounded by differences in model size, architecture, and training regime.

All five manuscripts should distinguish external methodological precedent from evidence generated by the project. A citation can motivate a method; it cannot validate a project-specific result.

# CPU-Constrained Training of Small Language Models
## Throughput, parallelism, and engineering trade-offs on hosted CI runners

**Status:** Research draft v0.1 — preliminary benchmark comparison  
**Claim policy:** Benchmark observations are configuration-specific; not general hardware laws.

### Abstract (provisional)
Small language-model experiments are often conducted under strict compute and budget constraints. This paper documents throughput measurements from CPU-based training runs and investigates how thread configuration, model family, and workflow engineering affect practical training speed. A preliminary engineering log records a 100.9M-parameter RONIN-IA experiment completing 500 updates in 383.24 seconds with two inter-op threads (167.0 tokens/s), while a four-thread configuration took 505.14 seconds (126.7 tokens/s). Other records include a 49.1M-parameter MINIRONIN Mamba run and a much larger HERETIC pilot. These heterogeneous observations motivate controlled benchmarking, but cannot establish that fewer threads are universally faster.

### 1. Research questions
1. How does thread configuration affect tokens/s and wall-clock time on a fixed runner?
2. How do model architecture, parameter count, sequence length, batch size, and gradient accumulation interact with throughput?
3. What fraction of end-to-end time is spent in data loading, tokenization, training, checkpointing, and evaluation?
4. Which workflow changes improve reproducibility and reduce wasted compute?

### 2. Preliminary measurements
Source: curated engineering record in MINIRONIN, `data/curated/minironin-performance-engineering-v1.jsonl`.

| Experiment | Reported parameter count | Updates | Wall time | Reported throughput |
|---|---:|---:|---:|---:|
| RONIN-IA, 2 inter-op threads | 100.9M | 500 | 383.24 s | 167.0 tokens/s |
| RONIN-IA, 4 inter-op threads | 100.9M | 500 | 505.14 s | 126.7 tokens/s |
| MINIRONIN Mamba | 49.1M | 1,000 | 1,166.33 s | 54.9 tokens/s |
| HERETIC pilot | ~500M | 50 | 13,096.33 s | 39.1 tokens/s |

The first two measurements are the most promising comparison, but the underlying run manifests must be checked for identical runner type, intra-op threads, sequence length, batch size, precision, data order, and timing boundaries. The remaining rows are not directly comparable because architecture and configuration differ.

### 3. Benchmark protocol
Use paired, randomized benchmark runs on the same runner class. Record:
- CPU model, allocated vCPU count, memory limit, OS image and software versions;
- PyTorch version, BLAS backend, intra-op and inter-op thread counts;
- model parameter count and architecture/config hash;
- batch size, sequence length, gradient accumulation, precision;
- dataset/cache identity and data-loader worker count;
- warm-up steps, measured steps, checkpoint frequency;
- wall time and tokens actually processed, not estimated from nominal batch size;
- peak resident memory, CPU utilization, and failure/restart events.

Run at least three repetitions per configuration when feasible. Report median, spread, and raw run data. Keep data preparation and training throughput separate.

#### 3.1 Additional Mamba continuation record

A MINIRONIN workflow log records a Mamba continuation from 1,000 to 2,000 cumulative steps, with 1,000 additional optimizer steps completed in 1,166.33 seconds. The log reports 49.1M parameters in the curated performance record, a checkpoint at step 2,000 (SHA-256 `4015cf070de7ca58cc3302fa80754308c86ecfc736b78a52eda267dbb441b364`), and a final mean loss over the last 50 steps of 1.9871. The run then failed during a later metadata operation with `KeyError: 'index_sha256'`. This reinforces the need to separate training duration and checkpoint recovery from workflow success.

#### 3.2 Environment and warning capture

The RONIN-IA expansion workflows record `OMP_NUM_THREADS=2` and `MKL_NUM_THREADS=2`. Separate Node.js runtime logs emit DEP0005 warnings for deprecated `Buffer()` usage. These warnings are infrastructure/toolchain observations; they are not evidence of a model-training defect and should not be conflated with Python training failures.

### 4. Engineering factors to investigate
- Thread oversubscription and CPU affinity.
- Data-loader stalls and corpus preloading.
- Tokenization performed inside versus outside the training workflow.
- Checkpoint serialization frequency and compression.
- Gradient accumulation and sequence length.
- Validation/holdout execution in the same job.
- Runner contention and CI host variability.

### 5. Preliminary interpretation
The two-thread RONIN-IA observation was faster than the four-thread observation in the recorded test. This is a useful hypothesis-generating result. It does not establish causality until the complete manifests and repeated runs confirm that all other variables were held constant.

### 6. Limitations
Hosted runners are not stable scientific instruments unless hardware allocation and contention are recorded. Throughput definitions may differ between logs. Parameter counts alone do not predict compute cost across architectures. A tokens/s figure without exact token accounting is insufficient for cross-run comparison.

### 7. Required next steps
1. Recover original workflow YAML and exact logs for both RONIN-IA thread tests.
2. Verify whether tokens/s counts input tokens, target tokens, or total processed tokens.
3. Repeat paired configurations on the same runner image.
4. Separate training-only throughput from end-to-end workflow duration.
5. Add energy measurements only if trustworthy instrumentation is available; otherwise do not estimate energy.
6. Publish scripts and raw machine-readable benchmark records.

### 8. Reproducibility package
`benchmark_manifest.json`, `throughput_runs.csv`, `benchmark.py`, `environment.txt`, and workflow YAML snapshots.

### References to add
PyTorch CPU performance guidance, reproducible systems benchmarking, and relevant literature on efficient training under resource constraints. All external references must be verified before citation.


### 6. What the workflow record can establish

The two RONIN-IA expansion jobs each completed the same high-level pipeline: CPU dependencies installed; function-preserving expansion checked on a small model; the exact 10k parent checkpoint downloaded; six source partitions separately admitted and verified; source hashes asserted; the partitions assembled; the model expanded, trained for 500 steps, screened on MMLU-Pro, and the checkpoint/report uploaded. The two runs have different workflow head commits and artifact digests, but the same experiment label, parent checkpoint SHA, nominal parameter target, step count, and corpus SHA.

This is stronger than a bare timing record because it documents the data and execution path. It is not enough to establish independent replication. A proper replication claim requires checking random seeds, initialization of newly introduced parameters, runner identity, library versions, and whether the two artifacts differ only in nondeterministic training state or in source/configuration. Until then, call them two executions of the same experiment specification.

### 7. CPU comparison: a cautious interpretation

The existing performance record reports 167.0 tokens/s at two inter-op threads and 126.7 tokens/s at four, for nominally the same 100.9M-parameter model and 500 updates. The two-thread run took 383.24 seconds; the four-thread run took 505.14 seconds. In this pair, four threads were approximately 32% slower in wall time (or about 24% lower throughput).

This is a within-record contrast, not a general CPU-scaling law. The runner model, physical-core allocation, intra-op thread count, BLAS configuration, CPU contention, warm-up, and exact artifact identity must be matched before attributing the difference to inter-op threads. The next benchmark should randomize run order and repeat each setting at least three times on the same runner class, reporting median and dispersion rather than one timing.

### 8. Practical reporting template

For each CPU run, report runner image and CPU model if exposed; Python/PyTorch/NumPy versions; OMP_NUM_THREADS, MKL_NUM_THREADS, intra-op and inter-op counts; batch and sequence dimensions; context length; gradient accumulation; precision; optimizer steps; processed tokens; wall time excluding and including setup; checkpoint time; evaluation time; and artifact size. Keep corpus download and tokenization times separate from steady-state training throughput.

### 9. Limitations

The current measurements come from hosted CI runners and a small number of runs. They do not establish a hardware-independent optimum, and throughput per second is not comparable across architectures unless the counted token unit and workload are identical. Parameter count alone is not a sufficient normalization for CPU cost.

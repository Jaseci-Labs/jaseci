# Jac matmul: original, optimized, and handwritten CUDA

The primary comparison has exactly three implementations. Both Jac columns use the **same Predicted packed graph layout**, lane order, inputs and launch geometry. The optimized column adds the **standard LLVM O2 middle-end pipeline** to the identical raw production LLVM module, verifies it, then emits PTX with the existing target machine. It retains the complete walker ABI, queues, type dispatch, arithmetic/bounds checks and status behavior. The scripts provide an explicit reproducible experimental compilation path; the production compiler keeps its current behavior.

**Original Jac** uses the production backend and its existing target-machine optimization/code generation settings. **Optimized Jac** adds the checked LLVM O2 middle-end experimentally. **Handwritten** uses the same `matmul_tiled_i64` 16×16 shared-memory kernel across all five shapes, including the ragged cases.

## Primary result: resident, actual kernel time

Microseconds per kernel, median Nsight Systems `end - start`. All three columns come from **one interleaved run**, `codegen/paired-profile`, with randomized arm order in each round (seed 928), 3 warmup rounds and 15 measured rounds × 16 graph nodes per arm/case. Each cell contains 240 measured kernel samples. These durations exclude GPU graph scheduling gaps, CPU work, allocations and transfers.

| M × K × N | Jac original | Jac with checked LLVM O2 | Handwritten tiled CUDA |
|---|---:|---:|---:|
| 3 × 5 × 2 | 8.384 | 7.264 | 1.568 |
| 17 × 31 × 19 | 52.736 | 45.216 | 2.176 |
| 64 × 128 × 64 | 183.745 | 155.872 | 4.704 |
| 128 × 128 × 128 | 228.113 | 164.577 | 4.832 |
| 256 × 256 × 256 | 2112.666 | 533.938 | 20.544 |

At 256³, compiler optimization gives **3.96×** speedup. Checked optimized Jac remains **25.99×** slower than the fixed handwritten tiled kernel. Both Jac measurements retain the full production graph execution contract.

Download the [compact CSV](primary/comparison.csv), [comparison JSON with exact source hashes](primary/comparison.json), and three concrete datasets: [original Jac](primary/jac_original.json), [checked optimized Jac](primary/jac_optimized.json), [handwritten CUDA](primary/handwritten.json). Each dataset includes individual profiler samples and the separate ordinary-event samples. The source-run identifiers and SHA-256 hashes identify the exact interleaved run for every sample.

## Why the original kernel is slow: supported findings

1. **A removable compiler cost is established.** Production emission verifies LLVM and emits PTX directly through the existing target machine. The raw cursor lowering places ten fixed scalar allocas in `start`, after the lane-bound branch. SROA alone leaves IR/PTX unchanged (identical PTX SHA-256). Hoisting only those nonescaping fixed allocas to `entry` and running SROA removes all ten allocas and all 20 static local loads plus 20 static local stores in PTX. This checked ablation nearly reproduces O2 performance. Actual driver-JIT function attributes change from 80 local bytes and 28 registers per thread to zero local bytes and 40 registers, confirming that the static assembly observation applies to the loaded kernels. Offline `ptxas` reports zero spill loads/stores in every variant: the original frame is explicit local storage, with zero register spills reported.

2. **General graph execution remains after compiler optimization.** O2 executes generic per-cursor FIFO traversal, CSR offset/target lookups, type dispatch, overflow and validation paths. Restricted chain controls execute much faster on regular layouts, but they accept a narrower contract and use a different compiler. Their measured speedups compare those complete implementations; attribution to queues and checks individually remains unresolved.

3. **Checks have interacting, layout-dependent effects.** Separate LLVM ablations bypass only overflow errors, only graph/limit errors, or both. Some improve regular layouts; removing all checks actually slows the random layout in this experiment. These transformations alter subsequent optimization and register allocation. The timings compare complete generated implementations; attribution to individual check costs remains unresolved. The checked optimized variant retains the production safety contract.

4. **Traversal representation matters, with non-monotonic controls.** Replacing CSR with one successor per node speeds the restricted chain kernel. A precomputed index schedule is faster than that successor kernel on Random928 but slower on regular layouts. The schedule also changes index organization and loop termination. Hardware-level attribution to cache misses, coalescing, occupancy and dependent-load latency remains unresolved.

The [supplementary ablation report](codegen/ABLATIONS.md) gives every controlled change, its restricted contract, all five shapes and all layouts. The [earlier dense baseline report](DENSE_BASELINES.md) retains the original pre-ablation comparison.

## Independent correctness and measurement checks

- Real Jac Scalar/RowNext/ColumnNext objects were packed by the production packer. Each node stores one int64 value. The saved input manifest and every binary array hash are checked. Every cursor chain is walked on the CPU and checked against the dense A/B matrices before GPU measurement.
- All five shapes compute the full M×N output, including negative values and ragged dimensions, with a NumPy int64 oracle. |A| ≤ 3, |B| ≤ 5 and |partial sum| ≤ 15K, so products and partial sums fit signed int64. Dense CUDA uses these same values and int64 arithmetic.
- Before every graph replay, output is poisoned with the bitwise complement of its expected value and status with `0xffffffff`, outside timing. After each replay all outputs are checked; every Jac/graph-control lane must return zero status.
- The primary profiler join verified all **11,560** launches, including prime and warmup launches; **9,600** were measured. The separate ablation join verified **43,350** launches; **36,000** were measured. Every name, order, grid and block matches the runner request. `--cuda-graph-trace=node` was used in both runs.
- Thirteen valid/error fixtures × three checked variants (baseline/O2/hoist+SROA), 39 standalone GPU launches, match the unmodified production host LLVM JIT exactly on output and status. Cases include multiply and add overflow, negative/out-of-range heads, invalid edge target, negative/overlarge CSR offsets, seed/branch queue overflow, cyclic round limit, type mismatch and empty channel. Failing lanes leave the poisoned result untouched. See [status validation](codegen/status-validation.json).
- The existing named-cursor CPU/JIT suite passes all 15 tests, including FIFO branching/repeated arrivals, conditional visitation, reports, cycles, overflow, shared matmul inputs and dynamic cursor counts. This is supporting coverage of the unchanged backend; the direct 39 GPU comparisons exercise the checked experimental variants.

## Separate ordinary CUDA-event cross-check

Same three groups, from `codegen/paired-ordinary`: 5 warmup and 25 measured rounds, 16 graph nodes per replay. Microseconds per invocation; these event intervals **include** GPU graph scheduling gaps. The primary table uses the separately measured actual kernel durations.

| M × K × N | Jac original | Jac with checked LLVM O2 | Handwritten tiled CUDA |
|---|---:|---:|---:|
| 3 × 5 × 2 | 8.492 | 7.342 | 1.714 |
| 17 × 31 × 19 | 52.864 | 45.376 | 2.304 |
| 64 × 128 × 64 | 184.960 | 159.470 | 4.992 |
| 128 × 128 × 128 | 231.488 | 169.792 | 5.120 |
| 256 × 256 × 256 | 2080.512 | 553.728 | 20.736 |

## Environment and reproduction

RTX 3090, driver 580.65.06, CUDA 12.9 nvcc/ptxas, bundled Jac LLVM with NVPTX. Ollama held approximately 23,462 MiB in the before/after snapshots; only about 370 MB was free after our context. These are **shared-GPU measurements**. Per-run before/after snapshots are embedded in `results.json`. Nsight instrumentation and shared GPU state can shift absolute timing; primary ratios use one interleaved run and the ordinary cross-check is separate.

Run [reproduce_codegen.sh](../../reproduce_codegen.sh) from the repository root to regenerate LLVM/PTX, both timing runs, profiler joins, error/status validation and report exports. GPU access is required. The original input arrays are reused unchanged. The script uses the current runner; the exact source revisions used by the earlier primary run are also saved as `codegen/paired-benchmark.py` and `codegen/paired-analyze_profile.py`, with hashes checked by the report generator. [commands.txt](codegen/commands.txt) records the invocation sequence and experimental identities.

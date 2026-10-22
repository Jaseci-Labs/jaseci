# Jac GPU layout: checked O2 Random before, Predicted after, tiled CUDA reference

Access-order-aware layout changes the 256³ Jac median from 947.380 to 540.418 µs: **1.753× faster**. The remaining Predicted / tiled CUDA gap is **26.10×**. Predicted regresses on the two smallest cases and improves the three larger cases across all three fixed random seeds.

## Primary policy and exact invariants

- **Jac before (Random928 + checked LLVM O2):** shuffled physical node IDs, consistently remapping fields, CSR rows/targets, heads and initialized queues.
- **Jac after (Predicted + identical checked LLVM O2):** complete cursor-a discovery BFS followed by complete cursor-b discovery BFS, preserving first occurrence: all A nodes, then all B nodes.
- **Handwritten CUDA reference (nvcc O3):** fixed `matmul_tiled_i64` 16×16 shared-memory tiled int64 kernel for every size, covering the same logical matrices and all outputs.

The Jac independent variable is **node layout only**. Both Jac arms reuse one loaded function and byte-identical checked O2 PTX. Source, arithmetic, logical graph identities/values/edges, lane order, walker-to-thread mapping, queue capacity, visit bound, initial state, output coverage and launch geometry are fixed. Jac uses block=(128,1,1), grid=(ceil(MN/128),1,1); CUDA uses block=(16,16,1), grid=(ceil(N/16),ceil(M/16),1).

Jac receives the standard LLVM O2 middle-end pipeline on the exact production raw module, followed by the existing target codegen. The reference receives nvcc `-O3 -arch=compute_86 -std=c++17`. Both receive regular optimizing pipelines; LLVM O2 and nvcc O3 are distinct pipelines with different optimization guarantees. The explicit checked O2 compilation path is experimental. The [research contract](../../RESEARCH_CONTRACT.md) and its recorded hash define the primary policy.

**Checked O2 PTX SHA-256:** `c24fea17965d672cdd2030704345307e07a3b386b44e64b62a1e9adc767fae81`. The [emitter](../../emit_checked_o2.py) first verifies that production emission matches the saved production PTX (`dda413df1e70f3f1c255b70b66b869dce57ea835b25229924a79d4755b4f22aa`), then optimizes that same raw LLVM. [Codegen provenance](optimized-codegen/codegen.json) includes IR/compiler hashes and offline ptxas output: zero stack bytes, zero spills, 40 registers. Safety checks/status paths are retained.

## Fresh primary result: full output coverage

**Median actual Nsight node-kernel end−start, microseconds.** All cells come from one randomized interleaved `optimized-profile` run. Random928 is the prespecified primary seed; Random929/930 provide supporting repetitions in the same run. Each cell contains 240 measured nodes (15 rounds × 16 sequential graph nodes), after three warmup rounds. Independent arm-order seed: 237.

| M × K × N | Jac before: Random928 + O2 | Jac after: Predicted + O2 | Handwritten tiled CUDA O3 | Layout speedup before/after | Residual gap after/reference |
|---|---:|---:|---:|---:|---:|
| 3 × 5 × 2 | 6.272 | 7.232 | 1.568 | 0.867× | 4.61× |
| 17 × 31 × 19 | 42.304 | 45.152 | 2.208 | 0.937× | 20.45× |
| 64 × 128 × 64 | 200.929 | 180.865 | 5.440 | 1.111× | 33.25× |
| 128 × 128 × 128 | 187.265 | 164.032 | 4.832 | 1.142× | 33.95× |
| 256 × 256 × 256 | 947.380 | 540.418 | 20.705 | 1.753× | 26.10× |

[Compact CSV](comparison.csv) · [JSON with exact source-run hashes](comparison.json) · [all actual kernel samples and launch join](optimized-profile/verified.json). Every kernel covers the full M×N output workload.

The independent launch audit matched **7,225** launches, including primes and warmups, with **6,000** measured nodes; 3,600 measured nodes belong to the three primary groups. Every kernel name, order, grid, block and graph-node position matches the request. Nsight uses `--cuda-graph-trace=node`.

### Variability and fixed seeds

| Shape | Random928 / Predicted | Random929 / Predicted | Random930 / Predicted |
|---|---:|---:|---:|
| 3 × 5 × 2 | 0.867× | 0.956× | 0.929× |
| 17 × 31 × 19 | 0.937× | 0.937× | 0.934× |
| 64 × 128 × 64 | 1.111× | 1.110× | 1.112× |
| 128 × 128 × 128 | 1.142× | 1.139× | 1.139× |
| 256 × 256 × 256 | 1.753× | 1.757× | 1.721× |

All three fixed seeds give the same direction at every size. [Seed data](seed-robustness.json) include each round’s paired mean ratio. [Variability data](variability.json) retain p10/p90, minima/maxima and separate ordinary-event medians; raw traced samples are retained.

| 256³ primary group | p10 µs | median µs | p90 µs |
|---|---:|---:|---:|
| Jac before (Random928 + checked LLVM O2) | 920.452 | 947.380 | 971.908 |
| Jac after (Predicted + checked LLVM O2) | 537.698 | 540.418 | 542.306 |
| Handwritten CUDA reference (nvcc O3) | 20.512 | 20.705 | 20.960 |

The separate ordinary-event run uses 5 warmup rounds and 25 measured rounds × 16 nodes, checking every replay. Its 256³ medians are 940.096 / 548.608 / 20.800 µs, giving 1.714× layout speedup. All five sizes have the same direction as the primary trace. Event intervals include graph scheduling gaps and come from a separate run; primary ratios use actual kernel times from `optimized-profile`.

## Full semantics and identity checks

The saved fixtures originate from real Jac Scalar/RowNext/ColumnNext objects and the production packer. Canonical discovery identities anchor the remapping. Predicted is independently reconstructed from complete lane chains as all-A BFS then all-B BFS. Each permutation is a full bijection. Every field/tag, CSR row/target, head and initialized queue is checked against the canonical graph, and every q/cursor/lane arrival is checked for the same logical identity. Array and permutation SHA-256 hashes are saved. The runner repeats these audits before GPU execution.

Before every replay, outside timing, output is poisoned with the bitwise complement of its expected value and Jac status with `0xffffffff`. Every M×N result is checked against independent NumPy int64 A@B and the saved full-output oracle; every Jac status must be zero. Input magnitudes bound every product by 15 and every partial sum by 15K. Supporting random seeds receive the same checks.

The identical O2 artifact also passed the earlier direct GPU [status validation](../../../handwritten_matmul/validation/20261021/codegen/status-validation.json), SHA-256 `bea7ec93a379cfd9913cf2fb6728867efa3710d8fe1d527ef85e0ff530f11d05`: 13 fixtures covering multiply/add overflow, round-limit cycles, queue capacity, invalid heads/targets/CSR, type mismatch, empty channel and valid execution. Each matched the production host JIT’s exact result/status; baseline, O2 and checked hoist+SROA totalled 39 passing executions. This report verifies the O2 artifact hash against that evidence. Fresh normal-case replays verify all outputs/statuses for every layout.

## Measured layout effect and address evidence

The controlled Random/Predicted timing difference establishes the layout effect under this workload and shared GPU context. The residual gap to tiled CUDA compares complete implementations: the graph kernel retains traversal queues, CSR lookup, dispatch and checks, while tiled CUDA uses dense indexing and cooperative shared-memory reuse. Component contributions to that whole-implementation gap remain unresolved.

The corrected O2 Nsight Compute probe requested `l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum` and returned **ERR_NVGPUCTRPERM**, exit 1. [Exact log](counters/o2-ncu.log) and [status](counters/o2-status.json) retain the access limitation. The probe is separate from primary timings.

The [deterministic address analysis](optimized-address-analysis.json) uses the exact layouts and actual 256-byte-aligned device array bases from the primary run. For each q, cursor and logical value/tag/CSR load, it counts distinct 32-byte address segments per logical warp access, merges duplicate lane addresses, and retains per-q statistics, count-vector hashes and example adjacent-lane addresses. These are deterministic address counts. Hardware transactions, cache misses and occupancy remain unmeasured; compiler load transformations and cache state are outside this model.

| 256³ logical warp access: mean distinct 32-byte segments | Random928 | Predicted |
|---|---:|---:|
| cursor a: value | 1.000 | 1.000 |
| cursor b: value | 31.987 | 8.000 |
| cursor b: csr_begin | 31.985 | 9.000 |
| cursor b: csr_end | 31.982 | 9.000 |
| cursor b: csr_target | 31.969 | 8.000 |

At N=256 a warp covers one row i and 32 adjacent columns j. Cursor a shares one A-node address across the warp in either layout. Cursor b visits 32 distinct nodes; Predicted places them consecutively, giving eight value-address segments versus about 32 with Random928. CSR begin/end indexing also includes the channel-row offset. Jac’s known cursor order therefore supports a concrete, reproducible address organization. Timings show useful speedup for larger cases and regression for small cases; the hardware mechanism behind those differences remains unresolved.

## Shared GPU and timing boundary

RTX 3090, driver 580.65.06, CUDA 12.9. Ollama held approximately 23,462 MiB in the before/after snapshots. The process measured 357.83 MB free after context creation. The largest planned allocation for the five arms was 40.35 MB. Each case checks current free VRAM and releases buffers before the next case. Full snapshots and allocation plans are in `optimized-profile/results.json` and `optimized-ordinary/results.json`.

Resident actual kernel intervals cover computation. Packing/remapping, compilation, allocation, transfers, output poisoning, verification and graph scheduling gaps are separate from this metric. Layout-construction cost is outside the resident-kernel measurement; the production input provenance and remapping scripts are retained. Absolute durations reflect this shared GPU context.

## Supplementary production-PTX history and 3000³ feasibility

The earlier [production-PTX confirmation](production-PTX-REPORT.md) and [same-trace pilot](../../pilot/comparison.json) are supplementary history using production emission before the added LLVM middle-end. The pilot’s 256³ Random928 / Predicted / tiled values were 4486.394 / 2069.116 / 20.608 µs. These data retain their own hashes, contract and source snapshot. The corrected primary table uses checked O2 for both Jac layouts and the new `optimized-profile` trace.

Historical 3000³ correctness covered **9,000,000 outputs**, with 27 billion multiply-accumulates. Separate historical actual timings covered **32,768 outputs per resident launch**: Random 70.802 ms, Predicted 8.973 ms, 7.891× subset speedup. That run has its own older PTX/data and no handwritten reference. Full-result correctness and subset timing are separate evidence.

One 3000³ packed graph requires 719.95 MB, exceeding the measured 357.83 MB free. Two layouts, dense full A/B/C, and bounded 32,768-query Jac buffers require approximately 1.66 GB before additional JIT/allocation headroom. Dense A/B/C alone occupy 216 MB. The historical temporary raw directory is currently absent; checked-in summaries, audits, hashes and source remain available.

A matched full-coverage 3000³ follow-up can use a GPU/session with sufficient free VRAM, retain the paired graphs, execute all 275 bounded Jac batches covering nine million outputs, and compare aggregate actual kernel time with the fixed tiled reference over the same outputs. A matched 32,768-output subset study needs a tiled reference covering that exact selection and explicit subset labeling. Paging/partitioning introduces an out-of-core question. [Scale record and historical hashes](scale-3000-feasibility.json) preserve the resource and coverage boundary.

## Reproduction and artifacts

[Reproduction script](../../reproduce.sh) · [runner](../../run.py) · [input/permutation audit](../../prepare.py) · [checked O2 emitter](../../emit_checked_o2.py) · [profiler join](../../analyze.py) · [address analysis](../../address_analysis.py). The [English PDF](../../../../../docs/presentations/jac-gpu-layout/jac-gpu-layout.pdf) is generated from the verified comparison and contract. The optional subtree capture is retained with its paused status; matmul supplies this report’s primary results.

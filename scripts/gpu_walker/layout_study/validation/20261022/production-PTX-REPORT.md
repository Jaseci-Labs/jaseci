# Supplementary production-PTX layout experiment

This archived experiment uses the production PTX without the added LLVM O2 middle-end. The corrected primary comparison is [REPORT.md](REPORT.md), with checked LLVM O2 in both Jac arms. The measured contract snapshot is [production-RESEARCH_CONTRACT.md](production-RESEARCH_CONTRACT.md).

# Jac GPU node layout: Random before, Predicted after, CUDA reference

The Jac independent variable is **node layout only**. Access-order-aware Predicted regresses on the two smallest full-matmul cases and improves the three larger cases across all three fixed random seeds. At 256³, the primary Random928/Predicted speedup is 2.063×; the remaining Predicted/tiled-CUDA reference gap is 103.40×.

## Contract and primary implementations

- **Jac before (Random928):** shuffled physical node IDs, with consistent field/CSR/target/head/seed-queue remapping.
- **Jac after (Predicted):** complete cursor-a discovery BFS followed by complete cursor-b discovery BFS, preserving first occurrence: all A nodes, then all B nodes.
- **Handwritten CUDA reference:** the fixed `matmul_tiled_i64` 16×16 shared-memory kernel on the same logical int64 matrices and all outputs.

Both Jac arms use the same loaded production function and byte-identical PTX (`dda413df1e70f3f1c255b70b66b869dce57ea835b25229924a79d4755b4f22aa`). Jac source, arithmetic, graph identities/edges, lane order, walker-to-thread mapping, queue/visit limits and launch geometry are fixed. Both launch 128 threads per block and ceil(MN/128) blocks. The reference uses its fixed 16×16 geometry and the same M,K,N inputs; its algorithm and launch geometry provide the performance target.

The [research contract](../../RESEARCH_CONTRACT.md) defines these invariants and acceptance checks. The report generator checks the three primary labels, common PTX/source hash, one loaded Jac function, Jac geometry, input/permutation hashes, logical traversal audits and profiler joins before export. Compiler optimization is fixed throughout the Jac layout pair.

## Fresh primary result: full output coverage

Median actual Nsight kernel end−start in **microseconds**, from one randomized interleaved `profile` run. Random928 is the prespecified primary seed; Random929/930 are supporting repetitions in the same run. Each cell contains 240 measured kernel nodes (15 rounds × 16 nodes), after three warmup rounds. Arm order is randomized independently of the layout seeds, with order seed 237.

| M × K × N | Jac before (Random928) | Jac after (Predicted) | Handwritten CUDA reference | Layout speedup before/after | Residual gap after/reference |
|---|---:|---:|---:|---:|---:|
| 3 × 5 × 2 | 7.264 | 8.224 | 1.568 | 0.883× | 5.24× |
| 17 × 31 × 19 | 49.313 | 52.609 | 2.176 | 0.937× | 24.18× |
| 64 × 128 × 64 | 230.881 | 212.753 | 5.440 | 1.085× | 39.11× |
| 128 × 128 × 128 | 316.289 | 228.081 | 4.832 | 1.387× | 47.20× |
| 256 × 256 × 256 | 4,435.973 | 2,150.666 | 20.800 | 2.063× | 103.40× |

[Compact CSV](comparison.csv) · [JSON with exact source-run hashes](comparison.json) · [sample distributions and profiler join](profile/verified.json). Durations include each full M×N kernel workload. The primary ratios use this one trace.

### Fixed-seed robustness

| Shape | Random928 / Predicted | Random929 / Predicted | Random930 / Predicted |
|---|---:|---:|---:|
| 3 × 5 × 2 | 0.883× | 0.961× | 0.938× |
| 17 × 31 × 19 | 0.937× | 0.940× | 0.934× |
| 64 × 128 × 64 | 1.085× | 1.098× | 1.090× |
| 128 × 128 × 128 | 1.387× | 1.381× | 1.356× |
| 256 × 256 × 256 | 2.063× | 2.057× | 2.092× |

All three seeds give the same direction for every size. [Supporting seed data](seed-robustness.json) retain per-round paired mean ratios; raw profiler samples retain p10/p90 and extrema. The separate ordinary-event run corroborates regression on the small cases and improvements on the larger cases. Its CUDA-event graph interval includes GPU graph scheduling gaps.

## Exact layout and semantics checks

The source fixtures were built from real Jac Scalar/RowNext/ColumnNext objects and the production packer. Saved canonical discovery identities anchor the remapping. The Predicted permutation is independently reconstructed from complete lane cursor chains and checked against all-A BFS then all-B BFS. Each saved permutation is a full bijection; field values/tags, every CSR row and target, heads and initialized queue are checked against that canonical graph. Each q/cursor arrival in every lane is checked for the same logical identity. Arrays and identity permutations have SHA-256 hashes.

Every replay poisons output with the bitwise complement of its expected int64 value and Jac status with `0xffffffff`, outside timing. All M×N outputs are checked against independent NumPy int64 A@B and the saved oracle, and every Jac status must be zero. Input magnitudes guarantee |partial sum| ≤ 15K. The same checks apply to each supporting random seed.

Nsight launch audit: **7,225** nodes verified, **6,000** measured including seed controls; 3,600 measured nodes belong to the primary three groups. Every name, order, grid, block and graph-node position matches the runner request, including primes and warmups. `--cuda-graph-trace=node` provides actual per-node durations.

## Address evidence and hardware-counter limitation

The Nsight Compute request for `l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum` returned **ERR_NVGPUCTRPERM**, exit 1. [Exact log](counters/ncu.log) and [status](counters/status.json) preserve the attempted collection. The counter-probe timing is excluded from the primary data.

The [deterministic address analysis](address-analysis.json) uses the exact saved layouts and actual 256-byte-aligned device array bases from the primary run. For every q, cursor and logical load it counts distinct 32-byte address segments within each logical warp access. It preserves those dimensions separately and records per-warp count hashes plus example adjacent-lane addresses. This is an address quantity; hardware transactions, cache misses and occupancy remain unmeasured. Compiler instruction transformations and cache state are outside the model.

| 256³ logical warp access, mean distinct 32-byte segments | Random928 | Predicted |
|---|---:|---:|
| cursor a: value | 1.000 | 1.000 |
| cursor b: value | 31.987 | 8.000 |
| cursor b: csr_begin | 31.985 | 9.000 |
| cursor b: csr_end | 31.982 | 9.000 |
| cursor b: csr_target | 31.969 | 8.000 |

At N=256 a warp covers one row i and 32 adjacent columns j. Cursor a therefore shares one A-node address across that warp in both layouts. Cursor b has 32 distinct node addresses; Predicted places those B nodes consecutively, giving eight value-address segments instead of about 32. CSR begin/end indexing also includes the channel-row offset. This establishes the address organization enabled by the traversal order. The timing evidence establishes the measured layout benefit and small-case regressions; their hardware causes remain unresolved.

## Shared GPU and measurement boundary

RTX 3090, driver 580.65.06, CUDA 12.9. Ollama held approximately 23,462 MiB in before/after snapshots. The primary process measured 357.83 MB free after context creation. Each case checks its allocation against current free VRAM and releases buffers before the next case. Snapshots and planned allocation bytes are stored in `profile/results.json` and `ordinary/results.json`.

Actual kernel timing excludes packing/remapping, compilation, allocations, transfers, output poisoning, verification and graph scheduling gaps. The ordinary event samples are separate. Layout construction cost is outside the resident-kernel question here; the source packer and all remapping scripts are retained for reproduction.

## Same-trace pilot and 3000³ scale assessment

The urgent [pilot](../../pilot/comparison.json) extracts Random928, Predicted and fixed tiled CUDA from the same earlier verified trace. At 256³ it measured 4486.394 / 2069.116 / 20.608 µs, a 2.168× layout speedup. Source paths and complete SHA-256 hashes are saved with that pilot; the fresh table above uses the new confirmation trace.

Historical 3000³ correctness covered **9,000,000 outputs** and 27 billion multiply-accumulates. The separate historical resident timing covered **32,768 outputs per launch**: Random 70.802 ms versus Predicted 8.973 ms, a 7.891× subset speedup. That historical run has no handwritten timing reference and uses its recorded older PTX/data. These values are explicitly subset timings, separate from full-result correctness and from the new primary table.

Current resource assessment: one 3000³ packed graph requires 719.95 MB, exceeding the measured 357.83 MB free. Two layouts plus dense A/B/C and bounded 32,768-query Jac private buffers require about 1.66 GB before additional allocation/JIT headroom. Dense A/B/C alone occupy 216 MB. The historical temporary raw directory is currently absent; checked-in summaries, hashes, audit and source remain available.

A matched full-coverage 3000³ follow-up can use a GPU/session with sufficient free VRAM, retain one Random and one Predicted graph, execute all 275 bounded Jac batches covering 9 million outputs, and compare aggregate actual kernel durations with the fixed tiled reference covering the same outputs. A matched 32,768-output subset study would need a tiled reference with exactly that output selection and explicit subset labeling. Paging or graph partitioning would introduce an out-of-core execution question. [Feasibility record and historical source hashes](scale-3000-feasibility.json) preserve the boundary.

## Artifacts and reproduction

The [runner](../../run.py), [input/permutation audit](../../prepare.py), [profiler join](../../analyze.py), [address analysis](../../address_analysis.py), [research contract](../../RESEARCH_CONTRACT.md) and [reproduction script](../../reproduce.sh) are scoped to this layout study. The [English PDF](../../../../../docs/presentations/jac-gpu-layout/jac-gpu-layout.pdf) is generated directly from the checked comparison and contract.

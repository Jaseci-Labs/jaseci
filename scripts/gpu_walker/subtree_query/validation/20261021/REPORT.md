# Batched subtree query on Jac GPU

Original production Jac CSR and the fixed checked handwritten per-query CSR kernel have similar timings across this sweep. The experimental checked LLVM O2 path is usually slower. This backend already uses phi nodes for its state and has zero allocas/local stack storage. The measured result differs from the earlier named-cursor matmul promotion result.

## Query and implementations

Each independent query starts at its root, includes that root, and visits every descendant in FIFO order. A node qualifies when `amount >= threshold`. The query returns the qualifying count, signed int64 amount sum, OR of alerts on qualifying nodes, total visited count and retained threshold. Queries share a read-only tree and maintain private state and queues.

The three primary groups use exactly the same saved production-packed CSR arrays, roots, thresholds, queue capacity and 128-thread per-query lane mapping. Immutable GPU pointers are shared across arms; outputs, status and FIFO scratch are private.

- **Original Jac:** the existing single-cursor CSR lowering and target-machine code generation settings.
- **Checked optimized Jac:** the identical raw LLVM module, standard LLVM O2 middle-end, verification and the same target emission. The experimental path preserves all production checks and status handling.
- **Handwritten CUDA:** one thread per query, the same CSR edge traversal and predicates, slot-major circular FIFO (`queue[slot * queries + lane]`), bounded visits/queue and checked int64 updates. The same kernel is used for every workload.

## Primary three-way comparison

Median resident **actual GPU kernel duration**, microseconds. All cells come from the single interleaved randomized `profile` run, with 3 warmup and 15 measured rounds, 8 sequential CUDA graph nodes per replay, and 120 measured kernel samples per cell. Seed 928. Nsight uses `--cuda-graph-trace=node`; its end−start intervals measure each actual kernel.

| Workload | Queries | Original Jac | Checked Jac + O2 | Handwritten CUDA |
|---|---:|---:|---:|---:|
| ragged37-mixed33 | 33 | 17.504 | 18.208 | 17.568 |
| binary511-root32 | 32 | 241.249 | 263.233 | 244.513 |
| binary511-mixed256 | 256 | 173.217 | 184.513 | 175.233 |
| binary4095-root16 | 16 | 2,020.425 | 2,174.922 | 2,048.041 |
| binary4095-mixed256 | 256 | 2,055.066 | 2,244.346 | 2,076.489 |
| binary4095-leaf1024 | 1024 | 1.921 | 1.952 | 1.920 |
| binary4095-small1024 | 1024 | 3.488 | 3.456 | 3.392 |
| ternary3280-root16 | 16 | 1,651.336 | 1,766.296 | 1,671.896 |
| quaternary4093-mixed128 | 128 | 2,044.729 | 2,203.402 | 2,069.994 |
| chain2048-mixed32 | 32 | 748.580 | 789.028 | 755.396 |
| irregular4095-mixed128 | 128 | 1,651.208 | 1,863.513 | 1,672.072 |
| irregular16383-mixed256 | 256 | 8,271.240 | 8,938.796 | 8,365.000 |
| binary1023-root1 | 1 | 403.202 | 441.122 | 408.866 |
| binary1023-root32 | 32 | 488.354 | 524.995 | 493.634 |
| binary1023-root128 | 128 | 517.443 | 557.795 | 523.235 |
| binary1023-root128-all | 128 | 507.091 | 547.811 | 512.963 |
| binary1023-root128-none | 128 | 469.122 | 458.386 | 448.322 |

Across the 17 cases, handwritten/original median-time ratios range from 0.956× to 1.014×; checked O2/original ranges from 0.977× to 1.129×. Lower time is faster. The 16,383-node irregular mixed batch takes 8.271 ms original Jac, 8.939 ms checked O2 and 8.365 ms handwritten in this run.

[CSV](primary/comparison.csv) · [compact JSON with source identifiers and hashes](primary/comparison.json) · [original dataset](primary/original.json) · [checked O2 dataset](primary/optimized.json) · [handwritten dataset](primary/handwritten.json). Individual durations, p10/p90, extrema, per-round means and ordinary-event samples are preserved in the datasets and raw results.

## Measured explanation

### The CSR backend already carries state in SSA

Inspection starts from `ptx_csr.lower_csr`, independently of the named-cursor backend. FIFO read/write positions, pending/step counters and the five query states are LLVM phi values. Original CSR has zero allocas; SROA-only emits byte-identical PTX. Original and O2 both have zero PTX local loads/stores and zero stack/spill bytes in ptxas. Actual driver-JIT attributes confirm zero local bytes; original uses 38 registers, O2 40 and checked handwritten 40.

O2 changes control flow and static instruction sites (global stores 13→8; global loads remain 12) while retaining all checks. Its elapsed-time result is usually a slowdown here. Static site counts and register counts describe generated code; the hardware mechanism behind this timing difference remains unresolved.

### Full traversal, batch size and predicate work

The general FIFO algorithms visit every subtree node even when the predicate rejects all nodes. The exact full workload is checked, including visited count. A mixed batch can contain one full-root traversal plus many short subtree queries; the query visit distribution is recorded below. Across heterogeneous batches, both total visits and per-query lengths change, so they are reported together.

The controlled 1-query versus 128-query all-match contrast uses byte-identical graph arrays, root 0, threshold −1001 and identical per-query results. Original Jac takes 403.202 versus 507.091 µs: 128× as many node visits in 1.26× the latency. This measures the batched execution benefit for this graph and kernel.

All-match and no-match 128-query controls also reuse byte-identical graph arrays and roots. Both visit 130,944 nodes. Original Jac takes 507.091 versus 469.122 µs; checked O2 takes 547.811 versus 458.386 µs. The predicate changes count/sum/alert work while traversal volume stays fixed.

### Check and FIFO-layout ablations

A separate interleaved eight-arm trace holds each workload fixed. LLVM diagnostic variants bypass overflow, graph/limit checks, or both before O2. Their contract is the validated finite tree inputs, zero initial accumulators, exact sufficient queue/visit bounds and proven int64 sums. Checked kernels additionally handle the invalid-input/error fixtures. CUDA unchecked uses the same restricted benchmark inputs.

CUDA query-major retains the full checks and traversal while changing scratch addressing to `queue[lane * capacity + slot]`. This changes address generation and physical scratch layout together.

| Supplementary workload | Checked O2 | O2 no overflow | O2 no validation | O2 unchecked | CUDA checked | CUDA unchecked | CUDA query-major |
|---|---:|---:|---:|---:|---:|---:|---:|
| binary4095-mixed256 | 2,261.101 | 1,858.986 | 1,992.042 | 1,596.760 | 2,092.875 | 1,521.273 | 1,503.304 |
| irregular16383-mixed256 | 8,994.934 | 7,437.516 | 7,764.303 | 6,262.919 | 8,418.995 | 6,081.862 | 6,391.512 |
| binary1023-root1 | 444.131 | 350.434 | 375.395 | 285.122 | 411.715 | 275.521 | 398.274 |
| binary1023-root128-all | 551.203 | 456.930 | 484.131 | 391.939 | 516.452 | 380.579 | 574.180 |
| binary1023-root128-none | 461.235 | 427.235 | 394.547 | 362.322 | 451.395 | 349.378 | 509.123 |

Removing selected checks speeds these whole generated implementations on the listed inputs. The variants are optimized independently, so the differences describe each experiment’s combined generated-code effect. Per-check additive cost percentages remain unresolved.

Query-major scratch is faster for the two listed mixed-subtree workloads and slower for the uniform 128-query full-root workloads. The ordinary-event ablation run corroborates these directions. Hardware attribution to cache, coalescing, occupancy and memory transactions remains open; this evidence consists of timing traces, source-controlled transformations and static/driver codegen attributes.

## Workloads and VRAM planning

All 632,829 query-node visits in the 17 complete workloads are checked against both serial Jac and an independent queue-based Python oracle. Trees include balanced binary/ternary trees, ragged binary/quaternary trees, a 2,048-node chain, and irregular bounded-degree trees. Amounts span −1000…1000; thresholds include all-match, partial-match and no-match cases. Leaves and short subtrees exercise varied query lengths.

| Workload | Tree / packed nodes | Depth | Query visits min / median / max | FIFO capacity | FIFO bytes per arm |
|---|---:|---:|---:|---:|---:|
| ragged37-mixed33 | 37 / 37 | 5 | 0 / 1 / 37 | 19 | 5,016 |
| binary511-root32 | 511 / 511 | 8 | 511 / 511 / 511 | 256 | 65,536 |
| binary511-mixed256 | 511 / 511 | 8 | 1 / 3 / 511 | 256 | 524,288 |
| binary4095-root16 | 4095 / 4095 | 11 | 4095 / 4095 / 4095 | 2048 | 262,144 |
| binary4095-mixed256 | 4095 / 4095 | 11 | 1 / 1 / 4095 | 2048 | 4,194,304 |
| binary4095-leaf1024 | 4095 / 817 | 11 | 1 / 1 / 1 | 1 | 8,192 |
| binary4095-small1024 | 4095 / 1311 | 11 | 1 / 1 / 3 | 2 | 16,384 |
| ternary3280-root16 | 3280 / 3280 | 7 | 3280 / 3280 / 3280 | 2187 | 279,936 |
| quaternary4093-mixed128 | 4093 / 4093 | 6 | 1 / 1 / 4093 | 3070 | 3,143,680 |
| chain2048-mixed32 | 2048 / 2048 | 2047 | 36 / 880 / 2048 | 1 | 256 |
| irregular4095-mixed128 | 4095 / 4095 | 22 | 1 / 2 / 4095 | 475 | 486,400 |
| irregular16383-mixed256 | 16383 / 16383 | 23 | 1 / 2 / 16383 | 2028 | 4,153,344 |
| binary1023-root1 | 1023 / 1023 | 9 | 1023 / 1023 / 1023 | 512 | 4,096 |
| binary1023-root32 | 1023 / 1023 | 9 | 1023 / 1023 / 1023 | 512 | 131,072 |
| binary1023-root128 | 1023 / 1023 | 9 | 1023 / 1023 / 1023 | 512 | 524,288 |
| binary1023-root128-all | 1023 / 1023 | 9 | 1023 / 1023 / 1023 | 512 | 524,288 |
| binary1023-root128-none | 1023 / 1023 | 9 | 1023 / 1023 / 1023 | 512 | 524,288 |

The memory probe measured 370.48 MB free after context creation. Preparation budgets 203.76 MB (55% of that value); each run rechecks current free VRAM before allocation. Exact peak live FIFO occupancy is computed over every query. Scratch is `queries × exact capacity × 8` bytes per arm. The eight-arm run’s largest planned live allocation is 33.85 MB. Read-only inputs are shared and cases are released sequentially.

## Correctness and launch audit

- Production Jac Item/Child objects and `gpu.pack_walkers` produce the actual CSR, with its discovery layout held fixed across the three arms. Saved node identities, field columns, each CSR row/target and query heads are checked against the original object tree. All saved arrays have SHA-256 checksums.
- Serial Jac runs every query; an independent CPU reference computes all five state fields. The replay runner independently traverses the saved packed CSR and checks those oracle outputs again.
- Every replay poisons all five output columns and status outside timing, then verifies every query field and zero status after execution. The maximum absolute sum is bounded by `max_abs_amount × max_visits`, safely inside signed int64.
- Direct status testing passes 17 fixtures × 4 checked kernels = 68 standalone GPU launches, comparing original Jac, checked O2, checked CUDA and checked query-major CUDA against the unmodified production host LLVM JIT. Cases cover ragged/negative queries, private initial state, equality above 2^53, positive and negative sum overflow, count and visited overflow, malformed heads/targets/CSR, queue/visit limits, a cycle, and empty roots. Failing lanes preserve every poisoned result field.
- Primary Nsight join: 7,395 launches verified, 6,120 measured. Supplementary join: 19,720 verified, 16,320 measured. Every kernel name, chronological position, grid and block matches the exact runner request, including prime and warmup nodes.
- The existing subtree CPU/JIT suite passes all four tests. Raw status evidence is in [correctness.json](correctness.json); raw traces and joins are in `profile/` and `ablation-profile/`.

## Measurement boundary and shared environment

RTX 3090, driver 580.65.06, CUDA 12.9 nvcc/ptxas, bundled Jac LLVM NVPTX. The GPU is shared with Ollama, which holds approximately 23,462 MiB in the saved snapshots. Before/after snapshots and free-memory values are stored per run. Absolute timings reflect that shared context; the primary ratios use the same interleaved run.

The primary metric is actual GPU kernel end−start. The ordinary event runs measure CUDA graph replay time per invocation, including graph scheduling gaps. Allocations, module compilation, graph preparation, transfers, poisoning and verification occur outside both timing intervals. `inputs.json` records CPU oracle, graph construction, serial Jac and packing time. Runner case records separately save allocation, H2D and graph capture/prime time; each replay’s D2H/verification is outside its event interval.

## Reproduction and presentation

Run [reproduce.sh](../../reproduce.sh) from the repository root with a fresh output directory and GPU access. The pipeline rebuilds real graphs, emits variants, validates, profiles and exports the report. [commands.txt](commands.txt) records the completed run commands; [provenance.json](provenance.json) records source hashes.

The [English PDF deck](../../../../../docs/presentations/jac-gpu-subtree/jac-gpu-subtree.pdf) and [deck generator](../../../../../docs/presentations/jac-gpu-subtree/generate.py) use white backgrounds and sans-serif typography, and verify the measured source hashes when generated.

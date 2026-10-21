# Supplementary compiler and traversal ablations

Source run: `ablation-profile`, a separate interleaved run from the three-way primary table. Values below are median actual Nsight kernel microseconds (240 measured nodes per cell). `ablation-ordinary/results.json` supplies the independent event samples. Time differences compare independently optimized implementations. Attribution to individual mechanism costs remains unresolved.

## Compiler transformations

| Variant | Controlled change | Safety contract |
|---|---|---|
| baseline | Existing production target emission | Full production |
| sroa | SROA only, unmodified raw module; assembly-equivalent baseline control | Full production |
| hoist_sroa | Hoist ten fixed scalar allocas from start to entry; SROA only | Full production |
| O2 | Standard LLVM O2 pipeline on the same raw module | Full production |
| O2_no_overflow | Bypass the two error.3 branches, then O2 | Diagnostic: bounded arithmetic only |
| O2_no_validation | Bypass errors 1/2/5/6, then O2; retain overflow and type dispatch | Diagnostic: valid finite graph/queue/round inputs only |
| O2_unchecked | Bypass all thirteen error branches above, then O2; retain generic FIFO and type dispatch | Diagnostic: both restrictions above |

All variants share the graph ABI and exact packed layout. `diagnose_codegen.py` saves the raw `input.ll`, each pre-codegen transformed IR, PTX, cubin, ptxas command/log and hashes. `emit_assembly` itself mutates its input IR; the raw module is captured before any emission. The benchmark loads PTX through the CUDA driver; cubins provide static diagnostic assembly evidence. Actual driver-JIT attributes are saved in `status-validation.json`.

| Variant | LLVM allocas | PTX local loads/stores (static sites) | ptxas stack bytes | ptxas registers |
|---|---:|---:|---:|---:|
| baseline | 10 | 20/20 | 80 | 28 |
| sroa | 10 | 20/20 | 80 | 28 |
| hoist_sroa | 0 | 0/0 | 0 | 40 |
| O2 | 0 | 0/0 | 0 | 40 |
| O2_no_overflow | 0 | 0/0 | 0 | 44 |
| O2_no_validation | 0 | 0/0 | 0 | 40 |
| O2_unchecked | 0 | 0/0 | 0 | 44 |

## Restricted graph controls

Host preconditions: exactly one Scalar seed per channel, zero initial total, both chains of exactly K nodes, degree 0/1, finite traversal, valid indices and bounded products/sums. The benchmark checks every chain value and type; it proves schedule compression preserves each lane’s actual node identities. Every control computes the same complete matmul and writes status zero; all replay outputs/statuses are poisoned and checked. The general walker additionally supports branching, repeated arrivals, arbitrary seeds, invalid-input reporting and overflow detection.

- `chain_csr`: NVCC implementation on the original packed values/CSR/heads; two register cursors, no FIFO or dynamic type/error machinery. Comparison with O2_unchecked measures the combined effect of specialization and compiler choice.
- `chain_next`: same restricted chain computation and lane geometry, but replace four CSR-offset plus two target load sites per round with two direct successor lookups, including -1 termination. The CPU derives the successor table from the exact packed CSR; node/value layout is held fixed. The transform changes lookup count and address dependencies together.
- `schedule`: precompute q-major A/B node-ID sequences from those same chains; keep original packed values and lane order. It replaces dynamic successors/termination with index loads and a K loop; its index organization and control flow differ from `chain_next`.
- `CUDA flat`: dense address arithmetic with the graph arms’ 128-thread one-dimensional geometry and lane order, and `#pragma unroll 1`, matching the schedule kernel’s loop policy. Dense naive/tiled use 256-thread 16×16 geometry and their own compiled loops. Flat versus naive compares both launch geometry and compiled loop policy.

## Actual kernel measurements

### 3 × 5 × 2

| Implementation | Current | Predicted | Random928 |
|---|---:|---:|---:|
| Jac baseline | 8.768 | 8.288 | 7.264 |
| Jac O2 | 7.776 | 7.136 | 6.368 |
| Jac hoist_sroa | 7.968 | 7.232 | 6.304 |
| Jac O2_no_overflow | 6.753 | 6.528 | 5.664 |
| Jac O2_no_validation | 6.592 | 5.952 | 5.024 |
| Jac O2_unchecked | 5.440 | 5.056 | 4.288 |
| Graph chain_csr | 2.976 | 2.752 | 2.496 |
| Graph chain_next | 2.208 | 2.048 | 2.080 |
| Graph schedule | 2.752 | 2.592 | 2.272 |
| Dense CUDA naive | 1.504 | — | — |
| Dense CUDA tiled | 1.568 | — | — |
| Dense CUDA flat | 1.792 | — | — |

### 17 × 31 × 19

| Implementation | Current | Predicted | Random928 |
|---|---:|---:|---:|
| Jac baseline | 45.504 | 45.728 | 42.977 |
| Jac O2 | 38.880 | 38.881 | 36.576 |
| Jac hoist_sroa | 39.025 | 39.041 | 36.577 |
| Jac O2_no_overflow | 33.376 | 33.248 | 31.120 |
| Jac O2_no_validation | 33.344 | 33.216 | 30.960 |
| Jac O2_unchecked | 27.200 | 27.201 | 25.041 |
| Graph chain_csr | 11.008 | 11.072 | 11.072 |
| Graph chain_next | 6.400 | 6.432 | 6.496 |
| Graph schedule | 9.984 | 10.000 | 9.728 |
| Dense CUDA naive | 2.624 | — | — |
| Dense CUDA tiled | 1.888 | — | — |
| Dense CUDA flat | 5.568 | — | — |

### 64 × 128 × 64

| Implementation | Current | Predicted | Random928 |
|---|---:|---:|---:|
| Jac baseline | 185.217 | 184.977 | 201.089 |
| Jac O2 | 157.633 | 157.249 | 174.785 |
| Jac hoist_sroa | 157.409 | 156.929 | 175.201 |
| Jac O2_no_overflow | 134.305 | 134.177 | 149.345 |
| Jac O2_no_validation | 135.360 | 135.105 | 152.289 |
| Jac O2_unchecked | 109.985 | 109.792 | 123.424 |
| Graph chain_csr | 41.857 | 41.985 | 51.200 |
| Graph chain_next | 22.465 | 22.592 | 27.744 |
| Graph schedule | 38.272 | 38.176 | 40.576 |
| Dense CUDA naive | 6.208 | — | — |
| Dense CUDA tiled | 4.736 | — | — |
| Dense CUDA flat | 19.968 | — | — |

### 128 × 128 × 128

| Implementation | Current | Predicted | Random928 |
|---|---:|---:|---:|
| Jac baseline | 230.466 | 230.113 | 319.282 |
| Jac O2 | 165.665 | 166.849 | 188.785 |
| Jac hoist_sroa | 165.057 | 165.377 | 189.889 |
| Jac O2_no_overflow | 141.825 | 141.601 | 166.401 |
| Jac O2_no_validation | 141.873 | 141.873 | 166.177 |
| Jac O2_unchecked | 116.001 | 115.808 | 136.225 |
| Graph chain_csr | 45.025 | 44.096 | 67.200 |
| Graph chain_next | 26.432 | 26.432 | 40.928 |
| Graph schedule | 40.416 | 39.424 | 46.817 |
| Dense CUDA naive | 6.304 | — | — |
| Dense CUDA tiled | 4.864 | — | — |
| Dense CUDA flat | 21.312 | — | — |

### 256 × 256 × 256

| Implementation | Current | Predicted | Random928 |
|---|---:|---:|---:|
| Jac baseline | 2118.316 | 2066.924 | 4402.171 |
| Jac O2 | 542.483 | 540.980 | 922.262 |
| Jac hoist_sroa | 537.555 | 538.227 | 934.246 |
| Jac O2_no_overflow | 450.627 | 444.931 | 899.541 |
| Jac O2_no_validation | 488.851 | 501.938 | 956.390 |
| Jac O2_unchecked | 398.211 | 384.994 | 990.086 |
| Graph chain_csr | 95.617 | 98.753 | 716.165 |
| Graph chain_next | 54.720 | 53.792 | 423.155 |
| Graph schedule | 81.617 | 80.353 | 117.265 |
| Dense CUDA naive | 23.904 | — | — |
| Dense CUDA tiled | 20.577 | — | — |
| Dense CUDA flat | 42.257 | — | — |

## Interpretation and unresolved attribution

At 256³ Predicted, baseline 2066.924 → hoist+SROA 538.227 µs closely matches O2 540.980 µs. At 3×5×2 and 17×31×19 the relative compiler improvement is smaller. The measured promotion benefit varies with matrix size.

On Predicted 256³, O2_no_overflow is 444.931, O2_no_validation 501.938, and O2_unchecked 384.994 µs. On Random928, however, checked O2 is 922.262 versus unchecked 990.086 µs; the ordinary-event run also shows the reversal. Deleting validation changes optimized PTX (including 17→21 static global-load sites and 6→10 global-store sites), and the overflow variants use different register counts. The hardware cause of the reversal remains unresolved. Static instruction sites describe generated code; dynamic transaction counts require separate measurements.

On Predicted, chain_next 53.792 is faster than schedule 80.353 µs; on Random928, chain_next 423.155 is slower than schedule 117.265 µs. The ordinary run corroborates both directions. The faster representation depends on layout. This control changes address streams and termination together, leaving their individual hardware contributions unresolved.

Current and Predicted are close on the large regular case, while Random928 is slower for multiple graph implementations. This establishes sensitivity to physical representation at fixed graph semantics. Cache hit rate, coalescing efficiency and occupancy remain unmeasured: earlier Nsight Compute access returned `ERR_NVGPUCTRPERM`.

The checked optimization path is experimental; the unchecked and restricted-chain paths serve as diagnostic controls.

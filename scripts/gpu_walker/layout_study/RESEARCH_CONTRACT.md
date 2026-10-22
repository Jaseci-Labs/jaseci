# Research contract: access-order-aware GPU node layout

## Objective and primary groups

Measure whether Jac visit/cursor access-order guarantees enable useful GPU node
layout optimization. The Jac independent variable is node layout alone.

The primary table contains exactly these three implementation columns:

1. **Jac before (Random + checked LLVM O2):** node IDs shuffled with a recorded fixed seed; standard checked LLVM O2 on the production raw module.
2. **Jac after (Predicted + checked LLVM O2):** access-order-aware layout with the identical checked LLVM O2 PTX. For matmul,
   concatenate the complete cursor-a discovery BFS with the complete cursor-b
   discovery BFS, preserving first occurrence: all A nodes followed by all B nodes.
3. **Handwritten CUDA reference:** the same fixed tiled int64 matmul kernel for
   every size, on the same logical matrices, with its fixed appropriate geometry.

The handwritten kernel uses nvcc O3. Both toolchains receive regular optimizing pipelines; LLVM O2 and nvcc O3 are distinct pipelines and provide different optimization guarantees. The handwritten column is a performance reference. The Random/Predicted pair
isolates layout. Current-layout and compiler-O2 variants are supplementary history.

## Jac invariants

Both Jac arms use byte-identical checked LLVM O2 PTX derived from the same production raw LLVM and the same entry point, source,
int64 arithmetic, logical node identities/values/edges, query starts, lane order,
walker-to-thread mapping, grid, block, queue capacity, visit bound, initial state,
output coverage and status contract. Only node IDs and their consistent array,
CSR-target and head remapping differ. Save each permutation and all array hashes.
Verify logical traversal equivalence from the saved arrays and identities.

## Measurement and outcomes

First extract a pilot from one existing trace containing all three arms, with its compiler policy explicitly labeled. The main confirmation uses checked LLVM O2 for both Jac layouts. Save its
exact paths and hashes. Then run all three primary arms in one fresh randomized
interleaved CUDA-graph experiment over all five existing shapes through 256 cubed.
Report actual Nsight Systems node-kernel medians in microseconds, Random/Predicted
layout speedup, and Predicted/handwritten residual gap. Retain distributions and
round identities. Additional fixed random seeds provide supporting robustness
repetitions and share the same run when practical. Report improvement, parity or
regression as observed. Record shared GPU context and separate ordinary-event
measurements when collected.

## Interpretation and acceptance checks

- Check every output against the independent int64 matrix oracle and every Jac
  status after every replay. Poison output/status outside timing.
- Validate source/PTX/input/permutation hashes and every saved logical chain.
- Independently join every profiler node by requested arm order, name and geometry,
  including primes and warmups; primary ratios use the same source run.
- Try Nsight Compute counters without changing driver settings. Record exact
  access limitations. A deterministic adjacent-lane/32-byte-address-segment
  analysis may supplement the trace, labeled as address analysis rather than
  measured transactions, cache misses or an explanation inferred from timing.
- Validate the report and PDF against this contract: three explicitly named
  primary groups, Jac layout as the only Jac variable, fixed reference kernel,
  exact run identifiers, both ratios, correctness and measurement boundaries.
- Preserve previous studies and unrelated files. Scope new scripts, raw evidence,
  report, CSV/JSON and concise white/sans-serif English PDF to this layout study.

A later subtree extension uses the same Random/ordered-BFS question with an
unchanged checked production CSR kernel. Its third reference is the fixed checked
handwritten CSR traversal on the after layout. Matmul is the first deliverable.

## Superseding primary compiler policy

The primary table uses checked LLVM O2 on both Jac layouts, and nvcc O3 for the fixed handwritten reference. The earlier production-PTX layout run and pilot are supplementary history. The optional subtree extension is paused while this corrected matmul comparison is completed.

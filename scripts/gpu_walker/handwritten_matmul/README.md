# Handwritten int64 CUDA matmul comparison

[Three-way measured report](validation/20261021/REPORT.md) ·
[CSV](validation/20261021/primary/comparison.csv) ·
[JSON](validation/20261021/primary/comparison.json) ·
[Supplementary ablations](validation/20261021/codegen/ABLATIONS.md)

The primary groups are original Jac, checked LLVM-O2 Jac, and the same
handwritten tiled CUDA kernel across all sizes. Both Jac groups hold the
production-packed Predicted layout fixed. The original backend still uses its
existing target-machine code generation settings; O2 adds an explicit LLVM
middle-end pipeline while preserving the walker checks and status semantics. Full profiler traces and independent error/status validation are saved.

Regenerate the investigation in an isolated output directory (requires GPU access):

```bash
bash scripts/gpu_walker/handwritten_matmul/reproduce_codegen.sh /tmp/matmul-reproduction
```

`diagnose_codegen.py` emits checked baseline, SROA, hoist+SROA and O2 variants,
plus clearly labelled diagnostic variants with selected error branches removed.
`benchmark.py --jac-variant NAME=PTX` interleaves additional compiled variants
with the baseline. `--graph-controls` enables restricted single-chain kernels;
their narrower contracts and unresolved attribution are documented in the
supplementary report. `validate_codegen.py` compares checked GPU error behavior
with the unmodified production LLVM JIT.


`matmul.cu` contains two handwritten kernels:

- `matmul_naive_i64`: each thread computes one complete output dot product from
  row-major A and B.
- `matmul_tiled_i64`: each 16×16 block computes a C tile and cooperatively loads
  A/B tiles into shared memory. All threads participate at the matrix boundaries.

The comparison uses the named-cursor Jac `Dot` walker and its real shared
Scalar/RowNext/ColumnNext input graph. A node holds one int64 value. Both CUDA
kernels also use int64 products and accumulation. The input magnitudes guarantee
that every intermediate fits int64. Every implementation computes the full M×N
output, including ragged dimensions, and is compared with an independent NumPy
int64 oracle.

`prepare_inputs.py` uses the existing Jac graph builder and production packer for
Current, Predicted and Random928. It saves actual packed arrays and generated
PTX. `benchmark.py` independently checks every cursor-chain value against the
corresponding dense matrix before launching. It can also replay the previously
saved graph artifacts without importing the compiler.

## Run

From the repository root, with NumPy installed in `env`:

```bash
# Use this checkout’s bundled LLVM; JAC_LLVM_SHIM can select another compatible NVPTX-enabled shim.
PYTHONPATH=jac:scripts/gpu_walker env/bin/python \
  scripts/gpu_walker/handwritten_matmul/prepare_inputs.py --output /tmp/matmul-inputs

env/bin/python scripts/gpu_walker/handwritten_matmul/benchmark.py \
  --inputs /tmp/matmul-inputs/inputs.json --output /tmp/matmul-ordinary

nsys profile --trace=cuda --cuda-graph-trace=node --sample=none --cpuctxsw=none \
  --force-overwrite=true --output /tmp/matmul-profile/trace \
  env/bin/python scripts/gpu_walker/handwritten_matmul/benchmark.py \
  --inputs /tmp/matmul-inputs/inputs.json --output /tmp/matmul-profile \
  --warmup 3 --repeats 15

nsys export --type sqlite --force-overwrite=true \
  --output /tmp/matmul-profile/trace.sqlite /tmp/matmul-profile/trace.nsys-rep

env/bin/python scripts/gpu_walker/handwritten_matmul/analyze_profile.py \
  /tmp/matmul-profile/results.json /tmp/matmul-profile/trace.sqlite \
  --output /tmp/matmul-profile/verified-kernels.json
```

GPU execution requires access to the NVIDIA device nodes. The default compiler
is `/usr/local/cuda-12.9/bin/nvcc`; `--nvcc` selects another installation.

## Timing and interpretation

All arrays are resident during measurement. Allocations, compiler work, graph
packing, transfers and output verification are outside the CUDA-event interval.
Sixteen sequential invocations are captured into a CUDA graph per arm; event time
is divided by sixteen. This retains GPU graph scheduling gaps while reducing
Python enqueue effects. Each replay verifies all outputs and all Jac statuses.
Measured round order is deterministically randomized.

A separate Nsight Systems run measures actual per-kernel end minus start. The
analyzer verifies **every** launch name, grid, block and position, including
untimed priming kernels, warmups and all graph replay nodes. It joins measured
kernels back to their case and arm and publishes the complete sample list.

The handwritten kernels exploit dense dimensions and address arithmetic. The
Jac kernel implements generic cursor traversal and its checks. Their comparison
measures that complete representation/execution difference; Current versus
Predicted versus Random compares layout within the same Jac kernel. The report
states the observed GPU sharing and exact measurement boundary.

Every replay poisons outputs with the bitwise complement of the expected result,
and Jac statuses with `0xffffffff`, before the timed interval. This catches
replays that leave previous output or status values untouched.

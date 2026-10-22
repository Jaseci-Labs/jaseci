# Jac on GPU: Matmul

English PDF slides comparing original Jac, checked LLVM O2 Jac and handwritten tiled CUDA.
White background, sans-serif text, 16:9 pages. The flow covers the research problem,
a traversal example, compiler optimization, the corresponding codegen example,
measurement data and interpretation.

Build from the repository root:

```sh
env/bin/python docs/presentations/jac-gpu-matmul/generate.py
```

Requires matplotlib. The builder verifies measurement source hashes and checks every
primary value against the recorded profiler summaries. `sources.json` records the
input files and their hashes. Measurements originate from commit `e476272e4`.

[PDF slides](jac-gpu-matmul.pdf) · [Measurement report](../../../scripts/gpu_walker/handwritten_matmul/validation/20261021/REPORT.md)

# Jac GPU layout study

[English PDF](jac-gpu-layout.pdf), eight white/sans-serif slides generated from the contract-validated measurements.

Primary groups: Jac Random928 + checked LLVM O2; Jac Predicted + identical checked LLVM O2; fixed tiled CUDA nvcc O3. The first pair isolates node layout. The CUDA column is the performance reference.

```bash
env/bin/python scripts/gpu_walker/layout_study/build_report.py scripts/gpu_walker/layout_study/validation/20261022
env/bin/python docs/presentations/jac-gpu-layout/generate.py
```

The generator checks exact contract/source hashes, all primary medians, sample counts and ratios against the independently verified Nsight node trace. [Detailed report](../../../scripts/gpu_walker/layout_study/validation/20261022/REPORT.md). `sources.json` records the deck's source hashes.

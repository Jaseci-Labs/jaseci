# Jac GPU node-layout study

The primary comparison isolates **node layout** between two Jac groups and adds a fixed CUDA performance reference:

1. Jac before: Random928 + checked standard LLVM O2.
2. Jac after: Predicted + the identical checked LLVM O2 PTX.
3. Handwritten reference: fixed 16×16 tiled int64 CUDA, nvcc O3.

Predicted concatenates complete cursor-a BFS, then complete cursor-b BFS: all A nodes, then all B nodes. Both Jac groups preserve full traversal/check/status semantics and use identical thread mapping and launch geometry. LLVM O2 and nvcc O3 are distinct optimizing pipelines. [Research contract](RESEARCH_CONTRACT.md).

[Measured English report](validation/20261022/REPORT.md) · [compact CSV](validation/20261022/comparison.csv) · [source-hashed JSON](validation/20261022/comparison.json) · [English PDF](../../../docs/presentations/jac-gpu-layout/jac-gpu-layout.pdf).

## Reproduce

From the repository root, with `env/bin/python`, NumPy, the bundled Jac LLVM, CUDA 12.9 and Nsight Systems:

```bash
scripts/gpu_walker/layout_study/reproduce.sh scripts/gpu_walker/layout_study/validation/NEW_RUN
```

Use a fresh destination. The script audits/remaps the saved real production-packed graphs, regenerates O2 from the same raw LLVM, profiles all three primary arms plus two supporting random seeds in one randomized interleaved run, validates every output/status, joins every Nsight node, collects a separate ordinary-event run and logical address analysis, and attempts one counter probe. Each case checks its planned allocation against currently free VRAM. A denied hardware-counter request is retained as `ERR_NVGPUCTRPERM` with the exact log.

CPU-only evidence validation and PDF generation for the recorded run:

```bash
env/bin/python scripts/gpu_walker/layout_study/build_report.py scripts/gpu_walker/layout_study/validation/20261022
env/bin/python docs/presentations/jac-gpu-layout/generate.py
```

`optimized-profile/` is the primary source run. It has 15 measured rounds × 16 graph nodes per arm/case after three warmup rounds. The ordinary run has 25 rounds after five warmup rounds. `verified.json` retains all actual kernel samples; `results.json` retains randomized order, event samples, full correctness flags, geometry, device bases and GPU snapshots. `inputs/` retains all binary arrays and permutations. `optimized-codegen/` retains raw/optimized LLVM, PTX, cubin and ptxas output. The emitter checks byte identity against the previously status-validated O2 artifact (13 fixtures).

`validation/20261022/commands.json` records the performed primary commands and tool versions. `extract_pilot.py` reproduces the supplementary same-trace production-PTX pilot. Earlier production-PTX layout evidence is archived in `production-PTX-REPORT.md`, `production-*`, `profile/`, `ordinary/` and `address-analysis.json`. The optional subtree capture remains paused with its source and raw data retained; it supplies no primary results here.

Historical 3000³ evidence separates full nine-million-output correctness from 32,768-output subset timing. The report records the measured VRAM boundary and options for a matched full-coverage three-arm follow-up.

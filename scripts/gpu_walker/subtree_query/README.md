# Batched subtree GPU benchmark

[Measured English report](validation/20261021/REPORT.md) ·
[Three-way CSV](validation/20261021/primary/comparison.csv) ·
[Three-way JSON](validation/20261021/primary/comparison.json) ·
[English PDF deck](../../../docs/presentations/jac-gpu-subtree/jac-gpu-subtree.pdf)

The primary groups are original production CSR Jac, the same raw LLVM with
checked standard LLVM O2, and one fixed handwritten checked per-query CSR kernel.
All three share saved production-packed graph arrays, query roots, thresholds,
FIFO capacity and full workloads. Every query returns count, signed int64 sum,
matching-node alert OR, visited count and retained threshold.

The default sweep covers 17 workloads: balanced and irregular trees, ragged
shapes, a deep chain, root/mixed/leaf queries, 1–1024 query batches and varied
predicate selectivity. Real Jac objects are packed through `gpu.pack_walkers`.
Serial Jac and an independent CPU oracle check every query. The primary metric
comes from one randomized interleaved Nsight Systems node-traced run; ordinary
CUDA-event graph timings are saved separately.

```bash
# Fresh output directory; GPU access and the repository env are required.
bash scripts/gpu_walker/subtree_query/reproduce.sh /tmp/jac-subtree-run

# Rebuild exports from the committed evidence.
env/bin/python scripts/gpu_walker/subtree_query/build_report.py \
  scripts/gpu_walker/subtree_query/validation/20261021

# Regenerate the deck from the committed measurements.
MPLCONFIGDIR=/tmp/jac-subtree-deck-mpl env/bin/python \
  docs/presentations/jac-gpu-subtree/generate.py
```

`run.py --inputs PATH/inputs.json --output PATH` replays saved packed workloads
using NumPy and the CUDA driver, independently of Jac compilation. The manifest
specifies the actual graph arrays, states, expected results and queue/visit
bounds. Allocations use the measured free VRAM and exact live FIFO capacity;
read-only arrays are shared, scratch is private, and cases run sequentially.

`--ablations` adds selected-check bypasses on the validated bounded inputs, a
CUDA unchecked control, and a fully checked query-major FIFO control. Their
contracts and measured effects appear in the report and ablation summary.
`validate.py` directly compares checked GPU status/output behavior with the
unmodified production LLVM host JIT, including malformed graphs and overflow.

`common.py` reuses the CUDA driver/event/graph helper from the committed matmul
benchmark; the runner records its SHA-256 along with its own source hashes.
Compilation uses bundled Jac LLVM and CUDA 12.9. GPU measurements record the
shared Ollama context and before/after device snapshots.

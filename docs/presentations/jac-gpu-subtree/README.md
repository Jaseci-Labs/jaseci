# Jac GPU: batched subtree queries

[English PDF](jac-gpu-subtree.pdf) · [Generator](generate.py) · [Source hashes](sources.json)

Twelve slides with white backgrounds and DejaVu Sans typography explain the
query semantics, three primary implementations, full workload sweep, measured
results, compiler evidence, controlled ablations and correctness checks.

The generator verifies the primary table, raw result/trace hashes, supplementary
trace joins and correctness evidence before producing the PDF.

```bash
MPLCONFIGDIR=/tmp/jac-subtree-deck-mpl env/bin/python \
  docs/presentations/jac-gpu-subtree/generate.py
```

Measurements live in
`scripts/gpu_walker/subtree_query/validation/20261021/`.
The primary table uses resident actual GPU kernel durations from one
interleaved randomized Nsight Systems run.

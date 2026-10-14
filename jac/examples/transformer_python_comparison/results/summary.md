# CPU correctness evidence

| case | FX output max abs | direct Inductor output max abs | FX intermediate max abs | direct Inductor intermediate max abs |
|---|---:|---:|---:|---:|
| small_float64_4x3 | 5.5511e-17 | 1.1102e-16 | 1.3323e-15 | 8.8818e-16 |
| small_float64_2x1 | 1.3878e-16 | 1.3878e-16 | 8.8818e-16 | 8.8818e-16 |
| small_float32_4x3 | 2.9802e-08 | 2.9802e-08 | 3.5763e-07 | 4.7684e-07 |
| medium_float32_7x5 | 1.1921e-07 | 5.9605e-08 | 1.1921e-06 | 7.1526e-07 |

All four cases passed, including 45 checkpoints, three repeated/changed inputs per case, eleven weight/buffer replacements, in-place mutation, five residual joins, causal masks, future isolation (nontrivial sequence lengths), encoder/cross-memory influence and four metadata/name guards. The small float64 case additionally compiles and validates the output-only graph.

Actual compiler entry: `torch._inductor.compile_fx.compile_fx`. Frontend capture probes: zero calls; no fallback. Internal AOTAutograd/functionalization/decomposition and Inductor helper tracing are still part of this backend.

CUDA was not run: the host GPU was occupied by Ollama and the isolated test environment uses CPU-only Torch. No driver changes or interference with that workload.

Existing example/library tree hashes verified unchanged. No performance measurements.

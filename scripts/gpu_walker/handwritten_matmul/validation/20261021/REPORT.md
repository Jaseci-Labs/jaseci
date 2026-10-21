# Handwritten CUDA matmul versus Jac GPU

All methods compute every output using the same signed int64 matrices. Each input node in Jac stores one integer.

## Actual kernel durations

Nsight Systems median `kernel.end - kernel.start`, microseconds per launch. This is a separately profiled run.

| M × K × N | CUDA naive | CUDA tiled | Jac Current | Jac Predicted | Jac Random 928 | Predicted / tiled |
|---|---:|---:|---:|---:|---:|---:|
| 3 × 5 × 2 | 1.312 | 1.376 | 7.616 | 7.072 | 6.400 | 5.14× |
| 17 × 31 × 19 | 2.624 | 1.888 | 45.536 | 45.792 | 42.912 | 24.25× |
| 64 × 128 × 64 | 6.176 | 4.704 | 184.193 | 183.745 | 201.025 | 39.06× |
| 128 × 128 × 128 | 6.240 | 4.800 | 227.905 | 227.233 | 312.289 | 47.34× |
| 256 × 256 × 256 | 23.840 | 20.608 | 2080.748 | 2069.116 | 4486.394 | 100.40× |

## Ordinary CUDA-event graph replay

Microseconds per kernel invocation. Each replay contains 16 sequential kernels; the event interval is divided by that number. This includes GPU graph scheduling gaps. Allocation, compilation, graph packing, upload, download and CPU verification are outside this interval.

| M × K × N | CUDA naive | CUDA tiled | Jac Current | Jac Predicted | Jac Random 928 |
|---|---:|---:|---:|---:|---:|
| 3 × 5 × 2 | 1.600 | 1.664 | 8.896 | 8.192 | 7.424 |
| 17 × 31 × 19 | 3.136 | 2.304 | 52.726 | 53.054 | 49.664 |
| 64 × 128 × 64 | 6.336 | 4.864 | 185.600 | 185.134 | 205.312 |
| 128 × 128 × 128 | 6.720 | 5.120 | 231.296 | 231.424 | 317.760 |
| 256 × 256 × 256 | 24.128 | 20.800 | 2115.456 | 2166.720 | 4436.352 |

## Execution and correctness

- GPU: NVIDIA GeForce RTX 3090. Ollama held 23,462 MiB in the before/after snapshots; these are shared-GPU measurements.
- Ordinary replay: 5 warmup and 25 measured rounds, randomized arm order with seed 928.
- Nsight launch-order/name/grid/block verification: 8025 launches; 6000 measured launches.
- Every replay checks every output against a NumPy int64 oracle; every Jac lane must also return status zero.
- Before timing, every packed graph cursor chain is walked on the CPU and its values are checked against the dense A and B inputs. Saved input and expected-output SHA-256 hashes are checked.
- Inputs include negative values and ragged dimensions. Magnitudes satisfy |A| <= 3 and |B| <= 5, so every product and partial sum fits signed int64 (absolute partial sum <= 15*K).

## What the comparison measures

The dense naive kernel computes one dot product per thread using address arithmetic. The tiled kernel cooperatively loads 16×16 A/B tiles into shared memory and reuses them across threads.

Jac runs the actual compiled two-cursor Dot walker on shared Scalar/RowNext/ColumnNext graph inputs. It performs graph traversal and the generated queue, type and arithmetic checks. The dense kernels use fixed matrix dimensions and the proven input bounds. The measured ratio compares these complete implementations; it combines representation, generated execution machinery and dense tiling effects.

Current, Predicted and Random keep the same graph semantics and lane order. Their differences are physical layout. Timings alone establish execution cost; hardware-counter attribution requires separate measurements.

## Artifacts

- `ordinary/results.json`: all unprofiled samples and checksums.
- `profile/results.json`: exact profiled request order.
- `profile/verified-kernels.json`: every actual kernel duration and the independent profiler join.
- `profile/trace.nsys-rep` / `profile/trace.sqlite`: raw profiler artifacts.
- `inputs/`: real Jac packed graph arrays, oracle outputs and original generated PTX.
- `matmul.cu`: handwritten dense kernels.

# Python Transformer frontend expression comparison

Two separately readable Python implementations of the same small, complete,
inference-only Transformer equations:

1. [`imperative.py`](imperative.py): ordinary `nn.Module` forward using
   `nn.Embedding`, `nn.Linear`, explicit multi-head attention, `nn.LayerNorm` and
   `nn.ReLU`. There is no FX or compiler code in this implementation.
2. [`explicit_fx.py`](explicit_fx.py): directly constructs a `torch.fx.Graph`
   with placeholders and `graph.call_function(torch.ops.aten....)` calls, then
   creates a `GraphModule` and passes it directly to **`compile_fx`**. It does
   not trace/export version 1, import Jac, recapture through Dynamo, or execute a
   custom operation-dispatch interpreter. Its Python attention/FFN/norm helpers
   only construct graph nodes.

Both consume shared deterministic tensors from [`weights.py`](weights.py),
seed 1729. The ordinary model binds those storages as 46 frozen `nn.Parameter`
fields plus one fixed position buffer. The FX graph has **no parameters or
buffers of its own**: all 47 tensors are explicit arguments, in the exported
name-to-argument order. Callers supply current `model.bindings()` on each call.
Replacing or mutating a weight with matching metadata therefore reaches existing
compiled code, rather than leaving a stale captured weight snapshot.

This is an expression/correctness comparison. **No performance or compilation
latency was measured.** Source verbosity and operation counts are not speed
measurements. No existing Jac example or library was changed.

## Architecture and inputs

One encoder layer and one decoder layer, five postnorm residual joins:

- independent source/target embeddings scaled by sqrt(dimension), plus fixed
  sinusoidal positional encoding;
- encoder self-attention with separate Q/K/V and output projections;
- decoder causal self-attention, explicit upper-triangle bool mask and -infinity
  masked scores;
- cross-attention with decoder queries and encoder-memory K/V;
- ReLU FFNs and residual LayerNorm with population variance and epsilon 1e-5;
- output projection/logits and vocabulary softmax.

Default configuration: dimension 8, 2 heads, FFN width 16, vocabulary 13,
position capacity 64. Inputs are nonempty rank-one int64 source/target token
sequences; activations have shape `[length, dimension]`, with no batch dimension.
No dropout, gradient computation, padding mask, training or KV cache is included.
Callers must supply valid token IDs. The ordinary forward accepts lengths up to
position capacity; each manually constructed/compiled graph has fixed lengths.

The demo uses source `[3,4,5,2]`, labels `[6,7,2]`, shifted target input
`[BOS=1,6,7]`. A teacher-forced forward predicts all label positions together;
causal masking prevents future input tokens from affecting earlier outputs.
Autoregressive generation would repeatedly extend the target and require an
outer loop and matching shape-specialized graphs; it is outside this fixed
forward example. Random weights demonstrate numerical execution, not language
model quality.

## Compiler boundary: direct Inductor, not Dynamo recapture

The actual entry in the tested installation is:

```python
from torch._inductor.compile_fx import compile_fx
compiled = compile_fx(
    copy.deepcopy(graph_module),
    [source, target, *ordered_weight_tensors],
    config_patches={"compile_threads": 1, "triton.cudagraphs": False},
)
result_tuple = compiled(source, target, *ordered_weight_tensors)
```

`compile_fx` is an **internal, version-sensitive API**, tested on PyTorch
**2.8.0+cpu**, Python 3.12.11. There is **no fallback** to `torch.compile`, eager
execution or another compiler. Import/compile failures propagate as failures.
A copy is compiled because this API takes ownership of and may mutate its input
GraphModule. The original constructed graph remains available for inspection.
Graph outputs are a flat tuple, as required by this direct backend path.

This bypasses Dynamo's model/Python-bytecode frontend capture. It still uses
Inductor's normal AOTAutograd, functionalization, decomposition, fake-tensor
propagation, graph optimization and code generation. PyTorch imports and uses
some `torch._dynamo` utilities internally; “bypass” does not mean that package
is absent or that all backend transformations are bypassed.

[`audit.py`](audit.py) installs failing probes during version-2 construction,
compilation and execution on `torch.compile`, Dynamo `optimize`,
`optimize_assert`, `export`, its bytecode `_compile` entry, `torch.export.export`
and `torch.jit.trace`. Frontend `torch.fx.symbolic_trace` is also blocked.
The sole allowed backend exception is the exact `torch._dynamo.utils.identity`
function when called by `torch._inductor.loop_body` for its internal dummy graph;
that trace is recorded separately and does not inspect version 1. All tested
frontend-capture probe counts were zero.

Direct backend calls do not supply Dynamo's automatic guards/recompilation.
The wrapper checks tensor names, shape, stride, dtype, device and requires-grad
metadata. Changed tensor values are allowed; changed metadata requires rebuilding
and recompiling. Edits to graph code also require explicit recompilation. The
wrapper is designed for this example, not a general replacement for Dynamo's
full guard system or a general graph runtime.

## Run

From the repository root, using the independent environment created for this task:

```bash
/tmp/transformer-python-comparison-venv/bin/python jac/examples/transformer_python_comparison/demo.py
/tmp/transformer-python-comparison-venv/bin/python jac/examples/transformer_python_comparison/validate.py --device cpu
python jac/examples/transformer_python_comparison/summarize.py
```

To recreate a CPU environment:

```bash
python3 -m venv /tmp/transformer-python-comparison-venv
/tmp/transformer-python-comparison-venv/bin/python -m pip install -r jac/examples/transformer_python_comparison/requirements.txt --index-url https://download.pytorch.org/whl/cpu
```

Only Torch and its required dependencies are installed; optional NumPy is not
needed. PyTorch may print a NumPy initialization warning in this minimal venv.
A C++ toolchain is needed by CPU Inductor. The scripts use one CPU/compiler thread
and a separate cache at `/tmp/transformer-python-comparison-inductor`; there is no
autotuning sweep or benchmark. First execution includes compilation.

CUDA validation is supported by `validate.py --device cuda:0` **with a compatible
CUDA-enabled Torch installation and a free GPU**. It was not run here: the host
RTX 3090/driver works, but was occupied by Ollama PID 2267828 (reported 100%
utilization, 23488/24576 MiB). The isolated environment intentionally uses CPU-only
Torch. The earlier sandbox-level `nvidia-smi` failure was a visibility restriction,
not evidence of a broken host driver. No driver settings or other workload was
changed. CUDA correctness remains outstanding.

## Actual graph and operation counts

Every tested shape/dtype constructs the same fixed architecture:

| original FX graph category | count |
|---|---:|
| token input placeholders | 2 |
| parameter/buffer placeholders | 47 |
| ATen `call_function` nodes | 157 |
| output node | 1 |
| total nodes | 207 |

The 157 nodes include 17 `aten.mm` linear projections, 6 `aten.bmm` attention
products, 4 softmax operations and 5 fully expanded LayerNorms. These are original
**pre-optimization graph counts**, not kernel counts. Counts by exact ATen target
are in `results/validation_cpu.json`.

Version 1 and version 2 express equivalent equations, but not identical ATen IR:
`nn.Linear` can use fused addmm, and `nn.LayerNorm` uses native normalization;
version 2 explicitly spells out transpose/mm/add and mean/center/square/rsqrt/
affine operations. Normalization/reduction rounding and backend fusion can differ.
Any future timing study seeking to isolate frontend capture cost must control
for these IR differences, captures, specialization, cache state and backend
settings. This example makes no causal performance attribution.

Exports are produced from the actual constructed graph, never a hand-written
forward or disconnected diagram:

- [`results/demo_fx.py`](results/demo_fx.py), [`results/demo.dot`](results/demo.dot):
  default output-only graph;
- [`results/small_float64_4x3_fx.py`](results/small_float64_4x3_fx.py),
  [`results/small_float64_4x3.dot`](results/small_float64_4x3.dot): graph returning
  final probabilities plus 45 diagnostic checkpoints;
- matching `*_spec.json` files map generated weight arguments and expression names
  to shapes/dtypes and checkpoint names; the source files are inspection exports,
  not independent serialized models with saved weights;
- [`export_graphs.py`](export_graphs.py) reconstructs the inspection artifacts
  from the saved case configurations and verifies their operation counts.

The validation graph returns intermediates, which can affect optimization and
lifetime. The small float64 test also compiles and verifies a separate output-only
graph, as used by the demo. No performance comparison between these modes is made.

## Completed correctness checks

Four CPU cases passed: small float64 lengths 4/3 and 2/1, small float32 lengths
4/3, and dimension-32/four-head/FFN-64/vocabulary-31 float32 lengths 7/5. Each case
compares 45 meaningful intermediate tensors (embeddings/positions, Q/K/V, scores,
mask/attention probabilities/context, residual joins, norms, FFNs, logits and final
probabilities) against the ordinary module. Tolerances: float64 atol 2e-11,
rtol 2e-10; float32 atol 3e-5, rtol 3e-4.

| case | direct Inductor output max abs | direct Inductor intermediate max abs |
|---|---:|---:|
| small float64 4/3 | 1.11e-16 | 8.88e-16 |
| small float64 2/1 | 1.39e-16 | 8.88e-16 |
| small float32 4/3 | 2.98e-8 | 4.77e-7 |
| medium float32 7/5 | 5.96e-8 | 7.15e-7 |

Additional checks: finite/normalized outputs, all five residual sums, exact causal
mask and masked attention zeros, future-token isolation for target lengths >1,
encoder-memory and cross-key/output influence, three repeated/changed input calls
per case followed by the original inputs, eleven parameter/position-buffer
replacements and in-place bias mutation without recompilation, metadata/name
guard rejection, and zero frontend capture calls. Weight replacements compare
all 45 checkpoints. With target length one, changing self-attention K weights
correctly changes the K projection while leaving the final result invariant:
the sole-key attention softmax is always one.

Compact evidence: [`results/summary.md`](results/summary.md),
[`results/summary.json`](results/summary.json). Raw errors and audit records:
[`results/validation_cpu.json`](results/validation_cpu.json). Existing example
and library trees are protected by an initial combined filename/content SHA-256
snapshot: **566 existing example files and 12 library files** match unchanged.
`preserve.py` rechecks these without importing old examples or libraries.

Limits: fixed lengths per manual graph; unbatched inference only; no training,
conditional/dynamic loop graph, automatic guard synthesis, automatic graph
capture or portable model serialization. Internal backend and audit details must
be revalidated for a different Torch version. CUDA testing remains unavailable
in the occupied host environment. No latency, throughput or speedup result is
claimed.

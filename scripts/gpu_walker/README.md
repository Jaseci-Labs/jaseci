# Jac numeric walkers to PTX

From the repository root, using this checkout's Jac compiler:

```bash
jac build jac/examples/gpu/chain.jac --as ptx --gpu-entry ChainSum -o dist/gpu
```

This emits `chain.ptx`, `chain.gpu.ll`, and `chain.ptx.json`. It does not run a GPU
kernel. The implementation is in `jaclang.compiler.backends.native.ptx_walker`,
written in Jac and using LLVM IRBuilder/NVPTX. It extracts an actual checked Jac
ability body; it does not substitute a handwritten sum kernel or generate C++.

To execute **actual Jac walker lists** on a GPU, use the new
[runtime launcher and memory allocation API](runtime.md). The example command is
`jac run jac/examples/gpu/chain_run.jac` on the NVIDIA server.

For the experimental CSR general-graph path:

```bash
jac build jac/examples/gpu/csr_graph.jac --as ptx --gpu-entry GraphSum \
  --gpu-graph-format csr -o dist/gpu-csr
jac run jac/examples/gpu/csr_graph_run.jac
```

This selects `jaclang.compiler.backends.native.ptx_csr`, reusing the same checked
numeric body lowering. The `jac-ptx-csr-v1` manifest describes CSR arrays, a
per-walker FIFO queue, and queue/visit bounds. See the
[CSR experiment and memory contract](runtime.md#general-graph-storage-experiment-2026-09-30).
CSR is one experimental representation and may be revised after measurement.

## Supported program

One node type with one or more numeric or boolean leaf fields, one empty edge type, one
walker with one or more private numeric or boolean fields and one synchronous entry ability.
Node and walker fields can contain plain local `obj` values with fixed, nonrecursive numeric or boolean
fields. Each leaf becomes a separate SoA column, including nested paths such as
`here.position.x`. Nested objects must not be shared by different packed nodes.
Mutable walker objects must belong to one walker and one state path, and cannot
also belong to a node. Boolean leaves may accompany either `float` (float64)
or `int` (signed int64) leaves. Numeric leaves must share one type. Lists, optional objects and mixed numeric types are not
part of this first multi-field implementation.
The body contains sequential state updates and scalar reports followed by one
typed outgoing tail `visit`. Statements may be guarded by `if`/`elif`/`else`,
with multiple statements or nested `if` per branch. Each statement reads the state produced by earlier statements;
an unassigned field keeps its value. Conditions support boolean fields, literals, short-circuit `and`/`or`, `not`, and
comparisons: `==`, `!=`, `<`, `<=`, `>`, or `>=`.

Assignments support `=`, `+=`, `-=`, and `*=`; expressions support `self`/`here`
field reads, matching numeric literals, unary signs, `+`, `-`, and `*`.
Integer walkers additionally support `%` and `%=` with Jac's signed modulo
semantics (for example, `-3 % 2 == 1`). Integer literals, inputs, and every
executed arithmetic intermediate must fit int64. Overflow and modulo by zero
produce per-lane error statuses; they never silently wrap or publish a partial
walker batch. Untaken branches do not execute their arithmetic.

For a complete example that sums even values while still traversing every node:

```bash
jac build jac/examples/gpu/even_chain.jac --as ptx --gpu-entry EvenSum -o dist/gpu
jac run jac/examples/gpu/even_chain_run.jac
```

The second command runs 1,000 actual walkers on CUDA and checks every result
against ordinary serial Jac. Integers remain integers throughout packing,
device execution and publication, including values above 2^53.

For multiple node fields, including an owned nested `Position` object:

```bash
jac build jac/examples/gpu/multi_field.jac --as ptx --gpu-entry WeightedSum --gpu-graph-format csr -o dist/gpu-fields
jac run jac/examples/gpu/multi_field_run.jac
```

The example packs `value`, `weight`, `position.x`, and `position.y` into four
aligned columns, runs 1,000 walkers on a branching graph, and compares their
results with ordinary Jac. Multi-column exports use `jac-ptx-chain-v2` or
`jac-ptx-csr-v2`; each kernel's `parameters` gives the exact pointer order and
`field_path` mapping. Existing single-column exports retain their v1 ABI.

For multiple walker fields and owned nested state:

```bash
jac build jac/examples/gpu/walker_fields.jac --as ptx --gpu-entry Statistics --gpu-graph-format csr -o dist/gpu-states
jac run jac/examples/gpu/walker_fields_run.jac
```

This example updates `total`, `count`, `metrics.weighted`, and `metrics.last`,
and checks every field against serial Jac for 1,000 walkers. Multiple walker
columns use v3 manifests: node columns and topology pointers, then all initial
state columns, all result columns, and the existing status/scratch/count
parameters. `parameters` specifies the full argument order. Scalar walker v1/v2
ABIs remain compatible. Top-level numeric walker fields require literal
defaults; nested state is packed from actual instances, and its manifest
`default_initial_states` entries are null.

Inheritance, node abilities, helpers, shared writes, object reports,
filtered/multi-hop queries, general loops, mixed numeric
field types, and other effects are rejected with source locations. Standalone
scalar function exports still support only the separate float64/bool subset.
Branching graphs require the explicit CSR option; the default chain path keeps
its zero-or-one-successor restriction.

The entry point processes M independent instances of the selected walker type.
One thread performs a complete traversal. The graph is read-only and shared;
walkers may share nodes or suffixes, and retain independent starting states.
Serial Jac spawn sequences are not automatically parallelized.

## Packed chain device interface

The manifest records the actual node, edge, and field names. All parameters are
positional; arrays are contiguous and aligned for their element types:

| Parameter | Type | Length / meaning |
| --- | --- | --- |
| values | float64 or int64 pointer | N node values |
| next | int64 pointer | N successor indices; -1 ends a chain |
| heads | int64 pointer | M starting indices; -1 means no traversal |
| initial_total | float64 or int64 pointer | M initial private walker fields |
| results | float64 or int64 pointer | M final private fields |
| status | uint32 pointer | M completion codes |
| node_count | uint64 | N |
| walker_count | uint64 | M |

Input arrays must cover the counts. Results and status must be separate from
each other and all inputs. Use a 1D grid/block configuration that covers M
walkers; skip the launch for an empty batch. Inputs describe only the selected
node and edge types, with zero or one outgoing edge per node. The runtime object
packer validates types and edge multiplicity; PTX generation alone does not pack
live Jac objects. Node indices must fit signed 64-bit values.

Status 0 means success. Status 1 reports an invalid reachable head/successor.
Status 2 reports a cycle after at most N body iterations. Status 3 reports signed
integer overflow; status 4 reports integer modulo by zero. The manifest's
`scalar_dtype` and parameter dtypes identify the numeric storage type.
Failed lanes do not write results; the caller must inspect status before consuming them. This
runtime rejection defines the accepted finite-chain input domain, rather than
silently truncating a cyclic Jac walk. Threads beyond M touch no buffers.

Node order is arbitrary: move all fields together and remap next/heads. The
kernel follows next, including backwards and shared links. Reordering walker
slots requires moving heads/initial states together and restoring output order.
The verifier emits a four-walker Ours layout example, not an automatic layout
optimizer or a performance benchmark.

## CPU differential and compilation checks

```bash
python3 -B scripts/gpu_walker/verify.py \
  --shim /absolute/path/to/libjacllvm.so \
  --cache /tmp/jac-gpu-compiler-cache \
  --output /tmp/jac-chain-verification
```

The script emits device PTX and verifies LLVM IR. Separately, it lowers the
same selected ability and traversal loop for the host CPU with an explicit lane
index, invokes lanes sequentially in reverse order, and compares against **real
Jac graph construction and serial walker execution** in an isolated in-memory
context, without a database. This is not a GPU emulator.
Checks include distinct initial states, empty batches and traversals, 31/32/33
and 257/1024 walker batches, uneven chains, shared suffixes, random node/walker
permutations, signed zero, subnormals, infinities, NaN, bounds/cycles, and changed
Jac body arithmetic. Unsupported source variants must fail compilation.

`results.json` records the checks and `gpu_executed: false`.
`four_walkers.inputs.json` contains concrete packed inputs and serial reference
results for packed-array inspection. CPU checks cannot verify CUDA launch argument
packing, device execution, warp scheduling, or GPU numerical behavior.

The regular tests are `jac/tests/compiler/backends/native/test_ptx_walker.jac`.
Run them with the scalar PTX and CLI regression tests when changing shared code.

Integer arithmetic and publication tests are also included in
`jac/tests/runtimelib/test_gpu.jac`. On a CUDA server with this checkout's Python
environment, run the same integer tests on both CPU lowering and real CUDA:

```bash
PYTHONPATH=jac JAC_GPU_TEST_CUDA=1 python3 -B scripts/gpu_walker/test_integers.py
```

The suite compares against ordinary Jac, checks negative modulo and int64 limits,
tests skipped branches and arithmetic failures, and verifies exact publication
and whole-batch rollback. Without the environment variable it uses CPU lowering
and a CUDA driver double, so a GPU is not required by the regular test runner.

Numeric reports are supported in both graph formats. See [report storage and
publication](runtime.md#numeric-reports) and `jac/examples/gpu/reports_run.jac`.

Boolean node and walker leaves use canonical 64-bit 0/1 SoA columns. Boolean
assignments and reports preserve Python `bool` identity. Streams containing
booleans use interleaved payload and tag columns in the v5 ABI; numeric-only
streams retain their existing representation. See `booleans_run.jac` and
`test_booleans.py` for serial comparisons and CUDA coverage.

## Matrix multiplication baseline

```bash
jac run jac/examples/gpu/matmul_run.jac
jac build jac/examples/gpu/matmul.jac --as ptx --gpu-entry DotProduct -o dist/gpu-matmul
```

`matmul_api.gpu_matmul(a, b)` returns `MatmulResult`, with the matrix in `.values`
and device execution information in `.execution`. Inputs are nonempty rectangular
matrices with matching inner dimensions. The example checks a 2x3 by 3x2 product
and a 32x16 by 16x33 product against serial Jac using float64 arithmetic.

Each output element has one `DotProduct` walker and a chain of K `ProductTerm`
nodes. The existing Jac compiler lowers the multiply and accumulation to PTX.
The graph packer discovers all starting nodes before successors, producing
`left[k * M * N + lane]` and `right[k * M * N + lane]` SoA columns; adjacent
walkers read adjacent slots at each dot-product step.

This is a graph-based correctness and layout baseline. It duplicates input
values into M*N*K nodes, requires `24*M*N*K + 28*M*N` device payload bytes,
and also builds graph objects on the host. It does not use shared-memory tiling
or tensor cores, and is intended for small matrices. A scalable dense matmul
needs direct matrix-array indexing and a separate kernel interface.

Run `PYTHONPATH=jac JAC_GPU_TEST_CUDA=1 python3 scripts/gpu_walker/test_matmul.py -v`
for shape, layout, input preservation, and real CUDA checks.

## Batched subtree queries

```bash
jac run jac/examples/gpu/subtree_query_run.jac
jac run jac/examples/gpu/subtree_query_run.jac --nodes 1023 --queries 2048
```

Each CSR walker queries a shared subtree using its own amount threshold and
returns a matching count, integer sum, boolean alert flag, and total visit count.
The runner checks every result against serial Jac and distinguishes CPU graph
construction, source compilation, and the complete GPU batch call. See the
[graph, semantics, and execution instructions](../../jac/examples/gpu/subtree_query.md).

## Device loops

`jac/examples/gpu/loops.jac` demonstrates dynamic `for i in range(here.value)`,
nested ranges, and `while` with a private scalar local. Both chain and CSR
kernels lower these to LLVM header/body/exit blocks with PHI values and a real
backedge. Runtime node values determine iteration counts; there is no compiler
constant unrolling. Each node ability invocation starts fresh local slots;
walker fields persist across nodes. Locals do not add kernel parameters.

Supported bounds are `range(stop)`, `range(start, stop)` and
`range(start, stop, step)`. Bounds are int64 expressions evaluated once on loop
entry; step must be a nonzero int64 literal (positive or negative). Internal
range advancement can terminate beyond int64 without an arithmetic error;
user arithmetic still reports int64 overflow. Range targets are fresh,
read-only locals visible only in their loop body. Initialize other int64,
float64 or boolean locals at ability top level before branches/loops; their
type must remain fixed. A `while` condition is a supported boolean expression
re-evaluated every iteration, including short-circuit expressions. Nested
loops, conditionals, walker field/local updates and scalar reports are allowed.

Explicitly rejected: loop `else`, `break`, `continue`, inner `visit`, other
iterables, unpacking targets, dynamic/zero range steps, writes to range targets,
new local declarations inside branches or loops, C-style iteration, and
async/comptime loops. The single typed tail
`visit` retains the existing traversal contract. Loops must terminate; graph
cycle/CSR visit bounds do not bound inner ability iterations. Device buffers,
matmul arrays and cooperative thread blocks remain outside this subset.

```bash
PYTHONPATH=jac python scripts/gpu_walker/test_loops.py -v
PYTHONPATH=jac python scripts/gpu_walker/test_reports.py -v
jac build jac/examples/gpu/loops.jac --as ptx --gpu-entry LoopSum -o /tmp/jac-loops
jac build jac/examples/gpu/loops.jac --as ptx --gpu-entry LoopSum --gpu-graph-format csr -o /tmp/jac-loops-csr
jac run jac/examples/gpu/loops.jac # serial Jac reference: 22
JAC_GPU_TEST_CUDA=1 PYTHONPATH=jac python scripts/gpu_walker/test_loops.py -v
```

Default tests compile NVPTX and execute the shared LLVM lowering using CPU JIT;
report/CSR runtime tests use a mock CUDA driver backed by that JIT. These are
not actual GPU execution. The opt-in CUDA command executes emitted PTX on a
working NVIDIA driver/device and compares against serial Jac and host JIT.

`jac run jac/examples/gpu/loops_run.jac` runs 64 actual walkers on CUDA with
per-node dynamic counts and nested loops, checking every result against serial
Jac. This command requires a working NVIDIA driver and device.

[2026-10-03 validation record](validation/loops_20261003.md) distinguishes
host JIT/mock checks from successful real RTX 3090 execution.

## Named multi-cursor walkers

[GPU named cursors](../../docs/design/gpu-named-cursors.md) documents the joint
arrival semantics, first GPU subset, typed multi-channel ABI and conservative
per-cursor batch BFS layout heuristic. The example is
`jac/examples/gpu/named_cursors.jac`; tests compare actual Jac CPU walkers with
LLVM host JIT and optional real CUDA execution:

```bash
PYTHONPATH=jac python scripts/gpu_walker/test_named_cursors.py -v
JAC_GPU_TEST_CUDA=1 PYTHONPATH=jac python scripts/gpu_walker/test_named_cursors.py -v
PYTHONPATH=jac python scripts/gpu_walker/compare_named_layouts.py --cuda --size 16 --repeats 3
```

The comparison records graph build, pack, allocation, H2D, synchronized kernel and
D2H costs. `--cuda` requires an actual accessible device; omitting it records host
JIT evidence and leaves device costs null. No CPU execution fallback substitutes
for CUDA. Shared input identities remain shared across channels and lanes.

### Reproducible named-cursor layout measurements

`compare_named_layouts.py` compares current discovery order, batch per-cursor
BFS prediction, and three fixed random physical permutations. Legacy chain
cases compare the existing packer against random permutations. Randomization
preserves physical identity deduplication, ordered CSR rows, repeated arrivals,
heads, lane assignment and all projected columns. Every launch is checked
against an integer/float CPU oracle and the current layout; selected lanes also
run the Jac CPU walker.

```sh
python scripts/gpu_walker/compare_named_layouts.py \
  --chain-cases 128x8 1024x64 --dot-cases 128x8 1024x32 \
  --matmul-cases 16x32x24 32x64x48 64x128x64 \
  --seeds 928 929 930 --warmup 6 --repeats 16 --profile \
  --output /tmp/jac-layout-exclusive
```

Use the repository Python environment, `PYTHONPATH=jac`, and the LLVM shim
configuration documented above. The script requires actual CUDA; mock execution
is never used for timing. Acquire an exclusive GPU interval before running it.
CSV/JSON include distributions and paired seed/pair ratios, separated resident
and one-shot modes. Graph construction and CPU oracle timing are separate.
Pack-through-D2H and graph-through-D2H are composed costs; the latter adds the
separately measured graph build and does not time application output publication.
Resident runs retain input buffers and exclude output poisoning/validation from
the kernel timer. CUDA event intervals may include host enqueue gaps; the
separate nsys replay supplies exact CUPTI kernel intervals. Profiler replay
reuses recorded packed inputs and does not measure CPU packing again.

Hardware counter capture uses a separate checksum-verified single-layout replay:

```sh
/opt/nvidia/nsight-compute/2025.2.1/ncu \
  --section SpeedOfLight --section MemoryWorkloadAnalysis --section Occupancy \
  --section LaunchStats --launch-skip 5 --launch-count 1 \
  --export /tmp/layout-counter --force-overwrite \
  python scripts/gpu_walker/profile_named_layout.py \
  --input /tmp/jac-layout-exclusive --case matmul-64x128x64 --layout Predicted
```

The default replay has one initialization kernel, four warmups, then the captured
kernel. Repeat for Current and Random-928/929/930. Counter profiling is separate
from ordinary timing; save the command, version, report and CSV export. Do not
interpret profiler replay timing as an unbiased performance benchmark. Counter
permission failures are evidence gaps: report measured times without attributing
cache, bandwidth, coalescing or occupancy bottlenecks.

The [recorded isolated experiment and evidence limits](../../docs/design/gpu-cursor-layout-results.md)
reports successful real-CUDA correctness, actual Current/Predicted array and
identity-order comparisons, paired seed distributions, Nsight timing and CPU
profiling. Hardware counter permission was unavailable; no cache/occupancy or
transaction explanation is claimed. Raw reports are retained under
[`dist/gpu-layout-exclusive-20261006/`](../../dist/gpu-layout-exclusive-20261006/README.md). The original run used `/tmp/jac-layout-exclusive/`; its complete archive is included in this repository.
`audit_layout_orders.py` rebuilds CPU graphs and checks every packed array against
the recorded SHA256 before recording deterministic discovery identity orders.
`profile_layout_cpu.py` produces CPU-only `.prof` files; `replay_layout_timings.py`
checks longer resident replay distributions; `analyze_layout_trace.py` extracts
correlated CUDA launch APIs and actual device copy events.

### Cursor concatenation prediction (2026-10-07)

The current `predicted` policy concatenates each cursor's complete multi-source
batch BFS in declaration order, deduplicates shared identities at first occurrence,
and appends unpredicted nodes in original discovery order. The former rank
interleaving implementation and mode are removed. The 2026-10-06 recorded
experiments remain historical evidence of that former policy.

Named-only experiments avoid compiling unrelated legacy Chain schemas:

```sh
PYTHONPATH=jac python scripts/gpu_walker/compare_named_layouts.py \
  --chain-cases --dot-cases 128x8 1024x32 \
  --matmul-cases 4x4x4 3x5x2 16x32x24 32x64x48 64x128x64 \
  --seeds 928 929 930 --warmup 6 --repeats 16 --profile \
  --output /tmp/jac-layout-cursor-concat-20261007
```

`audit_matmul_cursor_layout.py --output /tmp/concat-audit` records actual physical
indices/identity labels for 4×4 and rectangular matmul, preserves every typed input
and SHA256, and asserts complete A batch BFS precedes complete B batch BFS.
Labels are recovered from Current heads/CSR; matrix coordinates do not influence
packing. `analyze_layout_sectors.py --input <recorded-input-folder>` separately
models distinct aligned 32-byte sectors for each logical load/cursor/warp/round.
Its output is **theoretical addresses**, not executed instruction counts,
hardware requests/transactions, cache misses, DRAM bytes or a bottleneck profile.
Never use that model in place of unavailable Nsight Compute counters.

The [2026-10-07 results](../../docs/design/gpu-cursor-concatenation-results.md)
include full small-matrix index audits, all-case identity/hash checks, paired
seed timing distributions, independent Nsight traces and CPU process-time
profiles. Nsight Compute returned `ERR_NVGPUCTRPERM`; theoretical address sectors
are reported separately and do not establish hardware cache/transaction/DRAM
behavior. Raw artifacts remain in `dist/gpu-cursor-concat-20261007/` and
`/tmp/jac-layout-cursor-concat-20261007/`. The former 2026-10-06 report measures
the removed rank-interleaving policy and is retained as historical evidence.

## Handwritten CUDA matmul comparison

[Two int64 CUDA kernels](handwritten_matmul/matmul.cu) and a
[complete-output comparison with Jac](handwritten_matmul/validation/20261021/REPORT.md)
cover dense naive/tiled execution and Current/Predicted/Random real Jac graphs.
The runner checks identical inputs and all outputs, and separately reports CUDA
graph event intervals and verified Nsight kernel durations.

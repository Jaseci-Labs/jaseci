# Tiny graph frontend comparisons

Three CPU float64 examples for a one-page slide. Full runnable code is in
`cases.jac` (existing Jac tensor_graph library) and `direct_fx.py` (manual FX
GraphModule construction). `snippets.json` has exactly three entries with
`title`, `equation`, `jac`, `fx`; each snippet is at most nine lines and 65
characters per line. No existing library/example or parent-owned slide is edited.

| case | equation |
|---|---|
| Linear | `y = x @ w + b` |
| Shared computation / residual | `h = x @ w; y = relu(h) + h` |
| Lazy Cond | `h = x @ w; y = cond(c, h + x, h - x)` |

`w` has shape **[in, out]** in both frontends. There is no artificial weight
transpose. All examples use the same 2x2 x/w tensors and the same length-two bias
from `fixtures.py`. `c` is a scalar bool tensor; positive/negative predicate tests
mean True/False (not elementwise numeric masks).

## Slide scaffold disclosure (show outside the code panels)

Suggested short English footer:

> Shared imports, input/weight setup and execution are omitted on both sides.
> `cond_modules` builds BOTH branch graphs: t(h,x)=clone(h+x), f(h,x)=clone(h-x).

The snippets are architecture-construction bodies, without function wrappers,
validation or runners. Full definitions/imports are provided, not assumed free:

- Jac `base()` constructs `TensorGraph(output_name="y")`, Input x and Parameter w.
  Linear explicitly declares Parameter b; Cond explicitly declares Input c.
- FX `base(...)` constructs an FX Graph and x/w placeholders, plus optional b/c.
  Bias/weights are explicit tensor arguments when the GraphModule is invoked.
- FX aliases `mm`, `add`, `sub`, `relu` name exact ATen overloads. `fx`, `nn`,
  `torch`, `operator` and the Jac node types are imported in the full files.
- **`cond_modules(g, root, add, sub)` is real graph construction work**, shown as
  a helper to fit the panel. It constructs/registers two branch GraphModules,
  each with explicit h/x placeholders, Add or Subtract, and an output clone.
  It returns two `get_attr` Node handles. Its complete implementation and the
  branch builder are in `direct_fx.py`.
- The FX snippets include graph output and GraphModule wrapping. The Jac graph
  already has its output name in the base container. Execution is omitted on both
  sides: Jac `g.run(feeds)` invokes the library's Compute walker; FX runs the
  generated GraphModule with its explicit tensor arguments. Neither frontend
  calls the other to build/execute its graph.

Jac `g.add(...)` returns a **node-name string**; input dictionaries map named
ports to producer names. FX `graph.call_function(...)` returns an **fx.Node
handle**; argument tuples refer to producer handles. Both share the SAME h node
for fanout; neither rebuilds/recomputes x@w at each consumer.

## Cond semantics

Jac Cond's `true_result` and `false_result` edges reference lazy result roots.
The existing library analyzes transitive dependency slices, computes shared h
once before selection, and its Compute walker visits only the selected exclusive
branch. FX explicitly puts h in the outer graph and Add/Subtract inside two
branch GraphModules, passed as explicit `(h, x)` operands to
`torch.ops.higher_order.cond` (the higher-order operator behind `torch.cond`).
Branches have no hidden weights/buffers. Cloning matches Jac Cond's fresh
contiguous output and avoids higher-order output aliasing.

This is **not `torch.where(c, eager_true, eager_false)`**: that expression would
compute both branch values before selection. Constructing both branch graphs is
necessary on both sides; evaluating both branches is not. First-version library
limits still apply: one non-nested Cond, pure DAG, scalar bool, compatible outputs.

## Run

From the repository root, using the existing Torch CPU venv and local Jac source:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=jac XDG_CACHE_HOME=/tmp/graph-frontend-comparison-cache /tmp/transformer-python-comparison-venv/bin/python -m jaclang run --backend python jac/examples/graph_frontend_comparison/cases.jac
```

No Jac package installation is required: `PYTHONPATH=jac` loads the source
importer. First invocation can spend several minutes building compiler/stub
catalog caches. The graph store may require permission to use Jac's user cache.
CPU Torch 2.8.0+cpu is installed in the venv. Its optional missing-NumPy warning
is harmless for these tensor-only examples. There is no CUDA use, Inductor compile
sweep, benchmark, speed claim, training or compiler integration here.

The command executes real Jac graphs and independently constructed eager FX
GraphModules, compares both against direct Torch equations, then saves compact
`validation.json`, real `*_jac.dot` exports and actual `*_fx.py` inspection code.
Validation records CPU operator **counts only**, not timing: shared MatMul once
in each frontend, plus selected-only Add/Subtract. Metadata planning runs outside
those counts. Cond repeats True/False/True to check state reset and selection;
walker traces prove the unselected exclusive node was not visited. Generated
branch forward definitions are included in `cond_fx.py` for inspection.

Completed result: Torch 2.8.0+cpu, three cases / five forward calls, all errors
exactly **0**. Actual Jac traces and CPU operator counts in `validation.json`
confirm one shared MatMul per call. FX Cond executes Add only for True and
Subtract only for False; Jac traces likewise exclude the unselected branch.
`snippets.json` schema, line counts/widths and Python fragment syntax also pass.

## Native Jac revision: three separate slides

Use **`snippets_native.json`** for the corrected three-page deck. It has exactly
three cases with `title`, `equation`, `jac`, `fx`, `disclosure`. Each panel shows
only explicit graph construction/execution (at most 20 lines); do not squeeze
all node/walker definitions onto a panel. The disclosures belong on the slide.
The original library-API version above and its files are retained for history.

Runnable native sources are `native_linear.jac`, `native_residual.jac`, and
`native_cond.jac`. Each independently declares its custom node/edge types and
Run walker. They **do not import tensor_graph**, use a builder API, or rely on
built-in tensor-operation node types. `Graph`, `Value`, `Input`, `Weight`,
`MatMul`, `Add`, `ReLU`, `Subtract`, `Select`, `Output`, `TensorEdge`, `Seed`,
`Then`/`Else` and `Run` are example-defined archetypes. Native Jac provides node,
edge, walker, connection, typed traversal, `here`, `visit`, and `spawn` syntax;
Torch supplies numerical math inside the custom methods.

Native variables x/w/h hold **actual Jac node instances**; the `name` fields
are trace labels, not producer-name lookup keys. This differs from the older
library example's string-name binding. FX variables hold symbolic fx.Node
handles. Both now show explicit producer/consumer connections in their own syntax.

The handwritten walker routes values along actual `TensorEdge(port)` edges and
checks inbox readiness before visiting an operation. The residual has one h node
with two outgoing consumers. Cond has explicit data edges to both disabled
branches and explicit **Then/Else control edges** from a custom Select node.
Select waits for the scalar condition and shared h/x, then enables/visits only
the typed selected branch. Only that branch delivers to Output. This is honest
custom native control flow, **not automatic dependency extraction or arbitrary
Jac-to-FX/Inductor lowering**. The Python FX version independently builds its two
branch GraphModules; its helper work is disclosed rather than treated as free.

These are fixed tiny acyclic graphs: one producer per ordinary input port,
mutually exclusive producers at the conditional output, no cycles, mutation or
general scheduler error analysis. A **fresh graph is constructed per invocation**;
reusing an existing graph would require explicit inbox/value/enabled-state reset.
No general lifetime optimizer or production tensor runtime is claimed.

Run all three actual native programs from the repository root:

```bash
/tmp/transformer-python-comparison-venv/bin/python jac/examples/graph_frontend_comparison/run_native.py
```

The driver sets local `PYTHONPATH=jac`, disables .pyc writes, uses the same
external compiler cache, and invokes each `.jac` program through `jaclang run
--backend python`. Jac's graph traversal requires access to its user-cache graph
store (`~/.cache/jac/pg/main.lock`); a restricted sandbox may need execution
permission outside that sandbox. This is required runtime access, not a request
to alter the shared compiler/library.

**Actual native validation passed**: CPU float64, linear/residual plus Cond
True/False/True, exact error **0** against independent FX and direct equations.
CPU operator counts verify one MatMul in each frontend per call; selected-only
Add/Subtract counts and native walker traces confirm lazy branch execution.
Results are in `validation_native.json` and per-case `validation_native_*.json`.
`native_validation.py` only supplies test inputs, runs the native functions and
checks results; numerical graph execution occurs in the Jac walkers. No compile
sweep, GPU work, slide edits, commits or pushes were performed.

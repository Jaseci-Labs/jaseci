# Native Jac vs direct Python FX

[English PDF](jac-vs-python-fx.pdf): three pages, one example per page:
Linear, shared MatMul/residual, and lazy conditional.

Jac uses actual node instances, native typed edge connections and walker spawn.
It does not import the tensor_graph library or use its graph-building API.
Custom operation nodes, port-ready routing and the Run walker are defined in the
full runnable native_*.jac examples; they are not language builtins. Cond uses
explicit typed Then/Else control edges, rather than automatic region extraction.
These native programs are not automatically compiled into FX.

Python constructs FX directly. Its cond_modules helper builds both branch
GraphModules with explicit operands. Both frontends use the same equations and
CPU float64 fixtures; all five forward calls pass with zero error. Shared MatMul
executes once per call, and the unselected exclusive branch is skipped.

The latest deck uses enlarged, operation-aligned presentation excerpts, rather
than full runnable-source exports. A/B/X are explanatory aliases for typed
input-port edges, and required constructor names/values, node/walker definitions,
input registration and execution are omitted. Cond's gate inputs and branch
activation are omitted and explicitly disclosed. These excerpts are not
standalone executable code and do not alter the tested examples. Cond aligns
semantic regions, not one node per node or source line per source line.
No language usability advantage or performance advantage is assumed.

Regenerate with Python and Matplotlib:

```sh
python docs/presentations/graph-frontends/generate.py
```

Evidence: `jac/examples/graph_frontend_comparison/validation_native.json`.

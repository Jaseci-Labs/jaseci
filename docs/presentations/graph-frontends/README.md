# Native Jac vs direct Python FX

[English PDF](jac-vs-python-fx.pdf): seven pages. Two context slides connect to
the professor-provided *Two Roads to the GPU*, followed by three example pages
and two discussion slides on current evidence and the research goal. Examples:
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

## ONNX comparison

All three example slides now include direct Python ONNX construction excerpts.
`N` aliases `onnx.helper.make_node`; `G` aliases `make_graph`. Input/output
value infos, graph/model wrapping, opset selection and execution are omitted.
The conditional uses an ONNX If with two branch GraphProto attributes; these
branches reference the outer h and x through lexical scope. It does not eagerly
execute both branch calculations. ONNX excerpts are documentation-checked API
illustrations, not newly runtime-validated examples. Existing Jac/FX correctness
results do not constitute ONNX validation.

Official references:
- https://onnx.ai/onnx/api/helper.html
- https://onnx.ai/onnx/operators/onnx__If.html

Only presentation files changed for this addition; runnable examples are untouched.

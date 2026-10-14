"""Jac node/port graphs; execute using the existing library Compute walker."""
import from jaclang.lib.tensor_graph {
    TensorGraph, Input, Parameter, MatMul, Add, ReLU, Subtract, Cond
}
import fixtures;
import validation;
import os;

def base -> TensorGraph {
    values = fixtures.tensors();
    g = TensorGraph(output_name="y");
    g.add(Input(name="x"));
    g.add(Parameter(name="w", value=values["w"]));
    return g;
}

def linear -> TensorGraph {
    g = base();
    g.add(Parameter(name="b", value=fixtures.tensors()["b"]));
    h = g.add(MatMul(name="h"), {"a": "x", "b": "w"});
    g.add(Add(name="y"), {"a": h, "b": "b"});
    return g;
}

def residual -> TensorGraph {
    g = base();
    h = g.add(MatMul(name="h"), {"a": "x", "b": "w"});
    r = g.add(ReLU(name="r"), {"x": h});
    g.add(Add(name="y"), {"a": r, "b": h});
    return g;
}

def conditional -> TensorGraph {
    g = base();
    g.add(Input(name="c"));
    h = g.add(MatMul(name="h"), {"a": "x", "b": "w"});
    t = g.add(Add(name="t"), {"a": h, "b": "x"});
    f = g.add(Subtract(name="f"), {"a": h, "b": "x"});
    g.add(Cond(name="y"), {"condition": "c",
        "true_result": t, "false_result": f});
    return g;
}

with entry {
    validation.main(linear(), residual(), conditional(),
                    os.path.dirname(__file__));
}

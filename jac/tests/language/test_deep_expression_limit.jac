"""A long operator chain compiles instead of exhausting the compiler's stack.
The walkers are driven directly at a depth no compile would reach."""

import os;
import subprocess;
import tempfile;
import from jaclang.compiler.backends.py.jcir_gen_pass { CgNode, write_ir_value }
import from jaclang.compiler.backends.py.codegen_ir { CodegenIrWriter }
import from jaclang.compiler.frontend.parser.frontend { parse }
import from jaclang.compiler.frontend.unitree { BinaryExpr }
import from tests.support { JAC_ROOT, jac_command }

glob TREE_DEPTH: int = 20000,
     IR_DEPTH: int = 50000;

def chain_source(operands: int) -> str {
    return (
        "import sys;\nwith entry {\n    x = "
        + "+".join(["1"] * operands)
        + ";\n    sys.stdout.write(str(x));\n}\n"
    );
}

def write_chain(dir: str, operands: int) -> str {
    path = os.path.join(dir, "chain.jac");
    with open(path, "w") as f {
        f.write(chain_source(operands));
    }
    return path;
}

def run_jac(cmd: str, path: str) -> str {
    result = subprocess.run(
        jac_command(cmd, path), capture_output=True, text=True, cwd=JAC_ROOT
    );
    return result.stdout + result.stderr;
}

def deep_cg_node(depth: int) -> CgNode {
    tree = CgNode(cls="Constant", keys=["value"], vals=[1]);
    for _ in range(depth) {
        tree = CgNode(cls="BinOp", keys=["left"], vals=[tree]);
    }
    return tree;
}

test "the sub-node table and flatten handle a tree far deeper than any stack allows" {
    (mod, had_error) = parse(chain_source(TREE_DEPTH));
    assert not had_error;

    ops = mod.get_all_sub_nodes(BinaryExpr);
    assert len(ops) == TREE_DEPTH - 1 , len(ops);

    nodes = mod.flatten();
    assert len(nodes) > TREE_DEPTH , len(nodes);
    assert nodes[0] is mod;
}

test "the ir emitter writes a value tree far deeper than any stack allows" {
    w = CodegenIrWriter();
    w.begin_module("<deep>");
    write_ir_value(w, deep_cg_node(IR_DEPTH));
    w.end_module();
    assert len(w.to_bytes()) > IR_DEPTH;
}

test "a ten thousand operand chain still gives the right answer" {
    # Native lowering recurses per operator and gives out near six thousand,
    # so above that the compiler falls back and warns; the answer stays right.
    with tempfile.TemporaryDirectory() as dir {
        out = run_jac("run", write_chain(dir, 10000));
        assert "10000" in out , out;
        assert "✖ Error" not in out , out;
    }
}

test "a ten thousand operand chain type checks" {
    with tempfile.TemporaryDirectory() as dir {
        out = run_jac("check", write_chain(dir, 10000));
        assert "maximum recursion depth" not in out , out;
        assert "1 passed" in out , out;
    }
}

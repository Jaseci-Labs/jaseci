"""A comptime fold is cached on the consumer's own source, nothing else.

A module that folds a value out of another module at compile time bakes that
value into its own artifact. Its cache entry is keyed on its own source and
annexes only, so editing the producer leaves the consumer's cached fold in
place until the consumer itself changes (or the cache is cleared).

Every test builds its own throwaway project in a tempdir and points the
platform cache-home variables at that tempdir while it runs, so the JIR
the test writes lands under the tempdir instead of the user's shared
cache, and tests are isolated from each other.
"""

import os;
import tempfile;
import time;
import from jaclang.compiler.driver.compiler { JacCompiler }
import from jaclang.compiler.driver.jir {
    SEC_NBITCODE,
    SEC_NOBJ,
    read_section_bytes
}
import from jaclang.compiler.driver.program { JacProgram }
import from jaclang.compiler.driver.ifacecache { artifact_cache_path }
import from types { CodeType }
import from unittest.mock { patch }
import from tests.support { cache_env }

glob SPEC_SRC: str = "obj Spec {\n    has name: str,\n        help: str;\n}\n",
     OTHER_SRC: str = "def helper -> int {\n    return 1;\n}\n",
     OTHER_SRC_EDIT: str = "def helper -> int {\n    return 2;\n}\n",
     CONSUMER_SRC: str = (
         "import from specmod { Spec }\n"
         "import from othermod { helper }\n\n"
         "comptime import from prodmod { SPEC }\n\n"
         "comptime FOLDED: str = SPEC.help;\n\n"
         "with entry {\n"
         "    print(FOLDED);\n"
         "    print(helper());\n"
         "}\n"
     );

def _isolated(tmp: str) -> any {
    env = cache_env(os.path.join(tmp, "cache"));
    env["JAC_HANDOFF"] = "";
    return patch.dict(os.environ, env);
}

def _base_src(text: str) -> str {
    return f"comptime BASE: str = \"{text}\";\n";
}

def _prod_src(text: str) -> str {
    return (
        "import from specmod { Spec }\n\n"
        "comptime import from basemod { BASE }\n\n"
        f"comptime SPEC: Spec = Spec(name=\"create\", help=BASE + \"{text}\");\n"
    );
}

def _write(path: str, body: str, backdate: bool = False) {
    with open(path, "w") as fh {
        fh.write(body);
    }
    if backdate {
        past = time.time() - 5;
        os.utime(path, (past, past));
    }
}

def _project -> dict[str, str] {
    tmp = tempfile.mkdtemp();
    paths: dict[str, str] = {"root": tmp};
    for name in ("specmod", "othermod", "basemod", "prodmod", "consmod") {
        paths[name] = os.path.realpath(os.path.join(tmp, f"{name}.jac"));
    }
    _write(paths["specmod"], SPEC_SRC, backdate=True);
    _write(paths["othermod"], OTHER_SRC, backdate=True);
    _write(paths["basemod"], _base_src("base one"), backdate=True);
    _write(paths["prodmod"], _prod_src(" help"), backdate=True);
    _write(paths["consmod"], CONSUMER_SRC, backdate=True);
    return paths;
}

def _consts(code: CodeType) -> list[str] {
    out: list[str] = [];
    for c in code.co_consts {
        if isinstance(c, str) {
            out.append(c);
        } elif hasattr(c, "co_consts") {
            out.extend(_consts(c));
        }
    }
    return out;
}

def _folded(path: str) -> list[str] {
    compiler = JacCompiler();
    prog = JacProgram();
    code = compiler.get_bytecode(path, prog);
    assert code is not None , (
        f"no bytecode for {path}: " f"{[a.pretty_print() for a in prog.errors_had]}"
    );
    return _consts(code);
}

test "a producer edit leaves the consumer's cached fold in place" {
    paths = _project();
    with _isolated(paths["root"]) {
        cold = _folded(paths["consmod"]);
        assert "base one help" in cold , f"cold compile did not fold: {cold}";
        _write(paths["prodmod"], _prod_src(" HELP"));
        warm = _folded(paths["consmod"]);
        assert "base one help" in warm , (
            f"a producer edit invalidated the consumer's cache: {warm}"
        );
        _write(paths["consmod"], CONSUMER_SRC + "\n");
        rebuilt = _folded(paths["consmod"]);
        assert "base one HELP" in rebuilt , (
            f"editing the consumer did not refold its producer: {rebuilt}"
        );
    }
}

test "an ordinary runtime import leaves a server consumer's fold cache alone" {
    paths = _project();
    _write(
        os.path.join(paths["root"], "jac.toml"),
        '[project]\nname = "fold-cache"\n[placement.pins]\nconsmod = "server"\n'
    );
    with _isolated(paths["root"]) {
        _folded(paths["consmod"]);
        cache = artifact_cache_path(paths["consmod"], JacProgram());
        assert read_section_bytes(cache.read_bytes(), SEC_NOBJ) is None;
        assert read_section_bytes(cache.read_bytes(), SEC_NBITCODE) is None;
        held = cache.read_bytes();
        _write(paths["othermod"], OTHER_SRC_EDIT);
        _folded(paths["consmod"]);
        assert cache.read_bytes() == held , (
            "a body-only edit to an ordinary dependency rebuilt the consumer"
        );
    }
}

test "a fold still resolves when the producer is served from its cache" {
    paths = _project();
    with _isolated(paths["root"]) {
        cold = _folded(paths["consmod"]);
        assert "base one help" in cold , f"cold compile did not fold: {cold}";
        artifact_cache_path(paths["consmod"], JacProgram()).unlink();
        again = _folded(paths["consmod"]);
        assert "base one help" in again , (
            f"the fold broke once the producer came back from cache: {again}"
        );
    }
}

test "a comptime embed cannot read outside its package root" {
    tmp = tempfile.mkdtemp();
    with _isolated(tmp) {
        proj = os.path.join(tmp, "pkg");
        os.makedirs(proj);
        _write(os.path.join(proj, "jac.toml"), "[project]\nname = \"pkg\"\n");
        _write(os.path.join(tmp, "secret.txt"), "top secret");
        src = os.path.realpath(os.path.join(proj, "leak.jac"));
        _write(
            src,
            "import from jaclang.comptime { embed_file }\n\n"
            "comptime BLOB: str = embed_file(\"../secret.txt\");\n\n"
            "with entry {\n"
            "    print(BLOB);\n"
            "}\n"
        );
        prog = JacProgram();
        JacCompiler().get_bytecode(src, prog);
        msgs = [a.pretty_print() for a in prog.errors_had];
        assert any("outside the package root" in m for m in msgs) , msgs;
    }
}

"""The engine run as `node`: the Node.js behaviors npm tooling (expo, chalk,
bin scripts) relies on. It runs where an engine is built (`jac native build
js-engine`, the `native:js-engine` CI lane) and skips elsewhere."""

import json;
import subprocess;
import tempfile;
import from pathlib { Path }
import from jaclang.client.js_engine { node_executable }

"""Run `script` (a file in `work`) under the engine and return its stdout."""
def run_script(work: Path, script: str) -> str {
    import from jaclang.artifacts.router { resolve }
    if resolve("js-engine").found is None {
        testskip("no js_engine is built here (jac native build js-engine)");
    }
    result = subprocess.run(
        [node_executable(), str(work / script)],
        cwd=str(work),
        capture_output=True,
        text=True,
        timeout=60
    );
    assert result.returncode == 0 , f"exit {result.returncode}:\n{result.stderr}";
    return result.stdout.strip();
}

def run_source(source: str) -> str {
    with tempfile.TemporaryDirectory() as tmp {
        work = Path(tmp);
        (work / "main.js").write_text(source);
        return run_script(work, "main.js");
    }
}

test "an optional chain short-circuits the calls and members after it" {
    out = run_source(
        "const a = null;\n"
            + "const o = { f() { return null; }, g() { return { h: () => 3 }; } };\n"
            + "console.log(JSON.stringify([\n"
            + "  a?.b().c === undefined,\n"
            + "  a?.b.c.d() === undefined,\n"
            + "  a?.[0].x === undefined,\n"
            + "  o.f()?.x.y === undefined,\n"
            + "  o.g()?.h() === 3,\n"
            + "  (a?.b)?.c === undefined,\n"
            + "  [a?.b().c, 1][1] === 1,\n"
            + "]));\n"
    );
    assert json.loads(out) == [True, True, True, True, True, True, True];
}

test "a required bin script keeps its hashbang line" {
    with tempfile.TemporaryDirectory() as tmp {
        work = Path(tmp);
        (work / "cli.js").write_text("#!/usr/bin/env node\nmodule.exports = 42;\n");
        (work / "main.js").write_text("console.log(require('./cli.js'));\n");
        assert run_script(work, "main.js") == "42";
    }
}

test "a function reads getters it inherits from a custom prototype" {
    out = run_source(
        "const proto = {};\n"
            + "Object.defineProperty(proto, 'bold', { get() { return typeof this; } });\n"
            + "function builder() {}\n"
            + "Object.setPrototypeOf(builder, proto);\n"
            + "const viaVar = builder.bold;\n"
            + "const key = 'bold';\n"
            + "console.log(JSON.stringify([viaVar, builder[key], 'bold' in builder]));\n"
    );
    assert json.loads(out) == ["function", "function", True];
}

test "module.exports defined as a getter is what require returns" {
    with tempfile.TemporaryDirectory() as tmp {
        work = Path(tmp);
        (work / "lazy.js").write_text(
            "Object.defineProperty(module, 'exports', { get() { return { v: 7 }; } });\n"
        );
        (work / "main.js").write_text("console.log(require('./lazy.js').v);\n");
        assert run_script(work, "main.js") == "7";
    }
}

test "process.version reports the Node.js API level" {
    out = run_source(
        "console.log(JSON.stringify([process.version, process.versions.node,"
            + " process.release.name]));\n"
    );
    (version, api, name) = json.loads(out);
    assert version == "v" + api;
    assert name == "node";
}

"""js_engine is an accelerator over bun. A release ships bun; an engine built
by `jac native build js-engine` (zig-out/js, with a record of the js_engine/
sources it came from) is used whenever it is current, for running tools and
for package management alike. A stale engine is not."""

import json;
import os;
import from pathlib { Path }
import from tempfile { TemporaryDirectory }
import from unittest.mock { patch }
import from jaclang.artifacts.model { Probe, Source }
import jaclang.artifacts.router as router;
import jaclang.client.js_runtime as js_runtime;
import from jaclang.client.js_runtime { JsEngineArtifact, RECORD_SUFFIX }

def _tree(base: Path) -> Path {
    repo = base / "jac";
    for rel in (
        "engine/src/main.jac",
        "napi/src/napi.jac",
        "native/build_native.zig"
    ) {
        path = repo / "js_engine" / rel;
        path.parent.mkdir(parents=True, exist_ok=True);
        path.write_text(f"// {rel}\n");
    }
    (repo / "js_engine" / "jac.toml").write_text("[project]\nname = 'js_engine'\n");
    return repo;
}

def _built_engine(repo: Path, digest: str) -> Path {
    engine = repo / "zig-out" / "js";
    engine.mkdir(parents=True);
    (engine / "libjs_engine.so").write_bytes(b"\x7fELF");
    (engine / RECORD_SUFFIX).write_text(json.dumps({"inputs": digest}));
    return engine;
}

def _probe(repo: Path) -> Probe {
    with patch.object(js_runtime, "_repo_root", return_value=str(repo)) {
        return JsEngineArtifact().probe_checkout();
    }
}

test "an engine built from these sources is current; an edit makes it stale" {
    with TemporaryDirectory() as tmp {
        repo = _tree(Path(tmp));
        assert _probe(repo).found is None , "nothing is built yet";
        engine = _built_engine(repo, js_runtime.js_engine_inputs_digest(str(repo)));
        found = _probe(repo).found;
        assert found is not None and found.source == Source.CHECKOUT;
        assert found.path == str(engine);
        (repo / "js_engine" / "engine" / "src" / "main.jac").write_text("// edited\n");
        stale = _probe(repo);
        assert stale.found is None and "js_engine/ changed" in stale.drift[0];
    }
}

def _with_engine(engine: (str | None), fn: any) -> any {
    resolved = Probe.hit(Source.CHECKOUT, engine, {}) if engine else Probe.missing();
    router.forget();
    try {
        with patch.object(JsEngineArtifact, "probe_sealed", return_value=None), patch.object(
            JsEngineArtifact, "probe_checkout", return_value=resolved
        ), patch.object(JsEngineArtifact, "probe_kit", return_value=Probe.missing()) {
            return fn();
        }
    } finally {
        router.forget();
    }
}

test "a current engine runs the tools and the package manager; otherwise bun does" {
    calls: list[tuple[list[str], str, bool]] = [];
    def engine_pm(args: list[str], cwd: str, capture: bool) -> tuple[int, str] {
        calls.append((list(args), cwd, capture));
        return (0, "engine");
    }
    with TemporaryDirectory() as tmp {
        def with_engine -> any {
            with patch(
                "jaclang.client.js_engine.node_executable",
                return_value=f"{tmp}/bin/node"
            ), patch("jaclang.client.js_engine.run_pm", side_effect=engine_pm) {
                return (
                    js_runtime.js_runtime_path(),
                    js_runtime.run_pm(["install"], tmp, capture=True)
                );
            }
        }
        (path, outcome) = _with_engine(tmp, with_engine);
        assert path == f"{tmp}/bin/node";
        assert outcome == (0, "engine") and calls == [(["install"], tmp, True)];
    }
    ran: list[list[str]] = [];
    def bun_run(argv: list[str], **kwargs: any) -> any {
        ran.append(list(argv));
        class _Done {
            has returncode: int = 0,
                stdout: str = "out",
                stderr: str = "";
        }
        return _Done();
    }
    def with_bun -> any {
        with patch.object(js_runtime, "js_runtime_path", return_value="/opt/bun"), patch(
            "subprocess.run", side_effect=bun_run
        ) {
            return js_runtime.run_pm(["add", "vite"], "/proj", capture=True);
        }
    }
    assert _with_engine(None, with_bun) == (0, "out");
    assert ran == [["/opt/bun", "add", "vite"]];
}

test "a release image that carries no engine runs bun quietly" {
    import sys;
    import io;
    err = io.StringIO();
    router.forget();
    try {
        with patch.object(
            JsEngineArtifact, "probe_sealed", return_value=Probe.by_design()
        ), patch.object(sys, "stderr", err) {
            resolution = router.resolve("js-engine");
        }
    } finally {
        router.forget();
    }
    assert resolution.on_floor() and resolution.quiet;
    assert err.getvalue() == "";
}

test "a build installs the engine for every jac; a sealed jac finds it there" {
    import sys;
    with TemporaryDirectory() as tmp {
        repo = _tree(Path(tmp));
        built = _built_engine(repo, js_runtime.js_engine_inputs_digest(str(repo)));
        installed = Path(tmp) / "cache" / "js-engine" / "current";
        with patch.object(
            js_runtime, "installed_engine_dir", return_value=str(installed)
        ) {
            js_runtime._install_engine(str(built));
            assert (installed / "libjs_engine.so").is_file();
            js_runtime._install_engine(str(built));
            assert (installed / "libjs_engine.so").is_file() , "a reinstall replaces it whole";
            with patch(
                "jaclang.jac0core.sealed._jaclang_image", return_value=object()
            ), patch.object(sys, "prefix", str(Path(tmp) / "rt" / "python")) {
                found = JsEngineArtifact().probe_sealed();
            }
            assert found is not None and found.found is not None;
            assert found.found.source == Source.CACHE;
            assert found.found.path == str(installed);
            with patch.object(js_runtime, "_repo_root", return_value=str(repo)) {
                assert JsEngineArtifact().probe_kit().found is None , "a js_engine checkout uses its own build";
            }
            with patch.object(js_runtime, "_repo_root", return_value=tmp) {
                assert JsEngineArtifact().probe_kit().found is not None;
            }
        }
    }
}

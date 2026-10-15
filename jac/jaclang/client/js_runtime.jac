import json;
import os;
import platform;

glob BUN_VERSION: str = "1.3.11",
     RECORD_SUFFIX: str = ".artifact.json",
     ENGINE_LIBRARY: str = "libjs_engine.so",
     ENGINE_SOURCES: tuple[str, ...] = ("engine/src", "napi/src", "native", "jac.toml");

def bun_name -> str {
    return "bun.exe" if platform.system() == "Windows" else "bun";
}

def bun_path_in(pkg_dir: str) -> str {
    return os.path.join(pkg_dir, "client", "_bun", bun_name());
}

def write_bun_record(path: str) {
    atomic_write(
        path + RECORD_SUFFIX, json.dumps({"version": BUN_VERSION}).encode("utf-8")
    );
}

def _recorded_version(path: str) -> str {
    try {
        with open(path + RECORD_SUFFIX, encoding="utf-8") as f {
            return str(json.load(f).get("version", ""));
        }
    } except (OSError, ValueError, AttributeError) {
        return "";
    }
}

def _probe_bun(path: str, source: Source) -> Probe {
    if not os.path.isfile(path) {
        return Probe.missing();
    }
    recorded = _recorded_version(path);
    if recorded != BUN_VERSION {
        return Probe.stale(
            [f"bun {recorded or 'of unknown version'} is not the pinned {BUN_VERSION}"]
        );
    }
    if platform.system() != "Windows" and not os.access(path, os.X_OK) {
        os.chmod(path, 0o755);
    }
    return Probe.hit(source, path, {"version": recorded});
}

def _pkg_dir -> str {
    return jaclang_pkg_root();
}

obj BunArtifact(Artifact) {
    has name: str = "bun",
        kind: ArtifactKind = ArtifactKind.CAPABILITY,
        release: ReleasePolicy = ReleasePolicy.REQUIRED,
        summary: str = "bun (the shipped JavaScript runtime)";

    override def probe_sealed -> (Probe | None) {
        image = sealed._jaclang_image();
        if image is None {
            return None;
        }
        return _probe_bun(bun_path_in(str(image.pkg_dir)), Source.SEALED);
    }

    override def probe_checkout -> Probe {
        return _probe_bun(bun_path_in(_pkg_dir()), Source.CHECKOUT);
    }

    override def probe_kit -> Probe {
        found = kit_image();
        if found is None {
            return Probe.missing("this process runs on no kit");
        }
        return _probe_bun(bun_path_in(found[0]), Source.KIT);
    }

    override def checkout_path -> str {
        return bun_path_in(_pkg_dir());
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        fetch_bun(osarch(), os.path.dirname(self.checkout_path()));
    }
}

def _repo_root -> str {
    return os.path.dirname(_pkg_dir());
}

def js_engine_build_dir -> str {
    return os.path.join(_repo_root(), "zig-out", "js");
}

def js_engine_inputs_digest(repo_root: str) -> str {
    import hashlib;
    digest = hashlib.sha256();
    base = os.path.join(repo_root, "js_engine");
    for rel in ENGINE_SOURCES {
        top = os.path.join(base, rel);
        paths = [top]
            if os.path.isfile(top)
            else sorted(
                os.path.join(d, f) for (d, _dirs, files) in os.walk(top) for f in files
            );
        for path in paths {
            digest.update(os.path.relpath(path, base).encode("utf-8"));
            with open(path, "rb") as f {
                digest.update(hashlib.sha256(f.read()).digest());
            }
        }
    }
    return digest.hexdigest();
}

def installed_engine_dir -> str {
    return str(bucket("js-engine").path() / "current");
}

def _installed_engine -> Probe {
    engine = installed_engine_dir();
    return Probe.hit(Source.CACHE, engine, {"inputs": _engine_record(engine)})
        if os.path.isfile(os.path.join(engine, ENGINE_LIBRARY))
        else Probe.missing("no engine is installed (jac native build js-engine)");
}

def ensure_node_link(engine: str) -> str {
    link = os.path.join(engine, "bin", "node");
    exe = process_executable();
    try {
        current = os.readlink(link);
    } except OSError {
        current = "";
    }
    if current != exe {
        os.makedirs(os.path.dirname(link), exist_ok=True);
        staged = f"{link}.{os.getpid()}";
        os.symlink(exe, staged);
        os.replace(staged, link);
    }
    return link;
}

def _install_engine(built: str) {
    import shutil;
    target = installed_engine_dir();
    os.makedirs(os.path.dirname(target), exist_ok=True);
    staging = f"{target}.{os.getpid()}";
    retired = f"{target}.old.{os.getpid()}";
    shutil.rmtree(staging, ignore_errors=True);
    shutil.copytree(built, staging, symlinks=True);
    if os.path.isdir(target) {
        os.replace(target, retired);
    }
    os.replace(staging, target);
    shutil.rmtree(retired, ignore_errors=True);
}

def _engine_record(engine: str) -> str {
    try {
        with open(os.path.join(engine, RECORD_SUFFIX), encoding="utf-8") as f {
            return str(json.load(f).get("inputs", ""));
        }
    } except (OSError, ValueError, AttributeError) {
        return "";
    }
}

obj JsEngineArtifact(Artifact) {
    has name: str = "js-engine",
        kind: ArtifactKind = ArtifactKind.ACCELERATOR,
        release: ReleasePolicy = ReleasePolicy.FLOOR,
        summary: str = "js_engine (the native JavaScript runtime)",
        floor: str = "bun",
        hosts: list[str] = ["linux-x86_64"];

    override def probe_sealed -> (Probe | None) {
        import sys;
        if sealed._jaclang_image() is None {
            return None;
        }
        engine = os.path.join(os.path.dirname(sys.prefix), "js");
        if os.path.isfile(os.path.join(engine, ENGINE_LIBRARY)) {
            return Probe.hit(Source.SEALED, engine, {});
        }
        installed = _installed_engine();
        return installed if installed.found is not None else Probe.by_design();
    }

    override def probe_checkout -> Probe {
        engine = js_engine_build_dir();
        if not os.path.isfile(os.path.join(engine, ENGINE_LIBRARY)) {
            return Probe.missing();
        }
        if _engine_record(engine) != js_engine_inputs_digest(_repo_root()) {
            return Probe.stale(["js_engine/ changed since the engine was built"]);
        }
        return Probe.hit(Source.CHECKOUT, engine, {});
    }

    override def probe_kit -> Probe {
        if os.path.isdir(os.path.join(_repo_root(), "js_engine")) {
            return Probe.missing("a checkout with js_engine/ uses its own build");
        }
        return _installed_engine();
    }

    override def checkout_path -> str {
        return js_engine_build_dir();
    }

    override def built -> Probe {
        found = self.probe_checkout();
        if found.found is None {
            return found;
        }
        if _engine_record(installed_engine_dir()) != _engine_record(found.found.path) {
            return Probe.stale(["the engine is built but not installed"]);
        }
        return found;
    }

    override def build_blocker -> str {
        import shutil;
        if not os.path.isdir(os.path.join(_repo_root(), "js_engine")) {
            return "this tree has no js_engine/";
        }
        if shutil.which("zig") or self.probe_checkout().found is not None {
            return "";
        }
        return "zig is not on PATH";
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        import subprocess;

        if force or self.probe_checkout().found is None {
            log("  zig build js-engine (about 18 minutes and 7 GB cold)");
            subprocess.run(["zig", "build", "js-engine"], cwd=_repo_root(), check=True);
            atomic_write(
                os.path.join(js_engine_build_dir(), RECORD_SUFFIX),
                json.dumps({"inputs": js_engine_inputs_digest(_repo_root())}).encode(
                    "utf-8"
                )
            );
        }
        ensure_node_link(js_engine_build_dir());
        _install_engine(js_engine_build_dir());
        log(f"  installed for every jac at {installed_engine_dir()}");
    }

    override def floor_present -> bool {
        return resolve("bun").found is not None;
    }

    override def provide_floor(log: Callable[[str], None]) {
        build(["bun"], log);
    }
}

def _engine -> (str | None) {
    found = resolve("js-engine").found;
    return found.path if found is not None else None;
}

def js_runtime_path -> str {
    if _engine() is not None {
        import from jaclang.client.js_engine { node_executable }
        return node_executable();
    }
    bun = require("bun").found;
    assert bun is not None;
    return bun.path;
}

def run_pm(args: list[str], cwd: str, capture: bool = False) -> tuple[int, str] {
    import subprocess;
    runtime = js_runtime_path();
    env = dict(os.environ);
    if _engine() is not None {
        env["PATH"] = os.path.dirname(runtime) + os.pathsep + env.get("PATH", "");
    }
    result = subprocess.run(
        [runtime] + list(args), cwd=cwd, env=env, text=True, capture_output=capture
    );
    if not capture {
        return (result.returncode, "");
    }
    return (
        result.returncode,
        (getattr(result, "stderr", "") or "") + (getattr(result, "stdout", "") or "")
    );
}

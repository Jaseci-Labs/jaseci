import json;
import os;
import platform;
import from jaclang.artifacts.model {
    Artifact,
    ArtifactKind,
    Probe,
    ReleasePolicy,
    Source
}

glob BUN_VERSION: str = "1.3.11",
     RECORD_SUFFIX: str = ".artifact.json",
     ENGINE_NOT_IN_TREE: str = "js_engine is not part of this tree yet (#9858)";

def bun_name -> str {
    return "bun.exe" if platform.system() == "Windows" else "bun";
}

def bun_path_in(pkg_dir: str) -> str {
    return os.path.join(pkg_dir, "client", "_bun", bun_name());
}

def write_bun_record(path: str) {
    import from jaclang.jac0core.cache_paths { atomic_write }
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
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    return jaclang_pkg_root();
}

obj BunArtifact(Artifact) {
    has name: str = "bun",
        kind: ArtifactKind = ArtifactKind.CAPABILITY,
        release: ReleasePolicy = ReleasePolicy.REQUIRED,
        summary: str = "bun (the shipped JavaScript runtime)";

    override def probe_sealed -> (Probe | None) {
        import from jaclang.jac0core { sealed }
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
        import from jaclang.artifacts.kit { kit_image }
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
        import from jaclang.artifacts.kit { osarch }
        import from jaclang.dist.payload.fetch { fetch_bun }
        fetch_bun(osarch(), os.path.dirname(self.checkout_path()));
    }
}

obj JsEngineArtifact(Artifact) {
    has name: str = "js-engine",
        kind: ArtifactKind = ArtifactKind.ACCELERATOR,
        release: ReleasePolicy = ReleasePolicy.FLOOR,
        summary: str = "js_engine (the native JavaScript runtime)",
        floor: str = "bun",
        hosts: list[str] = ["linux-x86_64"];

    override def probe_checkout -> Probe {
        return Probe.missing(ENGINE_NOT_IN_TREE);
    }

    override def checkout_path -> str {
        return "";
    }

    override def build_blocker -> str {
        return ENGINE_NOT_IN_TREE;
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        raise RuntimeError(ENGINE_NOT_IN_TREE);
    }

    override def floor_present -> bool {
        import from jaclang.artifacts.router { resolve }
        return resolve("bun").found is not None;
    }

    override def provide_floor(log: Callable[[str], None]) {
        import from jaclang.artifacts.router { build }
        build(["bun"], log);
    }
}

def js_runtime_path -> str {
    import from jaclang.artifacts.router { require, resolve }
    engine = resolve("js-engine").found;
    if engine is not None {
        return engine.path;
    }
    bun = require("bun").found;
    assert bun is not None;
    return bun.path;
}

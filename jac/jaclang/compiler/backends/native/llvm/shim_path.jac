import hashlib;
import json;
import os;
import sys;
import from jaclang.artifacts.model {
    Artifact,
    ArtifactKind,
    Probe,
    ReleasePolicy,
    Source
}

glob TOOLCHAIN_INPUTS: tuple[str, ...] = (
         "build.zig",
         "build.zig.zon",
         "bootstrap/pins.json"
     ),
     NATIVE_SOURCE_SUFFIXES: tuple[str, ...] = (".cpp", ".h", ".hpp"),
     RECORD_SUFFIX: str = ".artifact.json";

def shim_name -> str {
    if os.name == "posix" {
        return "libjacllvm.dylib" if sys.platform == "darwin" else "libjacllvm.so";
    }
    return "jacllvm.dll";
}

def placed_shim_path -> str {
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), shim_name());
}

def _repo_root -> str {
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    return os.path.dirname(jaclang_pkg_root());
}

def shim_inputs_digest(repo_root: str) -> str {
    h = hashlib.sha256();
    for rel in TOOLCHAIN_INPUTS {
        h.update(rel.encode());
        with open(os.path.join(repo_root, *rel.split("/")), "rb") as f {
            h.update(f.read());
        }
    }
    native = os.path.join(repo_root, "native");
    sources: list[str] = [];
    for (walk_dir, dirs, files) in os.walk(native) {
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
        ];
        for name in files {
            if name.endswith(NATIVE_SOURCE_SUFFIXES) {
                sources.append(
                    os.path.relpath(os.path.join(walk_dir, name), native).replace(
                        os.sep, "/"
                    )
                );
            }
        }
    }
    for rel in sorted(sources) {
        h.update(b"native/");
        h.update(rel.encode());
        with open(os.path.join(native, *rel.split("/")), "rb") as f {
            h.update(f.read());
        }
    }
    return h.hexdigest();
}

def write_shim_record(shim_path: str, repo_root: str) {
    import from jaclang.jac0core.cache_paths { atomic_write }
    atomic_write(
        shim_path + RECORD_SUFFIX,
        json.dumps({"inputs": shim_inputs_digest(repo_root)}).encode("utf-8")
    );
}

def _recorded_inputs(shim_path: str) -> str {
    try {
        with open(shim_path + RECORD_SUFFIX, encoding="utf-8") as f {
            return str(json.load(f).get("inputs", ""));
        }
    } except (OSError, ValueError, AttributeError) {
        return "";
    }
}

def _probe(shim_path: str, source: Source) -> Probe {
    if not os.path.isfile(shim_path) {
        return Probe.missing();
    }
    recorded = _recorded_inputs(shim_path);
    if not recorded {
        return Probe.stale(
            ["the shim carries no record of the sources it was built from"]
        );
    }
    repo = _repo_root();
    if not os.path.isdir(os.path.join(repo, "native")) {
        return Probe.hit(source, shim_path, {"inputs": recorded});
    }
    if recorded != shim_inputs_digest(repo) {
        return Probe.stale(
            ["jac/native, build.zig or the LLVM pin changed since it was built"]
        );
    }
    return Probe.hit(source, shim_path, {"inputs": recorded});
}

obj ShimArtifact(Artifact) {
    has name: str = "llvm-shim",
        kind: ArtifactKind = ArtifactKind.ACCELERATOR,
        release: ReleasePolicy = ReleasePolicy.REQUIRED,
        summary: str = "the LLVM shim (native code generation)",
        floor: str = "Python placement for native-default code";

    override def probe_sealed -> (Probe | None) {
        import from jaclang.jac0core { sealed }
        if sealed._jaclang_image() is None {
            return None;
        }
        path = placed_shim_path();
        return Probe.hit(Source.SEALED, path, {})
            if os.path.isfile(path)
            else Probe.missing("this image carries no LLVM shim");
    }

    override def probe_checkout -> Probe {
        return _probe(placed_shim_path(), Source.CHECKOUT);
    }

    override def probe_kit -> Probe {
        import from jaclang.artifacts.kit { kit_image, kit_path }
        if kit_image() is None {
            return Probe.missing("this process runs on no kit");
        }
        return _probe(
            kit_path(
                os.path.join("compiler", "backends", "native", "llvm", shim_name())
            ),
            Source.KIT
        );
    }

    override def checkout_path -> str {
        return placed_shim_path();
    }

    override def build_blocker -> str {
        import shutil;
        return "" if shutil.which("zig") else "zig is not on PATH";
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        import subprocess;
        log(
            "  zig build jacllvm (links the pinned LLVM; places the shim and its record)"
        );
        subprocess.run(["zig", "build", "jacllvm"], cwd=_repo_root(), check=True);
    }
}

def shim_path -> str {
    import from jaclang.artifacts.router { require }
    found = require("llvm-shim").found;
    assert found is not None;
    return found.path;
}

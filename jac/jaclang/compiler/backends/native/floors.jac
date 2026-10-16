import hashlib;
import os;
import sys;

glob WASM_FLOOR_MANIFEST: str = "SOURCES.sha256",
     PYTHON_VARIANTS: tuple[str, ...] = ("cpython", "jacpython");

def _repo_root -> str {
    return os.path.dirname(jaclang_pkg_root());
}

def _has_archives(path: str) -> bool {
    return os.path.isdir(path) and any(n.endswith(".a") for n in os.listdir(path));
}

def _zig_blocker -> str {
    import shutil;
    return "" if shutil.which("zig") else "zig is not on PATH";
}

def _zig_build(step: str) {
    import subprocess;
    subprocess.run(["zig", "build", step], cwd=_repo_root(), check=True);
}

def _floor_tier(
    sealed: bool, rel: str, source: Source, check: Callable[[str], bool]
) -> Probe {
    floor_dir = runtime_floor_root(sealed);
    if not floor_dir {
        return Probe.missing("this process runs on no kit");
    }
    path = os.path.join(floor_dir, rel);
    return Probe.hit(source, path, {}) if check(path) else Probe.missing();
}

def _running_python_variant -> str {
    parts = os.path.realpath(sys.prefix).split(os.sep);
    for (i, part) in enumerate(parts) {
        if part == ".python-build" and i + 1 < len(parts) {
            return parts[i + 1];
        }
    }
    return "";
}

obj CFloorArtifact(Artifact) {
    has name: str = "c-floor",
        kind: ArtifactKind = ArtifactKind.ACCELERATOR,
        release: ReleasePolicy = ReleasePolicy.REQUIRED,
        summary: str = "the C floor archives (static OpenSSL, SQLite, zlib, ...)",
        floor: str = "dynamic linking against the system libraries";

    def target -> str {
        return self.variant or osarch();
    }

    override def probe_sealed -> (Probe | None) {
        if sealed._jaclang_image() is None {
            return None;
        }
        return _floor_tier(True, self.target(), Source.SEALED, _has_archives);
    }

    override def probe_checkout -> Probe {
        running = _running_python_variant();
        order = [running]
            + [
                v
                for v in PYTHON_VARIANTS
                if v != running
            ]
            if running
            else list(PYTHON_VARIANTS);
        for variant in order {
            libdir = os.path.join(
                _repo_root(),
                ".python-build",
                variant,
                self.target(),
                "python",
                "build",
                "lib"
            );
            if _has_archives(libdir) {
                return Probe.hit(Source.CHECKOUT, libdir, {"python": variant});
            }
        }
        return Probe.missing();
    }

    override def probe_kit -> Probe {
        return _floor_tier(False, self.target(), Source.KIT, _has_archives);
    }

    override def checkout_path -> str {
        return os.path.join(_repo_root(), ".python-build");
    }

    override def build_blocker -> str {
        if self.target() != osarch() {
            return (
                f"`zig build build-python` builds the C floor only for this host ({osarch()}); "
                f"build it on a {self.target()} host or use a kit that carries it"
            );
        }
        return _zig_blocker();
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        log("  zig build build-python (the source-built Python and its C floor)");
        _zig_build("build-python");
    }
}

obj MuslArtifact(Artifact) {
    has name: str = "musl",
        kind: ArtifactKind = ArtifactKind.CAPABILITY,
        release: ReleasePolicy = ReleasePolicy.REQUIRED,
        summary: str = "the static musl runtime (statically linked native binaries)",
        hosts: list[str] = ["linux"];

    def target -> str {
        return self.variant or osarch();
    }

    override def probe_sealed -> (Probe | None) {
        if sealed._jaclang_image() is None {
            return None;
        }
        return _floor_tier(
            True, os.path.join(self.target(), "musl"), Source.SEALED, _has_libc
        );
    }

    override def probe_checkout -> Probe {
        libdir = self.checkout_path();
        return Probe.hit(Source.CHECKOUT, libdir, {})
            if _has_libc(libdir)
            else Probe.missing();
    }

    override def probe_kit -> Probe {
        return _floor_tier(
            False, os.path.join(self.target(), "musl"), Source.KIT, _has_libc
        );
    }

    override def checkout_path -> str {
        return os.path.join(_repo_root(), ".pbs-build", self.target(), "musl", "lib");
    }

    override def build_blocker -> str {
        return _zig_blocker();
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        log(f"  zig build vendor-musl-{self.target()}");
        _zig_build(f"vendor-musl-{self.target()}");
    }
}

def _has_libc(path: str) -> bool {
    return os.path.isfile(os.path.join(path, "libc.a"));
}

def wasm_rt_src_dir -> str {
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "wasm_rt");
}

def wasm_floor_drift(libc_dir: str) -> (list[str] | None) {
    manifest = os.path.join(libc_dir, WASM_FLOOR_MANIFEST);
    try {
        with open(manifest, "r", encoding="utf-8") as fh {
            rows = fh.read().splitlines();
        }
    } except OSError {
        return None;
    }
    src_root = wasm_rt_src_dir();
    drifted: list[str] = [];
    for row in rows {
        line = row.strip();
        if not line or " " not in line {
            continue;
        }
        (want, rel) = line.split(" ", 1);
        try {
            with open(os.path.join(src_root, rel.strip()), "rb") as src {
                got = hashlib.sha256(src.read()).hexdigest();
            }
        } except OSError {
            drifted.append(rel.strip());
            continue;
        }
        if got != want {
            drifted.append(rel.strip());
        }
    }
    return drifted;
}

def _has_bitcode(path: str) -> bool {
    return os.path.isdir(path) and any(n.endswith(".bc") for n in os.listdir(path));
}

def _wasm_probe(path: str, source: Source) -> Probe {
    if not _has_bitcode(path) {
        return Probe.missing();
    }
    drift = wasm_floor_drift(path);
    if drift is None {
        return Probe.stale(["it carries no source manifest to check against wasm_rt/"]);
    }
    if drift {
        return Probe.stale([f"wasm_rt/{rel} changed" for rel in drift]);
    }
    return Probe.hit(source, path, {});
}

obj WasmLibcArtifact(Artifact) {
    has name: str = "wasm-libc",
        kind: ArtifactKind = ArtifactKind.CAPABILITY,
        release: ReleasePolicy = ReleasePolicy.REQUIRED,
        summary: str = "the wasm32 libc bitcode (the wasm host-contract floor)";

    override def probe_sealed -> (Probe | None) {
        if sealed._jaclang_image() is None {
            return None;
        }
        return _floor_tier(
            True, os.path.join("wasm32", "libc"), Source.SEALED, _has_bitcode
        );
    }

    override def probe_checkout -> Probe {
        return _wasm_probe(self.checkout_path(), Source.CHECKOUT);
    }

    override def probe_kit -> Probe {
        floor_dir = runtime_floor_root(False);
        if not floor_dir {
            return Probe.missing("this process runs on no kit");
        }
        return _wasm_probe(os.path.join(floor_dir, "wasm32", "libc"), Source.KIT);
    }

    override def checkout_path -> str {
        return os.path.join(_repo_root(), ".pbs-build", "wasm32", "libc");
    }

    override def build_blocker -> str {
        return _zig_blocker();
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        log("  zig build vendor-wasm-libc");
        _zig_build("vendor-wasm-libc");
    }
}

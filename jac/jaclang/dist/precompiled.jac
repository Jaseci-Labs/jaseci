import os;
import sys;

def _pkg_dir -> str {
    return jaclang_pkg_root();
}

def bundle_root(pkg_dir: str) -> str {
    return os.path.join(pkg_dir, "_precompiled");
}

def _python_tag -> str {
    return f"cpython-{sys.version_info.major}{sys.version_info.minor}";
}

def bundle_misses(pkg_dir: str) -> list[str] {
    units = os.path.join(bundle_root(pkg_dir), _python_tag());
    misses: list[str] = [];
    for source in sealable_sources(pkg_dir) {
        if not jir_cacheable_source_path(source) {
            continue;
        }
        rel = os.path.relpath(source, pkg_dir).replace(os.sep, "/");
        unit = os.path.join(units, os.path.splitext(rel)[0] + ".jir");
        try {
            with open(unit, "rb") as f {
                data = f.read();
            }
        } except OSError {
            misses.append(rel);
            continue;
        }
        if not precompiled_jir_matches_source(data, source, package_root=pkg_dir) {
            misses.append(rel);
        }
    }
    return misses;
}

obj PrecompiledArtifact(Artifact) {
    has name: str = "precompiled",
        kind: ArtifactKind = ArtifactKind.ACCELERATOR,
        release: ReleasePolicy = ReleasePolicy.REQUIRED,
        summary: str = "the precompiled compiler bundle (JIR)",
        floor: str = "compiling the compiler from source";

    override def probe_sealed -> (Probe | None) {
        image = sealed._jaclang_image();
        if image is None {
            return None;
        }
        return Probe.hit(Source.SEALED, bundle_root(str(image.pkg_dir)), {});
    }

    override def probe_checkout -> Probe {
        pkg = _pkg_dir();
        if not os.path.isdir(os.path.join(bundle_root(pkg), _python_tag())) {
            return Probe.missing();
        }
        misses = bundle_misses(pkg);
        if misses {
            return Probe.stale(
                [f"jaclang/{rel} has no reusable unit" for rel in misses]
            );
        }
        return Probe.hit(Source.CHECKOUT, bundle_root(pkg), {});
    }

    override def probe_kit -> Probe {
        return Probe.missing(
            "a kit's bundle belongs to its own compiler, not this checkout"
        );
    }

    override def checkout_path -> str {
        return bundle_root(_pkg_dir());
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        log(f"  precompiling {_pkg_dir()}");
        run_precompile(os.path.dirname(_pkg_dir()));
    }
}

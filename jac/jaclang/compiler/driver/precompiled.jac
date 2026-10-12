import os;
import sys;
import from jaclang.artifacts.model {
    Artifact,
    ArtifactKind,
    Probe,
    ReleasePolicy,
    Source
}

def _pkg_dir -> str {
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    return jaclang_pkg_root();
}

def bundle_root(pkg_dir: str) -> str {
    return os.path.join(pkg_dir, "_precompiled");
}

def _python_tag -> str {
    return f"cpython-{sys.version_info.major}{sys.version_info.minor}";
}

def bundle_misses(pkg_dir: str) -> list[str] {
    import from jaclang.compiler.driver.jir {
        compiler_source_files,
        jir_cacheable_source_path,
        precompiled_jir_matches_source
    }
    units = os.path.join(bundle_root(pkg_dir), _python_tag());
    misses: list[str] = [];
    for rel in compiler_source_files(pkg_dir) {
        source = os.path.join(pkg_dir, rel.replace("/", os.sep));
        if not jir_cacheable_source_path(source) {
            continue;
        }
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
        import from jaclang.jac0core { sealed }
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
        import from jaclang.dist.precompile_bytecode { run_precompile }
        log(f"  precompiling {_pkg_dir()}");
        run_precompile(os.path.dirname(_pkg_dir()));
    }
}

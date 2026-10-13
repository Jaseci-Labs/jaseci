import hashlib;
import json;
import os;
import sys;
import from jaclang.compiler.driver.compile_options {
    CompileOptions,
    NATIVE_LINK_MODE_BITCODE,
    NATIVE_LINK_MODE_OBJECTS
}
import type from jaclang.compiler.kernel_target { KernelTarget }
import type from jaclang.compiler.driver.program { JacProgram }
import type from jaclang.compiler.backends.native.link_plan { LinkPlan, LinkResult }
import from jaclang.artifacts.model {
    Artifact,
    ArtifactKind,
    Probe,
    ReleasePolicy,
    Source
}

glob NOT_BUILT: str = "not built",
     LAYOUT_SIDECAR_SUFFIX: str = ".layout.json",
     KERNEL_DEV_LINK_MODE: str = NATIVE_LINK_MODE_OBJECTS,
     SEALED_LINK_MODE: str = NATIVE_LINK_MODE_BITCODE;

obj ResolvedKernel {
    has lib_path: str,
        layout: dict[str, any],
        source: str,
        plan_digest: str = "";
}

class KernelUnavailable(RuntimeError) {}

def kernel_lib_name -> str {
    if sys.platform == "darwin" {
        return "libjac_compiler.dylib";
    }
    if sys.platform.startswith("win") {
        return "jac_compiler.dll";
    }
    return "libjac_compiler.so";
}

def source_tree_kernel_path -> str {
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    return os.path.join(jaclang_pkg_root(), "compiler", kernel_lib_name());
}

def read_sidecar(lib_path: str) -> (dict[str, any] | None) {
    data: any = None;
    try {
        with open(lib_path + LAYOUT_SIDECAR_SUFFIX, "r", encoding="utf-8") as f {
            data = json.load(f);
        }
    } except Exception {
        return None;
    }
    if not isinstance(data, dict) or not isinstance(data.get("classes"), dict) {
        return None;
    }
    return data;
}

def sealed_link_refusal(record: dict[str, any], sidecar: dict[str, any]) -> str {
    mode = str(record.get("mode", SEALED_LINK_MODE));
    linked = str(sidecar.get("link_mode", SEALED_LINK_MODE));
    if linked != mode {
        return f"the manifest records a {mode} link but the sidecar a {linked} link";
    }
    if mode == SEALED_LINK_MODE {
        return "";
    }
    return f"a sealed image carries a {SEALED_LINK_MODE} link, not a {mode} link";
}

def _from_sealed_image -> (ResolvedKernel | None) {
    import from jaclang.jac0core { sealed }
    image = sealed._jaclang_image();
    if image is None {
        return None;
    }
    record = image.native_artifact();
    if record is None {
        raise KernelUnavailable(
            "sealed jaclang image carries no native compiler kernel; the image "
            "is immutable, so rebuild the payload"
        );
    }
    lib_path = str(image.pkg_dir / record["path"]);
    sidecar = read_sidecar(lib_path);
    if not os.path.isfile(lib_path) or sidecar is None {
        raise KernelUnavailable(
            f"sealed jaclang image names kernel {lib_path} but it or its "
            f"{LAYOUT_SIDECAR_SUFFIX} sidecar is missing"
        );
    }
    if _sha256_file(lib_path) != record.get("sha256") {
        raise KernelUnavailable(
            f"sealed kernel {lib_path} does not match its manifest sha256"
        );
    }
    refusal = sealed_link_refusal(record, sidecar);
    if refusal {
        raise KernelUnavailable(f"sealed kernel {lib_path}: {refusal}");
    }
    if str(sidecar.get("plan_digest", "")) != str(record.get("plan_digest", "")) {
        raise KernelUnavailable(
            f"sealed kernel {lib_path}: sidecar plan digest disagrees with the manifest"
        );
    }
    return ResolvedKernel(
        lib_path=lib_path,
        layout=sidecar["classes"],
        source="sealed",
        plan_digest=str(record.get("plan_digest", ""))
    );
}

def kernel_options -> CompileOptions {
    return CompileOptions(
        aot_mode=True,
        native_require=[],
        native_link_mode=KERNEL_DEV_LINK_MODE,
        na_debug=False,
        default_codespace="native",
        native_unit=True,
        kernel_build=True,
        skip_native_engine=True,
        native_target="",
        na_gc_mode="cycles",
        memory_profile="managed",
        nogc_enforce_all=False,
        memory_enforce=[],
        memory_exempt=[],
        native_threads=4,
        rc_debug_codegen=False,
        native_debug=False,
        opt_level=2,
        dump_ir_path="",
        debug_ir=False,
        rc_stats=False,
        nogc_debug=False
    );
}

def kernel_plan(
    prog: (JacProgram | None) = None,
    mode: str = "",
    target: (KernelTarget | None) = None
) -> LinkPlan {
    import from jaclang.compiler.driver.program { JacProgram }
    import from jaclang.compiler.native_scope { kernel_root_path }
    import from jaclang.compiler.backends.native.link_plan { build_link_plan }
    program = prog if prog is not None else JacProgram();
    options = kernel_options();
    root_path = target.root_module_path() if target is not None else kernel_root_path();
    return build_link_plan(program, [root_path], options, mode=mode, native_unit=True);
}

def _sha256_file(path: str) -> str {
    h = hashlib.sha256();
    with open(path, "rb") as f {
        while True {
            chunk = f.read(1 << 20);
            if not chunk {
                break;
            }
            h.update(chunk);
        }
    }
    return h.hexdigest();
}

def _unit_label(path: str) -> str {
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    try {
        return os.path.relpath(path, os.path.dirname(jaclang_pkg_root()));
    } except ValueError {
        return path;
    }
}

def unit_drift(
    sidecar: dict[str, any], recorded: dict[str, any], units: list[str]
) -> list[str] {
    import from jaclang.compiler.driver.jir {
        native_producer_digest,
        running_compiler_digest,
        unit_source_digest
    }
    import from jaclang.compiler.frontend.codeinfo { native_unit_identity }
    options = kernel_options();
    drift: list[str] = [];
    if str(sidecar.get("compiler_digest", ""))
        not in (
            running_compiler_digest(),
            native_producer_digest(options.kernel_build)
        ) {
        drift.append("the compiler's native ABI changed");
    }
    if str(sidecar.get("codegen_identity", "")) != options.base_codegen_identity() {
        drift.append("native code generation changed");
    }
    triple = options.effective_triple();
    if str(sidecar.get("triple", "")) != triple {
        drift.append(
            f"built for {sidecar.get('triple') or 'another target'}, not {triple}"
        );
    }
    python = f"{sys.version_info.major}.{sys.version_info.minor}";
    if str(sidecar.get("python", "")) != python {
        drift.append(f"built for Python {sidecar.get('python') or '?'}, not {python}");
    }
    ids = sidecar.get("unit_ids");
    idents = (
        [str(i) for i in ids]
            if isinstance(ids, list) and len(ids) == len(units)
            else [native_unit_identity(u) for u in units]
    );
    if len(recorded) != len(idents) {
        drift.append("the kernel's unit set changed");
        return drift;
    }
    policy = sidecar.get("unit_policy");
    recorded_policy: dict[str, any] = policy if isinstance(policy, dict) else {};
    for (ident, path) in zip(idents, units) {
        if recorded.get(ident) != unit_source_digest(path) {
            drift.append(f"{_unit_label(path)} changed");
        } elif int(recorded_policy.get(ident, 0))
            != int(options.native_required_for(path)) {
            drift.append(f"{_unit_label(path)} changed native placement");
        }
    }
    return drift;
}

def _inspect(
    lib_path: str, expected_sha: str = ""
) -> tuple[(dict[str, any] | None), list[str]] {
    sidecar = read_sidecar(lib_path);
    if sidecar is None or not os.path.isfile(lib_path) {
        return (None, [NOT_BUILT]);
    }
    try {
        actual = _sha256_file(lib_path);
    } except OSError as e {
        return (None, [f"the kernel is unreadable ({e})"]);
    }
    if actual != (expected_sha or sidecar.get("artifact_sha256")) {
        return (None, ["the kernel does not match the hash its record carries"]);
    }
    import from jaclang.compiler.driver.jir { sidecar_unit_paths }
    units = sidecar_unit_paths(sidecar);
    recorded = sidecar.get("unit_sources");
    if not units or not isinstance(recorded, dict) or not recorded {
        return (None, ["the kernel's record names no unit sources"]);
    }
    drift = unit_drift(sidecar, recorded, units);
    return ((None if drift else sidecar), drift);
}


def _bundled_kernel -> tuple[str, dict[str, any]] | None {
    import from jaclang.artifacts.kit { kit_image }
    found = kit_image();
    if found is None {
        return None;
    }
    (site_pkg, image) = found;
    record = image.native_artifact();
    if not record {
        return None;
    }
    return (os.path.join(site_pkg, str(record.get("path", ""))), dict(record));
}

def _probe(lib_path: str, source: Source, expected_sha: str = "") -> Probe {
    (sidecar, drift) = _inspect(lib_path, expected_sha=expected_sha);
    if sidecar is not None {
        return Probe.hit(source, lib_path, sidecar);
    }
    return Probe.missing() if drift == [NOT_BUILT] else Probe.stale(drift);
}

obj KernelArtifact(Artifact) {
    has name: str = "kernel",
        kind: ArtifactKind = ArtifactKind.ACCELERATOR,
        release: ReleasePolicy = ReleasePolicy.REQUIRED,
        summary: str = "the native compiler kernel",
        floor: str = "the bytecode compiler",
        requires: list[str] = ["llvm-shim", "stubcat"],
        consumes: list[str] = ["stubcat"];

    override def unavailable_reason -> str {
        try {
            import from jaclang.compiler.driver.toolchain { native_pipeline_available }
            (ok, why) = native_pipeline_available();
        } except Exception as e {
            return f"the native toolchain is unavailable ({e})";
        }
        return "" if ok else (why or "the native toolchain is unavailable");
    }

    override def probe_sealed -> (Probe | None) {
        sealed = _from_sealed_image();
        if sealed is None {
            return None;
        }
        record = dict(read_sidecar(sealed.lib_path) or {});
        record["plan_digest"] = sealed.plan_digest;
        return Probe.hit(Source.SEALED, sealed.lib_path, record);
    }

    override def probe_checkout -> Probe {
        return _probe(source_tree_kernel_path(), Source.CHECKOUT);
    }

    override def probe_kit -> Probe {
        found = _bundled_kernel();
        if found is None {
            return Probe.missing("this process runs on no kit that carries one");
        }
        (lib_path, record) = found;
        return _probe(lib_path, Source.KIT, expected_sha=str(record.get("sha256", "")));
    }

    override def checkout_path -> str {
        return source_tree_kernel_path();
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        if exact {
            import from jaclang.compiler.driver.jir { require_exact_compiler_products }
            require_exact_compiler_products();
        }
        build_kernel(source_tree_kernel_path(), log=log);
    }
}

def _catalog_active(program: JacProgram) -> bool {
    import from jaclang.compiler.frontend.host { active_host }
    host = active_host();
    host.compiler_for(program).ensure_stub_catalog();
    return host.has_active_stub_catalog();
}

def catalog_blocker(program: JacProgram) -> str {
    if _catalog_active(program) {
        return "";
    }
    import from jaclang.artifacts.model { Resolution }
    import from jaclang.artifacts.router { _announce, artifact_named, resolve }
    why = "it reads typeshed only through the stub catalog, which is unavailable ("
        + (resolve("stubcat").reason or "not built")
        + ")";
    _announce(artifact_named("kernel"), Resolution(name="kernel", reason=why));
    return why;
}

def resolve_kernel -> (ResolvedKernel | None) {
    import from jaclang.artifacts.router { resolve }
    found = resolve("kernel").found;
    if found is None {
        return None;
    }
    return ResolvedKernel(
        lib_path=found.path,
        layout=found.record["classes"],
        source=found.source.value,
        plan_digest=str(found.record.get("plan_digest", ""))
    );
}

def build_kernel(
    dst: str = "",
    log: (Callable[[str], None] | None) = None,
    link_mode: str = KERNEL_DEV_LINK_MODE
) -> LinkResult {
    import from jaclang.artifacts.router { publish }
    import from jaclang.compiler.backends.native.kernel_stage0 { link_kernel }
    destination = dst or source_tree_kernel_path();
    tmp = f"{destination}.{os.getpid()}.tmp";
    try {
        result = link_kernel(tmp, log=log, link_mode=link_mode);
        publish(tmp, destination, companions=(LAYOUT_SIDECAR_SUFFIX, ));
        result.output_path = destination;
    } finally {
        for leftover in (tmp, tmp + LAYOUT_SIDECAR_SUFFIX, tmp + ".target.json") {
            try {
                os.remove(leftover);
            } except OSError {}
        }
    }
    return result;
}

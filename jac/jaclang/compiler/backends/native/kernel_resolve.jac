import from jaclang.jac0core.cache_paths { atomic_write }
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

glob STUBCAT_BUILDING_ENV: str = "JAC_STUBCAT_BUILDING",
     LAYOUT_SIDECAR_SUFFIX: str = ".layout.json",
     KERNEL_DEV_LINK_MODE: str = NATIVE_LINK_MODE_OBJECTS,
     SEALED_LINK_MODE: str = NATIVE_LINK_MODE_BITCODE,
     PR_KIT_KERNEL_ENV: str = "JAC_PR_KIT_KERNEL",
     PR_KIT_KERNEL_OMITTED: str = "none",
     PR_KIT_EVENT: str = "pull_request";

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

def seal_omits_kernel -> bool {
    requested = os.environ.get(PR_KIT_KERNEL_ENV, "").strip().lower();
    if not requested {
        return False;
    }
    if requested != PR_KIT_KERNEL_OMITTED {
        raise ValueError(
            f"{PR_KIT_KERNEL_ENV}={requested!r}: expected {PR_KIT_KERNEL_OMITTED} "
            "or nothing"
        );
    }
    event = os.environ.get("GITHUB_EVENT_NAME", "");
    if os.environ.get("GITHUB_ACTIONS") != "true" or event != PR_KIT_EVENT {
        raise RuntimeError(
            f"{PR_KIT_KERNEL_ENV}={PR_KIT_KERNEL_OMITTED} is honored only in a "
            f"{PR_KIT_EVENT} CI build (this is {event or 'not a CI build'}); a "
            "shipped image carries its kernel"
        );
    }
    return True;
}

def omitted_kernel_record -> dict[str, any] {
    return {"units": {}, "kernel": PR_KIT_KERNEL_OMITTED, "kit": PR_KIT_EVENT};
}

def kit_omits_kernel(native: any) -> bool {
    return isinstance(native, dict)
        and native.get("kernel") == PR_KIT_KERNEL_OMITTED
        and native.get("kit") == PR_KIT_EVENT
        and not native.get("artifact");
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

def _sealed_kit_omits_kernel -> bool {
    import from jaclang.jac0core { sealed }
    image = sealed._jaclang_image();
    return image is not None and kit_omits_kernel(image.native);
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
        return (None, ["no kernel has been built"]);
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

def _resolved(lib_path: str, sidecar: dict[str, any], source: str) -> ResolvedKernel {
    return ResolvedKernel(
        lib_path=lib_path,
        layout=sidecar["classes"],
        source=source,
        plan_digest=str(sidecar.get("plan_digest", ""))
    );
}

def tree_kernel -> tuple[(ResolvedKernel | None), list[str]] {
    lib_path = source_tree_kernel_path();
    (sidecar, drift) = _inspect(lib_path);
    if sidecar is None {
        return (None, drift);
    }
    return (_resolved(lib_path, sidecar, "tree"), []);
}

def _bundled_image -> (tuple[str, any] | None) {
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    site_pkg = os.path.join(os.path.dirname(sys.prefix), "site", "jaclang");
    if not os.path.isdir(os.path.join(site_pkg, "_precompiled")) {
        return None;
    }
    if os.path.realpath(site_pkg) == os.path.realpath(jaclang_pkg_root()) {
        return None;
    }
    try {
        import from jaclang.jac0core.sealed { load_image }
        image = load_image(os.path.join(site_pkg, "_precompiled"));
    } except Exception {
        return None;
    }
    return (site_pkg, image) if image is not None else None;
}

def _bundled_kit_omits_kernel -> bool {
    found = _bundled_image();
    return found is not None and kit_omits_kernel(found[1].native);
}

def kit_kernel -> tuple[(ResolvedKernel | None), list[str]] {
    found = _bundled_image();
    if found is None {
        return (None, ["this process runs on no kit"]);
    }
    (site_pkg, image) = found;
    record = image.native_artifact();
    if not record {
        return (None, ["the kit carries no kernel"]);
    }
    lib_path = os.path.join(site_pkg, str(record.get("path", "")));
    (sidecar, drift) = _inspect(lib_path, expected_sha=str(record.get("sha256", "")));
    if sidecar is None {
        return (None, drift);
    }
    return (_resolved(lib_path, sidecar, "kit"), []);
}

def _from_source_tree -> tuple[(ResolvedKernel | None), str] {
    (ok, why) = (False, "");
    try {
        import from jaclang.compiler.driver.toolchain { native_pipeline_available }
        (ok, why) = native_pipeline_available();
    } except Exception as e {
        why = f"the native toolchain is unavailable ({e})";
    }
    if not ok {
        return (None, why or "the native toolchain is unavailable");
    }
    (tree, drift) = tree_kernel();
    if tree is not None {
        return (tree, "");
    }
    if _bundled_kit_omits_kernel() {
        return (None, "");
    }
    (kit, _) = kit_kernel();
    if kit is not None {
        return (kit, "");
    }
    summary = drift[0];
    if len(drift) > 1 {
        summary += f" (and {len(drift) - 1} more)";
    }
    if summary != "no kernel has been built" {
        summary = f"the kernel is stale: {summary}";
    } else {
        summary = "no kernel has been built in this checkout";
    }
    return (None, summary);
}

glob _NOTICE: dict[str, bool] = {"shown": False};

def _announce_bytecode(reason: str) {
    if _NOTICE["shown"] {
        return;
    }
    _NOTICE["shown"] = True;
    (on, off) = ("\033[1;33m", "\033[0m") if sys.stderr.isatty() else ("", "");
    sys.stderr.write(
        f"{on}jac: the compiler is running from bytecode (slower): {reason}.{off}\n"
        f"{on}jac: run `jac kernel build` to build the native compiler kernel; "
        f"`jac kernel status` shows what it is missing.{off}\n"
    );
    sys.stderr.flush();
}

def resolve_kernel -> (ResolvedKernel | None) {
    if os.environ.get(STUBCAT_BUILDING_ENV) {
        return None;
    }
    if _sealed_kit_omits_kernel() {
        return None;
    }
    sealed = _from_sealed_image();
    if sealed is not None {
        return sealed;
    }
    (found, reason) = _from_source_tree();
    if found is None and reason {
        _announce_bytecode(reason);
    }
    return found;
}

def _publish_kernel(source: str, destination: str) {
    import from pathlib { Path }
    atomic_write(destination, Path(source).read_bytes(), mode=0o755);
    atomic_write(
        destination + LAYOUT_SIDECAR_SUFFIX,
        Path(source + LAYOUT_SIDECAR_SUFFIX).read_bytes(),
        mode=0o644
    );
}

def build_kernel(
    dst: str = "",
    log: (Callable[[str], None] | None) = None,
    link_mode: str = KERNEL_DEV_LINK_MODE
) -> LinkResult {
    import from jaclang.compiler.backends.native.kernel_stage0 { link_kernel }
    destination = dst or source_tree_kernel_path();
    tmp = f"{destination}.{os.getpid()}.tmp";
    try {
        result = link_kernel(tmp, log=log, link_mode=link_mode);
        _publish_kernel(tmp, destination);
    } finally {
        for leftover in (tmp, tmp + LAYOUT_SIDECAR_SUFFIX, tmp + ".target.json") {
            try {
                os.remove(leftover);
            } except OSError {}
        }
    }
    return result;
}

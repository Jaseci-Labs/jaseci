import sys;

glob ARTIFACTS: dict = {
         "llvm-shim": "jaclang.compiler.backends.native.llvm.shim_path:ShimArtifact",
         "c-floor": "jaclang.compiler.backends.native.floors:CFloorArtifact",
         "musl": "jaclang.compiler.backends.native.floors:MuslArtifact",
         "wasm-libc": "jaclang.compiler.backends.native.floors:WasmLibcArtifact",
         "typeshed": "jaclang.compiler.types.stubcat.locate:TypeshedArtifact",
         "stubcat": "jaclang.compiler.types.stubcat.locate:StubcatArtifact",
         "precompiled": "jaclang.dist.precompiled:PrecompiledArtifact",
         "kernel": "jaclang.compiler.backends.native.kernel_resolve:KernelArtifact",
         "llvm-cbe": "jaclang.toolchains.c_backend:CBackendArtifact",
         "bun": "jaclang.client.js_runtime:BunArtifact",
         "js-engine": "jaclang.client.js_runtime:JsEngineArtifact",
         "jacpython": "jaclang.dist.interpreter:JacPythonArtifact"
     },
     ROUTER_MODULES: tuple = (
         "jaclang.artifacts.model",
         "jaclang.artifacts.router",
         "jaclang.artifacts.kit"
     );

def _marks -> set {
    import from jaclang.jac0core.handoff { handoff }
    marked = handoff().get("building");
    if isinstance(marked, list) {
        return {str(name) for name in marked};
    }
    return set();
}

def _record(marked: set) {
    import from jaclang.jac0core.handoff { update_handoff }
    update_handoff(building=sorted(marked) or None);
}

def building -> frozenset {
    return frozenset(_marks());
}

def begin(names: list) -> list {
    marked = _marks();
    added = [
        name
        for name in names
        if name not in marked
    ];
    _record(marked | set(added));
    return added;
}

def end(names: list) {
    _record(_marks() - set(names));
}

def resolution_in_flight -> bool {
    names = set(ROUTER_MODULES);
    for target in ARTIFACTS.values() {
        names.add(target.split(":", 1)[0]);
    }
    for name in names {
        module = sys.modules.get(name);
        spec = module?.__spec__ if module is not None else None;
        if spec is not None and getattr(spec, "_initializing", False) {
            return True;
        }
    }
    return False;
}

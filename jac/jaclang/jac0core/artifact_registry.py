"""Every artifact the router knows, and which of them this process builds
(pure Python, boot-safe).

The kernel is resolved inside the compiler's own import chain, so this
module never imports an artifact: entries name ``module:Class`` and the
router loads them on first use. A process that builds an artifact runs that
artifact's floor, and so does every artifact that consumes it; a build
script marks its artifacts with ``begin`` before importing the compiler; the
marks travel in the handoff record (``jaclang.jac0core.handoff``), so the build's own
child processes run the floor too.
"""

from __future__ import annotations

import sys

ARTIFACTS: dict[str, str] = {
    "llvm-shim": "jaclang.compiler.backends.native.llvm.shim_path:ShimArtifact",
    "c-floor": "jaclang.compiler.backends.native.floors:CFloorArtifact",
    "musl": "jaclang.compiler.backends.native.floors:MuslArtifact",
    "wasm-libc": "jaclang.compiler.backends.native.floors:WasmLibcArtifact",
    "typeshed": "jaclang.compiler.types.stubcat.locate:TypeshedArtifact",
    "stubcat": "jaclang.compiler.types.stubcat.locate:StubcatArtifact",
    "precompiled": "jaclang.compiler.driver.precompiled:PrecompiledArtifact",
    "kernel": "jaclang.compiler.backends.native.kernel_resolve:KernelArtifact",
    "llvm-cbe": "jaclang.toolchains.c_backend:CBackendArtifact",
    "bun": "jaclang.client.js_runtime:BunArtifact",
    "js-engine": "jaclang.client.js_runtime:JsEngineArtifact",
    "jacpython": "jaclang.dist.interpreter:JacPythonArtifact",
}

ROUTER_MODULES: tuple[str, ...] = (
    "jaclang.artifacts.model",
    "jaclang.artifacts.router",
    "jaclang.artifacts.kit",
)

def _marks() -> set[str]:
    from jaclang.jac0core.handoff import handoff

    marked = handoff().get("building")
    return {str(name) for name in marked} if isinstance(marked, list) else set()


def _record(marked: set[str]) -> None:
    from jaclang.jac0core.handoff import update_handoff

    update_handoff(building=sorted(marked) or None)


def building() -> frozenset[str]:
    """The artifacts this process, or the build that spawned it, is building."""
    return frozenset(_marks())


def begin(names: list[str] | tuple[str, ...]) -> list[str]:
    marked = _marks()
    added = [name for name in names if name not in marked]
    _record(marked | set(added))
    return added


def end(names: list[str] | tuple[str, ...]) -> None:
    _record(_marks() - set(names))


def resolution_in_flight() -> bool:
    """True while a module the router needs is still executing its import: a
    compile nested in that import must run on the floor rather than re-enter
    a half-initialized module."""
    names = set(ROUTER_MODULES)
    names.update(target.split(":", 1)[0] for target in ARTIFACTS.values())
    for name in names:
        module = sys.modules.get(name)
        spec = getattr(module, "__spec__", None) if module is not None else None
        if spec is not None and getattr(spec, "_initializing", False):
            return True
    return False

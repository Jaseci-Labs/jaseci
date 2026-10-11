"""Every artifact the router knows, and which of them this process builds
(pure Python, boot-safe).

The kernel is resolved inside the compiler's own import chain, so this
module never imports an artifact: entries name ``module:Class`` and the
router loads them on first use. A process that builds an artifact runs that
artifact's floor, and so does every artifact that consumes it; a build
script marks its artifacts with ``begin`` before importing the compiler.
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
    "kernel": "jaclang.compiler.backends.native.kernel_resolve:KernelArtifact",
    "llvm-cbe": "jaclang.toolchains.c_backend:CBackendArtifact",
}

ROUTER_MODULES: tuple[str, ...] = (
    "jaclang.artifacts.model",
    "jaclang.artifacts.router",
    "jaclang.artifacts.kit",
)

_BUILDING: set[str] = set()


def building() -> frozenset[str]:
    return frozenset(_BUILDING)


def begin(names: list[str] | tuple[str, ...]) -> list[str]:
    added = [name for name in names if name not in _BUILDING]
    _BUILDING.update(added)
    return added


def end(names: list[str] | tuple[str, ...]) -> None:
    for name in names:
        _BUILDING.discard(name)


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

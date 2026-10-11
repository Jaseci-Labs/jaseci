import os;
import sys;
import type from jaclang.jac0core.sealed { SealedImage }

glob _KIT: list[tuple[str, (SealedImage | None)]] = [];

def kit_image -> (tuple[str, SealedImage] | None) {
    if not _KIT {
        _KIT.append(_find_kit());
    }
    (site_pkg, image) = _KIT[0];
    return (site_pkg, image) if image is not None else None;
}

def kit_path(rel: str) -> str {
    found = kit_image();
    return os.path.join(found[0], rel) if found is not None else "";
}

def _find_kit -> tuple[str, (SealedImage | None)] {
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    site_pkg = os.path.join(os.path.dirname(sys.prefix), "site", "jaclang");
    if not os.path.isdir(os.path.join(site_pkg, "_precompiled")) {
        return ("", None);
    }
    if os.path.realpath(site_pkg) == os.path.realpath(jaclang_pkg_root()) {
        return ("", None);
    }
    try {
        import from jaclang.jac0core.sealed { load_image }
        return (site_pkg, load_image(os.path.join(site_pkg, "_precompiled")));
    } except Exception {
        return ("", None);
    }
}

def runtime_floor_root(sealed: bool) -> str {
    """The `python/floor` directory of the runtime this process runs on: the
    sealed image's own for a sealed process, the kit's for a rerouted
    checkout. Empty when there is neither.""";
    site_pkg = "";
    if sealed {
        import from jaclang.jac0core { sealed as sealed_mod }
        image = sealed_mod._jaclang_image();
        site_pkg = str(image.pkg_dir) if image is not None else "";
    } else {
        found = kit_image();
        site_pkg = found[0] if found is not None else "";
    }
    if not site_pkg {
        return "";
    }
    return os.path.join(os.path.dirname(os.path.dirname(site_pkg)), "python", "floor");
}

def osarch(triple: str = "") -> str {
    """`<os>-<arch>` as the build trees and floors name a platform
    (linux-x86_64, macos-aarch64), for a target triple or this host.""";
    import platform;
    text = (triple or f"{sys.platform}-{platform.machine()}").lower();
    arch = "aarch64" if ("aarch64" in text or "arm64" in text) else "x86_64";
    if "wasm" in text {
        return "wasm32";
    }
    if "darwin" in text or "apple" in text or "macos" in text {
        return f"macos-{arch}";
    }
    if "win" in text {
        return f"windows-{arch}";
    }
    return f"linux-{arch}";
}

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

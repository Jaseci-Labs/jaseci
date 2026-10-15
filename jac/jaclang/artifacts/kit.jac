import os;
import sys;

glob _KIT: list[tuple[str, (SealedImage | None)]] = [],
     PR_KIT_EVENT: str = "pull_request",
     PR_KIT_LABEL_PREFIX: str = "native:";

def kit_image -> (tuple[str, SealedImage] | None) {
    if not _KIT {
        _KIT.append(_find_kit());
    }
    (site_pkg, image) = _KIT[0];
    return (site_pkg, image) if image is not None else None;
}

def pr_kit_omits(name: str) -> bool {
    if os.environ.get("GITHUB_ACTIONS") != "true"
        or os.environ.get("GITHUB_EVENT_NAME") != PR_KIT_EVENT {
        return False;
    }
    return PR_KIT_LABEL_PREFIX + name not in _pr_labels();
}

def _pr_labels -> set[str] {
    import json;
    try {
        with open(os.environ.get("GITHUB_EVENT_PATH", ""), encoding="utf-8") as f {
            event: any = json.load(f);
        }
    } except (OSError, ValueError) {
        return set();
    }
    pull = event.get("pull_request") if isinstance(event, dict) else None;
    labels = pull.get("labels") if isinstance(pull, dict) else None;
    return {
        str(label.get("name", ""))
        for label in (labels if isinstance(labels, list) else [])
        if isinstance(label, dict)
    };
}

def kit_path(rel: str) -> str {
    found = kit_image();
    return os.path.join(found[0], rel) if found is not None else "";
}

def _find_kit -> tuple[str, (SealedImage | None)] {
    import jaclang;
    site_pkg = os.path.join(os.path.dirname(sys.prefix), "site", "jaclang");
    if not os.path.isdir(os.path.join(site_pkg, "_precompiled")) {
        return ("", None);
    }
    if os.path.realpath(site_pkg)
        == os.path.realpath(os.path.dirname(str(jaclang.__file__))) {
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

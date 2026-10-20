impl TargetSpec.kernel_file_name -> str {
    return f"{self.shared_prefix}jac_compiler{self.shared_suffix}";
}

impl triple_osarch(triple: str) -> str {
    text = triple.lower();
    arch = "aarch64" if ("aarch64" in text or "arm64" in text) else "x86_64";
    if "darwin" in text or "apple" in text or "macos" in text {
        return f"macos-{arch}";
    }
    if "windows" in text or "win32" in text or "msvc" in text or "mingw" in text {
        return f"windows-{arch}";
    }
    return f"linux-{arch}";
}

impl target_spec(name: str) -> TargetSpec {
    wanted = name
        if name in [spec.osarch for spec in RELEASE_TARGETS]
        else triple_osarch(name);
    for spec in RELEASE_TARGETS {
        if spec.osarch == wanted {
            return spec;
        }
    }
    known = ", ".join(spec.osarch for spec in RELEASE_TARGETS);
    raise UnknownTarget(f"no release target named {name!r} (known: {known})");
}

impl host_target_spec -> TargetSpec {
    import platform;
    return target_spec(triple_osarch(f"{sys.platform}-{platform.machine()}"));
}

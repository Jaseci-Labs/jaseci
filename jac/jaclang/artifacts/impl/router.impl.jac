impl names -> list[str] {
    import from jaclang.jac0core.artifact_registry { ARTIFACTS }
    return list(ARTIFACTS);
}

impl artifact_named(name: str) -> Artifact {
    found = _ENTRIES.get(name);
    if found is not None {
        return found;
    }
    import importlib;
    import from jaclang.jac0core.artifact_registry { ARTIFACTS }
    (base, _, variant) = name.partition("@");
    target = ARTIFACTS.get(base);
    if target is None {
        raise KeyError(f"no artifact named {base!r}; known: {', '.join(ARTIFACTS)}");
    }
    (module_name, attr) = target.split(":", 1);
    made = getattr(importlib.import_module(module_name), attr)();
    if variant {
        made.variant = variant;
        made.name = name;
    }
    _ENTRIES[name] = made;
    return made;
}

impl resolve(name: str) -> Resolution {
    known = _RESOLVED.get(name);
    if known is not None {
        return known;
    }
    import from jaclang.jac0core.artifact_registry { resolution_in_flight }
    if resolution_in_flight() {
        return Resolution(name=name, reason="still loading", quiet=True, deferred=True);
    }
    resolution = _decide(artifact_named(name));
    _RESOLVED[name] = resolution;
    if resolution.on_floor() and not resolution.quiet {
        _announce(artifact_named(name), resolution);
    }
    return resolution;
}

impl require(name: str) -> Resolution {
    resolution = resolve(name);
    artifact = artifact_named(name);
    if resolution.on_floor()
        and artifact.provision
        and not resolution.deferred
        and artifact.host_supported() {
        resolution = _provision(artifact, resolution);
    }
    if resolution.on_floor() {
        raise ArtifactUnavailable(
            f"{artifact.summary} is unavailable: {resolution.reason or 'not built'}. "
            f"Run `jac native build {name}`."
        );
    }
    return resolution;
}

impl forget(name: str = "") -> None {
    if name {
        _RESOLVED.pop(name, None);
        _ANNOUNCED.discard(name);
        return;
    }
    _RESOLVED.clear();
    _ANNOUNCED.clear();
}

impl building_now -> frozenset[str] {
    import from jaclang.jac0core.artifact_registry { building as marked }
    return marked();
}

impl building(names: list[str]) -> _BuildingSpan {
    return _BuildingSpan(added=list(names));
}

impl _BuildingSpan.__enter__ -> _BuildingSpan {
    import from jaclang.jac0core.artifact_registry { begin }
    self.added = begin(self.added);
    forget();
    return self;
}

impl _BuildingSpan.__exit__(
    _exc_type: object, _exc_value: object, _traceback: object
) -> bool {
    import from jaclang.jac0core.artifact_registry { end }
    end(self.added);
    forget();
    return False;
}

impl build_order(requested: list[str]) -> list[str] {
    ordered: list[str] = [];
    visiting: set[str] = set();

    def place(name: str) {
        if name in ordered {
            return;
        }
        if name in visiting {
            raise ValueError(f"artifact dependency cycle through {name}");
        }
        visiting.add(name);
        for dep in artifact_named(name).requires {
            place(dep);
        }
        visiting.discard(name);
        ordered.append(name);
    }

    for name in requested {
        place(name);
    }
    return ordered;
}

impl publish(stage: str, destination: str, companions: tuple[str, ...] = ()) -> None {
    import from pathlib { Path }
    import from jaclang.jac0core.cache_paths { FileLock, atomic_write }
    payloads = [(destination, Path(stage).read_bytes(), 0o755)];
    for suffix in companions {
        payloads.append(
            (destination + suffix, Path(stage + suffix).read_bytes(), 0o644)
        );
    }
    with FileLock(destination + ".lock") {
        for (path, data, mode) in payloads {
            atomic_write(path, data, mode=mode);
        }
    }
}

impl tiers(name: str) -> list[tuple[str, Probe]] {
    artifact = artifact_named(name);
    found: list[tuple[str, Probe]] = [];
    sealed = artifact.probe_sealed();
    if sealed is not None {
        return [(Source.SEALED.value, sealed)];
    }
    found.append((Source.CHECKOUT.value, artifact.probe_checkout()));
    found.append((Source.KIT.value, artifact.probe_kit()));
    return found;
}

impl release_set -> list[str] {
    return [
        n
        for n in names()
        if artifact_named(n).release == ReleasePolicy.REQUIRED
    ];
}

impl shipped_floors -> list[str] {
    return [
        n
        for n in names()
        if artifact_named(n).release == ReleasePolicy.FLOOR
    ];
}

impl build(
    requested: list[str],
    log: Callable[[str], None],
    force: bool = False,
    exact: bool = False,
    strict: bool = False
) -> list[str] {
    import subprocess;
    built: list[str] = [];
    for name in build_order(requested) {
        artifact = artifact_named(name);
        if not artifact.host_supported() {
            message = f"{name}: cannot be built on this host";
            if strict {
                raise ArtifactUnavailable(message);
            }
            log(f"skipped {message}");
            continue;
        }
        why = artifact.unavailable_reason() or artifact.build_blocker();
        if why {
            if strict {
                raise ArtifactUnavailable(f"{name}: {why}");
            }
            log(f"skipped {name}: {why}");
            continue;
        }
        if not (force and name in requested) and artifact.built().found is not None {
            log(f"{name}: current");
            continue;
        }
        log(f"building {name}");
        try {
            with building([name]) {
                artifact.build(log, force, exact);
            }
        } except subprocess.CalledProcessError as e {
            command = " ".join(str(part) for part in e.cmd)
                if isinstance(e.cmd, (list, tuple))
                else str(e.cmd);
            raise ArtifactUnavailable(
                f"{name}: `{command}` failed (exit status {e.returncode}); see its output above"
            ) from None;
        }
        forget(name);
        after = artifact.built();
        if after.found is None {
            raise ArtifactUnavailable(
                f"{name} was built but does not match its inputs: "
                    + "; ".join(after.drift[:5])
            );
        }
        built.append(name);
    }
    return built;
}

impl unmet(required: list[str]) -> list[str] {
    problems: list[str] = [];
    for name in required {
        artifact = artifact_named(name);
        if not artifact.host_supported() {
            continue;
        }
        if artifact.release == ReleasePolicy.FLOOR {
            if not artifact.floor_present() {
                problems.append(
                    f"{name}: its shipped floor ({artifact.floor}) is missing"
                );
            }
            continue;
        }
        resolution = resolve(name);
        if resolution.on_floor() {
            problems.append(f"{name}: {resolution.reason or 'not built'}");
        }
    }
    return problems;
}

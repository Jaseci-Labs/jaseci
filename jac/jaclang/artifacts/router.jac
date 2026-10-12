import from jaclang.artifacts.model {
    Artifact,
    ArtifactKind,
    ArtifactUnavailable,
    Probe,
    ReleasePolicy,
    Resolution,
    Source
}

glob _ENTRIES: dict[str, Artifact] = {},
     _RESOLVED: dict[str, Resolution] = {},
     _ANNOUNCED: set[str] = set();

def names -> list[str];
def artifact_named(name: str) -> Artifact;
def resolve(name: str) -> Resolution;
def require(name: str) -> Resolution;
def forget(name: str = "") -> None;
def building_now -> frozenset[str];
def building(names: list[str]) -> _BuildingSpan;
def build_order(requested: list[str]) -> list[str];
def publish(stage: str, destination: str, companions: tuple[str, ...] = ()) -> None;
def tiers(name: str) -> list[tuple[str, Probe]];
def release_set -> list[str];
def shipped_floors -> list[str];
def build(
    requested: list[str],
    log: Callable[[str], None],
    force: bool = False,
    exact: bool = False,
    strict: bool = False
) -> list[str];

def unmet(required: list[str]) -> list[str];

obj _BuildingSpan {
    has added: list[str];

    def __enter__ -> _BuildingSpan;
    def __exit__(_exc_type: object, _exc_value: object, _traceback: object) -> bool;
}

def _decide(artifact: Artifact) -> Resolution {
    if artifact.disabled() {
        return Resolution(name=artifact.name, reason="being built", quiet=True);
    }
    sealed = artifact.probe_sealed();
    if sealed is not None {
        if sealed.found is not None {
            return Resolution(name=artifact.name, found=sealed.found);
        }
        return Resolution(
            name=artifact.name,
            reason="this image ships its floor",
            quiet=sealed.omitted
        );
    }
    why = artifact.unavailable_reason();
    if why {
        return Resolution(name=artifact.name, reason=why);
    }
    tree = artifact.probe_checkout();
    if tree.found is not None {
        return Resolution(name=artifact.name, found=tree.found);
    }
    kit = artifact.probe_kit();
    if kit.found is not None {
        return Resolution(name=artifact.name, found=kit.found);
    }
    if kit.omitted {
        return Resolution(
            name=artifact.name, reason="the kit ships its floor", quiet=True
        );
    }
    return Resolution(name=artifact.name, reason=tree.describe());
}

def _announce(artifact: Artifact, resolution: Resolution) {
    if artifact.name in _ANNOUNCED
        or artifact.kind != ArtifactKind.ACCELERATOR
        or artifact.release == ReleasePolicy.FLOOR {
        return;
    }
    _ANNOUNCED.add(artifact.name);
    import sys;
    (on, off) = ("\033[1;33m", "\033[0m") if sys.stderr.isatty() else ("", "");
    sys.stderr.write(
        f"{on}jac: {artifact.name} runs on its floor ({artifact.floor}, slower): "
        f"{resolution.reason}. Run `jac native build {artifact.name}`; "
        f"`jac native status {artifact.name}` shows what moved.{off}\n"
    );
    sys.stderr.flush();
}

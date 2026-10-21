impl collect_client_graph(
    roots: list[Path],
    artifact_of: Callable[[Path], ClientArtifact],
    variant_of: Callable[[Path], Path],
    virtual_modules: set[str],
    visited: set[Path]
) -> ClientGraph {
    result = ClientGraph();
    pending: list[Path] = list(reversed(roots));
    artifacts: dict[Path, ClientArtifact] = {};
    walked: set[Path] = set();
    refreshed: set[Path] = set();

    def require(path: Path) -> ClientArtifact {
        found = artifacts.get(path);
        if found is None {
            found = artifact_of(path);
            artifacts[path] = found;
        }
        return found;
    }

    def check_runtime_imports(path: Path, artifact: ClientArtifact) -> None {
        for (dependency, names) in artifact.manifest.runtime_imports.items() {
            if not names {
                continue;
            }
            target: Path = variant_of(Path(dependency).resolve());
            provider_artifact = require(target);
            provider = provider_artifact.manifest;
            missing = sorted(set(names) - set(provider.exports + provider.globals));
            if missing {
                raise ClientBundleError(
                    f"{path}: runtime import(s) {', '.join(missing)} are not exported "
                    f"by {target}. Only exposed declarations (`:protect` or `:pub`) "
                    "and client-placed values cross into the bundle; annotation-only "
                    "references must not produce runtime imports."
                );
            }
            if target in visited and target not in walked and target not in refreshed {
                refreshed.add(target);
                result.refreshed.append(ClientUnit(target, provider_artifact));
                check_runtime_imports(target, provider_artifact);
            }
        }
    }

    while pending {
        path = variant_of(pending.pop().resolve());
        if path in visited {
            continue;
        }
        visited.add(path);
        walked.add(path);
        if path.suffix != '.jac' {
            if path.is_file() {
                result.assets.append(path);
            }
            continue;
        }
        artifact = require(path);
        result.modules.append(ClientUnit(path, artifact));
        check_runtime_imports(path, artifact);
        imports = [
            Path(str(import_path))
            for (name, import_path) in artifact.manifest.imports.items()
            if name not in virtual_modules
        ];
        pending.extend(reversed(imports));
    }
    return result;
}

import from collections.abc { Callable }
import from pathlib { Path }

obj ClientUnit {
    has path: Path,
        artifact: ClientArtifact;
}

obj ClientGraph {
    has modules: list[ClientUnit] = [],
        assets: list[Path] = [];
}

def collect_client_graph(
    roots: list[Path],
    artifact_of: Callable[[Path], ClientArtifact],
    variant_of: Callable[[Path], Path],
    virtual_modules: set[str],
    visited: set[Path]
) -> ClientGraph;

import platform;
import from pathlib { Path }
import from uuid { UUID }

def collect_node_connections(
    current_node: NodeArchetype, visited_nodes: set, connections: set, edge_ids: set
) -> None;

def traverse_graph(
    nd: NodeArchetype,
    cur_depth: int,
    depth: int,
    edge_type: list[str],
    traverse: bool,
    connections: list[tuple[NodeArchetype, NodeArchetype, EdgeArchetype]],
    node_depths: dict[(NodeArchetype, int)],
    visited_nodes: list[NodeArchetype],
    queue: list[tuple[NodeArchetype, int]],
    bfs: bool,
    dfs: Callable,
    node_limit: int,
    edge_limit: int
) -> None;

def storage_key(id: UUID) -> str;

def to_uuid(id: (UUID | str)) -> UUID;


def release_arch(raw: str) -> str;


def host_arch -> str;


def host_os -> str;


def triple_arch(triple: str) -> str;

def get_name(target_path: (str | None) = None) -> (str | None);

def get_db_path(base_path: str, target_path: (str | None) = None) -> (str | None);

impl storage_key(id: UUID) -> str {
    return f"anchor:{str(id)}";
}

impl to_uuid(id: (UUID | str)) -> UUID {
    if isinstance(id, UUID) {
        return id;
    }
    return UUID(str(id));
}


impl release_arch(raw: str) -> str {
    m = raw.strip().lower();
    if m in ("arm64", "aarch64") {
        return "aarch64";
    }
    if m in ("amd64", "x86_64") {
        return "x86_64";
    }
    return m;
}


impl host_arch -> str {
    return release_arch(platform.machine());
}


impl host_os -> str {
    sysname = platform.system().strip().lower();
    if sysname == "darwin" {
        return "macos";
    }
    return sysname;
}


impl triple_arch(triple: str) -> str {
    if "aarch64" in triple.lower() or "arm64" in triple.lower() {
        return "aarch64";
    }
    return "x86_64";
}

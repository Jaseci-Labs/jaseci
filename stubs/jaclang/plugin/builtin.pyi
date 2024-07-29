from jaclang.runtimelib.constructs import NodeArchitype as NodeArchitype

def dotgen(
    node: NodeArchitype | None = None,
    depth: int | None = None,
    traverse: bool | None = None,
    edge_type: list[str] | None = None,
    bfs: bool | None = None,
    edge_limit: int | None = None,
    node_limit: int | None = None,
    dot_file: str | None = None,
) -> str: ...

"""Jac's Key Elemental Abstractions"""

import:py from datetime, datetime;
import:py from uuid, UUID, uuid4;
import:py from jaclang.jac.constant, EdgeDir;
import:py from jaclang.jac.plugin, Architype, AbsRootHook, hookimpl;

include:jac corelib_impl;


enum AccessMode;

obj Memory {
    has index: dict[UUID, Element] = {},
        save_queue: list[Element] = [];

    #* Main Accessors *#
    can get_obj(caller_id: UUID, item_id: UUID,
                override: bool = False) -> Element;
    can has_obj(item_id: UUID) -> bool;
    can save_obj(caller_id: UUID, item: Element);
    can del_obj(caller_id: UUID, item: Element);

    #* Utility Functions *#
    can get_object_distribution -> dict;
    can get_mem_size -> float;
}

obj ExecutionContext {
    has master: Master = :>uuid4,
        memory: Memory = Memory();

    can reset;
    can get_root() -> Node;
}

"Global Execution Context, should be monkey patched by the user."
glob exec_ctx = ExecutionContext();

obj ElementInterface {
    has jid: UUID = :>uuid4,
        timestamp: datetime = :>datetime.now,
        persist: bool = False,
        access_mode: AccessMode = AccessMode.PRIVATE,
        rw_access: set = :>set,
        ro_access: set = :>set,
        owner_id: UUID = exec_ctx.master,
        mem: Memory = exec_ctx.memory;

    can make_public_ro;
    can make_public_rw;
    can make_private;
    can is_public_ro -> bool;
    can is_public_rw -> bool;
    can is_private -> bool;
    can is_readable(caller_id: UUID) -> bool;
    can is_writable(caller_id: UUID) -> bool;
    can give_access(caller_id: UUID, read_write: bool = False);
    can revoke_access(caller_id: UUID);
}

obj ObjectInterface:ElementInterface: {}

obj DataSpatialInterface:ObjectInterface: {
    static has ds_entry_funcs: list[dict]=[],
               ds_exit_funcs: list[dict]=[];

    static can on_entry(cls: type, triggers: list[type]);
    static can on_exit(cls: type, triggers: list[type]);
}

obj NodeInterface:DataSpatialInterface: {
    has edges: dict[EdgeDir, list[Edge]]
        = {EdgeDir.IN: [], EdgeDir.OUT: []};

    can connect_node(nd: Node, edg: Edge) -> Node;
    can edges_to_nodes(dir: EdgeDir) -> list[Node];
    can __call__(walk: Walker);
}

obj EdgeInterface:DataSpatialInterface: {
    has source: Node = None,
        target: Node = None,
        dir: EdgeDir = None;

    can apply_dir(dir: EdgeDir) -> Edge;
    can attach(src: Node, trg: Node) -> Edge;
    can __call__(walk: Walker);
}

obj WalkerInterface:DataSpatialInterface: {
    has path: list[Node] = [],
        next: list[Node] = [],
        ignores: list[Node] = [],
        disengaged: bool = False;

    can visit_node(nds: list[Node]|list[Edge]|Node|Edge);
    can ignore_node(nds: list[Node]|list[Edge]|Node|Edge);
    can disengage_now;
    can __call__(nd: Node);
}
obj Root:AbsRootHook: {
    has _jac_: NodeInterface;
    has RootType: type;
}

obj Master {
    has _jac_: ElementInterface = ElementInterface();
    has root_node: Root = Root(NodeInterface(), Root);
}

obj JacPlugin {
    static can bind_architype(arch: AT, arch_type: str) -> bool;
    static can get_root() -> Architype;
}
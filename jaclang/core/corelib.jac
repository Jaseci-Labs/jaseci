"""Jac's Key Elemental Abstractions"""

import:py from datetime, datetime;
import:py from uuid, UUID, uuid4;
import:py from jaclang.jac.constant, EdgeDir;

include:jac memory_impl;
include:jac exec_ctx_impl;
include:jac element_impl;
include:jac arch_impl;


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

obj DataSpatialInterface {
    static has ds_entry_funcs: list[dict]=[],
               ds_exit_funcs: list[dict]=[];

    static can on_entry(cls: type, triggers: list[type]);
    static can on_exit(cls: type, triggers: list[type]);
}

obj ObjectInterface:ElementInterface: {}

obj NodeInterface:ObjectInterface: {
    has edges: dict[EdgeDir, list[Edge]]
        = {EdgeDir.IN: [], EdgeDir.OUT: []};

    can connect_node(nd: Node, edg: Edge) -> Node;
    can edges_to_nodes(dir: EdgeDir) -> list[Node];
}

obj EdgeInterface:ObjectInterface: {
    has source: Node = None,
        target: Node = None,
        dir: EdgeDir = None;

    can apply_dir(dir: EdgeDir) -> Edge;
    can attach(src: Node, trg: Node) -> Edge;
}

obj WalkerInterface:ObjectInterface: {
    has path: list[Node] = [],
        next: list[Node] = [],
        ignores: list[Node] = [],
        disengaged: bool = False;

    can visit_node(nds: list[Node]|list[Edge]|Node|Edge);
    can ignore_node(nds: list[Node]|list[Edge]|Node|Edge);
    can disengage_now;
}

obj Element {
    has _jac_: ElementInterface = ElementInterface();
}

obj Object:Element: {
    has _jac_: ObjectInterface = ObjectInterface();
    static has _jac_ds_: DataSpatialInterface = DataSpatialInterface();
}

obj Node:Object: {
    has _jac_: NodeInterface = NodeInterface();
    can __call__(walk: Walker);
}

obj Edge:Object: {
    has _jac_: EdgeInterface = EdgeInterface();
    can __call__(walk: Walker);
}

obj Walker:Object: {
    has _jac_: WalkerInterface = WalkerInterface();
    can __call__(nd: Node);
}

obj Master:Element: { has root_node: Node = Node(); }

can make_architype(base_class: type) -> type;
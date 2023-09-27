"""Jac's Key Elemental Abstractions"""

import:py from datetime, datetime;
import:py from uuid, UUID, uuid4;
import:py from jaclang.jac.constant, EdgeDir;

include:jac impl.memory_impl;
include:jac impl.exec_ctx_impl;
include:jac impl.element_impl;
include:jac impl.arch_impl;


enum AccessMode;

object Memory {
    has index: dict[UUID, Element], save_queue: list[Element];

    #* Main Accessors *#
    can get_obj(caller_id: UUID, item_id: UUID,
                override: bool = False) -> Element?;
    can has_obj(item_id: UUID) -> bool;
    can save_obj(caller_id: UUID, item: Element);
    can del_obj(caller_id: UUID, item: Element);

    #* Utility Functions *#
    can get_object_distribution -> dict;
    can get_mem_size -> float;
}

object ExecutionContext {
    has master: Master = :>uuid4,
        memory: Memory = Memory();

    can reset;
    can get_root() -> Node;
}

"Global Execution Context, should be monkey patched by the user."
global exec_ctx = ExecutionContext();

object ElementInterface {
    has jid: UUID = :>uuid4,
        py_obj: any = None,
        timestamp: datetime = :>datetime.now,
        persist: bool = False,
        access_mode: AccessMode = AccessMode.PRIVATE,
        rw_access: set = :>set,
        ro_access: set = :>set,
        owner_id: UUID = exec_ctx.master,
        mem: Memory = exec_ctx.memory;

    can <init>(py_obj: any);
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

object ObjectInterface:ElementInterface {
    static has ds_entry_funcs: list[dict]=[],
               ds_exit_funcs: list[dict]=[];

    static can on_entry(cls: type, triggers: list[type]);
    static can on_exit(cls: type, triggers: list[type]);
}

object NodeInterface:ObjectInterface {
    has edges_: dict[EdgeDir, list[Edge]]
        = {EdgeDir.IN: [], EdgeDir.OUT: []};

    can connect_node_(nd: Node, edg: Edge) -> Node;
    can edges_to_nodes_(dir: EdgeDir) -> list[Node];
}

object EdgeInterface:ObjectInterface {
    has source_: Node?,
        target_: Node?,
        dir_: EdgeDir?;

    can apply_dir_(dir: EdgeDir) -> Edge;
    can attach_(src: Node, trg: Node) -> Edge;
}

object WalkerInterface:ObjectInterface {
    has path_: list[Node] = [],
        next_: list[Node] = [],
        ignores_: list[Node] = [],
        disengaged_: bool = False;

    can visit_(nds: list[Node]|list[Edge]|Node|Edge);
    can ignore_(nds: list[Node]|list[Edge]|Node|Edge);
    can disengage_;
}

object Element {
    has _jac_: ElementInterface = ElementInterface();
    can <init>(_jac_pyobj: any);
}

object Object:Element {
    has _jac_: ObjectInterface = ObjectInterface();
}

object Node:Object {
    has _jac_: NodeInterface = NodeInterface();
    can __call__(walk: Walker);
}

object Edge:Object {
    has _jac_: EdgeInterface = EdgeInterface();
    can __call__(walk: Walker);
}

object Walker:Object {
    has _jac_: WalkerInterface = WalkerInterface();
    can __call__(nd: Node);
}

object Master:Element { has root_node: Node = Node(); }

can make_architype(base_class: type) -> type;
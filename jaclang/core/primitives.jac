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
    has master: Master,
        memory: Memory;

    can <init>(master: UUID, memory: Memory);
    can get_root() -> Node;
}

global exec_ctx = ExecutionContext(:>uuid4, Memory());

object ElementMetaData {
    has jid: UUID = :>uuid4,
        timestamp: datetime = :>datetime.now,
        persist: bool = False,
        access_mode: AccessMode = AccessMode.PRIVATE,
        rw_access: set = :>set,
        ro_access: set = :>set,
        owner_id: UUID = exec_ctx.master,
        mem: Memory = exec_ctx.memory;
}

object Element {
    has _jinfo: ElementMetaData = ElementMetaData();

    can _jac_make_public_ro;
    can _jac_make_public_rw;
    can _jac_make_private;
    can _jac_is_public_ro -> bool;
    can _jac_is_public_rw -> bool;
    can _jac_is_private -> bool;
    can _jac_is_readable(caller_id: UUID) -> bool;
    can _jac_is_writable(caller_id: UUID) -> bool;
    can _jac_give_access(caller_id: UUID, read_write: bool = False);
    can _jac_revoke_access(caller_id: UUID);
}

object Object:Element {
    static has _jac_ds_entry_funcs: list[dict]=[],
               _jac_ds_exit_funcs: list[dict]=[];

    static can _jac_on_entry(cls: type, triggers: list[type]);
    static can _jac_on_exit(cls: type, triggers: list[type]);
}

object Node:Object {
    has _jac_edges_: dict[EdgeDir, list[Edge]]
        = {EdgeDir.IN: [], EdgeDir.OUT: []};

    can __call__(walk: Walker);
    can _jac_connect_node_(nd: Node, edg: Edge) -> Node;
    can _jac_edges_to_nodes_(dir: EdgeDir) -> list[Node];
}

object Edge:Object {
    has _jac_source_: Node?,
        _jac_target_: Node?,
        _jac_dir_: EdgeDir?;

    can __call__(walk: Walker);
    can _jac_apply_dir_(dir: EdgeDir) -> Edge;
    can _jac_attach_(src: Node, trg: Node) -> Edge;
}

object Walker:Object {
    has _jac_path_: list[Node] = [],
        _jac_next_: list[Node] = [];

    can __call__(nd: Node);
    can _jac_visit_(nds: list[Node]|list[Edge]);
    can _jac_disengage_;
}

object Master:Element {
    has root_node: Node = Node();
}

can make_architype(base_class: type) -> type {
    can class_decorator(cls: type) -> type {
        # Check if cls is a subclass of base_class
        if not issubclass(cls, base_class) {
            # If it's not, create a new class with the same name that inherits from both cls and base_class
            cls = type(cls.__name__, (base_class, cls), {});
        }
        return cls;
    }
    return class_decorator;
}
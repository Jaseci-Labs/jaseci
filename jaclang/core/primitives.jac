"""Jac's Key Elemental Abstractions"""

import:py from datetime, datetime;
import:py from uuid, UUID, uuid4;

include:jac impl.memory_impl;
include:jac impl.exec_ctx_impl;
include:jac impl.element_impl;
include:jac impl.node_impl;


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

    can init(master: UUID, memory: Memory);
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
    static
    has _jac_ds_entry_funcs: list[dict]=[],
        _jac_ds_exit_funcs: list[dict]=[];

    static
    can _jac_on_enter(cls: type, triggers: list[type]);

    static
    can _jac_on_exit(cls: type, triggers: list[type]);
}

object Node:Object {
    has _jac_edges: list[Edge];

    can __call__(walk: Walker);
}

object Edge:Object {
    has _jac_source: Node, _jac_target: Node;
}

object Walker:Object {
    has _jac_path: list[Node],
        _jac_next: list[Node];

    can __call__(nd: Node);
}

object Master:Element {
    has root_node: Node = Node();
}
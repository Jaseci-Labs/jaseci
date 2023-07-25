"""Jac's Key Elemental Abstractions"""

import:py from datetime, datetime;
import:py from uuid, UUID, uuid4;

include:jac impl.memory_impl;
include:jac impl.exec_ctx_impl;
include:jac impl.element_impl;


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
    has __jinfo: ElementMetaData = ElementMetaData();

    can __jac_make_public_ro;
    can __jac_make_public_rw;
    can __jac_make_private;
    can __jac_is_public_ro -> bool;
    can __jac_is_public_rw -> bool;
    can __jac_is_private -> bool;
    can __jac_is_readable(caller_id: UUID) -> bool;
    can __jac_is_writable(caller_id: UUID) -> bool;
    can __jac_give_access(caller_id: UUID, read_write: bool = False);
    can __jac_revoke_access(caller_id: UUID);
}

object Object:Element {}

object Node:Object {
    has __j_edges: list[Edge];
}

object Edge:Object {
    has __j_source: Node, __j_target: Node;
}

object Walker:Object {
    has __j_path: list[Node],
        __j_next: Node?;
}

object Master:Element {
    has root_node: Node = Node();
}
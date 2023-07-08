"""Jac's Key Elemental Abstractions"""

import:py from datetime, datetime;
import:py from uuid, UUID, uuid4;

include:jac impl.memory_impl;
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

object ElementMetaData {
    has jid: UUID = uuid4(),
        timestamp: datetime = datetime.now(),
        persist: bool = False,
        access_mode: AccessMode = AccessMode.PRIVATE,
        rw_access: set = |> set,
        ro_access: set = |> set,
        owner_id: UUID,
        mem: Memory;
}

object Element {
    has __jinfo: ElementMetaData;

    can init(owner_id: UUID, memory: Memory, jid: UUID, persist: bool = False);
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

object Ability:Element {}

object Master:Element {}


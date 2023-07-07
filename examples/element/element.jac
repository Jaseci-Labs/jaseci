"""Jac's Key Elemental Abstractions"""

import:py from datetime, datetime;
import:py from uuid, UUID, uuid4;

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
    has jinfo: ElementMetaData;

    can init(owner_id: UUID, memory: Memory, jid: UUID, persist: bool = False);
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

"""Implementation for Jac's Element Abstractions"""

:enum:AccessMode {
    READ_ONLY,
    READ_WRITE,
    PRIVATE
}

:object:Memory:ability:get_obj
(caller_id: UUID, item_id: UUID, override: bool = False) -> Element? {
    ret = item_id |> <here>.index.get;
    if override or (ret is not None and caller_id |> ret.__is_readable) {
        return ret;
    }
}

:object:Memory:ability:has_obj
(item_id: UUID) -> bool {
    return item_id in <here>.index;
}

:object:Memory:ability:save_obj
(caller_id: UUID, item: Element) {
    if caller_id |> item.is_writable {
        <here>.index[item.id] = item;
        if item._persist {
            item |> <here>.save_obj_list.add;
        }
    }
    self.mem[item.id] = item;
    if item._persist {
        item |> self.save_obj_list.add;
    }

}

:object:Memory:ability:del_obj
(caller_id: UUID, item: Element);

:object:Memory:ability:get_object_distribution -> dict {
}

:object:Memory:ability:get_mem_size -> float {
}

:object:Element:ability:init
(owner_id: UUID, memory: Memory, jid: UUID, persist: bool = False) {
}

:object:Element:ability:__jac_make_public_ro {
}
:object:Element:ability:__jac_make_public_rw {
}
:object:Element:ability:__jac_make_private {
}
:object:Element:ability:__jac_is_public_ro -> bool {
}
:object:Element:ability:__jac_is_public_rw -> bool {
}
:object:Element:ability:__jac_is_private -> bool {
}

:object:Element:ability:__jac_is_readable
(caller_id: UUID) -> bool{
}

:object:Element:ability:__jac_is_writable
(caller_id: UUID) -> bool {
}
:object:Element:ability:__jac_give_access
(caller_id: UUID, read_write: bool = False) {
}

:object:Element:ability:__jac_revoke_access
(caller_id: UUID) {

}

:object:Element:ability:__jac_get_access_mode -> AccessMode {
}
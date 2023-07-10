"""Implementation for Jac's Element Abstractions"""

:enum:AccessMode {
    READ_ONLY,
    READ_WRITE,
    PRIVATE
}

:object:Element:ability:init
(owner_id: UUID, memory: Memory, jid: UUID, persist: bool = False) {
    <self>.__jinfo.owner_id = owner_id;
    <self>.__jinfo.memory = memory;
    <self>.__jinfo._persist = persist;
}

:object:Element:ability:__jac_make_public_ro {
    <self>.__jinfo.access_mode = AccessMode.READ_ONLY;
}

:object:Element:ability:__jac_make_public_rw {
    <self>.__jinfo.access_mode = AccessMode.READ_WRITE;
}

:object:Element:ability:__jac_make_private {
    <self>.__jinfo.access_mode = AccessMode.PRIVATE;
}

:object:Element:ability:__jac_is_public_ro -> bool {
    return <self>.__jinfo.access_mode == AccessMode.READ_ONLY;
}

:object:Element:ability:__jac_is_public_rw -> bool {
    return <self>.__jinfo.access_mode == AccessMode.READ_WRITE;
}

:object:Element:ability:__jac_is_private -> bool {
    return <self>.__jinfo.access_mode == AccessMode.PRIVATE;
}

:object:Element:ability:__jac_is_readable
(caller_id: UUID) -> bool{
    return (
            caller_id == <self>.owner_id
            or |> <self>.is_public_read
            or caller_id in <self>.ro_access
            or caller_id in <self>.rw_access
        );
}

:object:Element:ability:__jac_is_writable
(caller_id: UUID) -> bool {
    return (
            caller_id == <self>.owner_id
            or |> <self>.is_public_write
            or caller_id in <self>.rw_access
        );
}

:object:Element:ability:__jac_give_access
(caller_id: UUID, read_write: bool = False) {
    if read_write {
        caller_id |> <self>.rw_access.add;
    }
    else {
        caller_id |> add .> ro_access .> <self>;
    }
}

:object:Element:ability:__jac_revoke_access
(caller_id: UUID) {
    caller_id |> <self>.ro_access.discard;
    caller_id |> <self>.rw_access.discard;
}
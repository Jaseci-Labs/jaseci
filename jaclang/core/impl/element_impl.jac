"""Implementation for Jac's Element Abstractions"""

:enum:AccessMode {
    READ_ONLY,
    READ_WRITE,
    PRIVATE
}

:object:Element:ability:<init>
(_jac_exec_ctx: ExecutionContext) {
    <self>.__jinfo = _jac_exec_ctx :> ExecutionContext;
}

:object:Element:ability:_jac_make_public_ro {
    <self>.__jinfo.access_mode = AccessMode.READ_ONLY;
}

:object:Element:ability:_jac_make_public_rw {
    <self>.__jinfo.access_mode = AccessMode.READ_WRITE;
}

:object:Element:ability:_jac_make_private {
    <self>.__jinfo.access_mode = AccessMode.PRIVATE;
}

:object:Element:ability:_jac_is_public_ro -> bool {
    return <self>.__jinfo.access_mode == AccessMode.READ_ONLY;
}

:object:Element:ability:_jac_is_public_rw -> bool {
    return <self>.__jinfo.access_mode == AccessMode.READ_WRITE;
}

:object:Element:ability:_jac_is_private -> bool {
    return <self>.__jinfo.access_mode == AccessMode.PRIVATE;
}

:object:Element:ability:_jac_is_readable
(caller_id: UUID) -> bool {
    return (
            caller_id == <self>.owner_id
            or |> <self>.is_public_read
            or caller_id in <self>.ro_access
            or caller_id in <self>.rw_access
        );
}

:object:Element:ability:_jac_is_writable
(caller_id: UUID) -> bool {
    return (
            caller_id == <self>.owner_id
            or |> <self>.is_public_write
            or caller_id in <self>.rw_access
        );
}

:object:Element:ability:_jac_give_access
(caller_id: UUID, read_write: bool = False) {
    if read_write {
        caller_id |> <self>.rw_access.add;
    }
    else {
        caller_id |> add .> ro_access .> <self>;
    }
}

:object:Element:ability:_jac_revoke_access
(caller_id: UUID) {
    caller_id |> <self>.ro_access.discard;
    caller_id |> <self>.rw_access.discard;
}

:object:Object:ability:_jac_on_entry
(cls: type, triggers: list) {
    can decorator(func: callable) -> callable {
        cls._jac_ds_entry_funcs.append({'types': triggers, 'func': func});
        can wrapper(*args: list, **kwargs: dict) -> callable {
            return func(*args, **kwargs);
        }
        return wrapper;
    }
    return decorator;
}

:object:Object:ability:_jac_on_exit
(cls: type, triggers: list) {
    can decorator(func: callable) -> callable {
        cls._jac_ds_exit_funcs.append({'types': triggers, 'func': func});
        can wrapper(*args: list, **kwargs: dict) -> callable {
            return func(*args, **kwargs);
        }
        return wrapper;
    }
    return decorator;
}

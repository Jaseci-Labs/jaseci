"""Implementation for Jac's Element Abstractions"""

:enum:AccessMode {
    READ_ONLY,
    READ_WRITE,
    PRIVATE
}

:obj:ElementInterface:can:make_public_ro {
    <self>.__jinfo.access_mode = AccessMode.READ_ONLY;
}

:obj:ElementInterface:can:make_public_rw {
    <self>.__jinfo.access_mode = AccessMode.READ_WRITE;
}

:obj:ElementInterface:can:make_private {
    <self>.__jinfo.access_mode = AccessMode.PRIVATE;
}

:obj:ElementInterface:can:is_public_ro -> bool {
    return <self>.__jinfo.access_mode == AccessMode.READ_ONLY;
}

:obj:ElementInterface:can:is_public_rw -> bool {
    return <self>.__jinfo.access_mode == AccessMode.READ_WRITE;
}

:obj:ElementInterface:can:is_private -> bool {
    return <self>.__jinfo.access_mode == AccessMode.PRIVATE;
}

:obj:ElementInterface:can:is_readable
(caller_id: UUID) -> bool {
    return (
            caller_id == <self>.owner_id
            or |> <self>.is_public_read
            or caller_id in <self>.ro_access
            or caller_id in <self>.rw_access
        );
}

:obj:ElementInterface:can:is_writable
(caller_id: UUID) -> bool {
    return (
            caller_id == <self>.owner_id
            or |> <self>.is_public_write
            or caller_id in <self>.rw_access
        );
}

:obj:ElementInterface:can:give_access
(caller_id: UUID, read_write: bool = False) {
    if read_write {
        caller_id |> <self>.rw_access.add;
    }
    else {
        caller_id |> add .> ro_access .> <self>;
    }
}

:obj:ElementInterface:can:revoke_access
(caller_id: UUID) {
    caller_id |> <self>.ro_access.discard;
    caller_id |> <self>.rw_access.discard;
}


:obj:DataSpatialInterface:can:on_entry
(cls: type, triggers: list) {
    can decorator(func: callable) -> callable {
        cls.ds_entry_funcs.append({'types': triggers, 'func': func});
        can wrapper(*args: list, **kwargs: dict) -> callable {
            return func(*args, **kwargs);
        }
        return wrapper;
    }
    return decorator;
}

:obj:DataSpatialInterface:can:on_exit
(cls: type, triggers: list) {
    can decorator(func: callable) -> callable {
        cls.ds_exit_funcs.append({'types': triggers, 'func': func});
        can wrapper(*args: list, **kwargs: dict) -> callable {
            return func(*args, **kwargs);
        }
        return wrapper;
    }
    return decorator;
}

:can:make_architype(base_class: type) -> type {
    can class_decorator(cls: type) -> type {
        # Check if cls is a subclass of base_class
        if not issubclass(cls, base_class) {
            # If it's not, create a new class with the same name that inherits from both cls and base_class
            cls = type(cls.__name__, (cls, base_class), {});
            # original_init = cls.__init__;
            # can new_init(self: cls, *args: list, **kwargs: dict) -> None {
            #     base_class.__init__(<self>, *args, **kwargs);
            #     original_init(<self>, *args, **kwargs);
            # }
            # cls.__init__ = new_init;
        }
        return cls;
    }
    return class_decorator;
}
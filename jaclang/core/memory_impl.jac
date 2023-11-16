"""Implementation for Jac's Element Abstractions"""
import:py sys;

:obj:Memory:can:get_obj
(caller_id: UUID, item_id: UUID, override: bool = False) -> Element {
    ret = item_id |> <self>.index.get;
    if override or (ret is not None and caller_id |> ret.__is_readable) {
        return ret;
    }
}

:obj:Memory:can:has_obj
(item_id: UUID) -> bool {
    return item_id in <self>.index;
}

:obj:Memory:can:save_obj
(caller_id: UUID, item: Element) {
    if caller_id |> item.is_writable {
        <self>.index[item.id] = item;
        if item._persist {
            item |> <self>.save_obj_list.add;
        }
    }
    <self>.mem[item.id] = item;
    if item._persist {
        item |> <self>.save_obj_list.add;
    }
}

:obj:Memory:can:del_obj
(caller_id: UUID, item: Element) {
    if caller_id |> item.is_writable {
        <self>.index.pop(item.id);
        if item._persist {
            item |> <self>.save_obj_list.remove;
        }
    }
}

:obj:Memory:can:get_object_distribution -> dict {
    dist = {};
    for i in |> <self>.index.keys {
        t = <self>.index[i] |> type;
        if t in dist {
            dist[t] += 1;
        }
        else {
            dist[t] = 1;
        }
    }
    return dist;
}

:obj:Memory:can:get_mem_size -> float {
    return (<self>.index |> sys.getsizeof) / 1024.0;
}

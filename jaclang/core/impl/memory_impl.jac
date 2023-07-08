"""Implementation for Jac's Element Abstractions"""
import:py sys;

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
    <here>.mem[item.id] = item;
    if item._persist {
        item |> <here>.save_obj_list.add;
    }
}

:object:Memory:ability:del_obj
(caller_id: UUID, item: Element) {
    if caller_id |> item.is_writable {
        <here>.index.pop(item.id);
        if item._persist {
            item |> <here>.save_obj_list.remove;
        }
    }
}

:object:Memory:ability:get_object_distribution -> dict {
    dist = {};
    for i in |> <here>.index.keys {
        t = <here>.index[i] |> type;
        if t in dist {
            dist[t] += 1;
        }
        else {
            dist[t] = 1;
        }
    }
    return dist;
}

:object:Memory:ability:get_mem_size -> float {
    return (<here>.index |> sys.getsizeof) / 1024.0;
}

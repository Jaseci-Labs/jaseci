"""Jac's Key Elemental Abstractions"""

import:py sys;
import:py from uuid, UUID, uuid4;
import:py from jaclang.jac.constant, EdgeDir;
import:py from jaclang.jac.plugin, hookimpl;

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

:obj:ExecutionContext:c:get_root
() {
    if <self>.master :> type == UUID {
        <self>.master = Master();
    }
    return <self>.master.root_node;
}

:obj:ExecutionContext:c:reset {
    <self>.<init>();
}

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

:obj:NodeInterface:can:connect_node
(nd: Node, edg: Edge) -> Node {
    (<self>.py_obj, nd) :> edg.attach;
    return <self>;
}

:obj:NodeInterface:can:edges_to_nodes
(dir: EdgeDir) -> list[Node] {
    ret_nodes = [];
    if dir in [EdgeDir.OUT, EdgeDir.ANY] {
        for i in <self>.edges[EdgeDir.OUT] {
            ret_nodes.append(i.target);
        }
    } elif dir in [EdgeDir.IN, EdgeDir.ANY] {
        for i in <self>.edges[EdgeDir.IN] {
            ret_nodes.append(i.source);
        }
    }
    return ret_nodes;
}

:obj:EdgeInterface:can:apply_dir
(dir: EdgeDir) -> Edge {
    <self>.dir = dir;
    return <self>;
}

:obj:EdgeInterface:can:attach
(src: Node, trg: Node) -> Edge {
    if <self>.dir == EdgeDir.IN {
        <self>.source = trg;
        <self>.target = src;
        <self> :> src._jac_.edges[EdgeDir.IN].append;
        <self> :> trg._jac_.edges[EdgeDir.OUT].append;
    } else {
        <self>.source = src;
        <self>.target = trg;
        <self> :> src._jac_.edges[EdgeDir.OUT].append;
        <self> :> trg._jac_.edges[EdgeDir.IN].append;
    }

    return <self>;
}

:obj:WalkerInterface:can:visit_node
(nds: list[Node]|list[Edge]|Node|Edge) {
    if isinstance(nds, list) {
        for i in nds {
            if(i not in <self>.ignores) { i :> <self>.next.append; }
        }
    } elif nds not in <self>.ignores { nds :> <self>.next.append; }
    return len(nds) if isinstance(nds, list) else 1;
}

:obj:WalkerInterface:can:ignore_node
(nds: list[Node]|list[Edge]|Node|Edge) {
    if isinstance(nds, list) {
        for i in nds {
            i :> <self>.ignores.append;
        }
    } else { nds :> <self>.ignores.append; }
}

:obj:WalkerInterface:can:disengage_now {
    <self>.next = [];
    <self>.disengaged = True;
}


:obj:NodeInterface:can:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self> :> walk;
}


:obj:EdgeInterface:can:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self>._jac_.target :> walk;
}

:obj:WalkerInterface:can:__call__
(nd: Node) {
    <self>._jac_.path = [];
    <self>._jac_.next = [nd];
    walker_type = <self>.__class__.__name__;
    while <self>._jac_.next :> len {
        nd = 0 :> <self>._jac_.next.pop;
        node_type = nd.__class__.__name__;

        for i in nd._jac_ds_.ds_entry_funcs {
            if i['func'].__qualname__.split(".")[0] == node_type and
                <self>:>type in i['types'] {
                (nd, <self>) :> i['func'];
            }
            if <self>._jac_.disengaged {return;}
        }
        for i in <self>._jac_ds_.ds_entry_funcs {
            if i['func'].__qualname__.split(".")[0] == walker_type and
                (nd:>type in i['types'] or nd in i['types']) {  # if nd==root direct chec
                (<self>, nd) :> i['func'];
            }
            if <self>._jac_.disengaged {return;}
        }
        for i in <self>._jac_ds_.ds_exit_funcs {
            if i['func'].__qualname__.split(".")[0] == walker_type and
            (nd:>type in i['types'] or nd in i['types']) {
                (<self>, nd) :> i['func'];
            }
            if <self>._jac_.disengaged {return;}
        }
        for i in nd._jac_ds_.ds_exit_funcs {
            if i['func'].__qualname__.split(".")[0] == node_type and
                <self>:>type in i['types'] {
                (nd, <self>) :> i['func'];
            }
            if <self>._jac_.disengaged {return;}
        }
        nd :> <self>._jac_.path.append;
    }
    <self>._jac_.ignores=[];
}

@hookimpl
:obj:JacPlugin:can:bind_architype
(arch: AT, arch_type: str) -> bool {
    match arch_type {
        case 'obj':
            arch._jac_ = ObjectInterface();
        case 'node':
            arch._jac_ = NodeInterface();
        case 'edge':
            arch._jac_ = EdgeInterface();
        case 'walker':
            arch._jac_ = WalkerInterface();
        case _:
            raise ("Invalid archetype type") :> TypeError;
    }
    return True;
}

@hookimpl
:obj:JacPlugin:can:get_root
() -> None {
    return exec_ctx.get_root();
}
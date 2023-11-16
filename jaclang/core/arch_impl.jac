"""Implementation for Jac's Element Abstractions"""
import:py from jaclang.jac.constant, EdgeDir;


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


:obj:Node:can:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self> :> walk;
}


:obj:Edge:can:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self>._jac_.target :> walk;
}

:obj:Walker:can:__call__
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
"""Implementation for Jac's Element Abstractions"""
import:py from jaclang.jac.constant, EdgeDir;

:object:Node:ability:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self> :> walk;
}

:object:Node:ability:_jac_connect_node_
(nd: Node, edg: Edge) -> Node {
    (<self>, nd) :> edg._jac_attach_;
    return <self>;
}

:object:Node:ability:_jac_edges_to_nodes_
(dir: EdgeDir) -> list[Node] {
    ret_nodes = [];
    if dir in [EdgeDir.OUT, EdgeDir.ANY] {
        for i in <self>._jac_edges_[EdgeDir.OUT] {
            ret_nodes.append(i._jac_target_);
        }
    } elif dir in [EdgeDir.IN, EdgeDir.ANY] {
        for i in <self>._jac_edges_[EdgeDir.IN] {
            ret_nodes.append(i._jac_source_);
        }

    }
    return ret_nodes;
}

:object:Edge:ability:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self>._jac_target_ :> walk;
}

:object:Edge:ability:_jac_apply_dir_
(dir: EdgeDir) -> Edge {
    <self>._jac_dir_ = dir;
    return <self>;
}

:object:Edge:ability:_jac_attach_
(src: Node, trg: Node) -> Edge {
    if <self>._jac_dir_ == EdgeDir.IN {
        <self>._jac_source_ = trg;
        <self>._jac_target_ = src;
        <self> :> src._jac_edges_[EdgeDir.IN].append;
        <self> :> trg._jac_edges_[EdgeDir.OUT].append;
    } else {
        <self>._jac_source_ = src;
        <self>._jac_target_ = trg;
        <self> :> src._jac_edges_[EdgeDir.OUT].append;
        <self> :> trg._jac_edges_[EdgeDir.IN].append;
    }

    return <self>;
}

:object:Walker:ability:__call__
(nd: Node) {
    <self>._jac_path_ = [];
    <self>._jac_next_ = [nd];
    walker_type = <self>.__class__.__name__;
    while <self>._jac_next_ :> len {
        nd = 0 :> <self>._jac_next_.pop;
        node_type = nd.__class__.__name__;

        for i in nd._jac_ds_entry_funcs {
            if i['func'].__qualname__.split(".")[0] == node_type and
                <self>:>type in i['types'] {
                (nd, <self>) :> i['func'];
            }
            if <self>._jac_disengaged_ {return;}
        }
        for i in <self>._jac_ds_entry_funcs {
            if i['func'].__qualname__.split(".")[0] == walker_type and
                (nd:>type in i['types'] or nd in i['types']) {  # if nd==root direct chec
                (<self>, nd) :> i['func'];
            }
            if <self>._jac_disengaged_ {return;}
        }
        for i in <self>._jac_ds_exit_funcs {
            if i['func'].__qualname__.split(".")[0] == walker_type and
            (nd:>type in i['types'] or nd in i['types']) {
                (<self>, nd) :> i['func'];
            }
            if <self>._jac_disengaged_ {return;}
        }
        for i in nd._jac_ds_exit_funcs {
            if i['func'].__qualname__.split(".")[0] == node_type and
                <self>:>type in i['types'] {
                (nd, <self>) :> i['func'];
            }
            if <self>._jac_disengaged_ {return;}
        }
        nd :> <self>._jac_path_.append;
    }
    <self>._jac_ignores_=[];
}

:object:Walker:ability:_jac_visit_
(nds: list[Node]|list[Edge]|Node|Edge) {
    if isinstance(nds, list) {
        for i in nds {
            if(i not in <self>._jac_ignores_) { i :> <self>._jac_next_.append; }
        }
    } elif nds not in <self>._jac_ignores_ { nds :> <self>._jac_next_.append; }
    return len(nds) if isinstance(nds, list) else 1;
}

:object:Walker:ability:_jac_ignore_
(nds: list[Node]|list[Edge]|Node|Edge) {
    if isinstance(nds, list) {
        for i in nds {
            i :> <self>._jac_ignores_.append;
        }
    } else { nds :> <self>._jac_ignores_.append; }
}

:object:Walker:ability:_jac_disengage_ {
    <self>._jac_next_ = [];
    <self>._jac_disengaged_ = True;
}
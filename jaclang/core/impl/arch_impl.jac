"""Implementation for Jac's Element Abstractions"""
import:py from jaclang.jac.constant, EdgeDir;

:o:Node:a:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self> :> walk;
}

:o:Node:a:_jac_connect_node_
(nd: Node, edg: Edge) -> Node {
    (<self>, nd) :> edg._jac_attach_;
    return <self>;
}

:o:Node:a:_jac_edges_to_nodes_
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

:o:Edge:a:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self>._jac_target_ :> walk;
}

:o:Edge:a:_jac_apply_dir_
(dir: EdgeDir) -> Edge {
    <self>._jac_dir_ = dir;
    return <self>;
}

:o:Edge:a:_jac_attach_
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

:o:Walker:a:__call__
(nd: Node) {
    <self>._jac_path_ = [];
    <self>._jac_next_ = [nd];
    # while <self>._jac_next_ :> len {
        nd = 0 :> <self>._jac_next_.pop;
        <self>._jac_next_ :> len :> print;
        for i in nd._jac_ds_enter_funcs {
            if <self>:>type in i['types'] {
                (nd, <self>) :> i['func'];
            }
        }
        for i in <self>._jac_ds_enter_funcs {
            if nd:>type in i['types'] or nd in i['types'] {  # if nd==root direct chec
                (<self>, nd) :> i['func'];
            }
        }
        for i in <self>._jac_ds_exit_funcs {
            if nd:>type in i['types'] or nd in i['types'] {
                (<self>, nd) :> i['func'];
            }
        }
        for i in nd._jac_ds_exit_funcs {
            if <self>:>type in i['types'] {
                (nd, <self>) :> i['func'];
            }
        }
        nd :> <self>._jac_path_.append;
        <self>._jac_next_ :> len :> print;
    # }
}

:o:Walker:a:_jac_visit_
(nds: list[Node]|list[Edge]) {
    <self>._jac_ds_enter_funcs :> print;
    for i in nds {
        i :> <self>._jac_next_.append;
    }
}
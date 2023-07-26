"""Implementation for Jac's Element Abstractions"""

:o:Node:a:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self> :> walk;
}

:o:Node:a:_jac_connect_node_(nd: Node, edg: Edge) -> Node {
    edg._jac_attach_(<self>, nd);
    return <self>;
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
    } else {
        <self>._jac_source_ = src;
        <self>._jac_target_ = trg;
    }
    <self> :> src._jac_edges_.append;
    <self> :> trg._jac_edges_.append;
    return <self>;
}

:o:Walker:a:__call__
(nd: Node) {
    for i in nd._jac_ds_entry_funcs {
        if <self>:>type in i['types'] {
            (nd, <self>) :> i['func'];
        }
    }
    for i in <self>._jac_ds_entry_funcs {
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
}
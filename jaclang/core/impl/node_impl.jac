"""Implementation for Jac's Element Abstractions"""

:o:Node:a:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self> :> walk;
}

:o:Edge:a:__call__
(walk: Walker) {
    if not (walk, Walker) :> isinstance {
        raise ("Argument must be a Walker instance") :> TypeError;
    }
    <self>._jac_target_ :> walk;
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
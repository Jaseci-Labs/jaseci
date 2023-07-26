"""Implementation for Jac's Element Abstractions"""

:o:Node:a:__call__
(walk: Walker) {
    walk(<self>);
}

:o:Walker:a:__call__
(nd: Node) {
    for i in nd._jac_ds_entry_funcs {
        if <self>:>type in i['types'] {
            i['func'](nd, <self>);
        }
    }
    for i in <self>._jac_ds_entry_funcs {
        if nd:>type in i['types'] or nd in i['types'] {  # if nd==root direct chec
            i['func'](<self>, nd);
        }
    }
    for i in <self>._jac_ds_exit_funcs {
        if nd:>type in i['types'] or nd in i['types'] {
            i['func'](<self>, nd);
        }
    }
    for i in nd._jac_ds_exit_funcs {
        if <self>:>type in i['types'] {
            i['func'](nd, <self>);
        }
    }
}
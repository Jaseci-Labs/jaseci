import from jaclang.runtime.osp_kernel { osp_skip_rest }
walker ScopeWalker {
    has seen: set[int] = set();

    can walk_scope with UniScopeNode entry;
}

import inspect;
import jaclang.runtime.osp_kernel as _kernel;
import from contextvars { ContextVar }
import from types { UnionType }
import from typing { cast }
import from jaclang.runtime.archetype {
    NodeAnchor,
    EdgeAnchor,
    ObjectSpatialFunction,
    WalkerArchetype
}
import from jaclang.runtime.osp_graph_sv { cls_of_tag, tag_of_cls }
import from jaclang.runtime.osp_kernel {
    OspSlot,
    OspWalkerDesc,
    OspNodeDesc,
    OspWalkScope,
    OspRuntime,
    UNTYPED
}

obj _ContextStack {
    has _var: any postinit;

    def postinit;
    def _list -> list[any];
    def append(x: any);
    def pop -> any;
    def __getitem__(k: any) -> any;
    def __bool__ -> bool;
    def __len__ -> int;
}

with entry {
    _kernel.DEFAULT.stack = cast(list[OspWalkScope], _ContextStack());
}

def isolate_request_walk_stack;

glob _desc_of_cls: dict[(any, OspWalkerDesc)] = {};

def _trigger_members(trig: any) -> list[type];

def _slots_from(funcs: list[ObjectSpatialFunction]) -> list[OspSlot];

def _mro_funcs(cls: any, attr: str) -> list[any];

def desc_for(cls: any) -> OspWalkerDesc;

def _sv_tag_of(handle: any) -> int;

def _sv_is_a(tag: int, base: int) -> bool;

glob _ndesc_of_cls: dict[type, OspNodeDesc] = {};

def _sv_node_desc(tag: int) -> OspNodeDesc;

def _sv_on_complete(scope: OspWalkScope, ok: bool);

def make_sv_runtime -> OspRuntime;

async def osp_spawn_async(
    rt: OspRuntime, wlk: any, wdesc: OspWalkerDesc, starts: list[any]
) -> any;

impl _ContextStack.postinit {
    self._var = ContextVar('osp_walk_stack', `default=None);
}

impl _ContextStack._list -> list[any] {
    v = self._var.get();
    return v if v is not None else [];
}

impl _ContextStack.append(x: any) {
    cur = self._var.get();
    new = `list(cur) if cur is not None else [];
    new.append(x);
    self._var.set(new);
}

impl _ContextStack.pop -> any {
    cur = self._var.get();
    new = `list(cur) if cur is not None else [];
    val = new.pop();
    self._var.set(new);
    return val;
}

impl _ContextStack.__getitem__(k: any) -> any {
    return self._list()[k];
}

impl _ContextStack.__bool__ -> bool {
    return bool(self._list());
}

impl _ContextStack.__len__ -> int {
    return len(self._list());
}

impl isolate_request_walk_stack {
    if isinstance(_kernel.DEFAULT.stack, _ContextStack) {
        _kernel.DEFAULT.stack._var.set([]);
    }
}

impl _trigger_members(trig: any) -> list[type] {
    if trig is None {
        return [];
    }
    if isinstance(trig, UnionType) {
        return `list(trig.__args__);
    }
    if isinstance(trig, tuple) {
        return `list(trig);
    }
    return [trig];
}

impl _slots_from(funcs: list[ObjectSpatialFunction]) -> list[OspSlot] {
    slots: list[OspSlot] = [];
    for f in funcs {
        members = _trigger_members(f.trigger);
        if not members {
            slots.append(OspSlot(trig_tag=UNTYPED, fn=f.func));
        } else {
            for m in members {
                slots.append(OspSlot(trig_tag=tag_of_cls(m), fn=f.func));
            }
        }
    }
    return slots;
}

impl _mro_funcs(cls: any, attr: str) -> list[any] {
    merged: dict[str, any] = {};
    for c in reversed(cls.__mro__) {
        clsfns = c.__dict__.get(attr);
        if clsfns {
            for fn in clsfns {
                merged[fn.name] = fn;
            }
        }
    }
    return `list(merged.values());
}

impl desc_for(cls: any) -> OspWalkerDesc {
    if cls in _desc_of_cls {
        return _desc_of_cls[cls];
    }
    desc = OspWalkerDesc(
        type_tag=tag_of_cls(cls),
        `entry=_slots_from(
            cast(list[ObjectSpatialFunction], _mro_funcs(cls, '_jac_entry_funcs_'))
        ),
        `exit=_slots_from(
            cast(list[ObjectSpatialFunction], _mro_funcs(cls, '_jac_exit_funcs_'))
        )
    );
    _desc_of_cls[cls] = desc;
    return desc;
}

impl _sv_tag_of(handle: any) -> int {
    return tag_of_cls(`type(handle));
}

impl _sv_is_a(tag: int, base: int) -> bool {
    tc = cls_of_tag(tag);
    bc = cls_of_tag(base);
    return tc is not None and bc is not None and issubclass(tc, bc);
}

impl _sv_node_desc(tag: int) -> OspNodeDesc {
    cls = cls_of_tag(tag);
    if cls is None {
        return OspNodeDesc(type_tag=tag, `entry=[], `exit=[]);
    }
    cached = _ndesc_of_cls.get(cls);
    if cached is not None {
        return cached;
    }
    d = desc_for(cls);
    nd = OspNodeDesc(type_tag=d.type_tag, `entry=d.`entry, `exit=d.`exit);
    _ndesc_of_cls[cls] = nd;
    return nd;
}

impl _sv_on_complete(scope: OspWalkScope, ok: bool) {
    if isinstance(scope.wlk, WalkerArchetype) {
        anch = scope.wlk.__jac__;
        walked: list[(NodeAnchor | EdgeAnchor)] = [];
        for step in scope.path {
            step_anchor = step?.__jac__;
            if isinstance(step_anchor, (NodeAnchor, EdgeAnchor)) {
                walked.append(step_anchor);
            }
        }
        anch.path = walked;
        anch.next = [];
        anch.ignores = [];
    }
    if scope.nested {
        return;
    }

    if isinstance(scope.wlk, WalkerArchetype) {
        scope.wlk.reports = scope.reports;
    }

    import from jaclang.runtime.runtime { JacRuntime }
    ctx = None;
    try {
        ctx = JacRuntime.peek_context();
        if ctx is None {
            return;
        }
        cs = ctx.call_state.get(None);
        if cs is not None {
            for r in scope.reports {
                cs.reports.put_nowait(r);
            }
        }
    } except Exception {}
    if ok and (ctx is not None) {
        try {
            ctx.mem.commit();
        } except Exception {}
    }
}

impl make_sv_runtime -> OspRuntime {
    return OspRuntime(
        tag_of=_sv_tag_of,
        is_a=_sv_is_a,
        node_desc=_sv_node_desc,
        on_complete=_sv_on_complete
    );
}

impl osp_spawn_async(
    rt: OspRuntime, wlk: any, wdesc: OspWalkerDesc, starts: list[any]
) -> any {
    eng = _kernel.DEFAULT;
    scope = eng.begin(wlk, starts);
    ok = False;
    try {
        while True {
            s = eng.next_slot(rt, scope, wdesc);
            if s is None {
                break;
            }
            result = s.fn(scope.cur_a, scope.cur_b);
            if inspect.iscoroutine(result) {
                await result;
            }
        }
        ok = True;
    } finally {
        eng.finish(scope, ok, rt);
    }
    return wlk;
}

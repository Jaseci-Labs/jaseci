"""Jac's Key Elemental Abstractions"""

import:py from datetime, datetime;
import:py from uuid, UUID, uuid4;
import:py from jaclang.compiler.constant, EdgeDir;
import:py from jaclang.plugin, Architype, ArchitypeProtocol, DSFunc, AbsRootHook, hookimpl;

enum AccessMode;

obj Memory {
    has index: dict[UUID, Element] = {},
        save_queue: list[Element] = [];
    #* Main Accessors *#
    can get_obj(caller_id: UUID, item_id: UUID, override: bool=False) -> Element;
    can has_obj(item_id: UUID) -> bool;
    can save_obj(caller_id: UUID, item: Element);
    can del_obj(caller_id: UUID, item: Element);
    #* Utility Functions *#

    can get_object_distribution -> dict;
    can get_mem_size -> float;
}

obj ExecutionContext {
    has master: Master = :> uuid4,
        memory: Memory = Memory();

    can reset;
    can get_root() -> Architype;
}

"Global Execution Context, should be monkey patched by the user."
glob exec_ctx = ExecutionContext();

obj ElementAnchor {
    has ob: object,
        jid: UUID = :> uuid4,
        timestamp: datetime = :> datetime.now,
        persist: bool = False,
        access_mode: AccessMode = AccessMode.PRIVATE,
        rw_access: set = :> set,
        ro_access: set = :> set,
        owner_id: UUID = exec_ctx.master,
        mem: Memory = exec_ctx.memory;

    can make_public_ro;
    can make_public_rw;
    can make_private;
    can is_public_ro -> bool;
    can is_public_rw -> bool;
    can is_private -> bool;
    can is_readable(caller_id: UUID) -> bool;
    can is_writable(caller_id: UUID) -> bool;
    can give_access(caller_id: UUID, read_write: bool=False);
    can revoke_access(caller_id: UUID);
}

obj ObjectAnchor :ElementAnchor, ArchitypeProtocol: {
    has ds_entry_funcs: list[DSFunc],
        ds_exit_funcs: list[DSFunc];

    static can on_entry(cls: type, triggers: list[type]);
    static can on_exit(cls: type, triggers: list[type]);
}

obj NodeAnchor :ObjectAnchor: {
    has edges: dict[EdgeDir, list[Edge]] = {EdgeDir.IN: [], EdgeDir.OUT: []};

    can connect_node(nd: Node, edg: Edge) -> Node;
    can edges_to_nodes(dir: EdgeDir) -> list[Node];
    can __call__(walk: Walker);
}

obj EdgeAnchor :ObjectAnchor: {
    has source: Node = None,
        target: Node = None,
        dir: EdgeDir = None;

    can apply_dir(dir: EdgeDir) -> Edge;
    can attach(src: Node, trg: Node) -> Edge;
    can __call__(walk: Walker);
}

obj WalkerAnchor :ObjectAnchor: {
    has path: list[Node] = [],
        next: list[Node] = [],
        ignores: list[Node] = [],
        disengaged: bool = False;

    can visit_node(nds: list[Node] | list[Edge] | Node | Edge);
    can ignore_node(nds: list[Node] | list[Edge] | Node | Edge);
    can disengage_now;
    can __call__(nd: Node);
}

obj Root :AbsRootHook: {
    has _jac_: NodeAnchor | None = None;

    can postinit {
        self._jac_ = NodeAnchor(self, ds_entry_funcs=[], ds_exit_funcs=[]);
    }
}

obj GenericEdge :ArchitypeProtocol: {
    has _jac_: EdgeAnchor | None = None;

    can postinit {
        self._jac_ = EdgeAnchor(self, ds_entry_funcs=[], ds_exit_funcs=[]);
    }
}

obj Master {
    has _jac_: ElementAnchor | None = None;
    has root_node: Root = Root(Root);

    can postinit {
        self._jac_ = ElementAnchor(self);
    }
}

obj JacPlugin {
    @hookimpl
    static can bind_architype(arch: AT, arch_type: str, on_entry: list[str], on_exit: list[str]) -> bool;
    @hookimpl
    static can get_root() -> Architype;
    @hookimpl
    static can build_edge(edge_spec: tuple[int, Optional[tuple], Optional[tuple]]) -> Architype;
    @hookimpl
    static can connect(left: T, right: T, edge_spec: tuple[int, Optional[type], Optional[tuple]]) -> Architype;
    @hookimpl
    static can visit_node(walker_obj: Any, expr: Any) -> bool;
}

:obj:Memory:can:get_obj
(caller_id: UUID, item_id: UUID, override: bool=False) -> Element {
    ret = item_id |> self.index.get;
    if override
        or (ret is not None and caller_id |> ret.__is_readable) {
        return ret;
    }
}

:obj:Memory:can:has_obj
(item_id: UUID) -> bool {
    return item_id in self.index;
}

:obj:Memory:can:save_obj
(caller_id: UUID, item: Element) {
    if caller_id |> item.is_writable {
        self.index[item.id] = item;
        if item._persist {
            item |> self.save_obj_list.add;
        }
    }
    self.mem[item.id] = item;
    if item._persist {
        item |> self.save_obj_list.add;
    }
}

:obj:Memory:can:del_obj
(caller_id: UUID, item: Element) {
    if caller_id |> item.is_writable {
        self.index.pop(item.id);
        if item._persist {
            item |> self.save_obj_list.remove;
        }
    }
}

:obj:Memory:can:get_object_distribution -> dict {
    dist = {};
    for i in |> self.index.keys {
        t = self.index[i] |> type;
        if t in dist {
            dist[t] += 1;
        } else {
            dist[t] = 1;
        }
    }
    return dist;
}

:obj:Memory:can:get_mem_size -> float {
    return (self.index |> sys.getsizeof) / 1024.0;
}

:obj:ExecutionContext:c:get_root() {
    if self.master :> type == UUID {
        self.master = Master();
    }
    return self.master.root_node;
}

:obj:ExecutionContext:c:reset {
    self.init();
}

"""Implementation for Jac's Element Abstractions"""
:enum:AccessMode {
    READ_ONLY,
    READ_WRITE,
    PRIVATE
}

:obj:ElementAnchor:can:make_public_ro {
    self.__jinfo.access_mode = AccessMode.READ_ONLY;
}

:obj:ElementAnchor:can:make_public_rw {
    self.__jinfo.access_mode = AccessMode.READ_WRITE;
}

:obj:ElementAnchor:can:make_private {
    self.__jinfo.access_mode = AccessMode.PRIVATE;
}

:obj:ElementAnchor:can:is_public_ro -> bool {
    return self.__jinfo.access_mode == AccessMode.READ_ONLY;
}

:obj:ElementAnchor:can:is_public_rw -> bool {
    return self.__jinfo.access_mode == AccessMode.READ_WRITE;
}

:obj:ElementAnchor:can:is_private -> bool {
    return self.__jinfo.access_mode == AccessMode.PRIVATE;
}

:obj:ElementAnchor:can:is_readable
(caller_id: UUID) -> bool {
    return (caller_id == self.owner_id
        or |> self.is_public_read
        or caller_id in self.ro_access
        or caller_id in self.rw_access);
}

:obj:ElementAnchor:can:is_writable
(caller_id: UUID) -> bool {
    return (caller_id == self.owner_id
        or |> self.is_public_write
        or caller_id in self.rw_access);
}

:obj:ElementAnchor:can:give_access
(caller_id: UUID, read_write: bool=False) {
    if read_write {
        caller_id |> self.rw_access.add;
    } else {
        caller_id |> add.>ro_access.>self;
    }
}

:obj:ElementAnchor:can:revoke_access
(caller_id: UUID) {
    caller_id |> self.ro_access.discard;
    caller_id |> self.rw_access.discard;
}

:obj:ObjectAnchor:can:on_entry
(cls: type, triggers: list) {
    can decorator(func: callable) -> callable {
        cls.ds_entry_funcs.append(
            {'types': triggers, 'func': func}
        );
        can wrapper(*args: list, **kwargs: dict) -> callable {
            return func(*args, **kwargs);
        }
        return wrapper;
    }
    return decorator;
}

:obj:ObjectAnchor:can:on_exit
(cls: type, triggers: list) {
    can decorator(func: callable) -> callable {
        cls.ds_exit_funcs.append(
            {'types': triggers, 'func': func}
        );
        can wrapper(*args: list, **kwargs: dict) -> callable {
            return func(*args, **kwargs);
        }
        return wrapper;
    }
    return decorator;
}

:obj:NodeAnchor:can:connect_node
(nd: NodeInterface, edg: EdgeInterface) -> Node {
    edg.attach(self, nd);
    return self;
}

:obj:NodeAnchor:can:edges_to_nodes
(dir: EdgeDir) -> list[Node] {
    ret_nodes = [];
    if dir in [EdgeDir.OUT, EdgeDir.ANY] {
        for i in self.edges[EdgeDir.OUT] {
            ret_nodes.append(i.target);
        }
    } elif dir in [EdgeDir.IN, EdgeDir.ANY] {
        for i in self.edges[EdgeDir.IN] {
            ret_nodes.append(i.source);
        }
    }
    return ret_nodes;
}

:obj:EdgeAnchor:can:apply_dir
(dir: EdgeDir) -> Edge {
    self.dir = dir;
    return self;
}

:obj:EdgeAnchor:can:attach
(src: NodeInterface, trg: NodeInterface) -> Edge {
    if self.dir == EdgeDir.IN {
        self.source = trg;
        self.target = src;
        self :> src.edges[EdgeDir.IN].append;
        self :> trg.edges[EdgeDir.OUT].append;
    } else {
        self.source = src;
        self.target = trg;
        self :> src.edges[EdgeDir.OUT].append;
        self :> trg.edges[EdgeDir.IN].append;
    }
    return self;
}

:obj:WalkerAnchor:can:visit_node
(nds: list[Node] | list[Edge] | Node | Edge) {
    if isinstance(nds, list) {
        for i in nds {
            if (i not in self.ignores) {
                i :> self.next.append;
            }
        }
    } elif nds not in self.ignores {
        nds :> self.next.append;
    }
    return len(nds) if isinstance(nds, list) else 1;
}

:obj:WalkerAnchor:can:ignore_node
(nds: list[Node] | list[Edge] | Node | Edge) {
    if isinstance(nds, list) {
        for i in nds {
            i :> self.ignores.append;
        }
    } else {
        nds :> self.ignores.append;
    }
}

:obj:WalkerAnchor:can:disengage_now {
    self.next = [];
    self.disengaged = True;
}

:obj:NodeAnchor:can:__call__
(walk: object) {
    if not isinstance(walk._jac_, WalkerAnchor) {
        raise TypeError("Argument must be a Walker instance");
    }
    walk(self);
}

:obj:EdgeAnchor:can:__call__
(walk: EdgeInterface) {
    if not isinstance(walk._jac_, WalkerAnchor) {
        raise TypeError("Argument must be a Walker instance");
    }
    walk(self._jac_.target);
}

:obj:WalkerAnchor:can:__call__
(nd: NodeInterface) {
    self.path = [];
    self.next = [nd];
    while len(self.next) {
        nd = self.next.pop(0);
        print(nd.__class__.__name__, self.ds_entry_funcs);
        for i in nd.ds_entry_funcs {
            if isinstance(self.ob, i.trigger) {
                i.func(nd.ob, self);
            }
            if self.disengaged {
                return;
            }
        }
        for i in self.ds_entry_funcs {
            if isinstance(nd.ob, i.trigger) {
                i.func(self.ob, nd);
            }
            if self.disengaged {
                return;
            }
        }
        for i in self.ds_exit_funcs {
            if isinstance(nd.ob, i.trigger) {
                i.func(self.ob, nd);
            }
            if self.disengaged {
                return;
            }
        }
        for i in nd.ds_exit_funcs {
            if isinstance(self.ob, i.trigger) {
                i.func(nd.ob, self);
            }
            if self.disengaged {
                return;
            }
        }
        nd :> self.path.append;
    }
    self.ignores = [];
}

:obj:JacPlugin:can:bind_architype
(arch: AT, arch_type: str, on_entry: list[DSFunc], on_exit: list[DSFunc]) -> bool {
    match arch_type {
        case 'obj':
            arch._jac_ = ObjectAnchor(
                ob=arch,
                ds_entry_funcs=on_entry,
                ds_exit_funcs=on_exit
            );
        case 'node':
            arch._jac_ = NodeAnchor(
                ob=arch,
                ds_entry_funcs=on_entry,
                ds_exit_funcs=on_exit
            );
        case 'edge':
            arch._jac_ = EdgeAnchor(
                ob=arch,
                ds_entry_funcs=on_entry,
                ds_exit_funcs=on_exit
            );
        case 'walker':
            arch._jac_ = WalkerAnchor(
                ob=arch,
                ds_entry_funcs=on_entry,
                ds_exit_funcs=on_exit
            );
        case _:
            raise ("Invalid archetype type") :> TypeError;
    }
    return True;
}

:obj:JacPlugin:can:get_root() -> None {
    return exec_ctx.get_root();
}

:obj:JacPlugin:can:build_edge
(edge_spec: tuple[int, Optional[type], Optional[tuple]]) -> Architype {
    if (not edge_spec[1]) {
        edg_type = GenericEdge;
    } else {
        edg_type = edge_spec[1];
    }
    edg = edg_type(*(edge_spec[2])) if edge_spec[2] else edg_type();
    edg._jac_.apply_dir(edge_spec[0]);
    return edg;
}

:obj:JacPlugin:can:connect
(left: T, right: T, edge_spec: tuple[int, Optional[type], Optional[tuple]]) -> Architype {
    edg = JacPlugin.build_edge(edge_spec);
    left.connect_node(right._jac_, edg._jac_);
}

:obj:JacPlugin:can:visit_node
(walker_obj: Any, expr: Any) -> bool {
    return walker_obj._jac_.visit_node(expr);
}

glob expected_area = 78.53981633974483;

test a1 {
    check assertAlmostEqual(calculate_area(RAD), expected_area);
}

test a2 {
    c = Circle(RAD);
    check assertAlmostEqual(c.area(), expected_area);
}

test a3 {
    c = Circle(RAD);
    check assertEqual(c.shape_type, ShapeType.CIRCLE);
}

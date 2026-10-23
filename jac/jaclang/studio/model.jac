import os;
import time;
import threading;

glob SKIP_DIRS: list[str] = [
         "node_modules",
         "__pycache__",
         "build",
         "dist",
         ".venv",
         "venv",
         "zig-out",
         "zig-pkg",
         "vendor"
     ],
     SYM_SCHEME: str = "jac://sym/";

node StNode {
    has key: str = "",
        name: str = "",
        kind: str = "",
        file: str = "",
        line: int = 0,
        end_line: int = 0,
        col: int = 0,
        doc: str = "";
}

node StProject(StNode) {
    has root_dir: str = "";
}

node StPackage(StNode) {}

node StModule(StNode) {
    has files: list[str] = [],
        mtime: float = 0.0,
        archwire: str = "",
        local_name: str = "",
        indexed: bool = False,
        error: str = "";
}

node StArchetype(StNode) {
    has bases: list[str] = [],
        walker_targets: list[str] = [],
        impl_file: str = "",
        impl_line: int = 0;
}

node StAbility(StNode) {
    has signature: str = "",
        owner: str = "",
        event: str = "",
        impl_file: str = "",
        impl_line: int = 0,
        impl_end_line: int = 0;
}

node StField(StNode) {
    has type_str: str = "",
        owner: str = "";
}

node StImpl(StNode) {
    has target: str = "";
}

node StRule(StNode) {
    has sources: list[str] = [],
        targets: list[str] = [],
        names: list[str] = [];
}

edge Contains: StNode --> StNode {}

edge Wire: StModule --> StModule {
    has names: list[str] = [],
        injected: bool = True,
        form: str = "",
        archwire: str = "",
        line: int = 0;
}

edge Implements: StImpl --> StNode {}

edge Governs: StRule --> StModule {}

edge Traverses: StArchetype --> StArchetype {}

edge Uses: StNode --> StNode {}

obj WireInfo {
    has provider: str,
        consumer: str,
        scope: str = "",
        names: list[str] = [],
        injected: bool = True,
        form: str = "",
        archwire: str = "",
        line: int = 0;

    def to_dict -> dict[str, any];
}

obj ProjectModel {
    has root_dir: str,
        top: StProject postinit,
        modules: dict[str, StModule] = {},
        packages: dict[str, StPackage] = {},
        symbols: dict[str, StNode] = {},
        by_file: dict[str, str] = {},
        wires: list[WireInfo] = [],
        rules: list[StRule] = [],
        archwires: list[str] = [],
        prog: JacProgram postinit,
        lock: any postinit,
        build_secs: float = 0.0,
        index_secs: float = 0.0;

    def postinit;
    def build(on_progress: any = None, index: bool = True);
    def index_all(on_progress: any = None);
    def _arch_files -> list[str];
    def _head_files -> list[str];
    def _rel_dotted(path: str) -> str;
    def _ensure_package(dotted: str) -> StNode;
    def _add_module(key: str, path: str, archwire: str, local_name: str) -> StModule;
    def _discover;
    def _spec_key(spec: WiringSpec, local: str) -> str;
    def _is_nested_project(arch: str) -> bool;
    def _add_wiring(arch: str, spec: WiringSpec);
    def _add_symbol(owner: StNode, sym: StNode);
    def _clear_module_symbols(mod: StModule);
    def _text(nd: any) -> str;
    def _span(sym: StNode, nd: uni.UniNode);
    def _doc(nd: any) -> str;
    def _ability_node(key: str, ab: uni.Ability, owner: str) -> StAbility;
    def index_module(key: str) -> bool;
    def _index_archetype(mod: StModule, arch: uni.Archetype);
    def _index_impl(mod: StModule, idef: uni.ImplDef) -> None;
    def _link_walkers;
    def refresh(path: str) -> list[str];
    def stale_files -> list[str];
    def module_for_file(path: str) -> (StModule | None);
    def providers(key: str) -> list[WireInfo];
    def consumers(key: str) -> list[WireInfo];
    def children(key: str) -> list[StNode];
    def node_for(key: str) -> (StNode | None);
    def implementations(key: str) -> list[StImpl];
    def traversals(key: str) -> list[StNode];
    def walkers_of(key: str) -> list[StNode];
    def rules_for(key: str) -> list[StRule];
    def search(
        query: str, limit: int = 50, kinds: (list[str] | None) = None
    ) -> list[StNode];

    def node_dict(nd: StNode) -> dict[str, any];
    def module_dict(key: str, deep: bool = True) -> dict[str, any];
    def _tree_dict(nd: StNode) -> dict[str, any];
    def to_dict(module: str = "") -> dict[str, any];
    def stats -> dict[str, any];
}

def fuzzy_score(q: str, key: str, name: str) -> int;

def sym_uri(key: str) -> str;

def find_project_root(start: str) -> str;

impl WireInfo.to_dict -> dict[str, any] {
    return {
        "provider": self.provider,
        "consumer": self.consumer,
        "scope": self.scope,
        "names": self.names,
        "injected": self.injected,
        "form": self.form,
        "archwire": self.archwire,
        "line": self.line
    };
}

impl ProjectModel.postinit {
    self.root_dir = os.path.realpath(self.root_dir);
    self.top = StProject(
        key="",
        name=os.path.basename(self.root_dir),
        kind="project",
        root_dir=self.root_dir
    );
    self.prog = JacProgram();
    self.lock = threading.RLock();
}

impl ProjectModel.build(on_progress: any = None, index: bool = True) {
    t0 = time.time();
    with self.lock {
        self._discover();
    }
    self.build_secs = time.time() - t0;
    if index {
        self.index_all(on_progress);
    }
}

impl ProjectModel.index_all(on_progress: any = None) {
    t0 = time.time();
    keys = sorted(
        [
            k
            for (k, m) in self.modules.items()
            if m.kind == "module"
        ]
    );
    total = len(keys);
    n = 0;
    for k in keys {
        self.index_module(k);
        n += 1;
        if on_progress is not None {
            on_progress(n, total, k);
        }
    }
    with self.lock {
        self._link_walkers();
    }
    self.index_secs = time.time() - t0;
}

impl ProjectModel._arch_files -> list[str] {
    found: list[str] = [];
    for (d, ds, fs) in os.walk(self.root_dir) {
        ds[:] = sorted(
            [
                x
                for x in ds
                if not x.startswith(".") and x not in SKIP_DIRS
            ]
        );
        if ARCH_FILE_NAME in fs {
            found.append(os.path.join(d, ARCH_FILE_NAME));
        }
    }
    return found;
}

impl ProjectModel._head_files -> list[str] {
    found: list[str] = [];
    for (d, ds, fs) in os.walk(self.root_dir) {
        ds[:] = sorted(
            [
                x
                for x in ds
                if not x.startswith(".") and x not in SKIP_DIRS
            ]
        );
        for f in sorted(fs) {
            if f.endswith(".jac") and f.count(".") == 1 and f != ARCH_FILE_NAME {
                found.append(os.path.join(d, f));
            }
        }
    }
    return found;
}

impl ProjectModel._rel_dotted(path: str) -> str {
    rel = os.path.relpath(path, self.root_dir);
    if rel.endswith(".jac") {
        rel = rel[:-4];
    }
    parts = [
        p
        for p in rel.split(os.sep)
        if p and p != "."
    ];
    if parts and parts[-1] == "__init__" {
        parts = parts[:-1];
    }
    return ".".join(parts);
}

impl ProjectModel._ensure_package(dotted: str) -> StNode {
    if not dotted {
        return self.top;
    }
    if dotted in self.packages {
        return self.packages[dotted];
    }
    pkg = StPackage(key=dotted, name=dotted.split(".")[-1], kind="package");
    self.packages[dotted] = pkg;
    parent_key = ".".join(dotted.split(".")[:-1]);
    parent = self._ensure_package(parent_key);
    parent +>:Contains():+> pkg;
    return pkg;
}

impl ProjectModel._add_module(
    key: str, path: str, archwire: str, local_name: str
) -> StModule {
    if key in self.modules {
        return self.modules[key];
    }
    real = os.path.realpath(path) if path else "";
    mod = StModule(
        key=key,
        name=key.split(".")[-1],
        kind="module" if path else "external",
        file=real,
        files=[real] if real else [],
        archwire=archwire,
        local_name=local_name
    );
    self.modules[key] = mod;
    if real {
        self.by_file[real] = key;
        try {
            mod.mtime = os.path.getmtime(real);
        } except OSError {}
        parent = self._ensure_package(".".join(key.split(".")[:-1]));
        parent +>:Contains():+> mod;
    }
    return mod;
}

impl ProjectModel._discover {
    specs: list[tuple[str, WiringSpec]] = [];
    for arch in self._arch_files() {
        spec = wiring_for_path(arch);
        if spec is None {
            continue;
        }
        self.archwires.append(arch);
        specs.append((arch, spec));
    }
    for (arch, spec) in specs {
        nested = self._is_nested_project(arch);
        for local in spec.project_modules() {
            path = spec.module_file(local);
            if not path or os.path.basename(path) == ARCH_FILE_NAME {
                continue;
            }
            key = self._rel_dotted(os.path.realpath(path))
                if nested
                else spec.import_name(local);
            self._add_module(key, path, arch, local);
        }
    }
    for path in self._head_files() {
        real = os.path.realpath(path);
        if real in self.by_file {
            continue;
        }
        self._add_module(self._rel_dotted(real), real, "", "");
    }
    for (arch, spec) in specs {
        self._add_wiring(arch, spec);
    }
}

impl ProjectModel._spec_key(spec: WiringSpec, local: str) -> str {
    path = spec.module_file(local);
    if path and os.path.realpath(path) in self.by_file {
        return self.by_file[os.path.realpath(path)];
    }
    if path {
        return spec.import_name(local);
    }
    return local;
}

impl ProjectModel._add_wiring(arch: str, spec: WiringSpec) {
    for w in spec.wires {
        prov_key = self._spec_key(spec, w.provider);
        prov = self.modules.get(prov_key);
        if prov is None {
            prov = self._add_module(prov_key, "", arch, w.provider);
        }
        names = [(n if not a else f"{n} as {a}") for (n, a) in w.items];
        form = "import" if w.is_module_form else "import from";
        if w.is_comptime {
            form = "comptime " + form;
        }
        if w.is_typed {
            form = "type " + form;
        }
        if w.is_absorb {
            form = "include";
        }
        for consumer in w.consumers {
            split = spec.split_consumer(consumer);
            (cmod, scope) = (consumer, []);
            if split is not None {
                (cmod, scope) = split;
            }
            ckey = self._spec_key(spec, cmod);
            cnode = self.modules.get(ckey);
            if cnode is None {
                cnode = self._add_module(ckey, "", arch, cmod);
            }
            info = WireInfo(
                provider=prov_key,
                consumer=ckey,
                scope=".".join(scope),
                names=names,
                injected=w.is_injected,
                form=form,
                archwire=arch,
                line=w.line
            );
            self.wires.append(info);
            prov +>:Wire(
                names=names,
                injected=w.is_injected,
                form=form,
                archwire=arch,
                line=w.line
            ):+> cnode;
        }
    }
    for r in spec.rules {
        rule = StRule(
            key=f"{arch}#{r.name}",
            name=r.name,
            kind="rule",
            file=os.path.realpath(arch),
            sources=[p.text for p in r.sources],
            targets=[p.text for p in r.targets],
            names=sorted(r.item_names) if r.item_names else []
        );
        self.rules.append(rule);
        self.top +>:Contains():+> rule;
        for (key, mod) in self.modules.items() {
            if mod.archwire != arch or not mod.local_name {
                continue;
            }
            for p in r.sources {
                if p.matches(mod.local_name) {
                    rule +>:Governs():+> mod;
                    break;
                }
            }
        }
    }
}

impl ProjectModel._add_symbol(owner: StNode, sym: StNode) {
    self.symbols[sym.key] = sym;
    owner +>:Contains():+> sym;
}

impl ProjectModel._clear_module_symbols(mod: StModule) {
    stale = [
        k
        for k in self.symbols
        if k.startswith(mod.key + ".")
    ];
    for k in stale {
        sym = self.symbols.pop(k);
        del sym;
    }
    for kid in [mod->:Contains:->] {
        del [edge mod->:Contains:->kid];
    }
    for f in mod.files[1:] {
        self.by_file.pop(f, None);
    }
    mod.files = mod.files[:1];
}

impl ProjectModel._text(nd: any) -> str {
    if nd is None {
        return "";
    }
    try {
        return " ".join(unparse_node(nd).split());
    } except Exception {
        return "";
    }
}

impl ProjectModel._span(sym: StNode, nd: uni.UniNode) {
    sym.file = os.path.realpath(nd.loc.mod_path);
    sym.line = nd.loc.first_line;
    sym.end_line = nd.loc.last_line;
    sym.col = nd.loc.col_start;
}

impl ProjectModel._doc(nd: any) -> str {
    doc = nd?.doc;
    if doc is None {
        return "";
    }
    try {
        return str(doc.lit_value).strip();
    } except Exception {
        return "";
    }
}

impl ProjectModel._ability_node(key: str, ab: uni.Ability, owner: str) -> StAbility {
    name = ab.name_ref.sym_name if ab.name_ref else "?";
    sig = ab.signature;
    sig_text = "";
    event = "";
    if isinstance(sig, uni.EventSignature) {
        event = self._text(sig.arch_tag_info);
        sig_text = f"with {event} {sig.event.value}".strip();
    } elif isinstance(sig, uni.FuncSignature) {
        sig_text = self._text(sig);
    }
    kind = "method" if owner else "def";
    if event or isinstance(sig, uni.EventSignature) {
        kind = "can";
    }
    snode = StAbility(
        key=key,
        name=name,
        kind=kind,
        signature=sig_text,
        owner=owner,
        event=event,
        doc=self._doc(ab)
    );
    self._span(snode, ab);
    return snode;
}

impl ProjectModel.index_module(key: str) -> bool {
    mod = self.modules.get(key);
    if mod is None or mod.kind != "module" {
        return False;
    }
    try {
        tree = active_host().woven_module(mod.file, self.prog);
    } except Exception as e {
        mod.error = str(e);
        return False;
    }
    if tree is None {
        mod.error = "could not parse";
        return False;
    }
    with self.lock {
        self._clear_module_symbols(mod);
        mod.error = "";
        mod.doc = self._doc(tree);
        for el in tree.body {
            if isinstance(el, uni.Archetype) {
                self._index_archetype(mod, el);
            } elif isinstance(el, uni.Enum) {
                name = el.name.sym_name;
                snode = StArchetype(
                    key=f"{key}.{name}",
                    name=name,
                    kind="enum",
                    bases=[self._text(b) for b in (el.base_classes or [])],
                    doc=self._doc(el)
                );
                self._span(snode, el);
                self._add_symbol(mod, snode);
            } elif isinstance(el, uni.Ability) {
                if el.name_ref is None {
                    continue;
                }
                anode = self._ability_node(f"{key}.{el.name_ref.sym_name}", el, "");
                self._add_symbol(mod, anode);
            }
        }
        for idef in tree.get_all_sub_nodes(uni.ImplDef) {
            self._index_impl(mod, idef);
        }
        try {
            mod.mtime = os.path.getmtime(mod.file);
        } except OSError {}
        mod.indexed = True;
    }
    return True;
}

impl ProjectModel._index_archetype(mod: StModule, arch: uni.Archetype) {
    name = arch.name.sym_name;
    akey = f"{mod.key}.{name}";
    snode = StArchetype(
        key=akey,
        name=name,
        kind=arch.arch_type.value,
        bases=[self._text(b) for b in (arch.base_classes or [])],
        doc=self._doc(arch)
    );
    self._span(snode, arch);
    self._add_symbol(mod, snode);
    for hv in arch.get_has_vars() {
        fname = hv.name.sym_name;
        f = StField(
            key=f"{akey}.{fname}",
            name=fname,
            kind="has",
            type_str=self._text(hv.type_tag.tag if hv.type_tag else None),
            owner=akey
        );
        self._span(f, hv);
        self._add_symbol(snode, f);
    }
    for ab in arch.get_methods() {
        if ab.name_ref is None {
            continue;
        }
        m = self._ability_node(f"{akey}.{ab.name_ref.sym_name}", ab, akey);
        self._add_symbol(snode, m);
        if m.event {
            snode.walker_targets.append(m.event);
        }
    }
}

impl ProjectModel._index_impl(mod: StModule, idef: uni.ImplDef) -> None {
    parts = [t.sym_name for t in idef.target];
    if not parts {
        return;
    }
    target = ".".join(parts);
    ikey = f"{mod.key}::idef::{target}";
    snode = StImpl(key=ikey, name=target, kind="impl", target=target);
    self._span(snode, idef);
    if snode.file and snode.file not in mod.files {
        mod.files.append(snode.file);
        self.by_file[snode.file] = mod.key;
    }
    self.symbols[ikey] = snode;
    mod +>:Contains():+> snode;
    decl = self.symbols.get(f"{mod.key}.{target}");
    if decl is not None {
        snode +>:Implements():+> decl;
        if isinstance(decl, StAbility) {
            decl.impl_file = snode.file;
            decl.impl_line = snode.line;
            decl.impl_end_line = snode.end_line;
        } elif isinstance(decl, StArchetype) {
            decl.impl_file = snode.file;
            decl.impl_line = snode.line;
        }
    }
}

impl ProjectModel._link_walkers {
    by_name: dict[str, list[StNode]] = {};
    for sym in self.symbols.values() {
        if isinstance(sym, StArchetype) and sym.kind in ["node", "edge"] {
            by_name.setdefault(sym.name, []).append(sym);
        }
    }
    for sym in list(self.symbols.values()) {
        if not isinstance(sym, StArchetype) or sym.kind != "walker" {
            continue;
        }
        for tgt in [sym->:Traverses:->] {
            del [edge sym->:Traverses:->tgt];
        }
        seen: set[str] = set();
        for ev in sym.walker_targets {
            for word in ev.replace("(", " ").replace(")", " ").replace(
                "|", " "
            ).replace(
                ",", " "
            ).split() {
                for cand in by_name.get(word, []) {
                    if cand.key not in seen {
                        seen.add(cand.key);
                        sym +>:Traverses():+> cand;
                    }
                }
            }
        }
    }
}

impl ProjectModel.refresh(path: str) -> list[str] {
    real = os.path.realpath(path);
    key = self.by_file.get(real);
    if key is None {
        base = active_host().base_file(real);
        if base {
            key = self.by_file.get(os.path.realpath(base));
        }
    }
    if key is None {
        if real.endswith(".jac")
            and os.path.exists(real)
            and real.startswith(self.root_dir) {
            with self.lock {
                key = self._rel_dotted(real);
                self._add_module(key, real, "", "");
            }
        } else {
            return [];
        }
    }
    self.prog = JacProgram();
    self.index_module(key);
    with self.lock {
        self._link_walkers();
    }
    return [key];
}

impl ProjectModel.stale_files -> list[str] {
    out: list[str] = [];
    for mod in list(self.modules.values()) {
        if mod.kind != "module" {
            continue;
        }
        for f in mod.files {
            try {
                if os.path.getmtime(f) > mod.mtime + 0.0001 {
                    out.append(f);
                    break;
                }
            } except OSError {
                out.append(f);
                break;
            }
        }
    }
    return out;
}

impl ProjectModel.module_for_file(path: str) -> (StModule | None) {
    key = self.by_file.get(os.path.realpath(path));
    return self.modules.get(key) if key else None;
}

impl ProjectModel.providers(key: str) -> list[WireInfo] {
    return [
        w
        for w in self.wires
        if w.consumer == key
    ];
}

impl ProjectModel.consumers(key: str) -> list[WireInfo] {
    return [
        w
        for w in self.wires
        if w.provider == key
    ];
}

impl ProjectModel.children(key: str) -> list[StNode] {
    nd: (StNode | None) = None;
    if key == "" {
        nd = self.top;
    } elif key in self.packages {
        nd = self.packages[key];
    } elif key in self.modules {
        nd = self.modules[key];
    } elif key in self.symbols {
        nd = self.symbols[key];
    }
    if nd is None {
        return [];
    }
    kids = [
        k
        for k in [nd->:Contains:->]
        if not isinstance(k, StImpl)
    ];
    return sorted(kids, key=lambda (k: StNode) -> tuple[int, str] { (k.line, k.name) });
}

impl ProjectModel.node_for(key: str) -> (StNode | None) {
    if key in self.modules {
        return self.modules[key];
    }
    if key in self.packages {
        return self.packages[key];
    }
    return self.symbols.get(key);
}

impl ProjectModel.implementations(key: str) -> list[StImpl] {
    nd = self.symbols.get(key);
    if nd is None {
        return [];
    }
    return [
        i
        for i in [nd<-:Implements:<-]
        if isinstance(i, StImpl)
    ];
}

impl ProjectModel.traversals(key: str) -> list[StNode] {
    nd = self.symbols.get(key);
    if nd is None {
        return [];
    }
    return [n for n in [nd->:Traverses:->]];
}

impl ProjectModel.walkers_of(key: str) -> list[StNode] {
    nd = self.symbols.get(key);
    if nd is None {
        return [];
    }
    return [n for n in [nd<-:Traverses:<-]];
}

impl ProjectModel.rules_for(key: str) -> list[StRule] {
    mod = self.modules.get(key);
    if mod is None {
        return [];
    }
    return [
        r
        for r in [mod<-:Governs:<-]
        if isinstance(r, StRule)
    ];
}

impl ProjectModel.search(
    query: str, limit: int = 50, kinds: (list[str] | None) = None
) -> list[StNode] {
    q = query.lower().strip();
    scored: list[tuple[int, str, StNode]] = [];
    pool: list[StNode] = list(self.modules.values()) + list(self.symbols.values());
    for nd in pool {
        if isinstance(nd, StImpl) {
            continue;
        }
        if kinds and nd.kind not in kinds {
            continue;
        }
        s = fuzzy_score(q, nd.key.lower(), nd.name.lower());
        if s >= 0 {
            scored.append((s, nd.key, nd));
        }
    }
    scored.sort(
        key=lambda (t: tuple[int, str, StNode]) -> tuple[int, int, str] { (
            -t[0],
            len(t[1]),
            t[1]
        ) }
    );
    return [t[2] for t in scored[:limit]];
}

impl ProjectModel.node_dict(nd: StNode) -> dict[str, any] {
    d: dict[str, any] = {
        "key": nd.key,
        "name": nd.name,
        "kind": nd.kind,
        "file": nd.file,
        "line": nd.line,
        "end_line": nd.end_line
    };
    if isinstance(nd, StArchetype) {
        d["bases"] = nd.bases;
        if nd.kind == "walker" {
            d["traverses"] = [t.key for t in self.traversals(nd.key)];
        }
    } elif isinstance(nd, StAbility) {
        d["signature"] = nd.signature;
        if nd.impl_file {
            d["impl"] = {
                "file": nd.impl_file,
                "line": nd.impl_line,
                "end_line": nd.impl_end_line
            };
        }
    } elif isinstance(nd, StField) {
        d["type"] = nd.type_str;
    } elif isinstance(nd, StModule) {
        d["files"] = nd.files;
        d["archwire"] = nd.archwire;
        if nd.error {
            d["error"] = nd.error;
        }
    }
    if nd.doc {
        d["doc"] = nd.doc;
    }
    return d;
}

impl ProjectModel.module_dict(key: str, deep: bool = True) -> dict[str, any] {
    mod = self.modules[key];
    d = self.node_dict(mod);
    d["providers"] = [w.to_dict() for w in self.providers(key)];
    d["consumers"] = [w.to_dict() for w in self.consumers(key)];
    d["rules"] = [r.name for r in self.rules_for(key)];
    if deep {
        d["symbols"] = [self._tree_dict(k) for k in self.children(key)];
    }
    return d;
}

impl ProjectModel._tree_dict(nd: StNode) -> dict[str, any] {
    d = self.node_dict(nd);
    kids = self.children(nd.key);
    if kids {
        d["children"] = [self._tree_dict(k) for k in kids];
    }
    return d;
}

impl ProjectModel.to_dict(module: str = "") -> dict[str, any] {
    if module {
        if module not in self.modules {
            return {"error": f"no module '{module}'"};
        }
        return self.module_dict(module);
    }
    mods = sorted(self.modules.keys());
    return {
        "root": self.root_dir,
        "archwires": self.archwires,
        "stats": self.stats(),
        "modules": [self.module_dict(k, deep=True) for k in mods],
        "rules": [
            {
                "name": r.name,
                "archwire": r.file,
                "sources": r.sources,
                "targets": r.targets,
                "names": r.names,
                "governs": [m.key for m in [r->:Governs:->]]
            } for r in self.rules
        ]
    };
}

impl ProjectModel.stats -> dict[str, any] {
    counts: dict[str, int] = {};
    for s in self.symbols.values() {
        counts[s.kind] = counts.get(s.kind, 0) + 1;
    }
    return {
        "modules": len(
            [
                m
                for m in self.modules.values()
                if m.kind == "module"
            ]
        ),
        "external": len(
            [
                m
                for m in self.modules.values()
                if m.kind == "external"
            ]
        ),
        "packages": len(self.packages),
        "wires": len(self.wires),
        "rules": len(self.rules),
        "symbols": counts,
        "discover_secs": round(self.build_secs, 3),
        "index_secs": round(self.index_secs, 3),
        "errors": len(
            [
                m
                for m in self.modules.values()
                if m.error
            ]
        )
    };
}

impl fuzzy_score(q: str, key: str, name: str) -> int {
    if not q {
        return 1;
    }
    if name == q {
        return 1000;
    }
    if name.startswith(q) {
        return 800 - len(name);
    }
    if q in name {
        return 600 - len(name);
    }
    if q in key {
        return 400 - len(key);
    }
    pos = 0;
    run = 0;
    score = 0;
    for ch in q {
        idx = key.find(ch, pos);
        if idx < 0 {
            return -1;
        }
        run = run + 1 if idx == pos else 0;
        score += 1 + run;
        pos = idx + 1;
    }
    return score;
}

impl sym_uri(key: str) -> str {
    return SYM_SCHEME + key;
}

impl find_project_root(start: str) -> str {
    cur = os.path.realpath(start);
    while True {
        if os.path.exists(os.path.join(cur, "jac.toml")) {
            return cur;
        }
        parent = os.path.dirname(cur);
        if parent == cur {
            return os.path.realpath(start);
        }
        cur = parent;
    }
}

impl ProjectModel._is_nested_project(arch: str) -> bool {
    cur = os.path.dirname(os.path.realpath(arch));
    while cur.startswith(self.root_dir) and cur != self.root_dir {
        if os.path.exists(os.path.join(cur, "jac.toml")) {
            return True;
        }
        cur = os.path.dirname(cur);
    }
    return False;
}

impl WireBinding.wire_text(consumer: str) -> str {
    words = self.form.split(" ");
    prefix = " ".join(
        [
            w
            for w in words
            if w in ("comptime", "include", "type")
        ]
    );
    if prefix == "type" {
        prefix = "type";
    }
    head = (prefix + " " if prefix else "") + self.provider;
    if "from" in words {
        item = self.name + (" as " + self.alias if self.alias else "");
        return f"{head} --> {consumer} {{ {item} }}";
    }
    alias = " as " + self.alias if self.alias else "";
    return f"{head}{alias} --> {consumer};";
}

impl WiringSpec.postinit -> None {
    self.package_prefix = _package_prefix(self.root_dir);
    for (i, wire) in enumerate(self.wires) {
        wire.index = i;
        self._wire_lines[wire.line] = wire;
        for consumer in wire.consumers {
            held = self._raw.setdefault(consumer, []);
            if not any([w is wire for w in held]) {
                held.append(wire);
            }
        }
    }
    rows: list[str] = [];
    for rule in self.rules {
        srcs = "|".join([p.text for p in rule.sources]);
        tgts = "|".join([p.text for p in rule.targets]);
        names = ",".join(sorted(rule.item_names)) if not rule.is_open else "*";
        rows.append(f"{rule.scope}:{rule.name}:{srcs}-->{tgts}:{names}");
    }
    self._policy_digest = hashlib.sha256("\n".join(rows).encode()).hexdigest()
        if rows
        else "";
}

impl WiringSpec.import_prefix -> str {
    if self._prefix is None {
        self._prefix = import_prefix_for(self.root_dir);
    }
    return self._prefix;
}

impl import_prefix_for(root_dir: str) -> str {
    project = active_host().project_root(root_dir);
    stop = os.path.realpath(project) if project else None;
    chain: list[str] = [];
    top = -1;
    cur = os.path.realpath(root_dir);
    while cur != stop {
        if os.path.isfile(os.path.join(cur, "__init__.jac"))
            or os.path.isfile(os.path.join(cur, "__init__.py")) {
            top = len(chain);
        }
        chain.append(os.path.basename(cur));
        parent = os.path.dirname(cur);
        if parent == cur {
            break;
        }
        cur = parent;
    }
    return ".".join(reversed(chain[:top + 1]));
}

impl WiringSpec.import_name(name: str) -> str {
    prefix = self.import_prefix();
    if prefix and name {
        return prefix + "." + name;
    }
    return prefix or name;
}

impl WiringSpec.module_name(path: str) -> (str | None) {
    local = local_module_name(self.root_dir, path);
    return self.package_prefix + local if local is not None else None;
}

impl local_module_name(root_dir: str, path: str) -> (str | None) {
    try {
        rel = os.path.relpath(os.path.realpath(path), os.path.realpath(root_dir));
    } except ValueError {
        return None;
    }
    if rel.startswith("..") {
        return None;
    }
    stem: str;
    if rel.endswith(".jac") {
        stem = rel[:-4];
    } elif rel.endswith(".py") {
        stem = rel[:-3];
    } else {
        return None;
    }
    parts = stem.split(os.sep);
    if parts and parts[-1] == "__init__" {
        parts = parts[:-1];
    }
    if not parts {
        return None;
    }
    for part in parts {
        if not part.isidentifier() {
            return None;
        }
    }
    return ".".join(parts);
}

impl WiringSpec._local_name(name: str) -> (str | None) {
    if not self.package_prefix {
        return name;
    }
    if not name.startswith(self.package_prefix) {
        return None;
    }
    return name[len(self.package_prefix):];
}

def _package_prefix(root_dir: str) -> str {
    facts = active_host().project_facts(root_dir);
    if facts is None or not facts.package_name {
        return "";
    }
    return facts.package_name.replace("/", ".") + ".";
}

impl WiringSpec.module_file(name: str) -> (str | None) {
    local = self._local_name(name) if name else None;
    if not local {
        return None;
    }
    parts = local.split(".");
    if any([not p for p in parts]) {
        return None;
    }
    found = active_host().resolve_local_module(self.root_dir, parts);
    if found is None or found[1] not in ("jac", "py") or not self.owns(found[0]) {
        return None;
    }
    return found[0];
}

impl WiringSpec.owns(path: str) -> bool {
    top = os.path.realpath(self.root_dir);
    cur = os.path.dirname(os.path.realpath(path));
    if cur != top and not cur.startswith(top + os.sep) {
        return False;
    }
    walked: list[str] = [];
    owned = True;
    while cur != top {
        cached = self._owned_dirs.get(cur);
        if cached is not None {
            owned = cached;
            break;
        }
        walked.append(cur);
        if os.path.isfile(os.path.join(cur, ARCH_FILE_NAME))
            or os.path.isfile(os.path.join(cur, "jac.toml")) {
            owned = False;
            break;
        }
        cur = os.path.dirname(cur);
    }
    for d in walked {
        self._owned_dirs[d] = owned;
    }
    return owned;
}

impl WiringSpec.split_consumer(path: str) -> (tuple[str, list[str]] | None) {
    if path in self._splits {
        return self._splits[path];
    }
    found: (tuple[str, list[str]] | None) = None;
    parts = path.split(".");
    for i in range(len(parts), 0, -1) {
        head = ".".join(parts[:i]);
        if self.module_file(head) is not None {
            found = (head, parts[i:]);
            break;
        }
    }
    self._splits[path] = found;
    return found;
}

impl WiringSpec.consumer_scope(consumer: str, wire: WireRec) -> list[str] {
    self.consumer_wires(consumer);
    return self._scopes.get((consumer, id(wire)), []);
}

impl WiringSpec.wire_at_line(line: int) -> (WireRec | None) {
    return self._wire_lines.get(line);
}

impl WiringSpec.is_package_dir(name: str) -> bool {
    local = self._local_name(name) if name else None;
    if not local {
        return False;
    }
    return os.path.isdir(os.path.join(self.root_dir, local.replace(".", os.sep)));
}

impl WiringSpec.project_modules -> list[str] {
    if self._project_modules is not None {
        return self._project_modules;
    }
    paths: list[str] = [];
    self._scan_modules(self.root_dir, paths, set());
    ignored = set(
        active_host().native_fact(
            HOST_FACT_GIT_IGNORED, os.path.realpath(self.root_dir)
        ).split(
            HOST_FACT_SEP
        )
    );
    found: list[str] = [];
    for path in paths {
        if os.path.realpath(path) in ignored {
            continue;
        }
        name = self.module_name(path);
        if name is not None {
            found.append(name);
        }
    }
    self._project_modules = found;
    return found;
}

impl WiringSpec._scan_modules(
    directory: str, found: list[str], seen: set[str]
) -> None {
    real = os.path.realpath(directory);
    if real in seen {
        return;
    }
    seen.add(real);
    try {
        entries = sorted(os.listdir(directory));
    } except OSError {
        return;
    }
    subdirs: list[str] = [];
    for fname in entries {
        full = os.path.join(directory, fname);
        if os.path.isdir(full) {
            if not fname.startswith(".")
                and fname not in SKIPPED_PROJECT_DIRS
                and not os.path.isfile(os.path.join(full, "jac.toml"))
                and not os.path.isfile(os.path.join(full, ARCH_FILE_NAME)) {
                subdirs.append(full);
            }
        } elif fname.endswith(".jac") {
            found.append(full);
        }
    }
    for sub in subdirs {
        self._scan_modules(sub, found, seen);
    }
}

impl WiringSpec.consumer_wires(consumer: str) -> list[WireRec] {
    held = self._by_consumer.get(consumer);
    if held is not None {
        return held;
    }
    dotted = consumer + ".";
    candidates: dict[int, WireRec] = {};
    for (path, wires) in self._raw.items() {
        if path == consumer or path.startswith(dotted) {
            for wire in wires {
                candidates[wire.index] = wire;
            }
        }
    }
    found: list[WireRec] = [];
    for index in sorted(candidates.keys()) {
        wire = candidates[index];
        for path in wire.consumers {
            if path != consumer and not path.startswith(dotted) {
                continue;
            }
            split = self.split_consumer(path);
            owner = split[0] if split is not None else path;
            if owner == consumer {
                found.append(wire);
                self._scopes[(consumer, id(wire))] = split[1]
                    if split is not None
                    else [];
                break;
            }
        }
    }
    self._by_consumer[consumer] = found;
    return found;
}

impl WiringSpec.is_covered(consumer: str) -> bool {
    return bool(self.consumer_wires(consumer));
}

impl WiringSpec.is_project_module(module: str) -> bool {
    return module in self.project_modules();
}

impl WiringSpec._wire_pieces(wire: WireRec) -> list[tuple[int, int, str]] {
    line0 = wire.line - 1;
    col = wire.col;
    head_form = import_form(wire.is_absorb, wire.is_typed, wire.is_comptime, False);
    if wire.is_module_form {
        text = head_form
            + " "
            + self.import_name(wire.provider)
            + (" as " + wire.alias if wire.alias else "")
            + ";";
        return [(line0, col, text)];
    }
    if not wire.payload {
        return [];
    }
    header = head_form + " from " + self.import_name(wire.provider);
    if wire.lb_line > wire.line {
        header = header + ("\n" * (wire.lb_line - wire.line)) + (" " * wire.lb_col);
    } elif wire.lb_col >= col + len(header) + 1 {
        header = header + (" " * (wire.lb_col - col - len(header)));
    } else {
        header = header + " ";
    }
    out: list[tuple[int, int, str]] = [];
    for (i, line) in enumerate((header + wire.payload).split("\n")) {
        out.append((line0 + i, col if i == 0 else 0, line));
    }
    return out;
}

impl WiringSpec.annex_source(consumer: str) -> (str | None) {
    wires = self.consumer_wires(consumer);
    if not wires {
        return None;
    }
    cached = self._annex_cache.get(consumer);
    if cached is not None {
        return cached;
    }
    placed: dict[int, list[tuple[int, str]]] = {};
    for wire in wires {
        for (line0, col, text) in self._wire_pieces(wire) {
            placed.setdefault(line0, []).append((col, text));
        }
    }
    if not placed {
        return None;
    }
    out: list[str] = [""] * (max(placed.keys()) + 1);
    for (line0, pieces) in placed.items() {
        pieces.sort();
        buf = "";
        for (col, text) in pieces {
            if len(buf) < col {
                buf = buf + (" " * (col - len(buf)));
            } elif buf {
                buf = buf + " ";
            }
            buf = buf + text;
        }
        out[line0] = buf;
    }
    text = "\n".join(out) + "\n";
    self._annex_cache[consumer] = text;
    return text;
}

impl WiringSpec.digest_for(consumer: str) -> str {
    rows: list[str] = [];
    for wire in self.consumer_wires(consumer) {
        scope = ".".join(self.consumer_scope(consumer, wire));
        provider = self.import_name(wire.provider);
        for binding in wire.bindings() {
            rows.append(
                "\x1f".join(
                    [scope, binding.form, provider, binding.name, binding.alias]
                )
            );
        }
    }
    if not rows and not self._policy_digest {
        return "";
    }
    rows.sort();
    return hashlib.sha256(
        (consumer + "\x00" + "\n".join(rows) + "\x00" + self._policy_digest).encode()
    ).hexdigest();
}

impl WireRec.bindings -> list[WireBinding] {
    if self.is_module_form {
        return [
            WireBinding(
                provider=self.provider,
                form=import_form(
                    self.is_absorb, self.is_typed, self.is_comptime, False
                ),
                alias=self.alias
            )
        ];
    }
    form = import_form(self.is_absorb, self.is_typed, self.is_comptime, True);
    return [
        WireBinding(provider=self.provider, form=form, name=name, alias=alias)
        for (name, alias) in self.items
    ];
}

impl WiringSpec.consumer_bindings(
    consumer: str, scope: (list[str] | None) = None
) -> dict[tuple[str, str, str, str], WireRec] {
    want = scope or [];
    out: dict[tuple[str, str, str, str], WireRec] = {};
    for wire in self.consumer_wires(consumer) {
        if self.consumer_scope(consumer, wire) != want {
            continue;
        }
        for binding in wire.bindings() {
            out.setdefault(binding.key(), wire);
        }
    }
    return out;
}

impl WiringSpec.import_provider(path_node: ModulePath) -> (str | None) {
    import from jaclang.compiler.frontend.codeinfo { is_bundled_native_module }
    if path_node.level == 0
        and path_node.string_path_value is None
        and (
            is_stdlib_module(path_node.dot_path_str.split(".")[0])
            or is_bundled_native_module(path_node.dot_path_str)
        ) {
        return None;
    }
    try {
        resolved = path_node.resolve_relative_path();
    } except Exception {
        return None;
    }
    if not resolved or not os.path.isfile(resolved) {
        return None;
    }
    module = self.module_name(resolved) if self.owns(resolved) else None;
    if module is None
        or path_node.level != 0
        or path_node.string_path_value is not None {
        return module;
    }
    if path_node.dot_path_str == self.import_name(module)
        or path_node.in_client_context()
        or path_node.in_native_context() {
        return module;
    }
    return None;
}

impl WiringSpec.rules_for_provider(provider: str) -> list[RuleRec] {
    return [
        rule
        for rule in self.rules
        if any([p.matches(provider, rule.scope) for p in rule.sources])
    ];
}

impl WiringSpec.rules_admitting(provider: str, consumer: str) -> list[RuleRec] {
    return [
        rule
        for rule in self.rules_for_provider(provider)
        if any([t.matches(consumer) for t in rule.targets])
    ];
}

impl WiringSpec.admitted_names(rules: list[RuleRec]) -> (set[str] | None) {
    payload_rules = [
        r
        for r in rules
        if not r.is_open
    ];
    if not payload_rules {
        return None;
    }
    names: set[str] = set();
    for rule in payload_rules {
        names |= rule.item_names;
    }
    return names;
}

impl PatternRec.matches(module: str, prefix: str = "") -> bool {
    base = ModulePattern.join_scope(prefix, self.dotted);
    if self.is_glob {
        return (not base) or module == base or module.startswith(base + ".");
    }
    return module == base;
}

impl pattern_text(pattern: ModulePattern) -> str {
    if pattern.path is None {
        return "*";
    }
    return pattern.dotted + (".*" if pattern.is_glob else "");
}

impl pattern_record(pattern: ModulePattern) -> PatternRec {
    return PatternRec(
        dotted=pattern.dotted, is_glob=pattern.is_glob, text=pattern_text(pattern)
    );
}

impl rule_record(rule: ImportRule) -> RuleRec {
    return RuleRec(
        name=rule.name.value,
        scope=rule.block.scope_prefix,
        sources=[pattern_record(p) for p in rule.sources],
        targets=[pattern_record(p) for p in rule.targets],
        item_names=set(rule.item_names),
        is_open=rule.is_open
    );
}

impl wire_record(wire: ImportWire, source: str = "") -> WireRec {
    alias = wire.provider.alias if wire.is_module_form else None;
    first = wire.loc.first_tok;
    rec = WireRec(
        provider=wire.provider_path,
        consumers=list(wire.consumer_paths),
        is_module_form=wire.is_module_form,
        is_absorb=wire.is_absorb,
        is_typed=wire.is_typed,
        is_comptime=wire.is_comptime,
        alias=alias.value if alias is not None else "",
        items=[]
            if wire.is_module_form
            else [
                (item.name.value, item.alias.value if item.alias is not None else "")
                for item in wire.items
            ],
        line=first.line_no
    );
    if not source {
        return rec;
    }
    rec.col = first.pos_start - (source.rfind("\n", 0, first.pos_start) + 1);
    if wire.is_module_form {
        return rec;
    }
    lbrace: (Token | None) = None;
    rbrace: (Token | None) = None;
    for k in [wire->:Kid:->] {
        if isinstance(k, Token) {
            if k.name == Tok.LBRACE and lbrace is None {
                lbrace = k;
            } elif k.name == Tok.RBRACE {
                rbrace = k;
            }
        }
    }
    if lbrace is None or rbrace is None {
        return rec;
    }
    rec.lb_line = lbrace.line_no;
    rec.lb_col = lbrace.pos_start - (source.rfind("\n", 0, lbrace.pos_start) + 1);
    rec.payload = source[lbrace.pos_start:rbrace.pos_end];
    return rec;
}

impl parse_records(
    source: str, path: str
) -> tuple[bool, list[WireRec], list[RuleRec]] {
    import from jaclang.compiler.frontend.parser.frontend { parse_woven }
    (mod, had_error) = parse_woven(source, path, None, [], load_kernel=False);
    wires: list[WireRec] = [];
    rules: list[RuleRec] = [];
    for stmt in mod.body {
        if not isinstance(stmt, GraphImport) {
            continue;
        }
        for item in stmt.body {
            if isinstance(item, ImportWire) {
                wires.append(wire_record(item, source));
            } elif isinstance(item, ImportRule) {
                rules.append(rule_record(item));
            }
        }
    }
    return (bool(had_error), wires, rules);
}

impl _split_list(text: str) -> list[str] {
    if not text {
        return [];
    }
    return text.split("\x1e");
}

impl _encode_patterns(patterns: list[PatternRec]) -> str {
    return "\x1e".join(
        [
            p.dotted + "\x1d" + ("1" if p.is_glob else "0") + "\x1d" + p.text
            for p in patterns
        ]
    );
}

impl _decode_patterns(text: str) -> (list[PatternRec] | None) {
    out: list[PatternRec] = [];
    for part in _split_list(text) {
        bits = part.split("\x1d");
        if len(bits) != 3 {
            return None;
        }
        out.append(PatternRec(dotted=bits[0], is_glob=bits[1] == "1", text=bits[2]));
    }
    return out;
}

impl encode_records(
    parse_failed: bool, wires: list[WireRec], rules: list[RuleRec]
) -> str {
    lines: list[str] = [
        "jacwire\x1f" + str(RECORDS_FORMAT) + "\x1f" + ("1" if parse_failed else "0")
    ];
    for w in wires {
        flags = ("1" if w.is_module_form else "0")
            + ("1" if w.is_absorb else "0")
            + ("1" if w.is_typed else "0")
            + ("1" if w.is_comptime else "0");
        items = "\x1e".join([name + "\x1d" + alias for (name, alias) in w.items]);
        lines.append(
            "\x1f".join(
                [
                    "W",
                    w.provider,
                    "\x1e".join(w.consumers),
                    flags,
                    w.alias,
                    items,
                    str(w.line),
                    str(w.col),
                    str(w.lb_line),
                    str(w.lb_col),
                    w.payload.replace("\n", "\x1c")
                ]
            )
        );
    }
    for r in rules {
        lines.append(
            "\x1f".join(
                [
                    "R",
                    r.name,
                    r.scope,
                    _encode_patterns(r.sources),
                    _encode_patterns(r.targets),
                    "\x1e".join(sorted(r.item_names)),
                    "1" if r.is_open else "0"
                ]
            )
        );
    }
    return "\n".join(lines);
}

impl decode_records(text: str) -> (tuple[bool, list[WireRec], list[RuleRec]] | None) {
    lines = text.split("\n");
    head = lines[0].split("\x1f");
    if len(head) != 3 or head[0] != "jacwire" or head[1] != str(RECORDS_FORMAT) {
        return None;
    }
    wires: list[WireRec] = [];
    rules: list[RuleRec] = [];
    for line in lines[1:] {
        f = line.split("\x1f");
        if f[0] == "W" and len(f) == 11 {
            flags = f[3];
            if len(flags) != 4
                or not (
                    f[6].isdigit()
                    and f[7].isdigit()
                    and f[8].isdigit()
                    and f[9].isdigit()
                ) {
                return None;
            }
            items: list[tuple[str, str]] = [];
            for pair in _split_list(f[5]) {
                bits = pair.split("\x1d");
                if len(bits) != 2 {
                    return None;
                }
                items.append((bits[0], bits[1]));
            }
            wires.append(
                WireRec(
                    provider=f[1],
                    consumers=_split_list(f[2]),
                    is_module_form=flags[0] == "1",
                    is_absorb=flags[1] == "1",
                    is_typed=flags[2] == "1",
                    is_comptime=flags[3] == "1",
                    alias=f[4],
                    items=items,
                    line=int(f[6]),
                    col=int(f[7]),
                    lb_line=int(f[8]),
                    lb_col=int(f[9]),
                    payload=f[10].replace("\x1c", "\n")
                )
            );
        } elif f[0] == "R" and len(f) == 7 {
            sources = _decode_patterns(f[3]);
            targets = _decode_patterns(f[4]);
            if sources is None or targets is None {
                return None;
            }
            rules.append(
                RuleRec(
                    name=f[1],
                    scope=f[2],
                    sources=sources,
                    targets=targets,
                    item_names=set(_split_list(f[5])),
                    is_open=f[6] == "1"
                )
            );
        } else {
            return None;
        }
    }
    return (head[2] == "1", wires, rules);
}

impl is_arch_file(path: str) -> bool {
    return os.path.basename(path) == ARCH_FILE_NAME;
}

impl arch_file_for(path: str) -> (str | None) {
    project = active_host().project_root(path);
    stop = os.path.realpath(project) if project else None;
    real = os.path.realpath(path);
    cur = real if os.path.isdir(real) else os.path.dirname(real);
    while True {
        candidate = os.path.join(cur, ARCH_FILE_NAME);
        if os.path.isfile(candidate) {
            return candidate;
        }
        if stop is not None and cur == stop {
            return None;
        }
        parent = os.path.dirname(cur);
        if parent == cur {
            return None;
        }
        cur = parent;
    }
}

impl compiled_by_seed(path: str) -> bool {
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    host = active_host();
    pkg = os.path.realpath(jaclang_pkg_root());
    base = host.base_file(path);
    real = os.path.realpath(base if base is not None else path);
    if not real.startswith(pkg + os.sep) {
        return False;
    }
    return host.is_seed_source(real[len(pkg) + 1:].replace(os.sep, "/"));
}

impl is_kernel_abi_contract(path: str) -> bool {
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    import from jaclang.compiler.native_scope { KERNEL_ABI_CONTRACT_REL }
    pkg = os.path.realpath(jaclang_pkg_root());
    real = os.path.realpath(path);
    if not real.startswith(pkg + os.sep) {
        return False;
    }
    return real[len(pkg) + 1:].replace(os.sep, "/") in KERNEL_ABI_CONTRACT_REL;
}

impl is_native_stdlib_source(path: str) -> bool {
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    stdlib = os.path.join(os.path.realpath(jaclang_pkg_root()), "runtime", "na_stdlib");
    return os.path.realpath(path).startswith(stdlib + os.sep);
}

impl is_stdlib_module(name: str) -> bool {
    if not _STDLIB_NAMES {
        _STDLIB_NAMES.append(
            set(
                active_host().native_fact(HOST_FACT_STDLIB_MODULES, "").split(
                    HOST_FACT_SEP
                )
            )
        );
    }
    return name in _STDLIB_NAMES[0];
}

impl scope_path_of(nd: UniNode) -> (list[str] | None) {
    names: list[str] = [];
    cur = nd.parent;
    while cur is not None and not isinstance(cur, Module) {
        if isinstance(cur, ImplDef) {
            return [t.sym_name for t in cur.target] + names;
        }
        if isinstance(cur, Ability) {
            if cur.name_ref is None {
                return None;
            }
            names.insert(0, cur.name_ref.sym_name);
        } elif isinstance(cur, (Archetype, Enum)) {
            names.insert(0, cur.name.sym_name);
        }
        cur = cur.parent;
    }
    return names;
}

impl scope_owners(mod: Module) -> dict[str, (Ability | ImplDef)] {
    index: dict[str, (Ability | ImplDef)] = {};
    for impl_node in mod.get_all_sub_nodes(typ=ImplDef) {
        base = scope_path_of(impl_node);
        if base is not None and isinstance(impl_node.body, `list) {
            index.setdefault(
                ".".join([*base, *[t.sym_name for t in impl_node.target]]), impl_node
            );
        }
    }
    for ability in mod.get_all_sub_nodes(typ=Ability) {
        base = scope_path_of(ability);
        if base is not None
            and ability.name_ref is not None
            and isinstance(ability.body, `list) {
            index.setdefault(".".join([*base, ability.name_ref.sym_name]), ability);
        }
    }
    return index;
}

impl inject_into_scope(owner: (Ability | ImplDef), stmt: UniNode) -> None {
    body: list[UniNode] = [owner->:BodyRole:->];
    kids: list[UniNode] = [owner->:Kid:->];
    anchor = -1;
    for i in range(len(kids)) {
        k = kids[i];
        if body and k is body[0] {
            anchor = i;
            break;
        }
        if not body and isinstance(k, Token) and k.name == Tok.RBRACE {
            anchor = i;
        }
    }
    if anchor < 0 {
        return;
    }
    with owner.structure_thawed() {
        owner.set_kids([*kids[:anchor], stmt, *kids[anchor:]], pos_update=False);
        owner._role_set(BodyRole, [stmt, *body]);
    }
    owner._invalidate_sub_node_tab();
}

impl _load_spec(root_dir: str, arch_path: str) -> WiringSpec {
    stamp: tuple[float, int] = (-1.0, -1);
    try {
        stamp = (os.path.getmtime(arch_path), os.path.getsize(arch_path));
    } except OSError {}
    key = os.path.realpath(root_dir);
    cached = _spec_cache.get(key);
    if cached is not None and cached[0] == stamp {
        return cached[1];
    }
    host = active_host();
    source = host.read_source(arch_path);
    digest = hashlib.sha256(source.encode()).hexdigest();
    records: (tuple[bool, list[WireRec], list[RuleRec]] | None) = None;
    held = host.wiring_records(digest);
    if held {
        records = decode_records(held);
    }
    if records is None {
        records = parse_records(source, arch_path);
        host.keep_wiring_records(
            digest, encode_records(records[0], records[1], records[2])
        );
    }
    spec = WiringSpec(
        root_dir=root_dir,
        path=arch_path,
        parse_failed=records[0],
        wires=records[1],
        rules=records[2]
    );
    _spec_cache[key] = (stamp, spec);
    return spec;
}

impl wiring_for_path(path: str) -> (WiringSpec | None) {
    if not path {
        return None;
    }
    arch = arch_file_for(path);
    if arch is None {
        return None;
    }
    root_dir = os.path.dirname(arch);
    scope = _resolution.get();
    if scope is not None and root_dir in scope and scope[root_dir] is not None {
        return scope[root_dir];
    }
    if root_dir in _building {
        return None;
    }
    spec: (WiringSpec | None) = None;
    _building.add(root_dir);
    try {
        spec = _load_spec(root_dir, arch);
    } finally {
        _building.discard(root_dir);
    }
    if scope is not None {
        scope[root_dir] = spec;
    }
    return spec;
}

impl dedupe_generated_imports(mod: Module) -> None {
    spec = wiring_for_path(mod.loc.mod_path);
    if spec is None {
        return;
    }
    consumer = spec.module_name(mod.loc.mod_path) or "";
    consumer_import = spec.import_name(consumer);
    written: set[tuple[str, str, str, str]] = set();
    generated: list[Import] = [];
    removed: set[int] = set();
    owners: (dict[str, (Ability | ImplDef)] | None) = None;
    for stmt in mod.body {
        if not isinstance(stmt, Import) {
            continue;
        }
        if stmt.loc.mod_path == spec.path {
            wire = spec.wire_at_line(stmt.loc.first_line);
            scope = spec.consumer_scope(consumer, wire) if wire is not None else [];
            if scope {
                removed.add(id(stmt));
                if owners is None {
                    owners = scope_owners(mod);
                }
                owner = owners.get(".".join(scope));
                if owner is None {
                    continue;
                }
                in_scope: set[tuple[str, str, str, str]] = set();
                for imp in owner.get_all_sub_nodes(typ=Import) {
                    if scope_path_of(imp) == scope {
                        in_scope |= import_keys(imp);
                    }
                }
                doomed: set[int] = set();
                for (key, item) in import_items(stmt) {
                    if key in in_scope
                        or relative_twin(key, consumer_import) in in_scope {
                        doomed.add(id(item));
                    }
                }
                if not doomed or not stmt.prune_items(doomed) {
                    inject_into_scope(owner, stmt);
                }
                continue;
            }
            generated.append(stmt);
            continue;
        }
        written |= import_keys(stmt);
    }
    for stmt in (generated if written else []) {
        doomed: set[int] = set();
        for (key, item) in import_items(stmt) {
            if key in written or relative_twin(key, consumer_import) in written {
                doomed.add(id(item));
            }
        }
        if doomed and stmt.prune_items(doomed) {
            removed.add(id(stmt));
        }
    }
    hoisted = [
        stmt
        for stmt in generated
        if id(stmt) not in removed
    ];
    if not removed and not hoisted {
        return;
    }
    moved = {id(stmt) for stmt in hoisted} | removed;
    rest = [
        s
        for s in mod.body
        if id(s) not in moved
    ];
    kids = [
        k
        for k in [mod->:Kid:->]
        if id(k) not in moved
    ];
    anchor = len(kids);
    if rest {
        for i in range(len(kids)) {
            if kids[i] is rest[0] {
                anchor = i;
                break;
            }
        }
    }
    mod._role_set(BodyRole, [*hoisted, *rest]);
    mod.set_kids(
        nodes=[*kids[:anchor], *hoisted, *kids[anchor:]] or [EmptyToken()],
        pos_update=False
    );
    mod._invalidate_sub_node_tab();
}

impl wiring_annex_for(file_path: str) -> (WovenAnnex | None) {
    if is_arch_file(file_path) {
        return None;
    }
    spec = wiring_for_path(file_path);
    if spec is None {
        return None;
    }
    consumer = spec.module_name(file_path);
    if consumer is None {
        return None;
    }
    text = spec.annex_source(consumer);
    if not text {
        return None;
    }
    return WovenAnnex(source=text, path=spec.path, consumer=spec.import_name(consumer));
}

impl wiring_digest_for(file_path: str) -> str {
    if is_arch_file(file_path) {
        return "";
    }
    spec = wiring_for_path(file_path);
    if spec is None {
        return "";
    }
    consumer = spec.module_name(file_path);
    if consumer is None {
        return "";
    }
    return spec.digest_for(consumer);
}

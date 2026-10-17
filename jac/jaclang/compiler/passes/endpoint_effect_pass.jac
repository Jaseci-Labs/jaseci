import from jaclang.compiler.frontend.roles { Kid }
import from jaclang.compiler.driver.pipeline_types { PassContract }
import from jaclang.compiler.frontend.unitree {
    Module,
    TreeWalker,
    UniNode,
    Ability,
    Archetype,
    Assignment,
    AstSymbolNode,
    AtomTrailer,
    BinaryExpr,
    BoolExpr,
    ConnectOp,
    DeleteStmt,
    DisconnectOp,
    EventSignature,
    Expr,
    FuncCall,
    KWPair,
    ListVal,
    MultiString,
    ability_of_symbol,
    ImplDef,
    Name,
    SpecialVarRef,
    String,
    Symbol,
    Token,
    UniScopeNode
}
import from jaclang.compiler.passes.context { CompileContext, TreePass }
import from jaclang.compiler.frontend.constant { SymbolType, Tokens as Tok }

def _literal_names(value: (Expr | None)) -> (list[str] | None) {
    if not isinstance(value, ListVal) {
        return None;
    }
    names: list[str] = [];
    for item in value.values {
        text: (str | bytes) = b"";
        if isinstance(item, String) {
            text = item.lit_value;
        } elif isinstance(item, MultiString)
            and all(isinstance(part, String) for part in item.strings) {
            text = item.lit_value;
        }
        if not isinstance(text, str) or not text {
            return None;
        }
        names.append(text);
    }
    return names;
}

obj CallableKey {
    has owner: (UniScopeNode | None) = None,
        key: str = "";
}

def callable_key(sym: Symbol) -> CallableKey {
    import from jaclang.compiler.native_bindings { is_owning_scope }
    parts: list[str] = [sym.sym_name];
    cur: (UniScopeNode | None) = sym.parent_tab;
    while cur is not None and not isinstance(cur, Module) {
        if is_owning_scope(cur) {
            parts.append(cur.scope_name);
        }
        cur = cur.parent_scope;
    }
    parts.reverse();
    return CallableKey(owner=cur, key=".".join(parts));
}

def _summary_strings(value: object) -> list[str] {
    out: list[str] = [];
    if isinstance(value, list) {
        for item in value {
            out.append(str(item));
        }
    }
    return out;
}

walker EndpointEffectPass(TreePass) {
    static has contract: PassContract = PassContract();
    has _is_writer: bool = False,
        _unknown: bool = False,
        _declared_reads: set[str] = set(),
        _declared_writes: set[str] = set(),
        _assumptions: set[str] = set(),
        _touches: set[str] = set(),
        _visited: set[int] = set(),
        _recording: bool = False,
        _summaries: dict[int, dict[str, any]] = {},
        _summarizing: set[int] = set();

    can prepare with entry {
        if self.ctx.nested_depth {
            return;
        }
        self._is_writer = False;
        self._unknown = False;
        self._declared_reads.clear();
        self._declared_writes.clear();
        self._assumptions.clear();
        self._touches.clear();
        self._visited.clear();
    }

    can enter_ability with Ability entry {
        import from jaclang.compiler.frontend.codeinfo { endpoint_key }
        if (
            not here.is_method
            and not here.in_client_context()
            and here.access is not None
            and here.access.tag.name == Tok.KW_PUB
            and isinstance(here.name_ref, Name)
        ) {
            self.module.gen.interop_manifest.endpoint_effects[
                endpoint_key(self.module, "func", here.name_ref.sym_name)
            ] = self._classify(
                self._resolved_body(here), "func", here.name_ref.sym_name, here
            );
        }
    }

    can enter_archetype with Archetype entry {
        import from jaclang.compiler.frontend.codeinfo { endpoint_key }
        if here.arch_kind != "walker" {
            return;
        }
        if not isinstance(here.name, Name) {
            return;
        }
        self.module.gen.interop_manifest.endpoint_effects[
            endpoint_key(self.module, "walker", here.name.sym_name)
        ] = self._classify(self._resolved_body(here), "walker", here.name.sym_name);
    }

    can record_callables with Module exit {
        import from jaclang.compiler.frontend.codeinfo { is_compiler_source_path }
        if self.ctx.nested_depth
            or not here.loc.mod_path.endswith(".jac")
            or is_compiler_source_path(here.loc.mod_path) {
            return;
        }
        self._recording = True;
        self._summaries.clear();
        self._summarizing.clear();
        effects: dict[str, dict[str, any]] = {};
        try {
            for ability in here.get_all_sub_nodes(Ability) {
                if ability.in_client_context()
                    or not isinstance(ability.name_ref, Name) {
                    continue;
                }
                sym = ability.name_ref.sym;
                if sym is None {
                    continue;
                }
                summary = self._summary(ability);
                if summary is not None {
                    effects[callable_key(sym).key] = summary;
                }
            }
        } finally {
            self._recording = False;
            self._summaries.clear();
        }
        here.gen.callable_effects = effects;
    }

    def _summary(ability: Ability) -> (dict[str, any] | None) {
        key = id(ability);
        done = self._summaries.get(key);
        if done is not None or key in self._summarizing {
            return done;
        }
        self._summarizing.add(key);
        was_writer = self._is_writer;
        was_unknown = self._unknown;
        reads = set(self._declared_reads);
        writes = set(self._declared_writes);
        assumptions = set(self._assumptions);
        touches = set(self._touches);
        visited = set(self._visited);
        self._is_writer = False;
        self._unknown = False;
        self._declared_reads.clear();
        self._declared_writes.clear();
        self._assumptions.clear();
        self._touches.clear();
        self._visited.clear();
        declared = self._declaration_effects(ability);
        if declared is not None {
            self._declared_reads.update(declared["reads"]);
            self._declared_writes.update(declared["writes"]);
        } else {
            body = self._resolved_body(ability);
            if not body {
                self._unknown = True;
            }
            for nd in body {
                self._scan(nd);
            }
        }
        summary = {
            "declared": declared is not None,
            "writer": self._is_writer,
            "unknown": self._unknown,
            "touches": sorted(self._touches),
            "reads": sorted(self._declared_reads),
            "writes": sorted(self._declared_writes),
            "assumptions": sorted(self._assumptions)
        };
        self._is_writer = was_writer;
        self._unknown = was_unknown;
        self._declared_reads = reads;
        self._declared_writes = writes;
        self._assumptions = assumptions;
        self._touches = touches;
        self._visited = visited;
        self._summarizing.discard(key);
        self._summaries[key] = summary;
        return summary;
    }

    def _served_effects(call: FuncCall) -> (dict[str, any] | None) {
        import from jaclang.compiler.types.stubcat.reader { CatModule }
        sym = self._call_target_symbol(call);
        if sym is None {
            return None;
        }
        found = callable_key(sym);
        owner = found.owner;
        if not isinstance(owner, CatModule) {
            return None;
        }
        return owner.gen.callable_effects.get(found.key);
    }

    def _apply(summary: dict[str, any], call: FuncCall) {
        if bool(summary.get("declared", False)) {
            import from jaclang.compiler.frontend.unparse { unparse_node }
            self._assumptions.add("Declared effects of " + unparse_node(call.target));
        }
        if bool(summary.get("writer", False)) {
            self._is_writer = True;
        }
        if bool(summary.get("unknown", False)) {
            self._unknown = True;
        }
        for name in _summary_strings(summary.get("touches")) {
            self._touches.add(name);
        }
        for name in _summary_strings(summary.get("reads")) {
            self._declared_reads.add(name);
        }
        for name in _summary_strings(summary.get("writes")) {
            self._declared_writes.add(name);
        }
        for name in _summary_strings(summary.get("assumptions")) {
            self._assumptions.add(name);
        }
    }

    def _classify(
        body_nodes: list[UniNode],
        kind: str,
        name: str,
        declaration: Ability | None = None
    ) -> dict[str, any] {
        import from jaclang.compiler.frontend.codeinfo { endpoint_descriptor }
        self._is_writer = False;
        self._unknown = False;
        self._declared_reads.clear();
        self._declared_writes.clear();
        self._assumptions.clear();
        self._touches.clear();
        self._visited.clear();
        declared = self._declaration_effects(declaration)
            if declaration is not None
            else None;
        if declared is not None {
            self._declared_reads.update(declared["reads"]);
            self._declared_writes.update(declared["writes"]);
            self._assumptions.add("Declared effects of " + name);
        } else {
            for nd in body_nodes {
                self._scan(nd);
            }
        }
        result: dict[str, any] = {};
        for (field, value) in endpoint_descriptor(self.module, kind, name).items() {
            result[field] = value;
        }
        result["reads"] = sorted(list(self._declared_reads))
            if declared is not None
            else ["*"];
        result["writes"] = ["*"]
            if self._is_writer or self._unknown
            else sorted(list(self._declared_writes));
        result["assumptions"] = sorted(list(self._assumptions));
        result["unknown"] = self._unknown;
        result["observed_tags"] = sorted(list(self._touches));
        return result;
    }

    def _scan(nd: (UniNode | None)) -> None {
        if nd is None {
            return;
        }

        if isinstance(nd, BinaryExpr) {
            if isinstance(nd.op, ConnectOp) {
                self._is_writer = True;

                if nd.op.conn_type and isinstance(nd.op.conn_type, Name) {
                    self._touches.add(nd.op.conn_type.sym_name);
                }
            } elif isinstance(nd.op, DisconnectOp) {
                self._is_writer = True;
            } elif isinstance(nd.op, Token) and nd.op.name == Tok.KW_SPAWN {
                self._is_writer = True;
            }
        }

        if isinstance(nd, DeleteStmt) {
            self._is_writer = True;
        }

        if isinstance(nd, Assignment) and nd.target {
            for tgt in nd.target {
                if isinstance(tgt, AtomTrailer) and tgt.is_attr {
                    self._is_writer = True;
                }
            }
        }

        if isinstance(nd, FuncCall) {
            arch_sym = self._call_target_symbol(nd);
            if arch_sym
                and arch_sym.sym_type in [SymbolType.NODE_ARCH, SymbolType.EDGE_ARCH] {
                self._is_writer = True;
                self._touches.add(arch_sym.sym_name);
            }

            if id(nd) not in self._visited {
                self._visited.add(id(nd));
                declared = self._declared_effects(nd);
                if declared is not None {
                    import from jaclang.compiler.frontend.unparse { unparse_node }
                    self._declared_reads.update(declared["reads"]);
                    self._declared_writes.update(declared["writes"]);
                    self._assumptions.add(
                        "Declared effects of " + unparse_node(nd.target)
                    );
                } else {
                    callee = self._callee_ability(nd) if self._recording else None;
                    recorded = self._summary(callee) if callee is not None else None;
                    if recorded is not None {
                        self._apply(recorded, nd);
                    } else {
                        body = self._callee_body(nd);
                        if not body {
                            served = self._served_effects(nd);
                            if served is not None {
                                self._apply(served, nd);
                            } else {
                                self._unknown = True;
                            }
                        }
                        for stmt in body {
                            self._scan(stmt);
                        }
                    }
                }
            }
        }

        if isinstance(nd, EventSignature) and nd.arch_tag_info {
            if isinstance(nd.arch_tag_info, Name) {
                self._touches.add(nd.arch_tag_info.sym_name);
            } elif isinstance(nd.arch_tag_info, BoolExpr) {
                for val in nd.arch_tag_info.values {
                    if isinstance(val, Name) {
                        self._touches.add(val.sym_name);
                    }
                }
            }
        }

        for child in [nd->:Kid:->] {
            if child {
                self._scan(child);
            }
        }
    }

    def _call_target_symbol(call: FuncCall) -> (Symbol | None) {
        if isinstance(call.target, Name) {
            sym = call.target.sym;
            if not sym {
                try {
                    sym = call.target.sym_tab.lookup(call.target.sym_name, deep=True);
                } except ValueError {
                    return None;
                }
            }
            return sym;
        }

        if isinstance(call.target, AtomTrailer) {
            attrs = call.target.as_attr_list;
            if attrs {
                last = attrs[-1];
                if isinstance(last, AstSymbolNode) and last.sym {
                    return last.sym;
                }
            }
        }
        return None;
    }

    def _declared_effects(call: FuncCall) -> dict[str, list[str]] | None {
        decl = ability_of_symbol(self._call_target_symbol(call));
        return self._declaration_effects(decl) if decl is not None else None;
    }

    def _declaration_effects(decl: Ability) -> dict[str, list[str]] | None {
        for decorator in decl.decorators or [] {
            if not isinstance(decorator, FuncCall) {
                continue;
            }
            target = ability_of_symbol(self._call_target_symbol(decorator));
            if target is None
                or not target.loc.mod_path.replace("\\", "/").endswith(
                    "/jaclang/lib/effects.jac"
                ) {
                continue;
            }
            result: dict[str, list[str]] = {"reads": [], "writes": []};
            for pair in decorator.params or [] {
                if not isinstance(pair, KWPair)
                    or pair.key is None
                    or pair.key.sym_name not in result {
                    raise ValueError(
                        "Effect declarations require reads= and writes= literal lists"
                    );
                }
                values = _literal_names(pair.value);
                if values is None {
                    raise ValueError(
                        "Effect dependencies must be literal nonempty strings"
                    );
                }
                result[pair.key.sym_name] = values;
            }
            return result;
        }
        return None;
    }

    def _callee_ability(call: FuncCall) -> (Ability | None) {
        sym = self._call_target_symbol(call);
        if not sym or not sym.defn {
            return None;
        }
        defn_node = sym.defn[0];
        if isinstance(defn_node, Ability) {
            return defn_node;
        }
        if defn_node.parent and isinstance(defn_node.parent, Ability) {
            return defn_node.parent;
        }
        return None;
    }

    def _callee_body(call: FuncCall) -> list[UniNode] {
        ability = self._callee_ability(call);
        return self._resolved_body(ability) if ability is not None else [];
    }

    def _resolved_body(owner: UniNode) -> list[UniNode] {
        if isinstance(owner, Archetype) {
            return owner._get_impl_resolved_body();
        }
        if not isinstance(owner, Ability) {
            return [];
        }
        body = owner.body;
        if isinstance(body, list) {
            return body;
        }
        out: list[UniNode] = [];
        if isinstance(body, ImplDef) and isinstance(body.body, list) {
            for stmt in body.body {
                out.append(stmt);
            }
        }
        return out;
    }
}

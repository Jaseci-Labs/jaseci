"""Lexically scoped name tables for native lowering. A scope reads through to its
parent, binds into itself, and leaving it drops everything it bound, so a
function body or an instantiation sees the names of the scopes around it
without copying them. The outermost scope may also draw on a source, which
produces a name's value the first time it is read."""
obj SymbolSource[V] {
    def provides(name: str) -> bool abst;
    def resolve(name: str) -> (V | None) abst;
}

obj SymbolScope[V] {
    has names: dict[str, V] = {},
        parent: (SymbolScope[V] | None) = None,
        source: (SymbolSource[V] | None) = None;

    def get(name: str) -> (V | None) {
        scope: (SymbolScope[V] | None) = self;
        outermost: SymbolScope[V] = self;
        while scope is not None {
            found = scope.names.get(name);
            if found is not None {
                return found;
            }
            outermost = scope;
            scope = scope.parent;
        }
        if outermost.source is not None {
            return outermost.source.resolve(name);
        }
        return None;
    }

    def contains(name: str) -> bool {
        scope: (SymbolScope[V] | None) = self;
        outermost: SymbolScope[V] = self;
        while scope is not None {
            if name in scope.names {
                return True;
            }
            outermost = scope;
            scope = scope.parent;
        }
        return outermost.source is not None and outermost.source.provides(name);
    }

    def set(name: str, value: V) {
        self.names[name] = value;
    }

    def drop(name: str) {
        self.names.pop(name, None);
    }

    def child -> SymbolScope[V] {
        return SymbolScope(parent=self);
    }

    def outermost -> SymbolScope[V] {
        scope: SymbolScope[V] = self;
        while scope.parent is not None {
            scope = scope.parent;
        }
        return scope;
    }

    def entries -> list[tuple[str, V]] {
        chain: list[SymbolScope[V]] = [];
        scope: (SymbolScope[V] | None) = self;
        while scope is not None {
            chain.append(scope);
            scope = scope.parent;
        }
        merged: dict[str, V] = {};
        for outer in reversed(chain) {
            merged.update(outer.names);
        }
        return list(merged.items());
    }
}

"""Lexically scoped name tables for native lowering. A scope reads through to its
parent, binds into itself, and leaving it drops everything it bound, so a
function body or an instantiation sees the names of the scopes around it
without copying them."""
obj SymbolScope[V] {
    has names: dict[str, V] = {},
        parent: (SymbolScope[V] | None) = None;

    def get(name: str) -> (V | None) {
        scope: (SymbolScope[V] | None) = self;
        while scope is not None {
            found = scope.names.get(name);
            if found is not None {
                return found;
            }
            scope = scope.parent;
        }
        return None;
    }

    def contains(name: str) -> bool {
        return self.get(name) is not None;
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

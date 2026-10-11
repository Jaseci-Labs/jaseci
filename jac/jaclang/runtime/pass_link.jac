import types;

class GlobalCell {
    static has __slots__: tuple[str, ...] = ("namespace", "name");
    has namespace: dict[str, object],
        name: str;

    def init(self: GlobalCell, namespace: dict[str, object], name: str) {
        self.namespace = namespace;
        self.name = name;
    }

    has cell_contents: object {
        getter {
            if self.name not in self.namespace {
                raise NameError(f"name '{self.name}' is not defined");
            }
            return self.namespace[self.name];
        }
        setter(self: GlobalCell, value: object) {
            self.namespace[self.name] = value;
        }
        deleter {
            del self.namespace[self.name];
        }
    }
}

class PassLink {
    static has __slots__: tuple[str, ...] = ("cell", );
    has cell: (types.CellType | GlobalCell);

    def init(self: PassLink, cell: (types.CellType | GlobalCell)) {
        self.cell = cell;
    }

    static def of_local(probe: types.FunctionType) -> PassLink {
        closure = probe.__closure__;
        assert closure , "a pass link probe reads exactly one enclosing local";
        return PassLink(closure[0]);
    }

    static def of_global(namespace: dict[str, object], name: str) -> PassLink {
        return PassLink(GlobalCell(namespace, name));
    }

    def put(self: PassLink, value: object) -> object {
        self.cell.cell_contents = value;
        return value;
    }

    def detach(self: PassLink) -> None {
        try {
            value = self.cell.cell_contents;
        } except (ValueError, NameError) {
            self.cell = types.CellType();
            return;
        }
        self.cell = types.CellType(value);
    }
}

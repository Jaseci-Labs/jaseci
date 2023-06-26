"""Jac Symbol Table."""
from typing import Optional

import jaclang.jac.absyntree as ast
from jaclang.jac.passes.ir_pass import Pass


class Symbol:
    """Symbol."""

    def __init__(self, typ: type, def_line: int, access: Optional[str] = None) -> None:
        """Initialize."""
        self.typ = typ
        self.def_line = def_line
        self.access = access


class SymbolTable:
    """Symbol Table."""

    def __init__(
        self,
        ir_pass: Pass,
        scope_name: str = "",
        parent: Optional["SymbolTable"] = None,
    ) -> None:
        """Initialize."""
        self._pass = ir_pass
        self.parent = parent
        self.tab: dict[str, Symbol] = {}

    def define_var(
        self, name: ast.Name, typ: type, access: Optional[str] = None
    ) -> None:
        """Create a variable."""
        var_name = name.value
        if (
            var_name in self.tab
            and self.tab[var_name].typ
            and not isinstance(typ, self.tab[var_name].typ)
        ):
            self._pass.log_error(
                f"Variable {var_name} already defined on line "
                f"{self.tab[var_name].def_line} as {self.tab[var_name].typ} "
                f"but now being defined as {typ} on line {name.line}"
            )
            return
        self.tab[var_name] = Symbol(
            typ=typ, def_line=self.tab[var_name].def_line, access=None
        )

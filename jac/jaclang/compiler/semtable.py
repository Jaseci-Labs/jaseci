"""Registry Utilities.

This module contains classes and functions for managing the registry of
semantic information.
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import jaclang.compiler.absyntree as ast


class SemInfo:
    """Semantic information class."""

    def __init__(
        self,
        node: ast.AstNode,
        name: str,
        type_str: Optional[str] = None,
        semstr: str = "",
    ) -> None:
        """Initialize the class."""
        self.node_type = type(node)
        self.name = name
        self.type = type_str
        self.semstr = semstr

    def __repr__(self) -> str:
        """Return the string representation of the class."""
        return f"{self.semstr} ({self.type}) ({self.name})"

    def get_children(
        self, sem_registry: SemRegistry, filter: Optional[type[ast.AstNode]] = None
    ) -> list[SemInfo]:
        """Get the children of the SemInfo."""
        scope, _ = sem_registry.lookup(name=self.name)
        self_scope = str(scope) + f".{self.name}({self.type})"
        _, children = sem_registry.lookup(scope=SemScope.get_scope_from_str(self_scope))
        if filter and children and isinstance(children, list):
            return [i for i in children if i.node_type == filter]
        return children if children and isinstance(children, list) else []


class SemScope:
    """Scope class."""

    def __init__(
        self, scope: str, type: str, parent: Optional[SemScope] = None
    ) -> None:
        """Initialize the class."""
        self.parent = parent
        self.type = type
        self.scope = scope

    def __str__(self) -> str:
        """Return the string representation of the class."""
        if self.parent:
            return f"{self.parent}.{self.scope}({self.type})"
        else:
            return f"{self.scope}({self.type})"

    def __repr__(self) -> str:
        """Return the string representation of the class."""
        return self.__str__()

    @staticmethod
    def get_scope_from_str(scope_str: str) -> Optional[SemScope]:
        """Get scope from string."""
        scope_list = scope_str.split(".")
        parent = None
        for scope in scope_list:
            scope_name, scope_type = scope.split("(")
            scope_type = scope_type[:-1]
            parent = SemScope(scope_name, scope_type, parent)
        return parent

    @property
    def as_type_str(self) -> Optional[str]:
        """Return the type string representation of the SemScope."""
        if self.type not in ["class", "node", "obj"]:
            return None
        type_str = self.scope
        node = self.parent
        while node and node.parent:
            if node.type not in ["class", "node", "obj"]:
                return type_str
            type_str = f"{node.scope}.{type_str}"
            node = node.parent
        return type_str


class SemRegistry:
    """Registry class."""

    def __init__(self) -> None:
        """Initialize the class."""
        self.registry: dict[SemScope, list[SemInfo]] = {}

    def add(self, scope: SemScope, seminfo: SemInfo) -> None:
        """Add semantic information to the registry."""
        for k in self.registry.keys():
            if str(k) == str(scope):
                scope = k
                break
        else:
            self.registry[scope] = []
        self.registry[scope].append(seminfo)

    def lookup(
        self,
        scope: Optional[SemScope] = None,
        name: Optional[str] = None,
        type: Optional[str] = None,
    ) -> tuple[Optional[SemScope], Optional[SemInfo | list[SemInfo]]]:
        """Lookup semantic information in the registry."""
        if scope:
            for k, v in self.registry.items():
                if str(k) == str(scope):
                    if name:
                        for i in v:
                            if i.name == name:
                                return k, i
                    elif type:
                        for i in v:
                            if i.type == type:
                                return k, i
                    else:
                        return k, v
        else:
            for k, v in self.registry.items():
                if name:
                    for i in v:
                        if i.name == name:
                            return k, i
                elif type:
                    for i in v:
                        if i.type == type:
                            return k, i
        return None, None

    @property
    def module_scope(self) -> SemScope:
        """Get the module scope."""
        for i in self.registry.keys():
            if not i.parent:
                break
        return i

    def pp(self) -> str:
        """Pretty print the registry."""
        ret_str = ""
        for k, v in self.registry.items():
            ret_str += f"{k}\n"
            for i in v:
                ret_str += f"  {i.name} {i.type} {i.semstr}\n"
        return ret_str

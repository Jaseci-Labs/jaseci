"""Registry Utilities.

This module contains classes and functions for managing the registry of
semantic information.
"""

from __future__ import annotations

from typing import Optional


class SemInfo:
    """Semantic information class."""

    def __init__(
        self, name: str, type: Optional[str] = None, semstr: Optional[str] = None
    ) -> None:
        """Initialize the class."""
        self.name = name
        self.type = type
        self.semstr = semstr

    def __repr__(self) -> str:
        """Return the string representation of the class."""
        return f"{self.semstr} ({self.type}) ({self.name})"


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
        """Return the type string representation of the SemsScope."""
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

    def pp(self) -> None:
        """Pretty print the registry."""
        for k, v in self.registry.items():
            print(k)
            for i in v:
                print(f"  {i.name} {i.type} {i.semstr}")

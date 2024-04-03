"""Registry Utilities.

This module contains classes and functions for managing the registry of
semantic information.
"""

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


class Scope:
    """Scope class."""

    def __init__(self, scope: str, type: str, parent: Optional["Scope"] = None) -> None:
        """Initialize the class."""
        self.parent = parent
        self.type = type
        self.scope = scope

    def __str__(self) -> str:
        """Return the string representation of the class."""
        if self.parent:
            return f"{self.parent}.{self.scope}({self.type})"
        return f"{self.scope}({self.type})"


class Registry:
    """Registry class."""

    def __init__(self) -> None:
        """Initialize the class."""
        self.registry: dict[Scope, list[SemInfo]] = {}

    def add(self, scope: Scope, seminfo: SemInfo) -> None:
        """Add semantic information to the registry."""
        for k in self.registry.keys():
            if str(k) == str(scope):
                scope = k
                break
        else:
            self.registry[scope] = []
        self.registry[scope].append(seminfo)

    def pp(self) -> None:
        """Pretty print the registry."""
        for k, v in self.registry.items():
            print(k)
            for i in v:
                print(f"  {i.name} {i.type} {i.semstr}")

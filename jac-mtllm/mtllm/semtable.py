"""Registry Utilities.

This module contains classes and functions for managing the registry of
semantic information.
"""

from __future__ import annotations

from typing import Optional

import jaclang.compiler.unitree as uni


class SemInfo:
    """Semantic information class."""

    def __init__(
        self,
        node: uni.UniNode,
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
        self, sem_registry: SemRegistry, filter: Optional[type[uni.UniNode]] = None
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

    def __init__(self, program_head: uni.ProgramModule, by_scope: SemScope) -> None:
        """Initialize the class."""
        self.program_head: uni.ProgramModule = program_head
        self.by_scope: SemScope = by_scope

    def lookup(
        self,
        scope: Optional[SemScope] = None,
        name: Optional[str] = None,
        _type: Optional[str] = None,
    ) -> tuple[Optional[SemScope], Optional[SemInfo | list[SemInfo]]]:
        """Lookup semantic information in the registry."""
        mods = self.program_head.hub
        #find the relavent symbol table
        # for mod_name, m in mods.items():
        #     if mod_name in str(self.by_scope) :
        #         mod = m
        #         break
        # symbol_table = mod.find_scope(self.by_scope.scope).get_parent()
        # print(f"SymbolTable: {symbol_table}")
        mod = mods[list(mods.keys())[0]]
        if not mod:
            raise ValueError("Module not found in the registry.")
        scope_obj = mod.find_scope(self.by_scope.scope)
        if not scope_obj:
            raise ValueError("Scope not found in the registry.")
        symbol_table = scope_obj.get_parent()
        # print(f"SymbolTable: {symbol_table}")

        if scope:
            print(f"Looking up scope: {scope}")
            symbol = symbol_table.lookup(scope.scope) if symbol_table else None
            # print(f"Symbol: {symbol}")
        else:
            if name:
                print(f"Looking up name: {name}")
                symbol = symbol_table.lookup(name) if symbol_table else None
            # else: not sure how to fetch only using the type of a symbol needs more digging of this use

        node = symbol.parent_tab if symbol else None
        print(f"Node: {node}")
        sem_info = []
        if isinstance(node, uni.UniNode):
            # print(f"Symbol: {symbol}")
            sem_scope = get_sem_scope(node)
            # print(f"Symbol: {symbol.get_type()}")
            # print(f"Symbol List: {node.names_in_scope}")
            for k, v in node.names_in_scope.items():
                sem_info.append(
                    SemInfo(
                        v.parent_tab,
                        v.sym_name,
                        str(v.parent_tab.get_type()), # this should report the expected type of the symbol (int, str ...)
                        "",
                    )
                )
        else:
            raise ValueError("Node not found in the registry.")

        print(f"SemInfo: {sem_info}")
        print(f"SemScope: {sem_scope}")

        # previous code
        # if scope:
        #     for k, v in self.registry.items():
        #         if str(k) == str(scope):
        #             if name:
        #                 for i in v:
        #                     if i.name == name:
        #                         return k, i
        #             elif type:
        #                 for i in v:
        #                     if i.type == type:
        #                         return k, i
        #             else:
        #                 return k, v
        # else:
        #     for k, v in self.registry.items():
        #         if name:
        #             for i in v:
        #                 if i.name == name:
        #                     return k, i
        #         elif type:
        #             for i in v:
        #                 if i.type == type:
        #                     return k, i
        return sem_scope, sem_info

    # @property
    # def module_scope(self) -> SemScope:
    #     """Get the module scope."""
    #     for i in self.registry.keys():
    #         if not i.parent:
    #             break
    #     return i

    # def pp(self) -> str:
    #     """Pretty print the registry."""
    #     ret_str = ""
    #     for k, v in self.registry.items():
    #         ret_str += f"{k}\n"
    #         for i in v:
    #             ret_str += f"  {i.name} {i.type} {i.semstr}\n"
    #     return ret_str

def get_sem_scope(node: uni.UniNode) -> SemScope:
    """Get scope of the node."""
    a = (
        node.name
        if isinstance(node, uni.Module)
        else (
            node.name.value
            if isinstance(node, (uni.Enum, uni.Archetype))
            else node.name_ref.sym_name if isinstance(node, uni.Ability) else ""
        )
    )
    if isinstance(node, uni.Module):
        return SemScope(a, "Module", None)
    elif isinstance(node, (uni.Enum, uni.Archetype, uni.Ability)):
        node_type = (
            node.__class__.__name__
            if isinstance(node, uni.Enum)
            else ("Ability" if isinstance(node, uni.Ability) else node.arch_type.value)
        )
        if node.parent:
            return SemScope(
                a,
                node_type,
                get_sem_scope(node.parent),
            )
    else:
        if node.parent:
            return get_sem_scope(node.parent)
    return SemScope("", "", None)
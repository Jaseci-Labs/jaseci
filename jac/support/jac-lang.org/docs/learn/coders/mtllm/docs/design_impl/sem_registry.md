<!-- Designed and Implemented by Chandra Irugalbandara -->

# SemRegistry, SemInfo, and SemScope

## Overview

The semantic registry system in the MTLLM framework consists of three main classes: `SemInfo`, `SemScope`, and `SemRegistry`. These classes work together to provide a structured way of storing and retrieving semantic information about various elements in a program. This document outlines the design and implementation details of each class.

> :Mermaid
>
> sequenceDiagram
>     participant C as Compiler
>     participant R as SemRegistry
>     participant S as SemScope
>     participant I as SemInfo
>     participant F as File System
>     C->>R: Initialize SemRegistry
>     loop For each AST node
>         C->>R: Get or Create SemScope
>         R->>S: Create if not exists
>         C->>I: Create SemInfo
>         C->>S: Add SemInfo to SemScope
>         S->>I: Store SemInfo
>     end
>     C->>R: Finalize Registry
>     R->>F: Save to Pickle File

## SemInfo

### Design

`SemInfo` is designed to encapsulate semantic information for individual elements in a program. It stores three key pieces of information:

1. `name`: The identifier of the element
2. `type`: The type of the element (optional)
3. `semstr`: A semantic string describing the element

### Implementation

```python
class SemInfo:
    def __init__(self, name: str, type: Optional[str] = None, semstr: str = "") -> None:
        self.name = name
        self.type = type
        self.semstr = semstr

    def __repr__(self) -> str:
        return f"{self.semstr} ({self.type}) ({self.name})"
```

#### Key Features:
- Simple initialization with optional `type` and `semstr`
- String representation includes all three attributes for easy debugging and display

## SemScope

### Design

`SemScope` represents a scope in the program, which can be nested. It includes:

1. `scope`: The name of the scope
2. `type`: The type of the scope (e.g., "class", "function")
3. `parent`: A reference to the parent scope (optional)

Additional features include:
- String representation that shows the full scope hierarchy
- Static method to create a `SemScope` from a string representation
- Property to get the scope as a type string

### Implementation

```python
class SemScope:
    def __init__(self, scope: str, type: str, parent: Optional[SemScope] = None) -> None:
        self.parent = parent
        self.type = type
        self.scope = scope

    def __str__(self) -> str:
        if self.parent:
            return f"{self.parent}.{self.scope}({self.type})"
        return f"{self.scope}({self.type})"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def get_scope_from_str(scope_str: str) -> Optional[SemScope]:
        scope_list = scope_str.split(".")
        parent = None
        for scope in scope_list:
            scope_name, scope_type = scope.split("(")
            scope_type = scope_type[:-1]
            parent = SemScope(scope_name, scope_type, parent)
        return parent

    @property
    def as_type_str(self) -> Optional[str]:
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
```

#### Key Features:
- Nested structure representation through the `parent` attribute
- String representation shows the full scope hierarchy
- `get_scope_from_str` allows reconstruction of a `SemScope` hierarchy from a string
- `as_type_str` property provides a string representation of the scope as a type, useful for type checking and inference

## SemRegistry

### Design

`SemRegistry` serves as the main container and manager for semantic information. It stores `SemInfo` objects organized by `SemScope`. Key features include:

1. Storage of semantic information in a nested dictionary structure
2. Methods for adding new semantic information
3. Flexible lookup functionality
4. Utility methods for accessing and displaying the registry contents

### Implementation

```python
class SemRegistry:
    def __init__(self) -> None:
        self.registry: dict[SemScope, list[SemInfo]] = {}

    def add(self, scope: SemScope, seminfo: SemInfo) -> None:
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
        for i in self.registry.keys():
            if not i.parent:
                break
        return i

    def pp(self) -> None:
        for k, v in self.registry.items():
            print(k)
            for i in v:
                print(f"  {i.name} {i.type} {i.semstr}")
```

#### Key Features:
- Efficient storage using a dictionary with `SemScope` as keys and lists of `SemInfo` as values
- `add` method handles the case of existing scopes and adds new `SemInfo` objects to the appropriate list
- Flexible `lookup` method allows searching by scope, name, or type, with various combinations
- `module_scope` property provides quick access to the top-level scope
- `pp` (pretty print) method for easy debugging and inspection of the registry contents

## Usage and Interaction

These classes work together to provide a comprehensive system for managing semantic information:

1. `SemInfo` objects are created to represent individual program elements.
2. `SemScope` objects are created to represent the hierarchical structure of the program.
3. `SemRegistry` is used to store and organize `SemInfo` objects within their respective `SemScope`s.
4. The `lookup` method of `SemRegistry` allows for flexible querying of semantic information based on various criteria.

This system enables efficient storage and retrieval of semantic information, which is crucial for the MTLLM framework's ability to understand and reason about program structure and meaning during compilation and inference processes.

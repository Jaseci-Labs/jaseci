"""Standalone test for a type system implementation."""

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union


class TypeCategory(Enum):
    """Categories of types."""

    UNBOUND = "UNBOUND"
    UNKNOWN = "UNKNOWN"
    ANY = "ANY"
    NEVER = "NEVER"
    FUNCTION = "FUNCTION"
    CLASS = "CLASS"
    MODULE = "MODULE"
    UNION = "UNION"
    TYPE_VAR = "TYPE_VAR"


class TypeFlags(Enum):
    """Flags that can be applied to types."""

    NONE = 0
    INSTANTIABLE = 1 << 0  # Type can be instantiated
    INSTANCE = 1 << 1  # Type is an instance
    AMBIGUOUS = 1 << 2  # Type is ambiguous (could be inferred differently)


class Type:
    """Base class for all types."""

    def __init__(self, category: TypeCategory, flags: int = TypeFlags.NONE.value):
        """Initialize a type with a category and flags."""
        self.category = category
        self.flags = flags

    def __str__(self) -> str:
        """Return a string representation of the type."""
        return f"{self.category.value}"

    def __eq__(self, other: object) -> bool:
        """Check if two types are equal."""
        if not isinstance(other, Type):
            return False
        return self.category == other.category and self.flags == other.flags


class UnboundType(Type):
    """Represents a name that is not bound to a value of any type."""

    def __init__(self):
        """Initialize an unbound type."""
        super().__init__(TypeCategory.UNBOUND)

    def __str__(self) -> str:
        """Return a string representation of the type."""
        return "Unbound"


class UnknownType(Type):
    """Represents an implicit Any type."""

    def __init__(self):
        """Initialize an unknown type."""
        super().__init__(TypeCategory.UNKNOWN)

    def __str__(self) -> str:
        """Return a string representation of the type."""
        return "Unknown"


class AnyType(Type):
    """Represents a type that can be anything."""

    def __init__(self):
        """Initialize an Any type."""
        super().__init__(TypeCategory.ANY)

    def __str__(self) -> str:
        """Return a string representation of the type."""
        return "Any"


class NeverType(Type):
    """Represents the bottom type, equivalent to an empty union."""

    def __init__(self):
        """Initialize a Never type."""
        super().__init__(TypeCategory.NEVER)

    def __str__(self) -> str:
        """Return a string representation of the type."""
        return "Never"


class FunctionType(Type):
    """Represents a callable type."""

    def __init__(
        self,
        param_types: List[Type],
        return_type: Type,
        is_method: bool = False,
        param_names: Optional[List[str]] = None,
    ):
        """Initialize a function type."""
        super().__init__(TypeCategory.FUNCTION)
        self.param_types = param_types
        self.return_type = return_type
        self.is_method = is_method
        self.param_names = param_names or [""] * len(param_types)

    def __str__(self) -> str:
        """Return a string representation of the type."""
        params = ", ".join(
            f"{name}: {param}" if name else str(param)
            for name, param in zip(self.param_names, self.param_types)
        )
        return f"({params}) -> {self.return_type}"

    def __eq__(self, other: object) -> bool:
        """Check if two function types are equal."""
        if not isinstance(other, FunctionType):
            return False
        if len(self.param_types) != len(other.param_types):
            return False
        if self.return_type != other.return_type:
            return False
        if self.is_method != other.is_method:
            return False
        for i in range(len(self.param_types)):
            if self.param_types[i] != other.param_types[i]:
                return False
        return True


class ClassType(Type):
    """Represents a class definition."""

    def __init__(
        self,
        name: str,
        fullname: str,
        base_types: Optional[List[Type]] = None,
        is_instantiated: bool = False,
    ):
        """Initialize a class type."""
        flags = TypeFlags.INSTANTIABLE.value
        if is_instantiated:
            flags |= TypeFlags.INSTANCE.value
        super().__init__(TypeCategory.CLASS, flags)
        self.name = name
        self.fullname = fullname
        self.base_types = base_types or []
        self.members: Dict[str, Symbol] = {}

    def __str__(self) -> str:
        """Return a string representation of the type."""
        return self.fullname

    def __eq__(self, other: object) -> bool:
        """Check if two class types are equal."""
        if not isinstance(other, ClassType):
            return False
        return (
            self.category == other.category
            and self.flags == other.flags
            and self.fullname == other.fullname
        )


class ModuleType(Type):
    """Represents a module instance."""

    def __init__(self, name: str, fullname: str):
        """Initialize a module type."""
        super().__init__(TypeCategory.MODULE)
        self.name = name
        self.fullname = fullname
        self.members: Dict[str, Symbol] = {}

    def __str__(self) -> str:
        """Return a string representation of the type."""
        return f"module {self.fullname}"

    def __eq__(self, other: object) -> bool:
        """Check if two module types are equal."""
        if not isinstance(other, ModuleType):
            return False
        return self.fullname == other.fullname


class UnionType(Type):
    """Represents a union of two or more other types."""

    def __init__(self, items: List[Type]):
        """Initialize a union type."""
        super().__init__(TypeCategory.UNION)
        # Flatten nested unions
        self.items: List[Type] = []
        for item in items:
            if isinstance(item, UnionType):
                self.items.extend(item.items)
            else:
                self.items.append(item)
        # Remove duplicates
        unique_items: List[Type] = []
        for item in self.items:
            if not any(item == x for x in unique_items):
                unique_items.append(item)
        self.items = unique_items

    def __str__(self) -> str:
        """Return a string representation of the type."""
        return f"Union[{', '.join(str(item) for item in self.items)}]"

    def __eq__(self, other: object) -> bool:
        """Check if two union types are equal."""
        if not isinstance(other, UnionType):
            return False
        if len(self.items) != len(other.items):
            return False
        # Check that all items in self.items are in other.items
        for item in self.items:
            if not any(item == x for x in other.items):
                return False
        return True


class Symbol:
    """Represents a symbol in the symbol table."""

    def __init__(
        self,
        name: str,
        type_obj: Type,
        is_defined: bool = True,
        is_readonly: bool = False,
    ):
        """Initialize a symbol."""
        self.name = name
        self.type = type_obj
        self.is_defined = is_defined
        self.is_readonly = is_readonly

    def __str__(self) -> str:
        """Return a string representation of the symbol."""
        readonly = "readonly " if self.is_readonly else ""
        defined = "" if self.is_defined else "undefined "
        return f"{readonly}{defined}{self.name}: {self.type}"


def is_subtype(source: Type, target: Type) -> bool:
    """Check if source is a subtype of target."""
    # Any type is a subtype of itself
    if source == target:
        return True

    # Any type is a subtype of Any
    if isinstance(target, AnyType):
        return True

    # Check class inheritance
    if isinstance(source, ClassType) and isinstance(target, ClassType):
        # Check if source is a subclass of target
        if source.fullname == target.fullname:
            return True

        # Check base classes
        for base in source.base_types:
            if is_subtype(base, target):
                return True

    # Check union types
    if isinstance(target, UnionType):
        # Source is a subtype if it's a subtype of any item in the union
        return any(is_subtype(source, item) for item in target.items)

    # Check function types
    if isinstance(source, FunctionType) and isinstance(target, FunctionType):
        # Check return type (covariant)
        if not is_subtype(source.return_type, target.return_type):
            return False

        # Check parameter types (contravariant)
        if len(source.param_types) != len(target.param_types):
            return False

        for i in range(len(source.param_types)):
            if not is_subtype(target.param_types[i], source.param_types[i]):
                return False

        return True

    return False


def join_types(types: List[Type]) -> Type:
    """Return the least upper bound of the given types."""
    if not types:
        return NeverType()
    if len(types) == 1:
        return types[0]

    # If any of the types is Any, the result is Any
    if any(isinstance(t, AnyType) for t in types):
        return AnyType()

    # If all types are the same, return that type
    first = types[0]
    if all(t == first for t in types[1:]):
        return first

    # For now, just return a union of the types
    # In a more sophisticated implementation, we would try to find a common supertype
    return UnionType(types)


def meet_types(types: List[Type]) -> Type:
    """Return the greatest lower bound of the given types."""
    if not types:
        return AnyType()
    if len(types) == 1:
        return types[0]

    # If any of the types is Never, the result is Never
    if any(isinstance(t, NeverType) for t in types):
        return NeverType()

    # If all types are the same, return that type
    first = types[0]
    if all(t == first for t in types[1:]):
        return first

    # For now, just return the first type that is a subtype of all others
    # In a more sophisticated implementation, we would compute the intersection
    for t in types:
        if all(is_subtype(t, other) for other in types):
            return t

    # If no type is a subtype of all others, return Never
    return NeverType()


# Create builtin types
BUILTIN_TYPES = {
    "int": ClassType("int", "builtins.int", is_instantiated=True),
    "float": ClassType("float", "builtins.float", is_instantiated=True),
    "str": ClassType("str", "builtins.str", is_instantiated=True),
    "bool": ClassType("bool", "builtins.bool", is_instantiated=True),
    "list": ClassType("list", "builtins.list", is_instantiated=True),
    "dict": ClassType("dict", "builtins.dict", is_instantiated=True),
    "set": ClassType("set", "builtins.set", is_instantiated=True),
    "tuple": ClassType("tuple", "builtins.tuple", is_instantiated=True),
    "None": ClassType("None", "builtins.None", is_instantiated=True),
    "Any": AnyType(),
    "Never": NeverType(),
    "object": ClassType("object", "builtins.object", is_instantiated=True),
}


class TypeBinder:
    """A simple type binder that associates nodes with types."""

    def __init__(self):
        """Initialize the type binder."""
        self.type_map = {}

    def bind_type(self, node, type_obj: Type) -> None:
        """Bind a type to a node."""
        self.type_map[node] = type_obj
        if hasattr(node, "type"):
            node.type = str(type_obj)

    def get_type(self, node) -> Optional[Type]:
        """Get the type of a node."""
        return self.type_map.get(node)


def test_type_system():
    """Test the basic functionality of our type system."""
    print("Testing Type System")
    print("=" * 80)

    # Test basic types
    print("\nBasic Types:")
    print("-" * 40)
    for name, type_obj in BUILTIN_TYPES.items():
        print(f"{name}: {type_obj}")

    # Test function types
    print("\nFunction Types:")
    print("-" * 40)
    add_func = FunctionType(
        [BUILTIN_TYPES["int"], BUILTIN_TYPES["int"]],
        BUILTIN_TYPES["int"],
        is_method=False,
        param_names=["a", "b"],
    )
    print(f"add function: {add_func}")

    greet_func = FunctionType(
        [BUILTIN_TYPES["str"]],
        BUILTIN_TYPES["str"],
        is_method=True,
        param_names=["name"],
    )
    print(f"greet method: {greet_func}")

    # Test class types
    print("\nClass Types:")
    print("-" * 40)
    person_class = ClassType("Person", "Person", is_instantiated=False)
    person_class.members["name"] = Symbol("name", BUILTIN_TYPES["str"])
    person_class.members["age"] = Symbol("age", BUILTIN_TYPES["int"])
    person_class.members["greet"] = Symbol("greet", greet_func)
    print(f"Person class: {person_class}")
    print("Person members:")
    for name, symbol in person_class.members.items():
        print(f"  {name}: {symbol.type}")

    # Test subtyping
    print("\nSubtyping:")
    print("-" * 40)
    print(
        f"int is a subtype of int: {is_subtype(BUILTIN_TYPES['int'], BUILTIN_TYPES['int'])}"
    )
    print(
        f"int is a subtype of float: {is_subtype(BUILTIN_TYPES['int'], BUILTIN_TYPES['float'])}"
    )
    print(
        f"int is a subtype of Any: {is_subtype(BUILTIN_TYPES['int'], BUILTIN_TYPES['Any'])}"
    )
    print(
        f"Any is a subtype of int: {is_subtype(BUILTIN_TYPES['Any'], BUILTIN_TYPES['int'])}"
    )

    # Test type operations
    print("\nType Operations:")
    print("-" * 40)
    int_float_join = join_types([BUILTIN_TYPES["int"], BUILTIN_TYPES["float"]])
    print(f"join(int, float): {int_float_join}")
    int_float_meet = meet_types([BUILTIN_TYPES["int"], BUILTIN_TYPES["float"]])
    print(f"meet(int, float): {int_float_meet}")

    print("\nTest completed successfully!")


def test_type_binding():
    """Test a simple type binding scenario."""
    print("\nTesting Type Binding")
    print("=" * 80)

    # Create a simple AST-like structure
    class Node:
        def __init__(self, name):
            self.name = name
            self.type = None

    # Create some nodes
    int_node = Node("x")
    float_node = Node("y")
    str_node = Node("s")
    bool_node = Node("b")
    add_node = Node("add")
    person_node = Node("Person")

    # Create a type binder
    binder = TypeBinder()

    # Bind types to nodes
    binder.bind_type(int_node, BUILTIN_TYPES["int"])
    binder.bind_type(float_node, BUILTIN_TYPES["float"])
    binder.bind_type(str_node, BUILTIN_TYPES["str"])
    binder.bind_type(bool_node, BUILTIN_TYPES["bool"])

    # Bind a function type
    add_func = FunctionType(
        [BUILTIN_TYPES["int"], BUILTIN_TYPES["int"]],
        BUILTIN_TYPES["int"],
        is_method=False,
        param_names=["a", "b"],
    )
    binder.bind_type(add_node, add_func)

    # Bind a class type
    person_class = ClassType("Person", "Person", is_instantiated=False)
    person_class.members["name"] = Symbol("name", BUILTIN_TYPES["str"])
    person_class.members["age"] = Symbol("age", BUILTIN_TYPES["int"])
    binder.bind_type(person_node, person_class)

    # Print the results
    print("\nNode Types:")
    print("-" * 40)
    for node, type_obj in binder.type_map.items():
        print(f"{node.name}: {type_obj}")

    print("\nTest completed successfully!")


if __name__ == "__main__":
    test_type_system()
    test_type_binding()

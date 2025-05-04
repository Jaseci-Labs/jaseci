"""Simple test for the type binding functionality."""

import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our type system
from jaclang.compiler.types import (
    BUILTIN_TYPES,
    ClassType,
    FunctionType,
    Symbol,
    Type,
    UnknownType,
    is_subtype,
    join_types,
    meet_types,
)


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

    class TypeBinder:
        def __init__(self):
            self.type_map = {}

        def bind_type(self, node, type_obj):
            self.type_map[node] = type_obj
            node.type = str(type_obj)

        def get_type(self, node):
            return self.type_map.get(node)

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

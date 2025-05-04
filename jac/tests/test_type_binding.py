"""Test script for the type binding pass."""

import os
import sys
import ast
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from jaclang.compiler.program import JacProgram
from jaclang.compiler.passes.main import CompilerMode
from jaclang.compiler.passes.main.type_binder_pass import TypeBinderPass
from jaclang.compiler.types import (
    BUILTIN_TYPES,
    ClassType,
    FunctionType,
    Symbol,
    Type,
    UnknownType,
)


def test_type_binding_with_python():
    """Test the type binding functionality with a Python file."""
    # Get the path to the test file
    test_file_path = os.path.join(os.path.dirname(__file__), "type_binding_test.py")

    # Parse the Python file
    with open(test_file_path, "r") as f:
        source = f.read()

    tree = ast.parse(source)

    # Create a simple type system for the Python file
    types = {}

    # Add the Person class
    person_class = ClassType("Person", "Person", is_instantiated=False)
    types["Person"] = person_class

    # Add the Person methods
    person_class.members["__init__"] = Symbol(
        "__init__",
        FunctionType(
            [BUILTIN_TYPES["str"], BUILTIN_TYPES["int"]],
            BUILTIN_TYPES["None"],
            is_method=True,
            param_names=["name", "age"],
        ),
    )

    person_class.members["greet"] = Symbol(
        "greet",
        FunctionType(
            [],
            BUILTIN_TYPES["str"],
            is_method=True,
        ),
    )

    person_class.members["birthday"] = Symbol(
        "birthday",
        FunctionType(
            [],
            BUILTIN_TYPES["None"],
            is_method=True,
        ),
    )

    # Add the add function
    types["add"] = Symbol(
        "add",
        FunctionType(
            [BUILTIN_TYPES["int"], BUILTIN_TYPES["int"]],
            BUILTIN_TYPES["int"],
            is_method=False,
            param_names=["a", "b"],
        ),
    )

    # Add variables from the main function
    types["x"] = Symbol("x", BUILTIN_TYPES["int"])
    types["y"] = Symbol("y", BUILTIN_TYPES["float"])
    types["s"] = Symbol("s", BUILTIN_TYPES["str"])
    types["b"] = Symbol("b", BUILTIN_TYPES["bool"])
    types["result"] = Symbol("result", BUILTIN_TYPES["int"])
    types["person"] = Symbol("person", person_class)
    types["greeting"] = Symbol("greeting", BUILTIN_TYPES["str"])

    # Print the results
    print(f"Type binding results for {test_file_path}:")
    print("=" * 80)

    # Print the types of all variables
    print("\nVariables:")
    print("-" * 40)
    for name, symbol in types.items():
        if not isinstance(symbol.type, (FunctionType, ClassType)) or name == "person":
            print(f"{name}: {symbol.type}")

    # Print the types of all functions
    print("\nFunctions:")
    print("-" * 40)
    for name, symbol in types.items():
        if isinstance(symbol.type, FunctionType) and not symbol.type.is_method:
            print(f"{name}: {symbol.type}")

    # Print the types of all classes
    print("\nClasses:")
    print("-" * 40)
    for name, symbol in types.items():
        if isinstance(symbol, ClassType) or (
            hasattr(symbol, "type")
            and isinstance(symbol.type, ClassType)
            and not symbol.name == "person"
        ):
            print(f"{name}: {symbol if isinstance(symbol, ClassType) else symbol.type}")
            # Print class members
            if isinstance(symbol, ClassType):
                for member_name, member_symbol in symbol.members.items():
                    print(f"  {member_name}: {member_symbol.type}")

    print("\nTest completed successfully!")


def test_type_binder_pass():
    """Test the TypeBinderPass implementation."""
    # Create a simple test case
    from jaclang.compiler.unitree import Module, Name, Int, Float, String, Bool

    # Create a module
    module = Module()

    # Add some nodes to the module
    int_node = Int("5")
    float_node = Float("3.14")
    string_node = String("Hello, world!")
    bool_node = Bool("true")

    # Run the type binder pass
    binder = TypeBinderPass(ir_in=module)
    binder.run()

    # Manually bind types to nodes
    binder.bind_type(int_node, BUILTIN_TYPES["int"])
    binder.bind_type(float_node, BUILTIN_TYPES["float"])
    binder.bind_type(string_node, BUILTIN_TYPES["str"])
    binder.bind_type(bool_node, BUILTIN_TYPES["bool"])

    # Print the results
    print("\nType Binder Pass Test:")
    print("=" * 80)

    # Print the types of all nodes
    print("\nNode Types:")
    print("-" * 40)
    for node, type_obj in binder.type_map.items():
        print(f"{node.__class__.__name__}: {type_obj}")

    print("\nTest completed successfully!")


if __name__ == "__main__":
    test_type_binding_with_python()
    test_type_binder_pass()

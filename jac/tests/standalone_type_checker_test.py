"""Standalone test for the type checking system."""

from standalone_type_system_test import (
    BUILTIN_TYPES,
    AnyType,
    ClassType,
    FunctionType,
    Symbol,
    Type,
    TypeBinder,
    UnknownType,
    is_subtype,
)


class TypeEvaluator:
    """A simple type evaluator that infers types for expressions."""

    def __init__(self, binder):
        """Initialize the type evaluator."""
        self.binder = binder
        self.type_map = binder.type_map.copy()

    def bind_type(self, node, type_obj: Type) -> None:
        """Bind a type to a node."""
        self.type_map[node] = type_obj
        if hasattr(node, "type"):
            node.type = str(type_obj)

    def get_type(self, node):
        """Get the type of a node."""
        return self.type_map.get(node)

    def evaluate_binary_expr(self, node, left_type, right_type, op):
        """Evaluate the type of a binary expression."""
        # Addition
        if op == "+":
            # int + int = int
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.int"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.int"
            ):
                return BUILTIN_TYPES["int"]

            # float + float = float, int + float = float, float + int = float
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
                and isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                return BUILTIN_TYPES["float"]

            # str + str = str
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.str"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.str"
            ):
                return BUILTIN_TYPES["str"]

        # Subtraction
        elif op == "-":
            # int - int = int
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.int"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.int"
            ):
                return BUILTIN_TYPES["int"]

            # float - float = float, int - float = float, float - int = float
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
                and isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                return BUILTIN_TYPES["float"]

        # Comparison operators
        elif op in ["==", "!=", "<", ">", "<=", ">="]:
            return BUILTIN_TYPES["bool"]

        # Default to Unknown
        return UnknownType()


class TypeChecker:
    """A simple type checker that checks type compatibility."""

    def __init__(self, evaluator):
        """Initialize the type checker."""
        self.evaluator = evaluator
        self.type_map = evaluator.type_map.copy()
        self.errors = []

    def get_type(self, node):
        """Get the type of a node."""
        return self.type_map.get(node)

    def check_assignment(self, target, value, target_type, value_type):
        """Check if an assignment is type-compatible."""
        if not is_subtype(value_type, target_type):
            self.errors.append(
                f"Type mismatch: Cannot assign value of type '{value_type}' "
                f"to variable of type '{target_type}'"
            )

    def check_binary_expr(self, node, left_type, right_type, op):
        """Check type compatibility for binary expressions."""
        # Addition
        if op == "+":
            # int + int, float + float, int + float, float + int
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
                and isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                return

            # str + str
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.str"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.str"
            ):
                return

            # Error for incompatible types
            self.errors.append(
                f"Operator '+' not supported for types '{left_type}' and '{right_type}'"
            )

        # Subtraction
        elif op == "-":
            # int - int, float - float, int - float, float - int
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
                and isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                return

            # Error for incompatible types
            self.errors.append(
                f"Operator '-' not supported for types '{left_type}' and '{right_type}'"
            )

        # Comparison operators
        elif op in ["==", "!="]:
            # Any types can be compared for equality
            return
        elif op in ["<", ">", "<=", ">="]:
            # int, float
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
                and isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                return

            # str
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.str"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.str"
            ):
                return

            # Error for incompatible types
            self.errors.append(
                f"Operator '{op}' not supported for types '{left_type}' and '{right_type}'"
            )


def test_type_checker():
    """Test the type checker with a simple example."""
    print("Testing Type Checker")
    print("=" * 80)

    # Create a simple AST-like structure
    class Node:
        def __init__(self, name):
            self.name = name
            self.type = None

    class BinaryExpr:
        def __init__(self, left, right, op):
            self.left = left
            self.right = right
            self.op = op
            self.type = None

    class Assignment:
        def __init__(self, target, value):
            self.target = target
            self.value = value
            self.type = None

    # Create some nodes
    int_node = Node("x")
    float_node = Node("y")
    str_node = Node("s")
    bool_node = Node("b")

    # Create a type binder
    binder = TypeBinder()

    # Bind types to nodes
    binder.bind_type(int_node, BUILTIN_TYPES["int"])
    binder.bind_type(float_node, BUILTIN_TYPES["float"])
    binder.bind_type(str_node, BUILTIN_TYPES["str"])
    binder.bind_type(bool_node, BUILTIN_TYPES["bool"])

    # Create a type evaluator
    evaluator = TypeEvaluator(binder)

    # Create some expressions
    add_int_int = BinaryExpr(int_node, int_node, "+")
    add_int_float = BinaryExpr(int_node, float_node, "+")
    add_str_str = BinaryExpr(str_node, str_node, "+")
    add_str_int = BinaryExpr(str_node, int_node, "+")
    sub_int_int = BinaryExpr(int_node, int_node, "-")
    sub_str_str = BinaryExpr(str_node, str_node, "-")
    eq_int_int = BinaryExpr(int_node, int_node, "==")
    lt_int_int = BinaryExpr(int_node, int_node, "<")
    lt_str_int = BinaryExpr(str_node, int_node, "<")

    # Evaluate expressions
    evaluator.bind_type(
        add_int_int,
        evaluator.evaluate_binary_expr(
            add_int_int,
            binder.get_type(int_node),
            binder.get_type(int_node),
            "+",
        ),
    )
    evaluator.bind_type(
        add_int_float,
        evaluator.evaluate_binary_expr(
            add_int_float,
            binder.get_type(int_node),
            binder.get_type(float_node),
            "+",
        ),
    )
    evaluator.bind_type(
        add_str_str,
        evaluator.evaluate_binary_expr(
            add_str_str,
            binder.get_type(str_node),
            binder.get_type(str_node),
            "+",
        ),
    )
    evaluator.bind_type(
        add_str_int,
        evaluator.evaluate_binary_expr(
            add_str_int,
            binder.get_type(str_node),
            binder.get_type(int_node),
            "+",
        ),
    )
    evaluator.bind_type(
        sub_int_int,
        evaluator.evaluate_binary_expr(
            sub_int_int,
            binder.get_type(int_node),
            binder.get_type(int_node),
            "-",
        ),
    )
    evaluator.bind_type(
        sub_str_str,
        evaluator.evaluate_binary_expr(
            sub_str_str,
            binder.get_type(str_node),
            binder.get_type(str_node),
            "-",
        ),
    )
    evaluator.bind_type(
        eq_int_int,
        evaluator.evaluate_binary_expr(
            eq_int_int,
            binder.get_type(int_node),
            binder.get_type(int_node),
            "==",
        ),
    )
    evaluator.bind_type(
        lt_int_int,
        evaluator.evaluate_binary_expr(
            lt_int_int,
            binder.get_type(int_node),
            binder.get_type(int_node),
            "<",
        ),
    )
    evaluator.bind_type(
        lt_str_int,
        evaluator.evaluate_binary_expr(
            lt_str_int,
            binder.get_type(str_node),
            binder.get_type(int_node),
            "<",
        ),
    )

    # Create some assignments
    assign_int_int = Assignment(int_node, int_node)
    assign_float_int = Assignment(float_node, int_node)
    assign_int_str = Assignment(int_node, str_node)

    # Create a type checker
    checker = TypeChecker(evaluator)

    # Check expressions
    checker.check_binary_expr(
        add_int_int,
        checker.get_type(int_node),
        checker.get_type(int_node),
        "+",
    )
    checker.check_binary_expr(
        add_int_float,
        checker.get_type(int_node),
        checker.get_type(float_node),
        "+",
    )
    checker.check_binary_expr(
        add_str_str,
        checker.get_type(str_node),
        checker.get_type(str_node),
        "+",
    )
    checker.check_binary_expr(
        add_str_int,
        checker.get_type(str_node),
        checker.get_type(int_node),
        "+",
    )
    checker.check_binary_expr(
        sub_int_int,
        checker.get_type(int_node),
        checker.get_type(int_node),
        "-",
    )
    checker.check_binary_expr(
        sub_str_str,
        checker.get_type(str_node),
        checker.get_type(str_node),
        "-",
    )
    checker.check_binary_expr(
        eq_int_int,
        checker.get_type(int_node),
        checker.get_type(int_node),
        "==",
    )
    checker.check_binary_expr(
        lt_int_int,
        checker.get_type(int_node),
        checker.get_type(int_node),
        "<",
    )
    checker.check_binary_expr(
        lt_str_int,
        checker.get_type(str_node),
        checker.get_type(int_node),
        "<",
    )

    # Check assignments
    checker.check_assignment(
        int_node,
        int_node,
        checker.get_type(int_node),
        checker.get_type(int_node),
    )
    checker.check_assignment(
        float_node,
        int_node,
        checker.get_type(float_node),
        checker.get_type(int_node),
    )
    checker.check_assignment(
        int_node,
        str_node,
        checker.get_type(int_node),
        checker.get_type(str_node),
    )

    # Print the results
    print("\nType Evaluation Results:")
    print("-" * 80)
    print(f"add_int_int: {evaluator.get_type(add_int_int)}")
    print(f"add_int_float: {evaluator.get_type(add_int_float)}")
    print(f"add_str_str: {evaluator.get_type(add_str_str)}")
    print(f"add_str_int: {evaluator.get_type(add_str_int)}")
    print(f"sub_int_int: {evaluator.get_type(sub_int_int)}")
    print(f"sub_str_str: {evaluator.get_type(sub_str_str)}")
    print(f"eq_int_int: {evaluator.get_type(eq_int_int)}")
    print(f"lt_int_int: {evaluator.get_type(lt_int_int)}")
    print(f"lt_str_int: {evaluator.get_type(lt_str_int)}")

    print("\nType Checking Results:")
    print("-" * 80)
    if checker.errors:
        print(f"Found {len(checker.errors)} type errors:")
        for error in checker.errors:
            print(f"  - {error}")
    else:
        print("No type errors found!")

    print("\nTest completed successfully!")


if __name__ == "__main__":
    test_type_checker()

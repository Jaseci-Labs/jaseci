"""Type evaluator pass for Jac language.

This pass evaluates and infers types for expressions based on their structure and context.
It builds on the type binding pass to provide more accurate type information.
"""

from typing import Dict, List, Optional, Set, Tuple, Union, cast

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.compiler.types import (
    BUILTIN_TYPES,
    AbilityType,
    AnyType,
    ClassType,
    EdgeType,
    EnumType,
    FunctionType,
    ModuleType,
    NodeType,
    Symbol,
    Type,
    TypeCategory,
    UnboundType,
    UnionType,
    UnknownType,
    WalkerType,
    is_subtype,
    join_types,
)
from jaclang.compiler.passes.main.type_binder_pass import TypeBinderPass


class TypeEvaluatorPass(UniPass):
    """Pass that evaluates and infers types for expressions."""

    def __init__(self, ir_in: uni.UniNode, prog=None) -> None:
        """Initialize the TypeEvaluatorPass."""
        super().__init__(ir_in, prog)
        # Run the type binder pass first to get initial type information
        self.binder = TypeBinderPass(ir_in, prog)
        self.binder.run()
        self.type_map = self.binder.type_map

    def bind_type(self, node: uni.UniNode, type_obj: Type) -> None:
        """Bind a type to a node."""
        self.type_map[node] = type_obj
        if isinstance(node, uni.AstSymbolNode):
            node.name_spec.expr_type = self._type_to_string(type_obj)

    def get_type(self, node: uni.UniNode) -> Optional[Type]:
        """Get the type of a node."""
        return self.type_map.get(node)

    def _type_to_string(self, type_obj: Type) -> str:
        """Convert a type to a string representation."""
        return str(type_obj)

    def _get_builtin_type(self, name: str) -> Type:
        """Get a builtin type by name."""
        return BUILTIN_TYPES.get(name, UnknownType())

    def before_pass(self) -> None:
        """Set up the pass."""
        super().before_pass()

    def after_pass(self) -> None:
        """Clean up after the pass."""
        super().after_pass()

    def enter_node(self, node: uni.UniNode) -> None:
        """Run on entering node."""
        super().enter_node(node)

        # Evaluate expressions
        if isinstance(node, uni.Expr):
            self.evaluate_expr(node)

    def evaluate_expr(self, node: uni.Expr) -> Optional[Type]:
        """Evaluate the type of an expression."""
        # Check if we already have a type for this node
        if node in self.type_map:
            return self.type_map[node]

        # Evaluate based on node type
        if isinstance(node, uni.BinaryExpr):
            return self.evaluate_binary_expr(node)
        elif isinstance(node, uni.UnaryExpr):
            return self.evaluate_unary_expr(node)
        elif isinstance(node, uni.FuncCall):
            return self.evaluate_func_call(node)
        elif isinstance(node, uni.AtomTrailer):
            return self.evaluate_atom_trailer(node)
        elif isinstance(node, uni.ListVal):
            return self.evaluate_list_val(node)
        elif isinstance(node, uni.DictVal):
            return self.evaluate_dict_val(node)
        elif isinstance(node, uni.SetVal):
            return self.evaluate_set_val(node)
        elif isinstance(node, uni.TupleVal):
            return self.evaluate_tuple_val(node)

        return None

    def evaluate_binary_expr(self, node: uni.BinaryExpr) -> Optional[Type]:
        """Evaluate the type of a binary expression."""
        left_type = self.evaluate_expr(node.left)
        right_type = self.evaluate_expr(node.right)

        if left_type is None or right_type is None:
            return None

        # Addition
        if isinstance(node.op, uni.AddOp):
            # int + int = int
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.int"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.int"
            ):
                result_type = self._get_builtin_type("int")
                self.bind_type(node, result_type)
                return result_type

            # float + float = float, int + float = float, float + int = float
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
            ) and (
                isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                result_type = self._get_builtin_type("float")
                self.bind_type(node, result_type)
                return result_type

            # str + str = str
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.str"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.str"
            ):
                result_type = self._get_builtin_type("str")
                self.bind_type(node, result_type)
                return result_type

            # list + list = list
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.list"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.list"
            ):
                result_type = self._get_builtin_type("list")
                self.bind_type(node, result_type)
                return result_type

        # Subtraction
        elif isinstance(node.op, uni.SubOp):
            # int - int = int
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.int"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.int"
            ):
                result_type = self._get_builtin_type("int")
                self.bind_type(node, result_type)
                return result_type

            # float - float = float, int - float = float, float - int = float
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
            ) and (
                isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                result_type = self._get_builtin_type("float")
                self.bind_type(node, result_type)
                return result_type

        # Multiplication
        elif isinstance(node.op, uni.MultOp):
            # int * int = int
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.int"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.int"
            ):
                result_type = self._get_builtin_type("int")
                self.bind_type(node, result_type)
                return result_type

            # float * float = float, int * float = float, float * int = float
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
            ) and (
                isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                result_type = self._get_builtin_type("float")
                self.bind_type(node, result_type)
                return result_type

            # str * int = str, int * str = str
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.str"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.int"
            ) or (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.int"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.str"
            ):
                result_type = self._get_builtin_type("str")
                self.bind_type(node, result_type)
                return result_type

            # list * int = list
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.list"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.int"
            ):
                result_type = self._get_builtin_type("list")
                self.bind_type(node, result_type)
                return result_type

        # Division
        elif isinstance(node.op, uni.DivOp):
            # int / int = float, float / float = float, int / float = float, float / int = float
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
            ) and (
                isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                result_type = self._get_builtin_type("float")
                self.bind_type(node, result_type)
                return result_type

        # Integer division
        elif isinstance(node.op, uni.FloorDivOp):
            # int // int = int
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.int"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.int"
            ):
                result_type = self._get_builtin_type("int")
                self.bind_type(node, result_type)
                return result_type

            # float // float = float, int // float = float, float // int = float
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
            ) and (
                isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                result_type = self._get_builtin_type("float")
                self.bind_type(node, result_type)
                return result_type

        # Modulo
        elif isinstance(node.op, uni.ModOp):
            # int % int = int
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname == "builtins.int"
                and isinstance(right_type, ClassType)
                and right_type.fullname == "builtins.int"
            ):
                result_type = self._get_builtin_type("int")
                self.bind_type(node, result_type)
                return result_type

            # float % float = float, int % float = float, float % int = float
            if (
                isinstance(left_type, ClassType)
                and left_type.fullname in ["builtins.int", "builtins.float"]
            ) and (
                isinstance(right_type, ClassType)
                and right_type.fullname in ["builtins.int", "builtins.float"]
            ):
                result_type = self._get_builtin_type("float")
                self.bind_type(node, result_type)
                return result_type

        # Comparison operators
        elif isinstance(
            node.op, (uni.EqOp, uni.NotEqOp, uni.LtOp, uni.GtOp, uni.LtEOp, uni.GtEOp)
        ):
            result_type = self._get_builtin_type("bool")
            self.bind_type(node, result_type)
            return result_type

        # Logical operators
        elif isinstance(node.op, (uni.AndOp, uni.OrOp)):
            result_type = self._get_builtin_type("bool")
            self.bind_type(node, result_type)
            return result_type

        # Default to Unknown
        result_type = UnknownType()
        self.bind_type(node, result_type)
        return result_type

    def evaluate_unary_expr(self, node: uni.UnaryExpr) -> Optional[Type]:
        """Evaluate the type of a unary expression."""
        operand_type = self.evaluate_expr(node.operand)

        if operand_type is None:
            return None

        # Negation
        if isinstance(node.op, uni.NegOp):
            # -int = int
            if (
                isinstance(operand_type, ClassType)
                and operand_type.fullname == "builtins.int"
            ):
                result_type = self._get_builtin_type("int")
                self.bind_type(node, result_type)
                return result_type

            # -float = float
            if (
                isinstance(operand_type, ClassType)
                and operand_type.fullname == "builtins.float"
            ):
                result_type = self._get_builtin_type("float")
                self.bind_type(node, result_type)
                return result_type

        # Not
        if isinstance(node.op, uni.NotOp):
            result_type = self._get_builtin_type("bool")
            self.bind_type(node, result_type)
            return result_type

        # Default to Unknown
        result_type = UnknownType()
        self.bind_type(node, result_type)
        return result_type

    def evaluate_func_call(self, node: uni.FuncCall) -> Optional[Type]:
        """Evaluate the type of a function call."""
        func_type = self.evaluate_expr(node.target)

        if func_type is None:
            return None

        if isinstance(func_type, FunctionType):
            result_type = func_type.return_type
            self.bind_type(node, result_type)
            return result_type

        # Handle built-in functions with special return types
        if isinstance(node.target, uni.NameAtom):
            if node.target.sym_name == "len":
                result_type = self._get_builtin_type("int")
                self.bind_type(node, result_type)
                return result_type
            elif node.target.sym_name == "str":
                result_type = self._get_builtin_type("str")
                self.bind_type(node, result_type)
                return result_type
            elif node.target.sym_name == "int":
                result_type = self._get_builtin_type("int")
                self.bind_type(node, result_type)
                return result_type
            elif node.target.sym_name == "float":
                result_type = self._get_builtin_type("float")
                self.bind_type(node, result_type)
                return result_type
            elif node.target.sym_name == "bool":
                result_type = self._get_builtin_type("bool")
                self.bind_type(node, result_type)
                return result_type
            elif node.target.sym_name == "list":
                result_type = self._get_builtin_type("list")
                self.bind_type(node, result_type)
                return result_type
            elif node.target.sym_name == "dict":
                result_type = self._get_builtin_type("dict")
                self.bind_type(node, result_type)
                return result_type
            elif node.target.sym_name == "set":
                result_type = self._get_builtin_type("set")
                self.bind_type(node, result_type)
                return result_type

        # If the target is a class type, the result is an instance of that class
        if isinstance(func_type, ClassType) and (
            func_type.flags & 1
        ):  # Check if INSTANTIABLE flag is set
            # Create a new instance type
            instance_type = ClassType(
                name=func_type.name,
                fullname=func_type.fullname,
                base_types=func_type.base_types,
                is_instantiated=True,
            )
            instance_type.members = func_type.members
            self.bind_type(node, instance_type)
            return instance_type

        # Default to Unknown
        result_type = UnknownType()
        self.bind_type(node, result_type)
        return result_type

    def evaluate_atom_trailer(self, node: uni.AtomTrailer) -> Optional[Type]:
        """Evaluate the type of an atom trailer (e.g., obj.attr)."""
        target_type = self.evaluate_expr(node.target)

        if target_type is None:
            return None

        if isinstance(target_type, ClassType) and isinstance(node.right, uni.NameAtom):
            # Look up the attribute in the class members
            attr_name = node.right.sym_name
            if attr_name in target_type.members:
                member_sym = target_type.members[attr_name]
                result_type = member_sym.type
                self.bind_type(node, result_type)
                return result_type

        # Default to Unknown
        result_type = UnknownType()
        self.bind_type(node, result_type)
        return result_type

    def evaluate_list_val(self, node: uni.ListVal) -> Optional[Type]:
        """Evaluate the type of a list literal."""
        result_type = self._get_builtin_type("list")
        self.bind_type(node, result_type)
        return result_type

    def evaluate_dict_val(self, node: uni.DictVal) -> Optional[Type]:
        """Evaluate the type of a dictionary literal."""
        result_type = self._get_builtin_type("dict")
        self.bind_type(node, result_type)
        return result_type

    def evaluate_set_val(self, node: uni.SetVal) -> Optional[Type]:
        """Evaluate the type of a set literal."""
        result_type = self._get_builtin_type("set")
        self.bind_type(node, result_type)
        return result_type

    def evaluate_tuple_val(self, node: uni.TupleVal) -> Optional[Type]:
        """Evaluate the type of a tuple literal."""
        result_type = self._get_builtin_type("tuple")
        self.bind_type(node, result_type)
        return result_type

"""Type checker pass for Jac language.

This pass checks type compatibility for expressions and statements.
It builds on the type evaluator pass to provide type checking.
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
)
from jaclang.compiler.passes.main.type_evaluator_pass import TypeEvaluatorPass


class TypeCheckerPass(UniPass):
    """Pass that checks type compatibility."""

    def __init__(self, ir_in: uni.UniNode, prog=None) -> None:
        """Initialize the TypeCheckerPass."""
        super().__init__(ir_in, prog)
        # Run the type evaluator pass first to get inferred type information
        self.evaluator = TypeEvaluatorPass(ir_in, prog)
        self.evaluator.run()
        self.type_map = self.evaluator.type_map

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

    def enter_assignment(self, node: uni.Assignment) -> None:
        """Check type compatibility for assignments."""
        # Get the type of the value
        value_type = self.get_type(node.value)
        if value_type is None:
            return

        # Check each target
        for target in node.target.items:
            self.check_assignment(target, value_type, node)

    def check_assignment(
        self, target: uni.UniNode, value_type: Type, node: uni.UniNode
    ) -> None:
        """Check if an assignment is type-compatible."""
        # Get the type of the target
        target_type = self.get_type(target)
        if target_type is None:
            return

        # Check if the value type is compatible with the target type
        if not is_subtype(value_type, target_type):
            self.log_error(
                f"Type mismatch: Cannot assign value of type '{self._type_to_string(value_type)}' "
                f"to variable of type '{self._type_to_string(target_type)}'",
                node_override=node,
            )

    def enter_func_call(self, node: uni.FuncCall) -> None:
        """Check type compatibility for function calls."""
        # Get the type of the function
        func_type = self.get_type(node.target)
        if func_type is None or not isinstance(func_type, FunctionType):
            return

        # Check if the function has parameters
        if not node.params or not func_type.param_types:
            return

        # Check each argument
        for i, arg in enumerate(node.params.items):
            # Skip if we've run out of parameter types
            if i >= len(func_type.param_types):
                break

            # Get the type of the argument
            arg_type = self.get_type(arg)
            if arg_type is None:
                continue

            # Get the expected parameter type
            param_type = func_type.param_types[i]

            # Check if the argument type is compatible with the parameter type
            if not is_subtype(arg_type, param_type):
                param_name = (
                    func_type.param_names[i]
                    if i < len(func_type.param_names)
                    else f"param{i+1}"
                )
                self.log_error(
                    f"Type mismatch: Argument of type '{self._type_to_string(arg_type)}' "
                    f"is not compatible with parameter '{param_name}' of type '{self._type_to_string(param_type)}'",
                    node_override=arg,
                )

    def enter_return_stmt(self, node: uni.ReturnStmt) -> None:
        """Check type compatibility for return statements."""
        # Get the enclosing function
        enclosing_func = node.parent_of_type((uni.Ability, uni.AbilityDef))
        if enclosing_func is None:
            return

        # Get the return type of the function
        func_type = self.get_type(enclosing_func)
        if func_type is None or not isinstance(func_type, FunctionType):
            return

        # Get the type of the return value
        if node.expr:
            return_value_type = self.get_type(node.expr)
            if return_value_type is None:
                return

            # Check if the return value type is compatible with the function's return type
            if not is_subtype(return_value_type, func_type.return_type):
                self.log_error(
                    f"Type mismatch: Return value of type '{self._type_to_string(return_value_type)}' "
                    f"is not compatible with return type '{self._type_to_string(func_type.return_type)}'",
                    node_override=node,
                )
        elif not isinstance(
            func_type.return_type, (AnyType, UnknownType)
        ) and func_type.return_type != self._get_builtin_type("None"):
            # If there's no return value but the function is expected to return a value
            self.log_error(
                f"Type mismatch: Missing return value for function with return type '{self._type_to_string(func_type.return_type)}'",
                node_override=node,
            )

    def enter_binary_expr(self, node: uni.BinaryExpr) -> None:
        """Check type compatibility for binary expressions."""
        # Get the types of the operands
        left_type = self.get_type(node.left)
        right_type = self.get_type(node.right)
        if left_type is None or right_type is None:
            return

        # Check operator compatibility based on operand types
        if isinstance(node.op, uni.AddOp):
            self._check_add_op_compatibility(left_type, right_type, node)
        elif isinstance(node.op, uni.SubOp):
            self._check_sub_op_compatibility(left_type, right_type, node)
        elif isinstance(node.op, uni.MultOp):
            self._check_mult_op_compatibility(left_type, right_type, node)
        elif isinstance(node.op, uni.DivOp):
            self._check_div_op_compatibility(left_type, right_type, node)
        elif isinstance(node.op, uni.FloorDivOp):
            self._check_floor_div_op_compatibility(left_type, right_type, node)
        elif isinstance(node.op, uni.ModOp):
            self._check_mod_op_compatibility(left_type, right_type, node)
        elif isinstance(node.op, (uni.EqOp, uni.NotEqOp)):
            # Equality operators can be used with any types
            pass
        elif isinstance(node.op, (uni.LtOp, uni.GtOp, uni.LtEOp, uni.GtEOp)):
            self._check_comparison_op_compatibility(left_type, right_type, node)
        elif isinstance(node.op, (uni.AndOp, uni.OrOp)):
            # Logical operators can be used with any types (Python-like behavior)
            pass

    def _check_add_op_compatibility(
        self, left_type: Type, right_type: Type, node: uni.BinaryExpr
    ) -> None:
        """Check compatibility for the + operator."""
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

        # list + list
        if (
            isinstance(left_type, ClassType)
            and left_type.fullname == "builtins.list"
            and isinstance(right_type, ClassType)
            and right_type.fullname == "builtins.list"
        ):
            return

        # Error for incompatible types
        self.log_error(
            f"Operator '+' not supported for types '{self._type_to_string(left_type)}' and '{self._type_to_string(right_type)}'",
            node_override=node,
        )

    def _check_sub_op_compatibility(
        self, left_type: Type, right_type: Type, node: uni.BinaryExpr
    ) -> None:
        """Check compatibility for the - operator."""
        # int - int, float - float, int - float, float - int
        if (
            isinstance(left_type, ClassType)
            and left_type.fullname in ["builtins.int", "builtins.float"]
            and isinstance(right_type, ClassType)
            and right_type.fullname in ["builtins.int", "builtins.float"]
        ):
            return

        # Error for incompatible types
        self.log_error(
            f"Operator '-' not supported for types '{self._type_to_string(left_type)}' and '{self._type_to_string(right_type)}'",
            node_override=node,
        )

    def _check_mult_op_compatibility(
        self, left_type: Type, right_type: Type, node: uni.BinaryExpr
    ) -> None:
        """Check compatibility for the * operator."""
        # int * int, float * float, int * float, float * int
        if (
            isinstance(left_type, ClassType)
            and left_type.fullname in ["builtins.int", "builtins.float"]
            and isinstance(right_type, ClassType)
            and right_type.fullname in ["builtins.int", "builtins.float"]
        ):
            return

        # str * int, int * str
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
            return

        # list * int
        if (
            isinstance(left_type, ClassType)
            and left_type.fullname == "builtins.list"
            and isinstance(right_type, ClassType)
            and right_type.fullname == "builtins.int"
        ):
            return

        # Error for incompatible types
        self.log_error(
            f"Operator '*' not supported for types '{self._type_to_string(left_type)}' and '{self._type_to_string(right_type)}'",
            node_override=node,
        )

    def _check_div_op_compatibility(
        self, left_type: Type, right_type: Type, node: uni.BinaryExpr
    ) -> None:
        """Check compatibility for the / operator."""
        # int / int, float / float, int / float, float / int
        if (
            isinstance(left_type, ClassType)
            and left_type.fullname in ["builtins.int", "builtins.float"]
            and isinstance(right_type, ClassType)
            and right_type.fullname in ["builtins.int", "builtins.float"]
        ):
            return

        # Error for incompatible types
        self.log_error(
            f"Operator '/' not supported for types '{self._type_to_string(left_type)}' and '{self._type_to_string(right_type)}'",
            node_override=node,
        )

    def _check_floor_div_op_compatibility(
        self, left_type: Type, right_type: Type, node: uni.BinaryExpr
    ) -> None:
        """Check compatibility for the // operator."""
        # int // int, float // float, int // float, float // int
        if (
            isinstance(left_type, ClassType)
            and left_type.fullname in ["builtins.int", "builtins.float"]
            and isinstance(right_type, ClassType)
            and right_type.fullname in ["builtins.int", "builtins.float"]
        ):
            return

        # Error for incompatible types
        self.log_error(
            f"Operator '//' not supported for types '{self._type_to_string(left_type)}' and '{self._type_to_string(right_type)}'",
            node_override=node,
        )

    def _check_mod_op_compatibility(
        self, left_type: Type, right_type: Type, node: uni.BinaryExpr
    ) -> None:
        """Check compatibility for the % operator."""
        # int % int, float % float, int % float, float % int
        if (
            isinstance(left_type, ClassType)
            and left_type.fullname in ["builtins.int", "builtins.float"]
            and isinstance(right_type, ClassType)
            and right_type.fullname in ["builtins.int", "builtins.float"]
        ):
            return

        # Error for incompatible types
        self.log_error(
            f"Operator '%' not supported for types '{self._type_to_string(left_type)}' and '{self._type_to_string(right_type)}'",
            node_override=node,
        )

    def _check_comparison_op_compatibility(
        self, left_type: Type, right_type: Type, node: uni.BinaryExpr
    ) -> None:
        """Check compatibility for comparison operators (<, >, <=, >=)."""
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
        op_str = node.op.__class__.__name__.replace("Op", "")
        self.log_error(
            f"Operator '{op_str}' not supported for types '{self._type_to_string(left_type)}' and '{self._type_to_string(right_type)}'",
            node_override=node,
        )

    def enter_unary_expr(self, node: uni.UnaryExpr) -> None:
        """Check type compatibility for unary expressions."""
        # Get the type of the operand
        operand_type = self.get_type(node.operand)
        if operand_type is None:
            return

        # Check operator compatibility based on operand type
        if isinstance(node.op, uni.NegOp):
            self._check_neg_op_compatibility(operand_type, node)
        elif isinstance(node.op, uni.NotOp):
            # Not operator can be used with any type (Python-like behavior)
            pass

    def _check_neg_op_compatibility(
        self, operand_type: Type, node: uni.UnaryExpr
    ) -> None:
        """Check compatibility for the - unary operator."""
        # -int, -float
        if isinstance(operand_type, ClassType) and operand_type.fullname in [
            "builtins.int",
            "builtins.float",
        ]:
            return

        # Error for incompatible types
        self.log_error(
            f"Unary operator '-' not supported for type '{self._type_to_string(operand_type)}'",
            node_override=node,
        )

    def enter_if_stmt(self, node: uni.IfStmt) -> None:
        """Check type compatibility for if statements."""
        # In Python-like languages, any type can be used as a condition
        pass

    def enter_while_stmt(self, node: uni.WhileStmt) -> None:
        """Check type compatibility for while statements."""
        # In Python-like languages, any type can be used as a condition
        pass

    def enter_in_for_stmt(self, node: uni.InForStmt) -> None:
        """Check type compatibility for for statements."""
        # Check if the collection is iterable
        if hasattr(node, "collection"):
            collection_type = self.get_type(node.collection)
            if collection_type is None:
                return

            # Check if the collection type is iterable
            if not self._is_iterable_type(collection_type):
                self.log_error(
                    f"Type '{self._type_to_string(collection_type)}' is not iterable",
                    node_override=node.collection,
                )

    def _is_iterable_type(self, type_obj: Type) -> bool:
        """Check if a type is iterable."""
        if isinstance(type_obj, ClassType):
            iterable_types = [
                "builtins.list",
                "builtins.tuple",
                "builtins.set",
                "builtins.dict",
                "builtins.str",
            ]
            return type_obj.fullname in iterable_types
        return False

    def enter_index_slice(self, node: uni.IndexSlice) -> None:
        """Check type compatibility for index/slice operations."""
        # Get the type of the target
        parent = node.parent
        if not isinstance(parent, uni.AtomTrailer):
            return
        target_type = self.get_type(parent.target)
        if target_type is None:
            return

        # Check if the target type is indexable
        if not self._is_indexable_type(target_type):
            self.log_error(
                f"Type '{self._type_to_string(target_type)}' is not indexable",
                node_override=parent,
            )
            return

        # Check if the index is valid for the target type
        for slice_item in node.slices:
            if isinstance(slice_item, uni.Slice):
                # Check slice bounds
                if slice_item.lower:
                    lower_type = self.get_type(slice_item.lower)
                    if lower_type and not self._is_valid_index_type(lower_type):
                        self.log_error(
                            f"Slice lower bound must be an integer, not '{self._type_to_string(lower_type)}'",
                            node_override=slice_item.lower,
                        )
                if slice_item.upper:
                    upper_type = self.get_type(slice_item.upper)
                    if upper_type and not self._is_valid_index_type(upper_type):
                        self.log_error(
                            f"Slice upper bound must be an integer, not '{self._type_to_string(upper_type)}'",
                            node_override=slice_item.upper,
                        )
                if slice_item.step:
                    step_type = self.get_type(slice_item.step)
                    if step_type and not self._is_valid_index_type(step_type):
                        self.log_error(
                            f"Slice step must be an integer, not '{self._type_to_string(step_type)}'",
                            node_override=slice_item.step,
                        )
            else:
                # Check index
                index_type = self.get_type(slice_item)
                if index_type and not self._is_valid_index_type(index_type):
                    self.log_error(
                        f"Index must be an integer, not '{self._type_to_string(index_type)}'",
                        node_override=slice_item,
                    )

                # Special case for dictionaries
                if (
                    isinstance(target_type, ClassType)
                    and target_type.fullname == "builtins.dict"
                ):
                    # Any type can be a dictionary key, so no additional checks needed
                    pass

    def _is_indexable_type(self, type_obj: Type) -> bool:
        """Check if a type is indexable."""
        if isinstance(type_obj, ClassType):
            indexable_types = [
                "builtins.list",
                "builtins.tuple",
                "builtins.str",
                "builtins.dict",
            ]
            return type_obj.fullname in indexable_types
        return False

    def _is_valid_index_type(self, type_obj: Type) -> bool:
        """Check if a type is valid for indexing."""
        if isinstance(type_obj, ClassType):
            return type_obj.fullname == "builtins.int"
        return False

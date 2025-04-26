"""extracting/setting JType from Jac expressions"""

from typing import Optional

import jaclang.compiler.absyntree as ast
import jaclang.compiler.passes.typecheck.type as jtype
from jaclang.settings import settings
from jaclang.utils.helpers import pascal_to_snake


class JacExpressionType:
    """Extract/Set JType from Jac expressions"""

    def __debug_print(self, msg: str) -> None:
        if settings.jac_semantics:
            print("[JacExpressionType]", msg)

    def get_type(self, node: Optional[ast.Expr]) -> jtype.JType:
        """Get type from any jac expression based"""
        if node is None:
            return jtype.JNoneType()
        name = pascal_to_snake(node.__class__.__name__)
        func_name = f"__get_{name}_expr_type"
        if hasattr(self, func_name):
            return getattr(self, func_name)(node)
        else:
            print(func_name, "is not implemented yet")
        return jtype.JNoneType()

    def set_type(self, node: ast.Expr, expr_type: jtype.JType) -> None:
        """Set type from any jac expression based"""
        name = pascal_to_snake(node.__class__.__name__)
        func_name = f"__set_{name}_expr_type"
        if hasattr(self, func_name):
            self.__debug_print(f"Setting type {expr_type} to {node.loc}")
            return getattr(self, func_name)(node, expr_type)
        else:
            self.__debug_print(f"{func_name} is not implemented yet")

    def __get_name_expr_type(self, node: ast.Name) -> jtype.JType:
        assert node.name_spec.sym is not None
        return node.name_spec.sym.jtype

    def __get_int_expr_type(self, node: ast.Int) -> jtype.JType:
        return jtype.JIntType()

    def __get_float_expr_type(self, node: ast.Float) -> jtype.JType:
        return jtype.JFloatType()

    def __get_bool_expr_type(self, node: ast.Bool) -> jtype.JType:
        return jtype.JBoolType()

    def __get_multi_string_expr_type(self, node: ast.MultiString) -> jtype.JType:
        return jtype.JStrType()

    def __get_string_expr_type(self, node: ast.MultiString) -> jtype.JType:
        return jtype.JStrType()

    def __get_builtin_type_expr_type(self, node: ast.BuiltinType) -> jtype.JType:
        type_map = {
            "TYP_INT": jtype.JIntType,
            "TYP_FLOAT": jtype.JFloatType,
            "TYP_STRING": jtype.JStrType,
            "TYP_BOOL": jtype.JBoolType,
        }

        if node.name in type_map:
            return type_map[node.name]()
        else:
            return jtype.JNoType()

    def __get_func_call_expr_type(self, node: ast.FuncCall) -> jtype.JType:
        assert isinstance(node.target, ast.Name)
        assert node.target.name_spec.sym is not None
        return node.target.name_spec.sym.jtype

    def __set_name_expr_type(self, node: ast.Name, expr_type: jtype.JType) -> None:
        assert node.name_spec.sym is not None
        node.name_spec.sym.jtype = expr_type

    def __set_name_atom_expr_type(
        self, node: ast.NameAtom, expr_type: jtype.JType
    ) -> None:
        assert node.sym is not None
        node.sym.jtype = expr_type

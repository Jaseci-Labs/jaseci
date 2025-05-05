"""extracting/setting JType from Jac expressions."""

from typing import Optional, Type

import jaclang.compiler.passes.typecheck.jtype as jtype
import jaclang.compiler.unitree as ast
from jaclang.settings import settings
from jaclang.utils.helpers import pascal_to_snake


class JacExpressionType:
    """Extract/Set JType from Jac expressions."""

    def __debug_print(self, msg: str) -> None:
        if settings.debug_jac_semantics:
            print("[JacExpressionType]", msg)

    def get_type(self, node: Optional[ast.Expr]) -> jtype.JType:
        """Get type from any jac expression based."""
        if node is None:
            return jtype.JNoneType()
        name = pascal_to_snake(node.__class__.__name__)
        func_name = f"_get_{name}_expr_type"
        if hasattr(self, func_name):
            return getattr(self, func_name)(node)
        else:
            self.__debug_print(f"{func_name} is not implemented yet")
        return jtype.JNoneType()

    def set_type(self, node: ast.Expr, expr_type: jtype.JType) -> None:
        """Set type from any jac expression based."""
        name = pascal_to_snake(node.__class__.__name__)
        func_name = f"_set_{name}_expr_type"
        if hasattr(self, func_name):
            self.__debug_print(f"Setting type {expr_type} to {node.loc}")
            return getattr(self, func_name)(node, expr_type)
        else:
            self.__debug_print(f"{func_name} is not implemented yet")

    def _get_name_expr_type(self, node: ast.Name) -> jtype.JType:
        if node.name_spec.sym is None:
            return jtype.JNoType()
        return node.name_spec.sym.jtype

    def _get_int_expr_type(self, node: ast.Int) -> jtype.JType:
        return jtype.JIntType()

    def _get_float_expr_type(self, node: ast.Float) -> jtype.JType:
        return jtype.JFloatType()

    def _get_bool_expr_type(self, node: ast.Bool) -> jtype.JType:
        return jtype.JBoolType()

    def _get_multi_string_expr_type(self, node: ast.MultiString) -> jtype.JType:
        return jtype.JStrType()

    def _get_string_expr_type(self, node: ast.MultiString) -> jtype.JType:
        return jtype.JStrType()

    def _get_builtin_type_expr_type(self, node: ast.BuiltinType) -> jtype.JType:
        type_map: dict[str, Type[jtype.JType]] = {
            "TYP_INT": jtype.JIntType,
            "TYP_FLOAT": jtype.JFloatType,
            "TYP_STRING": jtype.JStrType,
            "TYP_BOOL": jtype.JBoolType,
        }

        if node.name in type_map:
            return type_map[node.name]()
        else:
            return jtype.JNoType()

    def _get_func_call_expr_type(self, node: ast.FuncCall) -> jtype.JType:
        func_type = self.get_type(node.target)
        assert isinstance(func_type, (jtype.JCallableType, jtype.JClassType))
        # In case of normal functions
        if isinstance(func_type, jtype.JCallableType):
            return func_type.return_type
        # In case of class constructor
        elif isinstance(func_type, jtype.JClassType):
            return jtype.JClassInstanceType(func_type)

    def _get_atom_trailer_expr_type(self, node: ast.AtomTrailer) -> jtype.JType:
        return self.get_type(node.as_attr_list[-1])

    def _set_name_expr_type(self, node: ast.Name, expr_type: jtype.JType) -> None:
        assert node.name_spec.sym is not None
        node.name_spec.sym.jtype = expr_type

    def _set_name_atom_expr_type(
        self, node: ast.NameAtom, expr_type: jtype.JType
    ) -> None:
        assert node.sym is not None
        node.sym.jtype = expr_type

    def _set_atom_trailer_expr_type(
        self, node: ast.AtomTrailer, expr_type: jtype.JType
    ) -> None:
        # assert False, "Types should be added as part of the name node"
        pass

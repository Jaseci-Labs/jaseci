"""extracting/setting JType from Jac expressions."""

from typing import Optional, Type

import jaclang.compiler.types as jtype
import jaclang.compiler.unitree as ast
from jaclang.compiler.types.registery import JTypeRegistry
from jaclang.settings import settings
from jaclang.utils.helpers import pascal_to_snake


class JTypeResolver:
    """Extract/Set JType from Jac expressions."""

    def __init__(self, type_registry: JTypeRegistry) -> None:
        """Initialize the JacTypeResolver."""
        self.type_registry = type_registry

    def __debug_print(self, msg: str) -> None:
        if settings.debug_jac_typing:
            print("[JacTypeResolver]", msg)

    def get_type(self, node: Optional[ast.Expr]) -> jtype.JType:
        """Get type from any jac expression."""
        if node is None:
            return jtype.JNoneType()
        
        name = pascal_to_snake(node.__class__.__name__)
        func_name = f"_get_{name}_expr_type"
        
        if hasattr(self, func_name):
            return getattr(self, func_name)(node)
        else:
            self.__debug_print(f"{func_name} is not implemented yet")
            return jtype.JAnyType()

    def set_type(self, node: ast.Expr, expr_type: jtype.JType) -> None:
        """Set type from any jac expression based."""
        name = pascal_to_snake(node.__class__.__name__)
        func_name = f"_set_{name}_expr_type"
        
        if hasattr(self, func_name):
            self.__debug_print(f"Setting type '{expr_type}' to {node.loc.mod_path}:{node.loc}")
            return getattr(self, func_name)(node, expr_type)
        else:
            self.__debug_print(f"{func_name} is not implemented yet")

    def _get_name_expr_type(self, node: ast.Name) -> jtype.JType:
        if node.name_spec.sym is None:
            return jtype.JAnyType()
        return node.name_spec.sym.jtype

    def _get_int_expr_type(self, node: ast.Int) -> jtype.JType:
        t = self.type_registry.get("builtins.int")
        assert isinstance(t, jtype.JClassType)
        return jtype.JClassInstanceType(t)

    def _get_float_expr_type(self, node: ast.Float) -> jtype.JType:
        t = self.type_registry.get("builtins.float")
        assert isinstance(t, jtype.JClassType)
        return jtype.JClassInstanceType(t)

    def _get_bool_expr_type(self, node: ast.Bool) -> jtype.JType:
        t = self.type_registry.get("builtins.bool")
        assert isinstance(t, jtype.JClassType)
        return jtype.JClassInstanceType(t)

    def _get_multi_string_expr_type(self, node: ast.MultiString) -> jtype.JType:
        t = self.type_registry.get("builtins.str")
        assert isinstance(t, jtype.JClassType)
        return jtype.JClassInstanceType(t)

    def _get_string_expr_type(self, node: ast.MultiString) -> jtype.JType:
        t = self.type_registry.get("builtins.str")
        assert isinstance(t, jtype.JClassType)
        return jtype.JClassInstanceType(t)
    
    def _get_null_expr_type(self, node: ast.Null) -> jtype.JType:
        return jtype.JNoneType()

    def _get_builtin_type_expr_type(self, node: ast.BuiltinType) -> jtype.JType:
        type_map: dict[str, str] = {
            "TYP_INT": "builtins.int",
            "TYP_FLOAT": "builtins.float",
            "TYP_STRING": "builtins.str",
            "TYP_BOOL": "builtins.bool",
        }

        t = self.type_registry.get(type_map[node.name])
        assert isinstance(t, jtype.JClassType)
        return jtype.JClassInstanceType(t)

    def _get_func_call_expr_type(self, node: ast.FuncCall) -> jtype.JType:
        func_type = self.get_type(node.target)
        assert isinstance(func_type, (jtype.JFunctionType, jtype.JClassType))
        
        # In case of normal functions
        if isinstance(func_type, jtype.JFunctionType):
            return func_type.return_type
        
        # In case of class constructor
        elif isinstance(func_type, jtype.JClassInstanceType):
            return func_type
        
        return jtype.JAnyType()


    def _set_name_expr_type(self, node: ast.Name, expr_type: jtype.JType) -> None:
        assert node.name_spec.sym is not None
        node.name_spec.sym.jtype = expr_type

    def _set_name_atom_expr_type(
        self, node: ast.NameAtom, expr_type: jtype.JType
    ) -> None:
        assert node.sym is not None
        node.sym.jtype = expr_type
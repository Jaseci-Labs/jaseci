from typing import Optional

import jaclang.compiler.absyntree as ast
import jaclang.compiler.passes.typecheck.type as jtype

from jaclang.utils.helpers import pascal_to_snake 


class JacExpressionType:
    def get_type(self, node: ast.Expr) -> Optional[jtype.JType]:
        name = pascal_to_snake(node.__class__.__name__)
        func_name = f"get_{name}_expr_type"
        if hasattr(self, func_name):
            return getattr(self, func_name)(node)
        return None
    
    def set_type(self, node: ast.Expr, expr_type: jtype.JType):
        self.set_name_expr_type(node, expr_type)

    def get_name_expr_type(self, node: ast.Name) -> jtype.JType:
        return node.name_spec.sym.jtype

    def get_int_expr_type(self, node: ast.Int) -> jtype.JType:
        return jtype.JIntType()

    def get_float_expr_type(self, node: ast.Float) -> jtype.JType:
        return jtype.JFloatType()
    
    def get_bool_expr_type(self, node: ast.Bool) -> jtype.JType:
        return jtype.JBoolType()

    def set_name_expr_type(self, node: ast.Name, expr_type: jtype.JType):
        node.name_spec.sym.jtype = expr_type


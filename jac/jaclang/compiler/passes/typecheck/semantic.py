from jaclang.compiler.passes import Pass

import jaclang.compiler.passes.typecheck.type as jtype
from jaclang.compiler.passes.typecheck.expr_type import JacExpressionType
import jaclang.compiler.absyntree as ast


class SemanticAnalysisPass(Pass):

    def before_pass(self):
        self.expr_check = JacExpressionType()

    # All variable definitions in Jac are handled as Assignment nodes
    def enter_assignment(self, node: ast.Assignment) -> None:
        target = node.target.items[0]
        type_annotation = node.type_tag.tag if node.type_tag else None
        value = node.value
        
        sym_type = self.expr_check.get_type(target)

        # type annotation exists
        # If the expr has type, then need to check that the annotation
        # is the same as expr type
        # If expr doesn't have type then set its' type to the annotated type
        if type_annotation:
            if sym_type is None:
                sym_type = jtype.getBuiltinType(type_annotation)
                self.expr_check.set_type(target, sym_type)
            else:
                annotation_type = jtype.getBuiltinType(type_annotation)
                if type(sym_type) is not type(annotation_type):
                    self.error(f"Can't redefine {target.sym_name} to be {annotation_type}")
        
        if value:
            value_type = self.expr_check.get_type(value)
            if not sym_type.is_assignable_from(value_type):
                self.error(f"Error: Can't assign a value {value_type} to a {sym_type} object")
            
        
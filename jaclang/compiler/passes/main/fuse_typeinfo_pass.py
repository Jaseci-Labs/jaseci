"""Integrate mypy infrastructure into Jac.

This is used to call mypy type checking into Jac files by integrating
mypy apis into Jac and use jac py ast in it.
"""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from mypy.types import Instance as mypyInstance

# import jaclang.compiler.passes.utils.mypy_ast_build as myab
# import mypy.nodes as mnodes


class FuseTypeInfo(Pass):
    """Python and bytecode file printing pass."""

    def __debug_print(self, *argv):
        print(f"FuseTypeInfo::", *argv)

    def __handle_node(self, node: ast.AstSymbolNode) -> None:
        try:
            if len(node.gen.mypy_ast) == 1:
                mypy_node = node.gen.mypy_ast[0].node
                mypy_type = mypy_node.type
                if isinstance(mypy_type, mypyInstance):
                    node.sym_info = ast.SymbolInfo(mypy_type)
                    self.__debug_print(f"FuseTypeInfo:: \"{node.__class__.__name__}::{node.value}\" type is \"{mypy_type}\"")
                else:
                    self.__debug_print(f"FuseTypeInfo:: {type(mypy_type)} isn't supported yet")
            elif len(node.gen.mypy_ast) > 1:
                self.__debug_print(f"FuseTypeInfo:: jac Name node \"{node.__class__.__name__}::{node.value}\" has multiple mypy nodes associated to it")
            else:
                self.__debug_print(f"FuseTypeInfo:: jac Name node \"{node.__class__.__name__}::{node.value}\" doesn't have mypy node associated to it")
        except:
            self.__debug_print(f"FuseTypeInfo:: Internal error with \"{node.__class__.__name__}::{node}\"")

    def enter_name(self, node: ast.Name) -> None:
        self.__handle_node(node)
    
    def enter_module_path(self, node: ast.ModulePath):
        self.__handle_node(node)
    
    def enter_module_item(self, node: ast.ModuleItem) -> None:
        self.__handle_node(node)
    
    def enter_architype(self, node: ast.Architype) -> None:
        self.__handle_node(node)
    
    def enter_arch_def(self, node: ast.ArchDef) -> None:
        self.__handle_node(node)
    
    def enter_enum(self, node: ast.Enum) -> None:
        self.__handle_node(node)
    
    def enter_enum_def(self, node: ast.EnumDef) -> None:
        self.__handle_node(node)

    def enter_ability(self, node: ast.Ability) -> None:
        self.__handle_node(node)

    def enter_ability_def(self, node: ast.AbilityDef) -> None:
        self.__handle_node(node)

    def enter_param_var(self, node: ast.ParamVar) -> None:
        self.__handle_node(node)

    def enter_has_var(self, node: ast.HasVar) -> None:
        self.__handle_node(node)
    
    def enter_multi_string(self, node: ast.MultiString) -> None:
        self.__handle_node(node)
    
    def enter_multi_string(self, node: ast.MultiString) -> None:
        self.__handle_node(node)

    def enter_f_string(self, node: ast.FString) -> None:
        self.__handle_node(node)

    def enter_list_val(self, node: ast.ListVal) -> None:
        self.__handle_node(node)

    def enter_set_val(self, node: ast.SetVal) -> None:
        self.__handle_node(node)

    def enter_tuple_val(self, node: ast.TupleVal) -> None:
        self.__handle_node(node)

    def enter_dict_val(self, node: ast.DictVal) -> None:
        self.__handle_node(node)

    def enter_list_compr(self, node: ast.ListCompr) -> None:
        self.__handle_node(node)

    def enter_dict_compr(self, node: ast.DictCompr) -> None:
        self.__handle_node(node)

    def enter_index_slice(self, node: ast.IndexSlice) -> None:
        self.__handle_node(node)

    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        self.__handle_node(node)

    def enter_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        self.__handle_node(node)

    def enter_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        self.__handle_node(node)

    def enter_filter_compr(self, node: ast.FilterCompr) -> None:
        self.__handle_node(node)

    def enter_assign_compr(self, node: ast.AssignCompr) -> None:
        self.__handle_node(node)
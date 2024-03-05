"""Integrate mypy infrastructure into Jac.

This is used to call mypy type checking into Jac files by integrating
mypy apis into Jac and use jac py ast in it.
"""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.utils.helpers import pascal_to_snake
import mypy.nodes as mypyNode
import mypy.types as mypyTypes
import os


class FuseTypeInfoPass(Pass):
    """Python and bytecode file self.__debug_printing pass."""

    def __debug_print(self, *argv):
        if "FuseTypeInfoDebug" in os.environ:
            print("FuseTypeInfo::", *argv)

    def __call_type_handler(
        self, node: ast.AstSymbolNode, mypy_type: mypyTypes.ProperType
    ):
        mypy_type_name = pascal_to_snake(mypy_type.__class__.__name__)
        type_handler_name = f"get_type_from_{mypy_type_name}"
        if hasattr(self, type_handler_name):
            getattr(self, type_handler_name)(node, mypy_type)
        else:
            self.__debug_print(
                f'"mypyTypes::{mypy_type.__class__.__name__}" isn\'t supported yet'
            )

    def __handle_node(func) -> None:
        def node_handler(self, node: ast.AstSymbolNode):
            try:
                if len(node.gen.mypy_ast) == 1:
                    func(self, node)
                elif len(node.gen.mypy_ast) > 1:
                    self.__debug_print(
                        f'jac node "{node.__class__.__name__}" has multiple mypy nodes associated to it'
                    )
                else:
                    self.__debug_print(
                        f'jac node "{node.__class__.__name__}" doesn\'t have mypy node associated to it'
                    )
            except AttributeError as e:
                self.__debug_print(
                    f'Internal error happened while parsing "{e.obj.__class__.__name__}"'
                )

        return node_handler

    @__handle_node
    def enter_name(self, node: ast.Name) -> None:
        mypy_node = node.gen.mypy_ast[0].node
        self.__call_type_handler(node, mypy_node.type)

    @__handle_node
    def enter_module_path(self, node: ast.ModulePath):
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_module_item(self, node: ast.ModuleItem) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_architype(self, node: ast.Architype) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_arch_def(self, node: ast.ArchDef) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_enum(self, node: ast.Enum) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_enum_def(self, node: ast.EnumDef) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_ability(self, node: ast.Ability) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_ability_def(self, node: ast.AbilityDef) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_param_var(self, node: ast.ParamVar) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_has_var(self, node: ast.HasVar) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_multi_string(self, node: ast.MultiString) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_f_string(self, node: ast.FString) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_list_val(self, node: ast.ListVal) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_set_val(self, node: ast.SetVal) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_tuple_val(self, node: ast.TupleVal) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_dict_val(self, node: ast.DictVal) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_list_compr(self, node: ast.ListCompr) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_dict_compr(self, node: ast.DictCompr) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_index_slice(self, node: ast.IndexSlice) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_filter_compr(self, node: ast.FilterCompr) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_assign_compr(self, node: ast.AssignCompr) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_func_call(self, node: ast.FuncCall) -> None:
        mypy_node: mypyNode.CallExpr = node.gen.mypy_ast[0]
        callee: mypyNode.NameExpr = mypy_node.callee
        if isinstance(callee.node, (mypyNode.FuncDef, mypyNode.OverloadedFuncDef)):
            self.__call_type_handler(node, callee.node.type)
        else:
            self.__debug_print(
                f'"{node.__class__.__name__}" mypy node isn\'t "FuncDef"',
                type(callee.node),
            )

    def get_type_from_instance(
        self, node: ast.AstSymbolNode, mypy_type: mypyTypes.Instance
    ):
        node.sym_info = ast.SymbolInfo(mypy_type)
        self.__debug_print(
            f'"{node.__class__.__name__}::{node.value}" type is "{mypy_type}"'
        )
        self.__debug_print(id(node))

    def get_type_from_callable_type(
        self, node: ast.AstSymbolNode, mypy_type: mypyTypes.CallableType
    ):
        node.sym_info = ast.SymbolInfo(mypy_type.ret_type)
        self.__debug_print(
            f'"{node.__class__.__name__}" type is "{mypy_type.ret_type}"'
        )
        self.__debug_print(id(node))

    # def get_type_from_overloaded(self, node: ast.AstSymbolNode, mypy_type: mypyTypes.Overloaded):
    #     node.sym_info = ast.SymbolInfo(mypy_type.ret_type)
    #     self.__debug_print(f"\"{node.__class__.__name__}\" type is \"{mypy_type.ret_type}\"")
    #     # self.__debug_print(id(node))

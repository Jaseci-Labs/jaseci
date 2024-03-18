"""Integrate mypy infrastructure into Jac.

This is used to call mypy type checking into Jac files by integrating
mypy apis into Jac and use jac py ast in it.
"""

from __future__ import annotations

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.utils.helpers import pascal_to_snake
import mypy.nodes as mypyNode
import mypy.types as mypyTypes
import os

import traceback


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
                f'{node.loc}"mypyTypes::{mypy_type.__class__.__name__}" isn\'t supported yet'
            )

    def __set_sym_table_link(self, node: ast.AstSymbolNode):
        typ = node.sym_info.typ.split(".")
        typ_sym_table = self.ir.sym_tab
        if typ[0] == typ_sym_table.name:
            for i in typ[1:]:
                f = typ_sym_table.find_scope(i)
                if f:
                    typ_sym_table = f

        if typ_sym_table != self.ir.sym_tab:
            node.sym_info.typ_sym_table = typ_sym_table

    @staticmethod
    def __handle_node(func):
        def node_handler(self: FuseTypeInfoPass, node: ast.AstSymbolNode):
            if not isinstance(node, ast.AstSymbolNode):
                print(f"Warning {node.__class__.__name__} is not an AstSymbolNode")
            
            try:
                jac_node_str = f'jac node "{node.loc}::{node.__class__.__name__}' 
                if hasattr(node, "value"):
                    jac_node_str += f'::{node.value}"'
                else:
                    jac_node_str += '"'

                # Jac node has only one mypy node linked to it
                if len(node.gen.mypy_ast) == 1:
                    func(self, node)
                    self.__set_sym_table_link(node)
                
                # Jac node has multiple mypy nodes linked to it
                elif len(node.gen.mypy_ast) > 1:
                    # Checking that these nodes are duplicate or not
                    temp = []
                    for n in node.gen.mypy_ast:
                        n_id = f"{type(node)}"
                        n_id += f"::{n.line}::{n.column}"
                        n_id += f" - {n.end_line}::{n.end_column}"
                        if n_id not in temp:
                            temp.append(n_id)

                    # Check the number of unique mypy nodes linked
                    if len(temp) > 1:
                        self.__debug_print(jac_node_str, "has multiple mypy nodes associated to it")
                    else:
                        # self.__debug_print(jac_node_str, "has duplicate mypy nodes associated to it")
                        func(self, node)
                        self.__set_sym_table_link(node)

                # Jac node doesn't have mypy nodes linked to it
                else:
                    self.__debug_print(jac_node_str, "doesn\'t have mypy node associated to it")

            except AttributeError as e:
                self.__debug_print(
                    f'Internal error happened while parsing "{e.obj.__class__.__name__}"'
                )
                traceback.print_exc()
                print(e)
        return node_handler

    def enter_import(self, node: ast.Import):
        # Pruning the import nodes
        self.prune()

    @__handle_node
    def enter_name(self, node: ast.Name) -> None:
        mypy_node = node.gen.mypy_ast[0] 
        
        if hasattr(mypy_node, "node"):
            orig_node = mypy_node
            mypy_node = mypy_node.node

            if isinstance(mypy_node, (mypyNode.Var, mypyNode.FuncDef)):
                self.__call_type_handler(node, mypy_node.type)

            elif isinstance(mypy_node, mypyNode.MypyFile):
                node.sym_info = ast.SymbolInfo("types.ModuleType")

            elif isinstance(mypy_node, mypyNode.TypeInfo):
                node.sym_info = ast.SymbolInfo(mypy_node.fullname)

            elif isinstance(mypy_node, mypyNode.OverloadedFuncDef):
                self.__call_type_handler(node, mypy_node.items[0].func.type)

            else:
                self.__debug_print(
                    f'"{node.loc}::{node.__class__.__name__}" mypy (with node attr) node isn\'t supported',
                    type(mypy_node),
                )
        
        else:
            if isinstance(mypy_node, mypyNode.ClassDef):
                mypy_node: mypyNode.ClassDef = node.gen.mypy_ast[0]
                node.sym_info.typ = mypy_node.fullname
                self.__set_sym_table_link(node)
            elif isinstance(mypy_node, mypyNode.FuncDef):
                self.__call_type_handler(node, mypy_node.type)
            elif isinstance(mypy_node, mypyNode.Argument):
                self.__call_type_handler(node, mypy_node.variable.type)
            else:
                self.__debug_print(
                    f'"{node.loc}::{node.__class__.__name__}" mypy node isn\'t supported',
                    type(mypy_node),
                )

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
        self.__call_type_handler(node, node.gen.mypy_ast[0].type.ret_type)

    @__handle_node
    def enter_ability_def(self, node: ast.AbilityDef) -> None:
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_param_var(self, node: ast.ParamVar) -> None:
        mypy_node: mypyNode.Argument = node.gen.mypy_ast[0]
        self.__call_type_handler(node, mypy_node.variable.type)

    # TODO: support all lhs if needed
    @__handle_node
    def enter_has_var(self, node: ast.HasVar) -> None:
        mypy_node = node.gen.mypy_ast[0]
        if isinstance(mypy_node, mypyNode.AssignmentStmt):
            n = mypy_node.lvalues[0].node
            if isinstance(n, (mypyNode.Var, mypyNode.FuncDef)):
                self.__call_type_handler(node, n.type)
            else:
                self.__debug_print(
                    "Getting type of 'AssignmentStmt' is only supported with Var and FuncDef"
                )
        else:
            self.__debug_print(
                "Getting type of 'HasVar' is only supported with AssignmentStmt"
            )

    @__handle_node
    def enter_multi_string(self, node: ast.MultiString) -> None:
        node.sym_info = ast.SymbolInfo("builtins.str")

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
        mypy_node: mypyNode.ClassDef = node.gen.mypy_ast[0]
        node.sym_info.typ = mypy_node.fullname
        self.__set_sym_table_link(node)

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
    def enter_int(self, node: ast.Int) -> None:
        node.sym_info.typ = "builtins.int"
    
    @__handle_node
    def enter_int(self, node: ast.Int) -> None:
        node.sym_info.typ = "builtins.int"

    @__handle_node
    def enter_float(self, node: ast.Float) -> None:
        node.sym_info.typ = "builtins.float"
    
    @__handle_node
    def enter_string(self, node: ast.String) -> None:
        node.sym_info.typ = "builtins.str"
    
    @__handle_node
    def enter_bool(self, node: ast.Bool) -> None:
        node.sym_info.typ = "builtins.bool"
    
    @__handle_node
    def enter_builtin_type(self, node: ast.BuiltinType) -> None:
        self.__debug_print("Getting type not supported in", type(node))
    
    def get_type_from_instance(
        self, node: ast.AstSymbolNode, mypy_type: mypyTypes.Instance
    ):
        node.sym_info = ast.SymbolInfo(str(mypy_type))

    def get_type_from_callable_type(
        self, node: ast.AstSymbolNode, mypy_type: mypyTypes.CallableType
    ):
        node.sym_info = ast.SymbolInfo(str(mypy_type.ret_type))

    # TODO: Which overloaded function to get the return value from?
    def get_type_from_overloaded(
        self, node: ast.AstSymbolNode, mypy_type: mypyTypes.Overloaded
    ):
        self.__call_type_handler(node, mypy_type.items[0])

    def get_type_from_none_type(
        self, node: ast.AstSymbolNode, mypy_type: mypyTypes.NoneType
    ):
        node.sym_info = ast.SymbolInfo("None")

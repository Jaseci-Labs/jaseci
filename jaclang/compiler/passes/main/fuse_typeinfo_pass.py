"""Integrate mypy infrastructure into Jac.

This is used to call mypy type checking into Jac files by integrating
mypy apis into Jac and use jac py ast in it.
"""

from __future__ import annotations

import traceback
from typing import Callable, TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.settings import settings
from jaclang.utils.helpers import pascal_to_snake
from jaclang.vendor.mypy.nodes import Node as VNode  # bit of a hack


import mypy.nodes as MypyNodes  # noqa N812
import mypy.types as MypyTypes  # noqa N812
from mypy.checkexpr import Type as MyType


T = TypeVar("T", bound=ast.AstSymbolNode)


class FuseTypeInfoPass(Pass):
    """Python and bytecode file self.__debug_printing pass."""

    node_type_hash: dict[MypyNodes.Node | VNode, MyType] = {}

    def __debug_print(self, *argv: object) -> None:
        if settings.fuse_type_info_debug:
            print("FuseTypeInfo::", *argv)

    def __call_type_handler(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.ProperType
    ) -> None:
        mypy_type_name = pascal_to_snake(mypy_type.__class__.__name__)
        type_handler_name = f"get_type_from_{mypy_type_name}"
        if hasattr(self, type_handler_name):
            getattr(self, type_handler_name)(node, mypy_type)
        else:
            self.__debug_print(
                f'{node.loc}"MypyTypes::{mypy_type.__class__.__name__}" isn\'t supported yet'
            )

    def __set_sym_table_link(self, node: ast.AstSymbolNode) -> None:
        typ = node.sym_info.typ.split(".")
        typ_sym_table = self.ir.sym_tab
        if typ_sym_table and typ[0] == typ_sym_table.name:
            for i in typ[1:]:
                f = typ_sym_table.find_scope(i)
                if f:
                    typ_sym_table = f

        if typ_sym_table != self.ir.sym_tab:
            node.sym_info.typ_sym_table = typ_sym_table

    @staticmethod
    def __handle_node(
        func: Callable[[FuseTypeInfoPass, T], None]
    ) -> Callable[[FuseTypeInfoPass, T], None]:
        def node_handler(self: FuseTypeInfoPass, node: T) -> None:
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
                        self.__debug_print(
                            jac_node_str, "has multiple mypy nodes associated to it"
                        )
                    else:
                        self.__debug_print(
                            jac_node_str, "has duplicate mypy nodes associated to it"
                        )
                        func(self, node)
                        self.__set_sym_table_link(node)

                # Jac node doesn't have mypy nodes linked to it
                else:
                    self.__debug_print(
                        jac_node_str, "doesn't have mypy node associated to it"
                    )

            except AttributeError as e:
                self.__debug_print(
                    f'Internal error happened while parsing "{e.obj.__class__.__name__}"'
                )
                traceback.print_exc()
                print(e)

        return node_handler

    def __collect_type_from_symbol(self, node: ast.AstSymbolNode) -> None:
        mypy_node = node.gen.mypy_ast[0]

        if hasattr(mypy_node, "node"):
            # orig_node = mypy_node
            mypy_node = mypy_node.node

            if isinstance(mypy_node, (MypyNodes.Var, MypyNodes.FuncDef)):
                self.__call_type_handler(node, mypy_node.type)

            elif isinstance(mypy_node, MypyNodes.MypyFile):
                node.sym_info = ast.SymbolInfo("types.ModuleType")

            elif isinstance(mypy_node, MypyNodes.TypeInfo):
                node.sym_info = ast.SymbolInfo(mypy_node.fullname)

            elif isinstance(mypy_node, MypyNodes.OverloadedFuncDef):
                self.__call_type_handler(node, mypy_node.items[0].func.type)

            elif mypy_node is None:
                node.sym_info = ast.SymbolInfo("None")

            else:
                self.__debug_print(
                    f'"{node.loc}::{node.__class__.__name__}" mypy (with node attr) node isn\'t supported',
                    type(mypy_node),
                )

        else:
            if isinstance(mypy_node, MypyNodes.ClassDef):
                node.sym_info.typ = mypy_node.fullname
                self.__set_sym_table_link(node)
            elif isinstance(mypy_node, MypyNodes.FuncDef):
                self.__call_type_handler(node, mypy_node.type)
            elif isinstance(mypy_node, MypyNodes.Argument):
                self.__call_type_handler(node, mypy_node.variable.type)
            elif isinstance(mypy_node, MypyNodes.Decorator):
                self.__call_type_handler(node, mypy_node.func.type.ret_type)
            else:
                self.__debug_print(
                    f'"{node.loc}::{node.__class__.__name__}" mypy node isn\'t supported',
                    type(mypy_node),
                )

    def enter_import(self, node: ast.Import) -> None:
        """Pass handler for import nodes."""
        # Pruning the import nodes
        self.prune()

    @__handle_node
    def enter_name(self, node: ast.NameSpec) -> None:
        """Pass handler for name nodes."""
        self.__collect_type_from_symbol(node)

    @__handle_node
    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Pass handler for ModulePath nodes."""
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_module_item(self, node: ast.ModuleItem) -> None:
        """Pass handler for ModuleItem nodes."""
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_architype(self, node: ast.Architype) -> None:
        """Pass handler for Architype nodes."""
        self.__collect_type_from_symbol(node)

    @__handle_node
    def enter_arch_def(self, node: ast.ArchDef) -> None:
        """Pass handler for ArchDef nodes."""
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_enum(self, node: ast.Enum) -> None:
        """Pass handler for Enum nodes."""
        self.__collect_type_from_symbol(node)

    @__handle_node
    def enter_enum_def(self, node: ast.EnumDef) -> None:
        """Pass handler for EnumDef nodes."""
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_ability(self, node: ast.Ability) -> None:
        """Pass handler for Ability nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.FuncDef):
            self.__call_type_handler(node, node.gen.mypy_ast[0].type.ret_type)
        else:
            self.__debug_print(
                f"{node.loc}: Can't get type of an ability from mypy node other than Ability.",
                type(node.gen.mypy_ast[0]),
            )

    @__handle_node
    def enter_ability_def(self, node: ast.AbilityDef) -> None:
        """Pass handler for AbilityDef nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.FuncDef):
            self.__call_type_handler(node, node.gen.mypy_ast[0].type.ret_type)
        else:
            self.__debug_print(
                f"{node.loc}: Can't get type of an AbilityDef from mypy node other than FuncDef.",
                type(node.gen.mypy_ast[0]),
            )

    @__handle_node
    def enter_param_var(self, node: ast.ParamVar) -> None:
        """Pass handler for ParamVar nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.Argument):
            mypy_node: MypyNodes.Argument = node.gen.mypy_ast[0]
            if mypy_node.variable.type:
                self.__call_type_handler(node, mypy_node.variable.type)
        else:
            self.__debug_print(
                f"{node.loc}: Can't get parameter value from mypyNode other than Argument"
            )

    # TODO: support all lhs if needed
    @__handle_node
    def enter_has_var(self, node: ast.HasVar) -> None:
        """Pass handler for HasVar nodes."""
        mypy_node = node.gen.mypy_ast[0]
        if isinstance(mypy_node, MypyNodes.AssignmentStmt):
            n = mypy_node.lvalues[0].node
            if isinstance(n, (MypyNodes.Var, MypyNodes.FuncDef)):
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
        """Pass handler for MultiString nodes."""
        node.sym_info = ast.SymbolInfo("builtins.str")

    @__handle_node
    def enter_f_string(self, node: ast.FString) -> None:
        """Pass handler for FString nodes."""
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_list_val(self, node: ast.ListVal) -> None:
        """Pass handler for ListVal nodes."""
        mypy_node = node.gen.mypy_ast[0]
        if mypy_node in self.node_type_hash:
            node.sym_info.typ = str(self.node_type_hash[mypy_node])
        else:
            node.sym_info.typ = "builtins.list"

    @__handle_node
    def enter_set_val(self, node: ast.SetVal) -> None:
        """Pass handler for SetVal nodes."""
        mypy_node = node.gen.mypy_ast[0]
        if mypy_node in self.node_type_hash:
            node.sym_info.typ = str(self.node_type_hash[mypy_node])
        else:
            node.sym_info.typ = "builtins.set"

    @__handle_node
    def enter_tuple_val(self, node: ast.TupleVal) -> None:
        """Pass handler for TupleVal nodes."""
        mypy_node = node.gen.mypy_ast[0]
        if mypy_node in self.node_type_hash:
            node.sym_info.typ = str(self.node_type_hash[mypy_node])
        else:
            node.sym_info.typ = "builtins.tuple"

    @__handle_node
    def enter_dict_val(self, node: ast.DictVal) -> None:
        """Pass handler for DictVal nodes."""
        mypy_node = node.gen.mypy_ast[0]
        if mypy_node in self.node_type_hash:
            node.sym_info.typ = str(self.node_type_hash[mypy_node])
        else:
            node.sym_info.typ = "builtins.dict"

    @__handle_node
    def enter_list_compr(self, node: ast.ListCompr) -> None:
        """Pass handler for ListCompr nodes."""
        mypy_node = node.gen.mypy_ast[0]
        node.sym_info.typ = str(self.node_type_hash[mypy_node])

    @__handle_node
    def enter_dict_compr(self, node: ast.DictCompr) -> None:
        """Pass handler for DictCompr nodes."""
        mypy_node = node.gen.mypy_ast[0]
        node.sym_info.typ = str(self.node_type_hash[mypy_node])

    @__handle_node
    def enter_index_slice(self, node: ast.IndexSlice) -> None:
        """Pass handler for IndexSlice nodes."""
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        """Pass handler for ArchRef nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.ClassDef):
            mypy_node: MypyNodes.ClassDef = node.gen.mypy_ast[0]
            node.sym_info.typ = mypy_node.fullname
            self.__set_sym_table_link(node)
        elif isinstance(node.gen.mypy_ast[0], MypyNodes.FuncDef):
            mypy_node2: MypyNodes.FuncDef = node.gen.mypy_ast[0]
            self.__call_type_handler(node, mypy_node2.type)
        else:
            self.__debug_print(
                f"{node.loc}: Can't get ArchRef value from mypyNode other than ClassDef",
                type(node.gen.mypy_ast[0]),
            )

    @__handle_node
    def enter_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        """Pass handler for SpecialVarRef nodes."""
        return self.enter_name(node)

    @__handle_node
    def enter_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Pass handler for EdgeOpRef nodes."""
        self.__collect_type_from_symbol(node)

    @__handle_node
    def enter_filter_compr(self, node: ast.FilterCompr) -> None:
        """Pass handler for FilterCompr nodes."""
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_assign_compr(self, node: ast.AssignCompr) -> None:
        """Pass handler for AssignCompr nodes."""
        self.__debug_print("Getting type not supported in", type(node))

    @__handle_node
    def enter_int(self, node: ast.Int) -> None:
        """Pass handler for Int nodes."""
        node.sym_info.typ = "builtins.int"

    @__handle_node
    def enter_float(self, node: ast.Float) -> None:
        """Pass handler for Float nodes."""
        node.sym_info.typ = "builtins.float"

    @__handle_node
    def enter_string(self, node: ast.String) -> None:
        """Pass handler for String nodes."""
        node.sym_info.typ = "builtins.str"

    @__handle_node
    def enter_bool(self, node: ast.Bool) -> None:
        """Pass handler for Bool nodes."""
        node.sym_info.typ = "builtins.bool"

    @__handle_node
    def enter_builtin_type(self, node: ast.BuiltinType) -> None:
        """Pass handler for BuiltinType nodes."""
        self.__collect_type_from_symbol(node)

    def get_type_from_instance(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.Instance
    ) -> None:
        """Get type info from mypy type Instance."""
        node.sym_info = ast.SymbolInfo(str(mypy_type))

    def get_type_from_callable_type(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.CallableType
    ) -> None:
        """Get type info from mypy type CallableType."""
        node.sym_info = ast.SymbolInfo(str(mypy_type.ret_type))

    # TODO: Which overloaded function to get the return value from?
    def get_type_from_overloaded(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.Overloaded
    ) -> None:
        """Get type info from mypy type Overloaded."""
        self.__call_type_handler(node, mypy_type.items[0])

    def get_type_from_none_type(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.NoneType
    ) -> None:
        """Get type info from mypy type NoneType."""
        node.sym_info = ast.SymbolInfo("None")

    def get_type_from_any_type(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.AnyType
    ) -> None:
        """Get type info from mypy type NoneType."""
        node.sym_info = ast.SymbolInfo("Any")

    def get_type_from_tuple_type(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.TupleType
    ) -> None:
        """Get type info from mypy type TupleType."""
        node.sym_info = ast.SymbolInfo("builtins.tuple")

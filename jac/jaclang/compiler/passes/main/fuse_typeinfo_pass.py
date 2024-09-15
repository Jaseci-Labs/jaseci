"""Integrate mypy infrastructure into Jac.

This is used to call mypy type checking into Jac files by integrating
mypy apis into Jac and use jac py ast in it.
"""

from __future__ import annotations

import re
from typing import Callable, Optional, TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.symtable import SymbolTable
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

    def __debug_print(self, msg: str) -> None:
        if settings.fuse_type_info_debug:
            self.log_info("FuseTypeInfo::" + msg)

    def __call_type_handler(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.Type
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
        typ_sym_table = self.ir.sym_tab
        assert isinstance(self.ir, ast.Module)

        sym_type = node.sym_type
        if re.match(r"builtins.(list|dict|tuple)", sym_type):
            sym_type = re.sub(r"\[.*\]", "", sym_type)

        typ = sym_type.split(".")

        if node.sym_type == "types.ModuleType" and node.sym:
            node.name_spec.type_sym_tab = node.sym.parent_tab.find_scope(node.sym_name)

        for i in typ:
            if i == self.ir.name:
                continue
            f = typ_sym_table.find_scope(i)
            if f:
                typ_sym_table = f

        if typ_sym_table != self.ir.sym_tab:
            node.name_spec.type_sym_tab = typ_sym_table

    def __collect_python_dependencies(self, node: ast.AstNode) -> None:
        assert isinstance(node, ast.AstSymbolNode)
        assert isinstance(self.ir, ast.Module)

        mypy_node = node.gen.mypy_ast[0]

        if isinstance(mypy_node, MypyNodes.RefExpr) and mypy_node.node:
            node_full_name = mypy_node.node.fullname
            if "." in node_full_name:
                mod_name = node_full_name[: node_full_name.rindex(".")]
            else:
                mod_name = node_full_name

            if mod_name not in self.ir.py_mod_dep_map:
                self.__debug_print(
                    f"Can't find a python file associated with {type(node)}::{node.loc}"
                )
                return

            mode_path = self.ir.py_mod_dep_map[mod_name]
            if mode_path.endswith(".jac"):
                return

            self.ir.py_raise_map[mod_name] = mode_path
        else:
            self.__debug_print(
                f"Collect python dependencies is not supported in {type(node)}::{node.loc}"
            )

    @staticmethod
    def __handle_node(
        func: Callable[[FuseTypeInfoPass, T], None]
    ) -> Callable[[FuseTypeInfoPass, T], None]:
        def node_handler(self: FuseTypeInfoPass, node: T) -> None:
            if not isinstance(node, ast.AstSymbolNode):
                self.__debug_print(
                    f"Warning {node.__class__.__name__} is not an AstSymbolNode"
                )

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
                    self.__collect_python_dependencies(node)

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
                            f"{jac_node_str} has multiple mypy nodes associated to it"
                        )
                    else:
                        self.__debug_print(
                            f"{jac_node_str} has duplicate mypy nodes associated to it"
                        )
                        func(self, node)
                        self.__set_sym_table_link(node)
                        self.__collect_python_dependencies(node)

                # Special handing for BuiltinType
                elif isinstance(node, ast.BuiltinType):
                    func(self, node)  # type: ignore
                    self.__set_sym_table_link(node)

                # Jac node doesn't have mypy nodes linked to it
                else:
                    self.__debug_print(
                        f"{jac_node_str} doesn't have mypy node associated to it"
                    )

            except AttributeError as e:
                if settings.fuse_type_info_debug:
                    raise e
                self.__debug_print(
                    f'{node.loc}: Internal error happened while parsing "{e.obj.__class__.__name__}"'
                )

        return node_handler

    def __collect_type_from_symbol(self, node: ast.AstSymbolNode) -> None:
        mypy_node = node.gen.mypy_ast[0]

        if isinstance(mypy_node, MypyNodes.MemberExpr):
            if mypy_node in self.node_type_hash:
                self.__call_type_handler(node, self.node_type_hash[mypy_node])
            else:
                self.__debug_print(f"{node.loc} MemberExpr type is not found")

        elif hasattr(mypy_node, "node"):
            # orig_node = mypy_node
            mypy_node = mypy_node.node

            if isinstance(mypy_node, (MypyNodes.Var, MypyNodes.FuncDef)):
                self.__call_type_handler(node, mypy_node.type)

            elif isinstance(mypy_node, MypyNodes.MypyFile):
                node.name_spec.sym_type = "types.ModuleType"

            elif isinstance(mypy_node, MypyNodes.TypeInfo):
                node.name_spec.sym_type = mypy_node.fullname

            elif isinstance(mypy_node, MypyNodes.OverloadedFuncDef):
                self.__call_type_handler(node, mypy_node.items[0].func.type)

            elif mypy_node is None:
                node.name_spec.sym_type = "None"

            else:
                self.__debug_print(
                    f'"{node.loc}::{node.__class__.__name__}" mypy (with node attr) node isn\'t supported'
                    f"{type(mypy_node)}"
                )

        else:
            if isinstance(mypy_node, MypyNodes.ClassDef):
                node.name_spec.sym_type = mypy_node.fullname
                self.__set_sym_table_link(node)
            elif isinstance(mypy_node, MypyNodes.FuncDef):
                self.__call_type_handler(node, mypy_node.type)
            elif isinstance(mypy_node, MypyNodes.Argument):
                self.__call_type_handler(node, mypy_node.variable.type)
            elif isinstance(mypy_node, MypyNodes.Decorator):
                self.__call_type_handler(node, mypy_node.func.type.ret_type)
            else:
                self.__debug_print(
                    f'"{node.loc}::{node.__class__.__name__}" mypy node isn\'t supported'
                    f"{type(mypy_node)}"
                )

    def __check_builltin_symbol(self, node: ast.NameAtom) -> None:
        if isinstance(node.parent, ast.AtomTrailer) and node is node.parent.right:
            return
        builtins_sym_tab = self.ir.sym_tab.find_scope("builtins")
        assert builtins_sym_tab is not None
        builtins_sym = builtins_sym_tab.lookup(node.sym_name)
        if builtins_sym:
            node.name_spec._sym = builtins_sym

    @__handle_node
    def enter_name(self, node: ast.NameAtom) -> None:
        """Pass handler for name nodes."""
        self.__collect_type_from_symbol(node)
        if node.sym is None:
            self.__check_builltin_symbol(node)

    @__handle_node
    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Pass handler for ModulePath nodes."""
        self.__debug_print(f"Getting type not supported in {type(node)}")

    @__handle_node
    def enter_module_item(self, node: ast.ModuleItem) -> None:
        """Pass handler for ModuleItem nodes."""
        self.__debug_print(f"Getting type not supported in {type(node)}")

    @__handle_node
    def enter_architype(self, node: ast.Architype) -> None:
        """Pass handler for Architype nodes."""
        self.__collect_type_from_symbol(node)

    @__handle_node
    def enter_arch_def(self, node: ast.ArchDef) -> None:
        """Pass handler for ArchDef nodes."""
        self.__debug_print(f"Getting type not supported in {type(node)}")

    @__handle_node
    def enter_enum(self, node: ast.Enum) -> None:
        """Pass handler for Enum nodes."""
        self.__collect_type_from_symbol(node)

    @__handle_node
    def enter_enum_def(self, node: ast.EnumDef) -> None:
        """Pass handler for EnumDef nodes."""
        self.__debug_print(f"Getting type not supported in {type(node)}")

    @__handle_node
    def enter_ability(self, node: ast.Ability) -> None:
        """Pass handler for Ability nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.FuncDef):
            self.__call_type_handler(node, node.gen.mypy_ast[0].type.ret_type)
        else:
            self.__debug_print(
                f"{node.loc}: Can't get type of an ability from mypy node other than Ability. "
                f"{type(node.gen.mypy_ast[0])}"
            )

    @__handle_node
    def enter_ability_def(self, node: ast.AbilityDef) -> None:
        """Pass handler for AbilityDef nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.FuncDef):
            self.__call_type_handler(node, node.gen.mypy_ast[0].type.ret_type)
        else:
            self.__debug_print(
                f"{node.loc}: Can't get type of an AbilityDef from mypy node other than FuncDef. "
                f"{type(node.gen.mypy_ast[0])}"
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

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Pass handler for HasVar nodes."""
        node.name_spec.sym_type = node.name.sym_type
        node.name_spec.type_sym_tab = node.name.type_sym_tab

    @__handle_node
    def enter_multi_string(self, node: ast.MultiString) -> None:
        """Pass handler for MultiString nodes."""
        node.name_spec.sym_type = "builtins.str"

    @__handle_node
    def enter_f_string(self, node: ast.FString) -> None:
        """Pass handler for FString nodes."""
        self.__debug_print(f"Getting type not supported in {type(node)}")

    @__handle_node
    def enter_list_val(self, node: ast.ListVal) -> None:
        """Pass handler for ListVal nodes."""
        mypy_node = node.gen.mypy_ast[0]
        if mypy_node in self.node_type_hash:
            node.name_spec.sym_type = str(self.node_type_hash[mypy_node])
        else:
            node.name_spec.sym_type = "builtins.list"

    @__handle_node
    def enter_set_val(self, node: ast.SetVal) -> None:
        """Pass handler for SetVal nodes."""
        mypy_node = node.gen.mypy_ast[0]
        if mypy_node in self.node_type_hash:
            node.name_spec.sym_type = str(self.node_type_hash[mypy_node])
        else:
            node.name_spec.sym_type = "builtins.set"

    @__handle_node
    def enter_tuple_val(self, node: ast.TupleVal) -> None:
        """Pass handler for TupleVal nodes."""
        mypy_node = node.gen.mypy_ast[0]
        if mypy_node in self.node_type_hash:
            node.name_spec.sym_type = str(self.node_type_hash[mypy_node])
        else:
            node.name_spec.sym_type = "builtins.tuple"

    @__handle_node
    def enter_dict_val(self, node: ast.DictVal) -> None:
        """Pass handler for DictVal nodes."""
        mypy_node = node.gen.mypy_ast[0]
        if mypy_node in self.node_type_hash:
            node.name_spec.sym_type = str(self.node_type_hash[mypy_node])
        else:
            node.name_spec.sym_type = "builtins.dict"

    @__handle_node
    def enter_list_compr(self, node: ast.ListCompr) -> None:
        """Pass handler for ListCompr nodes."""
        mypy_node = node.gen.mypy_ast[0]
        node.name_spec.sym_type = str(self.node_type_hash[mypy_node])

    @__handle_node
    def enter_dict_compr(self, node: ast.DictCompr) -> None:
        """Pass handler for DictCompr nodes."""
        mypy_node = node.gen.mypy_ast[0]
        node.name_spec.sym_type = str(self.node_type_hash[mypy_node])

    @__handle_node
    def enter_index_slice(self, node: ast.IndexSlice) -> None:
        """Pass handler for IndexSlice nodes."""
        self.__debug_print(f"Getting type not supported in {type(node)}")

    @__handle_node
    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        """Pass handler for ArchRef nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.ClassDef):
            mypy_node: MypyNodes.ClassDef = node.gen.mypy_ast[0]
            node.name_spec.sym_type = mypy_node.fullname
            self.__set_sym_table_link(node)
        elif isinstance(node.gen.mypy_ast[0], MypyNodes.FuncDef):
            mypy_node2: MypyNodes.FuncDef = node.gen.mypy_ast[0]
            self.__call_type_handler(node, mypy_node2.type)
        else:
            self.__debug_print(
                f"{node.loc}: Can't get ArchRef value from mypyNode other than ClassDef "
                f"type(node.gen.mypy_ast[0])"
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
        self.__debug_print(f"Getting type not supported in {type(node)}")

    @__handle_node
    def enter_assign_compr(self, node: ast.AssignCompr) -> None:
        """Pass handler for AssignCompr nodes."""
        self.__debug_print(f"Getting type not supported in {type(node)}")

    @__handle_node
    def enter_int(self, node: ast.Int) -> None:
        """Pass handler for Int nodes."""
        node.name_spec.sym_type = "builtins.int"

    @__handle_node
    def enter_float(self, node: ast.Float) -> None:
        """Pass handler for Float nodes."""
        node.name_spec.sym_type = "builtins.float"

    @__handle_node
    def enter_string(self, node: ast.String) -> None:
        """Pass handler for String nodes."""
        node.name_spec.sym_type = "builtins.str"

    @__handle_node
    def enter_bool(self, node: ast.Bool) -> None:
        """Pass handler for Bool nodes."""
        node.name_spec.sym_type = "builtins.bool"

    @__handle_node
    def enter_builtin_type(self, node: ast.BuiltinType) -> None:
        """Pass handler for BuiltinType nodes."""
        self.__check_builltin_symbol(node)
        node.name_spec.sym_type = f"builtins.{node.sym_name}"

    def get_type_from_instance(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.Instance
    ) -> None:
        """Get type info from mypy type Instance."""
        node.name_spec.sym_type = str(mypy_type)

    def get_type_from_callable_type(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.CallableType
    ) -> None:
        """Get type info from mypy type CallableType."""
        self.__call_type_handler(node, mypy_type.ret_type)

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
        node.name_spec.sym_type = "None"

    def get_type_from_any_type(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.AnyType
    ) -> None:
        """Get type info from mypy type NoneType."""
        node.name_spec.sym_type = "Any"

    def get_type_from_tuple_type(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.TupleType
    ) -> None:
        """Get type info from mypy type TupleType."""
        node.name_spec.sym_type = "builtins.tuple"

    def get_type_from_type_type(
        self, node: ast.AstSymbolNode, mypy_type: MypyTypes.TypeType
    ) -> None:
        """Get type info from mypy type TypeType."""
        node.name_spec.sym_type = str(mypy_type.item)

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Add new symbols in the symbol table in case of self."""
        # This will fix adding new items to the class through self
        # self.x = 5  # will add x to self datatype symbol table
        for target in node.target.items:
            if (
                isinstance(target, ast.AtomTrailer)
                and isinstance(target.target, ast.SpecialVarRef)
                and target.target.sym_name == "self"
            ):
                self_obj = target.target
                right_obj = target.right
                if self_obj.type_sym_tab and isinstance(right_obj, ast.AstSymbolNode):
                    self_obj.type_sym_tab.def_insert(right_obj)

        # Support adding the correct type symbol table in case of ModuleType
        # This will only work for target=Val & target1=target2=val and
        #   target is a moduleType
        # it won't work in case of
        #   - target1, target2 = Val1, Val2  <-- tuples need more attention
        #   - target = a.b.c                 <-- will be fixed after thakee's PR
        #   - a.b.c = val                    <-- will be fixed after thakee's PR
        for target in node.target.items:
            if (
                isinstance(target, ast.Name)
                and target.sym_type == "types.ModuleType"
                and isinstance(node.value, ast.Name)
            ):
                target.type_sym_tab = node.value.type_sym_tab

    def expand_atom_trailer(self, node_list: list[ast.AstNode]) -> list[ast.AstNode]:
        """Expand the atom trailer object in a list of AstNode."""
        out: list[ast.AstNode] = []
        for i in node_list:
            if isinstance(i, ast.AtomTrailer):
                out.append(i.target)
                out.append(i.right)
            elif isinstance(i, ast.FuncCall):
                out.append(i.target)
            else:
                out.append(i)
        return out

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Adding symbol links to AtomTrailer right nodes."""
        # This will fix adding the symbol links to nodes in atom trailer
        # self.x.z = 5  # will add symbol links to both x and z

        # This function originally used `as_attr_list` in AtomTrailer
        # but an issue happened when doing stuff like fool_me().CONST_VALUE2
        # The issue was due to the way `as_attr_list` implemented so the fix
        # was to implement it again to get all items in AtomTrailer even if
        # their type is not an AstSymbolNode
        atom_trailer_unwind = self.expand_atom_trailer([node])
        iteration_count = 0
        while any(
            isinstance(i, (ast.AtomTrailer, ast.FuncCall)) for i in atom_trailer_unwind
        ):
            atom_trailer_unwind = self.expand_atom_trailer(atom_trailer_unwind)
            iteration_count += 1
            if iteration_count > 50:
                break

        for i in range(1, len(atom_trailer_unwind)):
            left = atom_trailer_unwind[i - 1]
            right = atom_trailer_unwind[i]

            assert isinstance(left, ast.AstSymbolNode)
            assert isinstance(right, ast.AstSymbolNode)

            if isinstance(right, ast.IndexSlice):
                # In case of index slice, left won't have a symbol table as it's a list/dict/set
                node_type: str = ""

                # left type is a list
                if left.sym_type.startswith("builtins.list["):
                    node_type = left.sym_type[len("builtins.list[") : -1]

                    # right index slice is a range then it's type is the same as left
                    if right.is_range:
                        right.name_spec.sym_type = left.sym_type
                        continue

                # left type is a dictionary
                elif left.sym_type.startswith("builtins.dict["):
                    node_type = (
                        left.sym_type[len("builtins.dict[") : -1].split(",")[1].strip()
                    )

                # unsupported type
                else:
                    continue

                right.name_spec.sym_type = node_type

                # Getting the correct symbol table and link it
                type_symtab: Optional[SymbolTable] = self.ir.sym_tab
                assert isinstance(self.ir, ast.Module)
                assert isinstance(type_symtab, SymbolTable)

                if re.match(r"builtins.(list|dict|tuple)", node_type):
                    node_type = re.sub(r"\[.*\]", "", node_type)

                for j in node_type.split("."):
                    if j == self.ir.name:
                        continue
                    type_symtab = type_symtab.find_scope(j)
                    if type_symtab is None:
                        break
                right.name_spec.type_sym_tab = type_symtab

            else:
                if left.type_sym_tab:
                    right.name_spec.sym = left.type_sym_tab.lookup(right.sym_name)
                    if right.name_spec.sym:
                        right.name_spec.sym.add_use(right.name_spec)

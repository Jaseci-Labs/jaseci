"""Type Information Fusion Pass for the Jac compiler.

This pass integrates mypy's type inference capabilities with Jac's AST by:

1. Collecting type information from mypy's analysis and attaching it to Jac AST nodes
2. Establishing type relationships between expressions, variables, and function returns
3. Resolving complex types including:
   - Collection types (lists, dictionaries, tuples, sets)
   - Union types
   - Module types
   - Custom user-defined types

4. Building symbol table links based on type information, enabling:
   - Proper attribute access resolution
   - Method call validation
   - Type-based code completion

This pass is essential for static type checking, IDE support, and enabling type-aware
optimizations in the compiler.
"""

from __future__ import annotations

import re
from typing import Callable, Optional, TypeVar

import jaclang.compiler.unitree as uni
from jaclang.compiler.constant import Constants, Tokens
from jaclang.compiler.passes import UniPass
from jaclang.compiler.unitree import UniScopeNode
from jaclang.utils.helpers import pascal_to_snake
from jaclang.vendor.mypy.nodes import Node as VNode  # bit of a hack


import mypy.nodes as MypyNodes  # noqa N812
import mypy.types as MypyTypes  # noqa N812
from mypy.checkexpr import Type as MyType


T = TypeVar("T", bound=uni.AstSymbolNode)


class FuseTypeInfoPass(UniPass):
    """Python and bytecode file self.__debug_printing pass."""

    node_type_hash: dict[MypyNodes.Node | VNode, MyType] = {}

    # Override this to support enter expression.
    def enter_node(self, node: uni.UniNode) -> None:
        """Run on entering node."""
        super().enter_node(node)

        if isinstance(node, uni.Expr):
            self.enter_expr(node)

    def __call_type_handler(self, mypy_type: MypyTypes.Type) -> Optional[str]:
        if isinstance(mypy_type, MypyTypes.UnionType):
            types: str = "Union["
            for i in mypy_type.items:
                mypy_type_name = pascal_to_snake(i.__class__.__name__)
                type_handler_name = f"get_type_from_{mypy_type_name}"
                if hasattr(self, type_handler_name):
                    types += getattr(self, type_handler_name)(i)
                    types += ", "
            types = types[:-2] + "]"
            return types
        else:
            mypy_type_name = pascal_to_snake(mypy_type.__class__.__name__)
            type_handler_name = f"get_type_from_{mypy_type_name}"
            if hasattr(self, type_handler_name):
                return getattr(self, type_handler_name)(mypy_type)
            return None

    def __set_type_sym_table_link(self, node: uni.AstSymbolNode) -> None:
        sym_type = node.expr_type
        if re.match(r"builtins.(list|dict|tuple)", sym_type):
            sym_type = re.sub(r"\[.*\]", "", sym_type)
        elif sym_type == "None" or sym_type == "NoType":
            return

        if node.expr_type == "types.ModuleType" and node.sym:
            node.name_spec.type_sym_tab = self.__get_parent_symtab(node.sym_name)

        partent_sym_table: Optional[UniScopeNode] = self.__get_parent_symtab(sym_type)
        if partent_sym_table is None:
            return
        typ = sym_type.split(".")
        typ_sym_table = partent_sym_table

        for i in typ:
            if i == self.ir_out.name:
                continue
            f = typ_sym_table.find_scope(i)
            if f:
                typ_sym_table = f

        if typ_sym_table != partent_sym_table:
            node.name_spec.type_sym_tab = typ_sym_table

    @staticmethod
    def __handle_node(
        func: Callable[[FuseTypeInfoPass, T], None],
    ) -> Callable[[FuseTypeInfoPass, T], None]:
        def node_handler(self: FuseTypeInfoPass, node: T) -> None:
            jac_node_str = f'jac node "{node.loc}::{node.__class__.__name__}'
            if hasattr(node, "value"):
                jac_node_str += f'::{node.value}"'
            else:
                jac_node_str += '"'

            # Jac node has only one mypy node linked to it
            if len(node.gen.mypy_ast) == 1:
                func(self, node)
                self.__set_type_sym_table_link(node)

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

                func(self, node)
                self.__set_type_sym_table_link(node)

            # Special handing for BuiltinType
            elif isinstance(node, uni.BuiltinType):
                func(self, node)  # type: ignore
                self.__set_type_sym_table_link(node)

        return node_handler

    def __collect_type_from_symbol(self, node: uni.AstSymbolNode) -> None:
        mypy_node = node.gen.mypy_ast[0]

        if isinstance(mypy_node, MypyNodes.MemberExpr):
            if mypy_node in self.node_type_hash:
                node.name_spec.expr_type = (
                    self.__call_type_handler(self.node_type_hash[mypy_node])
                    or node.name_spec.expr_type
                )

        elif hasattr(mypy_node, "node"):
            # orig_node = mypy_node
            mypy_node = mypy_node.node

            if isinstance(mypy_node, (MypyNodes.Var, MypyNodes.FuncDef)):
                node.name_spec.expr_type = (
                    self.__call_type_handler(mypy_node.type) or node.name_spec.expr_type
                )

            elif isinstance(mypy_node, MypyNodes.MypyFile):
                node.name_spec.expr_type = "types.ModuleType"

            elif isinstance(mypy_node, MypyNodes.TypeInfo):
                node.name_spec.expr_type = mypy_node.fullname

            elif isinstance(mypy_node, MypyNodes.OverloadedFuncDef):
                node.name_spec.expr_type = (
                    self.__call_type_handler(mypy_node.items[0].func.type)
                    or node.name_spec.expr_type
                )

            elif mypy_node is None:
                node.name_spec.expr_type = "None"

        else:
            if isinstance(mypy_node, MypyNodes.ClassDef):
                node.name_spec.expr_type = mypy_node.fullname
                self.__set_type_sym_table_link(node)
            elif isinstance(mypy_node, MypyNodes.FuncDef):
                node.name_spec.expr_type = (
                    self.__call_type_handler(mypy_node.type) or node.name_spec.expr_type
                )
            elif isinstance(mypy_node, MypyNodes.Argument):
                node.name_spec.expr_type = (
                    self.__call_type_handler(mypy_node.variable.type)
                    or node.name_spec.expr_type
                )
            elif isinstance(mypy_node, MypyNodes.Decorator):
                node.name_spec.expr_type = (
                    self.__call_type_handler(mypy_node.func.type.ret_type)
                    or node.name_spec.expr_type
                )

    def __check_builltin_symbol(self, node: uni.NameAtom) -> None:
        if isinstance(node.parent, uni.AtomTrailer) and node is node.parent.right:
            return
        builtins_sym_tab = None
        for mod in self.prog.mod.hub.values():
            if mod.name == "builtins":
                builtins_sym_tab = mod.sym_tab

        assert builtins_sym_tab is not None
        builtins_sym = builtins_sym_tab.lookup(node.sym_name)
        if builtins_sym:
            node.name_spec._sym = builtins_sym

    collection_types_map = {
        uni.ListVal: "builtins.list",
        uni.SetVal: "builtins.set",
        uni.TupleVal: "builtins.tuple",
        uni.DictVal: "builtins.dict",
        uni.ListCompr: None,
        uni.DictCompr: None,
    }

    # NOTE (Thakee): Since expression nodes are not AstSymbolNodes, I'm not decorating this with __handle_node
    # and IMO instead of checking if it's a symbol node or an expression, we somehow mark expressions as
    # valid nodes that can have symbols. At this point I'm leaving this like this and lemme know
    # otherwise.
    # NOTE (GAMAL): This will be fixed through the AstTypedNode
    def enter_expr(self: FuseTypeInfoPass, node: uni.Expr) -> None:
        """Enter an expression node."""
        if len(node.gen.mypy_ast) == 0:
            return

        # No need to run this handling in case of a previous type
        # was set during the pass, if not then we hope that the
        # mypy node has a type associated to it
        if node.expr_type != "NoType":
            return

        # Check if the expression is a data spatial expression
        # Support disconnectOp
        if isinstance(node, uni.BinaryExpr):
            if isinstance(node.op, uni.DisconnectOp):
                node.expr_type = "builtins.bool"
                return

            # Support spwan and connectOp
            elif (
                isinstance(node.op, uni.ConnectOp)
                or node.op.name == Tokens.KW_SPAWN.value
            ):
                if node.gen.mypy_ast[-1] in self.node_type_hash:
                    node.expr_type = (
                        self.__call_type_handler(
                            self.node_type_hash[node.gen.mypy_ast[-1]]
                        )
                        or node.expr_type
                    )
                return

        if isinstance(node, uni.EdgeRefTrailer) and any(
            isinstance(k, uni.FilterCompr) for k in node.kid
        ):
            if node.gen.mypy_ast[-1] in self.node_type_hash:
                node.expr_type = (
                    self.__call_type_handler(self.node_type_hash[node.gen.mypy_ast[-1]])
                    or node.expr_type
                )
            return

        # If the corrosponding mypy ast node type has stored here, get the values.
        mypy_node = node.gen.mypy_ast[0]
        if mypy_node in self.node_type_hash:
            mytype: MyType = self.node_type_hash[mypy_node]
            node.expr_type = self.__call_type_handler(mytype) or node.expr_type

        # Set they symbol type for collection expression.
        #
        # GenCompr is an instance of ListCompr but we don't handle it here.
        # so the isinstace (node, <classes>) doesn't work, I'm going with type(...) == ...
        if type(node) in self.collection_types_map:
            assert isinstance(node, uni.AtomExpr)  # To make mypy happy.
            collection_type = self.collection_types_map[type(node)]
            if collection_type is not None:
                node.name_spec.expr_type = collection_type
            if mypy_node in self.node_type_hash:
                node.name_spec.expr_type = (
                    self.__call_type_handler(mytype) or node.name_spec.expr_type
                )

    @__handle_node
    def enter_name(self, node: uni.NameAtom) -> None:
        """Pass handler for name nodes."""
        self.__collect_type_from_symbol(node)
        if node.sym is None:
            self.__check_builltin_symbol(node)

    @__handle_node
    def enter_module_path(self, node: uni.ModulePath) -> None:
        """Pass handler for ModulePath nodes."""

    @__handle_node
    def enter_module_item(self, node: uni.ModuleItem) -> None:
        """Pass handler for ModuleItem nodes."""

    @__handle_node
    def enter_architype(self, node: uni.Architype) -> None:
        """Pass handler for Architype nodes."""
        self.__collect_type_from_symbol(node)

    @__handle_node
    def enter_arch_def(self, node: uni.ArchDef) -> None:
        """Pass handler for ArchDef nodes."""

    @__handle_node
    def enter_enum(self, node: uni.Enum) -> None:
        """Pass handler for Enum nodes."""
        self.__collect_type_from_symbol(node)

    @__handle_node
    def enter_enum_def(self, node: uni.EnumDef) -> None:
        """Pass handler for EnumDef nodes."""

    @__handle_node
    def enter_ability(self, node: uni.Ability) -> None:
        """Pass handler for Ability nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.FuncDef):
            node.name_spec.expr_type = (
                self.__call_type_handler(node.gen.mypy_ast[0].type.ret_type)
                or node.name_spec.expr_type
            )

    @__handle_node
    def enter_ability_def(self, node: uni.AbilityDef) -> None:
        """Pass handler for AbilityDef nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.FuncDef):
            node.name_spec.expr_type = (
                self.__call_type_handler(node.gen.mypy_ast[0].type.ret_type)
                or node.name_spec.expr_type
            )

    @__handle_node
    def enter_param_var(self, node: uni.ParamVar) -> None:
        """Pass handler for ParamVar nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.Argument):
            mypy_node: MypyNodes.Argument = node.gen.mypy_ast[0]
            if mypy_node.variable.type:
                node.name_spec.expr_type = (
                    self.__call_type_handler(mypy_node.variable.type)
                    or node.name_spec.expr_type
                )

    # TODO: support all lhs if needed
    @__handle_node
    def enter_has_var(self, node: uni.HasVar) -> None:
        """Pass handler for HasVar nodes."""
        mypy_node = node.gen.mypy_ast[0]
        if isinstance(mypy_node, MypyNodes.AssignmentStmt):
            n = mypy_node.lvalues[0].node
            if isinstance(n, (MypyNodes.Var, MypyNodes.FuncDef)):
                node.name_spec.expr_type = (
                    self.__call_type_handler(n.type) or node.name_spec.expr_type
                )

    def exit_has_var(self, node: uni.HasVar) -> None:
        """Pass handler for HasVar nodes."""
        node.name_spec.expr_type = node.name.expr_type
        node.name_spec.type_sym_tab = node.name.type_sym_tab

    @__handle_node
    def enter_multi_string(self, node: uni.MultiString) -> None:
        """Pass handler for MultiString nodes."""
        node.name_spec.expr_type = "builtins.str"

    @__handle_node
    def enter_f_string(self, node: uni.FString) -> None:
        """Pass handler for FString nodes."""

    @__handle_node
    def enter_arch_ref(self, node: uni.ArchRef) -> None:
        """Pass handler for ArchRef nodes."""
        if isinstance(node.gen.mypy_ast[0], MypyNodes.ClassDef):
            mypy_node: MypyNodes.ClassDef = node.gen.mypy_ast[0]
            node.name_spec.expr_type = mypy_node.fullname
            self.__set_type_sym_table_link(node)
        elif isinstance(node.gen.mypy_ast[0], MypyNodes.FuncDef):
            mypy_node2: MypyNodes.FuncDef = node.gen.mypy_ast[0]
            node.name_spec.expr_type = (
                self.__call_type_handler(mypy_node2.type) or node.name_spec.expr_type
            )

    @__handle_node
    def enter_special_var_ref(self, node: uni.SpecialVarRef) -> None:
        """Pass handler for SpecialVarRef nodes."""
        if node.py_resolve_name() == Constants.ROOT:
            if node.gen.mypy_ast[-1] in self.node_type_hash:
                node.name_spec.expr_type = (
                    self.__call_type_handler(self.node_type_hash[node.gen.mypy_ast[-1]])
                    or node.name_spec.expr_type
                )
        else:
            self.enter_name(node)

    @__handle_node
    def enter_edge_op_ref(self, node: uni.EdgeOpRef) -> None:
        """Pass handler for EdgeOpRef nodes."""
        self.__collect_type_from_symbol(node)

    @__handle_node
    def enter_filter_compr(self, node: uni.FilterCompr) -> None:
        """Pass handler for FilterCompr nodes."""

    @__handle_node
    def enter_assign_compr(self, node: uni.AssignCompr) -> None:
        """Pass handler for AssignCompr nodes."""

    @__handle_node
    def enter_int(self, node: uni.Int) -> None:
        """Pass handler for Int nodes."""
        node.name_spec.expr_type = "builtins.int"

    @__handle_node
    def enter_float(self, node: uni.Float) -> None:
        """Pass handler for Float nodes."""
        node.name_spec.expr_type = "builtins.float"

    @__handle_node
    def enter_string(self, node: uni.String) -> None:
        """Pass handler for String nodes."""
        node.name_spec.expr_type = "builtins.str"

    @__handle_node
    def enter_bool(self, node: uni.Bool) -> None:
        """Pass handler for Bool nodes."""
        node.name_spec.expr_type = "builtins.bool"

    @__handle_node
    def enter_builtin_type(self, node: uni.BuiltinType) -> None:
        """Pass handler for BuiltinType nodes."""
        self.__check_builltin_symbol(node)
        node.name_spec.expr_type = f"builtins.{node.sym_name}"

    def get_type_from_instance(self, mypy_type: MypyTypes.Instance) -> Optional[str]:
        #  FIXME: Returning str(mypy_type) won't work for literal values since it would be
        # like Literal['foo'] instead of builtins.str, so we need to get the type fullname.
        # Not sure if this is the best way to do it.
        ret = str(mypy_type)
        if ret.startswith("Literal[") and ret.endswith("]"):
            return mypy_type.type.fullname
        return ret

    def get_type_from_callable_type(
        self, mypy_type: MypyTypes.CallableType
    ) -> Optional[str]:
        return self.__call_type_handler(mypy_type.ret_type)

    # TODO: Which overloaded function to get the return value from?
    def get_type_from_overloaded(
        self, mypy_type: MypyTypes.Overloaded
    ) -> Optional[str]:
        return self.__call_type_handler(mypy_type.items[-1])

    def get_type_from_none_type(self, mypy_type: MypyTypes.NoneType) -> Optional[str]:
        return "None"

    def get_type_from_any_type(self, mypy_type: MypyTypes.AnyType) -> Optional[str]:
        return "Any"

    def get_type_from_tuple_type(self, mypy_type: MypyTypes.TupleType) -> Optional[str]:
        return "builtins.tuple"

    def get_type_from_type_type(self, mypy_type: MypyTypes.TypeType) -> Optional[str]:
        return str(mypy_type.item)

    def get_type_from_type_var_type(
        self, mypy_type: MypyTypes.TypeVarType
    ) -> Optional[str]:
        return str(mypy_type.name)

    def exit_assignment(self, node: uni.Assignment) -> None:
        """Add new symbols in the symbol table in case of self."""
        # This will fix adding new items to the class through self
        # self.x = 5  # will add x to self datatype symbol table
        for target in node.target.items:
            if (
                isinstance(target, uni.AtomTrailer)
                and isinstance(target.target, uni.SpecialVarRef)
                and target.target.sym_name == "self"
            ):
                self_obj = target.target
                right_obj = target.right
                if self_obj.type_sym_tab and isinstance(right_obj, uni.AstSymbolNode):
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
                isinstance(target, uni.Name)
                and target.expr_type == "types.ModuleType"
                and isinstance(node.value, uni.Name)
            ):
                target.type_sym_tab = node.value.type_sym_tab

    def expand_atom_trailer(self, node_list: list[uni.UniNode]) -> list[uni.UniNode]:
        """Expand the atom trailer object in a list of UniNode."""
        out: list[uni.UniNode] = []
        for i in node_list:
            if isinstance(i, uni.AtomTrailer):
                out.append(i.target)
                out.append(i.right)
            elif isinstance(i, uni.FuncCall):
                out.append(i.target)
            else:
                out.append(i)
        return out

    def exit_atom_trailer(self, node: uni.AtomTrailer) -> None:
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
            isinstance(i, (uni.AtomTrailer, uni.FuncCall)) for i in atom_trailer_unwind
        ):
            atom_trailer_unwind = self.expand_atom_trailer(atom_trailer_unwind)
            iteration_count += 1
            if iteration_count > 50:
                break

        for i in range(1, len(atom_trailer_unwind)):
            left = atom_trailer_unwind[i - 1]
            right = atom_trailer_unwind[i]

            assert isinstance(left, (uni.Expr, uni.AstSymbolNode))
            assert isinstance(right, uni.AstSymbolNode)

            if isinstance(right, uni.IndexSlice):
                # In case of index slice, left won't have a symbol table as it's a list/dict/set
                node_type: str = ""

                # left type is a list
                if left.expr_type.startswith(("builtins.list[", "jaclang.JacList[")):
                    node_type = left.expr_type[left.expr_type.find("[") + 1 : -1]

                    # right index slice is a range then it's type is the same as left
                    if right.is_range:
                        right.expr_type = left.expr_type
                        right.parent_of_type(uni.AtomTrailer).expr_type = node_type
                        continue

                # left type is a dictionary
                elif left.expr_type.startswith("builtins.dict["):
                    node_type = (
                        left.expr_type[len("builtins.dict[") : -1].split(",")[1].strip()
                    )

                # unsupported type
                else:
                    continue

                right.expr_type = node_type
                right.parent_of_type(uni.AtomTrailer).expr_type = node_type

                if re.match(r"builtins.(list|dict|tuple)", node_type):
                    node_type = re.sub(r"\[.*\]", "", node_type)

                # Getting the correct symbol table and link it
                type_symtab: Optional[UniScopeNode] = self.__get_parent_symtab(
                    node_type
                )

                if type_symtab is None:
                    return

                for j in node_type.split("."):
                    if j == type_symtab.nix_name:
                        continue
                    type_symtab = type_symtab.find_scope(j)
                    if type_symtab is None:
                        break
                right.type_sym_tab = type_symtab

            else:
                # Fix the symbolTable linking in case of type annotations
                # TODO: This will not work if an AtomTrailer was used as type annotations
                if left.type_sym_tab is None and isinstance(node.parent, uni.SubTag):
                    assert isinstance(left, uni.AstSymbolNode)
                    left.name_spec.type_sym_tab = self.ir_out.sym_tab.find_scope(
                        left.sym_name
                    )

                if left.type_sym_tab:
                    right.name_spec.sym = left.type_sym_tab.lookup(right.sym_name)
                    if right.name_spec.sym:
                        right.name_spec.sym.add_use(right.name_spec)

    def __get_parent_symtab(self, typ: str) -> Optional[UniScopeNode]:
        for mod_ast in self.prog.mod.hub.values():
            mod_table = mod_ast.sym_tab
            if mod_table.nix_name == typ.split(".")[0]:
                return mod_table
        return None

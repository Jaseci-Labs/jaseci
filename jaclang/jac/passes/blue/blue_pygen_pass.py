"""Jac Blue pass for Jaseci Ast."""
import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Constants as Con
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.passes import Pass


class BluePygenPass(Pass):
    """Jac blue transpilation to python pass."""

    def before_pass(self) -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.indent_level = 0
        self.debuginfo = {"jac_mods": []}
        self.preamble = ast.AstNode(parent=None, mod_link=None, kid=[], line=0)
        self.preamble.meta["py_code"] = "from __future__ import annotations\n"
        self.cur_arch = None  # tracks current architype during transpilation

    def enter_node(self, node: ast.AstNode) -> None:
        """Enter node."""
        if node:
            node.meta["py_code"] = ""
        return Pass.enter_node(self, node)

    def indent_str(self) -> str:
        """Return string for indent."""
        return " " * self.indent_size * self.indent_level

    def emit_ln(self, node: ast.AstNode, s: str) -> None:
        """Emit code to node."""
        self.emit(node, s.strip().strip("\n"))
        self.emit(node, f"  # {self.get_mod_index(node)} {node.line}\n")

    def emit_ln_unique(self, node: ast.AstNode, s: str) -> None:
        """Emit code to node."""
        if s not in node.meta["py_code"]:
            ilev = self.indent_level
            self.indent_level = 0
            self.emit_ln(node, s)
            self.indent_level = ilev

    def get_mod_index(self, node: ast.AstNode) -> int:
        """Get module index."""
        path = node.mod_link.mod_path if node.mod_link else None
        if not path:
            return -1
        if path not in self.debuginfo["jac_mods"]:
            self.debuginfo["jac_mods"].append(path)
        return self.debuginfo["jac_mods"].index(path)

    def emit(self, node: ast.AstNode, s: str) -> None:
        """Emit code to node."""
        node.meta["py_code"] += self.indent_str() + s.replace(
            "\n", "\n" + self.indent_str()
        )
        if "\n" in node.meta["py_code"]:
            node.meta["py_code"] = node.meta["py_code"].rstrip(" ")

    def needs_jac_import(self) -> None:
        """Check if import is needed."""
        self.emit_ln_unique(
            self.preamble, "from jaclang import jac_blue_import as __jac_import__"
        )

    def needs_enum(self) -> None:
        """Check if enum is needed."""
        self.emit_ln_unique(
            self.preamble,
            "from enum import Enum as __jac_Enum__, auto as __jac_auto__",
        )

    def emit_jac_error_handler(self, node: ast.AstNode) -> None:
        """Emit error handler."""
        self.emit_ln_unique(self.preamble, "import traceback as __jac_traceback__")
        self.emit_ln_unique(
            self.preamble, "from jaclang import handle_jac_error as __jac_error__"
        )
        self.emit_ln(node, "except Exception as e:")
        self.indent_level += 1
        # self.emit_ln(node, "__jac_traceback__.print_exc()")
        self.emit_ln(node, "tb = __jac_traceback__.extract_tb(e.__traceback__)")
        self.emit_ln(node, "__jac_tmp__ = __jac_error__(_jac_pycodestring_, e, tb)")
        # self.emit_ln(node, "print(__jac_tmp__)\nraise e")
        self.emit_ln(
            node,
            "e.args = (f'{e.args[0]}\\n' + __jac_tmp__,) + e.args[1:] "
            f"if '{Con.JAC_ERROR_PREAMBLE}' not in str(e) else e.args",
        )
        self.emit_ln(node, "raise e")
        self.indent_level -= 1

    def decl_def_missing(self, decl: str = "this") -> None:
        """Warn about declaration."""
        self.error(
            f"Unable to find definition for {decl} declaration. Perhaps there's an `include` missing?"
        )

    def ds_feature_warn(self) -> None:
        """Warn about feature."""
        self.warning("Data spatial features not supported in bootstrap Jac.")

    def exit_parse(self, node: ast.Parse) -> None:
        """Sub objects.

        name: str,
        """
        self.error(f"Parse node should not be in this AST!! {node.name}")
        raise ValueError("Parse node should not be in AST after being Built!!")

    def exit_token(self, node: ast.Token) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        """
        self.emit(node, node.value)

    def exit_name(self, node: ast.Name) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        already_declared: bool,
        """
        self.emit(node, node.value)

    def exit_constant(self, node: ast.Constant) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        typ: type,
        """
        self.emit(node, node.value)

    def exit_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: "Elements",
        """
        self.emit_ln(node, node.doc.value)
        self.emit(node, self.preamble.meta["py_code"])
        if node.body:
            self.emit(node, node.body.meta["py_code"])
        self.emit(node, f'r""" {Con.JAC_DEBUG_SPLITTER}\n')
        for i in self.debuginfo["jac_mods"]:
            self.emit(node, f"{i}\n")
        self.emit(node, f'{Con.JAC_DEBUG_SPLITTER} """\n')
        self.ir = node
        self.ir.meta["py_code"] = self.ir.meta["py_code"].rstrip()

    def exit_elements(self, node: ast.Elements) -> None:
        """Sub objects.

        elements: list[GlobalVars | Test | ModuleCode | Import | Architype | Ability | AbilitySpec],
        """
        for i in node.elements:
            self.emit(node, i.meta["py_code"])
            self.emit(node, "\n")

    def exit_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        doc: Optional["Token"],
        access: Optional[Token],
        assignments: "AssignmentList",
        is_frozen: bool,
        """
        if node.doc:
            self.emit_ln(node, node.doc.value)
        self.emit(node, node.assignments.meta["py_code"])

    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Optional[Name],
        doc: Optional[Token],
        body: CodeBlock,
        """
        test_name = node.name.value
        test_code = "import unittest as __jac_unittest__\n"
        test_code += "__jac_tc__ = __jac_unittest__.TestCase()\n"
        test_code += "__jac_suite__ = __jac_unittest__.TestSuite()\n"
        test_code += "class __jac_check:\n"
        test_code += "    def __getattr__(self, name):\n"
        test_code += "        return getattr(__jac_tc__, 'assert'+name)"
        self.emit_ln_unique(self.preamble, test_code)
        self.emit_ln(node, f"def test_{test_name}():")
        self.indent_level += 1
        if node.doc:
            self.emit_ln(node, node.doc.value)
        self.emit_ln(node, "check = __jac_check()")
        self.emit_ln(node, node.body.meta["py_code"])
        self.indent_level -= 1
        self.emit_ln(
            node,
            f"__jac_suite__.addTest(__jac_unittest__.FunctionTestCase(test_{test_name}))",
        )

    def exit_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        doc: Optional[Token],
        name: Optional[Name],
        body: CodeBlock,

        """
        if node.doc:
            self.emit_ln(node, node.doc.value)
        if node.name:
            self.emit_ln(node, f"if __name__ == '{node.name.meta['py_code']}':")
            self.indent_level += 1
            self.emit(node, node.body.meta["py_code"])
            self.indent_level -= 1
        else:
            self.emit(node, node.body.meta["py_code"])

    def exit_py_inline_code(self, node: ast.PyInlineCode) -> None:
        """Sub objects.

        code: Token,
        """
        self.emit_ln(node, node.code.value)

    def exit_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: Token,
        path: "ModulePath",
        alias: Optional[Token],
        items: Optional["ModuleItems"],
        is_absorb: bool,  # For includes
        self.sub_module = None
        """
        if node.lang.value == Con.JAC_LANG_IMP:  # injects module into sys.modules
            self.needs_jac_import()
            self.emit_ln(
                node,
                f"__jac_import__(target='{node.path.meta['py_code']}', base_path=__file__)",
            )
        if node.is_absorb:
            self.emit_ln(
                node,
                f"from {node.path.meta['py_code']} import *",
            )
            if node.items:
                self.warning(
                    "Includes import * in target module into current namespace."
                )
            return
        if not node.items:
            if not node.alias:
                self.emit_ln(node, f"import {node.path.meta['py_code']}")
            else:
                self.emit_ln(
                    node,
                    f"import {node.path.meta['py_code']} as {node.alias.meta['py_code']}",
                )
        else:
            self.emit_ln(
                node,
                f"from {node.path.meta['py_code']} import {node.items.meta['py_code']}",
            )

    def exit_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: list[Token],
        """
        self.emit(node, "".join([i.value for i in node.path]))

    def exit_module_items(self, node: ast.ModuleItems) -> None:
        """Sub objects.

        items: list["ModuleItem"],
        """
        self.emit(node, ", ".join([i.meta["py_code"] for i in node.items]))

    def exit_module_item(self, node: ast.ModuleItem) -> None:
        """Sub objects.

        name: Token,
        alias: Optional[Token],
        """
        if node.alias:
            self.emit(node, node.name.value + " as " + node.alias.value)
        else:
            self.emit(node, node.name.value)

    # NOTE: Incomplete for Jac Purple and Red
    def exit_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        doc: Optional[Token],
        decorators: Optional["Decorators"],
        access: Optional[Token],
        base_classes: "BaseClasses",
        body: Optional["ArchBlock"],
        """
        if node.decorators:
            self.emit(node, node.decorators.meta["py_code"])
        if not len(node.base_classes.base_classes):
            self.emit_ln(node, f"class {node.name.meta['py_code']}:")
        else:
            self.emit_ln(
                node,
                f"class {node.name.meta['py_code']}({node.base_classes.meta['py_code']}):",
            )
        self.indent_level += 1
        if node.doc:
            self.emit_ln(node, node.doc.value)
        if node.body:
            self.emit(node, node.body.meta["py_code"])
        self.indent_level -= 1

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional["DottedNameList"],
        arch: "ObjectRef | NodeRef | EdgeRef | WalkerRef",
        body: "ArchBlock",
        """

    def exit_decorators(self, node: ast.Decorators) -> None:
        """Sub objects.

        calls: list["ExprType"],
        """
        for i in node.calls:
            self.emit_ln(node, "@" + i.meta["py_code"])

    def exit_base_classes(self, node: ast.BaseClasses) -> None:
        """Sub objects.

        base_classes: list[DottedNameList],
        """
        self.emit(node, ", ".join([i.meta["py_code"] for i in node.base_classes]))

    # NOTE: Incomplete for Jac Purple and Red
    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: Name | SpecialVarRef | ArchRef,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        is_abstract: bool,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        signature: Optional[FuncSignature | TypeSpec | EventSignature],
        body: Optional[CodeBlock],
        arch_attached: Optional["ArchBlock"] = None,
        """
        ability_name = node.py_resolve_name()
        if node.arch_attached and ability_name == "__init__":
            return
        if node.decorators:
            self.emit(node, node.decorators.meta["py_code"])
        if isinstance(node.signature, (ast.FuncSignature, ast.EventSignature)):
            if "->" in node.signature.meta["py_code"]:
                node.signature.meta["py_code"] = node.signature.meta["py_code"].replace(
                    " ->", ") ->"
                )
            else:
                node.signature.meta["py_code"] += ")"
            if node.arch_attached and not node.is_static:
                self.emit_ln(
                    node, f"def {ability_name}(self,{node.signature.meta['py_code']}:"
                )
            else:
                if node.arch_attached and node.is_static:
                    self.emit_ln(node, "@classmethod")
                self.emit_ln(
                    node, f"def {ability_name}({node.signature.meta['py_code']}:"
                )
        else:
            if node.arch_attached:
                self.emit_ln(node, f"def {ability_name}(self):")
            else:
                self.emit_ln(node, f"def {ability_name}():")
        self.indent_level += 1
        if node.doc:
            self.emit_ln(node, node.doc.value)
        if node.body:
            self.emit_ln(node, "try:")
            self.indent_level += 1
            self.emit(node, node.body.meta["py_code"])
            self.indent_level -= 1
            self.emit_jac_error_handler(node)
        elif node.is_abstract:
            self.emit_ln(node, "pass")
        self.indent_level -= 1

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional["DottedNameList"],
        ability: AbilityRef,
        body: CodeBlock,
        """

    def exit_arch_block(self, node: ast.ArchBlock) -> None:
        """Sub objects.

        members: list["ArchHas | Ability"],
        """
        init_func = None
        for i in node.members:
            if isinstance(i, ast.Ability) and i.py_resolve_name() == "__init__":
                init_func = i
                break
        static_has_members = [
            i for i in node.members if isinstance(i, ast.ArchHas) and i.is_static
        ]
        for i in static_has_members:
            self.emit(node, i.meta["py_code"])
            self.emit(node, "\n")

        if init_func and init_func.decorators:
            self.emit(node, init_func.decorators.meta["py_code"])
        self.emit_ln(node, "def __init__(self,")
        self.indent_level += 1
        if has_members := [
            i for i in node.members if isinstance(i, ast.ArchHas) and not i.is_static
        ]:
            for i in has_members:
                for j in i.vars.vars:
                    self.emit_ln(node, f"{j.name.value} = None,")
        if init_func and init_func.signature:
            if "->" in init_func.signature.meta["py_code"]:
                init_func.signature.meta["py_code"] = init_func.signature.meta[
                    "py_code"
                ].split("->")[0]
            if len(init_func.signature.meta["py_code"]):
                self.emit_ln(node, f"{init_func.signature.meta['py_code']},")
        self.emit_ln(node, " *args, **kwargs):")
        if not init_func:
            self.emit_ln(node, "super().__init__(*args, **kwargs)")
        for i in has_members:
            for j in i.vars.vars:
                if j.value:
                    self.emit_ln(
                        node,
                        f"self.{j.name.value} = {j.value.meta['py_code']} if {j.name.value} is "
                        f"None else {j.name.value}",
                    )
                else:
                    self.emit_ln(node, f"self.{j.name.value} = {j.name.value}")
        if init_func and init_func.body:
            self.emit(node, f"{init_func.body.meta['py_code']}")
        self.indent_level -= 1
        for i in node.members:
            if i not in has_members + static_has_members:
                self.emit(node, i.meta["py_code"])
                self.emit(node, "\n")

    def exit_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        doc: Optional[Token],
        is_static: bool,
        access: Optional[Token],
        vars: "HasVarList",
        is_frozen: bool,
        """
        self.emit(node, node.vars.meta["py_code"])

    def exit_has_var_list(self, node: ast.HasVarList) -> None:
        """Sub objects.

        vars: list[HasVar],
        """
        for i in node.vars:
            self.emit_ln(node, i.meta["py_code"])

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Token,
        type_tag: TypeSpec,
        value: Optional["ExprType"],
        """
        if node.value:
            self.emit(
                node,
                f"{node.name.value}: {node.type_tag.meta['py_code']} = {node.value.meta['py_code']}",
            )
        else:
            self.emit(
                node, f"{node.name.value}: {node.type_tag.meta['py_code']} = None"
            )

    def exit_type_spec_list(self, node: ast.TypeSpecList) -> None:
        """Sub objects.

        types: list[TypeSpec],
        """
        self.emit(node, "|".join([i.meta["py_code"] for i in node.types]))

    def exit_type_spec(self, node: ast.TypeSpec) -> None:
        """Sub objects.

        typ: "Token | DottedNameList",
        list_nest: TypeSpec,
        dict_nest: TypeSpec,
        """
        if node.dict_nest:
            self.emit(
                node,
                f"dict[{node.list_nest.meta['py_code']}, {node.dict_nest.meta['py_code']}]",
            )
        elif node.list_nest:
            self.emit(node, f"list[{node.list_nest.meta['py_code']}]")
        else:
            self.emit(node, node.spec_type.meta["py_code"])

    # NOTE: Incomplete for Jac Purple and Red
    def exit_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional["TypeList | TypeSpec"],
        return_type: Optional["TypeSpec"],
        """
        self.error("Event style abilities not supported in bootstrap Jac")

    def exit_dotted_name_list(self, node: ast.DottedNameList) -> None:
        """Sub objects.

        names: list[all_refs],
        """
        self.emit(node, ".".join([i.meta["py_code"] for i in node.names]))

    def exit_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        self.emit(node, ".".join([i.meta["py_code"] for i in node.archs]))

    def exit_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional[FuncParams],
        return_type: Optional[TypeSpec],
        self.is_arch_attached = False
        """
        if node.params:
            self.emit(node, node.params.meta["py_code"])
        if node.return_type:
            self.emit(node, f" -> {node.return_type.meta['py_code']}")

    def exit_func_params(self, node: ast.FuncParams) -> None:
        """Sub objects.

        params: list["ParamVar"],
        """
        first_out = False
        for i in node.params:
            self.emit(node, ", ") if first_out else None
            self.emit(node, i.meta["py_code"])
            first_out = True

    def exit_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Token,
        unpack: Optional[Token],
        type_tag: "TypeSpec",
        value: Optional["ExprType"],
        """
        if node.unpack:
            self.emit(node, f"{node.unpack.value}")
        if node.value:
            self.emit(
                node,
                f"{node.name.value}: {node.type_tag.meta['py_code']} = {node.value.meta['py_code']}",
            )
        else:
            self.emit(node, f"{node.name.value}: {node.type_tag.meta['py_code']}")

    def exit_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: BaseClasses,
        body: Optional[EnumBlock],
        """
        if node.decorators:
            self.emit_ln(node, node.decorators.meta["py_code"])
        if len(node.base_classes.base_classes):
            self.emit_ln(
                node,
                f"class {node.name.meta['py_code']}({node.base_classes.meta['py_code']}):",
            )
        else:
            self.needs_enum()
            self.emit_ln(node, f"class {node.name.value}(__jac_Enum__):")
        self.indent_level += 1
        if node.doc:
            self.emit_ln(node, node.doc.value)
        if node.body:
            self.emit(node, node.body.meta["py_code"])
        self.indent_level -= 1

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional[DottedNameList],
        body: EnumBlock,
        """

    def exit_enum_block(self, node: ast.EnumBlock) -> None:
        """Sub objects.

        stmts: list['Name|Assignment'],
        """
        for i in node.stmts:
            if isinstance(i, ast.Name):
                self.emit_ln(node, i.meta["py_code"] + " = __jac_auto__()")
            else:
                self.emit_ln(node, i.meta["py_code"])

    def exit_code_block(self, node: ast.CodeBlock) -> None:
        """Sub objects.

        stmts: list["StmtType"],
        """
        if len(node.stmts) == 0:
            self.emit_ln(node, "pass")
        for i in node.stmts:
            self.emit(node, i.meta["py_code"])
            if len(i.meta["py_code"]) and i.meta["py_code"][-1] != "\n":
                self.emit_ln(node, "\n")

    def exit_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        elseifs: Optional[ElseIfs],
        else_body: Optional[ElseStmt],
        """
        self.emit_ln(node, f"if {node.condition.meta['py_code']}:")
        self.indent_level += 1
        self.emit(node, node.body.meta["py_code"])
        self.indent_level -= 1
        self.emit(node, "\n")
        if node.elseifs:
            self.emit(node, node.elseifs.meta["py_code"])
        if node.else_body:
            self.emit(node, node.else_body.meta["py_code"])

    def exit_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: TypeList,
        body: CodeBlock,
        """
        self.ds_feature_warn()

    def exit_else_ifs(self, node: ast.ElseIfs) -> None:
        """Sub objects.

        elseifs: list[IfStmt],
        """
        for i in node.elseifs:
            self.emit_ln(node, f"elif {i.condition.meta['py_code']}:")
            self.indent_level += 1
            self.emit(node, i.body.meta["py_code"])
            self.indent_level -= 1
            self.emit(node, "\n")

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        self.emit_ln(node, "else:")
        self.indent_level += 1
        self.emit(node, node.body.meta["py_code"])
        self.indent_level -= 1
        self.emit(node, "\n")

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        excepts: Optional[ExceptList],
        finally_body: Optional[FinallyStmt],
        """
        self.emit_ln(node, "try:")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["py_code"])
        self.indent_level -= 1
        if node.excepts:
            self.emit_ln(node, node.excepts.meta["py_code"])
        if node.finally_body:
            self.emit_ln(node, node.finally_body.meta["py_code"])

    def exit_except(self, node: ast.Except) -> None:
        """Sub objects.

        typ: ExprType,
        name: Optional[Token],
        body: CodeBlock,
        """
        if node.name:
            self.emit_ln(
                node, f"except {node.ex_type.meta['py_code']} as {node.name.value}:"
            )
        else:
            self.emit_ln(node, f"except {node.ex_type.meta['py_code']}:")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["py_code"])
        self.indent_level -= 1

    def exit_except_list(self, node: ast.ExceptList) -> None:
        """Sub objects.

        excepts: list[Except],
        """
        for i in node.excepts:
            self.emit_ln(node, i.meta["py_code"])

    def exit_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: CodeBlock,
        """
        self.emit_ln(node, "finally:")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["py_code"])
        self.indent_level -= 1

    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: CodeBlock,
        """
        self.emit_ln(node, f"{node.iter.meta['py_code']}")
        self.emit_ln(node, f"while {node.condition.meta['py_code']}:")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["py_code"])
        self.emit_ln(node, f"{node.count_by.meta['py_code']}")
        self.indent_level -= 1

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        name_list: Token,
        collection: ExprType,
        body: CodeBlock,
        """
        names = node.name_list.meta["py_code"]
        self.emit_ln(node, f"for {names} in {node.collection.meta['py_code']}:")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["py_code"])
        self.indent_level -= 1

    def exit_name_list(self, node: ast.NameList) -> None:
        """Sub objects.

        names: list[Name],
        """
        self.emit(node, ",".join([i.meta["py_code"] for i in node.names]))

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: CodeBlock,
        """
        self.emit_ln(node, f"while {node.condition.meta['py_code']}:")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["py_code"])
        self.indent_level -= 1

    def exit_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        exprs: "ExprAsItemList",
        body: "CodeBlock",
        """
        self.emit_ln(node, f"with {node.exprs.meta['py_code']}:")
        self.indent_level += 1
        self.emit_ln(node, node.body.meta["py_code"])
        self.indent_level -= 1

    def exit_expr_as_item_list(self, node: ast.ExprAsItemList) -> None:
        """Sub objects.

        items: list["ExprAsItem"],
        """
        self.emit(node, ", ".join([i.meta["py_code"] for i in node.items]))

    def exit_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: "ExprType",
        alias: Optional[Token],
        """
        if node.alias:
            self.emit(node, node.expr.meta["py_code"] + " as " + node.alias.value)
        else:
            self.emit(node, node.expr.meta["py_code"])

    def exit_raise_stmt(self, node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        """
        if node.cause:
            self.emit_ln(node, f"raise {node.cause.meta['py_code']}")
        else:
            self.emit_ln(node, "raise")

    def exit_assert_stmt(self, node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        """
        if node.error_msg:
            self.emit_ln(
                node,
                f"assert {node.condition.meta['py_code']}, {node.error_msg.meta['py_code']}",
            )
        else:
            self.emit_ln(node, f"assert {node.condition.meta['py_code']}")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """
        if node.ctrl.name == Tok.KW_SKIP:
            self.ds_feature_warn()
        else:
            self.emit_ln(node, node.ctrl.value)

    def exit_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.emit_ln(node, f"del {node.target.meta['py_code']}")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_report_stmt(self, node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """
        self.ds_feature_warn()

    def exit_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        if node.expr:
            self.emit_ln(node, f"return {node.expr.meta['py_code']}")
        else:
            self.emit_ln(node, "return")

    def exit_yield_stmt(self, node: ast.YieldStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        if node.expr:
            self.emit_ln(node, f"yield {node.expr.meta['py_code']}")
        else:
            self.emit_ln(node, "yield")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_visit_stmt(self, node: ast.VisitStmt) -> None:
        """Sub objects.

        vis_type: Optional[Token],
        target: Optional["ExprType"],
        else_body: Optional["ElseStmt"],
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        """Sub objects.

        hops: Optional[ExprType],
        else_body: Optional[ElseStmt],
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects."""
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_await_stmt(self, node: ast.AwaitStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.ds_feature_warn()

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        is_static: bool,
        target: AtomType,
        value: ExprType,
        """
        if node.is_static:
            self.warning("Static variable semantics is not supported in bootstrap Jac")
        self.emit(node, f"{node.target.meta['py_code']} = {node.value.meta['py_code']}")

    # NOTE: Incomplete for Jac Purple and Red
    def exit_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """
        if isinstance(node.op, (ast.DisconnectOp, ast.ConnectOp)):
            self.ds_feature_warn()
        if isinstance(node.op, ast.Token):
            if node.op.value in [
                *["+", "-", "*", "/", "%", "**"],
                *["+=", "-=", "*=", "/=", "%=", "**="],
                *[">>", "<<", ">>=", "<<="],
                *["//=", "&=", "|=", "^=", "~="],
                *["//", "&", "|", "^"],
                *[">", "<", ">=", "<=", "==", "!=", ":="],
                *["and", "or", "in", "not in", "is", "is not"],
            ]:
                self.emit(
                    node,
                    f"{node.left.meta['py_code']} {node.op.value} {node.right.meta['py_code']}",
                )
            elif node.op.name in [
                Tok.PIPE_FWD,
                Tok.KW_SPAWN,
                Tok.A_PIPE_FWD,
            ] and isinstance(node.left, ast.TupleVal):
                params = node.left.meta["py_code"]
                params = params.replace(",)", ")") if params[-2:] == ",)" else params
                self.emit(node, f"{node.right.meta['py_code']}{params}")
            elif node.op.name in [Tok.PIPE_BKWD, Tok.A_PIPE_BKWD] and isinstance(
                node.right, ast.TupleVal
            ):
                params = node.right.meta["py_code"]
                params = params.replace(",)", ")") if params[-2:] == ",)" else params
                self.emit(node, f"{node.left.meta['py_code']}{params}")
            elif node.op.name == Tok.PIPE_FWD and isinstance(node.right, ast.TupleVal):
                self.ds_feature_warn()
            elif node.op.name == Tok.PIPE_FWD:
                self.emit(
                    node, f"{node.right.meta['py_code']}({node.left.meta['py_code']}"
                )
                paren_count = (
                    node.meta["pipe_chain_count"]
                    if "pipe_chain_count" in node.meta
                    else 1
                )
                if (
                    isinstance(node.parent, ast.BinaryExpr)
                    and isinstance(node.parent.op, ast.Token)
                    and node.parent.op.name == Tok.PIPE_FWD
                ):
                    node.parent.meta["pipe_chain_count"] = paren_count + 1
                else:
                    self.emit(node, ")" * paren_count)

            elif node.op.name in [Tok.KW_SPAWN, Tok.A_PIPE_FWD]:
                self.emit(
                    node, f"{node.right.meta['py_code']}({node.left.meta['py_code']}"
                )
                paren_count = (
                    node.meta["a_pipe_chain_count"]
                    if "a_pipe_chain_count" in node.meta
                    else 1
                )
                if (
                    isinstance(node.parent, ast.BinaryExpr)
                    and isinstance(node.parent.op, ast.Token)
                    and node.parent.op.name
                    in [
                        Tok.KW_SPAWN,
                        Tok.A_PIPE_FWD,
                    ]
                ):
                    node.parent.meta["a_pipe_chain_count"] = paren_count + 1
                else:
                    self.emit(node, ")" * paren_count)

            elif node.op.name in [Tok.PIPE_BKWD, Tok.A_PIPE_BKWD]:
                self.emit(
                    node, f"{node.left.meta['py_code']}({node.right.meta['py_code']})"
                )
            elif node.op.name == Tok.ELVIS_OP:
                self.emit(
                    node,
                    f"{Con.JAC_TMP} "
                    f"if ({Con.JAC_TMP} := ({node.left.meta['py_code']})) is not None "
                    f"else {node.right.meta['py_code']}",
                )
            else:
                self.error(
                    f"Binary operator {node.op.value} not supported in bootstrap Jac"
                )

    def exit_if_else_expr(self, node: ast.IfElseExpr) -> None:
        """Sub objects.

        condition: BinaryExpr | IfElseExpr,
        value: ExprType,
        else_value: ExprType,
        """
        self.emit(
            node,
            f"{node.value.meta['py_code']} if {node.condition.meta['py_code']} "
            f"else {node.else_value.meta['py_code']}",
        )

    def exit_unary_expr(self, node: ast.UnaryExpr) -> None:
        """Sub objects.

        operand: ExprType,
        op: Token,
        """
        if node.op.value in ["-", "~", "+"]:
            self.emit(node, f"{node.op.value}{node.operand.meta['py_code']}")
        elif node.op.value == "(":  # (expression) reuses unary expr
            self.emit(node, f"({node.operand.meta['py_code']})")
        elif node.op.value == "not":
            self.emit(node, f"not {node.operand.meta['py_code']}")
        elif node.op.name in [Tok.PIPE_FWD, Tok.KW_SPAWN, Tok.A_PIPE_FWD]:
            self.emit(node, f"{node.operand.meta['py_code']}()")
        else:
            self.error(f"Unary operator {node.op.value} not supported in bootstrap Jac")

    def exit_unpack_expr(self, node: ast.UnpackExpr) -> None:
        """Sub objects.

        target: ExprType,
        is_dict: bool,
        """
        if node.is_dict:
            self.emit(node, f"**{node.target.meta['py_code']}")
        else:
            self.emit(node, f"*{node.target.meta['py_code']}")

    def exit_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: list[Token],
        """
        for string in node.strings:
            self.emit(node, string.meta["py_code"])

    def exit_list_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.emit(
            node, f"[{', '.join([value.meta['py_code'] for value in node.values])}]"
        )

    def exit_set_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.emit(
            node, f"{{{', '.join([value.meta['py_code'] for value in node.values])}}}"
        )

    def exit_tuple_val(self, node: ast.TupleVal) -> None:
        """Sub objects.

        first_expr: Optional["ExprType"],
        exprs: Optional[ExprList],
        assigns: Optional[AssignmentList],
        """
        self.emit(node, "(")
        if node.first_expr:
            self.emit(node, f"{node.first_expr.meta['py_code']}")
        if not node.exprs and not node.assigns:
            self.emit(node, ",)")
        if node.exprs:
            self.emit(node, f", {node.exprs.meta['py_code']}")

        if node.assigns:
            if node.first_expr:
                self.emit(node, f", {node.assigns.meta['py_code']}")
            else:
                self.emit(node, f"{node.assigns.meta['py_code']}")
        self.emit(node, ")")

    def exit_expr_list(self, node: ast.ExprList) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.emit(
            node, f"{', '.join([value.meta['py_code'] for value in node.values])}"
        )

    def exit_dict_val(self, node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: list["KVPair"],
        """
        self.emit(
            node,
            f"{{{', '.join([kv_pair.meta['py_code'] for kv_pair in node.kv_pairs])}}}",
        )

    def exit_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        name_list: NameList,
        collection: ExprType,
        conditional: Optional[ExprType],
        is_list: bool,
        is_gen: bool,
        is_set: bool,
        """
        names = node.name_list.meta["py_code"]
        partial = (
            f"{node.out_expr.meta['py_code']} for {names} "
            f"in {node.collection.meta['py_code']}"
        )
        if node.conditional:
            partial += f" if {node.conditional.meta['py_code']}"
        if node.is_list:
            self.emit(node, f"[{partial}]")
        elif node.is_set:
            self.emit(node, f"{{{partial}}}")
        elif node.is_gen:
            self.emit(node, f"({partial})")

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        outk_expr: ExprType,
        outv_expr: ExprType,
        name_list: NameList,
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        names = node.name_list.meta["py_code"]
        partial = (
            f"{node.outk_expr.meta['py_code']}: {node.outv_expr.meta['py_code']} for "
            f"{names}"
        )
        partial += f" in {node.collection.meta['py_code']}"
        if node.conditional:
            partial += f" if {node.conditional.meta['py_code']}"
        self.emit(node, f"{{{partial}}}")

    def exit_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """
        self.emit(node, f"{node.key.meta['py_code']}: {node.value.meta['py_code']}")

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: AtomType,
        right: IndexSlice | ArchRefType | Token,
        null_ok: bool,
        """
        if node.null_ok:
            if isinstance(node.right, ast.IndexSlice):
                self.emit(
                    node,
                    f"({node.target.meta['py_code']}{node.right.meta['py_code']} "
                    f"if {node.target.meta['py_code']} is not None else None)",
                )
            else:
                self.emit(
                    node,
                    f"({node.target.meta['py_code']}.{node.right.meta['py_code']} "
                    f"if {node.target.meta['py_code']} is not None else None)",
                )
        else:
            if isinstance(node.right, ast.IndexSlice):
                self.emit(
                    node,
                    f"{node.target.meta['py_code']}{node.right.meta['py_code']}",
                )
            else:
                self.emit(
                    node,
                    f"{node.target.meta['py_code']}.{node.right.meta['py_code']}",
                )

    # NOTE: Incomplete for Jac Purple and Red
    def exit_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: AtomType,
        params: Optional[ParamList],
        """
        if node.params:
            self.emit(
                node,
                f"{node.target.meta['py_code']}({node.params.meta['py_code']})",
            )
        else:
            self.emit(node, f"{node.target.meta['py_code']}()")

    def exit_param_list(self, node: ast.ParamList) -> None:
        """Sub objects.

        p_args: Optional[ExprList],
        p_kwargs: Optional[AssignmentList],
        """
        if node.p_args and node.p_kwargs:
            self.emit(
                node,
                f"{node.p_args.meta['py_code']}, {node.p_kwargs.meta['py_code']}",
            )
        elif node.p_args:
            self.emit(node, f"{node.p_args.meta['py_code']}")
        elif node.p_kwargs:
            self.emit(node, f"{node.p_kwargs.meta['py_code']}")

    def exit_assignment_list(self, node: ast.AssignmentList) -> None:
        """Sub objects.

        values: list[Assignment],
        """
        if isinstance(node.parent, ast.GlobalVars):
            for i in node.values:
                self.emit_ln(node, i.meta["py_code"])
        else:
            self.emit(
                node, f"{', '.join([value.meta['py_code'] for value in node.values])}"
            )

    def exit_index_slice(self, node: ast.IndexSlice) -> None:
        """Sub objects.

        start: ExprType,
        stop: Optional[ExprType],
        """
        if node.is_range:
            self.emit(
                node,
                f"[{node.start.meta['py_code'] if node.start else ''}:"
                f"{node.stop.meta['py_code'] if node.stop else ''}]",
            )
        elif node.start:
            self.emit(node, f"[{node.start.meta['py_code']}]")
        else:
            self.ice("Something went horribly wrong.")

    def exit_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        """Sub objects.

        var: Token,
        """
        self.emit(node, node.py_resolve_name())

    # NOTE: Incomplete for Jac Purple and Red (maybe for global)
    def exit_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        name: Name,
        arch: Token,
        """
        self.emit(node, node.py_resolve_name())

    # NOTE: Incomplete for Jac Purple and Red
    def exit_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_cond: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_disconnect_op(self, node: ast.DisconnectOp) -> None:
        """Sub objects.

        filter_cond: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red
    def exit_connect_op(self, node: ast.ConnectOp) -> None:
        """Sub objects.

        spawn: Optional[ExprType],
        edge_dir: EdgeDir,
        """
        self.ds_feature_warn()

    # NOTE: Incomplete for Jac Purple and Red (to consider)
    def exit_filter_compr(self, node: ast.FilterCompr) -> None:
        """Sub objects.

        compares: list[BinaryExpr],
        """
        self.ds_feature_warn()

    def exit_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: list["Token | ExprType"],
        """
        self.emit(node, 'f"')
        for part in node.parts:
            if isinstance(part, ast.Token) and part.name == "PIECE":
                self.emit(node, f"{part.meta['py_code']}")
            else:
                self.emit(node, "{" + part.meta["py_code"] + "}")
        self.emit(node, '"')

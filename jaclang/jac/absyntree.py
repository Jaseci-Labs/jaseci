"""Abstract class for IR Passes for Jac."""
from __future__ import annotations

import pprint
from typing import Optional, Union

from jaclang.jac.constant import Constants as Con, EdgeDir
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.symtable import SymbolTable


class AstNode:
    """Abstract syntax tree node for Jac."""

    def __init__(self, mod_link: Optional[Module], kid: list[AstNode]) -> None:
        """Initialize ast."""
        self.parent: Optional[AstNode] = None
        self.kid = [x.set_parent(self) for x in kid]
        self.mod_link = mod_link
        self.sym_tab: Optional[SymbolTable] = None
        self._sub_node_tab: dict[AstNode, list[AstNode]] = {}
        self._typ: type = type(None)
        self.meta: dict = {}
        self.tok_range: tuple[Token, Token] = self.resolve_tok_range()

    @property
    def line(self) -> int:
        """Get line number."""
        return self.tok_range[0].line_no

    def add_kids_left(self, nodes: list[AstNode]) -> AstNode:
        """Add kid left."""
        self.kid = [*nodes, *self.kid]
        for i in nodes:
            i.parent = self
        self.tok_range = self.resolve_tok_range()
        return self

    def add_kids_right(self, nodes: list[AstNode]) -> AstNode:
        """Add kid right."""
        self.kid = [*self.kid, *nodes]
        for i in nodes:
            i.parent = self
        self.tok_range = self.resolve_tok_range()
        return self

    def set_kids(self, nodes: list[AstNode]) -> AstNode:
        """Set kids."""
        self.kid = nodes
        for i in nodes:
            i.parent = self
        self.tok_range = self.resolve_tok_range()
        return self

    def set_parent(self, parent: AstNode) -> AstNode:
        """Set parent."""
        self.parent = parent
        return self

    def resolve_tok_range(self) -> tuple[Token, Token]:
        """Get token range."""
        if len(self.kid):
            return (
                self.kid[0].tok_range[0],
                self.kid[-1].tok_range[1],
            )
        elif isinstance(self, Token):
            return (self, self)
        else:
            raise ValueError(f"Empty kid for Token {type(self).__name__}")

    def to_dict(self) -> dict:
        """Return dict representation of node."""
        ret = {
            "node": str(type(self).__name__),
            "kid": [x.to_dict() for x in self.kid if x],
            "line": self.tok_range[0].line,
        }
        if isinstance(self, Token):
            ret["name"] = self.name
            ret["value"] = self.value
        return ret

    def print(self, depth: Optional[int] = None) -> None:
        """Print ast."""
        pprint.PrettyPrinter(depth=depth).pprint(self.to_dict())


# AST Mid Level Node Types
# --------------------------
class Module(AstNode):
    """Whole Program node type for Jac Ast."""

    def __init__(
        self,
        name: str,
        doc: Optional[Token],
        body: list[AstNode],
        mod_path: str,
        rel_mod_path: str,
        is_imported: bool,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize whole program node."""
        self.name = name
        self.doc = doc
        self.body = body
        self.mod_path = mod_path
        self.rel_mod_path = rel_mod_path
        self.is_imported = is_imported
        super().__init__(
            mod_link=mod_link,
            kid=kid,
        )


class GlobalVars(AstNode):
    """GlobalVars node type for Jac Ast."""

    def __init__(
        self,
        access: Optional[AccessTag],
        assignments: list[Assignment],
        is_frozen: bool,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize global var node."""
        self.doc: Optional[Constant] = None
        self.access = access
        self.assignments = assignments
        self.is_frozen = is_frozen
        super().__init__(mod_link=mod_link, kid=kid)


class AccessTag(AstNode):
    """AccessTag node type for Jac Ast."""

    def __init__(
        self,
        access: Token,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize access tag node."""
        self.access = access
        super().__init__(mod_link=mod_link, kid=kid)


class Test(AstNode):
    """Test node type for Jac Ast."""

    TEST_COUNT = 0

    def __init__(
        self,
        name: Name | Token,
        doc: Optional[Token],
        body: CodeBlock,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize test node."""
        self.doc = doc
        Test.TEST_COUNT += 1 if isinstance(name, Token) else 0
        self.name: Name = (  # for auto generated test names
            name
            if isinstance(name, Name)
            else Name(
                name="NAME",
                value=f"test_{Test.TEST_COUNT}",
                col_start=name.col_start,
                col_end=name.col_end,
                tok_range=name.tok_range,
                already_declared=False,
                parent=name.parent,
                mod_link=name.mod_link,
                kid=name.kid,
                sym_tab=name.sym_tab,
            )
        )
        # kid[0] = self.name  # Index is 0 since Doc string is inserted after init
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class ModuleCode(AstNode):
    """Free mod code for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Token],
        name: Optional[Name],
        body: CodeBlock,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize test node."""
        self.doc = doc
        self.name = name
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class PyInlineCode(AstNode):
    """Inline Python code node type for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Constant],
        code: Token,
        mod_link: Optional[Module],
        kid: list[AstNode],
        tok_range: tuple[Token, Token],
    ) -> None:
        """Initialize inline python code node."""
        self.doc = doc
        self.code = code
        super().__init__(mod_link=mod_link, kid=kid, tok_range=tok_range)


class Import(AstNode):
    """Import node type for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Constant],
        lang: Name,
        path: ModulePath,
        alias: Optional[Name],
        items: Optional[ModuleItems],
        is_absorb: bool,  # For includes
        mod_link: Optional[Module],
        kid: list[AstNode],
        sub_module: Optional["Module"] = None,
    ) -> None:
        """Initialize import node."""
        self.doc = doc
        self.lang = lang
        self.path = path
        self.alias = alias
        self.items = items
        self.is_absorb = is_absorb
        self.sub_module = sub_module

        super().__init__(mod_link=mod_link, kid=kid)


class ModulePath(AstNode):
    """ModulePath node type for Jac Ast."""

    def __init__(
        self,
        path: list[Name],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize module path node."""
        self.path = path
        self.path_str = "".join([p.value for p in path])
        super().__init__(mod_link=mod_link, kid=kid)


class ModuleItems(AstNode):
    """ModuleItems node type for Jac Ast."""

    def __init__(
        self,
        items: list[ModuleItem],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize module items node."""
        self.items = items
        super().__init__(mod_link=mod_link, kid=kid)


class ModuleItem(AstNode):
    """ModuleItem node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        alias: Optional[Token],
        mod_link: Optional[Module],
        kid: list[AstNode],
        body: Optional[AstNode] = None,
    ) -> None:
        """Initialize module item node."""
        self.name = name
        self.alias = alias
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class Architype(AstNode):
    """ObjectArch node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        arch_type: Token,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[AccessTag],
        base_classes: BaseClasses,
        body: Optional[ArchBlock],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize object arch node."""
        self.name = name
        self.arch_type = arch_type
        self.doc = doc
        self.decorators = decorators
        self.base_classes = base_classes
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class ArchDef(AstNode):
    """ArchDef node type for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Token],
        target: ArchRefChain,
        body: ArchBlock,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize arch def node."""
        self.doc = doc
        self.target = target
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class Decorators(AstNode):
    """Decorators node type for Jac Ast."""

    def __init__(
        self,
        calls: list[ExprType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize decorators node."""
        self.calls = calls
        super().__init__(mod_link=mod_link, kid=kid)


class BaseClasses(AstNode):
    """BaseArch node type for Jac Ast."""

    def __init__(
        self,
        base_classes: list[DottedNameList],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize base classes node."""
        self.base_classes = base_classes
        super().__init__(mod_link=mod_link, kid=kid)


class Ability(AstNode):
    """Ability node type for Jac Ast."""

    def __init__(
        self,
        name_ref: Name | SpecialVarRef,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        is_abstract: bool,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[AccessTag],
        signature: Optional[FuncSignature | TypeSpec | EventSignature],
        body: Optional[CodeBlock],
        mod_link: Optional[Module],
        kid: list[AstNode],
        arch_attached: Optional[ArchBlock] = None,
    ) -> None:
        """Initialize func arch node."""
        self.name_ref = name_ref
        self.is_func = is_func
        self.is_async = is_async
        self.is_static = is_static
        self.is_abstract = is_abstract
        self.doc = doc
        self.decorators = decorators

        self.signature = signature
        self.body = body
        self.arch_attached = arch_attached
        super().__init__(mod_link=mod_link, kid=kid)

    def py_resolve_name(self) -> str:
        """Resolve name."""
        if isinstance(self.name_ref, Name):
            return self.name_ref.value
        elif isinstance(self.name_ref, (SpecialVarRef, ArchRef)):
            return self.name_ref.py_resolve_name()
        else:
            raise NotImplementedError


class AbilityDef(AstNode):
    """AbilityDef node type for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Token],
        target: ArchRefChain,
        signature: FuncSignature | EventSignature,
        body: CodeBlock,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize ability def node."""
        self.doc = doc
        self.target = target
        self.signature = signature
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class EventSignature(AstNode):
    """EventSignature node type for Jac Ast."""

    def __init__(
        self,
        event: Token,
        arch_tag_info: Optional[TypeSpecList],
        return_type: Optional["TypeSpec"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize event signature node."""
        self.event = event
        self.arch_tag_info = arch_tag_info
        self.return_type = return_type
        super().__init__(mod_link=mod_link, kid=kid)


class DottedNameList(AstNode):
    """DottedNameList node type for Jac Ast."""

    def __init__(
        self,
        names: list[Token | SpecialVarRef | Name],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize name list node."""
        self.names = names
        super().__init__(mod_link=mod_link, kid=kid)


class ArchRefChain(AstNode):
    """Arch ref list node type for Jac Ast."""

    def __init__(
        self,
        archs: list[ArchRef],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize name list ."""
        self.archs = archs
        super().__init__(mod_link=mod_link, kid=kid)

    def py_resolve_name(self) -> str:
        """Resolve name."""
        return ".".join(
            [f"({x.arch.value[1]}){x.py_resolve_name()}" for x in self.archs]
        )


class FuncSignature(AstNode):
    """FuncSignature node type for Jac Ast."""

    def __init__(
        self,
        params: Optional["FuncParams"],
        return_type: Optional["TypeSpec"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize method signature node."""
        self.params = params
        self.return_type = return_type
        super().__init__(mod_link=mod_link, kid=kid)


class FuncParams(AstNode):
    """ArchBlock node type for Jac Ast."""

    def __init__(
        self,
        params: list["ParamVar"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize method params node."""
        self.params = params
        super().__init__(mod_link=mod_link, kid=kid)


class ParamVar(AstNode):
    """ParamVar node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        unpack: Optional[Token],
        type_tag: "TypeSpec",
        value: Optional[ExprType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize param var node."""
        self.name = name
        self.unpack = unpack
        self.type_tag = type_tag
        self.value = value
        super().__init__(mod_link=mod_link, kid=kid)


class Enum(AstNode):
    """Enum node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[AccessTag],
        base_classes: "BaseClasses",
        body: Optional["EnumBlock"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize object arch node."""
        self.name = name
        self.doc = doc
        self.decorators = decorators
        self.base_classes = base_classes
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class EnumDef(AstNode):
    """EnumDef node type for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Token],
        target: ArchRefChain,
        body: EnumBlock,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize arch def node."""
        self.doc = doc
        self.target = target
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class EnumBlock(AstNode):
    """EnumBlock node type for Jac Ast."""

    def __init__(
        self,
        stmts: list["Name|Assignment"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize enum block node."""
        self.stmts = stmts
        super().__init__(mod_link=mod_link, kid=kid)


class ArchBlock(AstNode):
    """ArchBlock node type for Jac Ast."""

    def __init__(
        self,
        members: list[ArchHas | Ability],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize arch block node."""
        self.members = members
        super().__init__(mod_link=mod_link, kid=kid)


class ArchHas(AstNode):
    """HasStmt node type for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Token],
        is_static: bool,
        access: Optional[AccessTag],
        vars: HasVarList,
        is_frozen: bool,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize has statement node."""
        self.doc = doc
        self.is_static = is_static
        self.vars = vars
        self.is_frozen = is_frozen
        super().__init__(mod_link=mod_link, kid=kid)


class HasVarList(AstNode):
    """HasVarList node type for Jac Ast."""

    def __init__(
        self,
        vars: list["HasVar"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize has var list node."""
        self.vars = vars
        super().__init__(mod_link=mod_link, kid=kid)


class HasVar(AstNode):
    """HasVar node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        type_tag: "TypeSpec",
        value: Optional[ExprType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize has var node."""
        self.name = name
        self.type_tag = type_tag
        self.value = value
        super().__init__(mod_link=mod_link, kid=kid)


class TypeSpecList(AstNode):
    """TypeSpecList node type for Jac Ast."""

    def __init__(
        self,
        types: list[TypeSpec],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize type list node."""
        self.types = types
        super().__init__(mod_link=mod_link, kid=kid)


class TypeSpec(AstNode):
    """TypeSpec node type for Jac Ast."""

    def __init__(
        self,
        spec_type: Token | DottedNameList,
        list_nest: TypeSpec,  # needed for lists
        dict_nest: TypeSpec,  # needed for dicts, uses list_nest as key
        null_ok: bool,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize type spec node."""
        self.spec_type = spec_type
        self.list_nest = list_nest
        self.dict_nest = dict_nest
        self.null_ok = null_ok
        super().__init__(mod_link=mod_link, kid=kid)


class CodeBlock(AstNode):
    """CodeBlock node type for Jac Ast."""

    def __init__(
        self,
        stmts: list[StmtType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize code block node."""
        self.stmts = stmts
        super().__init__(mod_link=mod_link, kid=kid)


class TypedCtxBlock(AstNode):
    """TypedCtxBlock node type for Jac Ast."""

    def __init__(
        self,
        type_ctx: TypeSpecList,
        body: CodeBlock,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize typed context block node."""
        self.type_ctx = type_ctx
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class IfStmt(AstNode):
    """IfStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: ExprType,
        body: "CodeBlock",
        elseifs: Optional["ElseIfs"],
        else_body: Optional["ElseStmt"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize if statement node."""
        self.condition = condition
        self.body = body
        self.elseifs = elseifs
        self.else_body = else_body
        super().__init__(mod_link=mod_link, kid=kid)


class ElseIfs(AstNode):
    """ElseIfs node type for Jac Ast."""

    def __init__(
        self,
        elseifs: list["IfStmt"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize elseifs node."""
        self.elseifs = elseifs
        super().__init__(mod_link=mod_link, kid=kid)


class ElseStmt(AstNode):
    """Else node type for Jac Ast."""

    def __init__(
        self,
        body: "CodeBlock",
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize else node."""
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class TryStmt(AstNode):
    """TryStmt node type for Jac Ast."""

    def __init__(
        self,
        body: "CodeBlock",
        excepts: Optional["ExceptList"],
        finally_body: Optional["FinallyStmt"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize try statement node."""
        self.body = body
        self.excepts = excepts
        self.finally_body = finally_body
        super().__init__(mod_link=mod_link, kid=kid)


class ExceptList(AstNode):
    """ExceptList node type for Jac Ast."""

    def __init__(
        self,
        excepts: list["Except"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize excepts node."""
        self.excepts = excepts
        super().__init__(mod_link=mod_link, kid=kid)


class Except(AstNode):
    """Except node type for Jac Ast."""

    def __init__(
        self,
        ex_type: ExprType,
        name: Optional[Token],
        body: "CodeBlock",
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize except node."""
        self.ex_type = ex_type
        self.name = name
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class FinallyStmt(AstNode):
    """FinallyStmt node type for Jac Ast."""

    def __init__(
        self,
        body: "CodeBlock",
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize finally statement node."""
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class IterForStmt(AstNode):
    """IterFor node type for Jac Ast."""

    def __init__(
        self,
        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: CodeBlock,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize iter for node."""
        self.iter = iter
        self.condition = condition
        self.count_by = count_by
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class InForStmt(AstNode):
    """InFor node type for Jac Ast."""

    def __init__(
        self,
        name_list: NameList,
        collection: ExprType,
        body: CodeBlock,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize in for node."""
        self.name_list = name_list
        self.collection = collection
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class NameList(AstNode):
    """NameList node type for Jac Ast."""

    def __init__(
        self,
        names: list[Name],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize name list node."""
        self.names = names
        super().__init__(mod_link=mod_link, kid=kid)


class WhileStmt(AstNode):
    """WhileStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: ExprType,
        body: "CodeBlock",
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize while statement node."""
        self.condition = condition
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class WithStmt(AstNode):
    """WithStmt node type for Jac Ast."""

    def __init__(
        self,
        exprs: "ExprAsItemList",
        body: "CodeBlock",
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize with statement node."""
        self.exprs = exprs
        self.body = body
        super().__init__(mod_link=mod_link, kid=kid)


class ExprAsItemList(AstNode):
    """ExprAsItemList node type for Jac Ast."""

    def __init__(
        self,
        items: list["ExprAsItem"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize module items node."""
        self.items = items
        super().__init__(mod_link=mod_link, kid=kid)


class ExprAsItem(AstNode):
    """ExprAsItem node type for Jac Ast."""

    def __init__(
        self,
        expr: ExprType,
        alias: Optional[Name],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize module item node."""
        self.expr = expr
        self.alias = alias
        super().__init__(mod_link=mod_link, kid=kid)


class RaiseStmt(AstNode):
    """RaiseStmt node type for Jac Ast."""

    def __init__(
        self,
        cause: Optional[ExprType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize raise statement node."""
        self.cause = cause
        super().__init__(mod_link=mod_link, kid=kid)


class AssertStmt(AstNode):
    """AssertStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: ExprType,
        error_msg: Optional[ExprType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize assert statement node."""
        self.condition = condition
        self.error_msg = error_msg
        super().__init__(mod_link=mod_link, kid=kid)


class CtrlStmt(AstNode):
    """CtrlStmt node type for Jac Ast."""

    def __init__(
        self,
        ctrl: Token,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize control statement node."""
        self.ctrl = ctrl
        super().__init__(mod_link=mod_link, kid=kid)


class DeleteStmt(AstNode):
    """DeleteStmt node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize delete statement node."""
        self.target = target
        super().__init__(mod_link=mod_link, kid=kid)


class ReportStmt(AstNode):
    """ReportStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: ExprType,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize report statement node."""
        self.expr = expr
        super().__init__(mod_link=mod_link, kid=kid)


class ReturnStmt(AstNode):
    """ReturnStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: Optional[ExprType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize return statement node."""
        self.expr = expr
        super().__init__(mod_link=mod_link, kid=kid)


class YieldStmt(AstNode):
    """YieldStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: Optional[ExprType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize yeild statement node."""
        self.expr = expr
        super().__init__(mod_link=mod_link, kid=kid)


class IgnoreStmt(AstNode):
    """IgnoreStmt node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize ignore statement node."""
        self.target = target
        super().__init__(mod_link=mod_link, kid=kid)


class WalkerStmtOnlyNode(AstNode):
    """WalkerStmtOnlyNode node type for Jac Ast."""

    def __init__(
        self,
        mod_link: Optional[Module],
        kid: list[AstNode],
        from_walker: bool = False,
    ) -> None:
        """Initialize walker statement only node."""
        self.from_walker = from_walker
        super().__init__(mod_link=mod_link, kid=kid)


class VisitStmt(WalkerStmtOnlyNode):
    """VisitStmt node type for Jac Ast."""

    def __init__(
        self,
        vis_type: Optional[Token],
        target: ExprType,
        else_body: Optional["ElseStmt"],
        mod_link: Optional[Module],
        kid: list[AstNode],
        from_walker: bool = False,
    ) -> None:
        """Initialize visit statement node."""
        self.vis_type = vis_type
        self.target = target
        self.else_body = else_body
        super().__init__(
            mod_link=mod_link,
            kid=kid,
            from_walker=from_walker,
        )


class RevisitStmt(WalkerStmtOnlyNode):
    """ReVisitStmt node type for Jac Ast."""

    def __init__(
        self,
        hops: Optional[ExprType],
        else_body: Optional["ElseStmt"],
        mod_link: Optional[Module],
        kid: list[AstNode],
        from_walker: bool = False,
    ) -> None:
        """Initialize revisit statement node."""
        self.hops = hops
        self.else_body = else_body
        super().__init__(
            mod_link=mod_link,
            kid=kid,
            from_walker=from_walker,
        )


class DisengageStmt(WalkerStmtOnlyNode):
    """DisengageStmt node type for Jac Ast."""

    def __init__(
        self,
        mod_link: Optional[Module],
        kid: list[AstNode],
        from_walker: bool = False,
    ) -> None:
        """Initialize disengage statement node."""
        super().__init__(
            mod_link=mod_link,
            kid=kid,
            from_walker=from_walker,
        )


class AwaitStmt(AstNode):
    """AwaitStmt node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize sync statement node."""
        self.target = target
        super().__init__(mod_link=mod_link, kid=kid)


class Assignment(AstNode):
    """Assignment node type for Jac Ast."""

    def __init__(
        self,
        is_static: bool,
        target: AtomType,
        value: ExprType,
        mutable: bool,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize assignment node."""
        self.is_static = is_static
        self.target = target
        self.value = value
        self.mutable = mutable
        super().__init__(mod_link=mod_link, kid=kid)


class BinaryExpr(AstNode):
    """ExprBinary node type for Jac Ast."""

    def __init__(
        self,
        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize binary expression node."""
        self.left = left
        self.right = right
        self.op = op
        super().__init__(mod_link=mod_link, kid=kid)


class IfElseExpr(AstNode):
    """ExprIfElse node type for Jac Ast."""

    def __init__(
        self,
        condition: "BinaryExpr | IfElseExpr",
        value: ExprType,
        else_value: ExprType,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize if else expression node."""
        self.condition = condition
        self.value = value
        self.else_value = else_value
        super().__init__(mod_link=mod_link, kid=kid)


class UnaryExpr(AstNode):
    """ExprUnary node type for Jac Ast."""

    def __init__(
        self,
        operand: ExprType,
        op: Token,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize unary expression node."""
        self.operand = operand
        self.op = op
        super().__init__(mod_link=mod_link, kid=kid)


class UnpackExpr(AstNode):
    """ExprUnpack node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        is_dict: bool,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize unpack expression node."""
        self.target = target
        self.is_dict = is_dict
        super().__init__(mod_link=mod_link, kid=kid)


class MultiString(AstNode):
    """ExprMultiString node type for Jac Ast."""

    def __init__(
        self,
        strings: list["Token | FString"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize multi string expression node."""
        self.strings = strings
        super().__init__(mod_link=mod_link, kid=kid)


class ExprList(AstNode):
    """ExprList node type for Jac Ast."""

    def __init__(
        self,
        values: list[ExprType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize expr value node."""
        self.values = values
        super().__init__(mod_link=mod_link, kid=kid)


class ListVal(ExprList):
    """ListVal node type for Jac Ast."""


class SetVal(ExprList):
    """SetVal node type for Jac Ast."""


class TupleVal(AstNode):
    """TupleVal node type for Jac Ast."""

    def __init__(
        self,
        first_expr: Optional[ExprType],
        exprs: Optional[ExprList],
        assigns: Optional[AssignmentList],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize tuple value node."""
        self.first_expr = first_expr
        self.exprs = exprs
        self.assigns = assigns
        super().__init__(mod_link=mod_link, kid=kid)


class DictVal(AstNode):
    """ExprDict node type for Jac Ast."""

    def __init__(
        self,
        kv_pairs: list["KVPair"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize dict expression node."""
        self.kv_pairs = kv_pairs
        super().__init__(mod_link=mod_link, kid=kid)


class InnerCompr(AstNode):
    """ListCompr node type for Jac Ast."""

    def __init__(
        self,
        out_expr: ExprType,
        name_list: NameList,
        collection: ExprType,
        conditional: Optional[ExprType],
        is_list: bool,
        is_gen: bool,
        is_set: bool,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize comprehension expression node."""
        self.out_expr = out_expr
        self.name_list = name_list
        self.collection = collection
        self.conditional = conditional
        self.is_list = is_list
        self.is_gen = is_gen
        self.is_set = is_set

        super().__init__(mod_link=mod_link, kid=kid)


class DictCompr(AstNode):
    """DictCompr node type for Jac Ast."""

    def __init__(
        self,
        outk_expr: ExprType,
        outv_expr: ExprType,
        name_list: NameList,
        collection: ExprType,
        conditional: Optional[ExprType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize comprehension expression node."""
        self.outk_expr = outk_expr
        self.outv_expr = outv_expr
        self.name_list = name_list
        self.collection = collection
        self.conditional = conditional
        super().__init__(mod_link=mod_link, kid=kid)


class KVPair(AstNode):
    """ExprKVPair node type for Jac Ast."""

    def __init__(
        self,
        key: ExprType,
        value: ExprType,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize key value pair expression node."""
        self.key = key
        self.value = value
        super().__init__(mod_link=mod_link, kid=kid)


class AtomTrailer(AstNode):
    """AtomTrailer node type for Jac Ast."""

    def __init__(
        self,
        target: AtomType,
        right: IndexSlice | ArchRef | Token,
        null_ok: bool,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize atom trailer expression node."""
        self.target = target
        self.right = right
        self.null_ok = null_ok
        super().__init__(mod_link=mod_link, kid=kid)


class FuncCall(AstNode):
    """FuncCall node type for Jac Ast."""

    def __init__(
        self,
        target: "AtomType",
        params: Optional["ParamList"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize function call expression node."""
        self.target = target
        self.params = params
        super().__init__(mod_link=mod_link, kid=kid)


class ParamList(AstNode):
    """ParamList node type for Jac Ast."""

    def __init__(
        self,
        p_args: Optional[ExprList],
        p_kwargs: Optional["AssignmentList"],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize parameter list expression node."""
        self.p_args = p_args
        self.p_kwargs = p_kwargs
        super().__init__(mod_link=mod_link, kid=kid)


class IndexSlice(AstNode):
    """IndexSlice node type for Jac Ast."""

    def __init__(
        self,
        start: Optional[ExprType],
        stop: Optional[ExprType],
        is_range: bool,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize index slice expression node."""
        self.start = start
        self.stop = stop
        self.is_range = is_range
        super().__init__(mod_link=mod_link, kid=kid)


class ArchRef(AstNode):
    """GlobalRef node type for Jac Ast."""

    def __init__(
        self,
        name_ref: Name | SpecialVarRef,
        arch: Token,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize global reference expression node."""
        self.name_ref = name_ref
        self.arch = arch
        super().__init__(mod_link=mod_link, kid=kid)

    def py_resolve_name(self) -> str:
        """Resolve name."""
        if isinstance(self.name_ref, Name):
            return self.name_ref.value
        elif isinstance(self.name_ref, SpecialVarRef):
            return self.name_ref.py_resolve_name()
        else:
            raise NotImplementedError


class SpecialVarRef(AstNode):
    """HereRef node type for Jac Ast."""

    def __init__(
        self,
        var: Token,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize special var reference expression node."""
        self.var = var
        super().__init__(mod_link=mod_link, kid=kid)

    def py_resolve_name(self) -> str:
        """Resolve name."""
        if self.var.name == Tok.SELF_OP:
            return "self"
        elif self.var.name == Tok.SUPER_OP:
            return "super()"
        elif self.var.name == Tok.ROOT_OP:
            return Con.ROOT
        elif self.var.name == Tok.HERE_OP:
            return Con.HERE
        elif self.var.name == Tok.INIT_OP:
            return "__init__"
        else:
            raise NotImplementedError("ICE: Special var reference not implemented")


class EdgeOpRef(WalkerStmtOnlyNode):
    """EdgeOpRef node type for Jac Ast."""

    def __init__(
        self,
        filter_type: Optional[ExprType],
        filter_cond: Optional[FilterCompr],
        edge_dir: EdgeDir,
        mod_link: Optional[Module],
        kid: list[AstNode],
        from_walker: bool = False,
    ) -> None:
        """Initialize edge op reference expression node."""
        self.filter_type = filter_type
        self.filter_cond = filter_cond
        self.edge_dir = edge_dir
        super().__init__(
            mod_link=mod_link,
            kid=kid,
            from_walker=from_walker,
        )


class DisconnectOp(EdgeOpRef):
    """DisconnectOpRef node type for Jac Ast."""


class ConnectOp(AstNode):
    """ConnectOpRef node type for Jac Ast."""

    def __init__(
        self,
        conn_type: Optional[ExprType],
        conn_assign: Optional[AssignmentList],
        edge_dir: EdgeDir,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize connect op reference expression node."""
        self.conn_type = conn_type
        self.conn_assign = conn_assign
        self.edge_dir = edge_dir
        super().__init__(mod_link=mod_link, kid=kid)


class FilterCompr(AstNode):
    """FilterCtx node type for Jac Ast."""

    def __init__(
        self,
        compares: list[BinaryExpr],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize filter_cond context expression node."""
        self.compares = compares
        super().__init__(mod_link=mod_link, kid=kid)


class FString(AstNode):
    """FString node type for Jac Ast."""

    def __init__(
        self,
        parts: list[Token | ExprType],
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize fstring expression node."""
        self.parts = parts
        super().__init__(mod_link=mod_link, kid=kid)


# AST Parse-Tree Node Types


# --------------------------
class Parse(AstNode):
    """Parse node type for Jac Ast."""

    def __init__(
        self,
        name: str,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize parse."""
        self.name = name
        super().__init__(mod_link=mod_link, kid=kid)

    def __repr__(self) -> str:
        """Return string representation of parse node."""
        return super().__repr__() + f" ({self.name})" + " line: " + str(self.line)


class Token(AstNode):
    """Token node type for Jac Ast."""

    def __init__(
        self,
        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize token."""
        self.name = name
        self.value = value
        self.line_no = line
        self.col_start = col_start
        self.col_end = col_end
        super().__init__(mod_link=mod_link, kid=kid)


class Name(Token):
    """Name node type for Jac Ast."""

    def __init__(
        self,
        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        already_declared: bool,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize name."""
        self.already_declared = already_declared
        super().__init__(
            name=name,
            value=value,
            line=line,
            col_start=col_start,
            col_end=col_end,
            mod_link=mod_link,
            kid=kid,
        )


class Constant(Token):
    """Constant node type for Jac Ast."""

    def __init__(
        self,
        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        typ: type,
        mod_link: Optional[Module],
        kid: list[AstNode],
    ) -> None:
        """Initialize constant."""
        super().__init__(
            name=name,
            value=value,
            line=line,
            col_start=col_start,
            col_end=col_end,
            mod_link=mod_link,
            kid=kid,
        )
        self._typ = typ


class SourceString(Token):
    """SourceString node type for Jac Ast."""

    def __init__(
        self,
        source: str,
    ) -> None:
        """Initialize source string."""
        super().__init__(
            name="",
            value=source,
            line=0,
            col_start=0,
            col_end=0,
            mod_link=None,
            kid=[],
        )


# ----------------


ElementType = Union[
    GlobalVars,
    Test,
    ModuleCode,
    Import,
    Architype,
    Ability,
    PyInlineCode,
    Import,
]

AtomType = Union[
    MultiString,
    ListVal,
    TupleVal,
    SetVal,
    DictVal,
    InnerCompr,
    DictCompr,
    AtomTrailer,
    EdgeOpRef,
    FilterCompr,
]

ExprType = Union[
    UnaryExpr,
    BinaryExpr,
    IfElseExpr,
    UnpackExpr,
    AtomType,
]


StmtType = Union[
    Import,
    Architype,
    Ability,
    Assignment,
    ExprType,
    IfStmt,
    TryStmt,
    IterForStmt,
    InForStmt,
    WhileStmt,
    WithStmt,
    RaiseStmt,
    AssertStmt,
    CtrlStmt,
    DeleteStmt,
    ReportStmt,
    ReturnStmt,
    YieldStmt,
    AwaitStmt,
    DisengageStmt,
    RevisitStmt,
    VisitStmt,
    IgnoreStmt,
]


# Utiliiy functions
# -----------------


def replace_node(node: AstNode, new_node: Optional[AstNode]) -> AstNode | None:
    """Replace node with new_node."""
    if node.parent:
        node.parent.kid[node.parent.kid.index(node)] = new_node
    if new_node:
        new_node.parent = node.parent
        for i in new_node.kid:
            if i:
                i.parent = new_node
    return new_node


def append_node(
    node: AstNode, new_node: Optional[AstNode], front: bool = False
) -> AstNode | None:
    """Replace node with new_node."""
    if front:
        node.kid.insert(0, new_node)
    else:
        node.kid.append(new_node)
    if new_node:
        new_node.parent = node
    return new_node

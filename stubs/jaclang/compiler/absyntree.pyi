import ast as ast3
from _typeshed import Incomplete
from jaclang.compiler import TOKEN_MAP as TOKEN_MAP
from jaclang.compiler.codeloc import (
    CodeGenTarget as CodeGenTarget,
    CodeLocInfo as CodeLocInfo,
)
from jaclang.compiler.constant import (
    DELIM_MAP as DELIM_MAP,
    EdgeDir as EdgeDir,
    JacSemTokenModifier as SemTokMod,
    JacSemTokenType as SemTokType,
    SymbolAccess as SymbolAccess,
    SymbolType as SymbolType,
    Tokens as Tok,
)
from jaclang.compiler.semtable import SemRegistry as SemRegistry
from jaclang.compiler.symtable import Symbol as Symbol, SymbolTable as SymbolTable
from jaclang.utils.treeprinter import (
    dotgen_ast_tree as dotgen_ast_tree,
    print_ast_tree as print_ast_tree,
)
from types import EllipsisType
from typing import Any, Callable, Generic, Sequence, TypeVar

class AstNode:
    parent: Incomplete
    kid: Incomplete
    gen: Incomplete
    meta: Incomplete
    loc: Incomplete
    def __init__(self, kid: Sequence[AstNode]) -> None: ...
    @property
    def sym_tab(self) -> SymbolTable: ...
    @sym_tab.setter
    def sym_tab(self, sym_tab: SymbolTable) -> None: ...
    def add_kids_left(
        self, nodes: Sequence[AstNode], pos_update: bool = True
    ) -> AstNode: ...
    def add_kids_right(
        self, nodes: Sequence[AstNode], pos_update: bool = True
    ) -> AstNode: ...
    def insert_kids_at_pos(
        self, nodes: Sequence[AstNode], pos: int, pos_update: bool = True
    ) -> AstNode: ...
    def set_kids(self, nodes: Sequence[AstNode]) -> AstNode: ...
    def set_parent(self, parent: AstNode) -> AstNode: ...
    def resolve_tok_range(self) -> tuple[Token, Token]: ...
    def gen_token(self, name: Tok, value: str | None = None) -> Token: ...
    def get_all_sub_nodes(self, typ: type[T], brute_force: bool = True) -> list[T]: ...
    def find_parent_of_type(self, typ: type[T]) -> T | None: ...
    def parent_of_type(self, typ: type[T]) -> T: ...
    def format(self) -> str: ...
    def to_dict(self) -> dict[str, str]: ...
    def pp(self, depth: int | None = None) -> str: ...
    def dotgen(self) -> str: ...
    def flatten(self) -> list[AstNode]: ...
    def normalize(self, deep: bool = False) -> bool: ...
    def unparse(self) -> str: ...

class AstSymbolNode(AstNode):
    name_spec: Incomplete
    def __init__(
        self, sym_name: str, name_spec: NameAtom, sym_category: SymbolType
    ) -> None: ...
    @property
    def sym(self) -> Symbol | None: ...
    @property
    def sym_name(self) -> str: ...
    @property
    def sym_category(self) -> SymbolType: ...
    @property
    def py_ctx_func(self) -> type[ast3.AST]: ...
    @property
    def sym_type(self) -> str: ...
    @property
    def type_sym_tab(self) -> SymbolTable | None: ...

class AstSymbolStubNode(AstSymbolNode):
    def __init__(self, sym_type: SymbolType) -> None: ...

class AstAccessNode(AstNode):
    access: Incomplete
    def __init__(self, access: SubTag[Token] | None) -> None: ...
    @property
    def access_type(self) -> SymbolAccess: ...

T = TypeVar("T", bound=AstNode)

class AstDocNode(AstNode):
    doc: Incomplete
    def __init__(self, doc: String | None) -> None: ...

class AstSemStrNode(AstNode):
    semstr: Incomplete
    def __init__(self, semstr: String | None) -> None: ...

class AstAsyncNode(AstNode):
    is_async: Incomplete
    def __init__(self, is_async: bool) -> None: ...

class AstElseBodyNode(AstNode):
    else_body: Incomplete
    def __init__(self, else_body: ElseStmt | ElseIf | None) -> None: ...

class AstTypedVarNode(AstNode):
    type_tag: Incomplete
    def __init__(self, type_tag: SubTag[Expr] | None) -> None: ...

class WalkerStmtOnlyNode(AstNode):
    from_walker: bool
    def __init__(self) -> None: ...

class Expr(AstNode): ...
class AtomExpr(Expr, AstSymbolStubNode): ...
class ElementStmt(AstDocNode): ...
class ArchBlockStmt(AstNode): ...
class EnumBlockStmt(AstNode): ...
class CodeBlockStmt(AstNode): ...

class AstImplOnlyNode(CodeBlockStmt, ElementStmt, AstSymbolNode):
    target: Incomplete
    body: Incomplete
    decl_link: Incomplete
    def __init__(
        self, target: ArchRefChain, body: SubNodeList, decl_link: AstNode | None
    ) -> None: ...
    @property
    def sym_tab(self) -> SymbolTable: ...
    @sym_tab.setter
    def sym_tab(self, sym_tab: SymbolTable) -> None: ...
    def create_impl_name_node(self) -> Name: ...

class AstImplNeedingNode(AstSymbolNode, Generic[T]):
    body: Incomplete
    def __init__(self, body: T | None) -> None: ...
    @property
    def needs_impl(self) -> bool: ...

class NameAtom(AtomExpr, EnumBlockStmt):
    name_of: Incomplete
    def __init__(self) -> None: ...
    @property
    def sym(self) -> Symbol | None: ...
    @sym.setter
    def sym(self, sym: Symbol) -> None: ...
    @property
    def sym_name(self) -> str: ...
    @property
    def sym_category(self) -> SymbolType: ...
    @property
    def clean_type(self) -> str: ...
    @property
    def py_ctx_func(self) -> type[ast3.AST]: ...
    @py_ctx_func.setter
    def py_ctx_func(self, py_ctx_func: type[ast3.AST]) -> None: ...
    @property
    def sym_type(self) -> str: ...
    @sym_type.setter
    def sym_type(self, sym_type: str) -> None: ...
    @property
    def type_sym_tab(self) -> SymbolTable | None: ...
    @type_sym_tab.setter
    def type_sym_tab(self, type_sym_tab: SymbolTable) -> None: ...
    @property
    def sem_token(self) -> tuple[SemTokType, SemTokMod] | None: ...

class ArchSpec(ElementStmt, CodeBlockStmt, AstSymbolNode, AstDocNode, AstSemStrNode):
    decorators: Incomplete
    def __init__(self, decorators: SubNodeList[Expr] | None = None) -> None: ...

class MatchPattern(AstNode): ...

class SubTag(AstNode, Generic[T]):
    tag: Incomplete
    def __init__(self, tag: T, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class SubNodeList(AstNode, Generic[T]):
    items: Incomplete
    delim: Incomplete
    left_enc: Incomplete
    right_enc: Incomplete
    def __init__(
        self,
        items: list[T],
        delim: Tok | None,
        kid: Sequence[AstNode],
        left_enc: Token | None = None,
        right_enc: Token | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class Module(AstDocNode):
    name: Incomplete
    source: Incomplete
    body: Incomplete
    is_imported: Incomplete
    stub_only: Incomplete
    impl_mod: Incomplete
    test_mod: Incomplete
    mod_deps: Incomplete
    registry: Incomplete
    terminals: Incomplete
    def __init__(
        self,
        name: str,
        source: JacSource,
        doc: String | None,
        body: Sequence[ElementStmt | String | EmptyToken],
        is_imported: bool,
        terminals: list[Token],
        kid: Sequence[AstNode],
        stub_only: bool = False,
        registry: SemRegistry | None = None,
    ) -> None: ...
    @property
    def annexable_by(self) -> str | None: ...
    def normalize(self, deep: bool = False) -> bool: ...
    def unparse(self) -> str: ...

class GlobalVars(ElementStmt, AstAccessNode):
    assignments: Incomplete
    is_frozen: Incomplete
    def __init__(
        self,
        access: SubTag[Token] | None,
        assignments: SubNodeList[Assignment],
        is_frozen: bool,
        kid: Sequence[AstNode],
        doc: String | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class Test(AstSymbolNode, ElementStmt):
    TEST_COUNT: int
    name: Incomplete
    body: Incomplete
    def __init__(
        self,
        name: Name | Token,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
        doc: String | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ModuleCode(ElementStmt, ArchBlockStmt, EnumBlockStmt):
    name: Incomplete
    body: Incomplete
    def __init__(
        self,
        name: SubTag[Name] | None,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
        doc: String | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class PyInlineCode(ElementStmt, ArchBlockStmt, EnumBlockStmt, CodeBlockStmt):
    code: Incomplete
    def __init__(
        self, code: Token, kid: Sequence[AstNode], doc: String | None = None
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class Import(ElementStmt, CodeBlockStmt):
    hint: Incomplete
    from_loc: Incomplete
    items: Incomplete
    is_absorb: Incomplete
    def __init__(
        self,
        hint: SubTag[Name] | None,
        from_loc: ModulePath | None,
        items: SubNodeList[ModuleItem] | SubNodeList[ModulePath],
        is_absorb: bool,
        kid: Sequence[AstNode],
        doc: String | None = None,
    ) -> None: ...
    @property
    def is_py(self) -> bool: ...
    @property
    def is_jac(self) -> bool: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ModulePath(AstSymbolNode):
    path: Incomplete
    level: Incomplete
    alias: Incomplete
    sub_module: Incomplete
    def __init__(
        self,
        path: list[Name] | None,
        level: int,
        alias: Name | None,
        kid: Sequence[AstNode],
    ) -> None: ...
    @property
    def path_str(self) -> str: ...
    def resolve_relative_path(self, target_item: str | None = None) -> str: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ModuleItem(AstSymbolNode):
    name: Incomplete
    alias: Incomplete
    sub_module: Incomplete
    def __init__(
        self, name: Name, alias: Name | None, kid: Sequence[AstNode]
    ) -> None: ...
    @property
    def from_parent(self) -> Import: ...
    @property
    def from_mod_path(self) -> ModulePath: ...
    def normalize(self, deep: bool = False) -> bool: ...

class Architype(ArchSpec, AstAccessNode, ArchBlockStmt, AstImplNeedingNode):
    name: Incomplete
    arch_type: Incomplete
    base_classes: Incomplete
    def __init__(
        self,
        name: Name,
        arch_type: Token,
        access: SubTag[Token] | None,
        base_classes: SubNodeList[Expr] | None,
        body: SubNodeList[ArchBlockStmt] | ArchDef | None,
        kid: Sequence[AstNode],
        doc: String | None = None,
        semstr: String | None = None,
        decorators: SubNodeList[Expr] | None = None,
    ) -> None: ...
    @property
    def is_abstract(self) -> bool: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ArchDef(AstImplOnlyNode):
    def __init__(
        self,
        target: ArchRefChain,
        body: SubNodeList[ArchBlockStmt],
        kid: Sequence[AstNode],
        doc: String | None = None,
        decl_link: Architype | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class Enum(ArchSpec, AstAccessNode, AstImplNeedingNode, ArchBlockStmt):
    name: Incomplete
    base_classes: Incomplete
    def __init__(
        self,
        name: Name,
        access: SubTag[Token] | None,
        base_classes: SubNodeList[Expr] | None,
        body: SubNodeList[EnumBlockStmt] | EnumDef | None,
        kid: Sequence[AstNode],
        doc: String | None = None,
        semstr: String | None = None,
        decorators: SubNodeList[Expr] | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class EnumDef(AstImplOnlyNode):
    def __init__(
        self,
        target: ArchRefChain,
        body: SubNodeList[EnumBlockStmt],
        kid: Sequence[AstNode],
        doc: String | None = None,
        decorators: SubNodeList[Expr] | None = None,
        decl_link: Enum | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class Ability(
    AstAccessNode,
    ElementStmt,
    AstAsyncNode,
    ArchBlockStmt,
    EnumBlockStmt,
    CodeBlockStmt,
    AstSemStrNode,
    AstImplNeedingNode,
):
    name_ref: Incomplete
    is_override: Incomplete
    is_static: Incomplete
    is_abstract: Incomplete
    decorators: Incomplete
    signature: Incomplete
    def __init__(
        self,
        name_ref: NameAtom,
        is_async: bool,
        is_override: bool,
        is_static: bool,
        is_abstract: bool,
        access: SubTag[Token] | None,
        signature: FuncSignature | EventSignature,
        body: SubNodeList[CodeBlockStmt] | AbilityDef | FuncCall | None,
        kid: Sequence[AstNode],
        semstr: String | None = None,
        doc: String | None = None,
        decorators: SubNodeList[Expr] | None = None,
    ) -> None: ...
    @property
    def is_method(self) -> bool: ...
    @property
    def owner_method(self) -> Architype | Enum | None: ...
    @property
    def is_genai_ability(self) -> bool: ...
    def py_resolve_name(self) -> str: ...
    def normalize(self, deep: bool = False) -> bool: ...

class AbilityDef(AstImplOnlyNode):
    signature: Incomplete
    decorators: Incomplete
    def __init__(
        self,
        target: ArchRefChain,
        signature: FuncSignature | EventSignature,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
        doc: String | None = None,
        decorators: SubNodeList[Expr] | None = None,
        decl_link: Ability | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class FuncSignature(AstSemStrNode):
    params: Incomplete
    return_type: Incomplete
    is_method: bool
    def __init__(
        self,
        params: SubNodeList[ParamVar] | None,
        return_type: Expr | None,
        kid: Sequence[AstNode],
        semstr: String | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...
    @property
    def is_static(self) -> bool: ...

class EventSignature(AstSemStrNode):
    event: Incomplete
    arch_tag_info: Incomplete
    return_type: Incomplete
    is_method: bool
    def __init__(
        self,
        event: Token,
        arch_tag_info: Expr | None,
        return_type: Expr | None,
        kid: Sequence[AstNode],
        semstr: String | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ArchRefChain(AstNode):
    archs: Incomplete
    def __init__(self, archs: list[ArchRef], kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...
    def py_resolve_name(self) -> str: ...
    def flat_name(self) -> str: ...

class ParamVar(AstSymbolNode, AstTypedVarNode, AstSemStrNode):
    name: Incomplete
    unpack: Incomplete
    value: Incomplete
    def __init__(
        self,
        name: Name,
        unpack: Token | None,
        type_tag: SubTag[Expr],
        value: Expr | None,
        kid: Sequence[AstNode],
        semstr: String | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = True) -> bool: ...

class ArchHas(AstAccessNode, AstDocNode, ArchBlockStmt):
    is_static: Incomplete
    vars: Incomplete
    is_frozen: Incomplete
    def __init__(
        self,
        is_static: bool,
        access: SubTag[Token] | None,
        vars: SubNodeList[HasVar],
        is_frozen: bool,
        kid: Sequence[AstNode],
        doc: String | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class HasVar(AstSymbolNode, AstTypedVarNode, AstSemStrNode):
    name: Incomplete
    value: Incomplete
    defer: Incomplete
    def __init__(
        self,
        name: Name,
        type_tag: SubTag[Expr],
        value: Expr | None,
        defer: bool,
        kid: Sequence[AstNode],
        semstr: String | None = None,
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class TypedCtxBlock(CodeBlockStmt):
    type_ctx: Incomplete
    body: Incomplete
    def __init__(
        self, type_ctx: Expr, body: SubNodeList[CodeBlockStmt], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class IfStmt(CodeBlockStmt, AstElseBodyNode):
    condition: Incomplete
    body: Incomplete
    def __init__(
        self,
        condition: Expr,
        body: SubNodeList[CodeBlockStmt],
        else_body: ElseStmt | ElseIf | None,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ElseIf(IfStmt):
    def normalize(self, deep: bool = False) -> bool: ...

class ElseStmt(AstNode):
    body: Incomplete
    def __init__(
        self, body: SubNodeList[CodeBlockStmt], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ExprStmt(CodeBlockStmt):
    expr: Incomplete
    in_fstring: Incomplete
    def __init__(
        self, expr: Expr, in_fstring: bool, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = True) -> bool: ...

class TryStmt(AstElseBodyNode, CodeBlockStmt):
    body: Incomplete
    excepts: Incomplete
    finally_body: Incomplete
    def __init__(
        self,
        body: SubNodeList[CodeBlockStmt],
        excepts: SubNodeList[Except] | None,
        else_body: ElseStmt | None,
        finally_body: FinallyStmt | None,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class Except(CodeBlockStmt):
    ex_type: Incomplete
    name: Incomplete
    body: Incomplete
    def __init__(
        self,
        ex_type: Expr,
        name: Name | None,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class FinallyStmt(CodeBlockStmt):
    body: Incomplete
    def __init__(
        self, body: SubNodeList[CodeBlockStmt], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class IterForStmt(AstAsyncNode, AstElseBodyNode, CodeBlockStmt):
    iter: Incomplete
    condition: Incomplete
    count_by: Incomplete
    body: Incomplete
    def __init__(
        self,
        iter: Assignment,
        is_async: bool,
        condition: Expr,
        count_by: Assignment,
        body: SubNodeList[CodeBlockStmt],
        else_body: ElseStmt | None,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class InForStmt(AstAsyncNode, AstElseBodyNode, CodeBlockStmt):
    target: Incomplete
    collection: Incomplete
    body: Incomplete
    def __init__(
        self,
        target: Expr,
        is_async: bool,
        collection: Expr,
        body: SubNodeList[CodeBlockStmt],
        else_body: ElseStmt | None,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class WhileStmt(CodeBlockStmt):
    condition: Incomplete
    body: Incomplete
    def __init__(
        self, condition: Expr, body: SubNodeList[CodeBlockStmt], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class WithStmt(AstAsyncNode, CodeBlockStmt):
    exprs: Incomplete
    body: Incomplete
    def __init__(
        self,
        is_async: bool,
        exprs: SubNodeList[ExprAsItem],
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ExprAsItem(AstNode):
    expr: Incomplete
    alias: Incomplete
    def __init__(
        self, expr: Expr, alias: Expr | None, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = True) -> bool: ...

class RaiseStmt(CodeBlockStmt):
    cause: Incomplete
    from_target: Incomplete
    def __init__(
        self, cause: Expr | None, from_target: Expr | None, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class AssertStmt(CodeBlockStmt):
    condition: Incomplete
    error_msg: Incomplete
    def __init__(
        self, condition: Expr, error_msg: Expr | None, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class CheckStmt(CodeBlockStmt):
    target: Incomplete
    def __init__(self, target: Expr, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class CtrlStmt(CodeBlockStmt):
    ctrl: Incomplete
    def __init__(self, ctrl: Token, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class DeleteStmt(CodeBlockStmt):
    target: Incomplete
    def __init__(self, target: Expr, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ReportStmt(CodeBlockStmt):
    expr: Incomplete
    def __init__(self, expr: Expr, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ReturnStmt(CodeBlockStmt):
    expr: Incomplete
    def __init__(self, expr: Expr | None, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class IgnoreStmt(WalkerStmtOnlyNode, CodeBlockStmt):
    target: Incomplete
    def __init__(self, target: Expr, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class VisitStmt(WalkerStmtOnlyNode, AstElseBodyNode, CodeBlockStmt):
    vis_type: Incomplete
    target: Incomplete
    def __init__(
        self,
        vis_type: SubNodeList[Expr] | None,
        target: Expr,
        else_body: ElseStmt | None,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class RevisitStmt(WalkerStmtOnlyNode, AstElseBodyNode, CodeBlockStmt):
    hops: Incomplete
    def __init__(
        self, hops: Expr | None, else_body: ElseStmt | None, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class DisengageStmt(WalkerStmtOnlyNode, CodeBlockStmt):
    def __init__(self, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class AwaitExpr(Expr):
    target: Incomplete
    def __init__(self, target: Expr, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class GlobalStmt(CodeBlockStmt):
    target: Incomplete
    def __init__(
        self, target: SubNodeList[NameAtom], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class NonLocalStmt(GlobalStmt):
    def normalize(self, deep: bool = False) -> bool: ...

class Assignment(AstSemStrNode, AstTypedVarNode, EnumBlockStmt, CodeBlockStmt):
    target: Incomplete
    value: Incomplete
    mutable: Incomplete
    aug_op: Incomplete
    is_enum_stmt: Incomplete
    def __init__(
        self,
        target: SubNodeList[Expr],
        value: Expr | YieldExpr | None,
        type_tag: SubTag[Expr] | None,
        kid: Sequence[AstNode],
        mutable: bool = True,
        aug_op: Token | None = None,
        semstr: String | None = None,
        is_enum_stmt: bool = False,
    ) -> None: ...
    def normalize(self, deep: bool = True) -> bool: ...

class BinaryExpr(Expr):
    left: Incomplete
    right: Incomplete
    op: Incomplete
    def __init__(
        self,
        left: Expr,
        right: Expr,
        op: Token | DisconnectOp | ConnectOp,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class CompareExpr(Expr):
    left: Incomplete
    rights: Incomplete
    ops: Incomplete
    def __init__(
        self, left: Expr, rights: list[Expr], ops: list[Token], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class BoolExpr(Expr):
    values: Incomplete
    op: Incomplete
    def __init__(
        self, op: Token, values: list[Expr], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class LambdaExpr(Expr):
    signature: Incomplete
    body: Incomplete
    def __init__(
        self, body: Expr, kid: Sequence[AstNode], signature: FuncSignature | None = None
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class UnaryExpr(Expr):
    operand: Incomplete
    op: Incomplete
    def __init__(self, operand: Expr, op: Token, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class IfElseExpr(Expr):
    condition: Incomplete
    value: Incomplete
    else_value: Incomplete
    def __init__(
        self, condition: Expr, value: Expr, else_value: Expr, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MultiString(AtomExpr):
    strings: Incomplete
    def __init__(
        self, strings: Sequence[String | FString], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class FString(AtomExpr):
    parts: Incomplete
    def __init__(
        self, parts: SubNodeList[String | ExprStmt] | None, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ListVal(AtomExpr):
    values: Incomplete
    def __init__(
        self, values: SubNodeList[Expr] | None, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class SetVal(AtomExpr):
    values: Incomplete
    def __init__(
        self, values: SubNodeList[Expr] | None, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class TupleVal(AtomExpr):
    values: Incomplete
    def __init__(
        self, values: SubNodeList[Expr | KWPair] | None, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class DictVal(AtomExpr):
    kv_pairs: Incomplete
    def __init__(self, kv_pairs: Sequence[KVPair], kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class KVPair(AstNode):
    key: Incomplete
    value: Incomplete
    def __init__(
        self, key: Expr | None, value: Expr, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class KWPair(AstNode):
    key: Incomplete
    value: Incomplete
    def __init__(
        self, key: NameAtom | None, value: Expr, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class InnerCompr(AstAsyncNode):
    target: Incomplete
    collection: Incomplete
    conditional: Incomplete
    def __init__(
        self,
        is_async: bool,
        target: Expr,
        collection: Expr,
        conditional: list[Expr] | None,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ListCompr(AtomExpr):
    out_expr: Incomplete
    compr: Incomplete
    def __init__(
        self, out_expr: Expr, compr: list[InnerCompr], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class GenCompr(ListCompr):
    def normalize(self, deep: bool = False) -> bool: ...

class SetCompr(ListCompr):
    def normalize(self, deep: bool = False) -> bool: ...

class DictCompr(AtomExpr):
    kv_pair: Incomplete
    compr: Incomplete
    def __init__(
        self, kv_pair: KVPair, compr: list[InnerCompr], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class AtomTrailer(Expr):
    target: Incomplete
    right: Incomplete
    is_attr: Incomplete
    is_null_ok: Incomplete
    is_genai: Incomplete
    def __init__(
        self,
        target: Expr,
        right: AtomExpr | Expr,
        is_attr: bool,
        is_null_ok: bool,
        kid: Sequence[AstNode],
        is_genai: bool = False,
    ) -> None: ...
    def normalize(self, deep: bool = True) -> bool: ...
    @property
    def as_attr_list(self) -> list[AstSymbolNode]: ...

class AtomUnit(Expr):
    value: Incomplete
    def __init__(self, value: Expr | YieldExpr, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = True) -> bool: ...

class YieldExpr(Expr):
    expr: Incomplete
    with_from: Incomplete
    def __init__(
        self, expr: Expr | None, with_from: bool, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class FuncCall(Expr):
    target: Incomplete
    params: Incomplete
    genai_call: Incomplete
    def __init__(
        self,
        target: Expr,
        params: SubNodeList[Expr | KWPair] | None,
        genai_call: FuncCall | None,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = True) -> bool: ...

class IndexSlice(AtomExpr):
    start: Incomplete
    stop: Incomplete
    step: Incomplete
    is_range: Incomplete
    def __init__(
        self,
        start: Expr | None,
        stop: Expr | None,
        step: Expr | None,
        is_range: bool,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = True) -> bool: ...

class ArchRef(AtomExpr):
    arch_name: Incomplete
    arch_type: Incomplete
    def __init__(
        self, arch_name: NameAtom, arch_type: Token, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class EdgeRefTrailer(Expr):
    chain: Incomplete
    edges_only: Incomplete
    def __init__(
        self, chain: list[Expr | FilterCompr], edges_only: bool, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = True) -> bool: ...

class EdgeOpRef(WalkerStmtOnlyNode, AtomExpr):
    filter_cond: Incomplete
    edge_dir: Incomplete
    def __init__(
        self, filter_cond: FilterCompr | None, edge_dir: EdgeDir, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class DisconnectOp(WalkerStmtOnlyNode):
    edge_spec: Incomplete
    def __init__(self, edge_spec: EdgeOpRef, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class ConnectOp(AstNode):
    conn_type: Incomplete
    conn_assign: Incomplete
    edge_dir: Incomplete
    def __init__(
        self,
        conn_type: Expr | None,
        conn_assign: AssignCompr | None,
        edge_dir: EdgeDir,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class FilterCompr(AtomExpr):
    f_type: Incomplete
    compares: Incomplete
    def __init__(
        self,
        f_type: Expr | None,
        compares: SubNodeList[CompareExpr] | None,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class AssignCompr(AtomExpr):
    assigns: Incomplete
    def __init__(
        self, assigns: SubNodeList[KWPair], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchStmt(CodeBlockStmt):
    target: Incomplete
    cases: Incomplete
    def __init__(
        self, target: Expr, cases: list[MatchCase], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchCase(AstNode):
    pattern: Incomplete
    guard: Incomplete
    body: Incomplete
    def __init__(
        self,
        pattern: MatchPattern,
        guard: Expr | None,
        body: list[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchOr(MatchPattern):
    patterns: Incomplete
    def __init__(
        self, patterns: list[MatchPattern], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchAs(MatchPattern):
    name: Incomplete
    pattern: Incomplete
    def __init__(
        self, name: NameAtom, pattern: MatchPattern | None, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchWild(MatchPattern):
    def normalize(self, deep: bool = False) -> bool: ...

class MatchValue(MatchPattern):
    value: Incomplete
    def __init__(self, value: Expr, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchSingleton(MatchPattern):
    value: Incomplete
    def __init__(self, value: Bool | Null, kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchSequence(MatchPattern):
    values: Incomplete
    def __init__(self, values: list[MatchPattern], kid: Sequence[AstNode]) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchMapping(MatchPattern):
    values: Incomplete
    def __init__(
        self, values: list[MatchKVPair | MatchStar], kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchKVPair(MatchPattern):
    key: Incomplete
    value: Incomplete
    def __init__(
        self, key: MatchPattern | NameAtom, value: MatchPattern, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchStar(MatchPattern):
    name: Incomplete
    is_list: Incomplete
    def __init__(
        self, name: NameAtom, is_list: bool, kid: Sequence[AstNode]
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class MatchArch(MatchPattern):
    name: Incomplete
    arg_patterns: Incomplete
    kw_patterns: Incomplete
    def __init__(
        self,
        name: AtomTrailer | NameAtom,
        arg_patterns: SubNodeList[MatchPattern] | None,
        kw_patterns: SubNodeList[MatchKVPair] | None,
        kid: Sequence[AstNode],
    ) -> None: ...
    def normalize(self, deep: bool = False) -> bool: ...

class Token(AstNode):
    file_path: Incomplete
    name: Incomplete
    value: Incomplete
    line_no: Incomplete
    end_line: Incomplete
    c_start: Incomplete
    c_end: Incomplete
    pos_start: Incomplete
    pos_end: Incomplete
    def __init__(
        self,
        file_path: str,
        name: str,
        value: str,
        line: int,
        end_line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
    ) -> None: ...
    def normalize(self, deep: bool = True) -> bool: ...
    def unparse(self) -> str: ...

class Name(Token, NameAtom):
    is_enum_singleton: Incomplete
    is_kwesc: Incomplete
    def __init__(
        self,
        file_path: str,
        name: str,
        value: str,
        line: int,
        end_line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        is_enum_singleton: bool = False,
        is_kwesc: bool = False,
    ) -> None: ...
    def unparse(self) -> str: ...
    @staticmethod
    def gen_stub_from_node(
        node: AstSymbolNode, name_str: str, set_name_of: AstSymbolNode | None = None
    ) -> Name: ...

class SpecialVarRef(Name):
    orig: Incomplete
    def __init__(self, var: Name) -> None: ...
    def py_resolve_name(self) -> str: ...

class Literal(Token, AtomExpr):
    SYMBOL_TYPE: Incomplete
    type_map: Incomplete
    def __init__(
        self,
        file_path: str,
        name: str,
        value: str,
        line: int,
        end_line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
    ) -> None: ...
    @property
    def lit_value(
        self,
    ) -> int | str | float | bool | None | Callable[[], Any] | EllipsisType: ...

class BuiltinType(Name, Literal, NameAtom):
    SYMBOL_TYPE: Incomplete
    @property
    def lit_value(self) -> Callable[[], Any]: ...

class Float(Literal):
    SYMBOL_TYPE: Incomplete
    @property
    def lit_value(self) -> float: ...

class Int(Literal):
    SYMBOL_TYPE: Incomplete
    @property
    def lit_value(self) -> int: ...

class String(Literal):
    SYMBOL_TYPE: Incomplete
    @property
    def lit_value(self) -> str: ...
    value: Incomplete
    def normalize(self, deep: bool = True) -> bool: ...
    def unparse(self) -> str: ...

class Bool(Literal):
    SYMBOL_TYPE: Incomplete
    @property
    def lit_value(self) -> bool: ...

class Null(Literal):
    SYMBOL_TYPE: Incomplete
    @property
    def lit_value(self) -> None: ...

class Ellipsis(Literal):
    SYMBOL_TYPE: Incomplete
    @property
    def lit_value(self) -> EllipsisType: ...

class EmptyToken(Token):
    def __init__(self) -> None: ...

class Semi(Token, CodeBlockStmt): ...

class CommentToken(Token):
    is_inline: Incomplete
    def __init__(
        self,
        file_path: str,
        name: str,
        value: str,
        line: int,
        end_line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        kid: Sequence[AstNode],
        is_inline: bool = False,
    ) -> None: ...

class JacSource(EmptyToken):
    value: Incomplete
    hash: Incomplete
    file_path: Incomplete
    comments: Incomplete
    def __init__(self, source: str, mod_path: str) -> None: ...
    @property
    def code(self) -> str: ...

class PythonModuleAst(EmptyToken):
    ast: Incomplete
    file_path: Incomplete
    def __init__(self, ast: ast3.Module, mod_path: str) -> None: ...

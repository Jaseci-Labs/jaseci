"""Abstract class for IR Passes for Jac."""
from __future__ import annotations

import ast as ast3
from typing import Any, Callable, Generic, Optional, Sequence, Type, TypeVar

from jaclang.compiler.codeloc import CodeGenTarget, CodeLocInfo
from jaclang.compiler.constant import Constants as Con, EdgeDir
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.symtable import Symbol, SymbolAccess, SymbolTable, SymbolType
from jaclang.utils.treeprinter import dotgen_ast_tree, print_ast_tree


class AstNode:
    """Abstract syntax tree node for Jac."""

    def __init__(self, kid: Sequence[AstNode]) -> None:
        """Initialize ast."""
        self.parent: Optional[AstNode] = None
        self.kid: list[AstNode] = [x.set_parent(self) for x in kid]
        self.sym_tab: Optional[SymbolTable] = None
        self._sub_node_tab: dict[type, list[AstNode]] = {}
        self._typ: type = type(None)
        self.gen: CodeGenTarget = CodeGenTarget()
        self.meta: dict[str, str] = {}
        self.loc: CodeLocInfo = CodeLocInfo(*self.resolve_tok_range())

    def add_kids_left(
        self, nodes: Sequence[AstNode], pos_update: bool = True
    ) -> AstNode:
        """Add kid left."""
        self.kid = [*nodes, *self.kid]
        if pos_update:
            for i in nodes:
                i.parent = self
            self.loc.update_first_token(self.kid[0].loc.first_tok)
        return self

    def add_kids_right(
        self, nodes: Sequence[AstNode], pos_update: bool = True
    ) -> AstNode:
        """Add kid right."""
        self.kid = [*self.kid, *nodes]
        if pos_update:
            for i in nodes:
                i.parent = self
            self.loc.update_last_token(self.kid[-1].loc.last_tok)
        return self

    def set_kids(self, nodes: Sequence[AstNode]) -> AstNode:
        """Set kids."""
        self.kid = [*nodes]
        for i in nodes:
            i.parent = self
        self.loc.update_token_range(*self.resolve_tok_range())
        return self

    def set_parent(self, parent: AstNode) -> AstNode:
        """Set parent."""
        self.parent = parent
        return self

    def resolve_tok_range(self) -> tuple[Token, Token]:
        """Get token range."""
        if len(self.kid):
            return (
                self.kid[0].loc.first_tok,
                self.kid[-1].loc.last_tok,
            )
        elif isinstance(self, Token):
            return (self, self)
        else:
            raise ValueError(f"Empty kid for Token {type(self).__name__}")

    def get_all_sub_nodes(self, typ: Type[T], brute_force: bool = True) -> list[T]:
        """Get all sub nodes of type."""
        from jaclang.compiler.passes import Pass

        return Pass.get_all_sub_nodes(node=self, typ=typ, brute_force=brute_force)

    def to_dict(self) -> dict[str, str]:
        """Return dict representation of node."""
        ret = {
            "node": str(type(self).__name__),
            "kid": str([x.to_dict() for x in self.kid if x]),
            "line": str(self.loc.first_line),
            "col": str(self.loc.col_start),
        }
        if isinstance(self, Token):
            ret["name"] = self.name
            ret["value"] = self.value
        return ret

    def pp(self, depth: Optional[int] = None) -> str:
        """Print ast."""
        return print_ast_tree(self, max_depth=depth)

    def dotgen(self) -> str:
        """Print ast."""
        return dotgen_ast_tree(self)


class AstSymbolNode(AstNode):
    """Nodes that have link to a symbol in symbol table."""

    def __init__(
        self, sym_name: str, sym_name_node: AstNode, sym_type: SymbolType
    ) -> None:
        """Initialize ast."""
        self.sym_link: Optional[Symbol] = None
        self.sym_name: str = sym_name
        self.sym_name_node = sym_name_node
        self.sym_type: SymbolType = sym_type
        self.py_ctx_func: Type[ast3.AST] = ast3.Load


class AstAccessNode(AstNode):
    """Nodes that have access."""

    def __init__(self, access: Optional[SubTag[Token]]) -> None:
        """Initialize ast."""
        self.access: Optional[SubTag[Token]] = access

    @property
    def access_type(self) -> SymbolAccess:
        """Get access spec."""
        return (
            SymbolAccess.PRIVATE
            if self.access and self.access.tag.value == Tok.KW_PRIV
            else SymbolAccess.PROTECTED
            if self.access and self.access.tag.value == Tok.KW_PROT
            else SymbolAccess.PUBLIC
        )


class AstDocNode(AstNode):
    """Nodes that have access."""

    def __init__(self, doc: Optional[String]) -> None:
        """Initialize ast."""
        self.doc: Optional[String] = doc


class AstSemStrNode(AstNode):
    """Nodes that have access."""

    def __init__(self, semstr: Optional[String]) -> None:
        """Initialize ast."""
        self.semstr: Optional[String] = semstr


class AstAsyncNode(AstNode):
    """Nodes that have access."""

    def __init__(self, is_async: bool) -> None:
        """Initialize ast."""
        self.is_async: bool = is_async


class AstElseBodyNode(AstNode):
    """Nodes that have access."""

    def __init__(self, else_body: Optional[ElseStmt | ElseIf]) -> None:
        """Initialize ast."""
        self.else_body: Optional[ElseStmt | ElseIf] = else_body


class AstTypedVarNode(AstNode):
    """Nodes that have access."""

    def __init__(self, type_tag: Optional[SubTag[Expr]]) -> None:
        """Initialize ast."""
        self.type_tag: Optional[SubTag[Expr]] = type_tag


class WalkerStmtOnlyNode(AstNode):
    """WalkerStmtOnlyNode node type for Jac Ast."""

    def __init__(self) -> None:
        """Initialize walker statement only node."""
        self.from_walker: bool = False


class AstImplOnlyNode(AstNode):
    """ImplOnly node type for Jac Ast."""

    def __init__(self, decl_link: Optional[AstNode]) -> None:
        """Initialize impl only node."""
        self.decl_link = decl_link


class Expr(AstNode):
    """Expr node type for Jac Ast."""


class AtomExpr(Expr, AstSymbolNode):
    """AtomExpr node type for Jac Ast."""


class ElementStmt(AstDocNode):
    """ElementStmt node type for Jac Ast."""


class ArchBlockStmt(AstNode):
    """ArchBlockStmt node type for Jac Ast."""


class EnumBlockStmt(AstNode):
    """EnumBlockStmt node type for Jac Ast."""


class CodeBlockStmt(AstNode):
    """CodeBlockStmt node type for Jac Ast."""


class NameSpec(AtomExpr, EnumBlockStmt):
    """NameSpec node type for Jac Ast."""


class ArchSpec(ElementStmt, CodeBlockStmt, AstSymbolNode, AstDocNode, AstSemStrNode):
    """ArchSpec node type for Jac Ast."""

    def __init__(self, decorators: Optional[SubNodeList[Expr]] = None) -> None:
        """Initialize walker statement only node."""
        self.decorators = decorators


class MatchPattern(AstNode):
    """MatchPattern node type for Jac Ast."""


T = TypeVar("T", bound=AstNode)


class SubTag(AstNode, Generic[T]):
    """SubTag node type for Jac Ast."""

    def __init__(
        self,
        tag: T,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize tag node."""
        self.tag = tag
        AstNode.__init__(self, kid=kid)


class SubNodeList(AstNode, Generic[T]):
    """SubNodeList node type for Jac Ast."""

    def __init__(
        self,
        items: list[T],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize sub node list node."""
        self.items = items
        AstNode.__init__(self, kid=kid)


# AST Mid Level Node Types
# --------------------------
class Module(AstDocNode):
    """Whole Program node type for Jac Ast."""

    def __init__(
        self,
        name: str,
        source: JacSource,
        doc: Optional[String],
        body: Sequence[ElementStmt | String | EmptyToken],
        is_imported: bool,
        kid: Sequence[AstNode],
        impl_mod: Optional[Module] = None,
        test_mod: Optional[Module] = None,
    ) -> None:
        """Initialize whole program node."""
        self.name = name
        self.source = source
        self.body = body
        self.is_imported = is_imported
        self.impl_mod = impl_mod
        self.test_mod = test_mod
        self.mod_deps: dict[str, Module] = {}
        AstNode.__init__(self, kid=kid)
        AstDocNode.__init__(self, doc=doc)


class GlobalVars(ElementStmt, AstAccessNode):
    """GlobalVars node type for Jac Ast."""

    def __init__(
        self,
        access: Optional[SubTag[Token]],
        assignments: SubNodeList[Assignment],
        is_frozen: bool,
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
    ) -> None:
        """Initialize global var node."""
        self.assignments = assignments
        self.is_frozen = is_frozen
        AstNode.__init__(self, kid=kid)
        AstAccessNode.__init__(self, access=access)
        AstDocNode.__init__(self, doc=doc)


class Test(AstSymbolNode, ElementStmt):
    """Test node type for Jac Ast."""

    TEST_COUNT = 0

    def __init__(
        self,
        name: Name | Token,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
    ) -> None:
        """Initialize test node."""
        Test.TEST_COUNT += 1 if isinstance(name, Token) else 0
        self.name: Name = (  # for auto generated test names
            name
            if isinstance(name, Name)
            else Name(
                file_path=name.file_path,
                name="NAME",
                value=f"test_t{Test.TEST_COUNT}",
                col_start=name.loc.col_start,
                col_end=name.loc.col_end,
                line=name.loc.first_line,
                pos_start=name.pos_start,
                pos_end=name.pos_end,
                kid=name.kid,
            )
        )
        self.name.parent = self
        # kid[0] = self.name  # Index is 0 since Doc string is inserted after init
        self.body = body
        AstNode.__init__(self, kid=kid)
        if self.name not in self.kid:
            self.add_kids_left([self.name], pos_update=False)
        AstSymbolNode.__init__(
            self,
            sym_name=self.name.sym_name,
            sym_name_node=self.name,
            sym_type=SymbolType.TEST,
        )
        AstDocNode.__init__(self, doc=doc)


class ModuleCode(ElementStmt):
    """Free mod code for Jac Ast."""

    def __init__(
        self,
        name: Optional[SubTag[Name]],
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
    ) -> None:
        """Initialize test node."""
        self.name = name
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstDocNode.__init__(self, doc=doc)


class PyInlineCode(ElementStmt, ArchBlockStmt, EnumBlockStmt, CodeBlockStmt):
    """Inline Python code node type for Jac Ast."""

    def __init__(
        self,
        code: Token,
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
    ) -> None:
        """Initialize inline python code node."""
        self.code = code
        AstNode.__init__(self, kid=kid)
        AstDocNode.__init__(self, doc=doc)


class Import(ElementStmt, CodeBlockStmt):
    """Import node type for Jac Ast."""

    def __init__(
        self,
        lang: SubTag[Name],
        path: ModulePath,
        items: Optional[SubNodeList[ModuleItem]],
        is_absorb: bool,  # For includes
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        sub_module: Optional[Module] = None,
    ) -> None:
        """Initialize import node."""
        self.lang = lang
        self.path = path
        self.items = items
        self.is_absorb = is_absorb
        self.sub_module = sub_module
        AstNode.__init__(self, kid=kid)
        AstDocNode.__init__(self, doc=doc)


class ModulePath(AstSymbolNode):
    """ModulePath node type for Jac Ast."""

    def __init__(
        self,
        path: Sequence[Token],
        alias: Optional[Name],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize module path node."""
        self.path = path
        self.alias = alias
        self.path_str: str = "".join([p.value for p in path])
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=alias.sym_name if alias else self.path_str,
            sym_name_node=alias if alias else self,
            sym_type=SymbolType.MODULE,
        )


class ModuleItem(AstSymbolNode):
    """ModuleItem node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        alias: Optional[Name],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize module item node."""
        self.name = name
        self.alias = alias
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=alias.sym_name if alias else name.sym_name,
            sym_name_node=alias if alias else name,
            sym_type=SymbolType.MOD_VAR,
        )


class Architype(ArchSpec, AstAccessNode, ArchBlockStmt):
    """ObjectArch node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        arch_type: Token,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[Expr]],
        body: Optional[SubNodeList[ArchBlockStmt] | ArchDef],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        semstr: Optional[String] = None,
        decorators: Optional[SubNodeList[Expr]] = None,
    ) -> None:
        """Initialize object arch node."""
        self.name = name
        self.arch_type = arch_type
        self.base_classes = base_classes
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=name.value,
            sym_name_node=name,
            sym_type=SymbolType.OBJECT_ARCH
            if arch_type.name == Tok.KW_OBJECT
            else SymbolType.NODE_ARCH
            if arch_type.name == Tok.KW_NODE
            else SymbolType.EDGE_ARCH
            if arch_type.name == Tok.KW_EDGE
            else SymbolType.WALKER_ARCH
            if arch_type.name == Tok.KW_WALKER
            else SymbolType.TYPE,
        )
        AstAccessNode.__init__(self, access=access)
        AstDocNode.__init__(self, doc=doc)
        AstSemStrNode.__init__(self, semstr=semstr)
        ArchSpec.__init__(self, decorators=decorators)


class ArchDef(ArchSpec, AstImplOnlyNode):
    """ArchDef node type for Jac Ast."""

    def __init__(
        self,
        target: ArchRefChain,
        body: SubNodeList[ArchBlockStmt],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[Expr]] = None,
        decl_link: Optional[Architype] = None,
    ) -> None:
        """Initialize arch def node."""
        self.target = target
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=target.py_resolve_name(),
            sym_name_node=target,
            sym_type=SymbolType.IMPL,
        )
        AstDocNode.__init__(self, doc=doc)
        ArchSpec.__init__(self, decorators=decorators)
        AstImplOnlyNode.__init__(self, decl_link=decl_link)


class Enum(ArchSpec, AstAccessNode):
    """Enum node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[Expr]],
        body: Optional[SubNodeList[EnumBlockStmt] | EnumDef],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        semstr: Optional[String] = None,
        decorators: Optional[SubNodeList[Expr]] = None,
    ) -> None:
        """Initialize object arch node."""
        self.name = name
        self.base_classes = base_classes
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=name.value,
            sym_name_node=name,
            sym_type=SymbolType.ENUM_ARCH,
        )
        AstAccessNode.__init__(self, access=access)
        AstDocNode.__init__(self, doc=doc)
        AstSemStrNode.__init__(self, semstr=semstr)
        ArchSpec.__init__(self, decorators=decorators)


class EnumDef(ArchSpec, AstImplOnlyNode):
    """EnumDef node type for Jac Ast."""

    def __init__(
        self,
        target: ArchRefChain,
        body: SubNodeList[EnumBlockStmt],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[Expr]] = None,
        decl_link: Optional[Enum] = None,
    ) -> None:
        """Initialize arch def node."""
        self.target = target
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=target.py_resolve_name(),
            sym_name_node=target,
            sym_type=SymbolType.IMPL,
        )
        AstDocNode.__init__(self, doc=doc)
        ArchSpec.__init__(self, decorators=decorators)
        AstImplOnlyNode.__init__(self, decl_link=decl_link)


class Ability(
    AstSymbolNode,
    AstAccessNode,
    ElementStmt,
    AstAsyncNode,
    ArchBlockStmt,
    CodeBlockStmt,
    AstSemStrNode,
):
    """Ability node type for Jac Ast."""

    def __init__(
        self,
        name_ref: NameSpec,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        is_abstract: bool,
        access: Optional[SubTag[Token]],
        signature: Optional[FuncSignature | EventSignature],
        body: Optional[SubNodeList[CodeBlockStmt] | AbilityDef],
        kid: Sequence[AstNode],
        semstr: Optional[String] = None,
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[Expr]] = None,
    ) -> None:
        """Initialize func arch node."""
        self.name_ref = name_ref
        self.is_func = is_func
        self.is_static = is_static
        self.is_abstract = is_abstract
        self.decorators = decorators
        self.signature = signature
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstSemStrNode.__init__(self, semstr=semstr)
        AstSymbolNode.__init__(
            self,
            sym_name=self.py_resolve_name(),
            sym_name_node=name_ref,
            sym_type=SymbolType.ABILITY,
        )
        AstAccessNode.__init__(self, access=access)
        AstDocNode.__init__(self, doc=doc)
        AstAsyncNode.__init__(self, is_async=is_async)

    @property
    def is_method(self) -> bool:
        """Check if is method."""
        check = isinstance(self.parent, SubNodeList) and isinstance(
            self.parent.parent, Architype
        )
        if check:
            self.sym_type = SymbolType.METHOD
        return check

    def py_resolve_name(self) -> str:
        """Resolve name."""
        if isinstance(self.name_ref, Name):
            return self.name_ref.value
        elif isinstance(self.name_ref, (SpecialVarRef, ArchRef)):
            return self.name_ref.py_resolve_name()
        else:
            raise NotImplementedError


class AbilityDef(AstSymbolNode, ElementStmt, AstImplOnlyNode, CodeBlockStmt):
    """AbilityDef node type for Jac Ast."""

    def __init__(
        self,
        target: ArchRefChain,
        signature: FuncSignature | EventSignature,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[Expr]] = None,
        decl_link: Optional[Ability] = None,
    ) -> None:
        """Initialize ability def node."""
        self.target = target
        self.signature = signature
        self.body = body
        self.decorators = decorators
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=target.py_resolve_name(),
            sym_name_node=target,
            sym_type=SymbolType.IMPL,
        )
        AstDocNode.__init__(self, doc=doc)
        AstImplOnlyNode.__init__(self, decl_link=decl_link)

    @property
    def is_method(self) -> bool:
        """Check if is method."""
        return (
            len(self.target.archs) > 1
            and self.target.archs[-2].arch.name != Tok.ABILITY_OP
        )


class FuncSignature(AstSemStrNode):
    """FuncSignature node type for Jac Ast."""

    def __init__(
        self,
        params: Optional[SubNodeList[ParamVar]],
        return_type: Optional[Expr],
        kid: Sequence[AstNode],
        semstr: Optional[String] = None,
    ) -> None:
        """Initialize method signature node."""
        self.params = params
        self.return_type = return_type
        AstNode.__init__(self, kid=kid)
        AstSemStrNode.__init__(self, semstr=semstr)

    @property
    def is_method(self) -> bool:
        """Check if is method."""
        return (isinstance(self.parent, Ability) and self.parent.is_method) or (
            isinstance(self.parent, AbilityDef) and self.parent.is_method
        )

    @property
    def is_static(self) -> bool:
        """Check if is static."""
        return (isinstance(self.parent, Ability) and self.parent.is_static) or (
            isinstance(self.parent, AbilityDef)
            and isinstance(self.parent.decl_link, Ability)
            and self.parent.decl_link.is_static
        )


class EventSignature(AstSemStrNode):
    """EventSignature node type for Jac Ast."""

    def __init__(
        self,
        event: Token,
        arch_tag_info: Optional[Expr],
        return_type: Optional[Expr],
        kid: Sequence[AstNode],
        semstr: Optional[String] = None,
    ) -> None:
        """Initialize event signature node."""
        self.event = event
        self.arch_tag_info = arch_tag_info
        self.return_type = return_type
        AstNode.__init__(self, kid=kid)
        AstSemStrNode.__init__(self, semstr=semstr)

    @property
    def is_method(self) -> bool:
        """Check if is method."""
        if (isinstance(self.parent, Ability) and self.parent.is_method) or (
            isinstance(self.parent, AbilityDef)
            and isinstance(self.parent.decl_link, Ability)
            and self.parent.decl_link.is_method
        ):
            return True
        return False


class ArchRefChain(AstNode):
    """Arch ref list node type for Jac Ast."""

    def __init__(
        self,
        archs: list[ArchRef],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize name list ."""
        self.archs = archs
        AstNode.__init__(self, kid=kid)

    def py_resolve_name(self) -> str:
        """Resolve name."""

        def get_tag(x: ArchRef) -> str:
            return x.arch.value[1] if x.arch.value != "enum" else "en"

        return ".".join([f"({get_tag(x)}){x.py_resolve_name()}" for x in self.archs])

    def flat_name(self) -> str:
        """Resolve name for python gen."""
        return (
            self.py_resolve_name().replace(".", "_").replace("(", "").replace(")", "_")
        )


class ParamVar(AstSymbolNode, AstTypedVarNode, AstSemStrNode):
    """ParamVar node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[Expr],
        value: Optional[Expr],
        kid: Sequence[AstNode],
        semstr: Optional[String] = None,
    ) -> None:
        """Initialize param var node."""
        self.name = name
        self.unpack = unpack
        self.value = value
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=name.value,
            sym_name_node=name,
            sym_type=SymbolType.VAR,
        )
        AstTypedVarNode.__init__(self, type_tag=type_tag)
        AstSemStrNode.__init__(self, semstr=semstr)


class ArchHas(AstAccessNode, AstDocNode, ArchBlockStmt):
    """HasStmt node type for Jac Ast."""

    def __init__(
        self,
        is_static: bool,
        access: Optional[SubTag[Token]],
        vars: SubNodeList[HasVar],
        is_frozen: bool,
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
    ) -> None:
        """Initialize has statement node."""
        self.is_static = is_static
        self.vars = vars
        self.is_frozen = is_frozen
        AstNode.__init__(self, kid=kid)
        AstAccessNode.__init__(self, access=access)
        AstDocNode.__init__(self, doc=doc)


class HasVar(AstSymbolNode, AstTypedVarNode, AstSemStrNode):
    """HasVar node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        type_tag: SubTag[Expr],
        value: Optional[Expr],
        kid: Sequence[AstNode],
        semstr: Optional[String] = None,
    ) -> None:
        """Initialize has var node."""
        self.name = name
        self.value = value
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=name.value,
            sym_name_node=name,
            sym_type=SymbolType.VAR,
        )
        AstTypedVarNode.__init__(self, type_tag=type_tag)
        AstSemStrNode.__init__(self, semstr=semstr)


class TypedCtxBlock(CodeBlockStmt):
    """TypedCtxBlock node type for Jac Ast."""

    def __init__(
        self,
        type_ctx: Expr,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize typed context block node."""
        self.type_ctx = type_ctx
        self.body = body
        AstNode.__init__(self, kid=kid)


class IfStmt(CodeBlockStmt, AstElseBodyNode):
    """IfStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: Expr,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt | ElseIf],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize if statement node."""
        self.condition = condition
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstElseBodyNode.__init__(self, else_body=else_body)


class ElseIf(IfStmt):
    """ElseIfs node type for Jac Ast."""


class ElseStmt(AstNode):
    """Else node type for Jac Ast."""

    def __init__(
        self,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize else node."""
        self.body = body
        AstNode.__init__(self, kid=kid)


class ExprStmt(CodeBlockStmt):
    """ExprStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: Expr,
        in_fstring: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize expr statement node."""
        self.expr = expr
        self.in_fstring = in_fstring
        AstNode.__init__(self, kid=kid)


class TryStmt(AstElseBodyNode, CodeBlockStmt):
    """TryStmt node type for Jac Ast."""

    def __init__(
        self,
        body: SubNodeList[CodeBlockStmt],
        excepts: Optional[SubNodeList[Except]],
        else_body: Optional[ElseStmt],
        finally_body: Optional[FinallyStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize try statement node."""
        self.body = body
        self.excepts = excepts
        self.finally_body = finally_body
        AstNode.__init__(self, kid=kid)
        AstElseBodyNode.__init__(self, else_body=else_body)


class Except(CodeBlockStmt):
    """Except node type for Jac Ast."""

    def __init__(
        self,
        ex_type: Expr,
        name: Optional[Name],
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize except node."""
        self.ex_type = ex_type
        self.name = name
        self.body = body
        AstNode.__init__(self, kid=kid)


class FinallyStmt(CodeBlockStmt):
    """FinallyStmt node type for Jac Ast."""

    def __init__(
        self,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize finally statement node."""
        self.body = body
        AstNode.__init__(self, kid=kid)


class IterForStmt(AstAsyncNode, AstElseBodyNode, CodeBlockStmt):
    """IterFor node type for Jac Ast."""

    def __init__(
        self,
        iter: Assignment,
        is_async: bool,
        condition: Expr,
        count_by: Assignment,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize iter for node."""
        self.iter = iter
        self.condition = condition
        self.count_by = count_by
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstAsyncNode.__init__(self, is_async=is_async)
        AstElseBodyNode.__init__(self, else_body=else_body)


class InForStmt(AstAsyncNode, AstElseBodyNode, CodeBlockStmt):
    """InFor node type for Jac Ast."""

    def __init__(
        self,
        target: Expr,
        is_async: bool,
        collection: Expr,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize in for node."""
        self.target = target
        self.collection = collection
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstAsyncNode.__init__(self, is_async=is_async)
        AstElseBodyNode.__init__(self, else_body=else_body)


class WhileStmt(CodeBlockStmt):
    """WhileStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: Expr,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize while statement node."""
        self.condition = condition
        self.body = body
        AstNode.__init__(self, kid=kid)


class WithStmt(AstAsyncNode, CodeBlockStmt):
    """WithStmt node type for Jac Ast."""

    def __init__(
        self,
        is_async: bool,
        exprs: SubNodeList[ExprAsItem],
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize with statement node."""
        self.exprs = exprs
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstAsyncNode.__init__(self, is_async=is_async)


class ExprAsItem(AstNode):
    """ExprAsItem node type for Jac Ast."""

    def __init__(
        self,
        expr: Expr,
        alias: Optional[Expr],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize module item node."""
        self.expr = expr
        self.alias = alias
        AstNode.__init__(self, kid=kid)


class RaiseStmt(CodeBlockStmt):
    """RaiseStmt node type for Jac Ast."""

    def __init__(
        self,
        cause: Optional[Expr],
        from_target: Optional[Expr],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize raise statement node."""
        self.cause = cause
        self.from_target = from_target
        AstNode.__init__(self, kid=kid)


class AssertStmt(CodeBlockStmt):
    """AssertStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: Expr,
        error_msg: Optional[Expr],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize assert statement node."""
        self.condition = condition
        self.error_msg = error_msg
        AstNode.__init__(self, kid=kid)


class CtrlStmt(CodeBlockStmt):
    """CtrlStmt node type for Jac Ast."""

    def __init__(
        self,
        ctrl: Token,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize control statement node."""
        self.ctrl = ctrl
        AstNode.__init__(self, kid=kid)


class DeleteStmt(CodeBlockStmt):
    """DeleteStmt node type for Jac Ast."""

    def __init__(
        self,
        target: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize delete statement node."""
        self.target = target
        AstNode.__init__(self, kid=kid)


class ReportStmt(CodeBlockStmt):
    """ReportStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize report statement node."""
        self.expr = expr
        AstNode.__init__(self, kid=kid)


class ReturnStmt(CodeBlockStmt):
    """ReturnStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: Optional[Expr],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize return statement node."""
        self.expr = expr
        AstNode.__init__(self, kid=kid)


class IgnoreStmt(WalkerStmtOnlyNode, CodeBlockStmt):
    """IgnoreStmt node type for Jac Ast."""

    def __init__(
        self,
        target: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize ignore statement node."""
        self.target = target
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)


class VisitStmt(WalkerStmtOnlyNode, AstElseBodyNode, CodeBlockStmt):
    """VisitStmt node type for Jac Ast."""

    def __init__(
        self,
        vis_type: Optional[SubNodeList[Expr]],
        target: Expr,
        else_body: Optional[ElseStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize visit statement node."""
        self.vis_type = vis_type
        self.target = target
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)
        AstElseBodyNode.__init__(self, else_body=else_body)


class RevisitStmt(WalkerStmtOnlyNode, AstElseBodyNode, CodeBlockStmt):
    """ReVisitStmt node type for Jac Ast."""

    def __init__(
        self,
        hops: Optional[Expr],
        else_body: Optional[ElseStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize revisit statement node."""
        self.hops = hops
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)
        AstElseBodyNode.__init__(self, else_body=else_body)


class DisengageStmt(WalkerStmtOnlyNode, CodeBlockStmt):
    """DisengageStmt node type for Jac Ast."""

    def __init__(
        self,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize disengage statement node."""
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)


class AwaitExpr(Expr):
    """AwaitStmt node type for Jac Ast."""

    def __init__(
        self,
        target: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize sync statement node."""
        self.target = target
        AstNode.__init__(self, kid=kid)


class GlobalStmt(CodeBlockStmt):
    """GlobalStmt node type for Jac Ast."""

    def __init__(
        self,
        target: SubNodeList[NameSpec],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize global statement node."""
        self.target = target
        AstNode.__init__(self, kid=kid)


class NonLocalStmt(GlobalStmt):
    """NonlocalStmt node type for Jac Ast."""


class Assignment(AstTypedVarNode, EnumBlockStmt, CodeBlockStmt):
    """Assignment node type for Jac Ast."""

    def __init__(
        self,
        target: SubNodeList[Expr],
        value: Optional[Expr | YieldExpr],
        type_tag: Optional[SubTag[Expr]],
        kid: Sequence[AstNode],
        mutable: bool = True,
        aug_op: Optional[Token] = None,
    ) -> None:
        """Initialize assignment node."""
        self.target = target
        self.value = value
        self.mutable = mutable
        self.aug_op = aug_op
        AstNode.__init__(self, kid=kid)
        AstTypedVarNode.__init__(self, type_tag=type_tag)


class BinaryExpr(Expr):
    """ExprBinary node type for Jac Ast."""

    def __init__(
        self,
        left: Expr,
        right: Expr,
        op: Token | DisconnectOp | ConnectOp,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize binary expression node."""
        self.left = left
        self.right = right
        self.op = op
        AstNode.__init__(self, kid=kid)


class CompareExpr(Expr):
    """ExprBinary node type for Jac Ast."""

    def __init__(
        self,
        left: Expr,
        rights: list[Expr],
        ops: list[Token],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize binary expression node."""
        self.left = left
        self.rights = rights
        self.ops = ops
        AstNode.__init__(self, kid=kid)


class LambdaExpr(Expr):
    """ExprLambda node type for Jac Ast."""

    def __init__(
        self,
        signature: FuncSignature,
        body: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize lambda expression node."""
        self.signature = signature
        self.body = body
        AstNode.__init__(self, kid=kid)


class UnaryExpr(Expr):
    """ExprUnary node type for Jac Ast."""

    def __init__(
        self,
        operand: Expr,
        op: Token,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize unary expression node."""
        self.operand = operand
        self.op = op
        AstNode.__init__(self, kid=kid)


class IfElseExpr(Expr):
    """ExprIfElse node type for Jac Ast."""

    def __init__(
        self,
        condition: Expr,
        value: Expr,
        else_value: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize if else expression node."""
        self.condition = condition
        self.value = value
        self.else_value = else_value
        AstNode.__init__(self, kid=kid)


class MultiString(AtomExpr):
    """ExprMultiString node type for Jac Ast."""

    def __init__(
        self,
        strings: Sequence[String | FString],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize multi string expression node."""
        self.strings = strings
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.STRING,
        )


class FString(AstSymbolNode):
    """FString node type for Jac Ast."""

    def __init__(
        self,
        parts: Optional[SubNodeList[String | ExprStmt]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize fstring expression node."""
        self.parts = parts
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.STRING,
        )


class ExprList(AstNode):
    """ExprList node type for Jac Ast."""

    def __init__(
        self,
        values: Optional[SubNodeList[Expr]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize expr value node."""
        self.values = values
        AstNode.__init__(self, kid=kid)


class ListVal(AtomExpr):
    """ListVal node type for Jac Ast."""

    def __init__(
        self,
        values: Optional[SubNodeList[Expr]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize value node."""
        self.values = values
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.SEQUENCE,
        )


class SetVal(AtomExpr):
    """SetVal node type for Jac Ast."""

    def __init__(
        self,
        values: Optional[SubNodeList[Expr]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize value node."""
        self.values = values
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.SEQUENCE,
        )


class TupleVal(AtomExpr):
    """TupleVal node type for Jac Ast."""

    def __init__(
        self,
        values: Optional[SubNodeList[Expr | KWPair]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize tuple value node."""
        self.values = values
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.SEQUENCE,
        )


class DictVal(AtomExpr):
    """ExprDict node type for Jac Ast."""

    def __init__(
        self,
        kv_pairs: Sequence[KVPair],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize dict expression node."""
        self.kv_pairs = kv_pairs
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.SEQUENCE,
        )


class KVPair(AstNode):
    """ExprKVPair node type for Jac Ast."""

    def __init__(
        self,
        key: Expr,
        value: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize key value pair expression node."""
        self.key = key
        self.value = value
        AstNode.__init__(self, kid=kid)


class KWPair(AstNode):
    """ExprKWPair node type for Jac Ast."""

    def __init__(
        self,
        key: NameSpec,
        value: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize keyword pair expression node."""
        self.key = key
        self.value = value
        AstNode.__init__(self, kid=kid)


class InnerCompr(AstAsyncNode):
    """ListCompr node type for Jac Ast."""

    def __init__(
        self,
        is_async: bool,
        target: Expr,
        collection: Expr,
        conditional: Optional[Expr],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize comprehension expression node."""
        self.target = target
        self.collection = collection
        self.conditional = conditional
        AstNode.__init__(self, kid=kid)
        AstAsyncNode.__init__(self, is_async=is_async)


class ListCompr(AtomExpr):
    """ListCompr node type for Jac Ast."""

    def __init__(
        self,
        out_expr: Expr,
        compr: list[InnerCompr],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize comprehension expression node."""
        self.out_expr = out_expr
        self.compr = compr
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.SEQUENCE,
        )


class GenCompr(ListCompr):
    """GenCompr node type for Jac Ast."""


class SetCompr(ListCompr):
    """SetCompr node type for Jac Ast."""


class DictCompr(AtomExpr):
    """DictCompr node type for Jac Ast."""

    def __init__(
        self,
        kv_pair: KVPair,
        compr: list[InnerCompr],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize comprehension expression node."""
        self.kv_pair = kv_pair
        self.compr = compr
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.SEQUENCE,
        )


class AtomTrailer(Expr):
    """AtomTrailer node type for Jac Ast."""

    def __init__(
        self,
        target: Expr,
        right: AtomExpr | Expr,
        is_attr: bool,
        is_null_ok: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize atom trailer expression node."""
        self.target = target
        self.right = right
        self.is_attr = is_attr
        self.is_null_ok = is_null_ok
        AstNode.__init__(self, kid=kid)


class AtomUnit(Expr):
    """AtomUnit node type for Jac Ast."""

    def __init__(
        self,
        value: Expr | YieldExpr,
        is_paren: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize atom unit expression node."""
        self.value = value
        self.is_paren = is_paren
        AstNode.__init__(self, kid=kid)


class YieldExpr(Expr):
    """YieldStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: Optional[Expr],
        with_from: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize yeild statement node."""
        self.expr = expr
        self.with_from = with_from
        AstNode.__init__(self, kid=kid)


class FuncCall(Expr):
    """FuncCall node type for Jac Ast."""

    def __init__(
        self,
        target: Expr,
        params: Optional[SubNodeList[Expr | KWPair]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize function call expression node."""
        self.target = target
        self.params = params
        AstNode.__init__(self, kid=kid)


class IndexSlice(AtomExpr):
    """IndexSlice node type for Jac Ast."""

    def __init__(
        self,
        start: Optional[Expr],
        stop: Optional[Expr],
        step: Optional[Expr],
        is_range: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize index slice expression node."""
        self.start = start
        self.stop = stop
        self.step = step
        self.is_range = is_range
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_type=SymbolType.SEQUENCE,
            sym_name_node=self,
        )


class ArchRef(NameSpec):
    """ArchRef node type for Jac Ast."""

    def __init__(
        self,
        name_ref: NameSpec,
        arch: Token,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize architype reference expression node."""
        self.name_ref = name_ref
        self.arch = arch
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=self.py_resolve_name(),
            sym_name_node=name_ref,
            sym_type=SymbolType.TYPE,
        )

    def py_resolve_name(self) -> str:
        """Resolve name."""
        if isinstance(self.name_ref, Name):
            return self.name_ref.value
        elif isinstance(self.name_ref, SpecialVarRef):
            return self.name_ref.py_resolve_name()
        else:
            raise NotImplementedError


class SpecialVarRef(NameSpec):
    """HereRef node type for Jac Ast."""

    def __init__(
        self,
        var: Token,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize special var reference expression node."""
        self.var = var
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=self.py_resolve_name(),
            sym_name_node=var,
            sym_type=SymbolType.VAR,
        )

    def py_resolve_name(self) -> str:
        """Resolve name."""
        if self.var.name == Tok.SELF_OP:
            return "self"
        elif self.var.name == Tok.SUPER_OP:
            return "super()"
        elif self.var.name == Tok.ROOT_OP:
            return Con.ROOT.value
        elif self.var.name == Tok.HERE_OP:
            return Con.HERE.value
        elif self.var.name == Tok.INIT_OP:
            return "__init__"
        elif self.var.name == Tok.POST_INIT_OP:
            return "__post_init__"
        else:
            raise NotImplementedError("ICE: Special var reference not implemented")


class EdgeOpRef(WalkerStmtOnlyNode, AtomExpr):
    """EdgeOpRef node type for Jac Ast."""

    def __init__(
        self,
        filter_type: Optional[Expr],
        filter_cond: Optional[FilterCompr],
        edge_dir: EdgeDir,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize edge op reference expression node."""
        self.filter_type = filter_type
        self.filter_cond = filter_cond
        self.edge_dir = edge_dir
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.SEQUENCE,
        )


class DisconnectOp(WalkerStmtOnlyNode):
    """DisconnectOpRef node type for Jac Ast."""

    def __init__(
        self,
        edge_spec: EdgeOpRef,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize disconnect op reference expression node."""
        self.edge_spec = edge_spec
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)


class ConnectOp(AstNode):
    """ConnectOpRef node type for Jac Ast."""

    def __init__(
        self,
        conn_type: Optional[Expr],
        conn_assign: Optional[AssignCompr],
        edge_dir: EdgeDir,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize connect op reference expression node."""
        self.conn_type = conn_type
        self.conn_assign = conn_assign
        self.edge_dir = edge_dir
        AstNode.__init__(self, kid=kid)


class FilterCompr(AtomExpr):
    """FilterCtx node type for Jac Ast."""

    def __init__(
        self,
        compares: SubNodeList[CompareExpr],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize filter_cond context expression node."""
        self.compares = compares
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.SEQUENCE,
        )


class AssignCompr(AtomExpr):
    """AssignCtx node type for Jac Ast."""

    def __init__(
        self,
        assigns: SubNodeList[KWPair],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize assign compr expression node."""
        self.assigns = assigns
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=SymbolType.SEQUENCE,
        )


# Match Nodes
# ------------


class MatchStmt(CodeBlockStmt):
    """MatchStmt node type for Jac Ast."""

    def __init__(
        self,
        target: Expr,
        cases: list[MatchCase],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match statement node."""
        self.target = target
        self.cases = cases
        AstNode.__init__(self, kid=kid)


class MatchCase(AstNode):
    """MatchCase node type for Jac Ast."""

    def __init__(
        self,
        pattern: MatchPattern,
        guard: Optional[Expr],
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match case node."""
        self.pattern = pattern
        self.guard = guard
        self.body = body
        AstNode.__init__(self, kid=kid)


class MatchOr(MatchPattern):
    """MatchOr node type for Jac Ast."""

    def __init__(
        self,
        patterns: list[MatchPattern],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match or node."""
        self.patterns = patterns
        AstNode.__init__(self, kid=kid)


class MatchAs(MatchPattern):
    """MatchAs node type for Jac Ast."""

    def __init__(
        self,
        name: NameSpec,
        pattern: Optional[MatchPattern],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match as node."""
        self.name = name
        self.pattern = pattern
        AstNode.__init__(self, kid=kid)


class MatchWild(MatchPattern):
    """Match wild card node type for Jac Ast."""


class MatchValue(MatchPattern):
    """MatchValue node type for Jac Ast."""

    def __init__(
        self,
        value: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match value node."""
        self.value = value
        AstNode.__init__(self, kid=kid)


class MatchSingleton(MatchPattern):
    """MatchSingleton node type for Jac Ast."""

    def __init__(
        self,
        value: Bool | Null,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match singleton node."""
        self.value = value
        AstNode.__init__(self, kid=kid)


class MatchSequence(MatchPattern):
    """MatchSequence node type for Jac Ast."""

    def __init__(
        self,
        values: list[MatchPattern],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match sequence node."""
        self.values = values
        AstNode.__init__(self, kid=kid)


class MatchMapping(MatchPattern):
    """MatchMapping node type for Jac Ast."""

    def __init__(
        self,
        values: list[MatchKVPair | MatchStar],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match mapping node."""
        self.values = values
        AstNode.__init__(self, kid=kid)


class MatchKVPair(MatchPattern):
    """MatchKVPair node type for Jac Ast."""

    def __init__(
        self,
        key: MatchPattern | NameSpec,
        value: MatchPattern,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match key value pair node."""
        self.key = key
        self.value = value
        AstNode.__init__(self, kid=kid)


class MatchStar(MatchPattern):
    """MatchStar node type for Jac Ast."""

    def __init__(
        self,
        name: NameSpec,
        is_list: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match star node."""
        self.name = name
        self.is_list = is_list
        AstNode.__init__(self, kid=kid)


class MatchArch(MatchPattern):
    """MatchClass node type for Jac Ast."""

    def __init__(
        self,
        name: NameSpec,
        arg_patterns: Optional[SubNodeList[MatchPattern]],
        kw_patterns: Optional[SubNodeList[MatchKVPair]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match class node."""
        self.name = name
        self.arg_patterns = arg_patterns
        self.kw_patterns = kw_patterns
        AstNode.__init__(self, kid=kid)


# AST Terminal Node Types
# --------------------------
class Token(AstNode):
    """Token node type for Jac Ast."""

    def __init__(
        self,
        file_path: str,
        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize token."""
        self.file_path = file_path
        self.name = name
        self.value = value
        self.line_no = line
        self.c_start = col_start
        self.c_end = col_end
        self.pos_start = pos_start
        self.pos_end = pos_end
        AstNode.__init__(self, kid=kid)


class Name(Token, NameSpec):
    """Name node type for Jac Ast."""

    def __init__(
        self,
        file_path: str,
        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        kid: Sequence[AstNode],
        is_enum_singleton: bool = False,
        is_kwesc: bool = False,
    ) -> None:
        """Initialize token."""
        self.is_enum_singleton = is_enum_singleton
        self.is_kwesc = is_kwesc
        Token.__init__(
            self,
            file_path=file_path,
            name=name,
            value=value,
            line=line,
            col_start=col_start,
            col_end=col_end,
            pos_start=pos_start,
            pos_end=pos_end,
            kid=kid,
        )
        AstSymbolNode.__init__(
            self,
            sym_name=value,
            sym_name_node=self,
            sym_type=SymbolType.VAR,
        )


class Literal(Token, AtomExpr):
    """Literal node type for Jac Ast."""

    SYMBOL_TYPE = SymbolType.VAR

    type_map = {
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        "bytes": bytes,
        "list": list,
        "tuple": tuple,
        "set": set,
        "dict": dict,
        "type": type,
    }

    def __init__(
        self,
        file_path: str,
        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize token."""
        Token.__init__(
            self,
            file_path=file_path,
            name=name,
            value=value,
            line=line,
            col_start=col_start,
            col_end=col_end,
            pos_start=pos_start,
            pos_end=pos_end,
            kid=kid,
        )
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=self.SYMBOL_TYPE,
        )

    @property
    def lit_value(self) -> int | str | float | bool | None | Callable[[], Any]:
        """Return literal value in its python type."""
        raise NotImplementedError


class TokenSymbol(Token, AstSymbolNode):
    """TokenSymbol node type for Jac Ast."""

    SYMBOL_TYPE = SymbolType.VAR

    def __init__(
        self,
        file_path: str,
        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize token."""
        Token.__init__(
            self,
            file_path=file_path,
            name=name,
            value=value,
            line=line,
            col_start=col_start,
            col_end=col_end,
            pos_start=pos_start,
            pos_end=pos_end,
            kid=kid,
        )
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            sym_name_node=self,
            sym_type=self.SYMBOL_TYPE,
        )


class BuiltinType(Name, Literal, NameSpec):
    """Type node type for Jac Ast."""

    SYMBOL_TYPE = SymbolType.VAR

    @property
    def lit_value(self) -> Callable[[], Any]:
        """Return literal value in its python type."""
        if self.value not in Literal.type_map:
            raise TypeError(f"ICE: {self.value} is not a callable builtin")
        return Literal.type_map[self.value]


class Float(Literal):
    """Float node type for Jac Ast."""

    SYMBOL_TYPE = SymbolType.NUMBER

    @property
    def lit_value(self) -> float:
        """Return literal value in its python type."""
        return float(self.value)


class Int(Literal):
    """Int node type for Jac Ast."""

    SYMBOL_TYPE = SymbolType.NUMBER

    @property
    def lit_value(self) -> int:
        """Return literal value in its python type."""
        return int(self.value)


class String(Literal):
    """String node type for Jac Ast."""

    SYMBOL_TYPE = SymbolType.STRING

    @property
    def lit_value(self) -> str:
        """Return literal value in its python type."""
        prefix_len = 3 if self.value.startswith(("'''", '"""')) else 1
        if any(
            self.value.startswith(prefix)
            and self.value[len(prefix) :].startswith(("'", '"'))
            for prefix in ["r", "b", "br", "rb"]
        ):
            return eval(self.value)

        elif self.value.startswith(("'", '"')):
            ret_str = self.value[prefix_len:-prefix_len]
        else:
            ret_str = self.value
        ret_str = ret_str.encode().decode("unicode_escape")
        return ret_str


class Bool(Literal):
    """Bool node type for Jac Ast."""

    SYMBOL_TYPE = SymbolType.BOOL

    @property
    def lit_value(self) -> bool:
        """Return literal value in its python type."""
        return self.value == "True"


class Null(Literal):
    """Semicolon node type for Jac Ast."""

    SYMBOL_TYPE = SymbolType.NULL

    @property
    def lit_value(self) -> None:
        """Return literal value in its python type."""
        return None


class EmptyToken(Token):
    """EmptyToken node type for Jac Ast."""

    def __init__(self) -> None:
        """Initialize empty token."""
        super().__init__(
            name="EmptyToken",
            file_path="",
            value="",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )


class Semi(Token, CodeBlockStmt):
    """Semicolon node type for Jac Ast."""


class CommentToken(Token):
    """CommentToken node type for Jac Ast."""

    def __init__(
        self,
        file_path: str,
        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        kid: Sequence[AstNode],
        is_inline: bool = False,
    ) -> None:
        """Initialize token."""
        self.file_path = file_path
        self.name = name
        self.value = value
        self.line_no = line
        self.c_start = col_start
        self.c_end = col_end
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.is_inline = is_inline
        AstNode.__init__(self, kid=kid)


# ----------------
class JacSource(EmptyToken):
    """SourceString node type for Jac Ast."""

    def __init__(self, source: str, mod_path: str) -> None:
        """Initialize source string."""
        super().__init__()
        self.value = source
        self.file_path = mod_path
        self.comments: list[CommentToken] = []

    @property
    def code(self) -> str:
        """Return code."""
        return self.value


class PythonModuleAst(EmptyToken):
    """SourceString node type for Jac Ast."""

    def __init__(self, ast: ast3.Module, mod_path: str) -> None:
        """Initialize source string."""
        super().__init__()
        self.ast = ast
        self.file_path = mod_path

"""Abstract class for IR Passes for Jac."""
from __future__ import annotations

import ast as ast3
import pprint
from abc import ABC
from typing import Any, Callable, Generic, Optional, Sequence, Type, TypeVar, Union

from jaclang.jac import jac_lark as jl
from jaclang.jac.codeloc import CodeGenTarget, CodeLocInfo
from jaclang.jac.constant import Constants as Con, EdgeDir
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.symtable import Symbol, SymbolAccess, SymbolTable, SymbolType


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
        from jaclang.jac.passes import Pass

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

    def print(self, use_pp: bool = False, depth: Optional[int] = None) -> None:
        """Print ast."""
        if use_pp:
            pprint.PrettyPrinter(depth=depth).pprint(self.to_dict())
        else:
            print_tree(self)


class AstSymbolNode(AstNode, ABC):
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


class AstAccessNode(AstNode, ABC):
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


class AstDocNode(AstNode, ABC):
    """Nodes that have access."""

    def __init__(self, doc: Optional[String]) -> None:
        """Initialize ast."""
        self.doc: Optional[String] = doc


class AstAsyncNode(AstNode, ABC):
    """Nodes that have access."""

    def __init__(self, is_async: bool) -> None:
        """Initialize ast."""
        self.is_async: bool = is_async


class AstElseBodyNode(AstNode, ABC):
    """Nodes that have access."""

    def __init__(self, else_body: Optional[ElseStmt | ElseIf]) -> None:
        """Initialize ast."""
        self.else_body: Optional[ElseStmt | ElseIf] = else_body


class AstTypedVarNode(AstNode, ABC):
    """Nodes that have access."""

    def __init__(self, type_tag: Optional[SubTag[ExprType]]) -> None:
        """Initialize ast."""
        self.type_tag: Optional[SubTag[ExprType]] = type_tag


class WalkerStmtOnlyNode(AstNode, ABC):
    """WalkerStmtOnlyNode node type for Jac Ast."""

    def __init__(self) -> None:
        """Initialize walker statement only node."""
        self.from_walker: bool = False


class AstImplOnlyNode(AstNode, ABC):
    """ImplOnly node type for Jac Ast."""


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
        body: Sequence[ElementStmt],
        is_imported: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize whole program node."""
        self.name = name
        self.source = source
        self.body = body
        self.is_imported = is_imported
        self.mod_deps: dict[str, Module] = {}
        AstNode.__init__(self, kid=kid)
        AstDocNode.__init__(self, doc=doc)


class GlobalVars(AstAccessNode, AstDocNode):
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


class Test(AstSymbolNode, AstDocNode):
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


class ModuleCode(AstDocNode):
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


class PyInlineCode(AstDocNode):
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


class Import(AstDocNode):
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


class Architype(AstSymbolNode, AstAccessNode, AstDocNode):
    """ObjectArch node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        arch_type: Token,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[ExprType]],
        body: Optional[SubNodeList[ArchBlockStmt] | ArchDef],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
    ) -> None:
        """Initialize object arch node."""
        self.name = name
        self.arch_type = arch_type
        self.decorators = decorators
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


class ArchDef(AstSymbolNode, AstAccessNode, AstDocNode, AstImplOnlyNode):
    """ArchDef node type for Jac Ast."""

    def __init__(
        self,
        target: ArchRefChain,
        body: SubNodeList[ArchBlockStmt],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
    ) -> None:
        """Initialize arch def node."""
        self.decorators = decorators
        self.target = target
        self.body = body
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=target.py_resolve_name(),
            sym_name_node=target,
            sym_type=SymbolType.IMPL,
        )
        AstAccessNode.__init__(self, access=None)
        AstDocNode.__init__(self, doc=doc)


class Enum(AstSymbolNode, AstAccessNode, AstDocNode):
    """Enum node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[ExprType]],
        body: Optional[SubNodeList[EnumBlockStmt] | EnumDef],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
    ) -> None:
        """Initialize object arch node."""
        self.name = name
        self.decorators = decorators
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


class EnumDef(AstSymbolNode, AstDocNode, AstImplOnlyNode):
    """EnumDef node type for Jac Ast."""

    def __init__(
        self,
        target: ArchRefChain,
        body: SubNodeList[EnumBlockStmt],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
    ) -> None:
        """Initialize arch def node."""
        self.target = target
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


class Ability(AstSymbolNode, AstAccessNode, AstDocNode, AstAsyncNode):
    """Ability node type for Jac Ast."""

    def __init__(
        self,
        name_ref: NameType,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        is_abstract: bool,
        access: Optional[SubTag[Token]],
        signature: Optional[FuncSignature | ExprType | EventSignature],
        body: Optional[SubNodeList[CodeBlockStmt] | AbilityDef],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
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


class AbilityDef(AstSymbolNode, AstDocNode, AstImplOnlyNode):
    """AbilityDef node type for Jac Ast."""

    def __init__(
        self,
        target: ArchRefChain,
        signature: FuncSignature | EventSignature,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[ExprType]] = None,
        decl_link: Optional[Ability] = None,
    ) -> None:
        """Initialize ability def node."""
        self.target = target
        self.signature = signature
        self.body = body
        self.decorators = decorators
        self.decl_link = decl_link
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=target.py_resolve_name(),
            sym_name_node=target,
            sym_type=SymbolType.IMPL,
        )
        AstDocNode.__init__(self, doc=doc)


class FuncSignature(AstNode):
    """FuncSignature node type for Jac Ast."""

    def __init__(
        self,
        params: Optional[SubNodeList[ParamVar]],
        return_type: Optional[SubTag[ExprType]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize method signature node."""
        self.params = params
        self.return_type = return_type
        AstNode.__init__(self, kid=kid)

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


class EventSignature(AstNode):
    """EventSignature node type for Jac Ast."""

    def __init__(
        self,
        event: Token,
        arch_tag_info: Optional[ExprType],
        return_type: Optional[SubTag[ExprType]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize event signature node."""
        self.event = event
        self.arch_tag_info = arch_tag_info
        self.return_type = return_type
        AstNode.__init__(self, kid=kid)

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
        return ".".join(
            [f"({x.arch.value[1]}){x.py_resolve_name()}" for x in self.archs]
        )

    def flat_name(self) -> str:
        """Resolve name for python gen."""
        return (
            self.py_resolve_name().replace(".", "_").replace("(", "").replace(")", "_")
        )


class ParamVar(AstSymbolNode, AstTypedVarNode):
    """ParamVar node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[ExprType],
        value: Optional[ExprType],
        kid: Sequence[AstNode],
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


class ArchHas(AstAccessNode, AstDocNode):
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


class HasVar(AstSymbolNode, AstTypedVarNode):
    """HasVar node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        type_tag: SubTag[ExprType],
        value: Optional[ExprType],
        kid: Sequence[AstNode],
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


class TypedCtxBlock(AstNode):
    """TypedCtxBlock node type for Jac Ast."""

    def __init__(
        self,
        type_ctx: ExprType,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize typed context block node."""
        self.type_ctx = type_ctx
        self.body = body
        AstNode.__init__(self, kid=kid)


class IfStmt(AstElseBodyNode):
    """IfStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: ExprType,
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


class ExprStmt(AstNode):
    """ExprStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: ExprType,
        in_fstring: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize expr statement node."""
        self.expr = expr
        self.in_fstring = in_fstring
        AstNode.__init__(self, kid=kid)


class TryStmt(AstElseBodyNode):
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


class Except(AstNode):
    """Except node type for Jac Ast."""

    def __init__(
        self,
        ex_type: ExprType,
        name: Optional[Name],
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize except node."""
        self.ex_type = ex_type
        self.name = name
        self.body = body
        AstNode.__init__(self, kid=kid)


class FinallyStmt(AstNode):
    """FinallyStmt node type for Jac Ast."""

    def __init__(
        self,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize finally statement node."""
        self.body = body
        AstNode.__init__(self, kid=kid)


class IterForStmt(AstAsyncNode, AstElseBodyNode):
    """IterFor node type for Jac Ast."""

    def __init__(
        self,
        iter: Assignment,
        is_async: bool,
        condition: ExprType,
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


class InForStmt(AstAsyncNode, AstElseBodyNode):
    """InFor node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        is_async: bool,
        collection: ExprType,
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


class WhileStmt(AstNode):
    """WhileStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize while statement node."""
        self.condition = condition
        self.body = body
        AstNode.__init__(self, kid=kid)


class WithStmt(AstAsyncNode):
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
        expr: ExprType,
        alias: Optional[ExprType],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize module item node."""
        self.expr = expr
        self.alias = alias
        AstNode.__init__(self, kid=kid)


class RaiseStmt(AstNode):
    """RaiseStmt node type for Jac Ast."""

    def __init__(
        self,
        cause: Optional[ExprType],
        from_target: Optional[ExprType],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize raise statement node."""
        self.cause = cause
        self.from_target = from_target
        AstNode.__init__(self, kid=kid)


class AssertStmt(AstNode):
    """AssertStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: ExprType,
        error_msg: Optional[ExprType],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize assert statement node."""
        self.condition = condition
        self.error_msg = error_msg
        AstNode.__init__(self, kid=kid)


class CtrlStmt(AstNode):
    """CtrlStmt node type for Jac Ast."""

    def __init__(
        self,
        ctrl: Token,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize control statement node."""
        self.ctrl = ctrl
        AstNode.__init__(self, kid=kid)


class DeleteStmt(AstNode):
    """DeleteStmt node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize delete statement node."""
        self.target = target
        AstNode.__init__(self, kid=kid)


class ReportStmt(AstNode):
    """ReportStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: ExprType,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize report statement node."""
        self.expr = expr
        AstNode.__init__(self, kid=kid)


class ReturnStmt(AstNode):
    """ReturnStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: Optional[ExprType],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize return statement node."""
        self.expr = expr
        AstNode.__init__(self, kid=kid)


class IgnoreStmt(WalkerStmtOnlyNode):
    """IgnoreStmt node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize ignore statement node."""
        self.target = target
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)


class VisitStmt(WalkerStmtOnlyNode, AstElseBodyNode):
    """VisitStmt node type for Jac Ast."""

    def __init__(
        self,
        vis_type: Optional[SubNodeList[ExprType]],
        target: ExprType,
        else_body: Optional[ElseStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize visit statement node."""
        self.vis_type = vis_type
        self.target = target
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)
        AstElseBodyNode.__init__(self, else_body=else_body)


class RevisitStmt(WalkerStmtOnlyNode, AstElseBodyNode):
    """ReVisitStmt node type for Jac Ast."""

    def __init__(
        self,
        hops: Optional[ExprType],
        else_body: Optional[ElseStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize revisit statement node."""
        self.hops = hops
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)
        AstElseBodyNode.__init__(self, else_body=else_body)


class DisengageStmt(WalkerStmtOnlyNode):
    """DisengageStmt node type for Jac Ast."""

    def __init__(
        self,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize disengage statement node."""
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)


class AwaitExpr(AstNode):
    """AwaitStmt node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize sync statement node."""
        self.target = target
        AstNode.__init__(self, kid=kid)


class GlobalStmt(AstNode):
    """GlobalStmt node type for Jac Ast."""

    def __init__(
        self,
        target: SubNodeList[NameType],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize global statement node."""
        self.target = target
        AstNode.__init__(self, kid=kid)


class NonLocalStmt(GlobalStmt):
    """NonlocalStmt node type for Jac Ast."""


class Assignment(AstTypedVarNode):
    """Assignment node type for Jac Ast."""

    def __init__(
        self,
        target: SubNodeList[ExprType],
        value: Optional[ExprType | YieldExpr],
        type_tag: Optional[SubTag[ExprType]],
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


class BinaryExpr(AstNode):
    """ExprBinary node type for Jac Ast."""

    def __init__(
        self,
        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize binary expression node."""
        self.left = left
        self.right = right
        self.op = op
        # below is used for paren matching with PIPE_FWD ops
        self.pipe_chain_count = 0
        self.a_pipe_chain_count = 0
        AstNode.__init__(self, kid=kid)


class LambdaExpr(AstNode):
    """ExprLambda node type for Jac Ast."""

    def __init__(
        self,
        signature: FuncSignature,
        body: ExprType,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize lambda expression node."""
        self.signature = signature
        self.body = body
        AstNode.__init__(self, kid=kid)


class UnaryExpr(AstNode):
    """ExprUnary node type for Jac Ast."""

    def __init__(
        self,
        operand: ExprType,
        op: Token,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize unary expression node."""
        self.operand = operand
        self.op = op
        AstNode.__init__(self, kid=kid)


class IfElseExpr(AstNode):
    """ExprIfElse node type for Jac Ast."""

    def __init__(
        self,
        condition: ExprType,
        value: ExprType,
        else_value: ExprType,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize if else expression node."""
        self.condition = condition
        self.value = value
        self.else_value = else_value
        AstNode.__init__(self, kid=kid)


class MultiString(AstSymbolNode):
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
        values: Optional[SubNodeList[ExprType]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize expr value node."""
        self.values = values
        AstNode.__init__(self, kid=kid)


class ListVal(AstSymbolNode):
    """ListVal node type for Jac Ast."""

    def __init__(
        self,
        values: Optional[SubNodeList[ExprType]],
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


class SetVal(AstSymbolNode):
    """SetVal node type for Jac Ast."""

    def __init__(
        self,
        values: Optional[SubNodeList[ExprType]],
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


class TupleVal(AstSymbolNode):
    """TupleVal node type for Jac Ast."""

    def __init__(
        self,
        values: Optional[SubNodeList[ExprType | KWPair]],
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


class DictVal(AstSymbolNode):
    """ExprDict node type for Jac Ast."""

    def __init__(
        self,
        kv_pairs: Sequence[KVPair],
        kid: Sequence[KVPair],
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
        key: ExprType,
        value: ExprType,
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
        key: NameType,
        value: ExprType,
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
        target: ExprType,
        collection: ExprType,
        conditional: Optional[ExprType],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize comprehension expression node."""
        self.target = target
        self.collection = collection
        self.conditional = conditional
        AstNode.__init__(self, kid=kid)
        AstAsyncNode.__init__(self, is_async=is_async)


class ListCompr(AstSymbolNode):
    """ListCompr node type for Jac Ast."""

    def __init__(
        self,
        out_expr: ExprType,
        compr: InnerCompr,
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


class DictCompr(AstSymbolNode):
    """DictCompr node type for Jac Ast."""

    def __init__(
        self,
        kv_pair: KVPair,
        compr: InnerCompr,
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


class AtomTrailer(AstNode):
    """AtomTrailer node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        right: AtomType,
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


class AtomUnit(AstNode):
    """AtomUnit node type for Jac Ast."""

    def __init__(
        self,
        value: ExprType | YieldExpr,
        is_paren: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize atom unit expression node."""
        self.value = value
        self.is_paren = is_paren
        AstNode.__init__(self, kid=kid)


class YieldExpr(AstNode):
    """YieldStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: Optional[ExprType],
        with_from: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize yeild statement node."""
        self.expr = expr
        self.with_from = with_from
        AstNode.__init__(self, kid=kid)


class FuncCall(AstNode):
    """FuncCall node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        params: Optional[SubNodeList[ExprType | KWPair]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize function call expression node."""
        self.target = target
        self.params = params
        AstNode.__init__(self, kid=kid)


class IndexSlice(AstSymbolNode):
    """IndexSlice node type for Jac Ast."""

    def __init__(
        self,
        start: Optional[ExprType],
        stop: Optional[ExprType],
        step: Optional[ExprType],
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


class ArchRef(AstSymbolNode):
    """ArchRef node type for Jac Ast."""

    def __init__(
        self,
        name_ref: NameType,
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


class SpecialVarRef(AstSymbolNode):
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
        else:
            raise NotImplementedError("ICE: Special var reference not implemented")


class EdgeOpRef(WalkerStmtOnlyNode, AstSymbolNode):
    """EdgeOpRef node type for Jac Ast."""

    def __init__(
        self,
        filter_type: Optional[ExprType],
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
        conn_type: Optional[ExprType],
        conn_assign: Optional[AssignCompr],
        edge_dir: EdgeDir,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize connect op reference expression node."""
        self.conn_type = conn_type
        self.conn_assign = conn_assign
        self.edge_dir = edge_dir
        AstNode.__init__(self, kid=kid)


class FilterCompr(AstNode):
    """FilterCtx node type for Jac Ast."""

    def __init__(
        self,
        compares: SubNodeList[BinaryExpr],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize filter_cond context expression node."""
        self.compares = compares
        AstNode.__init__(self, kid=kid)


class AssignCompr(AstNode):
    """AssignCtx node type for Jac Ast."""

    def __init__(
        self,
        assigns: SubNodeList[KWPair],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize assign compr expression node."""
        self.assigns = assigns
        AstNode.__init__(self, kid=kid)


# Match Nodes
# ------------


class MatchStmt(AstNode):
    """MatchStmt node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
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
        guard: Optional[ExprType],
        body: SubNodeList[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match case node."""
        self.pattern = pattern
        self.guard = guard
        self.body = body
        AstNode.__init__(self, kid=kid)


class MatchOr(AstNode):
    """MatchOr node type for Jac Ast."""

    def __init__(
        self,
        patterns: list[MatchPattern],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match or node."""
        self.patterns = patterns
        AstNode.__init__(self, kid=kid)


class MatchAs(AstNode):
    """MatchAs node type for Jac Ast."""

    def __init__(
        self,
        name: NameType,
        pattern: Optional[MatchPattern],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match as node."""
        self.name = name
        self.pattern = pattern
        AstNode.__init__(self, kid=kid)


class MatchWild(AstNode):
    """Match wild card node type for Jac Ast."""


class MatchValue(AstNode):
    """MatchValue node type for Jac Ast."""

    def __init__(
        self,
        value: ExprType,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match value node."""
        self.value = value
        AstNode.__init__(self, kid=kid)


class MatchSingleton(AstNode):
    """MatchSingleton node type for Jac Ast."""

    def __init__(
        self,
        value: Bool | Null,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match singleton node."""
        self.value = value
        AstNode.__init__(self, kid=kid)


class MatchSequence(AstNode):
    """MatchSequence node type for Jac Ast."""

    def __init__(
        self,
        values: list[MatchPattern],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match sequence node."""
        self.values = values
        AstNode.__init__(self, kid=kid)


class MatchMapping(AstNode):
    """MatchMapping node type for Jac Ast."""

    def __init__(
        self,
        values: list[MatchKVPair | MatchStar],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match mapping node."""
        self.values = values
        AstNode.__init__(self, kid=kid)


class MatchKVPair(AstNode):
    """MatchKVPair node type for Jac Ast."""

    def __init__(
        self,
        key: MatchPattern | NameType,
        value: MatchPattern,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match key value pair node."""
        self.key = key
        self.value = value
        AstNode.__init__(self, kid=kid)


class MatchStar(AstNode):
    """MatchStar node type for Jac Ast."""

    def __init__(
        self,
        name: NameType,
        is_list: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match star node."""
        self.name = name
        self.is_list = is_list
        AstNode.__init__(self, kid=kid)


class MatchArch(AstNode):
    """MatchClass node type for Jac Ast."""

    def __init__(
        self,
        name: NameType,
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


class Name(TokenSymbol):
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
    ) -> None:
        """Initialize token."""
        self.is_enum_singleton = is_enum_singleton
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


class Literal(TokenSymbol):
    """Literal node type for Jac Ast."""

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

    @property
    def lit_value(self) -> int | str | float | bool | None | Callable[[], Any]:
        """Return literal value in its python type."""
        raise NotImplementedError


class BuiltinType(Name, Literal):
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
        return self.ast_str

    @property
    def ast_str(self) -> str:
        """Return ast string."""
        if (self.value.startswith("'''") and self.value.endswith("'''")) or (
            self.value.startswith('"""') and self.value.endswith('"""')
        ):
            ast_str = self.value[3:-3]
        elif (self.value.startswith("'") and self.value.endswith("'")) or (
            self.value.startswith('"') and self.value.endswith('"')
        ):
            ast_str = self.value[1:-1]
        else:
            ast_str = self.value
        return ast_str


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


class Semi(Token):
    """Semicolon node type for Jac Ast."""


# ----------------
class JacSource(EmptyToken):
    """SourceString node type for Jac Ast."""

    def __init__(self, source: str, mod_path: str) -> None:
        """Initialize source string."""
        super().__init__()
        self.value = source
        self.file_path = mod_path
        self.comments: list[jl.Token] = []

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


# ----------------

ArchType = Union[
    Architype,
    ArchDef,
    Enum,
    EnumDef,
]

NameType = Union[
    Name,
    SpecialVarRef,
    ArchRef,
]

AtomType = Union[
    NameType,
    Literal,
    MultiString,
    ListVal,
    TupleVal,
    SetVal,
    DictVal,
    ListCompr,
    SetCompr,
    GenCompr,
    DictCompr,
    EdgeOpRef,
    FilterCompr,
    AssignCompr,
    IndexSlice,
]

ExprType = Union[
    AwaitExpr,
    UnaryExpr,
    BinaryExpr,
    IfElseExpr,
    FuncCall,
    YieldExpr,
    AtomTrailer,
    AtomType,
    AtomUnit,
]

ElementStmt = Union[
    GlobalVars,
    Test,
    ModuleCode,
    Ability,
    AbilityDef,
    ArchType,
    PyInlineCode,
    Import,
]

ArchBlockStmt = Union[
    Ability,
    Architype,
    ArchHas,
    PyInlineCode,
]

EnumBlockStmt = Union[
    Name,
    Assignment,
    PyInlineCode,
]

CodeBlockStmt = Union[
    ArchType,
    ExprStmt,
    Import,
    Ability,
    AbilityDef,
    Assignment,
    IfStmt,
    IfElseExpr,
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
    DisengageStmt,
    RevisitStmt,
    VisitStmt,
    IgnoreStmt,
    PyInlineCode,
    TypedCtxBlock,
    GlobalStmt,
    NonLocalStmt,
    MatchStmt,
    Semi,
]


MatchPattern = Union[
    MatchValue,
    MatchSingleton,
    MatchSequence,
    MatchStar,
    MatchMapping,
    MatchArch,
    MatchWild,
    MatchAs,
    MatchOr,
]


def print_tree(
    root: AstNode,
    marker: str = "+-- ",
    level_markers: Optional[list[bool]] = None,
    output_file: Optional[str] = None,
) -> None:
    """Recursive function that prints the hierarchical structure of a tree."""

    def __node_repr_in_tree(node: AstNode) -> str:
        if isinstance(node, Token):
            return f"{node.__class__.__name__} - {node.value}"
            # return f"{node.__class__.__name__}({node.name}, {node.value})"
        else:
            return node.__class__.__name__

    if root is None:
        return

    empty_str = " " * len(marker)
    connection_str = "|" + empty_str[:-1]
    if not level_markers:
        level_markers = []
    level = len(level_markers)  # recursion level

    def mapper(draw: bool) -> str:
        return connection_str if draw else empty_str

    markers = "".join(map(mapper, level_markers[:-1]))
    markers += marker if level > 0 else ""
    if output_file:
        with open(output_file, "a+") as f:
            print(f"{markers}{__node_repr_in_tree(root)}", file=f)
    else:
        print(f"{markers}{__node_repr_in_tree(root)}")
    # After root has been printed, recurse down (depth-first) the child nodes.
    for i, child in enumerate(root.kid):
        # The last child will not need connection markers on the current level
        # (see example above)
        is_last = i == len(root.kid) - 1
        print_tree(
            child, marker, [*level_markers, not is_last], output_file=output_file
        )

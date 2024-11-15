"""Abstract class for IR Passes for Jac."""

from __future__ import annotations

import ast as ast3
import builtins
import os
from dataclasses import dataclass
from hashlib import md5
from types import EllipsisType
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    Sequence,
    TYPE_CHECKING,
    Type,
    TypeVar,
)


from jaclang.compiler import TOKEN_MAP
from jaclang.compiler.codeloc import CodeGenTarget, CodeLocInfo
from jaclang.compiler.constant import (
    Constants as Con,
    EdgeDir,
    JacSemTokenModifier as SemTokMod,
    JacSemTokenType as SemTokType,
    SymbolType,
)
from jaclang.compiler.constant import DELIM_MAP, SymbolAccess, Tokens as Tok
from jaclang.compiler.semtable import SemRegistry
from jaclang.utils.treeprinter import dotgen_ast_tree, print_ast_tree

if TYPE_CHECKING:
    from jaclang.compiler.symtable import Symbol, SymbolTable


class AstNode:
    """Abstract syntax tree node for Jac."""

    def __init__(self, kid: Sequence[AstNode]) -> None:
        """Initialize ast."""
        self.parent: Optional[AstNode] = None
        self.kid: list[AstNode] = [x.set_parent(self) for x in kid]
        self._sym_tab: Optional[SymbolTable] = None
        self._sub_node_tab: dict[type, list[AstNode]] = {}
        self._in_mod_nodes: list[AstNode] = []
        self.gen: CodeGenTarget = CodeGenTarget()
        self.meta: dict[str, str] = {}
        self.loc: CodeLocInfo = CodeLocInfo(*self.resolve_tok_range())

    @property
    def sym_tab(self) -> SymbolTable:
        """Get symbol table."""
        # sym_tab should never be accessed without being set in codebase
        if not self._sym_tab:
            raise ValueError(
                f"Symbol table not set for {type(self).__name__}. Impossible.\n"
                f"Node: {self.pp()}\n"
                f"Parent: {self.parent.pp() if self.parent else None}\n"
            )
        return self._sym_tab

    @sym_tab.setter
    def sym_tab(self, sym_tab: SymbolTable) -> None:
        """Set symbol table."""
        self._sym_tab = sym_tab

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

    def insert_kids_at_pos(
        self, nodes: Sequence[AstNode], pos: int, pos_update: bool = True
    ) -> AstNode:
        """Insert kids at position."""
        self.kid = [*self.kid[:pos], *nodes, *self.kid[pos:]]
        if pos_update:
            for i in nodes:
                i.parent = self
            self.loc.update_token_range(*self.resolve_tok_range())
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

    def gen_token(self, name: Tok, value: Optional[str] = None) -> Token:
        """Generate token."""
        value = (
            value
            if value
            else (
                DELIM_MAP[name]
                if name in DELIM_MAP
                else TOKEN_MAP[name.value] if name.value in TOKEN_MAP else name.value
            )
        )
        return Token(
            name=name,
            value=value,
            orig_src=self.loc.orig_src,
            col_start=self.loc.col_start,
            col_end=0,
            line=self.loc.first_line,
            end_line=self.loc.last_line,
            pos_start=0,
            pos_end=0,
        )

    def get_all_sub_nodes(self, typ: Type[T], brute_force: bool = True) -> list[T]:
        """Get all sub nodes of type."""
        from jaclang.compiler.passes import Pass

        return Pass.get_all_sub_nodes(node=self, typ=typ, brute_force=brute_force)

    def find_parent_of_type(self, typ: Type[T]) -> Optional[T]:
        """Get parent of type."""
        from jaclang.compiler.passes import Pass

        return Pass.find_parent_of_type(node=self, typ=typ)

    def parent_of_type(self, typ: Type[T]) -> T:
        """Get parent of type."""
        ret = self.find_parent_of_type(typ)
        if isinstance(ret, typ):
            return ret
        else:
            raise ValueError(f"Parent of type {typ} not found.")

    def format(self) -> str:
        """Get all sub nodes of type."""
        from jaclang.compiler.passes.tool import JacFormatPass

        return JacFormatPass(self, None).ir.gen.jac

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

    def flatten(self) -> list[AstNode]:
        """Flatten ast."""
        ret = [self]
        for k in self.kid:
            ret += k.flatten()
        return ret

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        return False

    def unparse(self) -> str:
        """Unparse ast node."""
        valid = self.normalize()
        res = " ".join([i.unparse() for i in self.kid])
        if not valid:
            raise NotImplementedError(f"Node {type(self).__name__} is not valid.")
        return res


class AstSymbolNode(AstNode):
    """Nodes that have link to a symbol in symbol table."""

    def __init__(
        self, sym_name: str, name_spec: NameAtom, sym_category: SymbolType
    ) -> None:
        """Initialize ast."""
        self.name_spec = name_spec
        self.name_spec.name_of = self
        self.name_spec._sym_name = sym_name
        self.name_spec._sym_category = sym_category

    @property
    def sym(self) -> Optional[Symbol]:
        """Get symbol."""
        return self.name_spec.sym

    @property
    def sym_name(self) -> str:
        """Get symbol name."""
        return self.name_spec.sym_name

    @property
    def sym_category(self) -> SymbolType:
        """Get symbol category."""
        return self.name_spec.sym_category

    @property
    def py_ctx_func(self) -> Type[ast3.AST]:
        """Get python context function."""
        return self.name_spec.py_ctx_func

    @property
    def expr_type(self) -> str:
        """Get symbol type."""
        return self.name_spec.expr_type

    @property
    def type_sym_tab(self) -> Optional[SymbolTable]:
        """Get type symbol table."""
        return self.name_spec.type_sym_tab


class AstSymbolStubNode(AstSymbolNode):
    """Nodes that have link to a symbol in symbol table."""

    def __init__(self, sym_type: SymbolType) -> None:
        """Initialize ast."""
        AstSymbolNode.__init__(
            self,
            sym_name=f"[{self.__class__.__name__}]",
            name_spec=Name.gen_stub_from_node(self, f"[{self.__class__.__name__}]"),
            sym_category=sym_type,
        )


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
            if self.access and self.access.tag.name == Tok.KW_PRIV
            else (
                SymbolAccess.PROTECTED
                if self.access and self.access.tag.name == Tok.KW_PROT
                else SymbolAccess.PUBLIC
            )
        )


T = TypeVar("T", bound=AstNode)


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


class Expr(AstNode):
    """Expr node type for Jac Ast."""

    def __init__(self, type_src: Optional[Expr] = None) -> None:
        """Initialize expression node."""
        self.type_src = type_src or self  # Only used for ArchRef
        self._sym_type: str = "NoType"
        self._type_sym_tab: Optional[SymbolTable] = None

    @property
    def expr_type(self) -> str:
        """Get symbol type."""
        return self.type_src._sym_type

    @expr_type.setter
    def expr_type(self, sym_type: str) -> None:
        """Set symbol type."""
        self.type_src._sym_type = sym_type

    @property
    def type_sym_tab(self) -> Optional[SymbolTable]:
        """Get type symbol table."""
        return self.type_src._type_sym_tab

    @type_sym_tab.setter
    def type_sym_tab(self, type_sym_tab: SymbolTable) -> None:
        """Set type symbol table."""
        self.type_src._type_sym_tab = type_sym_tab


class AtomExpr(Expr, AstSymbolStubNode):
    """AtomExpr node type for Jac Ast."""


class ElementStmt(AstDocNode):
    """ElementStmt node type for Jac Ast."""


class ArchBlockStmt(AstNode):
    """ArchBlockStmt node type for Jac Ast."""


class EnumBlockStmt(AstNode):
    """EnumBlockStmt node type for Jac Ast."""


class CodeBlockStmt(AstNode):
    """CodeBlockStmt node type for Jac Ast."""


class AstImplOnlyNode(CodeBlockStmt, ElementStmt, AstSymbolNode):
    """ImplOnly node type for Jac Ast."""

    def __init__(
        self, target: ArchRefChain, body: SubNodeList, decl_link: Optional[AstNode]
    ) -> None:
        """Initialize impl only node."""
        self.target = target
        self.body = body
        self.decl_link = decl_link
        AstSymbolNode.__init__(
            self,
            sym_name=self.target.py_resolve_name(),
            name_spec=self.create_impl_name_node(),
            sym_category=SymbolType.IMPL,
        )

    @property
    def sym_tab(self) -> SymbolTable:
        """Get symbol table."""
        return super().sym_tab

    @sym_tab.setter
    def sym_tab(self, sym_tab: SymbolTable) -> None:
        """Set symbol table."""
        self._sym_tab = sym_tab
        self.name_spec._sym_tab = sym_tab

    def create_impl_name_node(self) -> Name:
        """Create impl name."""
        ret = Name(
            orig_src=self.target.archs[-1].loc.orig_src,
            name=Tok.NAME.value,
            value=self.target.py_resolve_name(),
            col_start=self.target.archs[0].loc.col_start,
            col_end=self.target.archs[-1].loc.col_end,
            line=self.target.archs[0].loc.first_line,
            end_line=self.target.archs[-1].loc.last_line,
            pos_start=self.target.archs[0].loc.pos_start,
            pos_end=self.target.archs[-1].loc.pos_end,
        )
        ret.name_of = self
        return ret


class AstImplNeedingNode(AstSymbolNode, Generic[T]):
    """Impl needing node type for Jac Ast."""

    def __init__(self, body: Optional[T]) -> None:
        """Initialize impl needing node."""
        self.body = body

    @property
    def needs_impl(self) -> bool:
        """Need impl."""
        return self.body is None


class NameAtom(AtomExpr, EnumBlockStmt):
    """NameSpec node type for Jac Ast."""

    def __init__(self) -> None:
        """Initialize name spec node."""
        self.name_of: AstSymbolNode = self
        self._sym: Optional[Symbol] = None
        self._sym_name: str = ""
        self._sym_category: SymbolType = SymbolType.UNKNOWN
        self._py_ctx_func: Type[ast3.AST] = ast3.Load
        AtomExpr.__init__(self)

    @property
    def sym(self) -> Optional[Symbol]:
        """Get symbol."""
        return self._sym

    @sym.setter
    def sym(self, sym: Symbol) -> None:
        """Set symbol."""
        self._sym = sym

    @property
    def sym_name(self) -> str:
        """Get symbol name."""
        return self._sym_name

    @property
    def sym_category(self) -> SymbolType:
        """Get symbol category."""
        return self._sym_category

    @property
    def clean_type(self) -> str:
        """Get clean type."""
        ret_type = self.expr_type.replace("builtins.", "").replace("NoType", "")
        return ret_type

    @property
    def py_ctx_func(self) -> Type[ast3.AST]:
        """Get python context function."""
        return self._py_ctx_func

    @py_ctx_func.setter
    def py_ctx_func(self, py_ctx_func: Type[ast3.AST]) -> None:
        """Set python context function."""
        self._py_ctx_func = py_ctx_func

    @property
    def sem_token(self) -> Optional[tuple[SemTokType, SemTokMod]]:
        """Resolve semantic token."""
        if isinstance(self.name_of, BuiltinType):
            return SemTokType.CLASS, SemTokMod.DECLARATION
        name_of = (
            self.sym.decl.name_of
            if self.sym and not isinstance(self.sym.decl.name_of, Name)
            else self.name_of
        )
        if isinstance(name_of, ModulePath):
            return SemTokType.NAMESPACE, SemTokMod.DEFINITION
        if isinstance(name_of, Architype):
            return SemTokType.CLASS, SemTokMod.DECLARATION
        if isinstance(name_of, Enum):
            return SemTokType.ENUM, SemTokMod.DECLARATION
        if isinstance(name_of, Ability) and name_of.is_method:
            return SemTokType.METHOD, SemTokMod.DECLARATION
        if isinstance(name_of, (Ability, Test)):
            return SemTokType.FUNCTION, SemTokMod.DECLARATION
        if isinstance(name_of, ParamVar):
            return SemTokType.PARAMETER, SemTokMod.DECLARATION
        if self.sym and self.sym_name.isupper():
            return SemTokType.VARIABLE, SemTokMod.READONLY
        if (
            self.sym
            and self.sym.decl.name_of == self.sym.decl
            and self.sym_name in dir(builtins)
            and callable(getattr(builtins, self.sym_name))
        ):
            return SemTokType.FUNCTION, SemTokMod.DEFINITION
        if self.sym:
            return SemTokType.PROPERTY, SemTokMod.DEFINITION
        return None


class ArchSpec(ElementStmt, CodeBlockStmt, AstSymbolNode, AstDocNode, AstSemStrNode):
    """ArchSpec node type for Jac Ast."""

    def __init__(self, decorators: Optional[SubNodeList[Expr]] = None) -> None:
        """Initialize walker statement only node."""
        self.decorators = decorators


class MatchPattern(AstNode):
    """MatchPattern node type for Jac Ast."""


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize sub tag node."""
        res = self.tag.normalize() if deep else True
        self.set_kids(nodes=[self.gen_token(Tok.COLON), self.tag])
        return res


# SubNodeList were created to simplify the type safety of the
# parser's implementation. We basically need to maintain tokens
# of mixed type in the kid list of the subnodelist as well as
# separating out typed items of interest in the ast node class body.
class SubNodeList(AstNode, Generic[T]):
    """SubNodeList node type for Jac Ast."""

    def __init__(
        self,
        items: list[T],
        delim: Optional[Tok],
        kid: Sequence[AstNode],
        left_enc: Optional[Token] = None,
        right_enc: Optional[Token] = None,
    ) -> None:
        """Initialize sub node list node."""
        self.items = items
        self.delim = delim
        self.left_enc = left_enc
        self.right_enc = right_enc
        AstNode.__init__(self, kid=kid)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize sub node list node."""
        res = True
        if deep:
            for i in self.items:
                res = res and i.normalize()
        new_kid: list[AstNode] = []
        if self.left_enc:
            new_kid.append(self.left_enc)
        for i in self.items:
            new_kid.append(i)
            if self.delim:
                new_kid.append(self.gen_token(self.delim))
        if self.delim and self.items:
            new_kid.pop()
        if self.right_enc:
            new_kid.append(self.right_enc)
        self.set_kids(nodes=new_kid if len(new_kid) else [EmptyToken()])
        return res


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
        terminals: list[Token],
        kid: Sequence[AstNode],
        stub_only: bool = False,
        registry: Optional[SemRegistry] = None,
    ) -> None:
        """Initialize whole program node."""
        self.name = name
        self.source = source
        self.body = body
        self.is_imported = is_imported
        self.stub_only = stub_only
        self.impl_mod: list[Module] = []
        self.test_mod: list[Module] = []
        self.mod_deps: dict[str, Module] = {}
        self.py_mod_dep_map: dict[str, str] = {}
        self.py_raise_map: dict[str, str] = {}
        self.registry = registry
        self.terminals: list[Token] = terminals
        self.is_raised_from_py: bool = False
        AstNode.__init__(self, kid=kid)
        AstDocNode.__init__(self, doc=doc)

    @property
    def annexable_by(self) -> Optional[str]:
        """Get annexable by."""
        if not self.stub_only and (
            self.loc.mod_path.endswith(".impl.jac")
            or self.loc.mod_path.endswith(".test.jac")
        ):
            head_mod_name = self.name.split(".")[0]
            potential_path = os.path.join(
                os.path.dirname(self.loc.mod_path),
                f"{head_mod_name}.jac",
            )
            if os.path.exists(potential_path) and potential_path != self.loc.mod_path:
                return potential_path
            annex_dir = os.path.split(os.path.dirname(self.loc.mod_path))[-1]
            if annex_dir.endswith(".impl") or annex_dir.endswith(".test"):
                head_mod_name = os.path.split(os.path.dirname(self.loc.mod_path))[
                    -1
                ].split(".")[0]
                potential_path = os.path.join(
                    os.path.dirname(os.path.dirname(self.loc.mod_path)),
                    f"{head_mod_name}.jac",
                )
                if (
                    os.path.exists(potential_path)
                    and potential_path != self.loc.mod_path
                ):
                    return potential_path
        return None

    def normalize(self, deep: bool = False) -> bool:
        """Normalize module node."""
        res = True
        if deep:
            res = self.doc.normalize() if self.doc else True
            for i in self.body:
                res = res and i.normalize()
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        new_kid.extend(self.body)
        self.set_kids(nodes=new_kid if len(new_kid) else [EmptyToken()])
        return res

    def unparse(self) -> str:
        """Unparse module node."""
        super().unparse()
        return self.format()


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize global var node."""
        res = True
        if deep:
            res = self.access.normalize(deep) if self.access else True
            res = res and self.assignments.normalize(deep)
            res = res and self.doc.normalize(deep) if self.doc else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        if self.is_frozen:
            new_kid.append(self.gen_token(Tok.KW_LET))
        else:
            new_kid.append(self.gen_token(Tok.KW_GLOBAL))
        if self.access:
            new_kid.append(self.access)
        new_kid.append(self.assignments)
        self.set_kids(nodes=new_kid)
        return res


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
                orig_src=name.orig_src,
                name=Tok.NAME.value,
                value=f"_jac_gen_{Test.TEST_COUNT}",
                col_start=name.loc.col_start,
                col_end=name.loc.col_end,
                line=name.loc.first_line,
                end_line=name.loc.last_line,
                pos_start=name.pos_start,
                pos_end=name.pos_end,
            )
        )
        self.name.parent = self
        self.name._sym_name = (
            f"test_{self.name.value}"
            if not self.name.value.startswith("test_")
            else self.name.value
        )
        self.body = body
        AstNode.__init__(self, kid=kid)
        if self.name not in self.kid:
            self.insert_kids_at_pos([self.name], pos=1, pos_update=False)
        AstSymbolNode.__init__(
            self,
            sym_name=self.name.sym_name,
            name_spec=self.name,
            sym_category=SymbolType.TEST,
        )
        AstDocNode.__init__(self, doc=doc)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize test node."""
        res = True
        if deep:
            res = self.name.normalize(deep)
            res = res and self.body.normalize(deep)
            res = res and self.doc.normalize(deep) if self.doc else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        new_kid.append(self.gen_token(Tok.KW_TEST))
        new_kid.append(self.name)
        new_kid.append(self.body)
        self.set_kids(nodes=new_kid)
        return res


class ModuleCode(ElementStmt, ArchBlockStmt, EnumBlockStmt):
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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize module code node."""
        res = True
        if deep:
            res = self.name.normalize(deep) if self.name else res
            res = res and self.body.normalize(deep)
            res = res and self.doc.normalize(deep) if self.doc else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        new_kid.append(self.gen_token(Tok.KW_WITH))
        new_kid.append(self.gen_token(Tok.KW_ENTRY))
        if self.name:
            new_kid.append(self.name)
        new_kid.append(self.body)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize inline python code node."""
        res = True
        if deep:
            res = self.code.normalize(deep)
            res = res and self.doc.normalize(deep) if self.doc else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        new_kid.append(self.gen_token(Tok.PYNLINE))
        new_kid.append(self.code)
        new_kid.append(self.gen_token(Tok.PYNLINE))
        self.set_kids(nodes=new_kid)
        return res


class Import(ElementStmt, CodeBlockStmt):
    """Import node type for Jac Ast."""

    def __init__(
        self,
        hint: Optional[SubTag[Name]],
        from_loc: Optional[ModulePath],
        items: SubNodeList[ModuleItem] | SubNodeList[ModulePath],
        is_absorb: bool,  # For includes
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
    ) -> None:
        """Initialize import node."""
        self.hint = hint
        self.from_loc = from_loc
        self.items = items
        self.is_absorb = is_absorb
        AstNode.__init__(self, kid=kid)
        AstDocNode.__init__(self, doc=doc)

    @property
    def is_py(self) -> bool:
        """Check if import is python."""
        if self.hint and self.hint.tag.value == "py":
            return True
        if not self.hint:
            return not self.__jac_detected
        return False

    @property
    def is_jac(self) -> bool:
        """Check if import is jac."""
        if self.hint and self.hint.tag.value == "jac":
            return True
        if not self.hint:
            return self.__jac_detected
        return False

    @property
    def __jac_detected(self) -> bool:
        """Check if import is jac."""
        if self.from_loc:
            if self.from_loc.resolve_relative_path().endswith(".jac"):
                return True
            if os.path.isdir(self.from_loc.resolve_relative_path()):
                if os.path.exists(
                    os.path.join(self.from_loc.resolve_relative_path(), "__init__.jac")
                ):
                    return True
                for i in self.items.items:
                    if isinstance(
                        i, ModuleItem
                    ) and self.from_loc.resolve_relative_path(i.name.value).endswith(
                        ".jac"
                    ):
                        return True
        return any(
            isinstance(i, ModulePath) and i.resolve_relative_path().endswith(".jac")
            for i in self.items.items
        )

    def normalize(self, deep: bool = False) -> bool:
        """Normalize import node."""
        res = True
        if deep:
            res = self.hint.normalize(deep) if self.hint else res
            res = res and self.from_loc.normalize(deep) if self.from_loc else res
            res = res and self.items.normalize(deep)
            res = res and self.doc.normalize(deep) if self.doc else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        if self.is_absorb:
            new_kid.append(self.gen_token(Tok.KW_INCLUDE))
        else:
            new_kid.append(self.gen_token(Tok.KW_IMPORT))
        if self.hint:
            new_kid.append(self.hint)
        if self.from_loc:
            new_kid.append(self.gen_token(Tok.KW_FROM))
            new_kid.append(self.from_loc)
            new_kid.append(self.gen_token(Tok.COMMA))
        new_kid.append(self.items)
        new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


class ModulePath(AstSymbolNode):
    """ModulePath node type for Jac Ast."""

    def __init__(
        self,
        path: Optional[list[Name]],
        level: int,
        alias: Optional[Name],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize module path node."""
        self.path = path
        self.level = level
        self.alias = alias
        self.sub_module: Optional[Module] = None
        self.abs_path: Optional[str] = None

        name_spec = alias if alias else path[0] if path else None

        AstNode.__init__(self, kid=kid)
        if not name_spec:
            pkg_name = self.loc.mod_path
            for _ in range(self.level):
                pkg_name = os.path.dirname(pkg_name)
            pkg_name = pkg_name.split(os.sep)[-1]
            name_spec = Name.gen_stub_from_node(self, pkg_name)
            self.level += 1
        if not isinstance(name_spec, Name):
            raise ValueError("ModulePath should have a name spec. Impossible.")
        AstSymbolNode.__init__(
            self,
            sym_name=name_spec.sym_name,
            name_spec=name_spec,
            sym_category=SymbolType.MODULE,
        )

    @property
    def dot_path_str(self) -> str:
        """Get path string."""
        return ("." * self.level) + ".".join(
            [p.value for p in self.path] if self.path else [self.name_spec.sym_name]
        )

    def resolve_relative_path(self, target_item: Optional[str] = None) -> str:
        """Convert an import target string into a relative file path."""
        target = self.dot_path_str
        if target_item:
            target += f".{target_item}"
        base_path = os.path.dirname(self.loc.mod_path)
        base_path = base_path if base_path else os.getcwd()
        parts = target.split(".")
        traversal_levels = self.level - 1 if self.level > 0 else 0
        actual_parts = parts[traversal_levels:]
        for _ in range(traversal_levels):
            base_path = os.path.dirname(base_path)
        relative_path = os.path.join(base_path, *actual_parts)
        relative_path = (
            relative_path + ".jac"
            if os.path.exists(relative_path + ".jac")
            else relative_path
        )
        return relative_path

    def normalize(self, deep: bool = False) -> bool:
        """Normalize module path node."""
        res = True
        if deep:
            if self.path:
                for p in self.path:
                    res = res and p.normalize(deep)
            res = res and self.alias.normalize(deep) if self.alias else res
        new_kid: list[AstNode] = []
        for _ in range(self.level):
            new_kid.append(self.gen_token(Tok.DOT))
        if self.path:
            for p in self.path:
                res = res and p.normalize(deep)
                new_kid.append(p)
                new_kid.append(self.gen_token(Tok.DOT))
            new_kid.pop()
        if self.alias:
            res = res and self.alias.normalize(deep)
            new_kid.append(self.gen_token(Tok.KW_AS))
            new_kid.append(self.alias)
        self.set_kids(nodes=new_kid)
        return res


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
        self.sub_module: Optional[Module] = None
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=alias.sym_name if alias else name.sym_name,
            name_spec=alias if alias else name,
            sym_category=SymbolType.MOD_VAR,
        )
        self.abs_path: Optional[str] = None

    @property
    def from_parent(self) -> Import:
        """Get import parent."""
        if (
            not self.parent
            or not self.parent.parent
            or not isinstance(self.parent.parent, Import)
        ):
            raise ValueError("Import parent not found. Not Possible.")
        return self.parent.parent

    @property
    def from_mod_path(self) -> ModulePath:
        """Get relevant module path."""
        if not self.from_parent.from_loc:
            raise ValueError("Module items should have module path. Not Possible.")
        return self.from_parent.from_loc

    def normalize(self, deep: bool = False) -> bool:
        """Normalize module item node."""
        res = True
        if deep:
            res = res and self.name.normalize(deep)
            res = res and self.alias.normalize(deep) if self.alias else res
        new_kid: list[AstNode] = [self.name]
        if self.alias:
            new_kid.append(self.gen_token(Tok.KW_AS))
            new_kid.append(self.alias)
        self.set_kids(nodes=new_kid)
        return res


class Architype(ArchSpec, AstAccessNode, ArchBlockStmt, AstImplNeedingNode):
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
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=name.value,
            name_spec=name,
            sym_category=(
                SymbolType.OBJECT_ARCH
                if arch_type.name == Tok.KW_OBJECT
                else (
                    SymbolType.NODE_ARCH
                    if arch_type.name == Tok.KW_NODE
                    else (
                        SymbolType.EDGE_ARCH
                        if arch_type.name == Tok.KW_EDGE
                        else (
                            SymbolType.WALKER_ARCH
                            if arch_type.name == Tok.KW_WALKER
                            else SymbolType.TYPE
                        )
                    )
                )
            ),
        )
        AstImplNeedingNode.__init__(self, body=body)
        AstAccessNode.__init__(self, access=access)
        AstDocNode.__init__(self, doc=doc)
        AstSemStrNode.__init__(self, semstr=semstr)
        ArchSpec.__init__(self, decorators=decorators)

    @property
    def is_abstract(self) -> bool:
        """Check if has an abstract method."""
        body = (
            self.body.items
            if isinstance(self.body, SubNodeList)
            else self.body.body.items if isinstance(self.body, ArchDef) else []
        )
        return any(isinstance(i, Ability) and i.is_abstract for i in body)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize architype node."""
        res = True
        if deep:
            res = self.name.normalize(deep)
            res = res and self.arch_type.normalize(deep)
            res = res and self.access.normalize(deep) if self.access else res
            res = (
                res and self.base_classes.normalize(deep) if self.base_classes else res
            )
            res = res and self.body.normalize(deep) if self.body else res
            res = res and self.doc.normalize(deep) if self.doc else res
            res = res and self.semstr.normalize(deep) if self.semstr else res
            res = res and self.decorators.normalize(deep) if self.decorators else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        if self.decorators:
            new_kid.append(self.gen_token(Tok.DECOR_OP))
            new_kid.append(self.decorators)
        new_kid.append(self.arch_type)
        if self.access:
            new_kid.append(self.access)
        if self.semstr:
            new_kid.append(self.semstr)
        new_kid.append(self.name)
        if self.base_classes:
            new_kid.append(self.gen_token(Tok.COLON))
            new_kid.append(self.base_classes)
            new_kid.append(self.gen_token(Tok.COLON))
        if self.body:
            if isinstance(self.body, AstImplOnlyNode):
                new_kid.append(self.gen_token(Tok.SEMI))
            else:
                new_kid.append(self.body)
        else:
            new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


class ArchDef(AstImplOnlyNode):
    """ArchDef node type for Jac Ast."""

    def __init__(
        self,
        target: ArchRefChain,
        body: SubNodeList[ArchBlockStmt],
        kid: Sequence[AstNode],
        doc: Optional[String] = None,
        decl_link: Optional[Architype] = None,
    ) -> None:
        """Initialize arch def node."""
        AstNode.__init__(self, kid=kid)
        AstDocNode.__init__(self, doc=doc)
        AstImplOnlyNode.__init__(self, target=target, body=body, decl_link=decl_link)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize arch def node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
            res = res and self.body.normalize(deep)
            res = res and self.doc.normalize(deep) if self.doc else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        new_kid.append(self.target)
        new_kid.append(self.body)
        self.set_kids(nodes=new_kid)
        return res


class Enum(ArchSpec, AstAccessNode, AstImplNeedingNode, ArchBlockStmt):
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
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=name.value,
            name_spec=name,
            sym_category=SymbolType.ENUM_ARCH,
        )
        AstImplNeedingNode.__init__(self, body=body)
        AstAccessNode.__init__(self, access=access)
        AstDocNode.__init__(self, doc=doc)
        AstSemStrNode.__init__(self, semstr=semstr)
        ArchSpec.__init__(self, decorators=decorators)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize enum node."""
        res = True
        if deep:
            res = self.name.normalize(deep)
            res = res and self.access.normalize(deep) if self.access else res
            res = (
                res and self.base_classes.normalize(deep) if self.base_classes else res
            )
            res = res and self.body.normalize(deep) if self.body else res
            res = res and self.doc.normalize(deep) if self.doc else res
            res = res and self.semstr.normalize(deep) if self.semstr else res
            res = res and self.decorators.normalize(deep) if self.decorators else res
        new_kid: list[AstNode] = []
        if self.decorators:
            new_kid.append(self.gen_token(Tok.DECOR_OP))
            new_kid.append(self.decorators)
        if self.doc:
            new_kid.append(self.doc)
        new_kid.append(self.gen_token(Tok.KW_ENUM))
        if self.access:
            new_kid.append(self.access)
        if self.semstr:
            new_kid.append(self.semstr)
        new_kid.append(self.name)
        if self.base_classes:
            new_kid.append(self.gen_token(Tok.COLON))
            new_kid.append(self.base_classes)
            new_kid.append(self.gen_token(Tok.COLON))
        if self.body:
            if isinstance(self.body, AstImplOnlyNode):
                new_kid.append(self.gen_token(Tok.SEMI))
            else:
                new_kid.append(self.gen_token(Tok.LBRACE))
                new_kid.append(self.body)
                new_kid.append(self.gen_token(Tok.RBRACE))
        else:
            new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


class EnumDef(AstImplOnlyNode):
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
        AstNode.__init__(self, kid=kid)
        AstDocNode.__init__(self, doc=doc)
        AstImplOnlyNode.__init__(self, target=target, body=body, decl_link=decl_link)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize enum def node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
            res = res and self.body.normalize(deep)
            res = res and self.doc.normalize(deep) if self.doc else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        new_kid.append(self.target)
        new_kid.append(self.gen_token(Tok.LBRACE))
        new_kid.append(self.body)
        new_kid.append(self.gen_token(Tok.RBRACE))
        self.set_kids(nodes=new_kid)
        return res


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
    """Ability node type for Jac Ast."""

    def __init__(
        self,
        name_ref: NameAtom,
        is_async: bool,
        is_override: bool,
        is_static: bool,
        is_abstract: bool,
        access: Optional[SubTag[Token]],
        signature: FuncSignature | EventSignature,
        body: Optional[SubNodeList[CodeBlockStmt] | AbilityDef | FuncCall],
        kid: Sequence[AstNode],
        semstr: Optional[String] = None,
        doc: Optional[String] = None,
        decorators: Optional[SubNodeList[Expr]] = None,
    ) -> None:
        """Initialize func arch node."""
        self.name_ref = name_ref
        self.is_override = is_override
        self.is_static = is_static
        self.is_abstract = is_abstract
        self.decorators = decorators
        self.signature = signature
        AstNode.__init__(self, kid=kid)
        AstImplNeedingNode.__init__(self, body=body)
        AstSemStrNode.__init__(self, semstr=semstr)
        AstSymbolNode.__init__(
            self,
            sym_name=self.py_resolve_name(),
            name_spec=name_ref,
            sym_category=SymbolType.ABILITY,
        )
        AstAccessNode.__init__(self, access=access)
        AstDocNode.__init__(self, doc=doc)
        AstAsyncNode.__init__(self, is_async=is_async)

    @property
    def is_method(self) -> bool:
        """Check if is func."""
        return self.signature.is_method

    @property
    def owner_method(self) -> Optional[Architype | Enum]:
        """Check if is owner method."""
        return (
            self.parent.parent
            if self.parent
            and self.parent.parent
            and isinstance(self.parent.parent, (Architype, Enum))
            else None
        )

    @property
    def is_genai_ability(self) -> bool:
        """Check if is genai_ability."""
        return isinstance(self.body, FuncCall)

    def py_resolve_name(self) -> str:
        """Resolve name."""
        if isinstance(self.name_ref, Name):
            return self.name_ref.value
        elif isinstance(self.name_ref, (SpecialVarRef, ArchRef)):
            return self.name_ref.py_resolve_name()
        else:
            raise NotImplementedError

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.name_ref.normalize(deep)
            res = res and self.access.normalize(deep) if self.access else res
            res = res and self.signature.normalize(deep) if self.signature else res
            res = res and self.body.normalize(deep) if self.body else res
            res = res and self.semstr.normalize(deep) if self.semstr else res
            res = res and self.decorators.normalize(deep) if self.decorators else res
            res = res and self.doc.normalize(deep) if self.doc else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        if self.decorators:
            new_kid.append(self.gen_token(Tok.DECOR_OP))
            new_kid.append(self.decorators)
            new_kid.append(self.gen_token(Tok.WS))
        if self.is_async:
            new_kid.append(self.gen_token(Tok.KW_ASYNC))
        if self.is_override:
            new_kid.append(self.gen_token(Tok.KW_OVERRIDE))
        if self.is_static:
            new_kid.append(self.gen_token(Tok.KW_STATIC))
        new_kid.append(self.gen_token(Tok.KW_CAN))
        if self.access:
            new_kid.append(self.access)
        if self.semstr:
            new_kid.append(self.semstr)
        new_kid.append(self.name_ref)
        if self.signature:
            new_kid.append(self.signature)
        if self.is_genai_ability:
            new_kid.append(self.gen_token(Tok.KW_BY))
        if self.is_abstract:
            new_kid.append(self.gen_token(Tok.KW_ABSTRACT))
        if self.body:
            if isinstance(self.body, AstImplOnlyNode):
                new_kid.append(self.gen_token(Tok.SEMI))
            else:
                new_kid.append(self.body)
                if self.is_genai_ability:
                    new_kid.append(self.gen_token(Tok.SEMI))
        else:
            new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


class AbilityDef(AstImplOnlyNode):
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
        self.signature = signature
        self.decorators = decorators
        AstNode.__init__(self, kid=kid)
        AstDocNode.__init__(self, doc=doc)
        AstImplOnlyNode.__init__(self, target=target, body=body, decl_link=decl_link)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ability def node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
            res = res and self.signature.normalize(deep)
            res = res and self.body.normalize(deep)
            res = res and self.doc.normalize(deep) if self.doc else res
            res = res and self.decorators.normalize(deep) if self.decorators else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        new_kid.append(self.target)
        new_kid.append(self.signature)

        new_kid.append(self.body)

        self.set_kids(nodes=new_kid)
        return res


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
        self.is_method = False
        AstNode.__init__(self, kid=kid)
        AstSemStrNode.__init__(self, semstr=semstr)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.params.normalize(deep) if self.params else res
            res = res and self.return_type.normalize(deep) if self.return_type else res
            res = res and self.semstr.normalize(deep) if self.semstr else res
        new_kid: list[AstNode] = [self.gen_token(Tok.LPAREN)]
        if self.params:
            new_kid.append(self.params)
        new_kid.append(self.gen_token(Tok.RPAREN))
        if self.return_type:
            new_kid.append(self.gen_token(Tok.RETURN_HINT))
            if self.semstr:
                new_kid.append(self.semstr)
                new_kid.append(self.gen_token(Tok.COLON))
            new_kid.append(self.return_type)
        self.set_kids(nodes=new_kid)
        return res

    @property
    def is_static(self) -> bool:
        """Check if is static."""
        return (isinstance(self.parent, Ability) and self.parent.is_static) or (
            isinstance(self.parent, AbilityDef)
            and isinstance(self.parent.decl_link, Ability)
            and self.parent.decl_link.is_static
        )

    @property
    def is_in_py_class(self) -> bool:
        """Check if the ability belongs to a class."""
        is_archi = self.find_parent_of_type(Architype)
        is_class = is_archi is not None and is_archi.arch_type.name == Tok.KW_CLASS

        return (
            isinstance(self.parent, Ability)
            and self.parent.is_method is not None
            and is_class
        ) or (
            isinstance(self.parent, AbilityDef)
            and isinstance(self.parent.decl_link, Ability)
            and self.parent.decl_link.is_method
            and is_class
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
        self.is_method = False
        AstNode.__init__(self, kid=kid)
        AstSemStrNode.__init__(self, semstr=semstr)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.event.normalize(deep)
            res = (
                res and self.arch_tag_info.normalize(deep)
                if self.arch_tag_info
                else res
            )
            res = res and self.return_type.normalize(deep) if self.return_type else res
            res = res and self.semstr.normalize(deep) if self.semstr else res
        new_kid: list[AstNode] = [self.gen_token(Tok.KW_WITH)]
        if self.arch_tag_info:
            new_kid.append(self.arch_tag_info)
        new_kid.append(self.event)
        if self.return_type:
            if self.semstr:
                new_kid.append(self.semstr)
            new_kid.append(self.gen_token(Tok.RETURN_HINT))
            new_kid.append(self.return_type)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            for a in self.archs:
                res = res and a.normalize(deep)
        new_kid: list[AstNode] = []
        for a in self.archs:
            new_kid.append(a)
        self.set_kids(nodes=new_kid)
        return res

    def py_resolve_name(self) -> str:
        """Resolve name."""

        def get_tag(x: ArchRef) -> str:
            return (
                "en"
                if x.arch_type.value == "enum"
                else "cls" if x.arch_type.value == "class" else x.arch_type.value[1]
            )

        return ".".join([f"({get_tag(x)}){x.sym_name}" for x in self.archs])

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
            name_spec=name,
            sym_category=SymbolType.VAR,
        )
        AstTypedVarNode.__init__(self, type_tag=type_tag)
        AstSemStrNode.__init__(self, semstr=semstr)

    def normalize(self, deep: bool = True) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.name.normalize(deep)
            res = res and self.unpack.normalize(deep) if self.unpack else res
            res = res and self.type_tag.normalize(deep) if self.type_tag else res
            res = res and self.value.normalize(deep) if self.value else res
            res = res and self.semstr.normalize(deep) if self.semstr else res
        new_kid: list[AstNode] = []
        if self.unpack:
            new_kid.append(self.unpack)
        new_kid.append(self.name)
        if self.semstr:
            new_kid.append(self.gen_token(Tok.COLON))
            new_kid.append(self.semstr)
        if self.type_tag:
            new_kid.append(self.type_tag)
        if self.value:
            new_kid.append(self.gen_token(Tok.EQ))
            new_kid.append(self.value)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize has statement node."""
        res = True
        if deep:
            res = self.access.normalize(deep) if self.access else res
            res = res and self.vars.normalize(deep) if self.vars else res
            res = res and self.doc.normalize(deep) if self.doc else res
        new_kid: list[AstNode] = []
        if self.doc:
            new_kid.append(self.doc)
        if self.is_static:
            new_kid.append(self.gen_token(Tok.KW_STATIC))
        (
            new_kid.append(self.gen_token(Tok.KW_LET))
            if self.is_frozen
            else new_kid.append(self.gen_token(Tok.KW_HAS))
        )
        if self.access:
            new_kid.append(self.access)
        new_kid.append(self.vars)
        new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


class HasVar(AstSymbolNode, AstTypedVarNode, AstSemStrNode):
    """HasVar node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        type_tag: SubTag[Expr],
        value: Optional[Expr],
        defer: bool,
        kid: Sequence[AstNode],
        semstr: Optional[String] = None,
    ) -> None:
        """Initialize has var node."""
        self.name = name
        self.value = value
        self.defer = defer
        AstNode.__init__(self, kid=kid)
        AstSymbolNode.__init__(
            self,
            sym_name=name.value,
            name_spec=name,
            sym_category=SymbolType.HAS_VAR,
        )
        AstTypedVarNode.__init__(self, type_tag=type_tag)
        AstSemStrNode.__init__(self, semstr=semstr)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize has var node."""
        res = True
        if deep:
            res = self.name.normalize(deep)
            res = res and self.type_tag.normalize(deep) if self.type_tag else res
            res = res and self.value.normalize(deep) if self.value else res
            res = res and self.semstr.normalize(deep) if self.semstr else res
        new_kid: list[AstNode] = [self.name]
        if self.semstr:
            new_kid.append(self.gen_token(Tok.COLON))
            new_kid.append(self.semstr)
        if self.type_tag:
            new_kid.append(self.type_tag)
        if self.value:
            new_kid.append(self.gen_token(Tok.EQ))
            new_kid.append(self.value)
        if self.defer:
            new_kid.append(self.gen_token(Tok.KW_BY))
            new_kid.append(self.gen_token(Tok.KW_POST_INIT))
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize typed context block node."""
        res = True
        if deep:
            res = self.type_ctx.normalize(deep)
            res = res and self.body.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.RETURN_HINT),
            self.type_ctx,
            self.body,
        ]
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize if statement node."""
        res = True
        if deep:
            res = self.condition.normalize(deep)
            res = res and self.body.normalize(deep)
            res = res and self.else_body.normalize(deep) if self.else_body else res
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_IF),
            self.condition,
            self.body,
        ]
        if self.else_body:
            new_kid.append(self.else_body)
        self.set_kids(nodes=new_kid)
        return res


class ElseIf(IfStmt):
    """ElseIfs node type for Jac Ast."""

    def normalize(self, deep: bool = False) -> bool:
        """Normalize else if statement node."""
        res = True
        if deep:
            res = self.condition.normalize(deep)
            res = res and self.body.normalize(deep)
            res = res and self.else_body.normalize(deep) if self.else_body else res
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_ELIF),
            self.condition,
            self.body,
        ]
        if self.else_body:
            new_kid.append(self.else_body)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize else statement node."""
        res = True
        if deep:
            res = self.body.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_ELSE),
            self.body,
        ]
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = True) -> bool:
        """Normalize ast node."""
        if deep:
            res = self.expr.normalize(deep)
        new_kid: list[AstNode] = []
        if self.in_fstring:
            new_kid.append(self.expr)
        else:
            new_kid.append(self.expr)
            new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res and self.expr is not None


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize try statement node."""
        res = True
        if deep:
            res = self.body.normalize(deep)
            res = res and self.excepts.normalize(deep) if self.excepts else res
            res = res and self.else_body.normalize(deep) if self.else_body else res
            res = (
                res and self.finally_body.normalize(deep) if self.finally_body else res
            )
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_TRY),
        ]
        new_kid.append(self.body)
        if self.excepts:
            new_kid.append(self.excepts)
        if self.else_body:
            new_kid.append(self.else_body)
        if self.finally_body:
            new_kid.append(self.finally_body)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize except node."""
        res = True
        if deep:
            res = self.ex_type.normalize(deep)
            res = res and self.name.normalize(deep) if self.name else res
            res = res and self.body.normalize(deep) if self.body else res
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_EXCEPT),
            self.ex_type,
        ]
        if self.name:
            new_kid.append(self.gen_token(Tok.KW_AS))
            new_kid.append(self.name)
        new_kid.append(self.body)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize finally statement node."""
        res = True
        if deep:
            res = self.body.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_FINALLY),
        ]
        new_kid.append(self.body)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize iter for node."""
        res = True
        if deep:
            res = self.iter.normalize(deep)
            res = self.condition.normalize(deep)
            res = self.count_by.normalize(deep)
            res = self.body.normalize(deep)
            res = self.else_body.normalize(deep) if self.else_body else res
        new_kid: list[AstNode] = []
        if self.is_async:
            new_kid.append(self.gen_token(Tok.KW_ASYNC))
        new_kid.append(self.gen_token(Tok.KW_FOR))
        new_kid.append(self.iter)
        new_kid.append(self.gen_token(Tok.KW_TO))
        new_kid.append(self.condition)
        new_kid.append(self.gen_token(Tok.KW_BY))
        new_kid.append(self.count_by)
        new_kid.append(self.body)
        if self.else_body:
            new_kid.append(self.else_body)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize in for node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
            res = res and self.collection.normalize(deep)
            res = res and self.body.normalize(deep)
            res = res and self.else_body.normalize(deep) if self.else_body else res
        new_kid: list[AstNode] = []
        if self.is_async:
            new_kid.append(self.gen_token(Tok.KW_ASYNC))
        new_kid.append(self.gen_token(Tok.KW_FOR))
        new_kid.append(self.target)
        new_kid.append(self.gen_token(Tok.KW_IN))
        new_kid.append(self.collection)

        if self.body:
            new_kid.append(self.body)
        if self.else_body:
            new_kid.append(self.else_body)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize while statement node."""
        res = True
        if deep:
            res = self.condition.normalize(deep)
            res = res and self.body.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_WHILE),
            self.condition,
        ]
        if self.body:
            new_kid.append(self.body)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize with statement node."""
        res = True
        if deep:
            res = self.exprs.normalize(deep)
            res = res and self.body.normalize(deep)
        new_kid: list[AstNode] = []
        if self.is_async:
            new_kid.append(self.gen_token(Tok.KW_ASYNC))
        new_kid.append(self.gen_token(Tok.KW_WITH))
        new_kid.append(self.exprs)
        new_kid.append(self.gen_token(Tok.LBRACE))
        new_kid.append(self.body)
        new_kid.append(self.gen_token(Tok.RBRACE))

        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = True) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.expr.normalize(deep)
            res = res and self.alias.normalize(deep) if self.alias else res
        new_kid: list[AstNode] = [self.expr]
        if self.alias:
            new_kid.append(self.gen_token(Tok.KW_AS))
            new_kid.append(self.alias)
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize raise statement node."""
        res = True
        if deep:
            res = res and self.cause.normalize(deep) if self.cause else res
            res = res and self.from_target.normalize(deep) if self.from_target else res
        new_kid: list[AstNode] = [self.gen_token(Tok.KW_RAISE)]
        if self.cause:
            new_kid.append(self.cause)
        if self.from_target:
            new_kid.append(self.gen_token(Tok.KW_FROM))
            new_kid.append(self.from_target)
        new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize assert statement node."""
        res = True
        if deep:
            res = self.condition.normalize(deep)
            res = res and self.error_msg.normalize(deep) if self.error_msg else res
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_ASSERT),
            self.condition,
        ]
        if self.error_msg:
            new_kid.append(self.gen_token(Tok.COMMA))
            new_kid.append(self.error_msg)
        new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


class CheckStmt(CodeBlockStmt):
    """DeleteStmt node type for Jac Ast."""

    def __init__(
        self,
        target: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize delete statement node."""
        self.target = target
        AstNode.__init__(self, kid=kid)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize delete statement node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_CHECK),
            self.target,
            self.gen_token(Tok.SEMI),
        ]
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize control statement node."""
        res = True
        if deep:
            res = self.ctrl.normalize(deep)
        new_kid: list[AstNode] = [self.ctrl, self.gen_token(Tok.SEMI)]
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize delete statement node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_DELETE),
            self.target,
            self.gen_token(Tok.SEMI),
        ]
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize report statement node."""
        res = True
        if deep:
            res = self.expr.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_REPORT),
            self.expr,
            self.gen_token(Tok.SEMI),
        ]
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize return statement node."""
        res = True
        if deep:
            res = self.expr.normalize(deep) if self.expr else res
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_RETURN),
        ]
        if self.expr:
            new_kid.append(self.expr)
        new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ignore statement node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_IGNORE),
            self.target,
            self.gen_token(Tok.SEMI),
        ]
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize visit statement node."""
        res = True
        if deep:
            res = self.vis_type.normalize(deep) if self.vis_type else res
            res = self.target.normalize(deep)
            res = res and self.else_body.normalize(deep) if self.else_body else res
        new_kid: list[AstNode] = []
        new_kid.append(self.gen_token(Tok.KW_VISIT))
        if self.vis_type:
            new_kid.append(self.gen_token(Tok.COLON))
            new_kid.append(self.vis_type)
            new_kid.append(self.gen_token(Tok.COLON))
        new_kid.append(self.target)
        if self.else_body:
            new_kid.append(self.else_body)
        else:
            new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize revisit statement node."""
        res = True
        if deep:
            res = self.hops.normalize(deep) if self.hops else res
            res = res and self.else_body.normalize(deep) if self.else_body else res
        new_kid: list[AstNode] = [self.gen_token(Tok.KW_REVISIT)]
        if self.hops:
            new_kid.append(self.hops)
        if self.else_body:
            new_kid.append(self.else_body)
        new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


class DisengageStmt(WalkerStmtOnlyNode, CodeBlockStmt):
    """DisengageStmt node type for Jac Ast."""

    def __init__(
        self,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize disengage statement node."""
        AstNode.__init__(self, kid=kid)
        WalkerStmtOnlyNode.__init__(self)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize disengage statement node."""
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_DISENGAGE),
            self.gen_token(Tok.SEMI),
        ]
        self.set_kids(nodes=new_kid)
        return True


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
        Expr.__init__(self)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize sync statement node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_AWAIT),
            self.target,
        ]
        self.set_kids(nodes=new_kid)
        return res


class GlobalStmt(CodeBlockStmt):
    """GlobalStmt node type for Jac Ast."""

    def __init__(
        self,
        target: SubNodeList[NameAtom],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize global statement node."""
        self.target = target
        AstNode.__init__(self, kid=kid)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize global statement node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.GLOBAL_OP),
            self.target,
            self.gen_token(Tok.SEMI),
        ]
        self.set_kids(nodes=new_kid)
        return res


class NonLocalStmt(GlobalStmt):
    """NonlocalStmt node type for Jac Ast."""

    def normalize(self, deep: bool = False) -> bool:
        """Normalize nonlocal statement node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.NONLOCAL_OP),
            self.target,
            self.gen_token(Tok.SEMI),
        ]
        self.set_kids(nodes=new_kid)
        return res


class Assignment(AstSemStrNode, AstTypedVarNode, EnumBlockStmt, CodeBlockStmt):
    """Assignment node type for Jac Ast."""

    def __init__(
        self,
        target: SubNodeList[Expr],
        value: Optional[Expr | YieldExpr],
        type_tag: Optional[SubTag[Expr]],
        kid: Sequence[AstNode],
        mutable: bool = True,
        aug_op: Optional[Token] = None,
        semstr: Optional[String] = None,
        is_enum_stmt: bool = False,
    ) -> None:
        """Initialize assignment node."""
        self.target = target
        self.value = value
        self.mutable = mutable
        self.aug_op = aug_op
        self.is_enum_stmt = is_enum_stmt
        AstNode.__init__(self, kid=kid)
        AstSemStrNode.__init__(self, semstr=semstr)
        AstTypedVarNode.__init__(self, type_tag=type_tag)

    def normalize(self, deep: bool = True) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
            res = res and self.value.normalize(deep) if self.value else res
            res = res and self.type_tag.normalize(deep) if self.type_tag else res
            res = res and self.aug_op.normalize(deep) if self.aug_op else res
        new_kid: list[AstNode] = []
        new_kid.append(self.target)
        if self.semstr:
            new_kid.append(self.gen_token(Tok.COLON))
            new_kid.append(self.semstr)
        if self.type_tag:
            new_kid.append(self.type_tag)
        if self.aug_op:
            new_kid.append(self.aug_op)
        if self.value:
            if not self.aug_op:
                new_kid.append(self.gen_token(Tok.EQ))
            new_kid.append(self.value)
        if isinstance(self.parent, SubNodeList) and isinstance(
            self.parent.parent, GlobalVars
        ):
            if self.parent.kid.index(self) == len(self.parent.kid) - 1:
                new_kid.append(self.gen_token(Tok.SEMI))
        elif (not self.is_enum_stmt) and not isinstance(self.parent, IterForStmt):
            new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.left.normalize(deep)
            res = res and self.right.normalize(deep) if self.right else res
            res = res and self.op.normalize(deep) if self.op else res
        new_kid: list[AstNode] = [
            self.gen_token(Tok.LPAREN),
            self.left,
            self.op,
            self.right,
            self.gen_token(Tok.RPAREN),
        ]
        self.set_kids(nodes=new_kid)
        return res


class CompareExpr(Expr):
    """CompareExpr node type for Jac Ast."""

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
        Expr.__init__(self)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.left.normalize(deep)
            for right in self.rights:
                res = res and right.normalize(deep)
            for op in self.ops:
                res = res and op.normalize(deep)
        new_kid: list[AstNode] = [self.left]
        for i, right in enumerate(self.rights):
            new_kid.append(self.ops[i])
            new_kid.append(right)
        self.set_kids(nodes=new_kid)
        return res


class BoolExpr(Expr):
    """BoolExpr node type for Jac Ast."""

    def __init__(
        self,
        op: Token,
        values: list[Expr],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize binary expression node."""
        self.values = values
        self.op = op
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            for value in self.values:
                res = res and value.normalize(deep)
            res = res and self.op.normalize(deep) if self.op else res
        new_kid: list[AstNode] = []
        for i, value in enumerate(self.values):
            if i > 0:
                new_kid.append(self.op)
            new_kid.append(value)
        self.set_kids(nodes=new_kid)
        return res


class LambdaExpr(Expr):
    """ExprLambda node type for Jac Ast."""

    def __init__(
        self,
        body: Expr,
        kid: Sequence[AstNode],
        signature: Optional[FuncSignature] = None,
    ) -> None:
        """Initialize lambda expression node."""
        self.signature = signature
        self.body = body
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.signature.normalize(deep) if self.signature else res
            res = res and self.body.normalize(deep)
        new_kid: list[AstNode] = [self.gen_token(Tok.KW_WITH)]
        if self.signature:
            new_kid.append(self.signature)
        new_kid += [
            self.gen_token(Tok.KW_CAN),
            self.body,
            self.gen_token(Tok.SEMI),
        ]
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.operand.normalize(deep)
            res = res and self.op.normalize(deep) if self.op else res
        new_kid: list[AstNode] = [self.op, self.operand]
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.condition.normalize(deep)
            res = res and self.value.normalize(deep)
            res = res and self.else_value.normalize(deep)
        new_kid: list[AstNode] = [
            self.value,
            self.gen_token(Tok.KW_IF),
            self.condition,
            self.gen_token(Tok.KW_ELSE),
            self.else_value,
        ]
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.STRING)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            for string in self.strings:
                res = res and string.normalize(deep)
        new_kid: list[AstNode] = []
        for string in self.strings:
            new_kid.append(string)
        self.set_kids(nodes=new_kid)
        return res


class FString(AtomExpr):
    """FString node type for Jac Ast."""

    def __init__(
        self,
        parts: Optional[SubNodeList[String | ExprStmt]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize fstring expression node."""
        self.parts = parts
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.STRING)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.parts.normalize(deep) if self.parts else res
        new_kid: list[AstNode] = []
        is_single_quote = (
            isinstance(self.kid[0], Token) and self.kid[0].name == Tok.FSTR_SQ_START
        )
        if self.parts:
            if is_single_quote:
                new_kid.append(self.gen_token(Tok.FSTR_SQ_START))
            else:
                new_kid.append(self.gen_token(Tok.FSTR_START))
            for i in self.parts.items:
                if isinstance(i, String):
                    i.value = (
                        "{{" if i.value == "{" else "}}" if i.value == "}" else i.value
                    )
            new_kid.append(self.parts)
            if is_single_quote:
                new_kid.append(self.gen_token(Tok.FSTR_SQ_END))
            else:
                new_kid.append(self.gen_token(Tok.FSTR_END))
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.SEQUENCE)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.values.normalize(deep) if self.values else res
        new_kid: list[AstNode] = [
            self.gen_token(Tok.LSQUARE),
        ]
        if self.values:
            new_kid.append(self.values)
        new_kid.append(self.gen_token(Tok.RSQUARE))
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.SEQUENCE)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.values.normalize(deep) if self.values else res
        new_kid: list[AstNode] = [
            self.gen_token(Tok.LBRACE),
        ]
        if self.values:
            new_kid.append(self.values)
        new_kid.append(self.gen_token(Tok.RBRACE))
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.SEQUENCE)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.values.normalize(deep) if self.values else res
        in_ret_type = (
            self.parent
            and isinstance(self.parent, IndexSlice)
            and self.parent
            and isinstance(self.parent.parent, AtomTrailer)
            and self.parent.parent
            and isinstance(self.parent.parent.parent, FuncSignature)
        )
        new_kid: list[AstNode] = (
            [
                self.gen_token(Tok.LPAREN),
            ]
            if not in_ret_type
            else []
        )
        if self.values:
            new_kid.append(self.values)
            if len(self.values.items) < 2:
                new_kid.append(self.gen_token(Tok.COMMA))
        if not in_ret_type:
            new_kid.append(self.gen_token(Tok.RPAREN))
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.SEQUENCE)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            for kv_pair in self.kv_pairs:
                res = res and kv_pair.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.LBRACE),
        ]
        for i, kv_pair in enumerate(self.kv_pairs):
            new_kid.append(kv_pair)
            if i < len(self.kv_pairs) - 1:
                new_kid.append(self.gen_token(Tok.COMMA))
        new_kid.append(self.gen_token(Tok.RBRACE))
        self.set_kids(nodes=new_kid)
        return res


class KVPair(AstNode):
    """ExprKVPair node type for Jac Ast."""

    def __init__(
        self,
        key: Optional[Expr],  # is **key if blank
        value: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize key value pair expression node."""
        self.key = key
        self.value = value
        AstNode.__init__(self, kid=kid)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.key.normalize(deep) if self.key else res
            res = res and self.value.normalize(deep)
        new_kid: list[AstNode] = []
        if self.key:
            new_kid.append(self.key)
            new_kid.append(self.gen_token(Tok.COLON))
        else:
            new_kid.append(self.gen_token(Tok.STAR_POW))
        new_kid.append(self.value)
        self.set_kids(nodes=new_kid)
        return res


class KWPair(AstNode):
    """ExprKWPair node type for Jac Ast."""

    def __init__(
        self,
        key: Optional[NameAtom],  # is **value if blank
        value: Expr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize keyword pair expression node."""
        self.key = key
        self.value = value
        AstNode.__init__(self, kid=kid)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.key.normalize(deep) if self.key else res
            res = res and self.value.normalize(deep)
        new_kid: list[AstNode] = []
        if self.key:
            new_kid.append(self.key)
            new_kid.append(self.gen_token(Tok.EQ))
        new_kid.append(self.value)
        self.set_kids(nodes=new_kid)
        return res


class InnerCompr(AstAsyncNode):
    """ListCompr node type for Jac Ast."""

    def __init__(
        self,
        is_async: bool,
        target: Expr,
        collection: Expr,
        conditional: Optional[list[Expr]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize comprehension expression node."""
        self.target = target
        self.collection = collection
        self.conditional = conditional
        AstNode.__init__(self, kid=kid)
        AstAsyncNode.__init__(self, is_async=is_async)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
            res = res and self.collection.normalize(deep)
            for cond in self.conditional if self.conditional else []:
                res = res and cond.normalize(deep)
        new_kid: list[AstNode] = []
        if self.is_async:
            new_kid.append(self.gen_token(Tok.KW_ASYNC))
        new_kid.append(self.gen_token(Tok.KW_FOR))
        new_kid.append(self.target)
        new_kid.append(self.gen_token(Tok.KW_IN))
        new_kid.append(self.collection)
        for cond in self.conditional if self.conditional else []:
            new_kid.append(self.gen_token(Tok.KW_IF))
            new_kid.append(cond)
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.SEQUENCE)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.out_expr.normalize(deep)
            for comp in self.compr:
                res = res and comp.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.LSQUARE),
            self.out_expr,
        ]
        for comp in self.compr:
            new_kid.append(comp)
        new_kid.append(self.gen_token(Tok.RSQUARE))
        self.set_kids(nodes=new_kid)
        return res


class GenCompr(ListCompr):
    """GenCompr node type for Jac Ast."""

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.out_expr.normalize(deep)
            for comp in self.compr:
                res = res and comp.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.LPAREN),
            self.out_expr,
        ]
        for comp in self.compr:
            new_kid.append(comp)
        new_kid.append(self.gen_token(Tok.RPAREN))
        self.set_kids(nodes=new_kid)
        return res


class SetCompr(ListCompr):
    """SetCompr node type for Jac Ast."""

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.out_expr.normalize(deep)
            for comp in self.compr:
                res = res and comp.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.LBRACE),
            self.out_expr,
        ]
        for comp in self.compr:
            new_kid.append(comp)
        new_kid.append(self.gen_token(Tok.RBRACE))
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.SEQUENCE)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        res = self.kv_pair.normalize(deep)
        for comp in self.compr:
            res = res and comp.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.LBRACE),
            self.kv_pair,
        ]
        for comp in self.compr:
            new_kid.append(comp)
        new_kid.append(self.gen_token(Tok.RBRACE))
        self.set_kids(nodes=new_kid)
        return res


class AtomTrailer(Expr):
    """AtomTrailer node type for Jac Ast."""

    def __init__(
        self,
        target: Expr,
        right: AtomExpr | Expr,
        is_attr: bool,
        is_null_ok: bool,
        kid: Sequence[AstNode],
        is_genai: bool = False,
    ) -> None:
        """Initialize atom trailer expression node."""
        self.target = target
        self.right = right
        self.is_attr = is_attr
        self.is_null_ok = is_null_ok
        self.is_genai = is_genai
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self)

    def normalize(self, deep: bool = True) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
            res = res and self.right.normalize(deep) if self.right else res
        new_kid: list[AstNode] = [self.target]
        if self.is_null_ok:
            new_kid.append(self.gen_token(Tok.NULL_OK))
        if self.is_attr:
            new_kid.append(self.gen_token(Tok.DOT))
        if self.right:
            new_kid.append(self.right)
        self.set_kids(nodes=new_kid)
        return res

    @property
    def as_attr_list(self) -> list[AstSymbolNode]:
        """Unwind trailer into list of ast symbol nodes."""
        left = self.right if isinstance(self.right, AtomTrailer) else self.target
        right = self.target if isinstance(self.right, AtomTrailer) else self.right
        trag_list: list[AstSymbolNode] = (
            [right] if isinstance(right, AstSymbolNode) else []
        )
        while isinstance(left, AtomTrailer) and left.is_attr:
            if isinstance(left.right, AstSymbolNode):
                trag_list.insert(0, left.right)
            left = left.target
        if isinstance(left, AstSymbolNode):
            trag_list.insert(0, left)
        return trag_list


class AtomUnit(Expr):
    """AtomUnit node type for Jac Ast."""

    def __init__(
        self,
        value: Expr | YieldExpr,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize atom unit expression node."""
        self.value = value
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self)

    def normalize(self, deep: bool = True) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.value.normalize(deep)
        new_kid: list[AstNode] = []
        new_kid.append(self.gen_token(Tok.LPAREN))
        new_kid.append(self.value)
        new_kid.append(self.gen_token(Tok.RPAREN))
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize yield statement node."""
        res = True
        if deep:
            res = self.expr.normalize(deep) if self.expr else res
        new_kid: list[AstNode] = [self.gen_token(Tok.KW_YIELD)]
        if self.with_from:
            new_kid.append(self.gen_token(Tok.KW_FROM))
        if self.expr:
            new_kid.append(self.expr)
        new_kid.append(self.gen_token(Tok.SEMI))
        self.set_kids(nodes=new_kid)
        return res


class FuncCall(Expr):
    """FuncCall node type for Jac Ast."""

    def __init__(
        self,
        target: Expr,
        params: Optional[SubNodeList[Expr | KWPair]],
        genai_call: Optional[FuncCall],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize function call expression node."""
        self.target = target
        self.params = params
        self.genai_call = genai_call
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self)

    def normalize(self, deep: bool = True) -> bool:
        """Normalize ast node."""
        if deep:
            res = self.target.normalize(deep)
            res = res and (not self.params or self.params.normalize(deep))
        new_kids = [self.target, self.gen_token(Tok.LPAREN, "(")]
        if self.params:
            new_kids.append(self.params)
        if self.genai_call:
            new_kids.append(self.gen_token(Tok.KW_BY))
            new_kids.append(self.genai_call)
        new_kids.append(self.gen_token(Tok.RPAREN, ")"))
        self.set_kids(nodes=new_kids)
        return res


class IndexSlice(AtomExpr):
    """IndexSlice node type for Jac Ast."""

    @dataclass
    class Slice:
        """Slice node for index slice."""

        start: Optional[Expr]
        stop: Optional[Expr]
        step: Optional[Expr]

    def __init__(
        self,
        slices: list[Slice],
        is_range: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize index slice expression node."""
        self.slices = slices
        self.is_range = is_range
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.SEQUENCE)

    def normalize(self, deep: bool = True) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            for slice in self.slices:
                res = slice.start.normalize(deep) if slice.start else res
                res = res and slice.stop.normalize(deep) if slice.stop else res
                res = res and slice.step.normalize(deep) if slice.step else res
        new_kid: list[AstNode] = []
        new_kid.append(self.gen_token(Tok.LSQUARE))
        if self.is_range:
            for i, slice in enumerate(self.slices):
                if i > 0:
                    new_kid.append(self.gen_token(Tok.COMMA))
                if slice.start:
                    new_kid.append(slice.start)
                new_kid.append(self.gen_token(Tok.COLON))
                if slice.stop:
                    new_kid.append(slice.stop)
                if slice.step:
                    new_kid.append(self.gen_token(Tok.COLON))
                    new_kid.append(slice.step)
        elif len(self.slices) == 1 and self.slices[0].start:
            new_kid.append(self.slices[0].start)
        else:
            res = False
        new_kid.append(self.gen_token(Tok.RSQUARE))
        self.set_kids(nodes=new_kid)
        return res


class ArchRef(AtomExpr):
    """ArchRef node type for Jac Ast."""

    def __init__(
        self,
        arch_name: NameAtom,
        arch_type: Token,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize architype reference expression node."""
        self.arch_name = arch_name
        self.arch_type = arch_type
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self, type_src=arch_name)
        AstSymbolNode.__init__(
            self,
            sym_name=arch_name.sym_name,
            name_spec=arch_name,
            sym_category=SymbolType.TYPE,
        )

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.arch_name.normalize(deep)
        new_kid: list[AstNode] = [self.arch_type, self.arch_name]
        self.set_kids(nodes=new_kid)
        return res


class EdgeRefTrailer(Expr):
    """EdgeRefTrailer node type for Jac Ast."""

    def __init__(
        self,
        chain: list[Expr | FilterCompr],
        edges_only: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize edge reference trailer expression node."""
        self.chain = chain
        self.edges_only = edges_only
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self)

    def normalize(self, deep: bool = True) -> bool:
        """Normalize ast node."""
        res = True
        for expr in self.chain:
            res = res and expr.normalize(deep)
        new_kid: list[AstNode] = []
        if self.edges_only:
            new_kid.append(self.gen_token(Tok.EDGE_OP))
        new_kid.append(self.gen_token(Tok.LSQUARE))
        new_kid.extend(self.chain)
        new_kid.append(self.gen_token(Tok.RSQUARE))
        self.set_kids(nodes=new_kid)
        return res


class EdgeOpRef(WalkerStmtOnlyNode, AtomExpr):
    """EdgeOpRef node type for Jac Ast."""

    def __init__(
        self,
        filter_cond: Optional[FilterCompr],
        edge_dir: EdgeDir,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize edge op reference expression node."""
        self.filter_cond = filter_cond
        self.edge_dir = edge_dir
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self)
        WalkerStmtOnlyNode.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.SEQUENCE)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.filter_cond.normalize(deep) if self.filter_cond else res
        new_kid: list[AstNode] = []
        if self.edge_dir == EdgeDir.IN:
            if not self.filter_cond:
                new_kid.append(self.gen_token(Tok.ARROW_L))
            else:
                new_kid.append(self.gen_token(Tok.ARROW_L_P1))
                new_kid.append(self.filter_cond)
                new_kid.append(self.gen_token(Tok.ARROW_L_P2))
        elif self.edge_dir == EdgeDir.OUT:
            if not self.filter_cond:
                new_kid.append(self.gen_token(Tok.ARROW_R))
            else:
                new_kid.append(self.gen_token(Tok.ARROW_R_P1))
                new_kid.append(self.filter_cond)
                new_kid.append(self.gen_token(Tok.ARROW_R_P2))
        else:
            if not self.filter_cond:
                new_kid.append(self.gen_token(Tok.ARROW_BI))
            else:
                new_kid.append(self.gen_token(Tok.ARROW_L_P1))
                new_kid.append(self.filter_cond)
                new_kid.append(self.gen_token(Tok.ARROW_R_P2))
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.edge_spec.normalize(deep)
        new_kid: list[AstNode] = [self.gen_token(Tok.KW_DELETE), self.edge_spec]
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.conn_type.normalize(deep) if self.conn_type else res
            res = res and self.conn_assign.normalize(deep) if self.conn_assign else res
        new_kid: list[AstNode] = []
        if self.edge_dir == EdgeDir.IN:
            if not self.conn_assign and not self.conn_type:
                new_kid.append(self.gen_token(Tok.CARROW_L))
            else:
                new_kid.append(self.gen_token(Tok.CARROW_L_P1))
                if self.conn_type:
                    new_kid.append(self.conn_type)
                if self.conn_assign:
                    new_kid.append(self.gen_token(Tok.COLON))
                    new_kid.append(self.conn_assign)
                new_kid.append(self.gen_token(Tok.CARROW_L_P2))
        elif self.edge_dir == EdgeDir.OUT:
            if not self.conn_assign and not self.conn_type:
                new_kid.append(self.gen_token(Tok.CARROW_R))
            else:
                new_kid.append(self.gen_token(Tok.CARROW_R_P1))
                if self.conn_type:
                    new_kid.append(self.conn_type)
                if self.conn_assign:
                    new_kid.append(self.gen_token(Tok.COLON))
                    new_kid.append(self.conn_assign)
                new_kid.append(self.gen_token(Tok.CARROW_R_P2))
        else:
            if not self.conn_assign and not self.conn_type:
                new_kid.append(self.gen_token(Tok.CARROW_BI))
            else:
                new_kid.append(self.gen_token(Tok.CARROW_L_P1))
                if self.conn_type:
                    new_kid.append(self.conn_type)
                if self.conn_assign:
                    new_kid.append(self.gen_token(Tok.COLON))
                    new_kid.append(self.conn_assign)
                new_kid.append(self.gen_token(Tok.CARROW_R_P2))
        self.set_kids(nodes=new_kid)
        return res


class FilterCompr(AtomExpr):
    """FilterCtx node type for Jac Ast."""

    def __init__(
        self,
        f_type: Optional[Expr],
        compares: Optional[SubNodeList[CompareExpr]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize filter_cond context expression node."""
        self.f_type = f_type
        self.compares = compares
        AstNode.__init__(self, kid=kid)
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.SEQUENCE)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.f_type.normalize(deep) if self.f_type else res
            res = res and self.compares.normalize(deep) if self.compares else res
        new_kid: list[AstNode] = []
        if not isinstance(self.parent, EdgeOpRef):
            new_kid.append(self.gen_token(Tok.LPAREN))
            if self.f_type:
                new_kid.append(self.gen_token(Tok.TYPE_OP))
            new_kid.append(self.gen_token(Tok.NULL_OK))
        if self.f_type:
            new_kid.append(self.f_type)
        if self.compares:
            if self.f_type:
                new_kid.append(self.gen_token(Tok.COLON))
            new_kid.append(self.compares)
        if not isinstance(self.parent, EdgeOpRef):
            new_kid.append(self.gen_token(Tok.RPAREN))
        self.set_kids(nodes=new_kid)
        return res


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
        Expr.__init__(self)
        AstSymbolStubNode.__init__(self, sym_type=SymbolType.SEQUENCE)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize ast node."""
        res = True
        if deep:
            res = self.assigns.normalize(deep)
        new_kid: list[AstNode] = []
        if isinstance(self.parent, ConnectOp):
            new_kid.append(self.assigns)
        else:
            new_kid.append(self.gen_token(Tok.LPAREN))
            new_kid.append(self.gen_token(Tok.EQ))
            new_kid.append(self.assigns)
            new_kid.append(self.gen_token(Tok.RPAREN))
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match statement node."""
        res = True
        if deep:
            res = self.target.normalize(deep)
            for case in self.cases:
                res = res and case.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.KW_MATCH),
            self.target,
        ]
        new_kid.append(self.gen_token(Tok.LBRACE))
        for case in self.cases:
            new_kid.append(case)
        new_kid.append(self.gen_token(Tok.RBRACE))

        self.set_kids(nodes=new_kid)
        return res


class MatchCase(AstNode):
    """MatchCase node type for Jac Ast."""

    def __init__(
        self,
        pattern: MatchPattern,
        guard: Optional[Expr],
        body: list[CodeBlockStmt],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match case node."""
        self.pattern = pattern
        self.guard = guard
        self.body = body
        AstNode.__init__(self, kid=kid)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match case node."""
        res = True
        if deep:
            res = self.pattern.normalize(deep)
            res = res and self.guard.normalize(deep) if self.guard else res
            for stmt in self.body:
                res = res and stmt.normalize(deep)
        new_kid: list[AstNode] = [self.gen_token(Tok.KW_CASE), self.pattern]
        if self.guard:
            new_kid.append(self.gen_token(Tok.KW_IF))
            new_kid.append(self.guard)
        new_kid.append(self.gen_token(Tok.COLON))
        if self.body:
            new_kid.extend([*self.body])
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match or node."""
        res = True
        if deep:
            for pattern in self.patterns:
                res = res and pattern.normalize(deep)
        new_kid: list[AstNode] = []
        for pattern in self.patterns:
            new_kid.append(pattern)
            new_kid.append(self.gen_token(Tok.KW_OR))
        new_kid.pop()
        self.set_kids(nodes=new_kid)
        return res


class MatchAs(MatchPattern):
    """MatchAs node type for Jac Ast."""

    def __init__(
        self,
        name: NameAtom,
        pattern: Optional[MatchPattern],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match as node."""
        self.name = name
        self.pattern = pattern
        AstNode.__init__(self, kid=kid)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match as node."""
        res = True
        if deep:
            res = self.name.normalize(deep)
            res = res and self.pattern.normalize(deep) if self.pattern else res
        new_kid: list[AstNode] = []
        if self.pattern:
            new_kid.append(self.pattern)
            new_kid.append(self.gen_token(Tok.KW_AS))
        new_kid.append(self.name)
        self.set_kids(nodes=new_kid)
        return res


class MatchWild(MatchPattern):
    """Match wild card node type for Jac Ast."""

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match wild card node."""
        AstNode.set_kids(
            self,
            nodes=[
                Name(
                    orig_src=self.loc.orig_src,
                    name=Tok.NAME,
                    value="_",
                    col_start=self.loc.col_start,
                    col_end=self.loc.col_end,
                    line=self.loc.first_line,
                    end_line=self.loc.last_line,
                    pos_start=self.loc.pos_start,
                    pos_end=self.loc.pos_end,
                )
            ],
        )
        return True


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match value node."""
        res = True
        if deep:
            res = self.value.normalize(deep)
        self.set_kids(nodes=[self.value])
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match singleton node."""
        res = True
        self.set_kids(nodes=[self.value])
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match sequence node."""
        res = True
        if deep:
            for value in self.values:
                res = res and value.normalize(deep)
        new_kid: list[AstNode] = [self.gen_token(Tok.LSQUARE)]
        for value in self.values:
            new_kid.append(value)
            new_kid.append(self.gen_token(Tok.COMMA))
        new_kid.pop()
        new_kid.append(self.gen_token(Tok.RSQUARE))
        self.set_kids(nodes=new_kid)
        return res


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

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match mapping node."""
        res = True
        if deep:
            for value in self.values:
                res = res and value.normalize(deep)
        new_kid: list[AstNode] = [self.gen_token(Tok.LBRACE)]
        for value in self.values:
            new_kid.append(value)
            new_kid.append(self.gen_token(Tok.COMMA))
        new_kid.pop()
        new_kid.append(self.gen_token(Tok.RBRACE))
        self.set_kids(nodes=new_kid)
        return res


class MatchKVPair(MatchPattern):
    """MatchKVPair node type for Jac Ast."""

    def __init__(
        self,
        key: MatchPattern | NameAtom,
        value: MatchPattern,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match key value pair node."""
        self.key = key
        self.value = value
        AstNode.__init__(self, kid=kid)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match key value pair node."""
        res = True
        if deep:
            res = (
                self.key.normalize(deep) if isinstance(self.key, MatchPattern) else True
            )
            res = res and self.value.normalize(deep)
        op = Tok.EQ if isinstance(self.key, Name) else Tok.COLON
        new_kid: list[AstNode] = [self.key, self.gen_token(op), self.value]
        self.set_kids(nodes=new_kid)
        return res


class MatchStar(MatchPattern):
    """MatchStar node type for Jac Ast."""

    def __init__(
        self,
        name: NameAtom,
        is_list: bool,
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match star node."""
        self.name = name
        self.is_list = is_list
        AstNode.__init__(self, kid=kid)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match star node."""
        res = True
        if deep:
            res = self.name.normalize(deep)
        new_kid: list[AstNode] = [
            self.gen_token(Tok.STAR_MUL if self.is_list else Tok.STAR_POW)
        ]
        new_kid.append(self.name)
        self.set_kids(nodes=new_kid)
        return res


class MatchArch(MatchPattern):
    """MatchClass node type for Jac Ast."""

    def __init__(
        self,
        name: AtomTrailer | NameAtom,
        arg_patterns: Optional[SubNodeList[MatchPattern]],
        kw_patterns: Optional[SubNodeList[MatchKVPair]],
        kid: Sequence[AstNode],
    ) -> None:
        """Initialize match class node."""
        self.name = name
        self.arg_patterns = arg_patterns
        self.kw_patterns = kw_patterns
        AstNode.__init__(self, kid=kid)

    def normalize(self, deep: bool = False) -> bool:
        """Normalize match class node."""
        res = True
        if deep:
            res = self.name.normalize(deep)
            res = res and (not self.arg_patterns or self.arg_patterns.normalize(deep))
            res = res and (not self.kw_patterns or self.kw_patterns.normalize(deep))
        new_kid: list[AstNode] = [self.name]
        new_kid.append(self.gen_token(Tok.LPAREN))
        if self.arg_patterns:
            new_kid.append(self.arg_patterns)
            new_kid.append(self.gen_token(Tok.COMMA))
        if self.kw_patterns:
            new_kid.append(self.kw_patterns)
        else:
            new_kid.pop()
        new_kid.append(self.gen_token(Tok.RPAREN))
        self.set_kids(nodes=new_kid)
        return res


# AST Terminal Node Types
# --------------------------
class Token(AstNode):
    """Token node type for Jac Ast."""

    def __init__(
        self,
        orig_src: JacSource,
        name: str,
        value: str,
        line: int,
        end_line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
    ) -> None:
        """Initialize token."""
        self.orig_src = orig_src
        self.name = name
        self.value = value
        self.line_no = line
        self.end_line = end_line
        self.c_start = col_start
        self.c_end = col_end
        self.pos_start = pos_start
        self.pos_end = pos_end
        AstNode.__init__(self, kid=[])

    def normalize(self, deep: bool = True) -> bool:
        """Normalize token."""
        return bool(self.value and self.name)

    def unparse(self) -> str:
        """Unparse token."""
        return self.value


class Name(Token, NameAtom):
    """Name node type for Jac Ast."""

    def __init__(
        self,
        orig_src: JacSource,
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
    ) -> None:
        """Initialize token."""
        self.is_enum_singleton = is_enum_singleton
        self.is_kwesc = is_kwesc
        Token.__init__(
            self,
            orig_src=orig_src,
            name=name,
            value=value,
            line=line,
            end_line=end_line,
            col_start=col_start,
            col_end=col_end,
            pos_start=pos_start,
            pos_end=pos_end,
        )
        NameAtom.__init__(self)
        AstSymbolNode.__init__(
            self,
            sym_name=value,
            name_spec=self,
            sym_category=SymbolType.VAR,
        )

    def unparse(self) -> str:
        """Unparse name."""
        super().unparse()
        return (f"<>{self.value}" if self.is_kwesc else self.value) + (
            ",\n" if self.is_enum_singleton else ""
        )

    @staticmethod
    def gen_stub_from_node(
        node: AstSymbolNode, name_str: str, set_name_of: Optional[AstSymbolNode] = None
    ) -> Name:
        """Generate name from node."""
        ret = Name(
            orig_src=node.loc.orig_src,
            name=Tok.NAME.value,
            value=name_str,
            col_start=node.loc.col_start,
            col_end=node.loc.col_end,
            line=node.loc.first_line,
            end_line=node.loc.last_line,
            pos_start=node.loc.pos_start,
            pos_end=node.loc.pos_end,
        )
        ret.name_of = set_name_of if set_name_of else ret
        if node._sym_tab:
            ret.sym_tab = node.sym_tab
        return ret


class SpecialVarRef(Name):
    """HereRef node type for Jac Ast."""

    def __init__(
        self,
        var: Name,
    ) -> None:
        """Initialize special var reference expression node."""
        self.orig = var
        Name.__init__(
            self,
            orig_src=var.orig_src,
            name=var.name,
            value=self.py_resolve_name(),  # TODO: This shouldnt be necessary
            line=var.line_no,
            end_line=var.end_line,
            col_start=var.c_start,
            col_end=var.c_end,
            pos_start=var.pos_start,
            pos_end=var.pos_end,
        )
        NameAtom.__init__(self)
        AstSymbolNode.__init__(
            self,
            sym_name=self.py_resolve_name(),
            name_spec=self,
            sym_category=SymbolType.VAR,
        )

    def py_resolve_name(self) -> str:
        """Resolve name."""
        if self.orig.name == Tok.KW_SELF:
            return "self"
        elif self.orig.name == Tok.KW_SUPER:
            return "super"
        elif self.orig.name == Tok.KW_ROOT:
            return Con.ROOT.value
        elif self.orig.name == Tok.KW_HERE:
            return Con.HERE.value
        elif self.orig.name == Tok.KW_INIT:
            return "__init__"
        elif self.orig.name == Tok.KW_POST_INIT:
            return "__post_init__"
        else:
            raise NotImplementedError("ICE: Special var reference not implemented")


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
        orig_src: JacSource,
        name: str,
        value: str,
        line: int,
        end_line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
    ) -> None:
        """Initialize token."""
        Token.__init__(
            self,
            orig_src=orig_src,
            name=name,
            value=value,
            line=line,
            end_line=end_line,
            col_start=col_start,
            col_end=col_end,
            pos_start=pos_start,
            pos_end=pos_end,
        )
        AstSymbolStubNode.__init__(self, sym_type=self.SYMBOL_TYPE)
        Expr.__init__(self)

    @property
    def lit_value(
        self,
    ) -> int | str | float | bool | None | Callable[[], Any] | EllipsisType:
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
        if isinstance(self.value, bytes):
            return self.value
        if any(
            self.value.startswith(prefix)
            and self.value[len(prefix) :].startswith(("'", '"'))
            for prefix in ["r", "b", "br", "rb"]
        ):
            return eval(self.value)

        elif self.value.startswith(("'", '"')):
            repr_str = self.value.encode().decode("unicode_escape")
            if (
                (self.value.startswith('"""') and self.value.endswith('"""'))
                or (self.value.startswith("'''") and self.value.endswith("'''"))
            ) and not self.find_parent_of_type(FString):
                return repr_str[3:-3]
            if (not self.find_parent_of_type(FString)) or (
                not (
                    self.parent
                    and isinstance(self.parent, SubNodeList)
                    and self.parent.parent
                    and isinstance(self.parent.parent, FString)
                )
            ):
                return repr_str[1:-1]
            return repr_str
        else:
            return self.value

    def normalize(self, deep: bool = True) -> bool:
        """Normalize string."""
        self.value = r"%s" % self.value
        return True

    def unparse(self) -> str:
        """Unparse string."""
        super().unparse()
        return repr(self.value)


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


class Ellipsis(Literal):
    """Ellipsis node type for Jac Ast."""

    SYMBOL_TYPE = SymbolType.NULL

    @property
    def lit_value(self) -> EllipsisType:
        """Return literal value in its python type."""
        return ...


class EmptyToken(Token):
    """EmptyToken node type for Jac Ast."""

    def __init__(self, orig_src: JacSource | None = None) -> None:
        """Initialize empty token."""
        super().__init__(
            name="EmptyToken",
            orig_src=orig_src or JacSource("", ""),
            value="",
            line=0,
            end_line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
        )


class Semi(Token, CodeBlockStmt):
    """Semicolon node type for Jac Ast."""


class CommentToken(Token):
    """CommentToken node type for Jac Ast."""

    def __init__(
        self,
        orig_src: JacSource,
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
    ) -> None:
        """Initialize token."""
        self.is_inline = is_inline

        Token.__init__(
            self,
            orig_src=orig_src,
            name=name,
            value=value,
            line=line,
            end_line=end_line,
            col_start=col_start,
            col_end=col_end,
            pos_start=pos_start,
            pos_end=pos_end,
        )

        AstNode.__init__(self, kid=kid)


# ----------------
class JacSource(EmptyToken):
    """SourceString node type for Jac Ast."""

    def __init__(self, source: str, mod_path: str) -> None:
        """Initialize source string."""
        super().__init__(self)
        self.value = source
        self.hash = md5(source.encode()).hexdigest()
        self.file_path = mod_path
        self.comments: list[CommentToken] = []

    @property
    def code(self) -> str:
        """Return code."""
        return self.value


class PythonModuleAst(EmptyToken):
    """SourceString node type for Jac Ast."""

    def __init__(self, ast: ast3.Module, orig_src: JacSource) -> None:
        """Initialize source string."""
        super().__init__()
        self.ast = ast
        self.orig_src = orig_src

        # This bellow attribute is un-necessary since it already exists in the orig_src
        # however I'm keeping it here not to break existing code trying to access file_path.
        # We can remove this in the future once we safley remove all references to it and
        # use orig_src.
        self.file_path = orig_src.file_path

"""Abstract class for IR Passes for Jac."""
from __future__ import annotations

import pprint
from typing import Optional, Union

from jaclang.jac.constant import Constants as Con, EdgeDir
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.symtable import SymbolTable


class AstNode:
    """Abstract syntax tree node for Jac."""

    def __init__(
        self,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list,
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize ast."""
        self.parent = parent
        self.kid = kid if kid else []
        self.mod_link = mod_link
        self.line = line
        self.sym_tab = sym_tab
        self._sub_node_tab: dict[type[AstNode], list[AstNode]] = {}
        self._typ: type = type(None)
        self.meta: dict = {}

    def to_dict(self) -> dict:
        """Return dict representation of node."""
        ret = {
            "node": str(type(self).__name__),
            "kid": [x.to_dict() for x in self.kid if x],
            "line": self.line,
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
        doc: Token,
        body: Optional["Elements"],
        mod_path: str,
        rel_mod_path: str,
        is_imported: bool,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize whole program node."""
        self.name = name
        self.doc = doc
        self.body = body
        self.mod_path = mod_path
        self.rel_mod_path = rel_mod_path
        self.is_imported = is_imported
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class Elements(AstNode):
    """Elements node type for Jac Ast."""

    def __init__(
        self,
        elements: list[GlobalVars | Test | ModuleCode | Import | Architype | Ability],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize elements node."""
        self.elements = elements
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class OOPAccessNode(AstNode):
    """OOPAccessNode node type for Jac Ast."""

    def __init__(
        self,
        access: Optional[Token],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize OOPAccessible node."""
        self.access = access
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class GlobalVars(OOPAccessNode):
    """GlobalVars node type for Jac Ast."""

    def __init__(
        self,
        doc: Optional["Token"],
        access: Optional[Token],
        assignments: "AssignmentList",
        is_frozen: bool,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize global var node."""
        self.doc = doc
        self.assignments = assignments
        self.is_frozen = is_frozen
        super().__init__(
            access=access,
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
        )


class Test(AstNode):
    """Test node type for Jac Ast."""

    TEST_COUNT = 0

    def __init__(
        self,
        name: Name | Token,
        doc: Optional[Token],
        body: CodeBlock,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
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
                line=name.line,
                already_declared=False,
                parent=name.parent,
                mod_link=name.mod_link,
                kid=name.kid,
                sym_tab=name.sym_tab,
            )
        )
        kid[0] = self.name  # Index is 0 since Doc string is inserted after init
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ModuleCode(AstNode):
    """Free mod code for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Token],
        name: Optional[Name],
        body: CodeBlock,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize test node."""
        self.doc = doc
        self.name = name
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class PyInlineCode(AstNode):
    """Inline Python code node type for Jac Ast."""

    def __init__(
        self,
        code: Token,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
    ) -> None:
        """Initialize inline python code node."""
        self.code = code
        super().__init__(parent=parent, mod_link=mod_link, kid=kid, line=line)


class Import(AstNode):
    """Import node type for Jac Ast."""

    def __init__(
        self,
        lang: Name,
        path: ModulePath,
        alias: Optional[Name],
        items: Optional[ModuleItems],
        is_absorb: bool,  # For includes
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
        sub_module: Optional["Module"] = None,
    ) -> None:
        """Initialize import node."""
        self.lang = lang
        self.path = path
        self.alias = alias
        self.items = items
        self.is_absorb = is_absorb
        self.sub_module = sub_module

        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ModulePath(AstNode):
    """ModulePath node type for Jac Ast."""

    def __init__(
        self,
        path: list[Name],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize module path node."""
        self.path = path
        self.path_str = "".join([p.value for p in path])
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ModuleItems(AstNode):
    """ModuleItems node type for Jac Ast."""

    def __init__(
        self,
        items: list[ModuleItem],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[ModuleItem],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize module items node."""
        self.items = items
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ModuleItem(AstNode):
    """ModuleItem node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        alias: Optional[Token],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
        body: Optional[AstNode] = None,
    ) -> None:
        """Initialize module item node."""
        self.name = name
        self.alias = alias
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class Architype(OOPAccessNode):
    """ObjectArch node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        arch_type: Token,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: BaseClasses,
        body: Optional[ArchBlock],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize object arch node."""
        self.name = name
        self.arch_type = arch_type
        self.doc = doc
        self.decorators = decorators
        self.base_classes = base_classes
        self.body = body
        super().__init__(
            access=access,
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
        )


class ArchDef(AstNode):
    """ArchDef node type for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Token],
        target: ArchRefChain,
        body: ArchBlock,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize arch def node."""
        self.doc = doc
        self.target = target
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class Decorators(AstNode):
    """Decorators node type for Jac Ast."""

    def __init__(
        self,
        calls: list[ExprType],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize decorators node."""
        self.calls = calls
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class BaseClasses(AstNode):
    """BaseArch node type for Jac Ast."""

    def __init__(
        self,
        base_classes: list[DottedNameList],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize base classes node."""
        self.base_classes = base_classes
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class Ability(OOPAccessNode):
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
        access: Optional[Token],
        signature: Optional[FuncSignature | TypeSpec | EventSignature],
        body: Optional[CodeBlock],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
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
        super().__init__(
            access=access,
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
        )

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
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize ability def node."""
        self.doc = doc
        self.target = target
        self.signature = signature
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class EventSignature(AstNode):
    """EventSignature node type for Jac Ast."""

    def __init__(
        self,
        event: Token,
        arch_tag_info: Optional[TypeSpecList],
        return_type: Optional["TypeSpec"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize event signature node."""
        self.event = event
        self.arch_tag_info = arch_tag_info
        self.return_type = return_type
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class DottedNameList(AstNode):
    """DottedNameList node type for Jac Ast."""

    def __init__(
        self,
        names: list[Token | SpecialVarRef | Name],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize name list node."""
        self.names = names
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ArchRefChain(AstNode):
    """Arch ref list node type for Jac Ast."""

    def __init__(
        self,
        archs: list[ArchRef],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize name list ."""
        self.archs = archs
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )

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
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize method signature node."""
        self.params = params
        self.return_type = return_type
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class FuncParams(AstNode):
    """ArchBlock node type for Jac Ast."""

    def __init__(
        self,
        params: list["ParamVar"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize method params node."""
        self.params = params
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ParamVar(AstNode):
    """ParamVar node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        unpack: Optional[Token],
        type_tag: "TypeSpec",
        value: Optional[ExprType],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize param var node."""
        self.name = name
        self.unpack = unpack
        self.type_tag = type_tag
        self.value = value
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class Enum(OOPAccessNode):
    """Enum node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: "BaseClasses",
        body: Optional["EnumBlock"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize object arch node."""
        self.name = name
        self.doc = doc
        self.decorators = decorators
        self.base_classes = base_classes
        self.body = body
        super().__init__(
            access=access,
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
        )


class EnumDef(AstNode):
    """EnumDef node type for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Token],
        target: ArchRefChain,
        body: EnumBlock,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize arch def node."""
        self.doc = doc
        self.target = target
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class EnumBlock(AstNode):
    """EnumBlock node type for Jac Ast."""

    def __init__(
        self,
        stmts: list["Name|Assignment"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize enum block node."""
        self.stmts = stmts
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ArchBlock(AstNode):
    """ArchBlock node type for Jac Ast."""

    def __init__(
        self,
        members: list[ArchHas | Ability],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize arch block node."""
        self.members = members
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ArchHas(OOPAccessNode):
    """HasStmt node type for Jac Ast."""

    def __init__(
        self,
        doc: Optional[Token],
        is_static: bool,
        access: Optional[Token],
        vars: HasVarList,
        is_frozen: bool,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize has statement node."""
        self.doc = doc
        self.is_static = is_static
        self.vars = vars
        self.is_frozen = is_frozen
        super().__init__(
            access=access,
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
        )


class HasVarList(AstNode):
    """HasVarList node type for Jac Ast."""

    def __init__(
        self,
        vars: list["HasVar"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize has var list node."""
        self.vars = vars
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class HasVar(AstNode):
    """HasVar node type for Jac Ast."""

    def __init__(
        self,
        name: Name,
        type_tag: "TypeSpec",
        value: Optional[ExprType],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize has var node."""
        self.name = name
        self.type_tag = type_tag
        self.value = value
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class TypeSpecList(AstNode):
    """TypeSpecList node type for Jac Ast."""

    def __init__(
        self,
        types: list[TypeSpec],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize type list node."""
        self.types = types
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class TypeSpec(AstNode):
    """TypeSpec node type for Jac Ast."""

    def __init__(
        self,
        spec_type: Token | DottedNameList,
        list_nest: TypeSpec,  # needed for lists
        dict_nest: TypeSpec,  # needed for dicts, uses list_nest as key
        null_ok: bool,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize type spec node."""
        self.spec_type = spec_type
        self.list_nest = list_nest
        self.dict_nest = dict_nest
        self.null_ok = null_ok
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class CodeBlock(AstNode):
    """CodeBlock node type for Jac Ast."""

    def __init__(
        self,
        stmts: list[StmtType],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize code block node."""
        self.stmts = stmts
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class TypedCtxBlock(AstNode):
    """TypedCtxBlock node type for Jac Ast."""

    def __init__(
        self,
        type_ctx: TypeSpecList,
        body: CodeBlock,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize typed context block node."""
        self.type_ctx = type_ctx
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class IfStmt(AstNode):
    """IfStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: ExprType,
        body: "CodeBlock",
        elseifs: Optional["ElseIfs"],
        else_body: Optional["ElseStmt"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize if statement node."""
        self.condition = condition
        self.body = body
        self.elseifs = elseifs
        self.else_body = else_body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ElseIfs(AstNode):
    """ElseIfs node type for Jac Ast."""

    def __init__(
        self,
        elseifs: list["IfStmt"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list["IfStmt"],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize elseifs node."""
        self.elseifs = elseifs
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ElseStmt(AstNode):
    """Else node type for Jac Ast."""

    def __init__(
        self,
        body: "CodeBlock",
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize else node."""
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class TryStmt(AstNode):
    """TryStmt node type for Jac Ast."""

    def __init__(
        self,
        body: "CodeBlock",
        excepts: Optional["ExceptList"],
        finally_body: Optional["FinallyStmt"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize try statement node."""
        self.body = body
        self.excepts = excepts
        self.finally_body = finally_body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ExceptList(AstNode):
    """ExceptList node type for Jac Ast."""

    def __init__(
        self,
        excepts: list["Except"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize excepts node."""
        self.excepts = excepts
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class Except(AstNode):
    """Except node type for Jac Ast."""

    def __init__(
        self,
        ex_type: ExprType,
        name: Optional[Token],
        body: "CodeBlock",
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize except node."""
        self.ex_type = ex_type
        self.name = name
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class FinallyStmt(AstNode):
    """FinallyStmt node type for Jac Ast."""

    def __init__(
        self,
        body: "CodeBlock",
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize finally statement node."""
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class IterForStmt(AstNode):
    """IterFor node type for Jac Ast."""

    def __init__(
        self,
        iter: Assignment,
        condition: ExprType,
        count_by: ExprType,
        body: CodeBlock,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize iter for node."""
        self.iter = iter
        self.condition = condition
        self.count_by = count_by
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class InForStmt(AstNode):
    """InFor node type for Jac Ast."""

    def __init__(
        self,
        name_list: NameList,
        collection: ExprType,
        body: CodeBlock,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize in for node."""
        self.name_list = name_list
        self.collection = collection
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class NameList(AstNode):
    """NameList node type for Jac Ast."""

    def __init__(
        self,
        names: list[Name],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize name list node."""
        self.names = names
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class WhileStmt(AstNode):
    """WhileStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: ExprType,
        body: "CodeBlock",
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize while statement node."""
        self.condition = condition
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class WithStmt(AstNode):
    """WithStmt node type for Jac Ast."""

    def __init__(
        self,
        exprs: "ExprAsItemList",
        body: "CodeBlock",
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize with statement node."""
        self.exprs = exprs
        self.body = body
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ExprAsItemList(AstNode):
    """ExprAsItemList node type for Jac Ast."""

    def __init__(
        self,
        items: list["ExprAsItem"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list["ExprAsItem"],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize module items node."""
        self.items = items
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ExprAsItem(AstNode):
    """ExprAsItem node type for Jac Ast."""

    def __init__(
        self,
        expr: ExprType,
        alias: Optional[Name],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize module item node."""
        self.expr = expr
        self.alias = alias
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class RaiseStmt(AstNode):
    """RaiseStmt node type for Jac Ast."""

    def __init__(
        self,
        cause: Optional[ExprType],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize raise statement node."""
        self.cause = cause
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class AssertStmt(AstNode):
    """AssertStmt node type for Jac Ast."""

    def __init__(
        self,
        condition: ExprType,
        error_msg: Optional[ExprType],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize assert statement node."""
        self.condition = condition
        self.error_msg = error_msg
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class CtrlStmt(AstNode):
    """CtrlStmt node type for Jac Ast."""

    def __init__(
        self,
        ctrl: Token,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize control statement node."""
        self.ctrl = ctrl
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class DeleteStmt(AstNode):
    """DeleteStmt node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize delete statement node."""
        self.target = target
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ReportStmt(AstNode):
    """ReportStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: ExprType,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize report statement node."""
        self.expr = expr
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ReturnStmt(AstNode):
    """ReturnStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: Optional[ExprType],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize return statement node."""
        self.expr = expr
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class YieldStmt(AstNode):
    """YieldStmt node type for Jac Ast."""

    def __init__(
        self,
        expr: Optional[ExprType],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize yeild statement node."""
        self.expr = expr
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class IgnoreStmt(AstNode):
    """IgnoreStmt node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize ignore statement node."""
        self.target = target
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class WalkerStmtOnlyNode(AstNode):
    """WalkerStmtOnlyNode node type for Jac Ast."""

    def __init__(
        self,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
        from_walker: bool = False,
    ) -> None:
        """Initialize walker statement only node."""
        self.from_walker = from_walker
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class VisitStmt(WalkerStmtOnlyNode):
    """VisitStmt node type for Jac Ast."""

    def __init__(
        self,
        vis_type: Optional[Token],
        target: ExprType,
        else_body: Optional["ElseStmt"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
        from_walker: bool = False,
    ) -> None:
        """Initialize visit statement node."""
        self.vis_type = vis_type
        self.target = target
        self.else_body = else_body
        super().__init__(
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
            from_walker=from_walker,
        )


class RevisitStmt(WalkerStmtOnlyNode):
    """ReVisitStmt node type for Jac Ast."""

    def __init__(
        self,
        hops: Optional[ExprType],
        else_body: Optional["ElseStmt"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
        from_walker: bool = False,
    ) -> None:
        """Initialize revisit statement node."""
        self.hops = hops
        self.else_body = else_body
        super().__init__(
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
            from_walker=from_walker,
        )


class DisengageStmt(WalkerStmtOnlyNode):
    """DisengageStmt node type for Jac Ast."""

    def __init__(
        self,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
        from_walker: bool = False,
    ) -> None:
        """Initialize disengage statement node."""
        super().__init__(
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
            from_walker=from_walker,
        )


class AwaitStmt(AstNode):
    """AwaitStmt node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize sync statement node."""
        self.target = target
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class Assignment(AstNode):
    """Assignment node type for Jac Ast."""

    def __init__(
        self,
        is_static: bool,
        target: AtomType,
        value: ExprType,
        mutable: bool,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize assignment node."""
        self.is_static = is_static
        self.target = target
        self.value = value
        self.mutable = mutable
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class BinaryExpr(AstNode):
    """ExprBinary node type for Jac Ast."""

    def __init__(
        self,
        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize binary expression node."""
        self.left = left
        self.right = right
        self.op = op
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class IfElseExpr(AstNode):
    """ExprIfElse node type for Jac Ast."""

    def __init__(
        self,
        condition: "BinaryExpr | IfElseExpr",
        value: ExprType,
        else_value: ExprType,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize if else expression node."""
        self.condition = condition
        self.value = value
        self.else_value = else_value
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class UnaryExpr(AstNode):
    """ExprUnary node type for Jac Ast."""

    def __init__(
        self,
        operand: ExprType,
        op: Token,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize unary expression node."""
        self.operand = operand
        self.op = op
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class UnpackExpr(AstNode):
    """ExprUnpack node type for Jac Ast."""

    def __init__(
        self,
        target: ExprType,
        is_dict: bool,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize unpack expression node."""
        self.target = target
        self.is_dict = is_dict
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class MultiString(AstNode):
    """ExprMultiString node type for Jac Ast."""

    def __init__(
        self,
        strings: list["Token | FString"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize multi string expression node."""
        self.strings = strings
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ExprList(AstNode):
    """ExprList node type for Jac Ast."""

    def __init__(
        self,
        values: list[ExprType],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize expr value node."""
        self.values = values
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


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
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize tuple value node."""
        self.first_expr = first_expr
        self.exprs = exprs
        self.assigns = assigns
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class DictVal(AstNode):
    """ExprDict node type for Jac Ast."""

    def __init__(
        self,
        kv_pairs: list["KVPair"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize dict expression node."""
        self.kv_pairs = kv_pairs
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


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
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize comprehension expression node."""
        self.out_expr = out_expr
        self.name_list = name_list
        self.collection = collection
        self.conditional = conditional
        self.is_list = is_list
        self.is_gen = is_gen
        self.is_set = is_set

        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class DictCompr(AstNode):
    """DictCompr node type for Jac Ast."""

    def __init__(
        self,
        outk_expr: ExprType,
        outv_expr: ExprType,
        name_list: NameList,
        collection: ExprType,
        conditional: Optional[ExprType],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize comprehension expression node."""
        self.outk_expr = outk_expr
        self.outv_expr = outv_expr
        self.name_list = name_list
        self.collection = collection
        self.conditional = conditional
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class KVPair(AstNode):
    """ExprKVPair node type for Jac Ast."""

    def __init__(
        self,
        key: ExprType,
        value: ExprType,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize key value pair expression node."""
        self.key = key
        self.value = value
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class AtomTrailer(AstNode):
    """AtomTrailer node type for Jac Ast."""

    def __init__(
        self,
        target: AtomType,
        right: IndexSlice | ArchRef | Token,
        null_ok: bool,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize atom trailer expression node."""
        self.target = target
        self.right = right
        self.null_ok = null_ok
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class FuncCall(AstNode):
    """FuncCall node type for Jac Ast."""

    def __init__(
        self,
        target: "AtomType",
        params: Optional["ParamList"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize function call expression node."""
        self.target = target
        self.params = params
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ParamList(AstNode):
    """ParamList node type for Jac Ast."""

    def __init__(
        self,
        p_args: Optional[ExprList],
        p_kwargs: Optional["AssignmentList"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize parameter list expression node."""
        self.p_args = p_args
        self.p_kwargs = p_kwargs
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class AssignmentList(AstNode):
    """AssignmentList node type for Jac Ast."""

    def __init__(
        self,
        values: list["Assignment"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize expr value node."""
        self.values = values
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class IndexSlice(AstNode):
    """IndexSlice node type for Jac Ast."""

    def __init__(
        self,
        start: Optional[ExprType],
        stop: Optional[ExprType],
        is_range: bool,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize index slice expression node."""
        self.start = start
        self.stop = stop
        self.is_range = is_range
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class ArchRef(AstNode):
    """GlobalRef node type for Jac Ast."""

    def __init__(
        self,
        name_ref: Name | SpecialVarRef,
        arch: Token,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize global reference expression node."""
        self.name_ref = name_ref
        self.arch = arch
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )

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
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize special var reference expression node."""
        self.var = var
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )

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
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
        from_walker: bool = False,
    ) -> None:
        """Initialize edge op reference expression node."""
        self.filter_type = filter_type
        self.filter_cond = filter_cond
        self.edge_dir = edge_dir
        super().__init__(
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
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
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize connect op reference expression node."""
        self.conn_type = conn_type
        self.conn_assign = conn_assign
        self.edge_dir = edge_dir
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class FilterCompr(AstNode):
    """FilterCtx node type for Jac Ast."""

    def __init__(
        self,
        compares: list[BinaryExpr],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize filter_cond context expression node."""
        self.compares = compares
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class FString(AstNode):
    """FString node type for Jac Ast."""

    def __init__(
        self,
        parts: list["Token | ExprType"],
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize fstring expression node."""
        self.parts = parts
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


# AST Parse-Tree Node Types


# --------------------------
class Parse(AstNode):
    """Parse node type for Jac Ast."""

    def __init__(
        self,
        name: str,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize parse."""
        self.name = name
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )

    def __repr__(self) -> str:
        """Return string representation of parse node."""
        return super().__repr__() + f" ({self.name})" + " line: " + str(self.line)


class Token(AstNode):
    """Token node type for Jac Ast."""

    def __init__(
        self,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize token."""
        self.name = name
        self.value = value
        self.col_start = col_start
        self.col_end = col_end
        super().__init__(
            parent=parent, mod_link=mod_link, kid=kid, line=line, sym_tab=sym_tab
        )


class Name(Token):
    """Name node type for Jac Ast."""

    def __init__(
        self,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        already_declared: bool,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize name."""
        self.already_declared = already_declared
        super().__init__(
            name=name,
            value=value,
            col_start=col_start,
            col_end=col_end,
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
        )


class Constant(Token):
    """Constant node type for Jac Ast."""

    def __init__(
        self,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        typ: type,
        parent: Optional[AstNode],
        mod_link: Optional[Module],
        kid: list[AstNode],
        line: int,
        sym_tab: Optional[SymbolTable] = None,
    ) -> None:
        """Initialize constant."""
        super().__init__(
            name=name,
            value=value,
            col_start=col_start,
            col_end=col_end,
            parent=parent,
            mod_link=mod_link,
            kid=kid,
            line=line,
            sym_tab=sym_tab,
        )
        self._typ = typ


# Aggregate Types
# ----------------


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

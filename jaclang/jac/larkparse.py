"""Lark parser for Jac Lang."""
from __future__ import annotations

import logging
import os

import jaclang.jac.absyntree as ast
from jaclang.jac import jac_lark as jl
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.passes.ir_pass import Pass
from jaclang.vendor.lark import Lark, logger


class JacParser(Pass):
    """Jac Parser."""

    dev_mode = True

    def before_pass(self) -> None:
        """Initialize parser."""
        super().before_pass()
        self.comments = []
        if JacParser.dev_mode:
            JacParser.make_dev()

    def transform(self, ir: ast.SourceString) -> ast.Module:
        """Transform input IR."""
        tree, self.comments = JacParser.parse(ir.value)
        tree = JacParser.TreeToAST(parser=self).transform(tree)
        return tree

    @staticmethod
    def _comment_callback(comment: str) -> None:
        JacParser.comment_cache.append(comment)

    @staticmethod
    def parse(ir: str) -> tuple[jl.Tree, list[str]]:
        """Parse input IR."""
        JacParser.comment_cache = []
        return (
            JacParser.parser.parse(ir),
            JacParser.comment_cache,
        )

    @staticmethod
    def make_dev() -> None:
        """Make parser in dev mode."""
        JacParser.parser = Lark.open(
            "jac.lark",
            parser="lalr",
            rel_to=__file__,
            strict=True,
            debug=True,
            lexer_callbacks={"COMMENT": JacParser._comment_callback},
        )
        logger.setLevel(logging.DEBUG)

    comment_cache = []
    parser = jl.Lark_StandAlone(lexer_callbacks={"COMMENT": _comment_callback})

    class TreeToAST(jl.Transformer):
        """Transform parse tree to AST."""

        def __init__(self, parser: JacParser, *args: bool, **kwargs: bool) -> None:
            """Initialize transformer."""
            super().__init__(*args, **kwargs)
            self.parse_ref = parser

        def ice(self) -> Exception:
            """Raise internal compiler error."""
            self.parse_ref.error("Unexpected item in parse tree!")
            return RuntimeError(
                f"{self.parse_ref.__class__.__name__} - Unexpected item in parse tree!"
            )

        def start(self, kid: list[ast.Module]) -> ast.Module:
            """Grammar rule.

            start: module
            """
            return kid[0]

        def module(self, kid: list[ast.AstNode]) -> ast.AstNode:
            """Grammar rule.

            module: (doc_tag? element (element_with_doc | element)*)?
            doc_tag (element_with_doc (element_with_doc | element)*)?
            """
            doc = kid[0] if len(kid) and isinstance(kid[0], ast.Constant) else None
            body = kid[1:] if doc else kid
            valid_body: list[ast.ElementType] = [
                i for i in body if isinstance(i, ast.ElementType)
            ]
            if len(valid_body) == len(body):
                mod = ast.Module(
                    name=self.parse_ref.mod_path.split(os.path.sep)[-1].split(".")[0],
                    doc=doc,
                    body=valid_body,
                    mod_path=self.parse_ref.mod_path,
                    rel_mod_path=self.parse_ref.rel_mod_path,
                    is_imported=False,
                    mod_link=None,
                    kid=kid,
                )
                self.mod_link = mod
                return mod
            else:
                raise self.ice()

        def element_with_doc(self, kid: list[ast.AstNode]) -> ast.ElementType:
            """Grammar rule.

            element_with_doc: doc_tag element
            """
            if isinstance(kid[1], ast.ElementType) and isinstance(kid[0], ast.Constant):
                kid[1].doc = kid[0]
                kid[1].add_kids_left([kid[0]])
                return kid[1]
            else:
                raise self.ice()

        def element(self, kid: list[ast.AstNode]) -> ast.ElementType:
            """Grammar rule.

            element: py_code_block
                | include_stmt
                | import_stmt
                | ability
                | architype
                | mod_code
                | test
                | global_var
            """
            if isinstance(kid[0], ast.ElementType):
                return kid[0]
            else:
                raise self.ice()

        def global_var(self, kid: list[ast.AstNode]) -> ast.GlobalVars:
            """Grammar rule.

            global_var: (KW_FREEZE | KW_GLOBAL) access_tag? assignment_list SEMI
            """
            is_frozen = isinstance(kid[0], ast.Token) and kid[0].name == Tok.KW_FREEZE
            access = kid[1] if isinstance(kid[1], ast.SubTag) else None
            assignments = kid[2] if access else kid[1]
            if isinstance(assignments, ast.SubNodeList):
                return ast.GlobalVars(
                    access=access,
                    assignments=assignments,
                    is_frozen=is_frozen,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def access_tag(self, kid: list[ast.AstNode]) -> ast.SubTag[ast.Token]:
            """Grammar rule.

            access_tag: COLON ( KW_PROT | KW_PUB | KW_PRIV )
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.Token):
                return ast.SubTag[ast.Token](
                    tag=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def test(self, kid: list[ast.AstNode]) -> ast.Test:
            """Grammar rule.

            test: KW_TEST NAME? code_block
            """
            name = kid[1] if isinstance(kid[1], ast.Name) else kid[0]
            codeblock = kid[2] if name else kid[1]
            if isinstance(codeblock, ast.SubNodeList) and isinstance(
                name, (ast.Name, ast.Token)
            ):
                return ast.Test(
                    name=name,
                    body=codeblock,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def mod_code(self, kid: list[ast.AstNode]) -> ast.ModuleCode:
            """Grammar rule.

            mod_code: KW_WITH KW_ENTRY sub_name? code_block
            """
            name = kid[2] if isinstance(kid[2], ast.SubTag) else None
            codeblock = kid[3] if name else kid[2]
            if isinstance(codeblock, ast.SubNodeList):
                return ast.ModuleCode(
                    name=name,
                    body=codeblock,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def doc_tag(self, kid: list[ast.AstNode]) -> ast.Constant:
            """Grammar rule.

            doc_tag: ( STRING | DOC_STRING )
            """
            if isinstance(kid[0], ast.Constant):
                return kid[0]
            else:
                raise self.ice()

        def py_code_block(self, kid: list[ast.AstNode]) -> ast.PyInlineCode:
            """Grammar rule.

            py_code_block: PYNLINE
            """
            if isinstance(kid[0], ast.Token):
                return ast.PyInlineCode(
                    code=kid[0],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def import_stmt(self, kid: list[ast.AstNode]) -> ast.Import:
            """Grammar rule.

            import_stmt: KW_IMPORT sub_name KW_FROM import_path COMMA import_items SEMI
                | KW_IMPORT sub_name import_path KW_AS NAME SEMI
                | KW_IMPORT sub_name import_path SEMI
            """
            lang = kid[1]
            path = kid[3] if isinstance(kid[3], ast.ModulePath) else kid[2]
            alias = kid[5] if isinstance(kid[4], ast.Name) else None
            items = kid[5] if isinstance(kid[4], ast.SubNodeList) else None
            is_absorb = False
            if (
                isinstance(lang, ast.SubTag)
                and isinstance(path, ast.ModulePath)
                and isinstance(alias, ast.Name)
                and isinstance(items, ast.SubNodeList)
            ):
                return ast.Import(
                    lang=lang,
                    path=path,
                    alias=alias,
                    items=items,
                    is_absorb=is_absorb,
                    mod_link=self.mod_link,
                    kid=kid,
                )

            else:
                raise self.ice()

        def include_stmt(self, kid: list[ast.AstNode]) -> ast.Import:
            """Grammar rule.

            include_stmt: KW_INCLUDE sub_name import_path SEMI
            """
            lang = kid[1]
            path = kid[3] if isinstance(kid[3], ast.ModulePath) else kid[2]
            is_absorb = True
            if isinstance(lang, ast.SubTag) and isinstance(path, ast.ModulePath):
                return ast.Import(
                    lang=lang,
                    path=path,
                    alias=None,
                    items=None,
                    is_absorb=is_absorb,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def import_path(self, kid: list[ast.AstNode]) -> ast.ModulePath:
            """Grammar rule.

            import_path: DOT? DOT? esc_name ((DOT esc_name)+)?
            """
            valid_path = [i for i in kid if isinstance(i, ast.Token)]
            if len(valid_path) == len(kid):
                return ast.ModulePath(
                    path=valid_path,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def import_items(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ModuleItem]:
            """Grammar rule.

            import_items: (import_items COMMA)? named_refs (KW_AS NAME)?
            """
            consume = None
            name = None
            alias = None
            item = None
            item_kids = []
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                name = kid[2]
                item_kids.append(name)
            else:
                name = kid[0]
                item_kids.append(name)
            if (
                len(kid) > 2
                and isinstance(kid[-2], ast.Token)
                and kid[-2].name == Tok.KW_AS
            ):
                alias = kid[-1]
                item_kids = item_kids + [kid[-2], alias]
            if isinstance(name, ast.Name) and isinstance(alias, ast.Name):
                item = ast.ModuleItem(
                    name=name,
                    alias=alias,
                    mod_link=self.mod_link,
                    kid=item_kids,
                )
            else:
                self.ice()
            new_kid = [item, *consume.kid] if consume else [item]
            valid_kid = [i for i in new_kid if isinstance(i, ast.ModuleItem)]
            if len(valid_kid) == len(new_kid):
                return ast.SubNodeList[ast.ModuleItem](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=[*valid_kid],
                )
            else:
                raise self.ice()

        def architype(self, kid: list[ast.AstNode]) -> ast.ArchType:
            """Grammar rule.

            architype: decorators architype
                    | enum
                    | architype_def
                    | architype_decl
            """
            if isinstance(kid[0], ast.SubNodeList):
                if isinstance(kid[1], ast.ArchType):
                    kid[1].decorators = kid[0]
                    kid[1].add_kids_left([kid[0]])
                    return kid[1]
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.ArchType):
                return kid[0]
            else:
                raise self.ice()

        def architype_decl(self, kid: list[ast.AstNode]) -> ast.ArchType:
            """Grammar rule.

            architype_decl: arch_type access_tag? NAME inherited_archs (member_block | SEMI)
            """
            arch_type = kid[0]
            access = kid[1] if isinstance(kid[1], ast.SubTag) else None
            name = kid[2] if access else kid[1]
            inh = kid[3] if access else kid[2]
            body = (
                kid[4]
                if access and isinstance(kid[4], ast.SubNodeList)
                else kid[3]
                if isinstance(kid[3], ast.SubNodeList)
                else None
            )
            if (
                isinstance(arch_type, ast.Token)
                and isinstance(name, ast.Name)
                and isinstance(inh, ast.SubNodeList)
            ):
                return ast.Architype(
                    arch_type=arch_type,
                    name=name,
                    access=access,
                    base_classes=inh,
                    body=body,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def architype_def(self, kid: list[ast.AstNode]) -> ast.ArchDef:
            """Grammar rule.

            architype_def: abil_to_arch_chain member_block
            """
            if isinstance(kid[0], ast.ArchRefChain) and isinstance(
                kid[1], ast.ArchBlock
            ):
                return ast.ArchDef(
                    target=kid[0],
                    body=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def arch_type(self, kid: list[ast.AstNode]) -> ast.Token:
            """Grammar rule.

            arch_type: KW_WALKER
                    | KW_OBJECT
                    | KW_EDGE
                    | KW_NODE
            """
            if isinstance(kid[0], ast.Token):
                return kid[0]
            else:
                raise self.ice()

        def decorators(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.ExprType]:
            """Grammar rule.

            decorators: (DECOR_OP atom)+
            """
            valid_decors = [i for i in kid if isinstance(i, ast.ExprType)]
            if len(valid_decors) == len(kid) / 2:
                return ast.SubNodeList[ast.ExprType](
                    items=valid_decors,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def inherited_archs(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.SubNodeList[ast.Name | ast.SpecialVarRef]]:
            """Grammar rule.

            inherited_archs: sub_name_dotted+
            """
            valid_inh = [i for i in kid if isinstance(i, ast.SubNodeList)]
            if len(valid_inh) == len(kid):
                return ast.SubNodeList[ast.SubNodeList[ast.Name | ast.SpecialVarRef]](
                    items=valid_inh,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def sub_name_dotted(
            self, kid: list[ast.AstNode]
        ) -> ast.SubTag[ast.SubNodeList[ast.Name]]:
            """Grammar rule.

            sub_name_dotted: COLON dotted_name
            """
            if isinstance(kid[1], ast.SubNodeList):
                return ast.SubTag[ast.SubNodeList[ast.Name]](
                    tag=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def sub_name(self, kid: list[ast.AstNode]) -> ast.SubTag[ast.Name]:
            """Grammar rule.

            sub_name: COLON NAME
            """
            if isinstance(kid[1], ast.Name):
                return ast.SubTag[ast.Name](
                    tag=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def dotted_name(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.Name | ast.SpecialVarRef]:
            """Grammar rule.

            dotted_name: (dotted_name DOT)? all_refs
            """
            consume = None
            name = None
            dot = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                dot = kid[1]
                name = kid[2]
            else:
                name = kid[0]
            new_kid = [name, dot, *consume.kid] if consume else [name]
            valid_kid = [
                i for i in new_kid if isinstance(i, (ast.Name, ast.SpecialVarRef))
            ]
            if len(valid_kid) == (len(new_kid) / 2 + len(new_kid) % 2):
                return ast.SubNodeList[ast.Name | ast.SpecialVarRef](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def any_ref(self, kid: list[ast.AstNode]) -> ast.Name | ast.SpecialVarRef:
            """Grammar rule.

            any_ref: special_ref
                    | named_ref
            """
            if isinstance(kid[0], ast.Name | ast.SpecialVarRef):
                return kid[0]
            else:
                raise self.ice()

        def named_ref(self, kid: list[ast.AstNode]) -> ast.Name:
            """Grammar rule.

            named_ref: global_ref
                    | esc_name
            """
            if isinstance(kid[0], ast.Name):
                return kid[0]
            else:
                raise self.ice()

        def esc_name(self, kid: list[ast.AstNode]) -> ast.Name:
            """Grammar rule.

            esc_name: KWESC_NAME
                    | NAME
            """
            if isinstance(kid[0], ast.Name):
                return kid[0]
            else:
                raise self.ice()

        def special_ref(self, kid: list[ast.AstNode]) -> ast.SpecialVarRef:
            """Grammar rule.

            special_ref: INIT_OP
                        | ROOT_OP
                        | SUPER_OP
                        | SELF_OP
                        | HERE_OP
            """
            if isinstance(kid[0], ast.Token):
                return ast.SpecialVarRef(
                    var=kid[0],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def enum(self, kid: list[ast.AstNode]) -> ast.Enum | ast.EnumDef:
            """Grammar rule.

            enum: enum_def
                | enum_decl
            """
            if isinstance(kid[0], (ast.Enum, ast.EnumDef)):
                return kid[0]
            else:
                raise self.ice()

        def enum_decl(self, kid: list[ast.AstNode]) -> ast.Enum:
            """Grammar rule.

            enum_decl: KW_ENUM access_tag? NAME inherited_archs? (enum_block | SEMI)
            """
            access = kid[1] if isinstance(kid[1], ast.SubTag) else None
            name = kid[2] if access else kid[1]
            inh = kid[3] if access else kid[2]
            body = (
                kid[4]
                if access and isinstance(kid[4], ast.SubNodeList)
                else kid[3]
                if isinstance(kid[3], ast.SubNodeList)
                else None
            )
            if isinstance(name, ast.Name) and isinstance(inh, ast.SubNodeList):
                return ast.Enum(
                    name=name,
                    access=access,
                    base_classes=inh,
                    body=body,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def enum_def(self, kid: list[ast.AstNode]) -> ast.EnumDef:
            """Grammar rule.

            enum_def: arch_to_enum_chain enum_block
            """
            if isinstance(kid[0], ast.ArchRefChain) and isinstance(
                kid[1], ast.SubNodeList
            ):
                return ast.EnumDef(
                    target=kid[0],
                    body=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def enum_block(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.Name | ast.Assignment]:
            """Grammar rule.

            enum_block: LBRACE enum_stmt_list? RBRACE
            """
            if isinstance(kid[1], ast.SubNodeList):
                return kid[1]
            else:
                return ast.SubNodeList[ast.Name | ast.Assignment](
                    items=[],
                    mod_link=self.mod_link,
                    kid=kid,
                )

        def enum_stmt_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.Name | ast.Assignment]:
            """Grammar rule.

            enum_stmt_list: (enum_stmt_list COMMA)? enum_item
            """
            consume = None
            name = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                name = kid[2]
            else:
                name = kid[0]
            new_kid = [name, comma, *consume.kid] if consume else [name]
            valid_kid = [
                i for i in new_kid if isinstance(i, (ast.Name, ast.Assignment))
            ]
            if len(valid_kid) == (len(new_kid) / 2 + len(new_kid) % 2):
                return ast.SubNodeList[ast.Name | ast.Assignment](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def enum_item(self, kid: list[ast.AstNode]) -> ast.Name | ast.Assignment:
            """Grammar rule.

            enum_item: NAME EQ expression
                    | NAME
            """
            if isinstance(kid[0], ast.Name):
                if len(kid) == 1:
                    return kid[0]
                elif isinstance(kid[2], ast.ExprType):
                    return ast.Assignment(
                        target=kid[0],
                        value=kid[2],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
            raise self.ice()

        def ability(self, kid: list[ast.AstNode]) -> ast.Ability | ast.AbilityDef:
            """Grammar rule.

            ability: decorators ability
                    | ability_def
                    | KW_ASYNC ability_decl
                    | ability_decl
            """
            if isinstance(kid[0], ast.SubNodeList):
                if isinstance(kid[1], (ast.Ability, ast.AbilityDef)):
                    kid[1].decorators = kid[0]
                    kid[1].add_kids_left([kid[0]])
                    return kid[1]
                else:
                    raise self.ice()
            elif isinstance(kid[0], (ast.Ability, ast.AbilityDef)):
                return kid[0]
            else:
                raise self.ice()

        def ability_decl(self, kid: list[ast.AstNode]) -> ast.Ability:
            """Grammar rule.

            ability_decl: KW_STATIC? KW_CAN access_tag? any_ref (func_decl | event_clause) (code_block | SEMI)
            """
            chomp = [*kid]
            is_static = isinstance(chomp[0], ast.Token)
            chomp = chomp[1:] if is_static else chomp
            access = chomp[0] if isinstance(chomp[0], ast.SubTag) else None
            chomp = chomp[1:] if access else chomp
            name = chomp[0]
            chomp = chomp[1:]
            is_func = isinstance(chomp[0], ast.FuncSignature)
            signature = chomp[0]
            chomp = chomp[1:]
            body = chomp[0] if isinstance(chomp[0], ast.SubNodeList) else None
            if isinstance(name, ast.NameType) and isinstance(
                signature, (ast.FuncSignature, ast.EventSignature)
            ):
                return ast.Ability(
                    name_ref=name,
                    is_func=is_func,
                    is_async=False,
                    is_static=is_static,
                    is_abstract=False,
                    access=access,
                    signature=signature,
                    body=body,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def ability_def(self, kid: list[ast.AstNode]) -> ast.AbilityDef:
            """Grammar rule.

            ability_def: arch_to_abil_chain (func_decl | event_clause) code_block
            """
            if (
                isinstance(kid[0], ast.ArchRefChain)
                and isinstance(kid[1], (ast.FuncSignature, ast.EventSignature))
                and isinstance(kid[2], ast.SubNodeList)
            ):
                return ast.AbilityDef(
                    target=kid[0],
                    signature=kid[1],
                    body=kid[2],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def abstract_ability(self, kid: list[ast.AstNode]) -> ast.Ability:
            """Grammar rule.

            abstract_ability: KW_STATIC? KW_CAN access_tag? any_ref (func_decl | event_clause) KW_ABSTRACT SEMI
            """
            chomp = [*kid]
            is_static = isinstance(chomp[0], ast.Token)
            chomp = chomp[1:] if is_static else chomp
            access = chomp[0] if isinstance(chomp[0], ast.SubTag) else None
            chomp = chomp[1:] if access else chomp
            name = chomp[0]
            chomp = chomp[1:]
            is_func = isinstance(chomp[0], ast.FuncSignature)
            signature = chomp[0]
            chomp = chomp[1:]
            if isinstance(name, ast.NameType) and isinstance(
                signature, (ast.FuncSignature, ast.EventSignature)
            ):
                return ast.Ability(
                    name_ref=name,
                    is_func=is_func,
                    is_async=False,
                    is_static=is_static,
                    is_abstract=True,
                    access=access,
                    signature=signature,
                    body=None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()


# enum_decl: KW_ENUM access_tag? NAME inherited_archs? (enum_block | SEMI)

# enum_def: arch_to_enum_chain enum_block

# enum_block: LBRACE enum_stmt_list? RBRACE

# enum_stmt_list: (enum_stmt_list COMMA)? enum_item

# enum_item: NAME EQ expression
#          | NAME

# ability: decorators ability
#         | ability_def
#         | KW_ASYNC ability_decl
#         | ability_decl

# ability_decl: KW_STATIC? KW_CAN access_tag? any_ref (func_decl | event_clause) (code_block | SEMI)
# ability_def: arch_to_abil_chain (func_decl | event_clause) code_block

# abstract_ability: KW_STATIC? KW_CAN access_tag? any_ref (func_decl | event_clause) KW_ABSTRACT SEMI

# event_clause: KW_WITH type_spec? (KW_EXIT | KW_ENTRY) return_type_tag?

# func_decl: (LPAREN func_decl_param_list? RPAREN)? return_type_tag?

# func_decl_param_list: param_var (COMMA func_decl_param_list)?

# param_var: (STAR_POW | STAR_MUL)? NAME type_tag (EQ expression)?

# member_block: LBRACE member_stmt_list? RBRACE

# member_stmt_list: member_stmt (member_stmt_list)?

# member_stmt: py_code_block
#            | doc_tag? abstract_ability
#            | doc_tag? ability
#            | doc_tag? architype
#            | doc_tag? has_stmt

# has_stmt: KW_STATIC? (KW_FREEZE | KW_HAS) access_tag? has_assign_clause SEMI

# has_assign_clause: typed_has_clause (COMMA has_assign_clause)?

# typed_has_clause: esc_name type_tag (EQ expression)?

# type_tag: COLON type_spec

# return_type_tag: RETURN_HINT? type_spec

# type_spec: single_type (BW_OR type_spec | NULL_OK)?

# single_type: TYP_DICT LSQUARE single_type COMMA single_type RSQUARE
#            | TYP_SET LSQUARE single_type RSQUARE
#            | TYP_TUPLE LSQUARE single_type RSQUARE
#            | TYP_LIST LSQUARE single_type RSQUARE
#            | dotted_name
#            | NULL
#            | builtin_type

# builtin_type: TYP_TYPE
#             | TYP_ANY
#             | TYP_BOOL
#             | TYP_DICT
#             | TYP_SET
#             | TYP_TUPLE
#             | TYP_LIST
#             | TYP_FLOAT
#             | TYP_INT
#             | TYP_BYTES
#             | TYP_STRING

# code_block: LBRACE statement_list? RBRACE

# statement_list: statement+

# statement: py_code_block
#           | walker_stmt
#           | await_stmt SEMI
#           | yield_stmt SEMI
#           | return_stmt SEMI
#           | report_stmt SEMI
#           | delete_stmt SEMI
#           | ctrl_stmt SEMI
#           | assert_stmt SEMI
#           | raise_stmt SEMI
#           | with_stmt
#           | while_stmt
#           | for_stmt
#           | try_stmt
#           | if_stmt
#           | expression SEMI
#           | static_assignment
#           | assignment SEMI
#           | typed_ctx_block
#           | doc_tag? ability
#           | doc_tag? architype
#           | import_stmt

# typed_ctx_block: RETURN_HINT type_spec code_block

# if_stmt: KW_IF expression code_block (elif_list? else_stmt? | elif_list?)

# elif_list: KW_ELIF expression code_block elif_list?

# else_stmt: KW_ELSE code_block

# try_stmt: KW_TRY code_block (except_list? finally_stmt? | finally_stmt)

# except_list: except_def+

# except_def: KW_EXCEPT expression (KW_AS NAME)? code_block

# finally_stmt: KW_FINALLY code_block

# for_stmt: KW_FOR (name_list KW_IN | assignment KW_TO expression KW_BY) expression code_block

# name_list: NAME (COMMA name_list)?

# while_stmt: KW_WHILE expression code_block

# with_stmt: KW_WITH expr_as_list code_block

# expr_as_list: (expression (KW_AS NAME)?) (COMMA expr_as_list)?

# raise_stmt: KW_RAISE expression?

# assert_stmt: KW_ASSERT expression (COMMA expression)?

# ctrl_stmt: KW_SKIP | KW_BREAK | KW_CONTINUE

# delete_stmt: KW_DELETE expression

# report_stmt: KW_REPORT expression

# return_stmt: KW_RETURN expression?

# yield_stmt: KW_YIELD expression?

# walker_stmt: disengage_stmt | revisit_stmt | visit_stmt | ignore_stmt

# ignore_stmt: KW_IGNORE expression SEMI

# visit_stmt: KW_VISIT (sub_name_dotted)? expression (else_stmt | SEMI)

# revisit_stmt: KW_REVISIT expression? (else_stmt | SEMI)

# disengage_stmt: KW_DISENGAGE SEMI

# await_stmt: KW_AWAIT expression

# assignment: KW_FREEZE? atom EQ expression

# static_assignment: KW_HAS assignment_list SEMI

# expression: pipe KW_IF expression KW_ELSE expression
#           | pipe

# pipe: pipe_back PIPE_FWD pipe
#     | pipe_back

# pipe_back: elvis_check PIPE_BKWD pipe_back
#          | elvis_check

# elvis_check: bitwise_or ELVIS_OP elvis_check
#            | bitwise_or

# bitwise_or: bitwise_xor BW_OR bitwise_or
#           | bitwise_xor

# bitwise_xor: bitwise_and BW_XOR bitwise_xor
#            | bitwise_and

# bitwise_and: shift BW_AND bitwise_and
#            | shift

# shift: logical RSHIFT shift
#      | logical LSHIFT shift
#      | logical

# logical: NOT logical
#        | compare KW_OR logical
#        | compare KW_AND logical
#        | compare

# compare: arithmetic cmp_op compare
#        | arithmetic

# arithmetic: term MINUS arithmetic
#           | term PLUS arithmetic
#           | term

# term: factor MOD term
#     | factor DIV term
#     | factor FLOOR_DIV term
#     | factor STAR_MUL term
#     | factor

# factor: power
#       | BW_NOT factor
#       | MINUS factor
#       | PLUS factor

# power: connect STAR_POW power
#      | connect

# connect: atomic_pipe
#        | atomic_pipe connect_op connect
#        | atomic_pipe disconnect_op connect

# atomic_pipe: atomic_pipe_back
#            | atomic_pipe KW_SPAWN atomic_pipe_back
#            | atomic_pipe A_PIPE_FWD atomic_pipe_back

# atomic_pipe_back: unpack
#                 | atomic_pipe_back A_PIPE_BKWD unpack

# unpack: ref
#       | STAR_MUL atom
#       | STAR_POW atom

# ref: walrus_assign
#    | BW_AND walrus_assign

# walrus_assign: ds_call walrus_op walrus_assign
#              | ds_call

# ds_call: atom
#        | PIPE_FWD atom
#        | A_PIPE_FWD atom
#        | KW_SPAWN atom

# walrus_op: RSHIFT_EQ
#          | LSHIFT_EQ
#          | BW_NOT_EQ
#          | BW_XOR_EQ
#          | BW_OR_EQ
#          | BW_AND_EQ
#          | MOD_EQ
#          | DIV_EQ
#          | FLOOR_DIV_EQ
#          | MUL_EQ
#          | SUB_EQ
#          | ADD_EQ
#          | WALRUS_EQ

# cmp_op: KW_ISN
#       | KW_IS
#       | KW_NIN
#       | KW_IN
#       | NE
#       | GTE
#       | LTE
#       | GT
#       | LT
#       | EE

# atom: edge_op_ref
#     | any_ref
#     | atomic_chain
#     | LPAREN expression RPAREN
#     | atom_collection
#     | atom_literal

# atom_literal: builtin_type
#             | NULL
#             | BOOL
#             | multistring
#             | FLOAT
#             | OCT
#             | BIN
#             | HEX
#             | INT

# atom_collection: dict_compr
#                | set_compr
#                | gen_compr
#                | list_compr
#                | dict_val
#                | set_val
#                | tuple_val
#                | list_val

# multistring: multistring fstring
#            | multistring STRING
#            | fstring
#            | STRING

# fstring: FSTR_START fstr_parts* FSTR_END

# fstr_parts: FSTR_PIECE
#           | FSTR_BESC
#           | fstr_expr
#           | fstring

# fstr_expr: LBRACE expression RBRACE

# list_val: LSQUARE expr_list? RSQUARE
# tuple_val: LPAREN tuple_list? RPAREN
# set_val: LBRACE expr_list RBRACE

# expr_list: expr_list COMMA expression | expression

# tuple_list: expression COMMA (expr_list COMMA assignment_list | assignment_list | expr_list)?
#           | assignment_list
#           | expression COMMA

# dict_val: LBRACE kv_pairs? RBRACE

# list_compr: LSQUARE inner_compr RSQUARE
# gen_compr: LPAREN inner_compr RPAREN
# set_compr: LBRACE inner_compr RBRACE
# inner_compr: expression KW_FOR name_list KW_IN walrus_assign (KW_IF expression)?

# dict_compr: LBRACE expression COLON expression KW_FOR name_list KW_IN walrus_assign (KW_IF expression)? RBRACE

# kv_pairs: (expression COLON expression COMMA)* expression COLON expression

# atomic_chain: atomic_call
#             | atomic_chain_unsafe
#             | atomic_chain_safe

# atomic_chain_unsafe: atom (filter_compr | edge_op_ref
# | index_slice | DOT_BKWD any_ref | DOT_FWD any_ref | DOT any_ref)

# atomic_chain_safe: atom NULL_OK (filter_compr | edge_op_ref | index_slice |
# DOT_BKWD any_ref | DOT_FWD any_ref | DOT any_ref)

# atomic_call: atom func_call_tail

# func_call_tail: LPAREN param_list? RPAREN

# param_list: (expr_list COMMA assignment_list) | assignment_list | expr_list

# assignment_list: assignment_list COMMA assignment | assignment

# index_slice: LSQUARE expression? (COLON expression?)? RSQUARE

# arch_ref: object_ref
#         | walker_ref
#         | edge_ref
#         | node_ref

# arch_or_ability_chain: (arch_or_ability_chain (ability_ref | arch_ref)) | ability_ref | arch_ref

# abil_to_arch_chain: arch_or_ability_chain arch_ref | arch_ref

# arch_to_abil_chain: arch_or_ability_chain ability_ref | ability_ref

# arch_to_enum_chain: arch_or_ability_chain enum_ref | enum_ref

# node_ref: NODE_OP NAME
# edge_ref: EDGE_OP NAME
# walker_ref: WALKER_OP NAME
# object_ref: OBJECT_OP esc_name
# enum_ref: ENUM_OP NAME
# ability_ref: ABILITY_OP (special_ref | esc_name)
# global_ref: GLOBAL_OP esc_name

# edge_op_ref: edge_any
#            | edge_from
#            | edge_to

# edge_to: ARROW_R_P1 expression (COLON filter_compare_list)? ARROW_R_P2
#        | ARROW_R

# edge_from: ARROW_L_P1 expression (COLON filter_compare_list)? ARROW_L_P2
#          | ARROW_L

# edge_any: ARROW_L_P1 expression (COLON filter_compare_list)? ARROW_R_P2
#         | ARROW_BI

# connect_op: connect_from
#           | connect_to

# disconnect_op: NOT edge_op_ref

# connect_to: CARROW_R_P1 expression (COLON assignment_list)? CARROW_R_P2
#           | CARROW_R

# connect_from: CARROW_L_P1 expression (COLON assignment_list)? CARROW_L_P2
#             | CARROW_L

# filter_compr: LPAREN EQ filter_compare_list RPAREN

# filter_compare_list: (esc_name cmp_op expression COMMA)* esc_name cmp_op expression

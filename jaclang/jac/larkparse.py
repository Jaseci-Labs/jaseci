"""Lark parser for Jac Lang."""
from __future__ import annotations


import logging
import os
from typing import Union

import jaclang.jac.absyntree as ast
from jaclang.jac import jac_lark as jl
from jaclang.jac.constant import EdgeDir, Tokens as Tok
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
            self.mod_link = None

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
            valid_body: list[ast.ElementStmt] = [
                i for i in body if isinstance(i, ast.ElementStmt)
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

        def element_with_doc(self, kid: list[ast.AstNode]) -> ast.ElementStmt:
            """Grammar rule.

            element_with_doc: doc_tag element
            """
            if isinstance(kid[1], ast.ElementStmt) and isinstance(kid[0], ast.Constant):
                kid[1].doc = kid[0]
                kid[1].add_kids_left([kid[0]])
                return kid[1]
            else:
                raise self.ice()

        def element(self, kid: list[ast.AstNode]) -> ast.ElementStmt:
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
            if isinstance(kid[0], ast.ElementStmt):
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
                kid[1], ast.SubNodeList
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
        ) -> ast.SubNodeList[ast.SubNodeList[ast.NameType]]:
            """Grammar rule.

            inherited_archs: sub_name_dotted+
            """
            valid_inh = [i for i in kid if isinstance(i, ast.SubNodeList)]
            if len(valid_inh) == len(kid):
                return ast.SubNodeList[ast.SubNodeList[ast.NameType]](
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

        def dotted_name(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.NameType]:
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
                return ast.SubNodeList[ast.NameType](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def any_ref(self, kid: list[ast.AstNode]) -> ast.NameType:
            """Grammar rule.

            any_ref: special_ref
                    | named_ref
            """
            if isinstance(kid[0], ast.NameType):
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
        ) -> ast.SubNodeList[ast.EnumBlockStmt]:
            """Grammar rule.

            enum_block: LBRACE enum_stmt_list? RBRACE
            """
            if isinstance(kid[1], ast.SubNodeList):
                kid[1].add_kids_left([kid[0]])
                kid[1].add_kids_right([kid[2]])
                return kid[1]
            else:
                return ast.SubNodeList[ast.EnumBlockStmt](
                    items=[],
                    mod_link=self.mod_link,
                    kid=kid,
                )

        def enum_stmt_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.EnumBlockStmt]:
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
            valid_kid = [i for i in new_kid if isinstance(i, ast.EnumBlockStmt)]
            if len(valid_kid) == (len(new_kid) / 2 + len(new_kid) % 2):
                return ast.SubNodeList[ast.EnumBlockStmt](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def enum_item(self, kid: list[ast.AstNode]) -> ast.EnumBlockStmt:
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

        def event_clause(self, kid: list[ast.AstNode]) -> ast.EventSignature:
            """Grammar rule.

            event_clause: KW_WITH type_specs? (KW_EXIT | KW_ENTRY) return_type_tag?
            """
            type_specs = kid[1] if isinstance(kid[1], ast.SubNodeList) else None
            return_spec = kid[-1] if isinstance(kid[-1], ast.TypeSpec) else None
            event = kid[2] if type_specs else kid[1]
            if isinstance(event, ast.Token) and isinstance(
                return_spec, ast.SubNodeList
            ):
                return ast.EventSignature(
                    event=event,
                    arch_tag_info=type_specs,
                    return_type=return_spec,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def func_decl(self, kid: list[ast.AstNode]) -> ast.FuncSignature:
            """Grammar rule.

            func_decl: (LPAREN func_decl_param_list? RPAREN)? retur_type_tag?
            """
            params = kid[1] if isinstance(kid[1], ast.SubNodeList) else None
            return_spec = kid[-1] if isinstance(kid[-1], ast.SubNodeList) else None
            if isinstance(params, ast.SubNodeList) and isinstance(
                return_spec, ast.SubNodeList
            ):
                return ast.FuncSignature(
                    params=params,
                    return_type=return_spec,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def func_decl_param_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ParamVar]:
            """Grammar rule.

            func_decl_param_list: (func_decl_param_list COMMA)? param_var
            """
            consume = None
            param = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                param = kid[2]
            else:
                param = kid[0]
            new_kid = [param, comma, *consume.kid] if consume else [param]
            valid_kid = [i for i in new_kid if isinstance(i, ast.ParamVar)]
            if len(valid_kid) == (len(new_kid) / 2 + len(new_kid) % 2):
                return ast.SubNodeList[ast.ParamVar](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def param_var(self, kid: list[ast.AstNode]) -> ast.ParamVar:
            """Grammar rule.

            param_var: (STAR_POW | STAR_MUL)? NAME type_tag (EQ expression)?
            """
            star = kid[0] if isinstance(kid[0], ast.Token) else None
            name = kid[1] if star else kid[0]
            type_tag = kid[2] if star else kid[1]
            value = kid[-1] if isinstance(kid[-1], ast.ExprType) else None
            if isinstance(name, ast.Name) and isinstance(type_tag, ast.SubNodeList):
                return ast.ParamVar(
                    name=name,
                    type_tag=type_tag,
                    value=value,
                    unpack=star,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def member_block(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ArchBlockStmt]:
            """Grammar rule.

            member_block: LBRACE member_stmt_list? RBRACE
            """
            if isinstance(kid[1], ast.SubNodeList):
                kid[1].add_kids_left([kid[0]])
                kid[1].add_kids_right([kid[2]])
                return kid[1]
            else:
                return ast.SubNodeList[ast.ArchBlockStmt](
                    items=[],
                    mod_link=self.mod_link,
                    kid=kid,
                )

        def member_stmt_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ArchBlockStmt]:
            """Grammar rule.

            member_stmt_list: (member_stmt_list)? member_stmt
            """
            consume = None
            stmt = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                stmt = kid[1]
            else:
                stmt = kid[0]
            new_kid = [stmt, *consume.kid] if consume else [stmt]
            valid_kid = [i for i in new_kid if isinstance(i, ast.ArchBlockStmt)]
            if len(valid_kid) == len(new_kid):
                return ast.SubNodeList[ast.ArchBlockStmt](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def member_stmt(self, kid: list[ast.AstNode]) -> ast.ArchBlockStmt:
            """Grammar rule.

            member_stmt: doc_tag? py_code_block
                        | doc_tag? abstract_ability
                        | doc_tag? ability
                        | doc_tag? architype
                        | doc_tag? has_stmt
            """
            if isinstance(kid[1], ast.ArchBlockStmt) and isinstance(
                kid[0], ast.Constant
            ):
                kid[1].doc = kid[0]
                kid[1].add_kids_left([kid[0]])
                return kid[1]
            elif isinstance(kid[0], ast.ArchBlockStmt):
                return kid[0]
            else:
                raise self.ice()

        def has_stmt(self, kid: list[ast.AstNode]) -> ast.ArchHas:
            """Grammar rule.

            has_stmt: KW_STATIC? (KW_FREEZE | KW_HAS) access_tag? has_assign_list SEMI
            """
            chomp = [*kid]
            is_static = (
                isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.KW_STATIC
            )
            chomp = chomp[1:] if is_static else chomp
            is_freeze = (
                isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.KW_FREEZE
            )
            chomp = chomp[1:]
            access = chomp[0] if isinstance(chomp[0], ast.SubTag) else None
            chomp = chomp[1:] if access else chomp
            assign = chomp[0]
            if isinstance(assign, ast.SubNodeList):
                return ast.ArchHas(
                    vars=assign,
                    is_static=is_static,
                    is_frozen=is_freeze,
                    access=access,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def has_assign_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.HasVar]:
            """Grammar rule.

            has_assign_list: (has_assign_list COMMA)? typed_has_clause
            """
            consume = None
            assign = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                assign = kid[2]
            else:
                assign = kid[0]
            new_kid = [assign, comma, *consume.kid] if consume else [assign]
            valid_kid = [i for i in new_kid if isinstance(i, ast.HasVar)]
            if len(valid_kid) == (len(new_kid) / 2 + len(new_kid) % 2):
                return ast.SubNodeList[ast.HasVar](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def typed_has_clause(self, kid: list[ast.AstNode]) -> ast.HasVar:
            """Grammar rule.

            typed_has_clause: esc_name type_tag (EQ expression)?
            """
            name = kid[0]
            type_tag = kid[1]
            value = kid[-1] if isinstance(kid[-1], ast.ExprType) else None
            if isinstance(name, ast.Name) and isinstance(type_tag, ast.SubTag):
                return ast.HasVar(
                    name=name,
                    type_tag=type_tag,
                    value=value,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def type_tag(
            self, kid: list[ast.AstNode]
        ) -> ast.SubTag[ast.SubNodeList[ast.TypeSpec]]:
            """Grammar rule.

            type_tag: COLON type_specs
            """
            if isinstance(kid[1], ast.SubNodeList):
                return ast.SubTag[ast.SubNodeList[ast.TypeSpec]](
                    tag=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def return_type_tag(
            self, kid: list[ast.AstNode]
        ) -> ast.SubTag[ast.SubNodeList[ast.TypeSpec]]:
            """Grammar rule.

            return_type_tag: RETURN_HINT type_specs
            """
            if isinstance(kid[1], ast.SubNodeList):
                return ast.SubTag[ast.SubNodeList[ast.TypeSpec]](
                    tag=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def type_specs(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.TypeSpec]:
            """Grammar rule.

            type_specs: (type_specs BW_OR)? single_type NULL_OK?
            """
            consume = None
            spec = None
            pipe = None
            null_ok = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                pipe = kid[1]
                spec = kid[2]
            else:
                spec = kid[0]
            if isinstance(kid[-1], ast.Token) and kid[-1].name == Tok.NULL_OK:
                null_ok = kid[-1]
            new_kid = [*consume.kid, pipe, spec] if consume else [spec]
            valid_kid = [i for i in new_kid if isinstance(i, ast.TypeSpec)]
            if null_ok:
                valid_kid[-1].null_ok = True
                valid_kid[-1].add_kids_right([null_ok])
            if len(valid_kid) == (len(new_kid) / 2 + len(new_kid) % 2):
                return ast.SubNodeList[ast.TypeSpec](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def single_type(self, kid: list[ast.AstNode]) -> ast.TypeSpec:
            """Grammar rule.

            single_type: TYP_DICT LSQUARE single_type COMMA single_type RSQUARE
                        | TYP_SET LSQUARE single_type RSQUARE
                        | TYP_TUPLE LSQUARE single_type RSQUARE
                        | TYP_LIST LSQUARE single_type RSQUARE
                        | dotted_name
                        | NULL
                        | builtin_type
            """
            spec_type = kid[0]
            list_nest = None
            dict_nest = None
            if len(kid) > 1:
                list_nest = kid[2]
            if len(kid) > 4:
                dict_nest = kid[4]
            if (
                isinstance(spec_type, (ast.Token, ast.SubNodeList))
                and (not list_nest or isinstance(list_nest, ast.TypeSpec))
                and (not dict_nest or isinstance(dict_nest, ast.TypeSpec))
            ):
                return ast.TypeSpec(
                    spec_type=spec_type,
                    list_nest=list_nest,
                    dict_nest=dict_nest,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def builtin_type(self, kid: list[ast.AstNode]) -> ast.Token:
            """Grammar rule.

            builtin_type: TYP_TYPE
                        | TYP_ANY
                        | TYP_BOOL
                        | TYP_DICT
                        | TYP_SET
                        | TYP_TUPLE
                        | TYP_LIST
                        | TYP_FLOAT
                        | TYP_INT
                        | TYP_BYTES
                        | TYP_STRING
            """
            if isinstance(kid[0], ast.Token):
                return kid[0]
            else:
                raise self.ice()

        def code_block(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.CodeBlockStmt]:
            """Grammar rule.

            code_block: LBRACE statement_list* RBRACE
            """
            if isinstance(kid[1], ast.SubNodeList):
                kid[1].add_kids_left([kid[0]])
                kid[1].add_kids_right([kid[2]])
                return kid[1]
            else:
                return ast.SubNodeList[ast.CodeBlockStmt](
                    items=[],
                    mod_link=self.mod_link,
                    kid=kid,
                )

        def statement_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.CodeBlockStmt]:
            """Grammar rule.

            statement_list: statement+
            """
            valid_stmt = [i for i in kid if isinstance(i, ast.CodeBlockStmt)]
            if len(valid_stmt) == len(kid):
                return ast.SubNodeList[ast.CodeBlockStmt](
                    items=valid_stmt,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def statement(self, kid: list[ast.AstNode]) -> ast.CodeBlockStmt:
            """Grammar rule.

            statement: py_code_block
                    | walker_stmt
                    | await_stmt SEMI
                    | yield_stmt SEMI
                    | return_stmt SEMI
                    | report_stmt SEMI
                    | delete_stmt SEMI
                    | ctrl_stmt SEMI
                    | assert_stmt SEMI
                    | raise_stmt SEMI
                    | with_stmt
                    | while_stmt
                    | for_stmt
                    | try_stmt
                    | if_stmt
                    | expression SEMI
                    | static_assignment
                    | assignment SEMI
                    | typed_ctx_block
                    | doc_tag? ability
                    | doc_tag? architype
                    | import_stmt
            """
            if isinstance(kid[0], ast.CodeBlockStmt):
                return kid[0]
            elif isinstance(kid[1], (ast.Ability, ast.Architype)) and isinstance(
                kid[0], ast.Constant
            ):
                kid[1].doc = kid[0]
                kid[1].add_kids_left([kid[0]])
                return kid[1]
            else:
                raise self.ice()

        def typed_ctx_block(self, kid: list[ast.AstNode]) -> ast.TypedCtxBlock:
            """Grammar rule.

            typed_ctx_block: RETURN_HINT type_specs code_block
            """
            if isinstance(kid[1], ast.SubNodeList) and isinstance(
                kid[2], ast.SubNodeList
            ):
                return ast.TypedCtxBlock(
                    type_ctx=kid[1],
                    body=kid[2],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def if_stmt(self, kid: list[ast.AstNode]) -> ast.IfStmt:
            """Grammar rule.

            if_stmt: KW_IF expression code_block elif_stmt? else_stmt?
            """
            if isinstance(kid[1], ast.ExprType) and isinstance(kid[2], ast.SubNodeList):
                return ast.IfStmt(
                    condition=kid[1],
                    body=kid[2],
                    elseifs=kid[3] if isinstance(kid[3], ast.ElseIfs) else None,
                    else_body=kid[4] if isinstance(kid[4], ast.ElseStmt) else None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def elif_stmt(self, kid: list[ast.AstNode]) -> ast.ElseIfs:
            """Grammar rule.

            elif_stmt: KW_ELIF expression code_block elif_stmt?
            """
            if isinstance(kid[1], ast.ExprType) and isinstance(kid[2], ast.SubNodeList):
                return ast.ElseIfs(
                    condition=kid[1],
                    body=kid[2],
                    elseifs=kid[3] if isinstance(kid[3], ast.ElseIfs) else None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def else_stmt(self, kid: list[ast.AstNode]) -> ast.ElseStmt:
            """Grammar rule.

            else_stmt: KW_ELSE code_block
            """
            if isinstance(kid[1], ast.SubNodeList):
                return ast.ElseStmt(
                    body=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def try_stmt(self, kid: list[ast.AstNode]) -> ast.TryStmt:
            """Grammar rule.

            try_stmt: KW_TRY code_block except_list? finally_stmt?
            """
            if isinstance(kid[1], ast.SubNodeList):
                return ast.TryStmt(
                    body=kid[1],
                    excepts=kid[2] if isinstance(kid[2], ast.SubNodeList) else None,
                    finally_body=kid[3]
                    if isinstance(kid[3], ast.FinallyStmt)
                    else None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def except_list(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.Except]:
            """Grammar rule.

            except_list: except_def+
            """
            valid_kid = [i for i in kid if isinstance(i, ast.Except)]
            if len(valid_kid) == len(kid):
                return ast.SubNodeList[ast.Except](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def except_def(self, kid: list[ast.AstNode]) -> ast.Except:
            """Grammar rule.

            except_def: KW_EXCEPT expression (KW_AS NAME)? code_block
            """
            ex_type = kid[1]
            name = kid[3] if isinstance(kid[3], ast.Name) else None
            body = kid[-1]
            if isinstance(ex_type, ast.ExprType) and isinstance(body, ast.SubNodeList):
                return ast.Except(
                    ex_type=ex_type,
                    name=name,
                    body=body,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def finally_stmt(self, kid: list[ast.AstNode]) -> ast.FinallyStmt:
            """Grammar rule.

            finally_stmt: KW_FINALLY code_block
            """
            if isinstance(kid[1], ast.SubNodeList):
                return ast.FinallyStmt(
                    body=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def for_stmt(self, kid: list[ast.AstNode]) -> ast.IterForStmt | ast.InForStmt:
            """Grammar rule.

            for_stmt: KW_FOR assignment KW_TO expression KW_BY expression code_block
                    | KW_FOR name_list KW_IN expression code_block
            """
            if isinstance(kid[1], ast.Assignment):
                if (
                    isinstance(kid[3], ast.ExprType)
                    and isinstance(kid[5], ast.ExprType)
                    and isinstance(kid[6], ast.SubNodeList)
                ):
                    return ast.IterForStmt(
                        iter=kid[1],
                        condition=kid[3],
                        count_by=kid[5],
                        body=kid[6],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[1], ast.SubNodeList):
                if isinstance(kid[3], ast.ExprType) and isinstance(
                    kid[4], ast.SubNodeList
                ):
                    return ast.InForStmt(
                        name_list=kid[1],
                        collection=kid[3],
                        body=kid[4],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            else:
                raise self.ice()

        def name_list(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.Name]:
            """Grammar rule.

            name_list: (name_list COMMA)? NAME
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
            valid_kid = [i for i in new_kid if isinstance(i, ast.Name)]
            if len(valid_kid) == (len(new_kid) / 2 + len(new_kid) % 2):
                return ast.SubNodeList[ast.Name](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def while_stmt(self, kid: list[ast.AstNode]) -> ast.WhileStmt:
            """Grammar rule.

            while_stmt: KW_WHILE expression code_block
            """
            if isinstance(kid[1], ast.ExprType) and isinstance(kid[2], ast.SubNodeList):
                return ast.WhileStmt(
                    condition=kid[1],
                    body=kid[2],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def with_stmt(self, kid: list[ast.AstNode]) -> ast.WithStmt:
            """Grammar rule.

            with_stmt: KW_WITH expr_as_list code_block
            """
            if isinstance(kid[1], ast.SubNodeList) and isinstance(
                kid[2], ast.SubNodeList
            ):
                return ast.WithStmt(
                    exprs=kid[1],
                    body=kid[2],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def expr_as_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ExprAsItem]:
            """Grammar rule.

            expr_as_list: (expr_as_list COMMA)? expression (KW_AS NAME)?
            """
            consume = None
            expr = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                expr = kid[2]
            else:
                expr = kid[0]
            name = kid[-1] if isinstance(kid[-1], ast.Name) else None
            new_kid = [expr, comma, *consume.kid] if consume else [expr]
            valid_kid = [i for i in new_kid if isinstance(i, ast.ExprAsItem)]
            if name:
                valid_kid[-1].alias = name
                valid_kid[-1].add_kids_right([name])
            return ast.SubNodeList[ast.ExprAsItem](
                items=valid_kid,
                mod_link=self.mod_link,
                kid=kid,
            )

        def raise_stmt(self, kid: list[ast.AstNode]) -> ast.RaiseStmt:
            """Grammar rule.

            raise_stmt: KW_RAISE expression?
            """
            if len(kid) > 1:
                if isinstance(kid[1], ast.ExprType) or not kid[1]:
                    return ast.RaiseStmt(
                        cause=kid[1],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            else:
                return ast.RaiseStmt(
                    cause=None,
                    mod_link=self.mod_link,
                    kid=kid,
                )

        def assert_stmt(self, kid: list[ast.AstNode]) -> ast.AssertStmt:
            """Grammar rule.

            assert_stmt: KW_ASSERT expression (COMMA expression)?
            """
            condition = kid[1]
            error_msg = kid[3] if len(kid) > 3 else None
            if isinstance(condition, ast.ExprType) and (
                isinstance(error_msg, ast.ExprType) or not error_msg
            ):
                return ast.AssertStmt(
                    condition=condition,
                    error_msg=error_msg,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def ctrl_stmt(self, kid: list[ast.AstNode]) -> ast.CtrlStmt:
            """Grammar rule.

            ctrl_stmt: KW_SKIP | KW_BREAK | KW_CONTINUE
            """
            if isinstance(kid[0], ast.Token):
                return ast.CtrlStmt(
                    ctrl=kid[0],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def delete_stmt(self, kid: list[ast.AstNode]) -> ast.DeleteStmt:
            """Grammar rule.

            delete_stmt: KW_DELETE expression
            """
            if isinstance(kid[1], ast.ExprType):
                return ast.DeleteStmt(
                    target=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def report_stmt(self, kid: list[ast.AstNode]) -> ast.ReportStmt:
            """Grammar rule.

            report_stmt: KW_REPORT expression
            """
            if isinstance(kid[1], ast.ExprType):
                return ast.ReportStmt(
                    expr=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def return_stmt(self, kid: list[ast.AstNode]) -> ast.ReturnStmt:
            """Grammar rule.

            return_stmt: KW_RETURN expression?
            """
            if len(kid) > 1:
                if isinstance(kid[1], ast.ExprType) or not kid[1]:
                    return ast.ReturnStmt(
                        expr=kid[1],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            else:
                return ast.ReturnStmt(
                    expr=None,
                    mod_link=self.mod_link,
                    kid=kid,
                )

        def yield_stmt(self, kid: list[ast.AstNode]) -> ast.YieldStmt:
            """Grammar rule.

            yield_stmt: KW_YIELD expression?
            """
            if len(kid) > 1:
                if isinstance(kid[1], ast.ExprType) or not kid[1]:
                    return ast.YieldStmt(
                        expr=kid[1],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            else:
                return ast.YieldStmt(
                    expr=None,
                    mod_link=self.mod_link,
                    kid=kid,
                )

        def walker_stmt(self, kid: list[ast.AstNode]) -> ast.CodeBlockStmt:
            """Grammar rule.

            walker_stmt: disengage_stmt | revisit_stmt | visit_stmt | ignore_stmt
            """
            if isinstance(kid[0], ast.CodeBlockStmt):
                return kid[0]
            else:
                raise self.ice()

        def ignore_stmt(self, kid: list[ast.AstNode]) -> ast.IgnoreStmt:
            """Grammar rule.

            ignore_stmt: KW_IGNORE expression SEMI
            """
            if isinstance(kid[1], ast.ExprType):
                return ast.IgnoreStmt(
                    target=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def visit_stmt(self, kid: list[ast.AstNode]) -> ast.VisitStmt:
            """Grammar rule.

            visit_stmt: KW_VISIT (sub_name_dotted)? expression (else_stmt | SEMI)
            """
            sub_name = kid[1] if isinstance(kid[1], ast.SubTag) else None
            target = kid[2] if sub_name else kid[1]
            else_body = kid[-1] if isinstance(kid[-1], ast.ElseStmt) else None
            if isinstance(target, ast.ExprType):
                return ast.VisitStmt(
                    vis_type=sub_name,
                    target=target,
                    else_body=else_body,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def revisit_stmt(self, kid: list[ast.AstNode]) -> ast.RevisitStmt:
            """Grammar rule.

            revisit_stmt: KW_REVISIT expression? (else_stmt | SEMI)
            """
            target = kid[1] if isinstance(kid[1], ast.ExprType) else None
            else_body = kid[-1] if isinstance(kid[-1], ast.ElseStmt) else None
            return ast.RevisitStmt(
                hops=target,
                else_body=else_body,
                mod_link=self.mod_link,
                kid=kid,
            )

        def disengage_stmt(self, kid: list[ast.AstNode]) -> ast.DisengageStmt:
            """Grammar rule.

            disengage_stmt: KW_DISENGAGE SEMI
            """
            return ast.DisengageStmt(
                mod_link=self.mod_link,
                kid=kid,
            )

        def await_stmt(self, kid: list[ast.AstNode]) -> ast.AwaitStmt:
            """Grammar rule.

            await_stmt: KW_AWAIT expression
            """
            if isinstance(kid[1], ast.ExprType):
                return ast.AwaitStmt(
                    target=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def assignment(self, kid: list[ast.AstNode]) -> ast.Assignment:
            """Grammar rule.

            assignment: KW_FREEZE? atom EQ expression
            """
            is_frozen = isinstance(kid[0], ast.Token) and kid[0].name == Tok.KW_FREEZE
            target = kid[1] if is_frozen else kid[0]
            value = kid[-1]
            if isinstance(target, ast.AtomType) and isinstance(value, ast.ExprType):
                return ast.Assignment(
                    target=target,
                    value=value,
                    mutable=not is_frozen,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def expression(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            expression: pipe KW_IF expression KW_ELSE expression
                      | pipe
            """
            if len(kid) > 1:
                if (
                    isinstance(kid[0], ast.ExprType)
                    and isinstance(kid[2], ast.ExprType)
                    and isinstance(kid[4], ast.ExprType)
                ):
                    return ast.IfElseExpr(
                        value=kid[0],
                        condition=kid[2],
                        else_value=kid[4],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.ExprType):
                return kid[0]
            else:
                raise self.ice()

        def binary_expr(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Binary expression helper."""
            if len(kid) > 1:
                if (
                    isinstance(kid[0], ast.ExprType)
                    and isinstance(
                        kid[1], (ast.Constant, ast.DisconnectOp, ast.ConnectOp)
                    )
                    and isinstance(kid[2], ast.ExprType)
                ):
                    return ast.BinaryExpr(
                        left=kid[0],
                        op=kid[1],
                        right=kid[2],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.ExprType):
                return kid[0]
            else:
                raise self.ice()

        def pipe(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            pipe: pipe_back PIPE_FWD pipe
                | pipe_back
            """
            return self.binary_expr(kid)

        def pipe_back(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            pipe_back: elvis_check PIPE_BKWD pipe_back
                     | elvis_check
            """
            return self.binary_expr(kid)

        def elvis_check(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            elvis_check: bitwise_or ELVIS_OP elvis_check
                       | bitwise_or
            """
            return self.binary_expr(kid)

        def bitwise_or(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            bitwise_or: bitwise_xor BW_OR bitwise_or
                      | bitwise_xor
            """
            return self.binary_expr(kid)

        def bitwise_xor(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            bitwise_xor: bitwise_and BW_XOR bitwise_xor
                       | bitwise_and
            """
            return self.binary_expr(kid)

        def bitwise_and(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            bitwise_and: shift BW_AND bitwise_and
                       | shift
            """
            return self.binary_expr(kid)

        def shift(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            shift: logical RSHIFT shift
                 | logical LSHIFT shift
                 | logical
            """
            return self.binary_expr(kid)

        def logical(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            logical: NOT logical
                   | compare KW_OR logical
                   | compare KW_AND logical
                   | compare
            """
            if len(kid) == 2:
                if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.ExprType):
                    return ast.UnaryExpr(
                        op=kid[0],
                        operand=kid[1],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            return self.binary_expr(kid)

        def compare(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            compare: arithmetic cmp_op compare
                   | arithmetic
            """
            return self.binary_expr(kid)

        def arithmetic(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            arithmetic: term MINUS arithmetic
                      | term PLUS arithmetic
                      | term
            """
            return self.binary_expr(kid)

        def term(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            term: factor MOD term
                 | factor DIV term
                 | factor FLOOR_DIV term
                 | factor STAR_MUL term
                 | factor
            """
            return self.binary_expr(kid)

        def factor(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            factor: power
                  | BW_NOT factor
                  | MINUS factor
                  | PLUS factor
            """
            if len(kid) == 2:
                if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.ExprType):
                    return ast.UnaryExpr(
                        op=kid[0],
                        operand=kid[1],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            return self.binary_expr(kid)

        def power(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            power: connect STAR_POW power
                  | connect
            """
            return self.binary_expr(kid)

        def connect(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            connect: atomic_pipe
                   | atomic_pipe connect_op connect
                   | atomic_pipe disconnect_op connect
            """
            return self.binary_expr(kid)

        def atomic_pipe(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            atomic_pipe: atomic_pipe_back
                       | atomic_pipe KW_SPAWN atomic_pipe_back
                       | atomic_pipe A_PIPE_FWD atomic_pipe_back
            """
            return self.binary_expr(kid)

        def atomic_pipe_back(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            atomic_pipe_back: unpack
                            | atomic_pipe_back A_PIPE_BKWD unpack
            """
            return self.binary_expr(kid)

        def unpack(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            unpack: ref
                  | STAR_MUL atom
                  | STAR_POW atom
            """
            if len(kid) == 2:
                if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.AtomType):
                    return ast.UnaryExpr(
                        op=kid[0],
                        operand=kid[1],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            return self.binary_expr(kid)

        def ref(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            ref: walrus_assign
               | BW_AND walrus_assign
            """
            if len(kid) == 2:
                if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.ExprType):
                    return ast.UnaryExpr(
                        op=kid[0],
                        operand=kid[1],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            return self.binary_expr(kid)

        def walrus_assign(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            walrus_assign: ds_call walrus_op walrus_assign
                         | ds_call
            """
            return self.binary_expr(kid)

        def ds_call(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            ds_call: atom
                   | PIPE_FWD atom
                   | A_PIPE_FWD atom
                   | KW_SPAWN atom
            """
            if len(kid) == 2:
                if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.ExprType):
                    return ast.UnaryExpr(
                        op=kid[0],
                        operand=kid[1],
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            return self.binary_expr(kid)

        def walrus_op(self, kid: list[ast.AstNode]) -> ast.Token:
            """Grammar rule.

            walrus_op: RSHIFT_EQ
                     | LSHIFT_EQ
                     | BW_NOT_EQ
                     | BW_XOR_EQ
                     | BW_OR_EQ
                     | BW_AND_EQ
                     | MOD_EQ
                     | DIV_EQ
                     | FLOOR_DIV_EQ
                     | MUL_EQ
                     | SUB_EQ
                     | ADD_EQ
                     | WALRUS_EQ
            """
            if isinstance(kid[0], ast.Token):
                return kid[0]
            else:
                raise self.ice()

        def cmp_op(self, kid: list[ast.AstNode]) -> ast.Token:
            """Grammar rule.

            cmp_op: KW_ISN
                  | KW_IS
                  | KW_NIN
                  | KW_IN
                  | NE
                  | GTE
                  | LTE
                  | GT
                  | LT
                  | EE
            """
            if isinstance(kid[0], ast.Token):
                return kid[0]
            else:
                raise self.ice()

        def atom(self, kid: list[ast.AstNode]) -> ast.ExprType:
            """Grammar rule.

            atom: edge_op_ref
                 | any_ref
                 | atomic_chain
                 | LPAREN expression RPAREN
                 | atom_collection
                 | atom_literal
            """
            if len(kid) == 1:
                if isinstance(kid[0], ast.AtomType):
                    return kid[0]
                else:
                    raise self.ice()
            elif len(kid) == 3:
                if (
                    isinstance(kid[0], ast.Token)
                    and isinstance(kid[1], ast.ExprType)
                    and isinstance(kid[2], ast.Token)
                ):
                    kid[1].add_kids_left([kid[0]])
                    kid[1].add_kids_right([kid[2]])
                    return kid[1]
                else:
                    raise self.ice()
            else:
                raise self.ice()

        def atom_literal(self, kid: list[ast.AstNode]) -> ast.AtomType:
            """Grammar rule.

            atom_literal: builtin_type
                        | NULL
                        | BOOL
                        | multistring
                        | FLOAT
                        | OCT
                        | BIN
                        | HEX
                        | INT
            """
            if isinstance(kid[0], ast.AtomType):
                return kid[0]
            else:
                raise self.ice()

        def atom_collection(self, kid: list[ast.AstNode]) -> ast.AtomType:
            """Grammar rule.

            atom_collection: dict_compr
                           | set_compr
                           | gen_compr
                           | list_compr
                           | dict_val
                           | set_val
                           | tuple_val
                           | list_val
            """
            if isinstance(kid[0], ast.AtomType):
                return kid[0]
            else:
                raise self.ice()

        def multistring(self, kid: list[ast.AstNode]) -> ast.AtomType:
            """Grammar rule.

            multistring: (fstring | STRING)+
            """
            valid_strs = [i for i in kid if isinstance(i, (ast.Constant, ast.FString))]
            if len(valid_strs) == len(kid):
                return ast.MultiString(
                    strings=valid_strs,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def fstring(self, kid: list[ast.AstNode]) -> ast.FString:
            """Grammar rule.

            fstring: FSTR_START fstr_parts FSTR_END
            """
            if len(kid) == 2:
                return ast.FString(
                    parts=None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            elif isinstance(kid[1], ast.SubNodeList):
                return ast.FString(
                    parts=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def fstr_parts(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.Constant | ast.ExprType]:
            """Grammar rule.

            fstr_parts: (FSTR_PIECE | FSTR_BESC | LBRACE expression RBRACE | fstring)*
            """
            valid_types = Union[ast.Constant, ast.ExprType]
            valid_parts = [i for i in kid if isinstance(i, valid_types)]
            if len(valid_parts) == len(kid):
                return ast.SubNodeList[ast.Constant | ast.ExprType](
                    items=valid_parts,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def list_val(self, kid: list[ast.AstNode]) -> ast.ListVal:
            """Grammar rule.

            list_val: LSQUARE expr_list? RSQUARE
            """
            if len(kid) == 2:
                return ast.ListVal(
                    values=None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            elif isinstance(kid[1], ast.SubNodeList):
                return ast.ListVal(
                    values=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def tuple_val(self, kid: list[ast.AstNode]) -> ast.TupleVal:
            """Grammar rule.

            tuple_val: LPAREN tuple_list? RPAREN
            """
            if len(kid) == 2:
                return ast.TupleVal(
                    values=None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            elif isinstance(kid[1], ast.SubNodeList):
                return ast.TupleVal(
                    values=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def set_val(self, kid: list[ast.AstNode]) -> ast.SetVal:
            """Grammar rule.

            set_val: LBRACE expr_list RBRACE
            """
            if len(kid) == 2:
                return ast.SetVal(
                    values=None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            elif isinstance(kid[1], ast.SubNodeList):
                return ast.SetVal(
                    values=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def expr_list(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.ExprType]:
            """Grammar rule.

            expr_list: (expr_list COMMA)? expression
            """
            consume = None
            expr = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                expr = kid[2]
            else:
                expr = kid[0]
            new_kid = [expr, comma, *consume.kid] if consume else [expr]
            valid_kid = [i for i in new_kid if isinstance(i, ast.ExprType)]
            return ast.SubNodeList[ast.ExprType](
                items=valid_kid,
                mod_link=self.mod_link,
                kid=kid,
            )

        def tuple_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ExprType | ast.Assignment]:
            """Grammar rule.

            tuple_list: expression COMMA expr_list COMMA assignment_list
                      | expression COMMA assignment_list
                      | expression COMMA expr_list
                      | expression COMMA
                      | assignment_list
            """
            chomp = [*kid]
            first_expr = None
            if isinstance(chomp[0], ast.SubNodeList):
                return chomp[0]
            else:
                first_expr = chomp[0]
                chomp = chomp[2:]
            expr_list = chomp[0].kid
            chomp = chomp[1:]
            if len(chomp):
                chomp = chomp[1:]
                expr_list = [*expr_list, *chomp[0].kid]
            expr_list = [first_expr, *expr_list]
            valid_type = Union[ast.ExprType, ast.Assignment]
            valid_kid = [i for i in expr_list if isinstance(i, valid_type)]
            if len(valid_kid) == len(expr_list):
                return ast.SubNodeList[ast.ExprType | ast.Assignment](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def dict_val(self, kid: list[ast.AstNode]) -> ast.DictVal:
            """Grammar rule.

            dict_val: LBRACE kv_pairs? RBRACE
            """
            if len(kid) == 2:
                return ast.DictVal(
                    kv_pairs=None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            elif isinstance(kid[1], ast.SubNodeList):
                return ast.DictVal(
                    kv_pairs=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def kv_pairs(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.KVPair]:
            """Grammar rule.

            kv_pairs: (kv_pairs COMMA)? kv_pair
            """
            consume = None
            kv_pair = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                kv_pair = kid[2]
            else:
                kv_pair = kid[0]
            new_kid = [kv_pair, comma, *consume.kid] if consume else [kv_pair]
            valid_kid = [i for i in new_kid if isinstance(i, ast.KVPair)]
            return ast.SubNodeList[ast.KVPair](
                items=valid_kid,
                mod_link=self.mod_link,
                kid=kid,
            )

        def kv_pair(self, kid: list[ast.AstNode]) -> ast.KVPair:
            """Grammar rule.

            kv_pair: expression COLON expression
            """
            if isinstance(kid[0], ast.ExprType) and isinstance(kid[2], ast.ExprType):
                return ast.KVPair(
                    key=kid[0],
                    value=kid[2],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def list_compr(self, kid: list[ast.AstNode]) -> ast.ListCompr:
            """Grammar rule.

            list_compr: LSQUARE inner_compr RSQUARE
            """
            if isinstance(kid[1], ast.InnerCompr):
                return ast.ListCompr(
                    compr=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def gen_compr(self, kid: list[ast.AstNode]) -> ast.GenCompr:
            """Grammar rule.

            gen_compr: LPAREN inner_compr RPAREN
            """
            if isinstance(kid[1], ast.InnerCompr):
                return ast.GenCompr(
                    compr=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def set_compr(self, kid: list[ast.AstNode]) -> ast.SetCompr:
            """Grammar rule.

            set_compr: LBRACE inner_compr RBRACE
            """
            if isinstance(kid[1], ast.InnerCompr):
                return ast.SetCompr(
                    compr=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def inner_compr(self, kid: list[ast.AstNode]) -> ast.InnerCompr:
            """Grammar rule.

            inner_compr: expression KW_FOR name_list KW_IN walrus_assign (KW_IF expression)?
            """
            if (
                isinstance(kid[0], ast.ExprType)
                and isinstance(kid[2], ast.SubNodeList)
                and isinstance(kid[4], ast.ExprType)
            ):
                return ast.InnerCompr(
                    out_expr=kid[0],
                    names=kid[2],
                    collection=kid[4],
                    conditional=kid[6]
                    if len(kid) > 5 and isinstance(kid[6], ast.ExprType)
                    else None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def dict_compr(self, kid: list[ast.AstNode]) -> ast.DictCompr:
            """Grammar rule.

            dict_compr: LBRACE kv_pair KW_FOR name_list KW_IN walrus_assign (KW_IF expression)? RBRACE
            """
            if (
                isinstance(kid[1], ast.KVPair)
                and isinstance(kid[3], ast.SubNodeList)
                and isinstance(kid[5], ast.ExprType)
            ):
                return ast.DictCompr(
                    kv_pair=kid[1],
                    names=kid[3],
                    collection=kid[5],
                    conditional=kid[7]
                    if len(kid) > 6 and isinstance(kid[7], ast.AtomType)
                    else None,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def atomic_chain(self, kid: list[ast.AstNode]) -> ast.AtomType:
            """Grammar rule.

            atomic_chain: atomic_call
                        | atomic_chain_unsafe
                        | atomic_chain_safe
            """
            if isinstance(kid[0], ast.AtomType):
                return kid[0]
            else:
                raise self.ice()

        def atomic_chain_unsafe(self, kid: list[ast.AstNode]) -> ast.AtomType:
            """Grammar rule.

            atomic_chain_unsafe: atom (filter_compr | edge_op_ref | index_slice)
                               | atom (DOT_BKWD | DOT_FWD | DOT) any_ref
            """
            if len(kid) == 2:
                if isinstance(kid[0], ast.AtomType) and isinstance(
                    kid[1], (ast.FilterCompr, ast.EdgeOpRef, ast.IndexSlice)
                ):
                    return ast.AtomTrailer(
                        target=kid[0],
                        right=kid[1],
                        null_ok=False,
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            elif len(kid) == 3:
                if (
                    isinstance(kid[0], ast.AtomType)
                    and isinstance(kid[1], ast.Token)
                    and isinstance(kid[2], ast.AtomType)
                ):
                    return ast.AtomTrailer(
                        target=kid[0] if kid[1].name != Tok.DOT_BKWD else kid[2],
                        right=kid[2] if kid[1].name != Tok.DOT_BKWD else kid[0],
                        null_ok=False,
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            else:
                raise self.ice()

        def atomic_chain_safe(self, kid: list[ast.AstNode]) -> ast.AtomType:
            """Grammar rule.

            atomic_chain_safe: atom NULL_OK (filter_compr | edge_op_ref | index_slice)
                             | atom NULL_OK (DOT_BKWD | DOT_FWD | DOT) any_ref
            """
            if len(kid) == 3:
                if isinstance(kid[0], ast.AtomType) and isinstance(
                    kid[2], (ast.FilterCompr, ast.EdgeOpRef, ast.IndexSlice)
                ):
                    return ast.AtomTrailer(
                        target=kid[0],
                        right=kid[2],
                        null_ok=True,
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            elif len(kid) == 4:
                if (
                    isinstance(kid[0], ast.AtomType)
                    and isinstance(kid[1], ast.Token)
                    and isinstance(kid[3], ast.AtomType)
                ):
                    return ast.AtomTrailer(
                        target=kid[0] if kid[1].name != Tok.DOT_BKWD else kid[3],
                        right=kid[3] if kid[1].name != Tok.DOT_BKWD else kid[0],
                        null_ok=True,
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            else:
                raise self.ice()

        def atomic_call(self, kid: list[ast.AstNode]) -> ast.FuncCall:
            """Grammar rule.

            atomic_call: atom LPAREN param_list? RPAREN
            """
            if (
                len(kid) == 4
                and isinstance(kid[0], ast.AtomType)
                and isinstance(kid[2], ast.SubNodeList)
            ):
                return ast.FuncCall(
                    target=kid[0], params=kid[2], mod_link=self.mod_link, kid=kid
                )
            elif len(kid) == 1 and isinstance(kid[0], ast.AtomType):
                return ast.FuncCall(
                    target=kid[0], params=None, mod_link=self.mod_link, kid=kid
                )
            else:
                raise self.ice()

        def param_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ExprType | ast.Assignment]:
            """Grammar rule.

            param_list: (expr_list COMMA assignment_list) | assignment_list | expr_list
            """
            if len(kid) == 1:
                if isinstance(kid[0], ast.SubNodeList):
                    return kid[0]
                else:
                    raise self.ice()
            else:
                valid_type = Union[ast.ExprType, ast.Assignment]
                valid_kid = [
                    i for i in [*kid[0].kid, *kid[2].kid] if isinstance(i, valid_type)
                ]
                if len(valid_kid) == len(kid[0].kid) + len(kid[2].kid):
                    return ast.SubNodeList[ast.ExprType | ast.Assignment](
                        items=valid_kid,
                        mod_link=self.mod_link,
                        kid=kid,
                    )
                else:
                    raise self.ice()

        def assignment_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.Assignment]:
            """Grammar rule.

            assignment_list: assignment_list COMMA assignment | assignment
            """
            consume = None
            assign = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                assign = kid[2]
            else:
                assign = kid[0]
            new_kid = [assign, comma, *consume.kid] if consume else [assign]
            valid_kid = [i for i in new_kid if isinstance(i, ast.Assignment)]
            return ast.SubNodeList[ast.Assignment](
                items=valid_kid,
                mod_link=self.mod_link,
                kid=kid,
            )

        def index_slice(self, kid: list[ast.AstNode]) -> ast.IndexSlice:
            """Grammar rule.

            index_slice: LSQUARE expression? (COLON expression?)? RSQUARE
            """
            if len(kid) == 2:
                return ast.IndexSlice(
                    start=None,
                    stop=None,
                    is_range=False,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            expr1 = kid[1]
            expr2 = None
            if len(kid) > 3:
                expr2 = kid[3]
            if isinstance(expr1, ast.ExprType) and (
                isinstance(expr2, ast.ExprType) or expr2 is None
            ):
                return ast.IndexSlice(
                    start=expr1,
                    stop=expr2,
                    is_range=True,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def arch_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            arch_ref: object_ref
                    | walker_ref
                    | edge_ref
                    | node_ref
            """
            if isinstance(kid[0], ast.ArchRef):
                return kid[0]
            else:
                raise self.ice()

        def node_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            node_ref: NODE_OP NAME
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameType):
                return ast.ArchRef(
                    arch=kid[0],
                    name_ref=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def edge_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            edge_ref: EDGE_OP NAME
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameType):
                return ast.ArchRef(
                    arch=kid[0],
                    name_ref=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def walker_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            walker_ref: WALKER_OP NAME
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameType):
                return ast.ArchRef(
                    arch=kid[0],
                    name_ref=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def object_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            object_ref: OBJECT_OP esc_name
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameType):
                return ast.ArchRef(
                    arch=kid[0],
                    name_ref=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def enum_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            enum_ref: ENUM_OP NAME
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameType):
                return ast.ArchRef(
                    arch=kid[0],
                    name_ref=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def ability_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            ability_ref: ABILITY_OP (special_ref | esc_name)
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameType):
                return ast.ArchRef(
                    arch=kid[0],
                    name_ref=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def global_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            global_ref: GLOBAL_OP esc_name
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameType):
                return ast.ArchRef(
                    arch=kid[0],
                    name_ref=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def arch_or_ability_chain(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ArchRef]:
            """Grammar rule.

            arch_or_ability_chain: arch_or_ability_chain? (ability_ref | arch_ref)
            """
            consume = None
            name = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                name = kid[1]
            else:
                name = kid[0]
            new_kid = [name, *consume.kid] if consume else [name]
            valid_kid = [i for i in new_kid if isinstance(i, ast.ArchRef)]
            if len(valid_kid) == len(new_kid):
                return ast.SubNodeList[ast.ArchRef](
                    items=valid_kid,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def abil_to_arch_chain(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ArchRef]:
            """Grammar rule.

            abil_to_arch_chain: arch_or_ability_chain? arch_ref
            """
            if len(kid) == 2:
                if isinstance(kid[1], ast.ArchRef) and isinstance(
                    kid[0], ast.SubNodeList
                ):
                    return ast.SubNodeList[ast.ArchRef](
                        items=[*(kid[0].items), kid[1]],
                        mod_link=self.mod_link,
                        kid=[*(kid[0].kid), kid[1]],
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.SubNodeList):
                return kid[0]
            else:
                raise self.ice()

        def arch_to_abil_chain(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ArchRef]:
            """Grammar rule.

            arch_to_abil_chain: arch_or_ability_chain? ability_ref
            """
            if len(kid) == 2:
                if isinstance(kid[1], ast.ArchRef) and isinstance(
                    kid[0], ast.SubNodeList
                ):
                    return ast.SubNodeList[ast.ArchRef](
                        items=[*(kid[0].items), kid[1]],
                        mod_link=self.mod_link,
                        kid=[*(kid[0].kid), kid[1]],
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.SubNodeList):
                return kid[0]
            else:
                raise self.ice()

        def arch_to_enum_chain(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ArchRef | ast.EnumDef]:
            """Grammar rule.

            arch_to_enum_chain: arch_or_ability_chain? enum_ref
            """
            if len(kid) == 2:
                if isinstance(kid[1], ast.EnumDef) and isinstance(
                    kid[0], ast.SubNodeList
                ):
                    return ast.SubNodeList[ast.ArchRef | ast.EnumDef](
                        items=[*(kid[0].items), kid[1]],
                        mod_link=self.mod_link,
                        kid=[*(kid[0].kid), kid[1]],
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.SubNodeList):
                return kid[0]
            else:
                raise self.ice()

        def edge_op_ref(self, kid: list[ast.AstNode]) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_op_ref: edge_any
                       | edge_from
                       | edge_to
            """
            if isinstance(kid[0], ast.EdgeOpRef):
                return kid[0]
            else:
                raise self.ice()

        def edge_to(self, kid: list[ast.AstNode]) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_to: ARROW_R_P1 expression (COLON filter_compare_list)? ARROW_R_P2
                   | ARROW_R
            """
            ftype = kid[1] if len(kid) >= 3 else None
            fcond = kid[3] if len(kid) >= 5 else None
            if isinstance(ftype, ast.ExprType) and (
                isinstance(fcond, ast.FilterCompr) or fcond is None
            ):
                return ast.EdgeOpRef(
                    filter_type=ftype,
                    filter_cond=fcond,
                    edge_dir=EdgeDir.OUT,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def edge_from(self, kid: list[ast.AstNode]) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_from: ARROW_L_P1 expression (COLON filter_compare_list)? ARROW_L_P2
                     | ARROW_L
            """
            ftype = kid[1] if len(kid) >= 3 else None
            fcond = kid[3] if len(kid) >= 5 else None
            if isinstance(ftype, ast.ExprType) and (
                isinstance(fcond, ast.FilterCompr) or fcond is None
            ):
                return ast.EdgeOpRef(
                    filter_type=ftype,
                    filter_cond=fcond,
                    edge_dir=EdgeDir.IN,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def edge_any(self, kid: list[ast.AstNode]) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_any: ARROW_L_P1 expression (COLON filter_compare_list)? ARROW_R_P2
                    | ARROW_BI
            """
            ftype = kid[1] if len(kid) >= 3 else None
            fcond = kid[3] if len(kid) >= 5 else None
            if isinstance(ftype, ast.ExprType) and (
                isinstance(fcond, ast.FilterCompr) or fcond is None
            ):
                return ast.EdgeOpRef(
                    filter_type=ftype,
                    filter_cond=fcond,
                    edge_dir=EdgeDir.ANY,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def connect_op(self, kid: list[ast.AstNode]) -> ast.ConnectOp:
            """Grammar rule.

            connect_op: connect_from
                      | connect_to
            """
            if isinstance(kid[0], ast.ConnectOp):
                return kid[0]
            else:
                raise self.ice()

        def disconnect_op(self, kid: list[ast.AstNode]) -> ast.DisconnectOp:
            """Grammar rule.

            disconnect_op: NOT edge_op_ref
            """
            if isinstance(kid[1], ast.EdgeOpRef):
                return ast.DisconnectOp(
                    edge_spec=kid[1],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def connect_to(self, kid: list[ast.AstNode]) -> ast.ConnectOp:
            """Grammar rule.

            connect_to: CARROW_R_P1 expression (COLON assignment_list)? CARROW_R_P2
                      | CARROW_R
            """
            conn_type = kid[1] if len(kid) >= 3 else None
            conn_assign = kid[3] if len(kid) >= 5 else None
            if isinstance(conn_type, ast.ExprType) and (
                isinstance(conn_assign, ast.SubNodeList) or conn_assign is None
            ):
                return ast.ConnectOp(
                    conn_type=conn_type,
                    conn_assign=conn_assign,
                    edge_dir=EdgeDir.OUT,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def connect_from(self, kid: list[ast.AstNode]) -> ast.ConnectOp:
            """Grammar rule.

            connect_from: CARROW_L_P1 expression (COLON assignment_list)? CARROW_L_P2
                        | CARROW_L
            """
            conn_type = kid[1] if len(kid) >= 3 else None
            conn_assign = kid[3] if len(kid) >= 5 else None
            if isinstance(conn_type, ast.ExprType) and (
                isinstance(conn_assign, ast.SubNodeList) or conn_assign is None
            ):
                return ast.ConnectOp(
                    conn_type=conn_type,
                    conn_assign=conn_assign,
                    edge_dir=EdgeDir.IN,
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def filter_compr(self, kid: list[ast.AstNode]) -> ast.FilterCompr:
            """Grammar rule.

            filter_compr: LPAREN EQ filter_compare_list RPAREN
            """
            if isinstance(kid[2], ast.SubNodeList):
                return ast.FilterCompr(
                    compares=kid[2],
                    mod_link=self.mod_link,
                    kid=kid,
                )
            else:
                raise self.ice()

        def filter_compare_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.BinaryExpr]:
            """Grammar rule.

            filter_compare_list: (filter_compare_list COMMA)? filter_compare_item
            """
            consume = None
            expr = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                expr = kid[2]
            else:
                expr = kid[0]
            new_kid = [expr, comma, *consume.kid] if consume else [expr]
            valid_kid = [i for i in new_kid if isinstance(i, ast.BinaryExpr)]
            return ast.SubNodeList[ast.BinaryExpr](
                items=valid_kid,
                mod_link=self.mod_link,
                kid=kid,
            )

        def filter_compare_item(self, kid: list[ast.AstNode]) -> ast.BinaryExpr:
            """Grammar rule.

            filter_compare_item: esc_name cmp_op expression
            """
            ret = self.binary_expr(kid)
            if isinstance(ret, ast.BinaryExpr):
                return ret
            else:
                raise self.ice()

        def __default_token__(self, token: jl.Token) -> ast.Token:
            """Token handler."""
            ret_type = ast.Token
            if token.type in [Tok.NAME, Tok.KWESC_NAME]:
                ret_type = ast.Name
            elif token.type in [
                Tok.FLOAT,
                Tok.INT,
                Tok.HEX,
                Tok.BIN,
                Tok.OCT,
                Tok.STRING,
                Tok.FSTR_BESC,
                Tok.FSTR_PIECE,
            ]:
                ret_type = ast.Constant

            return ret_type(
                name=token.type,
                value=token.value,
                line=token.line if token.line is not None else 0,
                col_start=token.column if token.column is not None else 0,
                col_end=token.end_column if token.end_column is not None else 0,
                pos_start=token.start_pos if token.start_pos is not None else 0,
                pos_end=token.end_pos if token.end_pos is not None else 0,
                mod_link=self.mod_link,
                kid=[],
            )

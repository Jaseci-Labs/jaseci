"""Lark parser for Jac Lang."""

from __future__ import annotations

import keyword
import logging
import os
from typing import Callable, TypeAlias, TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler import jac_lark as jl  # type: ignore
from jaclang.compiler.constant import EdgeDir, Tokens as Tok
from jaclang.compiler.passes.ir_pass import Pass
from jaclang.vendor.lark import Lark, Transformer, Tree, logger


T = TypeVar("T", bound=ast.AstNode)


class JacParser(Pass):
    """Jac Parser."""

    dev_mode = False

    def __init__(self, input_ir: ast.JacSource) -> None:
        """Initialize parser."""
        self.source = input_ir
        self.mod_path = input_ir.loc.mod_path
        self.node_list: list[ast.AstNode] = []
        if JacParser.dev_mode:
            JacParser.make_dev()
        Pass.__init__(self, input_ir=input_ir, prior=None)

    def transform(self, ir: ast.AstNode) -> ast.Module:
        """Transform input IR."""
        try:
            tree, comments = JacParser.parse(
                self.source.value, on_error=self.error_callback
            )
            mod = JacParser.TreeToAST(parser=self).transform(tree)
            self.source.comments = [self.proc_comment(i, mod) for i in comments]
            if isinstance(mod, ast.Module):
                return mod
            else:
                raise self.ice()
        except jl.UnexpectedInput as e:
            catch_error = ast.EmptyToken()
            catch_error.orig_src = self.source
            catch_error.line_no = e.line
            catch_error.end_line = e.line
            catch_error.c_start = e.column
            catch_error.c_end = e.column + 1
            catch_error.pos_start = e.pos_in_stream or 0
            catch_error.pos_end = catch_error.pos_start + 1

            error_msg = "Syntax Error"
            if len(e.args) >= 1 and isinstance(e.args[0], str):
                error_msg += e.args[0]
            self.error(error_msg, node_override=catch_error)

        except Exception as e:
            self.error(f"Internal Error: {e}")

        return ast.Module(
            name="",
            source=self.source,
            doc=None,
            body=[],
            terminals=[],
            is_imported=False,
            kid=[ast.EmptyToken()],
        )

    @staticmethod
    def proc_comment(token: jl.Token, mod: ast.AstNode) -> ast.CommentToken:
        """Process comment."""
        return ast.CommentToken(
            orig_src=mod.loc.orig_src,
            name=token.type,
            value=token.value,
            line=token.line or 0,
            end_line=token.end_line or 0,
            col_start=token.column or 0,
            col_end=token.end_column or 0,
            pos_start=token.start_pos or 0,
            pos_end=token.end_pos or 0,
            kid=[],
        )

    def error_callback(self, e: jl.UnexpectedInput) -> bool:
        """Handle error."""
        return False

    @staticmethod
    def _comment_callback(comment: jl.Token) -> None:
        JacParser.comment_cache.append(comment)

    @staticmethod
    def parse(
        ir: str, on_error: Callable[[jl.UnexpectedInput], bool]
    ) -> tuple[jl.Tree[jl.Tree[str]], list[jl.Token]]:
        """Parse input IR."""
        JacParser.comment_cache = []
        return (
            JacParser.parser.parse(ir, on_error=on_error),
            JacParser.comment_cache,
        )

    @staticmethod
    def make_dev() -> None:
        """Make parser in dev mode."""
        JacParser.parser = Lark.open(
            "jac.lark",
            parser="lalr",
            rel_to=__file__,
            debug=True,
            lexer_callbacks={"COMMENT": JacParser._comment_callback},
        )
        JacParser.JacTransformer = Transformer[Tree[str], ast.AstNode]  # type: ignore
        logger.setLevel(logging.DEBUG)

    comment_cache: list[jl.Token] = []

    parser = jl.Lark_StandAlone(lexer_callbacks={"COMMENT": _comment_callback})  # type: ignore
    JacTransformer: TypeAlias = jl.Transformer[jl.Tree[str], ast.AstNode]

    class TreeToAST(JacTransformer):
        """Transform parse tree to AST."""

        def __init__(self, parser: JacParser, *args: bool, **kwargs: bool) -> None:
            """Initialize transformer."""
            super().__init__(*args, **kwargs)
            self.parse_ref = parser
            self.terminals: list[ast.Token] = []
            # TODO: Once the kid is removed from the ast, we can get rid of this
            # node_idx and directly pop(0) kid as we process the nodes.
            self.node_idx = 0
            self.nodes: list[ast.AstNode] = []

        def ice(self) -> Exception:
            """Raise internal compiler error."""
            self.parse_ref.error("Internal Compiler Error, Invalid Parse Tree!")
            return RuntimeError(
                f"{self.parse_ref.__class__.__name__} - Internal Compiler Error, Invalid Parse Tree!"
            )

        def _node_update(self, node: T) -> T:
            self.parse_ref.cur_node = node
            if node not in self.parse_ref.node_list:
                self.parse_ref.node_list.append(node)
            return node

        def _call_userfunc(
            self, tree: jl.Tree, new_children: None | list[ast.AstNode] = None
        ) -> ast.AstNode:
            self.nodes = new_children or tree.children  # type: ignore[assignment]
            try:
                return self._node_update(super()._call_userfunc(tree, new_children))
            finally:
                self.nodes = []
                self.node_idx = 0

        def _call_userfunc_token(self, token: jl.Token) -> ast.AstNode:
            return self._node_update(super()._call_userfunc_token(token))

        def _binary_expr_unwind(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Binary expression helper."""
            if len(kid) > 1:
                if (
                    isinstance(kid[0], ast.Expr)
                    and isinstance(
                        kid[1],
                        (ast.Token, ast.DisconnectOp, ast.ConnectOp),
                    )
                    and isinstance(kid[2], ast.Expr)
                ):
                    return ast.BinaryExpr(
                        left=kid[0],
                        op=kid[1],
                        right=kid[2],
                        kid=kid,
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.Expr):
                return kid[0]
            else:
                raise self.ice()

        # ******************************************************************* #
        # Parser Helper functions.                                            #
        # ******************************************************************* #

        def match(self, ty: type[T]) -> T | None:
            """Return a node matching type 'ty' if possible from the current nodes."""
            if (self.node_idx < len(self.nodes)) and isinstance(
                self.nodes[self.node_idx], ty
            ):
                self.node_idx += 1
                return self.nodes[self.node_idx - 1]  # type: ignore[return-value]
            return None

        def consume(self, ty: type[T]) -> T:
            """Consume and return the specified type, if it's not exists, will be an internal compiler error."""
            if node := self.match(ty):
                return node
            raise self.ice()

        def match_token(self, tok: Tok) -> ast.Token | None:
            """Match a token with the given type and return it."""
            if token := self.match(ast.Token):
                if token.name == tok.name:
                    return token
                self.node_idx -= (
                    1  # We're already matched but wrong token so undo matching it.
                )
            return None

        def consume_token(self, tok: Tok) -> ast.Token:
            """Consume a token with the given type and return it."""
            if token := self.match_token(tok):
                return token
            raise self.ice()

        def match_many(self, ty: type[T]) -> list[T]:
            """Match 0 or more of the given type and return the list."""
            nodes: list[ast.AstNode] = []
            while node := self.match(ty):
                nodes.append(node)
            return nodes  # type: ignore[return-value]

        def consume_many(self, ty: type[T]) -> list[T]:
            """Match 1 or more of the given type and return the list."""
            nodes: list[ast.AstNode] = [self.consume(ty)]
            while node := self.match(ty):
                nodes.append(node)
            return nodes  # type: ignore[return-value]

        # ******************************************************************* #
        # Parsing Rules                                                       #
        # ******************************************************************* #

        def start(self, _: None) -> ast.Module:
            """Grammar rule.

            start: module
            """
            module = self.consume(ast.Module)
            module._in_mod_nodes = self.parse_ref.node_list
            return module

        def module(self, _: None) -> ast.Module:
            """Grammar rule.

            module: (doc_tag? element (element_with_doc | element)*)?
            doc_tag (element_with_doc (element_with_doc | element)*)?
            """
            doc = self.match(ast.String)
            body = self.match_many(ast.ElementStmt)
            mod = ast.Module(
                name=self.parse_ref.mod_path.split(os.path.sep)[-1].rstrip(".jac"),
                source=self.parse_ref.source,
                doc=doc,
                body=body,
                is_imported=False,
                terminals=self.terminals,
                kid=(
                    self.nodes
                    or [ast.EmptyToken(ast.JacSource("", self.parse_ref.mod_path))]
                ),
            )
            return mod

        def element_with_doc(self, _: None) -> ast.ElementStmt:
            """Grammar rule.

            element_with_doc: doc_tag element
            """
            doc = self.consume(ast.String)
            element = self.consume(ast.ElementStmt)
            element.doc = doc
            element.add_kids_left([doc])
            return element

        def element(self, _: None) -> ast.ElementStmt:
            """Grammar rule.

            element: py_code_block
                | import_stmt
                | ability
                | architype
                | free_code
                | test
                | global_var
            """
            return self.consume(ast.ElementStmt)

        def global_var(self, _: None) -> ast.GlobalVars:
            """Grammar rule.

            global_var: (KW_LET | KW_GLOBAL) access_tag? assignment_list SEMI
            """
            is_frozen = self.consume(ast.Token).name == Tok.KW_LET
            access_tag = self.match(ast.SubTag)
            assignments = self.consume(ast.SubNodeList)
            self.consume_token(Tok.SEMI)
            return ast.GlobalVars(
                access=access_tag,
                assignments=assignments,
                is_frozen=is_frozen,
                kid=self.nodes,
            )

        def access_tag(self, _: None) -> ast.SubTag[ast.Token]:
            """Grammar rule.

            access_tag: COLON ( KW_PROT | KW_PUB | KW_PRIV )
            """
            self.consume_token(Tok.COLON)
            access = self.consume(ast.Token)
            return ast.SubTag[ast.Token](tag=access, kid=self.nodes)

        def test(self, _: None) -> ast.Test:
            """Grammar rule.

            test: KW_TEST NAME? code_block
            """
            # Q(thakee): Why the name should be KW_TEST if no name present?
            test_tok = self.consume_token(Tok.KW_TEST)
            name = self.match(ast.Name) or test_tok
            codeblock = self.consume(ast.SubNodeList)
            return ast.Test(
                name=name,
                body=codeblock,
                kid=self.nodes,
            )

        def free_code(self, _: None) -> ast.ModuleCode:
            """Grammar rule.

            free_code: KW_WITH KW_ENTRY sub_name? code_block
            """
            self.consume_token(Tok.KW_WITH)
            self.consume_token(Tok.KW_ENTRY)
            name = self.match(ast.SubTag)
            codeblock = self.consume(ast.SubNodeList)
            return ast.ModuleCode(
                name=name,
                body=codeblock,
                kid=self.nodes,
            )

        def doc_tag(self, _: None) -> ast.String:
            """Grammar rule.

            doc_tag: ( STRING | DOC_STRING )
            """
            return self.consume(ast.String)

        def py_code_block(self, _: None) -> ast.PyInlineCode:
            """Grammar rule.

            py_code_block: PYNLINE
            """
            pyinline = self.consume_token(Tok.PYNLINE)
            return ast.PyInlineCode(
                code=pyinline,
                kid=self.nodes,
            )

        def import_stmt(self, _: None) -> ast.Import:
            """Grammar rule.

            import_stmt: KW_IMPORT sub_name? KW_FROM from_path LBRACE import_items RBRACE
                       | KW_IMPORT sub_name? KW_FROM from_path COMMA import_items SEMI  //Deprecated
                       | KW_IMPORT sub_name? import_path (COMMA import_path)* SEMI
                       | include_stmt
            """
            if import_stmt := self.match(ast.Import):  # Include Statement.
                return import_stmt

            # TODO: kid will be removed so let's keep as it is for now.
            kid = self.nodes

            from_path: ast.ModulePath | None = None
            self.consume_token(Tok.KW_IMPORT)
            lang = self.match(ast.SubTag)

            if self.match_token(Tok.KW_FROM):
                from_path = self.consume(ast.ModulePath)
                self.consume(ast.Token)  # LBRACE or COMMA
                items = self.consume(ast.SubNodeList)
                if self.consume(ast.Token).name == Tok.SEMI:  # RBRACE or SEMI
                    self.parse_ref.warning(
                        "Deprecated syntax, use braces for multiple imports (e.g, import from mymod {a, b, c})",
                    )
            else:
                paths = [self.consume(ast.ModulePath)]
                while self.match_token(Tok.COMMA):
                    paths.append(self.consume(ast.ModulePath))
                self.consume_token(Tok.SEMI)
                items = ast.SubNodeList[ast.ModulePath](
                    items=paths,
                    delim=Tok.COMMA,
                    # TODO: kid will be removed so let's keep as it is for now.
                    kid=self.nodes[2 if lang else 1 : -1],
                )
                kid = (kid[:2] if lang else kid[:1]) + [items] + kid[-1:]

            is_absorb = False
            return ast.Import(
                hint=lang,
                from_loc=from_path,
                items=items,
                is_absorb=is_absorb,
                kid=kid,
            )

        def from_path(self, _: None) -> ast.ModulePath:
            """Grammar rule.

            from_path: (DOT | ELLIPSIS)* import_path
                     | (DOT | ELLIPSIS)+
            """
            level = 0
            while True:
                if self.match_token(Tok.DOT):
                    level += 1
                elif self.match_token(Tok.ELLIPSIS):
                    level += 3
                else:
                    break
            if import_path := self.match(ast.ModulePath):
                kids = [i for i in self.nodes if isinstance(i, ast.Token)]
                import_path.level = level
                import_path.add_kids_left(kids)
                return import_path

            return ast.ModulePath(
                path=None,
                level=level,
                alias=None,
                kid=self.nodes,
            )

        def include_stmt(self, _: None) -> ast.Import:
            """Grammar rule.

            include_stmt: KW_INCLUDE sub_name? import_path SEMI
            """
            kid = self.nodes  # TODO: Will be removed.
            self.consume_token(Tok.KW_INCLUDE)
            lang = self.match(ast.SubTag)
            from_path = self.consume(ast.ModulePath)
            items = ast.SubNodeList[ast.ModulePath](
                items=[from_path], delim=Tok.COMMA, kid=[from_path]
            )
            kid = (
                (kid[:2] if lang else kid[:1]) + [items] + kid[-1:]
            )  # TODO: Will be removed.
            is_absorb = True
            return ast.Import(
                hint=lang,
                from_loc=None,
                items=items,
                is_absorb=is_absorb,
                kid=kid,
            )

        def import_path(self, _: None) -> ast.ModulePath:
            """Grammar rule.

            import_path: named_ref (DOT named_ref)* (KW_AS NAME)?
            """
            valid_path = [self.consume(ast.Name)]
            while self.match_token(Tok.DOT):
                valid_path.append(self.consume(ast.Name))
            alias = self.consume(ast.Name) if self.match_token(Tok.KW_AS) else None
            return ast.ModulePath(
                path=valid_path,
                level=0,
                alias=alias,
                kid=self.nodes,
            )

        def import_items(self, _: None) -> ast.SubNodeList[ast.ModuleItem]:
            """Grammar rule.

            import_items: (import_item COMMA)* import_item COMMA?
            """
            items = [self.consume(ast.ModuleItem)]
            while self.match_token(Tok.COMMA):
                if module_item := self.match(ast.ModuleItem):
                    items.append(module_item)
            ret = ast.SubNodeList[ast.ModuleItem](
                items=items,
                delim=Tok.COMMA,
                kid=self.nodes,
            )
            return ret

        def import_item(self, _: None) -> ast.ModuleItem:
            """Grammar rule.

            import_item: named_ref (KW_AS NAME)?
            """
            name = self.consume(ast.Name)
            alias = self.consume(ast.Name) if self.match_token(Tok.KW_AS) else None
            return ast.ModuleItem(
                name=name,
                alias=alias,
                kid=self.nodes,
            )

        def architype(
            self, _: None
        ) -> ast.ArchSpec | ast.ArchDef | ast.Enum | ast.EnumDef:
            """Grammar rule.

            architype: decorators? architype_decl
                    | architype_def
                    | enum
            """
            archspec: ast.ArchSpec | ast.ArchDef | ast.Enum | ast.EnumDef | None = None

            decorators = self.match(ast.SubNodeList)
            if decorators is not None:
                archspec = self.consume(ast.ArchSpec)
                archspec.decorators = decorators
                archspec.add_kids_left([decorators])
            else:
                archspec = (
                    self.match(ast.ArchSpec)
                    or self.match(ast.ArchDef)
                    or self.match(ast.Enum)
                    or self.consume(ast.EnumDef)
                )
            return archspec

        def architype_decl(self, _: None) -> ast.ArchSpec:
            """Grammar rule.

            architype_decl: arch_type access_tag? STRING? NAME inherited_archs? (member_block | SEMI)
            """
            arch_type = self.consume(ast.Token)
            access = self.match(ast.SubTag)
            semstr = self.match(ast.String)
            name = self.consume(ast.Name)
            sub_list1 = self.match(ast.SubNodeList)
            sub_list2 = self.match(ast.SubNodeList)
            if self.match_token(Tok.SEMI):
                inh, body = sub_list1, None
            else:
                body = (
                    sub_list2 or sub_list1
                )  # if sub_list2 is None then body is sub_list1
                inh = sub_list2 and sub_list1  # if sub_list2 is None then inh is None.
            return ast.Architype(
                arch_type=arch_type,
                name=name,
                semstr=semstr,
                access=access,
                base_classes=inh,
                body=body,
                kid=self.nodes,
            )

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

        def decorators(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.Expr]:
            """Grammar rule.

            decorators: (DECOR_OP atomic_chain)+
            """
            valid_decors = [i for i in kid if isinstance(i, ast.Expr)]
            if len(valid_decors) == len(kid) / 2:
                return ast.SubNodeList[ast.Expr](
                    items=valid_decors,
                    delim=Tok.DECOR_OP,
                    kid=kid,
                )
            else:
                raise self.ice()

        def inherited_archs(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.Expr]:
            """Grammar rule.

            inherited_archs: LT (atomic_chain COMMA)* atomic_chain GT
                           | COLON (atomic_chain COMMA)* atomic_chain COLON
            """
            valid_inh = [i for i in kid if isinstance(i, ast.Expr)]
            return ast.SubNodeList[ast.Expr](
                items=valid_inh,
                delim=Tok.COMMA,
                kid=kid,
            )

        def sub_name(self, kid: list[ast.AstNode]) -> ast.SubTag[ast.Name]:
            """Grammar rule.

            sub_name: COLON NAME
            """
            if isinstance(kid[1], ast.Name):
                return ast.SubTag[ast.Name](
                    tag=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def named_ref(self, kid: list[ast.AstNode]) -> ast.NameAtom:
            """Grammar rule.

            named_ref: special_ref
                    | KWESC_NAME
                    | NAME
            """
            if isinstance(kid[0], ast.NameAtom):
                return kid[0]
            else:
                raise self.ice()

        def special_ref(self, kid: list[ast.AstNode]) -> ast.SpecialVarRef:
            """Grammar rule.

            special_ref: KW_INIT
                        | KW_POST_INIT
                        | KW_ROOT
                        | KW_SUPER
                        | KW_SELF
                        | KW_HERE
            """
            if isinstance(kid[0], ast.Name):
                return ast.SpecialVarRef(var=kid[0])
            else:
                raise self.ice()

        def enum(self, _: None) -> ast.Enum | ast.EnumDef:
            """Grammar rule.

            enum: decorators? enum_decl
                | enum_def
            """
            if decorator := self.match(ast.SubNodeList):
                enum_decl = self.consume(ast.Enum)
                enum_decl.decorators = decorator
                enum_decl.add_kids_left([decorator])
                return enum_decl
            return self.match(ast.Enum) or self.consume(ast.EnumDef)

        def enum_decl(self, _: None) -> ast.Enum:
            """Grammar rule.

            enum_decl: KW_ENUM access_tag? STRING? NAME inherited_archs? (enum_block | SEMI)
            """
            self.consume_token(Tok.KW_ENUM)
            access = self.match(ast.SubTag)
            semstr = self.match(ast.String)
            name = self.consume(ast.Name)
            sub_list1 = self.match(ast.SubNodeList)
            sub_list2 = self.match(ast.SubNodeList)
            if self.match_token(Tok.SEMI):
                inh, body = sub_list1, None
            else:
                body = sub_list2 or sub_list1
                inh = sub_list2 and sub_list1
            return ast.Enum(
                semstr=semstr,
                name=name,
                access=access,
                base_classes=inh,
                body=body,
                kid=self.nodes,
            )

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
                    kid=kid,
                )
            else:
                raise self.ice()

        def enum_block(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.EnumBlockStmt]:
            """Grammar rule.

            enum_block: LBRACE ((enum_stmt COMMA)* enum_stmt COMMA?)? RBRACE
            """
            ret = ast.SubNodeList[ast.EnumBlockStmt](items=[], delim=Tok.COMMA, kid=kid)
            ret.items = [i for i in kid if isinstance(i, ast.EnumBlockStmt)]
            return ret

        def enum_stmt(self, _: None) -> ast.EnumBlockStmt:
            """Grammar rule.

            enum_stmt: NAME (COLON STRING)? EQ expression
                    | NAME (COLON STRING)?
                    | py_code_block
                    | free_code
                    | abstract_ability
                    | ability
            """
            if stmt := (
                self.match(ast.PyInlineCode)
                or self.match(ast.ModuleCode)
                or self.match(ast.Ability)
            ):
                return stmt
            name = self.consume(ast.Name)
            semstr = self.consume(ast.String) if self.match_token(Tok.COLON) else None
            expr = self.consume(ast.Expr) if self.match_token(Tok.EQ) else None
            targ = ast.SubNodeList[ast.Expr](items=[name], delim=Tok.COMMA, kid=[name])
            self.nodes[0] = targ
            return ast.Assignment(
                target=targ,
                value=expr,
                type_tag=None,
                kid=self.nodes,
                semstr=semstr,
                is_enum_stmt=True,
            )

        def ability(self, _: None) -> ast.Ability | ast.AbilityDef | ast.FuncCall:
            """Grammer rule.

            ability: decorators? KW_ASYNC? ability_decl
                    | decorators? genai_ability
                    | ability_def
            """
            ability: ast.Ability | ast.AbilityDef | None = None
            decorators = self.match(ast.SubNodeList)
            is_async = self.match_token(Tok.KW_ASYNC)
            ability = self.match(ast.Ability)
            if is_async and ability:
                ability.is_async = True
                ability.add_kids_left([is_async])
            if ability is None:
                ability = self.consume(ast.AbilityDef)
            if decorators:
                for dec in decorators.items:
                    if (
                        isinstance(dec, ast.NameAtom)
                        and dec.sym_name == "staticmethod"
                        and isinstance(ability, (ast.Ability))
                    ):
                        ability.is_static = True
                        decorators.items.remove(dec)  # noqa: B038
                        break
                if decorators.items:
                    ability.decorators = decorators
                    ability.add_kids_left([decorators])
                return ability
            return ability

        def ability_decl(self, _: None) -> ast.Ability:
            """Grammar rule.

            ability_decl: KW_OVERRIDE? KW_STATIC? KW_CAN access_tag? STRING?
                named_ref (func_decl | event_clause) (code_block | SEMI)
            """
            signature: ast.FuncSignature | ast.EventSignature | None = None
            body: ast.SubNodeList | None = None
            is_override = self.match_token(Tok.KW_OVERRIDE) is not None
            is_static = self.match_token(Tok.KW_STATIC) is not None
            self.consume_token(Tok.KW_CAN)
            access = self.match(ast.SubTag)
            semstr = self.match(ast.String)
            name = self.consume(ast.NameAtom)
            signature = self.match(ast.FuncSignature) or self.consume(
                ast.EventSignature
            )
            if (body := self.match(ast.SubNodeList)) is None:
                self.consume_token(Tok.SEMI)
            return ast.Ability(
                name_ref=name,
                is_async=False,
                is_override=is_override,
                is_static=is_static,
                is_abstract=False,
                access=access,
                semstr=semstr,
                signature=signature,
                body=body,
                kid=self.nodes,
            )

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
                    kid=kid,
                )
            else:
                raise self.ice()

        # We need separate production rule for abstract_ability because we don't
        # want to allow regular abilities outside of classed to be abstract.
        def abstract_ability(self, _: None) -> ast.Ability:
            """Grammar rule.

            abstract_ability: KW_OVERRIDE? KW_STATIC? KW_CAN access_tag? STRING?
                named_ref (func_decl | event_clause) KW_ABSTRACT SEMI
            """
            signature: ast.FuncSignature | ast.EventSignature | None = None
            is_override = self.match_token(Tok.KW_OVERRIDE) is not None
            is_static = self.match_token(Tok.KW_STATIC) is not None
            self.consume_token(Tok.KW_CAN)
            access = self.match(ast.SubTag)
            semstr = self.match(ast.String)
            name = self.consume(ast.NameAtom)
            signature = self.match(ast.FuncSignature) or self.consume(
                ast.EventSignature
            )
            self.consume_token(Tok.KW_ABSTRACT)
            self.consume_token(Tok.SEMI)
            return ast.Ability(
                name_ref=name,
                is_async=False,
                is_override=is_override,
                is_static=is_static,
                is_abstract=True,
                access=access,
                semstr=semstr,
                signature=signature,
                body=None,
                kid=self.nodes,
            )

        def genai_ability(self, _: None) -> ast.Ability:
            """Grammar rule.

            genai_ability: KW_OVERRIDE? KW_STATIC? KW_CAN access_tag? STRING?
            named_ref (func_decl) KW_BY atomic_call SEMI
            """
            is_override = self.match_token(Tok.KW_OVERRIDE) is not None
            is_static = self.match_token(Tok.KW_STATIC) is not None
            self.consume_token(Tok.KW_CAN)
            access = self.match(ast.SubTag)
            semstr = self.match(ast.String)
            name = self.consume(ast.NameAtom)
            signature = self.match(ast.FuncSignature) or self.consume(
                ast.EventSignature
            )
            self.consume_token(Tok.KW_BY)
            body = self.consume(ast.FuncCall)
            self.consume_token(Tok.SEMI)
            return ast.Ability(
                name_ref=name,
                is_async=False,
                is_override=is_override,
                is_static=is_static,
                is_abstract=False,
                access=access,
                semstr=semstr,
                signature=signature,
                body=body,
                kid=self.nodes,
            )

        def event_clause(self, _: None) -> ast.EventSignature:
            """Grammar rule.

            event_clause: KW_WITH expression? (KW_EXIT | KW_ENTRY) (STRING? RETURN_HINT expression)?
            """
            return_spec: ast.Expr | None = None
            semstr: ast.String | None = None
            self.consume_token(Tok.KW_WITH)
            type_specs = self.match(ast.Expr)
            event = self.match_token(Tok.KW_EXIT) or self.consume_token(Tok.KW_ENTRY)
            if semstr := self.match(ast.String):
                self.consume_token(Tok.RETURN_HINT)
                return_spec = self.consume(ast.Expr)
            return ast.EventSignature(
                semstr=semstr,
                event=event,
                arch_tag_info=type_specs,
                return_type=return_spec,
                kid=self.nodes,
            )

        def func_decl(self, kid: list[ast.AstNode]) -> ast.FuncSignature:
            """Grammar rule.

            func_decl: (LPAREN func_decl_params? RPAREN)? (RETURN_HINT (STRING COLON)? expression)?
            """
            params = (
                kid[1] if len(kid) > 1 and isinstance(kid[1], ast.SubNodeList) else None
            )
            return_spec = (
                kid[-1] if len(kid) and isinstance(kid[-1], ast.Expr) else None
            )
            semstr = (
                kid[-3]
                if return_spec and len(kid) > 3 and isinstance(kid[-3], ast.String)
                else None
            )
            if (isinstance(params, ast.SubNodeList) or params is None) and (
                isinstance(return_spec, ast.Expr) or return_spec is None
            ):
                return ast.FuncSignature(
                    semstr=semstr,
                    params=params,
                    return_type=return_spec,
                    kid=(
                        kid
                        if len(kid)
                        else [
                            ast.EmptyToken(ast.JacSource("", self.parse_ref.mod_path))
                        ]
                    ),
                )
            else:
                raise self.ice()

        def func_decl_params(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ParamVar]:
            """Grammar rule.

            func_decl_params: (param_var COMMA)* param_var COMMA?
            """
            ret = ast.SubNodeList[ast.ParamVar](
                items=[i for i in kid if isinstance(i, ast.ParamVar)],
                delim=Tok.COMMA,
                kid=kid,
            )
            return ret

        def param_var(self, kid: list[ast.AstNode]) -> ast.ParamVar:
            """Grammar rule.

            param_var: (STAR_POW | STAR_MUL)? NAME (COLON STRING)? type_tag (EQ expression)?
            """
            star = (
                kid[0]
                if isinstance(kid[0], ast.Token)
                and kid[0].name != Tok.NAME
                and not isinstance(kid[0], ast.String)
                else None
            )
            name = kid[1] if (star) else kid[0]
            value = kid[-1] if isinstance(kid[-1], ast.Expr) else None
            type_tag = kid[-3] if value else kid[-1]
            semstr = (
                kid[3]
                if star and len(kid) > 3 and isinstance(kid[3], ast.String)
                else (
                    kid[2]
                    if len(kid) > 4 and value and isinstance(kid[2], ast.String)
                    else (
                        kid[2]
                        if len(kid) > 2 and isinstance(kid[2], ast.String)
                        else None
                    )
                )
            )
            if isinstance(name, ast.Name) and isinstance(type_tag, ast.SubTag):
                return ast.ParamVar(
                    semstr=semstr,
                    name=name,
                    type_tag=type_tag,
                    value=value,
                    unpack=star,
                    kid=kid,
                )
            else:
                raise self.ice()

        def member_block(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ArchBlockStmt]:
            """Grammar rule.

            member_block: LBRACE member_stmt* RBRACE
            """
            ret = ast.SubNodeList[ast.ArchBlockStmt](
                items=[],
                delim=Tok.WS,
                kid=kid,
            )
            ret.items = [i for i in kid if isinstance(i, ast.ArchBlockStmt)]
            ret.left_enc = kid[0] if isinstance(kid[0], ast.Token) else None
            ret.right_enc = kid[-1] if isinstance(kid[-1], ast.Token) else None
            return ret

        def member_stmt(self, kid: list[ast.AstNode]) -> ast.ArchBlockStmt:
            """Grammar rule.

            member_stmt: doc_tag? py_code_block
                        | doc_tag? abstract_ability
                        | doc_tag? ability
                        | doc_tag? architype
                        | doc_tag? has_stmt
            """
            if isinstance(kid[0], ast.ArchBlockStmt):
                ret = kid[0]
            elif (
                isinstance(kid[1], ast.ArchBlockStmt)
                and isinstance(kid[1], ast.AstDocNode)
                and isinstance(kid[0], ast.String)
            ):
                kid[1].doc = kid[0]
                kid[1].add_kids_left([kid[0]])
                ret = kid[1]
            else:
                raise self.ice()
            if isinstance(ret, ast.Ability):
                ret.signature.is_method = True
            return ret

        def has_stmt(self, kid: list[ast.AstNode]) -> ast.ArchHas:
            """Grammar rule.

            has_stmt: KW_STATIC? (KW_LET | KW_HAS) access_tag? has_assign_list SEMI
            """
            chomp = [*kid]
            is_static = (
                isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.KW_STATIC
            )
            chomp = chomp[1:] if is_static else chomp
            is_freeze = isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.KW_LET
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
                new_kid = [*consume.kid, comma, assign]
            else:
                assign = kid[0]
                new_kid = [assign]
            valid_kid = [i for i in new_kid if isinstance(i, ast.HasVar)]
            return ast.SubNodeList[ast.HasVar](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def typed_has_clause(self, kid: list[ast.AstNode]) -> ast.HasVar:
            """Grammar rule.

            typed_has_clause: named_ref (COLON STRING)? type_tag (EQ expression | KW_BY KW_POST_INIT)?
            """
            name = kid[0]
            semstr = kid[2] if len(kid) > 2 and isinstance(kid[2], ast.String) else None
            type_tag = kid[3] if semstr else kid[1]
            defer = isinstance(kid[-1], ast.Token) and kid[-1].name == Tok.KW_POST_INIT
            value = kid[-1] if not defer and isinstance(kid[-1], ast.Expr) else None
            if isinstance(name, ast.Name) and isinstance(type_tag, ast.SubTag):
                return ast.HasVar(
                    semstr=semstr,
                    name=name,
                    type_tag=type_tag,
                    defer=defer,
                    value=value,
                    kid=kid,
                )
            else:
                raise self.ice()

        def type_tag(self, kid: list[ast.AstNode]) -> ast.SubTag[ast.Expr]:
            """Grammar rule.

            type_tag: COLON expression
            """
            if isinstance(kid[1], ast.Expr):
                return ast.SubTag[ast.Expr](
                    tag=kid[1],
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
                return ast.BuiltinType(
                    name=kid[0].name,
                    orig_src=self.parse_ref.source,
                    value=kid[0].value,
                    line=kid[0].loc.first_line,
                    end_line=kid[0].loc.last_line,
                    col_start=kid[0].loc.col_start,
                    col_end=kid[0].loc.col_end,
                    pos_start=kid[0].pos_start,
                    pos_end=kid[0].pos_end,
                )
            else:
                raise self.ice()

        def code_block(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.CodeBlockStmt]:
            """Grammar rule.

            code_block: LBRACE statement* RBRACE
            """
            left_enc = kid[0] if isinstance(kid[0], ast.Token) else None
            right_enc = kid[-1] if isinstance(kid[-1], ast.Token) else None
            valid_stmt = [i for i in kid if isinstance(i, ast.CodeBlockStmt)]
            if len(valid_stmt) == len(kid) - 2:
                return ast.SubNodeList[ast.CodeBlockStmt](
                    items=valid_stmt,
                    delim=Tok.WS,
                    left_enc=left_enc,
                    right_enc=right_enc,
                    kid=kid,
                )
            else:
                raise self.ice()

        def statement(self, kid: list[ast.AstNode]) -> ast.CodeBlockStmt:
            """Grammar rule.

            statement: import_stmt
                    | ability
                    | architype
                    | if_stmt
                    | while_stmt
                    | for_stmt
                    | try_stmt
                    | match_stmt
                    | with_stmt
                    | global_ref SEMI
                    | nonlocal_ref SEMI
                    | typed_ctx_block
                    | return_stmt SEMI
                    | (yield_expr | KW_YIELD) SEMI
                    | raise_stmt SEMI
                    | assert_stmt SEMI
                    | check_stmt SEMI
                    | assignment SEMI
                    | delete_stmt SEMI
                    | report_stmt SEMI
                    | expression SEMI
                    | ctrl_stmt SEMI
                    | py_code_block
                    | walker_stmt
                    | SEMI
            """
            if isinstance(kid[0], ast.CodeBlockStmt) and len(kid) < 2:
                return kid[0]
            elif isinstance(kid[0], ast.Token) and kid[0].name == Tok.KW_YIELD:
                return ast.ExprStmt(
                    expr=(
                        expr := ast.YieldExpr(
                            expr=None,
                            with_from=False,
                            kid=kid,
                        )
                    ),
                    in_fstring=False,
                    kid=[expr],
                )
            elif isinstance(kid[0], ast.Expr):
                return ast.ExprStmt(
                    expr=kid[0],
                    in_fstring=False,
                    kid=kid,
                )
            elif isinstance(kid[0], ast.CodeBlockStmt):
                kid[0].add_kids_right([kid[1]])
                return kid[0]
            else:
                raise self.ice()

        def typed_ctx_block(self, kid: list[ast.AstNode]) -> ast.TypedCtxBlock:
            """Grammar rule.

            typed_ctx_block: RETURN_HINT expression code_block
            """
            if isinstance(kid[1], ast.Expr) and isinstance(kid[2], ast.SubNodeList):
                return ast.TypedCtxBlock(
                    type_ctx=kid[1],
                    body=kid[2],
                    kid=kid,
                )
            else:
                raise self.ice()

        def if_stmt(self, _: None) -> ast.IfStmt:
            """Grammar rule.

            if_stmt: KW_IF expression code_block (elif_stmt | else_stmt)?
            """
            self.consume_token(Tok.KW_IF)
            condition = self.consume(ast.Expr)
            body = self.consume(ast.SubNodeList)
            else_body = self.match(ast.ElseStmt) or self.match(ast.ElseIf)
            return ast.IfStmt(
                condition=condition,
                body=body,
                else_body=else_body,
                kid=self.nodes,
            )

        def elif_stmt(self, _: None) -> ast.ElseIf:
            """Grammar rule.

            elif_stmt: KW_ELIF expression code_block (elif_stmt | else_stmt)?
            """
            self.consume_token(Tok.KW_ELIF)
            condition = self.consume(ast.Expr)
            body = self.consume(ast.SubNodeList)
            else_body = self.match(ast.ElseStmt) or self.match(ast.ElseIf)
            return ast.ElseIf(
                condition=condition,
                body=body,
                else_body=else_body,
                kid=self.nodes,
            )

        def else_stmt(self, _: None) -> ast.ElseStmt:
            """Grammar rule.

            else_stmt: KW_ELSE code_block
            """
            self.consume_token(Tok.KW_ELSE)
            body = self.consume(ast.SubNodeList)
            return ast.ElseStmt(
                body=body,
                kid=self.nodes,
            )

        def try_stmt(self, _: None) -> ast.TryStmt:
            """Grammar rule.

            try_stmt: KW_TRY code_block except_list? else_stmt? finally_stmt?
            """
            self.consume_token(Tok.KW_TRY)
            block = self.consume(ast.SubNodeList)
            except_list = self.match(ast.SubNodeList)
            else_stmt = self.match(ast.ElseStmt)
            finally_stmt = self.match(ast.FinallyStmt)
            return ast.TryStmt(
                body=block,
                excepts=except_list,
                else_body=else_stmt,
                finally_body=finally_stmt,
                kid=self.nodes,
            )

        def except_list(self, _: None) -> ast.SubNodeList[ast.Except]:
            """Grammar rule.

            except_list: except_def+
            """
            items = [self.consume(ast.Except)]
            while expt := self.match(ast.Except):
                items.append(expt)
            return ast.SubNodeList[ast.Except](
                items=items,
                delim=Tok.WS,
                kid=self.nodes,
            )

        def except_def(self, _: None) -> ast.Except:
            """Grammar rule.

            except_def: KW_EXCEPT expression (KW_AS NAME)? code_block
            """
            name: ast.Name | None = None
            self.consume_token(Tok.KW_EXCEPT)
            ex_type = self.consume(ast.Expr)
            if self.match_token(Tok.KW_AS):
                name = self.consume(ast.Name)
            body = self.consume(ast.SubNodeList)
            return ast.Except(
                ex_type=ex_type,
                name=name,
                body=body,
                kid=self.nodes,
            )

        def finally_stmt(self, _: None) -> ast.FinallyStmt:
            """Grammar rule.

            finally_stmt: KW_FINALLY code_block
            """
            self.consume_token(Tok.KW_FINALLY)
            body = self.consume(ast.SubNodeList)
            return ast.FinallyStmt(
                body=body,
                kid=self.nodes,
            )

        def for_stmt(self, kid: list[ast.AstNode]) -> ast.IterForStmt | ast.InForStmt:
            """Grammar rule.

            for_stmt: KW_ASYNC? KW_FOR assignment KW_TO expression KW_BY
                        expression code_block else_stmt?
                    | KW_ASYNC? KW_FOR expression KW_IN expression code_block else_stmt?
            """
            chomp = [*kid]
            is_async = bool(
                isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.KW_ASYNC
            )
            chomp = chomp[1:] if is_async else chomp
            if isinstance(chomp[1], ast.Assignment):
                if (
                    isinstance(chomp[3], ast.Expr)
                    and isinstance(chomp[5], ast.Assignment)
                    and isinstance(chomp[6], ast.SubNodeList)
                ):
                    return ast.IterForStmt(
                        is_async=is_async,
                        iter=chomp[1],
                        condition=chomp[3],
                        count_by=chomp[5],
                        body=chomp[6],
                        else_body=(
                            chomp[-1] if isinstance(chomp[-1], ast.ElseStmt) else None
                        ),
                        kid=kid,
                    )
                else:
                    raise self.ice()
            elif isinstance(chomp[1], ast.Expr):
                if isinstance(chomp[3], ast.Expr) and isinstance(
                    chomp[4], ast.SubNodeList
                ):
                    return ast.InForStmt(
                        is_async=is_async,
                        target=chomp[1],
                        collection=chomp[3],
                        body=chomp[4],
                        else_body=(
                            chomp[-1] if isinstance(chomp[-1], ast.ElseStmt) else None
                        ),
                        kid=kid,
                    )
                else:
                    raise self.ice()
            else:
                raise self.ice()

        def while_stmt(self, kid: list[ast.AstNode]) -> ast.WhileStmt:
            """Grammar rule.

            while_stmt: KW_WHILE expression code_block
            """
            if isinstance(kid[1], ast.Expr) and isinstance(kid[2], ast.SubNodeList):
                return ast.WhileStmt(
                    condition=kid[1],
                    body=kid[2],
                    kid=kid,
                )
            else:
                raise self.ice()

        def with_stmt(self, kid: list[ast.AstNode]) -> ast.WithStmt:
            """Grammar rule.

            with_stmt: KW_ASYNC? KW_WITH expr_as_list code_block
            """
            chomp = [*kid]
            is_async = bool(
                isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.KW_ASYNC
            )
            chomp = chomp[1:] if is_async else chomp
            if isinstance(chomp[1], ast.SubNodeList) and isinstance(
                chomp[2], ast.SubNodeList
            ):
                return ast.WithStmt(
                    is_async=is_async,
                    exprs=chomp[1],
                    body=chomp[2],
                    kid=kid,
                )
            else:
                raise self.ice()

        def expr_as_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.ExprAsItem]:
            """Grammar rule.

            expr_as_list: (expr_as COMMA)* expr_as
            """
            ret = ast.SubNodeList[ast.ExprAsItem](
                items=[i for i in kid if isinstance(i, ast.ExprAsItem)],
                delim=Tok.COMMA,
                kid=kid,
            )
            return ret

        def expr_as(self, kid: list[ast.AstNode]) -> ast.ExprAsItem:
            """Grammar rule.

            expr_as: expression (KW_AS expression)?
            """
            expr = kid[0]
            alias = kid[2] if len(kid) > 1 else None
            if isinstance(expr, ast.Expr) and (
                alias is None or isinstance(alias, ast.Expr)
            ):
                return ast.ExprAsItem(
                    expr=expr,
                    alias=alias,
                    kid=kid,
                )
            else:
                raise self.ice()

        def raise_stmt(self, kid: list[ast.AstNode]) -> ast.RaiseStmt:
            """Grammar rule.

            raise_stmt: KW_RAISE (expression (KW_FROM expression)?)?
            """
            chomp = [*kid][1:]
            e_type = (
                chomp[0] if len(chomp) > 0 and isinstance(chomp[0], ast.Expr) else None
            )
            chomp = chomp[2:] if e_type and len(chomp) > 1 else chomp[1:]
            e = chomp[0] if len(chomp) > 0 and isinstance(chomp[0], ast.Expr) else None
            return ast.RaiseStmt(
                cause=e_type,
                from_target=e,
                kid=kid,
            )

        def assert_stmt(self, kid: list[ast.AstNode]) -> ast.AssertStmt:
            """Grammar rule.

            assert_stmt: KW_ASSERT expression (COMMA expression)?
            """
            condition = kid[1]
            error_msg = kid[3] if len(kid) > 3 else None
            if isinstance(condition, ast.Expr):
                return ast.AssertStmt(
                    condition=condition,
                    error_msg=(error_msg if isinstance(error_msg, ast.Expr) else None),
                    kid=kid,
                )
            else:
                raise self.ice()

        def check_stmt(self, kid: list[ast.AstNode]) -> ast.CheckStmt:
            """Grammar rule.

            check_stmt: KW_CHECK expression
            """
            if isinstance(kid[1], ast.Expr):
                return ast.CheckStmt(
                    target=kid[1],
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
                    kid=kid,
                )
            else:
                raise self.ice()

        def delete_stmt(self, kid: list[ast.AstNode]) -> ast.DeleteStmt:
            """Grammar rule.

            delete_stmt: KW_DELETE expression
            """
            if isinstance(kid[1], ast.Expr):
                return ast.DeleteStmt(
                    target=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def report_stmt(self, kid: list[ast.AstNode]) -> ast.ReportStmt:
            """Grammar rule.

            report_stmt: KW_REPORT expression
            """
            if isinstance(kid[1], ast.Expr):
                return ast.ReportStmt(
                    expr=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def return_stmt(self, kid: list[ast.AstNode]) -> ast.ReturnStmt:
            """Grammar rule.

            return_stmt: KW_RETURN expression?
            """
            if len(kid) > 1:
                return ast.ReturnStmt(
                    expr=kid[1] if isinstance(kid[1], ast.Expr) else None,
                    kid=kid,
                )
            else:
                return ast.ReturnStmt(
                    expr=None,
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
            if isinstance(kid[1], ast.Expr):
                return ast.IgnoreStmt(
                    target=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def visit_stmt(self, kid: list[ast.AstNode]) -> ast.VisitStmt:
            """Grammar rule.

            visit_stmt: KW_VISIT (inherited_archs)? expression (else_stmt | SEMI)
            """
            sub_name = kid[1] if isinstance(kid[1], ast.SubNodeList) else None
            target = kid[2] if sub_name else kid[1]
            else_body = kid[-1] if isinstance(kid[-1], ast.ElseStmt) else None
            if isinstance(target, ast.Expr):
                return ast.VisitStmt(
                    vis_type=sub_name,
                    target=target,
                    else_body=else_body,
                    kid=kid,
                )
            else:
                raise self.ice()

        def revisit_stmt(self, kid: list[ast.AstNode]) -> ast.RevisitStmt:
            """Grammar rule.

            revisit_stmt: KW_REVISIT expression? (else_stmt | SEMI)
            """
            target = kid[1] if isinstance(kid[1], ast.Expr) else None
            else_body = kid[-1] if isinstance(kid[-1], ast.ElseStmt) else None
            return ast.RevisitStmt(
                hops=target,
                else_body=else_body,
                kid=kid,
            )

        def disengage_stmt(self, kid: list[ast.AstNode]) -> ast.DisengageStmt:
            """Grammar rule.

            disengage_stmt: KW_DISENGAGE SEMI
            """
            return ast.DisengageStmt(
                kid=kid,
            )

        def global_ref(self, kid: list[ast.AstNode]) -> ast.GlobalStmt:
            """Grammar rule.

            global_ref: GLOBAL_OP name_list
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.SubNodeList):
                return ast.GlobalStmt(target=kid[1], kid=kid)
            else:
                raise self.ice()

        def nonlocal_ref(self, kid: list[ast.AstNode]) -> ast.NonLocalStmt:
            """Grammar rule.

            nonlocal_ref: NONLOCAL_OP name_list
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.SubNodeList):
                return ast.NonLocalStmt(target=kid[1], kid=kid)
            else:
                raise self.ice()

        def assignment(self, kid: list[ast.AstNode]) -> ast.Assignment:
            """Grammar rule.

            assignment: KW_LET? (atomic_chain EQ)+ (yield_expr | expression)
                    | atomic_chain (COLON STRING)? type_tag (EQ (yield_expr | expression))?
                    | atomic_chain aug_op (yield_expr | expression)
            """
            chomp = [*kid]
            is_frozen = isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.KW_LET
            is_aug = None
            assignees = []
            chomp = chomp[1:] if is_frozen else chomp
            value = chomp[-1] if isinstance(chomp[-1], ast.Expr) else None
            chomp = (
                chomp[:-2]
                if value and isinstance(chomp[-3], ast.SubTag)
                else chomp[:-1] if value else chomp
            )
            type_tag = chomp[-1] if isinstance(chomp[-1], ast.SubTag) else None
            if not value:
                semstr = chomp[2] if len(chomp) > 2 else None
                chomp = chomp[:-2] if semstr else chomp
            else:
                if type_tag:
                    chomp = chomp[:-1]
                    semstr = (
                        chomp[-1]
                        if len(chomp) > 1 and isinstance(chomp[-1], ast.String)
                        else None
                    )
                    chomp = chomp[:-2] if semstr else chomp
                else:
                    semstr = None
                    if (
                        isinstance(chomp[1], ast.Token)
                        and chomp[1].name != Tok.EQ
                        and chomp[1].name != Tok.COLON
                    ):
                        assignees += [chomp[0]]
                        is_aug = chomp[1]
                        chomp = chomp[2:]
                    else:
                        while (
                            len(chomp) > 1
                            and isinstance(chomp[0], ast.Expr)
                            and isinstance(chomp[1], ast.Token)
                            and chomp[1].name == Tok.EQ
                        ):
                            assignees += [chomp[0], chomp[1]]
                            chomp = chomp[2:]

            assignees += chomp
            valid_assignees = [i for i in assignees if isinstance(i, (ast.Expr))]
            new_targ = ast.SubNodeList[ast.Expr](
                items=valid_assignees,
                delim=Tok.EQ,
                kid=assignees,
            )
            kid = [x for x in kid if x not in assignees]
            kid.insert(1, new_targ) if is_frozen else kid.insert(0, new_targ)
            if is_aug:
                return ast.Assignment(
                    target=new_targ,
                    type_tag=type_tag if isinstance(type_tag, ast.SubTag) else None,
                    value=value,
                    mutable=is_frozen,
                    aug_op=is_aug,
                    kid=kid,
                )
            return ast.Assignment(
                target=new_targ,
                type_tag=type_tag if isinstance(type_tag, ast.SubTag) else None,
                value=value,
                mutable=is_frozen,
                kid=kid,
                semstr=semstr if isinstance(semstr, ast.String) else None,
            )

        def expression(self, _: None) -> ast.Expr:
            """Grammar rule.

            expression: walrus_assign
                    | pipe (KW_IF expression KW_ELSE expression)?
                    | lambda_expr
            """
            value = self.consume(ast.Expr)
            if self.match_token(Tok.KW_IF):
                condition = self.consume(ast.Expr)
                self.consume_token(Tok.KW_ELSE)
                else_value = self.consume(ast.Expr)
                return ast.IfElseExpr(
                    value=value,
                    condition=condition,
                    else_value=else_value,
                    kid=self.nodes,
                )
            return value

        def walrus_assign(self, _: None) -> ast.Expr:
            """Grammar rule.

            walrus_assign: (walrus_assign WALRUS_EQ)? pipe
            """
            return self._binary_expr_unwind(self.nodes)

        def lambda_expr(self, kid: list[ast.AstNode]) -> ast.LambdaExpr:
            """Grammar rule.

            lamda_expr: KW_WITH func_decl_params? (RETURN_HINT expression)? KW_CAN expression
            """
            chomp = [*kid][1:]
            params = chomp[0] if isinstance(chomp[0], ast.SubNodeList) else None
            chomp = chomp[1:] if params else chomp
            return_type = (
                chomp[1]
                if isinstance(chomp[0], ast.Token)
                and chomp[0].name == Tok.RETURN_HINT
                and isinstance(chomp[1], ast.Expr)
                else None
            )
            chomp = chomp[2:] if return_type else chomp
            chomp = chomp[1:]
            sig_kid: list[ast.AstNode] = []
            if params:
                sig_kid.append(params)
            if return_type:
                sig_kid.append(return_type)
            signature = (
                ast.FuncSignature(
                    params=params,
                    return_type=return_type,
                    kid=sig_kid,
                )
                if params or return_type
                else None
            )
            new_kid = [i for i in kid if i != params and i != return_type]
            new_kid.insert(1, signature) if signature else None
            if isinstance(chomp[0], ast.Expr):
                return ast.LambdaExpr(
                    signature=signature,
                    body=chomp[0],
                    kid=new_kid,
                )
            else:
                raise self.ice()

        def pipe(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            pipe: pipe_back PIPE_FWD pipe
                | pipe_back
            """
            return self._binary_expr_unwind(kid)

        def pipe_back(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            pipe_back: bitwise_or PIPE_BKWD pipe_back
                     | bitwise_or
            """
            return self._binary_expr_unwind(kid)

        def bitwise_or(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            bitwise_or: bitwise_xor BW_OR bitwise_or
                      | bitwise_xor
            """
            return self._binary_expr_unwind(kid)

        def bitwise_xor(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            bitwise_xor: bitwise_and BW_XOR bitwise_xor
                       | bitwise_and
            """
            return self._binary_expr_unwind(kid)

        def bitwise_and(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            bitwise_and: shift BW_AND bitwise_and
                       | shift
            """
            return self._binary_expr_unwind(kid)

        def shift(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            shift: (shift (RSHIFT | LSHIFT))? logical_or
            """
            return self._binary_expr_unwind(kid)

        def logical_or(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            logical_or: logical_and (KW_OR logical_and)*
            """
            if len(kid) > 1:
                values = [i for i in kid if isinstance(i, ast.Expr)]
                ops = kid[1] if isinstance(kid[1], ast.Token) else None
                if not ops:
                    raise self.ice()
                return ast.BoolExpr(
                    op=ops,
                    values=values,
                    kid=kid,
                )
            elif isinstance(kid[0], ast.Expr):
                return kid[0]
            else:

                raise self.ice()

        def logical_and(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            logical_and: logical_not (KW_AND logical_not)*
            """
            if len(kid) > 1:
                values = [i for i in kid if isinstance(i, ast.Expr)]
                ops = kid[1] if isinstance(kid[1], ast.Token) else None
                if not ops:
                    raise self.ice()
                return ast.BoolExpr(
                    op=ops,
                    values=values,
                    kid=kid,
                )
            elif isinstance(kid[0], ast.Expr):
                return kid[0]
            else:

                raise self.ice()

        def logical_not(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            logical_or: (logical_or KW_OR)? logical_and
            """
            if len(kid) == 2:
                if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.Expr):
                    return ast.UnaryExpr(
                        op=kid[0],
                        operand=kid[1],
                        kid=kid,
                    )
                else:
                    raise self.ice()
            if isinstance(kid[0], ast.Expr):
                return kid[0]
            else:
                raise self.ice()

        def compare(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            compare: (arithmetic cmp_op)* arithmetic
            """
            if len(kid) > 1:
                ops = [i for i in kid[1::2] if isinstance(i, ast.Token)]
                left = kid[0]
                rights = [i for i in kid[1:][1::2] if isinstance(i, ast.Expr)]
                if isinstance(left, ast.Expr) and len(ops) == len(rights):
                    return ast.CompareExpr(
                        left=left,
                        ops=ops,
                        rights=rights,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.Expr):
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

        def arithmetic(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            arithmetic: (arithmetic (MINUS | PLUS))? term
            """
            return self._binary_expr_unwind(kid)

        def term(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            term: (term (MOD | DIV | FLOOR_DIV | STAR_MUL | DECOR_OP))? power
            """
            return self._binary_expr_unwind(kid)

        def factor(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            factor: (BW_NOT | MINUS | PLUS) factor | connect
            """
            if len(kid) == 2:
                if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.Expr):
                    return ast.UnaryExpr(
                        op=kid[0],
                        operand=kid[1],
                        kid=kid,
                    )
                else:
                    raise self.ice()
            return self._binary_expr_unwind(kid)

        def power(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            power: (power STAR_POW)? factor
            """
            return self._binary_expr_unwind(kid)

        def connect(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            connect: (connect (connect_op | disconnect_op))? atomic_pipe
            """
            return self._binary_expr_unwind(kid)

        def atomic_pipe(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            atomic_pipe: (atomic_pipe A_PIPE_FWD)? atomic_pipe_back
            """
            return self._binary_expr_unwind(kid)

        def atomic_pipe_back(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            atomic_pipe_back: (atomic_pipe_back A_PIPE_BKWD)? ds_spawn
            """
            return self._binary_expr_unwind(kid)

        def ds_spawn(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            ds_spawn: (ds_spawn KW_SPAWN)? unpack
            """
            return self._binary_expr_unwind(kid)

        def unpack(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            unpack: STAR_MUL? ref
            """
            if len(kid) == 2:
                if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.Expr):
                    return ast.UnaryExpr(
                        op=kid[0],
                        operand=kid[1],
                        kid=kid,
                    )
                else:
                    raise self.ice()
            return self._binary_expr_unwind(kid)

        def ref(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            ref: walrus_assign
               | BW_AND walrus_assign
            """
            if len(kid) == 2:
                if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.Expr):
                    return ast.UnaryExpr(
                        op=kid[0],
                        operand=kid[1],
                        kid=kid,
                    )
                else:
                    raise self.ice()
            return self._binary_expr_unwind(kid)

        def pipe_call(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            pipe_call: atomic_chain
                | PIPE_FWD atomic_chain
                | A_PIPE_FWD atomic_chain
                | KW_SPAWN atomic_chain
                | KW_AWAIT atomic_chain
            """
            if len(kid) == 2:
                if (
                    isinstance(kid[0], ast.Token)
                    and kid[0].name == Tok.KW_AWAIT
                    and isinstance(kid[1], ast.Expr)
                ):
                    return ast.AwaitExpr(
                        target=kid[1],
                        kid=kid,
                    )
                elif isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.Expr):
                    return ast.UnaryExpr(
                        op=kid[0],
                        operand=kid[1],
                        kid=kid,
                    )
                else:
                    raise self.ice()
            return self._binary_expr_unwind(kid)

        def aug_op(self, kid: list[ast.AstNode]) -> ast.Token:
            """Grammar rule.

            aug_op: RSHIFT_EQ
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

        def atomic_chain(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            atomic_chain: atomic_chain NULL_OK? (filter_compr | assign_compr | index_slice)
                        | atomic_chain NULL_OK? (DOT_BKWD | DOT_FWD | DOT) named_ref
                        | (atomic_call | atom | edge_ref_chain)
            """
            if len(kid) < 2 and isinstance(kid[0], ast.Expr):
                return kid[0]
            chomp = [*kid]
            target = chomp[0]
            chomp = chomp[1:]
            is_null_ok = False
            if isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.NULL_OK:
                is_null_ok = True
                chomp = chomp[1:]
            if (
                len(chomp) == 1
                and isinstance(chomp[0], ast.AtomExpr)
                and isinstance(target, ast.Expr)
            ):
                return ast.AtomTrailer(
                    target=target,
                    right=chomp[0],
                    is_null_ok=is_null_ok,
                    is_attr=False,
                    kid=kid,
                )
            elif (
                len(chomp) > 1
                and isinstance(chomp[0], ast.Token)
                and isinstance(chomp[1], (ast.AtomExpr, ast.AtomTrailer))
                and isinstance(target, ast.Expr)
            ):
                return ast.AtomTrailer(
                    target=(target if chomp[0].name != Tok.DOT_BKWD else chomp[1]),
                    right=(chomp[1] if chomp[0].name != Tok.DOT_BKWD else target),
                    is_null_ok=is_null_ok,
                    is_attr=True,
                    kid=kid,
                )
            else:
                raise self.ice()

        def atomic_call(self, kid: list[ast.AstNode]) -> ast.FuncCall:
            """Grammar rule.

            atomic_call: atomic_chain LPAREN param_list? (KW_BY atomic_call)? RPAREN
            """
            if (
                len(kid) > 4
                and isinstance(kid[0], ast.Expr)
                and kid[-2]
                and isinstance(kid[-2], ast.FuncCall)
            ):
                return ast.FuncCall(
                    target=kid[0],
                    params=kid[2] if isinstance(kid[2], ast.SubNodeList) else None,
                    genai_call=kid[-2],
                    kid=kid,
                )
            if (
                len(kid) == 4
                and isinstance(kid[0], ast.Expr)
                and isinstance(kid[2], ast.SubNodeList)
            ):
                return ast.FuncCall(
                    target=kid[0], params=kid[2], genai_call=None, kid=kid
                )
            elif len(kid) == 3 and isinstance(kid[0], ast.Expr):
                return ast.FuncCall(
                    target=kid[0], params=None, genai_call=None, kid=kid
                )
            else:
                raise self.ice()

        def index_slice(self, kid: list[ast.AstNode]) -> ast.IndexSlice:
            """Grammar rule.

            index_slice: LSQUARE                                                        \
                            expression? COLON expression? (COLON expression?)?          \
                            (COMMA expression? COLON expression? (COLON expression?)?)* \
                         RSQUARE
                        | list_val
            """
            if len(kid) == 1:
                index = kid[0]
                if isinstance(index, ast.ListVal):
                    if not index.values:
                        raise self.ice()
                    if len(index.values.items) == 1:
                        expr = index.values.items[0] if index.values else None
                    else:
                        sublist = ast.SubNodeList[ast.Expr | ast.KWPair](
                            items=[*index.values.items], delim=Tok.COMMA, kid=index.kid
                        )
                        expr = ast.TupleVal(values=sublist, kid=[sublist])
                        kid = [expr]
                    return ast.IndexSlice(
                        slices=[ast.IndexSlice.Slice(start=expr, stop=None, step=None)],
                        is_range=False,
                        kid=kid,
                    )
                else:
                    raise self.ice()
            else:
                slices: list[ast.IndexSlice.Slice] = []
                chomp = kid[1:]

                while not (
                    isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.RSQUARE
                ):
                    expr1 = expr2 = expr3 = None

                    if isinstance(chomp[0], ast.Expr):
                        expr1 = chomp[0]
                        chomp.pop(0)
                    chomp.pop(0)

                    if isinstance(chomp[0], ast.Expr):
                        expr2 = chomp[0]
                        chomp.pop(0)

                    if isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.COLON:
                        chomp.pop(0)
                        if isinstance(chomp[0], ast.Expr):
                            expr3 = chomp[0]
                            chomp.pop(0)

                    if isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.COMMA:
                        chomp.pop(0)

                    slices.append(
                        ast.IndexSlice.Slice(start=expr1, stop=expr2, step=expr3)
                    )

                return ast.IndexSlice(
                    slices=slices,
                    is_range=True,
                    kid=kid,
                )

        def atom(self, kid: list[ast.AstNode]) -> ast.Expr:
            """Grammar rule.

            atom: named_ref
                 | LPAREN (expression | yield_expr) RPAREN
                 | atom_collection
                 | atom_literal
                 | type_ref
            """
            if len(kid) == 1:
                if isinstance(kid[0], ast.AtomExpr):
                    return kid[0]
                else:
                    raise self.ice()
            elif len(kid) == 3:
                if (
                    isinstance(kid[0], ast.Token)
                    and isinstance(kid[1], (ast.Expr, ast.YieldExpr))
                    and isinstance(kid[2], ast.Token)
                ):
                    ret = ast.AtomUnit(value=kid[1], kid=kid)
                    return ret
                else:
                    raise self.ice()
            else:
                raise self.ice()

        def yield_expr(self, kid: list[ast.AstNode]) -> ast.YieldExpr:
            """Grammar rule.

            yield_expr: KW_YIELD KW_FROM? expression
            """
            if isinstance(kid[-1], ast.Expr):
                return ast.YieldExpr(
                    expr=kid[-1],
                    with_from=len(kid) > 2,
                    kid=kid,
                )
            else:
                raise self.ice()

        def atom_literal(self, kid: list[ast.AstNode]) -> ast.AtomExpr:
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
            if isinstance(kid[0], ast.AtomExpr):
                return kid[0]
            else:
                raise self.ice()

        def atom_collection(self, kid: list[ast.AstNode]) -> ast.AtomExpr:
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
            if isinstance(kid[0], ast.AtomExpr):
                return kid[0]
            else:
                raise self.ice()

        def multistring(self, kid: list[ast.AstNode]) -> ast.AtomExpr:
            """Grammar rule.

            multistring: (fstring | STRING | DOC_STRING)+
            """
            valid_strs = [i for i in kid if isinstance(i, (ast.String, ast.FString))]
            if len(valid_strs) == len(kid):
                return ast.MultiString(
                    strings=valid_strs,
                    kid=kid,
                )
            else:
                raise self.ice()

        def fstring(self, kid: list[ast.AstNode]) -> ast.FString:
            """Grammar rule.

            fstring: FSTR_START fstr_parts FSTR_END
                | FSTR_SQ_START fstr_sq_parts FSTR_SQ_END
            """
            if len(kid) == 2:
                return ast.FString(
                    parts=None,
                    kid=kid,
                )
            elif isinstance(kid[1], ast.SubNodeList):
                return ast.FString(
                    parts=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def fstr_parts(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.String | ast.ExprStmt]:
            """Grammar rule.

            fstr_parts: (FSTR_PIECE | FSTR_BESC | LBRACE expression RBRACE )*
            """
            valid_parts: list[ast.String | ast.ExprStmt] = [
                (
                    i
                    if isinstance(i, ast.String)
                    else ast.ExprStmt(expr=i, in_fstring=True, kid=[i])
                )
                for i in kid
                if isinstance(i, ast.Expr)
            ]
            return ast.SubNodeList[ast.String | ast.ExprStmt](
                items=valid_parts,
                delim=None,
                kid=valid_parts,
            )

        def fstr_sq_parts(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.String | ast.ExprStmt]:
            """Grammar rule.

            fstr_sq_parts: (FSTR_SQ_PIECE | FSTR_BESC | LBRACE expression RBRACE )*
            """
            valid_parts: list[ast.String | ast.ExprStmt] = [
                (
                    i
                    if isinstance(i, ast.String)
                    else ast.ExprStmt(expr=i, in_fstring=True, kid=[i])
                )
                for i in kid
                if isinstance(i, ast.Expr)
            ]
            return ast.SubNodeList[ast.String | ast.ExprStmt](
                items=valid_parts,
                delim=None,
                kid=valid_parts,
            )

        def list_val(self, kid: list[ast.AstNode]) -> ast.ListVal:
            """Grammar rule.

            list_val: LSQUARE (expr_list COMMA?)? RSQUARE
            """
            if len(kid) == 2:
                return ast.ListVal(
                    values=None,
                    kid=kid,
                )
            elif isinstance(kid[1], ast.SubNodeList):
                return ast.ListVal(
                    values=kid[1],
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
                    kid=kid,
                )
            elif isinstance(kid[1], ast.SubNodeList):
                return ast.TupleVal(
                    values=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def set_val(self, kid: list[ast.AstNode]) -> ast.SetVal:
            """Grammar rule.

            set_val: LBRACE expr_list COMMA? RBRACE
            """
            if len(kid) == 2:
                return ast.SetVal(
                    values=None,
                    kid=kid,
                )
            elif isinstance(kid[1], ast.SubNodeList):
                return ast.SetVal(
                    values=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def expr_list(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.Expr]:
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
                new_kid = [*consume.kid, comma, expr]
            else:
                expr = kid[0]
                new_kid = [expr]
            valid_kid = [i for i in new_kid if isinstance(i, ast.Expr)]
            return ast.SubNodeList[ast.Expr](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def kw_expr_list(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.KWPair]:
            """Grammar rule.

            kw_expr_list: (kw_expr_list COMMA)? kw_expr
            """
            consume = None
            expr = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                expr = kid[2]
                new_kid = [*consume.kid, comma, expr]
            else:
                expr = kid[0]
                new_kid = [expr]
            valid_kid = [i for i in new_kid if isinstance(i, ast.KWPair)]
            return ast.SubNodeList[ast.KWPair](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def kw_expr(self, kid: list[ast.AstNode]) -> ast.KWPair:
            """Grammar rule.

            kw_expr: named_ref EQ expression | STAR_POW expression
            """
            if (
                len(kid) == 3
                and isinstance(kid[0], ast.NameAtom)
                and isinstance(kid[2], ast.Expr)
            ):
                return ast.KWPair(
                    key=kid[0],
                    value=kid[2],
                    kid=kid,
                )
            elif len(kid) == 2 and isinstance(kid[1], ast.Expr):
                return ast.KWPair(
                    key=None,
                    value=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def name_list(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.Name]:
            """Grammar rule.

            name_list: (named_ref COMMA)* named_ref
            """
            valid_kid = [i for i in kid if isinstance(i, ast.Name)]
            return ast.SubNodeList[ast.Name](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=kid,
            )

        def tuple_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.Expr | ast.KWPair]:
            """Grammar rule.

            tuple_list: expression COMMA expr_list    COMMA kw_expr_list COMMA?
                      | expression COMMA kw_expr_list COMMA?
                      | expression COMMA expr_list    COMMA?
                      | expression COMMA
                      | kw_expr_list COMMA?
            """
            chomp = [*kid]
            first_expr = None
            if isinstance(chomp[0], ast.SubNodeList):
                # The chomp will be like this:
                #     kw_expr_list, [COMMA]
                if len(chomp) > 1:
                    # Add the comma to the subnode list if it exists, otherwise the last comma will not be a part of
                    # the ast, we need it for formatting.
                    chomp[0].kid.append(chomp[1])
                return chomp[0]
            else:
                # The chomp will be like this:
                #     expression, COMMA, [subnode_list, [COMMA, [kw_expr_list, [COMMA]]]]
                # Pop the first expression from chomp.
                first_expr = chomp[0]  # Get the first expression.
                chomp = chomp[2:]  # Get rid of expr and comma.

            # The chomp will be like this:
            #     [subnode_list, [COMMA, [kw_expr_list, [COMMA]]]]
            expr_list = []
            if len(chomp):
                expr_list = chomp[0].kid  # Get the kids subnode list.
                chomp = chomp[2:]  # Get rid of the subnode list and a comma if exists.
                if len(chomp):
                    # The chomp will be like this: [kw_expr_list, [COMMA]]
                    expr_list = [*expr_list, *chomp[0].kid]
            expr_list = [first_expr, *expr_list]
            valid_kid = [i for i in expr_list if isinstance(i, (ast.Expr, ast.KWPair))]
            return ast.SubNodeList[ast.Expr | ast.KWPair](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=kid,
            )

        def dict_val(self, kid: list[ast.AstNode]) -> ast.DictVal:
            """Grammar rule.

            dict_val: LBRACE ((kv_pair COMMA)* kv_pair COMMA?)? RBRACE
            """
            ret = ast.DictVal(
                kv_pairs=[],
                kid=kid,
            )
            ret.kv_pairs = [i for i in kid if isinstance(i, ast.KVPair)]
            return ret

        def kv_pair(self, kid: list[ast.AstNode]) -> ast.KVPair:
            """Grammar rule.

            kv_pair: expression COLON expression | STAR_POW expression
            """
            if (
                len(kid) == 3
                and isinstance(kid[0], ast.Expr)
                and isinstance(kid[2], ast.Expr)
            ):
                return ast.KVPair(
                    key=kid[0],
                    value=kid[2],
                    kid=kid,
                )
            elif len(kid) == 2 and isinstance(kid[1], ast.Expr):
                return ast.KVPair(
                    key=None,
                    value=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def list_compr(self, kid: list[ast.AstNode]) -> ast.ListCompr:
            """Grammar rule.

            list_compr: LSQUARE expression inner_compr+ RSQUARE
            """
            comprs = [i for i in kid if isinstance(i, ast.InnerCompr)]
            if isinstance(kid[1], ast.Expr):
                return ast.ListCompr(
                    out_expr=kid[1],
                    compr=comprs,
                    kid=kid,
                )
            else:
                raise self.ice()

        def gen_compr(self, kid: list[ast.AstNode]) -> ast.GenCompr:
            """Grammar rule.

            gen_compr: LPAREN expression inner_compr+ RPAREN
            """
            comprs = [i for i in kid if isinstance(i, ast.InnerCompr)]
            if isinstance(kid[1], ast.Expr):
                return ast.GenCompr(
                    out_expr=kid[1],
                    compr=comprs,
                    kid=kid,
                )
            else:
                raise self.ice()

        def set_compr(self, kid: list[ast.AstNode]) -> ast.SetCompr:
            """Grammar rule.

            set_compr: LBRACE expression inner_compr+ RBRACE
            """
            comprs = [i for i in kid if isinstance(i, ast.InnerCompr)]
            if isinstance(kid[1], ast.Expr) and isinstance(kid[2], ast.InnerCompr):
                return ast.SetCompr(
                    out_expr=kid[1],
                    compr=comprs,
                    kid=kid,
                )
            else:
                raise self.ice()

        def dict_compr(self, kid: list[ast.AstNode]) -> ast.DictCompr:
            """Grammar rule.

            dict_compr: LBRACE kv_pair inner_compr+ RBRACE
            """
            comprs = [i for i in kid if isinstance(i, ast.InnerCompr)]
            if isinstance(kid[1], ast.KVPair) and isinstance(kid[2], ast.InnerCompr):
                return ast.DictCompr(
                    kv_pair=kid[1],
                    compr=comprs,
                    kid=kid,
                )
            else:
                raise self.ice()

        def inner_compr(self, kid: list[ast.AstNode]) -> ast.InnerCompr:
            """Grammar rule.

            inner_compr: KW_ASYNC? KW_FOR atomic_chain KW_IN pipe_call (KW_IF walrus_assign)*
            """
            chomp = [*kid]
            is_async = bool(
                isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.KW_ASYNC
            )
            chomp = chomp[1:] if is_async else chomp
            chomp = chomp[1:]
            if isinstance(chomp[0], ast.Expr) and isinstance(chomp[2], ast.Expr):
                return ast.InnerCompr(
                    is_async=is_async,
                    target=chomp[0],
                    collection=chomp[2],
                    conditional=(
                        [i for i in chomp[4:] if isinstance(i, ast.Expr)]
                        if len(chomp) > 4 and isinstance(chomp[4], ast.Expr)
                        else None
                    ),
                    kid=chomp,
                )
            else:
                raise self.ice()

        def param_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.Expr | ast.KWPair]:
            """Grammar rule.

            param_list: expr_list    COMMA kw_expr_list COMMA?
                      | kw_expr_list COMMA?
                      | expr_list    COMMA?
            """
            ends_with_comma = (
                len(kid) > 1
                and isinstance(kid[-1], ast.Token)
                and kid[-1].name == "COMMA"
            )
            if len(kid) == 1 or (len(kid) == 2 and ends_with_comma):
                if isinstance(kid[0], ast.SubNodeList):
                    if (
                        ends_with_comma
                    ):  # Append the trailing comma to the subnode list.
                        kid[0].kid.append(kid[1])
                    return kid[0]
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.SubNodeList) and isinstance(
                kid[2], ast.SubNodeList
            ):
                valid_kid = [
                    i
                    for i in [*kid[0].items, *kid[2].items]
                    if isinstance(i, (ast.Expr, ast.KWPair))
                ]
                if len(valid_kid) == len(kid[0].items) + len(kid[2].items):
                    return ast.SubNodeList[ast.Expr | ast.KWPair](
                        items=valid_kid,
                        delim=Tok.COMMA,
                        kid=kid,
                    )
                else:
                    raise self.ice()
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
                new_kid = [*consume.kid, comma, assign]
            else:
                assign = kid[0]
                new_kid = [assign]
            valid_kid = [i for i in new_kid if isinstance(i, ast.Assignment)]
            return ast.SubNodeList[ast.Assignment](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def arch_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            arch_ref: object_ref
                    | walker_ref
                    | edge_ref
                    | node_ref
                    | type_ref
            """
            if isinstance(kid[0], ast.ArchRef):
                return kid[0]
            else:
                raise self.ice()

        def node_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            node_ref: NODE_OP NAME
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameAtom):
                return ast.ArchRef(
                    arch_type=kid[0],
                    arch_name=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def edge_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            edge_ref: EDGE_OP NAME
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameAtom):
                return ast.ArchRef(
                    arch_type=kid[0],
                    arch_name=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def walker_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            walker_ref: WALKER_OP NAME
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameAtom):
                return ast.ArchRef(
                    arch_type=kid[0],
                    arch_name=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def class_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            class_ref: CLASS_OP name_ref
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameAtom):
                return ast.ArchRef(
                    arch_type=kid[0],
                    arch_name=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def object_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            object_ref: OBJECT_OP name_ref
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameAtom):
                return ast.ArchRef(
                    arch_type=kid[0],
                    arch_name=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def type_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            type_ref: TYPE_OP (named_ref | builtin_type)
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameAtom):
                return ast.ArchRef(
                    arch_type=kid[0],
                    arch_name=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def enum_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            enum_ref: ENUM_OP NAME
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameAtom):
                return ast.ArchRef(
                    arch_type=kid[0],
                    arch_name=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def ability_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            ability_ref: ABILITY_OP (special_ref | name_ref)
            """
            if isinstance(kid[0], ast.Token) and isinstance(kid[1], ast.NameAtom):
                return ast.ArchRef(
                    arch_type=kid[0],
                    arch_name=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def arch_or_ability_chain(self, kid: list[ast.AstNode]) -> ast.ArchRefChain:
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
            new_kid = [*consume.kid, name] if consume else [name]
            valid_kid = [i for i in new_kid if isinstance(i, ast.ArchRef)]
            if len(valid_kid) == len(new_kid):
                return ast.ArchRefChain(
                    archs=valid_kid,
                    kid=new_kid,
                )
            else:
                raise self.ice()

        def abil_to_arch_chain(self, kid: list[ast.AstNode]) -> ast.ArchRefChain:
            """Grammar rule.

            abil_to_arch_chain: arch_or_ability_chain? arch_ref
            """
            if len(kid) == 2:
                if isinstance(kid[1], ast.ArchRef) and isinstance(
                    kid[0], ast.ArchRefChain
                ):
                    return ast.ArchRefChain(
                        archs=[*(kid[0].archs), kid[1]],
                        kid=[*(kid[0].kid), kid[1]],
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.ArchRef):
                return ast.ArchRefChain(
                    archs=[kid[0]],
                    kid=kid,
                )
            else:
                raise self.ice()

        def arch_to_abil_chain(self, kid: list[ast.AstNode]) -> ast.ArchRefChain:
            """Grammar rule.

            arch_to_abil_chain: arch_or_ability_chain? ability_ref
            """
            if len(kid) == 2:
                if isinstance(kid[1], ast.ArchRef) and isinstance(
                    kid[0], ast.ArchRefChain
                ):
                    return ast.ArchRefChain(
                        archs=[*(kid[0].archs), kid[1]],
                        kid=[*(kid[0].kid), kid[1]],
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.ArchRef):
                return ast.ArchRefChain(
                    archs=[kid[0]],
                    kid=kid,
                )
            else:
                raise self.ice()

        def arch_to_enum_chain(self, kid: list[ast.AstNode]) -> ast.ArchRefChain:
            """Grammar rule.

            arch_to_enum_chain: arch_or_ability_chain? enum_ref
            """
            if len(kid) == 2:
                if isinstance(kid[1], ast.ArchRef) and isinstance(
                    kid[0], ast.ArchRefChain
                ):
                    return ast.ArchRefChain(
                        archs=[*(kid[0].archs), kid[1]],
                        kid=[*(kid[0].kid), kid[1]],
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], ast.ArchRef):
                return ast.ArchRefChain(
                    archs=[kid[0]],
                    kid=kid,
                )
            else:
                raise self.ice()

        def edge_ref_chain(self, kid: list[ast.AstNode]) -> ast.EdgeRefTrailer:
            """Grammar rule.

            (EDGE_OP|NODE_OP)? LSQUARE expression? (edge_op_ref (filter_compr | expression)?)+ RSQUARE
            """
            valid_chain = [i for i in kid if isinstance(i, (ast.Expr, ast.FilterCompr))]
            return ast.EdgeRefTrailer(
                chain=valid_chain,
                edges_only=isinstance(kid[0], ast.Token) and kid[0].name == Tok.EDGE_OP,
                kid=kid,
            )

        def edge_op_ref(self, kid: list[ast.AstNode]) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_op_ref: (edge_any | edge_from | edge_to)
            """
            if isinstance(kid[0], ast.EdgeOpRef):
                return kid[0]
            else:
                raise self.ice()

        def edge_to(self, kid: list[ast.AstNode]) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_to: ARROW_R_P1 typed_filter_compare_list ARROW_R_P2
                   | ARROW_R
            """
            fcond = kid[1] if len(kid) > 1 else None
            if isinstance(fcond, ast.FilterCompr) or fcond is None:
                return ast.EdgeOpRef(filter_cond=fcond, edge_dir=EdgeDir.OUT, kid=kid)
            else:
                raise self.ice()

        def edge_from(self, kid: list[ast.AstNode]) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_from: ARROW_L_P1 typed_filter_compare_list ARROW_L_P2
                     | ARROW_L
            """
            fcond = kid[1] if len(kid) > 1 else None
            if isinstance(fcond, ast.FilterCompr) or fcond is None:
                return ast.EdgeOpRef(filter_cond=fcond, edge_dir=EdgeDir.IN, kid=kid)
            else:
                raise self.ice()

        def edge_any(self, kid: list[ast.AstNode]) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_any: ARROW_L_P1 typed_filter_compare_list ARROW_R_P2
                    | ARROW_BI
            """
            fcond = kid[1] if len(kid) > 1 else None
            if isinstance(fcond, ast.FilterCompr) or fcond is None:
                return ast.EdgeOpRef(filter_cond=fcond, edge_dir=EdgeDir.ANY, kid=kid)
            else:
                raise self.ice()

        def connect_op(self, kid: list[ast.AstNode]) -> ast.ConnectOp:
            """Grammar rule.

            connect_op: connect_from | connect_to | connect_any
            """
            if len(kid) < 2 and isinstance(kid[0], ast.ConnectOp):
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
                    kid=kid,
                )
            else:
                raise self.ice()

        def connect_to(self, kid: list[ast.AstNode]) -> ast.ConnectOp:
            """Grammar rule.

            connect_to: CARROW_R_P1 expression (COLON kw_expr_list)? CARROW_R_P2
                      | CARROW_R
            """
            conn_type = kid[1] if len(kid) >= 3 else None
            conn_assign = kid[3] if len(kid) >= 5 else None
            if (isinstance(conn_type, ast.Expr) or conn_type is None) and (
                isinstance(conn_assign, ast.SubNodeList) or conn_assign is None
            ):
                conn_assign = (
                    ast.AssignCompr(assigns=conn_assign, kid=[conn_assign])
                    if conn_assign
                    else None
                )
                if conn_assign:
                    kid[3] = conn_assign
                return ast.ConnectOp(
                    conn_type=conn_type,
                    conn_assign=conn_assign,
                    edge_dir=EdgeDir.OUT,
                    kid=kid,
                )
            else:
                raise self.ice()

        def connect_from(self, kid: list[ast.AstNode]) -> ast.ConnectOp:
            """Grammar rule.

            connect_from: CARROW_L_P1 expression (COLON kw_expr_list)? CARROW_L_P2
                        | CARROW_L
            """
            conn_type = kid[1] if len(kid) >= 3 else None
            conn_assign = kid[3] if len(kid) >= 5 else None
            if (isinstance(conn_type, ast.Expr) or conn_type is None) and (
                isinstance(conn_assign, ast.SubNodeList) or conn_assign is None
            ):
                conn_assign = (
                    ast.AssignCompr(assigns=conn_assign, kid=[conn_assign])
                    if conn_assign
                    else None
                )
                if conn_assign:
                    kid[3] = conn_assign
                return ast.ConnectOp(
                    conn_type=conn_type,
                    conn_assign=conn_assign,
                    edge_dir=EdgeDir.IN,
                    kid=kid,
                )
            else:
                raise self.ice()

        def connect_any(self, kid: list[ast.AstNode]) -> ast.ConnectOp:
            """Grammar rule.

            connect_any: CARROW_BI | CARROW_L_P1 expression (COLON kw_expr_list)? CARROW_R_P2
            """
            conn_type = kid[1] if len(kid) >= 3 else None
            conn_assign = kid[3] if len(kid) >= 5 else None
            if (isinstance(conn_type, ast.Expr) or conn_type is None) and (
                isinstance(conn_assign, ast.SubNodeList) or conn_assign is None
            ):
                conn_assign = (
                    ast.AssignCompr(assigns=conn_assign, kid=[conn_assign])
                    if conn_assign
                    else None
                )
                if conn_assign:
                    kid[3] = conn_assign
                return ast.ConnectOp(
                    conn_type=conn_type,
                    conn_assign=conn_assign,
                    edge_dir=EdgeDir.ANY,
                    kid=kid,
                )
            else:
                raise self.ice()

        def filter_compr(self, kid: list[ast.AstNode]) -> ast.FilterCompr:
            """Grammar rule.

            filter_compr: LPAREN NULL_OK filter_compare_list RPAREN
                        | LPAREN TYPE_OP NULL_OK typed_filter_compare_list RPAREN
            """
            if isinstance(kid[2], ast.SubNodeList):
                return ast.FilterCompr(compares=kid[2], f_type=None, kid=kid)
            elif isinstance(kid[3], ast.FilterCompr):
                kid[3].add_kids_left(kid[:3])
                kid[3].add_kids_right(kid[4:])
                return kid[3]
            else:
                raise self.ice()

        def filter_compare_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.CompareExpr]:
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
                new_kid = [*consume.kid, comma, expr]
            else:
                expr = kid[0]
                new_kid = [expr]
            valid_kid = [i for i in new_kid if isinstance(i, ast.CompareExpr)]
            return ast.SubNodeList[ast.CompareExpr](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def typed_filter_compare_list(self, kid: list[ast.AstNode]) -> ast.FilterCompr:
            """Grammar rule.

            typed_filter_compare_list: expression (COLON filter_compare_list)?
            """
            chomp = [*kid]
            expr = chomp[0]
            chomp = chomp[1:]
            compares = (
                chomp[1]
                if len(chomp)
                and isinstance(chomp[0], ast.Token)
                and chomp[0].name == Tok.COLON
                else None
            )
            if isinstance(expr, ast.Expr) and (
                (isinstance(compares, ast.SubNodeList)) or compares is None
            ):
                return ast.FilterCompr(compares=compares, f_type=expr, kid=kid)
            else:
                raise self.ice()

        def filter_compare_item(self, kid: list[ast.AstNode]) -> ast.CompareExpr:
            """Grammar rule.

            filter_compare_item: name_ref cmp_op expression
            """
            ret = self.compare(kid)
            if isinstance(ret, ast.CompareExpr):
                return ret
            else:
                raise self.ice()

        def assign_compr(self, kid: list[ast.AstNode]) -> ast.AssignCompr:
            """Grammar rule.

            filter_compr: LPAREN EQ kw_expr_list RPAREN
            """
            if isinstance(kid[2], ast.SubNodeList):
                return ast.AssignCompr(
                    assigns=kid[2],
                    kid=kid,
                )
            else:
                raise self.ice()

        def match_stmt(self, kid: list[ast.AstNode]) -> ast.MatchStmt:
            """Grammar rule.

            match_stmt: KW_MATCH expr_list LBRACE match_case_block+ RBRACE
            """
            cases = [i for i in kid if isinstance(i, ast.MatchCase)]
            if isinstance(kid[1], ast.Expr):
                return ast.MatchStmt(
                    target=kid[1],
                    cases=cases,
                    kid=kid,
                )
            else:
                raise self.ice()

        def match_case_block(self, kid: list[ast.AstNode]) -> ast.MatchCase:
            """Grammar rule.

            match_case_block: KW_CASE pattern_seq (KW_IF expression)? COLON statement_list
            """
            pattern = kid[1]
            guard = kid[3] if isinstance(kid[3], ast.Expr) else None
            stmts = [i for i in kid if isinstance(i, ast.CodeBlockStmt)]
            if isinstance(pattern, ast.MatchPattern) and isinstance(
                guard, (ast.Expr, type(None))
            ):
                return ast.MatchCase(
                    pattern=pattern,
                    guard=guard,
                    body=stmts,
                    kid=kid,
                )
            else:
                raise self.ice()

        def pattern_seq(self, kid: list[ast.AstNode]) -> ast.MatchPattern:
            """Grammar rule.

            pattern_seq: (or_pattern | as_pattern)
            """
            if isinstance(kid[0], ast.MatchPattern):
                return kid[0]
            else:
                raise self.ice()

        def or_pattern(self, kid: list[ast.AstNode]) -> ast.MatchPattern:
            """Grammar rule.

            or_pattern: (pattern BW_OR)* pattern
            """
            if len(kid) == 1:
                if isinstance(kid[0], ast.MatchPattern):
                    return kid[0]
                else:
                    raise self.ice()
            else:
                patterns = [i for i in kid if isinstance(i, ast.MatchPattern)]
                return ast.MatchOr(
                    patterns=patterns,
                    kid=kid,
                )

        def as_pattern(self, kid: list[ast.AstNode]) -> ast.MatchPattern:
            """Grammar rule.

            as_pattern: pattern KW_AS NAME
            """
            if isinstance(kid[0], ast.MatchPattern) and isinstance(
                kid[2], ast.NameAtom
            ):
                return ast.MatchAs(
                    pattern=kid[0],
                    name=kid[2],
                    kid=kid,
                )
            else:
                raise self.ice()

        def pattern(self, kid: list[ast.AstNode]) -> ast.MatchPattern:
            """Grammar rule.

            pattern: literal_pattern
                | capture_pattern
                | sequence_pattern
                | mapping_pattern
                | class_pattern
            """
            if isinstance(kid[0], ast.MatchPattern):
                return kid[0]
            else:
                raise self.ice()

        def literal_pattern(self, kid: list[ast.AstNode]) -> ast.MatchPattern:
            """Grammar rule.

            literal_pattern: (INT | FLOAT | multistring)
            """
            if isinstance(kid[0], ast.Expr):
                return ast.MatchValue(
                    value=kid[0],
                    kid=kid,
                )
            else:
                raise self.ice()

        def singleton_pattern(self, kid: list[ast.AstNode]) -> ast.MatchPattern:
            """Grammar rule.

            singleton_pattern: (NULL | BOOL)
            """
            if isinstance(kid[0], (ast.Bool, ast.Null)):
                return ast.MatchSingleton(
                    value=kid[0],
                    kid=kid,
                )
            else:
                raise self.ice()

        def capture_pattern(self, kid: list[ast.AstNode]) -> ast.MatchPattern:
            """Grammar rule.

            capture_pattern: NAME
            """
            if (
                len(kid) == 1
                and isinstance(kid[0], ast.Name)
                and kid[0].sym_name == "_"
            ):
                return ast.MatchWild(
                    kid=kid,
                )
            if isinstance(kid[0], ast.NameAtom):
                return ast.MatchAs(
                    name=kid[0],
                    pattern=None,
                    kid=kid,
                )
            else:
                raise self.ice()

        def sequence_pattern(self, kid: list[ast.AstNode]) -> ast.MatchPattern:
            """Grammar rule.

            sequence_pattern: LSQUARE list_inner_pattern (COMMA list_inner_pattern)* RSQUARE
                            | LPAREN list_inner_pattern (COMMA list_inner_pattern)* RPAREN
            """
            patterns = [i for i in kid if isinstance(i, ast.MatchPattern)]
            return ast.MatchSequence(
                values=patterns,
                kid=kid,
            )

        def mapping_pattern(self, kid: list[ast.AstNode]) -> ast.MatchMapping:
            """Grammar rule.

            mapping_pattern: LBRACE (dict_inner_pattern (COMMA dict_inner_pattern)*)? RBRACE
            """
            patterns = [
                i for i in kid if isinstance(i, (ast.MatchKVPair, ast.MatchStar))
            ]
            return ast.MatchMapping(
                values=patterns,
                kid=kid,
            )

        def list_inner_pattern(self, kid: list[ast.AstNode]) -> ast.MatchPattern:
            """Grammar rule.

            list_inner_pattern: (pattern_seq | STAR_MUL NAME)
            """
            if isinstance(kid[0], ast.MatchPattern):
                return kid[0]
            elif isinstance(kid[-1], ast.Name):
                return ast.MatchStar(
                    is_list=True,
                    name=kid[-1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def dict_inner_pattern(
            self, kid: list[ast.AstNode]
        ) -> ast.MatchKVPair | ast.MatchStar:
            """Grammar rule.

            dict_inner_pattern: (pattern_seq COLON pattern_seq | STAR_POW NAME)
            """
            if isinstance(kid[0], ast.MatchPattern) and isinstance(
                kid[2], ast.MatchPattern
            ):
                return ast.MatchKVPair(
                    key=kid[0],
                    value=kid[2],
                    kid=kid,
                )
            elif isinstance(kid[-1], ast.Name):
                return ast.MatchStar(
                    is_list=False,
                    name=kid[-1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def class_pattern(self, kid: list[ast.AstNode]) -> ast.MatchArch:
            """Grammar rule.

            class_pattern: NAME (DOT NAME)* LPAREN kw_pattern_list? RPAREN
                        | NAME (DOT NAME)* LPAREN pattern_list (COMMA kw_pattern_list)? RPAREN
            """
            chomp = [*kid]
            cur_element = chomp[0]
            chomp = chomp[1:]
            while not (isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.LPAREN):
                if isinstance(chomp[0], ast.Token) and chomp[0].name == Tok.DOT:
                    target_ = cur_element
                    right_ = chomp[1]
                    if isinstance(right_, (ast.Expr, ast.AtomExpr)) and isinstance(
                        target_, ast.Expr
                    ):
                        cur_element = ast.AtomTrailer(
                            target=target_,
                            right=right_,
                            is_attr=True,
                            is_null_ok=False,
                            kid=[target_, chomp[0], right_],
                        )
                        chomp = chomp[2:]
                    else:
                        raise self.ice()
                elif isinstance(cur_element, ast.NameAtom):
                    chomp = chomp[1:]
                else:
                    break
            name = cur_element
            lparen = chomp[0]
            rapren = chomp[-1]
            first = chomp[1]
            if len(chomp) > 4:
                second = chomp[3]
                comma = chomp[2]
            else:
                second = None
                comma = None
            arg = (
                first
                if isinstance(first, ast.SubNodeList)
                and isinstance(first.items[0], ast.MatchPattern)
                else None
            )
            kw = (
                second
                if isinstance(second, ast.SubNodeList)
                and isinstance(second.items[0], ast.MatchKVPair)
                else (
                    first
                    if isinstance(first, ast.SubNodeList)
                    and isinstance(first.items[0], ast.MatchKVPair)
                    else None
                )
            )
            if isinstance(name, (ast.NameAtom, ast.AtomTrailer)):
                kid_nodes = [name, lparen]
                if arg:
                    kid_nodes.append(arg)
                    if kw:
                        kid_nodes.extend([comma, kw]) if comma else kid_nodes.append(kw)
                elif kw:
                    kid_nodes.append(kw)
                kid_nodes.append(rapren)

                return ast.MatchArch(
                    name=name,
                    arg_patterns=arg,
                    kw_patterns=kw,
                    kid=kid_nodes,
                )
            else:
                raise self.ice()

        def pattern_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.MatchPattern]:
            """Grammar rule.

            pattern_list: (pattern_list COMMA)? pattern_seq
            """
            consume = None
            pattern = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                pattern = kid[2]
            else:
                pattern = kid[0]
            new_kid = [*consume.kid, comma, pattern] if consume else [pattern]
            valid_kid = [i for i in new_kid if isinstance(i, ast.MatchPattern)]
            return ast.SubNodeList[ast.MatchPattern](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=kid,
            )

        def kw_pattern_list(
            self, kid: list[ast.AstNode]
        ) -> ast.SubNodeList[ast.MatchKVPair]:
            """Grammar rule.

            kw_pattern_list: (kw_pattern_list COMMA)? named_ref EQ pattern_seq
            """
            consume = None
            name = None
            eq = None
            value = None
            comma = None
            if isinstance(kid[0], ast.SubNodeList):
                consume = kid[0]
                comma = kid[1]
                name = kid[2]
                eq = kid[3]
                value = kid[4]
                if not isinstance(name, ast.NameAtom) or not isinstance(
                    value, ast.MatchPattern
                ):
                    raise self.ice()
                new_kid = [
                    *consume.kid,
                    comma,
                    ast.MatchKVPair(key=name, value=value, kid=[name, eq, value]),
                ]
            else:
                name = kid[0]
                eq = kid[1]
                value = kid[2]
                if not isinstance(name, ast.NameAtom) or not isinstance(
                    value, ast.MatchPattern
                ):
                    raise self.ice()
                new_kid = [
                    ast.MatchKVPair(key=name, value=value, kid=[name, eq, value])
                ]
            if isinstance(name, ast.NameAtom) and isinstance(value, ast.MatchPattern):
                valid_kid = [i for i in new_kid if isinstance(i, ast.MatchKVPair)]
                return ast.SubNodeList[ast.MatchKVPair](
                    items=valid_kid,
                    delim=Tok.COMMA,
                    kid=new_kid,
                )
            else:
                raise self.ice()

        def __default_token__(self, token: jl.Token) -> ast.Token:
            """Token handler."""
            ret_type = ast.Token
            if token.type in [Tok.NAME, Tok.KWESC_NAME]:
                ret_type = ast.Name
            if token.type in [
                Tok.KW_INIT,
                Tok.KW_POST_INIT,
                Tok.KW_ROOT,
                Tok.KW_SUPER,
                Tok.KW_SELF,
                Tok.KW_HERE,
            ]:
                ret_type = ast.Name
            elif token.type == Tok.SEMI:
                ret_type = ast.Semi
            elif token.type == Tok.NULL:
                ret_type = ast.Null
            elif token.type == Tok.ELLIPSIS:
                ret_type = ast.Ellipsis
            elif token.type == Tok.FLOAT:
                ret_type = ast.Float
            elif token.type in [Tok.INT, Tok.INT, Tok.HEX, Tok.BIN, Tok.OCT]:
                ret_type = ast.Int
            elif token.type in [
                Tok.STRING,
                Tok.FSTR_BESC,
                Tok.FSTR_PIECE,
                Tok.FSTR_SQ_PIECE,
                Tok.DOC_STRING,
            ]:
                ret_type = ast.String
                if token.type == Tok.FSTR_BESC:
                    token.value = token.value[1:]
            elif token.type == Tok.BOOL:
                ret_type = ast.Bool
            elif token.type == Tok.PYNLINE and isinstance(token.value, str):
                token.value = token.value.replace("::py::", "")
            ret = ret_type(
                orig_src=self.parse_ref.source,
                name=token.type,
                value=token.value[2:] if token.type == Tok.KWESC_NAME else token.value,
                line=token.line if token.line is not None else 0,
                end_line=token.end_line if token.end_line is not None else 0,
                col_start=token.column if token.column is not None else 0,
                col_end=token.end_column if token.end_column is not None else 0,
                pos_start=token.start_pos if token.start_pos is not None else 0,
                pos_end=token.end_pos if token.end_pos is not None else 0,
            )
            if isinstance(ret, ast.Name):
                if token.type == Tok.KWESC_NAME:
                    ret.is_kwesc = True
                if ret.value in keyword.kwlist:
                    err = jl.UnexpectedInput(f"Python keyword {ret.value} used as name")
                    err.line = ret.loc.first_line
                    err.column = ret.loc.col_start
                    raise err
            self.terminals.append(ret)
            return ret

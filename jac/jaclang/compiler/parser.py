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
            self.cur_nodes: list[ast.AstNode] = []

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
            self.cur_nodes = new_children or tree.children  # type: ignore[assignment]
            try:
                return self._node_update(super()._call_userfunc(tree, new_children))
            finally:
                self.cur_nodes = []
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
            if (self.node_idx < len(self.cur_nodes)) and isinstance(
                self.cur_nodes[self.node_idx], ty
            ):
                self.node_idx += 1
                return self.cur_nodes[self.node_idx - 1]  # type: ignore[return-value]
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

            module: (toplevel_stmt (tl_stmt_with_doc | toplevel_stmt)*)?
                | STRING (tl_stmt_with_doc | toplevel_stmt)*
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
                    self.cur_nodes
                    or [ast.EmptyToken(ast.JacSource("", self.parse_ref.mod_path))]
                ),
            )
            return mod

        def tl_stmt_with_doc(self, _: None) -> ast.ElementStmt:
            """Grammar rule.

            tl_stmt_with_doc: doc_tag toplevel_stmt
            """
            doc = self.consume(ast.String)
            element = self.consume(ast.ElementStmt)
            element.doc = doc
            element.add_kids_left([doc])
            return element

        def toplevel_stmt(self, _: None) -> ast.ElementStmt:
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
            return ast.GlobalVars(
                access=access_tag,
                assignments=assignments,
                is_frozen=is_frozen,
                kid=self.cur_nodes,
            )

        def access_tag(self, _: None) -> ast.SubTag[ast.Token]:
            """Grammar rule.

            access_tag: COLON ( KW_PROT | KW_PUB | KW_PRIV )
            """
            self.consume_token(Tok.COLON)
            access = self.consume(ast.Token)
            return ast.SubTag[ast.Token](tag=access, kid=self.cur_nodes)

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
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
            )

        def py_code_block(self, _: None) -> ast.PyInlineCode:
            """Grammar rule.

            py_code_block: PYNLINE
            """
            pyinline = self.consume_token(Tok.PYNLINE)
            return ast.PyInlineCode(
                code=pyinline,
                kid=self.cur_nodes,
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
            kid = self.cur_nodes

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
                    kid=self.cur_nodes[2 if lang else 1 : -1],
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
                kids = [i for i in self.cur_nodes if isinstance(i, ast.Token)]
                import_path.level = level
                import_path.add_kids_left(kids)
                return import_path

            return ast.ModulePath(
                path=None,
                level=level,
                alias=None,
                kid=self.cur_nodes,
            )

        def include_stmt(self, _: None) -> ast.Import:
            """Grammar rule.

            include_stmt: KW_INCLUDE sub_name? import_path SEMI
            """
            kid = self.cur_nodes  # TODO: Will be removed.
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
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
            )

        def architype_def(self, _: None) -> ast.ArchDef:
            """Grammar rule.

            architype_def: abil_to_arch_chain member_block
            """
            archref = self.consume(ast.ArchRefChain)
            subnodelist = self.consume(ast.SubNodeList)
            return ast.ArchDef(
                target=archref,
                body=subnodelist,
                kid=self.cur_nodes,
            )

        def arch_type(self, _: None) -> ast.Token:
            """Grammar rule.

            arch_type: KW_WALKER
                    | KW_OBJECT
                    | KW_EDGE
                    | KW_NODE
            """
            return self.consume(ast.Token)

        def decorators(self, _: None) -> ast.SubNodeList[ast.Expr]:
            """Grammar rule.

            decorators: (DECOR_OP atomic_chain)+
            """
            self.consume_token(Tok.DECOR_OP)
            return ast.SubNodeList[ast.Expr](
                items=self.consume_many(ast.Expr),
                delim=Tok.DECOR_OP,
                kid=self.cur_nodes,
            )

        def inherited_archs(self, kid: list[ast.AstNode]) -> ast.SubNodeList[ast.Expr]:
            """Grammar rule.

            inherited_archs: LT (atomic_chain COMMA)* atomic_chain GT
                           | COLON (atomic_chain COMMA)* atomic_chain COLON
            """
            self.match_token(Tok.LT) or self.consume_token(Tok.COLON)
            items: list = []
            while inherited_arch := self.match(ast.Expr):
                items.append(inherited_arch)
                self.match_token(Tok.COMMA)
            self.match_token(Tok.LT) or self.consume_token(Tok.COLON)
            return ast.SubNodeList[ast.Expr](items=items, delim=Tok.COMMA, kid=kid)

        def sub_name(self, _: None) -> ast.SubTag[ast.Name]:
            """Grammar rule.

            sub_name: COLON NAME
            """
            self.consume_token(Tok.COLON)
            target = self.consume(ast.Name)
            return ast.SubTag(
                tag=target,
                kid=self.cur_nodes,
            )

        def named_ref(self, _: None) -> ast.NameAtom:
            """Grammar rule.

            named_ref: special_ref
                    | KWESC_NAME
                    | NAME
            """
            return self.consume(ast.NameAtom)

        def special_ref(self, _: None) -> ast.SpecialVarRef:
            """Grammar rule.

            special_ref: KW_INIT
                        | KW_POST_INIT
                        | KW_ROOT
                        | KW_SUPER
                        | KW_SELF
                        | KW_HERE
            """
            return ast.SpecialVarRef(var=self.consume(ast.Name))

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
                kid=self.cur_nodes,
            )

        def enum_def(self, _: None) -> ast.EnumDef:
            """Grammar rule.

            enum_def: arch_to_enum_chain enum_block
            """
            enum_def = self.consume(ast.ArchRefChain)
            enum_block = self.consume(ast.SubNodeList)
            return ast.EnumDef(
                target=enum_def,
                body=enum_block,
                kid=self.cur_nodes,
            )

        def enum_block(self, _: None) -> ast.SubNodeList[ast.EnumBlockStmt]:
            """Grammar rule.

            enum_block: LBRACE ((enum_stmt COMMA)* enum_stmt COMMA?)? RBRACE
            """
            self.consume_token(Tok.LBRACE)
            enum_statements: list = []
            while enum_stmt := self.match(ast.EnumBlockStmt):
                enum_statements.append(enum_stmt)
                self.match_token(Tok.COMMA)
            self.consume_token(Tok.RBRACE)
            return ast.SubNodeList[ast.EnumBlockStmt](
                items=enum_statements,
                delim=Tok.COMMA,
                kid=self.cur_nodes,
            )

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
            self.cur_nodes[0] = targ
            return ast.Assignment(
                target=targ,
                value=expr,
                type_tag=None,
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
            )

        def ability_def(self, kid: list[ast.AstNode]) -> ast.AbilityDef:
            """Grammar rule.

            ability_def: arch_to_abil_chain (func_decl | event_clause) code_block
            """
            target = self.consume(ast.ArchRefChain)
            signature = self.match(ast.FuncSignature) or self.consume(
                ast.EventSignature
            )
            body = self.consume(ast.SubNodeList)

            return ast.AbilityDef(
                target=target,
                signature=signature,
                body=body,
                kid=self.cur_nodes,
            )

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
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
            )

        def func_decl(self, _: None) -> ast.FuncSignature:
            """Grammar rule.

            func_decl: (LPAREN func_decl_params? RPAREN)? (RETURN_HINT (STRING COLON)? expression)?
            """
            params: ast.SubNodeList | None = None
            return_spec: ast.Expr | None = None
            semstr: ast.String | None = None
            if self.match_token(Tok.LPAREN):
                params = self.match(ast.SubNodeList)
                self.consume_token(Tok.RPAREN)
            if self.match_token(Tok.RETURN_HINT):
                if semstr := self.match(ast.String):
                    self.consume_token(Tok.COLON)
                return_spec = self.match(ast.Expr)
            return ast.FuncSignature(
                semstr=semstr,
                params=params,
                return_type=return_spec,
                kid=(
                    self.cur_nodes
                    if len(self.cur_nodes)
                    else [ast.EmptyToken(ast.JacSource("", self.parse_ref.mod_path))]
                ),
            )

        def func_decl_params(self, _: None) -> ast.SubNodeList[ast.ParamVar]:
            """Grammar rule.

            func_decl_params: (param_var COMMA)* param_var COMMA?
            """
            paramvar: list = []
            while param_stmt := self.match(ast.ParamVar):
                paramvar.append(param_stmt)
                self.match_token(Tok.COMMA)
            return ast.SubNodeList[ast.ParamVar](
                items=paramvar,
                delim=Tok.COMMA,
                kid=self.cur_nodes,
            )

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

        def member_block(self, _: None) -> ast.SubNodeList[ast.ArchBlockStmt]:
            """Grammar rule.

            member_block: LBRACE member_stmt* RBRACE
            """
            left_enc = self.consume_token(Tok.LBRACE)
            items = self.match_many(ast.ArchBlockStmt)
            right_enc = self.consume_token(Tok.RBRACE)
            ret = ast.SubNodeList[ast.ArchBlockStmt](
                items=items,
                delim=Tok.WS,
                kid=self.cur_nodes,
            )
            ret.left_enc = left_enc
            ret.right_enc = right_enc
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

        def has_assign_list(self, _: None) -> ast.SubNodeList[ast.HasVar]:
            """Grammar rule.

            has_assign_list: (has_assign_list COMMA)? typed_has_clause
            """
            if consume := self.match(ast.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                assign = self.consume(ast.HasVar)
                new_kid = [*consume.kid, comma, assign]
            else:
                assign = self.consume(ast.HasVar)
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

        def type_tag(self, _: None) -> ast.SubTag[ast.Expr]:
            """Grammar rule.

            type_tag: COLON expression
            """
            self.consume_token(Tok.COLON)
            tag = self.consume(ast.Expr)
            return ast.SubTag[ast.Expr](tag=tag, kid=self.cur_nodes)

        def builtin_type(self, _: None) -> ast.Token:
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
            token = self.consume(ast.Token)
            return ast.BuiltinType(
                name=token.name,
                orig_src=self.parse_ref.source,
                value=token.value,
                line=token.loc.first_line,
                end_line=token.loc.last_line,
                col_start=token.loc.col_start,
                col_end=token.loc.col_end,
                pos_start=token.pos_start,
                pos_end=token.pos_end,
            )

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
            if (code_block := self.match(ast.CodeBlockStmt)) and len(
                self.cur_nodes
            ) < 2:
                return code_block
            elif (token := self.match(ast.Token)) and token.name == Tok.KW_YIELD:
                return ast.ExprStmt(
                    expr=(
                        expr := ast.YieldExpr(
                            expr=None,
                            with_from=False,
                            kid=self.cur_nodes,
                        )
                    ),
                    in_fstring=False,
                    kid=[expr],
                )
            elif isinstance(kid[0], ast.Expr):
                return ast.ExprStmt(
                    expr=kid[0],
                    in_fstring=False,
                    kid=self.cur_nodes,
                )
            elif isinstance(kid[0], ast.CodeBlockStmt):
                kid[0].add_kids_right([kid[1]])
                return kid[0]
            else:
                raise self.ice()

        def typed_ctx_block(self, _: None) -> ast.TypedCtxBlock:
            """Grammar rule.

            typed_ctx_block: RETURN_HINT expression code_block
            """
            self.consume_token(Tok.RETURN_HINT)
            ctx = self.consume(ast.Expr)
            body = self.consume(ast.SubNodeList)
            return ast.TypedCtxBlock(
                type_ctx=ctx,
                body=body,
                kid=self.cur_nodes,
            )

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
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
            )

        def else_stmt(self, _: None) -> ast.ElseStmt:
            """Grammar rule.

            else_stmt: KW_ELSE code_block
            """
            self.consume_token(Tok.KW_ELSE)
            body = self.consume(ast.SubNodeList)
            return ast.ElseStmt(
                body=body,
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
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
                kid=self.cur_nodes,
            )

        def finally_stmt(self, _: None) -> ast.FinallyStmt:
            """Grammar rule.

            finally_stmt: KW_FINALLY code_block
            """
            self.consume_token(Tok.KW_FINALLY)
            body = self.consume(ast.SubNodeList)
            return ast.FinallyStmt(
                body=body,
                kid=self.cur_nodes,
            )

        def for_stmt(self, _: None) -> ast.IterForStmt | ast.InForStmt:
            """Grammar rule.

            for_stmt: KW_ASYNC? KW_FOR assignment KW_TO expression KW_BY
                        expression code_block else_stmt?
                    | KW_ASYNC? KW_FOR expression KW_IN expression code_block else_stmt?
            """
            is_async = bool(self.match_token(Tok.KW_ASYNC))
            self.consume_token(Tok.KW_FOR)
            if iter := self.match(ast.Assignment):
                self.consume_token(Tok.KW_TO)
                condition = self.consume(ast.Expr)
                self.consume_token(Tok.KW_BY)
                count_by = self.consume(ast.Assignment)
                body = self.consume(ast.SubNodeList)
                else_body = self.match(ast.ElseStmt)
                return ast.IterForStmt(
                    is_async=is_async,
                    iter=iter,
                    condition=condition,
                    count_by=count_by,
                    body=body,
                    else_body=else_body,
                    kid=self.cur_nodes,
                )
            target = self.consume(ast.Expr)
            self.consume_token(Tok.KW_IN)
            collection = self.consume(ast.Expr)
            body = self.consume(ast.SubNodeList)
            else_body = self.match(ast.ElseStmt)
            return ast.InForStmt(
                is_async=is_async,
                target=target,
                collection=collection,
                body=body,
                else_body=else_body,
                kid=self.cur_nodes,
            )

        def while_stmt(self, _: None) -> ast.WhileStmt:
            """Grammar rule.

            while_stmt: KW_WHILE expression code_block
            """
            self.consume_token(Tok.KW_WHILE)
            condition = self.consume(ast.Expr)
            body = self.consume(ast.SubNodeList)
            return ast.WhileStmt(
                condition=condition,
                body=body,
                kid=self.cur_nodes,
            )

        def with_stmt(self, _: None) -> ast.WithStmt:
            """Grammar rule.

            with_stmt: KW_ASYNC? KW_WITH expr_as_list code_block
            """
            is_async = bool(self.match_token(Tok.KW_ASYNC))
            self.consume_token(Tok.KW_WITH)
            exprs = self.consume(ast.SubNodeList)
            body = self.consume(ast.SubNodeList)
            return ast.WithStmt(
                is_async=is_async,
                exprs=exprs,
                body=body,
                kid=self.cur_nodes,
            )

        def expr_as_list(self, _: None) -> ast.SubNodeList[ast.ExprAsItem]:
            """Grammar rule.

            expr_as_list: (expr_as COMMA)* expr_as
            """
            items = [self.consume(ast.ExprAsItem)]
            while self.match_token(Tok.COMMA):
                items.append(self.consume(ast.ExprAsItem))
            return ast.SubNodeList[ast.ExprAsItem](
                items=items,
                delim=Tok.COMMA,
                kid=self.cur_nodes,
            )

        def expr_as(self, _: None) -> ast.ExprAsItem:
            """Grammar rule.

            expr_as: expression (KW_AS expression)?
            """
            expr = self.consume(ast.Expr)
            alias = self.consume(ast.Expr) if self.match_token(Tok.KW_AS) else None
            return ast.ExprAsItem(
                expr=expr,
                alias=alias,
                kid=self.cur_nodes,
            )

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

        def assert_stmt(self, _: None) -> ast.AssertStmt:
            """Grammar rule.

            assert_stmt: KW_ASSERT expression (COMMA expression)?
            """
            error_msg: ast.Expr | None = None
            self.consume_token(Tok.KW_ASSERT)
            condition = self.consume(ast.Expr)
            if self.match_token(Tok.COMMA):
                error_msg = self.consume(ast.Expr)
            return ast.AssertStmt(
                condition=condition,
                error_msg=error_msg,
                kid=self.cur_nodes,
            )

        def check_stmt(self, _: None) -> ast.CheckStmt:
            """Grammar rule.

            check_stmt: KW_CHECK expression
            """
            self.consume_token(Tok.KW_CHECK)
            target = self.consume(ast.Expr)
            return ast.CheckStmt(
                target=target,
                kid=self.cur_nodes,
            )

        def ctrl_stmt(self, _: None) -> ast.CtrlStmt:
            """Grammar rule.

            ctrl_stmt: KW_SKIP | KW_BREAK | KW_CONTINUE
            """
            tok = (
                self.match_token(Tok.KW_SKIP)
                or self.match_token(Tok.KW_BREAK)
                or self.consume_token(Tok.KW_CONTINUE)
            )
            return ast.CtrlStmt(
                ctrl=tok,
                kid=self.cur_nodes,
            )

        def delete_stmt(self, _: None) -> ast.DeleteStmt:
            """Grammar rule.

            delete_stmt: KW_DELETE expression
            """
            self.consume_token(Tok.KW_DELETE)
            target = self.consume(ast.Expr)
            return ast.DeleteStmt(
                target=target,
                kid=self.cur_nodes,
            )

        def report_stmt(self, _: None) -> ast.ReportStmt:
            """Grammar rule.

            report_stmt: KW_REPORT expression
            """
            self.consume_token(Tok.KW_REPORT)
            target = self.consume(ast.Expr)
            return ast.ReportStmt(
                expr=target,
                kid=self.cur_nodes,
            )

        def return_stmt(self, _: None) -> ast.ReturnStmt:
            """Grammar rule.

            return_stmt: KW_RETURN expression?
            """
            self.consume_token(Tok.KW_RETURN)
            expr = self.match(ast.Expr)
            return ast.ReturnStmt(
                expr=expr,
                kid=self.cur_nodes,
            )

        def walker_stmt(self, _: None) -> ast.CodeBlockStmt:
            """Grammar rule.

            walker_stmt: disengage_stmt | revisit_stmt | visit_stmt | ignore_stmt
            """
            return self.consume(ast.CodeBlockStmt)

        def ignore_stmt(self, _: None) -> ast.IgnoreStmt:
            """Grammar rule.

            ignore_stmt: KW_IGNORE expression SEMI
            """
            self.consume_token(Tok.KW_IGNORE)
            target = self.consume(ast.Expr)
            self.consume_token(Tok.SEMI)
            return ast.IgnoreStmt(
                target=target,
                kid=self.cur_nodes,
            )

        def visit_stmt(self, _: None) -> ast.VisitStmt:
            """Grammar rule.

            visit_stmt: KW_VISIT (inherited_archs)? expression (else_stmt | SEMI)
            """
            self.consume_token(Tok.KW_VISIT)
            sub_name = self.match(ast.SubNodeList)
            target = self.consume(ast.Expr)
            else_body = self.match(ast.ElseStmt)
            if else_body is None:
                self.consume_token(Tok.SEMI)
            return ast.VisitStmt(
                vis_type=sub_name,
                target=target,
                else_body=else_body,
                kid=self.cur_nodes,
            )

        def revisit_stmt(self, _: None) -> ast.RevisitStmt:
            """Grammar rule.

            revisit_stmt: KW_REVISIT expression? (else_stmt | SEMI)
            """
            self.consume_token(Tok.KW_REVISIT)
            target = self.match(ast.Expr)
            else_body = self.match(ast.ElseStmt)
            if else_body is None:
                self.consume_token(Tok.SEMI)
            return ast.RevisitStmt(
                hops=target,
                else_body=else_body,
                kid=self.cur_nodes,
            )

        def disengage_stmt(self, _: None) -> ast.DisengageStmt:
            """Grammar rule.

            disengage_stmt: KW_DISENGAGE SEMI
            """
            kw = self.consume_token(Tok.KW_DISENGAGE)
            semi = self.consume_token(Tok.SEMI)
            return ast.DisengageStmt(
                kid=[kw, semi],
            )

        def global_ref(self, _: None) -> ast.GlobalStmt:
            """Grammar rule.

            global_ref: GLOBAL_OP name_list
            """
            self.consume_token(Tok.GLOBAL_OP)
            target = self.consume(ast.SubNodeList)
            return ast.GlobalStmt(
                target=target,
                kid=self.cur_nodes,
            )

        def nonlocal_ref(self, _: None) -> ast.NonLocalStmt:
            """Grammar rule.

            nonlocal_ref: NONLOCAL_OP name_list
            """
            self.consume_token(Tok.NONLOCAL_OP)
            target = self.consume(ast.SubNodeList)
            return ast.NonLocalStmt(
                target=target,
                kid=self.cur_nodes,
            )

        def assignment(self, _: None) -> ast.Assignment:
            """Grammar rule.

            assignment: KW_LET? (atomic_chain EQ)+ (yield_expr | expression)
                    | atomic_chain (COLON STRING)? type_tag (EQ (yield_expr | expression))?
                    | atomic_chain aug_op (yield_expr | expression)
            """
            assignees: list = []
            type_tag: ast.SubTag | None = None
            is_aug: ast.Token | None = None
            semstr: ast.String | None = None

            is_frozen = bool(self.match_token(Tok.KW_LET))
            if first_expr := self.match(ast.Expr):
                assignees.append(first_expr)

            token = self.match(ast.Token)
            if token and (token.name == Tok.EQ):
                assignees.append(token)
                while expr := self.match(ast.Expr):
                    eq = self.match_token(Tok.EQ)
                    assignees.append(expr)
                    if eq:
                        assignees.append(eq)
                value = assignees.pop()
            elif token and (token.name not in {Tok.COLON, Tok.EQ}):
                is_aug = token
                value = self.consume(ast.Expr)
            else:
                semstr = (
                    self.match(ast.String)
                    if (token and (token.name == Tok.COLON))
                    else None
                )
                type_tag = self.consume(ast.SubTag)
                value = self.consume(ast.Expr) if self.match_token(Tok.EQ) else None

            valid_assignees = [i for i in assignees if isinstance(i, (ast.Expr))]
            new_targ = ast.SubNodeList[ast.Expr](
                items=valid_assignees,
                delim=Tok.EQ,
                kid=assignees,
            )
            kid = [x for x in self.cur_nodes if x not in assignees]
            kid.insert(1, new_targ) if is_frozen else kid.insert(0, new_targ)
            if is_aug:
                return ast.Assignment(
                    target=new_targ,
                    type_tag=type_tag,
                    value=value,
                    mutable=is_frozen,
                    aug_op=is_aug,
                    kid=kid,
                )
            return ast.Assignment(
                target=new_targ,
                type_tag=type_tag,
                value=value,
                mutable=is_frozen,
                kid=kid,
                semstr=semstr,
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
                    kid=self.cur_nodes,
                )
            return value

        def walrus_assign(self, _: None) -> ast.Expr:
            """Grammar rule.

            walrus_assign: (walrus_assign WALRUS_EQ)? pipe
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def lambda_expr(self, _: None) -> ast.LambdaExpr:
            """Grammar rule.

            lamda_expr: KW_WITH func_decl_params? (RETURN_HINT expression)? KW_CAN expression
            """
            return_type: ast.Expr | None = None
            sig_kid: list[ast.AstNode] = []
            self.consume_token(Tok.KW_WITH)
            params = self.match(ast.SubNodeList)
            if self.match_token(Tok.RETURN_HINT):
                return_type = self.consume(ast.Expr)
            self.consume_token(Tok.KW_CAN)
            body = self.consume(ast.Expr)
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
            new_kid = [i for i in self.cur_nodes if i != params and i != return_type]
            new_kid.insert(1, signature) if signature else None
            return ast.LambdaExpr(
                signature=signature,
                body=body,
                kid=new_kid,
            )

        def pipe(self, _: None) -> ast.Expr:
            """Grammar rule.

            pipe: pipe_back PIPE_FWD pipe
                | pipe_back
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def pipe_back(self, _: None) -> ast.Expr:
            """Grammar rule.

            pipe_back: bitwise_or PIPE_BKWD pipe_back
                     | bitwise_or
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def bitwise_or(self, _: None) -> ast.Expr:
            """Grammar rule.

            bitwise_or: bitwise_xor BW_OR bitwise_or
                      | bitwise_xor
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def bitwise_xor(self, _: None) -> ast.Expr:
            """Grammar rule.

            bitwise_xor: bitwise_and BW_XOR bitwise_xor
                       | bitwise_and
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def bitwise_and(self, _: None) -> ast.Expr:
            """Grammar rule.

            bitwise_and: shift BW_AND bitwise_and
                       | shift
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def shift(self, _: None) -> ast.Expr:
            """Grammar rule.

            shift: (shift (RSHIFT | LSHIFT))? logical_or
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def logical_or(self, _: None) -> ast.Expr:
            """Grammar rule.

            logical_or: logical_and (KW_OR logical_and)*
            """
            value = self.consume(ast.Expr)
            if not (ops := self.match_token(Tok.KW_OR)):
                return value
            values: list = [value]
            while value := self.consume(ast.Expr):
                values.append(value)
                if not self.match_token(Tok.KW_OR):
                    break
            return ast.BoolExpr(
                op=ops,
                values=values,
                kid=self.cur_nodes,
            )

        def logical_and(self, _: None) -> ast.Expr:
            """Grammar rule.

            logical_and: logical_not (KW_AND logical_not)*
            """
            value = self.consume(ast.Expr)
            if not (ops := self.match_token(Tok.KW_AND)):
                return value
            values: list = [value]
            while value := self.consume(ast.Expr):
                values.append(value)
                if not self.match_token(Tok.KW_AND):
                    break
            return ast.BoolExpr(
                op=ops,
                values=values,
                kid=self.cur_nodes,
            )

        def logical_not(self, _: None) -> ast.Expr:
            """Grammar rule.

            logical_not: NOT logical_not | compare
            """
            if op := self.match_token(Tok.NOT):
                operand = self.consume(ast.Expr)
                return ast.UnaryExpr(
                    op=op,
                    operand=operand,
                    kid=self.cur_nodes,
                )
            return self.consume(ast.Expr)

        def compare(self, _: None) -> ast.Expr:
            """Grammar rule.

            compare: (arithmetic cmp_op)* arithmetic
            """
            ops: list = []
            rights: list = []
            left = self.consume(ast.Expr)
            while op := self.match(ast.Token):
                ops.append(op)
                rights.append(self.consume(ast.Expr))
            if not ops:
                return left
            return ast.CompareExpr(
                left=left,
                ops=ops,
                rights=rights,
                kid=self.cur_nodes,
            )

        def cmp_op(self, _: None) -> ast.Token:
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
            return self.consume(ast.Token)

        def arithmetic(self, _: None) -> ast.Expr:
            """Grammar rule.

            arithmetic: (arithmetic (MINUS | PLUS))? term
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def term(self, _: None) -> ast.Expr:
            """Grammar rule.

            term: (term (MOD | DIV | FLOOR_DIV | STAR_MUL | DECOR_OP))? power
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def factor(self, _: None) -> ast.Expr:
            """Grammar rule.

            factor: (BW_NOT | MINUS | PLUS) factor | connect
            """
            if (
                op := self.match_token(Tok.BW_NOT)
                or self.match_token(Tok.MINUS)
                or self.match_token(Tok.PLUS)
            ):
                operand = self.consume(ast.Expr)
                return ast.UnaryExpr(
                    op=op,
                    operand=operand,
                    kid=self.cur_nodes,
                )
            return self._binary_expr_unwind(self.cur_nodes)

        def power(self, _: None) -> ast.Expr:
            """Grammar rule.

            power: (power STAR_POW)? factor
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def connect(self, _: None) -> ast.Expr:
            """Grammar rule.

            connect: (connect (connect_op | disconnect_op))? atomic_pipe
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def atomic_pipe(self, _: None) -> ast.Expr:
            """Grammar rule.

            atomic_pipe: (atomic_pipe A_PIPE_FWD)? atomic_pipe_back
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def atomic_pipe_back(self, _: None) -> ast.Expr:
            """Grammar rule.

            atomic_pipe_back: (atomic_pipe_back A_PIPE_BKWD)? ds_spawn
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def ds_spawn(self, _: None) -> ast.Expr:
            """Grammar rule.

            ds_spawn: (ds_spawn KW_SPAWN)? unpack
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def unpack(self, _: None) -> ast.Expr:
            """Grammar rule.

            unpack: STAR_MUL? ref
            """
            if op := self.match_token(Tok.STAR_MUL):
                operand = self.consume(ast.Expr)
                return ast.UnaryExpr(
                    op=op,
                    operand=operand,
                    kid=self.cur_nodes,
                )
            return self._binary_expr_unwind(self.cur_nodes)

        def ref(self, _: None) -> ast.Expr:
            """Grammar rule.

            ref: walrus_assign
               | BW_AND walrus_assign
            """
            if op := self.match_token(Tok.BW_AND):
                operand = self.consume(ast.Expr)
                return ast.UnaryExpr(
                    op=op,
                    operand=operand,
                    kid=self.cur_nodes,
                )
            return self._binary_expr_unwind(self.cur_nodes)

        def pipe_call(self, _: None) -> ast.Expr:
            """Grammar rule.

            pipe_call: atomic_chain
                | PIPE_FWD atomic_chain
                | A_PIPE_FWD atomic_chain
                | KW_SPAWN atomic_chain
                | KW_AWAIT atomic_chain
            """
            if len(self.cur_nodes) == 2:
                if self.match_token(Tok.KW_AWAIT):
                    target = self.consume(ast.Expr)
                    return ast.AwaitExpr(
                        target=target,
                        kid=self.cur_nodes,
                    )
                elif op := self.match(ast.Token):
                    operand = self.consume(ast.Expr)
                    return ast.UnaryExpr(
                        op=op,
                        operand=operand,
                        kid=self.cur_nodes,
                    )
            return self._binary_expr_unwind(self.cur_nodes)

        def aug_op(self, _: None) -> ast.Token:
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
            return self.consume(ast.Token)

        def atomic_chain(self, _: None) -> ast.Expr:
            """Grammar rule.

            atomic_chain: atomic_chain NULL_OK? (filter_compr | assign_compr | index_slice)
                        | atomic_chain NULL_OK? (DOT_BKWD | DOT_FWD | DOT) named_ref
                        | (atomic_call | atom | edge_ref_chain)
            """
            if len(self.cur_nodes) == 1:
                return self.consume(ast.Expr)
            target = self.consume(ast.Expr)
            is_null_ok = bool(self.match_token(Tok.NULL_OK))
            if right := self.match(ast.AtomExpr):
                return ast.AtomTrailer(
                    target=target,
                    right=right,
                    is_null_ok=is_null_ok,
                    is_attr=False,
                    kid=self.cur_nodes,
                )
            token = (
                self.match_token(Tok.DOT_BKWD)
                or self.match_token(Tok.DOT_FWD)
                or self.consume_token(Tok.DOT)
            )
            name = self.match(ast.AtomExpr) or self.consume(ast.AtomTrailer)
            return ast.AtomTrailer(
                target=(target if token.name != Tok.DOT_BKWD else name),
                right=(name if token.name != Tok.DOT_BKWD else target),
                is_null_ok=is_null_ok,
                is_attr=True,
                kid=self.cur_nodes,
            )

        def atomic_call(self, _: None) -> ast.FuncCall:
            """Grammar rule.

            atomic_call: atomic_chain LPAREN param_list? (KW_BY atomic_call)? RPAREN
            """
            genai_call: ast.FuncCall | None = None
            target = self.consume(ast.Expr)
            self.consume_token(Tok.LPAREN)
            params = self.match(ast.SubNodeList)
            if self.match_token(Tok.KW_BY):
                genai_call = self.consume(ast.FuncCall)
            self.consume_token(Tok.RPAREN)
            return ast.FuncCall(
                target=target,
                params=params,
                genai_call=genai_call,
                kid=self.cur_nodes,
            )

        def index_slice(self, _: None) -> ast.IndexSlice:
            """Grammar rule.

            index_slice: LSQUARE                                                        \
                            expression? COLON expression? (COLON expression?)?          \
                            (COMMA expression? COLON expression? (COLON expression?)?)* \
                         RSQUARE
                        | list_val
            """
            if len(self.cur_nodes) == 1:
                index = self.consume(ast.ListVal)
                if not index.values:
                    raise self.ice()
                if len(index.values.items) == 1:
                    expr = index.values.items[0] if index.values else None
                    kid = self.cur_nodes
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
                self.consume_token(Tok.LSQUARE)
                slices: list[ast.IndexSlice.Slice] = []
                while not self.match_token(Tok.RSQUARE):
                    expr1 = self.match(ast.Expr)
                    self.consume_token(Tok.COLON)
                    expr2 = self.match(ast.Expr)
                    expr3 = (
                        self.match(ast.Expr) if self.match_token(Tok.COLON) else None
                    )
                    self.match_token(Tok.COMMA)
                    slices.append(
                        ast.IndexSlice.Slice(start=expr1, stop=expr2, step=expr3)
                    )
                return ast.IndexSlice(
                    slices=slices,
                    is_range=True,
                    kid=self.cur_nodes,
                )

        def atom(self, _: None) -> ast.Expr:
            """Grammar rule.

            atom: named_ref
                 | LPAREN (expression | yield_expr) RPAREN
                 | atom_collection
                 | atom_literal
                 | type_ref
            """
            if self.match_token(Tok.LPAREN):
                value = self.match(ast.Expr) or self.consume(ast.YieldExpr)
                self.consume_token(Tok.RPAREN)
                return ast.AtomUnit(value=value, kid=self.cur_nodes)
            return self.consume(ast.AtomExpr)

        def yield_expr(self, _: None) -> ast.YieldExpr:
            """Grammar rule.

            yield_expr: KW_YIELD KW_FROM? expression
            """
            self.consume_token(Tok.KW_YIELD)
            is_with_from = bool(self.match_token(Tok.KW_FROM))
            expr = self.consume(ast.Expr)
            return ast.YieldExpr(
                expr=expr,
                with_from=is_with_from,
                kid=self.cur_nodes,
            )

        def atom_literal(self, _: None) -> ast.AtomExpr:
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
            return self.consume(ast.AtomExpr)

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
            return self.consume(ast.AtomExpr)

        def multistring(self, _: None) -> ast.AtomExpr:
            """Grammar rule.

            multistring: (fstring | STRING)+
            """
            valid_strs = [self.match(ast.String) or self.consume(ast.FString)]
            while node := (self.match(ast.String) or self.match(ast.FString)):
                valid_strs.append(node)
            return ast.MultiString(
                strings=valid_strs,
                kid=self.cur_nodes,
            )

        def fstring(self, _: None) -> ast.FString:
            """Grammar rule.

            fstring: FSTR_START fstr_parts FSTR_END
                | FSTR_SQ_START fstr_sq_parts FSTR_SQ_END
            """
            self.match_token(Tok.FSTR_START) or self.consume_token(Tok.FSTR_SQ_START)
            target = self.match(ast.SubNodeList)
            self.match_token(Tok.FSTR_END) or self.consume_token(Tok.FSTR_SQ_END)
            return ast.FString(
                parts=target,
                kid=self.cur_nodes,
            )

        def fstr_parts(self, _: None) -> ast.SubNodeList[ast.String | ast.ExprStmt]:
            """Grammar rule.

            fstr_parts: (FSTR_PIECE | FSTR_BESC | LBRACE expression RBRACE )*
            """
            valid_parts: list[ast.String | ast.ExprStmt] = [
                (
                    i
                    if isinstance(i, ast.String)
                    else ast.ExprStmt(expr=i, in_fstring=True, kid=[i])
                )
                for i in self.cur_nodes
                if isinstance(i, ast.Expr)
            ]
            return ast.SubNodeList[ast.String | ast.ExprStmt](
                items=valid_parts,
                delim=None,
                kid=valid_parts,
            )

        def fstr_sq_parts(self, _: None) -> ast.SubNodeList[ast.String | ast.ExprStmt]:
            """Grammar rule.

            fstr_sq_parts: (FSTR_SQ_PIECE | FSTR_BESC | LBRACE expression RBRACE )*
            """
            valid_parts: list[ast.String | ast.ExprStmt] = [
                (
                    i
                    if isinstance(i, ast.String)
                    else ast.ExprStmt(expr=i, in_fstring=True, kid=[i])
                )
                for i in self.cur_nodes
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

        def tuple_val(self, _: None) -> ast.TupleVal:
            """Grammar rule.

            tuple_val: LPAREN tuple_list? RPAREN
            """
            self.consume_token(Tok.LPAREN)
            target = self.match(ast.SubNodeList)
            self.consume_token(Tok.RPAREN)
            return ast.TupleVal(
                values=target,
                kid=self.cur_nodes,
            )

        def set_val(self, _: None) -> ast.SetVal:
            """Grammar rule.

            set_val: LBRACE expr_list COMMA? RBRACE
            """
            self.match_token(Tok.LBRACE)
            expr_list = self.match(ast.SubNodeList)
            self.match_token(Tok.COMMA)
            self.match_token(Tok.RBRACE)
            return ast.SetVal(
                values=expr_list,
                kid=self.cur_nodes,
            )

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
            if consume := self.match(ast.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                expr = self.consume(ast.KWPair)
                new_kid = [*consume.kid, comma, expr]
            else:
                expr = self.consume(ast.KWPair)
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

        def tuple_list(self, _: None) -> ast.SubNodeList[ast.Expr | ast.KWPair]:
            """Grammar rule.

            tuple_list: expression COMMA expr_list    COMMA kw_expr_list COMMA?
                      | expression COMMA kw_expr_list COMMA?
                      | expression COMMA expr_list    COMMA?
                      | expression COMMA
                      | kw_expr_list COMMA?
            """
            if first_expr := self.match(ast.SubNodeList):
                comma = self.match_token(Tok.COMMA)
                if comma:
                    first_expr.kid.append(comma)
                return first_expr
            expr = self.consume(ast.Expr)
            self.consume_token(Tok.COMMA)
            second_expr = self.match(ast.SubNodeList)
            self.match_token(Tok.COMMA)
            kw_expr_list = self.match(ast.SubNodeList)
            self.match_token(Tok.COMMA)
            expr_list: list = []
            if second_expr:
                expr_list = second_expr.kid
                if kw_expr_list:
                    expr_list = [*expr_list, *kw_expr_list.kid]
            expr_list = [expr, *expr_list]
            valid_kid = [i for i in expr_list if isinstance(i, (ast.Expr, ast.KWPair))]
            return ast.SubNodeList[ast.Expr | ast.KWPair](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=self.cur_nodes,
            )

        def dict_val(self, _: None) -> ast.DictVal:
            """Grammar rule.

            dict_val: LBRACE ((kv_pair COMMA)* kv_pair COMMA?)? RBRACE
            """
            self.consume_token(Tok.LBRACE)
            kv_pairs: list = []
            while item := self.match(ast.KVPair):
                kv_pairs.append(item)
                self.match_token(Tok.COMMA)
            self.consume_token(Tok.RBRACE)
            return ast.DictVal(
                kv_pairs=kv_pairs,
                kid=self.cur_nodes,
            )

        def kv_pair(self, _: None) -> ast.KVPair:
            """Grammar rule.

            kv_pair: expression COLON expression | STAR_POW expression
            """
            if self.match_token(Tok.STAR_POW):
                value = self.consume(ast.Expr)
                return ast.KVPair(
                    key=None,
                    value=value,
                    kid=self.cur_nodes,
                )
            key = self.consume(ast.Expr)
            self.consume_token(Tok.COLON)
            value = self.consume(ast.Expr)
            return ast.KVPair(
                key=key,
                value=value,
                kid=self.cur_nodes,
            )

        def list_compr(self, _: None) -> ast.ListCompr:
            """Grammar rule.

            list_compr: LSQUARE expression inner_compr+ RSQUARE
            """
            self.consume_token(Tok.LSQUARE)
            out_expr = self.consume(ast.Expr)
            comprs = self.consume_many(ast.InnerCompr)
            self.consume_token(Tok.RSQUARE)
            return ast.ListCompr(
                out_expr=out_expr,
                compr=comprs,
                kid=self.cur_nodes,
            )

        def gen_compr(self, _: None) -> ast.GenCompr:
            """Grammar rule.

            gen_compr: LPAREN expression inner_compr+ RPAREN
            """
            self.consume_token(Tok.LPAREN)
            out_expr = self.consume(ast.Expr)
            comprs = self.consume_many(ast.InnerCompr)
            self.consume_token(Tok.RPAREN)
            return ast.GenCompr(
                out_expr=out_expr,
                compr=comprs,
                kid=self.cur_nodes,
            )

        def set_compr(self, _: None) -> ast.SetCompr:
            """Grammar rule.

            set_compr: LBRACE expression inner_compr+ RBRACE
            """
            self.consume_token(Tok.LBRACE)
            out_expr = self.consume(ast.Expr)
            comprs = self.consume_many(ast.InnerCompr)
            self.consume_token(Tok.RBRACE)
            return ast.SetCompr(
                out_expr=out_expr,
                compr=comprs,
                kid=self.cur_nodes,
            )

        def dict_compr(self, _: None) -> ast.DictCompr:
            """Grammar rule.

            dict_compr: LBRACE kv_pair inner_compr+ RBRACE
            """
            self.consume_token(Tok.LBRACE)
            kv_pair = self.consume(ast.KVPair)
            comprs = self.consume_many(ast.InnerCompr)
            self.consume_token(Tok.RBRACE)
            return ast.DictCompr(
                kv_pair=kv_pair,
                compr=comprs,
                kid=self.cur_nodes,
            )

        def inner_compr(self, _: None) -> ast.InnerCompr:
            """Grammar rule.

            inner_compr: KW_ASYNC? KW_FOR atomic_chain KW_IN pipe_call (KW_IF walrus_assign)*
            """
            conditional: list = []
            is_async = bool(self.match_token(Tok.KW_ASYNC))
            self.consume_token(Tok.KW_FOR)
            target = self.consume(ast.Expr)
            self.consume_token(Tok.KW_IN)
            collection = self.consume(ast.Expr)
            while self.match_token(Tok.KW_IF):
                conditional.append(self.consume(ast.Expr))
            return ast.InnerCompr(
                is_async=is_async,
                target=target,
                collection=collection,
                conditional=conditional,
                kid=self.cur_nodes,
            )

        def param_list(self, _: None) -> ast.SubNodeList[ast.Expr | ast.KWPair]:
            """Grammar rule.

            param_list: expr_list    COMMA kw_expr_list COMMA?
                      | kw_expr_list COMMA?
                      | expr_list    COMMA?
            """
            kw_expr_list: ast.SubNodeList | None = None
            expr_list = self.consume(ast.SubNodeList)
            if len(self.cur_nodes) > 2:
                self.consume_token(Tok.COMMA)
                kw_expr_list = self.consume(ast.SubNodeList)
            ends_comma = self.match_token(Tok.COMMA)
            if kw_expr_list:
                valid_kid = [
                    i
                    for i in [*expr_list.items, *kw_expr_list.items]
                    if isinstance(i, (ast.Expr, ast.KWPair))
                ]
                return ast.SubNodeList[ast.Expr | ast.KWPair](
                    items=valid_kid,
                    delim=Tok.COMMA,
                    kid=self.cur_nodes,
                )
            else:
                if ends_comma:
                    expr_list.kid.append(ends_comma)
                return expr_list

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
            return self.consume(ast.ArchRef)

        def node_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            node_ref: NODE_OP NAME
            """
            arch_type = self.consume(ast.Token)
            arch_name = self.consume(ast.NameAtom)
            return ast.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def edge_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            edge_ref: EDGE_OP NAME
            """
            arch_type = self.consume(ast.Token)
            arch_name = self.consume(ast.NameAtom)
            return ast.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def walker_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            walker_ref: WALKER_OP NAME
            """
            arch_type = self.consume(ast.Token)
            arch_name = self.consume(ast.NameAtom)
            return ast.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def class_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            class_ref: CLASS_OP name_ref
            """
            arch_type = self.consume(ast.Token)
            arch_name = self.consume(ast.NameAtom)
            return ast.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def object_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            object_ref: OBJECT_OP name_ref
            """
            arch_type = self.consume(ast.Token)
            arch_name = self.consume(ast.NameAtom)
            return ast.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def type_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            type_ref: TYPE_OP (named_ref | builtin_type)
            """
            arch_type = self.consume(ast.Token)
            arch_name = self.consume(ast.NameAtom)
            return ast.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def enum_ref(self, kid: list[ast.AstNode]) -> ast.ArchRef:
            """Grammar rule.

            enum_ref: ENUM_OP NAME
            """
            arch_type = self.consume(ast.Token)
            arch_name = self.consume(ast.NameAtom)
            return ast.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def ability_ref(self, _: None) -> ast.ArchRef:
            """Grammar rule.

            ability_ref: ABILITY_OP (special_ref | name_ref)
            """
            arch_type = self.consume_token(Tok.ABILITY_OP)
            arch_name = self.consume(ast.NameAtom)
            return ast.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def arch_or_ability_chain(self, kid: list[ast.AstNode]) -> ast.ArchRefChain:
            """Grammar rule.

            arch_or_ability_chain: arch_or_ability_chain? (ability_ref | arch_ref)
            """
            consume = self.match(ast.ArchRefChain)
            name = self.consume(ast.ArchRef)
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
            return self.consume(ast.EdgeOpRef)

        def edge_to(self, _: None) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_to: ARROW_R_P1 typed_filter_compare_list ARROW_R_P2
                   | ARROW_R
            """
            if self.match_token(Tok.ARROW_R):
                fcond = None
            else:
                self.consume_token(Tok.ARROW_R_P1)
                fcond = self.consume(ast.FilterCompr)
                self.consume_token(Tok.ARROW_R_P2)
            return ast.EdgeOpRef(
                filter_cond=fcond, edge_dir=EdgeDir.OUT, kid=self.cur_nodes
            )

        def edge_from(self, _: None) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_from: ARROW_L_P1 typed_filter_compare_list ARROW_L_P2
                     | ARROW_L
            """
            if self.match_token(Tok.ARROW_L):
                fcond = None
            else:
                self.consume_token(Tok.ARROW_L_P1)
                fcond = self.consume(ast.FilterCompr)
                self.consume_token(Tok.ARROW_L_P2)
            return ast.EdgeOpRef(
                filter_cond=fcond, edge_dir=EdgeDir.IN, kid=self.cur_nodes
            )

        def edge_any(self, _: None) -> ast.EdgeOpRef:
            """Grammar rule.

            edge_any: ARROW_L_P1 typed_filter_compare_list ARROW_R_P2
                    | ARROW_BI
            """
            if self.match_token(Tok.ARROW_BI):
                fcond = None
            else:
                self.consume_token(Tok.ARROW_L_P1)
                fcond = self.consume(ast.FilterCompr)
                self.consume_token(Tok.ARROW_R_P2)
            return ast.EdgeOpRef(
                filter_cond=fcond, edge_dir=EdgeDir.ANY, kid=self.cur_nodes
            )

        def connect_op(self, _: None) -> ast.ConnectOp:
            """Grammar rule.

            connect_op: connect_from | connect_to | connect_any
            """
            return self.consume(ast.ConnectOp)

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

        def connect_to(self, _: None) -> ast.ConnectOp:
            """Grammar rule.

            connect_to: CARROW_R_P1 expression (COLON kw_expr_list)? CARROW_R_P2
                      | CARROW_R
            """
            conn_type: ast.Expr | None = None
            conn_assign_sub: ast.SubNodeList | None = None
            if self.match_token(Tok.CARROW_R_P1):
                conn_type = self.consume(ast.Expr)
                conn_assign_sub = (
                    self.consume(ast.SubNodeList)
                    if self.match_token(Tok.COLON)
                    else None
                )
                self.consume_token(Tok.CARROW_R_P2)
            else:
                self.consume_token(Tok.CARROW_R)
            conn_assign = (
                ast.AssignCompr(assigns=conn_assign_sub, kid=[conn_assign_sub])
                if conn_assign_sub
                else None
            )
            if conn_assign:
                self.cur_nodes[3] = conn_assign
            return ast.ConnectOp(
                conn_type=conn_type,
                conn_assign=conn_assign,
                edge_dir=EdgeDir.OUT,
                kid=self.cur_nodes,
            )

        def connect_from(self, _: None) -> ast.ConnectOp:
            """Grammar rule.

            connect_from: CARROW_L_P1 expression (COLON kw_expr_list)? CARROW_L_P2
                        | CARROW_L
            """
            conn_type: ast.Expr | None = None
            conn_assign_sub: ast.SubNodeList | None = None
            if self.match_token(Tok.CARROW_L_P1):
                conn_type = self.consume(ast.Expr)
                conn_assign_sub = (
                    self.consume(ast.SubNodeList)
                    if self.match_token(Tok.COLON)
                    else None
                )
                self.consume_token(Tok.CARROW_L_P2)
            else:
                self.consume_token(Tok.CARROW_L)
            conn_assign = (
                ast.AssignCompr(assigns=conn_assign_sub, kid=[conn_assign_sub])
                if conn_assign_sub
                else None
            )
            if conn_assign:
                self.cur_nodes[3] = conn_assign
            return ast.ConnectOp(
                conn_type=conn_type,
                conn_assign=conn_assign,
                edge_dir=EdgeDir.IN,
                kid=self.cur_nodes,
            )

        def connect_any(self, _: None) -> ast.ConnectOp:
            """Grammar rule.

            connect_any: CARROW_BI | CARROW_L_P1 expression (COLON kw_expr_list)? CARROW_R_P2
            """
            conn_type: ast.Expr | None = None
            conn_assign_sub: ast.SubNodeList | None = None
            if self.match_token(Tok.CARROW_L_P1):
                conn_type = self.consume(ast.Expr)
                conn_assign_sub = (
                    self.consume(ast.SubNodeList)
                    if self.match_token(Tok.COLON)
                    else None
                )
                self.consume_token(Tok.CARROW_R_P2)
            else:
                self.consume_token(Tok.CARROW_BI)
            conn_assign = (
                ast.AssignCompr(assigns=conn_assign_sub, kid=[conn_assign_sub])
                if conn_assign_sub
                else None
            )
            if conn_assign:
                self.cur_nodes[3] = conn_assign
            return ast.ConnectOp(
                conn_type=conn_type,
                conn_assign=conn_assign,
                edge_dir=EdgeDir.ANY,
                kid=self.cur_nodes,
            )

        def filter_compr(self, _: None) -> ast.FilterCompr:
            """Grammar rule.

            filter_compr: LPAREN NULL_OK filter_compare_list RPAREN
                        | LPAREN TYPE_OP NULL_OK typed_filter_compare_list RPAREN
            """
            kid = self.cur_nodes
            self.consume_token(Tok.LPAREN)
            if self.match_token(Tok.TYPE_OP):
                self.consume_token(Tok.NULL_OK)
                f_type = self.consume(ast.FilterCompr)
                f_type.add_kids_left(kid[:3])
                f_type.add_kids_right(kid[4:])
                self.consume_token(Tok.RPAREN)
                return f_type
            self.consume_token(Tok.NULL_OK)
            compares = self.consume(ast.SubNodeList)
            self.consume_token(Tok.RPAREN)
            return ast.FilterCompr(
                compares=compares,
                f_type=None,
                kid=self.cur_nodes,
            )

        def filter_compare_list(self, _: None) -> ast.SubNodeList[ast.CompareExpr]:
            """Grammar rule.

            filter_compare_list: (filter_compare_list COMMA)? filter_compare_item
            """
            if consume := self.match(ast.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                expr = self.consume(ast.CompareExpr)
                new_kid = [*consume.kid, comma, expr]
            else:
                expr = self.consume(ast.CompareExpr)
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

        def filter_compare_item(self, _: None) -> ast.CompareExpr:
            """Grammar rule.

            filter_compare_item: name_ref cmp_op expression
            """
            name_ref = self.consume(ast.Name)
            cmp_op = self.consume(ast.Token)
            expr = self.consume(ast.Expr)
            return ast.CompareExpr(
                left=name_ref, ops=[cmp_op], rights=[expr], kid=self.cur_nodes
            )

        def assign_compr(self, _: None) -> ast.AssignCompr:
            """Grammar rule.

            filter_compr: LPAREN EQ kw_expr_list RPAREN
            """
            self.consume_token(Tok.LPAREN)
            self.consume_token(Tok.EQ)
            assigns = self.consume(ast.SubNodeList)
            self.consume_token(Tok.RPAREN)
            return ast.AssignCompr(assigns=assigns, kid=self.cur_nodes)

        def match_stmt(self, _: None) -> ast.MatchStmt:
            """Grammar rule.

            match_stmt: KW_MATCH expr_list LBRACE match_case_block+ RBRACE
            """
            self.consume_token(Tok.KW_MATCH)
            target = self.consume(ast.Expr)
            self.consume_token(Tok.LBRACE)
            cases = [self.consume(ast.MatchCase)]
            while case := self.match(ast.MatchCase):
                cases.append(case)
            self.consume_token(Tok.RBRACE)
            return ast.MatchStmt(
                target=target,
                cases=cases,
                kid=self.cur_nodes,
            )

        def match_case_block(self, _: None) -> ast.MatchCase:
            """Grammar rule.

            match_case_block: KW_CASE pattern_seq (KW_IF expression)? COLON statement_list
            """
            guard: ast.Expr | None = None
            self.consume_token(Tok.KW_CASE)
            pattern = self.consume(ast.MatchPattern)
            if self.match_token(Tok.KW_IF):
                guard = self.consume(ast.Expr)
            self.consume_token(Tok.COLON)
            stmts = [self.consume(ast.CodeBlockStmt)]
            while stmt := self.match(ast.CodeBlockStmt):
                stmts.append(stmt)
            return ast.MatchCase(
                pattern=pattern,
                guard=guard,
                body=stmts,
                kid=self.cur_nodes,
            )

        def pattern_seq(self, _: None) -> ast.MatchPattern:
            """Grammar rule.

            pattern_seq: (or_pattern | as_pattern)
            """
            return self.consume(ast.MatchPattern)

        def or_pattern(self, _: None) -> ast.MatchPattern:
            """Grammar rule.

            or_pattern: (pattern BW_OR)* pattern
            """
            patterns: list = [self.consume(ast.MatchPattern)]
            while self.match_token(Tok.BW_OR):
                patterns.append(self.consume(ast.MatchPattern))
            if len(patterns) == 1:
                return patterns[0]
            return ast.MatchOr(
                patterns=patterns,
                kid=self.cur_nodes,
            )

        def as_pattern(self, _: None) -> ast.MatchPattern:
            """Grammar rule.

            as_pattern: pattern KW_AS NAME
            """
            pattern = self.consume(ast.MatchPattern)
            self.consume_token(Tok.KW_AS)
            name = self.consume(ast.NameAtom)
            return ast.MatchAs(
                pattern=pattern,
                name=name,
                kid=self.cur_nodes,
            )

        def pattern(self, kid: list[ast.AstNode]) -> ast.MatchPattern:
            """Grammar rule.

            pattern: literal_pattern
                | capture_pattern
                | sequence_pattern
                | mapping_pattern
                | class_pattern
            """
            return self.consume(ast.MatchPattern)

        def literal_pattern(self, _: None) -> ast.MatchPattern:
            """Grammar rule.

            literal_pattern: (INT | FLOAT | multistring)
            """
            value = self.consume(ast.Expr)
            return ast.MatchValue(
                value=value,
                kid=self.cur_nodes,
            )

        def singleton_pattern(self, _: None) -> ast.MatchPattern:
            """Grammar rule.

            singleton_pattern: (NULL | BOOL)
            """
            value = self.match(ast.Null) or self.consume(ast.Bool)
            return ast.MatchSingleton(
                value=value,
                kid=self.cur_nodes,
            )

        def capture_pattern(self, _: None) -> ast.MatchPattern:
            """Grammar rule.

            capture_pattern: NAME
            """
            name = self.consume(ast.Name)
            if name.sym_name == "_":
                return ast.MatchWild(
                    kid=self.cur_nodes,
                )
            return ast.MatchAs(
                name=name,
                pattern=None,
                kid=self.cur_nodes,
            )

        def sequence_pattern(self, _: None) -> ast.MatchPattern:
            """Grammar rule.

            sequence_pattern: LSQUARE list_inner_pattern (COMMA list_inner_pattern)* RSQUARE
                            | LPAREN list_inner_pattern (COMMA list_inner_pattern)* RPAREN
            """
            self.consume_token(Tok.LSQUARE) or self.consume_token(Tok.LPAREN)
            patterns = [self.consume(ast.MatchPattern)]
            while self.match_token(Tok.COMMA):
                patterns.append(self.consume(ast.MatchPattern))
            self.consume_token(Tok.RSQUARE) or self.consume_token(Tok.RPAREN)
            return ast.MatchSequence(
                values=patterns,
                kid=self.cur_nodes,
            )

        def mapping_pattern(self, _: None) -> ast.MatchMapping:
            """Grammar rule.

            mapping_pattern: LBRACE (dict_inner_pattern (COMMA dict_inner_pattern)*)? RBRACE
            """
            self.consume_token(Tok.LBRACE)
            patterns = [self.match(ast.MatchKVPair) or self.consume(ast.MatchStar)]
            while self.match_token(Tok.COMMA):
                patterns.append(
                    self.match(ast.MatchKVPair) or self.consume(ast.MatchStar)
                )
            self.consume_token(Tok.RBRACE)
            return ast.MatchMapping(
                values=patterns,
                kid=self.cur_nodes,
            )

        def list_inner_pattern(self, _: None) -> ast.MatchPattern:
            """Grammar rule.

            list_inner_pattern: (pattern_seq | STAR_MUL NAME)
            """
            if self.match_token(Tok.STAR_MUL):
                name = self.consume(ast.Name)
                return ast.MatchStar(
                    is_list=True,
                    name=name,
                    kid=self.cur_nodes,
                )
            return self.consume(ast.MatchPattern)

        def dict_inner_pattern(self, _: None) -> ast.MatchKVPair | ast.MatchStar:
            """Grammar rule.

            dict_inner_pattern: (pattern_seq COLON pattern_seq | STAR_POW NAME)
            """
            if self.match_token(Tok.STAR_POW):
                name = self.consume(ast.Name)
                return ast.MatchStar(
                    is_list=False,
                    name=name,
                    kid=self.cur_nodes,
                )
            pattern = self.consume(ast.MatchPattern)
            self.consume_token(Tok.COLON)
            value = self.consume(ast.MatchPattern)
            return ast.MatchKVPair(key=pattern, value=value, kid=self.cur_nodes)

        def class_pattern(self, _: None) -> ast.MatchArch:
            """Grammar rule.

            class_pattern: NAME (DOT NAME)* LPAREN kw_pattern_list? RPAREN
                        | NAME (DOT NAME)* LPAREN pattern_list (COMMA kw_pattern_list)? RPAREN
            """
            cur_element = self.consume(ast.NameAtom)
            trailer: ast.AtomTrailer | None = None
            while dot := self.match_token(Tok.DOT):
                target = trailer if trailer else cur_element
                right = self.consume(ast.Expr)
                trailer = ast.AtomTrailer(
                    target=target,
                    right=right,
                    is_attr=True,
                    is_null_ok=False,
                    kid=[target, dot, right],
                )
            name = trailer if trailer else cur_element
            if not isinstance(name, (ast.NameAtom, ast.AtomTrailer)):
                raise TypeError(
                    f"Expected name to be either NameAtom or AtomTrailer, got {type(name)}"
                )
            lparen = self.consume_token(Tok.LPAREN)
            first = self.match(ast.SubNodeList)
            second = (
                self.consume(ast.SubNodeList)
                if (comma := self.match_token(Tok.COMMA))
                else None
            )
            rparen = self.consume_token(Tok.RPAREN)
            arg = (
                first
                if (first and isinstance(first.items[0], ast.MatchPattern))
                else None
            )
            kw = (
                second
                if (second and isinstance(second.items[0], ast.MatchKVPair))
                else (
                    first
                    if (first and isinstance(first.items[0], ast.MatchKVPair))
                    else None
                )
            )
            kid_nodes: list = [name, lparen]
            if arg:
                kid_nodes.append(arg)
                if kw:
                    kid_nodes.extend([comma, kw]) if comma else kid_nodes.append(kw)
            elif kw:
                kid_nodes.append(kw)
            kid_nodes.append(rparen)
            return ast.MatchArch(
                name=name,
                arg_patterns=arg,
                kw_patterns=kw,
                kid=kid_nodes,
            )

        def pattern_list(self, _: None) -> ast.SubNodeList[ast.MatchPattern]:
            """Grammar rule.

            pattern_list: (pattern_list COMMA)? pattern_seq
            """
            if consume := self.match(ast.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                pattern = self.consume(ast.MatchPattern)
            else:
                pattern = self.consume(ast.MatchPattern)
            new_kid = [*consume.kid, comma, pattern] if consume else [pattern]
            valid_kid = [i for i in new_kid if isinstance(i, ast.MatchPattern)]
            return ast.SubNodeList[ast.MatchPattern](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def kw_pattern_list(self, _: None) -> ast.SubNodeList[ast.MatchKVPair]:
            """Grammar rule.

            kw_pattern_list: (kw_pattern_list COMMA)? named_ref EQ pattern_seq
            """
            new_kid: list = []
            if consume := self.match(ast.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                new_kid.extend([*consume.kid, comma])
            name = self.consume(ast.NameAtom)
            eq = self.consume_token(Tok.EQ)
            value = self.consume(ast.MatchPattern)
            new_kid.extend(
                [ast.MatchKVPair(key=name, value=value, kid=[name, eq, value])]
            )
            valid_kid = [i for i in new_kid if isinstance(i, ast.MatchKVPair)]
            return ast.SubNodeList[ast.MatchKVPair](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

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

"""Lark parser for Jac Lang."""

from __future__ import annotations

import keyword
import logging
import os
from typing import Callable, TYPE_CHECKING, TypeAlias, TypeVar

import jaclang.compiler.unitree as uni
from jaclang.compiler import jac_lark as jl  # type: ignore
from jaclang.compiler.constant import EdgeDir, Tokens as Tok
from jaclang.compiler.passes.ast_pass import Transform
from jaclang.vendor.lark import Lark, Transformer, Tree, logger

if TYPE_CHECKING:
    from jaclang.compiler.program import JacProgram

T = TypeVar("T", bound=uni.UniNode)


class JacParser(Transform[uni.Source, uni.Module]):
    """Jac Parser."""

    dev_mode = False

    def __init__(self, root_ir: uni.Source, prog: JacProgram) -> None:
        """Initialize parser."""
        self.mod_path = root_ir.loc.mod_path
        self.node_list: list[uni.UniNode] = []
        if JacParser.dev_mode:
            JacParser.make_dev()
        Transform.__init__(self, ir_in=root_ir, prog=prog)

    def transform(self, ir_in: uni.Source) -> uni.Module:
        """Transform input IR."""
        try:
            tree, comments = JacParser.parse(ir_in.value, on_error=self.error_callback)
            mod = JacParser.TreeToAST(parser=self).transform(tree)
            ir_in.comments = [self.proc_comment(i, mod) for i in comments]
            if isinstance(mod, uni.Module):
                self.ir_out = mod
                return mod
            else:
                raise self.ice()
        except jl.UnexpectedInput as e:
            catch_error = uni.EmptyToken()
            catch_error.orig_src = ir_in
            catch_error.line_no = e.line
            catch_error.end_line = e.line
            catch_error.c_start = e.column
            catch_error.c_end = e.column + 1
            catch_error.pos_start = e.pos_in_stream or 0
            catch_error.pos_end = catch_error.pos_start + 1

            error_msg = "Syntax Error"
            if len(e.args) >= 1 and isinstance(e.args[0], str):
                error_msg += e.args[0]
            self.log_error(error_msg, node_override=catch_error)

        except Exception as e:
            self.log_error(f"Internal Error: {e}")

        return uni.Module.make_stub(inject_src=ir_in)

    @staticmethod
    def proc_comment(token: jl.Token, mod: uni.UniNode) -> uni.CommentToken:
        """Process comment."""
        return uni.CommentToken(
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
        JacParser.JacTransformer = Transformer[Tree[str], uni.UniNode]  # type: ignore
        logger.setLevel(logging.DEBUG)

    comment_cache: list[jl.Token] = []

    parser = jl.Lark_StandAlone(lexer_callbacks={"COMMENT": _comment_callback})  # type: ignore
    JacTransformer: TypeAlias = jl.Transformer[jl.Tree[str], uni.UniNode]

    class TreeToAST(JacTransformer):
        """Transform parse tree to AST."""

        def __init__(self, parser: JacParser, *args: bool, **kwargs: bool) -> None:
            """Initialize transformer."""
            super().__init__(*args, **kwargs)
            self.parse_ref = parser
            self.terminals: list[uni.Token] = []
            # TODO: Once the kid is removed from the ast, we can get rid of this
            # node_idx and directly pop(0) kid as we process the nodes.
            self.node_idx = 0
            self.cur_nodes: list[uni.UniNode] = []

        def ice(self) -> Exception:
            """Raise internal compiler error."""
            self.parse_ref.log_error("Internal Compiler Error, Invalid Parse Tree!")
            return RuntimeError(
                f"{self.parse_ref.__class__.__name__} - Internal Compiler Error, Invalid Parse Tree!"
            )

        def _node_update(self, node: T) -> T:
            self.parse_ref.cur_node = node
            if node not in self.parse_ref.node_list:
                self.parse_ref.node_list.append(node)
            return node

        def _call_userfunc(
            self, tree: jl.Tree, new_children: None | list[uni.UniNode] = None
        ) -> uni.UniNode:
            self.cur_nodes = new_children or tree.children  # type: ignore[assignment]
            try:
                return self._node_update(super()._call_userfunc(tree, new_children))
            finally:
                self.cur_nodes = []
                self.node_idx = 0

        def _call_userfunc_token(self, token: jl.Token) -> uni.UniNode:
            return self._node_update(super()._call_userfunc_token(token))

        def _binary_expr_unwind(self, kid: list[uni.UniNode]) -> uni.Expr:
            """Binary expression helper."""
            if len(kid) > 1:
                if (
                    isinstance(kid[0], uni.Expr)
                    and (isinstance(kid[1], uni.Token) and kid[1].name == Tok.KW_JACGO)
                    and (isinstance(kid[2], uni.Token) and kid[2].name == Tok.KW_SPAWN)
                    and isinstance(kid[3], uni.Expr)
                ):
                    return uni.SpawnExpr(
                        left=kid[0],
                        is_jacgo=True,
                        op=kid[2],
                        right=kid[3],
                        kid=kid,
                    )
                elif (
                    isinstance(kid[0], uni.Expr)
                    and (isinstance(kid[1], uni.Token) and kid[1].name == Tok.KW_SPAWN)
                    and isinstance(kid[2], uni.Expr)
                ):
                    return uni.SpawnExpr(
                        left=kid[0],
                        is_jacgo=False,
                        op=kid[1],
                        right=kid[2],
                        kid=kid,
                    )
                elif (
                    isinstance(kid[0], uni.Expr)
                    and isinstance(
                        kid[1],
                        (uni.Token, uni.DisconnectOp, uni.ConnectOp),
                    )
                    and isinstance(kid[2], uni.Expr)
                ):
                    return uni.BinaryExpr(
                        left=kid[0],
                        op=kid[1],
                        right=kid[2],
                        kid=kid,
                    )
                else:
                    raise self.ice()
            elif isinstance(kid[0], uni.Expr):
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

        def match_token(self, tok: Tok) -> uni.Token | None:
            """Match a token with the given type and return it."""
            if token := self.match(uni.Token):
                if token.name == tok.name:
                    return token
                self.node_idx -= (
                    1  # We're already matched but wrong token so undo matching it.
                )
            return None

        def consume_token(self, tok: Tok) -> uni.Token:
            """Consume a token with the given type and return it."""
            if token := self.match_token(tok):
                return token
            raise self.ice()

        def match_many(self, ty: type[T]) -> list[T]:
            """Match 0 or more of the given type and return the list."""
            nodes: list[uni.UniNode] = []
            while node := self.match(ty):
                nodes.append(node)
            return nodes  # type: ignore[return-value]

        def consume_many(self, ty: type[T]) -> list[T]:
            """Match 1 or more of the given type and return the list."""
            nodes: list[uni.UniNode] = [self.consume(ty)]
            while node := self.match(ty):
                nodes.append(node)
            return nodes  # type: ignore[return-value]

        # ******************************************************************* #
        # Parsing Rules                                                       #
        # ******************************************************************* #

        def start(self, _: None) -> uni.Module:
            """Grammar rule.

            start: module
            """
            module = self.consume(uni.Module)
            module._in_mod_nodes = self.parse_ref.node_list
            return module

        def module(self, _: None) -> uni.Module:
            """Grammar rule.

            module: (toplevel_stmt (tl_stmt_with_doc | toplevel_stmt)*)?
                | STRING (tl_stmt_with_doc | toplevel_stmt)*
            """
            doc = self.match(uni.String)
            body = self.match_many(uni.ElementStmt)
            mod = uni.Module(
                name=self.parse_ref.mod_path.split(os.path.sep)[-1].rstrip(".jac"),
                source=self.parse_ref.ir_in,
                doc=doc,
                body=body,
                terminals=self.terminals,
                kid=(
                    self.cur_nodes
                    or [uni.EmptyToken(uni.Source("", self.parse_ref.mod_path))]
                ),
            )
            return mod

        def tl_stmt_with_doc(self, _: None) -> uni.ElementStmt:
            """Grammar rule.

            tl_stmt_with_doc: doc_tag toplevel_stmt
            """
            doc = self.consume(uni.String)
            element = self.consume(uni.ElementStmt)
            element.doc = doc
            element.add_kids_left([doc])
            return element

        def toplevel_stmt(self, _: None) -> uni.ElementStmt:
            """Grammar rule.

            element: py_code_block
                | import_stmt
                | ability
                | architype
                | free_code
                | test
                | global_var
            """
            return self.consume(uni.ElementStmt)

        def global_var(self, _: None) -> uni.GlobalVars:
            """Grammar rule.

            global_var: (KW_LET | KW_GLOBAL) access_tag? assignment_list SEMI
            """
            is_frozen = self.consume(uni.Token).name == Tok.KW_LET
            access_tag = self.match(uni.SubTag)
            assignments = self.consume(uni.SubNodeList)
            return uni.GlobalVars(
                access=access_tag,
                assignments=assignments,
                is_frozen=is_frozen,
                kid=self.cur_nodes,
            )

        def access_tag(self, _: None) -> uni.SubTag[uni.Token]:
            """Grammar rule.

            access_tag: COLON ( KW_PROT | KW_PUB | KW_PRIV )
            """
            self.consume_token(Tok.COLON)
            access = self.consume(uni.Token)
            return uni.SubTag[uni.Token](tag=access, kid=self.cur_nodes)

        def test(self, _: None) -> uni.Test:
            """Grammar rule.

            test: KW_TEST NAME? code_block
            """
            # Q(thakee): Why the name should be KW_TEST if no name present?
            test_tok = self.consume_token(Tok.KW_TEST)
            name = self.match(uni.Name) or test_tok
            codeblock = self.consume(uni.SubNodeList)
            return uni.Test(
                name=name,
                body=codeblock,
                kid=self.cur_nodes,
            )

        def free_code(self, _: None) -> uni.ModuleCode:
            """Grammar rule.

            free_code: KW_WITH KW_ENTRY sub_name? code_block
            """
            self.consume_token(Tok.KW_WITH)
            self.consume_token(Tok.KW_ENTRY)
            name = self.match(uni.SubTag)
            codeblock = self.consume(uni.SubNodeList)
            return uni.ModuleCode(
                name=name,
                body=codeblock,
                kid=self.cur_nodes,
            )

        def py_code_block(self, _: None) -> uni.PyInlineCode:
            """Grammar rule.

            py_code_block: PYNLINE
            """
            pyinline = self.consume_token(Tok.PYNLINE)
            return uni.PyInlineCode(
                code=pyinline,
                kid=self.cur_nodes,
            )

        def import_stmt(self, _: None) -> uni.Import:
            """Grammar rule.

            import_stmt: KW_IMPORT sub_name? KW_FROM from_path LBRACE import_items RBRACE
                       | KW_IMPORT sub_name? KW_FROM from_path COMMA import_items SEMI  //Deprecated
                       | KW_IMPORT sub_name? import_path (COMMA import_path)* SEMI
                       | include_stmt
            """
            if import_stmt := self.match(uni.Import):  # Include Statement.
                return import_stmt

            # TODO: kid will be removed so let's keep as it is for now.
            kid = self.cur_nodes

            from_path: uni.ModulePath | None = None
            self.consume_token(Tok.KW_IMPORT)
            lang = self.match(uni.SubTag)

            if self.match_token(Tok.KW_FROM):
                from_path = self.consume(uni.ModulePath)
                self.consume(uni.Token)  # LBRACE or COMMA
                items = self.consume(uni.SubNodeList)
                if self.consume(uni.Token).name == Tok.SEMI:  # RBRACE or SEMI
                    self.parse_ref.log_warning(
                        "Deprecated syntax, use braces for multiple imports (e.g, import from mymod {a, b, c})",
                    )
            else:
                paths = [self.consume(uni.ModulePath)]
                while self.match_token(Tok.COMMA):
                    paths.append(self.consume(uni.ModulePath))
                self.consume_token(Tok.SEMI)
                items = uni.SubNodeList[uni.ModulePath](
                    items=paths,
                    delim=Tok.COMMA,
                    # TODO: kid will be removed so let's keep as it is for now.
                    kid=self.cur_nodes[2 if lang else 1 : -1],
                )
                kid = (kid[:2] if lang else kid[:1]) + [items] + kid[-1:]

            is_absorb = False
            return uni.Import(
                hint=lang,
                from_loc=from_path,
                items=items,
                is_absorb=is_absorb,
                kid=kid,
            )

        def from_path(self, _: None) -> uni.ModulePath:
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
            if import_path := self.match(uni.ModulePath):
                kids = [i for i in self.cur_nodes if isinstance(i, uni.Token)]
                import_path.level = level
                import_path.add_kids_left(kids)
                return import_path

            return uni.ModulePath(
                path=None,
                level=level,
                alias=None,
                kid=self.cur_nodes,
            )

        def include_stmt(self, _: None) -> uni.Import:
            """Grammar rule.

            include_stmt: KW_INCLUDE sub_name? import_path SEMI
            """
            kid = self.cur_nodes  # TODO: Will be removed.
            self.consume_token(Tok.KW_INCLUDE)
            lang = self.match(uni.SubTag)
            from_path = self.consume(uni.ModulePath)
            items = uni.SubNodeList[uni.ModulePath](
                items=[from_path], delim=Tok.COMMA, kid=[from_path]
            )
            kid = (
                (kid[:2] if lang else kid[:1]) + [items] + kid[-1:]
            )  # TODO: Will be removed.
            is_absorb = True
            return uni.Import(
                hint=lang,
                from_loc=None,
                items=items,
                is_absorb=is_absorb,
                kid=kid,
            )

        def import_path(self, _: None) -> uni.ModulePath:
            """Grammar rule.

            import_path: named_ref (DOT named_ref)* (KW_AS NAME)?
            """
            valid_path = [self.consume(uni.Name)]
            while self.match_token(Tok.DOT):
                valid_path.append(self.consume(uni.Name))
            alias = self.consume(uni.Name) if self.match_token(Tok.KW_AS) else None
            return uni.ModulePath(
                path=valid_path,
                level=0,
                alias=alias,
                kid=self.cur_nodes,
            )

        def import_items(self, _: None) -> uni.SubNodeList[uni.ModuleItem]:
            """Grammar rule.

            import_items: (import_item COMMA)* import_item COMMA?
            """
            items = [self.consume(uni.ModuleItem)]
            while self.match_token(Tok.COMMA):
                if module_item := self.match(uni.ModuleItem):
                    items.append(module_item)
            ret = uni.SubNodeList[uni.ModuleItem](
                items=items,
                delim=Tok.COMMA,
                kid=self.cur_nodes,
            )
            return ret

        def import_item(self, _: None) -> uni.ModuleItem:
            """Grammar rule.

            import_item: named_ref (KW_AS NAME)?
            """
            name = self.consume(uni.Name)
            alias = self.consume(uni.Name) if self.match_token(Tok.KW_AS) else None
            return uni.ModuleItem(
                name=name,
                alias=alias,
                kid=self.cur_nodes,
            )

        def architype(
            self, _: None
        ) -> uni.ArchSpec | uni.ArchDef | uni.Enum | uni.EnumDef:
            """Grammar rule.

            architype: decorators? architype_decl
                    | architype_def
                    | enum
            """
            archspec: uni.ArchSpec | uni.ArchDef | uni.Enum | uni.EnumDef | None = None

            decorators = self.match(uni.SubNodeList)
            if decorators is not None:
                archspec = self.consume(uni.ArchSpec)
                archspec.decorators = decorators
                archspec.add_kids_left([decorators])
            else:
                archspec = (
                    self.match(uni.ArchSpec)
                    or self.match(uni.ArchDef)
                    or self.match(uni.Enum)
                    or self.consume(uni.EnumDef)
                )
            return archspec

        def architype_decl(self, _: None) -> uni.ArchSpec:
            """Grammar rule.

            architype_decl: arch_type access_tag? STRING? NAME inherited_archs? (member_block | SEMI)
            """
            arch_type = self.consume(uni.Token)
            access = self.match(uni.SubTag)
            semstr = self.match(uni.String)
            name = self.consume(uni.Name)
            sub_list1 = self.match(uni.SubNodeList)
            sub_list2 = self.match(uni.SubNodeList)
            if self.match_token(Tok.SEMI):
                inh, body = sub_list1, None
            else:
                body = (
                    sub_list2 or sub_list1
                )  # if sub_list2 is None then body is sub_list1
                inh = sub_list2 and sub_list1  # if sub_list2 is None then inh is None.
            return uni.Architype(
                arch_type=arch_type,
                name=name,
                semstr=semstr,
                access=access,
                base_classes=inh,
                body=body,
                kid=self.cur_nodes,
            )

        def architype_def(self, _: None) -> uni.ArchDef:
            """Grammar rule.

            architype_def: abil_to_arch_chain member_block
            """
            archref = self.consume(uni.ArchRefChain)
            subnodelist = self.consume(uni.SubNodeList)
            return uni.ArchDef(
                target=archref,
                body=subnodelist,
                kid=self.cur_nodes,
            )

        def arch_type(self, _: None) -> uni.Token:
            """Grammar rule.

            arch_type: KW_WALKER
                    | KW_OBJECT
                    | KW_EDGE
                    | KW_NODE
            """
            return self.consume(uni.Token)

        def decorators(self, _: None) -> uni.SubNodeList[uni.Expr]:
            """Grammar rule.

            decorators: (DECOR_OP atomic_chain)+
            """
            self.consume_token(Tok.DECOR_OP)
            return uni.SubNodeList[uni.Expr](
                items=self.consume_many(uni.Expr),
                delim=Tok.DECOR_OP,
                kid=self.cur_nodes,
            )

        def inherited_archs(self, kid: list[uni.UniNode]) -> uni.SubNodeList[uni.Expr]:
            """Grammar rule.

            inherited_archs: LT (atomic_chain COMMA)* atomic_chain GT
                           | COLON (atomic_chain COMMA)* atomic_chain COLON
            """
            self.match_token(Tok.LT) or self.consume_token(Tok.COLON)
            items: list = []
            while inherited_arch := self.match(uni.Expr):
                items.append(inherited_arch)
                self.match_token(Tok.COMMA)
            self.match_token(Tok.LT) or self.consume_token(Tok.COLON)
            return uni.SubNodeList[uni.Expr](items=items, delim=Tok.COMMA, kid=kid)

        def sub_name(self, _: None) -> uni.SubTag[uni.Name]:
            """Grammar rule.

            sub_name: COLON NAME
            """
            self.consume_token(Tok.COLON)
            target = self.consume(uni.Name)
            return uni.SubTag(
                tag=target,
                kid=self.cur_nodes,
            )

        def named_ref(self, _: None) -> uni.NameAtom:
            """Grammar rule.

            named_ref: special_ref
                    | KWESC_NAME
                    | NAME
            """
            return self.consume(uni.NameAtom)

        def special_ref(self, _: None) -> uni.SpecialVarRef:
            """Grammar rule.

            special_ref: KW_INIT
                        | KW_POST_INIT
                        | KW_ROOT
                        | KW_SUPER
                        | KW_SELF
                        | KW_HERE
            """
            return uni.SpecialVarRef(var=self.consume(uni.Name))

        def enum(self, _: None) -> uni.Enum | uni.EnumDef:
            """Grammar rule.

            enum: decorators? enum_decl
                | enum_def
            """
            if decorator := self.match(uni.SubNodeList):
                enum_decl = self.consume(uni.Enum)
                enum_decl.decorators = decorator
                enum_decl.add_kids_left([decorator])
                return enum_decl
            return self.match(uni.Enum) or self.consume(uni.EnumDef)

        def enum_decl(self, _: None) -> uni.Enum:
            """Grammar rule.

            enum_decl: KW_ENUM access_tag? STRING? NAME inherited_archs? (enum_block | SEMI)
            """
            self.consume_token(Tok.KW_ENUM)
            access = self.match(uni.SubTag)
            semstr = self.match(uni.String)
            name = self.consume(uni.Name)
            sub_list1 = self.match(uni.SubNodeList)
            sub_list2 = self.match(uni.SubNodeList)
            if self.match_token(Tok.SEMI):
                inh, body = sub_list1, None
            else:
                body = sub_list2 or sub_list1
                inh = sub_list2 and sub_list1
            return uni.Enum(
                semstr=semstr,
                name=name,
                access=access,
                base_classes=inh,
                body=body,
                kid=self.cur_nodes,
            )

        def enum_def(self, _: None) -> uni.EnumDef:
            """Grammar rule.

            enum_def: arch_to_enum_chain enum_block
            """
            enum_def = self.consume(uni.ArchRefChain)
            enum_block = self.consume(uni.SubNodeList)
            return uni.EnumDef(
                target=enum_def,
                body=enum_block,
                kid=self.cur_nodes,
            )

        def enum_block(self, _: None) -> uni.SubNodeList[uni.EnumBlockStmt]:
            """Grammar rule.

            enum_block: LBRACE ((enum_stmt COMMA)* enum_stmt COMMA?)? RBRACE
            """
            self.consume_token(Tok.LBRACE)
            enum_statements: list = []
            while enum_stmt := self.match(uni.EnumBlockStmt):
                enum_statements.append(enum_stmt)
                self.match_token(Tok.COMMA)
            self.consume_token(Tok.RBRACE)
            return uni.SubNodeList[uni.EnumBlockStmt](
                items=enum_statements,
                delim=Tok.COMMA,
                kid=self.cur_nodes,
            )

        def enum_stmt(self, _: None) -> uni.EnumBlockStmt:
            """Grammar rule.

            enum_stmt: NAME (COLON STRING)? EQ expression
                    | NAME (COLON STRING)?
                    | py_code_block
                    | free_code
                    | abstract_ability
                    | ability
            """
            if stmt := (
                self.match(uni.PyInlineCode)
                or self.match(uni.ModuleCode)
                or self.match(uni.Ability)
            ):
                return stmt
            name = self.consume(uni.Name)
            semstr = self.consume(uni.String) if self.match_token(Tok.COLON) else None
            expr = self.consume(uni.Expr) if self.match_token(Tok.EQ) else None
            targ = uni.SubNodeList[uni.Expr](items=[name], delim=Tok.COMMA, kid=[name])
            self.cur_nodes[0] = targ
            return uni.Assignment(
                target=targ,
                value=expr,
                type_tag=None,
                kid=self.cur_nodes,
                semstr=semstr,
                is_enum_stmt=True,
            )

        def ability(self, _: None) -> uni.Ability | uni.AbilityDef | uni.FuncCall:
            """Grammer rule.

            ability: decorators? KW_ASYNC? ability_decl
                    | decorators? genai_ability
                    | ability_def
            """
            ability: uni.Ability | uni.AbilityDef | None = None
            decorators = self.match(uni.SubNodeList)
            is_async = self.match_token(Tok.KW_ASYNC)
            ability = self.match(uni.Ability)
            if is_async and ability:
                ability.is_async = True
                ability.add_kids_left([is_async])
            if ability is None:
                ability = self.consume(uni.AbilityDef)
            if decorators:
                for dec in decorators.items:
                    if (
                        isinstance(dec, uni.NameAtom)
                        and dec.sym_name == "staticmethod"
                        and isinstance(ability, (uni.Ability))
                    ):
                        ability.is_static = True
                        decorators.items.remove(dec)  # noqa: B038
                        break
                if decorators.items:
                    ability.decorators = decorators
                    ability.add_kids_left([decorators])
                return ability
            return ability

        def ability_decl(self, _: None) -> uni.Ability:
            """Grammar rule.

            ability_decl: KW_OVERRIDE? KW_STATIC? KW_CAN access_tag? STRING?
                named_ref (func_decl | event_clause) (code_block | SEMI)
            """
            signature: uni.FuncSignature | uni.EventSignature | None = None
            body: uni.SubNodeList | None = None
            is_override = self.match_token(Tok.KW_OVERRIDE) is not None
            is_static = self.match_token(Tok.KW_STATIC) is not None
            self.consume_token(Tok.KW_CAN)
            access = self.match(uni.SubTag)
            semstr = self.match(uni.String)
            name = self.consume(uni.NameAtom)
            signature = self.match(uni.FuncSignature) or self.consume(
                uni.EventSignature
            )
            if (body := self.match(uni.SubNodeList)) is None:
                self.consume_token(Tok.SEMI)
            return uni.Ability(
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

        def ability_def(self, kid: list[uni.UniNode]) -> uni.AbilityDef:
            """Grammar rule.

            ability_def: arch_to_abil_chain (func_decl | event_clause) code_block
            """
            target = self.consume(uni.ArchRefChain)
            signature = self.match(uni.FuncSignature) or self.consume(
                uni.EventSignature
            )
            body = self.consume(uni.SubNodeList)

            return uni.AbilityDef(
                target=target,
                signature=signature,
                body=body,
                kid=self.cur_nodes,
            )

        # We need separate production rule for abstract_ability because we don't
        # want to allow regular abilities outside of classed to be abstract.
        def abstract_ability(self, _: None) -> uni.Ability:
            """Grammar rule.

            abstract_ability: KW_OVERRIDE? KW_STATIC? KW_CAN access_tag? STRING?
                named_ref (func_decl | event_clause) KW_ABSTRACT SEMI
            """
            signature: uni.FuncSignature | uni.EventSignature | None = None
            is_override = self.match_token(Tok.KW_OVERRIDE) is not None
            is_static = self.match_token(Tok.KW_STATIC) is not None
            self.consume_token(Tok.KW_CAN)
            access = self.match(uni.SubTag)
            semstr = self.match(uni.String)
            name = self.consume(uni.NameAtom)
            signature = self.match(uni.FuncSignature) or self.consume(
                uni.EventSignature
            )
            self.consume_token(Tok.KW_ABSTRACT)
            self.consume_token(Tok.SEMI)
            return uni.Ability(
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

        def genai_ability(self, _: None) -> uni.Ability:
            """Grammar rule.

            genai_ability: KW_OVERRIDE? KW_STATIC? KW_CAN access_tag? STRING?
            named_ref (func_decl) KW_BY atomic_call SEMI
            """
            is_override = self.match_token(Tok.KW_OVERRIDE) is not None
            is_static = self.match_token(Tok.KW_STATIC) is not None
            self.consume_token(Tok.KW_CAN)
            access = self.match(uni.SubTag)
            semstr = self.match(uni.String)
            name = self.consume(uni.NameAtom)
            signature = self.match(uni.FuncSignature) or self.consume(
                uni.EventSignature
            )
            self.consume_token(Tok.KW_BY)
            body = self.consume(uni.FuncCall)
            self.consume_token(Tok.SEMI)
            return uni.Ability(
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

        def event_clause(self, _: None) -> uni.EventSignature:
            """Grammar rule.

            event_clause: KW_WITH expression? (KW_EXIT | KW_ENTRY) (STRING? RETURN_HINT expression)?
            """
            return_spec: uni.Expr | None = None
            semstr: uni.String | None = None
            self.consume_token(Tok.KW_WITH)
            type_specs = self.match(uni.Expr)
            event = self.match_token(Tok.KW_EXIT) or self.consume_token(Tok.KW_ENTRY)
            if semstr := self.match(uni.String):
                self.consume_token(Tok.RETURN_HINT)
                return_spec = self.consume(uni.Expr)
            return uni.EventSignature(
                semstr=semstr,
                event=event,
                arch_tag_info=type_specs,
                return_type=return_spec,
                kid=self.cur_nodes,
            )

        def func_decl(self, _: None) -> uni.FuncSignature:
            """Grammar rule.

            func_decl: (LPAREN func_decl_params? RPAREN)? (RETURN_HINT (STRING COLON)? expression)?
            """
            params: uni.SubNodeList | None = None
            return_spec: uni.Expr | None = None
            semstr: uni.String | None = None
            if self.match_token(Tok.LPAREN):
                params = self.match(uni.SubNodeList)
                self.consume_token(Tok.RPAREN)
            if self.match_token(Tok.RETURN_HINT):
                if semstr := self.match(uni.String):
                    self.consume_token(Tok.COLON)
                return_spec = self.match(uni.Expr)
            return uni.FuncSignature(
                semstr=semstr,
                params=params,
                return_type=return_spec,
                kid=(
                    self.cur_nodes
                    if len(self.cur_nodes)
                    else [uni.EmptyToken(uni.Source("", self.parse_ref.mod_path))]
                ),
            )

        def func_decl_params(self, _: None) -> uni.SubNodeList[uni.ParamVar]:
            """Grammar rule.

            func_decl_params: (param_var COMMA)* param_var COMMA?
            """
            paramvar: list = []
            while param_stmt := self.match(uni.ParamVar):
                paramvar.append(param_stmt)
                self.match_token(Tok.COMMA)
            return uni.SubNodeList[uni.ParamVar](
                items=paramvar,
                delim=Tok.COMMA,
                kid=self.cur_nodes,
            )

        def param_var(self, _: None) -> uni.ParamVar:
            """Grammar rule.

            param_var: (STAR_POW | STAR_MUL)? NAME (COLON STRING)? type_tag (EQ expression)?
            """
            star = self.match_token(Tok.STAR_POW) or self.match_token(Tok.STAR_MUL)
            name = self.consume(uni.Name)
            semstr = self.match(uni.String) if self.match_token(Tok.COLON) else None
            type_tag = self.consume(uni.SubTag)
            value = self.consume(uni.Expr) if self.match_token(Tok.EQ) else None
            return uni.ParamVar(
                semstr=semstr,
                name=name,
                type_tag=type_tag,
                value=value,
                unpack=star,
                kid=self.cur_nodes,
            )

        def member_block(self, _: None) -> uni.SubNodeList[uni.ArchBlockStmt]:
            """Grammar rule.

            member_block: LBRACE member_stmt* RBRACE
            """
            left_enc = self.consume_token(Tok.LBRACE)
            items = self.match_many(uni.ArchBlockStmt)
            right_enc = self.consume_token(Tok.RBRACE)
            ret = uni.SubNodeList[uni.ArchBlockStmt](
                items=items,
                delim=Tok.WS,
                kid=self.cur_nodes,
            )
            ret.left_enc = left_enc
            ret.right_enc = right_enc
            return ret

        def member_stmt(self, _: None) -> uni.ArchBlockStmt:
            """Grammar rule.

            member_stmt: doc_tag? py_code_block
                        | doc_tag? abstract_ability
                        | doc_tag? ability
                        | doc_tag? architype
                        | doc_tag? has_stmt
            """
            doc = self.match(uni.String)
            ret = self.consume(uni.ArchBlockStmt)
            if doc and isinstance(ret, uni.AstDocNode):
                ret.doc = doc
                ret.add_kids_left([doc])
            if isinstance(ret, uni.Ability):
                ret.signature.is_method = True
            return ret

        def has_stmt(self, kid: list[uni.UniNode]) -> uni.ArchHas:
            """Grammar rule.

            has_stmt: KW_STATIC? (KW_LET | KW_HAS) access_tag? has_assign_list SEMI
            """
            chomp = [*kid]
            is_static = (
                isinstance(chomp[0], uni.Token) and chomp[0].name == Tok.KW_STATIC
            )
            chomp = chomp[1:] if is_static else chomp
            is_freeze = isinstance(chomp[0], uni.Token) and chomp[0].name == Tok.KW_LET
            chomp = chomp[1:]
            access = chomp[0] if isinstance(chomp[0], uni.SubTag) else None
            chomp = chomp[1:] if access else chomp
            assign = chomp[0]
            if isinstance(assign, uni.SubNodeList):
                return uni.ArchHas(
                    vars=assign,
                    is_static=is_static,
                    is_frozen=is_freeze,
                    access=access,
                    kid=kid,
                )
            else:
                raise self.ice()

        def has_assign_list(self, _: None) -> uni.SubNodeList[uni.HasVar]:
            """Grammar rule.

            has_assign_list: (has_assign_list COMMA)? typed_has_clause
            """
            if consume := self.match(uni.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                assign = self.consume(uni.HasVar)
                new_kid = [*consume.kid, comma, assign]
            else:
                assign = self.consume(uni.HasVar)
                new_kid = [assign]
            valid_kid = [i for i in new_kid if isinstance(i, uni.HasVar)]
            return uni.SubNodeList[uni.HasVar](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def typed_has_clause(self, _: None) -> uni.HasVar:
            """Grammar rule.

            typed_has_clause: named_ref (COLON STRING)? type_tag (EQ expression | KW_BY KW_POST_INIT)?
            """
            semstr: uni.String | None = None
            value: uni.Expr | None = None
            defer: bool = False
            name = self.consume(uni.Name)
            if self.match_token(Tok.COLON):
                semstr = self.consume(uni.String)
            type_tag = self.consume(uni.SubTag)
            if self.match_token(Tok.EQ):
                value = self.consume(uni.Expr)
            elif self.match_token(Tok.KW_BY):
                defer = bool(self.consume_token(Tok.KW_POST_INIT))
            return uni.HasVar(
                semstr=semstr,
                name=name,
                type_tag=type_tag,
                defer=defer,
                value=value,
                kid=self.cur_nodes,
            )

        def type_tag(self, _: None) -> uni.SubTag[uni.Expr]:
            """Grammar rule.

            type_tag: COLON expression
            """
            self.consume_token(Tok.COLON)
            tag = self.consume(uni.Expr)
            return uni.SubTag[uni.Expr](tag=tag, kid=self.cur_nodes)

        def builtin_type(self, _: None) -> uni.Token:
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
            token = self.consume(uni.Token)
            return uni.BuiltinType(
                name=token.name,
                orig_src=self.parse_ref.ir_in,
                value=token.value,
                line=token.loc.first_line,
                end_line=token.loc.last_line,
                col_start=token.loc.col_start,
                col_end=token.loc.col_end,
                pos_start=token.pos_start,
                pos_end=token.pos_end,
            )

        def code_block(
            self, kid: list[uni.UniNode]
        ) -> uni.SubNodeList[uni.CodeBlockStmt]:
            """Grammar rule.

            code_block: LBRACE statement* RBRACE
            """
            left_enc = kid[0] if isinstance(kid[0], uni.Token) else None
            right_enc = kid[-1] if isinstance(kid[-1], uni.Token) else None
            valid_stmt = [i for i in kid if isinstance(i, uni.CodeBlockStmt)]
            if len(valid_stmt) == len(kid) - 2:
                return uni.SubNodeList[uni.CodeBlockStmt](
                    items=valid_stmt,
                    delim=Tok.WS,
                    left_enc=left_enc,
                    right_enc=right_enc,
                    kid=kid,
                )
            else:
                raise self.ice()

        def statement(self, kid: list[uni.UniNode]) -> uni.CodeBlockStmt:
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
            if (code_block := self.match(uni.CodeBlockStmt)) and len(
                self.cur_nodes
            ) < 2:
                return code_block
            elif (token := self.match(uni.Token)) and token.name == Tok.KW_YIELD:
                return uni.ExprStmt(
                    expr=(
                        expr := uni.YieldExpr(
                            expr=None,
                            with_from=False,
                            kid=self.cur_nodes,
                        )
                    ),
                    in_fstring=False,
                    kid=[expr],
                )
            elif isinstance(kid[0], uni.Expr):
                return uni.ExprStmt(
                    expr=kid[0],
                    in_fstring=False,
                    kid=self.cur_nodes,
                )
            elif isinstance(kid[0], uni.CodeBlockStmt):
                kid[0].add_kids_right([kid[1]])
                return kid[0]
            else:
                raise self.ice()

        def typed_ctx_block(self, _: None) -> uni.TypedCtxBlock:
            """Grammar rule.

            typed_ctx_block: RETURN_HINT expression code_block
            """
            self.consume_token(Tok.RETURN_HINT)
            ctx = self.consume(uni.Expr)
            body = self.consume(uni.SubNodeList)
            return uni.TypedCtxBlock(
                type_ctx=ctx,
                body=body,
                kid=self.cur_nodes,
            )

        def if_stmt(self, _: None) -> uni.IfStmt:
            """Grammar rule.

            if_stmt: KW_IF expression code_block (elif_stmt | else_stmt)?
            """
            self.consume_token(Tok.KW_IF)
            condition = self.consume(uni.Expr)
            body = self.consume(uni.SubNodeList)
            else_body = self.match(uni.ElseStmt) or self.match(uni.ElseIf)
            return uni.IfStmt(
                condition=condition,
                body=body,
                else_body=else_body,
                kid=self.cur_nodes,
            )

        def elif_stmt(self, _: None) -> uni.ElseIf:
            """Grammar rule.

            elif_stmt: KW_ELIF expression code_block (elif_stmt | else_stmt)?
            """
            self.consume_token(Tok.KW_ELIF)
            condition = self.consume(uni.Expr)
            body = self.consume(uni.SubNodeList)
            else_body = self.match(uni.ElseStmt) or self.match(uni.ElseIf)
            return uni.ElseIf(
                condition=condition,
                body=body,
                else_body=else_body,
                kid=self.cur_nodes,
            )

        def else_stmt(self, _: None) -> uni.ElseStmt:
            """Grammar rule.

            else_stmt: KW_ELSE code_block
            """
            self.consume_token(Tok.KW_ELSE)
            body = self.consume(uni.SubNodeList)
            return uni.ElseStmt(
                body=body,
                kid=self.cur_nodes,
            )

        def try_stmt(self, _: None) -> uni.TryStmt:
            """Grammar rule.

            try_stmt: KW_TRY code_block except_list? else_stmt? finally_stmt?
            """
            self.consume_token(Tok.KW_TRY)
            block = self.consume(uni.SubNodeList)
            except_list = self.match(uni.SubNodeList)
            else_stmt = self.match(uni.ElseStmt)
            finally_stmt = self.match(uni.FinallyStmt)
            return uni.TryStmt(
                body=block,
                excepts=except_list,
                else_body=else_stmt,
                finally_body=finally_stmt,
                kid=self.cur_nodes,
            )

        def except_list(self, _: None) -> uni.SubNodeList[uni.Except]:
            """Grammar rule.

            except_list: except_def+
            """
            items = [self.consume(uni.Except)]
            while expt := self.match(uni.Except):
                items.append(expt)
            return uni.SubNodeList[uni.Except](
                items=items,
                delim=Tok.WS,
                kid=self.cur_nodes,
            )

        def except_def(self, _: None) -> uni.Except:
            """Grammar rule.

            except_def: KW_EXCEPT expression (KW_AS NAME)? code_block
            """
            name: uni.Name | None = None
            self.consume_token(Tok.KW_EXCEPT)
            ex_type = self.consume(uni.Expr)
            if self.match_token(Tok.KW_AS):
                name = self.consume(uni.Name)
            body = self.consume(uni.SubNodeList)
            return uni.Except(
                ex_type=ex_type,
                name=name,
                body=body,
                kid=self.cur_nodes,
            )

        def finally_stmt(self, _: None) -> uni.FinallyStmt:
            """Grammar rule.

            finally_stmt: KW_FINALLY code_block
            """
            self.consume_token(Tok.KW_FINALLY)
            body = self.consume(uni.SubNodeList)
            return uni.FinallyStmt(
                body=body,
                kid=self.cur_nodes,
            )

        def for_stmt(self, _: None) -> uni.IterForStmt | uni.InForStmt:
            """Grammar rule.

            for_stmt: KW_ASYNC? KW_FOR assignment KW_TO expression KW_BY
                        expression code_block else_stmt?
                    | KW_ASYNC? KW_FOR expression KW_IN expression code_block else_stmt?
            """
            is_async = bool(self.match_token(Tok.KW_ASYNC))
            self.consume_token(Tok.KW_FOR)
            if iter := self.match(uni.Assignment):
                self.consume_token(Tok.KW_TO)
                condition = self.consume(uni.Expr)
                self.consume_token(Tok.KW_BY)
                count_by = self.consume(uni.Assignment)
                body = self.consume(uni.SubNodeList)
                else_body = self.match(uni.ElseStmt)
                return uni.IterForStmt(
                    is_async=is_async,
                    iter=iter,
                    condition=condition,
                    count_by=count_by,
                    body=body,
                    else_body=else_body,
                    kid=self.cur_nodes,
                )
            target = self.consume(uni.Expr)
            self.consume_token(Tok.KW_IN)
            collection = self.consume(uni.Expr)
            body = self.consume(uni.SubNodeList)
            else_body = self.match(uni.ElseStmt)
            return uni.InForStmt(
                is_async=is_async,
                target=target,
                collection=collection,
                body=body,
                else_body=else_body,
                kid=self.cur_nodes,
            )

        def while_stmt(self, _: None) -> uni.WhileStmt:
            """Grammar rule.

            while_stmt: KW_WHILE expression code_block
            """
            self.consume_token(Tok.KW_WHILE)
            condition = self.consume(uni.Expr)
            body = self.consume(uni.SubNodeList)
            return uni.WhileStmt(
                condition=condition,
                body=body,
                kid=self.cur_nodes,
            )

        def with_stmt(self, _: None) -> uni.WithStmt:
            """Grammar rule.

            with_stmt: KW_ASYNC? KW_WITH expr_as_list code_block
            """
            is_async = bool(self.match_token(Tok.KW_ASYNC))
            self.consume_token(Tok.KW_WITH)
            exprs = self.consume(uni.SubNodeList)
            body = self.consume(uni.SubNodeList)
            return uni.WithStmt(
                is_async=is_async,
                exprs=exprs,
                body=body,
                kid=self.cur_nodes,
            )

        def expr_as_list(self, _: None) -> uni.SubNodeList[uni.ExprAsItem]:
            """Grammar rule.

            expr_as_list: (expr_as COMMA)* expr_as
            """
            items = [self.consume(uni.ExprAsItem)]
            while self.match_token(Tok.COMMA):
                items.append(self.consume(uni.ExprAsItem))
            return uni.SubNodeList[uni.ExprAsItem](
                items=items,
                delim=Tok.COMMA,
                kid=self.cur_nodes,
            )

        def expr_as(self, _: None) -> uni.ExprAsItem:
            """Grammar rule.

            expr_as: expression (KW_AS expression)?
            """
            expr = self.consume(uni.Expr)
            alias = self.consume(uni.Expr) if self.match_token(Tok.KW_AS) else None
            return uni.ExprAsItem(
                expr=expr,
                alias=alias,
                kid=self.cur_nodes,
            )

        def raise_stmt(self, _: None) -> uni.RaiseStmt:
            """Grammar rule.

            raise_stmt: KW_RAISE (expression (KW_FROM expression)?)?
            """
            e_type: uni.Expr | None = None
            from_target: uni.Expr | None = None
            self.consume_token(Tok.KW_RAISE)
            if e_type := self.match(uni.Expr):
                from_target = (
                    self.consume(uni.Expr) if self.match_token(Tok.KW_FROM) else None
                )
            return uni.RaiseStmt(
                cause=e_type,
                from_target=from_target,
                kid=self.cur_nodes,
            )

        def assert_stmt(self, _: None) -> uni.AssertStmt:
            """Grammar rule.

            assert_stmt: KW_ASSERT expression (COMMA expression)?
            """
            error_msg: uni.Expr | None = None
            self.consume_token(Tok.KW_ASSERT)
            condition = self.consume(uni.Expr)
            if self.match_token(Tok.COMMA):
                error_msg = self.consume(uni.Expr)
            return uni.AssertStmt(
                condition=condition,
                error_msg=error_msg,
                kid=self.cur_nodes,
            )

        def check_stmt(self, _: None) -> uni.CheckStmt:
            """Grammar rule.

            check_stmt: KW_CHECK expression
            """
            self.consume_token(Tok.KW_CHECK)
            target = self.consume(uni.Expr)
            return uni.CheckStmt(
                target=target,
                kid=self.cur_nodes,
            )

        def ctrl_stmt(self, _: None) -> uni.CtrlStmt:
            """Grammar rule.

            ctrl_stmt: KW_SKIP | KW_BREAK | KW_CONTINUE
            """
            tok = (
                self.match_token(Tok.KW_SKIP)
                or self.match_token(Tok.KW_BREAK)
                or self.consume_token(Tok.KW_CONTINUE)
            )
            return uni.CtrlStmt(
                ctrl=tok,
                kid=self.cur_nodes,
            )

        def delete_stmt(self, _: None) -> uni.DeleteStmt:
            """Grammar rule.

            delete_stmt: KW_DELETE expression
            """
            self.consume_token(Tok.KW_DELETE)
            target = self.consume(uni.Expr)
            return uni.DeleteStmt(
                target=target,
                kid=self.cur_nodes,
            )

        def report_stmt(self, _: None) -> uni.ReportStmt:
            """Grammar rule.

            report_stmt: KW_REPORT expression
            """
            self.consume_token(Tok.KW_REPORT)
            target = self.consume(uni.Expr)
            return uni.ReportStmt(
                expr=target,
                kid=self.cur_nodes,
            )

        def return_stmt(self, _: None) -> uni.ReturnStmt:
            """Grammar rule.

            return_stmt: KW_RETURN expression?
            """
            self.consume_token(Tok.KW_RETURN)
            expr = self.match(uni.Expr)
            return uni.ReturnStmt(
                expr=expr,
                kid=self.cur_nodes,
            )

        def walker_stmt(self, _: None) -> uni.CodeBlockStmt:
            """Grammar rule.

            walker_stmt: disengage_stmt | revisit_stmt | visit_stmt | ignore_stmt
            """
            return self.consume(uni.CodeBlockStmt)

        def ignore_stmt(self, _: None) -> uni.IgnoreStmt:
            """Grammar rule.

            ignore_stmt: KW_IGNORE expression SEMI
            """
            self.consume_token(Tok.KW_IGNORE)
            target = self.consume(uni.Expr)
            self.consume_token(Tok.SEMI)
            return uni.IgnoreStmt(
                target=target,
                kid=self.cur_nodes,
            )

        def visit_stmt(self, _: None) -> uni.VisitStmt:
            """Grammar rule.

            visit_stmt: KW_VISIT (inherited_archs)? expression (else_stmt | SEMI)
            """
            self.consume_token(Tok.KW_VISIT)
            sub_name = self.match(uni.SubNodeList)
            target = self.consume(uni.Expr)
            else_body = self.match(uni.ElseStmt)
            if else_body is None:
                self.consume_token(Tok.SEMI)
            return uni.VisitStmt(
                vis_type=sub_name,
                target=target,
                else_body=else_body,
                kid=self.cur_nodes,
            )

        def revisit_stmt(self, _: None) -> uni.RevisitStmt:
            """Grammar rule.

            revisit_stmt: KW_REVISIT expression? (else_stmt | SEMI)
            """
            self.consume_token(Tok.KW_REVISIT)
            target = self.match(uni.Expr)
            else_body = self.match(uni.ElseStmt)
            if else_body is None:
                self.consume_token(Tok.SEMI)
            return uni.RevisitStmt(
                hops=target,
                else_body=else_body,
                kid=self.cur_nodes,
            )

        def disengage_stmt(self, _: None) -> uni.DisengageStmt:
            """Grammar rule.

            disengage_stmt: KW_DISENGAGE SEMI
            """
            kw = self.consume_token(Tok.KW_DISENGAGE)
            semi = self.consume_token(Tok.SEMI)
            return uni.DisengageStmt(
                kid=[kw, semi],
            )

        def global_ref(self, _: None) -> uni.GlobalStmt:
            """Grammar rule.

            global_ref: GLOBAL_OP name_list
            """
            self.consume_token(Tok.GLOBAL_OP)
            target = self.consume(uni.SubNodeList)
            return uni.GlobalStmt(
                target=target,
                kid=self.cur_nodes,
            )

        def nonlocal_ref(self, _: None) -> uni.NonLocalStmt:
            """Grammar rule.

            nonlocal_ref: NONLOCAL_OP name_list
            """
            self.consume_token(Tok.NONLOCAL_OP)
            target = self.consume(uni.SubNodeList)
            return uni.NonLocalStmt(
                target=target,
                kid=self.cur_nodes,
            )

        def assignment(self, _: None) -> uni.Assignment:
            """Grammar rule.

            assignment: KW_LET? (atomic_chain EQ)+ (yield_expr | expression)
                    | atomic_chain (COLON STRING)? type_tag (EQ (yield_expr | expression))?
                    | atomic_chain aug_op (yield_expr | expression)
            """
            assignees: list = []
            type_tag: uni.SubTag | None = None
            is_aug: uni.Token | None = None
            semstr: uni.String | None = None

            is_frozen = bool(self.match_token(Tok.KW_LET))
            if first_expr := self.match(uni.Expr):
                assignees.append(first_expr)

            token = self.match(uni.Token)
            if token and (token.name == Tok.EQ):
                assignees.append(token)
                while expr := self.match(uni.Expr):
                    eq = self.match_token(Tok.EQ)
                    assignees.append(expr)
                    if eq:
                        assignees.append(eq)
                value = assignees.pop()
            elif token and (token.name not in {Tok.COLON, Tok.EQ}):
                is_aug = token
                value = self.consume(uni.Expr)
            else:
                semstr = (
                    self.match(uni.String)
                    if (token and (token.name == Tok.COLON))
                    else None
                )
                type_tag = self.consume(uni.SubTag)
                value = self.consume(uni.Expr) if self.match_token(Tok.EQ) else None

            valid_assignees = [i for i in assignees if isinstance(i, (uni.Expr))]
            new_targ = uni.SubNodeList[uni.Expr](
                items=valid_assignees,
                delim=Tok.EQ,
                kid=assignees,
            )
            kid = [x for x in self.cur_nodes if x not in assignees]
            kid.insert(1, new_targ) if is_frozen else kid.insert(0, new_targ)
            if is_aug:
                return uni.Assignment(
                    target=new_targ,
                    type_tag=type_tag,
                    value=value,
                    mutable=is_frozen,
                    aug_op=is_aug,
                    kid=kid,
                )
            return uni.Assignment(
                target=new_targ,
                type_tag=type_tag,
                value=value,
                mutable=is_frozen,
                kid=kid,
                semstr=semstr,
            )

        def expression(self, _: None) -> uni.Expr:
            """Grammar rule.

            expression: walrus_assign
                    | pipe (KW_IF expression KW_ELSE expression)?
                    | lambda_expr
            """
            value = self.consume(uni.Expr)
            if self.match_token(Tok.KW_IF):
                condition = self.consume(uni.Expr)
                self.consume_token(Tok.KW_ELSE)
                else_value = self.consume(uni.Expr)
                return uni.IfElseExpr(
                    value=value,
                    condition=condition,
                    else_value=else_value,
                    kid=self.cur_nodes,
                )
            return value

        def walrus_assign(self, _: None) -> uni.Expr:
            """Grammar rule.

            walrus_assign: (walrus_assign WALRUS_EQ)? pipe
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def lambda_expr(self, _: None) -> uni.LambdaExpr:
            """Grammar rule.

            lamda_expr: KW_WITH func_decl_params? (RETURN_HINT expression)? KW_CAN expression
            """
            return_type: uni.Expr | None = None
            sig_kid: list[uni.UniNode] = []
            self.consume_token(Tok.KW_WITH)
            params = self.match(uni.SubNodeList)
            if self.match_token(Tok.RETURN_HINT):
                return_type = self.consume(uni.Expr)
            self.consume_token(Tok.KW_CAN)
            body = self.consume(uni.Expr)
            if params:
                sig_kid.append(params)
            if return_type:
                sig_kid.append(return_type)
            signature = (
                uni.FuncSignature(
                    params=params,
                    return_type=return_type,
                    kid=sig_kid,
                )
                if params or return_type
                else None
            )
            new_kid = [i for i in self.cur_nodes if i != params and i != return_type]
            new_kid.insert(1, signature) if signature else None
            return uni.LambdaExpr(
                signature=signature,
                body=body,
                kid=new_kid,
            )

        def pipe(self, _: None) -> uni.Expr:
            """Grammar rule.

            pipe: pipe_back PIPE_FWD pipe
                | pipe_back
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def pipe_back(self, _: None) -> uni.Expr:
            """Grammar rule.

            pipe_back: bitwise_or PIPE_BKWD pipe_back
                     | bitwise_or
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def bitwise_or(self, _: None) -> uni.Expr:
            """Grammar rule.

            bitwise_or: bitwise_xor BW_OR bitwise_or
                      | bitwise_xor
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def bitwise_xor(self, _: None) -> uni.Expr:
            """Grammar rule.

            bitwise_xor: bitwise_and BW_XOR bitwise_xor
                       | bitwise_and
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def bitwise_and(self, _: None) -> uni.Expr:
            """Grammar rule.

            bitwise_and: shift BW_AND bitwise_and
                       | shift
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def shift(self, _: None) -> uni.Expr:
            """Grammar rule.

            shift: (shift (RSHIFT | LSHIFT))? logical_or
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def logical_or(self, _: None) -> uni.Expr:
            """Grammar rule.

            logical_or: logical_and (KW_OR logical_and)*
            """
            value = self.consume(uni.Expr)
            if not (ops := self.match_token(Tok.KW_OR)):
                return value
            values: list = [value]
            while value := self.consume(uni.Expr):
                values.append(value)
                if not self.match_token(Tok.KW_OR):
                    break
            return uni.BoolExpr(
                op=ops,
                values=values,
                kid=self.cur_nodes,
            )

        def logical_and(self, _: None) -> uni.Expr:
            """Grammar rule.

            logical_and: logical_not (KW_AND logical_not)*
            """
            value = self.consume(uni.Expr)
            if not (ops := self.match_token(Tok.KW_AND)):
                return value
            values: list = [value]
            while value := self.consume(uni.Expr):
                values.append(value)
                if not self.match_token(Tok.KW_AND):
                    break
            return uni.BoolExpr(
                op=ops,
                values=values,
                kid=self.cur_nodes,
            )

        def logical_not(self, _: None) -> uni.Expr:
            """Grammar rule.

            logical_not: NOT logical_not | compare
            """
            if op := self.match_token(Tok.NOT):
                operand = self.consume(uni.Expr)
                return uni.UnaryExpr(
                    op=op,
                    operand=operand,
                    kid=self.cur_nodes,
                )
            return self.consume(uni.Expr)

        def compare(self, _: None) -> uni.Expr:
            """Grammar rule.

            compare: (arithmetic cmp_op)* arithmetic
            """
            ops: list = []
            rights: list = []
            left = self.consume(uni.Expr)
            while op := self.match(uni.Token):
                ops.append(op)
                rights.append(self.consume(uni.Expr))
            if not ops:
                return left
            return uni.CompareExpr(
                left=left,
                ops=ops,
                rights=rights,
                kid=self.cur_nodes,
            )

        def cmp_op(self, _: None) -> uni.Token:
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
            return self.consume(uni.Token)

        def arithmetic(self, _: None) -> uni.Expr:
            """Grammar rule.

            arithmetic: (arithmetic (MINUS | PLUS))? term
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def term(self, _: None) -> uni.Expr:
            """Grammar rule.

            term: (term (MOD | DIV | FLOOR_DIV | STAR_MUL | DECOR_OP))? power
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def factor(self, _: None) -> uni.Expr:
            """Grammar rule.

            factor: (BW_NOT | MINUS | PLUS) factor | connect
            """
            if (
                op := self.match_token(Tok.BW_NOT)
                or self.match_token(Tok.MINUS)
                or self.match_token(Tok.PLUS)
            ):
                operand = self.consume(uni.Expr)
                return uni.UnaryExpr(
                    op=op,
                    operand=operand,
                    kid=self.cur_nodes,
                )
            return self._binary_expr_unwind(self.cur_nodes)

        def power(self, _: None) -> uni.Expr:
            """Grammar rule.

            power: (power STAR_POW)? factor
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def connect(self, _: None) -> uni.Expr:
            """Grammar rule.

            connect: (connect (connect_op | disconnect_op))? atomic_pipe
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def atomic_pipe(self, _: None) -> uni.Expr:
            """Grammar rule.

            atomic_pipe: (atomic_pipe A_PIPE_FWD)? atomic_pipe_back
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def atomic_pipe_back(self, _: None) -> uni.Expr:
            """Grammar rule.

            atomic_pipe_back: (atomic_pipe_back A_PIPE_BKWD)? ds_spawn
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def ds_spawn(self, _: None) -> uni.Expr:
            """Grammar rule.

            ds_spawn: (ds_spawn KW_SPAWN)? unpack
            """
            return self._binary_expr_unwind(self.cur_nodes)

        def unpack(self, _: None) -> uni.Expr:
            """Grammar rule.

            unpack: STAR_MUL? ref
            """
            if op := self.match_token(Tok.STAR_MUL):
                operand = self.consume(uni.Expr)
                return uni.UnaryExpr(
                    op=op,
                    operand=operand,
                    kid=self.cur_nodes,
                )
            return self._binary_expr_unwind(self.cur_nodes)

        def ref(self, _: None) -> uni.Expr:
            """Grammar rule.

            ref: walrus_assign
               | BW_AND walrus_assign
            """
            if op := self.match_token(Tok.BW_AND):
                operand = self.consume(uni.Expr)
                return uni.UnaryExpr(
                    op=op,
                    operand=operand,
                    kid=self.cur_nodes,
                )
            return self._binary_expr_unwind(self.cur_nodes)

        def pipe_call(self, _: None) -> uni.Expr:
            """Grammar rule.

            pipe_call: atomic_chain
                | PIPE_FWD atomic_chain
                | A_PIPE_FWD atomic_chain
                | KW_SPAWN atomic_chain
                | KW_AWAIT atomic_chain
            """
            if len(self.cur_nodes) == 2:
                if self.match_token(Tok.KW_AWAIT):
                    target = self.consume(uni.Expr)
                    return uni.AwaitExpr(
                        target=target,
                        kid=self.cur_nodes,
                    )
                elif op := self.match(uni.Token):
                    operand = self.consume(uni.Expr)
                    return uni.UnaryExpr(
                        op=op,
                        operand=operand,
                        kid=self.cur_nodes,
                    )
            return self._binary_expr_unwind(self.cur_nodes)

        def aug_op(self, _: None) -> uni.Token:
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
            return self.consume(uni.Token)

        def atomic_chain(self, _: None) -> uni.Expr:
            """Grammar rule.

            atomic_chain: atomic_chain NULL_OK? (filter_compr | assign_compr | index_slice)
                        | atomic_chain NULL_OK? (DOT_BKWD | DOT_FWD | DOT) named_ref
                        | (atomic_call | atom | edge_ref_chain)
            """
            if len(self.cur_nodes) == 1:
                return self.consume(uni.Expr)
            target = self.consume(uni.Expr)
            is_null_ok = bool(self.match_token(Tok.NULL_OK))
            if right := self.match(uni.AtomExpr):
                return uni.AtomTrailer(
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
            name = self.match(uni.AtomExpr) or self.consume(uni.AtomTrailer)
            return uni.AtomTrailer(
                target=(target if token.name != Tok.DOT_BKWD else name),
                right=(name if token.name != Tok.DOT_BKWD else target),
                is_null_ok=is_null_ok,
                is_attr=True,
                kid=self.cur_nodes,
            )

        def atomic_call(self, _: None) -> uni.FuncCall:
            """Grammar rule.

            atomic_call: atomic_chain LPAREN param_list? (KW_BY atomic_call)? RPAREN
            """
            genai_call: uni.FuncCall | None = None
            target = self.consume(uni.Expr)
            self.consume_token(Tok.LPAREN)
            params = self.match(uni.SubNodeList)
            if self.match_token(Tok.KW_BY):
                genai_call = self.consume(uni.FuncCall)
            self.consume_token(Tok.RPAREN)
            return uni.FuncCall(
                target=target,
                params=params,
                genai_call=genai_call,
                kid=self.cur_nodes,
            )

        def index_slice(self, _: None) -> uni.IndexSlice:
            """Grammar rule.

            index_slice: LSQUARE                                                        \
                            expression? COLON expression? (COLON expression?)?          \
                            (COMMA expression? COLON expression? (COLON expression?)?)* \
                         RSQUARE
                        | list_val
            """
            if len(self.cur_nodes) == 1:
                index = self.consume(uni.ListVal)
                if not index.values:
                    raise self.ice()
                if len(index.values.items) == 1:
                    expr = index.values.items[0] if index.values else None
                    kid = self.cur_nodes
                else:
                    sublist = uni.SubNodeList[uni.Expr | uni.KWPair](
                        items=[*index.values.items], delim=Tok.COMMA, kid=index.kid
                    )
                    expr = uni.TupleVal(values=sublist, kid=[sublist])
                    kid = [expr]
                return uni.IndexSlice(
                    slices=[uni.IndexSlice.Slice(start=expr, stop=None, step=None)],
                    is_range=False,
                    kid=kid,
                )
            else:
                self.consume_token(Tok.LSQUARE)
                slices: list[uni.IndexSlice.Slice] = []
                while not self.match_token(Tok.RSQUARE):
                    expr1 = self.match(uni.Expr)
                    self.consume_token(Tok.COLON)
                    expr2 = self.match(uni.Expr)
                    expr3 = (
                        self.match(uni.Expr) if self.match_token(Tok.COLON) else None
                    )
                    self.match_token(Tok.COMMA)
                    slices.append(
                        uni.IndexSlice.Slice(start=expr1, stop=expr2, step=expr3)
                    )
                return uni.IndexSlice(
                    slices=slices,
                    is_range=True,
                    kid=self.cur_nodes,
                )

        def atom(self, _: None) -> uni.Expr:
            """Grammar rule.

            atom: named_ref
                 | LPAREN (expression | yield_expr) RPAREN
                 | atom_collection
                 | atom_literal
                 | type_ref
            """
            if self.match_token(Tok.LPAREN):
                value = self.match(uni.Expr) or self.consume(uni.YieldExpr)
                self.consume_token(Tok.RPAREN)
                return uni.AtomUnit(value=value, kid=self.cur_nodes)
            return self.consume(uni.AtomExpr)

        def yield_expr(self, _: None) -> uni.YieldExpr:
            """Grammar rule.

            yield_expr: KW_YIELD KW_FROM? expression
            """
            self.consume_token(Tok.KW_YIELD)
            is_with_from = bool(self.match_token(Tok.KW_FROM))
            expr = self.consume(uni.Expr)
            return uni.YieldExpr(
                expr=expr,
                with_from=is_with_from,
                kid=self.cur_nodes,
            )

        def atom_literal(self, _: None) -> uni.AtomExpr:
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
            return self.consume(uni.AtomExpr)

        def atom_collection(self, kid: list[uni.UniNode]) -> uni.AtomExpr:
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
            return self.consume(uni.AtomExpr)

        def multistring(self, _: None) -> uni.AtomExpr:
            """Grammar rule.

            multistring: (fstring | STRING)+
            """
            valid_strs = [self.match(uni.String) or self.consume(uni.FString)]
            while node := (self.match(uni.String) or self.match(uni.FString)):
                valid_strs.append(node)
            return uni.MultiString(
                strings=valid_strs,
                kid=self.cur_nodes,
            )

        def fstring(self, _: None) -> uni.FString:
            """Grammar rule.

            fstring: FSTR_START fstr_parts FSTR_END
                | FSTR_SQ_START fstr_sq_parts FSTR_SQ_END
            """
            self.match_token(Tok.FSTR_START) or self.consume_token(Tok.FSTR_SQ_START)
            target = self.match(uni.SubNodeList)
            self.match_token(Tok.FSTR_END) or self.consume_token(Tok.FSTR_SQ_END)
            return uni.FString(
                parts=target,
                kid=self.cur_nodes,
            )

        def fstr_parts(self, _: None) -> uni.SubNodeList[uni.String | uni.ExprStmt]:
            """Grammar rule.

            fstr_parts: (FSTR_PIECE | FSTR_BESC | LBRACE expression RBRACE )*
            """
            valid_parts: list[uni.String | uni.ExprStmt] = [
                (
                    i
                    if isinstance(i, uni.String)
                    else uni.ExprStmt(expr=i, in_fstring=True, kid=[i])
                )
                for i in self.cur_nodes
                if isinstance(i, uni.Expr)
            ]
            return uni.SubNodeList[uni.String | uni.ExprStmt](
                items=valid_parts,
                delim=None,
                kid=valid_parts,
            )

        def fstr_sq_parts(self, _: None) -> uni.SubNodeList[uni.String | uni.ExprStmt]:
            """Grammar rule.

            fstr_sq_parts: (FSTR_SQ_PIECE | FSTR_BESC | LBRACE expression RBRACE )*
            """
            valid_parts: list[uni.String | uni.ExprStmt] = [
                (
                    i
                    if isinstance(i, uni.String)
                    else uni.ExprStmt(expr=i, in_fstring=True, kid=[i])
                )
                for i in self.cur_nodes
                if isinstance(i, uni.Expr)
            ]
            return uni.SubNodeList[uni.String | uni.ExprStmt](
                items=valid_parts,
                delim=None,
                kid=valid_parts,
            )

        def list_val(self, _: None) -> uni.ListVal:
            """Grammar rule.

            list_val: LSQUARE (expr_list COMMA?)? RSQUARE
            """
            self.consume_token(Tok.LSQUARE)
            values = self.match(uni.SubNodeList)
            self.match_token(Tok.COMMA)
            self.consume_token(Tok.RSQUARE)
            return uni.ListVal(
                values=values,
                kid=self.cur_nodes,
            )

        def tuple_val(self, _: None) -> uni.TupleVal:
            """Grammar rule.

            tuple_val: LPAREN tuple_list? RPAREN
            """
            self.consume_token(Tok.LPAREN)
            target = self.match(uni.SubNodeList)
            self.consume_token(Tok.RPAREN)
            return uni.TupleVal(
                values=target,
                kid=self.cur_nodes,
            )

        def set_val(self, _: None) -> uni.SetVal:
            """Grammar rule.

            set_val: LBRACE expr_list COMMA? RBRACE
            """
            self.match_token(Tok.LBRACE)
            expr_list = self.match(uni.SubNodeList)
            self.match_token(Tok.COMMA)
            self.match_token(Tok.RBRACE)
            return uni.SetVal(
                values=expr_list,
                kid=self.cur_nodes,
            )

        def expr_list(self, kid: list[uni.UniNode]) -> uni.SubNodeList[uni.Expr]:
            """Grammar rule.

            expr_list: (expr_list COMMA)? expression
            """
            new_kid: list = []
            if consume := self.match(uni.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                new_kid.extend([*consume.kid, comma])
            expr = self.consume(uni.Expr)
            new_kid.extend([expr])
            valid_kid = [i for i in new_kid if isinstance(i, uni.Expr)]
            return uni.SubNodeList[uni.Expr](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def kw_expr_list(self, kid: list[uni.UniNode]) -> uni.SubNodeList[uni.KWPair]:
            """Grammar rule.

            kw_expr_list: (kw_expr_list COMMA)? kw_expr
            """
            if consume := self.match(uni.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                expr = self.consume(uni.KWPair)
                new_kid = [*consume.kid, comma, expr]
            else:
                expr = self.consume(uni.KWPair)
                new_kid = [expr]
            valid_kid = [i for i in new_kid if isinstance(i, uni.KWPair)]
            return uni.SubNodeList[uni.KWPair](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def kw_expr(self, _: None) -> uni.KWPair:
            """Grammar rule.

            kw_expr: named_ref EQ expression | STAR_POW expression
            """
            if self.match_token(Tok.STAR_POW):
                value = self.consume(uni.Expr)
                key = None
            else:
                key = self.consume(uni.Name)
                self.consume_token(Tok.EQ)
                value = self.consume(uni.Expr)
            return uni.KWPair(
                key=key,
                value=value,
                kid=self.cur_nodes,
            )

        def name_list(self, _: None) -> uni.SubNodeList[uni.Name]:
            """Grammar rule.

            name_list: (named_ref COMMA)* named_ref
            """
            valid_kid = [self.consume(uni.Name)]
            while self.match_token(Tok.COMMA):
                valid_kid.append(self.consume(uni.Name))
            return uni.SubNodeList[uni.Name](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=self.cur_nodes,
            )

        def tuple_list(self, _: None) -> uni.SubNodeList[uni.Expr | uni.KWPair]:
            """Grammar rule.

            tuple_list: expression COMMA expr_list    COMMA kw_expr_list COMMA?
                      | expression COMMA kw_expr_list COMMA?
                      | expression COMMA expr_list    COMMA?
                      | expression COMMA
                      | kw_expr_list COMMA?
            """
            if first_expr := self.match(uni.SubNodeList):
                comma = self.match_token(Tok.COMMA)
                if comma:
                    first_expr.kid.append(comma)
                return first_expr
            expr = self.consume(uni.Expr)
            self.consume_token(Tok.COMMA)
            second_expr = self.match(uni.SubNodeList)
            self.match_token(Tok.COMMA)
            kw_expr_list = self.match(uni.SubNodeList)
            self.match_token(Tok.COMMA)
            expr_list: list = []
            if second_expr:
                expr_list = second_expr.kid
                if kw_expr_list:
                    expr_list = [*expr_list, *kw_expr_list.kid]
            expr_list = [expr, *expr_list]
            valid_kid = [i for i in expr_list if isinstance(i, (uni.Expr, uni.KWPair))]
            return uni.SubNodeList[uni.Expr | uni.KWPair](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=self.cur_nodes,
            )

        def dict_val(self, _: None) -> uni.DictVal:
            """Grammar rule.

            dict_val: LBRACE ((kv_pair COMMA)* kv_pair COMMA?)? RBRACE
            """
            self.consume_token(Tok.LBRACE)
            kv_pairs: list = []
            while item := self.match(uni.KVPair):
                kv_pairs.append(item)
                self.match_token(Tok.COMMA)
            self.consume_token(Tok.RBRACE)
            return uni.DictVal(
                kv_pairs=kv_pairs,
                kid=self.cur_nodes,
            )

        def kv_pair(self, _: None) -> uni.KVPair:
            """Grammar rule.

            kv_pair: expression COLON expression | STAR_POW expression
            """
            if self.match_token(Tok.STAR_POW):
                value = self.consume(uni.Expr)
                return uni.KVPair(
                    key=None,
                    value=value,
                    kid=self.cur_nodes,
                )
            key = self.consume(uni.Expr)
            self.consume_token(Tok.COLON)
            value = self.consume(uni.Expr)
            return uni.KVPair(
                key=key,
                value=value,
                kid=self.cur_nodes,
            )

        def list_compr(self, _: None) -> uni.ListCompr:
            """Grammar rule.

            list_compr: LSQUARE expression inner_compr+ RSQUARE
            """
            self.consume_token(Tok.LSQUARE)
            out_expr = self.consume(uni.Expr)
            comprs = self.consume_many(uni.InnerCompr)
            self.consume_token(Tok.RSQUARE)
            return uni.ListCompr(
                out_expr=out_expr,
                compr=comprs,
                kid=self.cur_nodes,
            )

        def gen_compr(self, _: None) -> uni.GenCompr:
            """Grammar rule.

            gen_compr: LPAREN expression inner_compr+ RPAREN
            """
            self.consume_token(Tok.LPAREN)
            out_expr = self.consume(uni.Expr)
            comprs = self.consume_many(uni.InnerCompr)
            self.consume_token(Tok.RPAREN)
            return uni.GenCompr(
                out_expr=out_expr,
                compr=comprs,
                kid=self.cur_nodes,
            )

        def set_compr(self, _: None) -> uni.SetCompr:
            """Grammar rule.

            set_compr: LBRACE expression inner_compr+ RBRACE
            """
            self.consume_token(Tok.LBRACE)
            out_expr = self.consume(uni.Expr)
            comprs = self.consume_many(uni.InnerCompr)
            self.consume_token(Tok.RBRACE)
            return uni.SetCompr(
                out_expr=out_expr,
                compr=comprs,
                kid=self.cur_nodes,
            )

        def dict_compr(self, _: None) -> uni.DictCompr:
            """Grammar rule.

            dict_compr: LBRACE kv_pair inner_compr+ RBRACE
            """
            self.consume_token(Tok.LBRACE)
            kv_pair = self.consume(uni.KVPair)
            comprs = self.consume_many(uni.InnerCompr)
            self.consume_token(Tok.RBRACE)
            return uni.DictCompr(
                kv_pair=kv_pair,
                compr=comprs,
                kid=self.cur_nodes,
            )

        def inner_compr(self, _: None) -> uni.InnerCompr:
            """Grammar rule.

            inner_compr: KW_ASYNC? KW_FOR atomic_chain KW_IN pipe_call (KW_IF walrus_assign)*
            """
            conditional: list = []
            is_async = bool(self.match_token(Tok.KW_ASYNC))
            self.consume_token(Tok.KW_FOR)
            target = self.consume(uni.Expr)
            self.consume_token(Tok.KW_IN)
            collection = self.consume(uni.Expr)
            while self.match_token(Tok.KW_IF):
                conditional.append(self.consume(uni.Expr))
            return uni.InnerCompr(
                is_async=is_async,
                target=target,
                collection=collection,
                conditional=conditional,
                kid=self.cur_nodes,
            )

        def param_list(self, _: None) -> uni.SubNodeList[uni.Expr | uni.KWPair]:
            """Grammar rule.

            param_list: expr_list    COMMA kw_expr_list COMMA?
                      | kw_expr_list COMMA?
                      | expr_list    COMMA?
            """
            kw_expr_list: uni.SubNodeList | None = None
            expr_list = self.consume(uni.SubNodeList)
            if len(self.cur_nodes) > 2:
                self.consume_token(Tok.COMMA)
                kw_expr_list = self.consume(uni.SubNodeList)
            ends_comma = self.match_token(Tok.COMMA)
            if kw_expr_list:
                valid_kid = [
                    i
                    for i in [*expr_list.items, *kw_expr_list.items]
                    if isinstance(i, (uni.Expr, uni.KWPair))
                ]
                return uni.SubNodeList[uni.Expr | uni.KWPair](
                    items=valid_kid,
                    delim=Tok.COMMA,
                    kid=self.cur_nodes,
                )
            else:
                if ends_comma:
                    expr_list.kid.append(ends_comma)
                return expr_list

        def assignment_list(self, _: None) -> uni.SubNodeList[uni.Assignment]:
            """Grammar rule.

            assignment_list: assignment_list COMMA assignment | assignment
            """
            if consume := self.match(uni.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                assign = self.consume(uni.Assignment)
                new_kid = [*consume.kid, comma, assign]
            else:
                assign = self.consume(uni.Assignment)
                new_kid = [assign]
            valid_kid = [i for i in new_kid if isinstance(i, uni.Assignment)]
            return uni.SubNodeList[uni.Assignment](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def arch_ref(self, kid: list[uni.UniNode]) -> uni.ArchRef:
            """Grammar rule.

            arch_ref: object_ref
                    | walker_ref
                    | edge_ref
                    | node_ref
                    | type_ref
            """
            return self.consume(uni.ArchRef)

        def node_ref(self, kid: list[uni.UniNode]) -> uni.ArchRef:
            """Grammar rule.

            node_ref: NODE_OP NAME
            """
            arch_type = self.consume(uni.Token)
            arch_name = self.consume(uni.NameAtom)
            return uni.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def edge_ref(self, kid: list[uni.UniNode]) -> uni.ArchRef:
            """Grammar rule.

            edge_ref: EDGE_OP NAME
            """
            arch_type = self.consume(uni.Token)
            arch_name = self.consume(uni.NameAtom)
            return uni.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def walker_ref(self, kid: list[uni.UniNode]) -> uni.ArchRef:
            """Grammar rule.

            walker_ref: WALKER_OP NAME
            """
            arch_type = self.consume(uni.Token)
            arch_name = self.consume(uni.NameAtom)
            return uni.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def class_ref(self, kid: list[uni.UniNode]) -> uni.ArchRef:
            """Grammar rule.

            class_ref: CLASS_OP name_ref
            """
            arch_type = self.consume(uni.Token)
            arch_name = self.consume(uni.NameAtom)
            return uni.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def object_ref(self, kid: list[uni.UniNode]) -> uni.ArchRef:
            """Grammar rule.

            object_ref: OBJECT_OP name_ref
            """
            arch_type = self.consume(uni.Token)
            arch_name = self.consume(uni.NameAtom)
            return uni.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def type_ref(self, kid: list[uni.UniNode]) -> uni.ArchRef:
            """Grammar rule.

            type_ref: TYPE_OP (named_ref | builtin_type)
            """
            arch_type = self.consume(uni.Token)
            arch_name = self.consume(uni.NameAtom)
            return uni.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def enum_ref(self, kid: list[uni.UniNode]) -> uni.ArchRef:
            """Grammar rule.

            enum_ref: ENUM_OP NAME
            """
            arch_type = self.consume(uni.Token)
            arch_name = self.consume(uni.NameAtom)
            return uni.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def ability_ref(self, _: None) -> uni.ArchRef:
            """Grammar rule.

            ability_ref: ABILITY_OP (special_ref | name_ref)
            """
            arch_type = self.consume_token(Tok.ABILITY_OP)
            arch_name = self.consume(uni.NameAtom)
            return uni.ArchRef(
                arch_type=arch_type,
                arch_name=arch_name,
                kid=self.cur_nodes,
            )

        def arch_or_ability_chain(self, kid: list[uni.UniNode]) -> uni.ArchRefChain:
            """Grammar rule.

            arch_or_ability_chain: arch_or_ability_chain? (ability_ref | arch_ref)
            """
            consume = self.match(uni.ArchRefChain)
            name = self.consume(uni.ArchRef)
            new_kid = [*consume.kid, name] if consume else [name]
            valid_kid = [i for i in new_kid if isinstance(i, uni.ArchRef)]
            return uni.ArchRefChain(
                archs=valid_kid,
                kid=new_kid,
            )

        def abil_to_arch_chain(self, _: None) -> uni.ArchRefChain:
            """Grammar rule.

            abil_to_arch_chain: arch_or_ability_chain? arch_ref
            """
            arch_chain = self.match(uni.ArchRefChain)
            arch_ref = self.consume(uni.ArchRef)
            if arch_chain:
                return uni.ArchRefChain(
                    archs=[*arch_chain.archs, arch_ref],
                    kid=[*arch_chain.kid, arch_ref],
                )
            return uni.ArchRefChain(
                archs=[arch_ref],
                kid=[arch_ref],
            )

        def arch_to_abil_chain(self, _: None) -> uni.ArchRefChain:
            """Grammar rule.

            arch_to_abil_chain: arch_or_ability_chain? ability_ref
            """
            arch_chain = self.match(uni.ArchRefChain)
            abil_ref = self.consume(uni.ArchRef)
            if arch_chain:
                return uni.ArchRefChain(
                    archs=[*arch_chain.archs, abil_ref],
                    kid=[*arch_chain.kid, abil_ref],
                )
            return uni.ArchRefChain(
                archs=[abil_ref],
                kid=[abil_ref],
            )

        def arch_to_enum_chain(self, _: None) -> uni.ArchRefChain:
            """Grammar rule.

            arch_to_enum_chain: arch_or_ability_chain? enum_ref
            """
            arch_chain = self.match(uni.ArchRefChain)
            enum_ref = self.consume(uni.ArchRef)
            if arch_chain:
                return uni.ArchRefChain(
                    archs=[*arch_chain.archs, enum_ref],
                    kid=[*arch_chain.kid, enum_ref],
                )
            return uni.ArchRefChain(
                archs=[enum_ref],
                kid=[enum_ref],
            )

        def edge_ref_chain(self, _: None) -> uni.EdgeRefTrailer:
            """Grammar rule.

            LSQUARE (KW_NODE| KW_EDGE)? expression? (edge_op_ref (filter_compr | expression)?)+ RSQUARE
            """
            self.consume_token(Tok.LSQUARE)
            edges_only = bool(self.match_token(Tok.KW_EDGE))
            self.match_token(Tok.KW_NODE)
            valid_chain = []
            if expr := self.match(uni.Expr):
                valid_chain.append(expr)
            valid_chain.extend(self.match_many(uni.Expr))
            self.consume_token(Tok.RSQUARE)
            return uni.EdgeRefTrailer(
                chain=valid_chain,
                edges_only=edges_only,
                kid=self.cur_nodes,
            )

        def edge_op_ref(self, kid: list[uni.UniNode]) -> uni.EdgeOpRef:
            """Grammar rule.

            edge_op_ref: (edge_any | edge_from | edge_to)
            """
            return self.consume(uni.EdgeOpRef)

        def edge_to(self, _: None) -> uni.EdgeOpRef:
            """Grammar rule.

            edge_to: ARROW_R_P1 typed_filter_compare_list ARROW_R_P2
                   | ARROW_R
            """
            if self.match_token(Tok.ARROW_R):
                fcond = None
            else:
                if not self.match_token(Tok.ARROW_R_P1):
                    self.consume_token(Tok.DARROW_R_P1)
                    self.parse_ref.log_warning(
                        "Deprecated syntax, use '->:' instead of '-:'",
                    )
                fcond = self.consume(uni.FilterCompr)
                self.consume_token(Tok.ARROW_R_P2)
            return uni.EdgeOpRef(
                filter_cond=fcond, edge_dir=EdgeDir.OUT, kid=self.cur_nodes
            )

        def edge_from(self, _: None) -> uni.EdgeOpRef:
            """Grammar rule.

            edge_from: ARROW_L_P1 typed_filter_compare_list ARROW_L_P2
                     | ARROW_L
            """
            if self.match_token(Tok.ARROW_L):
                fcond = None
            else:
                self.consume_token(Tok.ARROW_L_P1)
                fcond = self.consume(uni.FilterCompr)
                if not self.match_token(Tok.ARROW_L_P2):
                    self.consume_token(Tok.DARROW_L_P2)
                    self.parse_ref.log_warning(
                        "Deprecated syntax, use ':<-' instead of ':-'",
                    )
            return uni.EdgeOpRef(
                filter_cond=fcond, edge_dir=EdgeDir.IN, kid=self.cur_nodes
            )

        def edge_any(self, _: None) -> uni.EdgeOpRef:
            """Grammar rule.

            edge_any: ARROW_L_P1 typed_filter_compare_list ARROW_R_P2
                    | ARROW_BI
            """
            if self.match_token(Tok.ARROW_BI):
                fcond = None
            else:
                self.consume_token(Tok.ARROW_L_P1)
                fcond = self.consume(uni.FilterCompr)
                self.consume_token(Tok.ARROW_R_P2)
            return uni.EdgeOpRef(
                filter_cond=fcond, edge_dir=EdgeDir.ANY, kid=self.cur_nodes
            )

        def connect_op(self, _: None) -> uni.ConnectOp:
            """Grammar rule.

            connect_op: connect_from | connect_to | connect_any
            """
            return self.consume(uni.ConnectOp)

        def disconnect_op(self, kid: list[uni.UniNode]) -> uni.DisconnectOp:
            """Grammar rule.

            disconnect_op: NOT edge_op_ref
            """
            if isinstance(kid[1], uni.EdgeOpRef):
                return uni.DisconnectOp(
                    edge_spec=kid[1],
                    kid=kid,
                )
            else:
                raise self.ice()

        def connect_to(self, _: None) -> uni.ConnectOp:
            """Grammar rule.

            connect_to: CARROW_R_P1 expression (COLON kw_expr_list)? CARROW_R_P2
                      | CARROW_R
            """
            conn_type: uni.Expr | None = None
            conn_assign_sub: uni.SubNodeList | None = None
            if (tok_rp1 := self.match_token(Tok.CARROW_R_P1)) or self.match_token(
                Tok.DCARROW_R_P1
            ):
                conn_type = self.consume(uni.Expr)
                conn_assign_sub = (
                    self.consume(uni.SubNodeList)
                    if self.match_token(Tok.COLON)
                    else None
                )
                self.consume_token(Tok.CARROW_R_P2)
                if not tok_rp1:
                    self.parse_ref.log_warning(
                        "Deprecated syntax, use '+>:' instead of '+:'",
                    )
            else:
                self.consume_token(Tok.CARROW_R)
            conn_assign = (
                uni.AssignCompr(assigns=conn_assign_sub, kid=[conn_assign_sub])
                if conn_assign_sub
                else None
            )
            if conn_assign:
                self.cur_nodes[3] = conn_assign
            return uni.ConnectOp(
                conn_type=conn_type,
                conn_assign=conn_assign,
                edge_dir=EdgeDir.OUT,
                kid=self.cur_nodes,
            )

        def connect_from(self, _: None) -> uni.ConnectOp:
            """Grammar rule.

            connect_from: CARROW_L_P1 expression (COLON kw_expr_list)? CARROW_L_P2
                        | CARROW_L
            """
            conn_type: uni.Expr | None = None
            conn_assign_sub: uni.SubNodeList | None = None
            if self.match_token(Tok.CARROW_L_P1):
                conn_type = self.consume(uni.Expr)
                conn_assign_sub = (
                    self.consume(uni.SubNodeList)
                    if self.match_token(Tok.COLON)
                    else None
                )
                if not self.match_token(Tok.CARROW_L_P2):
                    self.consume_token(Tok.DCARROW_L_P2)
                    self.parse_ref.log_warning(
                        "Deprecated syntax, use ':<+' instead of ':+'",
                    )
            else:
                self.consume_token(Tok.CARROW_L)
            conn_assign = (
                uni.AssignCompr(assigns=conn_assign_sub, kid=[conn_assign_sub])
                if conn_assign_sub
                else None
            )
            if conn_assign:
                self.cur_nodes[3] = conn_assign
            return uni.ConnectOp(
                conn_type=conn_type,
                conn_assign=conn_assign,
                edge_dir=EdgeDir.IN,
                kid=self.cur_nodes,
            )

        def connect_any(self, _: None) -> uni.ConnectOp:
            """Grammar rule.

            connect_any: CARROW_BI | CARROW_L_P1 expression (COLON kw_expr_list)? CARROW_R_P2
            """
            conn_type: uni.Expr | None = None
            conn_assign_sub: uni.SubNodeList | None = None
            if self.match_token(Tok.CARROW_L_P1):
                conn_type = self.consume(uni.Expr)
                conn_assign_sub = (
                    self.consume(uni.SubNodeList)
                    if self.match_token(Tok.COLON)
                    else None
                )
                self.consume_token(Tok.CARROW_R_P2)
            else:
                self.consume_token(Tok.CARROW_BI)
            conn_assign = (
                uni.AssignCompr(assigns=conn_assign_sub, kid=[conn_assign_sub])
                if conn_assign_sub
                else None
            )
            if conn_assign:
                self.cur_nodes[3] = conn_assign
            return uni.ConnectOp(
                conn_type=conn_type,
                conn_assign=conn_assign,
                edge_dir=EdgeDir.ANY,
                kid=self.cur_nodes,
            )

        def filter_compr(self, _: None) -> uni.FilterCompr:
            """Grammar rule.

            filter_compr: LPAREN NULL_OK filter_compare_list RPAREN
                        | LPAREN TYPE_OP NULL_OK typed_filter_compare_list RPAREN
            """
            kid = self.cur_nodes
            self.consume_token(Tok.LPAREN)
            if self.match_token(Tok.TYPE_OP):
                self.consume_token(Tok.NULL_OK)
                f_type = self.consume(uni.FilterCompr)
                f_type.add_kids_left(kid[:3])
                f_type.add_kids_right(kid[4:])
                self.consume_token(Tok.RPAREN)
                return f_type
            self.consume_token(Tok.NULL_OK)
            compares = self.consume(uni.SubNodeList)
            self.consume_token(Tok.RPAREN)
            return uni.FilterCompr(
                compares=compares,
                f_type=None,
                kid=self.cur_nodes,
            )

        def filter_compare_list(self, _: None) -> uni.SubNodeList[uni.CompareExpr]:
            """Grammar rule.

            filter_compare_list: (filter_compare_list COMMA)? filter_compare_item
            """
            if consume := self.match(uni.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                expr = self.consume(uni.CompareExpr)
                new_kid = [*consume.kid, comma, expr]
            else:
                expr = self.consume(uni.CompareExpr)
                new_kid = [expr]
            valid_kid = [i for i in new_kid if isinstance(i, uni.CompareExpr)]
            return uni.SubNodeList[uni.CompareExpr](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def typed_filter_compare_list(self, _: None) -> uni.FilterCompr:
            """Grammar rule.

            typed_filter_compare_list: expression (COLON filter_compare_list)?
            """
            compares: uni.SubNodeList | None = None
            expr = self.consume(uni.Expr)
            if self.match_token(Tok.COLON):
                compares = self.consume(uni.SubNodeList)
            return uni.FilterCompr(compares=compares, f_type=expr, kid=self.cur_nodes)

        def filter_compare_item(self, _: None) -> uni.CompareExpr:
            """Grammar rule.

            filter_compare_item: name_ref cmp_op expression
            """
            name_ref = self.consume(uni.Name)
            cmp_op = self.consume(uni.Token)
            expr = self.consume(uni.Expr)
            return uni.CompareExpr(
                left=name_ref, ops=[cmp_op], rights=[expr], kid=self.cur_nodes
            )

        def assign_compr(self, _: None) -> uni.AssignCompr:
            """Grammar rule.

            filter_compr: LPAREN EQ kw_expr_list RPAREN
            """
            self.consume_token(Tok.LPAREN)
            self.consume_token(Tok.EQ)
            assigns = self.consume(uni.SubNodeList)
            self.consume_token(Tok.RPAREN)
            return uni.AssignCompr(assigns=assigns, kid=self.cur_nodes)

        def match_stmt(self, _: None) -> uni.MatchStmt:
            """Grammar rule.

            match_stmt: KW_MATCH expr_list LBRACE match_case_block+ RBRACE
            """
            self.consume_token(Tok.KW_MATCH)
            target = self.consume(uni.Expr)
            self.consume_token(Tok.LBRACE)
            cases = [self.consume(uni.MatchCase)]
            while case := self.match(uni.MatchCase):
                cases.append(case)
            self.consume_token(Tok.RBRACE)
            return uni.MatchStmt(
                target=target,
                cases=cases,
                kid=self.cur_nodes,
            )

        def match_case_block(self, _: None) -> uni.MatchCase:
            """Grammar rule.

            match_case_block: KW_CASE pattern_seq (KW_IF expression)? COLON statement_list
            """
            guard: uni.Expr | None = None
            self.consume_token(Tok.KW_CASE)
            pattern = self.consume(uni.MatchPattern)
            if self.match_token(Tok.KW_IF):
                guard = self.consume(uni.Expr)
            self.consume_token(Tok.COLON)
            stmts = [self.consume(uni.CodeBlockStmt)]
            while stmt := self.match(uni.CodeBlockStmt):
                stmts.append(stmt)
            return uni.MatchCase(
                pattern=pattern,
                guard=guard,
                body=stmts,
                kid=self.cur_nodes,
            )

        def pattern_seq(self, _: None) -> uni.MatchPattern:
            """Grammar rule.

            pattern_seq: (or_pattern | as_pattern)
            """
            return self.consume(uni.MatchPattern)

        def or_pattern(self, _: None) -> uni.MatchPattern:
            """Grammar rule.

            or_pattern: (pattern BW_OR)* pattern
            """
            patterns: list = [self.consume(uni.MatchPattern)]
            while self.match_token(Tok.BW_OR):
                patterns.append(self.consume(uni.MatchPattern))
            if len(patterns) == 1:
                return patterns[0]
            return uni.MatchOr(
                patterns=patterns,
                kid=self.cur_nodes,
            )

        def as_pattern(self, _: None) -> uni.MatchPattern:
            """Grammar rule.

            as_pattern: pattern KW_AS NAME
            """
            pattern = self.consume(uni.MatchPattern)
            self.consume_token(Tok.KW_AS)
            name = self.consume(uni.NameAtom)
            return uni.MatchAs(
                pattern=pattern,
                name=name,
                kid=self.cur_nodes,
            )

        def pattern(self, kid: list[uni.UniNode]) -> uni.MatchPattern:
            """Grammar rule.

            pattern: literal_pattern
                | capture_pattern
                | sequence_pattern
                | mapping_pattern
                | class_pattern
            """
            return self.consume(uni.MatchPattern)

        def literal_pattern(self, _: None) -> uni.MatchPattern:
            """Grammar rule.

            literal_pattern: (INT | FLOAT | multistring)
            """
            value = self.consume(uni.Expr)
            return uni.MatchValue(
                value=value,
                kid=self.cur_nodes,
            )

        def singleton_pattern(self, _: None) -> uni.MatchPattern:
            """Grammar rule.

            singleton_pattern: (NULL | BOOL)
            """
            value = self.match(uni.Null) or self.consume(uni.Bool)
            return uni.MatchSingleton(
                value=value,
                kid=self.cur_nodes,
            )

        def capture_pattern(self, _: None) -> uni.MatchPattern:
            """Grammar rule.

            capture_pattern: NAME
            """
            name = self.consume(uni.Name)
            if name.sym_name == "_":
                return uni.MatchWild(
                    kid=self.cur_nodes,
                )
            return uni.MatchAs(
                name=name,
                pattern=None,
                kid=self.cur_nodes,
            )

        def sequence_pattern(self, _: None) -> uni.MatchPattern:
            """Grammar rule.

            sequence_pattern: LSQUARE list_inner_pattern (COMMA list_inner_pattern)* RSQUARE
                            | LPAREN list_inner_pattern (COMMA list_inner_pattern)* RPAREN
            """
            self.consume_token(Tok.LSQUARE) or self.consume_token(Tok.LPAREN)
            patterns = [self.consume(uni.MatchPattern)]
            while self.match_token(Tok.COMMA):
                patterns.append(self.consume(uni.MatchPattern))
            self.consume_token(Tok.RSQUARE) or self.consume_token(Tok.RPAREN)
            return uni.MatchSequence(
                values=patterns,
                kid=self.cur_nodes,
            )

        def mapping_pattern(self, _: None) -> uni.MatchMapping:
            """Grammar rule.

            mapping_pattern: LBRACE (dict_inner_pattern (COMMA dict_inner_pattern)*)? RBRACE
            """
            self.consume_token(Tok.LBRACE)
            patterns = [self.match(uni.MatchKVPair) or self.consume(uni.MatchStar)]
            while self.match_token(Tok.COMMA):
                patterns.append(
                    self.match(uni.MatchKVPair) or self.consume(uni.MatchStar)
                )
            self.consume_token(Tok.RBRACE)
            return uni.MatchMapping(
                values=patterns,
                kid=self.cur_nodes,
            )

        def list_inner_pattern(self, _: None) -> uni.MatchPattern:
            """Grammar rule.

            list_inner_pattern: (pattern_seq | STAR_MUL NAME)
            """
            if self.match_token(Tok.STAR_MUL):
                name = self.consume(uni.Name)
                return uni.MatchStar(
                    is_list=True,
                    name=name,
                    kid=self.cur_nodes,
                )
            return self.consume(uni.MatchPattern)

        def dict_inner_pattern(self, _: None) -> uni.MatchKVPair | uni.MatchStar:
            """Grammar rule.

            dict_inner_pattern: (pattern_seq COLON pattern_seq | STAR_POW NAME)
            """
            if self.match_token(Tok.STAR_POW):
                name = self.consume(uni.Name)
                return uni.MatchStar(
                    is_list=False,
                    name=name,
                    kid=self.cur_nodes,
                )
            pattern = self.consume(uni.MatchPattern)
            self.consume_token(Tok.COLON)
            value = self.consume(uni.MatchPattern)
            return uni.MatchKVPair(key=pattern, value=value, kid=self.cur_nodes)

        def class_pattern(self, _: None) -> uni.MatchArch:
            """Grammar rule.

            class_pattern: NAME (DOT NAME)* LPAREN kw_pattern_list? RPAREN
                        | NAME (DOT NAME)* LPAREN pattern_list (COMMA kw_pattern_list)? RPAREN
            """
            cur_element = self.consume(uni.NameAtom)
            trailer: uni.AtomTrailer | None = None
            while dot := self.match_token(Tok.DOT):
                target = trailer if trailer else cur_element
                right = self.consume(uni.Expr)
                trailer = uni.AtomTrailer(
                    target=target,
                    right=right,
                    is_attr=True,
                    is_null_ok=False,
                    kid=[target, dot, right],
                )
            name = trailer if trailer else cur_element
            if not isinstance(name, (uni.NameAtom, uni.AtomTrailer)):
                raise TypeError(
                    f"Expected name to be either NameAtom or AtomTrailer, got {type(name)}"
                )
            lparen = self.consume_token(Tok.LPAREN)
            first = self.match(uni.SubNodeList)
            second = (
                self.consume(uni.SubNodeList)
                if (comma := self.match_token(Tok.COMMA))
                else None
            )
            rparen = self.consume_token(Tok.RPAREN)
            arg = (
                first
                if (first and isinstance(first.items[0], uni.MatchPattern))
                else None
            )
            kw = (
                second
                if (second and isinstance(second.items[0], uni.MatchKVPair))
                else (
                    first
                    if (first and isinstance(first.items[0], uni.MatchKVPair))
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
            return uni.MatchArch(
                name=name,
                arg_patterns=arg,
                kw_patterns=kw,
                kid=kid_nodes,
            )

        def pattern_list(self, _: None) -> uni.SubNodeList[uni.MatchPattern]:
            """Grammar rule.

            pattern_list: (pattern_list COMMA)? pattern_seq
            """
            if consume := self.match(uni.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                pattern = self.consume(uni.MatchPattern)
            else:
                pattern = self.consume(uni.MatchPattern)
            new_kid = [*consume.kid, comma, pattern] if consume else [pattern]
            valid_kid = [i for i in new_kid if isinstance(i, uni.MatchPattern)]
            return uni.SubNodeList[uni.MatchPattern](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def kw_pattern_list(self, _: None) -> uni.SubNodeList[uni.MatchKVPair]:
            """Grammar rule.

            kw_pattern_list: (kw_pattern_list COMMA)? named_ref EQ pattern_seq
            """
            new_kid: list = []
            if consume := self.match(uni.SubNodeList):
                comma = self.consume_token(Tok.COMMA)
                new_kid.extend([*consume.kid, comma])
            name = self.consume(uni.NameAtom)
            eq = self.consume_token(Tok.EQ)
            value = self.consume(uni.MatchPattern)
            new_kid.extend(
                [uni.MatchKVPair(key=name, value=value, kid=[name, eq, value])]
            )
            valid_kid = [i for i in new_kid if isinstance(i, uni.MatchKVPair)]
            return uni.SubNodeList[uni.MatchKVPair](
                items=valid_kid,
                delim=Tok.COMMA,
                kid=new_kid,
            )

        def __default_token__(self, token: jl.Token) -> uni.Token:
            """Token handler."""
            ret_type = uni.Token
            if token.type in [Tok.NAME, Tok.KWESC_NAME]:
                ret_type = uni.Name
            if token.type in [
                Tok.KW_INIT,
                Tok.KW_POST_INIT,
                Tok.KW_ROOT,
                Tok.KW_SUPER,
                Tok.KW_SELF,
                Tok.KW_HERE,
            ]:
                ret_type = uni.Name
            elif token.type == Tok.SEMI:
                ret_type = uni.Semi
            elif token.type == Tok.NULL:
                ret_type = uni.Null
            elif token.type == Tok.ELLIPSIS:
                ret_type = uni.Ellipsis
            elif token.type == Tok.FLOAT:
                ret_type = uni.Float
            elif token.type in [Tok.INT, Tok.INT, Tok.HEX, Tok.BIN, Tok.OCT]:
                ret_type = uni.Int
            elif token.type in [
                Tok.STRING,
                Tok.FSTR_BESC,
                Tok.FSTR_PIECE,
                Tok.FSTR_SQ_PIECE,
            ]:
                ret_type = uni.String
                if token.type == Tok.FSTR_BESC:
                    token.value = token.value[1:]
            elif token.type == Tok.BOOL:
                ret_type = uni.Bool
            elif token.type == Tok.PYNLINE and isinstance(token.value, str):
                token.value = token.value.replace("::py::", "")
            ret = ret_type(
                orig_src=self.parse_ref.ir_in,
                name=token.type,
                value=token.value[2:] if token.type == Tok.KWESC_NAME else token.value,
                line=token.line if token.line is not None else 0,
                end_line=token.end_line if token.end_line is not None else 0,
                col_start=token.column if token.column is not None else 0,
                col_end=token.end_column if token.end_column is not None else 0,
                pos_start=token.start_pos if token.start_pos is not None else 0,
                pos_end=token.end_pos if token.end_pos is not None else 0,
            )
            if isinstance(ret, uni.Name):
                if token.type == Tok.KWESC_NAME:
                    ret.is_kwesc = True
                if ret.value in keyword.kwlist:
                    err = jl.UnexpectedInput(f"Python keyword {ret.value} used as name")
                    err.line = ret.loc.first_line
                    err.column = ret.loc.col_start
                    raise err
            self.terminals.append(ret)
            return ret

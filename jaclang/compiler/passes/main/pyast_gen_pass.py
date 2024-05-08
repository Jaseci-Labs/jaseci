"""Jac Blue pass for Jaseci Ast.

At the end of this pass a meta['py_code'] is present with pure python code
in each node. Module nodes contain the entire module code.
"""

import ast as ast3
import textwrap
from typing import Optional, Sequence, TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import Constants as Con, EdgeDir, Tokens as Tok
from jaclang.compiler.passes import Pass
from jaclang.core.utils import extract_params, extract_type, get_sem_scope

T = TypeVar("T", bound=ast3.AST)


class PyastGenPass(Pass):
    """Jac blue transpilation to python pass."""

    cout = 1

    @staticmethod
    def node_compilable_test(node: ast3.AST) -> None:
        """Convert any AST node to a compilable module node."""
        if isinstance(node, ast3.Module):
            pass
        elif isinstance(node, (ast3.Expr, ast3.stmt)):
            node = ast3.Module(body=[node], type_ignores=[])
        elif isinstance(node, list) and all(isinstance(n, ast3.stmt) for n in node):
            node = ast3.Module(body=node, type_ignores=[])
        else:
            node = ast3.Module(body=[], type_ignores=[])
        try:
            compile(node, "<ast>", "exec")
        except TypeError as e:
            print(ast3.dump(node, indent=2))
            raise e
        except Exception:
            pass

    def before_pass(self) -> None:
        """Initialize pass."""
        self.debuginfo: dict[str, list[str]] = {"jac_mods": []}
        self.already_added: list[str] = []
        self.preamble: list[ast3.AST] = [
            self.sync(
                ast3.ImportFrom(
                    module="__future__",
                    names=[self.sync(ast3.alias(name="annotations", asname=None))],
                    level=0,
                ),
                jac_node=self.ir,
            )
        ]

    def exit_node(self, node: ast.AstNode) -> None:
        """Exit node."""
        super().exit_node(node)
        # for i in node.gen.py_ast:  # Internal validation
        #     self.node_compilable_test(i)

        # TODO: USE THIS TO SYNC
        #     if isinstance(i, ast3.AST):
        #         i.jac_link = node

    def needs_jac_import(self) -> None:
        """Check if import is needed."""
        if "jimport" in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="jaclang",
                    names=[
                        self.sync(
                            ast3.alias(name="jac_import", asname="__jac_import__")
                        )
                    ],
                    level=0,
                ),
                jac_node=self.ir,
            )
        )
        self.already_added.append("jimport")

    def needs_typing(self) -> None:
        """Check if enum is needed."""
        if "typing" in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.Import(
                    names=[
                        self.sync(
                            ast3.alias(name="typing", asname="_jac_typ"),
                            jac_node=self.ir,
                        ),
                    ]
                ),
                jac_node=self.ir,
            )
        )
        self.already_added.append("typing")

    def needs_enum(self) -> None:
        """Check if enum is needed."""
        if "enum" in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="enum",
                    names=[
                        self.sync(ast3.alias(name="Enum", asname="__jac_Enum__")),
                        self.sync(ast3.alias(name="auto", asname="__jac_auto__")),
                    ],
                    level=0,
                ),
                jac_node=self.ir,
            )
        )
        self.already_added.append("enum")

    def needs_jac_feature(self) -> None:
        """Check if enum is needed."""
        if "jac_feature" in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="jaclang.plugin.feature",
                    names=[
                        self.sync(
                            ast3.alias(name="JacFeature", asname=Con.JAC_FEATURE.value)
                        ),
                    ],
                    level=0,
                ),
                jac_node=self.ir,
            )
        )
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="jaclang.plugin.builtin",
                    names=[self.sync(ast3.alias(name="*", asname=None))],
                    level=0,
                ),
                jac_node=self.ir,
            )
        )
        self.already_added.append("jac_feature")

    def needs_dataclass(self) -> None:
        """Check if enum is needed."""
        if "dataclass" in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="dataclasses",
                    names=[
                        self.sync(
                            ast3.alias(name="dataclass", asname="__jac_dataclass__")
                        ),
                    ],
                    level=0,
                ),
                jac_node=self.ir,
            )
        )
        self.already_added.append("dataclass")

    def needs_dataclass_field(self) -> None:
        """Check if enum is needed."""
        if "dataclass_field" in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="dataclasses",
                    names=[
                        self.sync(ast3.alias(name="field", asname="__jac_field__")),
                    ],
                    level=0,
                ),
                jac_node=self.ir,
            )
        )
        self.already_added.append("dataclass_field")

    def flatten(self, body: list[T | list[T] | None]) -> list[T]:
        """Flatten ast list."""
        new_body = []
        for i in body:
            if isinstance(i, list):
                new_body += i
            elif i is not None:
                new_body.append(i) if i else None
        return new_body

    def sync(
        self, py_node: T, jac_node: Optional[ast.AstNode] = None, deep: bool = False
    ) -> T:
        """Sync ast locations."""
        if not jac_node:
            jac_node = self.cur_node
        for i in ast3.walk(py_node) if deep else [py_node]:
            if isinstance(i, ast3.AST):
                i.lineno = jac_node.loc.first_line
                i.col_offset = jac_node.loc.col_start
                i.end_lineno = (
                    jac_node.loc.last_line
                    if jac_node.loc.last_line
                    else jac_node.loc.first_line
                )
                i.end_col_offset = (
                    jac_node.loc.col_end
                    if jac_node.loc.col_end
                    else jac_node.loc.col_start
                )
                i.jac_link: list[ast3.AST] = [jac_node]  # type: ignore
        return py_node

    def link_jac_py_nodes(
        self, jac_node: ast.AstNode, py_nodes: list[ast3.AST]
    ) -> None:
        """Link jac name ast to py ast nodes."""
        jac_node.gen.py_ast = py_nodes
        for i in py_nodes:
            if isinstance(i.jac_link, list):  # type: ignore
                i.jac_link.append(jac_node)  # type: ignore

    def pyinline_sync(
        self,
        py_nodes: list[ast3.AST],
    ) -> list[ast3.AST]:
        """Sync ast locations."""
        for node in py_nodes:
            for i in ast3.walk(node):
                if isinstance(i, ast3.AST):
                    if hasattr(i, "lineno") and i.lineno is not None:
                        i.lineno += self.cur_node.loc.first_line
                    if hasattr(i, "end_lineno") and i.end_lineno is not None:
                        i.end_lineno += self.cur_node.loc.first_line
                    i.jac_link: ast3.AST = [self.cur_node]  # type: ignore
        return py_nodes

    def resolve_stmt_block(
        self,
        node: (
            ast.SubNodeList[ast.CodeBlockStmt]
            | ast.SubNodeList[ast.ArchBlockStmt]
            | ast.SubNodeList[ast.EnumBlockStmt]
            | None
        ),
        doc: Optional[ast.String] = None,
    ) -> list[ast3.AST]:
        """Unwind codeblock."""
        valid_stmts = (
            [i for i in node.items if not isinstance(i, ast.Semi)] if node else []
        )
        ret: list[ast3.AST] = (
            [self.sync(ast3.Pass(), node)]
            if isinstance(node, ast.SubNodeList) and not valid_stmts
            else (
                self.flatten(
                    [
                        x.gen.py_ast
                        for x in valid_stmts
                        if not isinstance(x, ast.AstImplOnlyNode)
                    ]
                )
                if node and isinstance(node.gen.py_ast, list)
                else []
            )
        )
        if doc:
            ret = [self.sync(ast3.Expr(value=doc.gen.py_ast[0]), jac_node=doc), *ret]
        return ret

    def sync_many(self, py_nodes: list[T], jac_node: ast.AstNode) -> list[T]:
        """Sync ast locations."""
        for py_node in py_nodes:
            self.sync(py_node, jac_node)
        return py_nodes

    def list_to_attrib(
        self, attribute_list: list[str], sync_node_list: Sequence[ast.AstNode]
    ) -> ast3.AST:
        """Convert list to attribute."""
        attr_node: ast3.Name | ast3.Attribute = self.sync(
            ast3.Name(id=attribute_list[0], ctx=ast3.Load()), sync_node_list[0]
        )
        for i in range(len(attribute_list)):
            if i == 0:
                continue
            attr_node = self.sync(
                ast3.Attribute(
                    value=attr_node, attr=attribute_list[i], ctx=ast3.Load()
                ),
                sync_node_list[i],
            )
        return attr_node

    def exit_sub_tag(self, node: ast.SubTag[ast.T]) -> None:
        """Sub objects.

        tag: T,
        """
        node.gen.py_ast = node.tag.gen.py_ast

    def exit_sub_node_list(self, node: ast.SubNodeList[ast.T]) -> None:
        """Sub objects.

        items: Sequence[T],
        """
        node.gen.py_ast = self.flatten([i.gen.py_ast for i in node.items])

    def exit_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        source: JacSource,
        doc: Optional[String],
        body: Sequence[ElementStmt],
        is_imported: bool,
        """
        clean_body = [i for i in node.body if not isinstance(i, ast.AstImplOnlyNode)]
        pre_body = [*node.impl_mod.body, *clean_body] if node.impl_mod else clean_body
        pre_body = [*pre_body, *node.test_mod.body] if node.test_mod else pre_body
        body = (
            [
                self.sync(ast3.Expr(value=node.doc.gen.py_ast[0]), jac_node=node.doc),
                *self.preamble,
                *[x.gen.py_ast for x in pre_body],
            ]
            if node.doc
            else [*self.preamble, *[x.gen.py_ast for x in pre_body]]
        )
        new_body = []
        for i in body:
            if isinstance(i, list):
                new_body += i
            else:
                new_body.append(i) if i else None
        node.gen.py_ast = [
            self.sync(
                ast3.Module(
                    body=new_body,
                    type_ignores=[],
                )
            )
        ]
        node.gen.py = ast3.unparse(node.gen.py_ast[0])

    def exit_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        access: Optional[SubTag[Token]],
        assignments: SubNodeList[Assignment],
        is_frozen: bool,
        doc: Optional[String],
        """
        if node.doc:
            doc = self.sync(ast3.Expr(value=node.doc.gen.py_ast[0]), jac_node=node.doc)
            if isinstance(doc, ast3.AST) and isinstance(
                node.assignments.gen.py_ast, list
            ):
                node.gen.py_ast = [doc] + node.assignments.gen.py_ast
            else:
                raise self.ice()
        else:
            node.gen.py_ast = node.assignments.gen.py_ast

    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Name | Token,
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[String],
        """
        self.needs_jac_feature()
        test_name = node.name.sym_name
        func = self.sync(
            ast3.FunctionDef(
                name=test_name,
                args=self.sync(
                    ast3.arguments(
                        posonlyargs=[],
                        args=[self.sync(ast3.arg(arg="check", annotation=None))],
                        kwonlyargs=[],
                        vararg=None,
                        kwargs=None,
                        kw_defaults=[],
                        defaults=[],
                    )
                ),
                body=self.resolve_stmt_block(node.body, doc=node.doc),
                decorator_list=[
                    self.sync(
                        ast3.Attribute(
                            value=self.sync(
                                ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                            ),
                            attr="create_test",
                            ctx=ast3.Load(),
                        )
                    )
                ],
                returns=self.sync(ast3.Constant(value=None)),
                type_comment=None,
                type_params=[],
            ),
        )
        node.gen.py_ast = [func]

    def exit_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        name: Optional[SubTag[Name]],
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[String],
        """
        if node.doc:
            doc = self.sync(ast3.Expr(value=node.doc.gen.py_ast[0]), jac_node=node.doc)
            if isinstance(node.body.gen.py_ast, list):
                node.gen.py_ast = [doc] + node.body.gen.py_ast
            else:
                raise self.ice()
        else:
            node.gen.py_ast = node.body.gen.py_ast
        if node.name:
            node.gen.py_ast = [
                self.sync(
                    ast3.If(
                        test=self.sync(
                            ast3.Compare(
                                left=self.sync(
                                    ast3.Name(id="__name__", ctx=ast3.Load())
                                ),
                                ops=[self.sync(ast3.Eq())],
                                comparators=[
                                    self.sync(
                                        ast3.Constant(value=node.name.tag.sym_name)
                                    )
                                ],
                            )
                        ),
                        body=node.gen.py_ast,
                        orelse=[],
                    )
                )
            ]

    def exit_py_inline_code(self, node: ast.PyInlineCode) -> None:
        """Sub objects.

        code: Token,
        doc: Optional[String],
        """
        if node.doc:
            doc = self.sync(ast3.Expr(value=node.doc.gen.py_ast[0]), jac_node=node.doc)
            if isinstance(doc, ast3.AST):
                node.gen.py_ast = self.pyinline_sync(
                    [doc, *ast3.parse(node.code.value).body]
                )

            else:
                raise self.ice()
        else:
            node.gen.py_ast = self.pyinline_sync(
                [*ast3.parse(textwrap.dedent(node.code.value)).body]
            )

    def exit_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: SubTag[Name],
        paths: list[ModulePath],
        alias: Optional[Name],
        items: Optional[SubNodeList[ModuleItem]],
        is_absorb: bool,
        doc: Optional[String],
        sub_module: Optional[Module],
        """
        py_nodes: list[ast3.AST] = []

        if node.doc:
            py_nodes.append(
                self.sync(ast3.Expr(value=node.doc.gen.py_ast[0]), jac_node=node.doc)
            )
        path_alias: dict[str, Optional[str]] = (
            {node.from_loc.path_str: None} if node.from_loc else {}
        )
        imp_from = {}
        if node.items:
            for item in node.items.items:
                if isinstance(item, ast.ModuleItem):
                    imp_from[item.name.sym_name] = (
                        item.alias.sym_name if item.alias else False
                    )
                elif isinstance(item, ast.ModulePath):
                    path_alias[item.path_str] = (
                        item.alias.sym_name if item.alias else None
                    )

        keys = []
        values = []
        for k in imp_from.keys():
            keys.append(self.sync(ast3.Constant(value=k)))
        for v in imp_from.values():
            values.append(self.sync(ast3.Constant(value=v)))

        self.needs_jac_import()
        for p, a in path_alias.items():
            py_nodes.append(
                self.sync(
                    ast3.Expr(
                        value=self.sync(
                            ast3.Call(
                                func=self.sync(
                                    ast3.Name(id="__jac_import__", ctx=ast3.Load())
                                ),
                                args=[],
                                keywords=[
                                    self.sync(
                                        ast3.keyword(
                                            arg="target",
                                            value=self.sync(
                                                ast3.Constant(value=p),
                                            ),
                                        )
                                    ),
                                    self.sync(
                                        ast3.keyword(
                                            arg="base_path",
                                            value=self.sync(
                                                ast3.Name(
                                                    id="__file__", ctx=ast3.Load()
                                                )
                                            ),
                                        )
                                    ),
                                    self.sync(
                                        ast3.keyword(
                                            arg="mod_bundle",
                                            value=self.sync(
                                                ast3.Name(
                                                    id="__jac_mod_bundle__",
                                                    ctx=ast3.Load(),
                                                )
                                            ),
                                        )
                                    ),
                                    self.sync(
                                        ast3.keyword(
                                            arg="lng",
                                            value=self.sync(
                                                ast3.Constant(
                                                    value=node.hint.tag.value
                                                ),
                                                node.hint,
                                            ),
                                        )
                                    ),
                                    self.sync(
                                        ast3.keyword(
                                            arg="absorb",
                                            value=self.sync(
                                                ast3.Constant(value=node.is_absorb),
                                            ),
                                        )
                                    ),
                                    self.sync(
                                        ast3.keyword(
                                            arg="mdl_alias",
                                            value=self.sync(
                                                ast3.Constant(value=a),
                                            ),
                                        )
                                    ),
                                    self.sync(
                                        ast3.keyword(
                                            arg="items",
                                            value=self.sync(
                                                ast3.Dict(keys=keys, values=values),
                                            ),
                                        )
                                    ),
                                ],
                            )
                        )
                    ),
                )
            )
        if node.is_absorb:
            source = node.items.items[0]
            if not isinstance(source, ast.ModulePath):
                raise self.ice()
            py_nodes.append(
                self.sync(
                    py_node=ast3.ImportFrom(
                        module=(source.path_str.lstrip(".") if source else None),
                        names=[self.sync(ast3.alias(name="*"), node)],
                        level=0,
                    ),
                    jac_node=node,
                )
            )
            if node.items:
                self.warning(
                    "Includes import * in target module into current namespace."
                )
        if not node.from_loc:
            py_nodes.append(self.sync(ast3.Import(names=node.items.gen.py_ast)))
        else:
            py_nodes.append(
                self.sync(
                    ast3.ImportFrom(
                        module=(
                            node.from_loc.path_str.lstrip(".")
                            if node.from_loc
                            else None
                        ),
                        names=node.items.gen.py_ast,
                        level=0,
                    )
                )
            )
        node.gen.py_ast = py_nodes

    def exit_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: Sequence[Token],
        alias: Optional[Name],
        path_str: str,
        """
        node.gen.py_ast = [
            self.sync(
                ast3.alias(
                    name=f"{node.path_str}",
                    asname=node.alias.sym_name if node.alias else None,
                )
            )
        ]
        if node.alias:
            self.link_jac_py_nodes(jac_node=node.alias, py_nodes=node.gen.py_ast)

    def exit_module_item(self, node: ast.ModuleItem) -> None:
        """Sub objects.

        name: Name,
        alias: Optional[Name],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.alias(
                    name=f"{node.name.sym_name}",
                    asname=node.alias.sym_name if node.alias else None,
                )
            )
        ]

    def exit_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[AtomType]],
        body: Optional[SubNodeList[ArchBlockStmt] | ArchDef],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        self.needs_jac_feature()
        self.needs_dataclass()
        body = self.resolve_stmt_block(
            node.body.body if isinstance(node.body, ast.ArchDef) else node.body,
            doc=node.doc,
        )
        decorators = (
            node.decorators.gen.py_ast
            if isinstance(node.decorators, ast.SubNodeList)
            else []
        )
        ds_on_entry, ds_on_exit = self.collect_events(node)
        if node.arch_type.name != Tok.KW_CLASS:
            decorators.append(
                self.sync(
                    ast3.Call(
                        func=self.sync(
                            ast3.Attribute(
                                value=self.sync(
                                    ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                                ),
                                attr=f"make_{node.arch_type.value}",
                                ctx=ast3.Load(),
                            )
                        ),
                        args=[],
                        keywords=[
                            self.sync(
                                ast3.keyword(
                                    arg="on_entry",
                                    value=self.sync(
                                        ast3.List(elts=ds_on_entry, ctx=ast3.Load())
                                    ),
                                )
                            ),
                            self.sync(
                                ast3.keyword(
                                    arg="on_exit",
                                    value=self.sync(
                                        ast3.List(elts=ds_on_exit, ctx=ast3.Load())
                                    ),
                                )
                            ),
                        ],
                    )
                )
            )
        decorators.append(
            self.sync(
                ast3.Call(
                    func=self.sync(ast3.Name(id="__jac_dataclass__", ctx=ast3.Load())),
                    args=[],
                    keywords=[
                        self.sync(
                            ast3.keyword(
                                arg="eq",
                                value=self.sync(
                                    ast3.Constant(value=False),
                                ),
                            )
                        )
                    ],
                )
            )
        )
        base_classes = node.base_classes.gen.py_ast if node.base_classes else []
        if node.is_abstract:
            self.needs_jac_feature()
            base_classes.append(
                self.sync(
                    ast3.Attribute(
                        value=self.sync(
                            ast3.Attribute(
                                value=self.sync(
                                    ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                                ),
                                attr="abc",
                                ctx=ast3.Load(),
                            )
                        ),
                        attr="ABC",
                        ctx=ast3.Load(),
                    )
                )
            )
        node.gen.py_ast = [
            self.sync(
                ast3.ClassDef(
                    name=node.name.sym_name,
                    bases=base_classes,
                    keywords=[],
                    body=body,
                    decorator_list=decorators,
                    type_params=[],
                )
            )
        ]
        self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)
        if isinstance(node.body, ast.ArchDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def collect_events(
        self, node: ast.Architype
    ) -> tuple[list[ast3.AST], list[ast3.AST]]:
        """Collect events."""
        ds_on_entry: list[ast3.AST] = []
        ds_on_exit: list[ast3.AST] = []
        for i in (
            node.body.body.items
            if isinstance(node.body, ast.ArchDef)
            else node.body.items if node.body else []
        ):
            if isinstance(i, ast.Ability) and isinstance(
                i.signature, ast.EventSignature
            ):
                func_spec = self.sync(
                    ast3.Call(
                        func=self.sync(
                            ast3.Attribute(
                                value=self.sync(
                                    ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                                ),
                                attr="DSFunc",
                                ctx=ast3.Load(),
                            )
                        ),
                        args=[
                            self.sync(ast3.Constant(value=i.sym_name)),
                            (
                                i.signature.arch_tag_info.gen.py_ast[0]
                                if i.signature.arch_tag_info
                                else self.sync(ast3.Constant(value=None))
                            ),
                        ],
                        keywords=[],
                    )
                )
                (
                    ds_on_entry.append(func_spec)
                    if i.signature.event.name == Tok.KW_ENTRY
                    else ds_on_exit.append(func_spec)
                )
        return ds_on_entry, ds_on_exit

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        body: SubNodeList[ArchBlockStmt],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        for i in node.target.archs:
            if i.sym_link:
                self.link_jac_py_nodes(jac_node=i, py_nodes=i.sym_link.decl.gen.py_ast)
                self.link_jac_py_nodes(
                    jac_node=i.name_ref, py_nodes=i.sym_link.decl.gen.py_ast
                )

    def exit_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        access: Optional[SubTag[Token]],
        base_classes: Optional[Optional[SubNodeList[AtomType]]],
        body: Optional[SubNodeList[EnumBlockStmt] | EnumDef],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        self.needs_enum()
        body = self.resolve_stmt_block(
            node.body.body if isinstance(node.body, ast.EnumDef) else node.body,
            doc=node.doc,
        )
        decorators = (
            node.decorators.gen.py_ast
            if isinstance(node.decorators, ast.SubNodeList)
            else []
        )
        base_classes = node.base_classes.gen.py_ast if node.base_classes else []
        if isinstance(base_classes, list):
            base_classes.append(
                self.sync(ast3.Name(id="__jac_Enum__", ctx=ast3.Load()))
            )
        else:
            raise self.ice()
        node.gen.py_ast = [
            self.sync(
                ast3.ClassDef(
                    name=node.name.sym_name,
                    bases=base_classes,
                    keywords=[],
                    body=body,
                    decorator_list=decorators,
                    type_params=[],
                )
            )
        ]
        if isinstance(node.body, ast.EnumDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        body: SubNodeList[EnumBlockStmt],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        for i in node.target.archs:
            if i.sym_link:
                self.link_jac_py_nodes(jac_node=i, py_nodes=i.sym_link.decl.gen.py_ast)
                self.link_jac_py_nodes(
                    jac_node=i.name_ref, py_nodes=i.sym_link.decl.gen.py_ast
                )

    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: NameType,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        is_abstract: bool,
        access: Optional[SubTag[Token]],
        signature: Optional[FuncSignature | ExprType | EventSignature],
        body: Optional[SubNodeList[CodeBlockStmt] | AbilityDef | FuncCall],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        func_type = ast3.AsyncFunctionDef if node.is_async else ast3.FunctionDef
        body = (
            self.gen_llm_body(node)
            if isinstance(node.body, ast.FuncCall)
            else (
                [
                    self.sync(
                        ast3.Expr(value=node.doc.gen.py_ast[0]), jac_node=node.doc
                    ),
                    self.sync(ast3.Pass(), node.body),
                ]
                if node.doc and node.is_abstract
                else (
                    [self.sync(ast3.Pass(), node.body)]
                    if node.is_abstract
                    else self.resolve_stmt_block(
                        (
                            node.body.body
                            if isinstance(node.body, ast.AbilityDef)
                            else node.body
                        ),
                        doc=node.doc,
                    )
                )
            )
        )
        if node.is_abstract and node.body:
            self.error(
                f"Abstract ability {node.sym_name} should not have a body.",
                node,
            )
        decorator_list = node.decorators.gen.py_ast if node.decorators else []
        if node.is_abstract:
            self.needs_jac_feature()
            decorator_list.append(
                self.sync(
                    ast3.Attribute(
                        value=self.sync(
                            ast3.Attribute(
                                value=self.sync(
                                    ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                                ),
                                attr="abc",
                                ctx=ast3.Load(),
                            )
                        ),
                        attr="abstractmethod",
                        ctx=ast3.Load(),
                    )
                )
            )
        if node.is_override:
            self.needs_typing()
            decorator_list.append(
                self.sync(
                    ast3.Attribute(
                        value=self.sync(ast3.Name(id="_jac_typ", ctx=ast3.Load())),
                        attr="override",
                        ctx=ast3.Load(),
                    )
                )
            )
        if node.is_static:
            decorator_list.insert(
                0, self.sync(ast3.Name(id="staticmethod", ctx=ast3.Load()))
            )
        if not body and not isinstance(node.body, ast.FuncCall):
            self.error("Ability has no body. Perhaps an impl must be imported.", node)
            body = [self.sync(ast3.Pass(), node)]

        node.gen.py_ast = [
            self.sync(
                func_type(
                    name=node.name_ref.sym_name,
                    args=node.signature.gen.py_ast[0] if node.signature else [],
                    body=body,
                    decorator_list=decorator_list,
                    returns=(
                        node.signature.return_type.gen.py_ast[0]
                        if node.signature and node.signature.return_type
                        else self.sync(ast3.Constant(value=None))
                    ),
                    type_params=[],
                )
            )
        ]
        self.link_jac_py_nodes(jac_node=node.name_ref, py_nodes=node.gen.py_ast)
        if isinstance(node.body, ast.AbilityDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def gen_llm_body(self, node: ast.Ability) -> list[ast3.AST]:
        """Generate llm body."""
        self.needs_jac_feature()
        if isinstance(node.body, ast.FuncCall):
            model = node.body.target.gen.py_ast[0]
            extracted_type = (
                "".join(extract_type(node.signature.return_type))
                if isinstance(node.signature, ast.FuncSignature)
                and node.signature.return_type
                else None
            )
            scope = self.sync(ast3.Constant(value=str(get_sem_scope(node))))
            model_params, include_info, exclude_info = extract_params(node.body)
            inputs = (
                [
                    self.sync(
                        ast3.Tuple(
                            elts=[
                                (
                                    self.sync(
                                        ast3.Constant(
                                            value=(
                                                param.semstr.lit_value
                                                if param.semstr
                                                else None
                                            )
                                        )
                                    )
                                ),
                                (
                                    param.type_tag.tag.gen.py_ast[0]
                                    if param.type_tag
                                    else None
                                ),
                                self.sync(ast3.Constant(value=param.name.value)),
                                self.sync(
                                    ast3.Name(
                                        id=param.name.value,
                                        ctx=ast3.Load(),
                                    )
                                ),
                            ],
                            ctx=ast3.Load(),
                        )
                    )
                    for param in node.signature.params.items
                ]
                if isinstance(node.signature, ast.FuncSignature)
                and node.signature.params
                else []
            )
            outputs = (
                [
                    (
                        self.sync(
                            ast3.Constant(
                                value=(
                                    node.signature.semstr.lit_value
                                    if node.signature.semstr
                                    else None
                                )
                            )
                        )
                    ),
                    (self.sync(ast3.Constant(value=(extracted_type)))),
                ]
                if isinstance(node.signature, ast.FuncSignature)
                else []
            )
            action = node.semstr.gen.py_ast[0] if node.semstr else None
            return [
                self.sync(
                    ast3.Assign(
                        targets=[self.sync(ast3.Name(id="output", ctx=ast3.Store()))],
                        value=self.by_llm_call(
                            model,
                            model_params,
                            scope,
                            inputs,
                            outputs,
                            action,
                            include_info,
                            exclude_info,
                        ),
                    )
                ),
                self.sync(
                    ast3.Try(
                        body=[
                            self.sync(
                                ast3.Return(
                                    value=self.sync(
                                        ast3.Call(
                                            func=self.sync(
                                                ast3.Name(id="eval", ctx=ast3.Load())
                                            ),
                                            args=[
                                                self.sync(
                                                    ast3.Name(
                                                        id="output", ctx=ast3.Load()
                                                    )
                                                )
                                            ],
                                            keywords=[],
                                        )
                                    )
                                )
                            )
                        ],
                        handlers=[
                            self.sync(
                                ast3.ExceptHandler(
                                    type=None,
                                    name=None,
                                    body=[
                                        self.sync(
                                            ast3.Return(
                                                value=self.sync(
                                                    ast3.Name(
                                                        id="output", ctx=ast3.Load()
                                                    )
                                                )
                                            )
                                        )
                                    ],
                                )
                            )
                        ],
                        orelse=[],
                        finalbody=[],
                    )
                ),
            ]
        else:
            return []

    def by_llm_call(
        self,
        model: ast3.AST,
        model_params: dict[str, ast.Expr],
        scope: ast3.AST,
        inputs: Sequence[Optional[ast3.AST]],
        outputs: Sequence[Optional[ast3.AST]] | ast3.Call,
        action: Optional[ast3.AST],
        include_info: list[tuple[str, ast3.AST]],
        exclude_info: list[tuple[str, ast3.AST]],
    ) -> ast3.Call:
        """Return the LLM Call, e.g. _Jac.with_llm()."""
        return self.sync(
            ast3.Call(
                func=self.sync(
                    ast3.Attribute(
                        value=self.sync(
                            ast3.Name(
                                id=Con.JAC_FEATURE.value,
                                ctx=ast3.Load(),
                            )
                        ),
                        attr="with_llm",
                        ctx=ast3.Load(),
                    )
                ),
                args=[],
                keywords=[
                    self.sync(
                        ast3.keyword(
                            arg="file_loc",
                            value=self.sync(ast3.Name(id="__file__", ctx=ast3.Load())),
                        )
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="model",
                            value=model,
                        )
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="model_params",
                            value=self.sync(
                                ast3.Dict(
                                    keys=[
                                        self.sync(ast3.Constant(value=key))
                                        for key in model_params.keys()
                                    ],
                                    values=[
                                        value.gen.py_ast[0]
                                        for value in model_params.values()
                                    ],
                                )
                            ),
                        )
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="scope",
                            value=scope,
                        )
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="incl_info",
                            value=self.sync(
                                ast3.List(
                                    elts=[
                                        self.sync(
                                            ast3.Tuple(
                                                elts=[
                                                    self.sync(ast3.Constant(value=key)),
                                                    value,
                                                ],
                                                ctx=ast3.Load(),
                                            )
                                        )
                                        for key, value in include_info
                                    ],
                                    ctx=ast3.Load(),
                                )
                            ),
                        )
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="excl_info",
                            value=self.sync(
                                ast3.List(
                                    elts=[
                                        self.sync(
                                            ast3.Tuple(
                                                elts=[
                                                    self.sync(ast3.Constant(value=key)),
                                                    value,
                                                ],
                                                ctx=ast3.Load(),
                                            )
                                        )
                                        for key, value in exclude_info
                                    ],
                                    ctx=ast3.Load(),
                                )
                            ),
                        ),
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="inputs",
                            value=self.sync(
                                ast3.List(
                                    elts=inputs,
                                    ctx=ast3.Load(),
                                )
                            ),
                        )
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="outputs",
                            value=(
                                self.sync(
                                    ast3.Tuple(
                                        elts=outputs,
                                        ctx=ast3.Load(),
                                    )
                                )
                                if not isinstance(outputs, ast3.Call)
                                else outputs
                            ),
                        )
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="action",
                            value=action,
                        )
                    ),
                ],
            )
        )

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        target: ArchRefChain,
        signature: FuncSignature | EventSignature,
        body: SubNodeList[CodeBlockStmt],
        doc: Optional[String],
        decorators: Optional[SubNodeList[ExprType]],
        """
        for i in node.target.archs:
            if i.sym_link:
                self.link_jac_py_nodes(jac_node=i, py_nodes=i.sym_link.decl.gen.py_ast)
                self.link_jac_py_nodes(
                    jac_node=i.name_ref, py_nodes=i.sym_link.decl.gen.py_ast
                )
        if isinstance(node.parent, ast.Ability) and node.parent.signature:
            # TODO: Here we need to do a link for each subnode to the original parent signature
            pass

    def exit_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional[SubNodeList[ParamVar]],
        return_type: Optional[SubTag[ExprType]],
        """
        params = (
            [self.sync(ast3.arg(arg="self", annotation=None))]
            if node.is_method and not node.is_static
            else []
        )
        vararg = None
        kwarg = None
        if isinstance(node.params, ast.SubNodeList):
            for i in node.params.items:
                if i.unpack and i.unpack.value == "*":
                    vararg = i.gen.py_ast[0]
                elif i.unpack and i.unpack.value == "**":
                    kwarg = i.gen.py_ast[0]
                else:
                    (
                        params.append(i.gen.py_ast[0])
                        if isinstance(i.gen.py_ast[0], ast3.arg)
                        else self.ice("This list should only be Args")
                    )
        defaults = (
            [x.value.gen.py_ast[0] for x in node.params.items if x.value]
            if node.params
            else []
        )
        node.gen.py_ast = [
            self.sync(
                ast3.arguments(
                    posonlyargs=[],
                    args=params,
                    kwonlyargs=[],
                    vararg=vararg,
                    kwarg=kwarg,
                    kw_defaults=[],
                    defaults=defaults,
                )
            )
        ]

    def exit_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional[ExprType],
        return_type: Optional[SubTag[ExprType]],
        """
        here = self.sync(
            ast3.arg(
                arg=f"{Con.HERE.value}",
                annotation=(
                    node.arch_tag_info.gen.py_ast[0] if node.arch_tag_info else None
                ),
            ),
            jac_node=node.arch_tag_info if node.arch_tag_info else node,
        )
        node.gen.py_ast = [
            self.sync(
                ast3.arguments(
                    posonlyargs=[],
                    args=(
                        [self.sync(ast3.arg(arg="self", annotation=None)), here]
                        if node.is_method
                        else [here]
                    ),
                    kwonlyargs=[],
                    vararg=None,
                    kwargs=None,
                    kw_defaults=[],
                    defaults=[],
                )
            )
        ]

    def exit_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        name_ref: NameType,
        arch: Token,
        """
        if node.arch.name == Tok.TYPE_OP:
            if (
                isinstance(node.name_ref, ast.SpecialVarRef)
                and node.name_ref.var.name == Tok.KW_ROOT
            ):
                node.gen.py_ast = [
                    self.sync(
                        ast3.Attribute(
                            value=self.sync(
                                ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                            ),
                            attr="RootType",
                            ctx=ast3.Load(),
                        )
                    )
                ]
            else:
                self.needs_typing()
                node.gen.py_ast = [
                    self.sync(
                        ast3.Attribute(
                            value=self.sync(ast3.Name(id="_jac_typ", ctx=ast3.Load())),
                            attr=node.name_ref.sym_name,
                            ctx=ast3.Load(),
                        )
                    )
                ]
        else:
            node.gen.py_ast = node.name_ref.gen.py_ast

    def exit_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: Sequence[ArchRef],
        """

        def make_attr_chain(arch: list[ast.ArchRef]) -> list[ast3.AST]:
            """Make attr chain."""
            if len(arch) == 0:
                return []
            if len(arch) == 1 and isinstance(arch[0].gen.py_ast, ast3.AST):
                return arch[0].gen.py_ast
            cur = arch[-1]
            attr = self.sync(
                ast3.Attribute(
                    value=make_attr_chain(arch[:-1]),
                    attr=cur.name_ref.sym_name,
                    ctx=ast3.Load(),
                ),
                jac_node=cur,
            )
            return [attr]

        node.gen.py_ast = make_attr_chain(node.archs)

    def exit_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: SubTag[ExprType],
        value: Optional[ExprType],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.arg(
                    arg=node.name.sym_name,
                    annotation=node.type_tag.gen.py_ast[0] if node.type_tag else None,
                )
            )
        ]
        self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)

    def exit_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        is_static: bool,
        access: Optional[SubTag[Token]],
        vars: SubNodeList[HasVar],
        is_frozen: bool,
        doc: Optional[String],
        """
        if node.doc:
            doc = self.sync(ast3.Expr(value=node.doc.gen.py_ast[0]), jac_node=node.doc)
            if isinstance(doc, ast3.AST) and isinstance(node.vars.gen.py_ast, list):
                node.gen.py_ast = [doc] + node.vars.gen.py_ast
            else:
                raise self.ice()
        else:
            node.gen.py_ast = node.vars.gen.py_ast  # TODO: This is a list

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Name,
        type_tag: SubTag[Expr],
        value: Optional[Expr],
        semstr: Optional[String] = None,
        """
        annotation = node.type_tag.gen.py_ast[0] if node.type_tag else None
        is_static_var = (
            node.parent
            and node.parent.parent
            and isinstance(node.parent.parent, ast.ArchHas)
            and node.parent.parent.is_static
        )
        is_in_class = (
            node.parent
            and node.parent.parent
            and node.parent.parent.parent
            and (
                (
                    isinstance(node.parent.parent.parent, ast.Architype)
                    and node.parent.parent.parent.arch_type.name == Tok.KW_CLASS
                )
                or (
                    node.parent.parent.parent.parent
                    and isinstance(node.parent.parent.parent.parent, ast.Architype)
                    and node.parent.parent.parent.parent.arch_type.name == Tok.KW_CLASS
                )
            )
        )
        if is_static_var:
            self.needs_typing()
            annotation = self.sync(
                ast3.Subscript(
                    value=self.sync(
                        ast3.Attribute(
                            value=self.sync(ast3.Name(id="_jac_typ", ctx=ast3.Load())),
                            attr="ClassVar",
                            ctx=ast3.Load(),
                        )
                    ),
                    slice=annotation,
                    ctx=ast3.Load(),
                )
            )
        (
            self.needs_dataclass_field()
            if node.defer and not (is_static_var or is_in_class)
            else None
        )
        node.gen.py_ast = [
            (
                self.sync(
                    ast3.AnnAssign(
                        target=node.name.gen.py_ast[0],
                        annotation=annotation,
                        value=(
                            self.sync(
                                ast3.Call(
                                    func=self.sync(
                                        ast3.Attribute(
                                            value=self.sync(
                                                ast3.Name(
                                                    id=Con.JAC_FEATURE.value,
                                                    ctx=ast3.Load(),
                                                )
                                            ),
                                            attr="has_instance_default",
                                            ctx=ast3.Load(),
                                        )
                                    ),
                                    args=[],
                                    keywords=[
                                        self.sync(
                                            ast3.keyword(
                                                arg="gen_func",
                                                value=self.sync(
                                                    ast3.Lambda(
                                                        args=self.sync(
                                                            ast3.arguments(
                                                                posonlyargs=[],
                                                                args=[],
                                                                kwonlyargs=[],
                                                                vararg=None,
                                                                kwargs=None,
                                                                kw_defaults=[],
                                                                defaults=[],
                                                            )
                                                        ),
                                                        body=node.value.gen.py_ast[0],
                                                    )
                                                ),
                                            )
                                        )
                                    ],
                                )
                            )
                            if node.value
                            and not (is_static_var or is_in_class or node.defer)
                            else (
                                self.sync(
                                    ast3.Call(
                                        func=self.sync(
                                            ast3.Name(
                                                id="__jac_field__",
                                                ctx=ast3.Load(),
                                            )
                                        ),
                                        args=[],
                                        keywords=[
                                            self.sync(
                                                ast3.keyword(
                                                    arg="init",
                                                    value=self.sync(
                                                        ast3.Constant(value=False)
                                                    ),
                                                )
                                            )
                                        ],
                                    )
                                )
                                if node.defer and not (is_static_var or is_in_class)
                                else node.value.gen.py_ast[0] if node.value else None
                            )
                        ),
                        simple=int(isinstance(node.name, ast.Name)),
                    )
                )
            )
        ]

    def exit_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """
        # TODO: Come back

    def exit_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt | ElseIf],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.If(
                    test=node.condition.gen.py_ast[0],
                    body=self.resolve_stmt_block(node.body),
                    orelse=node.else_body.gen.py_ast if node.else_body else [],
                )
            )
        ]

    def exit_else_if(self, node: ast.ElseIf) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt | ElseIf],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.If(
                    test=node.condition.gen.py_ast[0],
                    body=self.resolve_stmt_block(node.body),
                    orelse=node.else_body.gen.py_ast if node.else_body else [],
                )
            )
        ]

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        """
        node.gen.py_ast = self.resolve_stmt_block(node.body)

    def exit_expr_stmt(self, node: ast.ExprStmt) -> None:
        """Sub objects.

        expr: ExprType,
        in_fstring: bool,
        """
        node.gen.py_ast = [
            (
                self.sync(ast3.Expr(value=node.expr.gen.py_ast[0]))
                if not node.in_fstring
                else self.sync(
                    ast3.FormattedValue(
                        value=node.expr.gen.py_ast[0],
                        conversion=-1,
                        format_spec=None,
                    )
                )
            )
        ]

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        excepts: Optional[SubNodeList[Except]],
        else_body: Optional[ElseStmt],
        finally_body: Optional[FinallyStmt],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Try(
                    body=self.resolve_stmt_block(node.body),
                    handlers=node.excepts.gen.py_ast if node.excepts else [],
                    orelse=node.else_body.gen.py_ast if node.else_body else [],
                    finalbody=node.finally_body.gen.py_ast if node.finally_body else [],
                )
            )
        ]

    def exit_except(self, node: ast.Except) -> None:
        """Sub objects.

        ex_type: ExprType,
        name: Optional[Name],
        body: SubNodeList[CodeBlockStmt],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.ExceptHandler(
                    type=node.ex_type.gen.py_ast[0],
                    name=node.name.sym_name if node.name else None,
                    body=self.resolve_stmt_block(node.body),
                )
            )
        ]
        if node.name:
            self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)

    def exit_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: SubNodeList[CodeBlockStmt],
        """
        node.gen.py_ast = self.resolve_stmt_block(node.body)

    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: Assignment,
        is_async: bool,
        condition: ExprType,
        count_by: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        """
        py_nodes: list[ast3.AST] = []
        body = node.body.gen.py_ast
        if (
            isinstance(body, list)
            and isinstance(node.count_by.gen.py_ast[0], ast3.AST)
            and isinstance(node.iter.gen.py_ast[0], ast3.AST)
        ):
            body += [node.count_by.gen.py_ast[0]]
        else:
            raise self.ice()
        py_nodes.append(node.iter.gen.py_ast[0])
        py_nodes.append(
            self.sync(
                ast3.While(
                    test=node.condition.gen.py_ast[0],
                    body=body,
                    orelse=node.else_body.gen.py_ast if node.else_body else [],
                )
            )
        )
        node.gen.py_ast = py_nodes

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        target: Expr,
        is_async: bool,
        collection: Expr,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        """
        for_node = ast3.AsyncFor if node.is_async else ast3.For
        node.gen.py_ast = [
            self.sync(
                for_node(
                    target=node.target.gen.py_ast[0],
                    iter=node.collection.gen.py_ast[0],
                    body=self.resolve_stmt_block(node.body),
                    orelse=node.else_body.gen.py_ast if node.else_body else [],
                )
            )
        ]

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: SubNodeList[CodeBlockStmt],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.While(
                    test=node.condition.gen.py_ast[0],
                    body=self.resolve_stmt_block(node.body),
                    orelse=[],
                )
            )
        ]

    def exit_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        is_async: bool,
        exprs: SubNodeList[ExprAsItem],
        body: SubNodeList[CodeBlockStmt],
        """
        with_node = ast3.AsyncWith if node.is_async else ast3.With
        node.gen.py_ast = [
            self.sync(
                with_node(
                    items=node.exprs.gen.py_ast, body=self.resolve_stmt_block(node.body)
                )
            )
        ]

    def exit_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: ExprType,
        alias: Optional[ExprType],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.withitem(
                    context_expr=node.expr.gen.py_ast[0],
                    optional_vars=node.alias.gen.py_ast[0] if node.alias else None,
                )
            )
        ]
        self.link_jac_py_nodes(jac_node=node.expr, py_nodes=node.gen.py_ast)
        if node.alias:
            self.link_jac_py_nodes(jac_node=node.alias, py_nodes=node.gen.py_ast)

    def exit_raise_stmt(self, node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        from_target: Optional[ExprType],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Raise(
                    exc=node.cause.gen.py_ast[0] if node.cause else None,
                    cause=node.from_target.gen.py_ast[0] if node.from_target else None,
                )
            )
        ]

    def exit_assert_stmt(self, node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Assert(
                    test=node.condition.gen.py_ast[0],
                    msg=node.error_msg.gen.py_ast[0] if node.error_msg else None,
                )
            )
        ]

    def exit_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """
        if node.ctrl.name == Tok.KW_BREAK:
            node.gen.py_ast = [self.sync(ast3.Break())]
        elif node.ctrl.name == Tok.KW_CONTINUE:
            node.gen.py_ast = [self.sync(ast3.Continue())]
        elif node.ctrl.name == Tok.KW_SKIP:
            node.gen.py_ast = [self.sync(ast3.Return(value=None))]

    def exit_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: SubNodeList[AtomType],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Delete(
                    targets=(
                        node.target.values.gen.py_ast
                        if isinstance(node.target, ast.TupleVal) and node.target.values
                        else node.target.gen.py_ast
                    )
                )
            )
        ]

    def exit_report_stmt(self, node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Expr(
                    value=self.sync(
                        self.sync(
                            ast3.Call(
                                func=self.sync(
                                    ast3.Attribute(
                                        value=self.sync(
                                            ast3.Name(
                                                id=Con.JAC_FEATURE.value,
                                                ctx=ast3.Load(),
                                            )
                                        ),
                                        attr="report",
                                        ctx=ast3.Load(),
                                    )
                                ),
                                args=node.expr.gen.py_ast,
                                keywords=[],
                            )
                        )
                    )
                )
            )
        ]

    def exit_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        node.gen.py_ast = [
            self.sync(ast3.Return(value=node.expr.gen.py_ast[0] if node.expr else None))
        ]

    def exit_yield_expr(self, node: ast.YieldExpr) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        if not node.with_from:
            node.gen.py_ast = [
                self.sync(
                    ast3.Yield(value=node.expr.gen.py_ast[0] if node.expr else None)
                )
            ]
        else:
            node.gen.py_ast = [
                self.sync(
                    ast3.YieldFrom(value=node.expr.gen.py_ast[0] if node.expr else None)
                )
            ]

    def exit_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        loc = self.sync(
            ast3.Name(id="self", ctx=ast3.Load())
            if node.from_walker
            else ast3.Name(id=Con.HERE.value, ctx=ast3.Load())
        )
        node.gen.py_ast = [
            self.sync(
                ast3.Expr(
                    value=self.sync(
                        ast3.Call(
                            func=self.sync(
                                ast3.Attribute(
                                    value=self.sync(
                                        ast3.Name(
                                            id=Con.JAC_FEATURE.value, ctx=ast3.Load()
                                        )
                                    ),
                                    attr="ignore",
                                    ctx=ast3.Load(),
                                )
                            ),
                            args=[loc, node.target.gen.py_ast[0]],
                            keywords=[],
                        )
                    )
                )
            )
        ]

    def exit_visit_stmt(self, node: ast.VisitStmt) -> None:
        """Sub objects.

        vis_type: Optional[SubNodeList[AtomType]],
        target: ExprType,
        else_body: Optional[ElseStmt],
        """
        loc = self.sync(
            ast3.Name(id="self", ctx=ast3.Load())
            if node.from_walker
            else ast3.Name(id=Con.HERE.value, ctx=ast3.Load())
        )
        node.gen.py_ast = [
            self.sync(
                ast3.If(
                    test=self.sync(
                        ast3.Call(
                            func=self.sync(
                                ast3.Attribute(
                                    value=self.sync(
                                        ast3.Name(
                                            id=Con.JAC_FEATURE.value, ctx=ast3.Load()
                                        )
                                    ),
                                    attr="visit_node",
                                    ctx=ast3.Load(),
                                )
                            ),
                            args=[loc, node.target.gen.py_ast[0]],
                            keywords=[],
                        )
                    ),
                    body=[self.sync(ast3.Pass())],
                    orelse=node.else_body.gen.py_ast if node.else_body else [],
                )
            )
        ]

    def exit_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        """Sub objects.

        hops: Optional[ExprType],
        else_body: Optional[ElseStmt],
        """
        self.warning("Revisit not used in Jac", node)
        node.gen.py_ast = [
            self.sync(ast3.Expr(value=self.sync(ast3.Constant(value=None))))
        ]

    def exit_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects."""
        loc = self.sync(
            ast3.Name(id="self", ctx=ast3.Load())
            if node.from_walker
            else ast3.Name(id=Con.HERE.value, ctx=ast3.Load())
        )
        node.gen.py_ast = [
            self.sync(
                ast3.Expr(
                    value=self.sync(
                        self.sync(
                            ast3.Call(
                                func=self.sync(
                                    ast3.Attribute(
                                        value=self.sync(
                                            ast3.Name(
                                                id=Con.JAC_FEATURE.value,
                                                ctx=ast3.Load(),
                                            )
                                        ),
                                        attr="disengage",
                                        ctx=ast3.Load(),
                                    )
                                ),
                                args=[loc],
                                keywords=[],
                            )
                        )
                    )
                )
            ),
            self.sync(ast3.Return()),
        ]

    def exit_await_expr(self, node: ast.AwaitExpr) -> None:
        """Sub objects.

        target: ExprType,
        """
        node.gen.py_ast = [self.sync(ast3.Await(value=node.target.gen.py_ast[0]))]

    def exit_global_stmt(self, node: ast.GlobalStmt) -> None:
        """Sub objects.

        target: SubNodeList[NameType],
        """
        py_nodes = []
        for x in node.target.items:
            py_nodes.append(
                self.sync(
                    ast3.Global(names=[x.sym_name]),
                    jac_node=x,
                )
            )
            self.link_jac_py_nodes(jac_node=x, py_nodes=[py_nodes[-1]])
        node.gen.py_ast = [*py_nodes]

    def exit_non_local_stmt(self, node: ast.NonLocalStmt) -> None:
        """Sub objects.

        target: SubNodeList[NameType],
        """
        py_nodes = []
        for x in node.target.items:
            py_nodes.append(
                self.sync(
                    ast3.Nonlocal(names=[x.sym_name]),
                    jac_node=x,
                )
            )
            self.link_jac_py_nodes(jac_node=x, py_nodes=[py_nodes[-1]])
        node.gen.py_ast = [*py_nodes]

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        target: SubNodeList[AtomType],
        value: Optional[ExprType | YieldStmt],
        type_tag: Optional[SubTag[ExprType]],
        mutable: bool =True,
        """
        value = (
            node.value.gen.py_ast[0]
            if node.value
            else (
                self.sync(
                    ast3.Call(
                        func=self.sync(ast3.Name(id="__jac_auto__", ctx=ast3.Load())),
                        args=[],
                        keywords=[],
                    )
                )
                if node.is_enum_stmt
                else None if node.type_tag else self.ice()
            )
        )
        if node.type_tag:
            node.gen.py_ast = [
                self.sync(
                    ast3.AnnAssign(
                        target=node.target.items[0].gen.py_ast[0],
                        annotation=node.type_tag.gen.py_ast[0],
                        value=node.value.gen.py_ast[0] if node.value else None,
                        simple=int(isinstance(node.target.gen.py_ast[0], ast3.Name)),
                    )
                )
            ]
        elif node.aug_op:
            node.gen.py_ast = [
                self.sync(
                    ast3.AugAssign(
                        target=node.target.items[0].gen.py_ast[0],
                        op=node.aug_op.gen.py_ast[0],
                        value=value,
                    )
                )
            ]
        else:
            node.gen.py_ast = [
                self.sync(ast3.Assign(targets=node.target.gen.py_ast, value=value))
            ]

    def exit_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """
        if isinstance(node.op, ast.ConnectOp):
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.sync(
                            ast3.Attribute(
                                value=self.sync(
                                    ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                                ),
                                attr="connect",
                                ctx=ast3.Load(),
                            )
                        ),
                        args=[],
                        keywords=[
                            self.sync(
                                ast3.keyword(
                                    arg="left",
                                    value=(
                                        node.right.gen.py_ast[0]
                                        if node.op.edge_dir == EdgeDir.IN
                                        else node.left.gen.py_ast[0]
                                    ),
                                )
                            ),
                            self.sync(
                                ast3.keyword(
                                    arg="right",
                                    value=(
                                        node.left.gen.py_ast[0]
                                        if node.op.edge_dir == EdgeDir.IN
                                        else node.right.gen.py_ast[0]
                                    ),
                                )
                            ),
                            self.sync(
                                ast3.keyword(
                                    arg="edge_spec",
                                    value=node.op.gen.py_ast[0],
                                )
                            ),
                        ],
                    )
                )
            ]
        elif isinstance(node.op, ast.DisconnectOp):
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.sync(
                            ast3.Attribute(
                                value=self.sync(
                                    ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                                ),
                                attr="disconnect",
                                ctx=ast3.Load(),
                            )
                        ),
                        args=[
                            node.left.gen.py_ast[0],
                            node.right.gen.py_ast[0],
                            self.sync(
                                ast3.Constant(value=node.op.edge_spec.edge_dir.name)
                            ),
                            (
                                node.op.edge_spec.filter_cond.gen.py_ast[0]
                                if node.op.edge_spec.filter_cond is not None
                                else self.sync(ast3.Constant(value=None))
                            ),
                        ],
                        keywords=[],
                    )
                )
            ]
        elif node.op.name in [Tok.KW_AND.value, Tok.KW_OR.value]:
            node.gen.py_ast = [
                self.sync(
                    ast3.BoolOp(
                        op=node.op.gen.py_ast[0],
                        values=[node.left.gen.py_ast[0], node.right.gen.py_ast[0]],
                    )
                )
            ]
        elif node.op.name in [Tok.WALRUS_EQ] and isinstance(
            node.left.gen.py_ast[0], ast3.Name
        ):
            node.left.gen.py_ast[0].ctx = ast3.Store()  # TODO: Short term fix
            node.gen.py_ast = [
                self.sync(
                    ast3.NamedExpr(
                        target=node.left.gen.py_ast[0],
                        value=node.right.gen.py_ast[0],
                    )
                )
            ]
        elif node.op.gen.py_ast and isinstance(node.op.gen.py_ast[0], ast3.AST):
            node.gen.py_ast = [
                self.sync(
                    ast3.BinOp(
                        left=node.left.gen.py_ast[0],
                        right=node.right.gen.py_ast[0],
                        op=node.op.gen.py_ast[0],
                    )
                )
            ]
        else:
            node.gen.py_ast = self.translate_jac_bin_op(node)

    def translate_jac_bin_op(self, node: ast.BinaryExpr) -> list[ast3.AST]:
        """Translate jac binary op."""
        if isinstance(node.op, (ast.DisconnectOp, ast.ConnectOp)):
            raise self.ice()
        elif node.op.name in [
            Tok.PIPE_FWD,
            Tok.A_PIPE_FWD,
        ]:
            func_node = ast.FuncCall(
                target=node.right,
                params=(
                    node.left.values
                    if isinstance(node.left, ast.TupleVal)
                    else ast.SubNodeList(
                        items=[node.left], delim=Tok.COMMA, kid=[node.left]
                    )
                ),
                genai_call=None,
                kid=node.kid,
            )
            self.exit_func_call(func_node)
            return func_node.gen.py_ast
        elif node.op.name in [Tok.KW_SPAWN]:
            self.needs_jac_feature()
            return [
                self.sync(
                    ast3.Call(
                        func=self.sync(
                            ast3.Attribute(
                                value=self.sync(
                                    ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                                ),
                                attr="spawn_call",
                                ctx=ast3.Load(),
                            )
                        ),
                        args=[node.left.gen.py_ast[0], node.right.gen.py_ast[0]],
                        keywords=[],
                    )
                )
            ]
        elif node.op.name in [
            Tok.PIPE_BKWD,
            Tok.A_PIPE_BKWD,
        ]:
            func_node = ast.FuncCall(
                target=node.left,
                params=(
                    node.right.values
                    if isinstance(node.right, ast.TupleVal)
                    else ast.SubNodeList(
                        items=[node.right], delim=Tok.COMMA, kid=[node.right]
                    )
                ),
                genai_call=None,
                kid=node.kid,
            )
            self.exit_func_call(func_node)
            return func_node.gen.py_ast
        elif node.op.name == Tok.PIPE_FWD and isinstance(node.right, ast.TupleVal):
            self.error("Invalid pipe target.")
        elif node.op.name == Tok.ELVIS_OP:
            self.needs_jac_feature()
            return [
                self.sync(
                    ast3.Call(
                        func=self.sync(
                            ast3.Attribute(
                                value=self.sync(
                                    ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                                ),
                                attr="elvis",
                                ctx=ast3.Load(),
                            )
                        ),
                        args=[node.left.gen.py_ast[0], node.right.gen.py_ast[0]],
                        keywords=[],
                    )
                )
            ]
        else:
            self.error(
                f"Binary operator {node.op.value} not supported in bootstrap Jac"
            )
        return []

    def exit_compare_expr(self, node: ast.CompareExpr) -> None:
        """Sub objects.

        left: Expr,
        rights: list[Expr],
        ops: list[Token],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Compare(
                    left=node.left.gen.py_ast[0],
                    comparators=[i.gen.py_ast[0] for i in node.rights],
                    ops=[i.gen.py_ast[0] for i in node.ops],
                )
            )
        ]

    def exit_bool_expr(self, node: ast.BoolExpr) -> None:
        """Sub objects.

        op: Token,
        values: list[Expr],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.BoolOp(
                    op=node.op.gen.py_ast[0],
                    values=[i.gen.py_ast[0] for i in node.values],
                )
            )
        ]

    def exit_lambda_expr(self, node: ast.LambdaExpr) -> None:
        """Sub objects.

        signature: FuncSignature,
        body: ExprType,
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Lambda(
                    args=(
                        node.signature.gen.py_ast[0]
                        if node.signature
                        else self.sync(
                            ast3.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            )
                        )
                    ),
                    body=node.body.gen.py_ast[0],
                )
            )
        ]

    def exit_unary_expr(self, node: ast.UnaryExpr) -> None:
        """Sub objects.

        operand: ExprType,
        op: Token,
        """
        if node.op.name == Tok.NOT:
            node.gen.py_ast = [
                self.sync(
                    ast3.UnaryOp(
                        op=self.sync(ast3.Not()),
                        operand=node.operand.gen.py_ast[0],
                    )
                )
            ]
        elif node.op.name == Tok.BW_NOT:
            node.gen.py_ast = [
                self.sync(
                    ast3.UnaryOp(
                        op=self.sync(ast3.Invert()),
                        operand=node.operand.gen.py_ast[0],
                    )
                )
            ]
        elif node.op.name == Tok.PLUS:
            node.gen.py_ast = [
                self.sync(
                    ast3.UnaryOp(
                        op=self.sync(ast3.UAdd()),
                        operand=node.operand.gen.py_ast[0],
                    )
                )
            ]
        elif node.op.name == Tok.MINUS:
            node.gen.py_ast = [
                self.sync(
                    ast3.UnaryOp(
                        op=self.sync(ast3.USub()),
                        operand=node.operand.gen.py_ast[0],
                    )
                )
            ]
        elif node.op.name in [Tok.PIPE_FWD, Tok.KW_SPAWN, Tok.A_PIPE_FWD]:
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=node.operand.gen.py_ast[0],
                        args=[],
                        keywords=[],
                    )
                )
            ]
        elif node.op.name in [Tok.STAR_MUL]:
            ctx_val = (
                node.operand.py_ctx_func()
                if isinstance(node.operand, ast.AstSymbolNode)
                else ast3.Load()
            )
            node.gen.py_ast = [
                self.sync(
                    ast3.Starred(
                        value=node.operand.gen.py_ast[0],
                        ctx=ctx_val,
                    )
                )
            ]
        elif node.op.name in [Tok.STAR_POW]:
            node.gen.py_ast = node.operand.gen.py_ast
        else:
            self.ice(f"Unknown Unary operator {node.op.value}")

    def exit_if_else_expr(self, node: ast.IfElseExpr) -> None:
        """Sub objects.

        condition: ExprType,
        value: ExprType,
        else_value: ExprType,
        """
        node.gen.py_ast = [
            self.sync(
                ast3.IfExp(
                    test=node.condition.gen.py_ast[0],
                    body=node.value.gen.py_ast[0],
                    orelse=node.else_value.gen.py_ast[0],
                )
            )
        ]

    def exit_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: Sequence[String | FString],
        """

        def get_pieces(str_seq: Sequence) -> list[str | ast3.AST]:
            """Pieces."""
            pieces: list[str | ast3.AST] = []
            for i in str_seq:
                if isinstance(i, ast.String):
                    pieces.append(i.lit_value)
                elif isinstance(i, ast.FString):
                    pieces.extend(get_pieces(i.parts.items)) if i.parts else None
                elif isinstance(i, ast.ExprStmt):
                    pieces.append(i.gen.py_ast[0])
                else:
                    raise self.ice("Multi string made of something weird.")
            return pieces

        combined_multi: list[str | bytes | ast3.AST] = []
        for item in get_pieces(node.strings):
            if (
                combined_multi
                and isinstance(item, str)
                and isinstance(combined_multi[-1], str)
            ):
                if isinstance(combined_multi[-1], str):
                    combined_multi[-1] += item
            elif (
                combined_multi
                and isinstance(item, bytes)
                and isinstance(combined_multi[-1], bytes)
            ):
                combined_multi[-1] += item
            else:
                combined_multi.append(item)
        for i in range(len(combined_multi)):
            if isinstance(combined_multi[i], (str, bytes)):
                combined_multi[i] = self.sync(ast3.Constant(value=combined_multi[i]))
        if len(combined_multi) > 1 or not isinstance(combined_multi[0], ast3.Constant):
            node.gen.py_ast = [
                self.sync(
                    ast3.JoinedStr(
                        values=combined_multi,
                    )
                )
            ]
        else:
            node.gen.py_ast = [combined_multi[0]]

    def exit_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: Optional[SubNodeList[String | ExprType]],
        """
        node.gen.py_ast = (
            node.parts.gen.py_ast
            if node.parts
            else [self.sync(ast3.Constant(value=""))]
        )

    def exit_list_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType]],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.List(
                    elts=node.values.gen.py_ast if node.values else [],
                    ctx=node.py_ctx_func(),
                )
            )
        ]

    def exit_set_val(self, node: ast.SetVal) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType]],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Set(
                    elts=node.values.gen.py_ast if node.values else [],
                    ctx=node.py_ctx_func(),
                )
            )
        ]

    def exit_tuple_val(self, node: ast.TupleVal) -> None:
        """Sub objects.

        values: Optional[SubNodeList[ExprType | Assignment]],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Tuple(
                    elts=node.values.gen.py_ast if node.values else [],
                    ctx=node.py_ctx_func(),
                )
            )
        ]

    def exit_dict_val(self, node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: Sequence[KVPair],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Dict(
                    keys=[
                        (x.key.gen.py_ast[0] if x.key else None) for x in node.kv_pairs
                    ],
                    values=[x.value.gen.py_ast[0] for x in node.kv_pairs],
                )
            )
        ]

    def exit_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """
        # Processed elsewhere

    def exit_k_w_pair(self, node: ast.KWPair) -> None:
        """Sub objects.

        key: NameType,
        value: ExprType,
        """
        node.gen.py_ast = [
            self.sync(
                ast3.keyword(
                    arg=node.key.sym_name if node.key else None,
                    value=node.value.gen.py_ast[0],
                )
            )
        ]
        if node.key:
            self.link_jac_py_nodes(jac_node=node.key, py_nodes=node.gen.py_ast)

    def exit_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        target: ExprType,
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.comprehension(
                    target=node.target.gen.py_ast[0],
                    iter=node.collection.gen.py_ast[0],
                    ifs=(
                        [x.gen.py_ast[0] for x in node.conditional]
                        if node.conditional
                        else []
                    ),
                    is_async=0,
                )
            )
        ]

    def exit_list_compr(self, node: ast.ListCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        compr: list[InnerCompr]
        """
        node.gen.py_ast = [
            self.sync(
                ast3.ListComp(
                    elt=node.out_expr.gen.py_ast[0],
                    generators=[i.gen.py_ast[0] for i in node.compr],
                )
            )
        ]

    def exit_gen_compr(self, node: ast.GenCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        compr: list[InnerCompr]
        """
        node.gen.py_ast = [
            self.sync(
                ast3.GeneratorExp(
                    elt=node.out_expr.gen.py_ast[0],
                    generators=[i.gen.py_ast[0] for i in node.compr],
                )
            )
        ]

    def exit_set_compr(self, node: ast.SetCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        compr: list[InnerCompr]
        """
        node.gen.py_ast = [
            self.sync(
                ast3.SetComp(
                    elt=node.out_expr.gen.py_ast[0],
                    generators=[i.gen.py_ast[0] for i in node.compr],
                )
            )
        ]

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        kv_pair: KVPair,
        names: SubNodeList[AtomType],
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.DictComp(
                    key=node.kv_pair.key.gen.py_ast[0] if node.kv_pair.key else None,
                    value=node.kv_pair.value.gen.py_ast[0],
                    generators=[i.gen.py_ast[0] for i in node.compr],
                )
            )
        ]

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: Expr,
        right: AtomExpr | Expr,
        is_attr: bool,
        is_null_ok: bool,
        is_genai: bool = False,
        """
        if node.is_genai:
            node.gen.py_ast = []
        if node.is_attr:
            if isinstance(node.right, ast.AstSymbolNode):
                node.gen.py_ast = [
                    self.sync(
                        ast3.Attribute(
                            value=node.target.gen.py_ast[0],
                            attr=(node.right.sym_name),
                            ctx=(node.right.py_ctx_func()),
                        )
                    )
                ]
                self.link_jac_py_nodes(
                    jac_node=node.right.sym_name_node, py_nodes=node.gen.py_ast
                )
            else:
                self.error("Invalid attribute access")
        elif isinstance(node.right, ast.FilterCompr):
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=node.right.gen.py_ast[0],
                        args=[node.target.gen.py_ast[0]],
                        keywords=[],
                    )
                )
            ]
        elif isinstance(node.right, ast.AssignCompr):
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.sync(
                            ast3.Attribute(
                                value=self.sync(
                                    ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                                ),
                                attr="assign_compr",
                                ctx=ast3.Load(),
                            )
                        ),
                        args=[node.target.gen.py_ast[0], node.right.gen.py_ast[0]],
                        keywords=[],
                    )
                )
            ]
        else:
            node.gen.py_ast = [
                self.sync(
                    ast3.Subscript(
                        value=node.target.gen.py_ast[0],
                        slice=node.right.gen.py_ast[0],
                        ctx=(
                            node.right.py_ctx_func()
                            if isinstance(node.right, ast.AstSymbolNode)
                            else ast3.Load()
                        ),
                    )
                )
            ]
            node.right.gen.py_ast[0].ctx = ast3.Load()  # type: ignore
        if node.is_null_ok:
            if isinstance(node.gen.py_ast[0], ast3.Attribute):
                node.gen.py_ast[0].value = self.sync(
                    ast3.Name(id="__jac_tmp", ctx=ast3.Load())
                )
            node.gen.py_ast = [
                self.sync(
                    ast3.IfExp(
                        test=self.sync(
                            ast3.NamedExpr(
                                target=self.sync(
                                    ast3.Name(id="__jac_tmp", ctx=ast3.Store())
                                ),
                                value=node.target.gen.py_ast[0],
                            )
                        ),
                        body=node.gen.py_ast[0],
                        orelse=self.sync(ast3.Constant(value=None)),
                    )
                )
            ]

    def exit_atom_unit(self, node: ast.AtomUnit) -> None:
        """Sub objects.

        value: AtomType | ExprType,
        is_paren: bool,
        """
        node.gen.py_ast = node.value.gen.py_ast

    def exit_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: Expr,
        params: Optional[SubNodeList[Expr | KWPair]],
        """
        func = node.target.gen.py_ast[0]
        args = []
        keywords = []
        if node.params and len(node.params.items) > 0:
            for x in node.params.items:
                if isinstance(x, ast.UnaryExpr) and x.op.name == Tok.STAR_POW:
                    keywords.append(
                        self.sync(ast3.keyword(value=x.operand.gen.py_ast[0]), x)
                    )
                elif isinstance(x, ast.Expr):
                    args.append(x.gen.py_ast[0])
                elif isinstance(x, ast.KWPair) and isinstance(
                    x.gen.py_ast[0], ast3.keyword
                ):
                    keywords.append(x.gen.py_ast[0])
                else:
                    self.ice("Invalid Parameter")
        if node.genai_call:
            self.needs_jac_feature()
            model = node.genai_call.target.gen.py_ast[0]
            model_params, include_info, exclude_info = extract_params(node.genai_call)
            action = self.sync(
                ast3.Constant(
                    value="Create an object of the specified type, using the specifically "
                    " provided input value(s) and look up any missing attributes from reliable"
                    " online sources to fill them in accurately."
                )
            )
            _output_ = "".join(extract_type(node.target))
            include_info.append(
                (
                    _output_.split(".")[0],
                    self.sync(ast3.Name(id=_output_.split(".")[0], ctx=ast3.Load())),
                )
            )
            scope = self.sync(
                ast3.Call(
                    func=self.sync(
                        ast3.Attribute(
                            value=self.sync(
                                ast3.Name(
                                    id=Con.JAC_FEATURE.value,
                                    ctx=ast3.Load(),
                                )
                            ),
                            attr="obj_scope",
                            ctx=ast3.Load(),
                        )
                    ),
                    args=[
                        self.sync(
                            ast3.Name(
                                id="__file__",
                                ctx=ast3.Load(),
                            )
                        ),
                        self.sync(ast3.Constant(value=_output_)),
                    ],
                    keywords=[],
                )
            )
            outputs = self.sync(
                ast3.Call(
                    func=self.sync(
                        ast3.Attribute(
                            value=self.sync(
                                ast3.Name(
                                    id=Con.JAC_FEATURE.value,
                                    ctx=ast3.Load(),
                                )
                            ),
                            attr="get_sem_type",
                            ctx=ast3.Load(),
                        )
                    ),
                    args=[
                        self.sync(
                            ast3.Name(
                                id="__file__",
                                ctx=ast3.Load(),
                            )
                        ),
                        self.sync(ast3.Constant(value=str(_output_))),
                    ],
                    keywords=[],
                )
            )
            if node.params and node.params.items:
                inputs = [
                    self.sync(
                        ast3.Tuple(
                            elts=[
                                self.sync(
                                    ast3.Call(
                                        func=self.sync(
                                            ast3.Attribute(
                                                value=self.sync(
                                                    ast3.Name(
                                                        id=Con.JAC_FEATURE.value,
                                                        ctx=ast3.Load(),
                                                    )
                                                ),
                                                attr="get_semstr_type",
                                                ctx=ast3.Load(),
                                            )
                                        ),
                                        args=[
                                            self.sync(
                                                ast3.Name(
                                                    id="__file__", ctx=ast3.Load()
                                                )
                                            ),
                                            scope,
                                            self.sync(
                                                ast3.Constant(
                                                    value=(
                                                        kw_pair.key.value
                                                        if isinstance(
                                                            kw_pair.key, ast.Name
                                                        )
                                                        else None
                                                    )
                                                )
                                            ),
                                            self.sync(ast3.Constant(value=True)),
                                        ],
                                        keywords=[],
                                    )
                                ),
                                self.sync(
                                    ast3.Call(
                                        func=self.sync(
                                            ast3.Attribute(
                                                value=self.sync(
                                                    ast3.Name(
                                                        id=Con.JAC_FEATURE.value,
                                                        ctx=ast3.Load(),
                                                    )
                                                ),
                                                attr="get_semstr_type",
                                                ctx=ast3.Load(),
                                            )
                                        ),
                                        args=[
                                            self.sync(
                                                ast3.Name(
                                                    id="__file__", ctx=ast3.Load()
                                                )
                                            ),
                                            scope,
                                            self.sync(
                                                ast3.Constant(
                                                    value=(
                                                        kw_pair.key.value
                                                        if isinstance(
                                                            kw_pair.key, ast.Name
                                                        )
                                                        else None
                                                    )
                                                )
                                            ),
                                            self.sync(ast3.Constant(value=False)),
                                        ],
                                        keywords=[],
                                    )
                                ),
                                self.sync(
                                    ast3.Constant(
                                        value=(
                                            kw_pair.key.value
                                            if isinstance(kw_pair.key, ast.Name)
                                            else None
                                        )
                                    )
                                ),
                                kw_pair.value.gen.py_ast[0],
                            ],
                            ctx=ast3.Load(),
                        )
                    )
                    for kw_pair in node.params.items
                    if isinstance(kw_pair, ast.KWPair)
                ]
                self.cout += 1
            else:
                inputs = []

            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.sync(ast3.Name(id="eval", ctx=ast3.Load())),
                        args=[
                            self.by_llm_call(
                                model,
                                model_params,
                                scope,
                                inputs,
                                outputs,
                                action,
                                include_info,
                                exclude_info,
                            ),
                        ],
                        keywords=[],
                    )
                )
            ]
        else:
            node.gen.py_ast = [
                self.sync(ast3.Call(func=func, args=args, keywords=keywords))
            ]

    def exit_index_slice(self, node: ast.IndexSlice) -> None:
        """Sub objects.

        start: Optional[ExprType],
        stop: Optional[ExprType],
        step: Optional[ExprType],
        is_range: bool,
        """
        if node.is_range:
            node.gen.py_ast = [
                self.sync(
                    ast3.Slice(
                        lower=node.start.gen.py_ast[0] if node.start else None,
                        upper=node.stop.gen.py_ast[0] if node.stop else None,
                        step=node.step.gen.py_ast[0] if node.step else None,
                    )
                )
            ]
        else:
            node.gen.py_ast = node.start.gen.py_ast if node.start else []

    def exit_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        """Sub objects.

        var: Token,
        """
        try:
            var_ast_expr = ast3.parse(node.sym_name).body[0]
            if not isinstance(var_ast_expr, ast3.Expr):
                raise self.ice("Invalid special var ref for pyast generation")
            var_ast = var_ast_expr.value
        except Exception:
            raise self.ice("Invalid special var ref for pyast generation")
        node.gen.py_ast = [self.sync(var_ast, deep=True)]

    def exit_edge_ref_trailer(self, node: ast.EdgeRefTrailer) -> None:
        """Sub objects.

        chain: list[Expr|FilterCompr],
        edges_only: bool,
        """
        pynode = node.chain[0].gen.py_ast[0]
        chomp = [*node.chain]
        last_edge = None
        if node.edges_only:
            for i in node.chain:
                if isinstance(i, ast.EdgeOpRef):
                    last_edge = i
        while len(chomp):
            cur = chomp[0]
            chomp = chomp[1:]
            if len(chomp) == len(node.chain) - 1 and not isinstance(cur, ast.EdgeOpRef):
                continue
            next_i = chomp[0] if chomp else None
            if isinstance(cur, ast.EdgeOpRef) and (
                not next_i or not isinstance(next_i, ast.EdgeOpRef)
            ):
                pynode = self.translate_edge_op_ref(
                    loc=pynode,
                    node=cur,
                    targ=(
                        next_i.gen.py_ast[0]
                        if next_i and not isinstance(next_i, ast.FilterCompr)
                        else None
                    ),
                    edges_only=node.edges_only and cur == last_edge,
                )
                if next_i and isinstance(next_i, ast.FilterCompr):
                    pynode = self.sync(
                        ast3.Call(
                            func=next_i.gen.py_ast[0],
                            args=[pynode],
                            keywords=[],
                        )
                    )
                chomp = chomp[1:] if next_i else chomp
            elif isinstance(cur, ast.EdgeOpRef) and isinstance(next_i, ast.EdgeOpRef):
                pynode = self.translate_edge_op_ref(
                    pynode,
                    cur,
                    targ=None,
                    edges_only=node.edges_only and cur == last_edge,
                )
            else:
                raise self.ice("Invalid edge ref trailer")

        node.gen.py_ast = [pynode]

    def exit_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_type: Optional[ExprType],
        filter_cond: Optional[FilterCompr],
        edge_dir: EdgeDir,
        """
        loc = self.sync(
            ast3.Name(id=Con.HERE.value, ctx=ast3.Load())
            if node.from_walker
            else ast3.Name(id="self", ctx=ast3.Load())
        )
        node.gen.py_ast = [loc]

    def translate_edge_op_ref(
        self,
        loc: ast3.AST,
        node: ast.EdgeOpRef,
        targ: Optional[ast3.AST],
        edges_only: bool,
    ) -> ast3.AST:
        """Generate ast for edge op ref call."""
        return self.sync(
            ast3.Call(
                func=self.sync(
                    ast3.Attribute(
                        value=self.sync(
                            ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                        ),
                        attr="edge_ref",
                        ctx=ast3.Load(),
                    )
                ),
                args=[loc],
                keywords=[
                    self.sync(
                        ast3.keyword(
                            arg="target_obj",
                            value=(
                                targ if targ else self.sync(ast3.Constant(value=None))
                            ),
                        )
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="dir",
                            value=self.sync(
                                ast3.Attribute(
                                    value=self.sync(
                                        ast3.Attribute(
                                            value=self.sync(
                                                ast3.Name(
                                                    id=Con.JAC_FEATURE.value,
                                                    ctx=ast3.Load(),
                                                )
                                            ),
                                            attr="EdgeDir",
                                            ctx=ast3.Load(),
                                        )
                                    ),
                                    attr=node.edge_dir.name,
                                    ctx=ast3.Load(),
                                )
                            ),
                        )
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="filter_func",
                            value=self.sync(
                                node.filter_cond.gen.py_ast[0]
                                if node.filter_cond
                                else self.sync(ast3.Constant(value=None))
                            ),
                        )
                    ),
                    self.sync(
                        ast3.keyword(
                            arg="edges_only",
                            value=self.sync(ast3.Constant(value=edges_only)),
                        )
                    ),
                ],
            )
        )

    def exit_disconnect_op(self, node: ast.DisconnectOp) -> None:
        """Sub objects.

        edge_spec: EdgeOpRef,
        """
        node.gen.py_ast = node.edge_spec.gen.py_ast

    def exit_connect_op(self, node: ast.ConnectOp) -> None:
        """Sub objects.

        conn_type: Optional[ExprType],
        conn_assign: Optional[AssignCompr],
        edge_dir: EdgeDir,
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Call(
                    func=self.sync(
                        ast3.Attribute(
                            value=self.sync(
                                ast3.Name(id=Con.JAC_FEATURE.value, ctx=ast3.Load())
                            ),
                            attr="build_edge",
                            ctx=ast3.Load(),
                        )
                    ),
                    args=[],
                    keywords=[
                        self.sync(
                            ast3.keyword(
                                arg="is_undirected",
                                value=self.sync(
                                    ast3.Constant(value=node.edge_dir == EdgeDir.ANY)
                                ),
                            )
                        ),
                        self.sync(
                            ast3.keyword(
                                arg="conn_type",
                                value=(
                                    node.conn_type.gen.py_ast[0]
                                    if node.conn_type
                                    else self.sync(ast3.Constant(value=None))
                                ),
                            )
                        ),
                        self.sync(
                            ast3.keyword(
                                arg="conn_assign",
                                value=(
                                    node.conn_assign.gen.py_ast[0]
                                    if node.conn_assign
                                    else self.sync(ast3.Constant(value=None))
                                ),
                            )
                        ),
                    ],
                )
            )
        ]

    def exit_filter_compr(self, node: ast.FilterCompr) -> None:
        """Sub objects.

        compares: SubNodeList[BinaryExpr],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Lambda(
                    args=self.sync(
                        ast3.arguments(
                            posonlyargs=[],
                            args=[self.sync(ast3.arg(arg="x"))],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[],
                        )
                    ),
                    body=self.sync(
                        ast3.ListComp(
                            elt=self.sync(ast3.Name(id="i", ctx=ast3.Load())),
                            generators=[
                                self.sync(
                                    ast3.comprehension(
                                        target=self.sync(
                                            ast3.Name(id="i", ctx=ast3.Store())
                                        ),
                                        iter=self.sync(
                                            ast3.Name(id="x", ctx=ast3.Load())
                                        ),
                                        ifs=(
                                            (
                                                [
                                                    self.sync(
                                                        ast3.Call(
                                                            func=self.sync(
                                                                ast3.Name(
                                                                    id="isinstance",
                                                                    ctx=ast3.Load(),
                                                                )
                                                            ),
                                                            args=[
                                                                self.sync(
                                                                    ast3.Name(
                                                                        id="i",
                                                                        ctx=ast3.Load(),
                                                                    )
                                                                ),
                                                                self.sync(
                                                                    node.f_type.gen.py_ast[
                                                                        0
                                                                    ]
                                                                ),
                                                            ],
                                                            keywords=[],
                                                        )
                                                    )
                                                ]
                                                if node.f_type
                                                else []
                                            )
                                            + [
                                                self.sync(
                                                    ast3.Compare(
                                                        left=self.sync(
                                                            ast3.Attribute(
                                                                value=self.sync(
                                                                    ast3.Name(
                                                                        id="i",
                                                                        ctx=ast3.Load(),
                                                                    ),
                                                                    jac_node=x,
                                                                ),
                                                                attr=x.gen.py_ast[
                                                                    0
                                                                ].left.id,
                                                                ctx=ast3.Load(),
                                                            ),
                                                            jac_node=x,
                                                        ),
                                                        ops=x.gen.py_ast[0].ops,
                                                        comparators=x.gen.py_ast[
                                                            0
                                                        ].comparators,
                                                    ),
                                                    jac_node=x,
                                                )
                                                for x in (
                                                    node.compares.items
                                                    if node.compares
                                                    else []
                                                )
                                                if isinstance(
                                                    x.gen.py_ast[0], ast3.Compare
                                                )
                                                and isinstance(
                                                    x.gen.py_ast[0].left, ast3.Name
                                                )
                                            ]
                                        ),
                                        is_async=0,
                                    )
                                )
                            ],
                        )
                    ),
                )
            )
        ]

    def exit_assign_compr(self, node: ast.AssignCompr) -> None:
        """Sub objects.

        assigns: SubNodeList[KWPair],
        """
        keys = []
        values = []
        for i in node.assigns.items:
            if i.key:  # TODO: add support for **kwargs in assign_compr
                keys.append(self.sync(ast3.Constant(i.key.sym_name)))
                values.append(i.value.gen.py_ast[0])
        key_tup = self.sync(ast3.Tuple(elts=keys, ctx=ast3.Load()))
        val_tup = self.sync(ast3.Tuple(elts=values, ctx=ast3.Load()))
        node.gen.py_ast = [
            self.sync(ast3.Tuple(elts=[key_tup, val_tup], ctx=ast3.Load()))
        ]

    def exit_match_stmt(self, node: ast.MatchStmt) -> None:
        """Sub objects.

        target: Expr,
        cases: list[MatchCase],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.Match(
                    subject=node.target.gen.py_ast[0],
                    cases=[x.gen.py_ast[0] for x in node.cases],
                )
            )
        ]

    def exit_match_case(self, node: ast.MatchCase) -> None:
        """Sub objects.

        pattern: MatchPattern,
        guard: Optional[ExprType],
        body: list[CodeBlockStmt],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.match_case(
                    pattern=node.pattern.gen.py_ast[0],
                    guard=node.guard.gen.py_ast[0] if node.guard else None,
                    body=[x.gen.py_ast[0] for x in node.body],
                )
            )
        ]

    def exit_match_or(self, node: ast.MatchOr) -> None:
        """Sub objects.

        patterns: list[MatchPattern],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.MatchOr(
                    patterns=[x.gen.py_ast[0] for x in node.patterns],
                )
            )
        ]

    def exit_match_as(self, node: ast.MatchAs) -> None:
        """Sub objects.

        name: NameType,
        pattern: MatchPattern,
        """
        node.gen.py_ast = [
            self.sync(
                ast3.MatchAs(
                    name=node.name.sym_name,
                    pattern=node.pattern.gen.py_ast[0] if node.pattern else None,
                )
            )
        ]

    def exit_match_wild(self, node: ast.MatchWild) -> None:
        """Sub objects."""
        node.gen.py_ast = [self.sync(ast3.MatchAs())]

    def exit_match_value(self, node: ast.MatchValue) -> None:
        """Sub objects.

        value: ExprType,
        """
        node.gen.py_ast = [self.sync(ast3.MatchValue(value=node.value.gen.py_ast[0]))]

    def exit_match_singleton(self, node: ast.MatchSingleton) -> None:
        """Sub objects.

        value: Bool | Null,
        """
        node.gen.py_ast = [self.sync(ast3.MatchSingleton(value=node.value.lit_value))]

    def exit_match_sequence(self, node: ast.MatchSequence) -> None:
        """Sub objects.

        values: list[MatchPattern],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.MatchSequence(
                    patterns=[x.gen.py_ast[0] for x in node.values],
                )
            )
        ]

    def exit_match_mapping(self, node: ast.MatchMapping) -> None:
        """Sub objects.

        values: list[MatchKVPair | MatchStar],
        """
        mapping = self.sync(ast3.MatchMapping(keys=[], patterns=[], rest=None))
        for i in node.values:
            if (
                isinstance(i, ast.MatchKVPair)
                and isinstance(i.key, ast.MatchValue)
                and isinstance(i.key.value.gen.py_ast[0], ast3.expr)
                and isinstance(i.value.gen.py_ast[0], ast3.pattern)
            ):
                mapping.keys.append(i.key.value.gen.py_ast[0])
                mapping.patterns.append(i.value.gen.py_ast[0])
            elif isinstance(i, ast.MatchStar):
                mapping.rest = i.name.sym_name
        node.gen.py_ast = [mapping]

    def exit_match_k_v_pair(self, node: ast.MatchKVPair) -> None:
        """Sub objects.

        key: MatchPattern | NameType,
        value: MatchPattern,
        """
        node.gen.py_ast = [
            self.sync(
                ast3.MatchMapping(
                    patterns=[node.key.gen.py_ast[0], node.value.gen.py_ast[0]],
                )
            )
        ]

    def exit_match_star(self, node: ast.MatchStar) -> None:
        """Sub objects.

        name: NameType,
        is_list: bool,
        """
        node.gen.py_ast = [self.sync(ast3.MatchStar(name=node.name.sym_name))]

    def exit_match_arch(self, node: ast.MatchArch) -> None:
        """Sub objects.

        name: NameType,
        arg_patterns: Optional[SubNodeList[MatchPattern]],
        kw_patterns: Optional[SubNodeList[MatchKVPair]],
        """
        node.gen.py_ast = [
            self.sync(
                ast3.MatchClass(
                    cls=node.name.gen.py_ast[0],
                    patterns=(
                        [x.gen.py_ast[0] for x in node.arg_patterns.items]
                        if node.arg_patterns
                        else []
                    ),
                    kwd_attrs=(
                        [
                            x.key.sym_name
                            for x in node.kw_patterns.items
                            if isinstance(x.key, ast.NameSpec)
                        ]
                        if node.kw_patterns
                        else []
                    ),
                    kwd_patterns=(
                        [x.value.gen.py_ast[0] for x in node.kw_patterns.items]
                        if node.kw_patterns
                        else []
                    ),
                )
            )
        ]

    def exit_token(self, node: ast.Token) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        if node.name == Tok.KW_AND:
            node.gen.py_ast = [self.sync(ast3.And())]
        elif node.name == Tok.KW_OR:
            node.gen.py_ast = [self.sync(ast3.Or())]
        elif node.name in [Tok.PLUS, Tok.ADD_EQ]:
            node.gen.py_ast = [self.sync(ast3.Add())]
        elif node.name in [Tok.BW_AND, Tok.BW_AND_EQ]:
            node.gen.py_ast = [self.sync(ast3.BitAnd())]
        elif node.name in [Tok.BW_OR, Tok.BW_OR_EQ]:
            node.gen.py_ast = [self.sync(ast3.BitOr())]
        elif node.name in [Tok.BW_XOR, Tok.BW_XOR_EQ]:
            node.gen.py_ast = [self.sync(ast3.BitXor())]
        elif node.name in [Tok.DIV, Tok.DIV_EQ]:
            node.gen.py_ast = [self.sync(ast3.Div())]
        elif node.name in [Tok.FLOOR_DIV, Tok.FLOOR_DIV_EQ]:
            node.gen.py_ast = [self.sync(ast3.FloorDiv())]
        elif node.name in [Tok.LSHIFT, Tok.LSHIFT_EQ]:
            node.gen.py_ast = [self.sync(ast3.LShift())]
        elif node.name in [Tok.MOD, Tok.MOD_EQ]:
            node.gen.py_ast = [self.sync(ast3.Mod())]
        elif node.name in [Tok.STAR_MUL, Tok.MUL_EQ]:
            node.gen.py_ast = [self.sync(ast3.Mult())]
        elif node.name in [Tok.DECOR_OP, Tok.MATMUL_EQ]:
            node.gen.py_ast = [self.sync(ast3.MatMult())]
        elif node.name in [Tok.STAR_POW, Tok.STAR_POW_EQ]:
            node.gen.py_ast = [self.sync(ast3.Pow())]
        elif node.name in [Tok.RSHIFT, Tok.RSHIFT_EQ]:
            node.gen.py_ast = [self.sync(ast3.RShift())]
        elif node.name in [Tok.MINUS, Tok.SUB_EQ]:
            node.gen.py_ast = [self.sync(ast3.Sub())]
        elif node.name in [Tok.BW_NOT, Tok.BW_NOT_EQ]:
            node.gen.py_ast = [self.sync(ast3.Invert())]
        elif node.name in [Tok.NOT]:
            node.gen.py_ast = [self.sync(ast3.Not())]
        elif node.name in [Tok.EQ]:
            node.gen.py_ast = [self.sync(ast3.NotEq())]
        elif node.name == Tok.EE:
            node.gen.py_ast = [self.sync(ast3.Eq())]
        elif node.name == Tok.GT:
            node.gen.py_ast = [self.sync(ast3.Gt())]
        elif node.name == Tok.GTE:
            node.gen.py_ast = [self.sync(ast3.GtE())]
        elif node.name == Tok.KW_IN:
            node.gen.py_ast = [self.sync(ast3.In())]
        elif node.name == Tok.KW_IS:
            node.gen.py_ast = [self.sync(ast3.Is())]
        elif node.name == Tok.KW_ISN:
            node.gen.py_ast = [self.sync(ast3.IsNot())]
        elif node.name == Tok.LT:
            node.gen.py_ast = [self.sync(ast3.Lt())]
        elif node.name == Tok.LTE:
            node.gen.py_ast = [self.sync(ast3.LtE())]
        elif node.name == Tok.NE:
            node.gen.py_ast = [self.sync(ast3.NotEq())]
        elif node.name == Tok.KW_NIN:
            node.gen.py_ast = [self.sync(ast3.NotIn())]

    def exit_name(self, node: ast.Name) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = [
            self.sync(ast3.Name(id=node.sym_name, ctx=node.py_ctx_func()))
        ]

    def exit_float(self, node: ast.Float) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = [self.sync(ast3.Constant(value=float(node.value)))]

    def exit_int(self, node: ast.Int) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """

        def handle_node_value(value: str) -> int:
            if value.startswith(("0x", "0X")):
                return int(value, 16)
            elif value.startswith(("0b", "0B")):
                return int(value, 2)
            elif value.startswith(("0o", "0O")):
                return int(value, 8)
            else:
                return int(value)

        node.gen.py_ast = [
            self.sync(
                ast3.Constant(value=handle_node_value(str(node.value)), kind=None)
            )
        ]

    def exit_string(self, node: ast.String) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = [self.sync(ast3.Constant(value=node.lit_value))]

    def exit_bool(self, node: ast.Bool) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = [self.sync(ast3.Constant(value=node.value == "True"))]

    def exit_builtin_type(self, node: ast.BuiltinType) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = [
            self.sync(ast3.Name(id=node.sym_name, ctx=node.py_ctx_func()))
        ]

    def exit_null(self, node: ast.Null) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = [self.sync(ast3.Constant(value=None))]

    def exit_ellipsis(self, node: ast.Ellipsis) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        node.gen.py_ast = [self.sync(ast3.Constant(value=...))]

    def exit_semi(self, node: ast.Semi) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """

    def exit_comment_token(self, node: ast.CommentToken) -> None:
        """Sub objects.

        file_path: str,
        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """

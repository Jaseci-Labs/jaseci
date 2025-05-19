"""Python AST Generation Pass for the Jac compiler.

This pass transforms the Jac AST into equivalent Python AST by:

1. Traversing the Jac AST and generating corresponding Python AST nodes
2. Handling all Jac language constructs and translating them to Python equivalents:
   - Classes, functions, and methods
   - Control flow statements (if/else, loops, try/except)
   - Data structures (lists, dictionaries, sets)
   - Special Jac features (walkers, abilities, archetypes)
   - Data spatial operations (node/edge connections)

3. Managing imports and dependencies between modules
4. Preserving source location information for error reporting
5. Generating appropriate Python code for Jac-specific constructs

The output of this pass is a complete Python AST representation that can be
compiled to Python bytecode or serialized to Python source code.
"""

import ast as ast3
import copy
import textwrap
from dataclasses import dataclass
from typing import List, Optional, Sequence, TypeVar, Union, cast

import jaclang.compiler.unitree as uni
from jaclang.compiler.constant import Constants as Con, EdgeDir, Tokens as Tok
from jaclang.compiler.passes import UniPass
from jaclang.settings import settings

T = TypeVar("T", bound=ast3.AST)


class PyastGenPass(UniPass):
    """Jac blue transpilation to python pass."""

    def before_pass(self) -> None:
        for i in self.ir_in.impl_mod + self.ir_in.test_mod:
            PyastGenPass(ir_in=i, prog=self.prog)
        self.debuginfo: dict[str, list[str]] = {"jac_mods": []}
        self.already_added: list[str] = []
        self.preamble: list[ast3.AST] = [
            self.sync(
                ast3.ImportFrom(
                    module="__future__",
                    names=[self.sync(ast3.alias(name="annotations", asname=None))],
                    level=0,
                ),
                jac_node=self.ir_out,
            ),
            (
                self.sync(
                    ast3.ImportFrom(
                        module="jaclang.runtimelib.builtin",
                        names=[
                            self.sync(
                                ast3.alias(
                                    name="*",
                                    asname=None,
                                )
                            )
                        ],
                        level=0,
                    ),
                    jac_node=self.ir_out,
                )
            ),
            (
                self.sync(
                    ast3.ImportFrom(
                        module="jaclang",
                        names=[
                            self.sync(
                                ast3.alias(
                                    name="JacMachineInterface",
                                    asname=settings.pyout_jaclib_alias,
                                )
                            ),
                        ],
                        level=0,
                    ),
                    jac_node=self.ir_out,
                )
            ),
        ]

    def enter_node(self, node: uni.UniNode) -> None:
        """Enter node."""
        if node.gen.py_ast:
            self.prune()
            return
        super().enter_node(node)

    def exit_node(self, node: uni.UniNode) -> None:
        """Exit node."""
        super().exit_node(node)
        # for i in node.gen.py_ast:  # Internal validation
        #     self.node_compilable_test(i)

        # TODO: USE THIS TO SYNC
        #     if isinstance(i, ast3.AST):
        #         i.jac_link = node

    def jaclib_obj(self, obj_name: str) -> ast3.Name | ast3.Attribute:
        """Return the object from jaclib as ast node based on the import config."""
        return self.sync(
            ast3.Attribute(
                value=self.sync(
                    ast3.Name(id=settings.pyout_jaclib_alias, ctx=ast3.Load())
                ),
                attr=obj_name,
                ctx=ast3.Load(),
            )
        )

    def needs_typing(self) -> None:
        """Check if enum is needed."""
        if self.needs_typing.__name__ in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.Import(
                    names=[
                        self.sync(
                            ast3.alias(name="typing"),
                            jac_node=self.ir_out,
                        ),
                    ]
                ),
                jac_node=self.ir_out,
            )
        )
        self.already_added.append(self.needs_typing.__name__)

    def needs_enum(self) -> None:
        """Check if enum is needed."""
        if self.needs_enum.__name__ in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="enum",
                    names=[
                        self.sync(ast3.alias(name="Enum", asname=None)),
                        self.sync(ast3.alias(name="auto", asname=None)),
                    ],
                    level=0,
                ),
                jac_node=self.ir_out,
            )
        )
        self.already_added.append(self.needs_enum.__name__)

    def needs_future(self) -> None:
        """Check if enum is needed."""
        if self.needs_future.__name__ in self.already_added:
            return
        self.preamble.append(
            self.sync(
                ast3.ImportFrom(
                    module="concurrent.futures",
                    names=[
                        self.sync(ast3.alias(name="Future", asname=None)),
                    ],
                    level=0,
                ),
                jac_node=self.ir_out,
            )
        )
        self.already_added.append(self.needs_future.__name__)

    def flatten(self, body: list[T | list[T] | None]) -> list[T]:
        new_body = []
        for i in body:
            if isinstance(i, list):
                new_body += i
            elif i is not None:
                new_body.append(i) if i else None
        return new_body

    def sync(
        self, py_node: T, jac_node: Optional[uni.UniNode] = None, deep: bool = False
    ) -> T:
        """Sync ast locations."""
        if not jac_node:
            jac_node = self.cur_node
        for i in ast3.walk(py_node) if deep else [py_node]:
            # TODO:here we are type ignore to hack the mypy bcz
            # python AST dosen't have lineno, col_offset, end_lineno, end_col_offset attributes.
            # we need to discuss with @marsninja
            if isinstance(i, ast3.AST):
                i.lineno = jac_node.loc.first_line  # type:ignore[attr-defined]
                i.col_offset = jac_node.loc.col_start  # type:ignore[attr-defined]
                i.end_lineno = (  # type:ignore[attr-defined]
                    jac_node.loc.last_line
                    if jac_node.loc.last_line
                    and (jac_node.loc.last_line > jac_node.loc.first_line)
                    else jac_node.loc.first_line
                )
                i.end_col_offset = (  # type:ignore[attr-defined]
                    jac_node.loc.col_end
                    if jac_node.loc.col_end
                    and (jac_node.loc.col_end > jac_node.loc.col_start)
                    else jac_node.loc.col_start
                )
                i.jac_link: list[ast3.AST] = [jac_node]  # type: ignore
        return py_node

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
            uni.SubNodeList[uni.CodeBlockStmt]
            | uni.SubNodeList[uni.ArchBlockStmt]
            | uni.SubNodeList[uni.EnumBlockStmt]
            | None
        ),
        doc: Optional[uni.String] = None,
    ) -> list[ast3.AST]:
        """Unwind codeblock."""
        valid_stmts = (
            [i for i in node.items if not isinstance(i, uni.Semi)] if node else []
        )
        ret: list[ast3.AST] = (
            [self.sync(ast3.Pass(), node)]
            if isinstance(node, uni.SubNodeList) and not valid_stmts
            else (
                self.flatten(
                    [
                        x.gen.py_ast
                        for x in valid_stmts
                        if not isinstance(x, uni.ImplDef)
                    ]
                )
                if node
                else []
            )
        )
        if doc:
            ret = [
                self.sync(
                    ast3.Expr(value=cast(ast3.expr, doc.gen.py_ast[0])), jac_node=doc
                ),
                *ret,
            ]
        return ret

    def sync_many(self, py_nodes: list[T], jac_node: uni.UniNode) -> list[T]:
        """Sync ast locations."""
        for py_node in py_nodes:
            self.sync(py_node, jac_node)
        return py_nodes

    def list_to_attrib(
        self, attribute_list: list[str], sync_node_list: Sequence[uni.UniNode]
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

    def exit_sub_tag(self, node: uni.SubTag[uni.T]) -> None:
        node.gen.py_ast = node.tag.gen.py_ast

    def exit_sub_node_list(self, node: uni.SubNodeList[uni.T]) -> None:
        node.gen.py_ast = self.flatten([i.gen.py_ast for i in node.items])

    def exit_module(self, node: uni.Module) -> None:
        clean_body = [i for i in node.body if not isinstance(i, uni.ImplDef)]
        pre_body: list[uni.UniNode] = []
        for pbody in node.impl_mod:
            pre_body = [*pre_body, *pbody.body]
        pre_body = [*pre_body, *clean_body]
        for pbody in node.test_mod:
            pre_body = [*pre_body, *pbody.body]
        body = (
            [
                self.sync(
                    ast3.Expr(value=cast(ast3.expr, node.doc.gen.py_ast[0])),
                    jac_node=node.doc,
                ),
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

    def exit_global_vars(self, node: uni.GlobalVars) -> None:
        if node.doc:
            doc = self.sync(
                ast3.Expr(value=cast(ast3.expr, node.doc.gen.py_ast[0])),
                jac_node=node.doc,
            )
            if isinstance(doc, ast3.AST) and isinstance(
                node.assignments.gen.py_ast, list
            ):
                node.gen.py_ast = [doc] + node.assignments.gen.py_ast
            else:
                raise self.ice()
        else:
            node.gen.py_ast = node.assignments.gen.py_ast

    def exit_test(self, node: uni.Test) -> None:
        test_name = node.name.sym_name
        func = self.sync(
            ast3.FunctionDef(
                name=test_name,
                args=self.sync(
                    ast3.arguments(
                        posonlyargs=[],
                        args=[
                            self.sync(
                                ast3.arg(arg=Con.JAC_CHECK.value, annotation=None)
                            )
                        ],
                        kwonlyargs=[],
                        vararg=None,
                        kwarg=None,
                        kw_defaults=[],
                        defaults=[],
                    )
                ),
                body=[
                    cast(ast3.stmt, stmt)
                    for stmt in self.resolve_stmt_block(node.body, doc=node.doc)
                ],
                decorator_list=[self.jaclib_obj("jac_test")],
                returns=self.sync(ast3.Constant(value=None)),
                type_comment=None,
                type_params=[],
            ),
        )
        if node.loc.mod_path.endswith(".test.jac"):
            func.decorator_list.append(
                self.sync(
                    ast3.Call(
                        func=self.jaclib_obj("impl_patch_filename"),
                        args=[],
                        keywords=[
                            self.sync(
                                ast3.keyword(
                                    arg="file_loc",
                                    value=self.sync(
                                        ast3.Constant(value=node.body.loc.mod_path)
                                    ),
                                )
                            ),
                        ],
                    )
                )
            )
        node.gen.py_ast = [func]

    def exit_module_code(self, node: uni.ModuleCode) -> None:
        node.gen.py_ast = self.resolve_stmt_block(node.body, doc=node.doc)
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
                                    self.sync(ast3.Constant(value=node.name.sym_name))
                                ],
                            )
                        ),
                        body=[cast(ast3.stmt, i) for i in node.gen.py_ast],
                        orelse=[],
                    )
                )
            ]

    def exit_py_inline_code(self, node: uni.PyInlineCode) -> None:
        if node.doc:
            doc = self.sync(
                ast3.Expr(value=cast(ast3.expr, node.doc.gen.py_ast[0])),
                jac_node=node.doc,
            )
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

    def exit_import(self, node: uni.Import) -> None:
        path_alias: dict[str, Optional[str]] = (
            {node.from_loc.dot_path_str: None} if node.from_loc else {}
        )
        imp_from = {}
        if node.items:
            for item in node.items.items:
                if isinstance(item, uni.ModuleItem):
                    imp_from[item.name.sym_name] = (
                        item.alias.sym_name if item.alias else None
                    )
                elif isinstance(item, uni.ModulePath):
                    path_alias[item.dot_path_str] = (
                        item.alias.sym_name if item.alias else None
                    )

        item_names: list[ast3.expr] = []
        item_keys: list[ast3.Constant] = []
        item_values: list[ast3.Constant] = []
        for k, v in imp_from.items():
            item_keys.append(self.sync(ast3.Constant(value=k)))
            item_values.append(self.sync(ast3.Constant(value=v)))
            item_names.append(
                self.sync(
                    ast3.Name(
                        id=v or k,
                        ctx=ast3.Store(),
                    )
                )
            )
        path_named_value: str
        py_nodes: list[ast3.AST] = []
        typecheck_nodes: list[ast3.AST] = []
        runtime_nodes: list[ast3.AST] = []

        if node.doc:
            py_nodes.append(
                self.sync(
                    ast3.Expr(value=cast(ast3.expr, node.doc.gen.py_ast[0])),
                    jac_node=node.doc,
                )
            )

        for path, alias in path_alias.items():
            path_named_value = ("_jac_inc_" if node.is_absorb else "") + (
                alias if alias else path
            ).lstrip(".").split(".")[0]
            # target_named_value = ""
            # for i in path.split("."):
            #     target_named_value += i if i else "."
            #     if i:
            #         break

            args = [
                self.sync(
                    ast3.Constant(value=path),
                ),
                self.sync(
                    ast3.Name(
                        id="__file__",
                        ctx=ast3.Load(),
                    )
                ),
            ]
            keywords = []

            if node.is_absorb:
                args.append(self.sync(ast3.Constant(value=node.is_absorb)))

            if alias is not None:
                keywords.append(
                    self.sync(
                        ast3.keyword(
                            arg="mdl_alias",
                            value=self.sync(
                                ast3.Constant(value=alias),
                            ),
                        )
                    )
                )

            if item_keys and item_values:
                keywords.append(
                    self.sync(
                        ast3.keyword(
                            arg="items",
                            value=self.sync(
                                ast3.Dict(
                                    keys=cast(list[ast3.expr | None], item_keys),
                                    values=cast(list[ast3.expr], item_values),
                                ),
                            ),
                        )
                    )
                )

            runtime_nodes.append(
                self.sync(
                    ast3.Assign(
                        targets=(
                            [
                                self.sync(
                                    ast3.Tuple(
                                        elts=(
                                            item_names
                                            or [
                                                self.sync(
                                                    ast3.Name(
                                                        id=path_named_value,
                                                        ctx=ast3.Store(),
                                                    )
                                                )
                                            ]
                                        ),
                                        ctx=ast3.Store(),
                                    )
                                )
                            ]
                        ),
                        value=self.sync(
                            ast3.Call(
                                func=self.jaclib_obj("py_jac_import"),
                                args=args,
                                keywords=keywords,
                            )
                        ),
                    ),
                ),
            )
        if node.is_absorb:
            absorb_exec = f"={path_named_value}.__dict__['"
            runtime_nodes.append(
                self.sync(
                    ast3.For(
                        target=self.sync(ast3.Name(id="i", ctx=ast3.Store())),
                        iter=self.sync(
                            ast3.IfExp(
                                test=self.sync(
                                    ast3.Compare(
                                        left=self.sync(ast3.Constant(value="__all__")),
                                        ops=[self.sync(ast3.In())],
                                        comparators=[
                                            self.sync(
                                                ast3.Attribute(
                                                    value=self.sync(
                                                        ast3.Name(
                                                            id=path_named_value,
                                                            ctx=ast3.Load(),
                                                        )
                                                    ),
                                                    attr="__dict__",
                                                    ctx=ast3.Load(),
                                                )
                                            )
                                        ],
                                    )
                                ),
                                body=self.sync(
                                    ast3.Attribute(
                                        value=self.sync(
                                            ast3.Name(
                                                id=path_named_value, ctx=ast3.Load()
                                            )
                                        ),
                                        attr="__all__",
                                        ctx=ast3.Load(),
                                    )
                                ),
                                orelse=self.sync(
                                    ast3.Attribute(
                                        value=self.sync(
                                            ast3.Name(
                                                id=path_named_value, ctx=ast3.Load()
                                            )
                                        ),
                                        attr="__dict__",
                                        ctx=ast3.Load(),
                                    )
                                ),
                            )
                        ),
                        body=[
                            self.sync(
                                ast3.If(
                                    test=self.sync(
                                        ast3.UnaryOp(
                                            op=self.sync(ast3.Not()),
                                            operand=self.sync(
                                                ast3.Call(
                                                    func=self.sync(
                                                        ast3.Attribute(
                                                            value=self.sync(
                                                                ast3.Name(
                                                                    id="i",
                                                                    ctx=ast3.Load(),
                                                                )
                                                            ),
                                                            attr="startswith",
                                                            ctx=ast3.Load(),
                                                        )
                                                    ),
                                                    args=[
                                                        self.sync(
                                                            ast3.Constant(value="_")
                                                        )
                                                    ],
                                                    keywords=[],
                                                )
                                            ),
                                        )
                                    ),
                                    body=[
                                        self.sync(
                                            ast3.Expr(
                                                value=self.sync(
                                                    ast3.Call(
                                                        func=self.sync(
                                                            ast3.Name(
                                                                id="exec",
                                                                ctx=ast3.Load(),
                                                            )
                                                        ),
                                                        args=[
                                                            self.sync(
                                                                ast3.JoinedStr(
                                                                    values=[
                                                                        self.sync(
                                                                            ast3.FormattedValue(
                                                                                value=self.sync(
                                                                                    ast3.Name(
                                                                                        id="i",
                                                                                        ctx=ast3.Load(),
                                                                                    )
                                                                                ),
                                                                                conversion=-1,
                                                                            )
                                                                        ),
                                                                        self.sync(
                                                                            ast3.Constant(
                                                                                value=absorb_exec
                                                                            )
                                                                        ),
                                                                        self.sync(
                                                                            ast3.FormattedValue(
                                                                                value=self.sync(
                                                                                    ast3.Name(
                                                                                        id="i",
                                                                                        ctx=ast3.Load(),
                                                                                    )
                                                                                ),
                                                                                conversion=-1,
                                                                            )
                                                                        ),
                                                                        self.sync(
                                                                            ast3.Constant(
                                                                                value="']"
                                                                            )
                                                                        ),
                                                                    ]
                                                                )
                                                            )
                                                        ],
                                                        keywords=[],
                                                    )
                                                )
                                            )
                                        )
                                    ],
                                    orelse=[],
                                )
                            )
                        ],
                        orelse=[],
                    )
                )
            )
        if node.is_absorb:
            source = node.items.items[0]
            if not isinstance(source, uni.ModulePath):
                raise self.ice()
            typecheck_nodes.append(
                self.sync(
                    py_node=ast3.ImportFrom(
                        module=(source.dot_path_str.lstrip(".") if source else None),
                        names=[self.sync(ast3.alias(name="*"), node)],
                        level=0,
                    ),
                    jac_node=node,
                )
            )
        elif not node.from_loc:
            typecheck_nodes.append(
                self.sync(
                    ast3.Import(
                        names=[cast(ast3.alias, x) for x in node.items.gen.py_ast]
                    )
                )
            )
        else:
            typecheck_nodes.append(
                self.sync(
                    ast3.ImportFrom(
                        module=(
                            node.from_loc.dot_path_str.lstrip(".")
                            if node.from_loc
                            else None
                        ),
                        names=[cast(ast3.alias, i) for i in node.items.gen.py_ast],
                        level=0,
                    )
                )
            )
        py_nodes.append(
            self.sync(
                ast3.If(
                    test=self.jaclib_obj("TYPE_CHECKING"),
                    body=[cast(ast3.stmt, node) for node in typecheck_nodes],
                    orelse=[cast(ast3.stmt, node) for node in runtime_nodes],
                )
            )
        )
        node.gen.py_ast = py_nodes

    def exit_module_path(self, node: uni.ModulePath) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.alias(
                    name=f"{node.dot_path_str}",
                    asname=node.alias.sym_name if node.alias else None,
                )
            )
        ]

    def exit_module_item(self, node: uni.ModuleItem) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.alias(
                    name=f"{node.name.sym_name}",
                    asname=node.alias.sym_name if node.alias else None,
                )
            )
        ]

    def enter_archetype(self, node: uni.Archetype) -> None:
        if isinstance(node.body, uni.ImplDef):
            self.traverse(node.body)

    def exit_archetype(self, node: uni.Archetype) -> None:
        body = self.resolve_stmt_block(
            (
                node.body.body
                if isinstance(node.body, uni.ImplDef)
                and isinstance(node.body.body, uni.SubNodeList)
                else node.body if isinstance(node.body, uni.SubNodeList) else None
            ),
            doc=node.doc,
        )

        if node.is_async:
            body.insert(
                0,
                self.sync(
                    ast3.Assign(
                        targets=[
                            self.sync(ast3.Name(id="__jac_async__", ctx=ast3.Store()))
                        ],
                        value=self.sync(ast3.Constant(value=node.is_async)),
                    )
                ),
            )

        decorators = (
            node.decorators.gen.py_ast
            if isinstance(node.decorators, uni.SubNodeList)
            else []
        )

        base_classes = node.base_classes.gen.py_ast if node.base_classes else []
        if node.arch_type.name != Tok.KW_CLASS:
            base_classes.append(self.jaclib_obj(node.arch_type.value.capitalize()))

        node.gen.py_ast = [
            self.sync(
                ast3.ClassDef(
                    name=node.name.sym_name,
                    bases=[cast(ast3.expr, i) for i in base_classes],
                    keywords=[],
                    body=[cast(ast3.stmt, i) for i in body],
                    decorator_list=[cast(ast3.expr, i) for i in decorators],
                    type_params=[],
                )
            )
        ]

    def enter_enum(self, node: uni.Enum) -> None:
        if isinstance(node.body, uni.ImplDef):
            self.traverse(node.body)

    def exit_enum(self, node: uni.Enum) -> None:
        self.needs_enum()
        body = self.resolve_stmt_block(
            (
                node.body.body
                if isinstance(node.body, uni.ImplDef)
                and isinstance(node.body.body, uni.SubNodeList)
                else node.body if isinstance(node.body, uni.SubNodeList) else None
            ),
            doc=node.doc,
        )
        decorators = (
            node.decorators.gen.py_ast
            if isinstance(node.decorators, uni.SubNodeList)
            else []
        )
        base_classes = node.base_classes.gen.py_ast if node.base_classes else []
        if isinstance(base_classes, list):
            base_classes.append(self.sync(ast3.Name(id="Enum", ctx=ast3.Load())))
        else:
            raise self.ice()
        node.gen.py_ast = [
            self.sync(
                ast3.ClassDef(
                    name=node.name.sym_name,
                    bases=[cast(ast3.expr, i) for i in base_classes],
                    keywords=[],
                    body=[cast(ast3.stmt, i) for i in body],
                    decorator_list=[cast(ast3.expr, i) for i in decorators],
                    type_params=[],
                )
            )
        ]

    def enter_ability(self, node: uni.Ability) -> None:
        if isinstance(node.body, uni.ImplDef):
            self.traverse(node.body)

    def gen_llm_body(self, node: uni.Ability) -> list[ast3.AST]:
        """Generate the by LLM body."""
        # to Avoid circular import
        from jaclang.runtimelib.machine import JacMachineInterface

        return JacMachineInterface.gen_llm_body(self, node)

    def exit_ability(self, node: uni.Ability) -> None:
        func_type = ast3.AsyncFunctionDef if node.is_async else ast3.FunctionDef
        body = (
            self.gen_llm_body(node)
            if isinstance(node.body, uni.FuncCall)
            or isinstance(node.body, uni.ImplDef)
            and isinstance(node.body.body, uni.FuncCall)
            else (
                [
                    self.sync(
                        ast3.Expr(value=cast(ast3.expr, node.doc.gen.py_ast[0])),
                        jac_node=node.doc,
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
                            if isinstance(node.body, uni.ImplDef)
                            and isinstance(node.body.body, uni.SubNodeList)
                            else node.body
                        ),
                        doc=node.doc,
                    )
                )
            )
        )
        if node.is_abstract and node.body:
            self.log_error(
                f"Abstract ability {node.sym_name} should not have a body.",
                node,
            )
        decorator_list = node.decorators.gen.py_ast if node.decorators else []
        if isinstance(node.signature, uni.EventSignature):
            decorator_list.append(
                self.jaclib_obj(
                    "entry" if node.signature.event.name == Tok.KW_ENTRY else "exit"
                )
            )

        if isinstance(node.body, uni.ImplDef):
            decorator_list.append(
                self.sync(
                    ast3.Call(
                        func=self.jaclib_obj("impl_patch_filename"),
                        args=[self.sync(ast3.Constant(value=node.body.loc.mod_path))],
                        keywords=[],
                    )
                )
            )
        if node.is_abstract:
            decorator_list.append(
                self.sync(ast3.Name(id="abstractmethod", ctx=ast3.Load()))
            )
        if node.is_override:
            decorator_list.append(self.sync(ast3.Name(id="override", ctx=ast3.Load())))
        if node.is_static:
            decorator_list.insert(
                0, self.sync(ast3.Name(id="staticmethod", ctx=ast3.Load()))
            )
        if not body and not isinstance(node.body, uni.FuncCall):
            self.log_error(
                "Ability has no body. Perhaps an impl must be imported.", node
            )
            body = [self.sync(ast3.Pass(), node)]

        node.gen.py_ast = [
            self.sync(
                func_type(
                    name=node.name_ref.sym_name,
                    args=(
                        cast(ast3.arguments, node.signature.gen.py_ast[0])
                        if node.signature
                        else self.sync(
                            ast3.arguments(
                                posonlyargs=[],
                                args=(
                                    [self.sync(ast3.arg(arg="self", annotation=None))]
                                    if node.is_method
                                    else []
                                ),
                                vararg=None,
                                kwonlyargs=[],
                                kw_defaults=[],
                                kwarg=None,
                                defaults=[],
                            )
                        )
                    ),
                    body=[cast(ast3.stmt, i) for i in body],
                    decorator_list=[cast(ast3.expr, i) for i in decorator_list],
                    returns=(
                        cast(ast3.expr, node.signature.return_type.gen.py_ast[0])
                        if node.signature and node.signature.return_type
                        else self.sync(ast3.Constant(value=None))
                    ),
                    type_params=[],
                )
            )
        ]

    def exit_impl_def(self, node: uni.ImplDef) -> None:
        pass

    def exit_func_signature(self, node: uni.FuncSignature) -> None:
        params = (
            [self.sync(ast3.arg(arg="self", annotation=None))]
            if (abl := node.find_parent_of_type(uni.Ability))
            and abl.is_method
            and not node.is_static
            and not node.is_in_py_class
            else []
        )
        vararg = None
        kwarg = None
        if isinstance(node.params, uni.SubNodeList):
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
                    args=[cast(ast3.arg, param) for param in params],
                    kwonlyargs=[],
                    vararg=cast(ast3.arg, vararg) if vararg else None,
                    kwarg=cast(ast3.arg, kwarg) if kwarg else None,
                    kw_defaults=[],
                    defaults=[cast(ast3.expr, default) for default in defaults],
                )
            )
        ]

    def exit_event_signature(self, node: uni.EventSignature) -> None:
        here = self.sync(
            ast3.arg(
                arg=f"{Con.HERE.value}",
                annotation=(
                    cast(ast3.expr, node.arch_tag_info.gen.py_ast[0])
                    if node.arch_tag_info
                    else None
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
                        if (abl := node.find_parent_of_type(uni.Ability))
                        and abl.is_method
                        else [here]
                    ),
                    kwonlyargs=[],
                    vararg=None,
                    kwarg=None,
                    kw_defaults=[],
                    defaults=[],
                )
            )
        ]

    def exit_type_ref(self, node: uni.TypeRef) -> None:
        if (
            isinstance(node.target, uni.SpecialVarRef)
            and node.target.orig.name == Tok.KW_ROOT
        ):
            node.gen.py_ast = [self.jaclib_obj("Root")]
        else:
            self.needs_typing()
            node.gen.py_ast = [
                self.sync(
                    ast3.Attribute(
                        value=self.sync(ast3.Name(id="typing", ctx=ast3.Load())),
                        attr=node.target.sym_name,
                        ctx=ast3.Load(),
                    )
                )
            ]

    def exit_param_var(self, node: uni.ParamVar) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.arg(
                    arg=node.name.sym_name,
                    annotation=(
                        cast(ast3.expr, node.type_tag.gen.py_ast[0])
                        if node.type_tag
                        else None
                    ),
                )
            )
        ]

    def exit_arch_has(self, node: uni.ArchHas) -> None:
        if node.doc:
            doc = self.sync(
                ast3.Expr(value=cast(ast3.expr, node.doc.gen.py_ast[0])),
                jac_node=node.doc,
            )
            if isinstance(doc, ast3.AST) and isinstance(node.vars.gen.py_ast, list):
                node.gen.py_ast = [doc] + node.vars.gen.py_ast
            else:
                raise self.ice()
        else:
            node.gen.py_ast = node.vars.gen.py_ast  # TODO: This is a list

    def exit_has_var(self, node: uni.HasVar) -> None:
        annotation = node.type_tag.gen.py_ast[0] if node.type_tag else None

        is_static_var = (
            node.parent
            and node.parent.parent
            and isinstance(node.parent.parent, uni.ArchHas)
            and node.parent.parent.is_static
        )

        is_in_class = (
            node.parent
            and node.parent.parent
            and node.parent.parent.parent
            and (
                (
                    isinstance(node.parent.parent.parent, uni.Archetype)
                    and node.parent.parent.parent.arch_type.name == Tok.KW_CLASS
                )
                or (
                    node.parent.parent.parent.parent
                    and isinstance(node.parent.parent.parent.parent, uni.Archetype)
                    and node.parent.parent.parent.parent.arch_type.name == Tok.KW_CLASS
                )
            )
        )

        value = None

        if is_in_class:
            value = cast(ast3.expr, node.value.gen.py_ast[0]) if node.value else None
        elif is_static_var:
            annotation = self.sync(
                ast3.Subscript(
                    value=self.sync(ast3.Name(id="ClassVar", ctx=ast3.Load())),
                    slice=cast(ast3.expr, annotation),
                    ctx=ast3.Load(),
                )
            )
            value = cast(ast3.expr, node.value.gen.py_ast[0]) if node.value else None
        elif node.defer:
            value = self.sync(
                ast3.Call(
                    func=self.jaclib_obj("field"),
                    args=[],
                    keywords=[
                        self.sync(
                            ast3.keyword(
                                arg="init",
                                value=self.sync(ast3.Constant(value=False)),
                            )
                        )
                    ],
                ),
            )
        elif node.value:
            if isinstance(node.value.gen.py_ast[0], ast3.Constant):
                value = cast(ast3.expr, node.value.gen.py_ast[0])
            else:
                value = self.sync(
                    ast3.Call(
                        func=self.jaclib_obj("field"),
                        args=[],
                        keywords=[
                            self.sync(
                                ast3.keyword(
                                    arg="factory",
                                    value=self.sync(
                                        ast3.Lambda(
                                            args=self.sync(
                                                ast3.arguments(
                                                    posonlyargs=[],
                                                    args=[],
                                                    kwonlyargs=[],
                                                    vararg=None,
                                                    kwarg=None,
                                                    kw_defaults=[],
                                                    defaults=[],
                                                )
                                            ),
                                            body=cast(
                                                ast3.expr,
                                                node.value.gen.py_ast[0],
                                            ),
                                        )
                                    ),
                                ),
                            )
                        ],
                    ),
                )

        node.gen.py_ast = [
            self.sync(
                ast3.AnnAssign(
                    target=cast(
                        ast3.Name | ast3.Attribute | ast3.Subscript,
                        node.name.gen.py_ast[0],
                    ),
                    annotation=(
                        cast(ast3.expr, annotation)
                        if annotation
                        else ast3.Constant(value=None)
                    ),
                    value=value,
                    simple=int(isinstance(node.name, uni.Name)),
                )
            )
        ]

    def exit_typed_ctx_block(self, node: uni.TypedCtxBlock) -> None:
        # TODO: Come back
        pass

    def exit_if_stmt(self, node: uni.IfStmt) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.If(
                    test=cast(ast3.expr, node.condition.gen.py_ast[0]),
                    body=cast(list[ast3.stmt], self.resolve_stmt_block(node.body)),
                    orelse=(
                        cast(list[ast3.stmt], node.else_body.gen.py_ast)
                        if node.else_body
                        else []
                    ),
                )
            )
        ]

    def exit_else_if(self, node: uni.ElseIf) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.If(
                    test=cast(ast3.expr, node.condition.gen.py_ast[0]),
                    body=cast(list[ast3.stmt], self.resolve_stmt_block(node.body)),
                    orelse=(
                        cast(list[ast3.stmt], node.else_body.gen.py_ast)
                        if node.else_body
                        else []
                    ),
                )
            )
        ]

    def exit_else_stmt(self, node: uni.ElseStmt) -> None:
        node.gen.py_ast = self.resolve_stmt_block(node.body)

    def exit_expr_stmt(self, node: uni.ExprStmt) -> None:
        node.gen.py_ast = [
            (
                self.sync(ast3.Expr(value=cast(ast3.expr, node.expr.gen.py_ast[0])))
                if not node.in_fstring
                else self.sync(
                    ast3.FormattedValue(
                        value=cast(ast3.expr, node.expr.gen.py_ast[0]),
                        conversion=-1,
                        format_spec=None,
                    )
                )
            )
        ]

    def exit_concurrent_expr(self, node: uni.ConcurrentExpr) -> None:
        func = ""
        if node.tok:
            match node.tok.value:
                case "flow":
                    func = "thread_run"
                case "wait":
                    func = "thread_wait"
        if func:
            lambda_ex = [
                self.sync(
                    ast3.Lambda(
                        args=(
                            self.sync(
                                ast3.arguments(
                                    posonlyargs=[],
                                    args=[],
                                    kwonlyargs=[],
                                    kw_defaults=[],
                                    defaults=[],
                                )
                            )
                        ),
                        body=cast(ast3.expr, node.target.gen.py_ast[0]),
                    )
                )
            ]
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.jaclib_obj(func),
                        args=cast(
                            list[ast3.expr],
                            (
                                lambda_ex
                                if func == "thread_run"
                                else [node.target.gen.py_ast[0]]  # type: ignore
                            ),
                        ),
                        keywords=[],
                    )
                )
            ]

    def exit_try_stmt(self, node: uni.TryStmt) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Try(
                    body=cast(list[ast3.stmt], self.resolve_stmt_block(node.body)),
                    handlers=(
                        [cast(ast3.ExceptHandler, i) for i in node.excepts.gen.py_ast]
                        if node.excepts
                        else []
                    ),
                    orelse=(
                        [cast(ast3.stmt, i) for i in node.else_body.gen.py_ast]
                        if node.else_body
                        else []
                    ),
                    finalbody=(
                        [cast(ast3.stmt, i) for i in node.finally_body.gen.py_ast]
                        if node.finally_body
                        else []
                    ),
                )
            )
        ]

    def exit_except(self, node: uni.Except) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.ExceptHandler(
                    type=(
                        cast(ast3.expr, node.ex_type.gen.py_ast[0])
                        if node.ex_type
                        else None
                    ),
                    name=node.name.sym_name if node.name else None,
                    body=[
                        cast(ast3.stmt, stmt)
                        for stmt in self.resolve_stmt_block(node.body)
                    ],
                )
            )
        ]

    def exit_finally_stmt(self, node: uni.FinallyStmt) -> None:
        node.gen.py_ast = self.resolve_stmt_block(node.body)

    def exit_iter_for_stmt(self, node: uni.IterForStmt) -> None:
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
                    test=cast(ast3.expr, node.condition.gen.py_ast[0]),
                    body=[cast(ast3.stmt, stmt) for stmt in body],
                    orelse=(
                        [cast(ast3.stmt, stmt) for stmt in node.else_body.gen.py_ast]
                        if node.else_body
                        else []
                    ),
                )
            )
        )
        node.gen.py_ast = py_nodes

    def exit_in_for_stmt(self, node: uni.InForStmt) -> None:
        for_node = ast3.AsyncFor if node.is_async else ast3.For
        node.gen.py_ast = [
            self.sync(
                for_node(
                    target=cast(ast3.expr, node.target.gen.py_ast[0]),
                    iter=cast(ast3.expr, node.collection.gen.py_ast[0]),
                    body=[
                        cast(ast3.stmt, stmt)
                        for stmt in self.resolve_stmt_block(node.body)
                    ],
                    orelse=(
                        [cast(ast3.stmt, stmt) for stmt in node.else_body.gen.py_ast]
                        if node.else_body
                        else []
                    ),
                )
            )
        ]

    def exit_while_stmt(self, node: uni.WhileStmt) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.While(
                    test=cast(ast3.expr, node.condition.gen.py_ast[0]),
                    body=[
                        cast(ast3.stmt, stmt)
                        for stmt in self.resolve_stmt_block(node.body)
                    ],
                    orelse=[],
                )
            )
        ]

    def exit_with_stmt(self, node: uni.WithStmt) -> None:
        with_node = ast3.AsyncWith if node.is_async else ast3.With
        node.gen.py_ast = [
            self.sync(
                with_node(
                    items=[cast(ast3.withitem, item) for item in node.exprs.gen.py_ast],
                    body=[
                        cast(ast3.stmt, stmt)
                        for stmt in self.resolve_stmt_block(node.body)
                    ],
                )
            )
        ]

    def exit_expr_as_item(self, node: uni.ExprAsItem) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.withitem(
                    context_expr=cast(ast3.expr, node.expr.gen.py_ast[0]),
                    optional_vars=(
                        cast(ast3.expr, node.alias.gen.py_ast[0])
                        if node.alias
                        else None
                    ),
                )
            )
        ]

    def exit_raise_stmt(self, node: uni.RaiseStmt) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Raise(
                    exc=(
                        cast(ast3.expr, node.cause.gen.py_ast[0])
                        if node.cause
                        else None
                    ),
                    cause=(
                        cast(ast3.expr, node.from_target.gen.py_ast[0])
                        if node.from_target
                        else None
                    ),
                )
            )
        ]

    def exit_assert_stmt(self, node: uni.AssertStmt) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Assert(
                    test=cast(ast3.expr, node.condition.gen.py_ast[0]),
                    msg=(
                        cast(ast3.expr, node.error_msg.gen.py_ast[0])
                        if node.error_msg
                        else None
                    ),
                )
            )
        ]

    def exit_check_stmt(self, node: uni.CheckStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        # TODO: Here is the list of assertions which are not implemented instead a simpler version of them will work.
        # ie. [] == [] will be assertEqual instead of assertListEqual. However I don't think this is needed since it can
        # only detected if both operand are compile time literal list or type inferable.
        #
        #   assertAlmostEqual
        #   assertNotAlmostEqual
        #   assertSequenceEqual
        #   assertListEqual
        #   assertTupleEqual
        #   assertSetEqual
        #   assertDictEqual
        #   assertCountEqual
        #   assertMultiLineEqual
        #   assertRaisesRegex
        #   assertWarnsRegex
        #   assertRegex
        #   assertNotRegex

        # The return type "struct" for the bellow check_node_isinstance_call.
        @dataclass
        class CheckNodeIsinstanceCallResult:
            isit: bool = False
            inst: ast3.AST | None = None
            clss: ast3.AST | None = None

        # This will check if a node is `isinstance(<expr>, <expr>)`, we're
        # using a function because it's reusable to check not isinstance(<expr>, <expr>).
        def check_node_isinstance_call(
            node: uni.FuncCall,
        ) -> CheckNodeIsinstanceCallResult:

            # Ensure the type of the FuncCall node is SubNodeList[Expr]
            # since the type can be: Optional[SubNodeList[Expr | KWPair]].
            if not (
                node.params is not None
                and len(node.params.items) == 2
                and isinstance(node.params.items[0], uni.Expr)
                and isinstance(node.params.items[1], uni.Expr)
            ):
                return CheckNodeIsinstanceCallResult()

            func = node.target.gen.py_ast[0]
            if not (isinstance(func, ast3.Name) and func.id == "isinstance"):
                return CheckNodeIsinstanceCallResult()

            return CheckNodeIsinstanceCallResult(
                True,
                node.params.items[0].gen.py_ast[0],
                node.params.items[1].gen.py_ast[0],
            )

        # By default the check expression will become assertTrue(<expr>), unless any pattern detected.
        assert_func_name = "assertTrue"
        assert_args_list = node.target.gen.py_ast

        # Compare operations. Note that We're only considering the compare
        # operation with a single operation ie. a < b < c is  ignored here.
        if (
            isinstance(node.target, uni.CompareExpr)
            and isinstance(node.target.gen.py_ast[0], ast3.Compare)
            and len(node.target.ops) == 1
        ):
            expr: uni.CompareExpr = node.target
            opty: uni.Token = expr.ops[0]

            optype2fn = {
                Tok.EE.name: "assertEqual",
                Tok.NE.name: "assertNotEqual",
                Tok.LT.name: "assertLess",
                Tok.LTE.name: "assertLessEqual",
                Tok.GT.name: "assertGreater",
                Tok.GTE.name: "assertGreaterEqual",
                Tok.KW_IN.name: "assertIn",
                Tok.KW_NIN.name: "assertNotIn",
                Tok.KW_IS.name: "assertIs",
                Tok.KW_ISN.name: "assertIsNot",
            }

            if opty.name in optype2fn:
                assert_func_name = optype2fn[opty.name]
                assert_args_list = [
                    expr.left.gen.py_ast[0],
                    expr.rights[0].gen.py_ast[0],
                ]

                # Override for <expr> is None.
                if opty.name == Tok.KW_IS and isinstance(expr.rights[0], uni.Null):
                    assert_func_name = "assertIsNone"
                    assert_args_list.pop()

                # Override for <expr> is not None.
                elif opty.name == Tok.KW_ISN and isinstance(expr.rights[0], uni.Null):
                    assert_func_name = "assertIsNotNone"
                    assert_args_list.pop()

        # Check if 'isinstance' is called.
        elif isinstance(node.target, uni.FuncCall) and isinstance(
            node.target.gen.py_ast[0], ast3.Call
        ):
            res = check_node_isinstance_call(node.target)
            if res.isit:
                # These assertions will make mypy happy.
                assert isinstance(res.inst, ast3.AST)
                assert isinstance(res.clss, ast3.AST)
                assert_func_name = "assertIsInstance"
                assert_args_list = [res.inst, res.clss]

        # Check if 'not isinstance(<expr>, <expr>)' is called.
        elif (
            isinstance(node.target, uni.UnaryExpr)
            and isinstance(node.target, uni.UnaryExpr)
            and isinstance(node.target.operand, uni.FuncCall)
            and isinstance(node.target.operand, uni.UnaryExpr)
        ):
            res = check_node_isinstance_call(node.target.operand)
            if res.isit:
                # These assertions will make mypy happy.
                assert isinstance(res.inst, ast3.AST)
                assert isinstance(res.clss, ast3.AST)
                assert_func_name = "assertIsNotInstance"
                assert_args_list = [res.inst, res.clss]

        # NOTE That the almost equal is NOT a builtin function of jaclang and won't work outside of the
        # check statement. And we're hacking the node here. Not sure if this is a hacky workaround to support
        # the almost equal functionality (snice there is no almost equal operator in jac and never needed ig.).

        # Check if 'almostEqual' is called.
        if isinstance(node.target, uni.FuncCall) and isinstance(
            node.target.gen.py_ast[0], ast3.Call
        ):
            func = node.target.target
            if isinstance(func, uni.Name) and func.value == "almostEqual":
                assert_func_name = "assertAlmostEqual"
                assert_args_list = []
                if node.target.params is not None:
                    for param in node.target.params.items:
                        assert_args_list.append(param.gen.py_ast[0])

        # assert_func_expr = "Con.JAC_CHECK.value.assertXXX"
        assert_func_expr: ast3.Attribute = self.sync(
            ast3.Attribute(
                value=self.sync(ast3.Name(id=Con.JAC_CHECK.value, ctx=ast3.Load())),
                attr=assert_func_name,
                ctx=ast3.Load(),
            )
        )

        # assert_call_expr = "(Con.JAC_CHECK.value.assertXXX)(args)"
        assert_call_expr: ast3.Call = self.sync(
            ast3.Call(
                func=assert_func_expr,
                args=[cast(ast3.expr, arg) for arg in assert_args_list],
                keywords=[],
            )
        )

        node.gen.py_ast = [self.sync(ast3.Expr(assert_call_expr))]

    def exit_ctrl_stmt(self, node: uni.CtrlStmt) -> None:
        if node.ctrl.name == Tok.KW_BREAK:
            node.gen.py_ast = [self.sync(ast3.Break())]
        elif node.ctrl.name == Tok.KW_CONTINUE:
            node.gen.py_ast = [self.sync(ast3.Continue())]
        elif node.ctrl.name == Tok.KW_SKIP:
            node.gen.py_ast = [self.sync(ast3.Return(value=None))]

    def exit_delete_stmt(self, node: uni.DeleteStmt) -> None:
        def set_ctx(
            targets: Union[ast3.AST, List[ast3.AST]], ctx: type
        ) -> List[ast3.AST]:
            """Set the given ctx (Load, Del) to AST node(s)."""
            if not isinstance(targets, list):
                targets = [targets]
            elif isinstance(targets[0], (ast3.List, ast3.Tuple)):
                targets = [i for i in targets[0].elts if isinstance(i, ast3.AST)]
            result = []
            for target in targets:
                if hasattr(target, "ctx"):
                    target = copy.copy(target)
                    target.ctx = ctx()
                result.append(target)
            return result

        destroy_expr = ast3.Expr(
            value=self.sync(
                ast3.Call(
                    func=self.jaclib_obj("destroy"),
                    args=[
                        self.sync(
                            ast3.List(
                                elts=cast(
                                    list[ast3.expr],
                                    set_ctx(node.py_ast_targets, ast3.Load),
                                ),
                                ctx=ast3.Load(),
                            )
                        )
                    ],
                    keywords=[],
                )
            )
        )
        delete_stmt = self.sync(
            ast3.Delete(
                targets=cast(list[ast3.expr], set_ctx(node.py_ast_targets, ast3.Del))
            )
        )
        node.gen.py_ast = [self.sync(destroy_expr), self.sync(delete_stmt)]

    def exit_report_stmt(self, node: uni.ReportStmt) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Expr(
                    value=self.sync(
                        self.sync(
                            ast3.Call(
                                func=self.jaclib_obj("report"),
                                args=cast(list[ast3.expr], node.expr.gen.py_ast),
                                keywords=[],
                            )
                        )
                    )
                )
            )
        ]

    def exit_return_stmt(self, node: uni.ReturnStmt) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Return(
                    value=(
                        cast(ast3.expr, node.expr.gen.py_ast[0]) if node.expr else None
                    )
                )
            )
        ]

    def exit_yield_expr(self, node: uni.YieldExpr) -> None:
        if not node.with_from:
            node.gen.py_ast = [
                self.sync(
                    ast3.Yield(
                        value=(
                            cast(ast3.expr, node.expr.gen.py_ast[0])
                            if node.expr
                            else None
                        )
                    )
                )
            ]
        else:
            node.gen.py_ast = [
                self.sync(
                    ast3.YieldFrom(
                        value=(
                            cast(ast3.expr, node.expr.gen.py_ast[0])
                            if node.expr
                            else self.sync(ast3.Constant(value=None))
                        )
                    )
                )
            ]

    def exit_ignore_stmt(self, node: uni.IgnoreStmt) -> None:
        walker = self.sync(
            ast3.Name(id="self", ctx=ast3.Load())
            if node.from_walker
            else ast3.Name(id=Con.HERE.value, ctx=ast3.Load())
        )

        node.gen.py_ast = [
            self.sync(
                ast3.Expr(
                    value=self.sync(
                        ast3.Call(
                            func=self.jaclib_obj("ignore"),
                            args=cast(
                                list[ast3.expr], [walker, node.target.gen.py_ast[0]]
                            ),
                            keywords=[],
                        )
                    )
                )
            )
        ]

    def exit_visit_stmt(self, node: uni.VisitStmt) -> None:
        loc = self.sync(
            ast3.Name(id="self", ctx=ast3.Load())
            if node.from_walker
            else ast3.Name(id=Con.HERE.value, ctx=ast3.Load())
        )

        visit_call = self.sync(
            ast3.Call(
                func=self.jaclib_obj("visit"),
                args=cast(list[ast3.expr], [loc, node.target.gen.py_ast[0]]),
                keywords=[],
            )
        )

        node.gen.py_ast = [
            (
                self.sync(
                    ast3.If(
                        test=self.sync(
                            ast3.UnaryOp(
                                op=self.sync(ast3.Not()),
                                operand=visit_call,
                            )
                        ),
                        body=cast(list[ast3.stmt], node.else_body.gen.py_ast),
                        orelse=[],
                    )
                )
                if node.else_body
                else self.sync(ast3.Expr(value=visit_call))
            )
        ]

    def exit_disengage_stmt(self, node: uni.DisengageStmt) -> None:
        loc = self.sync(
            ast3.Name(id="self", ctx=ast3.Load())
            if node.from_walker
            else ast3.Name(id=Con.HERE.value, ctx=ast3.Load())
        )
        node.gen.py_ast = [
            self.sync(
                ast3.Expr(
                    self.sync(
                        ast3.Call(
                            func=self.jaclib_obj("disengage"),
                            args=[loc],
                            keywords=[],
                        )
                    )
                )
            ),
            self.sync(ast3.Return()),
        ]

    def exit_await_expr(self, node: uni.AwaitExpr) -> None:
        parent_node = node.parent
        while parent_node and (parent_node := parent_node.parent):
            if hasattr(parent_node, "is_async") and parent_node.is_async:
                node.gen.py_ast = [
                    self.sync(
                        ast3.Await(value=cast(ast3.expr, node.target.gen.py_ast[0]))
                    )
                ]
                break
        else:
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.jaclib_obj("await_obj"),
                        args=[cast(ast3.expr, node.target.gen.py_ast[0])],
                        keywords=[],
                    )
                )
            ]

    def exit_global_stmt(self, node: uni.GlobalStmt) -> None:
        py_nodes = []
        for x in node.target.items:
            py_nodes.append(
                self.sync(
                    ast3.Global(names=[x.sym_name]),
                    jac_node=x,
                )
            )
        node.gen.py_ast = [*py_nodes]

    def exit_non_local_stmt(self, node: uni.NonLocalStmt) -> None:
        py_nodes = []
        for x in node.target.items:
            py_nodes.append(
                self.sync(
                    ast3.Nonlocal(names=[x.sym_name]),
                    jac_node=x,
                )
            )
        node.gen.py_ast = [*py_nodes]

    def exit_assignment(self, node: uni.Assignment) -> None:
        value = (
            node.value.gen.py_ast[0]
            if node.value
            else (
                self.sync(
                    ast3.Call(
                        func=self.sync(ast3.Name(id="auto", ctx=ast3.Load())),
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
                        target=cast(ast3.Name, node.target.items[0].gen.py_ast[0]),
                        annotation=cast(ast3.expr, node.type_tag.gen.py_ast[0]),
                        value=(
                            cast(ast3.expr, node.value.gen.py_ast[0])
                            if node.value
                            else None
                        ),
                        simple=int(isinstance(node.target.gen.py_ast[0], ast3.Name)),
                    )
                )
            ]
        elif node.aug_op:
            node.gen.py_ast = [
                self.sync(
                    ast3.AugAssign(
                        target=cast(ast3.Name, node.target.items[0].gen.py_ast[0]),
                        op=cast(ast3.operator, node.aug_op.gen.py_ast[0]),
                        value=(
                            cast(ast3.expr, value)
                            if isinstance(value, ast3.expr)
                            else ast3.Constant(value=None)
                        ),
                    )
                )
            ]
        else:
            node.gen.py_ast = [
                self.sync(
                    ast3.Assign(
                        targets=cast(list[ast3.expr], node.target.gen.py_ast),
                        value=(
                            cast(ast3.expr, value)
                            if isinstance(value, ast3.expr)
                            else ast3.Constant(value=None)
                        ),
                    )
                )
            ]

    def exit_binary_expr(self, node: uni.BinaryExpr) -> None:
        if isinstance(node.op, uni.ConnectOp):
            left = (
                node.right.gen.py_ast[0]
                if node.op.edge_dir == EdgeDir.IN
                else node.left.gen.py_ast[0]
            )
            right = (
                node.left.gen.py_ast[0]
                if node.op.edge_dir == EdgeDir.IN
                else node.right.gen.py_ast[0]
            )

            keywords = [
                self.sync(ast3.keyword(arg="left", value=cast(ast3.expr, left))),
                self.sync(ast3.keyword(arg="right", value=cast(ast3.expr, right))),
            ]

            if node.op.conn_type:
                keywords.append(
                    self.sync(
                        ast3.keyword(
                            arg="edge",
                            value=cast(ast3.expr, node.op.conn_type.gen.py_ast[0]),
                        )
                    )
                )

            if node.op.edge_dir == EdgeDir.ANY:
                keywords.append(
                    self.sync(
                        ast3.keyword(
                            arg="undir", value=self.sync(ast3.Constant(value=True))
                        )
                    )
                )

            if node.op.conn_assign:
                keywords.append(
                    self.sync(
                        ast3.keyword(
                            arg="conn_assign",
                            value=cast(ast3.expr, node.op.conn_assign.gen.py_ast[0]),
                        )
                    )
                )

            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.jaclib_obj("connect"),
                        args=[],
                        keywords=keywords,
                    )
                )
            ]

        elif isinstance(node.op, uni.DisconnectOp):
            keywords = [
                self.sync(
                    ast3.keyword(
                        arg="left", value=cast(ast3.expr, node.left.gen.py_ast[0])
                    )
                ),
                self.sync(
                    ast3.keyword(
                        arg="right", value=cast(ast3.expr, node.right.gen.py_ast[0])
                    )
                ),
            ]

            if node.op.edge_spec.edge_dir != EdgeDir.OUT:
                keywords.append(
                    self.sync(
                        ast3.keyword(
                            arg="EdgeDir",
                            value=self.sync(
                                ast3.Attribute(
                                    value=self.jaclib_obj("EdgeDir"),
                                    attr=node.op.edge_spec.edge_dir.name,
                                    ctx=ast3.Load(),
                                )
                            ),
                        )
                    )
                )

            if node.op.edge_spec.filter_cond:
                keywords.append(
                    self.sync(
                        ast3.keyword(
                            arg="filter",
                            value=cast(
                                ast3.expr,
                                node.op.edge_spec.filter_cond.gen.py_ast[0],
                            ),
                        ),
                    )
                )

            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.jaclib_obj("disconnect"),
                        args=[],
                        keywords=keywords,
                    )
                )
            ]
        elif node.op.name in [Tok.KW_AND.value, Tok.KW_OR.value]:
            node.gen.py_ast = [
                self.sync(
                    ast3.BoolOp(
                        op=cast(ast3.boolop, node.op.gen.py_ast[0]),
                        values=[
                            cast(ast3.expr, node.left.gen.py_ast[0]),
                            cast(ast3.expr, node.right.gen.py_ast[0]),
                        ],
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
                        target=cast(ast3.Name, node.left.gen.py_ast[0]),
                        value=cast(ast3.expr, node.right.gen.py_ast[0]),
                    )
                )
            ]
        elif node.op.gen.py_ast and isinstance(node.op.gen.py_ast[0], ast3.AST):
            node.gen.py_ast = [
                self.sync(
                    ast3.BinOp(
                        left=cast(ast3.expr, node.left.gen.py_ast[0]),
                        right=cast(ast3.expr, node.right.gen.py_ast[0]),
                        op=cast(ast3.operator, node.op.gen.py_ast[0]),
                    )
                )
            ]
        else:
            node.gen.py_ast = self.translate_jac_bin_op(node)

    def translate_jac_bin_op(self, node: uni.BinaryExpr) -> list[ast3.AST]:
        if isinstance(node.op, (uni.DisconnectOp, uni.ConnectOp)):
            raise self.ice()
        elif node.op.name in [
            Tok.PIPE_FWD,
            Tok.A_PIPE_FWD,
        ]:
            func_node = uni.FuncCall(
                target=node.right,
                params=(
                    node.left.values
                    if isinstance(node.left, uni.TupleVal)
                    else uni.SubNodeList(
                        items=[node.left], delim=Tok.COMMA, kid=[node.left]
                    )
                ),
                genai_call=None,
                kid=node.kid,
            )
            func_node.parent = node.parent
            self.exit_func_call(func_node)
            return func_node.gen.py_ast
        elif node.op.name in [Tok.KW_SPAWN]:
            return [
                self.sync(
                    ast3.Call(
                        func=self.jaclib_obj("spawn"),
                        args=cast(
                            list[ast3.expr],
                            [node.left.gen.py_ast[0], node.right.gen.py_ast[0]],
                        ),
                        keywords=[],
                    )
                )
            ]
        elif node.op.name in [
            Tok.PIPE_BKWD,
            Tok.A_PIPE_BKWD,
        ]:
            func_node = uni.FuncCall(
                target=node.left,
                params=(
                    node.right.values
                    if isinstance(node.right, uni.TupleVal)
                    else uni.SubNodeList(
                        items=[node.right], delim=Tok.COMMA, kid=[node.right]
                    )
                ),
                genai_call=None,
                kid=node.kid,
            )
            func_node.parent = node.parent
            self.exit_func_call(func_node)
            return func_node.gen.py_ast
        elif node.op.name == Tok.PIPE_FWD and isinstance(node.right, uni.TupleVal):
            self.log_error("Invalid pipe target.")
        else:
            self.log_error(
                f"Binary operator {node.op.value} not supported in bootstrap Jac"
            )
        return []

    def exit_compare_expr(self, node: uni.CompareExpr) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Compare(
                    left=cast(ast3.expr, node.left.gen.py_ast[0]),
                    comparators=[cast(ast3.expr, i.gen.py_ast[0]) for i in node.rights],
                    ops=[cast(ast3.cmpop, i.gen.py_ast[0]) for i in node.ops],
                )
            )
        ]

    def exit_bool_expr(self, node: uni.BoolExpr) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.BoolOp(
                    op=cast(ast3.boolop, node.op.gen.py_ast[0]),
                    values=[cast(ast3.expr, i.gen.py_ast[0]) for i in node.values],
                )
            )
        ]

    def exit_lambda_expr(self, node: uni.LambdaExpr) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Lambda(
                    args=(
                        cast(ast3.arguments, node.signature.gen.py_ast[0])
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
                    body=cast(ast3.expr, node.body.gen.py_ast[0]),
                )
            )
        ]

    def exit_unary_expr(self, node: uni.UnaryExpr) -> None:
        if node.op.name == Tok.NOT:
            node.gen.py_ast = [
                self.sync(
                    ast3.UnaryOp(
                        op=self.sync(ast3.Not()),
                        operand=cast(ast3.expr, node.operand.gen.py_ast[0]),
                    )
                )
            ]
        elif node.op.name == Tok.BW_NOT:
            node.gen.py_ast = [
                self.sync(
                    ast3.UnaryOp(
                        op=self.sync(ast3.Invert()),
                        operand=cast(ast3.expr, node.operand.gen.py_ast[0]),
                    )
                )
            ]
        elif node.op.name == Tok.PLUS:
            node.gen.py_ast = [
                self.sync(
                    ast3.UnaryOp(
                        op=self.sync(ast3.UAdd()),
                        operand=cast(ast3.expr, node.operand.gen.py_ast[0]),
                    )
                )
            ]
        elif node.op.name == Tok.MINUS:
            node.gen.py_ast = [
                self.sync(
                    ast3.UnaryOp(
                        op=self.sync(ast3.USub()),
                        operand=cast(ast3.expr, node.operand.gen.py_ast[0]),
                    )
                )
            ]
        elif node.op.name in [Tok.PIPE_FWD, Tok.KW_SPAWN, Tok.A_PIPE_FWD]:
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=cast(ast3.expr, node.operand.gen.py_ast[0]),
                        args=[],
                        keywords=[],
                    )
                )
            ]
        elif node.op.name in [Tok.STAR_MUL]:
            ctx_val = (
                node.operand.py_ctx_func()
                if isinstance(node.operand, uni.AstSymbolNode)
                else ast3.Load()
            )
            node.gen.py_ast = [
                self.sync(
                    ast3.Starred(
                        value=cast(ast3.expr, node.operand.gen.py_ast[0]),
                        ctx=cast(ast3.expr_context, ctx_val),
                    )
                )
            ]
        elif node.op.name in [Tok.STAR_POW]:
            node.gen.py_ast = node.operand.gen.py_ast
        elif node.op.name in [Tok.BW_AND]:
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.sync(ast3.Name(id="jobj", ctx=ast3.Load())),
                        args=[],
                        keywords=[
                            self.sync(
                                ast3.keyword(
                                    arg="id",
                                    value=cast(ast3.expr, node.operand.gen.py_ast[0]),
                                )
                            ),
                        ],
                    )
                )
            ]
        else:
            self.ice(f"Unknown Unary operator {node.op.value}")

    def exit_if_else_expr(self, node: uni.IfElseExpr) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.IfExp(
                    test=cast(ast3.expr, node.condition.gen.py_ast[0]),
                    body=cast(ast3.expr, node.value.gen.py_ast[0]),
                    orelse=cast(ast3.expr, node.else_value.gen.py_ast[0]),
                )
            )
        ]

    def exit_multi_string(self, node: uni.MultiString) -> None:
        def get_pieces(str_seq: Sequence) -> list[str | ast3.AST]:
            pieces: list[str | ast3.AST] = []
            for i in str_seq:
                if isinstance(i, uni.String):
                    pieces.append(i.lit_value)
                elif isinstance(i, uni.FString):
                    pieces.extend(get_pieces(i.parts.items)) if i.parts else None
                elif isinstance(i, uni.ExprStmt):
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
                        values=[cast(ast3.expr, node) for node in combined_multi],
                    )
                )
            ]
        else:
            node.gen.py_ast = [combined_multi[0]]

    def exit_f_string(self, node: uni.FString) -> None:
        node.gen.py_ast = (
            node.parts.gen.py_ast
            if node.parts
            else [self.sync(ast3.Constant(value=""))]
        )

    def exit_list_val(self, node: uni.ListVal) -> None:
        if isinstance(node.py_ctx_func(), ast3.Load):
            node.gen.py_ast = [
                self.sync(
                    ast3.List(
                        elts=(
                            cast(list[ast3.expr], node.values.gen.py_ast)
                            if node.values
                            else []
                        ),
                        ctx=ast3.Load(),
                    )
                )
            ]
        else:
            node.gen.py_ast = [
                self.sync(
                    ast3.List(
                        elts=(
                            [cast(ast3.expr, item) for item in node.values.gen.py_ast]
                            if node.values and node.values.gen.py_ast
                            else []
                        ),
                        ctx=cast(ast3.expr_context, node.py_ctx_func()),
                    )
                )
            ]

    def exit_set_val(self, node: uni.SetVal) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Set(
                    elts=(
                        [cast(ast3.expr, i) for i in node.values.gen.py_ast]
                        if node.values
                        else []
                    ),
                )
            )
        ]

    def exit_tuple_val(self, node: uni.TupleVal) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Tuple(
                    elts=(
                        cast(list[ast3.expr], node.values.gen.py_ast)
                        if node.values
                        else []
                    ),
                    ctx=cast(ast3.expr_context, node.py_ctx_func()),
                )
            )
        ]

    def exit_dict_val(self, node: uni.DictVal) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Dict(
                    keys=[
                        cast(ast3.expr, x.key.gen.py_ast[0]) if x.key else None
                        for x in node.kv_pairs
                    ],
                    values=[
                        cast(ast3.expr, x.value.gen.py_ast[0]) for x in node.kv_pairs
                    ],
                )
            )
        ]

    def exit_k_v_pair(self, node: uni.KVPair) -> None:
        pass

    def exit_k_w_pair(self, node: uni.KWPair) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.keyword(
                    arg=node.key.sym_name if node.key else None,
                    value=cast(ast3.expr, node.value.gen.py_ast[0]),
                )
            )
        ]

    def exit_inner_compr(self, node: uni.InnerCompr) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.comprehension(
                    target=cast(ast3.expr, node.target.gen.py_ast[0]),
                    iter=cast(ast3.expr, node.collection.gen.py_ast[0]),
                    ifs=(
                        [cast(ast3.expr, x.gen.py_ast[0]) for x in node.conditional]
                        if node.conditional
                        else []
                    ),
                    is_async=0,
                )
            )
        ]

    def exit_list_compr(self, node: uni.ListCompr) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.ListComp(
                    elt=cast(ast3.expr, node.out_expr.gen.py_ast[0]),
                    generators=cast(
                        list[ast3.comprehension], [i.gen.py_ast[0] for i in node.compr]
                    ),
                )
            )
        ]

    def exit_gen_compr(self, node: uni.GenCompr) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.GeneratorExp(
                    elt=cast(ast3.expr, node.out_expr.gen.py_ast[0]),
                    generators=[
                        cast(ast3.comprehension, i.gen.py_ast[0]) for i in node.compr
                    ],
                )
            )
        ]

    def exit_set_compr(self, node: uni.SetCompr) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.SetComp(
                    elt=cast(ast3.expr, node.out_expr.gen.py_ast[0]),
                    generators=[
                        cast(ast3.comprehension, i.gen.py_ast[0]) for i in node.compr
                    ],
                )
            )
        ]

    def exit_dict_compr(self, node: uni.DictCompr) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.DictComp(
                    key=(
                        cast(ast3.expr, node.kv_pair.key.gen.py_ast[0])
                        if node.kv_pair.key
                        else cast(ast3.expr, ast3.Constant(value=None))
                    ),
                    value=cast(ast3.expr, node.kv_pair.value.gen.py_ast[0]),
                    generators=[
                        cast(ast3.comprehension, i.gen.py_ast[0]) for i in node.compr
                    ],
                )
            )
        ]

    def exit_atom_trailer(self, node: uni.AtomTrailer) -> None:
        if node.is_genai:
            node.gen.py_ast = []
        if node.is_attr:
            if isinstance(node.right, uni.AstSymbolNode):
                node.gen.py_ast = [
                    self.sync(
                        ast3.Attribute(
                            value=cast(ast3.expr, node.target.gen.py_ast[0]),
                            attr=(node.right.sym_name),
                            ctx=cast(ast3.expr_context, node.right.py_ctx_func()),
                        )
                    )
                ]
            else:
                self.log_error("Invalid attribute access")
        elif isinstance(node.right, uni.FilterCompr):
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.jaclib_obj("filter"),
                        args=[],
                        keywords=[
                            self.sync(
                                ast3.keyword(
                                    arg="items",
                                    value=cast(ast3.expr, node.target.gen.py_ast[0]),
                                )
                            ),
                            self.sync(
                                ast3.keyword(
                                    arg="func",
                                    value=cast(ast3.expr, node.right.gen.py_ast[0]),
                                )
                            ),
                        ],
                    )
                )
            ]
        elif isinstance(node.right, uni.AssignCompr):
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.jaclib_obj("assign"),
                        args=cast(
                            list[ast3.expr],
                            [node.target.gen.py_ast[0], node.right.gen.py_ast[0]],
                        ),
                        keywords=[],
                    )
                )
            ]
        else:
            node.gen.py_ast = [
                self.sync(
                    ast3.Subscript(
                        value=cast(ast3.expr, node.target.gen.py_ast[0]),
                        slice=cast(ast3.expr, node.right.gen.py_ast[0]),
                        ctx=(
                            cast(ast3.expr_context, node.right.py_ctx_func())
                            if isinstance(node.right, uni.AstSymbolNode)
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
                                value=cast(ast3.expr, node.target.gen.py_ast[0]),
                            )
                        ),
                        body=cast(ast3.expr, node.gen.py_ast[0]),
                        orelse=self.sync(ast3.Constant(value=None)),
                    )
                )
            ]

    def exit_atom_unit(self, node: uni.AtomUnit) -> None:
        node.gen.py_ast = node.value.gen.py_ast

    def by_llm_call(
        self,
        model: ast3.AST,
        model_params: dict[str, uni.Expr],
        scope: ast3.AST,
        inputs: Sequence[Optional[ast3.AST]],
        outputs: Sequence[Optional[ast3.AST]] | ast3.Call,
        action: Optional[ast3.AST],
        include_info: list[tuple[str, ast3.AST]],
        exclude_info: list[tuple[str, ast3.AST]],
    ) -> ast3.Call:
        """Return the LLM Call, e.g. _Jac.with_llm()."""
        # to avoid circular import
        from jaclang.runtimelib.machine import JacMachineInterface

        return JacMachineInterface.by_llm_call(
            self,
            model,
            model_params,
            scope,
            inputs,
            outputs,
            action,
            include_info,
            exclude_info,
        )

    def get_by_llm_call_args(self, node: uni.FuncCall) -> dict:
        """Get the arguments for the by_llm_call."""
        # to avoid circular import
        from jaclang.runtimelib.machine import JacMachineInterface

        return JacMachineInterface.get_by_llm_call_args(self, node)

    def exit_func_call(self, node: uni.FuncCall) -> None:
        func = node.target.gen.py_ast[0]
        args = []
        keywords = []
        if node.params and len(node.params.items) > 0:
            for x in node.params.items:
                if isinstance(x, uni.UnaryExpr) and x.op.name == Tok.STAR_POW:
                    keywords.append(
                        self.sync(
                            ast3.keyword(
                                value=cast(ast3.expr, x.operand.gen.py_ast[0])
                            ),
                            x,
                        )
                    )
                elif isinstance(x, uni.Expr):
                    args.append(x.gen.py_ast[0])
                elif isinstance(x, uni.KWPair) and isinstance(
                    x.gen.py_ast[0], ast3.keyword
                ):
                    keywords.append(x.gen.py_ast[0])
                else:
                    self.ice("Invalid Parameter")
        if node.genai_call:
            by_llm_call_args = self.get_by_llm_call_args(node)
            node.gen.py_ast = [self.sync(self.by_llm_call(**by_llm_call_args))]
        else:
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=cast(ast3.expr, func),
                        args=[cast(ast3.expr, arg) for arg in args],
                        keywords=keywords,
                    )
                )
            ]

    def exit_index_slice(self, node: uni.IndexSlice) -> None:
        if node.is_range:
            if len(node.slices) > 1:  # Multiple slices. Example arr[a:b, c:d]
                node.gen.py_ast = [
                    self.sync(
                        ast3.Tuple(
                            elts=[
                                self.sync(
                                    ast3.Slice(
                                        lower=(
                                            cast(ast3.expr, slice.start.gen.py_ast[0])
                                            if slice.start
                                            else None
                                        ),
                                        upper=(
                                            cast(ast3.expr, slice.stop.gen.py_ast[0])
                                            if slice.stop
                                            else None
                                        ),
                                        step=(
                                            cast(ast3.expr, slice.step.gen.py_ast[0])
                                            if slice.step
                                            else None
                                        ),
                                    )
                                )
                                for slice in node.slices
                            ],
                            ctx=ast3.Load(),
                        )
                    )
                ]
            elif len(node.slices) == 1:  # Single slice. Example arr[a]
                slice = node.slices[0]
                node.gen.py_ast = [
                    self.sync(
                        ast3.Slice(
                            lower=(
                                cast(ast3.expr, slice.start.gen.py_ast[0])
                                if slice.start
                                else None
                            ),
                            upper=(
                                cast(ast3.expr, slice.stop.gen.py_ast[0])
                                if slice.stop
                                else None
                            ),
                            step=(
                                cast(ast3.expr, slice.step.gen.py_ast[0])
                                if slice.step
                                else None
                            ),
                        )
                    )
                ]
        else:
            if len(node.slices) > 0 and node.slices[0].start is not None:
                node.gen.py_ast = node.slices[0].start.gen.py_ast
            else:
                node.gen.py_ast = []

    def exit_special_var_ref(self, node: uni.SpecialVarRef) -> None:
        if node.name == Tok.KW_SUPER:
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.sync(ast3.Name(id="super", ctx=node.py_ctx_func())),
                        args=[],
                        keywords=[],
                    )
                )
            ]
        elif node.name == Tok.KW_ROOT:
            node.gen.py_ast = [
                self.sync(
                    ast3.Call(
                        func=self.jaclib_obj("root"),
                        args=[],
                        keywords=[],
                    )
                )
            ]

        else:
            node.gen.py_ast = [
                self.sync(ast3.Name(id=node.sym_name, ctx=node.py_ctx_func()))
            ]

    def exit_edge_ref_trailer(self, node: uni.EdgeRefTrailer) -> None:
        pynode = node.chain[0].gen.py_ast[0]
        chomp = [*node.chain]
        last_edge = None
        if node.edges_only:
            for i in node.chain:
                if isinstance(i, uni.EdgeOpRef):
                    last_edge = i
        while len(chomp):
            cur = chomp[0]
            chomp = chomp[1:]
            if len(chomp) == len(node.chain) - 1 and not isinstance(cur, uni.EdgeOpRef):
                continue
            next_i = chomp[0] if chomp else None
            if isinstance(cur, uni.EdgeOpRef) and (
                not next_i or not isinstance(next_i, uni.EdgeOpRef)
            ):
                pynode = self.translate_edge_op_ref(
                    loc=pynode,
                    node=cur,
                    targ=(
                        next_i.gen.py_ast[0]
                        if next_i and not isinstance(next_i, uni.FilterCompr)
                        else None
                    ),
                    edges_only=node.edges_only and cur == last_edge,
                )
                if next_i and isinstance(next_i, uni.FilterCompr):
                    pynode = self.sync(
                        ast3.Call(
                            func=self.jaclib_obj("filter"),
                            args=[],
                            keywords=[
                                self.sync(
                                    ast3.keyword(
                                        arg="items",
                                        value=cast(ast3.expr, pynode),
                                    )
                                ),
                                self.sync(
                                    ast3.keyword(
                                        arg="func",
                                        value=cast(ast3.expr, next_i.gen.py_ast[0]),
                                    )
                                ),
                            ],
                        )
                    )
                chomp = chomp[1:] if next_i else chomp
            elif isinstance(cur, uni.EdgeOpRef) and isinstance(next_i, uni.EdgeOpRef):
                pynode = self.translate_edge_op_ref(
                    pynode,
                    cur,
                    targ=None,
                    edges_only=node.edges_only and cur == last_edge,
                )
            else:
                raise self.ice("Invalid edge ref trailer")

        node.gen.py_ast = [pynode]

    def exit_edge_op_ref(self, node: uni.EdgeOpRef) -> None:
        loc = self.sync(
            ast3.Name(id=Con.HERE.value, ctx=ast3.Load())
            if node.from_walker
            else ast3.Name(id="self", ctx=ast3.Load())
        )
        node.gen.py_ast = [loc]

    def translate_edge_op_ref(
        self,
        loc: ast3.AST,
        node: uni.EdgeOpRef,
        targ: ast3.AST | None,
        edges_only: bool,
    ) -> ast3.AST:
        """Generate ast for edge op ref call."""
        keywords = [self.sync(ast3.keyword(arg="sources", value=cast(ast3.expr, loc)))]

        if targ:
            keywords.append(
                self.sync(ast3.keyword(arg="targets", value=cast(ast3.expr, targ)))
            )

        if node.edge_dir != EdgeDir.OUT:
            keywords.append(
                self.sync(
                    ast3.keyword(
                        arg="dir",
                        value=self.sync(
                            ast3.Attribute(
                                value=self.jaclib_obj("EdgeDir"),
                                attr=node.edge_dir.name,
                                ctx=ast3.Load(),
                            )
                        ),
                    )
                )
            )

        if node.filter_cond:
            keywords.append(
                self.sync(
                    ast3.keyword(
                        arg="filter",
                        value=cast(
                            ast3.expr, self.sync(node.filter_cond.gen.py_ast[0])
                        ),
                    )
                )
            )

        if edges_only:
            keywords.append(
                self.sync(
                    ast3.keyword(
                        arg="edges_only",
                        value=self.sync(ast3.Constant(value=edges_only)),
                    )
                )
            )

        return self.sync(
            ast3.Call(
                func=self.jaclib_obj("refs"),
                args=[],
                keywords=keywords,
            )
        )

    def exit_disconnect_op(self, node: uni.DisconnectOp) -> None:
        node.gen.py_ast = node.edge_spec.gen.py_ast

    def exit_connect_op(self, node: uni.ConnectOp) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Call(
                    func=self.jaclib_obj("build_edge"),
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
                                    cast(ast3.expr, node.conn_type.gen.py_ast[0])
                                    if node.conn_type
                                    else self.sync(ast3.Constant(value=None))
                                ),
                            )
                        ),
                        self.sync(
                            ast3.keyword(
                                arg="conn_assign",
                                value=(
                                    cast(ast3.expr, node.conn_assign.gen.py_ast[0])
                                    if node.conn_assign
                                    else self.sync(ast3.Constant(value=None))
                                ),
                            )
                        ),
                    ],
                )
            )
        ]

    def exit_filter_compr(self, node: uni.FilterCompr) -> None:
        iter_name = "i"

        comprs: list[ast3.Compare | ast3.Call] = (
            [
                self.sync(
                    ast3.Call(
                        func=self.sync(
                            ast3.Name(
                                id="isinstance",
                                ctx=ast3.Load(),
                            )
                        ),
                        args=cast(
                            list[ast3.expr],
                            [
                                self.sync(
                                    ast3.Name(
                                        id=iter_name,
                                        ctx=ast3.Load(),
                                    )
                                ),
                                self.sync(node.f_type.gen.py_ast[0]),
                            ],
                        ),
                        keywords=[],
                    )
                )
            ]
            if node.f_type
            else []
        )
        comprs.extend(
            self.sync(
                ast3.Compare(
                    left=self.sync(
                        ast3.Attribute(
                            value=self.sync(
                                ast3.Name(
                                    id=iter_name,
                                    ctx=ast3.Load(),
                                ),
                                jac_node=x,
                            ),
                            attr=x.gen.py_ast[0].left.id,
                            ctx=ast3.Load(),
                        ),
                        jac_node=x,
                    ),
                    ops=x.gen.py_ast[0].ops,
                    comparators=x.gen.py_ast[0].comparators,
                ),
                jac_node=x,
            )
            for x in (node.compares.items if node.compares else [])
            if isinstance(x.gen.py_ast[0], ast3.Compare)
            and isinstance(x.gen.py_ast[0].left, ast3.Name)
        )

        if body := (
            self.sync(
                ast3.BoolOp(
                    op=self.sync(ast3.And()),
                    values=[cast(ast3.expr, item) for item in comprs],
                )
            )
            if len(comprs) > 1
            else (comprs[0] if comprs else None)
        ):
            node.gen.py_ast = [
                self.sync(
                    ast3.Lambda(
                        args=self.sync(
                            ast3.arguments(
                                posonlyargs=[],
                                args=[self.sync(ast3.arg(arg=iter_name))],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            )
                        ),
                        body=body,
                    )
                )
            ]

    def exit_assign_compr(self, node: uni.AssignCompr) -> None:
        keys = []
        values = []
        for i in node.assigns.items:
            if i.key:  # TODO: add support for **kwargs in assign_compr
                keys.append(self.sync(ast3.Constant(i.key.sym_name)))
                values.append(i.value.gen.py_ast[0])
        key_tup = self.sync(
            ast3.Tuple(
                elts=[key for key in keys if isinstance(key, ast3.expr)],
                ctx=ast3.Load(),
            )
        )
        val_tup = self.sync(
            ast3.Tuple(
                elts=[v for v in values if isinstance(v, ast3.expr)], ctx=ast3.Load()
            )
        )
        node.gen.py_ast = [
            self.sync(ast3.Tuple(elts=[key_tup, val_tup], ctx=ast3.Load()))
        ]

    def exit_match_stmt(self, node: uni.MatchStmt) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.Match(
                    subject=cast(ast3.expr, node.target.gen.py_ast[0]),
                    cases=[cast(ast3.match_case, x.gen.py_ast[0]) for x in node.cases],
                )
            )
        ]

    def exit_match_case(self, node: uni.MatchCase) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.match_case(
                    pattern=cast(ast3.pattern, node.pattern.gen.py_ast[0]),
                    guard=(
                        cast(ast3.expr, node.guard.gen.py_ast[0])
                        if node.guard
                        else None
                    ),
                    body=[cast(ast3.stmt, x.gen.py_ast[0]) for x in node.body],
                )
            )
        ]

    def exit_match_or(self, node: uni.MatchOr) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.MatchOr(
                    patterns=[
                        cast(ast3.pattern, x.gen.py_ast[0]) for x in node.patterns
                    ],
                )
            )
        ]

    def exit_match_as(self, node: uni.MatchAs) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.MatchAs(
                    name=node.name.sym_name,
                    pattern=(
                        cast(ast3.pattern, node.pattern.gen.py_ast[0])
                        if node.pattern
                        else None
                    ),
                )
            )
        ]

    def exit_match_wild(self, node: uni.MatchWild) -> None:
        node.gen.py_ast = [self.sync(ast3.MatchAs())]

    def exit_match_value(self, node: uni.MatchValue) -> None:
        node.gen.py_ast = [
            self.sync(ast3.MatchValue(value=cast(ast3.expr, node.value.gen.py_ast[0])))
        ]

    def exit_match_singleton(self, node: uni.MatchSingleton) -> None:
        node.gen.py_ast = [self.sync(ast3.MatchSingleton(value=node.value.lit_value))]

    def exit_match_sequence(self, node: uni.MatchSequence) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.MatchSequence(
                    patterns=[cast(ast3.pattern, x.gen.py_ast[0]) for x in node.values],
                )
            )
        ]

    def exit_match_mapping(self, node: uni.MatchMapping) -> None:
        mapping = self.sync(ast3.MatchMapping(keys=[], patterns=[], rest=None))
        for i in node.values:
            if (
                isinstance(i, uni.MatchKVPair)
                and isinstance(i.key, uni.MatchValue)
                and isinstance(i.key.value.gen.py_ast[0], ast3.expr)
                and isinstance(i.value.gen.py_ast[0], ast3.pattern)
            ):
                mapping.keys.append(i.key.value.gen.py_ast[0])
                mapping.patterns.append(i.value.gen.py_ast[0])
            elif isinstance(i, uni.MatchStar):
                mapping.rest = i.name.sym_name
        node.gen.py_ast = [mapping]

    def exit_match_k_v_pair(self, node: uni.MatchKVPair) -> None:
        pass

    def exit_match_star(self, node: uni.MatchStar) -> None:
        node.gen.py_ast = [self.sync(ast3.MatchStar(name=node.name.sym_name))]

    def exit_match_arch(self, node: uni.MatchArch) -> None:
        node.gen.py_ast = [
            self.sync(
                ast3.MatchClass(
                    cls=cast(ast3.expr, node.name.gen.py_ast[0]),
                    patterns=(
                        [
                            cast(ast3.pattern, x.gen.py_ast[0])
                            for x in node.arg_patterns.items
                        ]
                        if node.arg_patterns
                        else []
                    ),
                    kwd_attrs=(
                        [
                            x.key.sym_name
                            for x in node.kw_patterns.items
                            if isinstance(x.key, uni.NameAtom)
                        ]
                        if node.kw_patterns
                        else []
                    ),
                    kwd_patterns=(
                        [
                            cast(ast3.pattern, x.value.gen.py_ast[0])
                            for x in node.kw_patterns.items
                        ]
                        if node.kw_patterns
                        else []
                    ),
                )
            )
        ]

    def exit_token(self, node: uni.Token) -> None:
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

    def exit_name(self, node: uni.Name) -> None:
        node.gen.py_ast = [
            self.sync(ast3.Name(id=node.sym_name, ctx=node.py_ctx_func()))
        ]

    def exit_float(self, node: uni.Float) -> None:
        node.gen.py_ast = [self.sync(ast3.Constant(value=float(node.value)))]

    def exit_int(self, node: uni.Int) -> None:
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

    def exit_string(self, node: uni.String) -> None:
        node.gen.py_ast = [self.sync(ast3.Constant(value=node.lit_value))]

    def exit_bool(self, node: uni.Bool) -> None:
        node.gen.py_ast = [self.sync(ast3.Constant(value=node.value == "True"))]

    def exit_builtin_type(self, node: uni.BuiltinType) -> None:
        node.gen.py_ast = [
            self.sync(ast3.Name(id=node.sym_name, ctx=node.py_ctx_func()))
        ]

    def exit_null(self, node: uni.Null) -> None:
        node.gen.py_ast = [self.sync(ast3.Constant(value=None))]

    def exit_ellipsis(self, node: uni.Ellipsis) -> None:
        node.gen.py_ast = [self.sync(ast3.Constant(value=...))]

    def exit_semi(self, node: uni.Semi) -> None:
        pass

    def exit_comment_token(self, node: uni.CommentToken) -> None:
        pass

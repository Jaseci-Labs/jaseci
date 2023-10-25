"""Lark parser for Jac Lang."""
from __future__ import annotations

import ast as py_ast
import os
from typing import Optional, TypeVar

import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Tokens as Tok
from jaclang.jac.passes.ir_pass import Pass
from jaclang.utils.helpers import pascal_to_snake

T = TypeVar("T", bound=ast.AstNode)


class PyAstBuildPass(Pass):
    """Jac Parser."""

    def nu(self, node: ast.T) -> ast.T:
        """Update node."""
        self.cur_node = node
        return node

    def pp(self, node: py_ast.AST) -> None:
        """Print python node."""
        print(
            f"{node.__class__.__name__} - {[(k, type(v)) for k, v in vars(node).items()]}"
        )

    def ice(self, msg: Optional[str] = None) -> Exception:
        """Raise internal compiler error."""
        if not msg:
            msg = "Internal Compiler Error, Invalid Python Parse Tree Conversion!"
        super().error(msg)
        return RuntimeError(f"{self.__class__.__name__} - {msg}")

    def convert(self, node: py_ast.AST) -> ast.AstNode:  # type: ignore
        """Get python node type."""
        if hasattr(self, f"proc_{pascal_to_snake(type(node).__name__)}"):
            return getattr(self, f"proc_{pascal_to_snake(type(node).__name__)}")(node)
        else:
            self.error(f"Unknown node type {type(node).__name__}")

    def transform(self, ir: ast.PythonModuleAst) -> Optional[ast.Module]:
        """Transform input IR."""
        self.ir = self.proc_module(ir.ast)
        return self.ir

    def proc_module(self, node: py_ast.Module) -> ast.Module:
        """Process python node.

        class Module(mod):
            __match_args__ = ("body", "type_ignores")
            body: list[stmt]
            type_ignores: list[TypeIgnore]
        """
        elements = [self.convert(i) for i in node.body]
        valid = [i for i in elements if isinstance(i, ast.ElementStmt)]
        if len(valid) != len(elements):
            self.error("Invalid module body")
        return self.nu(
            ast.Module(
                name=self.mod_path.split(os.path.sep)[-1].split(".")[0],
                source=ast.JacSource(""),
                doc=elements[0] if isinstance(elements[0], ast.String) else None,
                body=valid,
                mod_path=self.mod_path,
                rel_mod_path=self.rel_mod_path,
                is_imported=False,
                kid=elements,
            )
        )

    def proc_function_def(
        self, node: py_ast.FunctionDef | py_ast.AsyncFunctionDef
    ) -> ast.Ability:
        """Process python node.

        class FunctionDef(stmt):
            __match_args__ = ("name", "args", "body", "decorator_list",
                              "returns", "type_comment", "type_params")
            name: _Identifier
            args: arguments
            body: list[stmt]
            decorator_list: list[expr]
            returns: expr | None
            if sys.version_info >= (3, 12):
            type_params: list[type_param]
        """
        name = ast.Name(
            name=Tok.NAME,
            value=node.name,
            line=node.lineno,
            col_start=node.col_offset,
            col_end=node.col_offset + len(node.name),
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        body = [self.convert(i) for i in node.body]
        valid_body = [i for i in body if isinstance(i, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in function body")
        valid_body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        doc = None
        decorators = [self.convert(i) for i in node.decorator_list]
        valid_decorators = [i for i in decorators if isinstance(i, ast.ExprType)]
        if len(valid_decorators) != len(decorators):
            self.error("Length mismatch in decorators on function")
        valid_decorators = (
            ast.SubNodeList[ast.ExprType](items=valid_decorators, kid=decorators)
            if len(valid_decorators)
            else None
        )
        res = self.convert(node.args)
        sig: Optional[ast.FuncSignature] | ast.ExprType = (
            res if isinstance(res, ast.FuncSignature) else None
        )
        ret_sig = self.convert(node.returns) if node.returns else None
        if isinstance(ret_sig, ast.ExprType):
            if not sig:
                sig = ret_sig
            else:
                sig.return_type = ast.SubTag[ast.ExprType](tag=ret_sig, kid=[ret_sig])
                sig.add_kids_right([sig.return_type])
        kid = [name, sig, valid_body] if sig else [name, valid_body]
        return ast.Ability(
            name_ref=name,
            is_func=True,
            is_async=False,
            is_static=False,
            is_abstract=False,
            access=None,
            signature=sig,
            body=valid_body,
            decorators=valid_decorators,
            doc=doc,
            kid=kid,
        )

    def proc_async_function_def(self, node: py_ast.AsyncFunctionDef) -> ast.Ability:
        """Process python node.

        class AsyncFunctionDef(stmt):
            __match_args__ = ("name", "args", "body", "decorator_list",
                              "returns", "type_comment", "type_params")
            name: _Identifier
            args: arguments
            body: list[stmt]
            decorator_list: list[expr]
            returns: expr | None
            if sys.version_info >= (3, 12):
                type_params: list[type_param]
        """
        ability = self.proc_function_def(node)
        ability.is_async = True
        return ability

    def proc_class_def(self, node: py_ast.ClassDef) -> ast.Architype:
        """Process python node.

        class ClassDef(stmt):
            __match_args__ = ("name", "bases", "keywords", "body",
                              "decorator_list", "type_params")
            name: _Identifier
            bases: list[expr]
            keywords: list[keyword]
            body: list[stmt]
            decorator_list: list[expr]
            if sys.version_info >= (3, 12):
            type_params: list[type_param]
        """
        name = ast.Name(
            name=Tok.NAME,
            value=node.name,
            line=node.lineno,
            col_start=node.col_offset,
            col_end=node.col_offset + len(node.name),
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        arch_type = ast.Token(
            name=Tok.KW_OBJECT,
            value="object",
            line=node.lineno,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        base_classes = [self.convert(base) for base in node.bases]
        valid_bases = [base for base in base_classes if isinstance(base, ast.AtomType)]
        if len(valid_bases) != len(base_classes):
            self.error("Length mismatch in base classes")
        valid_bases = (
            ast.SubNodeList[ast.AtomType](items=valid_bases, kid=base_classes)
            if len(valid_bases)
            else None
        )
        body = [self.convert(i) for i in node.body]
        valid_body = [i for i in body if isinstance(i, ast.ArchBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in classes body")
        valid_body = ast.SubNodeList[ast.ArchBlockStmt](items=valid_body, kid=body)
        doc = None
        decorators = [self.convert(i) for i in node.decorator_list]
        valid_decorators = [i for i in decorators if isinstance(i, ast.ExprType)]
        if len(valid_decorators) != len(decorators):
            self.error("Length mismatch in decorators in class")
        valid_decorators = (
            ast.SubNodeList[ast.ExprType](items=valid_decorators, kid=decorators)
            if len(valid_decorators)
            else None
        )
        kid = [name, valid_bases, valid_body] if valid_bases else [name, valid_body]
        return ast.Architype(
            arch_type=arch_type,
            name=name,
            access=None,
            base_classes=valid_bases,
            body=valid_body,
            kid=kid,
            doc=doc,
            decorators=valid_decorators,
        )

    def proc_return(self, node: py_ast.Return) -> ast.ExprType | None:
        """Process python node.

        class Return(stmt):
            __match_args__ = ("value",)
            value: expr | None
        """
        value = self.convert(node.value) if node.value else None
        if value and not isinstance(value, ast.ExprType):
            self.error("Invalid return value")
        else:
            return value

    def proc_delete(self, node: py_ast.Delete) -> ast.DeleteStmt:
        """Process python node.

        class Delete(stmt):
            __match_args__ = ("targets",)
            targets: list[expr]
        """
        exprs = [self.convert(target) for target in node.targets]
        valid_exprs = [expr for expr in exprs if isinstance(expr, ast.ExprType)]
        if not len(valid_exprs) or len(valid_exprs) != len(exprs):
            self.error("Length mismatch in delete targets")
        return ast.DeleteStmt(
            target=ast.ExprList(
                values=ast.SubNodeList[ast.ExprType](items=valid_exprs, kid=exprs),
                kid=exprs,
            ),
            kid=exprs,
        )

    def proc_assign(self, node: py_ast.Assign) -> ast.Assignment:
        """Process python node.

        class Assign(stmt):
            targets: list[expr]
            value: expr
        """
        targets = [self.convert(target) for target in node.targets]
        valid_targets = [
            target for target in targets if isinstance(target, ast.AtomType)
        ]
        if len(valid_targets) != len(targets):
            self.error("Length mismatch in assignment targets")
        if len(valid_targets) == 1:
            valid_targets = valid_targets[0]
        else:
            valid_targets = ast.TupleVal(
                ast.SubNodeList[ast.ExprType | ast.Assignment](
                    items=valid_targets, kid=targets
                ),
                kid=targets,
            )
        value = self.convert(node.value)
        if isinstance(value, ast.ExprType):
            return ast.Assignment(
                target=valid_targets,
                value=value,
                kid=[valid_targets, value],
            )
        else:
            raise self.ice()

    def proc_aug_assign(self, node: py_ast.AugAssign) -> ast.BinaryExpr:
        """Process python node.

        class AugAssign(stmt):
            __match_args__ = ("target", "op", "value")
            target: Name | Attribute | Subscript
            op: operator
            value: expr
        """
        target = self.convert(node.target)
        op = self.convert(node.op)
        value = self.convert(node.value)
        if (
            isinstance(value, ast.ExprType)
            and isinstance(target, ast.ExprType)
            and isinstance(op, ast.Token)
        ):
            return ast.BinaryExpr(
                left=target,
                op=op,
                right=value,
                kid=[target, op, value],
            )
        else:
            raise self.ice()

    def proc_ann_assign(self, node: py_ast.AnnAssign) -> ast.Assignment:
        """Process python node.

        class AnnAssign(stmt):
            __match_args__ = ("target", "annotation", "value", "simple")
            target: Name | Attribute | Subscript
            annotation: expr
            value: expr | None
            simple: int
        """
        target = self.convert(node.target)
        # annotation = self.proc_node(node.annotation)
        # simple = node.simple
        value = self.convert(node.value) if node.value else None
        if isinstance(target, ast.AtomType) and isinstance(value, ast.ExprType):
            return ast.Assignment(
                target=target,
                value=value,
                kid=[target, value],
            )
        else:
            raise self.ice()

    def proc_for(self, node: py_ast.For) -> ast.InForStmt:
        """Process python node.

        class For(stmt):
            __match_args__ = ("target", "iter", "body", "orelse")
            target: expr
            iter: expr
            body: list[stmt]
            orelse: list[stmt]
        """
        target = self.convert(node.target)
        iter = self.convert(node.iter)
        body = [self.convert(i) for i in node.body]
        valid_body = [i for i in body if isinstance(i, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in for body")
        valid_body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        orelse = [self.convert(i) for i in node.orelse]
        valid_orelse = [i for i in orelse if isinstance(i, ast.CodeBlockStmt)]
        if len(valid_orelse) != len(orelse):
            self.error("Length mismatch in for orelse")
        valid_orelse = ast.SubNodeList[ast.CodeBlockStmt](
            items=valid_orelse, kid=orelse
        )
        raise self.ice(f"IMPLEMENT ME{target}{iter}")

    def proc_async_for(self, node: py_ast.AsyncFor) -> ast.InForStmt:
        """Process AsyncFor node.

        class AsyncFor(stmt):
            __match_args__ = ("target", "iter", "body", "orelse")
            target: expr
            iter: expr
            body: list[stmt]
            orelse: list[stmt]`
        """
        target = self.convert(node.target)
        iter = self.convert(node.iter)
        body = [self.convert(stmt) for stmt in node.body]
        valid_body = [stmt for stmt in body if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in async for body")
        body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        orelse = [self.convert(stmt) for stmt in node.orelse]
        valid_orelse = [stmt for stmt in orelse if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_orelse) != len(orelse):
            self.error("Length mismatch in async for orelse")
        orelse = ast.SubNodeList[ast.CodeBlockStmt](items=valid_orelse, kid=orelse)
        raise self.ice(f"IMPLEMENT ME {target} {iter} ")

    def proc_while(self, node: py_ast.While) -> ast.CodeBlockStmt:
        """Process While node.

        class While(stmt):
            __match_args__ = ("test", "body", "orelse")
            test: expr
            body: list[stmt]
            orelse: list[stmt]
        """
        test = self.convert(node.test)
        body = [self.convert(stmt) for stmt in node.body]
        valid_body = [stmt for stmt in body if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in async for body")
        body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        orelse = [self.convert(stmt) for stmt in node.orelse]
        valid_orelse = [stmt for stmt in orelse if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_orelse) != len(orelse):
            self.error("Length mismatch in async for orelse")
        orelse = ast.SubNodeList[ast.CodeBlockStmt](items=valid_orelse, kid=orelse)
        raise self.ice(f"IMPLEMENT ME{test}")

    def proc_if(self, node: py_ast.If) -> ast.CodeBlockStmt:
        """Process If node.

        class If(stmt):
            __match_args__ = ("test", "body", "orelse")
            test: expr
            body: list[stmt]
            orelse: list[stmt]
        """
        test = self.convert(node.test)
        body = [self.convert(stmt) for stmt in node.body]
        valid_body = [stmt for stmt in body if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in async for body")
        body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        orelse = [self.convert(stmt) for stmt in node.orelse]
        valid_orelse = [stmt for stmt in orelse if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_orelse) != len(orelse):
            self.error("Length mismatch in async for orelse")
        orelse = ast.SubNodeList[ast.CodeBlockStmt](items=valid_orelse, kid=orelse)
        raise self.ice(f"IMPLEMENT ME{test}")

    def proc_with(self, node: py_ast.With) -> ast.CodeBlockStmt:
        """Process With node.

        class With(stmt):
            __match_args__ = ("items", "body")
            items: list[withitem]
            body: list[stmt]
        """
        items = [self.convert(item) for item in node.items]
        valid_items = [item for item in items if isinstance(item, ast.ExprAsItem)]
        if len(valid_items) != len(items):
            self.error("Length mismatch in with items")
        items = ast.SubNodeList[ast.ExprAsItem](items=valid_items, kid=items)
        body = [self.convert(stmt) for stmt in node.body]
        valid_body = [stmt for stmt in body if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in async for body")
        body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        raise self.ice("IMPLEMENT ME")

    def proc_async_with(self, node: py_ast.AsyncWith) -> ast.CodeBlockStmt:
        """Process AsyncWith node.

        class AsyncWith(stmt):
            __match_args__ = ("items", "body")
            items: list[withitem]
            body: list[stmt]
        """
        items = [self.convert(item) for item in node.items]
        valid_items = [item for item in items if isinstance(item, ast.ExprAsItem)]
        if len(valid_items) != len(items):
            self.error("Length mismatch in with items")
        items = ast.SubNodeList[ast.ExprAsItem](items=valid_items, kid=items)
        body = [self.convert(stmt) for stmt in node.body]
        valid_body = [stmt for stmt in body if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in async for body")
        body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        raise self.ice("IMPLEMENT ME")

    def proc_raise(self, node: py_ast.Raise) -> ast.RaiseStmt:
        """Process python node."""

    def proc_assert(self, node: py_ast.Assert) -> ast.AstNode:
        """Process python node."""

    def proc_attribute(self, node: py_ast.Attribute) -> ast.AstNode:
        """Process python node."""

    def proc_await(self, node: py_ast.Await) -> ast.AstNode:
        """Process python node."""

    def proc_bin_op(self, node: py_ast.BinOp) -> ast.AstNode:
        """Process python node."""

    def proc_bool_op(self, node: py_ast.BoolOp) -> ast.AstNode:
        """Process python node."""

    def proc_break(self, node: py_ast.Break) -> ast.AstNode:
        """Process python node."""

    def proc_call(self, node: py_ast.Call) -> ast.AstNode:
        """Process python node."""

    def proc_compare(self, node: py_ast.Compare) -> ast.AstNode:
        """Process python node."""

    def proc_constant(self, node: py_ast.Constant) -> ast.AstNode:
        """Process python node."""

    def proc_continue(self, node: py_ast.Continue) -> ast.AstNode:
        """Process python node."""

    def proc_dict(self, node: py_ast.Dict) -> ast.AstNode:
        """Process python node."""

    def proc_dict_comp(self, node: py_ast.DictComp) -> ast.AstNode:
        """Process python node."""

    def proc_ellipsis(self, node: py_ast.Ellipsis) -> ast.AstNode:
        """Process python node."""

    def proc_except_handler(self, node: py_ast.ExceptHandler) -> ast.AstNode:
        """Process python node."""

    def proc_expr(self, node: py_ast.Expr) -> ast.AstNode:
        """Process python node."""

    def proc_formatted_value(self, node: py_ast.FormattedValue) -> ast.AstNode:
        """Process python node."""

    def proc_function_type(self, node: py_ast.FunctionType) -> ast.AstNode:
        """Process python node."""

    def proc_generator_exp(self, node: py_ast.GeneratorExp) -> ast.AstNode:
        """Process python node."""

    def proc_global(self, node: py_ast.Global) -> ast.AstNode:
        """Process python node."""

    def proc_if_exp(self, node: py_ast.IfExp) -> ast.AstNode:
        """Process python node."""

    def proc_import(self, node: py_ast.Import) -> ast.AstNode:
        """Process python node."""

    def proc_import_from(self, node: py_ast.ImportFrom) -> ast.AstNode:
        """Process python node."""

    def proc_joined_str(self, node: py_ast.JoinedStr) -> ast.AstNode:
        """Process python node."""

    def proc_lambda(self, node: py_ast.Lambda) -> ast.AstNode:
        """Process python node."""

    def proc_list(self, node: py_ast.List) -> ast.AstNode:
        """Process python node."""

    def proc_list_comp(self, node: py_ast.ListComp) -> ast.AstNode:
        """Process python node."""

    def proc_match(self, node: py_ast.Match) -> ast.AstNode:
        """Process python node."""

    def proc_match_as(self, node: py_ast.MatchAs) -> ast.AstNode:
        """Process python node."""

    def proc_match_class(self, node: py_ast.MatchClass) -> ast.AstNode:
        """Process python node."""

    def proc_match_mapping(self, node: py_ast.MatchMapping) -> ast.AstNode:
        """Process python node."""

    def proc_match_or(self, node: py_ast.MatchOr) -> ast.AstNode:
        """Process python node."""

    def proc_match_sequence(self, node: py_ast.MatchSequence) -> ast.AstNode:
        """Process python node."""

    def proc_match_singleton(self, node: py_ast.MatchSingleton) -> ast.AstNode:
        """Process python node."""

    def proc_match_star(self, node: py_ast.MatchStar) -> ast.AstNode:
        """Process python node."""

    def proc_match_value(self, node: py_ast.MatchValue) -> ast.AstNode:
        """Process python node."""

    def proc_name(self, node: py_ast.Name) -> ast.AstNode:
        """Process python node."""

    def proc_named_expr(self, node: py_ast.NamedExpr) -> ast.AstNode:
        """Process python node."""

    def proc_nonlocal(self, node: py_ast.Nonlocal) -> ast.AstNode:
        """Process python node."""

    def proc_pass(self, node: py_ast.Pass) -> ast.AstNode:
        """Process python node."""

    def proc_set(self, node: py_ast.Set) -> ast.AstNode:
        """Process python node."""

    def proc_set_comp(self, node: py_ast.SetComp) -> ast.AstNode:
        """Process python node."""

    def proc_slice(self, node: py_ast.Slice) -> ast.AstNode:
        """Process python node."""

    def proc_starred(self, node: py_ast.Starred) -> ast.AstNode:
        """Process python node."""

    def proc_subscript(self, node: py_ast.Subscript) -> ast.AstNode:
        """Process python node."""

    def proc_try(self, node: py_ast.Try) -> ast.AstNode:
        """Process python node."""

    def proc_try_star(self, node: py_ast.TryStar) -> ast.AstNode:
        """Process python node."""

    def proc_tuple(self, node: py_ast.Tuple) -> ast.AstNode:
        """Process python node."""

    def proc_unary_op(self, node: py_ast.UnaryOp) -> ast.AstNode:
        """Process python node."""

    def proc_yield(self, node: py_ast.Yield) -> ast.AstNode:
        """Process python node."""

    def proc_yield_from(self, node: py_ast.YieldFrom) -> ast.AstNode:
        """Process python node."""

    def proc_alias(self, node: py_ast.alias) -> ast.AstNode:
        """Process python node."""

    def proc_arg(self, node: py_ast.arg) -> ast.AstNode:
        """Process python node."""

    def proc_arguments(self, node: py_ast.arguments) -> ast.AstNode:
        """Process python node."""

    def proc_comprehension(self, node: py_ast.comprehension) -> ast.AstNode:
        """Process python node."""

    def proc_keyword(self, node: py_ast.keyword) -> ast.AstNode:
        """Process python node."""

    def proc_match_case(self, node: py_ast.match_case) -> ast.AstNode:
        """Process python node."""

    def proc_withitem(self, node: py_ast.withitem) -> ast.AstNode:
        """Process python node."""

    def proc_param_spec(self, node: py_ast.ParamSpec) -> ast.AstNode:
        """Process python node."""

    def proc_type_alias(self, node: py_ast.TypeAlias) -> ast.AstNode:
        """Process python node."""

    def proc_type_var(self, node: py_ast.TypeVar) -> ast.AstNode:
        """Process python node."""

    def proc_type_var_tuple(self, node: py_ast.TypeVarTuple) -> ast.AstNode:
        """Process python node."""

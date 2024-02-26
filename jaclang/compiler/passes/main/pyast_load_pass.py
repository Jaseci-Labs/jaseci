# type: ignore
"""Lark parser for Jac Lang."""

from __future__ import annotations

import ast as py_ast
import os
from typing import Optional, TypeVar, Union

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes.ir_pass import Pass
from jaclang.utils.helpers import pascal_to_snake

T = TypeVar("T", bound=ast.AstNode)


class PyastBuildPass(Pass[ast.PythonModuleAst]):
    """Jac Parser."""

    def __init__(self, input_ir: ast.PythonModuleAst) -> None:
        """Initialize parser."""
        self.mod_path = input_ir.loc.mod_path
        Pass.__init__(self, input_ir=input_ir, prior=None)

    def nu(self, node: T) -> T:
        """Update node."""
        self.cur_node = node
        return node

    def pp(self, node: py_ast.AST) -> None:
        """Print python node."""
        print(
            f"{node.__class__.__name__} - {[(k, type(v)) for k, v in vars(node).items()]}"
        )

    def convert(self, node: py_ast.AST) -> ast.AstNode:
        """Get python node type."""
        print(
            f"working on {type(node).__name__} line {node.lineno if hasattr(node, 'lineno') else 0}"
        )
        if hasattr(self, f"proc_{pascal_to_snake(type(node).__name__)}"):
            ret = getattr(self, f"proc_{pascal_to_snake(type(node).__name__)}")(node)
        else:
            raise self.ice(f"Unknown node type {type(node).__name__}")
        print(f"finshed {type(node).__name__} ---------------------")
        return ret

    def transform(self, ir: ast.PythonModuleAst) -> ast.Module:
        """Transform input IR."""
        self.ir: ast.Module = self.proc_module(ir.ast)
        return self.ir

    def proc_module(self, node: py_ast.Module) -> ast.Module:
        """Process python node.

        class Module(mod):
            __match_args__ = ("body", "type_ignores")
            body: list[stmt]
            type_ignores: list[TypeIgnore]
        """
        elements: list[ast.AstNode] = [self.convert(i) for i in node.body]
        elements[0] = (
            elements[0].expr
            if isinstance(elements[0], ast.ExprStmt)
            and isinstance(elements[0].expr, ast.String)
            else elements[0]
        )
        valid = [
            i
            for i in elements
            if isinstance(
                i,
                (ast.ElementStmt, ast.String, ast.EmptyToken),
            )
        ]
        if len(valid) != len(elements):
            raise self.ice("Invalid module body")
        ret = ast.Module(
            name=self.mod_path.split(os.path.sep)[-1].split(".")[0],
            source=ast.JacSource("", mod_path=self.mod_path),
            doc=(elements[0] if isinstance(elements[0], ast.String) else None),
            body=valid[1:] if isinstance(valid[0], ast.String) else valid,
            is_imported=False,
            kid=elements,
        )
        ret.gen.py_ast = [node]
        return self.nu(ret)

    def proc_function_def(
        self, node: py_ast.FunctionDef | py_ast.AsyncFunctionDef
    ) -> ast.Ability:
        """Process python node.

        class FunctionDef(stmt):
            name: _Identifier
            args: arguments
            body: list[stmt]
            decorator_list: list[expr]
            returns: expr | None
            if sys.version_info >= (3, 12):
            type_params: list[type_param]
        """
        name = ast.Name(
            file_path=self.mod_path,
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
        valid = [i for i in body if isinstance(i, (ast.CodeBlockStmt, ast.TupleVal))]

        if len(valid) != len(body):
            raise self.ice("Length mismatch in function body")
        valid_body = ast.SubNodeList[ast.CodeBlockStmt](items=valid, kid=valid)
        doc = None
        decorators = [self.convert(i) for i in node.decorator_list]
        valid_dec = [i for i in decorators if isinstance(i, ast.Expr)]
        if len(valid_dec) != len(decorators):
            raise self.ice("Length mismatch in decorators on function")
        valid_decorators = (
            ast.SubNodeList[ast.Expr](items=valid_dec, kid=decorators)
            if len(valid_dec)
            else None
        )
        res = self.convert(node.args)
        sig: Optional[ast.FuncSignature] = (
            res if isinstance(res, ast.FuncSignature) else None
        )
        ret_sig = self.convert(node.returns) if node.returns else None
        if isinstance(ret_sig, ast.Expr):
            if not sig:
                sig = ast.FuncSignature(params=None, return_type=ret_sig, kid=[ret_sig])
            else:
                sig.return_type = ret_sig
                sig.add_kids_right([sig.return_type])
        kid = [name, sig, valid_body] if sig else [name, valid_body]
        ret = ast.Ability(
            name_ref=name,
            is_func=True,
            is_async=False,
            is_static=False,
            is_abstract=False,
            is_override=False,
            access=None,
            signature=sig,
            body=valid_body,
            decorators=valid_decorators,
            doc=doc,
            kid=kid,
        )
        return ret

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

        class ClassDef(stmt):name = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value=node.name,
            line=node.lineno,
            col_start=node.col_offset,
            col_end=node.col_offset + len(node.name),
            pos_start=0,
            pos_end=0,
            kid=[],
        )
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
            file_path=self.mod_path,
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
            file_path=self.mod_path,
            name=Tok.KW_OBJECT,
            value="object",
            line=node.lineno,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        body = [self.convert(i) for i in node.body]
        valid = [i for i in body if isinstance(i, ast.ArchBlockStmt)]
        if len(valid) != len(body):
            self.error("Length mismatch in classes body")
        valid_body = ast.SubNodeList[ast.ArchBlockStmt](items=valid, kid=body)

        base_classes = [self.convert(base) for base in node.bases]
        valid2: list[ast.Expr] = [
            base for base in base_classes if isinstance(base, ast.Expr)
        ]
        if len(valid2) != len(base_classes):
            raise self.ice("Length mismatch in base classes")
        valid_bases = (
            ast.SubNodeList[ast.Expr](items=valid2, kid=base_classes)
            if len(valid2)
            else None
        )
        body = [self.convert(i) for i in node.body]
        valid3 = [i for i in body if isinstance(i, ast.ArchBlockStmt)]
        if len(valid3) != len(body):
            raise self.ice("Length mismatch in classes body")
        valid_body = ast.SubNodeList[ast.ArchBlockStmt](items=valid3, kid=body)
        doc = None
        decorators = [self.convert(i) for i in node.decorator_list]
        valid_dec = [i for i in decorators if isinstance(i, ast.Expr)]
        if len(valid_dec) != len(decorators):
            raise self.ice("Length mismatch in decorators in class")
        valid_decorators = (
            ast.SubNodeList[ast.Expr](items=valid_dec, kid=decorators)
            if len(valid_dec)
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

    def proc_return(self, node: py_ast.Return) -> ast.Expr | None:
        """Process python node.

        class Return(stmt):
            __match_args__ = ("value",)
            value: expr | None
        """
        value = self.convert(node.value) if node.value else None
        if value and not isinstance(value, ast.Expr):
            raise self.ice("Invalid return value")
        else:
            return value

    def proc_delete(self, node: py_ast.Delete) -> ast.DeleteStmt:
        """Process python node.

        class Delete(stmt):
            __match_args__ = ("targets",)
            targets: list[expr]
        """
        exprs = [self.convert(target) for target in node.targets]
        valid_exprs = [expr for expr in exprs if isinstance(expr, ast.Expr)]
        if not len(valid_exprs) or len(valid_exprs) != len(exprs):
            raise self.ice("Length mismatch in delete targets")
        target = ast.SubNodeList[ast.Expr | ast.KWPair](items=[*valid_exprs], kid=exprs)
        return ast.DeleteStmt(
            target=(
                valid_exprs[0]
                if len(valid_exprs) > 1
                else ast.TupleVal(values=target, kid=[target])
            ),
            kid=exprs,
        )

    def proc_assign(self, node: py_ast.Assign) -> ast.Assignment:
        """Process python node.

        class Assign(stmt):
            targets: list[expr]
            value: expr
        """
        value = self.convert(node.value)
        if isinstance(value, (ast.Expr)):
            value_subtag = ast.SubTag[ast.Expr](tag=value, kid=[value])
        else:
            raise self.ice()

        targets = [self.convert(target) for target in node.targets]
        valid = [target for target in targets if isinstance(target, ast.Expr)]
        if len(valid) == len(targets):
            valid_targets = ast.SubNodeList[ast.Expr](items=valid, kid=valid)
        else:
            raise self.ice("Length mismatch in assignment targets")

        if isinstance(value, ast.Expr):
            return ast.Assignment(
                target=valid_targets,
                value=value,
                type_tag=value_subtag,
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
            isinstance(value, ast.Expr)
            and isinstance(target, ast.Expr)
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
        annotation = self.convert(node.annotation)
        if isinstance(annotation, ast.Expr):
            annotation = ast.SubTag[ast.Expr](tag=annotation, kid=[annotation])
        else:
            raise self.ice()
        value = self.convert(node.value) if node.value else None
        valid_types = Union[ast.Expr, ast.YieldExpr]
        if (
            isinstance(target, ast.SubNodeList)
            and (isinstance(value, valid_types) or not value)
            and isinstance(annotation, ast.Expr)
        ):
            return ast.Assignment(
                target=target,
                value=value,
                type_tag=annotation,
                kid=[target, annotation, value] if value else [target, annotation],
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
            raise self.ice("Length mismatch in for body")

        valid_body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        orelse = [self.convert(i) for i in node.orelse]
        valid_orelse = [i for i in orelse if isinstance(i, ast.CodeBlockStmt)]
        if len(valid_orelse) != len(orelse):
            raise self.ice("Length mismatch in for orelse")
        if orelse:
            valid_orelse = ast.SubNodeList[ast.CodeBlockStmt](
                items=valid_orelse, kid=orelse
            )
        else:
            valid_orelse = None

        return ast.InForStmt(
            target=target,
            is_async=True,
            collection=iter,
            body=valid_body,
            else_body=valid_orelse,
            kid=(
                [target, iter, valid_body, valid_orelse]
                if orelse
                else [target, iter, valid_body]
            ),
        )

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
            raise self.ice("Length mismatch in async for body")
        body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        orelse = [self.convert(stmt) for stmt in node.orelse]
        valid_orelse = [stmt for stmt in orelse if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_orelse) != len(orelse):
            raise self.ice("Length mismatch in async for orelse")
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
            raise self.ice("Length mismatch in async for body")
        body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        orelse = [self.convert(stmt) for stmt in node.orelse]
        valid_orelse = [stmt for stmt in orelse if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_orelse) != len(orelse):
            raise self.ice("Length mismatch in async for orelse")
        orelse = ast.SubNodeList[ast.CodeBlockStmt](items=valid_orelse, kid=orelse)
        raise self.ice(f"IMPLEMENT ME{test}")

    def proc_if(self, node: py_ast.If) -> ast.IfStmt:
        """Process If node.

        class If(stmt):
            __match_args__ = ("test", "body", "orelse")
            test: expr
            body: list[stmt]
            orelse: list[stmt]
        """
        test = self.convert(node.test)
        body = [self.convert(stmt) for stmt in node.body]
        valid_body = [
            stmt for stmt in body if isinstance(stmt, (ast.CodeBlockStmt, ast.Expr))
        ]
        if len(valid_body) != len(body):
            self.error("Length mismatch in async for body")
        body2 = ast.SubNodeList[ast.Expr](items=valid_body, kid=body)

        orelse = [self.convert(stmt) for stmt in node.orelse]
        valid_orelse = [
            stmt
            for stmt in orelse
            if isinstance(stmt, (ast.Expr, ast.IfStmt, ast.ElseIf, ast.ElseStmt))
        ]
        orelse2 = (
            ast.SubNodeList[ast.Expr](items=valid_orelse, kid=orelse)
            if valid_orelse
            else None
        )
        if isinstance(test, ast.Expr):
            ret = ast.IfStmt(
                condition=test,
                body=valid_body,
                else_body=valid_orelse,
                kid=[test, body2, orelse2] if orelse2 is not None else [test, body2],
            )
        else:
            self.ice()
        return ret

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
            raise self.ice("Length mismatch in with items")
        items = ast.SubNodeList[ast.ExprAsItem](items=valid_items, kid=items)
        body = [self.convert(stmt) for stmt in node.body]
        valid_body = [stmt for stmt in body if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            raise self.ice("Length mismatch in async for body")
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
            raise self.ice("Length mismatch in with items")
        items = ast.SubNodeList[ast.ExprAsItem](items=valid_items, kid=items)
        body = [self.convert(stmt) for stmt in node.body]
        valid_body = [stmt for stmt in body if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            raise self.ice("Length mismatch in async for body")
        body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        raise self.ice("IMPLEMENT ME")

    def proc_raise(self, node: py_ast.Raise) -> None:
        """Process python node."""

    def proc_assert(self, node: py_ast.Assert) -> None:
        """Process python node."""

    def proc_attribute(self, node: py_ast.Attribute) -> ast.AtomTrailer:
        """Proassignment targetscess python node.

        class Attribute(expr):
        if sys.version_info >= (3, 10):
            __match_args__ = ("value", "attr", "ctx")
        value: expr
        attr: _Identifier
        ctx: expr_context
        """
        value = self.convert(node.value)

        attribute = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value=node.attr,
            line=node.lineno,
            col_start=node.col_offset,
            col_end=node.col_offset + len(node.attr),
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        if isinstance(value, ast.Expr):
            ret = ast.AtomTrailer(
                target=value,
                right=attribute,
                is_attr=True,
                is_null_ok=False,
                kid=[value, attribute],
            )
        else:
            self.ice()
        return ret

    def proc_await(self, node: py_ast.Await) -> None:
        """Process python node."""

    def proc_bin_op(self, node: py_ast.BinOp) -> None:
        """Process python node.

        class BinOp(expr):
            if sys.version_info >= (3, 10):
                __match_args__ = ("left", "op", "right")
            left: expr
            op: operator
            right: expr
        """
        left = self.convert(node.left)
        op = self.convert(node.op)
        right = self.convert(node.right)
        if (
            isinstance(left, ast.Expr)
            and isinstance(op, ast.Token)
            and isinstance(right, ast.Expr)
        ):
            return ast.BinaryExpr(
                left=left,
                op=op,
                right=right,
                kid=[left, op, right],
            )
        else:
            raise self.ice()

    def proc_unary_op(self, node: py_ast.UnaryOp) -> None:
        """Process python node.

        class UnaryOp(expr):
            op: unaryop
            operand: expr
        """
        op = self.convert(node.op)
        operand = self.convert(node.operand)
        if isinstance(op, ast.Token) and isinstance(operand, ast.Expr):
            return ast.UnaryExpr(
                op=op,
                operand=operand,
                kid=[op, operand],
            )
        else:
            raise self.ice()

    def proc_bool_op(self, node: py_ast.BoolOp) -> None:
        """Process python node.

        class BoolOp(expr): a and b and c
            op: boolop
            values: list[expr]
        """
        op = self.convert(node.op)
        values = [self.convert(value) for value in node.values]
        valid = [value for value in values if isinstance(value, ast.Expr)]
        valid_values = ast.SubNodeList[ast.Expr](items=valid, kid=valid)
        print("okok")
        return ast.BoolExpr(op=op, values=valid, kid=[op, valid_values])

    def proc_break(self, node: py_ast.Break) -> None:
        """Process python node."""

    def proc_call(self, node: py_ast.Call) -> ast.FuncCall:
        """Process python node.

        class Call(expr):
        if sys.version_info >= (3, 10):
            __match_args__ = ("func", "args", "keywords")
        func: expr
        args: list[expr]
        keywords: list[keyword]
        """
        func = self.convert(node.func)
        params_in: list[ast.Expr | ast.KWPair] = []
        args = [self.convert(arg) for arg in node.args]
        keywords = [self.convert(keyword) for keyword in node.keywords]

        for i in args:
            if isinstance(i, ast.Expr):
                params_in.append(i)
        for i in keywords:
            if isinstance(i, ast.KWPair):
                params_in.append(i)
        if len(params_in) != 0:
            params_in2: ast.SubNodeList = ast.SubNodeList[ast.Expr | ast.KWPair](
                items=params_in, kid=params_in
            )
        else:
            params_in2 = None
        if isinstance(func, ast.Expr):
            return ast.FuncCall(
                target=func,
                params=params_in2,
                kid=[func, params_in2] if params_in2 else [func],
            )
        else:
            raise self.ice()

    def proc_compare(self, node: py_ast.Compare) -> ast.CompareExpr:
        """Process python node.

        class Compare(expr):
        if sys.version_info >= (3, 10):
            __match_args__ = ("left", "ops", "comparators")
        left: expr
        ops: list[cmpop]
        comparators: list[expr]
        """
        left = self.convert(node.left)
        comparators = [self.convert(comparator) for comparator in node.comparators]
        valid_comparators = [
            comparator for comparator in comparators if isinstance(comparator, ast.Expr)
        ]
        comparators2 = ast.SubNodeList[ast.Expr](
            items=valid_comparators, kid=comparators
        )
        ops = [self.convert(op) for op in node.ops]
        valid_ops = [op for op in ops if isinstance(op, ast.Token)]
        ops2 = ast.SubNodeList[ast.Token](items=valid_ops, kid=ops)

        kids = [left, ops2, comparators2]
        if (
            isinstance(left, ast.Expr)
            and len(ops) == len(valid_ops)
            and len(comparators) == len(valid_comparators)
        ):
            return ast.CompareExpr(
                left=left, rights=valid_comparators, ops=valid_ops, kid=kids
            )
        else:
            raise self.ice()

    def proc_constant(self, node: py_ast.Constant) -> ast.Literal:
        """Process python node.

        class Constant(expr):
            value: Any  # None, str, bytes, bool, int, float, complex, Ellipsis
            kind: str | None
            # Aliases for value, for backwards compatibility
            s: Any
            n: int | float | complex
        """
        type_mapping = {
            int: ast.Int,
            float: ast.Float,
            str: ast.String,
            bool: ast.Bool,
            type(None): ast.Null,
        }
        value_type = type(node.value)
        if value_type in type_mapping:
            if value_type is None:
                token_type = "NULL"
            elif value_type == str:
                token_type = "STRING"
            else:
                token_type = f"{value_type.__name__.upper()}"

            return type_mapping[value_type](
                file_path=self.mod_path,
                name=token_type,
                value=node.value,
                line=node.lineno,
                col_start=node.col_offset,
                col_end=node.col_offset + len(str(node.value)),
                pos_start=0,
                pos_end=0,
                kid=[],
            )
        else:
            raise self.ice()

    def proc_continue(self, node: py_ast.Continue) -> None:
        """Process python node."""

    def proc_dict(self, node: py_ast.Dict) -> None:
        """Process python node."""

    def proc_dict_comp(self, node: py_ast.DictComp) -> None:
        """Process python node."""

    def proc_ellipsis(self, node: py_ast.Ellipsis) -> None:
        """Process python node."""

    def proc_except_handler(self, node: py_ast.ExceptHandler) -> ast.Except:
        """Process python node.

        class ExceptHandler(excepthandler):
            type: expr | None
            name: _Identifier | None
            body: list[stmt]
        """
        type = self.convert(node.type) if node.type is not None else None
        name = (
            ast.Name(
                file_path=self.mod_path,
                name=Tok.NAME,
                value=node.name,
                line=node.lineno,
                col_start=node.col_offset,
                col_end=node.col_offset + len(node.name),
                pos_start=0,
                pos_end=0,
                kid=[],
            )
            if node.name is not None
            else None
        )
        body = [self.convert(i) for i in node.body]
        for i in body:
            print(i)
        valid = [i for i in body if isinstance(i, (ast.CodeBlockStmt))]
        if len(valid) != len(body):
            raise self.ice("Length mismatch in except handler body")
        valid_body = ast.SubNodeList[ast.CodeBlockStmt](items=valid, kid=valid)
        kid = []
        if type:
            kid.append(type)
        if name:
            kid.append(name)
        kid.append(valid_body)
        return ast.Except(
            ex_type=type,
            name=name,
            body=valid_body,
            kid=kid,
        )

    def proc_expr(self, node: py_ast.Expr) -> ast.ExprStmt:
        """Process python node.

        class Expr(stmt):
            value: expr
        """
        value = self.convert(node.value)
        if isinstance(value, ast.Expr):
            return ast.ExprStmt(expr=value, in_fstring=False, kid=[value])
        else:
            raise self.ice()

    def proc_formatted_value(self, node: py_ast.FormattedValue) -> ast.ExprStmt:
        """Process python node.

        class FormattedValue(expr):
        if sys.version_info >= (3, 10):
            __match_args__ = ("value", "conversion", "format_spec")
        value: expr
        conversion: int
        format_spec: expr | None
        """
        value = self.convert(node.value)
        if isinstance(value, ast.Expr):
            ret = ast.ExprStmt(
                expr=value,
                in_fstring=True,
                kid=[value],
            )
        else:
            self.ice()
        return ret

        # value = self.convert(node.value)
        # format_spec = self.convert(node.format_spec) if node.format_spec else None

    def proc_function_type(self, node: py_ast.FunctionType) -> None:
        """Process python node."""

    def proc_generator_exp(self, node: py_ast.GeneratorExp) -> None:
        """Process python node."""

    def proc_global(self, node: py_ast.Global) -> None:
        """Process python node."""

    def proc_if_exp(self, node: py_ast.IfExp) -> ast.IfElseExpr:
        """Process python node.

        class IfExp(expr):
            test: expr
            body: expr
            orelse: expr
        """
        test = self.convert(node.test)
        body = self.convert(node.body)
        orelse = self.convert(node.orelse)
        if (
            isinstance(test, ast.Expr)
            and isinstance(body, ast.Expr)
            and isinstance(orelse, ast.Expr)
        ):
            return ast.IfElseExpr(
                value=body, condition=test, else_value=orelse, kid=[body, test, orelse]
            )
        else:
            self.ice()

    def proc_import(self, node: py_ast.Import) -> ast.Import:
        """Process python node.

        class Import(stmt):
            names: list[alias]
        """
        names = [self.convert(name) for name in node.names]
        valid_names = [name for name in names if isinstance(name, ast.ExprAsItem)]
        if len(valid_names) != len(names):
            self.error("Length mismatch in import names")
        paths = []
        for name in valid_names:
            if isinstance(name.expr, ast.Name):
                paths.append(
                    ast.ModulePath(
                        path=[name.expr],
                        level=0,
                        alias=name.alias if name.alias is not None else None,
                        kid=[i for i in name.kid if i],
                    )
                )
            # Need to unravel atom trailers
            else:
                self.ice()
        lang = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value="py",
            line=node.lineno,
            col_start=node.col_offset,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        pytag = ast.SubTag[ast.Name](tag=lang, kid=[lang])
        ret = ast.Import(
            lang=pytag,
            paths=paths,
            items=None,
            is_absorb=False,
            kid=[pytag, *paths],
        )
        return ret

    def proc_import_from(self, node: py_ast.ImportFrom) -> ast.Import:
        """Process python node.

        class ImportFrom(stmt):
            module: str | None
            names: list[alias]
            level: int
        """
        lang = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value="py",
            line=node.lineno,
            col_start=node.col_offset,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        modpaths: list[ast.Name] = []
        if node.module:
            for i in node.module.split("."):
                modpaths.append(
                    ast.Name(
                        file_path=self.mod_path,
                        name=Tok.NAME,
                        value=i,
                        line=node.lineno,
                        col_start=0,
                        col_end=0,
                        pos_start=0,
                        pos_end=0,
                        kid=[],
                    )
                )
        path = ast.ModulePath(
            path=modpaths,
            level=node.level,
            alias=None,
            kid=modpaths,
        )
        names = [self.convert(name) for name in node.names]
        valid_names = []
        for name in names:
            if (
                isinstance(name, ast.ExprAsItem)
                and isinstance(name.expr, ast.Name)
                and isinstance(name.alias, ast.Name)
            ):
                valid_names.append(
                    ast.ModuleItem(
                        name=name.expr, alias=name.alias, kid=[i for i in name.kid if i]
                    )
                )
            else:
                self.ice()
        items = (
            ast.SubNodeList[ast.ModuleItem](items=valid_names, kid=valid_names)
            if valid_names
            else None
        )
        if not items:
            raise self.ice("No valid names in import from")
        pytag = ast.SubTag[ast.Name](tag=lang, kid=[lang])
        ret = ast.Import(
            lang=pytag,
            paths=[path],
            items=items,
            is_absorb=False,
            kid=[pytag, path, items],
        )
        return ret

    def proc_joined_str(self, node: py_ast.JoinedStr) -> ast.MultiString:
        """Process python node.

        class JoinedStr(expr):
        if sys.version_info >= (3, 10):
            __match_args__ = ("values",)
        values: list[expr]
        """
        values = [self.convert(value) for value in node.values]
        valid = [
            value for value in values if isinstance(value, (ast.String, ast.FString))
        ]
        return ast.MultiString(strings=valid, kid=values)

    def proc_lambda(self, node: py_ast.Lambda) -> None:
        """Process python node."""

    def proc_list(self, node: py_ast.List) -> ast.ListVal:
        """Process python node.

        class List(expr):
            elts: list[expr]
            ctx: expr_context
        """
        elts = [self.convert(elt) for elt in node.elts]
        valid_elts = [elt for elt in elts if isinstance(elt, ast.Expr)]
        if len(valid_elts) != len(elts):
            raise self.ice("Length mismatch in list elements")
        return ast.ListVal(
            values=(
                ast.SubNodeList[ast.Expr](items=valid_elts, kid=valid_elts)
                if valid_elts
                else None
            ),
            kid=valid_elts,
        )

    def proc_list_comp(self, node: py_ast.ListComp) -> None:
        """Process python node."""

    def proc_match(self, node: py_ast.Match) -> None:
        """Process python node."""

    def proc_match_as(self, node: py_ast.MatchAs) -> None:
        """Process python node."""

    def proc_match_class(self, node: py_ast.MatchClass) -> None:
        """Process python node."""

    def proc_match_mapping(self, node: py_ast.MatchMapping) -> None:
        """Process python node."""

    def proc_match_or(self, node: py_ast.MatchOr) -> None:
        """Process python node."""

    def proc_match_sequence(self, node: py_ast.MatchSequence) -> None:
        """Process python node."""

    def proc_match_singleton(self, node: py_ast.MatchSingleton) -> None:
        """Process python node."""

    def proc_match_star(self, node: py_ast.MatchStar) -> None:
        """Process python node."""

    def proc_match_value(self, node: py_ast.MatchValue) -> None:
        """Process python node."""

    def proc_name(self, node: py_ast.Name) -> ast.Name:
        """Process python node.

        class Name(expr):
        if sys.version_info >= (3, 10):
            __match_args__ = ("id", "ctx")
        id: _Identifier
        ctx: expr_context
        """
        ret = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value=node.id,
            line=node.lineno,
            col_start=node.col_offset,
            col_end=node.col_offset + len(node.id),
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_named_expr(self, node: py_ast.NamedExpr) -> None:
        """Process python node."""

    def proc_nonlocal(self, node: py_ast.Nonlocal) -> None:
        """Process python node."""

    def proc_pass(self, node: py_ast.Pass) -> ast.SubNodeList:
        """Process python node."""
        l_brace = ast.Token(
            file_path=self.mod_path,
            name=Tok.LBRACE,
            value="{",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        r_brace = ast.Token(
            file_path=self.mod_path,
            name=Tok.RBRACE,
            value="}",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ast.SubNodeList[ast.CodeBlockStmt | ast.ArchBlockStmt](
            items=[], kid=[l_brace, r_brace]
        )

    def proc_set(self, node: py_ast.Set) -> None:
        """Process python node."""

    def proc_set_comp(self, node: py_ast.SetComp) -> None:
        """Process python node."""

    def proc_slice(self, node: py_ast.Slice) -> ast.IndexSlice:
        """Process python node.

        class Slice(_Slice):
            lower: expr | None
            upper: expr | None
            step: expr | None
        """
        print("comes to slice")
        lower = self.convert(node.lower) if node.lower else None
        upper = self.convert(node.upper) if node.upper else None
        step = self.convert(node.step) if node.step else None
        return ast.IndexSlice(
            start=lower, stop=upper, step=step, is_range=True, kid=[lower, upper, step]
        )

    def proc_starred(self, node: py_ast.Starred) -> None:
        """Process python node."""

    def proc_subscript(self, node: py_ast.Subscript) -> None:
        """Process python node.

        class Subscript(expr):
            value: expr
            slice: _Slice
            ctx: expr_context
        """
        value = self.convert(node.value)
        slice = self.convert(node.slice)
        return ast.AtomTrailer(
            target=value,
            right=slice,
            is_attr=False,
            is_null_ok=False,
            kid=[value, slice],
        )

    def proc_try(self, node: py_ast.Try) -> ast.TryStmt:
        """Process python node.

        class Try(stmt):
            body: list[stmt]
            handlers: list[ExceptHandler]
            orelse: list[stmt]
            finalbody: list[stmt]
        """
        body = [self.convert(i) for i in node.body]
        valid = [i for i in body if isinstance(i, (ast.CodeBlockStmt))]
        if len(valid) != len(body):
            raise self.ice("Length mismatch in try body")
        # valid_body = ast.SubNodeList[ast.CodeBlockStmt](items=valid, kid=valid)

        handlers = [self.convert(i) for i in node.handlers]
        print("inside try: ", len(handlers))
        for i in handlers:
            print(i)

    def proc_try_star(self, node: py_ast.TryStar) -> None:
        """Process python node."""

    def proc_tuple(self, node: py_ast.Tuple) -> ast.TupleVal:
        """Process python node.

        class Tuple(expr):
            elts: list[expr]
            ctx: expr_context
        """
        elts = [self.convert(elt) for elt in node.elts]
        valid = [i for i in elts if isinstance(i, (ast.Expr, ast.KWPair))]
        if len(elts) != len(valid):
            raise self.ice("Length mismatch in tuple elts")
        valid_elts = ast.SubNodeList[ast.Expr | ast.KWPair](items=valid, kid=valid)
        return ast.TupleVal(values=valid_elts, kid=elts)

    def proc_yield(self, node: py_ast.Yield) -> None:
        """Process python node."""

    def proc_yield_from(self, node: py_ast.YieldFrom) -> None:
        """Process python node."""

    def proc_alias(self, node: py_ast.alias) -> ast.ExprAsItem:
        """Process python node.

        class alias(AST):
            name: _Identifier
            asname: _Identifier | None
        """
        name = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value=node.name,
            line=node.lineno,
            col_start=node.col_offset,
            col_end=node.col_offset + len(node.name),
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        asname = (
            ast.Name(
                file_path=self.mod_path,
                name=Tok.NAME,
                value=node.asname,
                line=node.lineno,
                col_start=node.col_offset,
                col_end=node.col_offset + len(node.asname),
                pos_start=0,
                pos_end=0,
                kid=[],
            )
            if node.asname
            else None
        )
        return ast.ExprAsItem(
            expr=name, alias=asname, kid=[name, asname] if asname else [name]
        )

    def proc_arg(self, node: py_ast.arg) -> ast.ParamVar:
        """Process python node.

        class arg(AST):
            arg: _Identifier
            annotation: expr | None
        """
        name = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value=node.arg,
            line=node.lineno,
            col_start=node.col_offset,
            col_end=node.col_offset + len(node.arg),
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        ann_expr = (
            self.convert(node.annotation)
            if node.annotation
            else ast.Name(
                file_path=self.mod_path,
                name=Tok.NAME,
                value="Any",
                line=node.lineno,
                col_start=node.col_offset,
                col_end=node.col_offset + 3,
                pos_start=0,
                pos_end=0,
                kid=[],
            )
        )
        if not isinstance(ann_expr, ast.Expr):
            raise self.ice("Expected annotation to be an expression")
        annot = ast.SubTag[ast.Expr](tag=ann_expr, kid=[ann_expr])
        paramvar = ast.ParamVar(
            name=name, type_tag=annot, unpack=None, value=None, kid=[name, annot]
        )
        return paramvar

    def proc_arguments(self, node: py_ast.arguments) -> ast.FuncSignature:
        """Process python node.

        class arguments(AST):
            args: list[arg]
            vararg: arg | None
            kwonlyargs: list[arg]
            kw_defaults: list[expr | None]
            kwarg: arg | None
            defaults: list[expr]
        """
        args = [self.convert(arg) for arg in node.args]
        vararg = self.convert(node.vararg) if node.vararg else None
        if vararg and isinstance(vararg, ast.ParamVar):
            vararg.unpack = ast.Token(
                file_path=self.mod_path,
                name=Tok.STAR_MUL,
                value="*",
                line=vararg.loc.first_line,
                col_start=vararg.loc.col_start,
                col_end=vararg.loc.col_end,
                pos_start=0,
                pos_end=0,
                kid=[],
            )
            vararg.add_kids_left([vararg.unpack])
        kwonlyargs = [self.convert(arg) for arg in node.kwonlyargs]
        for i in range(len(kwonlyargs)):
            kwa = kwonlyargs[i]
            kwd = node.kw_defaults[i]
            kwdefault = self.convert(kwd) if kwd else None
            if (
                kwdefault
                and isinstance(kwa, ast.ParamVar)
                and isinstance(kwdefault, ast.Expr)
            ):
                kwa.value = kwdefault
                kwa.add_kids_right([kwa.value])
        kwarg = self.convert(node.kwarg) if node.kwarg else None
        if kwarg and isinstance(kwarg, ast.ParamVar):
            kwarg.unpack = ast.Token(
                file_path=self.mod_path,
                name=Tok.STAR_POW,
                value="**",
                line=kwarg.loc.first_line,
                col_start=kwarg.loc.col_start,
                col_end=kwarg.loc.col_end,
                pos_start=0,
                pos_end=0,
                kid=[],
            )
            kwarg.add_kids_left([kwarg.unpack])
        defaults = [self.convert(expr) for expr in node.defaults if type(expr) is None]

        params = [*args]
        if vararg:
            params.append(vararg)
        params += kwonlyargs
        if kwarg:
            params.append(kwarg)
        params += defaults

        valid_params = [param for param in params if isinstance(param, ast.ParamVar)]
        if len(valid_params) != len(params):
            raise self.ice("Length mismatch in arguments")
        fs_params = ast.SubNodeList[ast.ParamVar](items=valid_params, kid=valid_params)
        return ast.FuncSignature(
            params=fs_params,
            return_type=None,
            kid=[fs_params],
        )

    def operator(self, tok: Tok, value: str) -> ast.Token:
        """Create an operator token."""
        return ast.Token(
            file_path=self.mod_path,
            name=tok,
            value=value,
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )

    def proc_and(self, node: py_ast.And) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.KW_AND, "and")

    def proc_or(self, node: py_ast.Or) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.KW_OR, "or")

    def proc_add(self, node: py_ast.Add) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.PLUS, "+")

    def proc_bit_and(self, node: py_ast.BitAnd) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.BW_AND, "&")

    def proc_bit_or(self, node: py_ast.BitOr) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.BW_OR, "|")

    def proc_bit_xor(self, node: py_ast.BitXor) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.BW_XOR, "^")

    def proc_div(self, node: py_ast.Div) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.DIV, "/")

    def proc_floor_div(self, node: py_ast.FloorDiv) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.FLOOR_DIV, "//")

    def proc_l_shift(self, node: py_ast.LShift) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.LSHIFT, "<<")

    def proc_mod(self, node: py_ast.Mod) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.MOD, "%")

    def proc_mult(self, node: py_ast.Mult) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.STAR_MUL, "*")

    def proc_mat_mult(self, node: py_ast.MatMult) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.DECOR_OP, "@")

    def proc_pow(self, node: py_ast.Pow) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.STAR_POW, "**")

    def proc_r_shift(self, node: py_ast.RShift) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.RSHIFT, ">>")

    def proc_sub(self, node: py_ast.Sub) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.MINUS, "-")

    def proc_invert(self, node: py_ast.Invert) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.BW_NOT, "~")

    def proc_not(self, node: py_ast.Not) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.NOT, "not")

    def proc_u_add(self, node: py_ast.UAdd) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.PLUS, "+")

    def proc_u_sub(self, node: py_ast.USub) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.MINUS, "-")

    def proc_eq(self, node: py_ast.Eq) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.EE, "==")

    def proc_gt(self, node: py_ast.Gt) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.GT, ">")

    def proc_gt_e(self, node: py_ast.GtE) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.GTE, ">=")

    def proc_in(self, node: py_ast.In) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.KW_IN, "in")

    def proc_is(self, node: py_ast.Is) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.KW_IS, "is")

    def proc_is_not(self, node: py_ast.IsNot) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.KW_ISN, "is not")

    def proc_lt(self, node: py_ast.Lt) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.LT, "<")

    def proc_lt_e(self, node: py_ast.LtE) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.LTE, "<=")

    def proc_not_eq(self, node: py_ast.NotEq) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.NE, "!=")

    def proc_not_in(self, node: py_ast.NotIn) -> ast.Token:
        """Process python node."""
        return self.operator(Tok.KW_NIN, "not in")

    def proc_comprehension(self, node: py_ast.comprehension) -> None:
        """Process python node."""

    def proc_keyword(self, node: py_ast.keyword) -> ast.KWPair:
        """Process python node.

        class keyword(AST):
        if sys.version_info >= (3, 10):
            __match_args__ = ("arg", "value")
        arg: _Identifier
        value: expr
        """
        if isinstance(node.value, ast.Expr):
            return ast.KWPair(key=node.arg, value=node.value, kid=[])
        else:
            raise self.ice()

    def proc_match_case(self, node: py_ast.match_case) -> None:
        """Process python node."""

    def proc_withitem(self, node: py_ast.withitem) -> None:
        """Process python node."""

    def proc_param_spec(self, node: py_ast.ParamSpec) -> None:
        """Process python node."""

    def proc_type_alias(self, node: py_ast.TypeAlias) -> None:
        """Process python node."""

    def proc_type_var(self, node: py_ast.TypeVar) -> None:
        """Process python node."""

    def proc_type_var_tuple(self, node: py_ast.TypeVarTuple) -> None:
        """Process python node."""

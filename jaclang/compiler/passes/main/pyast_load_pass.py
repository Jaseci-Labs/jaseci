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
        print(f"working on {type(node).__name__} ---------------------")
        if hasattr(self, f"proc_{pascal_to_snake(type(node).__name__)}"):
            return getattr(self, f"proc_{pascal_to_snake(type(node).__name__)}")(node)
        else:
            raise self.ice(f"Unknown node type {type(node).__name__}")

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
        valid = [
            i
            for i in elements
            if isinstance(i, (ast.ElementStmt, ast.String, ast.EmptyToken))
        ]
        if len(valid) != len(elements):
            self.error("Invalid module body")
        ret = ast.Module(
            name=self.mod_path.split(os.path.sep)[-1].split(".")[0],
            source=ast.JacSource("", mod_path=self.mod_path),
            doc=elements[0] if isinstance(elements[0], ast.String) else None,
            body=valid,
            is_imported=False,
            kid=elements,
        )
        ret.gen.py_ast = node
        return self.nu(ret)

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
        valid = [i for i in body if isinstance(i, (ast.CodeBlockStmt))]
        # if len(valid) != len(body):
        #     print("body:",body, "valid:", valid)
        #     self.error("Length mismatch in function body")
        valid_body = ast.SubNodeList[ast.CodeBlockStmt](items=valid, kid=body)
        doc = None
        decorators = [self.convert(i) for i in node.decorator_list]
        valid_dec = [i for i in decorators if isinstance(i, ast.Expr)]
        if len(valid_dec) != len(decorators):
            self.error("Length mismatch in decorators on function")
        valid_decorators = (
            ast.SubNodeList[ast.Expr](items=valid_dec, kid=decorators)
            if len(valid_dec)
            else None
        )
        res = self.convert(node.args)
        sig: Optional[ast.FuncSignature] | ast.Expr = (
            res if isinstance(res, ast.FuncSignature) else None
        )
        ret_sig = self.convert(node.returns) if node.returns else None
        if isinstance(ret_sig, ast.Expr):
            if not sig:
                sig = ret_sig
            else:
                sig.return_type = ast.SubTag[ast.Expr](tag=ret_sig, kid=[ret_sig])
                sig.add_kids_right([sig.return_type])
        kid = [name, sig, valid_body] if sig else [name, valid_body]
        ret = ast.Ability(
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
        # print("inside function def: \n", ret.pp())
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
        valid_body = [i for i in body if isinstance(i, (ast.ArchBlockStmt))]
        # for i in body:
        #     print(i)
        # for i in valid_body:
        #     print(i)
        if len(valid_body) != len(body):
            # print(len(body), len(valid_body))
            self.error("Length mismatch in classes body")
        valid_body = ast.SubNodeList[ast.ArchBlockStmt](items=valid_body, kid=body)

        base_classes = [self.convert(base) for base in node.bases]
        valid_bases = [base for base in base_classes if isinstance(base, ast.AtomExpr)]
        if len(valid_bases) != len(base_classes):
            self.error("Length mismatch in base classes")
        valid_bases = (
            ast.SubNodeList[ast.AtomExpr](items=valid_bases, kid=base_classes)
            if len(valid_bases)
            else None
        )
        doc = None
        decorators = [self.convert(i) for i in node.decorator_list]
        valid_decorators = [i for i in decorators if isinstance(i, ast.Expr)]
        if len(valid_decorators) != len(decorators):
            self.error("Length mismatch in decorators in class")
        valid_decorators = (
            ast.SubNodeList[ast.Expr](items=valid_decorators, kid=decorators)
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

    def proc_return(self, node: py_ast.Return) -> ast.Expr | None:
        """Process python node.

        class Return(stmt):
            __match_args__ = ("value",)
            value: expr | None
        """
        value = self.convert(node.value) if node.value else None
        if value and isinstance(value, ast.Expr):
            return value  # pavi made changes here. needs check
        else:
            return None

    def proc_delete(self, node: py_ast.Delete) -> ast.DeleteStmt:
        """Process python node.

        class Delete(stmt):
            __match_args__ = ("targets",)
            targets: list[expr]
        """
        exprs = [self.convert(target) for target in node.targets]
        valid_exprs = [expr for expr in exprs if isinstance(expr, ast.AtomExpr)]
        if not len(valid_exprs) or len(valid_exprs) != len(exprs):
            self.error("Length mismatch in delete targets")
        return ast.DeleteStmt(
            target=ast.SubNodeList[ast.AtomExpr](items=valid_exprs, kid=exprs),
            kid=exprs,
        )

    def proc_assign(self, node: py_ast.Assign) -> ast.Assignment:
        """Process python node.

        class Assign(stmt):
            targets: list[expr]
            value: expr
        """
        value = self.convert(node.value)
        if isinstance(value, ast.Expr):
            value_subtag = ast.SubTag[ast.Expr](tag=value, kid=[value])
        else:
            raise self.ice()

        targets = [self.convert(target) for target in node.targets]
        valid_targets = [target for target in targets if isinstance(target, ast.Expr)]
        if len(valid_targets) == len(targets):
            valid_targets2 = ast.SubNodeList[ast.Expr](items=valid_targets, kid=targets)
        else:
            raise self.ice("Length mismatch in assignment targets")

        if isinstance(value, ast.Expr):
            return ast.Assignment(
                target=valid_targets2,
                value=value,
                type_tag=value_subtag,
                kid=[valid_targets2, value],
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
        print("Body,Valid Body:    ", len(body), ",", len(valid_body))
        if len(valid_body) != len(body):
            self.error("Length mismatch in async for body")
        body2 = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)

        orelse = [self.convert(stmt) for stmt in node.orelse]
        valid_orelse = [
            stmt
            for stmt in orelse
            if isinstance(stmt, (ast.Expr, ast.IfStmt, ast.ElseIf, ast.ElseStmt))
        ]
        for i in valid_orelse:
            print("valid orelse: ", i)

        if valid_orelse:
            orelse2 = ast.SubNodeList[ast.Expr](items=valid_orelse, kid=valid_orelse)
        else:
            orelse2 = None
        print("orelse length:   ", len(orelse), len(valid_orelse))

        if isinstance(test, ast.Expr):
            ret = ast.IfStmt(
                condition=test,
                body=body2,
                else_body=orelse2,
                kid=[test, body2, orelse2] if orelse2 else [test, body2],
            )
        else:
            self.ice()
        print("return success ")
        # print(ret.condition, ret.body, ret.else_body)
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

    def proc_add(self, node: py_ast.Add) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.ADD_EQ,
            value="+",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_bit_and(self, node: py_ast.BitAnd) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.BW_AND_EQ,
            value="&",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_bit_or(self, node: py_ast.BitOr) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.BW_OR_EQ,
            value="|",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_bit_xor(self, node: py_ast.BitXor) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.BW_XOR_EQ,
            value="^",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_floor_div(self, node: py_ast.FloorDiv) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.DIV,
            value="/",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_lshift(self, node: py_ast.LShift) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.STAR_MUL,
            value="*",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_mod(self, node: py_ast.Mod) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.STAR_MUL,
            value="*",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_mult(self, node: py_ast.Mult) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.STAR_MUL,
            value="*",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_mat_mult(self, node: py_ast.MatMult) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.STAR_MUL,
            value="*",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_pow(self, node: py_ast.Pow) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.STAR_MUL,
            value="*",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_rshift(self, node: py_ast.RShift) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.STAR_MUL,
            value="*",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_sub(self, node: py_ast.Sub) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.STAR_MUL,
            value="*",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_eq(self, node: py_ast.Eq) -> ast.Token:
        """Process python node."""
        ret = ast.Token(
            file_path=self.mod_path,
            name=Tok.EQ,
            value="=",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        return ret

    def proc_bin_op(self, node: py_ast.BinOp) -> ast.BinaryExpr:
        """Process python node.

        class BinOp(expr):
        if sys.version_info >= (3, 10):
            __match_args__ = ("left", "op", "right")
        left: expr
        op: operator
        right: expr
        """
        left = self.convert(node.left)
        right = self.convert(node.right)
        op = self.convert(node.op)
        if (
            isinstance(left, ast.Expr)
            and isinstance(right, ast.Expr)
            and isinstance(op, (ast.Token, ast.DisconnectOp, ast.ConnectOp))
        ):
            return ast.BinaryExpr(
                left=left,
                op=op,
                right=right,
                kid=[left, op, right],
            )
        else:
            raise self.ice()

    def proc_bool_op(self, node: py_ast.BoolOp) -> None:
        """Process python node."""

        # class BoolOp(expr):
        # if sys.version_info >= (3, 10):
        #     __match_args__ = ("op", "values")
        # op: boolop
        # values: list[expr]
        # """
        # op = self.convert(node.op)
        # values =[self.convert(value) for value in node.values]
        # valid = [value for value in values if isinstance(value, ast.AtomExpr)]
        # return ast.Bool(
        # )

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
        l_paren = ast.Token(
            file_path=self.mod_path,
            name=Tok.LPAREN,
            value="(",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
        r_paren = ast.Token(
            file_path=self.mod_path,
            name=Tok.RPAREN,
            value=")",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
            kid=[],
        )
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
        parens = [l_paren, r_paren]
        if params_in:
            params_in2: ast.SubNodeList = ast.SubNodeList(
                items=params_in, kid=params_in
            )
        else:
            params_in2: ast.SubNodeList = ast.SubNodeList(items=params_in, kid=parens)
        if isinstance(func, ast.Expr):
            return ast.FuncCall(
                target=func,
                params=params_in2,
                kid=params_in if params_in else parens,
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
        ops = [self.convert(op) for op in node.ops]
        valid_ops = [op for op in ops if isinstance(op, ast.Token)]
        kids = [left]
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

    def proc_except_handler(self, node: py_ast.ExceptHandler) -> None:
        """Process python node."""

    def proc_expr(self, node: py_ast.Expr) -> ast.Expr:
        """Process python node.

        class Expr(stmt):
            value: expr
        """
        value = self.convert(node.value)
        if isinstance(value, ast.Expr):
            return value
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

    def proc_if_exp(self, node: py_ast.IfExp) -> None:
        """Process python node."""

    def proc_import(self, node: py_ast.Import) -> None:
        """Process python node."""

        # class Import(stmt):
        # if sys.version_info >= (3, 10):
        #     __match_args__ = ("names",)
        # names: list[alias]
        # """
        # names = [self.convert(name) for name in node.names]
        # valid_names = [name for name in names if isinstance(name, ast.ModuleItem)]
        # # if len(valid_names) != len(names):
        # #     self.error("Length mismatch in classes body")
        # valid_names2 = ast.SubNodeList[ast.ModuleItem](items=valid_names, kid=names)
        # ret = ast.Import(
        #     lang="py",
        #     path=ast.ModulePath,
        #     items=valid_names2,
        #     is_absorb=True,
        #     kid=[],
        # )
        # return ret

    def proc_import_from(self, node: py_ast.ImportFrom) -> None:
        """Process python node."""

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

    def proc_list(self, node: py_ast.List) -> None:
        """Process python node."""

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

    def proc_load(self, node: py_ast.Name) -> None:
        """Process python node."""
        # print(node.ctx, "...,")
        # param = ast.Name(
        #     file_path=self.mod_path,
        #     name=Tok.NAME,
        #     value=node.id,
        #     line=node.lineno,
        #     col_start=node.col_offset,
        #     col_end=node.col_offset + len(node.id),
        #     pos_start=0,
        #     pos_end=0,
        #     kid=[],
        # )
        # print("param is : ", param)
        # return param

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

    def proc_slice(self, node: py_ast.Slice) -> None:
        """Process python node."""

    def proc_starred(self, node: py_ast.Starred) -> None:
        """Process python node."""

    def proc_subscript(self, node: py_ast.Subscript) -> None:
        """Process python node."""

    def proc_try(self, node: py_ast.Try) -> None:
        """Process python node."""

    def proc_try_star(self, node: py_ast.TryStar) -> None:
        """Process python node."""

    def proc_tuple(self, node: py_ast.Tuple) -> None:
        """Process python node."""

    def proc_unary_op(self, node: py_ast.UnaryOp) -> None:
        """Process python node."""

    def proc_yield(self, node: py_ast.Yield) -> None:
        """Process python node."""

    def proc_yield_from(self, node: py_ast.YieldFrom) -> None:
        """Process python node."""

    def proc_alias(self, node: py_ast.alias) -> None:
        """Process python node."""

    def proc_arg(self, node: py_ast.arg) -> None:
        """Process python node.

        class arg(AST):
        if sys.version_info >= (3, 10):
            __match_args__ = ("arg", "annotation", "type_comment")
        arg: _Identifier
        annotation: expr | None
        """

    def proc_arguments(self, node: py_ast.arguments) -> None:
        """Process python node.

        class arguments(AST):
        if sys.version_info >= (3, 10):
            __match_args__ = ("posonlyargs", "args", "vararg", "kwonlyargs", "kw_defaults", "kwarg", "defaults")
        if sys.version_info >= (3, 8):
            posonlyargs: list[arg]
        args: list[arg]
        vararg: arg | None
        kwonlyargs: list[arg]
        kw_defaults: list[expr | None]
        kwarg: arg | None
        defaults: list[expr]
        """
        # args = [self.convert(arg) for arg in node.args]
        # vararg = node.vararg
        # kwonlyargs = [self.convert(arg) for arg in node.args]

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

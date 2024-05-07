"""Lark parser for Jac Lang."""

from __future__ import annotations

import ast as py_ast
import os
from typing import Optional, Sequence, TypeAlias, TypeVar

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
        # print(
        #     f"{node.__class__.__name__} - {[(k, type(v)) for k, v in vars(node).items()]}"
        # )

    def convert(self, node: py_ast.AST) -> ast.AstNode:
        """Get python node type."""
        # print(
        #     f"working on {type(node).__name__} line {node.lineno if hasattr(node, 'lineno') else 0}"
        # )
        if hasattr(self, f"proc_{pascal_to_snake(type(node).__name__)}"):
            ret = getattr(self, f"proc_{pascal_to_snake(type(node).__name__)}")(node)
        else:
            raise self.ice(f"Unknown node type {type(node).__name__}")
        # print(f"finshed {type(node).__name__} ---------------------")
        # print("normalizing", ret.__class__.__name__)
        # print(ret.unparse())
        # ret.unparse()
        return ret

    def transform(self, ir: ast.PythonModuleAst) -> ast.Module:
        """Transform input IR."""
        self.ir: ast.Module = self.proc_module(ir.ast)
        return self.ir

    def extract_with_entry(
        self, body: list[ast.AstNode], exclude_types: TypeAlias = T
    ) -> list[T | ast.ModuleCode]:
        """Extract with entry from a body."""

        def gen_mod_code(with_entry_body: list[ast.CodeBlockStmt]) -> ast.ModuleCode:
            with_entry_subnodelist = ast.SubNodeList[ast.CodeBlockStmt](
                items=with_entry_body,
                delim=Tok.WS,
                kid=with_entry_body,
                left_enc=self.operator(Tok.LBRACE, "{"),
                right_enc=self.operator(Tok.RBRACE, "}"),
            )
            return ast.ModuleCode(
                name=None,
                body=with_entry_subnodelist,
                kid=[with_entry_subnodelist],
                doc=None,
            )

        extracted: list[T | ast.ModuleCode] = []
        with_entry_body: list[ast.CodeBlockStmt] = []
        for i in body:
            if isinstance(i, exclude_types):
                if len(with_entry_body):
                    extracted.append(gen_mod_code(with_entry_body))
                    with_entry_body = []
                extracted.append(i)
            elif isinstance(i, ast.CodeBlockStmt):
                if isinstance(i, ast.ExprStmt) and isinstance(i.expr, ast.String):
                    self.convert_to_doc(i.expr)
                with_entry_body.append(i)
            else:
                self.ice("Invalid type for with entry body")
        if len(with_entry_body):
            extracted.append(gen_mod_code(with_entry_body))
        return extracted

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
        doc_str_list = [elements[0]] if isinstance(elements[0], ast.String) else []
        valid = (
            (doc_str_list)
            + self.extract_with_entry(elements[1:], (ast.ElementStmt, ast.EmptyToken))
            if doc_str_list
            else self.extract_with_entry(elements[:], (ast.ElementStmt, ast.EmptyToken))
        )
        doc_str = elements[0] if isinstance(elements[0], ast.String) else None
        self.convert_to_doc(doc_str) if doc_str else None
        ret = ast.Module(
            name=self.mod_path.split(os.path.sep)[-1].split(".")[0],
            source=ast.JacSource("", mod_path=self.mod_path),
            doc=doc_str,
            body=valid[1:] if valid and isinstance(valid[0], ast.String) else valid,
            is_imported=False,
            kid=valid,
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
        )
        body = [self.convert(i) for i in node.body]
        valid = [i for i in body if isinstance(i, (ast.CodeBlockStmt))]
        if len(valid) != len(body):
            raise self.ice("Length mismatch in function body")

        if (
            len(valid)
            and isinstance(valid[0], ast.ExprStmt)
            and isinstance(valid[0].expr, ast.String)
        ):
            doc = valid[0].expr
            self.convert_to_doc(doc)
            valid_body = ast.SubNodeList[ast.CodeBlockStmt](
                items=valid[1:],
                delim=Tok.WS,
                kid=valid[1:],
                left_enc=self.operator(Tok.LBRACE, "{"),
                right_enc=self.operator(Tok.RBRACE, "}"),
            )
        else:
            doc = None
            valid_body = ast.SubNodeList[ast.CodeBlockStmt](
                items=valid,
                delim=Tok.WS,
                kid=valid,
                left_enc=self.operator(Tok.LBRACE, "{"),
                right_enc=self.operator(Tok.RBRACE, "}"),
            )
        decorators = [self.convert(i) for i in node.decorator_list]
        valid_dec = [i for i in decorators if isinstance(i, ast.Expr)]
        if len(valid_dec) != len(decorators):
            raise self.ice("Length mismatch in decorators on function")
        valid_decorators = (
            ast.SubNodeList[ast.Expr](
                items=valid_dec, delim=Tok.DECOR_OP, kid=decorators
            )
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
        kid = ([doc] if doc else []) + (
            [name, sig, valid_body] if sig else [name, valid_body]
        )
        ret = ast.Ability(
            name_ref=name,
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

    def proc_class_def(self, node: py_ast.ClassDef) -> ast.Architype | ast.Enum:
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
        )
        arch_type = ast.Token(
            file_path=self.mod_path,
            name=Tok.KW_OBJECT,
            value="obj",
            line=node.lineno,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
        )
        body = [self.convert(i) for i in node.body]
        for body_stmt in body:
            if (
                isinstance(body_stmt, ast.Ability)
                and isinstance(body_stmt.name_ref, ast.Name)
                and body_stmt.name_ref.value == "__init__"
            ):
                tok = ast.Token(
                    file_path=self.mod_path,
                    name=Tok.KW_INIT,
                    value="init",
                    line=node.lineno,
                    col_start=node.col_offset,
                    col_end=node.col_offset + len("init"),
                    pos_start=0,
                    pos_end=0,
                )
                body_stmt.name_ref = ast.SpecialVarRef(var=tok, kid=[tok])
            if (
                isinstance(body_stmt, ast.Ability)
                and body_stmt.signature
                and isinstance(body_stmt.signature, ast.FuncSignature)
                and body_stmt.signature.params
            ):
                body_stmt.signature.params.items = [
                    param
                    for param in body_stmt.signature.params.items
                    if param.name.value != "self"
                ]
        doc = (
            body[0].expr
            if isinstance(body[0], ast.ExprStmt)
            and isinstance(body[0].expr, ast.String)
            else None
        )
        self.convert_to_doc(doc) if doc else None
        body = body[1:] if doc else body
        valid: list[ast.ArchBlockStmt] = (
            self.extract_with_entry(body, ast.ArchBlockStmt)
            if not (isinstance(body[0], ast.Semi) and len(body) == 1)
            else []
        )
        empty_block: Sequence[ast.AstNode] = [
            self.operator(Tok.LBRACE, "{"),
            self.operator(Tok.RBRACE, "}"),
        ]
        valid_body = ast.SubNodeList[ast.ArchBlockStmt](
            items=valid,
            delim=Tok.WS,
            kid=(valid if valid else empty_block),
            left_enc=self.operator(Tok.LBRACE, "{"),
            right_enc=self.operator(Tok.RBRACE, "}"),
        )
        converted_base_classes = [self.convert(base) for base in node.bases]
        base_classes: list[ast.Expr] = [
            base for base in converted_base_classes if isinstance(base, ast.Expr)
        ]
        valid_bases = (
            ast.SubNodeList[ast.Expr](
                items=base_classes, delim=Tok.COMMA, kid=base_classes
            )
            if base_classes
            else None
        )
        converted_decorators_list = [self.convert(i) for i in node.decorator_list]
        decorators = [i for i in converted_decorators_list if isinstance(i, ast.Expr)]
        valid_decorators = (
            ast.SubNodeList[ast.Expr](
                items=decorators, delim=Tok.DECOR_OP, kid=decorators
            )
            if decorators
            else None
        )
        if (
            base_classes
            and isinstance(base_classes[0], ast.Name)
            and base_classes[0].value == "Enum"
        ):
            if len(base_classes) > 1:
                raise ValueError(
                    "Python's Enum class cannot be used with multiple inheritance."
                )
            arch_type.name = Tok.KW_ENUM
            arch_type.value = "enum"
            valid_enum_body: list[ast.EnumBlockStmt] = []
            for class_body_stmt in node.body:
                converted_stmt = self.convert(class_body_stmt)
                if isinstance(converted_stmt, ast.EnumBlockStmt):
                    if isinstance(converted_stmt, ast.Assignment):
                        converted_stmt.is_enum_stmt = True
                    valid_enum_body.append(converted_stmt)
                else:
                    if isinstance(converted_stmt, ast.ExprStmt) and isinstance(
                        converted_stmt.expr, ast.String
                    ):
                        continue
                    tok = ast.Token(
                        file_path=self.mod_path,
                        name=Tok.PYNLINE,
                        value=py_ast.unparse(class_body_stmt),
                        line=node.lineno,
                        col_start=node.col_offset,
                        col_end=node.col_offset + len(py_ast.unparse(class_body_stmt)),
                        pos_start=0,
                        pos_end=0,
                    )
                    valid_enum_body.append(ast.PyInlineCode(code=tok, kid=[tok]))

            valid_enum_body2: list[ast.EnumBlockStmt] = [
                i for i in valid_enum_body if isinstance(i, ast.EnumBlockStmt)
            ]
            enum_body = ast.SubNodeList[ast.EnumBlockStmt](
                items=valid_enum_body2, delim=Tok.COMMA, kid=valid_enum_body2
            )
            if doc:
                doc.line_no = name.line_no
            return ast.Enum(
                name=name,
                access=None,
                base_classes=None,
                body=enum_body,
                kid=[doc, name, enum_body] if doc else [name, enum_body],
                doc=doc,
                decorators=valid_decorators,
            )
        kid = (
            [name, valid_bases, valid_body, doc]
            if doc and valid_bases
            else (
                [name, valid_bases, valid_body]
                if valid_bases
                else [name, valid_body, doc] if doc else [name, valid_body]
            )
        )
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

    def proc_return(self, node: py_ast.Return) -> ast.ReturnStmt | None:
        """Process python node.

        class Return(stmt):
            __match_args__ = ("value",)
            value: expr | None
        """
        value = self.convert(node.value) if node.value else None
        if not value:
            return ast.ReturnStmt(
                expr=None, kid=[self.operator(Tok.KW_RETURN, "return")]
            )
        elif value and isinstance(value, ast.Expr):
            return ast.ReturnStmt(expr=value, kid=[value])
        else:
            raise self.ice("Invalid return value")

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
        target = ast.SubNodeList[ast.Expr | ast.KWPair](
            items=[*valid_exprs], delim=Tok.COMMA, kid=exprs
        )
        target_1 = (
            valid_exprs[0]
            if len(valid_exprs) > 1
            else ast.TupleVal(values=target, kid=[target])
        )
        return ast.DeleteStmt(
            target=target_1,
            kid=[target],
        )

    def proc_assign(self, node: py_ast.Assign) -> ast.Assignment:
        """Process python node.

        class Assign(stmt):
            targets: list[expr]
            value: expr
        """
        value = self.convert(node.value)
        targets = [self.convert(target) for target in node.targets]
        valid = [target for target in targets if isinstance(target, ast.Expr)]
        if len(valid) == len(targets):
            valid_targets = ast.SubNodeList[ast.Expr](
                items=valid, delim=Tok.EQ, kid=valid
            )
        else:
            raise self.ice("Length mismatch in assignment targets")
        if isinstance(value, ast.Expr):
            return ast.Assignment(
                target=valid_targets,
                value=value,
                type_tag=None,
                kid=[valid_targets, value],
            )
        else:
            raise self.ice()

    def proc_aug_assign(self, node: py_ast.AugAssign) -> ast.Assignment:
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
            targ = ast.SubNodeList[ast.Expr](
                items=[target], delim=Tok.COMMA, kid=[target]
            )
            return ast.Assignment(
                target=targ,
                type_tag=None,
                mutable=True,
                aug_op=op,
                value=value,
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
            annotation_subtag = ast.SubTag[ast.Expr](tag=annotation, kid=[annotation])
        else:
            raise self.ice()
        value = self.convert(node.value) if node.value else None
        if (
            (isinstance(value, (ast.Expr, ast.YieldExpr)) or not value)
            and isinstance(annotation, ast.Expr)
            and isinstance(target, ast.Expr)
        ):
            target = ast.SubNodeList[ast.Expr](
                items=[target], delim=Tok.EQ, kid=[target]
            )
            return ast.Assignment(
                target=target,
                value=value if isinstance(value, (ast.Expr, ast.YieldExpr)) else None,
                type_tag=annotation_subtag,
                kid=(
                    [target, annotation_subtag, value]
                    if value
                    else [target, annotation_subtag]
                ),
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
        val_body = [i for i in body if isinstance(i, ast.CodeBlockStmt)]
        if len(val_body) != len(body):
            raise self.ice("Length mismatch in for body")

        valid_body = ast.SubNodeList[ast.CodeBlockStmt](
            items=val_body,
            delim=Tok.WS,
            kid=val_body,
            left_enc=self.operator(Tok.LBRACE, "{"),
            right_enc=self.operator(Tok.RBRACE, "}"),
        )
        orelse = [self.convert(i) for i in node.orelse]
        val_orelse = [i for i in orelse if isinstance(i, ast.CodeBlockStmt)]
        if len(val_orelse) != len(orelse):
            raise self.ice("Length mismatch in for orelse")
        if orelse:
            valid_orelse = ast.SubNodeList[ast.CodeBlockStmt](
                items=val_orelse,
                delim=Tok.WS,
                kid=orelse,
                left_enc=self.operator(Tok.LBRACE, "{"),
                right_enc=self.operator(Tok.RBRACE, "}"),
            )
        else:
            valid_orelse = None
        fin_orelse = (
            ast.ElseStmt(body=valid_orelse, kid=[valid_orelse])
            if valid_orelse
            else None
        )
        if isinstance(target, ast.Expr) and isinstance(iter, ast.Expr):
            return ast.InForStmt(
                target=target,
                is_async=False,
                collection=iter,
                body=valid_body,
                else_body=fin_orelse,
                kid=(
                    [target, iter, valid_body, fin_orelse]
                    if fin_orelse
                    else [target, iter, valid_body]
                ),
            )
        else:
            raise self.ice()

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
        body = [self.convert(i) for i in node.body]
        val_body = [i for i in body if isinstance(i, ast.CodeBlockStmt)]
        if len(val_body) != len(body):
            raise self.ice("Length mismatch in for body")

        valid_body = ast.SubNodeList[ast.CodeBlockStmt](
            items=val_body,
            delim=Tok.WS,
            kid=val_body,
            left_enc=self.operator(Tok.LBRACE, "{"),
            right_enc=self.operator(Tok.RBRACE, "}"),
        )
        orelse = [self.convert(i) for i in node.orelse]
        val_orelse = [i for i in orelse if isinstance(i, ast.CodeBlockStmt)]
        if len(val_orelse) != len(orelse):
            raise self.ice("Length mismatch in for orelse")
        if orelse:
            valid_orelse = ast.SubNodeList[ast.CodeBlockStmt](
                items=val_orelse,
                delim=Tok.WS,
                kid=orelse,
                left_enc=self.operator(Tok.LBRACE, "{"),
                right_enc=self.operator(Tok.RBRACE, "}"),
            )
        else:
            valid_orelse = None
        fin_orelse = (
            ast.ElseStmt(body=valid_orelse, kid=[valid_orelse])
            if valid_orelse
            else None
        )
        if isinstance(target, ast.Expr) and isinstance(iter, ast.Expr):
            return ast.InForStmt(
                target=target,
                is_async=True,
                collection=iter,
                body=valid_body,
                else_body=fin_orelse,
                kid=(
                    [target, iter, valid_body, fin_orelse]
                    if fin_orelse
                    else [target, iter, valid_body]
                ),
            )
        else:
            raise self.ice()

    def proc_while(self, node: py_ast.While) -> ast.WhileStmt:
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
            raise self.ice("Length mismatch in while body")
        fin_body = ast.SubNodeList[ast.CodeBlockStmt](
            items=valid_body,
            delim=Tok.WS,
            kid=valid_body,
            left_enc=self.operator(Tok.LBRACE, "{"),
            right_enc=self.operator(Tok.RBRACE, "}"),
        )
        if isinstance(test, ast.Expr):
            return ast.WhileStmt(
                condition=test,
                body=fin_body,
                kid=[test, fin_body],
            )
        else:
            raise self.ice()

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
        valid_body = [stmt for stmt in body if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in async for body")
        body2 = ast.SubNodeList[ast.CodeBlockStmt](
            items=valid_body,
            delim=Tok.WS,
            kid=body,
            left_enc=self.operator(Tok.LBRACE, "{"),
            right_enc=self.operator(Tok.RBRACE, "}"),
        )

        orelse = [self.convert(stmt) for stmt in node.orelse]
        valid_orelse = [
            stmt for stmt in orelse if isinstance(stmt, (ast.CodeBlockStmt))
        ]
        if valid_orelse:
            first_elm = valid_orelse[0]
            if isinstance(first_elm, ast.IfStmt):
                else_body: Optional[ast.ElseIf | ast.ElseStmt] = ast.ElseIf(
                    condition=first_elm.condition,
                    body=first_elm.body,
                    else_body=first_elm.else_body,
                    kid=first_elm.kid,
                )
            else:
                orelse2 = ast.SubNodeList[ast.CodeBlockStmt](
                    items=valid_orelse,
                    delim=Tok.WS,
                    kid=orelse,
                    left_enc=self.operator(Tok.LBRACE, "{"),
                    right_enc=self.operator(Tok.RBRACE, "}"),
                )
                else_body = ast.ElseStmt(body=orelse2, kid=[orelse2])
        else:
            else_body = None
        if isinstance(test, ast.Expr):
            ret = ast.IfStmt(
                condition=test,
                body=body2,
                else_body=else_body,
                kid=(
                    [test, body2, else_body] if else_body is not None else [test, body2]
                ),
            )
        else:
            raise self.ice()
        return ret

    def proc_with(self, node: py_ast.With) -> ast.WithStmt:
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
        items_sub = ast.SubNodeList[ast.ExprAsItem](
            items=valid_items, delim=Tok.COMMA, kid=items
        )
        body = [self.convert(stmt) for stmt in node.body]
        valid_body = [stmt for stmt in body if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            raise self.ice("Length mismatch in async for body")
        body_sub = ast.SubNodeList[ast.CodeBlockStmt](
            items=valid_body,
            delim=Tok.WS,
            kid=body,
            left_enc=self.operator(Tok.LBRACE, "{"),
            right_enc=self.operator(Tok.RBRACE, "}"),
        )
        return ast.WithStmt(
            is_async=False, exprs=items_sub, body=body_sub, kid=[items_sub, body_sub]
        )

    def proc_async_with(self, node: py_ast.AsyncWith) -> ast.WithStmt:
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
        items_sub = ast.SubNodeList[ast.ExprAsItem](
            items=valid_items, delim=Tok.COMMA, kid=items
        )
        body = [self.convert(stmt) for stmt in node.body]
        valid_body = [stmt for stmt in body if isinstance(stmt, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            raise self.ice("Length mismatch in async for body")
        body_sub = ast.SubNodeList[ast.CodeBlockStmt](
            items=valid_body,
            delim=Tok.WS,
            kid=body,
            left_enc=self.operator(Tok.LBRACE, "{"),
            right_enc=self.operator(Tok.RBRACE, "}"),
        )
        return ast.WithStmt(
            is_async=True, exprs=items_sub, body=body_sub, kid=[items_sub, body_sub]
        )

    def proc_raise(self, node: py_ast.Raise) -> ast.RaiseStmt:
        """Process python node.

        class Raise(stmt):
            exc: expr | None
            cause: expr | None
        """
        exc = self.convert(node.exc) if node.exc else None
        cause = self.convert(node.cause) if node.cause else None
        kid: list[ast.Expr | ast.Token] = []
        if isinstance(exc, ast.Expr):
            kid = [exc]
        if isinstance(cause, ast.Expr):
            kid.append(cause)
        if not (exc and cause):
            kid.append(self.operator(Tok.KW_RAISE, "raise"))
        if (isinstance(cause, ast.Expr) or cause is None) and (
            isinstance(exc, ast.Expr) or exc is None
        ):
            if node.exc and not node.cause:
                return ast.RaiseStmt(
                    cause=None,
                    from_target=None,
                    kid=[self.operator(Tok.KW_RAISE, "raise")],
                )
            else:
                return ast.RaiseStmt(cause=cause, from_target=exc, kid=kid)
        else:
            raise self.ice()

    def proc_assert(self, node: py_ast.Assert) -> ast.AssertStmt:
        """Process python node.

        class Assert(stmt):
            test: expr
            msg: expr | None
        """
        test = self.convert(node.test)
        msg = self.convert(node.msg) if node.msg is not None else None
        if isinstance(test, ast.Expr) and (isinstance(msg, ast.Expr) or msg is None):
            return ast.AssertStmt(
                condition=test,
                error_msg=msg,
                kid=[test, msg] if msg is not None else [test],
            )
        else:
            raise self.ice()

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
        )
        if isinstance(value, ast.Expr):
            return ast.AtomTrailer(
                target=value,
                right=attribute,
                is_attr=True,
                is_null_ok=False,
                kid=[value, attribute],
            )
        else:
            raise self.ice()

    def proc_await(self, node: py_ast.Await) -> ast.AwaitExpr:
        """Process python node.

        class Await(expr):
            value: expr
        """
        value = self.convert(node.value)
        if isinstance(value, ast.Expr):
            return ast.AwaitExpr(target=value, kid=[value])
        else:
            raise self.ice()

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

    def proc_unary_op(self, node: py_ast.UnaryOp) -> ast.UnaryExpr:
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

    def proc_bool_op(self, node: py_ast.BoolOp) -> ast.BoolExpr:
        """Process python node.

        class BoolOp(expr): a and b and c
            op: boolop
            values: list[expr]
        """
        op = self.convert(node.op)
        values = [self.convert(value) for value in node.values]
        valid = [value for value in values if isinstance(value, ast.Expr)]
        valid_values = ast.SubNodeList[ast.Expr](
            items=valid, delim=Tok.COMMA, kid=values
        )
        if isinstance(op, ast.Token) and len(valid) == len(values):
            return ast.BoolExpr(op=op, values=valid, kid=[op, valid_values])
        else:
            raise self.ice()

    def proc_break(self, node: py_ast.Break) -> ast.CtrlStmt:
        """Process python node."""
        break_tok = ast.Token(
            file_path=self.mod_path,
            name=Tok.KW_BREAK,
            value="break",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
        )
        return ast.CtrlStmt(ctrl=break_tok, kid=[break_tok])

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
            params_in2 = ast.SubNodeList[ast.Expr | ast.KWPair](
                items=params_in, delim=Tok.COMMA, kid=params_in
            )
        else:
            params_in2 = None
        if isinstance(func, ast.Expr):
            return ast.FuncCall(
                target=func,
                params=params_in2,
                genai_call=None,
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
            items=valid_comparators, delim=Tok.COMMA, kid=comparators
        )
        ops = [self.convert(op) for op in node.ops]
        valid_ops = [op for op in ops if isinstance(op, ast.Token)]
        ops2 = ast.SubNodeList[ast.Token](items=valid_ops, delim=Tok.COMMA, kid=ops)

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
            bytes: ast.String,
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
                value=(
                    f'"{repr(node.value)[1:-1]}"'
                    if value_type == str
                    else str(node.value)
                ),
                line=node.lineno,
                col_start=node.col_offset,
                col_end=node.col_offset + len(str(node.value)),
                pos_start=0,
                pos_end=0,
            )
        else:
            raise self.ice("Invalid type for constant")

    def proc_continue(self, node: py_ast.Continue) -> ast.CtrlStmt:
        """Process python node."""
        continue_tok = ast.Token(
            file_path=self.mod_path,
            name=Tok.KW_CONTINUE,
            value="continue",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
        )
        return ast.CtrlStmt(ctrl=continue_tok, kid=[continue_tok])

    def proc_dict(self, node: py_ast.Dict) -> ast.DictVal:
        """Process python node.

        class Dict(expr):
            keys: list[expr | None]
            values: list[expr]
        """
        keys = [self.convert(i) if i else None for i in node.keys]
        values = [self.convert(i) for i in node.values]
        valid_keys = [i for i in keys if isinstance(i, ast.Expr) or i is None]
        valid_values = [i for i in values if isinstance(i, ast.Expr)]
        kvpair: list[ast.KVPair] = []
        for i in range(len(values)):
            key_pluck = valid_keys[i]
            kvp = ast.KVPair(
                key=key_pluck,
                value=valid_values[i],
                kid=(
                    [key_pluck, valid_values[i]]
                    if key_pluck is not None
                    else [valid_values[i]]
                ),
            )
            kvpair.append(kvp)
        return ast.DictVal(
            kv_pairs=kvpair,
            kid=(
                [*kvpair]
                if len(kvpair)
                else [self.operator(Tok.LBRACE, "{"), self.operator(Tok.RBRACE, "}")]
            ),
        )

    def proc_dict_comp(self, node: py_ast.DictComp) -> ast.DictCompr:
        """Process python node.

        class DictComp(expr):
            key: expr
            value: expr
            generators: list[comprehension]
        """
        key = self.convert(node.key)
        value = self.convert(node.value)
        if isinstance(key, ast.Expr) and isinstance(value, ast.Expr):
            kv_pair = ast.KVPair(key=key, value=value, kid=[key, value])
        else:
            raise self.ice()
        generators = [self.convert(i) for i in node.generators]
        valid = [i for i in generators if isinstance(i, (ast.InnerCompr))]
        if len(valid) != len(generators):
            raise self.ice("Length mismatch in dict compr generators")
        compr = ast.SubNodeList[ast.InnerCompr](items=valid, delim=Tok.COMMA, kid=valid)
        return ast.DictCompr(kv_pair=kv_pair, compr=valid, kid=[kv_pair, compr])

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
        if not type:
            type = ast.Name(
                file_path=self.mod_path,
                name=Tok.NAME,
                value="Any",
                line=node.lineno,
                col_start=node.col_offset,
                col_end=node.col_offset + 3,
                pos_start=0,
                pos_end=0,
            )
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
            )
            if node.name is not None
            else None
        )

        body = [self.convert(i) for i in node.body]
        valid = [i for i in body if isinstance(i, (ast.CodeBlockStmt))]
        if len(valid) != len(body):
            raise self.ice("Length mismatch in except handler body")
        valid_body = ast.SubNodeList[ast.CodeBlockStmt](
            items=valid,
            delim=Tok.WS,
            kid=valid,
            left_enc=self.operator(Tok.LBRACE, "{"),
            right_enc=self.operator(Tok.RBRACE, "}"),
        )
        kid = []
        if type:
            kid.append(type)
        if name:
            kid.append(name)
        kid.append(valid_body)
        if isinstance(type, ast.Expr) and (isinstance(name, ast.Name) or not name):
            return ast.Except(
                ex_type=type,
                name=name,
                body=valid_body,
                kid=kid,
            )
        else:
            raise self.ice()

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
            raise self.ice()
        return ret

    def proc_function_type(self, node: py_ast.FunctionType) -> None:
        """Process python node."""

    def proc_generator_exp(self, node: py_ast.GeneratorExp) -> ast.GenCompr:
        """Process python node..

        class SetComp(expr):
            elt: expr
            generators: list[comprehension]
        """
        elt = self.convert(node.elt)
        generators = [self.convert(gen) for gen in node.generators]
        valid = [gen for gen in generators if isinstance(gen, ast.InnerCompr)]
        if len(generators) != len(valid):
            raise self.ice("Length mismatch in list comp generators")
        compr = ast.SubNodeList[ast.InnerCompr](items=valid, delim=Tok.COMMA, kid=valid)
        if isinstance(elt, ast.Expr):
            return ast.GenCompr(out_expr=elt, compr=valid, kid=[elt, compr])
        else:
            raise self.ice()

    def proc_global(self, node: py_ast.Global) -> ast.GlobalStmt:
        """Process python node.

        class Global(stmt):
            names: list[_Identifier]
        """
        names: list[ast.NameSpec] = []
        for id in node.names:
            names.append(
                ast.Name(
                    file_path=self.mod_path,
                    name=Tok.NAME,
                    value=id,
                    line=node.lineno,
                    col_start=node.col_offset,
                    col_end=node.col_offset + len(id),
                    pos_start=0,
                    pos_end=0,
                )
            )
        target = ast.SubNodeList[ast.NameSpec](items=names, delim=Tok.COMMA, kid=names)
        return ast.GlobalStmt(target=target, kid=[target])

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
            raise self.ice()

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
            if isinstance(name.expr, ast.Name) and (
                isinstance(name.alias, ast.Name) or name.alias is None
            ):
                paths.append(
                    ast.ModulePath(
                        path=[name.expr],
                        level=0,
                        alias=name.alias,
                        kid=[i for i in name.kid if i],
                    )
                )
            # Need to unravel atom trailers
            else:
                raise self.ice()
        lang = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value="py",
            line=node.lineno,
            col_start=node.col_offset,
            col_end=0,
            pos_start=0,
            pos_end=0,
        )
        pytag = ast.SubTag[ast.Name](tag=lang, kid=[lang])
        items = ast.SubNodeList[ast.ModulePath](items=paths, delim=Tok.COMMA, kid=paths)
        ret = ast.Import(
            hint=pytag,
            from_loc=None,
            items=items,
            is_absorb=False,
            kid=[pytag, items],
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
                and (isinstance(name.alias, ast.Name) or name.alias is None)
            ):
                valid_names.append(
                    ast.ModuleItem(
                        name=name.expr,
                        alias=name.alias if name.alias is not None else None,
                        kid=[i for i in name.kid if i],
                    )
                )
            else:
                raise self.ice()
        items = (
            ast.SubNodeList[ast.ModuleItem](
                items=valid_names, delim=Tok.COMMA, kid=valid_names
            )
            if valid_names
            else None
        )
        if not items:
            raise self.ice("No valid names in import from")
        pytag = ast.SubTag[ast.Name](tag=lang, kid=[lang])
        ret = ast.Import(
            hint=pytag,
            from_loc=path,
            items=items,
            is_absorb=False,
            kid=[pytag, path, items],
        )
        return ret

    def proc_joined_str(self, node: py_ast.JoinedStr) -> ast.FString:
        """Process python node.

        class JoinedStr(expr):
        if sys.version_info >= (3, 10):
            __match_args__ = ("values",)
        values: list[expr]
        """
        values = [self.convert(value) for value in node.values]
        valid = [
            value for value in values if isinstance(value, (ast.String, ast.ExprStmt))
        ]
        valid_values = ast.SubNodeList[ast.String | ast.ExprStmt](
            items=valid, delim=None, kid=valid
        )
        return ast.FString(parts=valid_values, kid=[valid_values])

    def proc_lambda(self, node: py_ast.Lambda) -> ast.LambdaExpr:
        """Process python node.

        class Lambda(expr):
            args: arguments
            body: expr
        """
        args = self.convert(node.args)
        body = self.convert(node.body)
        if isinstance(args, ast.FuncSignature) and isinstance(body, ast.Expr):
            return ast.LambdaExpr(signature=args, body=body, kid=[args, body])
        else:
            raise self.ice()

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
        l_square = self.operator(Tok.LSQUARE, "[")
        r_square = self.operator(Tok.RSQUARE, "]")
        return ast.ListVal(
            values=(
                ast.SubNodeList[ast.Expr](
                    items=valid_elts, delim=Tok.COMMA, kid=valid_elts
                )
                if valid_elts
                else None
            ),
            kid=[*valid_elts] if valid_elts else [l_square, r_square],
        )

    def proc_list_comp(self, node: py_ast.ListComp) -> ast.ListCompr:
        """Process python node.

        class ListComp(expr):
            elt: expr
            generators: list[comprehension]
        """
        elt = self.convert(node.elt)
        generators = [self.convert(gen) for gen in node.generators]
        valid = [gen for gen in generators if isinstance(gen, ast.InnerCompr)]
        if len(generators) != len(valid):
            raise self.ice("Length mismatch in list comp generators")
        compr = ast.SubNodeList[ast.InnerCompr](items=valid, delim=Tok.COMMA, kid=valid)
        if isinstance(elt, ast.Expr):
            return ast.ListCompr(out_expr=elt, compr=valid, kid=[elt, compr])
        else:
            raise self.ice()

    def proc_match(self, node: py_ast.Match) -> ast.MatchStmt:
        """Process python node.

        class Match(stmt):
            subject: expr
            cases: list[match_case]
        """
        subject = self.convert(node.subject)
        cases = [self.convert(i) for i in node.cases]
        valid = [case for case in cases if isinstance(case, ast.MatchCase)]
        if isinstance(subject, ast.Expr):
            return ast.MatchStmt(target=subject, cases=valid, kid=[subject, *valid])
        else:
            raise self.ice()

    def proc_match_as(self, node: py_ast.MatchAs) -> ast.MatchAs | ast.MatchWild:
        """Process python node.

        class MatchAs(pattern):
            pattern: _Pattern | None
            name: _Identifier | None
        """
        pattern = self.convert(node.pattern) if node.pattern else None
        name = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value=node.name if node.name else "_",
            line=node.lineno,
            col_start=node.col_offset,
            col_end=(
                (node.col_offset + len(node.name))
                if node.name
                else (node.col_offset + 1)
            ),
            pos_start=0,
            pos_end=0,
        )

        if isinstance(pattern, ast.MatchPattern):
            return ast.MatchAs(
                name=name,
                pattern=pattern,
                kid=[name, pattern] if pattern else [name],
            )
        else:
            return ast.MatchWild(kid=[name])

    def proc_match_class(self, node: py_ast.MatchClass) -> ast.MatchArch:
        """Process python node.

        class MatchClass(pattern):
            cls: expr
            patterns: list[pattern]
            kwd_attrs: list[_Identifier]
            kwd_patterns: list[pattern]
        """
        cls = self.convert(node.cls)
        kid = [cls]
        if len(node.patterns) != 0:
            patterns = [self.convert(i) for i in node.patterns]
            valid_patterns = [i for i in patterns if isinstance(i, ast.MatchPattern)]
            if len(patterns) == len(valid_patterns):
                patterns_sub = ast.SubNodeList[ast.MatchPattern](
                    items=valid_patterns, delim=Tok.COMMA, kid=valid_patterns
                )
                kid.append(patterns_sub)
            else:
                raise self.ice()
        else:
            patterns_sub = None

        if len(node.kwd_patterns):
            names: list[ast.Name] = []
            kv_pairs: list[ast.MatchKVPair] = []
            for kwd_attrs in node.kwd_attrs:
                names.append(
                    ast.Name(
                        file_path=self.mod_path,
                        name=Tok.NAME,
                        value=kwd_attrs,
                        line=node.lineno,
                        col_start=node.col_offset,
                        col_end=node.col_offset + len(kwd_attrs),
                        pos_start=0,
                        pos_end=0,
                    )
                )
            kwd_patterns = [self.convert(i) for i in node.kwd_patterns]
            valid_kwd_patterns = [
                i for i in kwd_patterns if isinstance(i, ast.MatchPattern)
            ]
            for i in range(len(kwd_patterns)):
                kv_pairs.append(
                    ast.MatchKVPair(
                        key=names[i],
                        value=valid_kwd_patterns[i],
                        kid=[names[i], valid_kwd_patterns[i]],
                    )
                )
            kw_patterns = ast.SubNodeList[ast.MatchKVPair](
                items=kv_pairs, delim=Tok.COMMA, kid=kv_pairs
            )
            kid.append(kw_patterns)
        else:
            kw_patterns = None
        if isinstance(cls, ast.NameSpec):
            return ast.MatchArch(
                name=cls, arg_patterns=patterns_sub, kw_patterns=kw_patterns, kid=kid
            )
        else:
            raise self.ice()

    def proc_match_mapping(self, node: py_ast.MatchMapping) -> ast.MatchMapping:
        """Process python node.

        class MatchMapping(pattern):
            keys: list[expr]
            patterns: list[pattern]
            rest: _Identifier | None
        """
        values: list[ast.MatchKVPair | ast.MatchStar] = []
        keys = [self.convert(i) for i in node.keys]
        valid_keys = [
            i for i in keys if isinstance(i, (ast.MatchPattern, ast.NameSpec))
        ]
        patterns = [self.convert(i) for i in node.patterns]
        valid_patterns = [i for i in patterns if isinstance(i, ast.MatchPattern)]
        for i in range(len(valid_keys)):
            kv_pair = ast.MatchKVPair(
                key=valid_keys[i],
                value=valid_patterns[i],
                kid=[valid_keys[i], valid_patterns[i]],
            )
            values.append(kv_pair)
        if node.rest:
            name = ast.Name(
                file_path=self.mod_path,
                name=Tok.NAME,
                value=node.rest,
                line=node.lineno,
                col_start=node.col_offset,
                col_end=node.col_offset + len(node.rest),
                pos_start=0,
                pos_end=0,
            )
            values.append(ast.MatchStar(name=name, is_list=True, kid=[name]))
        return ast.MatchMapping(values=values, kid=values)

    def proc_match_or(self, node: py_ast.MatchOr) -> ast.MatchOr:
        """Process python node.

        class MatchOr(pattern):
            patterns: list[pattern]
        """
        patterns = [self.convert(i) for i in node.patterns]
        valid = [i for i in patterns if isinstance(i, ast.MatchPattern)]
        return ast.MatchOr(patterns=valid, kid=valid)

    def proc_match_sequence(self, node: py_ast.MatchSequence) -> ast.MatchSequence:
        """Process python node.

        class MatchSequence(pattern):
            patterns: list[pattern]
        """
        patterns = [self.convert(i) for i in node.patterns]
        valid = [i for i in patterns if isinstance(i, ast.MatchPattern)]
        if len(patterns) == len(valid):
            return ast.MatchSequence(values=valid, kid=valid)
        else:
            raise self.ice()

    def proc_match_singleton(self, node: py_ast.MatchSingleton) -> ast.MatchSingleton:
        """Process python node.

        class MatchSingleton(pattern):
            value: Literal[True, False] | None
        """
        type = Tok.NULL if node.value is None else Tok.BOOL
        ret_type = ast.Null if node.value is None else ast.Bool
        value = ret_type(
            file_path=self.mod_path,
            name=type,
            value=str(node.value),
            line=node.lineno,
            col_start=node.col_offset,
            col_end=node.col_offset + len(str(node.value)),
            pos_start=0,
            pos_end=0,
        )
        if isinstance(value, (ast.Bool, ast.Null)):
            return ast.MatchSingleton(value=value, kid=[value])
        else:
            raise self.ice()

    def proc_match_star(self, node: py_ast.MatchStar) -> ast.MatchStar:
        """Process python node.

        class MatchStar(pattern):
            name: _Identifier | None
        """
        name = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value=node.name if node.name is not None else "_",
            line=node.lineno,
            col_start=node.col_offset,
            col_end=node.col_offset + len(node.name if node.name is not None else "_"),
            pos_start=0,
            pos_end=0,
        )
        return ast.MatchStar(name=name, is_list=True, kid=[name])

    def proc_match_value(self, node: py_ast.MatchValue) -> ast.MatchValue:
        """Process python node.

        class MatchValue(pattern):
            value: expr
        """
        value = self.convert(node.value)
        if isinstance(value, ast.Expr):
            return ast.MatchValue(value=value, kid=[value])
        else:
            raise self.ice()

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
        )
        return ret

    def proc_named_expr(self, node: py_ast.NamedExpr) -> ast.BinaryExpr:
        """Process python node.

        class NamedExpr(expr):
            target: Name
            value: expr
        """
        target = self.convert(node.target)
        value = self.convert(node.value)
        if isinstance(value, ast.Expr) and isinstance(target, ast.Name):
            return ast.BinaryExpr(
                left=target,
                op=self.operator(Tok.WALRUS_EQ, ":="),
                right=value,
                kid=[target, value],
            )
        else:
            raise self.ice()

    def proc_nonlocal(self, node: py_ast.Nonlocal) -> ast.NonLocalStmt:
        """Process python node.

        class Nonlocal(stmt):
            names: list[_Identifier]
        """
        names: list[ast.NameSpec] = []
        for name in node.names:
            names.append(
                ast.Name(
                    file_path=self.mod_path,
                    name=Tok.NAME,
                    value=name,
                    line=node.lineno,
                    col_start=node.col_offset,
                    col_end=node.col_offset + len(name),
                    pos_start=0,
                    pos_end=0,
                )
            )
        target = ast.SubNodeList[ast.NameSpec](items=names, delim=Tok.COMMA, kid=names)
        return ast.NonLocalStmt(target=target, kid=names)

    def proc_pass(self, node: py_ast.Pass) -> ast.Semi:
        """Process python node."""
        return ast.Semi(
            file_path=self.mod_path,
            name=Tok.SEMI,
            value=";",
            line=0,
            col_start=0,
            col_end=0,
            pos_start=0,
            pos_end=0,
        )

    def proc_set(self, node: py_ast.Set) -> ast.SetVal:
        """Process python node.

        class Set(expr):
            elts: list[expr]
        """
        if len(node.elts) != 0:
            elts = [self.convert(i) for i in node.elts]
            valid = [i for i in elts if isinstance(i, (ast.Expr))]
            if len(valid) != len(elts):
                raise self.ice("Length mismatch in set body")
            valid_elts = ast.SubNodeList[ast.Expr](
                items=valid, delim=Tok.COMMA, kid=valid
            )
            kid: list[ast.AstNode] = [*valid]
        else:
            valid_elts = None
            l_brace = self.operator(Tok.LBRACE, "{")
            r_brace = self.operator(Tok.RBRACE, "}")
            kid = [l_brace, r_brace]
        return ast.SetVal(values=valid_elts, kid=kid)

    def proc_set_comp(self, node: py_ast.SetComp) -> ast.ListCompr:
        """Process python node.

        class SetComp(expr):
            elt: expr
            generators: list[comprehension]
        """
        elt = self.convert(node.elt)
        generators = [self.convert(gen) for gen in node.generators]
        valid = [gen for gen in generators if isinstance(gen, ast.InnerCompr)]
        if len(generators) != len(valid):
            raise self.ice("Length mismatch in list comp generators")
        compr = ast.SubNodeList[ast.InnerCompr](items=valid, delim=Tok.COMMA, kid=valid)
        if isinstance(elt, ast.Expr):
            return ast.SetCompr(out_expr=elt, compr=valid, kid=[elt, compr])
        else:
            raise self.ice()

    def proc_slice(self, node: py_ast.Slice) -> ast.IndexSlice:
        """Process python node.

        class Slice(_Slice):
            lower: expr | None
            upper: expr | None
            step: expr | None
        """
        lower = self.convert(node.lower) if node.lower else None
        upper = self.convert(node.upper) if node.upper else None
        step = self.convert(node.step) if node.step else None
        valid_kid = [i for i in [lower, upper, step] if i]
        if not valid_kid:
            valid_kid = [self.operator(Tok.COLON, ":")]
        if (
            (isinstance(lower, ast.Expr) or lower is None)
            and (isinstance(upper, ast.Expr) or upper is None)
            and (isinstance(step, ast.Expr) or step is None)
        ):
            return ast.IndexSlice(
                start=lower,
                stop=upper,
                step=step,
                is_range=True,
                kid=valid_kid,
            )
        else:
            raise self.ice()

    def proc_starred(self, node: py_ast.Starred) -> ast.UnaryExpr:
        """Process python node.

        class Starred(expr):
            value: expr
            ctx: expr_context
        """
        star_tok = self.operator(Tok.STAR_MUL, "*")
        value = self.convert(node.value)
        if isinstance(value, ast.Expr):
            return ast.UnaryExpr(operand=value, op=star_tok, kid=[value, star_tok])
        else:
            raise self.ice()

    def proc_subscript(self, node: py_ast.Subscript) -> ast.AtomTrailer:
        """Process python node.

        class Subscript(expr):
            value: expr
            slice: _Slice
            ctx: expr_context
        """
        value = self.convert(node.value)
        slice = self.convert(node.slice)
        if not isinstance(slice, ast.IndexSlice) and isinstance(slice, ast.Expr):
            slice = ast.IndexSlice(
                start=slice,
                stop=None,
                step=None,
                is_range=False,
                kid=[slice],
            )
        if isinstance(value, ast.Expr) and isinstance(slice, ast.IndexSlice):
            return ast.AtomTrailer(
                target=value,
                right=slice,
                is_attr=False,
                is_null_ok=False,
                kid=[value, slice],
            )
        else:
            raise self.ice()

    def proc_try(self, node: py_ast.Try | py_ast.TryStar) -> ast.TryStmt:
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
        valid_body = ast.SubNodeList[ast.CodeBlockStmt](
            items=valid,
            delim=Tok.WS,
            kid=valid,
            left_enc=self.operator(Tok.LBRACE, "{"),
            right_enc=self.operator(Tok.RBRACE, "}"),
        )
        kid: list[ast.AstNode] = [valid_body]

        if len(node.handlers) != 0:
            handlers = [self.convert(i) for i in node.handlers]
            valid_handlers = [i for i in handlers if isinstance(i, (ast.Except))]
            if len(handlers) != len(valid_handlers):
                raise self.ice("Length mismatch in try handlers")
            excepts = ast.SubNodeList[ast.Except](
                items=valid_handlers, delim=Tok.WS, kid=valid_handlers
            )
            kid.append(excepts)
        else:
            excepts = None

        if len(node.orelse) != 0:
            orelse = [self.convert(i) for i in node.orelse]
            valid_orelse = [i for i in orelse if isinstance(i, (ast.CodeBlockStmt))]
            if len(orelse) != len(valid_orelse):
                raise self.ice("Length mismatch in try orelse")
            else_body = ast.SubNodeList[ast.CodeBlockStmt](
                items=valid_orelse,
                delim=Tok.WS,
                kid=valid_orelse,
                left_enc=self.operator(Tok.LBRACE, "{"),
                right_enc=self.operator(Tok.RBRACE, "}"),
            )
            kid.append(else_body)
        else:
            else_body = None

        if len(node.finalbody) != 0:
            finalbody = [self.convert(i) for i in node.finalbody]
            valid_finalbody = [
                i for i in finalbody if isinstance(i, (ast.CodeBlockStmt))
            ]
            if len(finalbody) != len(valid_finalbody):
                raise self.ice("Length mismatch in try finalbody")
            finally_body = ast.SubNodeList[ast.CodeBlockStmt](
                items=valid_finalbody,
                delim=Tok.WS,
                kid=valid_finalbody,
                left_enc=self.operator(Tok.LBRACE, "{"),
                right_enc=self.operator(Tok.RBRACE, "}"),
            )
            kid.append(finally_body)
        else:
            finally_body = None

        return ast.TryStmt(
            body=valid_body,
            excepts=excepts,
            else_body=(
                ast.ElseStmt(body=else_body, kid=[else_body]) if else_body else None
            ),
            finally_body=(
                ast.FinallyStmt(body=finally_body, kid=[finally_body])
                if finally_body
                else None
            ),
            kid=kid,
        )

    def proc_try_star(self, node: py_ast.TryStar) -> ast.TryStmt:
        """Process python node.

        class Try(stmt):
            body: list[stmt]
            handlers: list[ExceptHandler]
            orelse: list[stmt]
            finalbody: list[stmt]
        """
        return self.proc_try(node)

    def proc_tuple(self, node: py_ast.Tuple) -> ast.TupleVal:
        """Process python node.

        class Tuple(expr):
            elts: list[expr]
            ctx: expr_context
        """
        elts = [self.convert(elt) for elt in node.elts]
        if len(node.elts) != 0:
            valid = [i for i in elts if isinstance(i, (ast.Expr, ast.KWPair))]
            if len(elts) != len(valid):
                raise self.ice("Length mismatch in tuple elts")
            valid_elts = ast.SubNodeList[ast.Expr | ast.KWPair](
                items=valid, delim=Tok.COMMA, kid=valid
            )
            kid = elts
        else:
            l_paren = self.operator(Tok.LPAREN, "(")
            r_paren = self.operator(Tok.RPAREN, ")")
            valid_elts = None
            kid = [l_paren, r_paren]
        return ast.TupleVal(values=valid_elts, kid=kid)

    def proc_yield(self, node: py_ast.Yield) -> ast.YieldExpr:
        """Process python node.

        class Yield(expr):
            value: expr | None
        """
        value = self.convert(node.value) if node.value else None
        if isinstance(value, ast.Expr):
            return ast.YieldExpr(expr=value, with_from=False, kid=[value])
        else:
            raise self.ice()

    def proc_yield_from(self, node: py_ast.YieldFrom) -> ast.YieldExpr:
        """Process python node."""
        value = self.convert(node.value)
        if isinstance(value, ast.Expr):
            return ast.YieldExpr(expr=value, with_from=True, kid=[value])
        else:
            raise self.ice()

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
        if valid_params:
            fs_params = ast.SubNodeList[ast.ParamVar](
                items=valid_params, delim=Tok.COMMA, kid=valid_params
            )
            return ast.FuncSignature(
                params=fs_params,
                return_type=None,
                kid=[fs_params],
            )
        else:
            _lparen = self.operator(Tok.LPAREN, "(")
            _rparen = self.operator(Tok.RPAREN, ")")
            return ast.FuncSignature(
                params=None,
                return_type=None,
                kid=[_lparen, _rparen],
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

    def proc_comprehension(self, node: py_ast.comprehension) -> ast.InnerCompr:
        """Process python node.

        class comprehension(AST):
            target: expr
            iter: expr
            ifs: list[expr]
            is_async: int
        """
        target = self.convert(node.target)
        iter = self.convert(node.iter)
        if len(node.ifs) != 0:
            ifs_list = [self.convert(ifs) for ifs in node.ifs]
            valid = [ifs for ifs in ifs_list if isinstance(ifs, ast.Expr)]
        else:
            valid = None
        is_async = node.is_async > 0
        if isinstance(target, ast.Expr) and isinstance(iter, ast.Expr):
            return ast.InnerCompr(
                is_async=is_async,
                target=target,
                collection=iter,
                conditional=valid,
                kid=[target, iter, *valid] if valid else [target, iter],
            )
        else:
            raise self.ice()

    def proc_keyword(self, node: py_ast.keyword) -> ast.KWPair:
        """Process python node.

        class keyword(AST):
        if sys.version_info >= (3, 10):
            __match_args__ = ("arg", "value")
        arg: _Identifier | None
        value: expr
        """
        arg = ast.Name(
            file_path=self.mod_path,
            name=Tok.NAME,
            value=node.arg if node.arg is not None else "_",
            line=node.lineno,
            col_start=node.col_offset,
            col_end=node.col_offset + len(node.arg if node.arg is not None else "_"),
            pos_start=0,
            pos_end=0,
        )
        value = self.convert(node.value)
        if isinstance(value, ast.Expr):
            return ast.KWPair(key=arg, value=value, kid=[arg, value])
        else:
            raise self.ice()

    def proc_match_case(self, node: py_ast.match_case) -> ast.MatchCase:
        """Process python node.

        class match_case(AST):
            pattern: _Pattern
            guard: expr | None
            body: list[stmt]
        """
        pattern = self.convert(node.pattern)
        guard = self.convert(node.guard) if node.guard is not None else None
        body = [self.convert(i) for i in node.body]
        valid = [i for i in body if isinstance(i, ast.CodeBlockStmt)]
        if isinstance(pattern, ast.MatchPattern) and (
            isinstance(guard, ast.Expr) or guard is None
        ):
            return ast.MatchCase(
                pattern=pattern,
                guard=guard,
                body=valid,
                kid=(
                    [pattern, guard, *valid] if guard is not None else [pattern, *valid]
                ),
            )
        else:
            raise self.ice()

    def proc_withitem(self, node: py_ast.withitem) -> ast.ExprAsItem:
        """Process python node.

        class withitem(AST):
            context_expr: expr
            optional_vars: expr | None
        """
        context_expr = self.convert(node.context_expr)
        optional_vars = (
            self.convert(node.optional_vars) if node.optional_vars is not None else None
        )
        if isinstance(context_expr, ast.Expr) and (
            isinstance(optional_vars, ast.Expr) or optional_vars is None
        ):
            return ast.ExprAsItem(
                expr=context_expr,
                alias=optional_vars if optional_vars else None,
                kid=[context_expr, optional_vars] if optional_vars else [context_expr],
            )
        else:
            raise self.ice()

    def proc_param_spec(self, node: py_ast.ParamSpec) -> None:
        """Process python node."""

    def proc_type_alias(self, node: py_ast.TypeAlias) -> None:
        """Process python node."""

    def proc_type_var(self, node: py_ast.TypeVar) -> None:
        """Process python node."""

    def proc_type_var_tuple(self, node: py_ast.TypeVarTuple) -> None:
        """Process python node."""

    def convert_to_doc(self, string: ast.String) -> None:
        """Convert a string to a docstring."""
        string.value = f'""{string.value}""'

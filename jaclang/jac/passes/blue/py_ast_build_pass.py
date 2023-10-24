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

    def proc_node(self, node: py_ast.AST) -> ast.AstNode:  # type: ignore
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
        elements = [self.proc_node(i) for i in node.body]
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

    def proc_interactive(self, node: py_ast.Interactive) -> None:
        """Process python node.

        class Interactive(mod):
            __match_args__ = ("body",)
            body: list[stmt]
        """
        self.error(f"{node.__class__.__name__} Not Supported")

    def proc_expression(self, node: py_ast.Expression) -> None:
        """Process python node.

        class Expression(mod):
            __match_args__ = ("body",)
            body: expr
        """
        self.error(f"{node.__class__.__name__} Not Supported")

    def proc_function_def(
        self, node: py_ast.FunctionDef | py_ast.AsyncFunctionDef
    ) -> ast.Ability:
        """Process python node.

        class FunctionDef(stmt):
            __match_args__ = ("name", "args", "body", "decorator_list", "returns", "type_comment")
            name: _Identifier
            args: arguments
            body: list[stmt]
            decorator_list: list[expr]
            returns: expr | None
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
        body = [self.proc_node(i) for i in node.body]
        valid_body = [i for i in body if isinstance(i, ast.CodeBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in function body")
        valid_body = ast.SubNodeList[ast.CodeBlockStmt](items=valid_body, kid=body)
        doc = None
        decorators = [self.proc_node(i) for i in node.decorator_list]
        valid_decorators = [i for i in decorators if isinstance(i, ast.ExprType)]
        if len(valid_decorators) != len(decorators):
            self.error("Length mismatch in decorators on function")
        valid_decorators = (
            ast.SubNodeList[ast.ExprType](items=valid_decorators, kid=decorators)
            if len(valid_decorators)
            else None
        )
        res = self.proc_node(node.args)
        sig: Optional[ast.FuncSignature] | ast.ExprType = (
            res if isinstance(res, ast.FuncSignature) else None
        )
        ret_sig = self.proc_node(node.returns) if node.returns else None
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
            __match_args__ = ("name", "args", "body", "decorator_list", "returns", "type_comment")
            name: _Identifier
            args: arguments
            body: list[stmt]
            decorator_list: list[expr]
            returns: expr | None
        """
        ability = self.proc_function_def(node)
        ability.is_async = True
        return ability

    def proc_class_def(self, node: py_ast.ClassDef) -> ast.Architype:
        """Process python node.

        class ClassDef(stmt):
            __match_args__ = ("name", "bases", "keywords", "body", "decorator_list")
            name: _Identifier
            bases: list[expr]
            keywords: list[keyword]
            body: list[stmt]
            decorator_list: list[expr]
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
        base_classes = [self.proc_node(base) for base in node.bases]
        valid_bases = [base for base in base_classes if isinstance(base, ast.AtomType)]
        if len(valid_bases) != len(base_classes):
            self.error("Length mismatch in base classes")
        valid_bases = (
            ast.SubNodeList[ast.AtomType](items=valid_bases, kid=base_classes)
            if len(valid_bases)
            else None
        )
        body = [self.proc_node(i) for i in node.body]
        valid_body = [i for i in body if isinstance(i, ast.ArchBlockStmt)]
        if len(valid_body) != len(body):
            self.error("Length mismatch in classes body")
        valid_body = ast.SubNodeList[ast.ArchBlockStmt](items=valid_body, kid=body)
        doc = None
        decorators = [self.proc_node(i) for i in node.decorator_list]
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


# class Return(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("value",)
#     value: expr | None

# class Delete(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("targets",)
#     targets: list[expr]

# class Assign(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("targets", "value", "type_comment")
#     targets: list[expr]
#     value: expr

# class AugAssign(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("target", "op", "value")
#     target: Name | Attribute | Subscript
#     op: operator
#     value: expr

# class AnnAssign(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("target", "annotation", "value", "simple")
#     target: Name | Attribute | Subscript
#     annotation: expr
#     value: expr | None
#     simple: int

# class For(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("target", "iter", "body", "orelse", "type_comment")
#     target: expr
#     iter: expr
#     body: list[stmt]
#     orelse: list[stmt]

# class AsyncFor(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("target", "iter", "body", "orelse", "type_comment")
#     target: expr
#     iter: expr
#     body: list[stmt]
#     orelse: list[stmt]

# class While(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("test", "body", "orelse")
#     test: expr
#     body: list[stmt]
#     orelse: list[stmt]

# class If(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("test", "body", "orelse")
#     test: expr
#     body: list[stmt]
#     orelse: list[stmt]

# class With(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("items", "body", "type_comment")
#     items: list[withitem]
#     body: list[stmt]

# class AsyncWith(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("items", "body", "type_comment")
#     items: list[withitem]
#     body: list[stmt]

# class Raise(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("exc", "cause")
#     exc: expr | None
#     cause: expr | None

# class Try(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("body", "handlers", "orelse", "finalbody")
#     body: list[stmt]
#     handlers: list[ExceptHandler]
#     orelse: list[stmt]
#     finalbody: list[stmt]

# if sys.version_info >= (3, 11):
#     class TryStar(stmt):
#         __match_args__ = ("body", "handlers", "orelse", "finalbody")
#         body: list[stmt]
#         handlers: list[ExceptHandler]
#         orelse: list[stmt]
#         finalbody: list[stmt]

# class Assert(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("test", "msg")
#     test: expr
#     msg: expr | None

# class Import(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("names",)
#     names: list[alias]

# class ImportFrom(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("module", "names", "level")
#     module: str | None
#     names: list[alias]
#     level: int

# class Global(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("names",)
#     names: list[_Identifier]

# class Nonlocal(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("names",)
#     names: list[_Identifier]

# class Expr(stmt):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("value",)
#     value: expr

# class Pass(stmt): ...
# class Break(stmt): ...
# class Continue(stmt): ...
# class expr(AST): ...

# class BoolOp(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("op", "values")
#     op: boolop
#     values: list[expr]

# class BinOp(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("left", "op", "right")
#     left: expr
#     op: operator
#     right: expr

# class UnaryOp(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("op", "operand")
#     op: unaryop
#     operand: expr

# class Lambda(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("args", "body")
#     args: arguments
#     body: expr

# class IfExp(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("test", "body", "orelse")
#     test: expr
#     body: expr
#     orelse: expr

# class Dict(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("keys", "values")
#     keys: list[expr | None]
#     values: list[expr]

# class Set(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("elts",)
#     elts: list[expr]

# class ListComp(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("elt", "generators")
#     elt: expr
#     generators: list[comprehension]

# class SetComp(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("elt", "generators")
#     elt: expr
#     generators: list[comprehension]

# class DictComp(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("key", "value", "generators")
#     key: expr
#     value: expr
#     generators: list[comprehension]

# class GeneratorExp(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("elt", "generators")
#     elt: expr
#     generators: list[comprehension]

# class Await(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("value",)
#     value: expr

# class Yield(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("value",)
#     value: expr | None

# class YieldFrom(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("value",)
#     value: expr

# class Compare(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("left", "ops", "comparators")
#     left: expr
#     ops: list[cmpop]
#     comparators: list[expr]

# class Call(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("func", "args", "keywords")
#     func: expr
#     args: list[expr]
#     keywords: list[keyword]

# class FormattedValue(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("value", "conversion", "format_spec")
#     value: expr
#     conversion: int
#     format_spec: expr | None

# class JoinedStr(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("values",)
#     values: list[expr]

# if sys.version_info < (3, 8):
#     class Num(expr):  # Deprecated in 3.8; use Constant
#         n: int | float | complex

#     class Str(expr):  # Deprecated in 3.8; use Constant
#         s: str

#     class Bytes(expr):  # Deprecated in 3.8; use Constant
#         s: bytes

#     class NameConstant(expr):  # Deprecated in 3.8; use Constant
#         value: Any

#     class Ellipsis(expr): ...  # Deprecated in 3.8; use Constant

# class Constant(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("value", "kind")
#     value: Any  # None, str, bytes, bool, int, float, complex, Ellipsis
#     kind: str | None
#     # Aliases for value, for backwards compatibility
#     s: Any
#     n: int | float | complex

# if sys.version_info >= (3, 8):
#     class NamedExpr(expr):
#         if sys.version_info >= (3, 10):
#             __match_args__ = ("target", "value")
#         target: Name
#         value: expr

# class Attribute(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("value", "attr", "ctx")
#     value: expr
#     attr: _Identifier
#     ctx: expr_context

# if sys.version_info >= (3, 9):
#     _Slice: typing_extensions.TypeAlias = expr
# else:
#     class slice(AST): ...
#     _Slice: typing_extensions.TypeAlias = slice

# class Slice(_Slice):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("lower", "upper", "step")
#     lower: expr | None
#     upper: expr | None
#     step: expr | None

# if sys.version_info < (3, 9):
#     class ExtSlice(slice):
#         dims: list[slice]

#     class Index(slice):
#         value: expr

# class Subscript(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("value", "slice", "ctx")
#     value: expr
#     slice: _Slice
#     ctx: expr_context

# class Starred(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("value", "ctx")
#     value: expr
#     ctx: expr_context

# class Name(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("id", "ctx")
#     id: _Identifier
#     ctx: expr_context

# class List(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("elts", "ctx")
#     elts: list[expr]
#     ctx: expr_context

# class Tuple(expr):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("elts", "ctx")
#     elts: list[expr]
#     ctx: expr_context
#     if sys.version_info >= (3, 9):
#         dims: list[expr]

# class expr_context(AST): ...

# if sys.version_info < (3, 9):
#     class AugLoad(expr_context): ...
#     class AugStore(expr_context): ...
#     class Param(expr_context): ...

#     class Suite(mod):
#         body: list[stmt]

# class Del(expr_context): ...
# class Load(expr_context): ...
# class Store(expr_context): ...
# class boolop(AST): ...
# class And(boolop): ...
# class Or(boolop): ...
# class operator(AST): ...
# class Add(operator): ...
# class BitAnd(operator): ...
# class BitOr(operator): ...
# class BitXor(operator): ...
# class Div(operator): ...
# class FloorDiv(operator): ...
# class LShift(operator): ...
# class Mod(operator): ...
# class Mult(operator): ...
# class MatMult(operator): ...
# class Pow(operator): ...
# class RShift(operator): ...
# class Sub(operator): ...
# class unaryop(AST): ...
# class Invert(unaryop): ...
# class Not(unaryop): ...
# class UAdd(unaryop): ...
# class USub(unaryop): ...
# class cmpop(AST): ...
# class Eq(cmpop): ...
# class Gt(cmpop): ...
# class GtE(cmpop): ...
# class In(cmpop): ...
# class Is(cmpop): ...
# class IsNot(cmpop): ...
# class Lt(cmpop): ...
# class LtE(cmpop): ...
# class NotEq(cmpop): ...
# class NotIn(cmpop): ...

# class comprehension(AST):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("target", "iter", "ifs", "is_async")
#     target: expr
#     iter: expr
#     ifs: list[expr]
#     is_async: int

# class excepthandler(AST): ...

# class ExceptHandler(excepthandler):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("type", "name", "body")
#     REMOVEMEtype: expr | None
#     name: _Identifier | None
#     body: list[stmt]

# class arguments(AST):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("posonlyargs", "args", "vararg", "kwonlyargs", "kw_defaults", "kwarg", "defaults")
#     if sys.version_info >= (3, 8):
#         posonlyargs: list[arg]
#     args: list[arg]
#     vararg: arg | None
#     kwonlyargs: list[arg]
#     kw_defaults: list[expr | None]
#     kwarg: arg | None
#     defaults: list[expr]

# class arg(AST):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("arg", "annotation", "type_comment")
#     arg: _Identifier
#     annotation: expr | None

# class keyword(AST):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("arg", "value")
#     arg: _Identifier | None
#     value: expr

# class alias(AST):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("name", "asname")
#     name: _Identifier
#     asname: _Identifier | None

# class withitem(AST):
#     if sys.version_info >= (3, 10):
#         __match_args__ = ("context_expr", "optional_vars")
#     context_expr: expr
#     optional_vars: expr | None

# if sys.version_info >= (3, 10):
#     class Match(stmt):
#         __match_args__ = ("subject", "cases")
#         subject: expr
#         cases: list[match_case]

#     class pattern(AST): ...
#     # Without the alias, Pyright complains variables named pattern are recursively defined
#     _Pattern: typing_extensions.TypeAlias = pattern

#     class match_case(AST):
#         __match_args__ = ("pattern", "guard", "body")
#         pattern: _Pattern
#         guard: expr | None
#         body: list[stmt]

#     class MatchValue(pattern):
#         __match_args__ = ("value",)
#         value: expr

#     class MatchSingleton(pattern):
#         __match_args__ = ("value",)
#         value: Literal[True, False, None]

#     class MatchSequence(pattern):
#         __match_args__ = ("patterns",)
#         patterns: list[pattern]

#     class MatchStar(pattern):
#         __match_args__ = ("name",)
#         name: _Identifier | None

#     class MatchMapping(pattern):
#         __match_args__ = ("keys", "patterns", "rest")
#         keys: list[expr]
#         patterns: list[pattern]
#         rest: _Identifier | None

#     class MatchClass(pattern):
#         __match_args__ = ("cls", "patterns", "kwd_attrs", "kwd_patterns")
#         cls: expr
#         patterns: list[pattern]
#         kwd_attrs: list[_Identifier]
#         kwd_patterns: list[pattern]

#     class MatchAs(pattern):
#         __match_args__ = ("pattern", "name")
#         pattern: _Pattern | None
#         name: _Identifier | None

#     class MatchOr(pattern):
#         __match_args__ = ("patterns",)
#         patterns: list[pattern]

"""Transpilation pass for Jaseci Ast."""
from jaclang.jac.ast import AstNode
from jaclang.jac.passes.ir_pass import Pass

# flake8: noqa


class PyCodeGenPass(Pass):
    """Jac transpilation to python pass."""

    def __init__(self: "PyCodeGenPass") -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.indent_level = 0
        self.cur_arch = None  # tracks current architype during transpilation
        super().__init__()

    def indent_str(self: "PyCodeGenPass", indent_delta: int) -> str:
        """Return string for indent."""
        return " " * self.indent_size * (self.indent_level + indent_delta)

    def emit_ln(
        self: "PyCodeGenPass", node: AstNode, s: str, indent_delta: int = 0
    ) -> None:
        """Emit code to node."""
        node.py_code += (
            self.indent_str(indent_delta)
            + s.replace("\n", "\n" + self.indent_str(indent_delta))
            + "\n"
        )

    def emit(self: "PyCodeGenPass", node: AstNode, s: str) -> None:
        """Emit code to node."""
        node.py_code += s

    def exit_module(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert module to python code."""
        for i in node.elements:
            self.emit(node, i.py_code)
        self.ir = node

    def exit_doc_string(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert doc_string to python code."""
        self.emit_ln(node, node.value.value)

    def exit_global_vars(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert global vars to python code."""
        for i in node.values:
            self.emit_ln(node, i.py_code)

    def exit_named_assign(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert named assign to python code."""
        self.emit(node, f"{node.name.py_code} = {node.value.py_code}")

    # class NamedAssign(AstNode):
    # class Test(AstNode):
    # class Import(AstNode):
    # class ModulePath(AstNode):
    # class ModuleItem(AstNode):
    # class ArchDecl(AstNode):
    # class ArchDef(AstNode):
    # class ObjectArch(AstNode):
    # class NodeArch(ObjectArch):
    # class EdgeArch(ObjectArch):
    # class WalkerArch(ObjectArch):
    # class SpawnerArch(AstNode):
    # class FuncArch(AstNode):
    # class BaseClasses(AstNode):
    # class AbilitySpec(AstNode):
    # class ArchBlock(AstNode):
    # class HasStmt(AstNode):
    # class ParamVar(AstNode):
    # class HasVar(ParamVar):
    # class HasVarTags(AstNode):
    # class TypeSpec(AstNode):
    # class CanDS(AstNode):
    # class CanMethod(CanDS):
    # class EventSignature(AstNode):
    # class MethodSignature(AstNode):
    # class NameList(AstNode):
    # class MethodParams(AstNode):
    # class CodeBlock(AstNode):
    # class IfStmt(AstNode):
    # class ElseIfs(AstNode):
    # class ElseStmt(AstNode):
    # class TryStmt(AstNode):
    # class ExceptList(AstNode):
    # class Except(AstNode):
    # class FinallyStmt(AstNode):
    # class IterForStmt(AstNode):
    # class InForStmt(AstNode):
    # class DictForStmt(AstNode):
    # class WhileStmt(AstNode):
    # class RaiseStmt(AstNode):
    # class AssertStmt(AstNode):
    # class CtrlStmt(AstNode):
    # class DeleteStmt(AstNode):
    # class ReportStmt(AstNode):
    # class ReturnStmt(AstNode):
    # class IgnoreStmt(AstNode):
    # class VisitStmt(AstNode):
    # class RevisitStmt(AstNode):
    # class DisengageStmt(AstNode):
    # class YeildStmt(AstNode):
    # class SyncStmt(AstNode):
    # class Assignment(AstNode):
    # class IfElseExpr(AstNode):
    # class BinaryExpr(AstNode):
    # class UnaryExpr(AstNode):
    # class SpawnWalkerExpr(AstNode):
    # class SpawnObjectExpr(AstNode):
    # class SpawnEdgeNodeExpr(AstNode):
    # class UnpackExpr(AstNode):
    # class RefExpr(AstNode):
    # class MultiString(AstNode):
    # class ExprList(AstNode):
    # class AssignmentList(ExprList):
    # class ListVal(ExprList):
    # class DictVal(AstNode):
    # class KVPair(AstNode):
    # class AtomTrailer(AstNode):
    # class DSCall(AstNode):
    # class FuncCall(AstNode):
    # class ParamList(AstNode):
    # class IndexSlice(AstNode):
    # class GlobalRef(AstNode):
    # class NodeRef(GlobalRef):
    # class EdgeRef(GlobalRef):
    # class WalkerRef(GlobalRef):
    # class SpawnerRef(GlobalRef):
    # class FuncRef(GlobalRef):
    # class ObjectRef(GlobalRef):
    # class AbilityRef(GlobalRef):
    # class EdgeOpRef(AstNode):
    # class ConnectOp(AstNode):
    # class DisconnectOp(EdgeOpRef):
    # class FilterCtx(AstNode):
    # class SpawnCtx(AstNode):

    def enter_node(self: Pass, node: AstNode) -> None:
        node.py_code = ""
        return super().enter_node(node)

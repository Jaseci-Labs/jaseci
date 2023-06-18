"""Transpilation pass for Jaseci Ast."""
from jaclang.jac.ast import AstNode, is_blank
from jaclang.jac.passes.ir_pass import Pass


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
        if not is_blank(node.doc):
            self.emit_ln(node, node.doc.py_code)
        self.emit(node, node.body.py_code)
        self.ir = node

    def exit_elements(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert module to python code."""
        for i in node.elements:
            self.emit(node, i.py_code)

    def exit_doc_string(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert doc_string to python code."""
        if not is_blank(node.value):
            self.emit_ln(node, node.value.value)

    def exit_global_vars(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert global vars to python code."""
        self.emit_ln(node, node.assignments.py_code)

    def exit_named_assign(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert named assign to python code."""
        self.emit(node, f"{node.name.py_code} = {node.value.py_code}")

    def exit_test(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert test to python code."""
        # TODO: implement

    def exit_import(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert import to python code."""
        if is_blank(node.items):
            if is_blank(node.alias):
                self.emit_ln(node, f"import {node.path.py_code}")
            else:
                self.emit_ln(
                    node, f"import {node.path.py_code} as {node.alias.py_code}"
                )
        else:
            for i in node.items:
                self.emit_ln(node, f"from {node.path.py_code} import {i.py_code}")

    def exit_module_path(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert module path to python code."""
        self.emit(node, "".join([i.value for i in node.path]))

    def exit_module_item(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert module item to python code."""
        if is_blank(node.alias):
            self.emit(node, node.name.value)
        else:
            self.emit(node, node.name.value + " as " + node.alias.value)

    # class ArchDecl(AstNode):
    # class ArchDef(AstNode):

    def enter_architype(self: "PyCodeGenPass", node: AstNode) -> None:
        """Enter architype."""
        if not is_blank(node.doc.value):
            self.emit(node, node.doc.value)

    def exit_architype(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert object arch to python code."""
        if is_blank(node.base_classes):
            self.emit_ln(node, f"class {node.name.py_code}:")
        else:
            self.emit_ln(
                node,
                f"class {node.name.py_code}({node.base_classes.py_code}):",
            )
        self.emit(node, node.body.py_code)

    # class NodeArch(ObjectArch):
    # class EdgeArch(ObjectArch):
    # class WalkerArch(ObjectArch):

    def exit_func_arch(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert func arch to python code."""
        self.emit_ln(node, f"def {node.name.py_code}({node.signature.py_code}):")
        self.emit(node, node.body.py_code)
        self.indent_level -= 1

    def exit_base_classes(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert base classes to python code."""
        self.emit(node, ", ".join([i.value for i in node.base_classes]))

    # class AbilitySpec(AstNode):

    def enter_arch_block(self: "PyCodeGenPass", node: AstNode) -> None:
        """Enter arch block."""
        self.indent_level += 1

    def exit_arch_block(self: "PyCodeGenPass", node: AstNode) -> None:
        """Exit arch block."""
        self.indent_level -= 1

    # def exit_arch_members(self: "PyCodeGenPass", node: AstNode) -> None:
    #     """Exit arch block."""
    #     for i in node.members:
    #         self.emit(node, i.py_code)

    # class HasStmt(AstNode):
    #     """HasStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "HasStmt",
    #         access: AstNode,
    #         vars: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize has statement node."""
    #         self.access = access
    #         self.vars = vars
    #         super().__init__(*args, **kwargs)

    # class ParamVar(AstNode):
    #     """ParamVar node type for Jac Ast."""

    #     def __init__(
    #         self: "ParamVar",
    #         name: AstNode,
    #         type_tag: AstNode,
    #         value: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize has var node."""
    #         self.name = name
    #         self.type_tag = type_tag
    #         self.value = value
    #         super().__init__(*args, **kwargs)

    # class HasVar(ParamVar):
    #     """HasVar node type for Jac Ast."""

    #     def __init__(
    #         self: "HasVar",
    #         tags: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize has var node."""
    #         self.tags = tags
    #         super().__init__(*args, **kwargs)

    # class HasVarTags(AstNode):
    #     """HasVarTags node type for Jac Ast."""

    #     def __init__(
    #         self: "HasVarTags",
    #         tags: list,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize has var tags node."""
    #         self.tags = tags
    #         super().__init__(*args, **kwargs)

    # class TypeSpec(AstNode):
    #     """TypeSpec node type for Jac Ast."""

    #     def __init__(
    #         self: "TypeSpec",
    #         typ: AstNode,
    #         nested1: AstNode,  # needed for lists
    #         nested2: AstNode,  # needed for dicts
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize type spec node."""
    #         self.typ = typ
    #         self.nested1 = nested1
    #         self.nested2 = nested2
    #         super().__init__(*args, **kwargs)

    # class CanDS(AstNode):
    #     """CanDS node type for Jac Ast."""

    #     def __init__(
    #         self: "CanDS",
    #         name: AstNode,
    #         access: AstNode,
    #         signature: AstNode,
    #         body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize can statement node."""
    #         self.name = name
    #         self.access = access
    #         self.signature = signature
    #         self.body = body
    #         super().__init__(*args, **kwargs)

    # class CanMethod(CanDS):
    #     """CanMethod node type for Jac Ast."""

    # class EventSignature(AstNode):
    #     """EventSignature node type for Jac Ast."""

    #     def __init__(
    #         self: "EventSignature",
    #         event: AstNode,
    #         arch_access: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize event signature node."""
    #         self.event = event
    #         self.arch_access = arch_access
    #         super().__init__(*args, **kwargs)

    # class FuncSignature(AstNode):
    #     """FuncSignature node type for Jac Ast."""

    #     def __init__(
    #         self: "FuncSignature",
    #         params: AstNode,
    #         return_type: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize method signature node."""
    #         self.params = params
    #         self.return_type = return_type
    #         super().__init__(*args, **kwargs)

    # class NameList(AstNode):
    #     """NameList node type for Jac Ast."""

    #     def __init__(
    #         self: "NameList",
    #         names: list,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize name list node."""
    #         self.names = names
    #         super().__init__(*args, **kwargs)

    # class FuncParams(AstNode):
    #     """ArchBlock node type for Jac Ast."""

    #     def __init__(
    #         self: "FuncParams",
    #         params: list,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize method params node."""
    #         self.params = params
    #         super().__init__(*args, **kwargs)

    # class CodeBlock(AstNode):
    #     """CodeBlock node type for Jac Ast."""

    #     def __init__(
    #         self: "CodeBlock",
    #         body: list,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize code block node."""
    #         self.body = body
    #         super().__init__(*args, **kwargs)

    # class IfStmt(AstNode):
    #     """IfStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "IfStmt",
    #         condition: AstNode,
    #         body: AstNode,
    #         elseifs: AstNode,
    #         else_body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize if statement node."""
    #         self.condition = condition
    #         self.body = body
    #         self.elseifs = elseifs
    #         self.else_body = else_body
    #         super().__init__(*args, **kwargs)

    # class ElseIfs(AstNode):
    #     """ElseIfs node type for Jac Ast."""

    #     def __init__(
    #         self: "ElseIfs",
    #         elseifs: list,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize elseifs node."""
    #         self.elseifs = elseifs
    #         super().__init__(*args, **kwargs)

    # class ElseStmt(AstNode):
    #     """Else node type for Jac Ast."""

    #     def __init__(
    #         self: "ElseStmt",
    #         body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize else node."""
    #         self.body = body
    #         super().__init__(*args, **kwargs)

    # class TryStmt(AstNode):
    #     """TryStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "TryStmt",
    #         body: AstNode,
    #         excepts: AstNode,
    #         finally_body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize try statement node."""
    #         self.body = body
    #         self.excepts = excepts
    #         self.finally_body = finally_body
    #         super().__init__(*args, **kwargs)

    # class ExceptList(AstNode):
    #     """ExceptList node type for Jac Ast."""

    #     def __init__(
    #         self: "ExceptList",
    #         excepts: list,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize excepts node."""
    #         self.excepts = excepts
    #         super().__init__(*args, **kwargs)

    # class Except(AstNode):
    #     """Except node type for Jac Ast."""

    #     def __init__(
    #         self: "Except",
    #         typ: AstNode,
    #         name: AstNode,
    #         body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize except node."""
    #         self.typ = typ
    #         self.name = name
    #         self.body = body
    #         super().__init__(*args, **kwargs)

    # class FinallyStmt(AstNode):
    #     """FinallyStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "FinallyStmt",
    #         body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize finally statement node."""
    #         self.body = body
    #         super().__init__(*args, **kwargs)

    # class IterForStmt(AstNode):
    #     """IterFor node type for Jac Ast."""

    #     def __init__(
    #         self: "IterForStmt",
    #         iter: AstNode,
    #         condition: AstNode,
    #         count_by: AstNode,
    #         body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize iter for node."""
    #         self.iter = iter
    #         self.condition = condition
    #         self.count_by = count_by
    #         self.body = body
    #         super().__init__(*args, **kwargs)

    # class InForStmt(AstNode):
    #     """InFor node type for Jac Ast."""

    #     def __init__(
    #         self: "InForStmt",
    #         name: AstNode,
    #         collection: AstNode,
    #         body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize in for node."""
    #         self.name = name
    #         self.collection = collection
    #         self.body = body
    #         super().__init__(*args, **kwargs)

    # class DictForStmt(AstNode):
    #     """DictForStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "DictForStmt",
    #         k_name: AstNode,
    #         v_name: AstNode,
    #         collection: AstNode,
    #         body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize dict for node."""
    #         self.k_name = k_name
    #         self.v_name = v_name
    #         self.collection = collection
    #         self.body = body
    #         super().__init__(*args, **kwargs)

    # class WhileStmt(AstNode):
    #     """WhileStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "WhileStmt",
    #         condition: AstNode,
    #         body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize while statement node."""
    #         self.condition = condition
    #         self.body = body
    #         super().__init__(*args, **kwargs)

    # class RaiseStmt(AstNode):
    #     """RaiseStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "RaiseStmt",
    #         cause: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize raise statement node."""
    #         self.cause = cause
    #         super().__init__(*args, **kwargs)

    # class AssertStmt(AstNode):
    #     """AssertStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "AssertStmt",
    #         condition: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize assert statement node."""
    #         self.condition = condition
    #         super().__init__(*args, **kwargs)

    # class CtrlStmt(AstNode):
    #     """CtrlStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "CtrlStmt",
    #         stmt: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize control statement node."""
    #         self.stmt = stmt
    #         super().__init__(*args, **kwargs)

    # class DeleteStmt(AstNode):
    #     """DeleteStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "DeleteStmt",
    #         target: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize delete statement node."""
    #         self.target = target
    #         super().__init__(*args, **kwargs)

    # class ReportStmt(AstNode):
    #     """ReportStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "ReportStmt",
    #         expr: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize report statement node."""
    #         self.expr = expr
    #         super().__init__(*args, **kwargs)

    # class ReturnStmt(AstNode):
    #     """ReturnStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "ReturnStmt",
    #         expr: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize return statement node."""
    #         self.expr = expr
    #         super().__init__(*args, **kwargs)

    # class IgnoreStmt(AstNode):
    #     """IgnoreStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "IgnoreStmt",
    #         target: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize ignore statement node."""
    #         self.target = target
    #         super().__init__(*args, **kwargs)

    # class VisitStmt(AstNode):
    #     """VisitStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "VisitStmt",
    #         typ: AstNode,
    #         target: AstNode,
    #         else_body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize visit statement node."""
    #         self.typ = typ
    #         self.target = target
    #         self.else_body = else_body
    #         super().__init__(*args, **kwargs)

    # class RevisitStmt(AstNode):
    #     """ReVisitStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "RevisitStmt",
    #         target: AstNode,
    #         hops: AstNode,
    #         else_body: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize revisit statement node."""
    #         self.target = target
    #         self.hops = hops
    #         self.else_body = else_body
    #         super().__init__(*args, **kwargs)

    # class DisengageStmt(AstNode):
    #     """DisengageStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "DisengageStmt",
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize disengage statement node."""
    #         super().__init__(*args, **kwargs)

    # class YeildStmt(AstNode):
    #     """YeildStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "YeildStmt",
    #         expr: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize yeild statement node."""
    #         self.expr = expr
    #         super().__init__(*args, **kwargs)

    # class SyncStmt(AstNode):
    #     """SyncStmt node type for Jac Ast."""

    #     def __init__(
    #         self: "SyncStmt",
    #         *args: list,
    #         target: AstNode,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize sync statement node."""
    #         self.target = target
    #         super().__init__(*args, **kwargs)

    # class Assignment(AstNode):
    #     """Assignment node type for Jac Ast."""

    #     def __init__(
    #         self: "Assignment",
    #         is_static: bool,
    #         target: AstNode,
    #         value: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize assignment node."""
    #         self.is_static = is_static
    #         self.target = target
    #         self.value = value
    #         super().__init__(*args, **kwargs)

    # class IfElseExpr(AstNode):
    #     """ExprIfElse node type for Jac Ast."""

    #     def __init__(
    #         self: "IfElseExpr",
    #         condition: AstNode,
    #         value: AstNode,
    #         else_value: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize if else expression node."""
    #         self.condition = condition
    #         self.value = value
    #         self.else_value = else_value
    #         super().__init__(*args, **kwargs)

    # class BinaryExpr(AstNode):
    #     """ExprBinary node type for Jac Ast."""

    #     def __init__(
    #         self: "BinaryExpr",
    #         left: AstNode,
    #         right: AstNode,
    #         op: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize binary expression node."""
    #         self.left = left
    #         self.right = right
    #         self.op = op
    #         super().__init__(*args, **kwargs)

    # class UnaryExpr(AstNode):
    #     """ExprUnary node type for Jac Ast."""

    #     def __init__(
    #         self: "UnaryExpr",
    #         operand: AstNode,
    #         op: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize unary expression node."""
    #         self.operand = operand
    #         self.op = op
    #         super().__init__(*args, **kwargs)

    # class SpawnWalkerExpr(AstNode):
    #     """ExprSpawnWalker node type for Jac Ast."""

    #     def __init__(
    #         self: "SpawnWalkerExpr",
    #         target: AstNode,
    #         location: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize spawn walker expression node."""
    #         self.target = target
    #         self.location = location
    #         super().__init__(*args, **kwargs)

    # class SpawnObjectExpr(AstNode):
    #     """ExprSpawnObject node type for Jac Ast."""

    #     def __init__(
    #         self: "SpawnObjectExpr",
    #         target: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize spawn object expression node."""
    #         self.target = target
    #         super().__init__(*args, **kwargs)

    # class SpawnEdgeNodeExpr(AstNode):
    #     """ExprSpawnEdgeNode node type for Jac Ast."""

    #     def __init__(
    #         self: "SpawnEdgeNodeExpr",
    #         edge: AstNode,
    #         node: AstNode,
    #         location: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize spawn edge node expression node."""
    #         self.edge = edge
    #         self.node = node
    #         self.location = location
    #         super().__init__(*args, **kwargs)

    # class UnpackExpr(AstNode):
    #     """ExprUnpack node type for Jac Ast."""

    #     def __init__(
    #         self: "UnpackExpr",
    #         target: AstNode,
    #         is_dict: bool,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize unpack expression node."""
    #         self.target = target
    #         super().__init__(*args, **kwargs)

    # class RefExpr(AstNode):
    #     """ExprRef node type for Jac Ast."""

    #     def __init__(
    #         self: "RefExpr",
    #         target: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize ref expression node."""
    #         self.target = target
    #         super().__init__(*args, **kwargs)

    # class MultiString(AstNode):
    #     """ExprMultiString node type for Jac Ast."""

    #     def __init__(
    #         self: "MultiString",
    #         strings: list,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize multi string expression node."""
    #         self.strings = strings
    #         super().__init__(*args, **kwargs)

    # class ExprList(AstNode):
    #     """ExprList node type for Jac Ast."""

    #     def __init__(
    #         self: "ExprList",
    #         values: list,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize list expression node."""
    #         self.values = values
    #         super().__init__(*args, **kwargs)

    # class AssignmentList(ExprList):
    #     """AssignmentList node type for Jac Ast."""

    # class ListVal(ExprList):
    #     """ExprList node type for Jac Ast."""

    # class DictVal(AstNode):
    #     """ExprDict node type for Jac Ast."""

    #     def __init__(
    #         self: "DictVal",
    #         kv_pairs: list,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize dict expression node."""
    #         self.kv_pairs = kv_pairs
    #         super().__init__(*args, **kwargs)

    # class KVPair(AstNode):
    #     """ExprKVPair node type for Jac Ast."""

    #     def __init__(
    #         self: "KVPair",
    #         key: AstNode,
    #         value: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize key value pair expression node."""
    #         self.key = key
    #         self.value = value
    #         super().__init__(*args, **kwargs)

    # class AtomTrailer(AstNode):
    #     """AtomTrailer node type for Jac Ast."""

    #     def __init__(
    #         self: "AtomTrailer",
    #         target: AstNode,
    #         right: list,
    #         null_ok: bool = False,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize atom trailer expression node."""
    #         self.target = target
    #         self.right = right
    #         self.null_ok = null_ok
    #         super().__init__(*args, **kwargs)

    # class DSCall(AstNode):
    #     """DSCall node type for Jac Ast."""

    #     def __init__(
    #         self: "DSCall",
    #         target: AstNode,
    #         a_name: AstNode,
    #         is_async: bool,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize ds call expression node."""
    #         self.target = target
    #         self.a_name = a_name
    #         self.is_async = is_async
    #         super().__init__(*args, **kwargs)

    # class FuncCall(AstNode):
    #     """FuncCall node type for Jac Ast."""

    #     def __init__(
    #         self: "FuncCall",
    #         target: AstNode,
    #         params: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize function call expression node."""
    #         self.target = target
    #         self.params = params
    #         super().__init__(*args, **kwargs)

    # class ParamList(AstNode):
    #     """ParamList node type for Jac Ast."""

    #     def __init__(
    #         self: "ParamList",
    #         p_args: AstNode,
    #         p_kwargs: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize parameter list expression node."""
    #         self.p_args = p_args
    #         self.p_kwargs = p_kwargs
    #         super().__init__(*args, **kwargs)

    # class IndexSlice(AstNode):
    #     """IndexSlice node type for Jac Ast."""

    #     def __init__(
    #         self: "IndexSlice",
    #         start: AstNode,
    #         stop: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize index slice expression node."""
    #         self.start = start
    #         self.stop = stop
    #         super().__init__(*args, **kwargs)

    # class GlobalRef(AstNode):
    #     """GlobalRef node type for Jac Ast."""

    #     def __init__(
    #         self: "GlobalRef",
    #         name: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize global reference expression node."""
    #         self.name = name
    #         super().__init__(*args, **kwargs)

    # class NodeRef(GlobalRef):
    #     """NodeRef node type for Jac Ast."""

    # class EdgeRef(GlobalRef):
    #     """EdgeRef node type for Jac Ast."""

    # class WalkerRef(GlobalRef):
    #     """WalkerRef node type for Jac Ast."""

    # class FuncRef(GlobalRef):
    #     """FuncRef node type for Jac Ast."""

    # class ObjectRef(GlobalRef):
    #     """ObjectRef node type for Jac Ast."""

    # class AbilityRef(GlobalRef):
    #     """AbilityRef node type for Jac Ast."""

    # class EdgeOpRef(AstNode):
    #     """EdgeOpRef node type for Jac Ast."""

    #     def __init__(
    #         self: "EdgeOpRef",
    #         filter_cond: AstNode,
    #         edge_dir: EdgeDir,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize edge op reference expression node."""
    #         self.filter_cond = filter_cond
    #         self.edge_dir = edge_dir
    #         super().__init__(*args, **kwargs)

    # class ConnectOp(AstNode):
    #     """ConnectOpRef node type for Jac Ast."""

    #     def __init__(
    #         self: "ConnectOp",
    #         spawn: AstNode,
    #         edge_dir: EdgeDir,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize connect op reference expression node."""
    #         self.spawn = spawn
    #         self.edge_dir = edge_dir
    #         super().__init__(*args, **kwargs)

    # class DisconnectOp(EdgeOpRef):
    #     """DisconnectOpRef node type for Jac Ast."""

    #     def __init__(
    #         self: "DisconnectOp",
    #         edge_ref: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize disconnect op reference expression node."""
    #         self.edge_ref = edge_ref
    #         super().__init__(*args, **kwargs)

    # class FilterCtx(AstNode):
    #     """FilterCtx node type for Jac Ast."""

    #     def __init__(
    #         self: "FilterCtx",
    #         compares: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize filter_cond context expression node."""
    #         self.compares = compares
    #         super().__init__(*args, **kwargs)

    # class SpawnCtx(AstNode):
    #     """SpawnCtx node type for Jac Ast."""

    #     def __init__(
    #         self: "SpawnCtx",
    #         spawns: AstNode,
    #         *args: list,
    #         **kwargs: dict,
    #     ) -> None:
    #         """Initialize spawn context expression node."""
    #         self.spawns = spawns
    #         super().__init__(*args, **kwargs)`

    def enter_node(self: Pass, node: AstNode) -> None:
        """Enter node."""
        node.py_code = ""
        return super().enter_node(node)

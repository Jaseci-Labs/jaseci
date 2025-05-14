"""DocIrGenPass for Jaseci Ast.

This is a pass for generating DocIr for Jac code.
"""

import re
from typing import Optional, Union, List
import jaclang.compiler.unitree as uni
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes import UniPass
import jaclang.compiler.passes.tool.doc_ir as doc
from jaclang.compiler.unitree import UniNode
from jaclang.settings import settings


class DocIRGenPass(UniPass):
    """DocIrGenPass generate DocIr for Jac code."""

    def before_pass(self) -> None:
        """Initialize pass."""
        # Options for DocIr generation
        self.indent_size = 4
        self.MAX_LINE_LENGTH = settings.max_line_length
        self.comments: list[uni.CommentToken] = []

    def enter_node(self, node: uni.UniNode) -> None:
        """Enter node."""
        node.gen.doc_ir = []
        super().enter_node(node)

    def text(self, text: str) -> doc.Text:
        """Create a Text node."""
        return doc.Text(text)

    def line(self, hard: bool = False, literal: bool = False) -> doc.Line:
        """Create a Line node."""
        return doc.Line(hard, literal)

    def hard_line(self) -> doc.Line:
        """Create a hard line break."""
        return doc.Line(hard=True)

    def literal_line(self) -> doc.Line:
        """Create a literal line break."""
        return doc.Line(literal=True)

    def group(
        self,
        contents: Union[doc.DocType, List[doc.DocType]],
        break_contiguous: bool = False,
    ) -> doc.Group:
        """Create a Group node."""
        return doc.Group(contents, break_contiguous)

    def indent(self, contents: Union[doc.DocType, List[doc.DocType]]) -> doc.Indent:
        """Create an Indent node."""
        return doc.Indent(contents)

    def concat(self, parts: List[doc.DocType]) -> doc.Concat:
        """Create a Concat node."""
        return doc.Concat(parts)

    def if_break(
        self,
        break_contents: Union[doc.DocType, List[doc.DocType]],
        flat_contents: Union[doc.DocType, List[doc.DocType]],
    ) -> doc.IfBreak:
        """Create an IfBreak node."""
        return doc.IfBreak(break_contents, flat_contents)

    def align(
        self, contents: Union[doc.DocType, List[doc.DocType]], n: Optional[int] = None
    ) -> doc.Align:
        """Create an Align node."""
        return doc.Align(contents, n)

    def join(self, separator: doc.DocType, parts: List[doc.DocType]) -> doc.DocType:
        """Join parts with separator."""
        if not parts:
            return self.concat([])

        result = [parts[0]]
        for part in parts[1:]:
            result.append(separator)
            result.append(part)

        return self.concat(result)

    def token_before(self, node: uni.Token) -> Optional[uni.Token]:
        """Get token before the current token."""
        if self.ir_out.terminals.index(node) == 0:
            return None
        return self.ir_out.terminals[self.ir_out.terminals.index(node) - 1]

    def token_after(self, node: uni.Token) -> Optional[uni.Token]:
        """Get token after the current token."""
        if self.ir_out.terminals.index(node) == len(self.ir_out.terminals) - 1:
            return None
        return self.ir_out.terminals[self.ir_out.terminals.index(node) + 1]

    def enter_module(self, node: uni.Module) -> None:
        """Enter module."""
        self.comments = node.source.comments

    def exit_module(self, node: uni.Module) -> None:
        """Exit module."""
        parts: list[doc.DocType] = []

        # Process docstrings
        if node.kid and isinstance(node.kid[0], uni.String):
            parts.append(
                self.group(
                    [self.text(node.kid[0].value), self.hard_line(), self.hard_line()]
                )
            )

        # Process imports
        import_parts: list[doc.DocType] = []
        for item in node.body:
            if isinstance(item, uni.Import) and item.gen.doc_ir:
                import_parts.append(
                    item.gen.doc_ir[0] if item.gen.doc_ir else self.text("")
                )
                import_parts.append(self.hard_line())

        if import_parts:
            parts.append(self.group(import_parts))
            parts.append(self.hard_line())

        # Process other top-level elements
        other_parts: list[doc.DocType] = []
        for item in node.body:
            if not isinstance(item, uni.Import) and item.gen.doc_ir:
                other_parts.append(
                    item.gen.doc_ir[0]
                    if isinstance(item.gen.doc_ir, list)
                    else item.gen.doc_ir
                )
                other_parts.append(self.hard_line())
                other_parts.append(self.hard_line())

        if other_parts and isinstance(other_parts[-1], doc.Line):
            other_parts.pop()  # Remove trailing line

        parts.append(self.group(other_parts))

        node.gen.doc_ir = [self.group(parts)]

    def exit_import(self, node: uni.Import) -> None:
        """Generate DocIR for import statements."""
        parts: list[doc.DocType] = [self.text("import ")]

        if node.items:
            item_parts: list[doc.DocType] = []
            for item in node.items.items:
                if item.gen.doc_ir and item.gen.doc_ir:
                    item_parts.append(item.gen.doc_ir[0])

            if item_parts:
                parts.append(self.join(self.text(", "), item_parts))

        parts.append(self.text(";"))
        node.gen.doc_ir = [self.group(parts)]

    def exit_module_item(self, node: uni.ModuleItem) -> None:
        """Generate DocIR for module items."""
        if node.alias:
            doc_ir: doc.DocType = self.concat(
                [
                    self.text(node.name.value),
                    self.text(" as "),
                    self.text(node.alias.value),
                ]
            )
        else:
            doc_ir = self.text(node.name.value)

        node.gen.doc_ir = [doc_ir]

    def exit_module_path(self, node: uni.ModulePath) -> None:
        """Generate DocIR for module paths."""
        parts: list[doc.DocType] = []

        if (
            node.path and node.path.items
        ):  # Check if node.path and node.path.items are not None
            for i, path_item in enumerate(node.path.items):
                if path_item.gen.doc_ir:
                    parts.append(
                        path_item.gen.doc_ir[0]
                        if isinstance(path_item.gen.doc_ir, list)
                        else path_item.gen.doc_ir
                    )
                    if i < len(node.path.items) - 1:
                        parts.append(self.text("."))

        node.gen.doc_ir = [self.group(parts)]

    def exit_architype(self, node: uni.Architype) -> None:
        """Generate DocIR for architypes."""
        parts: list[doc.DocType] = []

        # Handle decorators
        if node.decorators:
            for decorator in node.decorators.items:
                if decorator.gen.doc_ir:
                    parts.append(decorator.gen.doc_ir[0])
                    parts.append(self.hard_line())

        # Type declaration
        header_parts: list[doc.DocType] = [self.text(node.arch_type.value)]
        if node.name:
            header_parts.append(self.text(" "))
            header_parts.append(self.text(node.name.value))

        # Inheritance
        if node.base_classes and node.base_classes.gen.doc_ir:
            header_parts.append(self.text(": "))
            header_parts.append(node.base_classes.gen.doc_ir[0])

        parts.append(self.group(header_parts))

        # Handle body
        if node.body:
            body_parts: list[doc.DocType] = []
            for item in node.body.items:
                if item.gen.doc_ir:
                    body_parts.append(item.gen.doc_ir[0])
                    body_parts.append(self.hard_line())

            parts.append(self.text(" {"))
            parts.append(
                self.indent(self.concat([self.hard_line(), self.group(body_parts)]))
            )
            parts.append(self.hard_line())
            parts.append(self.text("}"))
        else:
            parts.append(self.text(" {}"))

        parts.append(self.text(";"))
        node.gen.doc_ir = [self.group(parts)]

    def exit_ability(self, node: uni.Ability) -> None:
        """Generate DocIR for abilities."""
        parts: list[doc.DocType] = []

        # Handle decorators
        if node.decorators:
            for decorator in node.decorators.items:
                if decorator.gen.doc_ir:
                    parts.append(decorator.gen.doc_ir[0])
                    parts.append(self.hard_line())

        # Static keyword
        if node.is_static:
            parts.append(self.text("static "))

        # Type (can/def)
        if node.is_def:
            parts.append(self.text("def"))
        else:
            parts.append(self.text("can"))
        parts.append(self.text(" "))

        # Name and signature
        if node.name_ref:
            parts.append(self.text(node.name_ref.unparse()))

        if node.signature and node.signature.gen.doc_ir:
            parts.append(node.signature.gen.doc_ir[0])

        # Handle body
        if node.body and node.body.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(self.text("{"))
            parts.append(
                self.indent(self.concat([self.hard_line(), node.body.gen.doc_ir[0]]))
            )
            parts.append(self.hard_line())
            parts.append(self.text("}"))
        else:
            parts.append(self.text(" {}"))

        parts.append(self.text(";"))
        node.gen.doc_ir = [self.group(parts)]

    def exit_func_signature(self, node: uni.FuncSignature) -> None:
        """Generate DocIR for function signatures."""
        parts: list[doc.DocType] = [self.text("(")]

        # Parameters
        if node.params:
            param_parts: list[doc.DocType] = []
            for param in node.params.items:
                if param.gen.doc_ir:
                    param_parts.append(param.gen.doc_ir[0])

            param_group = self.group(self.join(self.text(", "), param_parts))

            # Check if parameters should be broken into multiple lines
            parts.append(
                self.if_break(
                    self.concat(
                        [
                            self.indent(
                                self.concat(
                                    [
                                        self.hard_line(),
                                        self.join(
                                            self.concat([self.text(","), self.line()]),
                                            param_parts,
                                        ),
                                    ]
                                )
                            ),
                            self.hard_line(),
                        ]
                    ),
                    param_group,
                )
            )

        parts.append(self.text(")"))

        # Return type
        if node.return_type and node.return_type.gen.doc_ir:
            parts.append(self.text(" -> "))
            parts.append(node.return_type.gen.doc_ir[0])

        node.gen.doc_ir = [self.group(parts)]

    def exit_param_var(self, node: uni.ParamVar) -> None:
        """Generate DocIR for parameter variables."""
        parts: list[doc.DocType] = []

        if node.name:
            parts.append(self.text(node.name.value))

        if node.type_tag and node.type_tag.gen.doc_ir:
            parts.append(self.text(": "))
            parts.append(
                node.type_tag.tag.gen.doc_ir[0]
                if isinstance(node.type_tag.tag.gen.doc_ir, list)
                else node.type_tag.tag.gen.doc_ir
            )

        if node.value and node.value.gen.doc_ir:
            parts.append(self.text(" = "))
            parts.append(
                node.value.gen.doc_ir[0]
                if isinstance(node.value.gen.doc_ir, list)
                else node.value.gen.doc_ir
            )

        node.gen.doc_ir = [self.group(parts)]

    def exit_type_ref(self, node: uni.TypeRef) -> None:
        """Generate DocIR for type references."""
        parts: list[doc.DocType] = []

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir[0])

        node.gen.doc_ir = [self.group(parts)]

    def exit_assignment(self, node: uni.Assignment) -> None:
        """Generate DocIR for assignments."""
        parts: list[doc.DocType] = []

        # Left side
        if node.target and node.target.gen.doc_ir:
            target_doc = node.target.gen.doc_ir[0]
            if target_doc:
                parts.append(target_doc)

        # Type annotation
        if node.type_tag and node.type_tag.gen.doc_ir:
            parts.append(self.text(": "))
            parts.append(node.type_tag.gen.doc_ir[0])

        # Assignment operator
        parts.append(self.text(" = "))

        # Right side
        if node.value and node.value.gen.doc_ir:
            parts.append(node.value.gen.doc_ir[0])

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_if_stmt(self, node: uni.IfStmt) -> None:
        """Generate DocIR for if statements."""
        parts: list[doc.DocType] = [self.text("if ")]

        # Condition
        if node.condition and node.condition.gen.doc_ir:
            parts.append(node.condition.gen.doc_ir[0])

        # Body
        parts.append(self.text(" "))
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        # Else or ElseIf
        if node.else_body and node.else_body.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(
                node.else_body.gen.doc_ir[0]
                if isinstance(node.else_body.gen.doc_ir, list)
                else node.else_body.gen.doc_ir
            )

        node.gen.doc_ir = [self.group(parts)]

    def exit_else_if(self, node: uni.ElseIf) -> None:
        """Generate DocIR for else if statements."""
        parts: list[doc.DocType] = [self.text("elif ")]

        # Condition
        if node.condition and node.condition.gen.doc_ir:
            parts.append(node.condition.gen.doc_ir[0])

        # Body
        parts.append(self.text(" "))
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        # Else or ElseIf
        if node.else_body and node.else_body.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(
                node.else_body.gen.doc_ir[0]
                if isinstance(node.else_body.gen.doc_ir, list)
                else node.else_body.gen.doc_ir
            )

        node.gen.doc_ir = [self.group(parts)]

    def exit_else_stmt(self, node: uni.ElseStmt) -> None:
        """Generate DocIR for else statements."""
        parts: list[doc.DocType] = [self.text("else ")]

        # Body
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_binary_expr(self, node: uni.BinaryExpr) -> None:
        """Generate DocIR for binary expressions."""
        parts: list[doc.DocType] = []

        # Left operand
        if node.left and node.left.gen.doc_ir:
            parts.append(node.left.gen.doc_ir[0])

        # Operator
        parts.append(self.text(" "))
        if isinstance(node.op, uni.Token):
            parts.append(self.text(node.op.value))
        elif node.op.gen.doc_ir:
            parts.append(node.op.gen.doc_ir[0])
        parts.append(self.text(" "))

        # Right operand
        if node.right and node.right.gen.doc_ir:
            parts.append(node.right.gen.doc_ir[0])

        node.gen.doc_ir = [self.group(parts)]

    def exit_expr_stmt(self, node: uni.ExprStmt) -> None:
        """Generate DocIR for expression statements."""
        parts: list[doc.DocType] = []

        if node.expr and node.expr.gen.doc_ir:
            parts.append(node.expr.gen.doc_ir[0])

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_return_stmt(self, node: uni.ReturnStmt) -> None:
        """Generate DocIR for return statements."""
        parts: list[doc.DocType] = [self.text("return")]

        if node.expr and node.expr.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(node.expr.gen.doc_ir[0])

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_func_call(self, node: uni.FuncCall) -> None:
        """Generate DocIR for function calls."""
        parts: list[doc.DocType] = []

        # Name or callable expression (target in FuncCall)
        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir[0])

        # Parameters
        parts.append(self.text("("))

        if node.params and node.params.items:
            param_parts: list[doc.DocType] = []
            for param in node.params.items:
                if param.gen.doc_ir:
                    param_parts.append(
                        param.gen.doc_ir[0]
                        if isinstance(param.gen.doc_ir, list)
                        else param.gen.doc_ir
                    )

            # Check if parameters should be broken into multiple lines
            if param_parts:
                param_group = self.group(self.join(self.text(", "), param_parts))

                # Advanced layout with conditional line breaks
                parts.append(
                    self.if_break(
                        self.concat(
                            [
                                self.indent(
                                    self.concat(
                                        [
                                            self.hard_line(),
                                            self.join(
                                                self.concat(
                                                    [self.text(","), self.line()]
                                                ),
                                                param_parts,
                                            ),
                                        ]
                                    )
                                ),
                                self.hard_line(),
                            ]
                        ),
                        param_group,
                    )
                )

        parts.append(self.text(")"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_atom_trailer(self, node: uni.AtomTrailer) -> None:
        """Generate DocIR for atom trailers."""
        parts: list[doc.DocType] = []

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir[0])

        # Null-safe operator
        if node.is_null_ok:
            parts.append(self.text("?."))
        # Dot operator for attribute access
        elif node.is_attr:
            parts.append(self.text("."))

        if node.right and node.right.gen.doc_ir:
            parts.append(node.right.gen.doc_ir[0])

        node.gen.doc_ir = [self.group(parts)]

    def exit_name(self, node: uni.Name) -> None:
        """Generate DocIR for names."""
        if node.is_kwesc:
            node.gen.doc_ir = [self.text(f"<>{node.value}")]
        else:
            node.gen.doc_ir = [self.text(node.value)]

    def exit_int(self, node: uni.Int) -> None:
        """Generate DocIR for integers."""
        node.gen.doc_ir = [self.text(node.value)]

    def exit_float(self, node: uni.Float) -> None:
        """Generate DocIR for floats."""
        node.gen.doc_ir = [self.text(node.value)]

    def exit_string(self, node: uni.String) -> None:
        """Generate DocIR for strings."""
        # Handle multiline strings
        if "\n" in node.value:
            lines = node.value.split("\n")
            parts: list[doc.DocType] = [self.text(lines[0])]

            for line in lines[1:]:
                parts.append(self.hard_line())
                parts.append(self.text(line))

            node.gen.doc_ir = [self.group(parts)]
        else:
            node.gen.doc_ir = [self.text(node.value)]

    def exit_list_val(self, node: uni.ListVal) -> None:
        """Generate DocIR for list values."""
        parts: list[doc.DocType] = [self.text("[")]

        if node.values:
            value_parts: list[doc.DocType] = []
            for value in node.values.items:
                if value.gen.doc_ir:
                    value_parts.append(
                        value.gen.doc_ir[0]
                        if isinstance(value.gen.doc_ir, list)
                        else value.gen.doc_ir
                    )

            if value_parts:
                # Check if list should be broken into multiple lines
                parts.append(
                    self.if_break(
                        self.concat(
                            [
                                self.indent(
                                    self.concat(
                                        [
                                            self.hard_line(),
                                            self.join(
                                                self.concat(
                                                    [self.text(","), self.line()]
                                                ),
                                                value_parts,
                                            ),
                                        ]
                                    )
                                ),
                                self.hard_line(),
                            ]
                        ),
                        self.join(self.text(", "), value_parts),
                    )
                )

        parts.append(self.text("]"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_dict_val(self, node: uni.DictVal) -> None:
        """Generate DocIR for dictionary values."""
        parts: list[doc.DocType] = [self.text("{")]

        if node.kv_pairs:
            pair_parts: list[doc.DocType] = []
            for pair in node.kv_pairs:
                if pair.gen.doc_ir:
                    pair_parts.append(
                        pair.gen.doc_ir[0]
                        if isinstance(pair.gen.doc_ir, list)
                        else pair.gen.doc_ir
                    )

            if pair_parts:
                # Check if dict should be broken into multiple lines
                parts.append(
                    self.if_break(
                        self.concat(
                            [
                                self.indent(
                                    self.concat(
                                        [
                                            self.hard_line(),
                                            self.join(
                                                self.concat(
                                                    [self.text(","), self.line()]
                                                ),
                                                pair_parts,
                                            ),
                                        ]
                                    )
                                ),
                                self.hard_line(),
                            ]
                        ),
                        self.join(self.text(", "), pair_parts),
                    )
                )

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_k_v_pair(self, node: uni.KVPair) -> None:
        """Generate DocIR for key-value pairs."""
        parts: list[doc.DocType] = []

        if node.key and node.key.gen.doc_ir:
            parts.append(node.key.gen.doc_ir[0])
            parts.append(self.text(": "))

        if node.value and node.value.gen.doc_ir:
            parts.append(node.value.gen.doc_ir[0])

        node.gen.doc_ir = [self.group(parts)]

    def exit_has_var(self, node: uni.HasVar) -> None:
        """Generate DocIR for has variable declarations."""
        parts: list[doc.DocType] = [self.text("has ")]

        if node.name:
            parts.append(self.text(node.name.value))

        if node.type_tag and node.type_tag.gen.doc_ir:
            parts.append(self.text(": "))
            parts.append(node.type_tag.gen.doc_ir[0])

        if node.value and node.value.gen.doc_ir:
            parts.append(self.text(" = "))
            parts.append(node.value.gen.doc_ir[0])

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_arch_has(self, node: uni.ArchHas) -> None:
        """Generate DocIR for architecture has declarations."""
        parts: list[doc.DocType] = [self.text("has ")]

        if node.is_static:
            parts.append(self.text("static "))

        if node.vars:
            var_parts: list[doc.DocType] = []
            for var in node.vars.items:
                if var.gen.doc_ir:
                    var_parts.append(var.gen.doc_ir[0])

            parts.append(self.join(self.text(", "), var_parts))

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_while_stmt(self, node: uni.WhileStmt) -> None:
        """Generate DocIR for while statements."""
        parts: list[doc.DocType] = [self.text("while ")]

        if node.condition and node.condition.gen.doc_ir:
            parts.append(node.condition.gen.doc_ir[0])

        parts.append(self.text(" "))
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_in_for_stmt(self, node: uni.InForStmt) -> None:
        """Generate DocIR for for-in statements."""
        parts: list[doc.DocType] = [self.text("for ")]

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir[0])

        parts.append(self.text(" in "))

        if node.collection and node.collection.gen.doc_ir:
            parts.append(node.collection.gen.doc_ir[0])

        parts.append(self.text(" "))
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_iter_for_stmt(self, node: uni.IterForStmt) -> None:
        """Generate DocIR for iterative for statements."""
        parts: list[doc.DocType] = [self.text("for ")]

        if node.iter and node.iter.gen.doc_ir:
            parts.append(node.iter.gen.doc_ir[0])
            parts.append(self.text("; "))
        else:
            parts.append(self.text("; "))

        if node.condition and node.condition.gen.doc_ir:
            parts.append(node.condition.gen.doc_ir[0])
            parts.append(self.text("; "))
        else:
            parts.append(self.text("; "))

        if node.count_by and node.count_by.gen.doc_ir:
            parts.append(node.count_by.gen.doc_ir[0])

        parts.append(self.text(" "))
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_try_stmt(self, node: uni.TryStmt) -> None:
        """Generate DocIR for try statements."""
        parts: list[doc.DocType] = [self.text("try ")]
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        # Handle except clauses
        if node.excepts and node.excepts.items:  # Added .items
            for except_clause in node.excepts.items:
                if except_clause.gen.doc_ir:
                    parts.append(self.text(" "))
                    parts.append(
                        except_clause.gen.doc_ir[0]
                        if isinstance(except_clause.gen.doc_ir, list)
                        else except_clause.gen.doc_ir
                    )

        # Handle finally clause
        if node.finally_body and node.finally_body.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(
                node.finally_body.gen.doc_ir[0]
                if isinstance(node.finally_body.gen.doc_ir, list)
                else node.finally_body.gen.doc_ir
            )

        node.gen.doc_ir = [self.group(parts)]

    def exit_except(self, node: uni.Except) -> None:
        """Generate DocIR for except clauses."""
        parts: list[doc.DocType] = [self.text("except")]

        if node.ex_type and node.ex_type.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(node.ex_type.gen.doc_ir[0])

        if node.name and node.name.gen.doc_ir:
            parts.append(self.text(" as "))
            parts.append(node.name.gen.doc_ir[0])

        parts.append(self.text(" "))
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_finally_stmt(self, node: uni.FinallyStmt) -> None:
        """Generate DocIR for finally statements."""
        parts: list[doc.DocType] = [self.text("finally ")]
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_tuple_val(self, node: uni.TupleVal) -> None:
        """Generate DocIR for tuple values."""
        parts: list[doc.DocType] = [self.text("(")]

        if node.values:
            value_parts: list[doc.DocType] = []
            for value in node.values.items:
                if value.gen.doc_ir:
                    value_parts.append(
                        value.gen.doc_ir[0]
                        if isinstance(value.gen.doc_ir, list)
                        else value.gen.doc_ir
                    )

            # Check if tuple should be broken into multiple lines
            if value_parts:
                parts.append(
                    self.if_break(
                        self.concat(
                            [
                                self.indent(
                                    self.concat(
                                        [
                                            self.hard_line(),
                                            self.join(
                                                self.concat(
                                                    [self.text(","), self.line()]
                                                ),
                                                value_parts,
                                            ),
                                        ]
                                    )
                                ),
                                self.hard_line(),
                            ]
                        ),
                        self.join(self.text(", "), value_parts),
                    )
                )

        parts.append(self.text(")"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_multi_string(self, node: uni.MultiString) -> None:
        """Generate DocIR for multiline strings."""
        parts: list[doc.DocType] = []

        for string in node.strings:
            if string.gen.doc_ir:
                parts.append(string.gen.doc_ir[0])
                parts.append(self.hard_line())

        if parts and isinstance(parts[-1], doc.Line):
            parts.pop()  # Remove trailing line

        node.gen.doc_ir = [self.group(parts)]

    def exit_set_val(self, node: uni.SetVal) -> None:
        """Generate DocIR for set values."""
        parts: list[doc.DocType] = [self.text("{")]

        if node.values:
            value_parts: list[doc.DocType] = []
            for value in node.values.items:
                if value.gen.doc_ir:
                    value_parts.append(value.gen.doc_ir[0])

            # Check if set should be broken into multiple lines
            parts.append(
                self.if_break(
                    self.concat(
                        [
                            self.indent(
                                self.concat(
                                    [
                                        self.hard_line(),
                                        self.join(
                                            self.concat([self.text(","), self.line()]),
                                            value_parts,
                                        ),
                                    ]
                                )
                            ),
                            self.hard_line(),
                        ]
                    ),
                    self.join(self.text(", "), value_parts),
                )
            )

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_special_var_ref(self, node: uni.SpecialVarRef) -> None:
        """Generate DocIR for special variable references."""
        parts: list[doc.DocType] = []

        if node.orig and node.orig.gen.doc_ir:
            parts.append(node.orig.gen.doc_ir[0])

        node.gen.doc_ir = [self.group(parts)]

    def exit_bool(self, node: uni.Bool) -> None:
        """Generate DocIR for boolean values."""
        node.gen.doc_ir = [self.text(node.value)]

    def exit_null(self, node: uni.Null) -> None:
        """Generate DocIR for null values."""
        node.gen.doc_ir = [self.text(node.value)]

    def exit_ellipsis(self, node: uni.Ellipsis) -> None:
        """Generate DocIR for ellipsis."""
        node.gen.doc_ir = [self.text(node.value)]

    def exit_with_stmt(self, node: uni.WithStmt) -> None:
        """Generate DocIR for with statements."""
        parts: list[doc.DocType] = [self.text("with ")]

        # Handle expressions
        if node.exprs:
            expr_parts: list[doc.DocType] = []
            for expr in node.exprs.items:
                if expr.gen.doc_ir:
                    expr_parts.append(
                        expr.gen.doc_ir[0]
                        if isinstance(expr.gen.doc_ir, list)
                        else expr.gen.doc_ir
                    )
            parts.append(self.join(self.text(", "), expr_parts))

        # Body
        parts.append(self.text(" "))
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_list_compr(self, node: uni.ListCompr) -> None:
        """Generate DocIR for list comprehensions."""
        parts: list[doc.DocType] = [self.text("[")]

        # Output expression
        if node.out_expr and node.out_expr.gen.doc_ir:
            parts.append(node.out_expr.gen.doc_ir[0])
            parts.append(self.text(" "))

        # Comprehension clauses
        for compr in node.compr:
            if compr.gen.doc_ir:
                parts.append(compr.gen.doc_ir[0])
                parts.append(self.text(" "))

        if parts and isinstance(parts[-1], doc.Text) and parts[-1].text == " ":
            parts.pop()  # Remove trailing space

        parts.append(self.text("]"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_inner_compr(self, node: uni.InnerCompr) -> None:
        """Generate DocIR for inner comprehension clauses."""
        parts: list[doc.DocType] = []

        if node.is_async:
            parts.append(self.text("async "))

        parts.append(self.text("for "))

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir[0])

        parts.append(self.text(" in "))

        if node.collection and node.collection.gen.doc_ir:
            parts.append(node.collection.gen.doc_ir[0])

        # Conditionals
        if node.conditional:
            for cond in node.conditional:
                if cond.gen.doc_ir:
                    parts.append(self.text(" if "))
                    parts.append(cond.gen.doc_ir[0])

        node.gen.doc_ir = [self.concat(parts)]

    def exit_f_string(self, node: uni.FString) -> None:
        """Generate DocIR for formatted strings."""
        parts: list[doc.DocType] = [self.text('f"')]

        if node.parts:
            for part in node.parts.items:
                if isinstance(part, uni.String):
                    parts.append(self.text(part.value))
                else:  # part is ExprStmt
                    parts.append(self.text("{"))
                    if part.gen.doc_ir:
                        parts.append(part.gen.doc_ir[0])
                    parts.append(self.text("}"))

        parts.append(self.text('"'))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_if_else_expr(self, node: uni.IfElseExpr) -> None:
        """Generate DocIR for conditional expressions."""
        parts: list[doc.DocType] = []

        if node.value and node.value.gen.doc_ir:
            parts.append(node.value.gen.doc_ir[0])

        parts.append(self.text(" if "))

        if node.condition and node.condition.gen.doc_ir:
            parts.append(node.condition.gen.doc_ir[0])

        parts.append(self.text(" else "))

        if node.else_value and node.else_value.gen.doc_ir:
            parts.append(node.else_value.gen.doc_ir[0])

        node.gen.doc_ir = [self.group(parts)]

    def exit_bool_expr(self, node: uni.BoolExpr) -> None:
        """Generate DocIR for boolean expressions (and/or)."""
        parts: list[doc.DocType] = []

        for i, value in enumerate(node.values):
            if value.gen.doc_ir:
                parts.append(value.gen.doc_ir[0])

                # Add operator between items, but not after the last one
                if i < len(node.values) - 1 and node.op:
                    parts.append(self.text(f" {node.op.value} "))

        node.gen.doc_ir = [self.group(parts)]

    def exit_unary_expr(self, node: uni.UnaryExpr) -> None:
        """Generate DocIR for unary expressions."""
        parts: list[doc.DocType] = []

        if node.op.value in ["-", "~", "+"]:
            # No space for these operators
            parts.append(self.text(node.op.value))
            if node.operand and node.operand.gen.doc_ir:
                parts.append(node.operand.gen.doc_ir[0])
        elif node.op.value == "not":
            # Space after 'not'
            parts.append(self.text("not "))
            if node.operand and node.operand.gen.doc_ir:
                parts.append(node.operand.gen.doc_ir[0])
        else:
            # Default case
            parts.append(self.text(node.op.value))
            if node.operand and node.operand.gen.doc_ir:
                parts.append(self.text(" "))
                parts.append(node.operand.gen.doc_ir[0])

        node.gen.doc_ir = [self.group(parts)]

    def exit_lambda_expr(self, node: uni.LambdaExpr) -> None:
        """Generate DocIR for lambda expressions."""
        parts: list[doc.DocType] = [self.text("lambda ")]

        # Parameters
        if node.signature and node.signature.params:
            param_parts: list[doc.DocType] = []
            for param in node.signature.params.items:
                if param.gen.doc_ir:
                    param_parts.append(param.gen.doc_ir[0])

            param_group = self.group(self.join(self.text(", "), param_parts))

            # Check if parameters should be broken into multiple lines
            parts.append(
                self.if_break(
                    self.concat(
                        [
                            self.indent(
                                self.concat(
                                    [
                                        self.hard_line(),
                                        self.join(
                                            self.concat([self.text(","), self.line()]),
                                            param_parts,
                                        ),
                                    ]
                                )
                            ),
                            self.hard_line(),
                        ]
                    ),
                    param_group,
                )
            )

        parts.append(self.text(")"))

        # Return type
        if (
            node.signature
            and node.signature.return_type
            and node.signature.return_type.gen.doc_ir
        ):
            parts.append(self.text(" -> "))
            if node.signature.return_type.gen.doc_ir:
                parts.append(node.signature.return_type.gen.doc_ir[0])

        # Body
        parts.append(self.text(" : "))
        if node.body and node.body.gen.doc_ir:
            if node.body.gen.doc_ir:
                parts.append(node.body.gen.doc_ir[0])

        node.gen.doc_ir = [self.group(parts)]

    def exit_edge_ref_trailer(self, node: uni.EdgeRefTrailer) -> None:
        """Generate DocIR for edge reference trailers."""
        parts: list[doc.DocType] = []

        for kid in node.kid:
            if kid.gen.doc_ir and kid.gen.doc_ir:  # check kid.gen.doc_ir is not empty
                parts.append(kid.gen.doc_ir[0])

        node.gen.doc_ir = [self.concat(parts)]

    def exit_edge_op_ref(self, node: uni.EdgeOpRef) -> None:
        """Generate DocIR for edge operation references."""
        parts: list[doc.DocType] = []

        for kid in node.kid:
            if kid.gen.doc_ir and kid.gen.doc_ir:  # check kid.gen.doc_ir is not empty
                parts.append(kid.gen.doc_ir[0])

        node.gen.doc_ir = [self.concat(parts)]

    def exit_index_slice(self, node: uni.IndexSlice) -> None:
        """Generate DocIR for index slices."""
        parts: list[doc.DocType] = [self.text("[")]

        if node.slices and len(node.slices) > 0:
            slice_parts: list[doc.DocType] = []

            for slice_item in node.slices:
                item_parts: list[doc.DocType] = []

                # Start
                if slice_item.start and slice_item.start.gen.doc_ir:
                    item_parts.append(
                        slice_item.start.gen.doc_ir[0]
                        if isinstance(slice_item.start.gen.doc_ir, list)
                        else slice_item.start.gen.doc_ir
                    )

                # Only add colon for range slices
                if node.is_range:
                    item_parts.append(self.text(":"))

                    # Stop
                    if slice_item.stop and slice_item.stop.gen.doc_ir:
                        item_parts.append(
                            slice_item.stop.gen.doc_ir[0]
                            if isinstance(slice_item.stop.gen.doc_ir, list)
                            else slice_item.stop.gen.doc_ir
                        )

                    # Step
                    if slice_item.step:
                        item_parts.append(self.text(":"))
                        if slice_item.step.gen.doc_ir:
                            item_parts.append(
                                slice_item.step.gen.doc_ir[0]
                                if isinstance(slice_item.step.gen.doc_ir, list)
                                else slice_item.step.gen.doc_ir
                            )

                slice_parts.append(self.concat(item_parts))

            # Join multiple slices with commas
            if len(slice_parts) > 1:
                parts.append(self.join(self.text(", "), slice_parts))
            else:
                parts.append(slice_parts[0])

        parts.append(self.text("]"))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_gen_compr(self, node: uni.GenCompr) -> None:
        """Generate DocIR for generator comprehensions."""
        parts: list[doc.DocType] = [self.text("(")]

        # Output expression
        if node.out_expr and node.out_expr.gen.doc_ir:
            parts.append(node.out_expr.gen.doc_ir[0])
            parts.append(self.text(" "))

        # Comprehension clauses
        for compr in node.compr:
            if compr.gen.doc_ir:
                parts.append(compr.gen.doc_ir[0])
                parts.append(self.text(" "))

        if parts and isinstance(parts[-1], doc.Text) and parts[-1].text == " ":
            parts.pop()  # Remove trailing space

        parts.append(self.text(")"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_set_compr(self, node: uni.SetCompr) -> None:
        """Generate DocIR for set comprehensions."""
        parts: list[doc.DocType] = [self.text("{")]

        # Output expression
        if node.out_expr and node.out_expr.gen.doc_ir:
            parts.append(node.out_expr.gen.doc_ir[0])
            parts.append(self.text(" "))

        # Comprehension clauses
        for compr in node.compr:
            if compr.gen.doc_ir:
                parts.append(compr.gen.doc_ir[0])
                parts.append(self.text(" "))

        if parts and isinstance(parts[-1], doc.Text) and parts[-1].text == " ":
            parts.pop()  # Remove trailing space

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_dict_compr(self, node: uni.DictCompr) -> None:
        """Generate DocIR for dictionary comprehensions."""
        parts: list[doc.DocType] = [self.text("{")]

        # Key-value pair
        if node.kv_pair and node.kv_pair.gen.doc_ir:
            parts.append(node.kv_pair.gen.doc_ir[0])
            parts.append(self.text(" "))

        # Comprehension clauses
        for compr in node.compr:
            if compr.gen.doc_ir:
                parts.append(compr.gen.doc_ir[0])
                parts.append(self.text(" "))

        if parts and isinstance(parts[-1], doc.Text) and parts[-1].text == " ":
            parts.pop()  # Remove trailing space

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_k_w_pair(self, node: uni.KWPair) -> None:
        """Generate DocIR for keyword arguments."""
        parts: list[doc.DocType] = []

        if node.key:
            parts.append(self.text(node.key.unparse()))
            parts.append(self.text("="))
            if node.value and node.value.gen.doc_ir:
                parts.append(node.value.gen.doc_ir[0])
        else:
            parts.append(self.text("**"))
            if node.value and node.value.gen.doc_ir:
                parts.append(node.value.gen.doc_ir[0])

        node.gen.doc_ir = [self.concat(parts)]

    def exit_await_expr(self, node: uni.AwaitExpr) -> None:
        """Generate DocIR for await expressions."""
        parts: list[doc.DocType] = [self.text("await ")]

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir[0])

        node.gen.doc_ir = [self.concat(parts)]

    def exit_yield_expr(self, node: uni.YieldExpr) -> None:
        """Generate DocIR for yield expressions."""
        parts: list[doc.DocType] = [self.text("yield")]

        if node.with_from:
            parts.append(self.text(" from"))

        if node.expr and node.expr.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(node.expr.gen.doc_ir[0])

        node.gen.doc_ir = [self.concat(parts)]

    def exit_ctrl_stmt(self, node: uni.CtrlStmt) -> None:
        """Generate DocIR for control statements (break, continue)."""
        # CtrlStmt does not have an expr attribute as per unitree.py
        node.gen.doc_ir = [self.text(f"{node.ctrl.value};")]

    def exit_delete_stmt(self, node: uni.DeleteStmt) -> None:
        """Generate DocIR for delete statements."""
        parts: list[doc.DocType] = [self.text("delete ")]

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir[0])

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_disengage_stmt(self, node: uni.DisengageStmt) -> None:
        """Generate DocIR for disengage statements."""
        node.gen.doc_ir = [self.text("disengage;")]

    def exit_report_stmt(self, node: uni.ReportStmt) -> None:
        """Generate DocIR for report statements."""
        parts: list[doc.DocType] = [self.text("report ")]

        if node.expr and node.expr.gen.doc_ir:
            parts.append(node.expr.gen.doc_ir[0])

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_assert_stmt(self, node: uni.AssertStmt) -> None:
        """Generate DocIR for assert statements."""
        parts: list[doc.DocType] = [self.text("assert ")]

        if node.condition and node.condition.gen.doc_ir:
            parts.append(node.condition.gen.doc_ir[0])

        # Optional error message
        if node.error_msg and node.error_msg.gen.doc_ir:
            parts.append(self.text(", "))
            parts.append(node.error_msg.gen.doc_ir[0])

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_raise_stmt(self, node: uni.RaiseStmt) -> None:
        """Generate DocIR for raise statements."""
        parts: list[doc.DocType] = [self.text("raise")]

        if node.cause and node.cause.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(node.cause.gen.doc_ir[0])

        # Optional from expression
        if node.from_target and node.from_target.gen.doc_ir:
            parts.append(self.text(" from "))
            parts.append(node.from_target.gen.doc_ir[0])

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_global_vars(self, node: uni.GlobalVars) -> None:
        """Generate DocIR for global variables."""
        parts: list[doc.DocType] = []

        # Keyword (let or global)
        if node.is_frozen:
            parts.append(self.text("let "))
        else:
            parts.append(self.text("global "))

        # Access specification
        if node.access and node.access.gen.doc_ir:
            parts.append(
                node.access.gen.doc_ir[0]
                if isinstance(node.access.gen.doc_ir, list)
                else node.access.gen.doc_ir
            )
            parts.append(self.text(" "))

        # Assignments
        if node.assignments and node.assignments.gen.doc_ir:
            parts.append(
                node.assignments.gen.doc_ir[0]
                if isinstance(node.assignments.gen.doc_ir, list)
                else node.assignments.gen.doc_ir
            )

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_module_code(self, node: uni.ModuleCode) -> None:
        """Generate DocIR for module code."""
        parts: list[doc.DocType] = []

        if (
            node.body and node.body.gen.doc_ir and node.body.gen.doc_ir
        ):  # check node.body.gen.doc_ir is not empty
            parts.append(node.body.gen.doc_ir[0])

        node.gen.doc_ir = [self.concat(parts)]

    def exit_global_stmt(self, node: uni.GlobalStmt) -> None:
        """Generate DocIR for global statements."""
        parts: list[doc.DocType] = [self.text("global ")]

        if node.target:
            name_parts: list[doc.DocType] = []
            for name in node.target.items:
                if name.gen.doc_ir:
                    name_parts.append(
                        name.gen.doc_ir[0]
                        if isinstance(name.gen.doc_ir, list)
                        else name.gen.doc_ir
                    )

            parts.append(self.join(self.text(", "), name_parts))

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_non_local_stmt(self, node: uni.NonLocalStmt) -> None:
        """Generate DocIR for nonlocal statements."""
        parts: list[doc.DocType] = [self.text("nonlocal ")]

        if node.target:
            name_parts: list[doc.DocType] = []
            for name in node.target.items:
                if name.gen.doc_ir:
                    name_parts.append(
                        name.gen.doc_ir[0]
                        if isinstance(name.gen.doc_ir, list)
                        else name.gen.doc_ir
                    )

            parts.append(self.join(self.text(", "), name_parts))

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_visit_stmt(self, node: uni.VisitStmt) -> None:
        """Generate DocIR for visit statements."""
        parts: list[doc.DocType] = [self.text("visit ")]

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir[0])

        if node.else_body and node.else_body.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(
                node.else_body.gen.doc_ir[0]
                if isinstance(node.else_body.gen.doc_ir, list)
                else node.else_body.gen.doc_ir
            )

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_ignore_stmt(self, node: uni.IgnoreStmt) -> None:
        """Generate DocIR for ignore statements."""
        parts: list[doc.DocType] = [self.text("ignore")]

        if node.target and node.target.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(node.target.gen.doc_ir[0])

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_connect_op(self, node: uni.ConnectOp) -> None:
        """Generate DocIR for connect operator."""
        parts: list[doc.DocType] = []

        if node.edge_dir == uni.EdgeDir.OUT:
            parts.append(self.text("-->"))
        elif node.edge_dir == uni.EdgeDir.IN:
            parts.append(self.text("<--"))
        elif node.edge_dir == uni.EdgeDir.ANY:
            parts.append(self.text("<-->"))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_disconnect_op(self, node: uni.DisconnectOp) -> None:
        """Generate DocIR for disconnect operator."""
        parts: list[doc.DocType] = []

        if node.edge_spec and node.edge_spec.edge_dir == uni.EdgeDir.OUT:
            parts.append(self.text("-/>"))
        elif node.edge_spec and node.edge_spec.edge_dir == uni.EdgeDir.IN:
            parts.append(self.text("</-"))
        elif node.edge_spec and node.edge_spec.edge_dir == uni.EdgeDir.ANY:
            parts.append(self.text("</>"))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_compare_expr(self, node: uni.CompareExpr) -> None:
        """Generate DocIR for comparison expressions."""
        parts: list[doc.DocType] = []

        # Left operand
        if node.left and node.left.gen.doc_ir:
            parts.append(
                node.left.gen.doc_ir[0] if node.left.gen.doc_ir else self.text("")
            )

        # Add operators and right operands
        for i, right in enumerate(node.rights):
            if i < len(node.ops):
                parts.append(self.text(f" {node.ops[i].value} "))
            if right.gen.doc_ir:
                parts.append(
                    right.gen.doc_ir[0]
                    if isinstance(right.gen.doc_ir, list)
                    else right.gen.doc_ir
                )

        node.gen.doc_ir = [self.group(parts)]

    def exit_atom_unit(self, node: uni.AtomUnit) -> None:
        """Generate DocIR for atom units (parenthesized expressions)."""
        parts: list[doc.DocType] = [self.text("(")]

        if node.value and node.value.gen.doc_ir:
            parts.append(node.value.gen.doc_ir[0])

        parts.append(self.text(")"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_expr_as_item(self, node: uni.ExprAsItem) -> None:
        """Generate DocIR for expression as item nodes."""
        parts: list[doc.DocType] = []

        if node.expr and node.expr.gen.doc_ir:
            parts.append(
                node.expr.gen.doc_ir[0]
                if isinstance(node.expr.gen.doc_ir, list)
                else node.expr.gen.doc_ir
            )

        if node.alias and node.alias.gen.doc_ir:
            parts.append(self.text(" as "))
            parts.append(
                node.alias.gen.doc_ir[0]
                if isinstance(node.alias.gen.doc_ir, list)
                else node.alias.gen.doc_ir
            )

        node.gen.doc_ir = [self.group(parts)]

    def exit_filter_compr(self, node: uni.FilterCompr) -> None:
        """Generate DocIR for filter comprehensions."""
        parts: list[doc.DocType] = []

        if node.f_type and node.f_type.gen.doc_ir:
            parts.append(self.text("filter "))
            parts.append(node.f_type.gen.doc_ir[0])

        node.gen.doc_ir = [self.concat(parts)]

    def exit_assign_compr(self, node: uni.AssignCompr) -> None:
        """Generate DocIR for assignment comprehensions."""
        parts: list[doc.DocType] = []

        if node.assigns:
            parts.append(self.text("with "))
            assign_parts: list[doc.DocType] = []
            for assign in node.assigns.items:
                if assign.gen.doc_ir:
                    assign_parts.append(
                        assign.gen.doc_ir[0]
                        if isinstance(assign.gen.doc_ir, list)
                        else assign.gen.doc_ir
                    )
            parts.append(self.join(self.text(", "), assign_parts))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_builtin_type(self, node: uni.BuiltinType) -> None:
        """Generate DocIR for builtin type nodes."""
        node.gen.doc_ir = [self.text(node.value)]

    def exit_py_inline_code(self, node: uni.PyInlineCode) -> None:
        """Generate DocIR for Python inline code blocks."""
        parts: list[doc.DocType] = [  # Ensure parts is list[doc.DocType]
            self.text("::py::"),
            self.hard_line(),
            self.text(node.code.value),
            self.hard_line(),
            self.text("::py::"),
        ]

        node.gen.doc_ir = [self.group(parts)]

    def exit_test(self, node: uni.Test) -> None:
        """Generate DocIR for test nodes."""
        parts: list[doc.DocType] = [self.text("test")]

        if node.name:
            parts.append(self.text(" "))
            parts.append(self.text(node.name.value))

        parts.append(self.text(" "))
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))
        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_check_stmt(self, node: uni.CheckStmt) -> None:
        """Generate DocIR for check statements."""
        parts: list[doc.DocType] = [self.text("check ")]

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir[0])

        parts.append(self.text(";"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_match_stmt(self, node: uni.MatchStmt) -> None:
        """Generate DocIR for match statements."""
        parts: list[doc.DocType] = [self.text("match ")]

        if node.target and node.target.gen.doc_ir:
            target_doc = node.target.gen.doc_ir[0]
            if target_doc:
                parts.append(target_doc)

        parts.append(self.text(" "))
        parts.append(self.text("{"))

        if node.cases:
            case_docs: list[doc.DocType] = []
            for case in node.cases:
                if case.gen.doc_ir:
                    case_doc_item = case.gen.doc_ir[0]
                    if case_doc_item:
                        case_docs.append(case_doc_item)
            if case_docs:
                parts.append(
                    self.indent(self.concat([self.hard_line(), self.concat(case_docs)]))
                )

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_match_case(self, node: uni.MatchCase) -> None:
        """Generate DocIR for match cases."""
        parts: list[doc.DocType] = [self.text("case ")]

        if node.pattern and node.pattern.gen.doc_ir:
            parts.append(node.pattern.gen.doc_ir[0])

        if node.guard and node.guard.gen.doc_ir:
            parts.append(self.text(" if "))
            parts.append(node.guard.gen.doc_ir[0])

        parts.append(self.text(":"))

        if node.body:
            body_content: list[doc.DocType] = []
            for stmt in node.body:
                if stmt.gen.doc_ir:
                    body_content.append(
                        stmt.gen.doc_ir[0]
                        if isinstance(stmt.gen.doc_ir, list)
                        else stmt.gen.doc_ir
                    )
                    body_content.append(self.hard_line())

            parts.append(
                self.indent(self.concat([self.hard_line(), self.concat(body_content)]))
            )

        node.gen.doc_ir = [self.group(parts)]

    def exit_match_value(self, node: uni.MatchValue) -> None:
        """Generate DocIR for match value patterns."""
        parts: list[doc.DocType] = []

        if node.value and node.value.gen.doc_ir:
            parts.append(
                node.value.gen.doc_ir[0]
                if isinstance(node.value.gen.doc_ir, list)
                else node.value.gen.doc_ir
            )

        node.gen.doc_ir = [self.concat(parts)]

    def exit_match_singleton(self, node: uni.MatchSingleton) -> None:
        """Generate DocIR for match singleton patterns."""
        parts: list[doc.DocType] = []

        if node.value and node.value.gen.doc_ir:
            parts.append(
                node.value.gen.doc_ir[0]
                if isinstance(node.value.gen.doc_ir, list)
                else node.value.gen.doc_ir
            )

        node.gen.doc_ir = [self.concat(parts)]

    def exit_match_sequence(self, node: uni.MatchSequence) -> None:
        """Generate DocIR for match sequence patterns."""
        parts: list[doc.DocType] = [self.text("[")]

        if node.values:
            pattern_parts: list[doc.DocType] = []
            for pattern in node.values:
                if pattern.gen.doc_ir:
                    pattern_parts.append(
                        pattern.gen.doc_ir[0]
                        if isinstance(pattern.gen.doc_ir, list)
                        else pattern.gen.doc_ir
                    )

            parts.append(self.join(self.text(", "), pattern_parts))

        parts.append(self.text("]"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_match_mapping(self, node: uni.MatchMapping) -> None:
        """Generate DocIR for match mapping patterns."""
        parts: list[doc.DocType] = [self.text("{")]

        if node.values:
            item_parts: list[doc.DocType] = []
            for item in node.values:
                if item.gen.doc_ir:
                    item_parts.append(
                        item.gen.doc_ir[0]
                        if isinstance(item.gen.doc_ir, list)
                        else item.gen.doc_ir
                    )

            parts.append(self.join(self.text(", "), item_parts))

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_match_or(self, node: uni.MatchOr) -> None:
        """Generate DocIR for match OR patterns."""
        parts: list[doc.DocType] = []

        if node.patterns:
            pattern_parts: list[doc.DocType] = []
            for pattern in node.patterns:
                if pattern.gen.doc_ir:
                    pattern_parts.append(
                        pattern.gen.doc_ir[0]
                        if isinstance(pattern.gen.doc_ir, list)
                        else pattern.gen.doc_ir
                    )

            parts.append(self.join(self.text(" | "), pattern_parts))

        node.gen.doc_ir = [self.group(parts)]

    def exit_match_as(self, node: uni.MatchAs) -> None:
        """Generate DocIR for match AS patterns."""
        parts: list[doc.DocType] = []

        if node.pattern and node.pattern.gen.doc_ir:
            parts.append(
                node.pattern.gen.doc_ir[0]
                if isinstance(node.pattern.gen.doc_ir, list)
                else node.pattern.gen.doc_ir
            )

        if node.name:
            parts.append(self.text(" as "))
            parts.append(self.text(node.name.sym_name))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_match_wild(self, node: uni.MatchWild) -> None:
        """Generate DocIR for match wildcard patterns."""
        node.gen.doc_ir = [self.text("_")]

    def exit_match_k_v_pair(self, node: uni.MatchKVPair) -> None:
        """Generate DocIR for match key-value pairs."""
        parts: list[doc.DocType] = []

        if node.key and node.key.gen.doc_ir:
            parts.append(
                node.key.gen.doc_ir[0]
                if isinstance(node.key.gen.doc_ir, list)
                else node.key.gen.doc_ir
            )

        parts.append(self.text(": "))

        if node.value and node.value.gen.doc_ir:
            parts.append(
                node.value.gen.doc_ir[0]
                if isinstance(node.value.gen.doc_ir, list)
                else node.value.gen.doc_ir
            )

        node.gen.doc_ir = [self.concat(parts)]

    def exit_match_arch(self, node: uni.MatchArch) -> None:
        """Generate DocIR for match architecture patterns."""
        parts: list[doc.DocType] = []

        if node.name and node.name.gen.doc_ir:
            parts.append(
                node.name.gen.doc_ir[0]
                if isinstance(node.name.gen.doc_ir, list)
                else node.name.gen.doc_ir
            )

        parts.append(self.text("("))

        if node.arg_patterns:
            arg_parts: list[doc.DocType] = []
            for arg in node.arg_patterns.items:
                if arg.gen.doc_ir:
                    arg_parts.append(
                        arg.gen.doc_ir[0]
                        if isinstance(arg.gen.doc_ir, list)
                        else arg.gen.doc_ir
                    )

            parts.append(self.join(self.text(", "), arg_parts))

        if node.kw_patterns:
            if node.arg_patterns:
                parts.append(self.text(", "))

            kw_parts: list[doc.DocType] = []
            for kw in node.kw_patterns.items:
                if kw.gen.doc_ir:
                    kw_parts.append(
                        kw.gen.doc_ir[0]
                        if isinstance(kw.gen.doc_ir, list)
                        else kw.gen.doc_ir
                    )

            parts.append(self.join(self.text(", "), kw_parts))

        parts.append(self.text(")"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_enum(self, node: uni.Enum) -> None:
        """Generate DocIR for enum declarations."""
        parts: list[doc.DocType] = []

        # Handle decorators
        if node.decorators:
            for decorator in node.decorators.items:
                if decorator.gen.doc_ir:
                    parts.append(decorator.gen.doc_ir[0])
                    parts.append(self.hard_line())

        # Enum declaration
        parts.append(self.text("enum "))
        if node.name:
            parts.append(self.text(node.name.value))

        # Inheritance
        if node.base_classes and node.base_classes.gen.doc_ir:
            parts.append(self.text(": "))
            parts.append(node.base_classes.gen.doc_ir[0])

        parts.append(self.text(" {"))

        if node.body:
            member_parts: list[doc.DocType] = []
            for member in node.body.items:
                if member.gen.doc_ir:
                    member_parts.append(
                        member.gen.doc_ir[0]
                        if isinstance(member.gen.doc_ir, list)
                        else member.gen.doc_ir
                    )
                    member_parts.append(self.hard_line())

            parts.append(
                self.indent(self.concat([self.hard_line(), self.concat(member_parts)]))
            )
            parts.append(self.hard_line())

        parts.append(self.text("};"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_sub_tag(self, node: uni.SubTag) -> None:
        """Generate DocIR for sub-tag nodes."""
        parts: list[doc.DocType] = []

        if node.tag and node.tag.gen.doc_ir:
            parts.append(
                node.tag.gen.doc_ir[0]
                if isinstance(node.tag.gen.doc_ir, list)
                else node.tag.gen.doc_ir
            )

        node.gen.doc_ir = [self.concat(parts)]

    def exit_sub_node_list(self, node: uni.SubNodeList) -> None:
        """Generate DocIR for sub-node lists."""
        parts: list[doc.DocType] = []

        if node.items:
            item_parts: list[doc.DocType] = []
            for item in node.items:
                if item.gen.doc_ir:
                    item_parts.append(
                        item.gen.doc_ir[0]
                        if isinstance(item.gen.doc_ir, list)
                        else item.gen.doc_ir
                    )

            parts.append(self.join(self.text(", "), item_parts))

        node.gen.doc_ir = [self.concat(parts)]

    def exit_token(self, node: uni.Token) -> None:
        """Generate DocIR for tokens."""
        node.gen.doc_ir = [self.text(node.value)]

    def exit_semi(self, node: uni.Semi) -> None:
        """Generate DocIR for semicolons."""
        node.gen.doc_ir = [self.text(node.value)]

    def exit_comment_token(self, node: uni.CommentToken) -> None:
        """Generate DocIR for comment tokens."""
        if node.is_inline:
            node.gen.doc_ir = [self.text(node.value)]
        else:
            node.gen.doc_ir = [self.group([self.text(node.value), self.hard_line()])]

    def exit_impl_def(self, node: uni.ImplDef) -> None:
        """Generate DocIR for implementation definitions."""
        parts: list[doc.DocType] = []

        if node.target and node.target.items:
            # Assuming the first item in target is the relevant one for now
            target_item = node.target.items[0]
            if target_item.gen.doc_ir:
                parts.append(
                    target_item.gen.doc_ir[0]
                    if isinstance(target_item.gen.doc_ir, list)
                    else target_item.gen.doc_ir
                )

        parts.append(self.text(" {"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

    def exit_event_signature(self, node: uni.EventSignature) -> None:
        """Generate DocIR for event signatures."""
        parts: list[doc.DocType] = []

        if node.event and node.event.gen.doc_ir:
            parts.append(node.event.gen.doc_ir[0])
        node.gen.doc_ir = [self.group(parts)]

    def exit_typed_ctx_block(self, node: uni.TypedCtxBlock) -> None:
        """Generate DocIR for typed context blocks."""
        parts: list[doc.DocType] = []

        if hasattr(node, "name") and node.name:
            parts.append(self.text(node.name.value))

        if hasattr(node, "type_tag") and node.type_tag and node.type_tag.gen.doc_ir:
            parts.append(self.text(": "))
            parts.append(node.type_tag.gen.doc_ir)

        parts.append(self.text(" {"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir[0]
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = [self.group(parts)]

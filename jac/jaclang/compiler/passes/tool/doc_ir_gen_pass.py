"""DocIrGenPass for Jaseci Ast.

This is a pass for generating DocIr for Jac code.
"""

from typing import List, Optional

import jaclang.compiler.passes.tool.doc_ir as doc
import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.settings import settings


class DocIRGenPass(UniPass):
    """DocIrGenPass generate DocIr for Jac code."""

    def before_pass(self) -> None:
        """Initialize pass."""
        # Options for DocIr generation
        self.comments = self.ir_in.source.comments
        self.indent_size = 4
        self.MAX_LINE_LENGTH = settings.max_line_length

    def after_pass(self) -> None:
        """After pass."""
        self.ir_out.gen.jac = self.print_jac()

    def text(self, text: str) -> doc.Text:
        """Create a Text node."""
        return doc.Text(text)

    def line(self, hard: bool = False, literal: bool = False) -> doc.Line:
        """Create a Line node."""
        return doc.Line(hard, literal)

    def hard_line(self) -> doc.Line:
        """Create a hard line break."""
        return doc.Line(hard=True)

    def tight_line(self) -> doc.Line:
        """Create a tight line break."""
        return doc.Line(tight=True)

    def literal_line(self) -> doc.Line:
        """Create a literal line break."""
        return doc.Line(literal=True)

    def group(
        self,
        contents: doc.DocType,
        break_contiguous: bool = False,
    ) -> doc.Group:
        """Create a Group node."""
        return doc.Group(contents, break_contiguous)

    def indent(self, contents: doc.DocType) -> doc.Indent:
        """Create an Indent node."""
        return doc.Indent(contents)

    def concat(self, parts: List[doc.DocType]) -> doc.Concat:
        """Create a Concat node."""
        return doc.Concat(parts)

    def if_break(
        self,
        break_contents: doc.DocType,
        flat_contents: doc.DocType,
    ) -> doc.IfBreak:
        """Create an IfBreak node."""
        return doc.IfBreak(break_contents, flat_contents)

    def align(self, contents: doc.DocType, n: Optional[int] = None) -> doc.Align:
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

    def exit_module(self, node: uni.Module) -> None:
        """Exit module."""
        parts: list[doc.DocType] = []

        # Process docstrings
        if node.kid and isinstance(node.kid[0], uni.String):
            parts.append(
                self.group(
                    self.concat(
                        [
                            self.text(node.kid[0].value),
                            self.hard_line(),
                            self.hard_line(),
                        ]
                    )
                )
            )

        # Process imports
        import_parts: list[doc.DocType] = []
        for item in node.body:
            if isinstance(item, uni.Import) and item.gen.doc_ir:
                import_parts.append(item.gen.doc_ir)
                import_parts.append(self.hard_line())

        if import_parts:
            parts.append(self.group(self.concat(import_parts)))
            parts.append(self.hard_line())

        # Process other top-level elements
        other_parts: list[doc.DocType] = []
        for item in node.body:
            if not isinstance(item, uni.Import) and item.gen.doc_ir:
                other_parts.append(item.gen.doc_ir)
                other_parts.append(self.hard_line())
                other_parts.append(self.hard_line())

        if other_parts and isinstance(other_parts[-1], doc.Line):
            other_parts.pop()  # Remove trailing line

        parts.append(self.group(self.concat(other_parts)))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_import(self, node: uni.Import) -> None:
        """Exit import node."""
        parts: List[doc.DocType] = []
        if node.doc:
            parts.append(node.doc.gen.doc_ir)
            parts.append(self.hard_line())
        if node.is_absorb:
            parts.append(self.text("include"))
        else:
            parts.append(self.text("import"))
        parts.append(self.text(" "))
        if node.from_loc:
            parts.append(self.text("from "))
            from_loc_gen_ir = node.from_loc.gen.doc_ir
            if from_loc_gen_ir:
                parts.append(from_loc_gen_ir)
            parts.append(self.text(" "))  # Space before {

            items_gen_ir = node.items.gen.doc_ir
            actual_items_doc: doc.DocType = self.concat([])  # Default to empty concat
            if items_gen_ir:
                actual_items_doc = items_gen_ir

            # Group the braced items to allow single-line or multi-line formatting
            braced_items = self.group(
                self.concat(
                    [
                        self.text("{"),
                        self.indent(
                            self.concat(
                                [
                                    self.line(),  # Soft line, becomes space or newline
                                    actual_items_doc,
                                ]
                            )
                        ),
                        self.line(),  # Soft line
                        self.text("}"),
                    ]
                )
            )
            parts.append(braced_items)
        else:
            items_gen_ir = node.items.gen.doc_ir
            if items_gen_ir:
                parts.append(items_gen_ir)
            parts.append(self.text(";"))
        node.gen.doc_ir = self.concat(parts)

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

        node.gen.doc_ir = doc_ir

    def exit_module_path(self, node: uni.ModulePath) -> None:
        """Generate DocIR for module paths."""
        parts: list[doc.DocType] = []

        if (
            node.path and node.path.items
        ):  # Check if node.path and node.path.items are not None
            for i, path_item in enumerate(node.path.items):
                if path_item.gen.doc_ir:
                    parts.append(path_item.gen.doc_ir)
                    if i < len(node.path.items) - 1:
                        parts.append(self.text("."))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_architype(self, node: uni.Architype) -> None:
        """Generate DocIR for architypes."""
        parts: list[doc.DocType] = []

        # Handle decorators
        if node.decorators and node.decorators.items:
            decorator_docs: list[doc.DocType] = []
            for decorator_node in node.decorators.items:
                if decorator_node.gen.doc_ir:
                    decorator_doc = decorator_node.gen.doc_ir
                    if decorator_doc:
                        decorator_docs.append(decorator_doc)
                        decorator_docs.append(self.hard_line())
            if decorator_docs:
                parts.extend(decorator_docs)

        # Type declaration: arch_type <name>
        header_parts: list[doc.DocType] = [self.text(node.arch_type.value)]
        if node.name and node.name.gen.doc_ir:  # name is Name, gen.doc_ir will be text
            header_parts.append(self.text(" "))
            name_doc = node.name.gen.doc_ir
            if name_doc:
                header_parts.append(name_doc)

        # Inheritance: : base1, base2
        if (
            node.base_classes
            and node.base_classes.items
            and node.base_classes.gen.doc_ir
        ):
            base_classes_doc = node.base_classes.gen.doc_ir
            if not (
                isinstance(base_classes_doc, doc.Concat) and not base_classes_doc.parts
            ):
                header_parts.append(self.text(": "))
                header_parts.append(base_classes_doc)

        parts.append(self.group(self.concat(header_parts)))  # Group the header part

        # Handle body: { ... }
        if node.body:
            parts.append(self.text(" {"))
            body_content_parts: list[doc.DocType] = []
            if isinstance(node.body, uni.SubNodeList) and node.body.items:
                # Iterate through items of SubNodeList and add hard_line after each
                for item in node.body.items:
                    if item.gen.doc_ir:
                        item_doc = item.gen.doc_ir
                        if item_doc:
                            body_content_parts.append(item_doc)
                            body_content_parts.append(self.hard_line())
                if body_content_parts and isinstance(
                    body_content_parts[-1], doc.Line
                ):  # Remove last hard_line
                    body_content_parts.pop()
            elif isinstance(node.body, uni.ImplDef) and node.body.gen.doc_ir:
                impl_def_doc = node.body.gen.doc_ir
                if impl_def_doc:
                    body_content_parts.append(impl_def_doc)

            if body_content_parts:
                parts.append(
                    self.indent(
                        self.concat([self.hard_line(), self.concat(body_content_parts)])
                    )
                )
                parts.append(self.hard_line())  # Line before closing brace
            else:  # Empty body {} vs {\n}
                parts.append(self.line())  # allow break for empty body like { \n }

            parts.append(self.text("}"))
        else:  # No body, e.g., forward declaration with SEMI
            parts.append(self.text(";"))  # From grammar: arch_type ... (body | SEMI)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_ability(self, node: uni.Ability) -> None:
        """Generate DocIR for abilities."""
        parts: list[doc.DocType] = []

        # Handle decorators
        if node.decorators and node.decorators.items:
            decorator_docs: list[doc.DocType] = []
            for decorator_node in node.decorators.items:
                if decorator_node.gen.doc_ir:
                    decorator_doc = decorator_node.gen.doc_ir
                    if decorator_doc:
                        decorator_docs.append(decorator_doc)
                        decorator_docs.append(self.hard_line())
            if decorator_docs:
                parts.extend(decorator_docs)

        header_parts: list[doc.DocType] = []
        # Static keyword
        if node.is_static:
            header_parts.append(self.text("static "))

        # Type (can/def)
        if node.is_def:
            header_parts.append(self.text("def"))
        else:
            header_parts.append(self.text("can"))

        # Name and signature
        if node.name_ref and node.name_ref.gen.doc_ir:
            name_ref_doc = node.name_ref.gen.doc_ir
            if name_ref_doc:
                header_parts.append(self.text(" "))
                header_parts.append(name_ref_doc)

        if node.signature and node.signature.gen.doc_ir:
            sig_doc = node.signature.gen.doc_ir
            if sig_doc:
                header_parts.append(sig_doc)

        parts.append(self.group(self.concat(header_parts)))  # Group the header

        # Handle body
        if node.body:  # body is SubNodeList[CodeBlockStmt] or ImplDef or FuncCall
            parts.append(self.text(" "))  # Space before {
            if isinstance(node.body, uni.FuncCall):  # GenAI ability: by func_call;
                parts.append(self.text("by "))
                if node.body.gen.doc_ir:
                    body_doc = node.body.gen.doc_ir
                    if body_doc:
                        parts.append(body_doc)
                parts.append(self.text(";"))
            elif isinstance(node.body, uni.SubNodeList):  # Regular ability with a block
                parts.append(self.text("{"))
                body_content_parts: list[doc.DocType] = []
                if node.body.items:
                    for item in node.body.items:
                        if item.gen.doc_ir:
                            item_doc = item.gen.doc_ir
                            if item_doc:
                                body_content_parts.append(item_doc)
                                body_content_parts.append(self.hard_line())
                    if body_content_parts and isinstance(
                        body_content_parts[-1], doc.Line
                    ):
                        body_content_parts.pop()  # remove last hard_line

                if body_content_parts:
                    parts.append(
                        self.indent(
                            self.concat(
                                [self.hard_line(), self.concat(body_content_parts)]
                            )
                        )
                    )
                    parts.append(self.hard_line())  # Line before closing brace
                else:  # Empty body {}
                    parts.append(self.line())  # allow break for empty body like { \n }
                parts.append(self.text("}"))
        elif node.is_abstract:  # abstract ability: def name() abstract;
            parts.append(self.text(" abstract;"))
        else:  # No body and not abstract, e.g. forward decl for event: can event_name with func_sig;
            parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_func_signature(self, node: uni.FuncSignature) -> None:
        """Generate DocIR for function signatures."""
        parts: list[doc.DocType] = [self.text("(")]

        if node.params and node.params.gen.doc_ir:
            # node.params.gen.doc_ir should now be the DocIR for the joined parameter list
            # as produced by the updated exit_sub_node_list
            params_doc = node.params.gen.doc_ir

            # Only add content if params_doc is not empty (e.g., not an empty self.concat([]))
            # We need a way to check if a DocType is "empty". For now, assume it might be non-empty.
            # A more robust check would be if params_doc is a Concat with no parts.
            is_empty_concat = (
                isinstance(params_doc, doc.Concat) and not params_doc.parts
            )

            if not is_empty_concat:
                parts.append(
                    self.indent(
                        self.concat(
                            [
                                self.tight_line(),  # soft line, becomes space or newline
                                params_doc,
                            ]
                        )
                    )
                )
                parts.append(self.tight_line())  # soft line before closing ')'
        parts.append(self.text(")"))

        # Return type
        if node.return_type and node.return_type.gen.doc_ir:
            return_type_doc = node.return_type.gen.doc_ir
            if return_type_doc:
                parts.append(self.text(" -> "))
                parts.append(return_type_doc)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_param_var(self, node: uni.ParamVar) -> None:
        """Generate DocIR for parameter variables."""
        parts: list[doc.DocType] = []

        if node.name:
            parts.append(self.text(node.name.value))

        if node.type_tag and node.type_tag.gen.doc_ir:
            parts.append(self.text(": "))
            parts.append(node.type_tag.tag.gen.doc_ir)

        if node.value and node.value.gen.doc_ir:
            parts.append(self.text(" = "))
            parts.append(node.value.gen.doc_ir)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_type_ref(self, node: uni.TypeRef) -> None:
        """Generate DocIR for type references."""
        parts: list[doc.DocType] = []

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_assignment(self, node: uni.Assignment) -> None:
        """Generate DocIR for assignments."""
        parts: list[doc.DocType] = []

        # Left side (target)
        if node.target and node.target.gen.doc_ir:  # target is SubNodeList[Expr]
            # Assuming node.target.gen.doc_ir is the processed doc for targets
            # If multiple targets (e.g. a,b = 1,2), SubNodeList should have handled joining them (e.g. with ", ")
            target_doc = node.target.gen.doc_ir
            if target_doc and not (
                isinstance(target_doc, doc.Concat) and not target_doc.parts
            ):
                parts.append(target_doc)

        # Type annotation
        if node.type_tag and node.type_tag.gen.doc_ir:
            type_tag_doc = node.type_tag.gen.doc_ir
            if type_tag_doc:
                parts.append(
                    self.text(": ")
                )  # unitree has SubTag for type_tag, which adds ':'
                # but here it's direct, so add ': '
                parts.append(type_tag_doc)

        # Assignment operator
        op_str = node.aug_op.value if node.aug_op else "="
        parts.append(self.text(f" {op_str} "))

        # Right side (value)
        if node.value and node.value.gen.doc_ir:
            value_doc = node.value.gen.doc_ir
            if value_doc:
                # Potentially breakable if the value is long
                parts.append(
                    self.group(self.indent(self.concat([self.line(), value_doc])))
                )

        # Semicolon, unless it's an Enum statement or inside specific for-loop parts
        # or inside GlobalVars (handled by GlobalVars exit)
        is_global_var_item = False
        if (
            node.parent
            and isinstance(node.parent, uni.SubNodeList)
            and node.parent.parent
            and isinstance(node.parent.parent, uni.GlobalVars)
        ):
            is_global_var_item = True

        if (
            not node.is_enum_stmt
            and not isinstance(node.parent, uni.IterForStmt)
            and not is_global_var_item
        ):
            parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_if_stmt(self, node: uni.IfStmt) -> None:
        """Generate DocIR for if statements."""
        parts: list[doc.DocType] = [self.text("if ")]

        # Condition
        if node.condition and node.condition.gen.doc_ir:
            cond_doc = node.condition.gen.doc_ir
            if cond_doc:
                # Group condition to allow breaking if it's very long
                parts.append(self.group(cond_doc))

        # Body: { ... }
        parts.append(self.text(" {"))  # Space before {
        body_content_parts: list[doc.DocType] = []
        if node.body and node.body.items:  # body is SubNodeList[CodeBlockStmt]
            for item in node.body.items:
                if item.gen.doc_ir:
                    item_doc = item.gen.doc_ir
                    if item_doc:
                        body_content_parts.append(item_doc)
                        body_content_parts.append(self.hard_line())
            if body_content_parts and isinstance(
                body_content_parts[-1], doc.Line
            ):  # remove last hard_line
                body_content_parts.pop()

        if body_content_parts:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(body_content_parts)])
                )
            )
            parts.append(self.hard_line())  # Line before closing brace
        else:  # Empty body {}
            parts.append(self.line())  # allow break for empty body like { \n }
        parts.append(self.text("}"))

        # Else or ElseIf
        if node.else_body and node.else_body.gen.doc_ir:
            # else_body could be ElseIf or ElseStmt. Their gen.doc_ir is the full construct.
            else_doc = node.else_body.gen.doc_ir
            if else_doc:
                parts.append(self.text(" "))  # Space before else/elif
                parts.append(else_doc)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_else_if(self, node: uni.ElseIf) -> None:
        """Generate DocIR for else if statements."""
        # uni.ElseIf inherits from uni.IfStmt, structure is similar: elif cond { body } else_chain?
        parts: list[doc.DocType] = [self.text("elif ")]

        # Condition
        if node.condition and node.condition.gen.doc_ir:
            cond_doc = node.condition.gen.doc_ir
            if cond_doc:
                parts.append(self.group(cond_doc))

        # Body: { ... }
        parts.append(self.text(" {"))
        body_content_parts: list[doc.DocType] = []
        if node.body and node.body.items:  # body is SubNodeList[CodeBlockStmt]
            for item in node.body.items:
                if item.gen.doc_ir:
                    item_doc = item.gen.doc_ir
                    if item_doc:
                        body_content_parts.append(item_doc)
                        body_content_parts.append(self.hard_line())
            if body_content_parts and isinstance(body_content_parts[-1], doc.Line):
                body_content_parts.pop()

        if body_content_parts:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(body_content_parts)])
                )
            )
            parts.append(self.hard_line())
        else:
            parts.append(self.line())
        parts.append(self.text("}"))

        # Else or ElseIf chain
        if node.else_body and node.else_body.gen.doc_ir:
            else_doc = node.else_body.gen.doc_ir
            if else_doc:
                parts.append(self.text(" "))
                parts.append(else_doc)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_else_stmt(self, node: uni.ElseStmt) -> None:
        """Generate DocIR for else statements."""
        parts: list[doc.DocType] = [self.text("else")]

        # Body: { ... }
        parts.append(self.text(" {"))
        body_content_parts: list[doc.DocType] = []
        if node.body and node.body.items:  # body is SubNodeList[CodeBlockStmt]
            for item in node.body.items:
                if item.gen.doc_ir:
                    item_doc = item.gen.doc_ir
                    if item_doc:
                        body_content_parts.append(item_doc)
                        body_content_parts.append(self.hard_line())
            if body_content_parts and isinstance(body_content_parts[-1], doc.Line):
                body_content_parts.pop()

        if body_content_parts:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(body_content_parts)])
                )
            )
            parts.append(self.hard_line())
        else:
            parts.append(self.line())
        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_binary_expr(self, node: uni.BinaryExpr) -> None:
        """Generate DocIR for binary expressions."""
        parts: list[doc.DocType] = []

        # Left operand
        if node.left and node.left.gen.doc_ir:
            left_doc = node.left.gen.doc_ir
            if left_doc:
                parts.append(left_doc)

        # Operator - with a potential line break before it
        op_str = ""
        if isinstance(node.op, uni.Token):
            op_str = node.op.value
        elif node.op and node.op.gen.doc_ir:  # For ConnectOp/DisconnectOp as op
            op_doc = node.op.gen.doc_ir
            if op_doc and isinstance(
                op_doc, doc.Text
            ):  # Assuming these ops become simple text
                op_str = op_doc.text
            elif op_doc:  # If it's a more complex DocType for an op
                parts.append(self.line())  # space or newline
                parts.append(op_doc)
                parts.append(self.text(" "))  # space after op
                op_str = "complex_op_handled"  # Flag to skip default op handling

        if op_str and op_str != "complex_op_handled":
            # Decide if operator needs spaces around it based on Jac style (e.g., `a+b` vs `a + b`)
            # Common style is spaces around binary ops, except maybe for `**`.
            # For now, always add spaces.
            parts.append(
                self.line()
            )  # Soft line before operator (becomes space or newline)
            parts.append(self.text(op_str))
            parts.append(
                self.text(" ")
            )  # Ensure space after operator if it doesn't break

        # Right operand
        if node.right and node.right.gen.doc_ir:
            right_doc = node.right.gen.doc_ir
            if right_doc:
                parts.append(right_doc)

        # The whole binary expression is a group. If it breaks, it tries to break at self.line().
        # Parentheses are not added by default by this formatter,
        # relying on parser to create AtomUnit (parenthesized expr) if original code had them
        # or if needed for precedence by other transformation passes.
        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_expr_stmt(self, node: uni.ExprStmt) -> None:
        """Generate DocIR for expression statements."""
        parts: list[doc.DocType] = []

        if node.expr and node.expr.gen.doc_ir:
            parts.append(node.expr.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_concurrent_expr(self, node: uni.ConcurrentExpr) -> None:
        """Generate DocIR for concurrent expressions."""
        parts: list[doc.DocType] = []

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_return_stmt(self, node: uni.ReturnStmt) -> None:
        """Generate DocIR for return statements."""
        parts: list[doc.DocType] = [self.text("return")]

        if node.expr and node.expr.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(node.expr.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_func_call(self, node: uni.FuncCall) -> None:
        """Generate DocIR for function calls."""
        parts: list[doc.DocType] = []

        # Name or callable expression (target in FuncCall)
        if node.target and node.target.gen.doc_ir:
            target_doc = node.target.gen.doc_ir
            if target_doc:
                parts.append(target_doc)

        # Parameters
        parts.append(self.text("("))

        if (
            node.params and node.params.items and node.params.gen.doc_ir
        ):  # Check items for non-empty list
            # node.params.gen.doc_ir is the DocIR for the joined parameter list
            params_doc = node.params.gen.doc_ir
            is_empty_concat = (
                isinstance(params_doc, doc.Concat) and not params_doc.parts
            )

            if not is_empty_concat:
                parts.append(
                    self.indent(
                        self.concat([self.tight_line(), params_doc])
                    )  # soft line
                )
                parts.append(self.tight_line())  # soft line before closing ')'

        parts.append(self.text(")"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_atom_trailer(self, node: uni.AtomTrailer) -> None:
        """Generate DocIR for atom trailers."""
        parts: list[doc.DocType] = []

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir)

        # Null-safe operator
        if node.is_null_ok:
            parts.append(self.text("?."))
        # Dot operator for attribute access
        elif node.is_attr:
            parts.append(self.text("."))

        if node.right and node.right.gen.doc_ir:
            parts.append(node.right.gen.doc_ir)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_name(self, node: uni.Name) -> None:
        """Generate DocIR for names."""
        if node.is_kwesc:
            node.gen.doc_ir = self.text(f"<>{node.value}")
        else:
            node.gen.doc_ir = self.text(node.value)

    def exit_int(self, node: uni.Int) -> None:
        """Generate DocIR for integers."""
        node.gen.doc_ir = self.text(node.value)

    def exit_float(self, node: uni.Float) -> None:
        """Generate DocIR for floats."""
        node.gen.doc_ir = self.text(node.value)

    def exit_string(self, node: uni.String) -> None:
        """Generate DocIR for strings."""
        # Handle multiline strings
        if "\n" in node.value:
            lines = node.value.split("\n")
            parts: list[doc.DocType] = [self.text(lines[0])]

            for line in lines[1:]:
                parts.append(self.hard_line())
                parts.append(self.text(line))

            node.gen.doc_ir = self.group(self.concat(parts))
        else:
            node.gen.doc_ir = self.text(node.value)

    def exit_list_val(self, node: uni.ListVal) -> None:
        """Generate DocIR for list values."""
        parts: list[doc.DocType] = [self.text("[")]

        if (
            node.values and node.values.items and node.values.gen.doc_ir
        ):  # Check items for non-empty list
            # node.values.gen.doc_ir is the DocIR for the joined value list
            values_doc = node.values.gen.doc_ir
            if not (isinstance(values_doc, doc.Concat) and not values_doc.parts):
                parts.append(
                    self.indent(self.concat([self.line(), values_doc]))  # soft line
                )
                parts.append(self.line())  # soft line before closing ']'
            # Python {} is an empty dict, set() is an empty set.
            # Jac {a,b} is a set. If node.values is empty, it should be set().
            # This pass currently generates {} for empty set if node.values is None/empty.
            # This might need adjustment if Jac syntax for empty set is different or needs explicit set().
            # For now, assuming {} is acceptable if the parser produces SetVal with no items.
            # If it must be `set()`, then this logic needs to change for empty `node.values`.
            # Based on unitree.SetVal.normalize, it produces {} for empty set.

        parts.append(self.text("]"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_dict_val(self, node: uni.DictVal) -> None:
        """Generate DocIR for dictionary values."""
        parts: list[doc.DocType] = [self.text("{")]

        # node.kv_pairs is a Python list of KVPair, not a SubNodeList here.
        # We need to get the doc_ir from each KVPair and join them.
        if node.kv_pairs:
            pair_docs: list[doc.DocType] = []
            for pair_node in node.kv_pairs:
                if pair_node.gen.doc_ir:
                    pair_doc = pair_node.gen.doc_ir
                    if pair_doc:
                        pair_docs.append(pair_doc)

            if pair_docs:
                # Join the KVPair docs with "," and a line break opportunity
                joined_kv_pairs = self.join(
                    self.concat([self.text(","), self.line()]), pair_docs
                )
                is_empty_concat = (
                    isinstance(joined_kv_pairs, doc.Concat)
                    and not joined_kv_pairs.parts
                )

                if not is_empty_concat:
                    parts.append(
                        self.indent(
                            self.concat([self.line(), joined_kv_pairs])  # soft line
                        )
                    )
                    parts.append(self.line())  # soft line before closing '}'

        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_k_v_pair(self, node: uni.KVPair) -> None:
        """Generate DocIR for key-value pairs."""
        parts: list[doc.DocType] = []

        if node.key and node.key.gen.doc_ir:
            parts.append(node.key.gen.doc_ir)
            parts.append(self.text(": "))

        if node.value and node.value.gen.doc_ir:
            parts.append(node.value.gen.doc_ir)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_has_var(self, node: uni.HasVar) -> None:
        """Generate DocIR for has variable declarations."""
        parts: list[doc.DocType] = []

        if node.name:
            parts.append(self.text(node.name.value))

        if node.type_tag and node.type_tag.gen.doc_ir:
            parts.append(self.text(": "))
            parts.append(node.type_tag.gen.doc_ir)

        if node.value and node.value.gen.doc_ir:
            parts.append(self.text(" = "))
            parts.append(node.value.gen.doc_ir)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_arch_has(self, node: uni.ArchHas) -> None:
        """Generate DocIR for architecture has declarations."""
        parts: list[doc.DocType] = []

        if node.doc:
            parts.insert(0, node.doc.gen.doc_ir)
            parts.append(self.hard_line())
        parts.append(self.text("has "))
        if node.is_static:
            parts.append(self.text("static "))

        if node.vars:
            var_parts: list[doc.DocType] = []
            for var in node.vars.items:
                if var.gen.doc_ir:
                    var_parts.append(var.gen.doc_ir)

            parts.append(
                self.align(
                    self.join(self.concat([self.text(", "), self.line()]), var_parts)
                )
            )

        parts.append(self.text(";"))
        parts.append(self.hard_line())

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_while_stmt(self, node: uni.WhileStmt) -> None:
        """Generate DocIR for while statements."""
        parts: list[doc.DocType] = [self.text("while ")]

        if node.condition and node.condition.gen.doc_ir:
            cond_doc = node.condition.gen.doc_ir
            if cond_doc:
                parts.append(self.group(cond_doc))

        parts.append(self.text(" {"))
        body_content_parts: list[doc.DocType] = []
        if node.body and node.body.items:  # body is SubNodeList[CodeBlockStmt]
            for item in node.body.items:
                if item.gen.doc_ir:
                    item_doc = item.gen.doc_ir
                    if item_doc:
                        body_content_parts.append(item_doc)
                        body_content_parts.append(self.hard_line())
            if body_content_parts and isinstance(body_content_parts[-1], doc.Line):
                body_content_parts.pop()

        if body_content_parts:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(body_content_parts)])
                )
            )
            parts.append(self.hard_line())
        else:
            parts.append(self.line())
        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_in_for_stmt(self, node: uni.InForStmt) -> None:
        """Generate DocIR for for-in statements."""
        parts: list[doc.DocType] = [self.text("for ")]

        if node.target and node.target.gen.doc_ir:
            target_doc = node.target.gen.doc_ir
            if target_doc:
                parts.append(self.group(target_doc))  # Target can be complex

        parts.append(self.text(" in "))

        if node.collection and node.collection.gen.doc_ir:
            coll_doc = node.collection.gen.doc_ir
            if coll_doc:
                parts.append(self.group(coll_doc))  # Collection can be complex

        parts.append(self.text(" {"))
        body_content_parts: list[doc.DocType] = []
        if node.body and node.body.items:  # body is SubNodeList[CodeBlockStmt]
            for item in node.body.items:
                if item.gen.doc_ir:
                    item_doc = item.gen.doc_ir
                    if item_doc:
                        body_content_parts.append(item_doc)
                        body_content_parts.append(self.hard_line())
            if body_content_parts and isinstance(body_content_parts[-1], doc.Line):
                body_content_parts.pop()

        if body_content_parts:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(body_content_parts)])
                )
            )
            parts.append(self.hard_line())
        else:
            parts.append(self.line())
        parts.append(self.text("}"))

        # Jac for...in doesn't have an else clause in unitree.py

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_iter_for_stmt(self, node: uni.IterForStmt) -> None:
        """Generate DocIR for iterative for statements."""
        parts: list[doc.DocType] = [self.text("for ")]

        # iter, condition, count_by are all potentially complex and groupable
        if node.iter and node.iter.gen.doc_ir:
            iter_doc = node.iter.gen.doc_ir
            if iter_doc:
                parts.append(self.group(iter_doc))
        # SEMI is added by Assignment node itself if it's a full statement.
        # Here, it's part of for, so explicit semicolon if not an aug_assign which is not allowed here by grammar.
        # The Assignment node in IterForStmt will not add its own semicolon due to parent context.
        parts.append(self.text("; "))

        if node.condition and node.condition.gen.doc_ir:
            cond_doc = node.condition.gen.doc_ir
            if cond_doc:
                parts.append(self.group(cond_doc))
        parts.append(self.text("; "))

        if node.count_by and node.count_by.gen.doc_ir:
            count_doc = node.count_by.gen.doc_ir
            if count_doc:
                parts.append(self.group(count_doc))
        # No final semicolon for the header part of for loop.

        parts.append(self.text(" {"))
        body_content_parts: list[doc.DocType] = []
        if node.body and node.body.items:  # body is SubNodeList[CodeBlockStmt]
            for item in node.body.items:
                if item.gen.doc_ir:
                    item_doc = item.gen.doc_ir
                    if item_doc:
                        body_content_parts.append(item_doc)
                        body_content_parts.append(self.hard_line())
            if body_content_parts and isinstance(body_content_parts[-1], doc.Line):
                body_content_parts.pop()

        if body_content_parts:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(body_content_parts)])
                )
            )
            parts.append(self.hard_line())
        else:
            parts.append(self.line())
        parts.append(self.text("}"))

        # Jac iter_for_stmt doesn't have an else clause in unitree.py

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_try_stmt(self, node: uni.TryStmt) -> None:
        """Generate DocIR for try statements."""
        parts: list[doc.DocType] = [self.text("try")]

        # Try Body
        parts.append(self.text(" {"))
        try_body_content_parts: list[doc.DocType] = []
        if node.body and node.body.items:  # body is SubNodeList[CodeBlockStmt]
            for item in node.body.items:
                if item.gen.doc_ir:
                    item_doc = item.gen.doc_ir
                    if item_doc:
                        try_body_content_parts.append(item_doc)
                        try_body_content_parts.append(self.hard_line())
            if try_body_content_parts and isinstance(
                try_body_content_parts[-1], doc.Line
            ):
                try_body_content_parts.pop()

        if try_body_content_parts:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(try_body_content_parts)])
                )
            )
            parts.append(self.hard_line())
        else:
            parts.append(self.line())
        parts.append(self.text("}"))

        # Handle except clauses (SubNodeList[Except])
        if node.excepts and node.excepts.items:
            for (
                except_clause_node
            ) in node.excepts.items:  # Iterate through uni.Except nodes
                if except_clause_node.gen.doc_ir:
                    except_doc = except_clause_node.gen.doc_ir
                    if except_doc:
                        parts.append(self.text(" "))  # Space before except
                        parts.append(except_doc)

        # Else body (if TryStmt supports it - uni.TryStmt has else_body: Optional[ElseStmt])
        # Jac grammar for try_stmt doesn't show an `else` block directly, python does.
        # Assuming no `else` for now for Jac `try` based on common Jac patterns.
        # If `node.else_body` exists and is relevant for Jac, it would be handled like `finally`.

        # Handle finally clause (FinallyStmt)
        if node.finally_body and node.finally_body.gen.doc_ir:
            finally_doc = node.finally_body.gen.doc_ir
            if finally_doc:
                parts.append(self.text(" "))  # Space before finally
                parts.append(finally_doc)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_except(self, node: uni.Except) -> None:
        """Generate DocIR for except clauses."""
        parts: list[doc.DocType] = [self.text("except")]

        if node.ex_type and node.ex_type.gen.doc_ir:
            ex_type_doc = node.ex_type.gen.doc_ir
            if ex_type_doc:
                parts.append(self.text(" "))
                parts.append(self.group(ex_type_doc))  # Exception type can be complex

        if node.name and node.name.gen.doc_ir:  # name is Name
            name_doc = node.name.gen.doc_ir
            if name_doc:
                parts.append(self.text(" as "))
                parts.append(name_doc)

        parts.append(self.text(" {"))
        body_content_parts: list[doc.DocType] = []
        if node.body and node.body.items:  # body is SubNodeList[CodeBlockStmt]
            for item in node.body.items:
                if item.gen.doc_ir:
                    item_doc = item.gen.doc_ir
                    if item_doc:
                        body_content_parts.append(item_doc)
                        body_content_parts.append(self.hard_line())
            if body_content_parts and isinstance(body_content_parts[-1], doc.Line):
                body_content_parts.pop()

        if body_content_parts:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(body_content_parts)])
                )
            )
            parts.append(self.hard_line())
        else:
            parts.append(self.line())
        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_finally_stmt(self, node: uni.FinallyStmt) -> None:
        """Generate DocIR for finally statements."""
        parts: list[doc.DocType] = [self.text("finally")]

        parts.append(self.text(" {"))
        body_content_parts: list[doc.DocType] = []
        if node.body and node.body.items:  # body is SubNodeList[CodeBlockStmt]
            for item in node.body.items:
                if item.gen.doc_ir:
                    item_doc = item.gen.doc_ir
                    if item_doc:
                        body_content_parts.append(item_doc)
                        body_content_parts.append(self.hard_line())
            if body_content_parts and isinstance(body_content_parts[-1], doc.Line):
                body_content_parts.pop()

        if body_content_parts:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(body_content_parts)])
                )
            )
            parts.append(self.hard_line())
        else:
            parts.append(self.line())
        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_tuple_val(self, node: uni.TupleVal) -> None:
        """Generate DocIR for tuple values."""
        parts: list[doc.DocType] = [self.text("(")]

        if node.values and node.values.items and node.values.gen.doc_ir:
            processed_values_doc = node.values.gen.doc_ir
            if not (
                isinstance(processed_values_doc, doc.Concat)
                and not processed_values_doc.parts
            ):
                parts.append(
                    self.indent(self.concat([self.tight_line(), processed_values_doc]))
                )

                # Handle trailing comma for single-element tuple
                if len(node.values.items) == 1:
                    parts.append(self.text(","))

                parts.append(self.tight_line())  # soft line before closing ')'

        parts.append(self.text(")"))
        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_multi_string(self, node: uni.MultiString) -> None:
        """Generate DocIR for multiline strings."""
        parts: list[doc.DocType] = []

        for string in node.strings:
            if string.gen.doc_ir:
                parts.append(string.gen.doc_ir)
                parts.append(self.hard_line())

        if parts and isinstance(parts[-1], doc.Line):
            parts.pop()  # Remove trailing line

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_set_val(self, node: uni.SetVal) -> None:
        """Generate DocIR for set values."""
        parts: list[doc.DocType] = [self.text("{")]

        if (
            node.values
            and node.values.items
            and hasattr(node.values, "gen")
            and node.values.gen.doc_ir
        ):
            values_doc = node.values.gen.doc_ir
            if not (isinstance(values_doc, doc.Concat) and not values_doc.parts):
                parts.append(
                    self.indent(self.concat([self.line(), values_doc]))  # soft line
                )
                parts.append(self.line())  # soft line before closing '}'

        parts.append(self.text("}"))
        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_special_var_ref(self, node: uni.SpecialVarRef) -> None:
        """Generate DocIR for special variable references."""
        node.gen.doc_ir = self.text(node.value)

    def exit_bool(self, node: uni.Bool) -> None:
        """Generate DocIR for boolean values."""
        node.gen.doc_ir = self.text(node.value)

    def exit_null(self, node: uni.Null) -> None:
        """Generate DocIR for null values."""
        node.gen.doc_ir = self.text(node.value)

    def exit_ellipsis(self, node: uni.Ellipsis) -> None:
        """Generate DocIR for ellipsis."""
        node.gen.doc_ir = self.text(node.value)

    def exit_with_stmt(self, node: uni.WithStmt) -> None:
        """Generate DocIR for with statements."""
        parts: list[doc.DocType] = [self.text("with ")]

        # Handle expressions
        if node.exprs:
            expr_parts: list[doc.DocType] = []
            for expr in node.exprs.items:
                if expr.gen.doc_ir:
                    expr_parts.append(expr.gen.doc_ir)
            parts.append(self.join(self.text(", "), expr_parts))

        # Body
        parts.append(self.text(" "))
        parts.append(self.text("{"))

        if node.body and node.body.gen.doc_ir:
            body_content = node.body.gen.doc_ir
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_list_compr(self, node: uni.ListCompr) -> None:
        """Generate DocIR for list comprehensions."""
        parts: list[doc.DocType] = [self.text("[")]

        # Output expression
        if node.out_expr and node.out_expr.gen.doc_ir:
            parts.append(node.out_expr.gen.doc_ir)
            parts.append(self.text(" "))

        # Comprehension clauses
        for compr in node.compr:
            if compr.gen.doc_ir:
                parts.append(compr.gen.doc_ir)
                parts.append(self.text(" "))

        if parts and isinstance(parts[-1], doc.Text) and parts[-1].text == " ":
            parts.pop()  # Remove trailing space

        parts.append(self.text("]"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_inner_compr(self, node: uni.InnerCompr) -> None:
        """Generate DocIR for inner comprehension clauses."""
        parts: list[doc.DocType] = []

        if node.is_async:
            parts.append(self.text("async "))

        parts.append(self.text("for "))

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir)

        parts.append(self.text(" in "))

        if node.collection and node.collection.gen.doc_ir:
            parts.append(node.collection.gen.doc_ir)

        # Conditionals
        if node.conditional:
            for cond in node.conditional:
                if cond.gen.doc_ir:
                    parts.append(self.text(" if "))
                    parts.append(cond.gen.doc_ir)

        node.gen.doc_ir = self.concat(parts)

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
                        parts.append(part.gen.doc_ir)
                    parts.append(self.text("}"))

        parts.append(self.text('"'))

        node.gen.doc_ir = self.concat(parts)

    def exit_if_else_expr(self, node: uni.IfElseExpr) -> None:
        """Generate DocIR for conditional expressions."""
        parts: list[doc.DocType] = []

        if node.value and node.value.gen.doc_ir:
            val_doc = node.value.gen.doc_ir
            if val_doc:
                parts.append(val_doc)

        parts.append(self.line())  # Potential break
        parts.append(self.text("if"))
        parts.append(self.text(" "))

        if node.condition and node.condition.gen.doc_ir:
            cond_doc = node.condition.gen.doc_ir
            if cond_doc:
                parts.append(cond_doc)

        parts.append(self.line())  # Potential break
        parts.append(self.text("else"))
        parts.append(self.text(" "))

        if node.else_value and node.else_value.gen.doc_ir:
            else_val_doc = node.else_value.gen.doc_ir
            if else_val_doc:
                parts.append(else_val_doc)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_bool_expr(self, node: uni.BoolExpr) -> None:
        """Generate DocIR for boolean expressions (and/or)."""
        parts: list[doc.DocType] = []
        op_str = node.op.value  # op is Token (KW_AND or KW_OR)

        for i, value_node in enumerate(node.values):
            if value_node.gen.doc_ir:
                value_doc = value_node.gen.doc_ir
                if value_doc:
                    parts.append(value_doc)

            if i < len(node.values) - 1:
                parts.append(self.line())  # Potential break + space
                parts.append(self.text(op_str))
                parts.append(self.text(" "))  # Space after operator

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_unary_expr(self, node: uni.UnaryExpr) -> None:
        """Generate DocIR for unary expressions."""
        parts: list[doc.DocType] = []
        op_val = node.op.value  # op is Token

        if op_val in ["-", "~", "+"]:  # Typically no space after these
            parts.append(self.text(op_val))
            if node.operand and node.operand.gen.doc_ir:
                operand_doc = node.operand.gen.doc_ir
                if operand_doc:
                    parts.append(operand_doc)
        elif op_val == "not":  # Space after "not"
            parts.append(self.text("not"))
            if node.operand and node.operand.gen.doc_ir:
                operand_doc = node.operand.gen.doc_ir
                if operand_doc:
                    parts.append(self.text(" "))  # Space before operand
                    parts.append(operand_doc)
        else:  # Default case, might include other unary ops like `await` (handled separately) or custom ones
            parts.append(self.text(op_val))
            if node.operand and node.operand.gen.doc_ir:
                operand_doc = node.operand.gen.doc_ir
                if operand_doc:
                    parts.append(self.text(" "))  # Space before operand
                    parts.append(operand_doc)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_lambda_expr(self, node: uni.LambdaExpr) -> None:
        """Generate DocIR for lambda expressions."""
        parts: list[doc.DocType] = [self.text("lambda")]

        # Signature (params and/or return type)
        if node.signature and node.signature.gen.doc_ir:
            sig_doc = node.signature.gen.doc_ir
            if sig_doc:
                if not (
                    isinstance(sig_doc, doc.Text) and sig_doc.text == "()"
                ):  # Avoid space for lambda () -> ...
                    parts.append(self.text(" "))
                parts.append(sig_doc)

        # Colon before body
        # The colon should be separated from the signature by a space,
        # and from the body by a space, or a break if the body is multiline.
        parts.append(self.text(":"))

        # Body of the lambda
        if node.body and node.body.gen.doc_ir:
            body_doc = node.body.gen.doc_ir
            if body_doc:
                # Indent the body if it breaks. Break before the body.
                parts.append(self.indent(self.concat([self.line(), body_doc])))

        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_edge_ref_trailer(self, node: uni.EdgeRefTrailer) -> None:
        """Generate DocIR for edge reference trailers."""
        parts: list[doc.DocType] = []

        for kid in node.kid:
            if kid.gen.doc_ir and kid.gen.doc_ir:  # check kid.gen.doc_ir is not empty
                parts.append(kid.gen.doc_ir)

        node.gen.doc_ir = self.concat(parts)

    def exit_edge_op_ref(self, node: uni.EdgeOpRef) -> None:
        """Generate DocIR for edge operation references."""
        parts: list[doc.DocType] = []

        for kid in node.kid:
            if kid.gen.doc_ir and kid.gen.doc_ir:  # check kid.gen.doc_ir is not empty
                parts.append(kid.gen.doc_ir)

        node.gen.doc_ir = self.concat(parts)

    def exit_index_slice(self, node: uni.IndexSlice) -> None:
        """Generate DocIR for index slices."""
        parts: list[doc.DocType] = [self.text("[")]

        if node.slices and len(node.slices) > 0:
            slice_parts: list[doc.DocType] = []

            for slice_item in node.slices:
                item_parts: list[doc.DocType] = []

                # Start
                if slice_item.start and slice_item.start.gen.doc_ir:
                    item_parts.append(slice_item.start.gen.doc_ir)

                # Only add colon for range slices
                if node.is_range:
                    item_parts.append(self.text(":"))

                    # Stop
                    if slice_item.stop and slice_item.stop.gen.doc_ir:
                        item_parts.append(slice_item.stop.gen.doc_ir)

                    # Step
                    if slice_item.step:
                        item_parts.append(self.text(":"))
                        if slice_item.step.gen.doc_ir:
                            item_parts.append(slice_item.step.gen.doc_ir)

                slice_parts.append(self.concat(item_parts))

            # Join multiple slices with commas
            if len(slice_parts) > 1:
                parts.append(self.join(self.text(", "), slice_parts))
            else:
                parts.append(slice_parts[0])

        parts.append(self.text("]"))

        node.gen.doc_ir = self.concat(parts)

    def exit_gen_compr(self, node: uni.GenCompr) -> None:
        """Generate DocIR for generator comprehensions."""
        parts: list[doc.DocType] = [self.text("(")]

        # Output expression
        if node.out_expr and node.out_expr.gen.doc_ir:
            parts.append(node.out_expr.gen.doc_ir)
            parts.append(self.text(" "))

        # Comprehension clauses
        for compr in node.compr:
            if compr.gen.doc_ir:
                parts.append(compr.gen.doc_ir)
                parts.append(self.text(" "))

        if parts and isinstance(parts[-1], doc.Text) and parts[-1].text == " ":
            parts.pop()  # Remove trailing space

        parts.append(self.text(")"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_set_compr(self, node: uni.SetCompr) -> None:
        """Generate DocIR for set comprehensions."""
        parts: list[doc.DocType] = [self.text("{")]

        # Output expression
        if node.out_expr and node.out_expr.gen.doc_ir:
            parts.append(node.out_expr.gen.doc_ir)
            parts.append(self.text(" "))

        # Comprehension clauses
        for compr in node.compr:
            if compr.gen.doc_ir:
                parts.append(compr.gen.doc_ir)
                parts.append(self.text(" "))

        if parts and isinstance(parts[-1], doc.Text) and parts[-1].text == " ":
            parts.pop()  # Remove trailing space

        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_dict_compr(self, node: uni.DictCompr) -> None:
        """Generate DocIR for dictionary comprehensions."""
        parts: list[doc.DocType] = [self.text("{")]

        # Key-value pair
        if node.kv_pair and node.kv_pair.gen.doc_ir:
            parts.append(node.kv_pair.gen.doc_ir)
            parts.append(self.text(" "))

        # Comprehension clauses
        for compr in node.compr:
            if compr.gen.doc_ir:
                parts.append(compr.gen.doc_ir)
                parts.append(self.text(" "))

        if parts and isinstance(parts[-1], doc.Text) and parts[-1].text == " ":
            parts.pop()  # Remove trailing space

        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_k_w_pair(self, node: uni.KWPair) -> None:
        """Generate DocIR for keyword arguments."""
        parts: list[doc.DocType] = []

        if node.key:
            parts.append(self.text(node.key.unparse()))
            parts.append(self.text("="))
            if node.value and node.value.gen.doc_ir:
                parts.append(node.value.gen.doc_ir)
        else:
            parts.append(self.text("**"))
            if node.value and node.value.gen.doc_ir:
                parts.append(node.value.gen.doc_ir)

        node.gen.doc_ir = self.concat(parts)

    def exit_await_expr(self, node: uni.AwaitExpr) -> None:
        """Generate DocIR for await expressions."""
        parts: list[doc.DocType] = [self.text("await ")]

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir)

        node.gen.doc_ir = self.concat(parts)

    def exit_yield_expr(self, node: uni.YieldExpr) -> None:
        """Generate DocIR for yield expressions."""
        parts: list[doc.DocType] = [self.text("yield")]

        if node.with_from:
            parts.append(self.text(" from"))

        if node.expr and node.expr.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(node.expr.gen.doc_ir)

        node.gen.doc_ir = self.concat(parts)

    def exit_ctrl_stmt(self, node: uni.CtrlStmt) -> None:
        """Generate DocIR for control statements (break, continue)."""
        # CtrlStmt does not have an expr attribute as per unitree.py
        node.gen.doc_ir = self.text(f"{node.ctrl.value};")

    def exit_delete_stmt(self, node: uni.DeleteStmt) -> None:
        """Generate DocIR for delete statements."""
        parts: list[doc.DocType] = [self.text("delete ")]

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_disengage_stmt(self, node: uni.DisengageStmt) -> None:
        """Generate DocIR for disengage statements."""
        node.gen.doc_ir = self.text("disengage;")

    def exit_report_stmt(self, node: uni.ReportStmt) -> None:
        """Generate DocIR for report statements."""
        parts: list[doc.DocType] = [self.text("report ")]

        if node.expr and node.expr.gen.doc_ir:
            parts.append(node.expr.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_assert_stmt(self, node: uni.AssertStmt) -> None:
        """Generate DocIR for assert statements."""
        parts: list[doc.DocType] = [self.text("assert ")]

        if node.condition and node.condition.gen.doc_ir:
            parts.append(node.condition.gen.doc_ir)

        # Optional error message
        if node.error_msg and node.error_msg.gen.doc_ir:
            parts.append(self.text(", "))
            parts.append(node.error_msg.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_raise_stmt(self, node: uni.RaiseStmt) -> None:
        """Generate DocIR for raise statements."""
        parts: list[doc.DocType] = [self.text("raise")]

        if node.cause and node.cause.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(node.cause.gen.doc_ir)

        # Optional from expression
        if node.from_target and node.from_target.gen.doc_ir:
            parts.append(self.text(" from "))
            parts.append(node.from_target.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

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
            parts.append(node.access.gen.doc_ir)
            parts.append(self.text(" "))

        # Assignments
        if node.assignments and node.assignments.gen.doc_ir:
            parts.append(node.assignments.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_module_code(self, node: uni.ModuleCode) -> None:
        """Generate DocIR for module code."""
        parts: list[doc.DocType] = []

        if (
            node.body and node.body.gen.doc_ir
        ):  # check node.body.gen.doc_ir is not empty
            parts.append(node.body.gen.doc_ir)

        node.gen.doc_ir = self.concat(parts)

    def exit_global_stmt(self, node: uni.GlobalStmt) -> None:
        """Generate DocIR for global statements."""
        parts: list[doc.DocType] = [self.text("global ")]

        if node.target:
            name_parts: list[doc.DocType] = []
            for name in node.target.items:
                if name.gen.doc_ir:
                    name_parts.append(name.gen.doc_ir)

            parts.append(self.join(self.text(", "), name_parts))

        parts.append(self.text(";"))

        node.gen.doc_ir = self.concat(parts)

    def exit_non_local_stmt(self, node: uni.NonLocalStmt) -> None:
        """Generate DocIR for nonlocal statements."""
        parts: list[doc.DocType] = [self.text("nonlocal ")]

        if node.target:
            name_parts: list[doc.DocType] = []
            for name in node.target.items:
                if name.gen.doc_ir:
                    name_parts.append(name.gen.doc_ir)

            parts.append(self.join(self.text(", "), name_parts))

        parts.append(self.text(";"))

        node.gen.doc_ir = self.concat(parts)

    def exit_visit_stmt(self, node: uni.VisitStmt) -> None:
        """Generate DocIR for visit statements."""
        parts: list[doc.DocType] = [self.text("visit ")]

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir)

        if node.else_body and node.else_body.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(node.else_body.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.concat(parts)

    def exit_ignore_stmt(self, node: uni.IgnoreStmt) -> None:
        """Generate DocIR for ignore statements."""
        parts: list[doc.DocType] = [self.text("ignore")]

        if node.target and node.target.gen.doc_ir:
            parts.append(self.text(" "))
            parts.append(node.target.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.concat(parts)

    def exit_connect_op(self, node: uni.ConnectOp) -> None:
        """Generate DocIR for connect operator."""
        parts: list[doc.DocType] = []

        if node.edge_dir == uni.EdgeDir.OUT:
            parts.append(self.text("-->"))
        elif node.edge_dir == uni.EdgeDir.IN:
            parts.append(self.text("<--"))
        elif node.edge_dir == uni.EdgeDir.ANY:
            parts.append(self.text("<-->"))

        node.gen.doc_ir = self.concat(parts)

    def exit_disconnect_op(self, node: uni.DisconnectOp) -> None:
        """Generate DocIR for disconnect operator."""
        parts: list[doc.DocType] = []

        if node.edge_spec and node.edge_spec.edge_dir == uni.EdgeDir.OUT:
            parts.append(self.text("-/>"))
        elif node.edge_spec and node.edge_spec.edge_dir == uni.EdgeDir.IN:
            parts.append(self.text("</-"))
        elif node.edge_spec and node.edge_spec.edge_dir == uni.EdgeDir.ANY:
            parts.append(self.text("</>"))

        node.gen.doc_ir = self.concat(parts)

    def exit_compare_expr(self, node: uni.CompareExpr) -> None:
        """Generate DocIR for comparison expressions."""
        parts: list[doc.DocType] = []

        # Left operand
        if node.left and node.left.gen.doc_ir:
            left_doc = node.left.gen.doc_ir
            if left_doc:
                parts.append(left_doc)

        # Add operators and right operands, allowing breaks before each operator
        for i, right_operand_node in enumerate(node.rights):
            if i < len(node.ops) and node.ops[i]:  # node.ops[i] is Token
                op_str = node.ops[i].value
                parts.append(self.line())  # Potential break + space
                parts.append(self.text(op_str))
                parts.append(self.text(" "))  # Space after operator

            if right_operand_node.gen.doc_ir:
                right_doc = right_operand_node.gen.doc_ir
                if right_doc:
                    parts.append(right_doc)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_atom_unit(self, node: uni.AtomUnit) -> None:
        """Generate DocIR for atom units (parenthesized expressions)."""
        parts: list[doc.DocType] = [self.text("(")]

        if node.value and node.value.gen.doc_ir:
            parts.append(node.value.gen.doc_ir)

        parts.append(self.text(")"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_expr_as_item(self, node: uni.ExprAsItem) -> None:
        """Generate DocIR for expression as item nodes."""
        parts: list[doc.DocType] = []

        if node.expr and node.expr.gen.doc_ir:
            parts.append(node.expr.gen.doc_ir)

        if node.alias and node.alias.gen.doc_ir:
            parts.append(self.text(" as "))
            parts.append(node.alias.gen.doc_ir)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_filter_compr(self, node: uni.FilterCompr) -> None:
        """Generate DocIR for filter comprehensions."""
        parts: list[doc.DocType] = []

        if (
            node.f_type and node.f_type.gen.doc_ir
        ):  # node.f_type is Expr, gen.doc_ir is list[DocType]
            parts.append(self.text("filter "))
            # Ensure we are appending the DocType element, not the list
            parts.append(node.f_type.gen.doc_ir)

        node.gen.doc_ir = self.concat(parts)

    def exit_assign_compr(self, node: uni.AssignCompr) -> None:
        """Generate DocIR for assignment comprehensions."""
        parts: list[doc.DocType] = []

        if node.assigns:
            parts.append(self.text("with "))
            assign_parts: list[doc.DocType] = []
            for assign in node.assigns.items:
                if assign.gen.doc_ir:
                    assign_parts.append(assign.gen.doc_ir)
            parts.append(self.join(self.text(", "), assign_parts))

        node.gen.doc_ir = self.concat(parts)

    def exit_builtin_type(self, node: uni.BuiltinType) -> None:
        """Generate DocIR for builtin type nodes."""
        node.gen.doc_ir = self.text(node.value)

    def exit_py_inline_code(self, node: uni.PyInlineCode) -> None:
        """Generate DocIR for Python inline code blocks."""
        parts: list[doc.DocType] = [  # Ensure parts is list[doc.DocType]
            self.text("::py::"),
            self.hard_line(),
            self.text(node.code.value),
            self.hard_line(),
            self.text("::py::"),
        ]

        node.gen.doc_ir = self.group(self.concat(parts))

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
                node.body.gen.doc_ir
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))
        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_check_stmt(self, node: uni.CheckStmt) -> None:
        """Generate DocIR for check statements."""
        parts: list[doc.DocType] = [self.text("check ")]

        if node.target and node.target.gen.doc_ir:
            parts.append(node.target.gen.doc_ir)

        parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_match_stmt(self, node: uni.MatchStmt) -> None:
        """Generate DocIR for match statements."""
        parts: list[doc.DocType] = [self.text("match ")]

        if node.target and node.target.gen.doc_ir:
            target_doc = (
                node.target.gen.doc_ir
                if isinstance(node.target.gen.doc_ir, list)
                else node.target.gen.doc_ir
            )
            if target_doc:
                parts.append(self.group(target_doc))  # Target can be complex

        parts.append(self.text(" {"))
        case_content_parts: list[doc.DocType] = []
        if node.cases:  # node.cases is list[MatchCase]
            for case_node in node.cases:
                if case_node.gen.doc_ir:
                    case_doc = (
                        case_node.gen.doc_ir
                        if isinstance(case_node.gen.doc_ir, list)
                        else case_node.gen.doc_ir
                    )
                    if case_doc:
                        case_content_parts.append(case_doc)
                        # MatchCase nodes should already include their own hard_line breaks if they are multiline.
                        # Here, we ensure each case is on a new line relative to the previous one.
                        case_content_parts.append(self.hard_line())
            if case_content_parts and isinstance(
                case_content_parts[-1], doc.Line
            ):  # remove last hard_line
                case_content_parts.pop()

        if case_content_parts:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(case_content_parts)])
                )
            )
            parts.append(self.hard_line())
        else:
            parts.append(self.line())
        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_match_case(self, node: uni.MatchCase) -> None:
        """Generate DocIR for match cases."""
        parts: list[doc.DocType] = [self.text("case ")]

        if node.pattern and node.pattern.gen.doc_ir:
            pattern_doc = (
                node.pattern.gen.doc_ir
                if isinstance(node.pattern.gen.doc_ir, list)
                else node.pattern.gen.doc_ir
            )
            if pattern_doc:
                parts.append(self.group(pattern_doc))

        if node.guard and node.guard.gen.doc_ir:
            guard_doc = (
                node.guard.gen.doc_ir
                if isinstance(node.guard.gen.doc_ir, list)
                else node.guard.gen.doc_ir
            )
            if guard_doc:
                parts.append(self.text(" if "))
                parts.append(self.group(guard_doc))

        parts.append(self.text(":"))

        body_stmt_docs: list[doc.DocType] = []
        if node.body:  # node.body is list[CodeBlockStmt]
            for stmt in node.body:
                if stmt.gen.doc_ir:
                    doc_for_stmt = (
                        stmt.gen.doc_ir
                        if isinstance(stmt.gen.doc_ir, list)
                        else stmt.gen.doc_ir
                    )
                    if doc_for_stmt:
                        body_stmt_docs.append(doc_for_stmt)
                        # Each statement in a block usually implies a newline for formatting,
                        # but the statement itself (e.g. ExprStmt) should end with its own ; and newline if appropriate.
                        # Here we ensure separation if multiple statements.
                        body_stmt_docs.append(self.hard_line())
            if body_stmt_docs and isinstance(body_stmt_docs[-1], doc.Line):
                body_stmt_docs.pop()  # Remove trailing hard_line from the last statement

        if body_stmt_docs:
            parts.append(
                self.indent(
                    self.concat([self.hard_line(), self.concat(body_stmt_docs)])
                )
            )
            # No final hard_line here; that's for between MatchCase elements if handled by parent (MatchStmt)
        elif not node.body:  # No body elements at all means `case foo:`
            # Potentially allow a break after colon for empty body `case foo: \n` vs `case foo:`
            # This is subtle. If Jac requires a `pass` or `break` for empty cases, parser should provide it.
            # If it's just `case x:`, adding an indented hard_line might look odd.
            # `self.line()` might be too little. `self.hard_line()` might be too much if followed by another case.
            # Let's assume for now empty body means nothing after colon for this line.
            pass

        # Each MatchCase is a group. If it's complex, it will break across lines.
        # The MatchStmt itself will put hard_lines between MatchCase DocIRs.
        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_match_value(self, node: uni.MatchValue) -> None:
        """Generate DocIR for match value patterns."""
        if node.value and node.value.gen.doc_ir:
            # MatchValue's value is an Expr. It should be groupable if complex.
            val_doc = (
                node.value.gen.doc_ir
                if isinstance(node.value.gen.doc_ir, list)
                else node.value.gen.doc_ir
            )
            node.gen.doc_ir = self.group(val_doc) if val_doc else self.text("")
        else:
            node.gen.doc_ir = self.text("")

    def exit_match_singleton(self, node: uni.MatchSingleton) -> None:
        """Generate DocIR for match singleton patterns."""
        if (
            node.value and node.value.gen.doc_ir
        ):  # value is Bool or Null (which are Tokens)
            val_doc = (
                node.value.gen.doc_ir
                if isinstance(node.value.gen.doc_ir, list)
                else node.value.gen.doc_ir
            )
            node.gen.doc_ir = val_doc if val_doc else self.text("")
        else:
            node.gen.doc_ir = self.text("")

    def exit_match_sequence(self, node: uni.MatchSequence) -> None:
        """Generate DocIR for match sequence patterns."""
        parts: list[doc.DocType] = [self.text("[")]

        if node.values:  # node.values is list[MatchPattern]
            pattern_docs: list[doc.DocType] = []
            for pattern_node in node.values:
                if pattern_node.gen.doc_ir:
                    p_doc = (
                        pattern_node.gen.doc_ir
                        if isinstance(pattern_node.gen.doc_ir, list)
                        else pattern_node.gen.doc_ir
                    )
                    if p_doc:
                        pattern_docs.append(p_doc)

            if pattern_docs:
                joined_patterns = self.join(
                    self.concat([self.text(","), self.line()]), pattern_docs
                )
                if not (
                    isinstance(joined_patterns, doc.Concat)
                    and not joined_patterns.parts
                ):
                    parts.append(
                        self.indent(self.concat([self.line(), joined_patterns]))
                    )
                    parts.append(self.line())  # soft line before closing ']'

        parts.append(self.text("]"))
        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_match_mapping(self, node: uni.MatchMapping) -> None:
        """Generate DocIR for match mapping patterns."""
        parts: list[doc.DocType] = [self.text("{")]

        if node.values:  # node.values is list[MatchKVPair | MatchStar]
            item_docs: list[doc.DocType] = []
            for item_node in node.values:
                if item_node.gen.doc_ir:
                    i_doc = (
                        item_node.gen.doc_ir
                        if isinstance(item_node.gen.doc_ir, list)
                        else item_node.gen.doc_ir
                    )
                    if i_doc:
                        item_docs.append(i_doc)

            if item_docs:
                joined_items = self.join(
                    self.concat([self.text(","), self.line()]), item_docs
                )
                if not (
                    isinstance(joined_items, doc.Concat) and not joined_items.parts
                ):
                    parts.append(self.indent(self.concat([self.line(), joined_items])))
                    parts.append(self.line())  # soft line before closing '}'

        parts.append(self.text("}"))
        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_match_or(self, node: uni.MatchOr) -> None:
        """Generate DocIR for match OR patterns."""
        pattern_docs: list[doc.DocType] = []
        if node.patterns:  # list[MatchPattern]
            for pattern_node in node.patterns:
                if pattern_node.gen.doc_ir:
                    p_doc = (
                        pattern_node.gen.doc_ir
                        if isinstance(pattern_node.gen.doc_ir, list)
                        else pattern_node.gen.doc_ir
                    )
                    if p_doc:
                        pattern_docs.append(
                            self.group(p_doc)
                        )  # Each pattern can be complex

        if pattern_docs:
            # Join with " | " allowing breaks before |
            # self.line() will be a space if flat, newline if breaks.
            separator = self.concat([self.text(" "), self.line(), self.text("| ")])
            node.gen.doc_ir = self.group(self.join(separator, pattern_docs))
        else:
            node.gen.doc_ir = self.text("")

    def exit_match_as(self, node: uni.MatchAs) -> None:
        """Generate DocIR for match AS patterns."""
        parts: list[doc.DocType] = []

        pattern_doc_present = False
        if node.pattern and node.pattern.gen.doc_ir:
            pattern_doc = node.pattern.gen.doc_ir
            if pattern_doc:
                parts.append(self.group(pattern_doc))  # Pattern can be complex
                pattern_doc_present = True

        if node.name and node.name.sym_name:  # name is NameAtom (Token)
            if pattern_doc_present:
                parts.append(self.text(" as "))
            # node.name.gen.doc_ir should exist if sym_name exists and exit_name was called
            name_doc = (
                node.name.gen.doc_ir
                if node.name.gen.doc_ir
                else self.text(node.name.sym_name)
            )
            if name_doc:
                parts.append(name_doc)

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_match_wild(self, node: uni.MatchWild) -> None:
        """Generate DocIR for match wildcard patterns."""
        node.gen.doc_ir = self.text("_")

    def exit_match_star(self, node: uni.MatchStar) -> None:
        """Generate DocIR for match star patterns (e.g., *args, **kwargs)."""
        prefix = "*" if node.is_list else "**"
        parts: list[doc.DocType] = [self.text(prefix)]
        if node.name and node.name.gen.doc_ir:  # name is NameAtom
            name_doc = node.name.gen.doc_ir
            if name_doc:
                parts.append(name_doc)
        node.gen.doc_ir = self.concat(parts)

    def exit_match_k_v_pair(self, node: uni.MatchKVPair) -> None:
        """Generate DocIR for match key-value pairs."""
        parts: list[doc.DocType] = []

        if (
            node.key and node.key.gen.doc_ir
        ):  # key is MatchPattern | NameAtom | AtomExpr
            key_doc = (
                node.key.gen.doc_ir
                if isinstance(node.key.gen.doc_ir, list)
                else node.key.gen.doc_ir
            )
            if key_doc:
                parts.append(key_doc)  # Key itself could be a group

        parts.append(self.text(": "))  # Space after colon

        if node.value and node.value.gen.doc_ir:  # value is MatchPattern
            value_doc = (
                node.value.gen.doc_ir
                if isinstance(node.value.gen.doc_ir, list)
                else node.value.gen.doc_ir
            )
            if value_doc:
                # Value pattern could be complex, group it and allow indent if it breaks
                parts.append(
                    self.group(self.indent(self.concat([self.line(), value_doc])))
                )

        node.gen.doc_ir = self.group(self.concat(parts))  # The KVPair is a group

    def exit_match_arch(self, node: uni.MatchArch) -> None:
        """Generate DocIR for match architecture patterns."""
        parts: list[doc.DocType] = []

        if node.name and node.name.gen.doc_ir:  # name is AtomTrailer | NameAtom
            name_doc = (
                node.name.gen.doc_ir
                if isinstance(node.name.gen.doc_ir, list)
                else node.name.gen.doc_ir
            )
            if name_doc:
                parts.append(name_doc)

        parts.append(self.text("("))

        arg_docs_present = False
        # Arg patterns (SubNodeList[MatchPattern])
        if (
            node.arg_patterns
            and node.arg_patterns.items
            and hasattr(node.arg_patterns, "gen")
            and node.arg_patterns.gen.doc_ir
        ):
            arg_patterns_doc = node.arg_patterns.gen.doc_ir
            if not (
                isinstance(arg_patterns_doc, doc.Concat) and not arg_patterns_doc.parts
            ):
                parts.append(
                    self.indent(self.concat([self.tight_line(), arg_patterns_doc]))
                )
                arg_docs_present = True

        # Keyword patterns (SubNodeList[MatchKVPair])
        if (
            node.kw_patterns
            and node.kw_patterns.items
            and hasattr(node.kw_patterns, "gen")
            and node.kw_patterns.gen.doc_ir
        ):
            kw_patterns_doc = node.kw_patterns.gen.doc_ir
            if not (
                isinstance(kw_patterns_doc, doc.Concat) and not kw_patterns_doc.parts
            ):
                if arg_docs_present:  # Add comma if args were also present
                    # This comma should be part of the indented block if args broke
                    # If args didn't break, it should be ", kw..."
                    # This is tricky. Simplest for now: always add comma before kw_patterns if args existed.
                    parts.append(self.text(","))
                    parts.append(self.line())  # allow break after comma

                # Check if kw_patterns_doc itself needs indenting (if it contains multiple items that could break)
                # For now, assume SubNodeList's output is already suitable for direct inclusion within the indent block.
                if not arg_docs_present:  # Need to start indent if args were not there
                    parts.append(
                        self.indent(self.concat([self.tight_line(), kw_patterns_doc]))
                    )
                else:  # Already in an indent potentially, just append
                    parts.append(kw_patterns_doc)
                arg_docs_present = True  # update flag as we now have content

        if arg_docs_present:
            parts.append(self.tight_line())  # soft line before closing ')'

        parts.append(self.text(")"))
        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_enum(self, node: uni.Enum) -> None:
        """Generate DocIR for enum declarations."""
        parts: list[doc.DocType] = []

        # Handle decorators
        if node.decorators and node.decorators.items:
            decorator_docs: list[doc.DocType] = []
            for decorator_node in node.decorators.items:
                if decorator_node.gen.doc_ir:
                    decorator_doc = (
                        decorator_node.gen.doc_ir
                        if isinstance(decorator_node.gen.doc_ir, list)
                        else decorator_node.gen.doc_ir
                    )
                    if decorator_doc:
                        decorator_docs.append(decorator_doc)
                        decorator_docs.append(self.hard_line())
            if decorator_docs:
                parts.extend(decorator_docs)

        # Enum declaration: enum <name>
        header_parts: list[doc.DocType] = [self.text("enum")]
        if node.name and node.name.gen.doc_ir:
            header_parts.append(self.text(" "))
            name_doc = (
                node.name.gen.doc_ir
                if isinstance(node.name.gen.doc_ir, list)
                else node.name.gen.doc_ir
            )
            if name_doc:
                header_parts.append(name_doc)

        # Inheritance: : base1, base2 (Note: unitree.Enum.normalize shows : base_classes :)
        # My current exit_architype uses just ": base_classes". Let's be consistent for now.
        if (
            node.base_classes
            and node.base_classes.items
            and hasattr(node.base_classes, "gen")
            and node.base_classes.gen.doc_ir
        ):
            base_classes_doc = node.base_classes.gen.doc_ir
            if not (
                isinstance(base_classes_doc, doc.Concat) and not base_classes_doc.parts
            ):
                header_parts.append(self.text(": "))
                header_parts.append(base_classes_doc)
                # unitree.Enum.normalize has a second colon after base_classes if present.
                # header_parts.append(self.text(" :")) # If strictly following that normalize

        parts.append(self.group(self.concat(header_parts)))

        # Handle body: { members... } or ; for impl
        if node.body:  # body is SubNodeList[Assignment] | ImplDef
            if isinstance(
                node.body, uni.ImplDef
            ):  # Forward declared enum with later impl
                parts.append(self.text(";"))  # enum MyEnum; (impl later)
                # The ImplDef itself will be formatted separately when visited.
            elif isinstance(
                node.body, uni.SubNodeList
            ):  # Assumed to be SubNodeList[Assignment]
                parts.append(self.text(" {"))
                member_content_parts: list[doc.DocType] = []
                if node.body.items:
                    for item_node in node.body.items:  # item_node should be Assignment
                        if item_node.gen.doc_ir:
                            item_doc = item_node.gen.doc_ir
                            if item_doc:
                                member_content_parts.append(item_doc)
                                # Enum members in Jac are typically one per line, like Python.
                                # Assignment node (if is_enum_stmt=True) won't add a semicolon.
                                # Python enum members can have trailing commas. Jac style TBD.
                                # For now, just hard_line after each member.
                                member_content_parts.append(self.hard_line())
                    if member_content_parts and isinstance(
                        member_content_parts[-1], doc.Line
                    ):
                        member_content_parts.pop()  # remove last hard_line

                if member_content_parts:
                    parts.append(
                        self.indent(
                            self.concat(
                                [self.hard_line(), self.concat(member_content_parts)]
                            )
                        )
                    )
                    parts.append(self.hard_line())
                else:
                    parts.append(self.line())
                parts.append(self.text("}"))
                parts.append(
                    self.text(";")
                )  # Enums defined with {} also end with ; in Jac
        else:  # No body, e.g., enum MyEnum;
            parts.append(self.text(";"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_sub_tag(self, node: uni.SubTag) -> None:
        """Generate DocIR for sub-tag nodes."""
        parts: list[doc.DocType] = []

        if node.tag and node.tag.gen.doc_ir:
            parts.append(node.tag.gen.doc_ir)

        node.gen.doc_ir = self.concat(parts)

    def exit_sub_node_list(self, node: uni.SubNodeList) -> None:
        """Generate DocIR for a SubNodeList.

        It joins the DocIR of its items using the specified delimiter if present.
        The result is a single DocType (usually a Concat).
        Enclosing brackets/parentheses and overall list indentation are typically
        handled by the parent node consuming this SubNodeList's DocIR.
        """
        item_docs: list[doc.DocType] = []
        if node.items:
            for item in node.items:
                item_docs.append(item.gen.doc_ir)

        if not item_docs:
            node.gen.doc_ir = self.concat([])  # Empty sequence
            return

        separator: doc.DocType
        if node.delim == uni.Tok.COMMA:
            separator = self.concat([self.text(","), self.line()])
        elif node.delim == uni.Tok.DOT:
            separator = self.concat([self.text("."), self.line()])
        elif node.delim is None:
            separator = self.line()
        else:
            # Try to use the delimiter's token value if it's a known token
            try:
                # Assuming DELIM_MAP or node.delim.value gives the string for the token
                delim_text = uni.DELIM_MAP.get(node.delim, node.delim.value)
                separator = self.concat([self.text(delim_text), self.line()])
            except AttributeError:
                # Fallback if delim is not a simple token with a value
                separator = self.line()  # Default to a space or break

        joined_items = self.join(separator, item_docs)
        node.gen.doc_ir = joined_items

    def exit_token(self, node: uni.Token) -> None:
        """Generate DocIR for tokens."""
        node.gen.doc_ir = self.text(node.value)

    def exit_semi(self, node: uni.Semi) -> None:
        """Generate DocIR for semicolons."""
        node.gen.doc_ir = self.text(node.value)

    def exit_comment_token(self, node: uni.CommentToken) -> None:
        """Generate DocIR for comment tokens."""
        if node.is_inline:
            node.gen.doc_ir = self.text(node.value)
        else:
            node.gen.doc_ir = self.group(
                self.concat([self.text(node.value), self.hard_line()])
            )

    def exit_impl_def(self, node: uni.ImplDef) -> None:
        """Generate DocIR for implementation definitions."""
        parts: list[doc.DocType] = []

        if node.target and node.target.items:
            # Assuming the first item in target is the relevant one for now
            target_item = node.target.items[0]
            if target_item.gen.doc_ir:
                parts.append(
                    target_item.gen.doc_ir
                    if isinstance(target_item.gen.doc_ir, list)
                    else target_item.gen.doc_ir
                )

        parts.append(self.text(" {"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_event_signature(self, node: uni.EventSignature) -> None:
        """Generate DocIR for event signatures."""
        parts: list[doc.DocType] = []

        if node.event and node.event.gen.doc_ir:
            parts.append(node.event.gen.doc_ir)
        node.gen.doc_ir = self.group(self.concat(parts))

    def exit_typed_ctx_block(self, node: uni.TypedCtxBlock) -> None:
        """Generate DocIR for typed context blocks."""
        parts: list[doc.DocType] = []

        if hasattr(node, "name") and node.name:
            parts.append(self.text(node.name.value))

        if hasattr(node, "type_tag") and node.type_tag and node.type_tag.gen.doc_ir:
            parts.append(self.text(": "))
            type_tag_doc = node.type_tag.gen.doc_ir
            if isinstance(type_tag_doc, list):  # Should be DocType from SubTag
                parts.append(type_tag_doc[0])
            else:
                parts.append(type_tag_doc)

        parts.append(self.text(" {"))

        if node.body and node.body.gen.doc_ir:
            body_content = (
                node.body.gen.doc_ir
                if isinstance(node.body.gen.doc_ir, list)
                else node.body.gen.doc_ir
            )
            parts.append(self.indent(self.concat([self.hard_line(), body_content])))
            parts.append(self.hard_line())

        parts.append(self.text("}"))

        node.gen.doc_ir = self.group(self.concat(parts))

    def print_jac(
        self,
        doc_node: Optional[doc.DocType] = None,
        indent_level: int = 0,
        width_remaining: Optional[int] = None,
        is_broken: bool = False,
    ) -> str:
        """Recursively print a Doc node or a list of Doc nodes."""
        if doc_node is None:
            doc_node = self.ir_in.gen.doc_ir

        if width_remaining is None:
            width_remaining = self.MAX_LINE_LENGTH

        if isinstance(
            doc_node, list
        ):  # This case should ideally not be hit if IR is consistent
            return self.print_jac(
                self.concat(doc_node),
                indent_level,
                width_remaining,
                is_broken,  # Use self.concat
            )
        if isinstance(doc_node, doc.Text):
            return doc_node.text

        elif isinstance(doc_node, doc.Line):
            if is_broken or doc_node.hard:
                return "\n" + " " * (indent_level * self.indent_size)
            elif doc_node.literal:  # literal soft line
                return "\n"
            elif doc_node.tight:
                return ""
            else:  # soft line, not broken
                return " "

        elif isinstance(doc_node, doc.Group):
            # Try to print flat first. For this attempt, the group itself isn't forced to break.
            flat_contents_str = self.print_jac(
                doc_node.contents, indent_level, width_remaining, is_broken=False
            )
            if (
                "\n" not in flat_contents_str
                and len(flat_contents_str) <= width_remaining
            ):
                return flat_contents_str
            else:
                full_width_for_broken_content = self.MAX_LINE_LENGTH - (
                    indent_level * self.indent_size
                )
                return self.print_jac(
                    doc_node.contents,
                    indent_level,
                    full_width_for_broken_content,
                    is_broken=True,
                )

        elif isinstance(doc_node, doc.Indent):
            new_indent_level = indent_level + 1

            width_for_indented_content = self.MAX_LINE_LENGTH - (
                new_indent_level * self.indent_size
            )
            return self.print_jac(
                doc_node.contents,
                new_indent_level,
                width_for_indented_content,  # Budget for lines within indent
                is_broken,  # is_broken state propagates
            )

        elif isinstance(doc_node, doc.Concat):
            result = ""
            # current_line_budget is the space left on the current line for the current part.
            current_line_budget = width_remaining

            for part in doc_node.parts:
                part_str = self.print_jac(
                    part, indent_level, current_line_budget, is_broken
                )
                result += part_str

                if "\n" in part_str:
                    # part_str created a newline. The next part starts on a new line.
                    # Its budget is the full width available at this indent level.
                    current_line_budget = self.MAX_LINE_LENGTH - (
                        indent_level * self.indent_size
                    )
                    # Subtract what the *last line* of part_str consumed from this budget.
                    # The characters on the last line after the indent string.
                    indent_str_len = indent_level * self.indent_size
                    last_line_of_part = part_str.splitlines()[-1]

                    content_on_last_line = 0
                    if last_line_of_part.startswith(" " * indent_str_len):
                        content_on_last_line = len(last_line_of_part) - indent_str_len
                    else:  # It was a line not starting with the full indent (e.g. literal \n)
                        content_on_last_line = len(last_line_of_part)

                    current_line_budget -= content_on_last_line
                else:
                    # part_str stayed on the same line. Reduce budget for next part on this line.
                    current_line_budget -= len(part_str)

                if current_line_budget < 0:  # Ensure budget isn't negative
                    current_line_budget = 0
            return result

        elif isinstance(doc_node, doc.IfBreak):
            if is_broken:
                return self.print_jac(
                    doc_node.break_contents, indent_level, width_remaining, is_broken
                )
            else:
                return self.print_jac(
                    doc_node.flat_contents, indent_level, width_remaining, is_broken
                )

        elif isinstance(doc_node, doc.Align):
            align_spaces = doc_node.n if doc_node.n is not None else self.indent_size
            # effective_total_indent_spaces_for_children = (
            #     indent_level * self.indent_size
            # ) + align_spaces
            child_indent_level_for_align = indent_level + (
                align_spaces // self.indent_size
            )

            child_width_budget = width_remaining - align_spaces
            if child_width_budget < 0:
                child_width_budget = 0

            return self.print_jac(
                doc_node.contents,
                child_indent_level_for_align,  # Approximated level for Lines inside
                child_width_budget,  # Budget for content on first line
                is_broken,
            )
        else:
            raise ValueError(f"Unknown DocType: {type(doc_node)}")

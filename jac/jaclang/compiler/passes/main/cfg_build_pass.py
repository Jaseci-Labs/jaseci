"""Control flow graph build pass.

This pass builds the control flow graph for the Jac program by filling in  details in UniBasicBlock.
These nodes will be linked together in the CFG pass.
"""

# from typing import TypeVar

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import AstPass


class CFGBuildPass(AstPass):
    """Jac Symbol table build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.while_loop_stack: list[list[uni.UniBasicBlock]] = []
        self.for_loop_stack: list[list[uni.UniBasicBlock]] = []
        self.function_call_stack: list[list[uni.UniBasicBlock]] = []

    def push_loop_stack(self, loop_header: uni.UniBasicBlock) -> None:
        """Push loop stack."""
        if isinstance(loop_header, uni.WhileStmt) and len(self.while_loop_stack) > 0:
            self.while_loop_stack.append([loop_header])
        elif (
            isinstance(loop_header, (uni.InForStmt, uni.IterForStmt))
            and len(self.for_loop_stack) > 0
        ):
            self.for_loop_stack.append([loop_header])

    def pop_loop_stack(self, node: uni.UniBasicBlock) -> None:
        """Pop loop stack."""
        if isinstance(node, uni.WhileStmt) and len(self.while_loop_stack) > 0:
            self.while_loop_stack.pop()
        elif (
            isinstance(node, (uni.InForStmt, uni.IterForStmt))
            and len(self.for_loop_stack) > 0
        ):
            self.for_loop_stack.pop()

    def top_loop_stack(self) -> list[uni.UniBasicBlock]:
        """Get top loop stack."""
        if len(self.while_loop_stack) > 0:
            return self.while_loop_stack[-1]
        else:
            return []

    def get_parent_bb(self, node: uni.UniNode) -> uni.UniBasicBlock | None:
        """Get parent basic block."""
        if not isinstance(node, uni.Module):
            parent_bb = node.parent_of_type(uni.UniBasicBlock)
            return parent_bb
        else:
            return None

    def link_bbs(self, source: uni.UniBasicBlock, target: uni.UniBasicBlock) -> None:
        """Link basic blocks."""
        if source and target:
            source.control_out_bbs.append(target)
            target.control_in_bbs.append(source)

    def sync_bbs(self, source: uni.UniBasicBlock, target: uni.UniBasicBlock) -> None:
        """Sync nodes."""
        if source and target:
            target.bb_stmts = source.bb_stmts
            target.control_in_bbs = source.control_in_bbs
            target.control_out_bbs = source.control_out_bbs

    def enter_node(self, node: uni.UniNode) -> None:
        """Enter UniBasicBlock nodes."""
        if isinstance(node, uni.UniBasicBlock):
            parent_bb = self.get_parent_bb(node)
            if isinstance(parent_bb, uni.UniBasicBlock):
                if isinstance(parent_bb, uni.IfStmt):
                    node.bb_stmts.append(node)
                    self.link_bbs(parent_bb, node)
                elif isinstance(node, (uni.InForStmt, uni.IterForStmt)):
                    self.push_loop_stack(parent_bb)
                    node.bb_stmts.append(node)
                    self.link_bbs(parent_bb, node)
                elif isinstance(parent_bb, uni.WhileStmt):
                    node.bb_stmts.append(node)
                    self.link_bbs(parent_bb, node)
                    if self.while_loop_stack:
                        self.while_loop_stack[-1].append(node)
                elif isinstance(parent_bb, (uni.InForStmt, uni.IterForStmt)):
                    node.bb_stmts.append(node)
                    self.link_bbs(parent_bb, node)
                    if self.for_loop_stack:
                        self.for_loop_stack[-1].append(node)
                elif self.while_loop_stack or self.for_loop_stack:
                    if self.for_loop_stack:
                        self.for_loop_stack[-1][-1] = node
                    if self.while_loop_stack:
                        self.while_loop_stack[-1][-1] = node
                    parent_bb.bb_stmts.append(node)
                    self.sync_bbs(parent_bb, node)
                else:
                    parent_bb.bb_stmts.append(node)
                    self.sync_bbs(parent_bb, node)
                # with open("output.txt", "a") as file:
                #     for obj in node.bb_stmts:
                #         file.write(str(obj.unparse()) + "\n---------------\n")
                #     file.write("=============================\n")

    def exit_while_stmt(self, node: uni.WhileStmt) -> None:
        """Exit while statement."""
        if self.while_loop_stack:
            from_node = self.while_loop_stack[-1][-1]
            self.link_bbs(from_node, node)
            self.pop_loop_stack(node)

    def exit_iter_for_stmt(self, node: uni.IterForStmt) -> None:
        """Exit for statement."""
        if self.for_loop_stack:
            from_node = self.for_loop_stack[-1][-1]
            self.link_bbs(from_node, node)
            self.pop_loop_stack(node)

    def exit_in_for_stmt(self, node: uni.InForStmt) -> None:
        """Exit for statement."""
        if self.for_loop_stack:
            from_node = self.for_loop_stack[-1][-1]
            self.link_bbs(from_node, node)
            self.pop_loop_stack(node)

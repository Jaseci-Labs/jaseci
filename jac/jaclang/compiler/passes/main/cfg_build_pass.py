"""Control flow graph build pass.

This pass builds the control flow graph for the Jac program by filling in  details in UniBasicBlock.
These nodes will be linked together in the CFG pass.
"""

import json

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
        if isinstance(loop_header, uni.WhileStmt):
            self.while_loop_stack.append([loop_header])
        elif isinstance(loop_header, (uni.InForStmt, uni.IterForStmt)):
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

    def get_parent_bb(self, node: uni.UniNode) -> uni.UniBasicBlock | None:
        """Get parent basic block."""
        if not isinstance(node, uni.Module):
            parent_bb = node.parent_of_type(uni.UniBasicBlock)
        return parent_bb

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
        if isinstance(node, uni.UniBasicBlock) and not isinstance(node, uni.Module):
            parent_bb = self.get_parent_bb(node)

            if isinstance(parent_bb, uni.IfStmt) and not isinstance(
                node, (uni.InForStmt, uni.IterForStmt, uni.WhileStmt)
            ):
                node.bb_stmts.append(node)
                self.link_bbs(parent_bb, node)
            elif isinstance(
                node, (uni.InForStmt, uni.IterForStmt, uni.WhileStmt)
            ):  # Loop Header Handling

                self.push_loop_stack(node)
                node.bb_stmts.append(node)

            elif isinstance(parent_bb, (uni.InForStmt, uni.IterForStmt, uni.WhileStmt)):
                node.bb_stmts.append(node)
                self.link_bbs(parent_bb, node)
            elif self.while_loop_stack or self.for_loop_stack:
                if self.for_loop_stack:
                    self.for_loop_stack[-1][-1] = node
                if self.while_loop_stack:
                    self.while_loop_stack[-1][-1] = node
                if parent_bb:
                    parent_bb.bb_stmts.append(node)
                    self.sync_bbs(parent_bb, node)
            else:
                if parent_bb:
                    parent_bb.bb_stmts.append(node)
                    self.sync_bbs(parent_bb, node)

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

    def exit_module(self, node: uni.Module) -> None:
        """After pass."""
        # CFGLinkPass(ir_in=node, prog=self.prog)
        bb_colector_pass = BBColectorPass(ir_in=node, prog=self.prog)
        self.basic_blocks = bb_colector_pass.basic_blocks
        unparsed_blocks = {
            bb_id: {
                "bb_stmts": [bb.unparse() for bb in bb_info["bb_stmts"]],
                "control_in_bbs": [bb.unparse() for bb in bb_info["control_in_bbs"]],
                "control_out_bbs": [bb.unparse() for bb in bb_info["control_out_bbs"]],
            }
            for bb_id, bb_info in self.basic_blocks.items()
        }
        with open(f"basic_blocks_{node.name}.json", "w") as json_file:
            json.dump(unparsed_blocks, json_file, default=str, indent=4)


class CFGLinkPass(AstPass):
    """Link basic blocks."""

    def before_pass(self) -> None:
        """Before pass."""
        self.new_links: list[tuple[uni.UniBasicBlock, uni.UniBasicBlock]] = []

    def get_parent_bb(self, node: uni.UniNode) -> list[uni.UniBasicBlock] | None:
        """Get parent basic block."""
        parent_bb: list[uni.UniBasicBlock] = []  # <-- fix
        if not isinstance(node, uni.Module):
            if isinstance(node.parent, uni.SubNodeList):
                code_block_list = [
                    n for n in node.parent.kid if isinstance(n, uni.UniBasicBlock)
                ]
                for i in range(len(code_block_list)):
                    if (
                        node == code_block_list[i]
                        and node not in code_block_list[i - 1].bb_stmts
                    ):
                        if i != 0:
                            top_parent_bb = code_block_list[i - 1]
                            parent_bb = self.get_end_of_control_flow(top_parent_bb)
                            if len(parent_bb) == 0:

                                parent_bb = [top_parent_bb]

                            return parent_bb

                        else:
                            parent_bb = [node.parent_of_type(uni.UniBasicBlock)]
                    else:
                        parent_bb = (
                            [node.parent_of_type(uni.UniBasicBlock)]
                            if not isinstance(
                                node.parent_of_type(uni.UniBasicBlock), uni.Module
                            )
                            else []
                        )
            else:
                parent_bb = [node.parent_of_type(uni.UniBasicBlock)]
        return parent_bb

    def get_end_of_control_flow(
        self, node: uni.UniBasicBlock
    ) -> list[uni.UniBasicBlock]:
        """Get end of control flow."""
        end_nodes: list[uni.UniBasicBlock] = []
        if isinstance(node, (uni.InForStmt, uni.IterForStmt, uni.WhileStmt)):
            if len(node.control_out_bbs) == 1:
                end_nodes.append(node)
            else:
                end_nodes.extend(self.get_end_of_control_flow(node.control_out_bbs[1]))
        else:

            if len(node.control_out_bbs) > 0:
                for bb in node.control_out_bbs:

                    end_nodes.extend(self.get_end_of_control_flow(bb))
            else:
                end_nodes.append(node)
        return end_nodes

    def enter_node(self, node: uni.UniNode) -> None:
        """Enter UniBasicBlock nodes."""
        if isinstance(node, uni.UniBasicBlock) and not isinstance(node, uni.Module):
            parent_bbs = self.get_parent_bb(node)
            if parent_bbs:
                for parent_bb in parent_bbs:
                    self.new_links.append((parent_bb, node))

    def after_pass(self) -> None:
        """After pass."""
        for source, target in self.new_links:
            source.control_out_bbs.append(target)
            target.control_in_bbs.append(source)


class BBColectorPass(AstPass):
    """Collect basic blocks."""

    def before_pass(self) -> None:
        """Before pass."""
        self.basic_blocks: dict = {}
        self.bb_counter = 0

    def enter_node(self, node: uni.UniNode) -> None:
        """Enter UniBasicBlock nodes."""
        if isinstance(node, uni.UniBasicBlock):
            if self.bb_counter == 0:
                self.basic_blocks[self.bb_counter] = {
                    "bb_stmts": node.bb_stmts,
                    "control_in_bbs": node.control_in_bbs,
                    "control_out_bbs": node.control_out_bbs,
                }
                self.bb_counter += 1
            else:
                for bb_id, bb_info in list(self.basic_blocks.items()):
                    if bb_info["bb_stmts"] == node.bb_stmts:
                        break
                    if bb_id == self.bb_counter - 1:
                        self.basic_blocks[self.bb_counter] = {
                            "bb_stmts": node.bb_stmts,
                            "control_in_bbs": node.control_in_bbs,
                            "control_out_bbs": node.control_out_bbs,
                        }
                        self.bb_counter += 1

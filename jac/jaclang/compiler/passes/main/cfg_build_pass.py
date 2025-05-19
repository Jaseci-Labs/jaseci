"""Control flow graph build pass for the Jac compiler.

This pass constructs a control flow graph (CFG) representation of the program by:
1. Identifying basic blocks (sequences of statements with a single entry and exit point)
2. Establishing control flow relationships between these blocks
3. Tracking loop structures and maintaining proper nesting relationships
4. Building connections between statements that affect control flow (conditionals, loops, etc.)

The CFG provides a foundation for data flow analysis, optimization, and understanding program execution paths.
The pass also includes functionality to coalesce basic blocks and generate visual representations of the CFG.
"""

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass


class CFGBuildPass(UniPass):
    """Jac Symbol table build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.while_loop_stack: list[list[uni.UniCFGNode]] = []
        self.for_loop_stack: list[list[uni.UniCFGNode]] = []
        self.ability_stack: list[list[uni.UniCFGNode]] = []
        self.to_connect: list[uni.UniCFGNode] = []
        self.first_exit: bool = False

    def push_loop_stack(self, loop_header: uni.UniCFGNode) -> None:
        """Push loop stack."""
        if isinstance(loop_header, uni.WhileStmt):
            self.while_loop_stack.append([loop_header])
        elif isinstance(loop_header, (uni.InForStmt, uni.IterForStmt)):
            self.for_loop_stack.append([loop_header])

    def pop_loop_stack(self, node: uni.UniCFGNode) -> None:
        """Pop loop stack."""
        if isinstance(node, uni.WhileStmt) and len(self.while_loop_stack) > 0:
            self.while_loop_stack.pop()
        elif (
            isinstance(node, (uni.InForStmt, uni.IterForStmt))
            and len(self.for_loop_stack) > 0
        ):
            self.for_loop_stack.pop()

    def get_parent_bb_stmt(self, node: uni.UniCFGNode) -> uni.UniCFGNode | None:
        """Get parent basic block."""
        if not isinstance(node, uni.Module):
            try:
                parent_bb_stmt = node.parent_of_type(uni.UniCFGNode)
                return parent_bb_stmt
            except Exception:
                return None
        else:
            return None

    def link_bbs(self, source: uni.UniCFGNode, target: uni.UniCFGNode) -> None:
        """Link basic blocks."""
        if source and target:
            if source.bb_out:
                source.bb_out.append(target)
            else:
                source.bb_out = [target]
            if target.bb_in:
                target.bb_in.append(source)
            else:
                target.bb_in = [source]

    def enter_node(self, node: uni.UniNode) -> None:
        """Enter BasicBlockStmt nodes."""
        if isinstance(node, uni.UniCFGNode) and not isinstance(node, uni.Semi):
            if isinstance(node.parent, uni.SubNodeList) and self.first_exit:
                bb_stmts = [
                    bbs for bbs in node.parent.kid if isinstance(bbs, uni.UniCFGNode)
                ]
                if (
                    node.parent.parent
                    and isinstance(node.parent.parent, uni.Archetype)
                    # and isinstance(node.parent.parent, uni.BasicBlockStmt)
                ):
                    parent_obj = node.parent.parent
                    if parent_obj:
                        self.link_bbs(parent_obj, node)
                elif bb_stmts[0] == node:
                    if (
                        isinstance(node.parent.parent, uni.ModuleCode)
                        and self.to_connect
                    ):
                        for bb in self.to_connect:
                            self.link_bbs(bb, node)
                            self.to_connect.remove(bb)  # if self.to_connect:
                    else:
                        parent_bb = self.get_parent_bb_stmt(node)
                        if parent_bb:
                            self.link_bbs(parent_bb, node)
                elif self.to_connect:
                    to_remove = []
                    for parent in self.to_connect:
                        if isinstance(parent, uni.UniCFGNode):
                            self.link_bbs(parent, node)
                            to_remove.append(parent)
                    for parent in to_remove:
                        self.to_connect.remove(parent)
                else:
                    for i in range(len(bb_stmts)):
                        if bb_stmts[i] == node:
                            parent_bb = bb_stmts[i - 1]
                            self.link_bbs(parent_bb, node)

            else:
                parent_bb = self.get_parent_bb_stmt(node)
                if parent_bb:
                    self.link_bbs(parent_bb, node)
            if isinstance(node, (uni.InForStmt, uni.IterForStmt, uni.WhileStmt)):
                self.push_loop_stack(node)
            else:
                if self.for_loop_stack:
                    self.for_loop_stack[-1].append(node)
                if self.while_loop_stack:
                    self.while_loop_stack[-1].append(node)
            if isinstance(node, uni.Ability):
                self.ability_stack.append([node])
            elif self.ability_stack:
                self.ability_stack[-1].append(node)

    def exit_node(self, node: uni.UniNode) -> None:
        """Exit BasicBlockStmt nodes."""
        if isinstance(node, uni.UniCFGNode) and not isinstance(node, uni.Semi):
            self.first_exit = True
            if not node.bb_out:
                self.to_connect.append(node)
            if (
                isinstance(node, (uni.InForStmt, uni.IterForStmt))
                and self.for_loop_stack
            ):
                for from_node in self.for_loop_stack[-1][1:]:
                    self.link_bbs(from_node, node)
                    if from_node in self.to_connect:
                        self.to_connect.remove(from_node)
                self.pop_loop_stack(node)
                self.to_connect.append(node)
            elif isinstance(node, uni.WhileStmt) and self.while_loop_stack:
                for from_node in self.while_loop_stack[-1][1:]:
                    self.link_bbs(from_node, node)
                    if from_node in self.to_connect:
                        self.to_connect.remove(from_node)
                self.pop_loop_stack(node)
                self.to_connect.append(node)
            elif isinstance(node, uni.Ability) and self.ability_stack:
                for from_node in self.ability_stack[-1][1:]:
                    if from_node in self.to_connect:
                        self.to_connect.remove(from_node)
                self.ability_stack.pop()

    def after_pass(self) -> None:
        """After pass."""
        if self.to_connect:
            for node in self.to_connect:
                if isinstance(node, uni.UniCFGNode):
                    parent_bb = self.get_parent_bb_stmt(node)
                    if parent_bb:
                        self.link_bbs(parent_bb, node)


class CoalesceBBPass(UniPass):
    """Fetch basic blocks."""

    def before_pass(self) -> None:
        """Before pass."""
        self.basic_blocks: dict = {}
        self.bb_counter: int = 0

    def get_bb(self, node: uni.UniCFGNode) -> list[uni.UniCFGNode]:
        """Get basic block."""
        head = node.get_head()
        tail = node.get_tail()
        bb_list: list[uni.UniCFGNode] = []
        if head and tail:
            cur_node = head
            while cur_node != tail:
                if cur_node not in bb_list:
                    bb_list.append(cur_node)
                if cur_node.bb_out:
                    cur_node = cur_node.bb_out[0]
            bb_list.append(tail) if tail not in bb_list else None

        return bb_list

    def enter_node(self, node: uni.UniNode) -> None:
        """Enter BasicBlockStmt nodes."""
        if isinstance(node, uni.UniCFGNode) and not isinstance(node, uni.Semi):
            tail = node.get_tail()
            bb = self.get_bb(node)
            for bbs in self.basic_blocks.values():
                if bbs["bb_stmts"] == bb:
                    return
            self.basic_blocks[self.bb_counter] = {
                "bb_stmts": bb,
                "bb_out": tail.bb_out,
            }
            self.bb_counter += 1

    def dotgen_cfg(self) -> str:
        """Generate dot graph for CFG."""
        cfg: dict = {}
        dot = "digraph G {\n"

        for key, bb in self.basic_blocks.items():
            cfg[key] = {
                "bb_stmts": bb["bb_stmts"],
                "bb_out": (
                    [0 for _ in range(len(bb["bb_out"]))] if bb["bb_out"] else None
                ),
            }

            if bb["bb_out"]:

                for out_obj in bb["bb_out"]:
                    for k, v in self.basic_blocks.items():
                        if out_obj == v["bb_stmts"][0]:
                            cfg[key]["bb_out"][bb["bb_out"].index(out_obj)] = k
                            break

        for key, bb in cfg.items():
            for i, bbs in enumerate(bb["bb_stmts"]):
                if isinstance(bbs, uni.ElseIf):
                    cfg[key]["bb_stmts"][i] = "elif " + bbs.condition.unparse()
                elif isinstance(bbs, uni.IfStmt):
                    cfg[key]["bb_stmts"][i] = "if " + bbs.condition.unparse()
                elif isinstance(bbs, uni.ElseStmt):
                    cfg[key]["bb_stmts"][i] = "else"
                elif isinstance(bbs, uni.Archetype):
                    cfg[key]["bb_stmts"][i] = "obj " + bbs.name.unparse()
                elif isinstance(bbs, uni.Ability):
                    cfg[key]["bb_stmts"][i] = (
                        "can " + bbs.name_ref.unparse() + bbs.signature.unparse()
                        if bbs.signature
                        else ""
                    )
                elif isinstance(bbs, (uni.InForStmt, uni.IterForStmt)):
                    cfg[key]["bb_stmts"][i] = (
                        (
                            "for "
                            + bbs.target.unparse()
                            + " in "
                            + bbs.collection.unparse()
                        )
                        if isinstance(bbs, uni.InForStmt)
                        else (
                            "for "
                            + bbs.iter.unparse()
                            + bbs.condition.unparse()
                            + bbs.count_by.unparse()
                        )
                    )
                elif isinstance(bbs, uni.WhileStmt):
                    cfg[key]["bb_stmts"][i] = "while " + bbs.condition.unparse()
                else:
                    cfg[key]["bb_stmts"][i] = bbs.unparse()

        for key, value in cfg.items():
            if value.get("bb_stmts"):
                stmts = "\\n".join(
                    [stmt.replace('"', '\\"') for stmt in value["bb_stmts"]]
                )
                dot += f'  {key} [label="BB{key}\\n{stmts}", shape=box];\n'
            else:
                dot += f'  {key} [label="BB{key}"];\n'

        for key, value in cfg.items():
            if value.get("bb_out"):
                for out_id in value["bb_out"]:
                    dot += f"  {key} -> {out_id};\n"

        dot += "}\n"
        return dot

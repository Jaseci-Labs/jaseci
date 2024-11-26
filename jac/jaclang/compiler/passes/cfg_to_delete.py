from __future__ import annotations

import dis
import sys
import types
from collections import defaultdict
import graphviz
import asyncio
from typing import Dict, Set, List, Tuple, Optional


class CFGNode:
    def __init__(self, offset: int, instructions: List[dis.Instruction]):
        self.offset = offset
        self.instructions = instructions
        self.next: List['CFGNode'] = []
        self.hits = 0  # Track number of times this node is executed

    def __repr__(self):
        return f"Node({self.offset})"


class CFGTracker:
    def __init__(self):
        self.cfg_cache: Dict[types.CodeType, Dict[int, CFGNode]] = {}
        self.coverage_data: Dict[types.CodeType,
                                 Set[Tuple[int, int]]] = defaultdict(set)

    def build_cfg(self, code: types.CodeType) -> Dict[int, CFGNode]:
        """Build CFG from bytecode"""
        if code in self.cfg_cache:
            return self.cfg_cache[code]

        # Get bytecode instructions
        instructions = list(dis.get_instructions(code))

        # Find basic block boundaries
        leaders = {0}  # First instruction is always a leader
        for i, inst in enumerate(instructions):
            if inst.opname in {'JUMP_ABSOLUTE', 'JUMP_FORWARD', 'POP_JUMP_IF_TRUE',
                               'POP_JUMP_IF_FALSE', 'JUMP_IF_TRUE_OR_POP',
                               'JUMP_IF_FALSE_OR_POP'}:
                leaders.add(inst.argval)  # Target of jump
                if i + 1 < len(instructions):
                    # Instruction after jump
                    leaders.add(instructions[i + 1].offset)

        # Create basic blocks
        blocks: Dict[int, CFGNode] = {}
        current_block: List[dis.Instruction] = []
        current_leader = 0

        for inst in instructions:
            if inst.offset in leaders and current_block:
                blocks[current_leader] = CFGNode(current_leader, current_block)
                current_block = []
                current_leader = inst.offset
            current_block.append(inst)

        if current_block:
            blocks[current_leader] = CFGNode(current_leader, current_block)

        # Connect blocks
        for offset, block in blocks.items():
            last_inst = block.instructions[-1]

            if last_inst.opname in {'JUMP_ABSOLUTE', 'JUMP_FORWARD'}:
                block.next.append(blocks[last_inst.argval])
            elif last_inst.opname in {'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE',
                                      'JUMP_IF_TRUE_OR_POP', 'JUMP_IF_FALSE_OR_POP'}:
                block.next.append(blocks[last_inst.argval])  # Branch target
                if offset + last_inst.size < instructions[-1].offset:
                    # Find next instruction's block
                    next_offset = offset + last_inst.size
                    while next_offset not in blocks:
                        next_offset += 1
                    block.next.append(blocks[next_offset])  # Fall-through
            elif offset + last_inst.size < instructions[-1].offset:
                # Sequential flow
                next_offset = offset + last_inst.size
                while next_offset not in blocks:
                    next_offset += 1
                block.next.append(blocks[next_offset])

        self.cfg_cache[code] = blocks
        return blocks

    def trace_callback(self, frame: types.FrameType, event: str) -> Optional[types.TraceFunction]:
        """Trace function to track executed branches"""
        if event != 'line':
            return self.trace_callback

        code = frame.f_code
        if code not in self.cfg_cache:
            self.build_cfg(code)

        # Find current basic block
        blocks = self.cfg_cache[code]
        current_offset = frame.f_lasti

        # Find the block containing this offset
        current_block = None
        for block in blocks.values():
            if block.offset <= current_offset <= block.offset + sum(inst.size for inst in block.instructions):
                current_block = block
                break

        if current_block:
            current_block.hits += 1
            # Record taken branches
            for next_block in current_block.next:
                self.coverage_data[code].add(
                    (current_block.offset, next_block.offset))

        return self.trace_callback

    def start_tracking(self):
        """Start tracking branch coverage"""
        sys.settrace(self.trace_callback)

    def stop_tracking(self):
        """Stop tracking branch coverage"""
        sys.settrace(None)

    def get_coverage_report(self, code: types.CodeType) -> str:
        """Generate coverage report for the given code object"""
        if code not in self.cfg_cache:
            return "No coverage data available"

        blocks = self.cfg_cache[code]
        taken_branches = self.coverage_data[code]

        # Calculate total possible branches
        total_branches = sum(len(block.next) for block in blocks.values())
        covered_branches = len(taken_branches)

        report = []
        report.append(f"Branch Coverage: {covered_branches}/{total_branches} "
                      f"({covered_branches/total_branches*100:.1f}%)")

        # Report uncovered branches
        uncovered = []
        for block in blocks.values():
            for next_block in block.next:
                if (block.offset, next_block.offset) not in taken_branches:
                    uncovered.append((block.offset, next_block.offset))

        if uncovered:
            report.append("\nUncovered branches:")
            for src, dst in sorted(uncovered):
                report.append(f"  {src} -> {dst}")

        return "\n".join(report)

    def visualize_cfg(self, code: types.CodeType, filename: str = 'cfg'):
        """Generate a visual representation of the CFG using graphviz"""
        if code not in self.cfg_cache:
            self.build_cfg(code)

        dot = graphviz.Digraph(comment='Control Flow Graph')
        blocks = self.cfg_cache[code]
        taken_branches = self.coverage_data[code]

        # Add nodes
        for block in blocks.values():
            label = f"Offset: {block.offset}\nHits: {block.hits}\n"
            label += "\n".join(str(inst) for inst in block.instructions)
            dot.node(str(block.offset), label)

        # Add edges
        for block in blocks.values():
            for next_block in block.next:
                color = 'green' if (
                    block.offset, next_block.offset) in taken_branches else 'red'
                dot.edge(str(block.offset), str(
                    next_block.offset), color=color)

        # Save the visualization
        dot.render(filename, view=True)

# Example usage


def example_function(x: int) -> int:
    if x > 0:
        if x % 2 == 0:
            return x * 2
        else:
            return x * 3
    return x


# Create tracker and start tracking
tracker = CFGTracker()
tracker.start_tracking()

# Run some test cases
example_function(4)
example_function(3)
example_function(0)

# Stop tracking and get report
tracker.stop_tracking()
print(tracker.get_coverage_report(example_function.__code__))

# Visualize the CFG
tracker.visualize_cfg(example_function.__code__, 'example_cfg')

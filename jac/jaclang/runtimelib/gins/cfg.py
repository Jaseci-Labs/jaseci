"""CFG generation primitives for generating a CFG in jaclang passes.
"""

import marshal
import dis
from collections import defaultdict
from typing import List, Optional, Iterator


class BytecodeOp:
    def __init__(
        self,
        op: int,
        arg: int,
        offset: int,
        argval: int,
        argrepr: str,
        is_jump_target: bool,
    ) -> None:
        self.op = op
        self.arg = arg
        self.offset = offset
        self.argval = argval
        self.argrepr = argrepr
        self.is_jump_target = is_jump_target
        # default the offset
        self.__offset_size = 0

    def __repr__(self):
        return f"Instr: offset={self.offset}, Opname={self.op}, arg={self.arg}, argval={self.argval}, argrepr={self.argrepr}, jump_t={self.is_jump_target}"

    def is_branch(self) -> bool:
        return self.op in {
            "JUMP_ABSOLUTE",
            "JUMP_FORWARD",
            "JUMP_BACKWARD",
            "POP_JUMP_IF_TRUE",
            "POP_JUMP_IF_FALSE",
            "JUMP_IF_TRUE_OR_POP",
            "JUMP_IF_FALSE_OR_POP",
        }

    def is_conditional_branch(self) -> bool:
        return self.op in {
            # TODO:These may not be used anymore?
            "JUMP_IF_TRUE_OR_POP",
            "JUMP_IF_FALSE_OR_POP",
            "POP_JUMP_IF_TRUE",
            "POP_JUMP_IF_FALSE",
        }

    def is_relative_branch(self) -> bool:
        return False

    def is_return(self) -> bool:
        return self.op == "RETURN_VALUE"

    def is_raise(self) -> bool:
        return self.op == "RAISE_VARARGS"

    def is_for_iter(self) -> bool:
        return self.op == "FOR_ITER"

    def set_offset_size(self, size) -> None:
        self.__offset_size = size

    def get_offset_size(self) -> int:
        return self.__offset_size

    def get_next_instruction_offset(self) -> int:
        return self.__offset_size + self.offset


class Block:
    def __init__(self, id: int, instructions: List):
        self.id: int = id
        self.instructions = instructions
        self.exec_count = 0
        # Potentially use offset instead
        self.bytecode_offsets = set(
            [instr.offset for instr in self.instructions if instr.offset != None]
        )

    def __repr__(self):
        instructions = "\n".join([str(instr) for instr in self.instructions])
        return f"bb{self.id}:\n{instructions}"


class BlockMap:
    def __init__(self) -> None:
        self.idx_to_block: Dict[int, Block] = {}

    def add_block(self, idx, block):
        self.idx_to_block[idx] = block

    def __repr__(self) -> str:
        result = []
        for block in self.idx_to_block.values():
            result.append(repr(block))
        return "\n".join(result)

    def __str__(self) -> str:
        return self.__repr__()


def disassemble_bytecode(bytecode):
    code_object = marshal.loads(bytecode)
    instructions = []
    for i, instr in enumerate(dis.get_instructions(code_object)):
        instructions.append(
            BytecodeOp(
                op=instr.opname,
                arg=instr.arg,
                offset=instr.offset,
                argval=instr.argval,
                argrepr=instr.argrepr,
                is_jump_target=instr.is_jump_target,
            )
        )
        # set offest size for calculating next instruction
        # last instruction is default of 0, but shouldn't be needed
        if i != 0:
            instruction = instructions[i - 1]
            instruction.set_offset_size(instr.offset - instructions[i - 1].offset)
    return instructions


def create_BBs(instructions: List[BytecodeOp]) -> BlockMap:
    block_starts = set([0])
    block_map = BlockMap()
    num_instr = len(instructions)

    # Create offset to index mapping
    offset_to_index = {instr.offset: idx for idx, instr in enumerate(instructions)}
    max_offset = instructions[-1].get_next_instruction_offset()
    # print(f"Offset to Index Mapping: {offset_to_index}")

    def valid_offset(offset):
        return offset >= 0 and offset <= max_offset

    # Identify all block starts
    for instr in instructions:
        if instr.is_branch() or instr.is_for_iter():
            next_instr_offset = instr.get_next_instruction_offset()
            target_offset = instr.argval

            if instr.is_for_iter():
                block_starts.add(instr.offset)
            elif valid_offset(next_instr_offset):
                block_starts.add(next_instr_offset)

            if valid_offset(target_offset):
                block_starts.add(target_offset)

    # identify the blocks, since we define BBs by jumps, a sorted list of those
    # instructions give a range for instructions each BB will hold
    block_starts_ordered = sorted(block_starts)
    for block_id, start_offset in enumerate(block_starts_ordered):
        end_offset = (
            block_starts_ordered[block_id + 1]
            if block_id + 1 < len(block_starts_ordered)
            else instructions[-1].get_next_instruction_offset()
        )
        start_index = offset_to_index[start_offset]
        end_index = offset_to_index[end_offset]

        # capture last instruction if the BB only has 1
        if start_index == end_index:
            end_index += 1

        # Collect instructions for this block
        block_instrs = instructions[start_index:end_index]
        block_map.add_block(block_id, Block(block_id, block_instrs))
    return block_map


class CFG:
    def __init__(self, block_map: BlockMap):
        self.nodes = set()
        self.edges = {}
        self.edge_counts = {}
        self.block_map = block_map

    def add_node(self, node_id):
        self.nodes.add(node_id)
        if node_id not in self.edges:
            self.edges[node_id] = []

    def add_edge(self, from_node, to_node):
        if from_node in self.edges:
            self.edges[from_node].append(to_node)
        else:
            self.edges[from_node] = to_node

        self.edge_counts[(from_node, to_node)] = 0

    def display_instructions(self):
        return repr(self.block_map)

    def get_cfg_repr(self):
        return self.__repr__()

    def to_json(self):
        obj = {'timestamp':0,'cfg_bbs':[]}
        for node in self.nodes:
            bb_obj = {
                'bb_id': node, 
                'freq':self.block_map.idx_to_block[node].exec_count,
                'edges':[]
            }
            if node in self.edges and self.edges[node]:
                for succ in self.edges[node]:
                    edge_obj = {'edge_to':succ,'freq': self.edge_counts[(node, succ)]}
                    bb_obj['edges'].append(edge_obj)
            bb_obj['edges'].append(edge_obj)
            obj['cfg_bbs'].append(bb_obj)
        return obj

    def __repr__(self):
        result = []
        for node in self.nodes:
            result.append(
                f"Node bb{node} (freq={self.block_map.idx_to_block[node].exec_count}):"
            )
            if node in self.edges and self.edges[node]:
                for succ in self.edges[node]:
                    result.append(f"(freq={self.edge_counts[(node, succ)]})-> bb{succ}")
        return "\n".join(result)


def create_cfg(block_map: BlockMap) -> CFG:
    cfg = CFG(block_map)

    for block_id, block in block_map.idx_to_block.items():
        cfg.add_node(block_id)

        first_instr = block.instructions[0]
        last_instr = block.instructions[-1]
        if first_instr.is_for_iter():
            # get the BB that starts with END_FOR
            end_for_offset = first_instr.argval
            end_for_block = find_block_by_offset(block_map, end_for_offset)
            if end_for_block is not None:
                cfg.add_edge(block_id, end_for_block)

        # handle jumps
        if last_instr.is_branch():
            target_offset = last_instr.argval
            target_block = find_block_by_offset(block_map, target_offset)
            if target_block is not None:
                cfg.add_edge(block_id, target_block)
            if last_instr.is_conditional_branch():
                fall_through_offset = block.instructions[
                    -1
                ].get_next_instruction_offset()
                fall_through_block = find_block_by_offset(
                    block_map, fall_through_offset
                )
                if fall_through_block is not None:
                    cfg.add_edge(block_id, fall_through_block)

        # handle fall-through to the next block for non-control flow instructions
        else:
            fall_through_offset = block.instructions[-1].get_next_instruction_offset()
            fall_through_block = find_block_by_offset(block_map, fall_through_offset)
            if (
                fall_through_block is not None
                and fall_through_offset != last_instr.offset
            ):
                cfg.add_edge(block_id, fall_through_block)

    return cfg


def find_block_by_offset(block_map: BlockMap, offset: int) -> int:
    for block_id, block in block_map.idx_to_block.items():
        if any(instr.offset == offset for instr in block.instructions):
            return block_id
    return None


def visualize_cfg(cfg: CFG):
    try:
        from graphviz import Digraph

        dot = Digraph(comment="Control Flow Graph")
        for node in cfg.nodes:
            dot.node(f"bb{node}", f"BB{node}")
        for from_node, to_nodes in cfg.edges.items():
            for to_node in to_nodes:
                dot.edge(f"bb{from_node}", f"bb{to_node}")
        return dot
    except ImportError:
        print("Graphviz not installed, can't visualize CFG")
        return None


# can use as a test

# if __name__ == "__main__":
#     # Sample list of instructions for processing
#     ##simple=
#     # instructions = disassemble_bytecode(b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x01\xf3*\x00\x00\x00\x97\x00d\x00d\x01l\x00m\x01Z\x01\x01\x00d\x00Z\x02d\x00Z\x03e\x03d\x00k\\\x00\x00r\x02d\x02Z\x02d\x03Z\x02y\x04)\x05\xe9\x00\x00\x00\x00)\x01\xda\x0bannotations\xe9\x01\x00\x00\x00\xe9\xff\xff\xff\xffN)\x04\xda\n__future__r\x02\x00\x00\x00\xda\x01a\xda\x01x\xa9\x00\xf3\x00\x00\x00\x00\xfaP/Users/jakobtherkelsen/Documents/jaseci-ginS/jac/examples/ginsScripts/simple.jac\xfa\x08<module>r\x0b\x00\x00\x00\x01\x00\x00\x00s%\x00\x00\x00\xf0\x03\x01\x01\x01\xf5\x02\x07\x02\x03\xd8\x05\x06\x801\xd8\x05\x06\x801\xd8\x06\x07\x881\x82f\xd8\x07\x08\x80Q\xe0\x05\x07\x811r\t\x00\x00\x00')
#     # hot path
#     instructions = disassemble_bytecode(
#         b"c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x01\xf3\xa4\x00\x00\x00\x97\x00U\x00d\x00d\x01l\x00m\x01Z\x01\x01\x00d\x00Z\x02d\x02e\x03d\x03<\x00\x00\x00d\x04Z\x04d\x02e\x03d\x05<\x00\x00\x00e\x02e\x04z\x00\x00\x00Z\x05d\x02e\x03d\x06<\x00\x00\x00\x02\x00e\x06d\x04\xab\x01\x00\x00\x00\x00\x00\x00D\x00]\x1c\x00\x00Z\x07e\x02d\x07z\x06\x00\x00r\ne\x04e\x02z\x00\x00\x00Z\x04e\x02e\x04z\x00\x00\x00Z\x05d\x08e\x07z\x05\x00\x00e\x04e\x05z\x05\x00\x00z\x00\x00\x00Z\x02\x8c\x1e\x04\x00d\tZ\x05e\x05d\tk(\x00\x00r\x03d\x08Z\x05y\ny\n)\x0b\xe9\x00\x00\x00\x00)\x01\xda\x0bannotations\xda\x03int\xda\x01x\xe9\x03\x00\x00\x00\xda\x01y\xda\x01z\xe9\x02\x00\x00\x00\xe9\x04\x00\x00\x00\xe9\n\x00\x00\x00N)\x08\xda\n__future__r\x02\x00\x00\x00r\x04\x00\x00\x00\xda\x0f__annotations__r\x06\x00\x00\x00r\x07\x00\x00\x00\xda\x05range\xda\x01i\xa9\x00\xf3\x00\x00\x00\x00\xfaU/Users/jakobtherkelsen/Documents/jaseci-ginS/jac/examples/gins_scripts/simple_for.jac\xda\x08<module>r\x12\x00\x00\x00\x01\x00\x00\x00sy\x00\x00\x00\xf0\x03\x01\x01\x01\xf6\x02\x0f\x02\x03\xd8\r\x0e\x80Q\x80s\x83Z\xd8\r\x0e\x80Q\x80s\x83Z\xd8\r\x0e\x90\x11\x89U\x80Q\x80s\x83^\xd9\x0e\x13\x90A\x8eh\x88\x11\xd8\n\x0b\x88a\x8a%\xd8\r\x0e\x90\x11\x89U\x88\x11\xd8\r\x0e\x90\x11\x89U\x88\x11\xe0\x0b\x0c\x88q\x895\x901\x98\x01\x917\x89?\x81q\xf0\x0b\x00\x0f\x17\xf0\x0e\x00\n\x0c\x80Q\xd8\x08\t\x88R\x8a\x07\xd8\n\x0b\x81q\xf0\x03\x00\t\x10r\x10\x00\x00\x00"
#     )
#     BBs = create_BBs(instructions)
#     print(BBs)

#     cfg = create_cfg(BBs)
#     print("\nControl Flow Graph (CFG):")
#     print(cfg)

#     # Visualize CFG
#     dot = visualize_cfg(cfg)
#     dot.render("cfg.gv", view=True)

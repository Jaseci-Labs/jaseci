from typing import List
from jaseci.jac.ir.passes import IrPass
from antlr4 import RuleNode


class ArchitypePass(IrPass):
    def __init__(self, to_screen=True, with_exit=False, **kwargs):
        super().__init__(**kwargs)
        self.to_screen = to_screen
        self.with_exit = with_exit
        self.output = {"nodes": [], "walkers": []}

    def extract_vars(self, nodes: List[RuleNode]):
        vars = []

        for node in nodes:
            if node.name == "attr_stmt":
                children = node.kid[0].kid
                for child_node in children:
                    if child_node.name == "has_assign":
                        var = {}
                        var["name"] = child_node.kid[0].token_text()
                        var["line"], var["col"] = child_node.kid[0].loc[:2]
                        vars.append(var)

        return vars

    def enter_node(self, node: RuleNode):
        if node.name == "architype":
            architype = {}
            if node.kid[0].name == "KW_NODE" or node.kid[0].name == "KW_WALKER":
                architype["name"] = node.kid[1].token_text()
                architype["line"] = node.kid[1].loc[0]
                architype["col"] = node.kid[1].loc[1]
                architype["vars"] = self.extract_vars(node.kid[2].kid)
                architype["block_start"] = {}
                architype["block_end"] = {}

                # attr_block
                block_node = node.kid[2]
                block_node_start_node = block_node.kid[0]
                block_node_end_node = block_node.kid[-1]
                architype["block_start"]["line"] = block_node_start_node.loc[0]
                architype["block_start"]["col"] = block_node_start_node.loc[1]
                architype["block_end"]["line"] = block_node_end_node.loc[0]
                architype["block_end"]["col"] = block_node_end_node.loc[1]

                if node.kid[0].name == "KW_NODE":
                    self.output["nodes"].append(architype)

                if node.kid[0].name == "KW_WALKER":
                    self.output["walkers"].append(architype)

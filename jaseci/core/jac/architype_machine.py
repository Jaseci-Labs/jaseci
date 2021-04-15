"""
Sentinel machine for jac code in AST form

This machine should be inhereted from the class that manages state referenced
through self.
"""
from core.graph.node import node
from core.graph.edge import edge
from core.jac.machine import machine


class architype_machine(machine):
    """Jac machine mixin for objects that will execute Jac code"""

    def run_architype(self, jac_ast):
        """
        architype:
            KW_NODE NAME (COLON INT)? attr_block
            | KW_EDGE NAME attr_block;
        ;
        """
        kid = jac_ast.kid
        if(kid[0].name == 'KW_NODE'):
            item = node(h=self._h, kind=kid[1].token_text())
            if(kid[2].name == 'COLON'):
                item.dimension = int(kid[3].token_text())
            self.run_attr_block(kid[-1], item)
        elif(kid[0].name == 'KW_EDGE'):
            item = edge(h=self._h, kind=kid[1].token_text())
            self.run_attr_block(kid[-1], item)
        item.owner_id = self.owner().id
        return item

    def run_attr_block(self, jac_ast, obj):
        """
        attr_block:
            LBRACE (attr_stmt)* RBRACE
            | COLON (attr_stmt)* SEMI
            | SEMI;
        """
        kid = jac_ast.kid
        for i in kid:
            if(i.name == 'attr_stmt'):
                self.run_attr_stmt(i, obj)

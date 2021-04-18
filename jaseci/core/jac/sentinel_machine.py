"""
Sentinel machine for jac code in AST form

This machine should be inhereted from the class that manages state referenced
through self.
"""
from core.actor.architype import architype
from core.actor.walker import walker
from core.jac.machine import machine

from core.utils.utils import logger

class sentinel_machine(machine):
    """Jac machine mixin for objects that will execute Jac code"""

    def run_start(self, jac_ast):
        """
        start: element+ EOF;
        """
        kid = jac_ast.kid
        for i in kid[:-1]:
            self.run_element(i)

    def run_element(self, jac_ast):
        """
        element:
            architype
            | walker

        """
        kid = jac_ast.kid
        if(kid[0].name == 'architype'):
            self.run_architype(kid[0])
        elif(kid[0].name == 'walker'):
            self.run_walker(kid[0])

    def run_architype(self, jac_ast):
        """
        architype:
            KW_NODE NAME (COLON INT)? attr_block
            | KW_EDGE NAME attr_block
            | KW_GRAPH NAME graph_block;
        """
        kid = jac_ast.kid
        arch = architype(h=self._h, code=jac_ast)
        arch.name = (f"{kid[0].token_text()}.{kid[1].token_text()}")
        arch.save()
        self.arch_ids.add_obj(arch)

    # Note: Sentinels only registers the attr_stmts
    def run_walker(self, jac_ast):
        """
        walker: KW_WALKER NAME LBRACE (attr_stmt)* statement* RBRACE;
        """
        kid = jac_ast.kid
        walk = walker(h=self._h, code=jac_ast)
        walk.name = kid[1].token_text()
        walk.save()
        self.walker_ids.add_obj(walk)

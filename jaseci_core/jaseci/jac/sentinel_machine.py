"""
Sentinel machine for jac code in AST form

This machine should be inhereted from the class that manages state referenced
through self.
"""
from jaseci.actor.architype import architype
from jaseci.actor.walker import walker
from jaseci.jac.machine import machine


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
            self.load_architype(kid[0])
        elif(kid[0].name == 'walker'):
            self.load_walker(kid[0])

    def load_architype(self, jac_ast):
        """
        architype:
            KW_NODE NAME (COLON INT)? attr_block
            | KW_EDGE NAME attr_block
            | KW_GRAPH NAME graph_block;
        """
        arch = architype(h=self._h, code=jac_ast)
        if(self.arch_ids.has_obj_by_name(arch.name)):
            self.arch_ids.remove_obj_by_name(arch.name)
        self.arch_ids.add_obj(arch)

    # Note: Sentinels only registers the attr_stmts
    def load_walker(self, jac_ast):
        """
        walker: KW_WALKER NAME LBRACE (attr_stmt)* statement* RBRACE;
        """
        walk = walker(h=self._h, code=jac_ast)
        if(self.walker_ids.has_obj_by_name(walk.name)):
            self.walker_ids.remove_obj_by_name(walk.name)
        self.walker_ids.add_obj(walk)

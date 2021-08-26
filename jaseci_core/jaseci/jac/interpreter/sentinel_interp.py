"""
Sentinel interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.actor.architype import architype
from jaseci.actor.walker import walker
from jaseci.jac.interpreter.interp import interp
import hashlib


class sentinel_interp(interp):
    """Jac interpreter mixin for objects that will execute Jac code"""

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
        arch = architype(m_id=self._m_id, h=self._h, code_ir=jac_ast)
        if(self.arch_ids.has_obj_by_name(arch.name)):
            self.arch_ids.remove_obj_by_name(arch.name)
        self.arch_ids.add_obj(arch)
        return arch

    # Note: Sentinels only registers the attr_stmts
    def load_walker(self, jac_ast):
        """
        walker:
            KW_WALKER NAME namespace_list LBRACE attr_stmt* walk_entry_block? (
                statement
                | walk_activity_block
            )* walk_exit_block? RBRACE;
        """
        walk = walker(m_id=self._m_id, h=self._h, code_ir=jac_ast)
        for i in self.run_namespace_list(jac_ast.kid[2]):
            name = walk._m_id+i
            walk.namespaces[hashlib.md5(name.encode()).hexdigest()] = i
        if(self.walker_ids.has_obj_by_name(walk.name)):
            self.walker_ids.remove_obj_by_name(walk.name)
        self.walker_ids.add_obj(walk)
        return walk

    def run_namespace_list(self, jac_ast):
        """
        namespace_list: NAME (COMMA NAME)* |;
        """
        kid = jac_ast.kid
        ret = []
        for i in kid:
            if(i.name == 'NAME'):
                ret.append(i.token_text())
        return ret

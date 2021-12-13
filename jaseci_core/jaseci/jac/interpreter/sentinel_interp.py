"""
Sentinel interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.actor.architype import architype
from jaseci.actor.walker import walker
from jaseci.jac.interpreter.interp import interp
from jaseci.utils.utils import parse_str_token


class sentinel_interp(interp):
    """Jac interpreter mixin for objects that will execute Jac code"""

    def run_start(self, jac_ast):
        """
        start: ver_label? element+ EOF;
        """
        kid = jac_ast.kid
        if(kid[0].name == 'ver_label'):
            self.run_ver_label(kid[0])
        for i in kid[:-1]:
            self.run_element(i)

    def run_ver_label(self, jac_ast):
        """
        ver_label: 'version' COLON STRING;
        """
        kid = jac_ast.kid
        self.version = parse_str_token(kid[2].token_text())

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
            self.arch_ids.destroy_obj_by_name(arch.name)
        self.arch_ids.add_obj(arch)
        return arch

    # Note: Sentinels only registers the attr_stmts
    def load_walker(self, jac_ast):
        """
        walker:
            KW_WALKER NAME namespaces? LBRACE attr_stmt* walk_entry_block? (
                statement
                | walk_activity_block
            )* walk_exit_block? RBRACE;
        """
        walk = walker(m_id=self._m_id, h=self._h, code_ir=jac_ast)
        if(jac_ast.kid[2].name == 'namespaces'):
            walk.namespaces = self.run_namespaces(jac_ast.kid[2])
        if(self.walker_ids.has_obj_by_name(walk.name)):
            self.walker_ids.destroy_obj_by_name(walk.name)
        self.walker_ids.add_obj(walk)
        return walk

    def run_namespaces(self, jac_ast):
        """
        namespaces: COLON name_list;
        """
        return self.run_name_list(jac_ast.kid[1])

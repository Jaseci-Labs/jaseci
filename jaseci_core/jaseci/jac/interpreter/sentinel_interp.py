"""
Sentinel interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.actor.architype import architype
from jaseci.actor.walker import walker
from jaseci.jac.interpreter.interp import interp
from jaseci.utils.utils import parse_str_token
from jaseci.jac.ir.jac_code import jac_ast_to_ir
from jaseci.jac.machine.jac_scope import jac_scope


class sentinel_interp(interp):
    """Jac interpreter mixin for objects that will execute Jac code"""

    def run_start(self, jac_ast):
        """
        start: ver_label? element* EOF;
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "ver_label":
            self.run_ver_label(kid[0])
        for i in kid[:-1]:
            self.run_element(i)

    def run_ver_label(self, jac_ast):
        """
        ver_label: 'version' COLON STRING;
        """
        kid = self.set_cur_ast(jac_ast)
        self.version = parse_str_token(kid[2].token_text())

    def run_element(self, jac_ast):
        """
        element: global | architype | walker | test;
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "global_var":
            self.load_global_var(kid[0])
        elif kid[0].name == "architype":
            self.load_architype(kid[0])
        elif kid[0].name == "walker":
            self.load_walker(kid[0])
        elif kid[0].name == "test":
            self.load_test(kid[0])

    def load_global_var(self, jac_ast):
        """
        global_var:
            KW_GLOBAL NAME EQ expression (COMMA NAME EQ expression)* SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        kid = kid[1:]
        while kid[0].name == "NAME":
            const_name = kid[0].token_text()
            if const_name in self.global_vars:
                self.rt_error(f"Global {const_name} already defined!", kid[0])
            else:
                self.global_vars[const_name] = self.run_expression(kid[2]).value
            kid = kid[4:] if kid[3].name == "COMMA" else kid[3:]

    def load_architype(self, jac_ast):
        """
        architype:
            KW_NODE NAME (COLON NAME)* (COLON INT)? attr_block
            | KW_EDGE NAME (COLON NAME)* attr_block
            | KW_GRAPH NAME graph_block;
        """
        kid = self.set_cur_ast(jac_ast)
        name = kid[1].token_text()
        kind = kid[0].token_text()
        arch = architype(
            m_id=self._m_id, h=self._h, code_ir=jac_ast, name=name, kind=kind
        )
        if len(kid) > 2 and kid[2].name == "COLON":
            for i in kid[2:]:
                if i.name == "NAME":
                    arch.super_archs.append(i.token_text())
        if self.arch_ids.has_obj_by_name(arch.name, kind=arch.kind):
            self.arch_ids.destroy_obj_by_name(arch.name, kind=arch.kind)
        self.arch_ids.add_obj(arch)
        self.arch_can_compile(kid[-1], arch)
        return arch

    def arch_can_compile(self, jac_ast, arch):
        """Helper function to statically compile can stmts for arch"""
        kid = self.set_cur_ast(jac_ast)
        self.push_scope(jac_scope(parent=self, has_obj=self, action_sets=[]))
        if jac_ast.name == "attr_block":
            for i in kid:
                if i.name == "attr_stmt" and i.kid[0].name == "can_stmt":
                    self.run_can_stmt(i.kid[0], arch)
        elif kid[0].name == "graph_block_spawn":
            kid = kid[0].kid[2].kid
            for i in kid:
                self.run_can_stmt(i, arch)
        self.pop_scope()

    # Note: Sentinels only registers the attr_stmts
    def load_walker(self, jac_ast):
        """
        walker: KW_WALKER NAME namespaces? walker_block;
        """
        kid = self.set_cur_ast(jac_ast)
        name = kid[1].token_text()
        kind = kid[0].token_text()
        walk = walker(m_id=self._m_id, h=self._h, code_ir=jac_ast, name=name, kind=kind)
        if jac_ast.kid[2].name == "namespaces":
            walk.namespaces = self.run_namespaces(jac_ast.kid[2])
        if self.walker_ids.has_obj_by_name(walk.name):
            self.walker_ids.destroy_obj_by_name(walk.name)
        self.walker_ids.add_obj(walk)
        return walk

    def load_test(self, jac_ast):
        """
        test:
            KW_TEST STRING KW_WITH (graph_ref | KW_GRAPH graph_block) KW_BY (
                (walker_ref spawn_ctx? (code_block | SEMI))
                | KW_WALKER walker_block
            );
        """
        kid = self.set_cur_ast(jac_ast)
        testcase = {
            "title": kid[1].token_text(),
            "graph_ref": None,
            "graph_block": None,
            "walker_ref": None,
            "spawn_ctx": None,
            "assert_block": None,
            "walker_block": None,
            "outcome": None,
        }
        kid = kid[3:]
        if kid[0].name == "graph_ref":
            graph_name = kid[0].kid[2].token_text()
            if not self.arch_ids.has_obj_by_name(graph_name, kind="graph"):
                self.rt_error(f"Graph {graph_name} not found!", kid[0])
                return
            testcase["graph_ref"] = graph_name
        else:
            kid = kid[1:]
            testcase["graph_block"] = jac_ast_to_ir(kid[0])
        kid = kid[2:]
        if kid[0].name == "walker_ref":
            walker_name = kid[0].kid[2].token_text()
            if not self.walker_ids.has_obj_by_name(walker_name):
                self.rt_error(f"Walker {walker_name} not found!", kid[0])
                return
            testcase["walker_ref"] = walker_name
            kid = kid[1:]
            if kid[0].name == "spawn_ctx":
                testcase["spawn_ctx"] = jac_ast_to_ir(kid[0])
                kid = kid[1:]
            if kid[0].name == "code_block":
                testcase["assert_block"] = jac_ast_to_ir(kid[0])
        else:
            kid = kid[1:]
            testcase["walker_block"] = jac_ast_to_ir(kid[0])

        self.testcases.append(testcase)

    def run_namespaces(self, jac_ast):
        """
        namespaces: COLON name_list;
        """
        return self.run_name_list(jac_ast.kid[1])

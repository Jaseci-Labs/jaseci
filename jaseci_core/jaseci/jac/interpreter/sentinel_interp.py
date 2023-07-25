"""
Sentinel interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.prim.architype import Architype
from jaseci.jac.interpreter.interp import Interp
from jaseci.utils.utils import parse_str_token
from jaseci.jac.ir.jac_code import jac_ast_to_ir
from jaseci.jac.machine.jac_scope import JacScope
from jaseci.prim.ability import Ability


class SentinelInterp(Interp):
    """Jac interpreter mixin for objects that will execute Jac code"""

    def run_start(self, jac_ast):
        """
        start: ver_label? element* EOF;
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "ver_label":
            self.run_ver_label(kid[0])
        for i in kid:
            self.run_element(i)

    def run_ver_label(self, jac_ast):
        """
        ver_label: 'version' COLON STRING;
        """
        kid = self.set_cur_ast(jac_ast)
        self.version = parse_str_token(kid[2].token_text())

    def run_element(self, jac_ast):
        """
        element: global_var | architype | test;
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "global_var":
            self.load_global_var(kid[0])
        elif kid[0].name == "architype":
            self.load_architype(kid[0])
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
                self.run_expression(kid[2])
                self.global_vars[const_name] = self.pop().value
            kid = kid[4:] if kid[3].name == "COMMA" else kid[3:]

    def load_architype(self, jac_ast):
        """
        architype:
            KW_NODE NAME (COLON NAME)* (COLON INT)? attr_block
            | KW_EDGE NAME (COLON NAME)* attr_block
            | KW_GRAPH NAME graph_block
            | KW_ASYNC? KW_WALKER NAME namespaces? walker_block;
        """
        kid = self.set_cur_ast(jac_ast)

        is_async = kid[0].name == "KW_ASYNC" and bool(kid.pop(0))

        name = kid[1].token_text()
        kind = kid[0].token_text()
        arch = Architype(
            m_id=self._m_id,
            h=self._h,
            code_ir=jac_ast,
            name=name,
            kind=kind,
            is_async=is_async,
            parent=self,
        )

        if len(kid) > 2 and kid[2].name == "COLON":
            for i in kid[2:]:
                if i.name == "NAME":
                    arch.super_archs.append(i.token_text())
        if self.arch_ids.has_obj_by_name(arch.name, kind=arch.kind):
            self.arch_ids.destroy_obj_by_name(arch.name, kind=arch.kind)
        self.arch_ids.add_obj(arch)
        self.arch_has_preproc(kid[-1], arch)
        self.arch_can_compile(kid[-1], arch)
        return arch

    # Note: Sentinels only registers the attr_stmts

    def arch_has_preproc(self, jac_ast, arch):
        """Helper function to statically compile can stmts for arch"""
        kid = self.set_cur_ast(jac_ast)
        if jac_ast.name in ["attr_block", "walker_block"]:
            for i in kid:
                if i.name == "attr_stmt" and i.kid[0].name == "has_stmt":
                    for j in i.kid[0].kid:
                        if j.name == "has_assign":
                            has_kid = j.kid
                            is_private = False
                            is_anchor = False
                            if has_kid[0].name == "KW_PRIVATE":
                                has_kid = has_kid[1:]
                                is_private = True
                            if has_kid[0].name == "KW_ANCHOR":
                                has_kid = has_kid[1:]
                                is_anchor = True
                            var_name = has_kid[0].token_text()
                            if is_private:
                                arch.private_vars.append(var_name)
                            if is_anchor and arch.anchor_var is None:
                                arch.anchor_var = var_name
                            arch.has_vars.append(var_name)
        arch.save()

    def arch_can_compile(self, jac_ast, arch):
        """Helper function to statically compile can stmts for arch"""
        kid = self.set_cur_ast(jac_ast)
        self.push_scope(
            JacScope(parent=self, name=f"a_cgen:{jac_ast.loc_str()}", has_obj=None)
        )
        if jac_ast.name in ["attr_block", "walker_block"]:
            for i in kid:
                if i.name == "attr_stmt" and i.kid[0].name == "can_stmt":
                    self.run_can_stmt(i.kid[0], arch)
        elif jac_ast.name == "graph_block":
            self.run_can_block(jac_ast.kid[2], arch)
        self.pop_scope()

    def run_can_block(self, jac_ast, arch):
        """
        can_block: (can_stmt)*;
        """
        kid = self.set_cur_ast(jac_ast)
        for i in kid:
            if i.name == "can_stmt":
                self.run_can_stmt(i, arch)

    def run_can_stmt(self, jac_ast, obj):
        """
        can_stmt:
            KW_CAN dotted_name (preset_in_out event_clause)? (
                COMMA dotted_name (preset_in_out event_clause)?
            )* SEMI
            | KW_CAN NAME event_clause? code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        kid = kid[1:]
        ir = None
        while True:
            action_type = "activity"
            access_list = None
            preset_in_out = None
            if kid[0].name == "NAME":
                action_name = kid[0].token_text()
            else:
                action_name = self.run_dotted_name(kid[0])
            kid = kid[1:]
            if len(kid) > 0 and kid[0].name == "preset_in_out":
                preset_in_out = jac_ast_to_ir(kid[0])
                kid = kid[1:]
            if len(kid) > 0 and kid[0].name == "event_clause":
                action_type, access_list = self.run_event_clause(kid[0])
                kid = kid[1:]
            if kid[0].name != "code_block":
                self.check_builtin_action(action_name, jac_ast)
            else:
                ir = kid[0]
            getattr(obj, f"{action_type}_ability_ids").add_obj(
                Ability(
                    m_id=self._m_id,
                    h=self._h,
                    name=action_name,
                    kind="ability",
                    code_ir=ir,
                    preset_in_out=preset_in_out,
                    access_list=access_list,
                    parent=self,
                )
            )
            if not len(kid) or kid[0].name != "COMMA":
                break
            else:
                kid = kid[1:]

    def run_event_clause(self, jac_ast):
        """
        event_clause:
                KW_WITH name_list? (KW_ENTRY | KW_EXIT | KW_ACTIVITY);
        """
        kid = self.set_cur_ast(jac_ast)
        nl = []
        if kid[1].name == "name_list":
            nl = self.run_name_list(kid[1])
        return kid[-1].token_text(), nl

    def load_test(self, jac_ast):
        """
        test:
            KW_TEST NAME? multistring KW_WITH (
                graph_ref
                | KW_GRAPH graph_block
            ) KW_BY (
                (walker_ref spawn_ctx? (code_block | SEMI))
                | KW_WALKER walker_block
            );
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_multistring(kid[2]) if kid[1].name == "NAME" else self.run_multistring(
            kid[1]
        )
        testcase = {
            "name": kid[1].token_text() if kid[1].name == "NAME" else "",
            "title": self.pop().value,
            "graph_ref": None,
            "graph_block": None,
            "walker_ref": None,
            "spawn_ctx": None,
            "assert_block": None,
            "walker_block": None,
            "outcome": None,
        }
        kid = kid[4:] if kid[1].name == "NAME" else kid[3:]
        if kid[0].name == "graph_ref":
            graph_name = kid[0].kid[-1].token_text()
            if not self.arch_ids.has_obj_by_name(graph_name, kind="graph"):
                self.rt_error(f"Graph {graph_name} not found!", kid[0])
            testcase["graph_ref"] = graph_name
        else:
            kid = kid[1:]
            testcase["graph_block"] = jac_ast_to_ir(kid[0])
        kid = kid[2:]
        if kid[0].name == "walker_ref":
            walker_name = kid[0].kid[-1].token_text()
            if not self.arch_ids.has_obj_by_name(name=walker_name, kind="walker"):
                self.rt_error(f"Walker {walker_name} not found!", kid[0])
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

"""
Sentinel interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.graph.node import Node
from jaseci.graph.edge import Edge
from jaseci.actor.walker import Walker
from jaseci.jac.interpreter.interp import Interp
from jaseci.jac.machine.jac_scope import JacScope
from jaseci.jac.machine.jac_value import jac_elem_unwrap as jeu


class ArchitypeInterp(Interp):
    """Jac interpreter mixin for objects that will execute Jac code"""

    def run_architype(self, jac_ast):
        """
        architype:
            KW_NODE NAME (COLON NAME)* attr_block
            | KW_EDGE NAME (COLON NAME)* attr_block
            | KW_TYPE NAME struct_block
            | KW_GRAPH NAME graph_block
            | KW_ASYNC? KW_WALKER NAME namespaces? walker_block;
        """
        if jac_ast is None:  # Using defaults
            if self.kind == "node" and self.name in ["root", "generic"]:
                return Node(
                    m_id=self._m_id,
                    h=self._h,
                    kind=self.kind,
                    name=self.name,
                    parent=self.parent(),
                )
            elif self.kind == "edge" and self.name in ["generic"]:
                return Edge(
                    m_id=self._m_id,
                    h=self._h,
                    kind=self.kind,
                    name=self.name,
                    parent=self.parent(),
                )

        kid = self.set_cur_ast(jac_ast)

        self.push_scope(JacScope(parent=self, has_obj=self, action_sets=[]))
        if kid[0].name == "KW_NODE":
            item = Node(
                m_id=self._m_id,
                h=self._h,
                kind=kid[0].token_text(),
                name=kid[1].token_text(),
                parent=self.parent(),
            )
            self.build_object_with_supers(item, kid[-1])
        elif kid[0].name == "KW_EDGE":
            item = Edge(
                m_id=self._m_id,
                h=self._h,
                kind=kid[0].token_text(),
                name=kid[1].token_text(),
                parent=self.parent(),
            )
            self.build_object_with_supers(item, kid[-1])
        elif kid[0].name == "KW_TYPE":
            item = self.run_struct_block(kid[-1])
        elif kid[0].name == "KW_GRAPH":
            item = self.run_graph_block(kid[-1])
        elif kid[0].name == "KW_WALKER":
            item = Walker(
                m_id=self._m_id,
                h=self._h,
                code_ir=jac_ast,
                name=kid[1].token_text(),
                kind=kid[0].token_text(),
                parent=self.parent(),
                is_async=self.is_async,
            )
            if kid[2].name == "namespaces":
                item.namespaces = self.run_namespaces(jac_ast.kid[2])
        elif jac_ast.name == "graph_block":  # usedi n jac tests
            item = self.run_graph_block(jac_ast)
        self.pop_scope()
        return item

    def run_namespaces(self, jac_ast):
        """
        namespaces: COLON name_list;
        """
        return self.run_name_list(jac_ast.kid[1])

    def run_attr_block(self, jac_ast, obj):
        """
        attr_block:
            LBRACE (attr_stmt)* RBRACE
            | COLON (attr_stmt)* SEMI
            | SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        for i in kid:
            if i.name == "attr_stmt":
                self.run_attr_stmt(i, obj)

    def run_struct_block(self, jac_ast):
        """
        struct_block: LBRACE (has_stmt)* RBRACE | COLON has_stmt | SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = {}
        for i in kid:
            if i.name == "has_stmt":
                self.run_has_stmt(i, ret)
        return ret

    def run_can_block(self, jac_ast):
        """
        can_block: (can_stmt)*;
        """
        kid = self.set_cur_ast(jac_ast)
        for i in kid:
            if i.name == "can_stmt":
                self.run_can_stmt(i, self)

    def run_graph_block(self, jac_ast):
        """
        graph_block: graph_block_spawn;
        """
        kid = self.set_cur_ast(jac_ast)
        return getattr(self, f"run_{kid[0].name}")(kid[0])

    def run_graph_block_spawn(self, jac_ast):
        """
        graph_block_spawn:
            LBRACE has_root can_block KW_SPAWN code_block RBRACE
            | COLON has_root can_block KW_SPAWN code_block SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        root_name = self.run_has_root(kid[1])
        self.run_can_block(kid[2])
        m = Interp(parent_override=self.parent(), caller=self)
        m.push_scope(
            JacScope(parent=self, has_obj=None, action_sets=[self.activity_action_ids])
        )
        try:
            m.run_code_block(kid[4])
        except Exception as e:
            self.rt_error(f"Internal Exception: {e}", m._cur_jac_ast)
        local_state = m._jac_scope.local_scope
        self.report = self.report + m.report
        if root_name in local_state.keys():
            obj = jeu(local_state[root_name], parent=self)
            if not isinstance(obj, Node):
                self.rt_error(f"{root_name} is {type(obj)} not node!", kid[3])
            return obj
        else:
            self.rt_error("Graph didn't produce root node!", kid[3])
            return None

    def run_has_root(self, jac_ast):
        """
        has_root: KW_HAS KW_ANCHOR NAME SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        return kid[2].token_text()

    # Helper Functions ##################

    def build_object_with_supers(self, item, jac_ast):
        for i in self.super_archs:
            super_jac_ast = (
                self.parent()
                .arch_ids.get_obj_by_name(name=i, kind=item.kind)
                .get_jac_ast()
                .kid[-1]
            )
            self.run_attr_block(super_jac_ast, item)
        self.run_attr_block(jac_ast, item)

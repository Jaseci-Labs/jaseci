"""
Walker interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.graph.node import Node
from jaseci.jac.interpreter.interp import Interp
from jaseci.jac.jac_set import JacSet
from jaseci.jac.machine.jac_scope import JacScope
from jaseci.jac.ir.jac_code import jac_ir_to_ast
from jaseci.utils.id_list import IdList


class WalkerInterp(Interp):
    """Jac interpreter mixin for objects that will execute Jac code"""

    # Walker only executes statements, sentinels handle attr_stmts

    def run_walker(self, jac_ast):
        """
        walker: KW_ASYNC? KW_WALKER NAME namespaces? walker_block;
        """
        kid = self.set_cur_ast(jac_ast)
        self.scope_and_run(
            jac_ast if jac_ast.name == "walker_block" else kid[-1],
            self.run_walker_block,
        )

    def run_walker_block(self, jac_ast):
        """
        walker_block:
            LBRACE attr_stmt* walk_entry_block? (
                statement
                | walk_activity_block
            )* walk_exit_block? RBRACE;
        """
        kid = self.set_cur_ast(jac_ast)
        if self.current_step == 0:
            for i in kid:
                if i.name == "attr_stmt":
                    self.run_attr_stmt(jac_ast=i, obj=self)
        archs = self.current_node.get_architype().arch_with_supers()
        act_list = IdList(self)
        for i in archs:
            act_list += i.entry_action_ids
        self.auto_trigger_node_actions(nd=self.current_node, act_list=act_list)

        for i in kid:
            if i.name == "walk_entry_block":
                self.run_walk_entry_block(i)
            if i.name == "statement":
                self.run_statement(i)
            if i.name == "walk_activity_block":
                self.run_walk_activity_block(i)

        # self.trigger_activity_actions()
        archs = self.current_node.get_architype().arch_with_supers()
        act_list = IdList(self)
        for i in archs:
            act_list += i.exit_action_ids
        self.auto_trigger_node_actions(nd=self.current_node, act_list=act_list)

        if not self.yielded and kid[-2].name == "walk_exit_block":
            self.run_walk_exit_block(kid[-2])

    def run_node_ctx_block(self, jac_ast):
        """
        node_ctx_block: name_list code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        for i in self.run_name_list(kid[0]):
            if self.current_node.get_architype().is_instance(i):
                self.run_code_block(kid[1])
                return

    def run_walk_entry_block(self, jac_ast):
        """
        walk_entry_block: KW_WITH KW_ENTRY code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        if self.current_step == 0:
            self.in_entry_exit = True
            self.run_code_block(kid[2])
            self.in_entry_exit = False

    def run_walk_exit_block(self, jac_ast):
        """
        walk_exit_block: KW_WITH KW_EXIT code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        self._stopped = None
        if len(self.next_node_ids) == 0:
            self.in_entry_exit = True
            self.run_code_block(kid[2])
            self.in_entry_exit = False

    def run_walk_activity_block(self, jac_ast):
        """
        walk_activity_block: KW_WITH KW_ACTIVITY code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_code_block(kid[2])

    def run_walker_action(self, jac_ast):
        """
        walker_action:
            ignore_action
            | take_action
            | disengage_action
            | yield_action;
        """
        kid = self.set_cur_ast(jac_ast)
        expr_func = getattr(self, f"run_{kid[0].name}")
        expr_func(kid[0])

    def run_ignore_action(self, jac_ast):
        """
        ignore_action: KW_IGNORE expression SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_expression(kid[1])
        result = self.pop().value
        if isinstance(result, Node):
            self.ignore_node_ids.add_obj(result)
        elif isinstance(result, JacSet):
            self.ignore_node_ids.add_obj_list(result)
        else:
            self.rt_error(f"{result} is not ignorable type (i.e., nodes)", kid[1])

    def run_take_action(self, jac_ast):
        """
        take_action:
            KW_TAKE (COLON NAME)? expression (SEMI | else_stmt);
        """
        kid = self.set_cur_ast(jac_ast)
        style = "b"
        if kid[1].name == "COLON":
            style = kid[2].token_text()
            kid = kid[2:]
        self.run_expression(kid[1])
        result = self.pop().value
        before = len(self.next_node_ids)
        if isinstance(result, Node):
            if style in ["b", "bfs"]:
                self.next_node_ids.add_obj(result, allow_dups=True)
            elif style in ["d", "dfs"]:
                self.next_node_ids.add_obj(result, push_front=True, allow_dups=True)
            else:
                self.rt_error(f"{style} is invalid take operation", kid[0])
        elif isinstance(result, JacSet):
            if style in ["b", "bfs"]:
                self.next_node_ids.add_obj_list(result, allow_dups=True)
            elif style in ["d", "dfs"]:
                self.next_node_ids.add_obj_list(
                    result, push_front=True, allow_dups=True
                )
            else:
                self.rt_error(f"{style} is invalid take operation", kid[0])
        elif result:
            self.rt_error(f"{result} is not destination type (i.e., nodes)", kid[1])
        after = len(self.next_node_ids)
        if before >= after and kid[2].name == "else_stmt":
            self.run_else_stmt(kid[2])
        after = len(self.next_node_ids)

    def run_disengage_action(self, jac_ast):
        """
        disengage_action: KW_DISENGAGE (report_action | SEMI);
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[1].name == "report_action":
            self.run_report_action(kid[1])
        self._stopped = "stop"
        self.next_node_ids.remove_all()

    def run_yield_action(self, jac_ast):
        """
        yield_action:
            KW_YIELD (
                report_action
                | disengage_action
                | take_action
                | SEMI
            );
        """
        kid = self.set_cur_ast(jac_ast)
        if len(kid) and kid[1].name != "SEMI":
            expr_func = getattr(self, f"run_{kid[1].name}")
            expr_func(kid[1])
        self.yield_walk()

    def run_preset_in_out(self, jac_ast, obj, act):
        """
        preset_in_out:
            DBL_COLON param_list? (DBL_COLON | COLON_OUT expression);

        obj: The node or edge with preset
        act: The action associated with preset
        """
        kid = self.set_cur_ast(jac_ast)
        param_list = {"args": [], "kwargs": []}
        m = Interp(parent_override=self.parent(), caller=self)
        arch = obj.get_architype()
        m.push_scope(
            JacScope(parent=self, has_obj=obj, action_sets=[arch.activity_action_ids])
        )
        m._jac_scope.set_agent_refs(cur_node=self.current_node, cur_walker=self)

        if kid[1].name == "param_list":
            param_list = m.run_param_list(kid[1]).value
        try:
            result = act.trigger(param_list, self._jac_scope, self)
        except Exception as e:
            self.rt_error(f"Internal Exception: {e}", m._cur_jac_ast)
            result = None
        if kid[-1].name == "expression":
            m.run_expression(kid[-1])
            dest = m.pop()
            dest.value = result
            dest.write(kid[-1])

    # Helper Functions ##################
    def auto_trigger_node_actions(self, nd, act_list):
        already_executed = []  # handles inhereted duplicates, (overriding)
        for i in act_list.obj_list():
            if (
                i.access_list
                and self.name not in i.access_list
                or i.name in already_executed
            ):
                continue
            if i.preset_in_out:
                self.run_preset_in_out(jac_ir_to_ast(i.preset_in_out), nd, i)
            else:
                self.call_ability(nd=nd, name=i.name, act_list=act_list)
            if not i.preset_in_out:  # All preset in and outs get executed
                already_executed.append(i.name)

    def scope_and_run(self, jac_ast, run_func):
        """
        Helper to run ast elements with execution scope added
        (Useful for running arbitrary code blocks as one-offs)
        """
        node_arch = self.current_node.get_architype()
        walk_arch = self.get_architype()
        self.push_scope(
            JacScope(
                parent=self,
                has_obj=self,
                action_sets=[
                    walk_arch.activity_action_ids,
                    node_arch.activity_action_ids,
                ],
            )
        )
        self._jac_scope.set_agent_refs(cur_node=self.current_node, cur_walker=self)

        run_func(jac_ast)
        self.pop_scope()

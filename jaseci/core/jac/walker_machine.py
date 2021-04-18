"""
Walker machine for jac code in AST form

This machine should be inhereted from the class that manages state referenced
through self.
"""
from core.actions.global_actions import global_action_ids
from core.element import element
from core.attr.action import action
from core.graph.node import node
from core.graph.edge import edge
from core.jac.machine import machine
from core.jac.jac_set import jac_set
from core.jac.jac_scope import jac_scope


class walker_machine(machine):
    """Jac machine mixin for objects that will execute Jac code"""
    # Walker only executes statements, sentinels handle attr_stmts

    def run_walker(self, jac_ast):
        """
        walker:
            KW_WALKER NAME LBRACE attr_stmt* walk_entry_block? (
                statement
                | walk_activity_block
            )* walk_exit_block? RBRACE;
        """
        self._jac_scope = jac_scope(self,
                                    self.local_scope,
                                    self.context,
                                    [global_action_ids,
                                     self.activity_action_ids,
                                     self.current_node.activity_action_ids])
        self.local_scope['here'] = self.current_node.id.urn

        self.trigger_entry_actions()
        kid = jac_ast.kid
        if(self.current_step == 0):
            for i in kid:
                if(i.name == 'attr_stmt'):
                    self.run_attr_stmt(jac_ast=i, obj=self)
        for i in kid:
            if(i.name == 'walk_entry_block'):
                self.run_walk_entry_block(i)
            if(i.name == 'statement'):
                self.run_statement(i)
            if(i.name == 'walk_activity_block'):
                self.run_walk_activity_block(i)
            if(i.name == 'walk_exit_block'):
                self.run_walk_exit_block(i)

        # self.trigger_activity_actions()
        self.trigger_exit_actions()

    def run_walk_entry_block(self, jac_ast):
        """
        walk_entry_block: KW_WITH KW_ENTRY code_block;
        """
        kid = jac_ast.kid
        if (self.current_step == 0):
            self.in_entry_exit = True
            self.run_code_block(kid[2])
            self.in_entry_exit = False

    def run_walk_exit_block(self, jac_ast):
        """
        walk_exit_block: KW_WITH KW_EXIT code_block;
        """
        kid = jac_ast.kid
        if (len(self.next_node_ids) == 0):
            self.in_entry_exit = True
            self.run_code_block(kid[2])
            self.in_entry_exit = False

    def run_walk_activity_block(self, jac_ast):
        """
        walk_activity_block: KW_WITH KW_ACTIVITY code_block;
        """
        kid = jac_ast.kid
        self.run_code_block(kid[2])

    def run_code_block(self, jac_ast):
        """
        code_block: LBRACE statement* RBRACE | COLON statement;
        TODO: Handle breaks and continues
        """
        kid = jac_ast.kid
        for i in kid:
            if (self.loop_ctrl):
                if (self.loop_ctrl == 'continue'):
                    self.loop_ctrl = None
                return
            if(i.name == 'statement'):
                self.run_statement(jac_ast=i)

    def run_node_ctx_block(self, jac_ast):
        """
        node_ctx_block: NAME (COMMA NAME)* code_block;
        """
        kid = jac_ast.kid
        while(kid[0].name != 'code_block'):
            if (self.current_node.kind == kid[0].token_text()):
                self.run_code_block(kid[-1])
                return
            kid = kid[1:]

    def run_statement(self, jac_ast):
        """
        statement:
            code_block
            | node_ctx_block
            | expression SEMI
            | if_stmt
            | for_stmt
            | while_stmt
            | ctrl_stmt SEMI
            | action_stmt;
        """
        if (self.stopped and not self.in_entry_exit):
            return
        kid = jac_ast.kid
        stmt_func = getattr(self, f'run_{kid[0].name}')
        stmt_func(kid[0])

    def run_if_stmt(self, jac_ast):
        """
        if_stmt: KW_IF expression code_block (elif_stmt)* (else_stmt)?;
        """
        kid = jac_ast.kid
        if(self.run_expression(kid[1])):
            self.run_code_block(kid[2])
            return
        kid = kid[3:]
        if(len(kid)):
            while True:
                if(kid[0].name == 'elif_stmt'):
                    if(self.run_elif_stmt(kid[0])):
                        return
                elif(kid[0].name == 'else_stmt'):
                    self.run_else_stmt(kid[0])
                    return
                kid = kid[1:]
                if(not len(kid)):
                    break

    def run_elif_stmt(self, jac_ast):
        """
        elif_stmt: KW_ELIF expression code_block;
        """
        kid = jac_ast.kid
        if(self.run_expression(kid[1])):
            self.run_code_block(kid[2])
            return True
        else:
            return False

    def run_else_stmt(self, jac_ast):
        """
        else_stmt: KW_ELSE code_block;
        """
        kid = jac_ast.kid
        self.run_code_block(kid[1])

    def run_for_stmt(self, jac_ast):
        """
        for_stmt:
            KW_FOR expression KW_TO expression KW_BY expression code_block
            | KW_FOR NAME KW_IN expression code_block;
        """
        kid = jac_ast.kid
        loops = 0
        if(kid[1].name == 'expression'):
            self.run_expression(kid[1])
            while self.run_expression(kid[3]):
                self.run_code_block(kid[6])
                loops += 1
                if (self.loop_ctrl == 'break'):
                    self.loop_ctrl = None
                    break
                self.run_expression(kid[5])
                if(loops > self.loop_limit):
                    self.rt_error(f'Hit loop limit, breaking...', kid[0])
        else:
            var_name = kid[1].token_text()
            lst = self.run_expression(kid[3])
            # should check that lst is list here
            for i in lst:
                self._jac_scope.set_live_var(var_name, i, [], kid[3])
                self.run_code_block(kid[4])
                loops += 1
                if (self.loop_ctrl == 'break'):
                    self.loop_ctrl = None
                    break
                if(loops > self.loop_limit):
                    self.rt_error(f'Hit loop limit, breaking...', kid[0])

    def run_while_stmt(self, jac_ast):
        """
        while_stmt: KW_WHILE expression code_block;
        """
        kid = jac_ast.kid
        loops = 0
        while self.run_expression(kid[1]):
            self.run_code_block(kid[2])
            loops += 1
            if (self.loop_ctrl == 'break'):
                self.loop_ctrl = None
                break
            if(loops > self.loop_limit):
                self.rt_error(f'Hit loop limit, breaking...', kid[0])

    def run_ctrl_stmt(self, jac_ast):
        """
        ctrl_stmt: KW_CONTINUE | KW_BREAK | KW_DISENGAGE | KW_SKIP;
        """
        kid = jac_ast.kid
        if (kid[0].name == 'KW_DISENGAGE'):
            self.stopped = 'stop'
            self.next_node_ids.remove_all()
        elif (kid[0].name == 'KW_SKIP'):
            self.stopped = 'skip'
        elif (kid[0].name == 'KW_BREAK'):
            self.loop_ctrl = 'break'
        elif (kid[0].name == 'KW_CONTINUE'):
            self.loop_ctrl = 'continue'

    def run_action_stmt(self, jac_ast):
        """
        action_stmt:
            ignore_action
            | take_action
            | report_action
            | destroy_action;
        """
        kid = jac_ast.kid
        expr_func = getattr(self, f'run_{kid[0].name}')
        return expr_func(kid[0])

    def run_ignore_action(self, jac_ast):
        """
        ignore_action: KW_IGNORE expression SEMI;
        """
        kid = jac_ast.kid
        result = self.run_expression(kid[1])
        if (isinstance(result, node)):
            self.ignore_node_ids.add_obj(result)
        elif (isinstance(result, jac_set)):
            self.ignore_node_ids += result
        else:
            self.rt_error(f'{result} is not ignorable type (i.e., nodes)',
                          kid[1])

    def run_take_action(self, jac_ast):
        """
        take_action:
            KW_TAKE expression (SEMI | else_stmt);
        """
        kid = jac_ast.kid
        result = self.run_expression(kid[1])
        before = len(self.next_node_ids)
        if (isinstance(result, node)):
            self.next_node_ids.add_obj(result)
        elif (isinstance(result, jac_set)):
            self.next_node_ids += result
        elif(result):
            self.rt_error(f'{result} is not destination type (i.e., nodes)',
                          kid[1])
        after = len(self.next_node_ids)
        if (before >= after and kid[2].name == 'else_stmt'):
            self.run_else_stmt(kid[2])
        after = len(self.next_node_ids)
        # if(before >= after and not self.stopped == 'stop'):
        #     self.rt_info(f"Walker was unable to take any edge" +
        #                  f" - {self.current_node}", kid[0])

    def run_report_action(self, jac_ast):
        """
        report_action: KW_REPORT expression SEMI;
        """
        kid = jac_ast.kid
        report = self.run_expression(kid[1])
        report = self._jac_scope.report_deep_serialize(report)
        self.report.append(report)
        self.log_history('reports',
                         {'from': self.current_node.id.urn,
                             'index': len(self.report)})

    def run_destroy_action(self, jac_ast):
        """
        destroy_action: KW_DESTROY expression SEMI;
        """
        kid = jac_ast.kid
        result = self.run_expression(kid[1])
        if (isinstance(result, node)):
            self.destroy_node_ids.add_obj(result)
        elif (isinstance(result, jac_set)):
            for i in result:
                self.destroy_node_ids.add_obj(i)
        else:
            self.rt_error(f'{result} is not destroyable type (i.e., nodes)',
                          kid[1])

    def run_expression(self, jac_ast):
        """
        expression: assignment | connect;
        """
        kid = jac_ast.kid
        expr_func = getattr(self, f'run_{kid[0].name}')
        return expr_func(kid[0])

    def run_assignment(self, jac_ast, assign_scope=None):
        """
        assignment:
            dotted_name array_idx* EQ expression
            | inc_assign
            | copy_assign;

        NOTE: assign_scope used to override normal behavior for special assigns
        such as walker spawns. assign_scope must be id_list of contexts
        """
        kid = jac_ast.kid
        if (len(kid) < 2):
            if (assign_scope is not None):
                self.rt_error("Can only use '=' with spawn", kid[0])
            assign_func = getattr(self, f'run_{kid[0].name}')
            return assign_func(kid[0])
        var_name = self.run_dotted_name(kid[0])
        arr_idx = []
        for i in kid:
            if(i.name == 'array_idx'):
                arr_idx.append(self.run_array_idx(i))
        result = self.run_expression(kid[-1])
        if (assign_scope is None):
            self._jac_scope.set_live_var(var_name, result, arr_idx, kid[0])
        else:
            if(isinstance(result, element)):
                result = result.id.urn
            assign_scope[var_name] = result
        return result

    def run_inc_assign(self, jac_ast):
        """
        inc_assign:
                dotted_name array_idx* (PEQ | MEQ | TEQ | DEQ) expression;
        """
        kid = jac_ast.kid
        var_name = self.run_dotted_name(kid[0])
        arr_idx = []
        for i in kid:
            if(i.name == 'array_idx'):
                arr_idx.append(self.run_array_idx(i))
        result = self._jac_scope.get_live_var(var_name, kid[0])
        if(kid[1].name == 'PEQ'):
            result = result + self.run_expression(kid[2])
        elif(kid[1].name == 'MEQ'):
            result = result - self.run_expression(kid[2])
        elif(kid[1].name == 'TEQ'):
            result = result * self.run_expression(kid[2])
        elif(kid[1].name == 'DEQ'):
            result = result / self.run_expression(kid[2])
        self._jac_scope.set_live_var(var_name, result, arr_idx, kid[0])
        return result

    def run_copy_assign(self, jac_ast):
        """
        copy_assign: dotted_name array_idx* CPY_EQ expression;
        """
        kid = jac_ast.kid
        var_name = self.run_dotted_name(kid[0])
        dest = self._jac_scope.get_live_var(var_name, kid[0])
        for i in kid:
            if(i.name == 'array_idx'):
                dest = dest[self.run_array_idx(i)]
        src = self.run_expression(kid[2])
        if (not self.rt_check_type(dest, node, kid[0]) or not
                self.rt_check_type(dest, node, kid[0])):
            self.rt_error("':=' only applies to nodes", kid[0])
            return dest
        if (dest.kind != src.kind):
            self.rt_error(f"Node arch {dest} don't match {src}!", kid[0])
            return dest
        for i in src.context.keys():
            if(i in dest.context.keys()):
                dest.context[i] = src.context[i]
        return dest

    def run_connect(self, jac_ast):
        """
        connect: logical ( (NOT)? edge_ref expression)?;
        """
        kid = jac_ast.kid
        if (len(kid) < 2):
            return self.run_logical(kid[0])
        base = self.run_logical(kid[0])
        target = self.run_expression(kid[-1])
        self.rt_check_type(base, node, kid[0])
        self.rt_check_type(target, node, kid[-1])
        if (kid[1].name == 'NOT'):
            # Line below PARTIALLY generalizes disconnect NEEDS REVIEW
            if (isinstance(target, jac_set)):
                target = self.run_edge_ref(kid[2]) * target
            else:
                target = self.run_edge_ref(
                    kid[2]) * jac_set(self, [target.id.urn])
            if(target):  # HACK: if should always eval true REview later
                target = target.obj_list()[0]
                base.detach_outbound(target) if base.is_attached_out(
                    target) else base.detach_inbound(target)
            target = base
        else:
            use_edge = self.run_edge_ref(kid[1], is_spawn=True)
            direction = kid[1].kid[0].name
            if (direction == 'edge_from'):
                base.attach_inbound(target, use_edge)
            else:
                base.attach_outbound(target, use_edge)
        return target

    def run_logical(self, jac_ast):
        """
        logical: compare ((KW_AND | KW_OR) compare)*;
        """
        kid = jac_ast.kid
        result = self.run_compare(kid[0])
        kid = kid[1:]
        while (kid):
            if (kid[0].name == 'KW_AND'):
                if (result):
                    result = result and self.run_compare(kid[1])
            elif (kid[0].name == 'KW_OR'):
                if (not result):
                    result = result or self.run_compare(kid[1])
            kid = kid[2:]
            if(not kid):
                break
        return result

    def run_compare(self, jac_ast):
        """
        compare:
            NOT compare
            | arithmetic (
                (EE | LT | GT | LTE | GTE | NE | KW_IN | nin) arithmetic
            )*;
        """
        kid = jac_ast.kid
        if(kid[0].name == 'NOT'):
            return not self.run_compare(kid[1])
        else:
            result = self.run_arithmetic(kid[0])
            kid = kid[1:]
            while (kid):
                other_res = self.run_arithmetic(kid[1])
                if(kid[0].name == 'EE'):
                    result = result == other_res
                elif(kid[0].name == 'LT'):
                    result = result < other_res
                elif(kid[0].name == 'GT'):
                    result = result > other_res
                elif(kid[0].name == 'LTE'):
                    result = result <= other_res
                elif(kid[0].name == 'GTE'):
                    result = result >= other_res
                elif(kid[0].name == 'NE'):
                    result = result != other_res
                elif(kid[0].name == 'KW_IN'):
                    result = result in other_res
                elif(kid[0].name == 'nin'):
                    result = result not in other_res
                kid = kid[2:]
                if(not kid):
                    break
            return result

    def run_arithmetic(self, jac_ast):
        """
        arithmetic: term ((PLUS | MINUS) term)*;
        """
        kid = jac_ast.kid
        result = self.run_term(kid[0])
        kid = kid[1:]
        while (kid):
            other_res = self.run_term(kid[1])
            if(kid[0].name == 'PLUS'):
                result = result + other_res
            elif(kid[0].name == 'MINUS'):
                result = result - other_res
            kid = kid[2:]
            if(not kid):
                break
        return result

    def run_term(self, jac_ast):
        """
        term: factor ((MUL | DIV | MOD) factor)*;
        """
        kid = jac_ast.kid
        result = self.run_factor(kid[0])
        kid = kid[1:]
        while (kid):
            other_res = self.run_factor(kid[1])
            if(kid[0].name == 'MUL'):
                result = result * other_res
            elif(kid[0].name == 'DIV'):
                result = result / other_res
            elif(kid[0].name == 'MOD'):
                result = result % other_res
            kid = kid[2:]
            if(not kid):
                break
        return result

    def run_factor(self, jac_ast):
        """
        factor: (PLUS | MINUS) factor | power;
        """
        kid = jac_ast.kid
        if(kid[0].name == 'power'):
            return self.run_power(kid[0])
        else:
            result = self.run_factor(kid[1])
            if(kid[0].name == 'MINUS'):
                result = -(result)
            return result

    def run_power(self, jac_ast):
        """
        power: func_call (POW factor)*;
        """
        kid = jac_ast.kid
        result = self.run_func_call(kid[0])
        kid = kid[1:]
        while (kid):
            result = result ** self.run_factor(kid[1])
            kid = kid[2:]
            if(not kid):
                break
        return result

    def run_func_call(self, jac_ast):
        """
        func_call:
            atom (LPAREN (expression (COMMA expression)*)? RPAREN)?
            | atom DOT KW_LENGTH
            | atom DOT KW_DESTROY LPAREN expression RPAREN;
        TODO: Function defintions
        """
        kid = jac_ast.kid
        atom_res = self.run_atom(kid[0])
        if(len(kid) < 3):
            return atom_res
        elif (kid[2].name == "KW_LENGTH"):
            if(isinstance(atom_res, list)):
                return len(atom_res)
            else:
                self.rt_error(f'Cannot get length of {atom_res}. Not List!',
                              kid[0])
                return 0
        elif (kid[2].name == "KW_DESTROY"):
            idx = self.run_expression(kid[4])
            if (isinstance(atom_res, list) and isinstance(idx, int)):
                del atom_res[idx]
                return atom_res
            else:
                self.rt_error(f'Cannot remove index {idx} from {atom_res}.',
                              kid[0])
                return atom_res
        else:
            param_list = []
            kid = kid[2:]
            while True:
                if(kid[0].name == 'RPAREN'):
                    break
                param_list.append(self.run_expression(kid[0]))
                kid = kid[1:]
                if (kid[0].name == 'COMMA'):
                    kid = kid[1:]
            if (isinstance(atom_res, action)):
                return atom_res.trigger(param_list)
            else:
                self.rt_error(f'Unable to execute function {atom_res}',
                              kid[0])

    def run_atom(self, jac_ast):
        """
        atom:
            INT
            | FLOAT
            | STRING
            | BOOL
            | array_ref
            | attr_ref
            | node_ref
            | edge_ref (node_ref)? /* Returns nodes even if edge */
            | list_val
            | dotted_name
            | LPAREN expression RPAREN
            | spawn
            | DEREF expression;
        """
        kid = jac_ast.kid
        if(kid[0].name == 'INT'):
            return int(kid[0].token_text())
        elif(kid[0].name == 'FLOAT'):
            return float(kid[0].token_text())
        elif(kid[0].name == 'STRING'):
            return str(bytes(kid[0].token_text(), "utf-8").
                       decode("unicode_escape")[1:-1])
        elif(kid[0].name == 'BOOL'):
            return bool(kid[0].token_text() == 'true')
        elif (kid[0].name == 'edge_ref' and len(kid) > 1):
            res = self.run_edge_ref(kid[0]) * self.run_node_ref(kid[1])
            return res
        elif(kid[0].name == 'dotted_name'):
            return self._jac_scope.get_live_var(self.run_dotted_name(kid[0]),
                                                kid[0])
        elif(kid[0].name == 'LPAREN'):
            return self.run_expression(kid[1])
        elif (kid[0].name == 'DEREF'):
            result = self.run_expression(kid[1])
            if (self.rt_check_type(result, element, kid[1])):
                result = result.jid
            return result
        else:
            return getattr(self, f'run_{kid[0].name}')(kid[0])

    def run_array_ref(self, jac_ast):
        """
        array_ref: dotted_name array_idx+;
        """
        kid = jac_ast.kid
        item = self._jac_scope.get_live_var(self.run_dotted_name(kid[0]),
                                            kid[0])
        result = item
        for i in kid:
            if(i.name == 'array_idx'):
                result = result[self.run_array_idx(i)]
        return self._jac_scope.reference_to_value(result)

    def run_array_idx(self, jac_ast):
        """
        array_idx: LSQUARE expression RSQUARE;
        """
        kid = jac_ast.kid
        return self.run_expression(kid[1])

    def run_attr_ref(self, jac_ast):
        """
        attr_ref: dotted_name DBL_COLON dotted_name;
        """
        kid = jac_ast.kid
        item = self._jac_flow.get_live_var(self.run_dotted_name(kid[0]),
                                           kid[0])
        attr = self.run_dotted_name(kid[3])
        found = None
        if (isinstance(item, node) or isinstance(item, edge)):
            if(attr in item.context.keys()):
                found = item.context[attr]
            if(not found):
                found = item.activity_action_ids. \
                    get_obj_by_name(attr, silent=True)
            if(isinstance(item, node)):
                if(not found):
                    found = item.entry_action_ids. \
                        get_obj_by_name(attr, silent=True)
                if(not found):
                    found = item.exit_action_ids. \
                        get_obj_by_name(attr, silent=True)
        if(found):
            return found
        else:
            self.rt_error(f'Unable to find {attr} attribute of {item}',
                          kid[0])
            return None

    def run_node_ref(self, jac_ast, is_spawn=False):
        """
        node_ref: KW_NODE (DBL_COLON NAME)?;

        NOTE: is_spawn is used to determine whehter this is being called from
        a rule to generate new nodes, or describe nodes to grab from a location
        """
        kid = jac_ast.kid
        if(not is_spawn):
            result = jac_set(self.owner())
            if (len(kid) > 1):
                for i in self.viable_nodes().obj_list():
                    if (i.kind == kid[2].token_text()):
                        result.add_obj(i)
            else:
                result += self.viable_nodes()
        else:
            if(len(kid) > 1):
                result = self.owner().arch_ids.get_obj_by_name(
                    'node.' + kid[2].token_text()).run()
            else:
                result = node(h=self._h)
            self.log_history('spawned', result)
        return result

    def run_edge_ref(self, jac_ast, is_spawn=False):
        """
        edge_ref: edge_to | edge_from | edge_any;
        """
        kid = jac_ast.kid
        expr_func = getattr(self, f'run_{kid[0].name}')
        return expr_func(kid[0], is_spawn)

    def run_edge_to(self, jac_ast, is_spawn=False):
        """
        edge_to: '-' ('[' NAME ']')? '->';
        """
        kid = jac_ast.kid
        if (not is_spawn):
            result = jac_set(self.owner())
            if(len(kid) > 2):
                for i in self.current_node.outbound_nodes():
                    if (i.get_edge(self.current_node).kind ==
                            kid[2].token_text()):
                        result.add_obj(i)
            else:
                for i in self.current_node.outbound_nodes():
                    result.add_obj(i)
        else:
            if(len(kid) > 2):
                result = self.owner().arch_ids.get_obj_by_name(
                    'edge.' + kid[2].token_text()).run()
            else:
                result = edge(h=self._h)
            self.log_history('spawned', result)

        return result

    def run_edge_from(self, jac_ast, is_spawn=False):
        """
        edge_from: '<-' ('[' NAME ']')? '-';
        """
        kid = jac_ast.kid
        if (not is_spawn):
            result = jac_set(self.owner())
            if(len(kid) > 2):
                for i in self.current_node.inbound_nodes():
                    if (i.get_edge(self.current_node).kind ==
                            kid[2].token_text()):
                        result.add_obj(i)
            else:
                for i in self.current_node.inbound_nodes():
                    result.add_obj(i)
        else:
            if(len(kid) > 2):
                result = self.owner().arch_ids.get_obj_by_name(
                    'edge.' + kid[2].token_text()).run()
            else:
                result = edge(h=self._h)
            self.log_history('spawned', result)
        return result

    def run_edge_any(self, jac_ast, is_spawn=False):
        """
        edge_any: '<-' ('[' NAME ']')? '->';
        """
        kid = jac_ast.kid
        if (not is_spawn):
            result = jac_set(self.owner())
            if(len(kid) > 2):
                for i in self.current_node.attached_nodes():
                    if (i.get_edge(self.current_node).kind ==
                            kid[2].token_text()):
                        result.add_obj(i)
            else:
                for i in self.current_node.attached_nodes():
                    result.add_obj(i)
        else:
            if(len(kid) > 2):
                result = self.owner().arch_ids.get_obj_by_name(
                    'edge.' + kid[2].token_text()).run()
            else:
                result = edge(h=self._h)
            self.log_history('spawned', result)

        return result

    def run_list_val(self, jac_ast):
        """
        list_val: LSQUARE (expression (COMMA expression)*)? RSQUARE;
        """
        kid = jac_ast.kid
        list_res = []
        for i in kid:
            if(i.name == 'expression'):
                list_res.append(self.run_expression(i))
        return list_res

    def run_spawn(self, jac_ast):
        """
        spawn: KW_SPAWN expression spawn_object;

        NOTE: spawn statements support locations that are either nodes or
        jac_sets
        """
        kid = jac_ast.kid
        location = self.run_expression(kid[1])
        if(isinstance(location, node)):
            return self.run_spawn_object(kid[2], location)
        elif(isinstance(location, jac_set)):
            res = []
            for i in location.obj_list():
                res.append(self.run_spawn_object(kid[2], i))
            return res
        else:
            self.rt_error(f'Spawn can not occur on {type(location)}!', kid[1])
            return None

    def run_spawn_object(self, jac_ast, location):
        """
        spawn_object: node_spawn | walker_spawn;
        """
        kid = jac_ast.kid
        expr_func = getattr(self, f'run_{kid[0].name}')
        return expr_func(kid[0], location)

    def run_node_spawn(self, jac_ast, location):
        """
        node_spawn: edge_ref node_ref spawn_ctx?;
        """
        kid = jac_ast.kid
        use_edge = self.run_edge_ref(kid[0], is_spawn=True)
        ret_node = self.run_node_ref(kid[1], is_spawn=True)
        direction = kid[0].kid[0].name
        if (direction == 'edge_from'):
            location.attach_inbound(ret_node, use_edge)
        else:
            location.attach_outbound(ret_node, use_edge)
        if (len(kid) > 2):
            self.run_spawn_ctx(kid[2], ret_node)
        return ret_node

    def run_walker_spawn(self, jac_ast, location):
        """
        walker_spawn: KW_WALKER DBL_COLON NAME spawn_ctx?;
        """
        kid = jac_ast.kid
        src_walk = self.owner().walker_ids.get_obj_by_name(kid[2].token_text())
        self.rt_check_type(src_walk, type(self), kid[2])
        walk = src_walk.duplicate(persist_dup=False)
        walk._jac_ast = src_walk._jac_ast
        walk.prime(location)
        if(len(kid) > 3):
            self.run_spawn_ctx(kid[3], walk)
        walk.run()
        ret = self._jac_scope.reference_to_value(walk.anchor_value())
        self.report = self.report + walk.report
        walk.destroy()
        return ret

    # TODO: check this with JM
    def run_graph_spawn(self, jac_ast, location):
        """
        graph_spawn: KW_GRAPH DBL_COLON NAME;
        """
        kid = jac_ast.kid
        result = self.owner().arch_ids.get_obj_by_name('graph.' + kid[2].token_text()).run()
        self.log_history('spawned', result)
        return result

    def run_spawn_ctx(self, jac_ast, obj):
        """
        spawn_ctx: LPAREN (assignment (COMMA assignment)*)? RPAREN;
        """
        kid = jac_ast.kid
        for i in kid:
            if (i.name == 'assignment'):
                self.run_assignment(i, assign_scope=obj.context)

    # Helper Functions ##################

    def trigger_entry_actions(self):
        """Trigger current node actions on entry"""
        for i in self.current_node.entry_action_ids.obj_list():
            i.trigger()

    def trigger_activity_actions(self):
        """Trigger current node actions on activity"""
        for i in self.current_node.activity_action_ids.obj_list():
            i.trigger()

    def trigger_exit_actions(self):
        """Trigger current node actions on exit"""
        for i in self.current_node.exit_action_ids.obj_list():
            i.trigger()

    def viable_nodes(self):
        """Returns all nodes that shouldnt be ignored"""
        ret = jac_set(self.owner())
        for i in self.current_node.attached_nodes():
            if (i not in self.ignore_node_ids.obj_list()):
                ret.add_obj(i)
        return ret

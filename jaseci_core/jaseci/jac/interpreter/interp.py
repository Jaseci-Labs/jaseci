"""
Interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.utils.utils import is_jsonable, is_urn, parse_str_token
from jaseci.element.element import element
from jaseci.graph.node import node
from jaseci.graph.edge import edge
from jaseci.attr.action import action
from jaseci.jac.jac_set import jac_set
from jaseci.jac.ir.jac_code import jac_ast_to_ir, jac_ir_to_ast
from jaseci.jac.machine.jac_scope import jac_scope
from jaseci.jac.machine.machine_state import machine_state

from jaseci.jac.machine.jac_value import jac_value
from jaseci.jac.machine.jac_value import jac_elem_unwrap as jeu
from copy import copy


class interp(machine_state):
    """Shared interpreter class across both sentinels and walkers"""

    def run_attr_stmt(self, jac_ast, obj):
        """
        attr_stmt: has_stmt | can_stmt;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[0].name == 'has_stmt'):
            self.run_has_stmt(kid[0], obj)
        elif(kid[0].name == 'can_stmt'):
            if(obj.j_type == 'walker'):
                self.run_can_stmt(kid[0], obj)
            else:
                obj = self.get_arch_for(obj)
                if(not obj._can_compiled_flag):
                    self.run_can_stmt(kid[0], obj)

    def run_has_stmt(self, jac_ast, obj):
        """
        has_stmt:
                KW_HAS KW_PRIVATE? KW_ANCHOR? has_assign
                (COMMA has_assign)* SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        kid = kid[1:]
        is_private = False
        is_anchor = False
        while True:
            if(kid[0].name == 'KW_PRIVATE'):
                kid = kid[1:]
                is_private = True
            if(kid[0].name == 'KW_ANCHOR'):
                kid = kid[1:]
                is_anchor = True
            self.run_has_assign(kid[0], obj, is_private, is_anchor)
            kid = kid[1:]
            if(not len(kid) or kid[0].name != 'COMMA'):
                break
            else:
                kid = kid[1:]

    def run_has_assign(self, jac_ast, obj, is_private, is_anchor):
        """
        has_assign: NAME | NAME EQ expression;
        """
        kid = self.set_cur_ast(jac_ast)
        var_name = kid[0].token_text()
        var_val = None  # jac's null
        if(len(kid) > 1):
            var_val = self.run_expression(kid[2]).value
        if(is_anchor):
            if('anchor' in dir(obj)):
                if(obj.anchor is None):
                    obj.anchor = var_name
            else:
                self.rt_error('anchors not allowed for this type',
                              kid[0])

        if(var_name == '_private'):
            self.rt_error(
                f'Has variable name of `_private` not allowed!', kid[0])
        elif (var_name not in obj.context.keys()):  # Runs only once
            jac_value(self, ctx=obj,
                      name=var_name, value=var_val).write(kid[0], force=True)
        if(is_private):
            if('_private' in obj.context.keys()):
                if(var_name not in obj.context['_private']):
                    obj.context['_private'].append(var_name)
            else:
                obj.context['_private'] = [var_name]

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
        while True:
            action_type = 'activity'
            access_list = None
            preset_in_out = None
            if (kid[0].name == 'NAME'):
                action_name = kid[0].token_text()
            else:
                action_name = self.run_dotted_name(kid[0])
            kid = kid[1:]
            if(len(kid) > 0 and kid[0].name == 'preset_in_out'):
                preset_in_out = jac_ast_to_ir(kid[0])
                kid = kid[1:]
            if(len(kid) > 0 and kid[0].name == 'event_clause'):
                action_type, access_list = self.run_event_clause(kid[0])
                kid = kid[1:]
            # if (not isinstance(obj, node) and action_type != 'activity'):
            #     self.rt_warn(
            #         "Only nodes has on entry/exit, treating as activity",
            #         kid[0])
            #     action_type = 'activity'
            if (kid[0].name == 'code_block'):
                act = action(
                    m_id=self._m_id,
                    h=self._h,
                    name=action_name,
                    value=jac_ast_to_ir(kid[0]),
                    preset_in_out=preset_in_out,
                    access_list=access_list
                )
                getattr(obj, f"{action_type}_action_ids").add_obj(act)
                self._jac_scope.add_action(act)
                break
            else:
                func_link = \
                    self.get_builtin_action(action_name, jac_ast)
                if(func_link):
                    act = action(
                        m_id=self._m_id,
                        h=self._h,
                        name=action_name,
                        value=func_link,
                        preset_in_out=preset_in_out,
                        access_list=access_list
                    )
                    getattr(obj, f"{action_type}_action_ids").add_obj(act)
                    self._jac_scope.add_action(act)
            if(not len(kid) or kid[0].name != 'COMMA'):
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
        if(kid[1].name == "name_list"):
            nl = self.run_name_list(kid[1])
        return kid[-1].token_text(), nl

    def run_dotted_name(self, jac_ast):
        """
        dotted_name: NAME (DOT NAME)*;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = ''
        for i in kid:
            if(i.name == 'NAME'):
                ret += i.token_text()
                if(i == kid[-1]):
                    break
                ret += '.'
        return ret

    def run_name_list(self, jac_ast):
        """
        name_list: NAME (COMMA NAME)*;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = []
        for i in kid:
            if(i.name == 'NAME'):
                ret.append(i.token_text())
        return ret

    def run_expr_list(self, jac_ast, wrap=False):
        """
        expr_list: expression (COMMA expression)*;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = []
        for i in kid:
            if(i.name == 'expression'):
                if(wrap):
                    ret.append(self.run_expression(i).wrap())
                else:
                    ret.append(self.run_expression(i).value)
        return jac_value(self, value=ret)

    def run_code_block(self, jac_ast):
        """
        code_block: LBRACE statement* RBRACE | COLON statement;
        """
        kid = self.set_cur_ast(jac_ast)
        for i in kid:
            if(i.name == 'statement' and not self._loop_ctrl):
                self.run_statement(jac_ast=i)

    def run_statement(self, jac_ast):
        """
        statement:
            code_block
            | node_ctx_block
            | expression SEMI
            | if_stmt
            | try_stmt
            | for_stmt
            | while_stmt
            | assert_stmt SEMI
            | ctrl_stmt SEMI
            | destroy_action
            | report_action
            | walker_action;
        """
        if (self._stopped):
            return
        kid = self.set_cur_ast(jac_ast)
        self.run_rule(kid[0])

    def run_if_stmt(self, jac_ast):
        """
        if_stmt: KW_IF expression code_block elif_stmt* else_stmt?;
        """
        kid = self.set_cur_ast(jac_ast)
        if(self.run_expression(kid[1]).value):
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

    def run_try_stmt(self, jac_ast):
        """
        try_stmt: KW_TRY code_block else_from_try?;
        """
        kid = self.set_cur_ast(jac_ast)
        try:
            self.run_code_block(kid[1])
            return
        except Exception as e:
            if(len(kid) > 2):
                self.run_else_from_try(kid[2], e)

    def run_else_from_try(self, jac_ast, e):
        """
        else_from_try:
            KW_ELSE (LPAREN NAME RPAREN)? code_block
            | KW_ELSE (KW_WITH NAME)? code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        if(len(kid) > 2):
            jac_value(self, ctx=self._jac_scope.local_scope,
                      name=kid[2].token_text(),
                      value=self.jac_exception(e, jac_ast)).write(kid[2])
        self.run_code_block(kid[-1])

    def run_elif_stmt(self, jac_ast):
        """
        elif_stmt: KW_ELIF expression code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        if(self.run_expression(kid[1]).value):
            self.run_code_block(kid[2])
            return True
        else:
            return False

    def run_else_stmt(self, jac_ast):
        """
        else_stmt: KW_ELSE code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_code_block(kid[1])

    def run_for_stmt(self, jac_ast):
        """
        for_stmt:
            KW_FOR expression KW_TO expression KW_BY expression code_block
            | KW_FOR NAME KW_IN expression code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        loops = 0
        if(kid[1].name == 'expression'):
            self.run_expression(kid[1])
            while self.run_expression(kid[3]).value:
                self._loop_ctrl = None
                self.run_code_block(kid[6])
                self.run_expression(kid[5])
                loops += 1
                if (self._loop_ctrl and self._loop_ctrl == 'break'):
                    break
                self._loop_ctrl = None
                if(loops > self._loop_limit):
                    self.rt_error(f'Hit loop limit, breaking...', kid[0])
                    self._loop_ctrl = 'break'
        else:
            var = self._jac_scope.get_live_var(
                kid[1].token_text(), create_mode=True)
            lst = self.run_expression(kid[3]).value
            # should check that lst is list here
            if(not isinstance(lst, list)):
                self.rt_error('Not a list for iteration!', kid[3])
            for i in lst:
                var.value = i
                var.write(kid[1])
                self.run_code_block(kid[4])
                loops += 1
                if (self._loop_ctrl and self._loop_ctrl == 'break'):
                    break
                self._loop_ctrl = None
                if(loops > self._loop_limit):
                    self.rt_error(f'Hit loop limit, breaking...', kid[0])
                    self._loop_ctrl = 'break'

    def run_while_stmt(self, jac_ast):
        """
        while_stmt: KW_WHILE expression code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        loops = 0
        while self.run_expression(kid[1]).value:
            self.run_code_block(kid[2])
            loops += 1
            if (self._loop_ctrl and self._loop_ctrl == 'break'):
                break
            self._loop_ctrl = None
            if(loops > self._loop_limit):
                self.rt_error(f'Hit loop limit, breaking...', kid[0])
                self._loop_ctrl = 'break'

    def run_ctrl_stmt(self, jac_ast):
        """
        ctrl_stmt: KW_CONTINUE | KW_BREAK | KW_SKIP;
        """
        kid = self.set_cur_ast(jac_ast)
        if (kid[0].name == 'KW_SKIP'):
            self._stopped = 'skip'
        elif (kid[0].name == 'KW_BREAK'):
            self._loop_ctrl = 'break'
        elif (kid[0].name == 'KW_CONTINUE'):
            self._loop_ctrl = 'continue'

    def run_assert_stmt(self, jac_ast):
        """
        assert_stmt: KW_ASSERT expression;
        """
        kid = self.set_cur_ast(jac_ast)
        passed = False
        try:
            passed = self.run_expression(kid[1]).value
        except Exception as e:
            e = self.jac_exception(e, jac_ast)
            raise Exception('Jac Assert Failed', kid[1].get_text(), e)
        if(not passed):
            raise Exception('Jac Assert Failed', kid[1].get_text())

    def run_destroy_action(self, jac_ast):
        """
        destroy_action: KW_DESTROY expression SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        result = self.run_expression(kid[1])
        if (isinstance(result.value, element)):
            self.destroy_node_ids.add_obj(result.value)
        elif (isinstance(result.value, jac_set)):
            self.destroy_node_ids.add_obj_list(result.value)
        result.self_destruct(kid[1])

    def run_report_action(self, jac_ast):
        """
        report_action:
            KW_REPORT expression SEMI
            | KW_REPORT DOT NAME EQ INT SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[1].name == "DOT"):
            if(kid[2].token_text() in ['status', 'status_code']):
                self.report_status = int(kid[4].token_text())
            else:
                self.rt_error(f'Invalid report attribute to set', kid[2])
        else:
            report = self.run_expression(kid[1]).wrap(serialize_mode=True)
            if(not is_jsonable(report)):
                self.rt_error(f'Report not Json serializable', kid[0])
            self.report.append(copy(report))

    def run_expression(self, jac_ast):
        """
        expression: connect (assignment | copy_assign | inc_assign)?;
        """
        def check_can_write(val):
            if(val.ctx is None):
                self.rt_error("Cannot assign to this experssion", kid[0])
                return False
            return True
        kid = self.set_cur_ast(jac_ast)
        if(len(kid) == 1):
            return self.run_connect(kid[0])
        else:
            if(kid[1].name == "assignment"):
                self._assign_mode = True
                dest = self.run_connect(kid[0])
                self._assign_mode = False
                if(not check_can_write(dest)):
                    return dest
                return self.run_assignment(kid[1], dest=dest)
            elif(kid[1].name == "copy_assign"):
                dest = self.run_connect(kid[0])
                if(not check_can_write(dest)):
                    return dest
                return self.run_copy_assign(kid[1], dest=dest)
            elif(kid[1].name == "inc_assign"):
                dest = self.run_connect(kid[0])
                if(not check_can_write(dest)):
                    return dest
                return self.run_inc_assign(kid[1], dest=dest)

    def run_assignment(self, jac_ast, dest):
        """
        assignment: EQ expression;
        """
        kid = self.set_cur_ast(jac_ast)
        result = self.run_expression(kid[1])
        dest.value = result.value
        dest.write(jac_ast)
        return dest

    def run_copy_assign(self, jac_ast, dest):
        """
        copy_assign: CPY_EQ expression;
        """
        kid = self.set_cur_ast(jac_ast)
        src = self.run_expression(kid[1])
        if (not self.rt_check_type(dest.value, [node, edge], kid[1])):
            self.rt_error("':=' only applies to nodes and edges", kid[1])
            return dest
        if (dest.value.name != src.value.name):
            self.rt_error(
                f"Node/edge arch {dest.value} don't "
                f"match {src.value}!", kid[1])
            return dest
        for i in src.value.context.keys():
            if(i in dest.value.context.keys()):
                jac_value(self, ctx=dest.value, name=i,
                          value=src.value.context[i]).write(jac_ast)
        return dest

    def run_inc_assign(self, jac_ast, dest):
        """
        inc_assign: (PEQ | MEQ | TEQ | DEQ) expression;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[0].name == 'PEQ'):
            dest.value = dest.value + self.run_expression(kid[1]).value
        elif(kid[0].name == 'MEQ'):
            dest.value = dest.value - self.run_expression(kid[1]).value
        elif(kid[0].name == 'TEQ'):
            dest.value = dest.value * self.run_expression(kid[1]).value
        elif(kid[0].name == 'DEQ'):
            dest.value = dest.value / self.run_expression(kid[1]).value
        dest.write(jac_ast)
        return dest

    def run_connect(self, jac_ast):
        """
        connect: logical ( (NOT)? edge_ref expression)?;
        """
        kid = self.set_cur_ast(jac_ast)
        if (len(kid) < 2):
            return self.run_logical(kid[0])
        bret = self.run_logical(kid[0])
        base = bret.value
        tret = self.run_expression(kid[-1])
        target = tret.value
        self.rt_check_type(base, [node, jac_set], kid[0])
        self.rt_check_type(target, [node, jac_set], kid[-1])
        if(isinstance(base, node)):
            base = jac_set(in_list=[base])
        if(isinstance(target, node)):
            target = jac_set(in_list=[target])
        if (kid[1].name == 'NOT'):
            for i in target.obj_list():
                for j in base.obj_list():
                    j.detach_edges(i, self.run_edge_ref(kid[2]).obj_list())
            return bret
        else:
            direction = kid[1].kid[0].name
            for i in target.obj_list():
                for j in base.obj_list():
                    use_edge = self.run_edge_ref(kid[1], is_spawn=True)
                    if (direction == 'edge_from'):
                        j.attach_inbound(i, [use_edge])
                    elif (direction == 'edge_to'):
                        j.attach_outbound(i, [use_edge])
                    else:
                        j.attach_bidirected(i, [use_edge])
        return tret

    def run_logical(self, jac_ast):
        """
        logical: compare ((KW_AND | KW_OR) compare)*;
        """
        kid = self.set_cur_ast(jac_ast)
        result = self.run_compare(kid[0])
        kid = kid[1:]
        while (kid):
            if (kid[0].name == 'KW_AND'):
                if (result):
                    result.value = result.value and self.run_compare(
                        kid[1]).value
            elif (kid[0].name == 'KW_OR'):
                if (not result):
                    result.value = result.value or self.run_compare(
                        kid[1]).value
            kid = kid[2:]
            if(not kid):
                break
        return result

    def run_compare(self, jac_ast):
        """
        compare: NOT compare | arithmetic (cmp_op arithmetic)*;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[0].name == 'NOT'):
            return jac_value(self, value=not self.run_compare(kid[1]).value)
        else:
            result = self.run_arithmetic(kid[0])
            kid = kid[1:]
            while (kid):
                other_res = self.run_arithmetic(kid[1])
                result = self.run_cmp_op(
                    kid[0], result, other_res)
                kid = kid[2:]
                if(not kid):
                    break
            return result

    def run_cmp_op(self, jac_ast, val1, val2):
        """
        cmp_op: EE | LT | GT | LTE | GTE | NE | KW_IN | nin;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[0].name == 'EE'):
            return jac_value(self, value=val1.value == val2.value)
        elif(kid[0].name == 'LT'):
            return jac_value(self, value=val1.value < val2.value)
        elif(kid[0].name == 'GT'):
            return jac_value(self, value=val1.value > val2.value)
        elif(kid[0].name == 'LTE'):
            return jac_value(self, value=val1.value <= val2.value)
        elif(kid[0].name == 'GTE'):
            return jac_value(self, value=val1.value >= val2.value)
        elif(kid[0].name == 'NE'):
            return jac_value(self, value=val1.value != val2.value)
        elif(kid[0].name == 'KW_IN'):
            return jac_value(self, value=val1.value in val2.value)
        elif(kid[0].name == 'nin'):
            return jac_value(self, value=val1.value not in val2.value)

    def run_arithmetic(self, jac_ast):
        """
        arithmetic: term ((PLUS | MINUS) term)*;
        """
        kid = self.set_cur_ast(jac_ast)
        result = self.run_term(kid[0])
        kid = kid[1:]
        while (kid):
            other_res = self.run_term(kid[1])
            if(kid[0].name == 'PLUS'):
                result.value = result.value + other_res.value
            elif(kid[0].name == 'MINUS'):
                result.value = result.value - other_res.value
            kid = kid[2:]
            if(not kid):
                break
        return result

    def run_term(self, jac_ast):
        """
        term: factor ((STAR_MUL | DIV | MOD) factor)*;
        """
        kid = self.set_cur_ast(jac_ast)
        result = self.run_factor(kid[0])
        kid = kid[1:]
        while (kid):
            other_res = self.run_factor(kid[1])
            if(kid[0].name == 'STAR_MUL'):
                result.value = result.value * other_res.value
            elif(kid[0].name == 'DIV'):
                result.value = result.value / other_res.value
            elif(kid[0].name == 'MOD'):
                result.value = result.value % other_res.value
            kid = kid[2:]
            if(not kid):
                break
        return result

    def run_factor(self, jac_ast):
        """
        factor: (PLUS | MINUS) factor | power;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[0].name == 'power'):
            return self.run_power(kid[0])
        else:
            result = self.run_factor(kid[1])
            if(kid[0].name == 'MINUS'):
                result.value = -(result.value)
            return result

    def run_power(self, jac_ast):
        """
        power: atom (POW factor)*;
        """
        kid = self.set_cur_ast(jac_ast)
        result = self.run_atom(kid[0])
        kid = kid[1:]
        if(len(kid) < 1):
            return result
        elif(kid[0].name == 'POW'):
            while (kid):
                result.value = result.value ** self.run_factor(kid[1]).value
                kid = kid[2:]
                if(not kid):
                    break
            return result

    def run_atom(self, jac_ast):
        """
        atom:
            INT
            | FLOAT
            | STRING
            | BOOL
            | NULL
            | NAME
            | node_edge_ref
            | list_val
            | dict_val
            | LPAREN expression RPAREN
            | DBL_COLON NAME spawn_ctx?
            | atom atom_trailer+
            | spawn
            | ref
            | deref
            | any_type;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[0].name == 'INT'):
            return jac_value(self, value=int(kid[0].token_text()))
        elif(kid[0].name == 'FLOAT'):
            return jac_value(self, value=float(kid[0].token_text()))
        elif(kid[0].name == 'STRING'):
            return jac_value(
                self, value=parse_str_token(kid[0].token_text()))
        elif(kid[0].name == 'BOOL'):
            return jac_value(self, value=bool(kid[0].token_text() == 'true'))
        elif(kid[0].name == 'NULL'):
            return jac_value(self, value=None)
        elif(kid[0].name == 'NAME'):
            name = kid[0].token_text()
            val = self._jac_scope.get_live_var(
                name, create_mode=self._assign_mode)
            if(val is None):
                self.rt_error(f"Variable not defined - {name}", kid[0])
                return jac_value(self, )
            return val
        elif(kid[0].name == 'LPAREN'):
            return self.run_expression(kid[1])
        elif(kid[0].name == 'DBL_COLON'):
            return self.run_atom_trailer(jac_ast, None)
        elif(kid[0].name == 'atom'):
            ret = self.run_atom(kid[0])
            for i in kid[1:]:
                ret = self.run_atom_trailer(i, ret)
            return ret
        else:
            return self.run_rule(kid[0])

    def run_atom_trailer(self, jac_ast, atom_res):
        """
        atom_trailer:
            DOT built_in
            | DOT NAME
            | index_slice
            | LPAREN expr_list? RPAREN
            | DBL_COLON NAME spawn_ctx?;
        """
        kid = self.set_cur_ast(jac_ast)
        if(atom_res is None):
            atom_res = jac_value(self, value=self._jac_scope.has_obj)
        if(kid[0].name == 'DOT'):
            if(kid[1].name == 'built_in'):

                return self.run_built_in(kid[1], atom_res)
            elif(kid[1].name == 'NAME'):
                d = atom_res.value
                n = kid[1].token_text()
                if(self.rt_check_type(d, [dict, element], kid[0])):
                    ret = jac_value(self, ctx=d, name=n)
                    ret.unwrap()
                    return ret
                else:
                    self.rt_error(f"Invalid variable {n}", kid[0])
        elif (kid[0].name == "index_slice"):
            if(not self.rt_check_type(
                    atom_res.value, [list, str, dict], kid[0])):
                return atom_res
            return self.run_index_slice(kid[0], atom_res)
        elif(kid[0].name == "LPAREN"):
            param_list = []
            if(kid[1].name == 'expr_list'):
                param_list = self.run_expr_list(kid[1]).value
            if (isinstance(atom_res.value, action)):
                try:
                    ret = atom_res.value.trigger(
                        param_list, self._jac_scope, self)
                except Exception as e:
                    self.rt_error(f'{e}', jac_ast)
                    ret = None
                return jac_value(self, value=ret)
            else:
                self.rt_error(f'Unable to execute ability',
                              kid[0])
        elif (kid[0].name == 'DBL_COLON'):
            if(len(kid) > 2):
                self.run_spawn_ctx(kid[2], atom_res.value)
            arch = self.get_arch_for(atom_res.value)
            self.call_ability(
                nd=atom_res.value,
                name=kid[1].token_text(),
                act_list=arch.activity_action_ids)
            return atom_res

    def run_ref(self, jac_ast):
        """
        ref: '&' expression;
        """
        kid = self.set_cur_ast(jac_ast)
        result = self.run_expression(kid[1])
        if (self.rt_check_type(result.value, element, kid[1])):
            result = jac_value(self, value=result.value.jid)
        return result

    def run_deref(self, jac_ast):
        """
        deref: '*' expression;
        """
        kid = self.set_cur_ast(jac_ast)
        result = self.run_expression(kid[1])
        if (is_urn(result.value)):
            result = jac_value(
                self, value=jeu(result.value.replace('urn', 'jac'), self))
        else:
            self.rt_error(f'{result.value} not valid reference', kid[1])
        return result

    def run_built_in(self, jac_ast, atom_res):
        """
        built_in:
            cast_built_in
            | obj_built_in
            | dict_built_in
            | list_built_in
            | string_built_in;
        """
        return self.run_rule(jac_ast.kid[0], atom_res)

    def run_cast_built_in(self, jac_ast, atom_res):
        """
        arch_built_in: any_type;
        """
        kid = self.set_cur_ast(jac_ast)
        typ = self.run_any_type(kid[0])
        if (typ.value == edge):
            if(isinstance(atom_res.value, node)):
                return jac_value(self, value=self.obj_set_to_jac_set(
                    self.current_node.attached_edges(atom_res.value)))
            elif(isinstance(atom_res.value, edge)):
                return atom_res
            elif(isinstance(atom_res.value, jac_set)):
                res = jac_set()
                for i in atom_res.value.obj_list():
                    if(isinstance(i, edge)):
                        res.add_obj(i)
                    elif(isinstance(i, node)):
                        res += self.obj_set_to_jac_set(
                            self.current_node.attached_edges(i))
                return jac_value(self, value=res)
            else:
                self.rt_error(f'Cannot get edges from {atom_res.value}. '
                              f'Type {atom_res.jac_type()} invalid', kid[0])
        # may want to remove 'here" node from return below
        elif (typ.value == node):
            if(isinstance(atom_res.value, node)):
                return atom_res
            elif(isinstance(atom_res.value, edge)):
                return jac_value(self, value=self.obj_set_to_jac_set(
                    atom_res.nodes()))
            elif(isinstance(atom_res.value, jac_set)):
                res = jac_set()
                for i in atom_res.value.obj_list():
                    if(isinstance(i, edge)):
                        res.add_obj(i.to_node())
                        res.add_obj(i.from_node())
                    elif(isinstance(i, node)):
                        res.add_obj(i)
                return jac_value(self, value=res)
            else:
                self.rt_error(f'Cannot get nodes from {atom_res}. '
                              f'Type {atom_res.jac_type()} invalid', kid[0])
        else:
            try:
                atom_res.value = typ.value(atom_res.value)
            except Exception:
                self.rt_error(
                    f'Invalid cast of {atom_res.jac_type()} '
                    f'to {typ.wrap()}', kid[0])
            return atom_res

        return atom_res

    def run_obj_built_in(self, jac_ast, atom_res):
        """
        obj_built_in: KW_CONTEXT | KW_INFO | KW_DETAILS;
        """
        kid = self.set_cur_ast(jac_ast)
        from jaseci.actor.walker import walker
        if (kid[0].name == "KW_CONTEXT"):
            if(self.rt_check_type(atom_res.value,
                                  [node, edge, walker], kid[0])):
                return jac_value(self, value=atom_res.value.context)
        elif (kid[0].name == "KW_INFO"):
            if(self.rt_check_type(atom_res.value,
                                  [node, edge, walker], kid[0])):
                return jac_value(
                    self, value=atom_res.value.serialize(detailed=False))
        elif (kid[0].name == "KW_DETAILS"):
            if(self.rt_check_type(atom_res.value,
                                  [node, edge, walker], kid[0])):
                return jac_value(
                    self, value=atom_res.value.serialize(detailed=True))
        return atom_res

    def run_dict_built_in(self, jac_ast, atom_res):
        """
        dict_built_in:
            KW_KEYS
            | LBRACE name_list RBRACE
            | (TYP_DICT DBL_COLON | DICT_DBL_COLON) NAME (
                LPAREN expr_list RPAREN
            )?;
        """
        kid = self.set_cur_ast(jac_ast)
        if (kid[0].name == "KW_KEYS"):
            if(isinstance(atom_res.value, dict)):
                return jac_value(self, value=list(atom_res.value.keys()))
            else:
                self.rt_error(f'Cannot get keys of {atom_res}. '
                              f'Not Dictionary!', kid[0])
                return jac_value(self, value=[])
        elif(len(kid) > 1 and kid[1].name == 'name_list'):
            filter_on = self.run_name_list(kid[1])
            d = atom_res.value
            if(self.rt_check_type(d, [dict], kid[0])):
                d = {k: d[k] for k in d if k in filter_on}
                return jac_value(self, value=d)
        else:
            if(not self.rt_check_type(atom_res.value, [dict], kid[0])):
                return atom_res
            kid = kid[1:]
            if(kid[0].name == "DBL_COLON"):
                kid = kid[1:]
            result = None
            op = kid[0].token_text()
            try:
                if (op == "items"):
                    result = jac_value(self, value=list(
                        map(list, atom_res.value.items())))
                elif (op == "copy"):
                    result = jac_value(self, value=atom_res.value.copy())
                elif (op == "keys"):
                    result = jac_value(self, value=list(atom_res.value.keys()))
                elif (op == "clear"):
                    result = jac_value(self, value=atom_res.value.clear())
                elif (op == "popitem"):
                    result = jac_value(self, value=list(
                        atom_res.value.popitem()))
                elif (op == "values"):
                    result = jac_value(self, value=list(
                        atom_res.value.values()))
                if (result):
                    if(len(kid) > 1):
                        self.rt_warn(
                            f"{op} does not take parameters, ignoring", kid[2])
                    return result
                if(len(kid) > 1):
                    args = self.run_expr_list(kid[2]).value
                    if (op == "pop"):
                        result = jac_value(
                            self, value=atom_res.value.pop(*args))
                    elif (op == "update"):
                        result = jac_value(
                            self, value=atom_res.value.update(*args))
                    if (result):
                        return result
            except Exception as e:
                self.rt_error(f'{e}', jac_ast)
            self.rt_error(f'Call to {op} is invalid.', jac_ast)

        return atom_res

    def run_list_built_in(self, jac_ast, atom_res):
        """
        list_built_in:
            KW_LENGTH
            | (TYP_LIST DBL_COLON | LIST_DBL_COLON) NAME (
                LPAREN expr_list RPAREN
            )?;
        """
        kid = self.set_cur_ast(jac_ast)
        if (kid[0].name == "KW_LENGTH"):
            if(isinstance(atom_res.value, list)):
                return jac_value(self, value=len(atom_res.value))
            else:
                self.rt_error(
                    f'Cannot get length of {atom_res.value}. Not List!',
                    kid[0])
                return jac_value(self, value=0)
        else:
            if(not self.rt_check_type(atom_res.value, [list], kid[0])):
                return atom_res
            kid = kid[1:]
            if(kid[0].name == "DBL_COLON"):
                kid = kid[1:]
            result = None
            op = kid[0].token_text()
            try:
                if (op == "reverse"):
                    result = jac_value(self, value=atom_res.value.reverse())
                elif (op == "copy"):
                    result = jac_value(self, value=atom_res.value.copy())
                elif (op == "sort"):
                    result = jac_value(self, value=atom_res.value.sort())
                elif (op == "clear"):
                    result = jac_value(self, value=atom_res.value.clear())
                elif (len(kid) < 2 and op == "pop"):
                    result = jac_value(self, value=atom_res.value.pop())
                if (result):
                    if(len(kid) > 1):
                        self.rt_warn(
                            f"{op} does not take parameters, ignoring", kid[2])
                    return result
                if(len(kid) > 1):
                    args = self.run_expr_list(kid[2]).value
                    if (op == "index"):
                        result = jac_value(
                            self, value=atom_res.value.index(*args))
                    elif (op == "append"):
                        result = jac_value(
                            self, value=atom_res.value.append(*args))
                    elif (op == "extend"):
                        result = jac_value(
                            self, value=atom_res.value.extend(*args))
                    elif (op == "insert"):
                        result = jac_value(
                            self, value=atom_res.value.insert(*args))
                    elif (op == "remove"):
                        result = jac_value(
                            self, value=atom_res.value.remove(*args))
                    elif (op == "count"):
                        result = jac_value(
                            self, value=atom_res.value.count(*args))
                    elif (op == "pop"):
                        result = jac_value(
                            self, value=atom_res.value.pop(*args))
                    if (result):
                        return result
            except Exception as e:
                self.rt_error(f'{e}', jac_ast)
            self.rt_error(f'Call to {op} is invalid.', jac_ast)
        return atom_res

    def run_string_built_in(self, jac_ast, atom_res):
        """
        string_built_in:
        (TYP_STRING DBL_COLON | STR_DBL_COLON) NAME (
                LPAREN expr_list RPAREN
        )?;
        """
        kid = self.set_cur_ast(jac_ast)
        if(not self.rt_check_type(atom_res.value, [str], kid[0])):
            return atom_res
        kid = kid[1:]
        if(kid[0].name == "DBL_COLON"):
            kid = kid[1:]
        result = None
        str_op = kid[0].token_text()
        try:
            if (str_op == "upper"):
                result = jac_value(self, value=atom_res.value.upper())
            elif (str_op == "lower"):
                result = jac_value(self, value=atom_res.value.lower())
            elif (str_op == "title"):
                result = jac_value(self, value=atom_res.value.title())
            elif (str_op == "capitalize"):
                result = jac_value(self, value=atom_res.value.capitalize())
            elif (str_op == "swap_case"):
                result = jac_value(self, value=atom_res.value.swapcase())
            elif (str_op == "is_alnum"):
                result = jac_value(self, value=atom_res.value.isalnum())
            elif (str_op == "is_alpha"):
                result = jac_value(self, value=atom_res.value.isalpha())
            elif (str_op == "is_digit"):
                result = jac_value(self, value=atom_res.value.isdigit())
            elif (str_op == "is_title"):
                result = jac_value(self, value=atom_res.value.istitle())
            elif (str_op == "is_upper"):
                result = jac_value(self, value=atom_res.value.isupper())
            elif (str_op == "is_lower"):
                result = jac_value(self, value=atom_res.value.islower())
            elif (str_op == "is_space"):
                result = jac_value(self, value=atom_res.value.isspace())
            elif (str_op == "load_json"):
                import json
                result = jac_value(self, value=json.loads(atom_res.value))
            elif (len(kid) < 2 and str_op == "split"):
                result = jac_value(self, value=atom_res.value.split())
            elif (len(kid) < 2 and str_op == "strip"):
                result = jac_value(self, value=atom_res.value.strip())
            elif (len(kid) < 2 and str_op == "lstrip"):
                result = jac_value(self, value=atom_res.value.lstrip())
            elif (len(kid) < 2 and str_op == "rstrip"):
                result = jac_value(self, value=atom_res.value.rstrip())
            if (result):
                if(len(kid) > 1):
                    self.rt_warn(
                        f"{str_op} does not take parameters, ignoring", kid[2])
                return result
            if(len(kid) > 1):
                args = self.run_expr_list(kid[2]).value
                if (str_op == "count"):
                    result = jac_value(self, value=atom_res.value.count(*args))
                elif (str_op == "find"):
                    result = jac_value(self, value=atom_res.value.find(*args))
                elif (str_op == "split"):
                    result = jac_value(self, value=atom_res.value.split(*args))
                elif (str_op == "join"):
                    result = jac_value(self, value=atom_res.value.join(*args))
                elif (str_op == "startswith"):
                    result = jac_value(
                        self, value=atom_res.value.startswith(*args))
                elif (str_op == "endswith"):
                    result = jac_value(
                        self, value=atom_res.value.endswith(*args))
                elif (str_op == "replace"):
                    result = jac_value(
                        self, value=atom_res.value.replace(*args))
                elif (str_op == "strip"):
                    result = jac_value(self, value=atom_res.value.strip(*args))
                elif (str_op == "lstrip"):
                    result = jac_value(
                        self, value=atom_res.value.lstrip(*args))
                elif (str_op == "rstrip"):
                    result = jac_value(
                        self, value=atom_res.value.rstrip(*args))
                if (result):
                    return result
        except Exception as e:
            self.rt_error(f'{e}', jac_ast)
        self.rt_error(f'Call to {str_op} is invalid.', jac_ast)
        return atom_res

    def run_node_edge_ref(self, jac_ast):
        """
        node_edge_ref:
            node_ref filter_ctx?
            | edge_ref (node_ref filter_ctx?)?;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[0].name == 'node_ref'):
            result = self.run_node_ref(kid[0])
            if(len(kid) > 1):
                result = self.run_filter_ctx(kid[1], result)
            return jac_value(self, value=result)

        elif (kid[0].name == 'edge_ref'):
            result = self.edge_to_node_jac_set(self.run_edge_ref(kid[0]))
            if(len(kid) > 1 and kid[1].name == 'node_ref'):
                nres = self.run_node_ref(kid[1])
                if(len(kid) > 2):
                    nres = self.run_filter_ctx(kid[2], nres)
                result = result * nres
            return jac_value(self, value=result)

    def run_node_ref(self, jac_ast, is_spawn=False):
        """
        node_ref: KW_NODE DBL_COLON NAME;
        """
        kid = self.set_cur_ast(jac_ast)
        if(not is_spawn):
            result = jac_set()
            if (len(kid) > 1):
                for i in self.viable_nodes().obj_list():
                    if (i.name == kid[2].token_text()):
                        result.add_obj(i)
            else:
                result += self.viable_nodes()
        else:
            result = self.parent().run_architype(
                kid[2].token_text(), kind='node', caller=self)
        return result

    def run_walker_ref(self, jac_ast):
        """
        walker_ref: KW_WALKER DBL_COLON NAME;
        """
        kid = self.set_cur_ast(jac_ast)
        return self.parent().spawn_walker(kid[2].token_text(), caller=self)

    def run_graph_ref(self, jac_ast):
        """
        graph_ref: KW_GRAPH DBL_COLON NAME;
        """
        kid = self.set_cur_ast(jac_ast)
        gph = self.parent().run_architype(
            kid[2].token_text(), kind='graph', caller=self)
        return gph

    def run_edge_ref(self, jac_ast, is_spawn=False):
        """
        edge_ref: edge_to | edge_from | edge_any;
        """
        kid = self.set_cur_ast(jac_ast)
        if(not is_spawn):
            return self.run_rule(kid[0])
        else:
            if(len(kid[0].kid) > 2):
                result = self.parent().run_architype(
                    kid[0].kid[2].token_text(), kind='edge',
                    caller=self)
                if(kid[0].kid[3].name == 'spawn_ctx'):
                    self.run_spawn_ctx(kid[0].kid[3], result)
                elif(kid[0].kid[3].name == 'filter_ctx'):
                    self.rt_error("Filtering not allowed here", kid[0].kid[3])
            else:
                result = edge(m_id=self._m_id, h=self._h,
                              kind='edge', name='generic')
            return result

    def run_edge_to(self, jac_ast):
        """
        edge_to:
            '-->'
            | '-' ('[' NAME (spawn_ctx | filter_ctx)? ']')? '->';
        """
        kid = self.set_cur_ast(jac_ast)
        result = jac_set()
        for i in self.current_node.outbound_edges() + \
                self.current_node.bidirected_edges():
            if (len(kid) > 2 and i.name != kid[2].token_text()):
                continue
            result.add_obj(i)
        if(len(kid) > 2 and kid[3].name == 'filter_ctx'):
            result = self.run_filter_ctx(kid[3], result)
        elif(len(kid) > 2 and kid[3].name == 'spawn_ctx'):
            self.rt_error("Assigning values not allowed here", kid[3])
        return result

    def run_edge_from(self, jac_ast):
        """
        edge_from:
            '<--'
            | '<-' ('[' NAME (spawn_ctx | filter_ctx)? ']')? '-';
        """
        kid = self.set_cur_ast(jac_ast)
        result = jac_set()
        for i in self.current_node.inbound_edges() + \
                self.current_node.bidirected_edges():
            if (len(kid) > 2 and i.name != kid[2].token_text()):
                continue
            result.add_obj(i)
        if(len(kid) > 2 and kid[3].name == 'filter_ctx'):
            result = self.run_filter_ctx(kid[3], result)
        elif(len(kid) > 2 and kid[3].name == 'spawn_ctx'):
            self.rt_error("Assigning values not allowed here", kid[3])
        return result

    def run_edge_any(self, jac_ast):
        """
        edge_any:
            '<-->'
            | '<-' ('[' NAME (spawn_ctx | filter_ctx)? ']')? '->';
        NOTE: these do not use strict bidirected semantic but any edge
        """
        kid = self.set_cur_ast(jac_ast)
        result = jac_set()
        for i in self.current_node.attached_edges():
            if (len(kid) > 2 and i.name != kid[2].token_text()):
                continue
            result.add_obj(i)
        if(len(kid) > 2 and kid[3].name == 'filter_ctx'):
            result = self.run_filter_ctx(kid[3], result)
        elif(len(kid) > 2 and kid[3].name == 'spawn_ctx'):
            self.rt_error("Assigning values not allowed here", kid[3])
        return result

    def run_list_val(self, jac_ast):
        """
        list_val: LSQUARE expr_list? RSQUARE;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[1].name == "expr_list"):
            return self.run_expr_list(kid[1])
        return jac_value(self, value=[])

    def run_index_slice(self, jac_ast, atom_res):
        """
        index_slice:
            LSQUARE expression RSQUARE
            | LSQUARE expression COLON expression RSQUARE;
        """
        kid = self.set_cur_ast(jac_ast)
        idx = self.run_expression(kid[1]).value
        if(type(idx) == str and idx not in atom_res.value.keys() and
           not self._assign_mode):
            self.rt_error(f'Key {idx} not found in object/dict.', kid[1])
        if(kid[2].name == "RSQUARE"):
            if(not self.rt_check_type(idx, [int, str], kid[1])):
                self.rt_error(
                    f'Index of type {type(idx)} not valid. '
                    f'Indicies must be an integer or string!', kid[1])
                return atom_res
            atom_res.unwrap()
            try:
                return jac_value(self, ctx=atom_res.value, name=idx)
            except Exception:
                self.rt_error("List index out of range", kid[1])
                return atom_res
        else:
            end = self.run_expression(kid[3]).value
            if(not self.rt_check_type(idx, [int], kid[1]) or
               not self.rt_check_type(end, [int], kid[3])):
                self.rt_error('List slice range not valid. '
                              'Indicies must be an integers!', kid[1])
                return atom_res
            atom_res.unwrap()
            try:
                return jac_value(self, ctx=atom_res.value, name=idx, end=end)
            except Exception:
                self.rt_error("List slice out of range", kid[1])
                return atom_res

    def run_dict_val(self, jac_ast):
        """
        dict_val: LBRACE (kv_pair (COMMA kv_pair)*)? RBRACE;
        """
        kid = self.set_cur_ast(jac_ast)
        dict_res = {}
        for i in kid:
            if(i.name == 'kv_pair'):
                self.run_kv_pair(i, dict_res)
        return jac_value(self, value=dict_res)

    def run_kv_pair(self, jac_ast, obj):
        """
        kv_pair: STRING COLON expression;
        """
        kid = self.set_cur_ast(jac_ast)
        obj[parse_str_token(kid[0].token_text())
            ] = self.run_expression(kid[2]).value

    def run_spawn(self, jac_ast):
        """
        spawn: KW_SPAWN expression spawn_object;

        NOTE: spawn statements support locations that are either nodes or
        jac_sets
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[1].name == 'expression'):
            location = self.run_expression(kid[1]).value
            if(isinstance(location, node)):
                return self.run_spawn_object(kid[2], location)
            elif(isinstance(location, jac_set)):
                res = []
                for i in location.obj_list():
                    res.append(self.run_spawn_object(kid[2], i))
                return jac_value(self, value=res)
            else:
                self.rt_error(
                    f'Spawn can not occur on {type(location)}!', kid[1])
        else:
            return self.run_spawn_object(kid[1], None)

    def run_spawn_object(self, jac_ast, location):
        """
        spawn_object: node_spawn | walker_spawn;
        """
        kid = self.set_cur_ast(jac_ast)
        return self.run_rule(kid[0], location)

    def run_node_spawn(self, jac_ast, location):
        """
        node_spawn: edge_ref? node_ref spawn_ctx?;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[0].name == 'node_ref'):
            ret_node = self.run_node_ref(kid[0], is_spawn=True)
        else:
            use_edge = self.run_edge_ref(kid[0], is_spawn=True)
            ret_node = self.run_node_ref(kid[1], is_spawn=True)
            direction = kid[0].kid[0].name
            if (direction == 'edge_from'):
                location.attach_inbound(ret_node, [use_edge])
            elif (direction == 'edge_to'):
                location.attach_outbound(ret_node, [use_edge])
            else:
                location.attach_bidirected(ret_node, [use_edge])
        if (kid[-1].name == 'spawn_ctx'):
            self.run_spawn_ctx(kid[-1], ret_node)
        return jac_value(self, value=ret_node)

    def run_walker_spawn(self, jac_ast, location):
        """
        walker_spawn: walker_ref spawn_ctx?;
        """
        kid = self.set_cur_ast(jac_ast)
        walk = self.run_walker_ref(kid[0])
        walk.prime(location)
        if(len(kid) > 1):
            self.run_spawn_ctx(kid[1], walk)
        walk.run()
        ret = jac_value(self, value=walk.anchor_value())
        ret.unwrap()
        self.report += walk.report
        if(walk.report_status):
            self.report_status = walk.report_status
        self.runtime_errors += walk.runtime_errors
        walk.destroy()
        return ret

    def run_graph_spawn(self, jac_ast, location):
        """
        graph_spawn: edge_ref graph_ref;
        """
        kid = self.set_cur_ast(jac_ast)
        use_edge = self.run_edge_ref(kid[0], is_spawn=True)
        result = self.run_graph_ref(kid[1])
        direction = kid[0].kid[0].name
        if (direction == 'edge_from'):
            location.attach_inbound(result, [use_edge])
        elif (direction == 'edge_to'):
            location.attach_outbound(result, [use_edge])
        else:
            location.attach_bidirected(result, [use_edge])
        return jac_value(self, value=result)

    def run_spawn_ctx(self, jac_ast, obj):
        """
        spawn_ctx: LPAREN (spawn_assign (COMMA spawn_assign)*)? RPAREN;
        """
        kid = self.set_cur_ast(jac_ast)
        for i in kid:
            if (i.name == 'spawn_assign'):
                self.run_spawn_assign(i, obj)

    def run_filter_ctx(self, jac_ast, obj):
        """
        filter_ctx:
                LPAREN (filter_compare (COMMA filter_compare)*)? RPAREN;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = jac_set()
        for i in obj.obj_list():
            for j in kid:
                if (j.name == 'filter_compare'):
                    if(self.run_filter_compare(j, i)):
                        ret.add_obj(i)
        return ret

    def run_spawn_assign(self, jac_ast, obj):
        """
        spawn_assign: NAME EQ expression;
        """
        kid = self.set_cur_ast(jac_ast)
        name = kid[0].token_text()
        result = self.run_expression(kid[-1]).value
        dest = jac_value(self, ctx=obj, name=name, value=result)
        if(obj.j_type == 'walker'):
            dest.write(kid[0], force=True)
        else:
            dest.write(kid[0])

    def run_filter_compare(self, jac_ast, obj):
        """
        filter_compare: NAME cmp_op expression;
        """
        kid = self.set_cur_ast(jac_ast)
        name = kid[0].token_text()
        if(name in obj.context.keys()):
            result = self.run_expression(kid[-1])
            return self.run_cmp_op(
                kid[1], jac_value(self, ctx=obj, name=name),
                result).value
        else:
            self.rt_error(f'{name} not present in object', kid[0])
            return False

    def run_any_type(self, jac_ast):
        """
        any_type:
            TYP_STRING
            | TYP_INT
            | TYP_FLOAT
            | TYP_LIST
            | TYP_DICT
            | TYP_BOOL
            | KW_NODE
            | KW_EDGE
            | KW_TYPE;
        """
        kid = self.set_cur_ast(jac_ast)
        if(kid[0].name == "TYP_STRING"):
            return jac_value(self, value=str)
        elif(kid[0].name == "TYP_INT"):
            return jac_value(self, value=int)
        elif(kid[0].name == "TYP_FLOAT"):
            return jac_value(self, value=float)
        elif(kid[0].name == "TYP_LIST"):
            return jac_value(self, value=list)
        elif(kid[0].name == "TYP_DICT"):
            return jac_value(self, value=dict)
        elif(kid[0].name == "TYP_BOOL"):
            return jac_value(self, value=bool)
        elif(kid[0].name == "KW_NODE"):
            return jac_value(self, value=node)
        elif(kid[0].name == "KW_EDGE"):
            return jac_value(self, value=edge)
        elif(kid[0].name == "KW_TYPE"):
            return jac_value(self, value=type)
        else:
            self.rt_error('Unrecognized type', kid[0])

    # Helper Functions ##################

    def call_ability(self, nd, name, act_list):
        m = interp(parent_override=self.parent(), caller=self)
        arch = self.get_arch_for(nd)
        m.push_scope(jac_scope(parent=nd,
                               has_obj=nd,
                               action_sets=[arch.activity_action_ids]))
        m._jac_scope.inherit_agent_refs(self._jac_scope)
        m.run_code_block(jac_ir_to_ast(
            act_list.get_obj_by_name(name).value))
        self.report += m.report
        if(m.report_status):
            self.report_status = m.report_status
        self.runtime_errors += m.runtime_errors

    def run_rule(self, jac_ast, *args):
        """Helper to run rule if exists in execution context"""
        # try:
        # if(not hasattr(self, f'run_{jac_ast.name}')):
        #     self.rt_error(
        #         f'This scope cannot execute the statement '
        #         f'"{jac_ast.get_text()}" of type {jac_ast.name}',
        #         jac_ast)
        #     return

        return getattr(self, f'run_{jac_ast.name}')(jac_ast, *args)
        # except Exception as e:
        #     self.rt_error(
        #         f"Cannot execute this type of code here! {e}", jac_ast)
        #     return None

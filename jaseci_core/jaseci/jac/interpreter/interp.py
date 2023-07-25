"""
Interpreter for jac code in AST form

This interpreter should be inhereted from the class that manages state
referenced through self.
"""
from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.task_svc import TaskService
from jaseci.utils.utils import is_jsonable, parse_str_token, uuid_re
from jaseci.prim.element import Element
from jaseci.prim.node import Node
from jaseci.prim.edge import Edge
from jaseci.jac.jac_set import JacSet
from jaseci.jac.ir.jac_code import jac_ast_to_ir, jac_ir_to_ast
from jaseci.jac.machine.jac_scope import JacScope
from jaseci.jac.jsci_vm.machine import VirtualMachine
from jaseci.jac.machine.machine_state import TryException

from jaseci.jac.machine.jac_value import JacValue
from jaseci.jac.machine.jac_value import jac_elem_unwrap as jeu
from jaseci.jac.machine.jac_value import jac_wrap_value as jwv
from json import dumps, loads
from copy import copy, deepcopy
from base64 import b64decode
from itertools import pairwise

from jaseci.jac.jsci_vm.op_codes import JsCmp


class Interp(VirtualMachine):
    """Shared interpreter class across both sentinels and walkers"""

    def run_dotted_name(self, jac_ast):
        """
        dotted_name: NAME (DOT NAME)*;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = ""
        for i in kid:
            if i.name == "NAME":
                ret += i.token_text()
                if i == kid[-1]:
                    break
                ret += "."
        return ret

    def run_name_list(self, jac_ast):
        """
        name_list: NAME (COMMA NAME)*;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = []
        for i in kid:
            if i.name == "NAME":
                ret.append(i.token_text())
        return ret

    def run_param_list(self, jac_ast):
        """
        param_list:
            expr_list
            | kw_expr_list
            | expr_list COMMA kw_expr_list;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = {"args": [], "kwargs": {}}
        if kid[0].name == "expr_list":
            ret["args"] = self.run_expr_list(kid[0]).value
        elif kid[0].name == "kw_expr_list":
            ret["kwargs"] = self.run_kw_expr_list(kid[0]).value
        if len(kid) > 1:
            ret["kwargs"] = self.run_kw_expr_list(kid[2]).value
        return JacValue(self, value=ret)

    def run_expr_list(self, jac_ast):
        """
        expr_list: connect (COMMA connect)*;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = []
        for i in kid:
            if i.name != "COMMA":
                ret.append(self.run_rule(i).value)
        return JacValue(self, value=ret)

    def run_kw_expr_list(self, jac_ast):
        """
        kw_expr_list: NAME EQ connect (COMMA NAME EQ connect)*;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = {}
        while len(kid):
            ret[kid[0].token_text()] = self.run_rule(kid[2]).value
            kid = kid[3:]
            if len(kid):
                kid = kid[1:]
        return JacValue(self, value=ret)

    def run_code_block(self, jac_ast):
        """
        code_block: LBRACE statement* RBRACE | COLON statement;
        """
        kid = self.set_cur_ast(jac_ast)
        for i in kid:
            if i.name == "statement" and not self._loop_ctrl:
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
        if self._stopped:
            return
        kid = self.set_cur_ast(jac_ast)
        self.run_rule(kid[0])

    def run_if_stmt(self, jac_ast):
        """
        if_stmt: KW_IF expression code_block elif_stmt* else_stmt?;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_expression(kid[1])
        if self.pop().value:
            self.run_code_block(kid[2])
            return
        kid = kid[3:]
        if len(kid):
            while True:
                if kid[0].name == "elif_stmt":
                    if self.run_elif_stmt(kid[0]):
                        return
                elif kid[0].name == "else_stmt":
                    self.run_else_stmt(kid[0])
                    return
                kid = kid[1:]
                if not len(kid):
                    break

    def run_try_stmt(self, jac_ast):
        """
        try_stmt: KW_TRY code_block else_from_try?;
        """
        kid = self.set_cur_ast(jac_ast)
        self._jac_try_mode += 1
        try:
            self.run_code_block(kid[1])
        except TryException as e:
            if len(kid) > 2:
                self.run_else_from_try(kid[2], e.ref)
        except Exception as e:
            if len(kid) > 2:
                self.run_else_from_try(kid[2], self.jac_exception(e, kid[2]))
        self._jac_try_mode -= 1

    def run_else_from_try(self, jac_ast, jac_ex):
        """
        else_from_try:
            KW_ELSE (LPAREN NAME RPAREN)? code_block
            | KW_ELSE (KW_WITH NAME)? code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        if len(kid) > 2:
            JacValue(
                self,
                ctx=self._jac_scope.local_scope,
                name=kid[2].token_text(),
                value=jac_ex,
            ).write(kid[2])
        self.run_code_block(kid[-1])

    def run_elif_stmt(self, jac_ast):
        """
        elif_stmt: KW_ELIF expression code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_expression(kid[1])
        if self.pop().value:
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
            | KW_FOR NAME (COMMA NAME)? KW_IN expression code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        loops = 0
        if kid[1].name == "expression":
            self.run_expression(kid[1])
            self.pop()
            self.run_expression(kid[3])
            while self.pop().value:
                self._loop_ctrl = None
                self.run_code_block(kid[6])
                self.run_expression(kid[5])
                self.pop()
                loops += 1
                if self._loop_ctrl and self._loop_ctrl == "break":
                    self._loop_ctrl = None
                    break
                if loops > self._loop_limit:
                    self.rt_error(f"Hit loop limit [{self._loop_limit}]!", kid[0])
                self.run_expression(kid[3])
        elif kid[3].name == "expression":
            var = self._jac_scope.get_live_var(kid[1].token_text(), create_mode=True)
            self.run_expression(kid[3])
            lst = self.pop().value

            if isinstance(lst, (list, dict)):
                for i in lst:
                    self._loop_ctrl = None
                    var.value = i
                    var.write(kid[1])
                    self.run_code_block(kid[4])
                    loops += 1
                    if self._loop_ctrl and self._loop_ctrl == "break":
                        self._loop_ctrl = None
                        break
                    if loops > self._loop_limit:
                        self.rt_error(f"Hit loop limit [{self._loop_limit}]!", kid[0])
            else:
                self.rt_error("Not a list/dict for iteration!", kid[3])
        else:
            key = self._jac_scope.get_live_var(kid[1].token_text(), create_mode=True)
            val = self._jac_scope.get_live_var(kid[3].token_text(), create_mode=True)
            self.run_expression(kid[5])
            source = self.pop().value

            lst = None
            if isinstance(source, dict):
                lst = source.items()
            elif isinstance(source, list):
                lst = enumerate(source)

            if not (lst is None):
                for k, v in lst:
                    self._loop_ctrl = None
                    key.value = k
                    key.write(kid[1])
                    val.value = v
                    val.write(kid[3])
                    self.run_code_block(kid[6])
                    loops += 1
                    if self._loop_ctrl and self._loop_ctrl == "break":
                        self._loop_ctrl = None
                        break
                    if loops > self._loop_limit:
                        self.rt_error(f"Hit loop limit [{self._loop_limit}]!", kid[0])
            else:
                self.rt_error("Not a list/dict for iteration!", kid[5])
        if self._loop_ctrl and self._loop_ctrl == "continue":
            self._loop_ctrl = None

    def run_while_stmt(self, jac_ast):
        """
        while_stmt: KW_WHILE expression code_block;
        """
        kid = self.set_cur_ast(jac_ast)
        loops = 0
        self.run_expression(kid[1])
        while self.pop().value:
            self._loop_ctrl = None
            self.run_code_block(kid[2])
            loops += 1
            if self._loop_ctrl and self._loop_ctrl == "break":
                self._loop_ctrl = None
                break
            if loops > self._loop_limit:
                self.rt_error(f"Hit loop limit [{self._loop_limit}]!", kid[0])
            self.run_expression(kid[1])
        if self._loop_ctrl and self._loop_ctrl == "continue":
            self._loop_ctrl = None

    def run_ctrl_stmt(self, jac_ast):
        """
        ctrl_stmt: KW_CONTINUE | KW_BREAK | KW_SKIP;
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "KW_SKIP":
            self._stopped = "skip"
        elif kid[0].name == "KW_BREAK":
            self._loop_ctrl = "break"
        elif kid[0].name == "KW_CONTINUE":
            self._loop_ctrl = "continue"

    def run_assert_stmt(self, jac_ast):
        """
        assert_stmt: KW_ASSERT expression;
        """
        kid = self.set_cur_ast(jac_ast)
        passed = False
        try:
            self.run_expression(kid[1])
            passed = self.pop().value
        except Exception as e:
            e = self.jac_exception(e, jac_ast)
            raise Exception("Jac Assert Failed", kid[1].get_text(), e)
        if not passed:
            raise Exception("Jac Assert Failed", kid[1].get_text())

    def run_destroy_action(self, jac_ast):
        """
        destroy_action: KW_DESTROY expression SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_expression(kid[1])
        result = self.pop()
        if isinstance(result.value, Element):
            self.destroy_node_ids.add_obj(result.value)
        elif isinstance(result.value, JacSet):
            self.destroy_node_ids.add_obj_list(result.value)
        result.self_destruct(kid[1])

    def run_report_action(self, jac_ast):
        """
        report_action:
            KW_REPORT expression SEMI
                | KW_REPORT COLON NAME EQ expression SEMI;
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[1].name == "COLON":
            self.run_expression(kid[4])
            if kid[2].token_text() in ["status", "status_code"]:
                self.report_status = self.pop().value
            elif kid[2].token_text() == "custom":
                self.report_custom = jwv(self.pop().value, serialize_mode=True)
            elif kid[2].token_text() == "file":
                self.report_file = self.pop().value
            elif kid[2].token_text() == "error":
                err = self.pop().value
                if isinstance(err, str):
                    self.runtime_errors.append(err)
                else:
                    self.runtime_errors.append(
                        f'{err["mod"]}:{err["name"]} - line {err["line"]}, '
                        + f'col {err["col"]} - rule {err["rule"]} - {err["msg"]}'
                    )
                    for stk in err.get("stack_trace", []):
                        self.runtime_stack_trace.append(stk)
            else:
                self.rt_error("Invalid report attribute to set", kid[2])
        else:
            self.run_expression(kid[1])
            report = jwv(self.pop().value, serialize_mode=True)
            if not is_jsonable(report):
                self.rt_error(f"Report {report} not Json serializable", kid[0])
            self.report.append(copy(report))

    def run_expression(self, jac_ast):
        """
        expression: connect (assignment | copy_assign | inc_assign)?;
        """
        try:
            if self.attempt_bytecode(jac_ast):
                return
            kid = self.set_cur_ast(jac_ast)
            if len(kid) == 1:
                self.push(self.run_rule(kid[0]))
            else:
                if kid[1].name == "assignment":
                    self._assign_mode = True
                    dest = self.run_rule(kid[0])
                    self._assign_mode = False
                    self.run_assignment(kid[1])
                    self.perform_assignment(dest, self.pop(), kid[0])
                elif kid[1].name == "copy_assign":
                    self._assign_mode = True
                    dest = self.run_rule(kid[0])
                    self._assign_mode = False
                    self.run_copy_assign(kid[1])
                    self.perform_copy_fields(dest, self.pop(), kid[0])
                elif kid[1].name == "inc_assign":
                    self._assign_mode = True
                    dest = self.run_rule(kid[0])
                    self._assign_mode = False
                    self.run_inc_assign(kid[1])
                    self.perform_increment(
                        dest, self.pop(), JsCmp[kid[1].kid[0].name], kid[0]
                    )
        except Exception as e:
            self.rt_error(e, jac_ast)

    def run_assignment(self, jac_ast):
        """
        assignment: EQ expression;
        """
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        self.run_expression(kid[1])

    def run_copy_assign(self, jac_ast):
        """
        copy_assign: CPY_EQ expression;
        """
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        self.run_expression(kid[1])

    def run_inc_assign(self, jac_ast):
        """
        inc_assign: (PEQ | MEQ | TEQ | DEQ) expression;
        """
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        self.run_expression(kid[1])

    def run_connect(self, jac_ast):
        """
        connect: logical ( (NOT edge_ref | connect_op) expression)?;
        """
        kid = self.set_cur_ast(jac_ast)
        if len(kid) < 2:
            return self.run_rule(kid[0])
        bret = self.run_rule(kid[0])
        base = bret.value
        self.run_expression(kid[-1])
        tret = self.pop()
        target = tret.value
        self.rt_check_type(base, [Node, JacSet], kid[0])
        self.rt_check_type(target, [Node, JacSet], kid[-1])
        if isinstance(base, Node):
            base = JacSet(in_list=[base])
        if isinstance(target, Node):
            target = JacSet(in_list=[target])
        if kid[1].name == "NOT":
            for i in target.obj_list():
                for j in base.obj_list():
                    j.detach_edges(i, self.run_edge_ref(kid[2]).obj_list())
            return bret
        else:
            direction = kid[1].kid[0].name
            for i in target.obj_list():
                for j in base.obj_list():
                    use_edge = self.run_connect_op(kid[1])
                    self.rt_check_type(i, Node, kid[-1])
                    self.rt_check_type(j, Node, kid[-1])
                    if direction == "connect_from":
                        j.attach_inbound(i, [use_edge])
                    elif direction == "connect_to":
                        j.attach_outbound(i, [use_edge])
                    else:
                        j.attach_bidirected(i, [use_edge])
        return bret

    def run_logical(self, jac_ast):
        """
        logical: compare ((KW_AND | KW_OR) compare)*;
        """
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        result = self.run_rule(kid[0])
        kid = kid[1:]
        while kid:
            if kid[0].name == "KW_AND":
                if result.value:
                    result.value = result.value and self.run_rule(kid[1]).value
            elif kid[0].name == "KW_OR":
                if not result.value:
                    result.value = result.value or self.run_rule(kid[1]).value
            kid = kid[2:]
            if not kid:
                break
        self.push(result)

    def run_compare(self, jac_ast):
        """
        compare: NOT compare | arithmetic (cmp_op arithmetic)*;
        """
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "NOT":
            self.push(JacValue(self, value=not self.run_rule(kid[1]).value))
        else:
            result = self.run_rule(kid[0])
            kid = kid[1:]
            while kid:
                other_res = self.run_rule(kid[1])
                self.run_cmp_op(kid[0], result, other_res)
                result = self.pop()
                kid = kid[2:]
                if not kid:
                    break
            self.push(result)

    def run_cmp_op(self, jac_ast, val1, val2):
        """
        cmp_op: EE | LT | GT | LTE | GTE | NE | KW_IN | nin;
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "EE":
            self.push(JacValue(self, value=val1.value == val2.value))
        elif kid[0].name == "LT":
            self.push(JacValue(self, value=val1.value < val2.value))
        elif kid[0].name == "GT":
            self.push(JacValue(self, value=val1.value > val2.value))
        elif kid[0].name == "LTE":
            self.push(JacValue(self, value=val1.value <= val2.value))
        elif kid[0].name == "GTE":
            self.push(JacValue(self, value=val1.value >= val2.value))
        elif kid[0].name == "NE":
            self.push(JacValue(self, value=val1.value != val2.value))
        elif kid[0].name == "KW_IN":
            self.push(JacValue(self, value=val1.value in val2.value))
        elif kid[0].name == "nin":
            self.push(JacValue(self, value=val1.value not in val2.value))

    def run_arithmetic(self, jac_ast):
        """
        arithmetic: term ((PLUS | MINUS) term)*;
        """
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        result = self.run_rule(kid[0])
        kid = kid[1:]
        while kid:
            other_res = self.run_rule(kid[1])
            if kid[0].name == "PLUS":
                result.value = result.value + other_res.value
            elif kid[0].name == "MINUS":
                result.value = result.value - other_res.value
            kid = kid[2:]
            if not kid:
                break
        self.push(result)

    def run_term(self, jac_ast):
        """
        term: factor ((STAR_MUL | DIV | MOD) factor)*;
        """
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        result = self.run_rule(kid[0])
        kid = kid[1:]
        while kid:
            other_res = self.run_rule(kid[1])
            if kid[0].name == "STAR_MUL":
                result.value = result.value * other_res.value
            elif kid[0].name == "DIV":
                result.value = result.value / other_res.value
            elif kid[0].name == "MOD":
                result.value = result.value % other_res.value
            kid = kid[2:]
            if not kid:
                break
        self.push(result)

    def run_factor(self, jac_ast):
        """
        factor: (PLUS | MINUS) factor | power;
        """
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        if len(kid) < 2:
            self.push(self.run_rule(kid[0]))
        else:
            result = self.run_rule(kid[1])
            if kid[0].name == "MINUS":
                result.value = -(result.value)
            self.push(result)

    def run_power(self, jac_ast):
        """
        power: atom (POW factor)*;
        """
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        result = self.run_rule(kid[0])
        kid = kid[1:]
        if len(kid) < 1:
            self.push(result)
        elif kid[0].name == "POW":
            while kid:
                result.value = result.value ** self.run_rule(kid[1]).value
                kid = kid[2:]
                if not kid:
                    break
            self.push(result)

    def run_global_ref(self, jac_ast):
        """
        global_ref: KW_GLOBAL DOT (obj_built_in | NAME);
        """
        try:
            kid = self.set_cur_ast(jac_ast)
            if kid[2].name == "obj_built_in":
                kid = self.set_cur_ast(kid[2])
                if kid[0].name == "KW_CONTEXT":
                    return JacValue(self, value=self.parent().global_vars)
                elif kid[0].name == "KW_INFO":
                    # Add additional accessible fields
                    return JacValue(self, value=self.get_info())
                else:
                    self.rt_error(f"Global {kid[0].name} is not supported!", jac_ast)
            else:
                token = kid[2].token_text()
                if token not in self.parent().global_vars:
                    self.rt_error(f"Global not defined - {token}", kid[2])

                return JacValue(self, ctx=self.parent().global_vars, name=token)

        except Exception as e:
            self.rt_error(e, jac_ast)

    def run_atom(self, jac_ast):
        """
        atom:
            INT
            | FLOAT
            | multistring
            | BOOL
            | NULL
            | NAME
            | global_ref
            | node_edge_ref
            | list_val
            | dict_val
            | LPAREN expression RPAREN
            | ability_op NAME spawn_ctx?
            | atom atom_trailer
            | KW_SYNC atom
            | spawn
            | ref
            | deref
            | any_type;
        """
        try:
            if self.attempt_bytecode(jac_ast):
                return
            kid = self.set_cur_ast(jac_ast)
            if kid[0].name == "INT":
                self.push(JacValue(self, value=int(kid[0].token_text())))
            elif kid[0].name == "FLOAT":
                self.push(JacValue(self, value=float(kid[0].token_text())))
            elif kid[0].name == "multistring":
                self.run_multistring(kid[0])
            elif kid[0].name == "BOOL":
                self.push(JacValue(self, value=bool(kid[0].token_text() == "true")))
            elif kid[0].name == "NULL":
                self.push(JacValue(self, value=None))
            elif kid[0].name == "NAME":
                self.load_variable(kid[0].token_text(), kid[0])
            elif kid[0].name == "LPAREN":
                self.run_expression(kid[1])
            elif kid[0].name == "ability_op":
                self.push(
                    self.run_ability_call(
                        jac_ast, atom_res=JacValue(self, value=self._jac_scope.has_obj)
                    )
                )
            elif kid[0].name == "atom":
                self.run_atom(kid[0])
                ret = self.pop()
                for i in kid[1:]:
                    ret = self.run_atom_trailer(i, ret)
                self.push(ret)
            elif kid[0].name == "KW_SYNC":
                self.run_atom(kid[1])
                val = self.pop()
                self.push(
                    JacValue(
                        self,
                        value=(
                            JsOrc.svc("task")
                            .poke(TaskService)
                            .get_by_task_id(val.value["result"], True)
                        ),
                    )
                )
            else:
                self.push(self.run_rule(kid[0]))

        except Exception as e:
            self.rt_error(e, jac_ast)

    def run_atom_trailer(self, jac_ast, atom_res):
        """
        atom_trailer:
            DOT built_in
            | DOT NAME
            | index_slice
            | ability_call;
        """
        try:
            kid = self.set_cur_ast(jac_ast)
            if isinstance(atom_res.value, Element):
                self._write_candidate = atom_res.value
            if kid[0].name == "DOT":
                if kid[1].name == "built_in":
                    return self.run_built_in(kid[1], atom_res)
                elif kid[1].name == "NAME":
                    d = atom_res.value
                    n = kid[1].token_text()
                    if self.rt_check_type(d, [dict, Element, JacSet], kid[0]):
                        if isinstance(d, Element):
                            self._write_candidate = d
                        if not isinstance(d, JacSet):
                            ret = JacValue(self, ctx=d, name=n)
                        else:
                            plucked = []
                            for i in d:
                                if n in i.context.keys():
                                    plucked.append(i.context[n])
                                else:
                                    self.rt_error(
                                        f"Some elements in set does not have {n}",
                                        kid[1],
                                    )
                            ret = JacValue(self, value=plucked)
                        return ret
                    else:
                        self.rt_error(f"Invalid variable {n}", kid[0])
            elif kid[0].name == "index_slice":
                if not self.rt_check_type(atom_res.value, [list, str, dict], kid[0]):
                    return atom_res
                return self.run_index_slice(kid[0], atom_res)
            elif kid[0].name == "ability_call":
                return self.run_ability_call(kid[0], atom_res)
        except Exception as e:
            self.rt_error(e, jac_ast)

    def run_ability_call(self, jac_ast, atom_res):
        """
        ability_call:
            LPAREN param_list? RPAREN
            | ability_op NAME spawn_ctx?;
        """
        from jaseci.prim.ability import Ability

        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "LPAREN":
            param_list = {"args": [], "kwargs": {}}
            if kid[1].name == "param_list":
                param_list = self.run_param_list(kid[1]).value
            if isinstance(atom_res.value, Ability):
                ret = atom_res.value.run_action(
                    param_list, self._jac_scope, self, jac_ast
                )
                return JacValue(self, value=ret)
            else:
                self.rt_error("Unable to execute ability", kid[0])
        elif kid[0].name == "ability_op":
            arch = self.run_ability_op(kid[0], atom_res)
            if len(kid) > 2:
                self.run_spawn_ctx(kid[2], atom_res.value)
            self.call_ability(
                nd=atom_res.value,
                name=kid[1].token_text(),
                act_list=arch.get_all_abilities(),
            )
            return atom_res

    def run_ability_op(self, jac_ast, atom_res):
        """
        ability_op: DBL_COLON | DBL_COLON NAME COLON;
        """
        kid = self.set_cur_ast(jac_ast)
        base_arch = atom_res.value.get_architype()
        if len(kid) > 1:
            kind = atom_res.value.kind
            name = kid[1].token_text()
            if name in base_arch.derived_types():
                return self.parent().arch_ids.get_obj_by_name(name=name, kind=kind)
            else:
                self.rt_error(f"{name} is not a super arch of {base_arch.name}", kid[1])
        else:
            return base_arch

    def run_ref(self, jac_ast):
        """
        ref: '&' atom;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_atom(kid[1])
        result = self.pop()
        if self.rt_check_type(result.value, Element, kid[1]):
            result = JacValue(self, value=result.value.jid)
        return result

    def run_deref(self, jac_ast):
        """
        deref: '*' atom;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_atom(kid[1])
        result = self.pop()

        if (
            isinstance(result.value, str)
            and len(result.value) < 64  # super long string, untrustworthy
            and not result.value.startswith("jac:uuid:")  # already an object
        ):
            matcher = uuid_re.search(result.value)
            if matcher and matcher.group(1):
                nd = jeu(f"jac:uuid:{matcher.group(1)}", self)
                if nd is not None:
                    return JacValue(self, value=nd)

        self.rt_error(f"{result.value} not valid reference", kid[1])

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
        self.run_any_type(kid[0])
        typ = self.pop()
        if typ.value == Edge:
            if isinstance(atom_res.value, Node):
                return JacValue(
                    self,
                    value=self.obj_set_to_jac_set(
                        self.here().attached_edges(atom_res.value)
                    ),
                )
            elif isinstance(atom_res.value, Edge):
                return atom_res
            elif isinstance(atom_res.value, JacSet):
                return JacValue(self, value=self._relevant_edges)
            else:
                self.rt_error(
                    f"Cannot get edges from {atom_res.value}. "
                    f"Type {atom_res.jac_type()} invalid",
                    kid[0],
                )
        # may want to remove 'here" node from return below
        elif typ.value == Node:
            if isinstance(atom_res.value, Node):
                return atom_res
            elif isinstance(atom_res.value, Edge):
                return JacValue(
                    self, value=self.obj_set_to_jac_set(atom_res.value.nodes())
                )
            elif isinstance(atom_res.value, JacSet):
                res = JacSet()
                for i in atom_res.value.obj_list():
                    if isinstance(i, Edge):
                        res.add_obj(i.to_node())
                        res.add_obj(i.from_node())
                    elif isinstance(i, Node):
                        res.add_obj(i)
                return JacValue(self, value=res)
            else:
                self.rt_error(
                    f"Cannot get nodes from {atom_res}. "
                    f"Type {atom_res.jac_type()} invalid",
                    kid[0],
                )
        else:
            try:
                if isinstance(atom_res.value, str) and typ.value == dict:
                    atom_res.value = loads(atom_res.value)
                elif isinstance(atom_res.value, dict) and typ.value == str:
                    atom_res.value = dumps(atom_res.value)
                else:
                    atom_res.value = typ.value(atom_res.value)
            except Exception as e:
                self.rt_error(
                    f"Invalid cast of {atom_res.jac_type()} "
                    f"to {jwv(typ.value)}: {e}",
                    kid[0],
                )
            return atom_res

        return atom_res

    def run_obj_built_in(self, jac_ast, atom_res):
        """
        obj_built_in: KW_CONTEXT | KW_INFO | KW_DETAILS;
        """
        kid = self.set_cur_ast(jac_ast)
        from jaseci.prim.walker import Walker

        if kid[0].name == "KW_CONTEXT":
            if self.rt_check_type(atom_res.value, [Node, Edge, Walker], kid[0]):
                return JacValue(self, ctx=atom_res.value, value=atom_res.value.context)
        elif kid[0].name == "KW_INFO":
            if self.rt_check_type(atom_res.value, [Node, Edge, Walker], kid[0]):
                return JacValue(
                    self,
                    ctx=atom_res.value,
                    value=atom_res.value.serialize(detailed=False),
                )
        elif kid[0].name == "KW_DETAILS":
            if self.rt_check_type(atom_res.value, [Node, Edge, Walker], kid[0]):
                return JacValue(
                    self,
                    ctx=atom_res.value,
                    value=atom_res.value.serialize(detailed=True),
                )
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
        if kid[0].name == "KW_KEYS":
            if isinstance(atom_res.value, dict):
                return JacValue(self, value=list(atom_res.value.keys()))
            else:
                self.rt_error(
                    f"Cannot get keys of {atom_res}. " f"Not Dictionary!", kid[0]
                )
        elif len(kid) > 1 and kid[1].name == "name_list":
            filter_on = self.run_name_list(kid[1])
            d = atom_res.value
            if self.rt_check_type(d, [dict], kid[0]):
                d = {k: d[k] for k in d if k in filter_on}
                return JacValue(self, value=d)
        else:
            if not self.rt_check_type(atom_res.value, [dict], kid[0]):
                return atom_res
            kid = kid[1:]
            if kid[0].name == "DBL_COLON":
                kid = kid[1:]
            result = None
            op = kid[0].token_text()
            try:
                if op == "items":
                    result = JacValue(
                        self, value=list(map(list, atom_res.value.items()))
                    )
                elif op == "copy":
                    result = JacValue(self, value=atom_res.value.copy())
                elif op == "deepcopy":
                    result = JacValue(self, value=deepcopy(atom_res.value))
                elif op == "keys":
                    result = JacValue(self, value=list(atom_res.value.keys()))
                elif op == "clear":
                    result = JacValue(self, value=atom_res.value.clear())
                    self.candidate_writethrough()
                elif op == "popitem":
                    result = JacValue(self, value=list(atom_res.value.popitem()))
                    self.candidate_writethrough()
                elif op == "values":
                    result = JacValue(self, value=list(atom_res.value.values()))
                if result:
                    if len(kid) > 1:
                        self.rt_warn(f"{op} does not take parameters, ignoring", kid[2])
                    return result
                if len(kid) > 1:
                    args = self.run_expr_list(kid[2]).value
                    if op == "pop":
                        result = JacValue(self, value=atom_res.value.pop(*args))
                        self.candidate_writethrough()
                    elif op == "update":
                        result = JacValue(self, value=atom_res.value.update(*args))
                        self.candidate_writethrough()
                    elif op == "get":
                        result = JacValue(self, value=atom_res.value.get(*args))
                    if result:
                        return result
            except Exception as e:
                self.rt_error(e, jac_ast)
            self.rt_error(f"Call to {op} is invalid.", jac_ast)

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
        if kid[0].name == "KW_LENGTH":
            if isinstance(atom_res.value, list):
                return JacValue(self, value=len(atom_res.value))
            else:
                self.rt_error(
                    f"Cannot get length of {atom_res.value}. Not List!", kid[0]
                )
        else:
            if not self.rt_check_type(atom_res.value, [list], kid[0]):
                return atom_res
            kid = kid[1:]
            if kid[0].name == "DBL_COLON":
                kid = kid[1:]
            result = None
            op = kid[0].token_text()
            try:
                if op == "reverse":
                    result = JacValue(self, value=atom_res.value.reverse())
                    self.candidate_writethrough()
                elif op == "reversed":
                    result = JacValue(self, value=list(reversed(atom_res.value)))
                elif op == "copy":
                    result = JacValue(self, value=atom_res.value.copy())
                elif op == "deepcopy":
                    result = JacValue(self, value=deepcopy(atom_res.value))
                elif op == "sort":
                    result = JacValue(self, value=atom_res.value.sort())
                    self.candidate_writethrough()
                elif op == "clear":
                    result = JacValue(self, value=atom_res.value.clear())
                    self.candidate_writethrough()
                elif op == "max":
                    result = JacValue(self, value=max(atom_res.value))
                elif op == "min":
                    result = JacValue(self, value=min(atom_res.value))
                elif op == "idx_of_max":
                    result = JacValue(
                        self, value=atom_res.value.index(max(atom_res.value))
                    )
                elif op == "idx_of_min":
                    result = JacValue(
                        self, value=atom_res.value.index(min(atom_res.value))
                    )
                elif op == "pairwise":
                    result = JacValue(
                        self, value=[list(s) for s in pairwise(atom_res.value)]
                    )
                elif op == "unique":
                    result = JacValue(self, value=list(set(atom_res.value)))

                elif len(kid) < 2 and op == "pop":
                    result = JacValue(self, value=atom_res.value.pop())
                    self.candidate_writethrough()
                if result:
                    if len(kid) > 1:
                        self.rt_warn(f"{op} does not take parameters, ignoring", kid[2])
                    return result
                if len(kid) > 1:
                    args = self.run_expr_list(kid[2]).value
                    if op == "index":
                        result = JacValue(self, value=atom_res.value.index(*args))
                    elif op == "append":
                        result = JacValue(self, value=atom_res.value.append(*args))
                        self.candidate_writethrough()
                    elif op == "extend":
                        result = JacValue(self, value=atom_res.value.extend(*args))
                        self.candidate_writethrough()
                    elif op == "insert":
                        result = JacValue(self, value=atom_res.value.insert(*args))
                        self.candidate_writethrough()
                    elif op == "remove":
                        result = JacValue(self, value=atom_res.value.remove(*args))
                        self.candidate_writethrough()
                    elif op == "count":
                        result = JacValue(self, value=atom_res.value.count(*args))
                    elif op == "pop":
                        result = JacValue(self, value=atom_res.value.pop(*args))
                        self.candidate_writethrough()
                    if result:
                        return result
            except Exception as e:
                self.rt_error(e, jac_ast)
            self.rt_error(f"Call to {op} is invalid.", jac_ast)
        return atom_res

    def run_string_built_in(self, jac_ast, atom_res):
        """
        string_built_in:
        (TYP_STRING DBL_COLON | STR_DBL_COLON) NAME (
                LPAREN expr_list RPAREN
        )?;
        """
        kid = self.set_cur_ast(jac_ast)
        if not self.rt_check_type(atom_res.value, [str], kid[0]):
            return atom_res
        kid = kid[1:]
        if kid[0].name == "DBL_COLON":
            kid = kid[1:]
        result = None
        str_op = kid[0].token_text()
        try:
            if str_op == "upper":
                result = JacValue(self, value=atom_res.value.upper())
            elif str_op == "lower":
                result = JacValue(self, value=atom_res.value.lower())
            elif str_op == "title":
                result = JacValue(self, value=atom_res.value.title())
            elif str_op == "capitalize":
                result = JacValue(self, value=atom_res.value.capitalize())
            elif str_op == "swap_case":
                result = JacValue(self, value=atom_res.value.swapcase())
            elif str_op == "is_alnum":
                result = JacValue(self, value=atom_res.value.isalnum())
            elif str_op == "is_alpha":
                result = JacValue(self, value=atom_res.value.isalpha())
            elif str_op == "is_digit":
                result = JacValue(self, value=atom_res.value.isdigit())
            elif str_op == "is_title":
                result = JacValue(self, value=atom_res.value.istitle())
            elif str_op == "is_upper":
                result = JacValue(self, value=atom_res.value.isupper())
            elif str_op == "is_lower":
                result = JacValue(self, value=atom_res.value.islower())
            elif str_op == "is_space":
                result = JacValue(self, value=atom_res.value.isspace())
            elif str_op == "load_json":
                import json

                result = JacValue(self, value=json.loads(atom_res.value))
            elif len(kid) < 2 and str_op == "split":
                result = JacValue(self, value=atom_res.value.split())
            elif len(kid) < 2 and str_op == "strip":
                result = JacValue(self, value=atom_res.value.strip())
            elif len(kid) < 2 and str_op == "lstrip":
                result = JacValue(self, value=atom_res.value.lstrip())
            elif len(kid) < 2 and str_op == "rstrip":
                result = JacValue(self, value=atom_res.value.rstrip())
            if result:
                if len(kid) > 1:
                    self.rt_warn(f"{str_op} does not take parameters, ignoring", kid[2])
                return result
            if len(kid) > 1:
                args = self.run_expr_list(kid[2]).value
                if str_op == "count":
                    result = JacValue(self, value=atom_res.value.count(*args))
                elif str_op == "find":
                    result = JacValue(self, value=atom_res.value.find(*args))
                elif str_op == "split":
                    result = JacValue(self, value=atom_res.value.split(*args))
                elif str_op == "join":
                    if len(args) == 1 and type(args[0]) is list:
                        args = args[0]

                    result = JacValue(
                        self, value=atom_res.value.join([str(arg) for arg in args])
                    )
                elif str_op == "startswith":
                    result = JacValue(self, value=atom_res.value.startswith(*args))
                elif str_op == "endswith":
                    result = JacValue(self, value=atom_res.value.endswith(*args))
                elif str_op == "replace":
                    result = JacValue(self, value=atom_res.value.replace(*args))
                elif str_op == "strip":
                    result = JacValue(self, value=atom_res.value.strip(*args))
                elif str_op == "lstrip":
                    result = JacValue(self, value=atom_res.value.lstrip(*args))
                elif str_op == "rstrip":
                    result = JacValue(self, value=atom_res.value.rstrip(*args))
                if result:
                    return result
        except Exception as e:
            self.rt_error(e, jac_ast)
        self.rt_error(f"Call to {str_op} is invalid.", jac_ast)
        return atom_res

    def run_node_edge_ref(self, jac_ast, viable_nodes=None):
        """
        node_edge_ref:
            node_ref filter_ctx? node_edge_ref?
            | edge_ref node_edge_ref?;
        """
        kid = self.set_cur_ast(jac_ast)
        result = JacSet()
        if kid[0].name == "node_ref":
            result = self.run_node_ref(kid[0], viable_nodes=viable_nodes)
            kid = kid[1:]
            if len(kid) and kid[0].name == "filter_ctx":
                result = self.run_filter_ctx(kid[0], result)
                kid = kid[1:]
            if len(kid):
                result = self.run_node_edge_ref(kid[0], viable_nodes=result).value

        elif kid[0].name == "edge_ref":
            if not viable_nodes:
                viable_nodes = [None]
            self._relevant_edges = JacSet()
            for i in viable_nodes:
                relevant_edges = self.run_edge_ref(kid[0], location=i)
                result += self.visibility_prune(
                    self.edge_to_node_jac_set(relevant_edges, location=i)
                )
                kid = kid[1:]
                if len(kid):
                    result = self.run_node_edge_ref(kid[0], viable_nodes=result).value

                    relevant_edges = self.edges_filter_on_nodes(relevant_edges, result)
                self._relevant_edges += relevant_edges
        return JacValue(self, value=result)

    def run_node_ref(self, jac_ast, is_spawn=False, viable_nodes=None):
        """
        node_ref: NODE_DBL_COLON NAME;
        """
        kid = self.set_cur_ast(jac_ast)
        if not is_spawn:
            result = JacSet()
            viable_nodes = self.visibility_prune(viable_nodes)
            if len(kid) > 1:
                for i in viable_nodes.obj_list():
                    try:
                        if i.get_architype().is_instance(kid[-1].token_text()):
                            result.add_obj(i)
                    except:
                        self.rt_warn(
                            f"Error occured while getting architype {i.name}. Skipping..."
                        )
            else:
                result += viable_nodes
        else:
            result = self.parent().run_architype(
                kid[-1].token_text(), kind="node", caller=self
            )
        return result

    def run_walker_ref(self, jac_ast, to_await=False):
        """
        walker_ref: WALKER_DBL_COLON NAME;
        """
        kid = self.set_cur_ast(jac_ast)
        name = kid[-1].token_text()
        wlk = self.yielded_walkers_ids.get_obj_by_name(name, silent=True)
        if wlk is None:
            wlk = self.parent().run_architype(name=name, kind="walker", caller=self)
        if wlk is None:
            self.rt_error(f"No walker {name} exists!", kid[-1])
        else:
            wlk._to_await = to_await
        return wlk

    def run_graph_ref(self, jac_ast):
        """
        graph_ref: GRAPH_DBL_COLON NAME;
        """
        kid = self.set_cur_ast(jac_ast)
        gph = self.parent().run_architype(
            kid[-1].token_text(), kind="graph", caller=self
        )
        return gph

    def run_type_ref(self, jac_ast):
        """
        type_ref: TYPE_DBL_COLON NAME;
        """
        kid = self.set_cur_ast(jac_ast)
        obj = self.parent().run_architype(
            kid[-1].token_text(), kind="type", caller=self
        )
        return JacValue(self, value=obj)

    def run_edge_ref(self, jac_ast, location=None):
        """
        edge_ref: edge_to | edge_from | edge_any;
        """
        kid = self.set_cur_ast(jac_ast)
        return self.run_rule(kid[0], location)

    def run_edge_to(self, jac_ast, location=None):
        """
        edge_to:
            '-->'
            | '-' ('[' NAME (spawn_ctx | filter_ctx)? ']')? '->';
        """
        kid = self.set_cur_ast(jac_ast)
        if not location:
            location = self.here()
        result = JacSet()
        for i in location.outbound_edges() + location.bidirected_edges():
            if len(kid) > 2 and not i.get_architype().is_instance(kid[2].token_text()):
                continue
            result.add_obj(i)
        if len(kid) > 2 and kid[3].name == "filter_ctx":
            result = self.run_filter_ctx(kid[3], result)
        elif len(kid) > 2 and kid[3].name == "spawn_ctx":
            self.rt_error("Assigning values not allowed here", kid[3])
        return result

    def run_edge_from(self, jac_ast, location=None):
        """
        edge_from:
            '<--'
            | '<-' ('[' NAME (spawn_ctx | filter_ctx)? ']')? '-';
        """
        kid = self.set_cur_ast(jac_ast)
        if not location:
            location = self.here()
        result = JacSet()
        for i in location.inbound_edges() + location.bidirected_edges():
            if len(kid) > 2 and not i.get_architype().is_instance(kid[2].token_text()):
                continue
            result.add_obj(i)
        if len(kid) > 2 and kid[3].name == "filter_ctx":
            result = self.run_filter_ctx(kid[3], result)
        elif len(kid) > 2 and kid[3].name == "spawn_ctx":
            self.rt_error("Assigning values not allowed here", kid[3])
        return result

    def run_edge_any(self, jac_ast, location=None):
        """
        edge_any:
            '<-->'
            | '<-' ('[' NAME (spawn_ctx | filter_ctx)? ']')? '->';
        NOTE: these do not use strict bidirected semantic but any edge
        """
        kid = self.set_cur_ast(jac_ast)
        if not location:
            location = self.here()
        result = JacSet()
        for i in location.attached_edges():
            if len(kid) > 2 and not i.get_architype().is_instance(kid[2].token_text()):
                continue
            result.add_obj(i)
        if len(kid) > 2 and kid[3].name == "filter_ctx":
            result = self.run_filter_ctx(kid[3], result)
        elif len(kid) > 2 and kid[3].name == "spawn_ctx":
            self.rt_error("Assigning values not allowed here", kid[3])
        return result

    def run_connect_op(self, jac_ast):
        """
        connect_op: connect_to | connect_from | connect_any;
        """
        kid = self.set_cur_ast(jac_ast)
        if len(kid[0].kid) > 2:
            result = self.parent().run_architype(
                kid[0].kid[2].token_text(), kind="edge", caller=self
            )
            if kid[0].kid[3].name == "spawn_ctx":
                self.run_spawn_ctx(kid[0].kid[3], result)
        else:
            result = Edge(
                m_id=self._m_id,
                h=self._h,
                kind="edge",
                name="generic",
            )
        return result

    def run_list_val(self, jac_ast):
        """
        list_val: LSQUARE expr_list? RSQUARE;
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[1].name == "expr_list":
            return self.run_expr_list(kid[1])
        return JacValue(self, value=[])

    def run_index_slice(self, jac_ast, atom_res):
        """
        index_slice:
            LSQUARE expression RSQUARE
            | LSQUARE expression COLON expression RSQUARE;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_expression(kid[1])
        idx = self.pop().value
        if kid[2].name == "RSQUARE":
            if not self.rt_check_type(idx, [int, str], kid[1]):
                self.rt_error(
                    f"Index of type {type(idx)} not valid. "
                    f"Indicies must be an integer or string!",
                    kid[1],
                )
            try:
                return JacValue(self, ctx=atom_res.value, name=idx)
            except Exception as e:
                self.rt_error(e, jac_ast, isinstance(e, (IndexError, AttributeError)))
        else:
            self.run_expression(kid[3])
            end = self.pop().value
            if not self.rt_check_type(idx, [int], kid[1]) or not self.rt_check_type(
                end, [int], kid[3]
            ):
                self.rt_error(
                    "List slice range not valid. Indicies must be an integers!",
                    kid[1],
                )
            try:
                return JacValue(self, ctx=atom_res.value, name=idx, end=end)
            except Exception as e:
                self.rt_error(e, jac_ast, isinstance(e, (IndexError, AttributeError)))

    def run_dict_val(self, jac_ast):
        """
        dict_val: LBRACE (kv_pair (COMMA kv_pair)*)? RBRACE;
        """
        kid = self.set_cur_ast(jac_ast)
        dict_res = {}
        for i in kid:
            if i.name == "kv_pair":
                self.run_kv_pair(i, dict_res)
        return JacValue(self, value=dict_res)

    def run_kv_pair(self, jac_ast, obj):
        """
        kv_pair: STRING COLON expression;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_expression(kid[0])
        key = self.pop().value
        if isinstance(key, str):
            self.run_expression(kid[2])
            obj[key] = self.pop().value
        else:
            self.rt_error(f"Key is not str type : {type(key)}!", kid[0])

    def run_spawn(self, jac_ast):
        """
        spawn: KW_SPAWN spawn_object;

        NOTE: spawn statements support locations that are either nodes or
        jac_sets
        """
        kid = self.set_cur_ast(jac_ast)
        return self.run_spawn_object(kid[1])

    def run_spawn_object(self, jac_ast):
        """
        spawn_object:
            node_spawn
            | walker_spawn
            | graph_spawn
            | type_spawn;
        """
        kid = self.set_cur_ast(jac_ast)
        return self.run_rule(kid[0])

    def run_spawn_edge(self, jac_ast):
        """
        spawn_edge: expression connect_op;
        """
        kid = self.set_cur_ast(jac_ast)
        self.run_expression(kid[0])
        loc = self.pop().value
        if isinstance(loc, JacSet):
            edge_set = [self.run_connect_op(kid[1]) for _ in loc]
            loc = loc.obj_list()
        else:
            edge_set = self.run_connect_op(kid[1])
        return {
            "location": loc,
            "use_edge": edge_set,
            "direction": kid[1].kid[0].name,
        }

    def run_node_spawn(self, jac_ast):
        """
        node_spawn: spawn_edge? node_ref spawn_ctx?;
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "node_ref":
            ret_node = self.run_node_ref(kid[0], is_spawn=True)
            if kid[-1].name == "spawn_ctx":
                self.run_spawn_ctx(kid[-1], ret_node)
            return JacValue(self, value=ret_node)
        else:
            sp = self.run_spawn_edge(kid[0])
            if isinstance(sp["location"], Node):
                ret_node = self.run_node_ref(kid[1], is_spawn=True)
                if sp["direction"] == "connect_from":
                    sp["location"].attach_inbound(ret_node, [sp["use_edge"]])
                elif sp["direction"] == "connect_to":
                    sp["location"].attach_outbound(ret_node, [sp["use_edge"]])
                else:
                    sp["location"].attach_bidirected(ret_node, [sp["use_edge"]])
                if kid[-1].name == "spawn_ctx":
                    self.run_spawn_ctx(kid[-1], ret_node)
                return JacValue(self, value=ret_node)
            elif isinstance(sp["location"], JacSet):
                res = []
                sp["location"] = sp["location"].obj_list()
                for i in range(len(sp["location"])):
                    ret_node = self.run_node_ref(kid[1], is_spawn=True)
                    if sp["direction"] == "connect_from":
                        sp["location"][i].attach_inbound(ret_node, [sp["use_edge"][i]])
                    elif sp["direction"] == "connect_to":
                        sp["location"][i].attach_outbound(ret_node, [sp["use_edge"][i]])
                    else:
                        sp["location"][i].attach_bidirected(
                            ret_node, [sp["use_edge"][i]]
                        )
                    if kid[-1].name == "spawn_ctx":
                        self.run_spawn_ctx(kid[-1], ret_node)
                    res.append(ret_node)
                return JacValue(self, value=res)
            else:
                self.rt_error(f'Spawn can not occur on {type(sp["location"])}!', kid[1])

    def run_graph_spawn(self, jac_ast):
        """
        graph_spawn: spawn_edge? graph_ref;
        """
        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "graph_ref":
            result = self.run_graph_ref(kid[0])
            return JacValue(self, value=result)
        else:
            sp = self.run_spawn_edge(kid[0])
            if isinstance(sp["location"], Node):
                ret_node = self.run_graph_ref(kid[1])
                if sp["direction"] == "connect_from":
                    sp["location"].attach_inbound(ret_node, [sp["use_edge"]])
                elif sp["direction"] == "connect_to":
                    sp["location"].attach_outbound(ret_node, [sp["use_edge"]])
                else:
                    sp["location"].attach_bidirected(ret_node, [sp["use_edge"]])
                return JacValue(self, value=ret_node)
            elif isinstance(sp["location"], JacSet):
                res = []
                sp["location"] = sp["location"].obj_list()
                for i in range(len(sp["location"])):
                    ret_node = self.run_graph_ref(kid[1])
                    if sp["direction"] == "connect_from":
                        sp["location"][i].attach_inbound(ret_node, [sp["use_edge"][i]])
                    elif sp["direction"] == "connect_to":
                        sp["location"][i].attach_outbound(ret_node, [sp["use_edge"][i]])
                    else:
                        sp["location"][i].attach_bidirected(
                            ret_node, [sp["use_edge"][i]]
                        )
                    res.append(ret_node)
                return JacValue(self, value=res)
            else:
                self.rt_error(f'Spawn can not occur on {type(sp["location"])}!', kid[1])

    def run_walker_spawn(self, jac_ast):
        """
        walker_spawn: expression KW_SYNC? walker_ref spawn_ctx?;
        """
        kid = self.set_cur_ast(jac_ast)
        is_await = kid[1].name == "KW_SYNC" and bool(kid.pop(1))
        self.run_expression(kid[0])
        location = self.pop().value
        if isinstance(location, Node):
            location = JacSet(in_list=[location])
        ret = []
        for i in location.obj_list():
            walk = self.run_walker_ref(kid[1], is_await)
            walk.prime(i, request_ctx=getattr(self, "request_context", {}))
            if len(kid) > 2:
                self.run_spawn_ctx(kid[2], walk)

            res = walk.run()

            if walk.for_queue() and not res["is_queued"]:
                res["result"] = walk.anchor_value()

            tr = JacValue(self, value=res if walk.for_queue() else walk.anchor_value())
            ret.append(tr.value)
            self.inherit_runtime_state(walk)
            walk.register_yield_or_destroy(self.yielded_walkers_ids)
        return JacValue(self, value=ret[0] if len(ret) == 1 else ret)

    def run_type_spawn(self, jac_ast):
        """
        type_spawn: type_ref spawn_ctx?;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = self.run_type_ref(kid[0])
        if kid[-1].name == "spawn_ctx":
            self.run_spawn_ctx(kid[-1], ret.value)
        return ret

    def run_spawn_ctx(self, jac_ast, obj):
        """
        spawn_ctx: LPAREN (spawn_assign (COMMA spawn_assign)*)? RPAREN;
        """
        kid = self.set_cur_ast(jac_ast)
        for i in kid:
            if i.name == "spawn_assign":
                self.run_spawn_assign(i, obj)

    def run_filter_ctx(self, jac_ast, obj):
        """
        filter_ctx:
                LPAREN (filter_compare (COMMA filter_compare)*)? RPAREN;
        """
        kid = self.set_cur_ast(jac_ast)
        ret = JacSet()
        for i in obj.obj_list():
            for j in kid:
                if j.name == "filter_compare":
                    if self.run_filter_compare(j, i):
                        ret.add_obj(i)
        return ret

    def run_spawn_assign(self, jac_ast, obj):
        """
        spawn_assign: NAME EQ expression;
        """
        kid = self.set_cur_ast(jac_ast)
        name = kid[0].token_text()
        self.run_expression(kid[-1])
        result = self.pop().value
        if isinstance(obj, dict):
            obj[name] = result
            return
        dest = JacValue(self, ctx=obj, name=name, value=result)
        if obj.j_type == "walker":
            dest.write(kid[0], force=True)
        else:
            dest.write(kid[0])

    def run_filter_compare(self, jac_ast, obj):
        """
        filter_compare: NAME cmp_op expression;
        """
        kid = self.set_cur_ast(jac_ast)
        name = kid[0].token_text()
        if name in obj.context.keys():
            self.run_expression(kid[-1])
            result = self.pop()
            self.run_cmp_op(kid[1], JacValue(self, ctx=obj, name=name), result)
            return self.pop().value
        else:
            self.rt_error(f"{name} not present in object", kid[0])

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
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        if kid[0].name == "TYP_STRING":
            self.push(JacValue(self, value=str))
        elif kid[0].name == "TYP_INT":
            self.push(JacValue(self, value=int))
        elif kid[0].name == "TYP_FLOAT":
            self.push(JacValue(self, value=float))
        elif kid[0].name == "TYP_LIST":
            self.push(JacValue(self, value=list))
        elif kid[0].name == "TYP_DICT":
            self.push(JacValue(self, value=dict))
        elif kid[0].name == "TYP_BOOL":
            self.push(JacValue(self, value=bool))
        elif kid[0].name == "KW_NODE":
            self.push(JacValue(self, value=Node))
        elif kid[0].name == "KW_EDGE":
            self.push(JacValue(self, value=Edge))
        elif kid[0].name == "KW_TYPE":
            self.push(JacValue(self, value=type))
        else:
            self.rt_error("Unrecognized type", kid[0])

    def run_multistring(self, jac_ast):
        """
        multistring: STRING+;
        """
        if self.attempt_bytecode(jac_ast):
            return
        kid = self.set_cur_ast(jac_ast)
        ret = ""
        for i in kid:
            ret += parse_str_token(i.token_text())
        self.push(JacValue(self, value=ret))

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        super().destroy()

    # Helper Functions ##################
    def attempt_bytecode(self, jac_ast):
        if hasattr(jac_ast, "bytecode") and jac_ast.bytecode:
            self.run_bytecode(b64decode(jac_ast.bytecode.encode()))
            return True
        return False

    def call_ability(self, nd, name, act_list):
        ability = act_list.get_obj_by_name(name)
        try:
            ability.j_master = self.j_master
            ability._mast = self._mast
            ability.run_ability(here=nd, visitor=self._jac_scope.visitor())
        except Exception as e:
            self.rt_error(f"Internal Exception: {e}", ability._cur_jac_ast)
        self.inherit_runtime_state(ability)

    def visibility_prune(self, node_set=None):
        """Returns all nodes that shouldnt be ignored"""
        ret = JacSet()
        if node_set is None:
            node_set = self.here().attached_nodes()
        for i in node_set:
            if i not in self.ignore_node_ids.obj_list():
                ret.add_obj(i)
        return ret

    def run_rule(self, jac_ast, *args):
        """Helper to run rule if exists in execution context"""
        try:
            val = getattr(self, f"run_{jac_ast.name}")(jac_ast, *args)
            # TODO: Rewrite after stack integration
            if jac_ast.name in [
                "any_type",
                "atom",
                "arithmetic",
                "term",
                "factor",
                "power",
                "cmp_op",
                "compare",
                "logical",
                "expression",
                "assignment",
                "copy_assign",
                "inc_assign",
                "multistring",
            ]:
                return self.pop()
            else:
                return val
            # return getattr(self, f"run_{jac_ast.name}")(jac_ast, *args)
        except AttributeError as e:
            if not hasattr(self, f"run_{jac_ast.name}"):
                self.rt_error(
                    f"This scope cannot execute the statement "
                    f'"{jac_ast.get_text()}" of type {jac_ast.name}',
                    jac_ast,
                )
            else:
                self.rt_error(e, jac_ast)
            return
        except Exception as e:
            self.rt_error(e, jac_ast)

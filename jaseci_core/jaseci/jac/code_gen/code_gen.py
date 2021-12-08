"""
Code generator for jac code in AST form
"""
from jaseci.jac.machine.op_codes import op
from jaseci.jac.machine.builtin_refs import ref


class code_gen():
    """Shared code generator class across both sentinels and walkers"""

    def __init__(self):
        self.machine_code = []
        self.label = []

    def gen_attr_stmt(self, jac_ast, obj):
        """
        attr_stmt: has_stmt | can_stmt;
        """
        kid = jac_ast.kid
        if(kid[0].name == 'has_stmt'):
            self.gen_has_stmt(kid[0], obj)
        elif(kid[0].name == 'can_stmt'):
            self.gen_can_stmt(kid[0], obj)

    def gen_has_stmt(self, jac_ast, obj):
        """
        has_stmt:
                KW_HAS KW_PRIVATE? KW_ANCHOR? has_assign
                (COMMA has_assign)* SEMI;
        """
        kid = jac_ast.kid
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
            self.gen_has_assign(kid[0], obj, is_private, is_anchor)
            kid = kid[1:]
            if(not len(kid) or kid[0].name != 'COMMA'):
                break
            else:
                kid = kid[1:]

    def gen_has_assign(self, jac_ast, obj, is_private, is_anchor):
        """
        has_assign: NAME | NAME EQ expression;
        """
        kid = jac_ast.kid
        var_name = kid[0].token_text()
        if(len(kid) > 1):
            self.gen_expression(kid[2])
        if(is_anchor):
            self.g_ins([op.SET_ANCHOR, obj, var_name])
        if(var_name == '_private'):
            self.gt_error(
                f'Has variable name of `_private` not allowed!', kid[0])
        else:
            self.g_ins([op.CREATE_CTX_VAR, obj, var_name,
                       ref.RESULT_OUT, is_private])

    # def gen_can_stmt(self, jac_ast, obj):
    #     """
    #     can_stmt:
    #         KW_CAN dotted_name preset_in_out? event_clause? (
    #             COMMA dotted_name preset_in_out? event_clause?
    #         )* SEMI
    #         | KW_CAN NAME event_clause? code_block;
    #     """
    #     kid = jac_ast.kid
    #     kid = kid[1:]
    #     l_out = self.next_lab()
    #     self.g_ins([op.B_A, l_out])
    #     while True:
    #         l_act_code = self.next_lab()
    #         self.g_lab(l_act_code)
    #         action_type = 'activity'
    #         preset_in_out = {'input': [], 'output': None}
    #         if (kid[0].name == 'NAME'):
    #             action_name = kid[0].token_text()
    #         else:
    #             action_name = self.gen_dotted_name(kid[0])
    #         kid = kid[1:]
    #         if(len(kid) > 0 and kid[0].name == 'preset_in_out'):
    #             self.gen_preset_in_out(kid[0], obj)
    #             self.g_ins([op.SET_REF_VAR, ref.TMP1, ref.RESULT_OUT])
    #             kid = kid[1:]
    #         if(len(kid) > 0 and kid[0].name == 'event_clause'):
    #             action_type = self.gen_event_clause(kid[0])
    #             kid = kid[1:]
    #         if (not isinstance(obj, node)):  # only nodes have on entry/exit
    #             action_type = 'activity'
    #         if (kid[0].name == 'code_block'):

    #             getattr(obj, f"{action_type}_action_ids").add_obj(
    #                 action(
    #                     h=self._h,
    #                     name=action_name,
    #                     value=kid[0],
    #                     preset_in_out=preset_in_out,
    #                     is_lib=False
    #                 )
    #             )
    #             break
    #         else:
    #             func_link = \
    #                 self.get_builtin_action(action_name, jac_ast)
    #             if(func_link):
    #                 getattr(obj, f"{action_type}_action_ids").add_obj(
    #                     action(
    #                         h=self._h,
    #                         name=action_name,
    #                         value=func_link,
    #                         preset_in_out=preset_in_out
    #                     )
    #                 )
    #         if(not len(kid) or kid[0].name != 'COMMA'):
    #             break
    #         else:
    #             kid = kid[1:]
    #     self.g_lab(l_out)

    # def gen_event_clause(self, jac_ast):
    #     """
    #     event_clause: KW_WITH (KW_ENTRY | KW_EXIT | KW_ACTIVITY);
    #     """
    #     kid = jac_ast.kid
    #     return kid[1].token_text()

    # def run_preset_in_out(self, jac_ast, obj):
    #     """
    #     preset_in_out: DBL_COLON NAME (COMMA NAME)* (COLON_OUT NAME)?;
    #     """
    #     kid = jac_ast.kid
    #     result = {'input': [], 'output': None}
    #     for i in kid:
    #         if (i.name == 'NAME'):
    #             if (i.token_text() not in obj.context.keys()):
    #                 self.rt_error(f"No context for preset param {i}", i)
    #             else:
    #                 prm = jac_value(obj, i.token_text())
    #                 result['input'].append(prm)
    #     if (kid[-2].name == 'COLON_OUT'):
    #         result['input'].pop()
    #         result['output'] = jac_value(obj, kid[-1].token_text())
    #     return result

    # def run_code_block(self, jac_ast):
    #     """
    #     code_block: LBRACE statement* RBRACE | COLON statement;
    #     TODO: Handle breaks and continues
    #     """
    #     kid = jac_ast.kid
    #     for i in kid:
    #         if (self._loop_ctrl):
    #             if (self._loop_ctrl == 'continue'):
    #                 self._loop_ctrl = None
    #             return
    #         if(i.name == 'statement'):
    #             self.run_statement(jac_ast=i)

    # def run_node_ctx_block(self, jac_ast):
    #     """
    #     node_ctx_block: NAME (COMMA NAME)* code_block;
    #     """
    #     kid = jac_ast.kid
    #     while(kid[0].name != 'code_block'):
    #         if (self.current_node.name == kid[0].token_text()):
    #             self.run_code_block(kid[-1])
    #             return
    #         kid = kid[1:]

    # def run_statement(self, jac_ast):
    #     """
    #     statement:
    #         code_block
    #         | node_ctx_block
    #         | expression SEMI
    #         | if_stmt
    #         | for_stmt
    #         | while_stmt
    #         | ctrl_stmt SEMI
    #         | report_action
    #         | walker_action;
    #     """
    #     if (self._stopped):
    #         return
    #     kid = jac_ast.kid
    #     if(not hasattr(self, f'run_{kid[0].name}')):
    #         self.rt_error(
    #             f'This scope cannot execute the statement '
    #             f'"{kid[0].get_text()}" of type {kid[0].name}',
    #             kid[0])
    #         return
    #     stmt_func = getattr(self, f'run_{kid[0].name}')
    #     stmt_func(kid[0])

    # def run_if_stmt(self, jac_ast):
    #     """
    #     if_stmt: KW_IF expression code_block (elif_stmt)* (else_stmt)?;
    #     """
    #     kid = jac_ast.kid
    #     if(self.run_expression(kid[1])):
    #         self.run_code_block(kid[2])
    #         return
    #     kid = kid[3:]
    #     if(len(kid)):
    #         while True:
    #             if(kid[0].name == 'elif_stmt'):
    #                 if(self.run_elif_stmt(kid[0])):
    #                     return
    #             elif(kid[0].name == 'else_stmt'):
    #                 self.run_else_stmt(kid[0])
    #                 return
    #             kid = kid[1:]
    #             if(not len(kid)):
    #                 break

    # def run_elif_stmt(self, jac_ast):
    #     """
    #     elif_stmt: KW_ELIF expression code_block;
    #     """
    #     kid = jac_ast.kid
    #     if(self.run_expression(kid[1])):
    #         self.run_code_block(kid[2])
    #         return True
    #     else:
    #         return False

    # def run_else_stmt(self, jac_ast):
    #     """
    #     else_stmt: KW_ELSE code_block;
    #     """
    #     kid = jac_ast.kid
    #     self.run_code_block(kid[1])

    # def run_for_stmt(self, jac_ast):
    #     """
    #     for_stmt:
    #         KW_FOR expression KW_TO expression KW_BY expression code_block
    #         | KW_FOR NAME KW_IN expression code_block;
    #     """
    #     kid = jac_ast.kid
    #     loops = 0
    #     if(kid[1].name == 'expression'):
    #         self.run_expression(kid[1])
    #         while self.run_expression(kid[3]):
    #             self.run_code_block(kid[6])
    #             loops += 1
    #             if (self._loop_ctrl == 'break'):
    #                 self._loop_ctrl = None
    #                 break
    #             self.run_expression(kid[5])
    #             if(loops > self._loop_limit):
    #                 self.rt_error(f'Hit loop limit, breaking...', kid[0])
    #     else:
    #         var_name = kid[1].token_text()
    #         lst = self.run_expression(kid[3])
    #         # should check that lst is list here
    #         for i in lst:
    #             self._jac_scope.set_live_var(var_name, i, [], kid[3])
    #             self.run_code_block(kid[4])
    #             loops += 1
    #             if (self._loop_ctrl == 'break'):
    #                 self._loop_ctrl = None
    #                 break
    #             if(loops > self._loop_limit):
    #                 self.rt_error(f'Hit loop limit, breaking...', kid[0])

    # def run_while_stmt(self, jac_ast):
    #     """
    #     while_stmt: KW_WHILE expression code_block;
    #     """
    #     kid = jac_ast.kid
    #     loops = 0
    #     while self.run_expression(kid[1]):
    #         self.run_code_block(kid[2])
    #         loops += 1
    #         if (self._loop_ctrl == 'break'):
    #             self._loop_ctrl = None
    #             break
    #         if(loops > self._loop_limit):
    #             self.rt_error(f'Hit loop limit, breaking...', kid[0])

    # def run_ctrl_stmt(self, jac_ast):
    #     """
    #     ctrl_stmt: KW_CONTINUE | KW_BREAK | KW_SKIP;
    #     """
    #     kid = jac_ast.kid
    #     if (kid[0].name == 'KW_SKIP'):
    #         self._stopped = 'skip'
    #     elif (kid[0].name == 'KW_BREAK'):
    #         self._loop_ctrl = 'break'
    #     elif (kid[0].name == 'KW_CONTINUE'):
    #         self._loop_ctrl = 'continue'

    # def run_report_action(self, jac_ast):
    #     """
    #     report_action: KW_REPORT expression SEMI;
    #     """
    #     kid = jac_ast.kid
    #     report = self.run_expression(kid[1])
    #     report = self._jac_scope.report_deep_serialize(report)
    #     if(not is_jsonable(report)):
    #         self.rt_error(f'Report not Json serializable', kid[0])
    #     self.report.append(report)

    # def run_expression(self, jac_ast):
    #     """
    #     expression: assignment | connect;
    #     """
    #     kid = jac_ast.kid
    #     expr_func = getattr(self, f'run_{kid[0].name}')
    #     return expr_func(kid[0])

    # def run_assignment(self, jac_ast, assign_scope=None):
    #     """
    #     assignment:
    #         dotted_name index* EQ expression
    #         | inc_assign
    #         | copy_assign;

    #     """
    #     kid = jac_ast.kid
    #     if (len(kid) < 2):
    #         if (assign_scope is not None):
    #             self.rt_error("Can only use '=' with spawn", kid[0])
    #         assign_func = getattr(self, f'run_{kid[0].name}')
    #         return assign_func(kid[0])
    #     var_name = self.run_dotted_name(kid[0])
    #     arr_idx = []
    #     for i in kid:
    #         if(i.name == 'index'):
    #             arr_idx.append(self.run_index(i))
    #     result = self.run_expression(kid[-1])
    #     if (assign_scope is None):
    #         self._jac_scope.set_live_var(var_name, result, arr_idx, kid[0])
    #     else:
    #         if(isinstance(result, element)):
    #             result = result.id.urn
    #         assign_scope[var_name] = result
    #     return result

    # def run_inc_assign(self, jac_ast):
    #     """
    #     inc_assign:
    #             dotted_name index* (PEQ | MEQ | TEQ | DEQ) expression;
    #     """
    #     kid = jac_ast.kid
    #     var_name = self.run_dotted_name(kid[0])
    #     arr_idx = []
    #     for i in kid:
    #         if(i.name == 'index'):
    #             arr_idx.append(self.run_index(i))
    #     result = self._jac_scope.get_live_var(var_name, kid[0])
    #     if(kid[1].name == 'PEQ'):
    #         result = result + self.run_expression(kid[2])
    #     elif(kid[1].name == 'MEQ'):
    #         result = result - self.run_expression(kid[2])
    #     elif(kid[1].name == 'TEQ'):
    #         result = result * self.run_expression(kid[2])
    #     elif(kid[1].name == 'DEQ'):
    #         result = result / self.run_expression(kid[2])
    #     self._jac_scope.set_live_var(var_name, result, arr_idx, kid[0])
    #     return result

    # def run_copy_assign(self, jac_ast):
    #     """
    #     copy_assign: dotted_name index* CPY_EQ expression;
    #     """
    #     kid = jac_ast.kid
    #     var_name = self.run_dotted_name(kid[0])
    #     dest = self._jac_scope.get_live_var(var_name, kid[0])
    #     for i in kid:
    #         if(i.name == 'index'):
    #             dest = dest[self.run_index(i)]
    #     src = self.run_expression(kid[2])
    #     if (not self.rt_check_type(dest, node, kid[0]) or not
    #             self.rt_check_type(dest, node, kid[0])):
    #         self.rt_error("':=' only applies to nodes", kid[0])
    #         return dest
    #     if (dest.name != src.name):
    #         self.rt_error(f"Node arch {dest} don't match {src}!", kid[0])
    #         return dest
    #     for i in src.context.keys():
    #         if(i in dest.context.keys()):
    #             dest.context[i] = src.context[i]
    #     return dest

    # def run_connect(self, jac_ast):
    #     """
    #     connect: logical ( (NOT)? edge_ref expression)?;
    #     """
    #     kid = jac_ast.kid
    #     if (len(kid) < 2):
    #         return self.run_logical(kid[0])
    #     base = self.run_logical(kid[0])
    #     target = self.run_expression(kid[-1])
    #     self.rt_check_type(base, node, kid[0])
    #     self.rt_check_type(target, [node, jac_set], kid[-1])
    #     if (kid[1].name == 'NOT'):
    #         # TODO: IF JACSET IS TARGET APLLY TO ALL MEMEBERS OF JACSET
    #         # Line below PARTIALLY generalizes disconnect NEEDS REVIEW
    #         if(isinstance(target, node)):
    #             base.detach_edges(target,
    #                               self.run_edge_ref(kid[2]).obj_list())
    #         elif(isinstance(target, jac_set)):
    #             for i in target.obj_list():
    #                 base.detach_edges(i,
    #                                   self.run_edge_ref(kid[2]).obj_list())
    #         else:
    #             logger.critical(
    #                 f'Cannot connect to {target} of type {type(target)}!')
    #         target = base
    #     else:
    #         direction = kid[1].kid[0].name
    #         if(isinstance(target, node)):
    #             target = jac_set(self, in_list=[target.jid])
    #         if(isinstance(target, jac_set)):
    #             for i in target.obj_list():
    #                 use_edge = self.run_edge_ref(kid[1], is_spawn=True)
    #                 if (direction == 'edge_from'):
    #                     base.attach_inbound(i, [use_edge])
    #                 elif (direction == 'edge_to'):
    #                     base.attach_outbound(i, [use_edge])
    #                 else:
    #                     base.attach_bidirected(i, [use_edge])
    #     return target

    # def run_logical(self, jac_ast):
    #     """
    #     logical: compare ((KW_AND | KW_OR) compare)*;
    #     """
    #     kid = jac_ast.kid
    #     result = self.run_compare(kid[0])
    #     kid = kid[1:]
    #     while (kid):
    #         if (kid[0].name == 'KW_AND'):
    #             if (result):
    #                 result = result and self.run_compare(kid[1])
    #         elif (kid[0].name == 'KW_OR'):
    #             if (not result):
    #                 result = result or self.run_compare(kid[1])
    #         kid = kid[2:]
    #         if(not kid):
    #             break
    #     return result

    # def run_compare(self, jac_ast):
    #     """
    #     compare:
    #         NOT compare
    #         | arithmetic (
    #             (EE | LT | GT | LTE | GTE | NE | KW_IN | nin) arithmetic
    #         )*;
    #     """
    #     kid = jac_ast.kid
    #     if(kid[0].name == 'NOT'):
    #         return not self.run_compare(kid[1])
    #     else:
    #         result = self.run_arithmetic(kid[0])
    #         kid = kid[1:]
    #         while (kid):
    #             other_res = self.run_arithmetic(kid[1])
    #             if(kid[0].name == 'EE'):
    #                 result = result == other_res
    #             elif(kid[0].name == 'LT'):
    #                 result = result < other_res
    #             elif(kid[0].name == 'GT'):
    #                 result = result > other_res
    #             elif(kid[0].name == 'LTE'):
    #                 result = result <= other_res
    #             elif(kid[0].name == 'GTE'):
    #                 result = result >= other_res
    #             elif(kid[0].name == 'NE'):
    #                 result = result != other_res
    #             elif(kid[0].name == 'KW_IN'):
    #                 result = result in other_res
    #             elif(kid[0].name == 'nin'):
    #                 result = result not in other_res
    #             kid = kid[2:]
    #             if(not kid):
    #                 break
    #         return result

    # def run_arithmetic(self, jac_ast):
    #     """
    #     arithmetic: term ((PLUS | MINUS) term)*;
    #     """
    #     kid = jac_ast.kid
    #     result = self.run_term(kid[0])
    #     kid = kid[1:]
    #     while (kid):
    #         other_res = self.run_term(kid[1])
    #         if(kid[0].name == 'PLUS'):
    #             result = result + other_res
    #         elif(kid[0].name == 'MINUS'):
    #             result = result - other_res
    #         kid = kid[2:]
    #         if(not kid):
    #             break
    #     return result

    # def run_term(self, jac_ast):
    #     """
    #     term: factor ((MUL | DIV | MOD) factor)*;
    #     """
    #     kid = jac_ast.kid
    #     result = self.run_factor(kid[0])
    #     kid = kid[1:]
    #     while (kid):
    #         other_res = self.run_factor(kid[1])
    #         if(kid[0].name == 'MUL'):
    #             result = result * other_res
    #         elif(kid[0].name == 'DIV'):
    #             result = result / other_res
    #         elif(kid[0].name == 'MOD'):
    #             result = result % other_res
    #         kid = kid[2:]
    #         if(not kid):
    #             break
    #     return result

    # def run_factor(self, jac_ast):
    #     """
    #     factor: (PLUS | MINUS) factor | power;
    #     """
    #     kid = jac_ast.kid
    #     if(kid[0].name == 'power'):
    #         return self.run_power(kid[0])
    #     else:
    #         result = self.run_factor(kid[1])
    #         if(kid[0].name == 'MINUS'):
    #             result = -(result)
    #         return result

    # def run_power(self, jac_ast):
    #     """
    #     power: func_call (POW factor)* | func_call index+;
    #     """
    #     kid = jac_ast.kid
    #     result = self.run_func_call(kid[0])
    #     kid = kid[1:]
    #     if(len(kid) < 1):
    #         return result
    #     elif(kid[0].name == 'POW'):
    #         while (kid):
    #             result = result ** self.run_factor(kid[1])
    #             kid = kid[2:]
    #             if(not kid):
    #                 break
    #         return result
    #     elif (kid[0].name == "index"):
    #         if(isinstance(result, list) or isinstance(result, dict)):
    #             for i in kid:
    #                 if(i.name == 'index'):
    #                     result = result[self.run_index(i)]
    #             result = self._jac_scope.reference_to_value(result)
    #             return result
    #         else:
    #             self.rt_error(f'Cannot index into {result}'
    #                           f' of type {type(result)}!',
    #                           kid[0])
    #             return 0

    # def run_func_call(self, jac_ast):
    #     """
    #     func_call:
    #         atom (LPAREN (expression (COMMA expression)*)? RPAREN)?
    #         | atom DOT func_built_in
    #         | atom? DBL_COLON NAME;
    #     """
    #     kid = jac_ast.kid
    #     atom_res = self._jac_scope.has_obj
    #     if (kid[0].name == 'atom'):
    #         atom_res = self.run_atom(kid[0])
    #         kid = kid[1:]
    #     if(len(kid) < 1):
    #         return atom_res
    #     elif(kid[0].name == 'DOT'):
    #         return self.run_func_built_in(atom_res, kid[1])
    #     elif (kid[0].name == 'DBL_COLON'):
    #         m = interp(owner_override=self.owner())
    #         m.push_scope(jac_scope(owner=self,
    #                                has_obj=atom_res,
    #                                action_sets=[atom_res.activity_action_ids]))
    #         m.run_code_block(atom_res.activity_action_ids.get_obj_by_name(
    #             kid[1].token_text()).value)
    #         self.report = self.report + m.report
    #         return atom_res
    #     elif(kid[0].name == "LPAREN"):
    #         param_list = []
    #         kid = kid[1:]
    #         while True:
    #             if(kid[0].name == 'RPAREN'):
    #                 break
    #             param_list.append(self.run_expression(kid[0]))
    #             kid = kid[1:]
    #             if (kid[0].name == 'COMMA'):
    #                 kid = kid[1:]
    #         if (isinstance(atom_res, action)):
    #             return atom_res.trigger(param_list)
    #         else:
    #             self.rt_error(f'Unable to execute function {atom_res}',
    #                           kid[0])

    # def run_func_built_in(self, atom_res, jac_ast):
    #     """
    #     func_built_in:
    #         | KW_LENGTH
    #         | KW_KEYS
    #         | KW_EDGE
    #         | KW_NODE
    #         | KW_DESTROY LPAREN expression RPAREN;
    #     """
    #     kid = jac_ast.kid
    #     if (kid[0].name == "KW_LENGTH"):
    #         if(isinstance(atom_res, list)):
    #             return len(atom_res)
    #         else:
    #             self.rt_error(f'Cannot get length of {atom_res}. Not List!',
    #                           kid[0])
    #             return 0
    #     elif (kid[0].name == "KW_KEYS"):
    #         if(isinstance(atom_res, dict)):
    #             return atom_res.keys()
    #         else:
    #             self.rt_error(f'Cannot get keys of {atom_res}. '
    #                           f'Not Dictionary!', kid[0])
    #             return []
    #     elif (kid[0].name == "KW_EDGE"):
    #         if(isinstance(atom_res, node)):
    #             return self.obj_set_to_jac_set(
    #                 self.current_node.attached_edges(atom_res))
    #         elif(isinstance(atom_res, edge)):
    #             return atom_res
    #         elif(isinstance(atom_res, jac_set)):
    #             res = jac_set(self)
    #             for i in atom_res.obj_list():
    #                 if(isinstance(i, edge)):
    #                     res.add_obj(i)
    #                 elif(isinstance(i, node)):
    #                     res += self.obj_set_to_jac_set(
    #                         self.current_node.attached_edges(i))
    #             return res
    #         else:
    #             self.rt_error(f'Cannot get edges from {atom_res}. '
    #                           f'Type {type(atom_res)} invalid', kid[0])
    #             return atom_res
    #     # may want to remove 'here" node from return below
    #     elif (kid[0].name == "KW_NODE"):
    #         if(isinstance(atom_res, node)):
    #             return atom_res
    #         elif(isinstance(atom_res, edge)):
    #             return self.obj_set_to_jac_set(atom_res.nodes())
    #         elif(isinstance(atom_res, jac_set)):
    #             res = jac_set(self)
    #             for i in atom_res.obj_list():
    #                 if(isinstance(i, edge)):
    #                     res.add_obj(i.to_node())
    #                     res.add_obj(i.from_node())
    #                 elif(isinstance(i, node)):
    #                     res.add_obj(i)
    #             return res
    #         else:
    #             self.rt_error(f'Cannot get edges from {atom_res}. '
    #                           f'Type {type(atom_res)} invalid', kid[0])
    #             return atom_res
    #     elif (kid[0].name == "KW_DESTROY"):
    #         idx = self.run_expression(kid[2])
    #         if (isinstance(atom_res, list) and isinstance(idx, int)):
    #             del atom_res[idx]
    #             return atom_res
    #         else:
    #             self.rt_error(f'Cannot remove index {idx} from {atom_res}.',
    #                           kid[0])
    #             return atom_res

    # def run_atom(self, jac_ast):
    #     """
    #     atom:
    #         INT
    #         | FLOAT
    #         | STRING
    #         | BOOL
    #         | array_ref
    #         | node_edge_ref
    #         | list_val
    #         | dotted_name
    #         | LPAREN expression RPAREN
    #         | spawn
    #         | DEREF expression;
    #     """
    #     kid = jac_ast.kid
    #     if(kid[0].name == 'INT'):
    #         return int(kid[0].token_text())
    #     elif(kid[0].name == 'FLOAT'):
    #         return float(kid[0].token_text())
    #     elif(kid[0].name == 'STRING'):
    #         return self.parse_str_token(kid[0].token_text())
    #     elif(kid[0].name == 'BOOL'):
    #         return bool(kid[0].token_text() == 'true')

    #     elif(kid[0].name == 'dotted_name'):
    #         return self._jac_scope.get_live_var(self.run_dotted_name(kid[0]),
    #                                             kid[0])
    #     elif(kid[0].name == 'LPAREN'):
    #         return self.run_expression(kid[1])
    #     elif (kid[0].name == 'DEREF'):
    #         result = self.run_expression(kid[1])
    #         if (self.rt_check_type(result, element, kid[1])):
    #             result = result.jid
    #         return result
    #     else:
    #         return getattr(self, f'run_{kid[0].name}')(kid[0])

    # def run_node_edge_ref(self, jac_ast):
    #     """
    #     node_edge_ref: node_ref | edge_ref (node_ref)?;
    #     """
    #     kid = jac_ast.kid
    #     is_nodeset = True
    #     if(kid[0].name == 'KW_NODE'):
    #         kid = kid[2:]
    #     if(kid[0].name == 'KW_EDGE'):
    #         kid = kid[2:]
    #         is_nodeset = False

    #     if(kid[0].name == 'node_ref'):
    #         if(is_nodeset):
    #             return self.run_node_ref(kid[0])
    #         else:
    #             return self.obj_set_to_jac_set(
    #                 self.current_node.attached_edges(
    #                     self.run_node_ref(kid[0])))
    #     elif (kid[0].name == 'edge_ref'):
    #         if(is_nodeset):
    #             result = self.edge_to_node_jac_set(self.run_edge_ref(kid[0]))
    #             if(len(kid) > 1 and kid[1].name == 'node_ref'):
    #                 result = result * self.run_node_ref(kid[1])
    #             return result
    #         else:
    #             result = self.run_edge_ref(kid[0])
    #             if(kid[1].name == 'node_ref'):
    #                 result = jac_set(
    #                     self, inlist=[i for i in result if i in
    #                                   self.obj_set_to_jac_set(
    #                                       self.current_node.attached_edges(
    #                                           self.run_node_ref(kid[1])))])
    #             return result

    # def run_node_ref(self, jac_ast, is_spawn=False):
    #     """
    #     node_ref: KW_NODE DBL_COLON NAME;
    #     """
    #     kid = jac_ast.kid
    #     if(not is_spawn):
    #         result = jac_set(self.owner())
    #         if (len(kid) > 1):
    #             for i in self.viable_nodes().obj_list():
    #                 if (i.name == kid[2].token_text()):
    #                     result.add_obj(i)
    #         else:
    #             result += self.viable_nodes()
    #     else:
    #         if(len(kid) > 1):
    #             result = self.owner().arch_ids.get_obj_by_name(
    #                 kid[2].token_text(), kind='node').run()
    #         else:
    #             result = node(h=self._h)
    #     return result

    # def run_walker_ref(self, jac_ast):
    #     """
    #     walker_ref: KW_WALKER DBL_COLON NAME;
    #     """
    #     kid = jac_ast.kid
    #     return self.owner().spawn_walker(kid[2].token_text())

    # def run_graph_ref(self, jac_ast):
    #     """
    #     graph_ref: KW_GRAPH DBL_COLON NAME;
    #     """
    #     kid = jac_ast.kid
    #     gph = self.owner().arch_ids.get_obj_by_name(
    #         kid[2].token_text(), kind='graph').run()
    #     return gph

    # def run_edge_ref(self, jac_ast, is_spawn=False):
    #     """
    #     edge_ref: edge_to | edge_from | edge_any;
    #     """
    #     kid = jac_ast.kid
    #     if(not is_spawn):
    #         expr_func = getattr(self, f'run_{kid[0].name}')
    #         return expr_func(kid[0])
    #     else:
    #         if(len(kid[0].kid) > 2):
    #             result = self.owner().arch_ids.get_obj_by_name(
    #                 kid[0].kid[2].token_text(), kind='edge').run()
    #         else:
    #             result = edge(h=self._h, kind='edge', name='generic')
    #         return result

    # def run_edge_to(self, jac_ast):
    #     """
    #     edge_to: '-' ('[' NAME ']')? '->';
    #     """
    #     kid = jac_ast.kid
    #     result = jac_set(self.owner())
    #     for i in self.current_node.outbound_edges() + \
    #             self.current_node.bidirected_edges():
    #         if (len(kid) > 2 and i.name != kid[2].token_text()):
    #             continue
    #         result.add_obj(i)
    #     return result

    # def run_edge_from(self, jac_ast):
    #     """
    #     edge_from: '<-' ('[' NAME ']')? '-';
    #     """
    #     kid = jac_ast.kid
    #     result = jac_set(self.owner())
    #     for i in self.current_node.inbound_edges() + \
    #             self.current_node.bidirected_edges():
    #         if (len(kid) > 2 and i.name != kid[2].token_text()):
    #             continue
    #         result.add_obj(i)
    #     return result

    # def run_edge_any(self, jac_ast):
    #     """
    #     edge_any: '<-' ('[' NAME ']')? '->';
    #     NOTE: these do not use strict bidirected semantic but any edge
    #     """
    #     kid = jac_ast.kid
    #     result = jac_set(self.owner())
    #     for i in self.current_node.attached_edges():
    #         if (len(kid) > 2 and i.name != kid[2].token_text()):
    #             continue
    #         result.add_obj(i)
    #     return result

    # def run_list_val(self, jac_ast):
    #     """
    #     list_val: LSQUARE (expression (COMMA expression)*)? RSQUARE;
    #     """
    #     kid = jac_ast.kid
    #     list_res = []
    #     for i in kid:
    #         if(i.name == 'expression'):
    #             list_res.append(self.run_expression(i))
    #     return list_res

    # def run_index(self, jac_ast):
    #     """
    #     index: LSQUARE expression RSQUARE;
    #     """
    #     kid = jac_ast.kid
    #     idx = self.run_expression(kid[1])
    #     if(not isinstance(idx, int) and not isinstance(idx, str)):
    #         self.rt_error(f'Index of type {type(idx)} not valid. '
    #                       f'Indicies must be an integer or string!', kid[1])
    #         return None
    #     return idx

    # def run_dict_val(self, jac_ast):
    #     """
    #     dict_val: LBRACE (kv_pair (COMMA kv_pair)*)? RBRACE;
    #     """
    #     kid = jac_ast.kid
    #     dict_res = {}
    #     for i in kid:
    #         if(i.name == 'kv_pair'):
    #             self.run_kv_pair(i, dict_res)
    #     return dict_res

    # def run_kv_pair(self, jac_ast, obj):
    #     """
    #     kv_pair: STRING COLON expression;
    #     """
    #     kid = jac_ast.kid
    #     obj[self.parse_str_token(kid[0].token_text())
    #         ] = self.run_expression(kid[2])

    # def run_spawn(self, jac_ast):
    #     """
    #     spawn: KW_SPAWN expression spawn_object;

    #     NOTE: spawn statements support locations that are either nodes or
    #     jac_sets
    #     """
    #     kid = jac_ast.kid
    #     if(kid[1].name == 'expression'):
    #         location = self.run_expression(kid[1])
    #         if(isinstance(location, node)):
    #             return self.run_spawn_object(kid[2], location)
    #         elif(isinstance(location, jac_set)):
    #             res = []
    #             for i in location.obj_list():
    #                 res.append(self.run_spawn_object(kid[2], i))
    #             return res
    #         else:
    #             self.rt_error(
    #                 f'Spawn can not occur on {type(location)}!', kid[1])
    #     else:
    #         return self.run_spawn_object(kid[1], None)

    # def run_spawn_object(self, jac_ast, location):
    #     """
    #     spawn_object: node_spawn | walker_spawn;
    #     """
    #     kid = jac_ast.kid
    #     expr_func = getattr(self, f'run_{kid[0].name}')
    #     return expr_func(kid[0], location)

    # def run_node_spawn(self, jac_ast, location):
    #     """
    #     node_spawn: edge_ref? node_ref spawn_ctx?;
    #     """
    #     kid = jac_ast.kid
    #     if(kid[0].name == 'node_ref'):
    #         ret_node = self.run_node_ref(kid[0], is_spawn=True)
    #     else:
    #         use_edge = self.run_edge_ref(kid[0], is_spawn=True)
    #         ret_node = self.run_node_ref(kid[1], is_spawn=True)
    #         direction = kid[0].kid[0].name
    #         if (direction == 'edge_from'):
    #             location.attach_inbound(ret_node, [use_edge])
    #         elif (direction == 'edge_to'):
    #             location.attach_outbound(ret_node, [use_edge])
    #         else:
    #             location.attach_bidirected(ret_node, [use_edge])
    #     if (kid[-1].name == 'spawn_ctx'):
    #         self.run_spawn_ctx(kid[-1], ret_node)
    #     return ret_node

    # def run_walker_spawn(self, jac_ast, location):
    #     """
    #     walker_spawn: walker_ref spawn_ctx?;
    #     """
    #     kid = jac_ast.kid
    #     walk = self.run_walker_ref(kid[0])
    #     walk.prime(location)
    #     if(len(kid) > 1):
    #         self.run_spawn_ctx(kid[1], walk)
    #     walk.run()
    #     ret = self._jac_scope.reference_to_value(walk.anchor_value())
    #     self.report = self.report + walk.report
    #     walk.destroy()
    #     return ret

    # def run_graph_spawn(self, jac_ast, location):
    #     """
    #     graph_spawn: edge_ref graph_ref;
    #     """
    #     kid = jac_ast.kid
    #     use_edge = self.run_edge_ref(kid[0], is_spawn=True)
    #     result = self.run_graph_ref(kid[1])
    #     direction = kid[0].kid[0].name
    #     if (direction == 'edge_from'):
    #         location.attach_inbound(result, [use_edge])
    #     elif (direction == 'edge_to'):
    #         location.attach_outbound(result, [use_edge])
    #     else:
    #         location.attach_bidirected(result, [use_edge])
    #     return result

    # def run_spawn_ctx(self, jac_ast, obj):
    #     """
    #     spawn_ctx: LPAREN (assignment (COMMA assignment)*)? RPAREN;
    #     """
    #     kid = jac_ast.kid
    #     for i in kid:
    #         if (i.name == 'assignment'):
    #             self.run_assignment(i, assign_scope=obj.context)

    # def gen_dotted_name(self, jac_ast):
    #     """
    #     dotted_name: NAME (DOT NAME)*;
    #     """
    #     kid = jac_ast.kid
    #     ret = ''
    #     while True:
    #         ret += kid[0].token_text()
    #         kid = kid[1:]
    #         if(not len(kid) or kid[0].name != 'DOT'):
    #             break
    #         if(kid[0].name == 'DOT'):
    #             ret += '.'
    #             kid = kid[1:]
    #     return ret

    # Helper Functions ##################
    def g_ins(self, ins):
        """Generates op with specified parameters"""
        self.machine_code.append(ins)

    def g_lab(self, name):
        """Inserts label in code"""
        self.machine_code.append(name)

    def next_lab(self):
        """Generate and return new label"""
        lab = f'L{len(self.label)}'
        self.label.append(lab)
        return lab

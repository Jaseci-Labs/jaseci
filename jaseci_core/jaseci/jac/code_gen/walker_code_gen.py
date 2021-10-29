"""
Walker code generator for jac code in AST form
"""
from jaseci.jac.code_gen.code_gen import code_gen
from jaseci.jac.machine.op_codes import op
from jaseci.jac.machine.builtin_refs import ref
from jaseci.graph.node import node
from jaseci.jac.jac_set import jac_set


class walker_code_gen(code_gen):
    """Jac walker code generator class"""

    def gen_walkter(self, jac_ast):
        """
        walker:
            KW_WALKER NAME LBRACE attr_stmt* walk_entry_block? (
                statement
                | walk_activity_block
            )* walk_exit_block? RBRACE;
        """
        kid = jac_ast.kid
        self.g_ins([op.PUSH_SCOPE_W])
        self.g_ins([op.SET_LIVE_VAR, 'here', ref.HERE_ID, []])
        l_skip_attr = self.next_lab()
        self.g_ins([op.B_NEQI, ref.STEP, 0, l_skip_attr])
        for i in kid:
            if(i.name == 'attr_stmt'):
                self.gen_attr_stmt(jac_ast=i, obj=ref.SELF)
        self.g_lab(l_skip_attr)
        for i in kid:
            if(i.name == 'walk_entry_block'):
                self.gen_walk_entry_block(i)
            if(i.name == 'statement'):
                self.gen_statement(i)
            if(i.name == 'walk_activity_block'):
                self.gen_walk_activity_block(i)
            if(i.name == 'walk_exit_block'):
                self.gen_walk_exit_block(i)
        self.g_ins([op.POP_SCOPE])
        self.g_ins([op.END])

    def gen_walk_entry_block(self, jac_ast):
        """
        walk_entry_block: KW_WITH KW_ENTRY code_block;
        """
        kid = jac_ast.kid
        l_skip = self.next_lab()
        self.g_ins([op.B_NEQI, ref.STEP, 0, l_skip])
        self.g_ins([op.SET_REF_VARI, ref.IN_ENT_EXIT, True])
        self.gen_code_block(kid[2])
        self.g_ins([op.SET_REF_VARI, ref.IN_ENT_EXIT, False])
        self.g_lab(l_skip)

    def gen_walk_activity_block(self, jac_ast):
        """
        walk_activity_block: KW_WITH KW_ACTIVITY code_block;
        """
        kid = jac_ast.kid
        self.gen_code_block(kid[2])

    def gen_walker_action(self, jac_ast):
        """
        walker_action:
            ignore_action
            | take_action
            | destroy_action
            | KW_DISENGAGE SEMI;
        """
        kid = jac_ast.kid
        if (kid[0].name == 'KW_DISENGAGE'):
            self.g_ins([op.SET_REF_VARI, ref.STOPPED, 'stop'])
            self.g_ins([op.IDS_CLEAR, ref.NEXT_N_IDS])
        else:
            expr_func = getattr(self, f'gen_{kid[0].name}')
            expr_func(kid[0])

    def gen_ignore_action(self, jac_ast):
        """
        ignore_action: KW_IGNORE expression SEMI;
        """
        kid = jac_ast.kid
        self.gen_expression(kid[1])
        l_out = self.next_lab()
        l_skip = self.next_lab()
        self.g_ins([op.B_NIT, ref.RESULT_OUT, node, l_skip])
        self.g_ins([op.IDS_ADD_OBJ, ref.IGNORE_N_IDS, ref.RESULT_OUT])
        self.g_ins([op.B_A, l_out])
        self.g_lab(l_skip)

        l_skip = self.next_lab()
        self.g_ins([op.B_NIT, ref.RESULT_OUT, jac_set, l_skip])
        self.g_ins([op.PLUS, ref.IGNORE_N_IDS,
                   ref.IGNORE_N_IDS,  ref.RESULT_OUT])
        self.g_ins([op.B_A, l_out])
        self.g_lab(l_skip)
        self.gen_rt_error('is not ignorable type (i.e., nodes)',
                          ref.RESULT_OUT)
        self.g_lab(l_out)

    def gen_take_action(self, jac_ast):
        """
        take_action:
            KW_TAKE expression (SEMI | else_stmt);
        """
        kid = jac_ast.kid
        self.gen_expression(kid[1])
        self.g_ins([op.IDS_GET_LEN, ref.TMP1, ref.NEXT_N_IDS])
        # before = len(self.next_node_ids)
        l_out = self.next_lab()
        l_skip = self.next_lab()
        self.g_ins([op.B_NIT, ref.RESULT_OUT, node, l_skip])
        self.g_ins([op.IDS_ADD_OBJ, ref.NEXT_N_IDS, ref.RESULT_OUT])
        self.g_ins([op.B_A, l_out])
        self.g_lab(l_skip)

        l_skip = self.next_lab()
        self.g_ins([op.B_NIT, ref.RESULT_OUT, jac_set, l_skip])
        self.g_ins([op.PLUS, ref.NEXT_N_IDS,
                   ref.NEXT_N_IDS,  ref.RESULT_OUT])
        self.g_ins([op.B_A, l_out])
        self.g_lab(l_skip)
        self.gen_rt_error('is not destination type (i.e., nodes)',
                          ref.RESULT_OUT)
        self.g_lab(l_out)
        self.g_ins([op.IDS_GET_LEN, ref.TMP2, ref.NEXT_N_IDS])
        if (kid[2].name == 'else_stmt'):
            l_skip = self.next_lab()
            self.g_ins([op.B_NEQ, ref.TMP1, ref.TMP2, l_skip])
            self.gen_else_stmt(kid[2])
            self.g_lab(l_skip)

    def gen_destroy_action(self, jac_ast):
        """
        destroy_action: KW_DESTROY expression SEMI;
        """
        kid = jac_ast.kid
        self.gen_expression(kid[1])
        l_out = self.next_lab()
        l_skip = self.next_lab()
        self.g_ins([op.B_NIT, ref.RESULT_OUT, node, l_skip])
        self.g_ins([op.IDS_ADD_OBJ, ref.DESTROY_N_IDS, ref.RESULT_OUT])
        self.g_ins([op.B_A, l_out])
        self.g_lab(l_skip)

        l_skip = self.next_lab()
        self.g_ins([op.B_NIT, ref.RESULT_OUT, jac_set, l_skip])
        self.g_ins([op.PLUS, ref.DESTROY_N_IDS,
                   ref.DESTROY_N_IDS,  ref.RESULT_OUT])
        self.g_ins([op.B_A, l_out])
        self.g_lab(l_skip)
        self.gen_rt_error('is not destroyable type (i.e., nodes)',
                          ref.RESULT_OUT)
        self.g_lab(l_out)

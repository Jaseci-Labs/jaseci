"""
Walker code generator for jac code in AST form
"""
from jaseci.jac.code_gen.code_gen import code_gen
from jaseci.jac.machine.op_codes import op_code
from jaseci.jac.machine.builtin_refs import w_ref


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
        self.g_ins([op_code.PUSH_SCOPE_W])
        self.g_ins([op_code.SET_LIVE_VAR, 'here', w_ref.HERE_ID])
        l_skip_attr = self.next_lab()
        self.g_ins([op_code.B_NEQ, w_ref.STEP, 0, l_skip_attr])
        for i in kid:
            if(i.name == 'attr_stmt'):
                self.gen_attr_stmt(jac_ast=i, obj=self)
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
        self.g_ins([op_code.POP_SCOPE])
        self.g_ins([op_code.END])

    def run_walk_entry_block(self, jac_ast):
        """
        walk_entry_block: KW_WITH KW_ENTRY code_block;
        """
        kid = jac_ast.kid
        self.g_ins([op_code.B_NEQ, w_ref.STEP, 0, w_lab.SKIP_ATTR])
        if (self.current_step == 0):
            self.in_entry_exit = True
            self.run_code_block(kid[2])
            self.in_entry_exit = False

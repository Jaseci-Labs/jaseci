"""Transpilation pass for Jaseci Ast."""
from jaseci.jac.passes.ir_pass import AstNode, Pass


# MACROS for rapid development
MAST = "active_master"
MAST_PATH = "jaseci.core.master"
SENT = f"{MAST}.active_sentinel"
RT = f"{MAST}.runtime"
SET_LINE_FUNC = lambda x: f"{RT}set_line('{x}')\n"  # noqa
REG_GLOB_FUNC = lambda x, y: f"{RT}.register_global({x}, {y})\n"  # noqa


class TranspilePass(Pass):
    """Jac transpilation to python pass."""

    def __init__(self: "TranspilePass", ir: AstNode) -> None:
        """Initialize pass."""
        super().__init__(ir)
        self.indent_size = 4

    def exit_start(self: "TranspilePass", node: AstNode) -> None:
        """Convert start to python code.

        start -> element_list
        """
        node.py_code = node.kid[0].py_code

    def exit_element_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert element list to python code.

        element_list -> element_list element
        element_list -> element
        """
        for i in node.kid:
            node.py_code += i.py_code + "\n"

    def exit_element(self: "TranspilePass", node: AstNode) -> None:
        """Convert element to python code.

        element -> ability
        element -> architype
        element -> import_stmt
        element -> test
        element -> global_var
        element -> DOC_STRING
        """
        node.py_code = node.kid[0].py_code

    def exit_global_var(self: "TranspilePass", node: AstNode) -> None:
        """Convert global var to python code.

        global_var -> KW_GLOBAL global_var_clause SEMI
        """
        node.py_code = node.kid[1].py_code + "\n"

    def exit_global_var_clause(self: "TranspilePass", node: AstNode) -> None:
        """Convert global var clause to python code.

        global_var_clause -> global_var_clause COMMA NAME EQ expression
        global_var_clause -> NAME EQ expression
        """
        if node.kid[0].name == "NAME":
            node.py_code = REG_GLOB_FUNC(node.kid[0].py_code, node.kid[2].py_code)
        else:
            node.py_code = node.kid[0].py_code
            node.py_code += REG_GLOB_FUNC(node.kid[2].py_code, node.kid[4].py_code)

    def exit_test(self: "TranspilePass", node: AstNode) -> None:
        """Convert test to python code.

        test -> KW_TEST NAME multistring KW_WITH attr_block spawn_ctx code_block
        test -> KW_TEST NAME multistring KW_WITH attr_block code_block
        test -> KW_TEST NAME multistring KW_WITH walker_ref spawn_ctx code_block
        test -> KW_TEST NAME multistring KW_WITH walker_ref code_block
        """
        # TODO: Add implementation

    def exit_import_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert import statement to python code.

        import_stmt -> KW_IMPORT COLON NAME KW_FROM import_path COMMA name_as_list SEMI
        import_stmt -> KW_IMPORT COLON NAME import_path KW_AS NAME SEMI
        import_stmt -> KW_IMPORT COLON NAME import_path SEMI
        """
        if node.kid[3].name == "KW_FROM":
            node.py_code = f"from {node.kid[4].py_code} import {node.kid[6].py_code}\n"
        elif node.kid[4].name == "KW_AS":
            node.py_code = f"import {node.kid[3].py_code} as {node.kid[5].py_code}\n"
        else:
            node.py_code = f"import {node.kid[3].py_code}"

    def exit_import_path(self: "TranspilePass", node: AstNode) -> None:
        """Convert import path to python code.

        import_path -> import_path_prefix import_path_tail
        import_path -> import_path_prefix
        """
        if len(node.kid) == 1:
            node.py_code = node.kid[0].py_code
        else:
            node.py_code = node.kid[0].py_code + node.kid[1].py_code

    def exit_import_path_prefix(self: "TranspilePass", node: AstNode) -> None:
        """Convert import path prefix to python code.

        import_path_prefix -> DOT DOT NAME
        import_path_prefix -> DOT NAME
        import_path_prefix -> NAME
        """
        for i in node.kid:
            node.py_code += i.py_code

    def exit_import_path_tail(self: "TranspilePass", node: AstNode) -> None:
        """Convert import path tail to python code.

        import_path_tail -> import_path_tail DOT NAME
        import_path_tail -> DOT NAME
        """
        for i in node.kid:
            node.py_code += i.py_code

    def exit_name_as_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert name as list to python code.

        name_as_list -> name_as_list COMMA NAME KW_AS NAME
        name_as_list -> NAME KW_AS NAME
        """
        for i in node.kid:
            node.py_code += i.py_code

    def exit_architype(self: "TranspilePass", node: AstNode) -> None:
        """Convert architype to python code.

        architype -> KW_WALKER NAME arch_decl_tail
        architype -> KW_OBJECT NAME arch_decl_tail
        architype -> KW_EDGE NAME arch_decl_tail
        architype -> KW_NODE NAME arch_decl_tail
        """
        class_type = node.kid[0].py_code.capitalize()
        class_name = node.kid[1].py_code.capitalize()
        node.py_code = f"class {class_name}({class_type}):\n"
        node.py_code += node.kid[2].py_code + "\n"

    # arch_decl_tail -> inherited_archs attr_block
    # arch_decl_tail -> attr_block
    # inherited_archs -> inherited_archs sub_name
    # inherited_archs -> sub_name
    # sub_name -> COLON NAME
    # ability -> KW_ABILITY arch_ref NAME code_block
    # attr_block -> SEMI
    # attr_block -> COLON attr_stmt
    # attr_block -> LBRACE DOC_STRING attr_stmt_list RBRACE
    # attr_block -> LBRACE attr_stmt_list RBRACE
    # attr_block -> LBRACE RBRACE
    # attr_stmt_list -> attr_stmt_list attr_stmt
    # attr_stmt_list -> attr_stmt
    # attr_stmt -> can_stmt
    # attr_stmt -> has_stmt
    # has_stmt -> KW_HAS has_assign_clause SEMI
    # has_assign_clause -> has_assign_clause COMMA has_assign
    # has_assign_clause -> has_assign
    # has_assign -> NAME type_spec EQ expression
    # has_assign -> NAME type_spec
    # has_assign -> has_tag NAME type_spec EQ expression
    # has_assign -> has_tag NAME type_spec
    # has_tag -> KW_ANCHOR
    # has_tag -> KW_HIDDEN
    # has_tag -> has_tag KW_ANCHOR
    # has_tag -> has_tag KW_HIDDEN
    # type_spec -> COLON type_name
    # type_name -> TYP_DICT LSQUARE type_name COMMA type_name RSQUARE
    # type_name -> TYP_LIST LSQUARE type_name RSQUARE
    # type_name -> NAME
    # type_name -> builtin_type
    # builtin_type -> KW_TYPE
    # builtin_type -> TYP_BOOL
    # builtin_type -> TYP_DICT
    # builtin_type -> TYP_SET
    # builtin_type -> TYP_TUPLE
    # builtin_type -> TYP_LIST
    # builtin_type -> TYP_FLOAT
    # builtin_type -> TYP_INT
    # builtin_type -> TYP_BYTES
    # builtin_type -> TYP_STRING
    # can_stmt -> KW_CAN NAME event_clause SEMI
    # can_stmt -> KW_CAN NAME event_clause code_block
    # can_stmt -> KW_CAN NAME SEMI
    # can_stmt -> KW_CAN NAME code_block
    # event_clause -> KW_WITH name_list KW_EXIT
    # event_clause -> KW_WITH name_list KW_ENTRY
    # event_clause -> KW_WITH KW_EXIT
    # event_clause -> KW_WITH KW_ENTRY
    # name_list -> name_list COMMA NAME
    # name_list -> NAME
    # code_block -> LBRACE statement_list RBRACE
    # code_block -> LBRACE RBRACE
    # statement_list -> statement
    # statement_list -> statement statement_list
    # statement -> walker_stmt
    # statement -> report_stmt SEMI
    # statement -> delete_stmt SEMI
    # statement -> ctrl_stmt SEMI
    # statement -> assert_stmt SEMI
    # statement -> while_stmt
    # statement -> for_stmt
    # statement -> try_stmt
    # statement -> if_stmt
    # statement -> expression SEMI
    # if_stmt -> KW_IF expression code_block elif_stmt_list else_stmt
    # if_stmt -> KW_IF expression code_block else_stmt
    # if_stmt -> KW_IF expression code_block
    # elif_stmt_list -> KW_ELIF expression code_block elif_stmt_list
    # elif_stmt_list -> KW_ELIF expression code_block
    # else_stmt -> KW_ELSE code_block
    # try_stmt -> KW_TRY code_block else_from_try
    # try_stmt -> KW_TRY code_block
    # else_from_try -> KW_ELSE code_block
    # else_from_try -> KW_ELSE KW_WITH NAME code_block
    # for_stmt -> KW_FOR atom COMMA atom KW_IN expression code_block
    # for_stmt -> KW_FOR atom KW_IN expression code_block
    # for_stmt -> KW_FOR atom EQ expression KW_TO expression KW_BY expression code_block
    # while_stmt -> KW_WHILE expression code_block
    # assert_stmt -> KW_ASSERT expression
    # ctrl_stmt -> KW_SKIP
    # ctrl_stmt -> KW_BREAK
    # ctrl_stmt -> KW_CONTINUE
    # delete_stmt -> KW_DELETE expression
    # report_stmt -> KW_REPORT sub_name EQ expression
    # report_stmt -> KW_REPORT expression
    # walker_stmt -> yield_stmt
    # walker_stmt -> disengage_stmt
    # walker_stmt -> take_stmt
    # walker_stmt -> ignore_stmt
    # ignore_stmt -> KW_IGNORE expression SEMI
    # take_stmt -> KW_TAKE sub_name expression else_stmt
    # take_stmt -> KW_TAKE expression else_stmt
    # take_stmt -> KW_TAKE sub_name expression SEMI
    # take_stmt -> KW_TAKE expression SEMI
    # disengage_stmt -> KW_DISENGAGE SEMI
    # yield_stmt -> KW_YIELD SEMI
    # expression -> connect assignment_op expression
    # expression -> connect
    # assignment_op -> DIV_EQ
    # assignment_op -> MUL_EQ
    # assignment_op -> SUB_EQ
    # assignment_op -> ADD_EQ
    # assignment_op -> CPY_EQ
    # assignment_op -> EQ
    # connect -> logical connect_op connect
    # connect -> logical NOT edge_op_ref connect
    # connect -> logical
    # logical -> compare KW_OR logical
    # logical -> compare KW_AND logical
    # logical -> compare
    # compare -> arithmetic cmp_op compare
    # compare -> NOT compare
    # compare -> arithmetic
    # cmp_op -> KW_NIN
    # cmp_op -> KW_IN
    # cmp_op -> NE
    # cmp_op -> GTE
    # cmp_op -> LTE
    # cmp_op -> GT
    # cmp_op -> LT
    # cmp_op -> EE
    # arithmetic -> term MINUS arithmetic
    # arithmetic -> term PLUS arithmetic
    # arithmetic -> term
    # term -> factor MOD term
    # term -> factor DIV term
    # term -> factor STAR_MUL term
    # term -> factor
    # factor -> power
    # factor -> MINUS factor
    # factor -> PLUS factor
    # power -> KW_SYNC atom
    # power -> deref
    # power -> ref
    # power -> atom POW factor
    # power -> atom
    # ref -> KW_REF atom
    # deref -> STAR_MUL atom
    # atom -> KW_VISITOR
    # atom -> KW_HERE
    # atom -> spawn
    # atom -> atom node_edge_ref
    # atom -> atom atom_trailer
    # atom -> ability_ref
    # atom -> global_ref
    # atom -> LPAREN expression RPAREN
    # atom -> atom_collection
    # atom -> atom_literal
    # atom_literal -> builtin_type
    # atom_literal -> NAME
    # atom_literal -> NULL
    # atom_literal -> BOOL
    # atom_literal -> DOC_STRING
    # atom_literal -> multistring
    # atom_literal -> FLOAT
    # atom_literal -> INT
    # atom_collection -> dict_val
    # atom_collection -> list_val
    # multistring -> STRING multistring
    # multistring -> STRING
    # list_val -> LSQUARE expr_list RSQUARE
    # list_val -> LSQUARE RSQUARE
    # expr_list -> expr_list COMMA connect
    # expr_list -> connect
    # dict_val -> LBRACE kv_pairs RBRACE
    # dict_val -> LBRACE RBRACE
    # kv_pairs -> connect COLON connect COMMA kv_pairs
    # kv_pairs -> connect COLON connect
    # ability_ref -> DBL_COLON NAME
    # atom_trailer -> PIPE_FWD spawn_ctx
    # atom_trailer -> PIPE_FWD filter_ctx
    # atom_trailer -> PIPE_FWD built_in
    # atom_trailer -> call
    # atom_trailer -> index_slice
    # atom_trailer -> DOT NAME
    # call -> ability_ref
    # call -> LPAREN param_list RPAREN
    # call -> LPAREN RPAREN
    # param_list -> expr_list COMMA kw_expr_list
    # param_list -> kw_expr_list
    # param_list -> expr_list
    # kw_expr_list -> NAME EQ connect COMMA kw_expr_list
    # kw_expr_list -> NAME EQ connect
    # index_slice -> LSQUARE expression COLON expression RSQUARE
    # index_slice -> LSQUARE expression RSQUARE
    # global_ref -> GLOBAL_OP NAME
    # global_ref -> GLOBAL_OP obj_built_in
    # node_edge_ref -> edge_op_ref
    # node_edge_ref -> node_ref filter_ctx
    # spawn -> KW_SPAWN spawn_arch
    # spawn_arch -> object_spawn spawn_ctx
    # spawn_arch -> walker_spawn spawn_ctx
    # spawn_arch -> node_spawn spawn_ctx
    # spawn_edge -> logical connect_op
    # node_spawn -> spawn_edge node_ref
    # node_spawn -> node_ref
    # walker_spawn -> walker_ref
    # walker_spawn -> connect walker_ref
    # walker_spawn -> KW_ASYNC connect walker_ref
    # object_spawn -> obj_ref
    # built_in -> cast_built_in
    # built_in -> obj_built_in
    # obj_built_in -> KW_DETAILS
    # obj_built_in -> KW_INFO
    # obj_built_in -> KW_CONTEXT
    # cast_built_in -> arch_ref
    # cast_built_in -> builtin_type
    # arch_ref -> obj_ref
    # arch_ref -> walker_ref
    # arch_ref -> node_ref
    # node_ref -> KW_NODE DBL_COLON NAME
    # walker_ref -> KW_WALKER DBL_COLON NAME
    # obj_ref -> KW_OBJECT DBL_COLON NAME
    # edge_op_ref -> edge_any
    # edge_op_ref -> edge_from
    # edge_op_ref -> edge_to
    # edge_to -> ARROW_R_p1 NAME filter_ctx ARROW_R_p2
    # edge_to -> ARROW_R
    # edge_from -> ARROW_L_p1 NAME filter_ctx ARROW_L_p2
    # edge_from -> ARROW_L
    # edge_any -> ARROW_L_p1 NAME filter_ctx ARROW_R_p2
    # edge_any -> ARROW_BI
    # connect_op -> connect_any
    # connect_op -> connect_from
    # connect_op -> connect_to
    # connect_to -> CARROW_R_p1 NAME spawn_ctx CARROW_R_p2
    # connect_to -> CARROW_R
    # connect_from -> CARROW_L_p1 NAME spawn_ctx CARROW_L_p2
    # connect_from -> CARROW_L
    # connect_any -> CARROW_L_p1 NAME spawn_ctx CARROW_R_p2
    # connect_any -> CARROW_BI
    # filter_ctx -> LPAREN filter_compare_list RPAREN
    # spawn_ctx -> LPAREN spawn_assign_list RPAREN
    # spawn_assign_list -> NAME EQ expression COMMA spawn_assign_list
    # spawn_assign_list -> NAME EQ expression
    # filter_compare_list -> NAME cmp_op expression COMMA filter_compare_list
    # filter_compare_list -> NAME cmp_op expression
    def exit_import_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert import stmt to python code."""
        node.py_code = node.kid[0].py_code

    def exit_int(self: "TranspilePass", node: AstNode) -> None:
        """Convert int to python code."""
        node.py_code = str(node.value)

    def exit_float(self: "TranspilePass", node: AstNode) -> None:
        """Convert float to python code."""
        node.py_code = str(node.value)

    def exit_multistring(self: "TranspilePass", node: AstNode) -> None:
        """Convert multistring to python code."""
        for i in node.kid:
            node.py_code += i.py_code + " "
        node.py_code = str(node.value)

    def exit_string(self: "TranspilePass", node: AstNode) -> None:
        """Convert string to python code."""
        node.py_code = str(node.value)

    def exit_doc_string(self: "TranspilePass", node: AstNode) -> None:
        """Convert doc string to python code."""
        node.py_code = str(node.value)

    def exit_bool(self: "TranspilePass", node: AstNode) -> None:
        """Convert bool to python code."""
        node.py_code = str(node.value)

    def exit_null(self: "TranspilePass", node: AstNode) -> None:
        """Convert null to python code."""
        node.py_code = str(node.value)

    def exit_name(self: "TranspilePass", node: AstNode) -> None:
        """Convert name to python code."""
        node.py_code = str(node.value)

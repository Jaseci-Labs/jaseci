"""Transpilation pass for Jaseci Ast."""
from jaseci.jac.passes.ir_pass import AstNode, AstNodeKind, Pass


# MACROS for rapid development
MAST = "active_master"
MAST_PATH = "jaseci.core.master"
SENT = f"{MAST}.active_sentinel"
RT = f"{MAST}.runtime"
SET_LINE_FUNC = lambda x: f"{RT}set_line('{x}')\n"  # noqa
REG_GLOB_FUNC = lambda x, y: f"{RT}.register_global({x}, {y})\n"  # noqa
GET_GLOBAL_FUNC = lambda x: f"{RT}.get_global({x})\n"  # noqa
HAS_TAGS = "HasTags"  # noqa
EVENT_TAG = "EventTag"  # noqa
BUILTIN_TAG = "BuiltinTag"  # noqa
SYNC_CMD = "sync_on"  # noqa
YIELD_CMD = "yield_now"  # noqa
A_CALL = "call_ability"  # noqa
W_CALL = "call_walker"  # noqa
APPLY_SPAWN_CTX = "apply_spawn_ctx"  # noqa
APPLY_FILTER_CTX = "apply_filter_ctx"  # noqa
CREATE_EDGE = "create_edge"  # noqa
CREATE_NODE = "create_node"  # noqa
CREATE_WALKER = "create_walker"  # noqa
CREATE_OBJECT = "create_object"  # noqa


class TranspilePass(Pass):
    """Jac transpilation to python pass."""

    def __init__(self: "TranspilePass", ir: AstNode) -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.indent_level = 0
        self.cur_arch = None  # tracks current architype during transpilation
        super().__init__(ir)

    def indent_str(self: "TranspilePass", indent_delta: int) -> str:
        """Return string for indent."""
        return " " * self.indent_size * (self.indent_level + indent_delta)

    def emit_ln(
        self: "TranspilePass", node: AstNode, s: str, indent_delta: int = 0
    ) -> None:
        """Emit code to node."""
        node.py_code += (
            self.indent_str(indent_delta)
            + s.replace("\n", "\n" + self.indent_str(indent_delta))
            + "\n"
        )

    def emit(self: "TranspilePass", node: AstNode, s: str) -> None:
        """Emit code to node."""
        # node.py_code += s

    def exit_start(self: "TranspilePass", node: AstNode) -> None:
        """Convert start to python code.

        start -> element_list
        """
        self.emit(node, node.kid[0].py_code)

    def exit_element_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert element list to python code.

        element_list -> element_list element
        element_list -> element
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_element(self: "TranspilePass", node: AstNode) -> None:
        """Convert element to python code.

        element -> ability
        element -> architype
        element -> import_stmt
        element -> test
        element -> global_var
        element -> DOC_STRING
        """
        self.emit(node, node.kid[0].py_code)

    def exit_global_var(self: "TranspilePass", node: AstNode) -> None:
        """Convert global var to python code.

        global_var -> KW_GLOBAL global_var_clause SEMI
        """
        self.emit_ln(node, node.kid[1].py_code)

    def exit_global_var_clause(self: "TranspilePass", node: AstNode) -> None:
        """Convert global var clause to python code.

        global_var_clause -> global_var_clause COMMA NAME EQ expression
        global_var_clause -> NAME EQ expression
        """
        if node.kid[0].name == "NAME":
            self.emit_ln(node, REG_GLOB_FUNC(node.kid[0].py_code, node.kid[2].py_code))
        else:
            self.emit_ln(node, node.kid[0].py_code)
            self.emit_ln(node, REG_GLOB_FUNC(node.kid[2].py_code, node.kid[4].py_code))

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
            self.emit_ln(
                node, f"from {node.kid[4].py_code} import {node.kid[6].py_code}"
            )
        elif node.kid[4].name == "KW_AS":
            self.emit_ln(node, f"import {node.kid[3].py_code} as {node.kid[5].py_code}")
        else:
            self.emit_ln(node, f"import {node.kid[3].py_code}")

    def exit_import_path(self: "TranspilePass", node: AstNode) -> None:
        """Convert import path to python code.

        import_path -> import_path_prefix import_path_tail
        import_path -> import_path_prefix
        """
        if len(node.kid) == 1:
            self.emit(node, node.kid[0].py_code)
        else:
            self.emit(node, node.kid[0].py_code + node.kid[1].py_code)

    def exit_import_path_prefix(self: "TranspilePass", node: AstNode) -> None:
        """Convert import path prefix to python code.

        import_path_prefix -> DOT DOT NAME
        import_path_prefix -> DOT NAME
        import_path_prefix -> NAME
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_import_path_tail(self: "TranspilePass", node: AstNode) -> None:
        """Convert import path tail to python code.

        import_path_tail -> import_path_tail DOT NAME
        import_path_tail -> DOT NAME
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_name_as_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert name as list to python code.

        name_as_list -> name_as_list COMMA NAME KW_AS NAME
        name_as_list -> name_as_list COMMA NAME
        name_as_list -> NAME KW_AS NAME
        name_as_list -> NAME
        """
        if len(node.kid) == 3:
            if node.kid[0].name == "NAME":
                self.emit(node, f"{node.kid[0].py_code} as {node.kid[2].py_code}")
            else:
                self.emit(node, f"{node.kid[0].py_code}, {node.kid[2].py_code}")
        elif len(node.kid) == 1:
            self.emit(node, f"{node.kid[0].py_code}")
        else:
            self.emit(
                node,
                f"{node.kid[0].py_code}, {node.kid[2].py_code} as {node.kid[4].py_code}",
            )

    def enter_architype(self: "TranspilePass", node: AstNode) -> None:
        """Convert architype to python code.

        architype -> KW_WALKER NAME arch_decl_tail
        architype -> KW_OBJECT NAME arch_decl_tail
        architype -> KW_EDGE NAME arch_decl_tail
        architype -> KW_NODE NAME arch_decl_tail
        """
        self.indent_level += 1
        self.cur_arch = {"name": node.kid[1].value, "typ": node.kid[0].value}

    def exit_architype(self: "TranspilePass", node: AstNode) -> None:
        """Convert architype to python code.

        architype -> KW_WALKER NAME arch_decl_tail
        architype -> KW_OBJECT NAME arch_decl_tail
        architype -> KW_EDGE NAME arch_decl_tail
        architype -> KW_NODE NAME arch_decl_tail
        """
        class_type = node.kid[0].py_code.capitalize()
        class_name = node.kid[1].py_code.capitalize() + "_" + class_type
        if "inherits" in node.kid[2].misc.keys():
            class_type = node.kid[2].misc["inherits"]
        self.emit_ln(node, f"class {class_name}({class_type}):", indent_delta=-1)
        self.emit_ln(node, "def __init__(self):")
        self.emit_ln(node, node.kid[2].py_code)
        self.indent_level -= 1
        self.cur_arch = None

    def exit_arch_decl_tail(self: "TranspilePass", node: AstNode) -> None:
        """Convert arch decl tail to python code.

        arch_decl_tail -> inherited_archs attr_block
        arch_decl_tail -> attr_block
        """
        if len(node.kid) == 1:
            self.emit(node, node.kid[0].py_code)
        else:
            node.misc["inherits"] = node.kid[0].py_code
            self.emit(node, node.kid[1].py_code)

    def exit_inherited_archs(self: "TranspilePass", node: AstNode) -> None:
        """Convert inherited archs to python code.

        inherited_archs -> inherited_archs sub_name
        inherited_archs -> sub_name
        """
        if len(node.kid) == 1:
            self.emit(node, node.kid[0].py_code.capitalize())
        else:
            self.emit(
                node, node.kid[0].py_code + ", " + node.kid[1].py_code.capitalize()
            )

    def exit_sub_name(self: "TranspilePass", node: AstNode) -> None:
        """Convert sub name to python code.

        sub_name -> COLON NAME
        """
        self.emit(node, node.kid[1].py_code)

    def enter_ability(self: "TranspilePass", node: AstNode) -> None:
        """Convert ability to python code.

        ability -> KW_ABILITY arch_ref DBL_COLON NAME func_decl code_block
        ability -> KW_ABILITY arch_ref DBL_COLON NAME code_block
        """
        self.indent_level += 1

    def exit_ability(self: "TranspilePass", node: AstNode) -> None:
        """Convert ability to python code.

        # OLD: ability -> KW_ABILITY arch_ref NAME code_block
        ability -> KW_ABILITY arch_ref DBL_COLON NAME func_decl code_block
        ability -> KW_ABILITY arch_ref DBL_COLON NAME code_block
        """
        for i in node.kid:
            self.emit(node, i.py_code)
        # arch = node.kid[1].py_code
        # if len(node.kid) == 5:
        #     name = f"ability_{arch['typ']}_{arch['name']}_{node.kid[3].py_code}"
        #     self.emit_ln(node, f"def {name}(here, visitor):", indent_delta=-1)
        #     self.emit_ln(node, node.kid[3].py_code)
        # self.indent_level -= 1

    def exit_attr_block(self: "TranspilePass", node: AstNode) -> None:
        """Convert attr block to python code.

        attr_block -> SEMI
        attr_block -> COLON attr_stmt
        attr_block -> LBRACE DOC_STRING attr_stmt_list RBRACE
        attr_block -> LBRACE attr_stmt_list RBRACE
        attr_block -> LBRACE RBRACE
        """
        if len(node.kid) == 1 or (len(node.kid) == 2 and node.kid[0].name != "COLON"):
            self.emit_ln(node, "pass")
        elif len(node.kid) == 4:
            self.emit_ln(node, node.kid[1].py_code)
            self.emit(node, node.kid[2].py_code)
        else:
            self.emit(node, node.kid[1].py_code)

    def exit_attr_stmt_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert attr stmt list to python code.

        attr_stmt_list -> attr_stmt_list attr_stmt
        attr_stmt_list -> attr_stmt
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_attr_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert attr stmt to python code.

        attr_stmt -> can_stmt
        attr_stmt -> has_stmt
        """
        self.emit(node, node.kid[0].py_code)

    def exit_has_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert has stmt to python code.

        has_stmt -> KW_HAS has_assign_clause SEMI
        """
        self.emit(node, node.kid[1].py_code)

    def exit_has_assign_clause(self: "TranspilePass", node: AstNode) -> None:
        """Convert has assign clause to python code.

        #TODO: BROKEN
        has_assign_clause -> has_assign_clause COMMA has_assign
        has_assign_clause -> has_assign
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_param_var(self: "TranspilePass", node: AstNode) -> None:
        """Convert function declaration to python code.

        TODO: Broken
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_has_tag(self: "TranspilePass", node: AstNode) -> None:
        """Convert has tag to python code.

        has_tag -> KW_ANCHOR
        has_tag -> KW_HIDDEN
        has_tag -> has_tag KW_ANCHOR
        has_tag -> has_tag KW_HIDDEN
        """
        if len(node.kid) == 1:
            self.emit(node, f"{HAS_TAGS}.{node.kid[0].py_code.upper()}")
        else:
            self.emit(
                node, f"{node.kid[0].py_code}, {HAS_TAGS}.{node.kid[0].py_code.upper()}"
            )

    def exit_type_spec(self: "TranspilePass", node: AstNode) -> None:
        """Convert type spec to python code.

        type_spec -> COLON type_name
        """
        self.emit(node, node.kid[1].py_code)

    def exit_type_name(self: "TranspilePass", node: AstNode) -> None:
        """Convert type name to python code.

        type_name -> TYP_DICT LSQUARE type_name COMMA type_name RSQUARE
        type_name -> TYP_LIST LSQUARE type_name RSQUARE
        type_name -> NAME
        type_name -> builtin_type
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_builtin_type(self: "TranspilePass", node: AstNode) -> None:
        """Convert builtin type to python code.

        builtin_type -> KW_TYPE
        builtin_type -> TYP_BOOL
        builtin_type -> TYP_DICT
        builtin_type -> TYP_SET
        builtin_type -> TYP_TUPLE
        builtin_type -> TYP_LIST
        builtin_type -> TYP_FLOAT
        builtin_type -> TYP_INT
        builtin_type -> TYP_BYTES
        builtin_type -> TYP_STRING
        """
        self.emit(node, node.kid[0].py_code)

    def exit_can_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert can stmt to python code."""
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_can_ds_ability(self: "TranspilePass", node: AstNode) -> None:
        """Convert can stmt to python code.

        can_stmt -> KW_CAN NAME event_clause SEMI
        can_stmt -> KW_CAN NAME event_clause code_block
        can_stmt -> KW_CAN NAME SEMI
        can_stmt -> KW_CAN NAME code_block
        """
        arch = self.cur_arch
        name = f"ability_{arch['typ']}_{arch['name']}_{node.kid[1].py_code}"
        if node.kid[-1] == "code_block":
            self.emit_ln(node, f"def {name}(here, visitor):")
            self.emit_ln(node, node.kid[-1].py_code, indent_delta=1)
        clause = "None" if node.kid[2].name != "event_clause" else node.kid[2].py_code
        self.emit_ln(
            node,
            f"self.add_ability(func={name}, on_event={clause})",
        )

    def exit_can_func_ability(self: "TranspilePass", node: AstNode) -> None:
        """Convert can stmt to python code.

        TODO: Broken
        can_stmt -> KW_CAN NAME event_clause SEMI
        can_stmt -> KW_CAN NAME event_clause code_block
        can_stmt -> KW_CAN NAME SEMI
        can_stmt -> KW_CAN NAME code_block
        """
        arch = self.cur_arch
        name = f"ability_{arch['typ']}_{arch['name']}_{node.kid[1].py_code}"
        if node.kid[-1] == "code_block":
            self.emit_ln(node, f"def {name}(here, visitor):")
            self.emit_ln(node, node.kid[-1].py_code, indent_delta=1)
        clause = "None" if node.kid[2].name != "event_clause" else node.kid[2].py_code
        self.emit_ln(
            node,
            f"self.add_ability(func={name}, on_event={clause})",
        )

    def exit_func_decl(self: "TranspilePass", node: AstNode) -> None:
        """Convert function declaration to python code.

        TODO: Broken
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_func_decl_param_list(self: "TranspilePass", node: AstNode) -> None:
        """TODO: Broken."""
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_event_clause(self: "TranspilePass", node: AstNode) -> None:
        """Convert event clause to python code.

        event_clause -> KW_WITH name_list KW_EXIT
        event_clause -> KW_WITH name_list KW_ENTRY
        event_clause -> KW_WITH KW_EXIT
        event_clause -> KW_WITH KW_ENTRY
        """
        event = node.kid[-1].py_code.upper()
        names = node.kid[1].py_code if node.kid[1].name == "name_list" else ""
        self.emit(node, f"({EVENT_TAG}.{event}, ({names}))")

    def exit_name_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert name list to python code.

        name_list -> name_list COMMA NAME
        name_list -> NAME
        """
        if len(node.kid) == 1:
            self.emit(node, f'"{node.kid[0].py_code}"')
        else:
            self.emit(node, f'{node.kid[0].py_code}, "{node.kid[2].py_code}"')

    def enter_code_block(self: "TranspilePass", node: AstNode) -> None:
        """Convert code block to python code.

        code_block -> LBRACE statement_list RBRACE
        code_block -> LBRACE RBRACE
        """
        self.indent_level += 1

    def exit_code_block(self: "TranspilePass", node: AstNode) -> None:
        """Convert code block to python code.

        code_block -> LBRACE statement_list RBRACE
        code_block -> LBRACE RBRACE
        """
        if len(node.kid) == 3:
            self.emit(node, node.kid[1].py_code)
        else:
            self.emit_ln(node, "pass")
        self.indent_level -= 1

    def exit_statement_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert statement list to python code.

        statement_list -> statement
        statement_list -> statement statement_list
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_statement(self: "TranspilePass", node: AstNode) -> None:
        """Convert statement to python code.

        statement -> walker_stmt
        statement -> report_stmt SEMI
        statement -> delete_stmt SEMI
        statement -> ctrl_stmt SEMI
        statement -> assert_stmt SEMI
        statement -> while_stmt
        statement -> for_stmt
        statement -> try_stmt
        statement -> if_stmt
        statement -> expression SEMI
        statement -> assignment SEMI
        """
        if node.kid[0].name in ["expression", "assignment"]:
            self.emit_ln(node, node.kid[0].py_code)
        else:
            self.emit(node, node.kid[0].py_code)

    def exit_if_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert if stmt to python code.

        if_stmt -> KW_IF expression code_block elif_stmt_list else_stmt
        if_stmt -> KW_IF expression code_block else_stmt
        if_stmt -> KW_IF expression code_block
        """
        self.emit_ln(node, "if " + node.kid[1].py_code + ":")
        self.emit(node, node.kid[2].py_code)
        if len(node.kid) == 4:
            self.emit(node, node.kid[3].py_code)
        elif len(node.kid) == 5:
            self.emit(node, node.kid[3].py_code)
            self.emit(node, node.kid[4].py_code)

    def exit_elif_stmt_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert elif stmt list to python code.

        elif_stmt_list -> KW_ELIF expression code_block elif_stmt_list
        elif_stmt_list -> KW_ELIF expression code_block
        """
        self.emit_ln(node, "elif " + node.kid[1].py_code + ":")
        self.emit(node, node.kid[2].py_code)
        if len(node.kid) == 4:
            self.emit(node, node.kid[3].py_code)

    def exit_else_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert else stmt to python code.

        else_stmt -> KW_ELSE code_block
        """
        self.emit_ln(node, "else:")
        self.emit(node, node.kid[1].py_code)

    def exit_try_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert try stmt to python code.

        try_stmt -> KW_TRY code_block else_from_try
        try_stmt -> KW_TRY code_block
        """
        self.emit_ln(node, "try:")
        self.emit(node, node.kid[1].py_code)
        if len(node.kid) == 3:
            self.emit(node, node.kid[2].py_code)

    def exit_else_from_try(self: "TranspilePass", node: AstNode) -> None:
        """Convert else from try to python code.

        else_from_try -> KW_ELSE code_block
        else_from_try -> KW_ELSE KW_WITH NAME code_block
        """
        if len(node.kid) == 4:
            name = node.kid[2].py_code
            self.emit_ln(node, f"except Exception as {name}:")
            self.emit(node, node.kid[3].py_code)
        else:
            self.emit_ln(node, "except Exception:")
            self.emit(node, node.kid[3].py_code)

    def exit_for_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert for stmt to python code.

        for_stmt -> KW_FOR atom COMMA atom KW_IN expression code_block
        for_stmt -> KW_FOR atom KW_IN expression code_block
        for_stmt -> KW_FOR assignment KW_TO expression KW_BY expression code_block
        """
        if len(node.kid) == 7:
            self.emit_ln(
                node,
                f"for {node.kid[1].py_code}, {node.kid[3].py_code} in {node.kid[5].py_code}:",
            )
            self.emit(node, node.kid[6].py_code)
        elif len(node.kid) == 5:
            self.emit_ln(node, f"for {node.kid[1].py_code} in {node.kid[3].py_code}:")
            self.emit(node, node.kid[4].py_code)
        else:
            self.emit_ln(node, f"{node.kid[1].py_code}")
            self.emit_ln(node, f"while {node.kid[3].py_code}:")
            self.emit(node, node.kid[5].py_code)
            self.emit_ln(node, f"{node.kid[6].py_code}", indent_delta=1)

    def exit_while_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert while stmt to python code.

        while_stmt -> KW_WHILE expression code_block
        """
        self.emit_ln(node, f"while {node.kid[1].py_code}:")
        self.emit(node, node.kid[2].py_code)

    def exit_assert_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert assert stmt to python code.

        assert_stmt -> KW_ASSERT expression
        """
        self.emit_ln(node, f"assert {node.kid[1].py_code}")

    def exit_ctrl_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert ctrl stmt to python code.

        ctrl_stmt -> KW_SKIP
        ctrl_stmt -> KW_BREAK
        ctrl_stmt -> KW_CONTINUE
        """
        if node.kid[0].name == "KW_SKIP":
            self.emit_ln(node, "visitor.skip()")
        self.emit_ln(node, node.kid[0].py_code)

    def exit_delete_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert delete stmt to python code.

        delete_stmt -> KW_DELETE expression
        """
        self.emit_ln(node, f"del {node.kid[1].py_code}")

    def exit_report_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert report stmt to python code.

        report_stmt -> KW_REPORT expression
        """
        self.emit_ln(node, f"visitor.report({node.kid[1].py_code})")

    def exit_return_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert return stmt to python code.

        return_stmt -> KW_RETURN expression
        """
        self.emit_ln(node, f"return {node.kid[1].py_code}")

    def exit_walker_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert walker stmt to python code.

        walker_stmt -> sync_stmt
        walker_stmt -> yield_stmt
        walker_stmt -> disengage_stmt
        walker_stmt -> revisit_stmt
        walker_stmt -> visit_stmt
        walker_stmt -> ignore_stmt
        """
        self.emit(node, node.kid[0].py_code)

    def exit_ignore_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert ignore stmt to python code.

        ignore_stmt -> KW_IGNORE expression SEMI
        """
        self.emit_ln(node, f"visitor.ignore({node.kid[1].py_code})")

    def exit_visit_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert visit stmt to python code.

        visit_stmt -> KW_VISIT sub_name expression else_stmt
        visit_stmt -> KW_VISIT expression else_stmt
        visit_stmt -> KW_VISIT sub_name expression SEMI
        visit_stmt -> KW_VISIT expression SEMI
        """
        if len(node.kid) == 5:
            self.emit_ln(
                node, f"visitor.visit({node.kid[2].py_code}, {node.kid[3].py_code})"
            )
            self.emit(node, node.kid[4].py_code)
        else:
            self.emit_ln(node, f"visitor.visit({node.kid[1].py_code})")
            self.emit(node, node.kid[2].py_code)

    def exit_revisit_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert visit stmt to python code.

        revisit_stmt -> KW_REVISIT expression else_stmt
        revisit_stmt -> KW_REVISIT else_stmt
        revisit_stmt -> KW_REVISIT expression SEMI
        revisit_stmt -> KW_REVISIT SEMI
        """
        if node.kid[-1].name == "else_stmt":
            if len(node.kid) == 2:
                self.emit_ln(node, "if visitor.revisit():")
            else:
                self.emit_ln(node, f"if visitor.revisit({node.kid[1].py_code}):")
            self.emit_ln(node, "pass", indent_delta=1)
            self.emit(node, node.kid[-1].py_code)
        elif len(node.kid) == 3:
            self.emit_ln(node, f"visitor.revisit({node.kid[1].py_code})")
        else:
            self.emit_ln(node, "visitor.revisit()")

    def exit_disengage_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert disengage stmt to python code.

        disengage_stmt -> KW_DISENGAGE SEMI
        """
        self.emit_ln(node, "visitor.disengage()")

    def exit_yield_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert yield stmt to python code.

        yield_stmt -> KW_YIELD SEMI
        """
        self.emit_ln(node, f"visitor.{YIELD_CMD}()")

    def exit_sync_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert sync stmt to python code.

        sync_stmt -> KW_SYNC expression SEMI
        """
        self.emit_ln(node, f"{RT}.{SYNC_CMD}({node.kid[1].py_code})")

    def exit_assignment(self: "TranspilePass", node: AstNode) -> None:
        """Convert assignment to python code.

        assignment -> atom EQ expression
        """
        self.emit(node, f"{node.kid[0].py_code} = {node.kid[2].py_code}")

    def exit_expression(self: "TranspilePass", node: AstNode) -> None:
        """Convert expression to python code.

        expression -> connect walrus_op expression
        expression -> connect
        """
        if len(node.kid) == 3 and node.kid[1].name == "WALRUS_EQ":
            self.emit(
                node,
                f"{node.kid[0].py_code} {node.kid[1].py_code} {node.kid[2].py_code}",
            )
        elif len(node.kid) == 1:
            self.emit(node, node.kid[0].py_code)
        else:
            self.emit(
                node,
                f"{node.kid[0].py_code}:={node.kid[0].py_code}{node.kid[1].py_code}{node.kid[2].py_code}",
            )

    def exit_walrus_op(self: "TranspilePass", node: AstNode) -> None:
        """Convert walrus op to python code.

        walrus_op -> DIV_EQ
        walrus_op -> MUL_EQ
        walrus_op -> SUB_EQ
        walrus_op -> ADD_EQ
        walrus_op -> WALRUS_EQ
        """
        self.emit(node, node.kid[0].py_code)

    def exit_connect(self: "TranspilePass", node: AstNode) -> None:
        """Convert connect to python code.

        connect -> logical connect_op connect
        connect -> logical NOT edge_op_ref connect
        connect -> logical
        """
        if len(node.kid) == 3:
            self.emit(
                node,
                f"{node.kid[0].py_code}.connect(typ={node.kid[1].py_code}, target={node.kid[2].py_code})",
            )
        elif len(node.kid) == 4:
            self.emit(
                node,
                f"{node.kid[0].py_code}.disconnect(typ={node.kid[2].py_code}, target={node.kid[3].py_code})",
            )
        else:
            self.emit(node, node.kid[0].py_code)

    def exit_logical(self: "TranspilePass", node: AstNode) -> None:
        """Convert logical to python code.

        logical -> compare KW_OR logical
        logical -> compare KW_AND logical
        logical -> compare
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_compare(self: "TranspilePass", node: AstNode) -> None:
        """Convert compare to python code.

        compare -> arithmetic cmp_op compare
        compare -> NOT compare
        compare -> arithmetic
        """
        if len(node.kid) == 2:
            self.emit(node, f"not {node.kid[1].py_code}")
        else:
            for i in node.kid:
                self.emit(node, i.py_code)

    def exit_cmp_op(self: "TranspilePass", node: AstNode) -> None:
        """Convert cmp_op to python code.

        cmp_op -> KW_NIN
        cmp_op -> KW_IN
        cmp_op -> NE
        cmp_op -> GTE
        cmp_op -> LTE
        cmp_op -> GT
        cmp_op -> LT
        cmp_op -> EE
        """
        self.emit(node, node.kid[0].py_code)

    def exit_arithmetic(self: "TranspilePass", node: AstNode) -> None:
        """Convert arithmetic to python code.

        arithmetic -> term MINUS arithmetic
        arithmetic -> term PLUS arithmetic
        arithmetic -> term
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_term(self: "TranspilePass", node: AstNode) -> None:
        """Convert term to python code.

        term -> factor MOD term
        term -> factor DIV term
        term -> factor STAR_MUL term
        term -> factor
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_factor(self: "TranspilePass", node: AstNode) -> None:
        """Convert factor to python code.

        factor -> power
        factor -> MINUS factor
        factor -> PLUS factor
        """
        op = "-" if node.kid[0].name == "MINUS" else ""
        if len(node.kid) == 2:
            self.emit(node, f"{op}{node.kid[1].py_code}")
        else:
            self.emit(node, node.kid[0].py_code)

    def exit_power(self: "TranspilePass", node: AstNode) -> None:
        """Convert power to python code.

        power -> deref
        power -> ref
        power -> atom POW factor
        power -> atom
        """
        if len(node.kid) == 3:
            self.emit(node, f"{node.kid[0].py_code} ** {node.kid[2].py_code}")
        else:
            self.emit(node, node.kid[0].py_code)

    def exit_ref(self: "TranspilePass", node: AstNode) -> None:
        """Convert ref to python code.

        ref -> KW_REF atom
        """
        self.emit(node, f"{RT}.ref({node.kid[1].py_code})")

    def exit_deref(self: "TranspilePass", node: AstNode) -> None:
        """Convert deref to python code.

        deref -> STAR_MUL atom
        """
        self.emit(node, f"{RT}.deref({node.kid[1].py_code})")

    def exit_atom(self: "TranspilePass", node: AstNode) -> None:
        """Convert atom to python code.

        atom -> KW_VISITOR
        atom -> KW_HERE
        atom -> spawn
        atom -> atom node_edge_ref
        atom -> atomic_chain
        atom -> global_ref
        atom -> LPAREN expression RPAREN
        atom -> atom_collection
        atom -> atom_literal
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_atom_literal(self: "TranspilePass", node: AstNode) -> None:
        """Convert atom_literal to python code.

        atom_literal -> builtin_type
        atom_literal -> NAME
        atom_literal -> NULL
        atom_literal -> BOOL
        atom_literal -> DOC_STRING
        atom_literal -> multistring
        atom_literal -> FLOAT
        atom_literal -> INT
        """
        self.emit(node, node.kid[0].py_code)

    def exit_atom_collection(self: "TranspilePass", node: AstNode) -> None:
        """Convert atom_collection to python code.

        atom_collection -> dict_val
        atom_collection -> list_val
        """
        self.emit(node, node.kid[0].py_code)

    def exit_multistring(self: "TranspilePass", node: AstNode) -> None:
        """Convert multistring to python code.

        multistring -> STRING multistring
        multistring -> STRING
        """
        if len(node.kid) == 1:
            self.emit(node, node.kid[0].py_code)
        else:
            self.emit(node, f"{node.kid[0].py_code} {node.kid[1].py_code}")

    def exit_list_val(self: "TranspilePass", node: AstNode) -> None:
        """Convert list_val to python code.

        list_val -> LSQUARE expr_list RSQUARE
        list_val -> LSQUARE RSQUARE
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_expr_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert expr_list to python code.

        expr_list -> expr_list COMMA expression
        expr_list -> expression
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_dict_val(self: "TranspilePass", node: AstNode) -> None:
        """Convert dict_val to python code.

        dict_val -> LBRACE kv_pairs RBRACE
        dict_val -> LBRACE RBRACE
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_kv_pairs(self: "TranspilePass", node: AstNode) -> None:
        """Convert kv_pairs to python code.

        kv_pairs -> expression COLON expression COMMA kv_pairs
        kv_pairs -> expression COLON expression
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_ability_run(self: "TranspilePass", node: AstNode) -> None:
        """Convert ability_run to python code.

        ability_run -> DBL_COLON NAME
        ability_run -> DBL_COLON
        ability_run -> DBL_COLON NAME KW_ASYNC
        ability_run -> DBL_COLON KW_ASYNC
        """
        if node.kid[-1].name == "KW_ASYNC":
            if node.kid[-2].name == "NAME":
                self.emit(node, f".{A_CALL}({node.kid[1].py_code}, is_async=True)")
            else:
                self.emit(node, f".{W_CALL}(is_async=True)")
        else:
            if len(node.kid) == 1:
                self.emit(node, f".{W_CALL}()")
            else:
                self.emit(node, f".{A_CALL}({node.kid[1].py_code})")

    def exit_atomic_chain(self: "TranspilePass", node: AstNode) -> None:
        """Convert atomic_chain to python code.

        atomic_chain -> atomic_chain_unsafe
        atomic_chain -> atomic_chain_safe  # TODO: implement
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_atomic_chain_unsafe(self: "TranspilePass", node: AstNode) -> None:
        """Convert atom_trailer to python code.

        atomic_chain -> atom PIPE_FWD spawn_ctx
        atomic_chain -> atom PIPE_FWD filter_ctx
        atomic_chain -> atom PIPE_FWD built_in
        atomic_chain -> atom call
        atomic_chain -> atom index_slice
        atomic_chain -> atom DOT NAME
        """
        if node.kid[1].name == "PIPE_FWD":
            if node[2].name == "spawn_ctx":
                self.emit(
                    node,
                    f"{RT}.{APPLY_SPAWN_CTX}(target={node.kid[0].py_code}, ctx={node.kid[2].py_code})",
                )
            elif node[2].name == "filter_ctx":
                self.emit(
                    node,
                    f"{RT}.{APPLY_FILTER_CTX}(target={node.kid[0].py_code}, ctx={node.kid[2].py_code})",
                )
            else:
                self.emit(
                    node,
                    f"{node.kid[2].py_code}({node.kid[0].py_code})",
                )
        else:
            for i in node.kid:
                self.emit(node, i.py_code)

    def exit_atomic_chain_safe(self: "TranspilePass", node: AstNode) -> None:
        """Convert atom_trailer to python code.

        # TODO: implement
        atomic_chain -> atom NULL_OK PIPE_FWD spawn_ctx
        atomic_chain -> atom NULL_OK PIPE_FWD filter_ctx
        atomic_chain -> atom NULL_OK PIPE_FWD built_in
        atomic_chain -> atom NULL_OK call
        atomic_chain -> atom NULL_OK index_slice
        atomic_chain -> atom NULL_OK DOT NAME
        """
        if node.kid[1].name == "PIPE_FWD":
            if node[2].name == "spawn_ctx":
                self.emit(
                    node,
                    f"{RT}.{APPLY_SPAWN_CTX}(target={node.kid[0].py_code}, ctx={node.kid[2].py_code})",
                )
            elif node[2].name == "filter_ctx":
                self.emit(
                    node,
                    f"{RT}.{APPLY_FILTER_CTX}(target={node.kid[0].py_code}, ctx={node.kid[2].py_code})",
                )
            else:
                self.emit(
                    node,
                    f"{node.kid[2].py_code}({node.kid[0].py_code})",
                )
        else:
            for i in node.kid:
                self.emit(node, i.py_code)

    def exit_call(self: "TranspilePass", node: AstNode) -> None:
        """Convert call to python code.

        call -> ability_run
        call -> LPAREN param_list RPAREN
        call -> LPAREN RPAREN
        """
        if len(node.kid) == 1:
            self.emit(node, {node.kid[0].py_code})
        elif len(node.kid) == 3:
            self.emit(node, f"({node.kid[1].py_code})")
        else:
            self.emit(node, "()")

    def exit_param_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert param_list to python code.

        param_list -> expr_list COMMA assignment_list
        param_list -> assignment_list
        param_list -> expr_list
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_assignment_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert assignment_list to python code.

        assignment_list -> assignment COMMA assignment_list
        assignment_list -> assignment
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_index_slice(self: "TranspilePass", node: AstNode) -> None:
        """Convert index_slice to python code.

        index_slice -> LSQUARE expression COLON expression RSQUARE
        index_slice -> LSQUARE expression RSQUARE
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    def exit_global_ref(self: "TranspilePass", node: AstNode) -> None:
        """Convert global_ref to python code.

        global_ref -> GLOBAL_OP NAME
        global_ref -> GLOBAL_OP obj_built_in
        """
        if node.kid[-1].name == "obj_built_in":
            self.emit(node, f"{GET_GLOBAL_FUNC}({node.kid[1].py_code})")
        else:
            self.emit(
                node, f"{GET_GLOBAL_FUNC}(({BUILTIN_TAG}.VAR, {node.kid[1].py_code}))"
            )

    # def exit_node_edge_ref(self: "TranspilePass", node: AstNode) -> None:
    #     """Convert node_edge_ref to python code.

    #     node_edge_ref -> edge_op_ref
    #     node_edge_ref -> node_ref filter_ctx
    #     """
    #     if len(node.kid) == 1:
    #         self.emit(node, node.kid[0].py_code)
    #     else:
    #         self.emit(
    #             node,
    #             f"{RT}.{APPLY_FILTER_CTX}(target={node.kid[0].py_code}, ctx={node.kid[1].py_code})",
    #         )

    def exit_spawn(self: "TranspilePass", node: AstNode) -> None:
        """Convert spawn to python code.

        spawn -> spawn_arch
        spawn -> spawn_edge
        """
        for i in node.kid:
            self.emit(node, i.py_code)

    # def exit_spawn_arch(self: "TranspilePass", node: AstNode) -> None:
    #     """Convert spawn_arch to python code.

    #     spawn_arch -> object_spawn
    #     spawn_arch -> walker_spawn
    #     spawn_arch -> node_spawn
    #     """
    #     for i in node.kid:
    #         self.emit(node, i.py_code)

    def exit_node_spawn(self: "TranspilePass", node: AstNode) -> None:
        """Convert node_spawn to python code.

        node_spawn -> spawn_edge node_ref
        node_spawn -> node_ref
        """
        if len(node.kid) == 1:
            self.emit(
                node, f"{RT}.{CREATE_NODE}(typ={node.kid[0].py_code}, connect=None)"
            )
        else:
            self.emit(
                node,
                f"{RT}.{CREATE_NODE}(typ={node.kid[0].py_code}, "
                f"connect=({node.kid[1].py_code},{node.kid[2].py_code}))",
            )

    def exit_spawn_edge(self: "TranspilePass", node: AstNode) -> None:
        """Convert spawn_edge to python code.

        spawn_edge -> logical connect_op
        """
        self.emit(
            node,
            f"{RT}.{CREATE_EDGE}({node.kid[0].py_code}, typ={node.kid[1].py_code})",
        )

    # def exit_walker_spawn(self: "TranspilePass", node: AstNode) -> None:
    #     """Convert walker_spawn to python code.

    #     walker_spawn -> walker_ref
    #     """
    #     self.emit(node, f"{RT}.{CREATE_WALKER}({node.kid[0].py_code})")

    # def exit_object_spawn(self: "TranspilePass", node: AstNode) -> None:
    #     """Convert object_spawn to python code.

    #     object_spawn -> object_ref
    #     """
    #     self.emit(node, f"{RT}.{CREATE_OBJECT}({node.kid[0].py_code})")

    def exit_built_in(self: "TranspilePass", node: AstNode) -> None:
        """Convert built_in to python code.

        built_in -> cast_built_in
        built_in -> obj_built_in
        """
        self.emit(node, node.kid[0].py_code)

    def exit_obj_built_in(self: "TranspilePass", node: AstNode) -> None:
        """Convert obj_built_in to python code.

        obj_built_in -> KW_DETAILS
        obj_built_in -> KW_INFO
        obj_built_in -> KW_CONTEXT
        """
        self.emit(node, f"({BUILTIN_TAG}.{node.kid[0].py_code.upper()}, None)")

    def exit_cast_built_in(self: "TranspilePass", node: AstNode) -> None:
        """Convert cast_built_in to python code.

        cast_built_in -> arch_ref
        cast_built_in -> builtin_type
        """
        self.emit(node, node.kid[2].py_code)

    def exit_arch_ref(self: "TranspilePass", node: AstNode) -> None:
        """Convert arch_ref to python code.

        arch_ref -> object_ref
        arch_ref -> walker_ref
        arch_ref -> node_ref
        """
        self.emit(node, node.kid[0].py_code)

    def exit_node_ref(self: "TranspilePass", node: AstNode) -> None:
        """Convert node_ref to python code.

        node_ref -> KW_NODE DBL_COLON NAME
        """
        self.emit(
            node,
            f"({BUILTIN_TAG}.{node.kid[0].py_code.upper()}, {node.kid[2].py_code})",
        )

    def exit_walker_ref(self: "TranspilePass", node: AstNode) -> None:
        """Convert walker_ref to python code.

        walker_ref -> KW_WALKER DBL_COLON NAME
        """
        # self.emit(
        #     node,
        #     f"({BUILTIN_TAG}.{node.kid[0].py_code.upper()}, {node.kid[2].py_code})",
        # )

    def exit_object_ref(self: "TranspilePass", node: AstNode) -> None:
        """Convert object_ref to python code.

        object_ref -> KW_OBJECT DBL_COLON NAME
        """
        self.emit(
            node,
            f"({BUILTIN_TAG}.{node.kid[0].py_code.upper()}, {node.kid[2].py_code})",
        )

    def exit_edge_op_ref(self: "TranspilePass", node: AstNode) -> None:
        """Convert edge_op_ref to python code.

        edge_op_ref -> edge_any
        edge_op_ref -> edge_from
        edge_op_ref -> edge_to
        """
        self.emit(node, node.kid[0].py_code)

    def exit_edge_any(self: "TranspilePass", node: AstNode) -> None:
        """Convert edge_any to python code.

        edge_any -> ARROW_L_p1 NAME filter_ctx ARROW_R_p2
        edge_any -> ARROW_BI
        """
        if len(node.kid) == 1:
            self.emit(node, f"({BUILTIN_TAG}.EDGE_ANY, None)")
        else:
            self.emit(
                node,
                f"({BUILTIN_TAG}.EDGE_ANY, ({node.kid[1].py_code}, {node.kid[2].py_code})",
            )

    def exit_edge_from(self: "TranspilePass", node: AstNode) -> None:
        """Convert edge_from to python code.

        edge_from -> ARROW_L_p1 NAME filter_ctx ARROW_L_p2
        edge_from -> ARROW_L
        """
        if len(node.kid) == 1:
            self.emit(node, f"({BUILTIN_TAG}.EDGE_FROM, None)")
        else:
            self.emit(
                node,
                f"({BUILTIN_TAG}.EDGE_FROM, ({node.kid[1].py_code}, {node.kid[2].py_code})",
            )

    def exit_edge_to(self: "TranspilePass", node: AstNode) -> None:
        """Convert edge_to to python code.

        edge_to -> ARROW_R_p1 NAME filter_ctx ARROW_R_p2
        edge_to -> ARROW_R
        """
        if len(node.kid) == 1:
            self.emit(node, f"({BUILTIN_TAG}.EDGE_TO, None)")
        else:
            self.emit(
                node,
                f"({BUILTIN_TAG}.EDGE_TO, ({node.kid[1].py_code}, {node.kid[2].py_code})",
            )

    def exit_connect_op(self: "TranspilePass", node: AstNode) -> None:
        """Convert connect_op to python code.

        connect_op -> connect_any
        connect_op -> connect_from
        connect_op -> connect_to
        """
        self.emit(node, node.kid[0].py_code)

    def exit_connect_to(self: "TranspilePass", node: AstNode) -> None:
        """Convert connect_to to python code.

        connect_to -> CARROW_R_p1 NAME spawn_ctx CARROW_R_p2
        connect_to -> CARROW_R
        """
        if len(node.kid) == 1:
            self.emit(node, f"({BUILTIN_TAG}.CONNECT_TO, None)")
        else:
            self.emit(
                node,
                f"({BUILTIN_TAG}.CONNECT_TO, ({node.kid[1].py_code}, {node.kid[2].py_code})",
            )

    def exit_connect_from(self: "TranspilePass", node: AstNode) -> None:
        """Convert connect_from to python code.

        connect_from -> CARROW_L_p1 NAME spawn_ctx CARROW_L_p2
        connect_from -> CARROW_L
        """
        if len(node.kid) == 1:
            self.emit(node, f"({BUILTIN_TAG}.CONNECT_FROM, None)")
        else:
            self.emit(
                node,
                f"({BUILTIN_TAG}.CONNECT_FROM, ({node.kid[1].py_code}, {node.kid[2].py_code})",
            )

    def exit_connect_any(self: "TranspilePass", node: AstNode) -> None:
        """Convert connect_any to python code.

        connect_any -> CARROW_L_p1 NAME spawn_ctx CARROW_R_p2
        connect_any -> CARROW_BI
        """
        if len(node.kid) == 1:
            self.emit(node, f"({BUILTIN_TAG}.CONNECT_ANY, None)")
        else:
            self.emit(
                node,
                f"({BUILTIN_TAG}.CONNECT_ANY, ({node.kid[1].py_code}, {node.kid[2].py_code})",
            )

    def exit_filter_ctx(self: "TranspilePass", node: AstNode) -> None:
        """Convert filter_ctx to python code.

        filter_ctx -> LPAREN filter_compare_list RPAREN
        """
        self.emit(node, f"{node.kid[1].py_code}")

    def exit_spawn_ctx(self: "TranspilePass", node: AstNode) -> None:
        """Convert spawn_ctx to python code.

        spawn_ctx -> LPAREN assignment_list RPAREN
        """
        self.emit(node, f"{node.kid[1].py_code}")

    def exit_filter_compare_list(self: "TranspilePass", node: AstNode) -> None:
        """Convert filter_compare_list to python code.

        filter_compare_list -> NAME cmp_op expression COMMA filter_compare_list
        filter_compare_list -> NAME cmp_op expression
        """
        if len(node.kid) == 3:
            self.emit(
                node,
                f"({BUILTIN_TAG}.FILTER_COMPARE_LIST, "
                f"({node.kid[0].py_code}, {node.kid[1].py_code}, {node.kid[2].py_code}))",
            )
        else:
            self.emit(
                node,
                f"({BUILTIN_TAG}.FILTER_COMPARE_LIST, "
                f"({node.kid[0].py_code}, {node.kid[1].py_code}, {node.kid[2].py_code})),  {node.kid[2].py_code})",
            )

    def exit_node(self: "TranspilePass", node: AstNode) -> None:
        """Convert node to python code."""
        if node.kind == AstNodeKind.TOKEN:
            if node.name == "DOC_STRING":
                self.emit_ln(node, node.value)
            else:
                self.emit(node, str(node.value))
        super().exit_node(node)

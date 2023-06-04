"""Transpilation pass for Jaseci Ast."""
from jaseci.jac.passes.ir_pass import AstNode, AstNodeKind, Pass


# MACROS for rapid development
MAST = "active_master"
MAST_PATH = "jaseci.core.master"
SENT = f"{MAST}.active_sentinel"
RT = f"{MAST}.runtime"
SET_LINE_FUNC = lambda x: f"{RT}set_line('{x}')\n"  # noqa
REG_GLOB_FUNC = lambda x, y: f"{RT}.register_global({x}, {y})\n"  # noqa
HAS_TAGS = "HasTags"  # noqa
EVENT_TAG = "EventTag"  # noqa
SYNC_CMD = "sync_on"  # noqa
YIELD_CMD = "yield_now"  # noqa


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
        node.py_code = (
            self.indent_str(indent_delta)
            + s.replace("\n", "\n" + self.indent_str(indent_delta))
            + "\n"
        )
        print(node.py_code)

    def emit(self: "TranspilePass", node: AstNode, s: str) -> None:
        """Emit code to node."""
        node.py_code += s

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

        ability -> KW_ABILITY arch_ref NAME code_block
        """
        self.indent_level += 1

    def exit_ability(self: "TranspilePass", node: AstNode) -> None:
        """Convert ability to python code.

        ability -> KW_ABILITY arch_ref NAME code_block
        """
        arch = node.kid[1].py_code
        name = f"ability_{arch['typ']}_{arch['name']}_{node.kid[2].py_code}"
        self.emit_ln(node, f"def {name}(here, visitor):", indent_delta=-1)
        self.emit_ln(node, node.kid[3].py_code)
        self.indent_level -= 1

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

        has_assign_clause -> has_assign_clause COMMA has_assign
        has_assign_clause -> has_assign
        """
        if len(node.kid) == 1:
            self.emit(node, node.kid[0].py_code)
        else:
            self.emit(node, node.kid[0].py_code)
            self.emit(node, node.kid[2].py_code)

    def exit_has_assign(self: "TranspilePass", node: AstNode) -> None:
        """Convert has assign to python code.

        has_assign -> NAME type_spec EQ expression
        has_assign -> NAME type_spec
        has_assign -> has_tag NAME type_spec EQ expression
        has_assign -> has_tag NAME type_spec
        """
        has_tag = node.kid[0].name == "has_tag"
        tags = node.kid[0].py_code if has_tag else ""
        name = node.kid[1].py_code if has_tag else node.kid[0].py_code
        typ = node.kid[2].py_code if has_tag else node.kid[1].py_code
        value = node.kid[-1].py_code if node.kid[-1].name == "expression" else "None"
        self.emit_ln(
            node,
            f"self.add_context(name={name}, value={value}, typ={typ}, tags=[{tags}])",
        )

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

    def exit_walker_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert walker stmt to python code.

        walker_stmt -> yield_stmt
        walker_stmt -> disengage_stmt
        walker_stmt -> take_stmt
        walker_stmt -> ignore_stmt
        """
        self.emit(node, node.kid[0].py_code)

    def exit_ignore_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert ignore stmt to python code.

        ignore_stmt -> KW_IGNORE expression SEMI
        """
        self.emit_ln(node, f"visitor.ignore({node.kid[1].py_code})")

    def exit_take_stmt(self: "TranspilePass", node: AstNode) -> None:
        """Convert take stmt to python code.

        take_stmt -> KW_TAKE sub_name expression else_stmt
        take_stmt -> KW_TAKE expression else_stmt
        take_stmt -> KW_TAKE sub_name expression SEMI
        take_stmt -> KW_TAKE expression SEMI
        """
        if len(node.kid) == 5:
            self.emit_ln(
                node, f"visitor.take({node.kid[2].py_code}, {node.kid[3].py_code})"
            )
            self.emit(node, node.kid[4].py_code)
        else:
            self.emit_ln(node, f"visitor.take({node.kid[1].py_code})")
            self.emit(node, node.kid[2].py_code)

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

    def exit_assignment(self: "TranspilePass", node: AstNode) -> None:
        """Convert assignment to python code.

        assignment -> atom EQ expression
        """
        self.emit_ln(node, f"{node.kid[0].py_code} = {node.kid[2].py_code}")

    def exit_expression(self: "TranspilePass", node: AstNode) -> None:
        """Convert expression to python code.

        expression -> connect walrus_op expression
        expression -> connect
        """
        if len(node.kid) == 3 and node.kid[1].name == "WALRUS_EQ":
            self.emit_ln(
                node,
                f"{node.kid[0].py_code} {node.kid[1].py_code} {node.kid[2].py_code}",
            )
        elif len(node.kid) == 1:
            self.emit(node, node.kid[0].py_code)
        else:
            self.emit_ln(
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
            self.emit_ln(
                node,
                f"{node.kid[0].py_code}.connect(typ={node.kid[1].py_code}, target={node.kid[2].py_code})",
            )
        elif len(node.kid) == 4:
            self.emit_ln(
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
        if len(node.kid) == 3:
            self.emit_ln(
                node,
                f"{node.kid[0].py_code} {node.kid[1].py_code} {node.kid[2].py_code}",
            )
        else:
            self.emit(node, node.kid[0].py_code)

    def exit_compare(self: "TranspilePass", node: AstNode) -> None:
        """Convert compare to python code.

        compare -> arithmetic cmp_op compare
        compare -> NOT compare
        compare -> arithmetic
        """
        if len(node.kid) == 3:
            self.emit_ln(
                node,
                f"{node.kid[0].py_code} {node.kid[1].py_code} {node.kid[2].py_code}",
            )
        elif len(node.kid) == 2:
            self.emit_ln(node, f"not {node.kid[1].py_code}")
        else:
            self.emit(node, node.kid[0].py_code)

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
        if len(node.kid) == 3:
            self.emit_ln(
                node,
                f"{node.kid[0].py_code} {node.kid[1].py_code} {node.kid[2].py_code}",
            )
        else:
            self.emit(node, node.kid[0].py_code)

    def exit_term(self: "TranspilePass", node: AstNode) -> None:
        """Convert term to python code.

        term -> factor MOD term
        term -> factor DIV term
        term -> factor STAR_MUL term
        term -> factor
        """
        if len(node.kid) == 3:
            self.emit_ln(
                node,
                f"{node.kid[0].py_code} {node.kid[1].py_code} {node.kid[2].py_code}",
            )
        else:
            self.emit(node, node.kid[0].py_code)

    def exit_factor(self: "TranspilePass", node: AstNode) -> None:
        """Convert factor to python code.

        factor -> power
        factor -> MINUS factor
        factor -> PLUS factor
        """
        op = "-" if node.kid[0].name == "MINUS" else ""
        if len(node.kid) == 2:
            self.emit_ln(node, f"{op}{node.kid[1].py_code}")
        else:
            self.emit(node, node.kid[0].py_code)

    def exit_power(self: "TranspilePass", node: AstNode) -> None:
        """Convert power to python code.

        power -> KW_SYNC atom
        power -> deref
        power -> ref
        power -> atom POW factor
        power -> atom
        """
        if node.kid[0].name == "KW_SYNC":
            self.emit_ln(node, f"visitor.{SYNC_CMD}({node.kid[1].py_code})")
        elif len(node.kid) == 3:
            self.emit(node, f"{node.kid[0].py_code} ** {node.kid[2].py_code}")
        else:
            self.emit(node, node.kid[0].py_code)

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
    # param_list -> expr_list COMMA assignment_list
    # param_list -> assignment_list
    # param_list -> expr_list
    # assignment_list -> assignment COMMA assignment_list
    # assignment_list -> assignment
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
    # spawn_ctx -> LPAREN assignment_list RPAREN
    # filter_compare_list -> NAME cmp_op expression COMMA filter_compare_list
    # filter_compare_list -> NAME cmp_op expression

    def exit_multistring(self: "TranspilePass", node: AstNode) -> None:
        """Convert multistring to python code."""
        for i in node.kid:
            self.emit(node, i.py_code + " ")
        self.emit(node, str(node.value))

    def exit_node(self: "TranspilePass", node: AstNode) -> None:
        """Convert node to python code."""
        if node.kind == AstNodeKind.TOKEN:
            self.emit(node, str(node.value))
        super().exit_node(node)

"""Transpilation of Jaseci code to python code."""

from jaseci.jac.lexer import JacLexer
from jaseci.jac.parser import JacParser


class JacTranspiler:
    """Transpiler for Jaseci code to python code."""

    def __init__(self: "JacTranspiler") -> None:
        """Initialize transpiler."""
        self.lexer = JacLexer()
        self.parser = JacParser()
        self.output = ""

    def transpile(self: "JacTranspiler", code: str) -> None:
        """Transpile code."""
        self.indent = 0
        self.cur_line = 0
        self.stack = []
        self.output = ""
        self.tree = self.parser.parse(self.lexer.tokenize(code))
        self.transpile_start(self.tree)
        return self.output

    def transpile_rule(self: "JacTranspiler", rule: tuple) -> str:
        """Convert rule to function name."""
        if isinstance(rule, tuple):
            self.check_line_changed(rule)
            return getattr(self, f"transpile_{rule[0]}")(rule)

    def emit(self: "JacTranspiler", code: str) -> None:
        """Emit code."""
        self.output += "    " * self.indent + code + "\n"

    def proc_rhs(self: "JacTranspiler", tree: tuple) -> None:
        """Process right hand side of rule."""
        for rule in tree[2:]:
            self.transpile_rule(rule)

    def check_line_changed(self: "JacTranspiler", rule: int) -> bool:
        """Check if line changed."""
        if self.cur_line != rule[1]:
            self.emit(f"active_sent.set_jac_line({int(rule[1])})")
            self.cur_line = int(rule[1])
            return True
        return False

    # All mighty start rule
    # ---------------------
    def transpile_start(self: "JacParser", tree: tuple) -> None:
        """Start rule."""
        self.emit("from jaseci.core.sentinel import active_sent")
        self.proc_rhs(tree)

    # Jac program structured as a list of elements
    # --------------------------------------------
    def transpile_element_list(self: "JacParser", tree: tuple) -> None:
        """Element list rule."""
        self.proc_rhs(tree)

    # Element types
    # -------------
    def transpile_element(self: "JacParser", tree: tuple) -> None:
        """Element rule."""
        self.emit(f"# {tree[2][0]}")
        self.proc_rhs(tree)

    def transpile_global_var(self: "JacParser", tree: tuple) -> None:
        """Global variable rule."""
        self.proc_rhs(tree)

    def transpile_global_var_clause(self: "JacParser", tree: tuple) -> None:
        """Global variable tail rule."""
        self.proc_rhs(tree)

    def transpile_test(self: "JacParser", tree: tuple) -> None:
        """Test rule."""
        self.proc_rhs(tree)

    # Import Statements
    # -----------------
    def transpile_import_stmt(self: "JacParser", tree: tuple) -> None:
        """Import rule."""
        self.proc_rhs(tree)

    def transpile_import_path(self: "JacParser", tree: tuple) -> None:
        """Import path rule."""
        self.proc_rhs(tree)

    def transpile_import_path_prefix(self: "JacParser", tree: tuple) -> None:
        """Import path prefix rule."""
        self.proc_rhs(tree)

    def transpile_import_path_tail(self: "JacParser", tree: tuple) -> None:
        """Import path tail rule."""
        self.proc_rhs(tree)

    def transpile_name_as_list(self: "JacParser", tree: tuple) -> None:
        """Name as list rule."""
        self.proc_rhs(tree)

    # Architype elements
    # ------------------
    def transpile_architype(self: "JacParser", tree: tuple) -> None:
        """Architype rule."""
        self.proc_rhs(tree)

    def transpile_arch_decl_tail(self: "JacParser", tree: tuple) -> None:
        """Architype tail rule."""
        self.proc_rhs(tree)

    def transpile_inherited_archs(self: "JacParser", tree: tuple) -> None:
        """Sub name list rule."""
        self.proc_rhs(tree)

    def transpile_sub_name(self: "JacParser", tree: tuple) -> None:
        """Sub name rule."""
        self.proc_rhs(tree)

    # Attribute blocks
    # ----------------
    def transpile_attr_block(self: "JacParser", tree: tuple) -> None:
        """Attribute block rule."""
        self.proc_rhs(tree)

    def transpile_attr_stmt_list(self: "JacParser", tree: tuple) -> None:
        """Attribute statement list rule."""
        self.proc_rhs(tree)

    def transpile_attr_stmt(self: "JacParser", tree: tuple) -> None:
        """Attribute statement rule."""
        self.proc_rhs(tree)

    # Has statements
    # --------------
    def transpile_has_stmt(self: "JacParser", tree: tuple) -> None:
        """Has statement rule."""
        self.proc_rhs(tree)

    def transpile_has_assign_clause(self: "JacParser", tree: tuple) -> None:
        """Has assign list rule."""
        self.proc_rhs(tree)

    def transpile_has_assign(self: "JacParser", tree: tuple) -> None:
        """Has assign rule."""
        self.proc_rhs(tree)

    def transpile_has_tag(self: "JacParser", tree: tuple) -> None:
        """Has tag rule."""
        self.proc_rhs(tree)

    def transpile_type_spec(self: "JacParser", tree: tuple) -> None:
        """Type hint rule."""
        self.proc_rhs(tree)

    def transpile_type_name(self: "JacParser", tree: tuple) -> None:
        """Type hint rule."""
        self.proc_rhs(tree)

    def transpile_builtin_type(self: "JacParser", tree: tuple) -> None:
        """Any type rule."""
        self.proc_rhs(tree)

    # Can statements
    # --------------
    def transpile_can_stmt(self: "JacParser", tree: tuple) -> None:
        """Can statement rule."""
        self.proc_rhs(tree)

    def transpile_event_clause(self: "JacParser", tree: tuple) -> None:
        """Event clause rule."""
        self.proc_rhs(tree)

    def transpile_name_list(self: "JacParser", tree: tuple) -> None:
        """Name list rule."""
        self.proc_rhs(tree)

    def transpile_code_block(self: "JacParser", tree: tuple) -> None:
        """Code block rule."""
        self.proc_rhs(tree)

    # Codeblock statements
    # --------------------
    def transpile_statement_list(self: "JacParser", tree: tuple) -> None:
        """Statement list rule."""
        self.proc_rhs(tree)

    def transpile_statement(self: "JacParser", tree: tuple) -> None:
        """Statement rule."""
        self.proc_rhs(tree)

    def transpile_if_stmt(self: "JacParser", tree: tuple) -> None:
        """If statement rule."""
        self.proc_rhs(tree)

    def transpile_elif_stmt_list(self: "JacParser", tree: tuple) -> None:
        """Else if statement list rule."""
        self.proc_rhs(tree)

    def transpile_else_stmt(self: "JacParser", tree: tuple) -> None:
        """Else statement rule."""
        self.proc_rhs(tree)

    def transpile_try_stmt(self: "JacParser", tree: tuple) -> None:
        """Try statement rule."""
        self.proc_rhs(tree)

    def transpile_else_from_try(self: "JacParser", tree: tuple) -> None:
        """Else from try rule."""
        self.proc_rhs(tree)

    def transpile_for_stmt(self: "JacParser", tree: tuple) -> None:
        """For statement rule."""
        self.proc_rhs(tree)

    def transpile_while_stmt(self: "JacParser", tree: tuple) -> None:
        """While statement rule."""
        self.proc_rhs(tree)

    def transpile_assert_stmt(self: "JacParser", tree: tuple) -> None:
        """Assert statement rule."""
        self.proc_rhs(tree)

    def transpile_ctrl_stmt(self: "JacParser", tree: tuple) -> None:
        """Control statement rule."""
        self.proc_rhs(tree)

    def transpile_delete_stmt(self: "JacParser", tree: tuple) -> None:
        """Delete statement rule."""
        self.proc_rhs(tree)

    def transpile_report_stmt(self: "JacParser", tree: tuple) -> None:
        """Report statement rule."""
        self.proc_rhs(tree)

    def transpile_walker_stmt(self: "JacParser", tree: tuple) -> None:
        """Walker statement rule."""
        self.proc_rhs(tree)

    def transpile_ignore_stmt(self: "JacParser", tree: tuple) -> None:
        """Ignore statement rule."""
        self.proc_rhs(tree)

    def transpile_take_stmt(self: "JacParser", tree: tuple) -> None:
        """Take statement rule."""
        self.proc_rhs(tree)

    def transpile_disengage_stmt(self: "JacParser", tree: tuple) -> None:
        """Disengage statement rule."""
        self.proc_rhs(tree)

    def transpile_yield_stmt(self: "JacParser", tree: tuple) -> None:
        """Yield statement rule."""
        self.proc_rhs(tree)

    # Expression rules
    # ----------------
    def transpile_expression(self: "JacParser", tree: tuple) -> None:
        """Expression rule."""
        self.proc_rhs(tree)

    def transpile_assignment_op(self: "JacParser", tree: tuple) -> None:
        """Production Assignment rule."""
        self.proc_rhs(tree)

    def transpile_connect(self: "JacParser", tree: tuple) -> None:
        """Connect rule."""
        self.proc_rhs(tree)

    def transpile_logical(self: "JacParser", tree: tuple) -> None:
        """Logical rule."""
        self.proc_rhs(tree)

    def transpile_compare(self: "JacParser", tree: tuple) -> None:
        """Compare rule."""
        self.proc_rhs(tree)

    def transpile_cmp_op(self: "JacParser", tree: tuple) -> None:
        """Compare operator rule."""
        self.proc_rhs(tree)

    def transpile_arithmetic(self: "JacParser", tree: tuple) -> None:
        """Arithmetic rule."""
        self.proc_rhs(tree)

    def transpile_term(self: "JacParser", tree: tuple) -> None:
        """Term rule."""
        self.proc_rhs(tree)

    def transpile_factor(self: "JacParser", tree: tuple) -> None:
        """Factor rule."""
        self.proc_rhs(tree)

    def transpile_power(self: "JacParser", tree: tuple) -> None:
        """Power rule."""
        self.proc_rhs(tree)

    def transpile_ref(self: "JacParser", tree: tuple) -> None:
        """Production for reference rule."""
        self.proc_rhs(tree)

    def transpile_deref(self: "JacParser", tree: tuple) -> None:
        """Dereference rule."""
        self.proc_rhs(tree)

    # Atom rules
    # --------------------
    def transpile_atom(self: "JacParser", tree: tuple) -> None:
        """Atom rule."""
        self.proc_rhs(tree)

    def transpile_multistring(self: "JacParser", tree: tuple) -> None:
        """Multistring rule."""
        self.proc_rhs(tree)

    def transpile_list_val(self: "JacParser", tree: tuple) -> None:
        """List value rule."""
        self.proc_rhs(tree)

    def transpile_expr_list(self: "JacParser", tree: tuple) -> None:
        """Expression list rule."""
        self.proc_rhs(tree)

    def transpile_dict_val(self: "JacParser", tree: tuple) -> None:
        """Production for dictionary value rule."""
        self.proc_rhs(tree)

    def transpile_kv_pairs(self: "JacParser", tree: tuple) -> None:
        """Key/value pairs rule."""
        self.proc_rhs(tree)

    def transpile_ability_op(self: "JacParser", tree: tuple) -> None:
        """Ability operator rule."""
        self.proc_rhs(tree)

    def transpile_atom_trailer(self: "JacParser", tree: tuple) -> None:
        """Atom trailer rule."""
        self.proc_rhs(tree)

    def transpile_ability_call(self: "JacParser", tree: tuple) -> None:
        """Ability call rule."""
        self.proc_rhs(tree)

    def transpile_param_list(self: "JacParser", tree: tuple) -> None:
        """Parameter list rule."""
        self.proc_rhs(tree)

    def transpile_kw_expr_list(self: "JacParser", tree: tuple) -> None:
        """Keyword expression list rule."""
        self.proc_rhs(tree)

    def transpile_index_slice(self: "JacParser", tree: tuple) -> None:
        """Index/slice rule."""
        self.proc_rhs(tree)

    def transpile_global_ref(self: "JacParser", tree: tuple) -> None:
        """Global reference rule."""
        self.proc_rhs(tree)

    def transpile_node_edge_ref(self: "JacParser", tree: tuple) -> None:
        """Node/edge reference rule."""
        self.proc_rhs(tree)

    # Spawn rules
    # -----------
    def transpile_spawn(self: "JacParser", tree: tuple) -> None:
        """Spawn rule."""
        self.proc_rhs(tree)

    def transpile_spawn_arch(self: "JacParser", tree: tuple) -> None:
        """Spawn object rule."""
        self.proc_rhs(tree)

    def transpile_spawn_edge(self: "JacParser", tree: tuple) -> None:
        """Spawn edge rule."""
        self.proc_rhs(tree)

    def transpile_node_spawn(self: "JacParser", tree: tuple) -> None:
        """Node spawn rule."""
        self.proc_rhs(tree)

    def transpile_walker_spawn(self: "JacParser", tree: tuple) -> None:
        """Walker spawn rule."""
        self.proc_rhs(tree)

    def transpile_object_spawn(self: "JacParser", tree: tuple) -> None:
        """Type spawn rule."""
        self.proc_rhs(tree)

    # Built-in function rules
    # -----------------------
    def transpile_built_in(self: "JacParser", tree: tuple) -> None:
        """Built-in rule."""
        self.proc_rhs(tree)

    def transpile_obj_built_in(self: "JacParser", tree: tuple) -> None:
        """Object built-in rule."""
        self.proc_rhs(tree)

    def transpile_cast_built_in(self: "JacParser", tree: tuple) -> None:
        """Cast built-in rule."""
        self.proc_rhs(tree)

    # Architype reference rules
    # -------------------------
    def transpile_arch_ref(self: "JacParser", tree: tuple) -> None:
        """Architype reference rule."""
        self.proc_rhs(tree)

    def transpile_node_ref(self: "JacParser", tree: tuple) -> None:
        """Node reference rule."""
        self.proc_rhs(tree)

    def transpile_edge_ref(self: "JacParser", tree: tuple) -> None:
        """Node reference rule."""
        self.proc_rhs(tree)

    def transpile_walker_ref(self: "JacParser", tree: tuple) -> None:
        """Walker reference rule."""
        self.proc_rhs(tree)

    def transpile_obj_ref(self: "JacParser", tree: tuple) -> None:
        """Type reference rule."""
        self.proc_rhs(tree)

    # Node / Edge reference and connection rules
    # ------------------------------------------
    def transpile_edge_op_ref(self: "JacParser", tree: tuple) -> None:
        """Edge reference rule."""
        self.proc_rhs(tree)

    def transpile_edge_to(self: "JacParser", tree: tuple) -> None:
        """Edge to rule."""
        self.proc_rhs(tree)

    def transpile_edge_from(self: "JacParser", tree: tuple) -> None:
        """Edge from rule."""
        self.proc_rhs(tree)

    def transpile_edge_any(self: "JacParser", tree: tuple) -> None:
        """Edge any rule."""
        self.proc_rhs(tree)

    def transpile_connect_op(self: "JacParser", tree: tuple) -> None:
        """Connect operator rule."""
        self.proc_rhs(tree)

    def transpile_connect_to(self: "JacParser", tree: tuple) -> None:
        """Connect to rule."""
        self.proc_rhs(tree)

    def transpile_connect_from(self: "JacParser", tree: tuple) -> None:
        """Connect from rule."""
        self.proc_rhs(tree)

    def transpile_connect_any(self: "JacParser", tree: tuple) -> None:
        """Connect any rule."""
        self.proc_rhs(tree)

    def transpile_filter_ctx(self: "JacParser", tree: tuple) -> None:
        """Filter context rule."""
        self.proc_rhs(tree)

    def transpile_spawn_ctx(self: "JacParser", tree: tuple) -> None:
        """Spawn context rule."""
        self.proc_rhs(tree)

    def transpile_spawn_assign_list(self: "JacParser", tree: tuple) -> None:
        """Spawn assignment list rule."""
        self.proc_rhs(tree)

    def transpile_filter_compare_list(self: "JacParser", tree: tuple) -> None:
        """Filter comparison list rule."""
        self.proc_rhs(tree)

    # Literal rules (overcomes sly limitations)
    # -----------------------------------------

    def transpile_int_literal(self: "JacParser", tree: tuple) -> None:
        """Integer literal rule."""
        self.proc_rhs(tree)

    def transpile_float_literal(self: "JacParser", tree: tuple) -> None:
        """Float literal rule."""
        self.proc_rhs(tree)

    def transpile_string_literal(self: "JacParser", tree: tuple) -> None:
        """Str literal rule."""
        self.proc_rhs(tree)

    def transpile_doc_string_literal(self: "JacParser", tree: tuple) -> None:
        """Doc_string literal rule."""
        self.proc_rhs(tree)

    def transpile_bool_literal(self: "JacParser", tree: tuple) -> None:
        """Boolean literal rule."""
        self.proc_rhs(tree)

    def transpile_null_literal(self: "JacParser", tree: tuple) -> None:
        """Null literal rule."""
        self.proc_rhs(tree)

    def transpile_name_literal(self: "JacParser", tree: tuple) -> None:
        """Name literal rule."""
        self.proc_rhs(tree)

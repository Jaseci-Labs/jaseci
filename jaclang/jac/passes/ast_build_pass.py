"""Pass that builds well formed AST from parse tree AST."""
from typing import Type

import jaclang.jac.ast as ast
from jaclang.jac.passes.ir_pass import Pass


class AstBuildPass(Pass):
    """Ast build pass."""

    # def __init__(self: "AstBuildPass", ir: ast.AstNode = None) -> None:
    #     """Initialize pass."""
    #     super().__init__(ir)

    def exit_start(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build WHOLE_BUILD Ast node."""
        node.kid = node.kid[0].kid
        self.ir = ast.WholeBuild(
            elements=node.kid, parent=None, kid=node.kid, line=node.line
        )

    def exit_element_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Chain list together into actual list."""
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]

    def exit_element(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Replace element with its kid."""
        node = replace_node(node, node.kid[0])
        if type(node) == ast.Token:
            update_kind(node, ast.DocString, value=node.value)

    def exit_global_var(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build GLOBAL_VAR Ast node."""
        node.kid = node.kid[:-3]  # only keep absorbed list of clauses
        update_kind(node, ast.GlobalVars, values=node.kid)

    def exit_global_var_clause(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build NAMED_ASSIGN list of Ast nodes."""
        if len(node.kid) == 3:
            # at base case abosrb node to front of parent
            node.parent.kid = [node] + node.parent.kid
        elif len(node.kid) >= 4:
            # at recursive case abosrb node to front of parent and
            # cut include all aborbed nodes so far
            node.parent.kid = [node] + node.kid[:-5] + node.parent.kid
        node.kid = [node.kid[-3], node.kid[-1]]
        update_kind(node, ast.NamedAssign, name=node.kid[0], value=node.kid[1])

    def exit_test(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build TEST Ast node."""
        node.kid = node.kid[1:]
        update_kind(
            node, ast.Test, name=node.kid[0], description=node.kid[1], body=node.kid[2]
        )

    def exit_import_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build IMPORT Ast node."""
        kid = node.kid
        meta = {
            "lang": kid[1],
            "path": kid[2],
            "alias": None,
            "items": None,
        }
        if len(node.kid) == 7:
            meta["path"] = kid[3]
            meta["items"] = kid[5]
            node.kid = [kid[1], kid[3], kid[5]]
        elif len(node.kid) == 6:
            meta["alias"] = kid[4]
            node.kid = [kid[1], kid[2], kid[4]]
        else:
            node.kid = [kid[1], kid[2]]
        update_kind(node, ast.Import, **meta)

    def exit_import_path(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build MOD_PATH Ast node."""
        if len(node.kid) == 1:
            node.kid = node.kid[0].kid
        else:
            node.kid = node.kid[0].kid + node.kid[1].kid
        update_kind(node, ast.ModulePath, path=node.kid)

    def exit_import_path_prefix(self: "AstBuildPass", node: ast.AstNode) -> None:
        """No action needed, absorbed by parent."""

    def exit_import_path_tail(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Chain list together into actual list."""
        if len(node.kid) > 2:
            node.kid = node.kid[0].kid + [node.kid[1], node.kid[2]]

    def exit_name_as_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build MOD_ITEM list of Ast nodes. TODO: VALIDATE."""
        meta = {}
        meta["alias"] = None
        if node.kid[0].name == "NAME":
            meta["name"] = node.kid[0]
            node.parent.kid = [node] + node.parent.kid
            if len(node.kid) == 3:
                node.kid = [node.kid[0], node.kid[2]]
                meta["alias"] = node.kid[2]
            else:
                node.kid = [node.kid[0]]
        elif node.kid[-2].name == "KW_AS":
            node.parent.kid = [node] + node.kid[:-5] + node.parent.kid
            node.kid = [node.kid[-3], node.kid[-1]]
            meta["name"] = node.kid[-3]
            meta["alias"] = node.kid[-1]
        else:
            node.parent.kid = [node] + node.kid[:-3] + node.parent.kid
            node.kid = [node.kid[-1]]
            meta["name"] = node.kid[-1]
        update_kind(node, ast.ModuleItem, **meta)

    def exit_architype(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build various architype Ast nodes."""
        if node.kid[0].name == "KW_SPAWNER":
            node.kid = node.kid[1:]
            update_kind(node, ast.SpawnerArch, name=node.kid[0], body=node.kid[1])
        else:
            meta = {}
            if node.kid[0].name == "KW_NODE":
                meta["kind"] = ast.NodeArch
            elif node.kid[0].name == "KW_EDGE":
                meta["kind"] = ast.EdgeArch
            elif node.kid[0].name == "KW_OBJECT":
                meta["kind"] = ast.ObjectArch
            elif node.kid[0].name == "KW_WALKER":
                meta["kind"] = ast.WalkerArch
            meta["name"] = node.kid[1]
            if (type(node.kid[2].kid[0])) == ast.BaseClasses:
                node.kid = [node.kid[1], node.kid[2].kid[0], node.kid[2].kid[1]]
                meta["base_classes"] = node.kid[1]
                meta["body"] = node.kid[2]
            else:
                node.kid = [node.kid[1], node.kid[2].kid[0]]
                meta["base_classes"] = None
                meta["body"] = node.kid[1]
            update_kind(node, **meta)

    def exit_arch_decl_tail(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Absorbed by single consumer."""

    def exit_inherited_archs(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Chain list together into actual list."""
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]
        update_kind(node, ast.BaseClasses, base_classes=node.kid)

    def exit_sub_name(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build SUB_NAME Ast node."""
        node = replace_node(node, node.kid[1])

    def exit_ability_spec(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build AbilitySpec Ast node."""
        meta = {}
        if node.kid[0].name == "NAME":
            meta["mod"] = node.kid[0]
            meta["arch"] = node.kid[1]
            meta["name"] = node.kid[2]
            if node.kid[3].name == "func_decl":
                meta["signature"] = node.kid[3]
                meta["body"] = node.kid[4]
            else:
                meta["signature"] = None
                meta["body"] = node.kid[3]
        else:
            meta["mod"] = None
            meta["arch"] = node.kid[0]
            meta["name"] = node.kid[1]
            if node.kid[2].name == "func_decl":
                meta["signature"] = node.kid[2]
                meta["body"] = node.kid[3]
            else:
                meta["signature"] = None
                meta["body"] = node.kid[2]
        update_kind(node, ast.AbilitySpec, **meta)

    def exit_attr_block(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Build ARCH_BLOCK Ast node."""
        meta = {"body": None}
        if len(node.kid) <= 2:
            node.kid = []
        else:
            node.kid = node.kid[1].kid
            meta["body"] = node.kid[0]
        update_kind(node, ast.ArchBlock, **meta)

    def exit_attr_stmt_list(self: "AstBuildPass", node: ast.AstNode) -> None:
        """Chain list together into actual list."""
        if len(node.kid) == 2:
            node.kid = node.kid[0].kid + [node.kid[1]]

    # def exit_attr_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    #     """Replace self with actual attr stmt."""
    #     node = replace_node(node, node.kid[0])

    # def exit_has_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    #     """Collect list of individual vars."""
    #     node = replace_node(node, node.kid[0])

    # def exit_has_assign_clause(self: "AstBuildPass", node: ast.AstNode) -> None:
    #     """Push list of individual vars into parent."""
    #     node = replace_node(node, node.kid[0])
    #     if len(node.kid) == 1:
    #         node.parent.kid = [node] + node.parent.kid

    # def exit_param_var(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_has_tag(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_type_spec(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_type_name(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_builtin_type(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_can_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_can_ds_ability(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_can_func_ability(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_event_clause(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_func_decl(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_func_decl_param_list(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_name_list(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_code_block(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_statement_list(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_statement(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_if_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_elif_stmt_list(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_else_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_try_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_else_from_try(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_for_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_while_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_assert_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_ctrl_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_delete_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_report_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_return_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_walker_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_ignore_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_visit_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_revisit_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_disengage_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_yield_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_sync_stmt(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_assignment(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_expression(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_walrus_assign(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_pipe(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_elvis_check(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_logical(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_compare(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_arithmetic(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_term(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_factor(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_power(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_connect(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_spawn_walker(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_spawn_object(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_spawn_edge_node(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_unpack(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_walrus_op(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_cmp_op(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_spawn_op(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_atom(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_atom_literal(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_atom_collection(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_multistring(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_list_val(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_expr_list(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_dict_val(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_kv_pairs(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_ability_run(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_atomic_chain(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_atomic_chain_unsafe(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_atomic_chain_safe(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_call(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_param_list(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_assignment_list(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_index_slice(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_global_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_arch_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_node_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_edge_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_walker_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_object_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_ability_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_edge_op_ref(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_edge_to(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_edge_from(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_edge_any(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_connect_op(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_connect_to(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_connect_from(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_connect_any(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_filter_ctx(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_spawn_ctx(self: "AstBuildPass", node: ast.AstNode) -> None:
    # def exit_filter_compare_list(self: "AstBuildPass", node: ast.AstNode) -> None:


def replace_node(node: ast.AstNode, new_node: ast.AstNode) -> None:
    """Replace node with new_node."""
    node.parent.kid[node.parent.kid.index(node)] = new_node
    return new_node


def update_kind(node: ast.AstNode, kind: Type[ast.AstNode], **kwargs: dict) -> None:
    """Update node kind."""
    new_node = kind(**kwargs, parent=node.parent, kid=node.kid, line=node.line)
    node.parent.kid[node.parent.kid.index(node)] = new_node
    return new_node

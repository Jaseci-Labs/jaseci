graph import {
    assembler --> compiler_annotations { assemble }
    assembler --> compiler_codegen { assemble }
    assembler --> compiler_defs { assemble }
    assembler --> compiler_emit { assemble }
    assembler --> product_compile { assemble }
    codegen_util --> compiler_annotations { expr_loc, nloc, no_loc, stmt_loc }
    codegen_util --> compiler_codegen { args_have_kw_defaults, ast_cmp_kind, ast_node_name, async_function_def_loc, binop_id, body_docstring, body_is_try_except_only, body_is_try_finally_only, call_effective_args, call_func_loc, class_effective_bases, class_effective_keywords, cmpop_filter_oparg, cmpop_oparg, comp_bound_names_from_target, comp_dict_map_loc, comp_leftmost_leaf, comp_name_bound, display_all_constant, display_const_items, display_has_starred, exec_tail_emits_code, expr_loc, fold_slice_const, function_argcounts, function_code_flags, function_def_loc, import_bind_name, inplace_binop_id, is_seq_literal, loop_body_has_break, match_pattern_loc, match_pattern_unwrap_or, match_pattern_wildcard, nloc, seq_target_elts, starred_target_index, stmt_loc, top_loc, try_fold_binop, try_handler_span, unary_opcode }
    codegen_util --> compiler_defs { async_function_def_loc, body_docstring, class_effective_bases, class_effective_keywords, exec_tail_emits_code, expr_loc, function_argcounts, function_code_flags, function_def_loc, import_bind_name, nested_code_qualname, nloc, stmt_loc }
    codegen_util --> compiler_emit { args_have_kw_defaults, ast_cmp_kind, ast_node_name, async_function_def_loc, binop_id, body_is_try_except_only, body_is_try_finally_only, call_effective_args, call_effective_keywords, call_func_loc, class_effective_bases, class_effective_keywords, cmpop_filter_oparg, cmpop_oparg, comp_bound_names_from_target, comp_dict_map_loc, comp_leftmost_leaf, comp_name_bound, display_all_constant, display_const_items, display_has_starred, exec_tail_emits_code, expr_loc, fold_default_leaf_values, fold_slice_const, function_argcounts, function_code_flags, function_def_loc, import_bind_name, inplace_binop_id, is_seq_literal, loop_body_has_break, match_pattern_loc, match_pattern_unwrap_or, match_pattern_wildcard, nested_code_qualname, nloc, seq_target_elts, starred_target_index, stmt_loc, top_loc, try_fold_binop, try_handler_span, unary_opcode }
    codegen_util --> compiler_exc { body_is_try_except_only, body_is_try_finally_only, exec_tail_emits_code, expr_loc, nloc, stmt_loc, try_handler_span }
    codegen_util --> compiler_loops { exec_tail_emits_code, expr_loc, loop_body_has_break, loop_body_has_try, nloc }
    codegen_util --> compiler_match { exec_tail_emits_code, expr_loc, match_pattern_loc, match_pattern_unwrap_or, match_pattern_wildcard, nloc, stmt_loc }
    compiler_annotations --> compiler_codegen { ann_scope_plan, collect_ann_plan, emit_module_annotation_setup, finish_module_annotations, visit_ann_assign }
    compiler_annotations --> compiler_defs { collect_ann_plan_class, emit_class_annotation_setup, emit_future_function_annotations, finish_class_annotations }
    compiler_annotations --> compiler_exc { ann_scope_plan }
    compiler_annotations --> compiler_loops { ann_scope_plan }
    compiler_annotations --> compiler_match { ann_scope_plan }
    compiler_codegen --> compiler_annotations.ann_store_target_tos { visit_store_target_tos }
    compiler_codegen --> compiler_defs { emit_name_store, visit_stmt }
    compiler_codegen --> compiler_emit.emit_comprehension_loop { visit_store_target_tos }
    compiler_codegen --> compiler_exc { emit_module_return, emit_name_delete, emit_name_store, emit_unit_loop_exit_epilogue, visit_return_stmt, visit_stmt_tail, visit_stmts, visit_store_target_tos }
    compiler_codegen --> compiler_loops { emit_module_return, emit_tail_and_finish, visit_stmt_tail, visit_stmts, visit_store_target_tos }
    compiler_codegen --> compiler_match { emit_module_return, emit_name_store, visit_stmt_tail, visit_stmts }
    compiler_codegen --> product_compile { compile_eval, compile_exec }
    compiler_context --> compiler_ir { compile_context }
    compiler_context --> product_compile { compile_context }
    compiler_defs as dispatch_defs --> compiler_codegen.visit_stmt;
    compiler_emit --> compiler_annotations { cellvars_from_sym, codegen_busy, codegen_fail, codegen_mangle, fast_local_index, fast_varnames_from_sym, freevars_from_sym, localsplus_index, localsplus_index_u, visit_expr, visit_subscript_index }
    compiler_emit --> compiler_codegen { cellvars_from_sym, codegen_busy, codegen_fail, codegen_mangle, comp_append_handler, comp_emit_bind_target, comp_emit_cleanup, comp_emit_filters, comp_emit_setup, comp_emit_single_elt, comp_finish_loop, comp_lead_loopvar_slot, comp_name_fast_index, comp_target_slots, compile_lambda_cfg, emit_anext_send_loop_footer, emit_anext_send_loop_header, emit_await_send_except_regions, emit_await_send_loop_footer, emit_await_send_loop_header, emit_branch_if_test_false, emit_branch_if_test_true, emit_cmp_link, emit_control_unwind, emit_folded_int, emit_function_defaults, emit_function_kwdefaults, emit_function_prologue, emit_generator_except_handler, emit_make_function_with_closure, emit_name_load, emit_return_unwind, emit_send_delegation_loop, emit_slice_bound, emit_slice_load, emit_starred_list_build, emit_suspendable_prologue, fast_local_index, fast_varnames_from_sym, finish_control_unwind, flush_pending_await_footers, freevars_from_sym, is_none_identity_test, localsplus_index, localsplus_index_u, name_load_opcode, register_int_literal_const, try_emit_fast_local_pair_load, unit_fail, varname_index, visit_boolop, visit_comp_dict_kv, visit_comp_elt, visit_compare, visit_dict_comp, visit_expr, visit_lambda, visit_list_comp, visit_set_comp, visit_subscript_index, visit_test_expr }
    compiler_emit --> compiler_defs { call_has_unpacking, cellvars_from_sym, codegen_busy, codegen_fail, codegen_mangle, emit_call_ex_positional, emit_call_instruction, emit_call_keyword_values, emit_folded_int, emit_function_defaults, emit_function_kwdefaults, emit_function_prologue, emit_generator_except_handler, emit_local_or_cell_store, emit_make_function_with_closure, emit_name_load, fast_local_index, fast_varnames_from_sym, flush_pending_await_footers, freevars_from_sym, inline_storage_names, localsplus_index, localsplus_index_u, visit_expr }
    compiler_emit --> compiler_exc { anext_send_loop, await_send_loop, codegen_busy, codegen_fail, emit_await_send_except_regions, emit_await_send_loop_footer, emit_await_send_loop_header, emit_return_unwind, emit_send_delegation_loop, visit_expr }
    compiler_emit --> compiler_loops { codegen_busy, codegen_fail, emit_anext_send_loop_footer, emit_anext_send_loop_header, emit_branch_if_test_false, emit_branch_if_test_true, emit_send_delegation_loop, visit_expr, visit_test_expr }
    compiler_emit --> compiler_match { codegen_busy, codegen_fail, codegen_mangle, emit_branch_if_test_false, fast_local_index, visit_expr, visit_test_expr }
    compiler_exc as dispatch_exc --> compiler_codegen.finish_source_scope;
    compiler_exc as dispatch_exc --> compiler_codegen.visit_stmt;
    compiler_exc --> compiler_defs { emit_deferred_comp_handlers }
    compiler_exc as dispatch_exc --> compiler_emit.compile_genexp_cfg;
    compiler_exc as dispatch_exc --> compiler_emit.compile_lambda_cfg;
    compiler_exc as dispatch_exc --> compiler_emit.emit_control_unwind;
    compiler_exc --> compiler_loops { emit_anext_send_except_regions }
    compiler_exc as dispatch_exc --> compiler_loops.visit_async_for;
    compiler_exc as dispatch_exc --> compiler_loops.visit_for;
    compiler_exc as dispatch_exc --> compiler_loops.visit_if;
    compiler_exc as dispatch_exc --> compiler_loops.visit_while;
    compiler_ir --> assembler { NO_LINE, cinstr, cloc, except_region, instr_size_codeunits, loc, same_loc }
    compiler_ir --> codegen_util { basicblock, cfg_builder, cinstr, cloc, comp_handler, except_region, loc, loop_frame, mk_instr, mk_jump, new_cfg_builder, no_loc, stmt_cont, unverified_cfg }
    compiler_ir --> compiler_annotations { basicblock, cfg_builder, cinstr, cloc, loc, new_cfg_builder, stmt_cont, unverified_cfg }
    compiler_ir --> compiler_codegen { basicblock, break_site, cfg_builder, cinstr, cloc, comp_handler, control_unwind, except_region, loc, loop_frame, mk_instr, mk_jump, new_cfg_builder, no_loc, stmt_cont, unverified_cfg }
    compiler_ir --> compiler_defs { cfg_builder, cloc, loc, new_cfg_builder, no_loc, stmt_cont, unverified_cfg }
    compiler_ir --> compiler_emit { await_footer_job, basicblock, cfg_builder, cinstr, cleanup_frame, cloc, comp_handler, control_unwind, except_region, loc, loop_frame, mk_instr, mk_jump, new_cfg_builder, no_loc, stmt_cont, try_await_frame, unverified_cfg, with_unwind_rec }
    compiler_ir --> compiler_exc { await_footer_job, basicblock, cfg_builder, cleanup_frame, cloc, except_region, loc, no_loc, stmt_cont, try_await_frame, with_unwind_rec }
    compiler_ir --> compiler_loops { basicblock, break_site, cfg_builder, cinstr, cloc, except_region, loc, loop_frame, mk_instr, mk_jump, no_loc, same_loc, stmt_cont }
    compiler_ir --> compiler_match { basicblock, cfg_builder, cloc, loc, stmt_cont }
    compiler_ir --> flowgraph { basicblock, cinstr, except_region, instr_size_codeunits, mk_instr, unverified_cfg }
    compiler_loops as dispatch_loops --> compiler_codegen.visit_stmt;
    compiler_match as dispatch_match --> compiler_codegen.visit_stmt;
    flowgraph --> assembler { flatten_blocks, verified_cfg }
    flowgraph --> compiler_annotations { verify_cfg }
    flowgraph --> compiler_codegen { optimize_swap_range, verify_cfg }
    flowgraph --> compiler_defs { verify_cfg }
    flowgraph --> compiler_emit { build_layout_pos, layout_pos, optimize_swap_range, verify_cfg }
    flowgraph --> compiler_exc { build_layout_pos, layout_pos }
    flowgraph --> compiler_loops { MAX_COPY_SIZE, copy_cinstr }
    flowgraph --> compiler_match { optimize_swap_range }
    flowgraph --> product_compile { verify_cfg }
    product_compile --> native_api { compile_ast, compile_source, prepare_ast_output }
}

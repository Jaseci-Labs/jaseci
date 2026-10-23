import from .sql_cases { SQLTests, run_case }

test "SQLite: module is portable as one file" {
    run_case(SQLTests("test_module_is_portable_as_one_file"));
}

test "SQLite: select parameters and order" {
    run_case(SQLTests("test_select_parameters_and_order"));
}

test "SQLite: join and shared parameter" {
    run_case(SQLTests("test_join_and_shared_parameter"));
}

test "SQLite: group by count" {
    run_case(SQLTests("test_group_by_count"));
}

test "SQLite: aggregate empty is one row" {
    run_case(SQLTests("test_aggregate_empty_is_one_row"));
}

test "SQLite: scalar optional empty yields null" {
    run_case(SQLTests("test_scalar_optional_empty_yields_null"));
}

test "SQLite: scalar requires proof and one column" {
    run_case(SQLTests("test_scalar_requires_proof_and_one_column"));
}

test "SQLite: correlated exists" {
    run_case(SQLTests("test_correlated_exists"));
}

test "SQLite: derived schema and scope" {
    run_case(SQLTests("test_derived_schema_and_scope"));
}

test "SQLite: union schema and arm limits" {
    run_case(SQLTests("test_union_schema_and_arm_limits"));
}

test "SQLite: cte" {
    run_case(SQLTests("test_cte"));
}

test "SQLite: recursive cte" {
    run_case(SQLTests("test_recursive_cte"));
}

test "SQLite: cte forward reference and recursive anchor rejected" {
    run_case(SQLTests("test_cte_forward_reference_and_recursive_anchor_rejected"));
}

test "SQLite: recursive step eligibility" {
    run_case(SQLTests("test_recursive_step_eligibility"));
}

test "SQLite: nullable three valued predicate" {
    run_case(SQLTests("test_nullable_three_valued_predicate"));
}

test "SQLite: parameter value type and bounds" {
    run_case(SQLTests("test_parameter_value_type_and_bounds"));
}

test "SQLite: injection is bound and identifiers are quoted" {
    run_case(SQLTests("test_injection_is_bound_and_identifiers_are_quoted"));
}

test "SQLite: wrong expression categories and types" {
    run_case(SQLTests("test_wrong_expression_categories_and_types"));
}

test "SQLite: alias and join scopes" {
    run_case(SQLTests("test_alias_and_join_scopes"));
}

test "SQLite: aggregate validation" {
    run_case(SQLTests("test_aggregate_validation"));
}

test "SQLite: mutated ast is revalidated" {
    run_case(SQLTests("test_mutated_ast_is_revalidated"));
}

test "SQLite: source field schema validation" {
    run_case(SQLTests("test_source_field_schema_validation"));
}

test "SQLite: projection expression type swap rejected" {
    run_case(SQLTests("test_projection_expression_type_swap_rejected"));
}

test "SQLite: projection derived arithmetic rejected" {
    run_case(SQLTests("test_projection_derived_arithmetic_rejected"));
}

test "SQLite: projection nullability swap rejected" {
    run_case(SQLTests("test_projection_nullability_swap_rejected"));
}

test "SQLite: projection same type swap allowed" {
    run_case(SQLTests("test_projection_same_type_swap_allowed"));
}

test "SQLite: recursive anchor clauses limit" {
    run_case(SQLTests("test_recursive_anchor_limit"));
}

test "SQLite: recursive anchor clauses order" {
    run_case(SQLTests("test_recursive_anchor_order"));
}

test "SQLite: recursive anchor clauses order and limit" {
    run_case(SQLTests("test_recursive_anchor_order_limit"));
}

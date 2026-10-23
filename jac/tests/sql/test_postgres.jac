"""Run the same behavioral cases on an explicitly supplied disposable PostgreSQL.

JAC_SQL_PG_SOCKET=/path/to/.s.PGSQL.PORT jac test jac/tests/sql/test_postgres.jac
"""
import os;
import unittest;
import jaclang.sql as sql;
glob s: any = sql;
import from .sql_cases { SQLTests, run_case }
class Rows {
    def init(self: Rows, values: any) -> object {
        self.values = values;
    }

    def fetchall(self: Rows) -> object {
        return self.values;
    }

    def fetchone(self: Rows) -> object {
        return self.values[0] if self.values else None;
    }
}

class Database {
    def init(self: Database) -> object {
        import from jaclang.data.pgwire { PgWireConnection }
        self.connection = PgWireConnection(
            user='sql_test',
            unix_sock=os.environ['JAC_SQL_PG_SOCKET'],
            database='postgres'
        );
        self.connection.run('BEGIN');
    }

    def execute(self: Database, sql: any, params: any = None) -> object {
        return Rows(self.connection.run(sql, **(params or {})));
    }

    def executescript(self: Database, script: any) -> object {
        for statement in script.split(';') {
            if statement.strip() {
                self.connection.run(statement);
            }
        }
    }

    def close(self: Database) -> object {
        try {
            self.connection.run('ROLLBACK');
        } finally {
            self.connection.close();
        }
    }
}

@unittest.skipUnless(
    os.environ.get('JAC_SQL_PG_SOCKET'), 'Set socket of a disposable SQL test cluster'
)
class PostgresTests(SQLTests) {
    def setUp(self: PostgresTests) -> object {
        self.id = s.field('id', s.int64_type());
        self.age = s.field('age', s.int64_type());
        self.name = s.field('name', s.text_type());
        self.people = s.table('people', [self.id, self.age, self.name], 'p');
        self.db = Database();
        self.addCleanup(self.db.close);
        self.db.executescript(
            'CREATE TEMP TABLE people(id BIGINT, age BIGINT, name TEXT);'
            "INSERT INTO people VALUES(1,20,'Ann'),(2,40,'Bob'),(3,40,'Cora');"
        );
    }
}


test "PostgreSQL: module is portable as one file" {
    run_case(PostgresTests("test_module_is_portable_as_one_file"));
}

test "PostgreSQL: select parameters and order" {
    run_case(PostgresTests("test_select_parameters_and_order"));
}

test "PostgreSQL: join and shared parameter" {
    run_case(PostgresTests("test_join_and_shared_parameter"));
}

test "PostgreSQL: group by count" {
    run_case(PostgresTests("test_group_by_count"));
}

test "PostgreSQL: aggregate empty is one row" {
    run_case(PostgresTests("test_aggregate_empty_is_one_row"));
}

test "PostgreSQL: scalar optional empty yields null" {
    run_case(PostgresTests("test_scalar_optional_empty_yields_null"));
}

test "PostgreSQL: scalar requires proof and one column" {
    run_case(PostgresTests("test_scalar_requires_proof_and_one_column"));
}

test "PostgreSQL: correlated exists" {
    run_case(PostgresTests("test_correlated_exists"));
}

test "PostgreSQL: derived schema and scope" {
    run_case(PostgresTests("test_derived_schema_and_scope"));
}

test "PostgreSQL: union schema and arm limits" {
    run_case(PostgresTests("test_union_schema_and_arm_limits"));
}

test "PostgreSQL: cte" {
    run_case(PostgresTests("test_cte"));
}

test "PostgreSQL: recursive cte" {
    run_case(PostgresTests("test_recursive_cte"));
}

test "PostgreSQL: cte forward reference and recursive anchor rejected" {
    run_case(PostgresTests("test_cte_forward_reference_and_recursive_anchor_rejected"));
}

test "PostgreSQL: recursive step eligibility" {
    run_case(PostgresTests("test_recursive_step_eligibility"));
}

test "PostgreSQL: nullable three valued predicate" {
    run_case(PostgresTests("test_nullable_three_valued_predicate"));
}

test "PostgreSQL: parameter value type and bounds" {
    run_case(PostgresTests("test_parameter_value_type_and_bounds"));
}

test "PostgreSQL: injection is bound and identifiers are quoted" {
    run_case(PostgresTests("test_injection_is_bound_and_identifiers_are_quoted"));
}

test "PostgreSQL: wrong expression categories and types" {
    run_case(PostgresTests("test_wrong_expression_categories_and_types"));
}

test "PostgreSQL: alias and join scopes" {
    run_case(PostgresTests("test_alias_and_join_scopes"));
}

test "PostgreSQL: aggregate validation" {
    run_case(PostgresTests("test_aggregate_validation"));
}

test "PostgreSQL: mutated ast is revalidated" {
    run_case(PostgresTests("test_mutated_ast_is_revalidated"));
}

test "PostgreSQL: source field schema validation" {
    run_case(PostgresTests("test_source_field_schema_validation"));
}

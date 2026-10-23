# Typed SQL prototype

Based on Jaseci-Labs/jaseci main `2a462fa254582478b14958f609ce218fc33a17e4`.
Development branch: `feat/typed-sql`. Implementation:
[`jac/jaclang/sql.jac`](../../../jac/jaclang/sql.jac).

The module builds SQL as structured values and validates it before rendering.
Implementation and tests use Jac; the test entry point is `jac test`.
It has one source file, one standard-library import (`uuid`) and no dependencies
on graph types, TTG, storage tables, drivers or project configuration. Forks can
copy the file and its tests, or cherry-pick the scoped commit. A portability test
copies the module to a temporary directory under a different module name and
executes a generated query. Jac itself remains the required language runtime.

## Semantic categories

| Category | Meaning | Implementation |
| --- | --- | --- |
| `ScalarExpr[T]` | One SQL value of type T | Typed wrapper over expression AST |
| `Relation[R, C]` | Rows with schema R and cardinality proof C | SELECT, UNION ALL, WITH |
| `Source` | A bound table, derived relation or CTE reference | Owns schema and alias |
| `Command` | Separate category for future data-changing statements | Category marker |

**SELECT is a relational expression.** `compile_sql` consumes a relation;
`named` projects scalar expressions. Conversion to a scalar subquery is explicit.
Current row shape is carried as a checked `Schema`; typed `Field[T]` keys carry
column types. The prototype does not synthesize a static record type from runtime
field names. Field existence and whole-query constraints are validated before SQL.

SQL types: Bool, Int64, Float64, Text, UUID and Nullable[T]. Type tokens and field
keys use generic marker types; data types are checked again during rendering.
The marker parameters are intentionally phantom, which the current all-rules
Jac lint configuration reports as unused-type-parameter warnings.

## Construction example

See [the runnable Jac example](../../../jac/examples/sql/typed_sql.jac).

```jac
import from jaclang.sql {
    field, int64_type, text_type, table, named, select_, gt, int64, compile_sql
}
with entry {
    name = field("name", text_type());
    age = field("age", int64_type());
    people = table("people", [name, age], "p");
    query = select_(
        [named("name", people.col(name))],
        source=people,
        where=gt(people.col(age), int64(30))
    );
    compiled = compile_sql(query);
    print(compiled.sql);
    print(compiled.params);
}
```

Representative PostgreSQL output:

```sql
SELECT "p"."name" AS "name"
FROM "people" AS "p"
WHERE ("p"."age" > CAST(:p0 AS bigint))
```

Parameters: `{"p0": 30}`. Identifiers are quoted independently from data binding.
Repeated use of the same parameter node reuses its binding; independent nodes
with equal values retain independent bindings. Named placeholders match the
existing Jac PG wire adapter. Explicit parameter casts preserve SQL types even
where PostgreSQL has no contextual type inference, including recursive anchors.

## What is statically checked

Actual negative Jac fixtures test rejection of:

- Text/Bool passed to Int64 addition, including a typed text-column lookup.
- Relation passed as a scalar projection, or scalar/command passed as a relation.
- Int64 used as WHERE's predicate.
- A Many relation passed to `scalar` or `scalar_one`.
- Incompatible types passed to equality.
- Scalar expressions passed directly in a projection list.

`test_types.jac` checks the positive module/example and asserts E1053 diagnostics
at all 11 expected invalid-call lines. Runtime/AST validation covers dynamic
schema information and callers from Python or gradual typing.

## Whole-query validation

The renderer checks each projection field against its expression type, including
nullability, in addition to comparing the declared row schema with those fields.
This rejects stale schema metadata after expression replacement, including inside
derived relations, before SQL is returned. It also validates bound column
sources and field types, sequential JOIN
visibility, alias collisions/shadowing, CTE visibility/order, compatible UNION/CTE
schemas, aggregate placement, nested aggregates, GROUP BY coverage and cardinality
proofs. Raw AST nodes are revalidated on every compile, so post-construction
mutation cannot silently invalidate a row-count proof or parameter type.

The initial grouping fragment accepts column expressions as group keys. Aggregates
are COUNT(*) returning non-null Int64 and SUM(Float64) returning nullable Float64.
SQL SUM(Int64) returns numeric in PostgreSQL and needs a future SqlNumeric type.
Addition currently operates on non-null Int64; SQL overflow retains database error
semantics. Schema descriptions are contracts supplied by the caller; matching them
to the physical database schema is the integrating application's responsibility.

`scalar(query, field)` accepts a proven AtMostOne or ExactlyOne single-column
relation and returns Nullable[T], because zero rows yields NULL. `limit_one`
constructs the AtMostOne proof with an actual LIMIT 1. `aggregate` constructs an
ExactlyOne proof, verified as an ungrouped aggregate without HAVING/LIMIT.
`scalar_one` preserves the output type of that proven one-row result. Plain
SELECT carries the conservative Many marker even for a literal projection.

NULL equality has a separate `eq_nullable` constructor returning Nullable[Bool].
WHERE accepts Bool or Nullable[Bool], retaining SQL's three-valued semantics.
COALESCE removes nullability with a checked non-null fallback; CAST retains source
nullability. Generic `param(type_token, value)` checks host value types and signed
Int64 range at construction; convenience factories have narrower Jac signatures.

## CTEs and recursion

`cte` declares output fields and an alias; `bind_cte` checks the body schema;
`with_ctes` establishes lexical scope. Recursive form is a SELECT anchor UNION ALL
SELECT step, with exactly one direct self-reference in the step. The initial step
fragment supports direct sources, predicates and scalar arithmetic. Aggregates,
subqueries, grouping and step-local ORDER/LIMIT are rejected with SqlError. This
makes the initial supported PostgreSQL recursive fragment explicit.

The anchor renders as `SELECT * FROM (anchor) AS "_recursive_anchor"` before
UNION ALL. This parenthesized subquery keeps anchor-local ORDER BY and LIMIT
inside the anchor while leaving the recursive step as a direct SELECT. Tests
execute LIMIT, ORDER BY, and their combination on PostgreSQL and SQLite.

CTE references are identities, not string interpolation. Forward references,
recursive anchor self-references and direct cyclic AST object graphs are rejected.
Recursive termination is defined by the query predicate, as with PostgreSQL itself.

## Extension path

1. Add structural nodes and validation for LEFT/LATERAL joins, CASE, arrays,
   table functions/ordinality and window expressions needed by TTG.
2. Add richer numeric/coercion rules and typed DML commands.
3. Migrate one existing sqlcompile or TTG hop emitter without changing its behavior.
4. Expand to recursive/budget query fragments while comparing results and plans.

A new construct should define its input/output SQL types, scope behavior and
rendering; include positive execution and rejection tests. The SQL AST is separate
from future graph analysis, logical optimization and cost-based planning.

## Verification

Run the Jac test files from the repository root:

```sh
jac test jac/tests/sql/test_sql.jac jac/tests/sql/test_types.jac -j 1 -v
jac check jac/jaclang/sql.jac jac/examples/sql/typed_sql.jac
jac run jac/examples/sql/typed_sql.jac
```

PostgreSQL tests use the same behavioral cases and an explicitly supplied disposable
cluster socket. They create transaction-local test tables and roll back each case:

```sh
JAC_SQL_PG_SOCKET=/path/to/.s.PGSQL.PORT \
  jac test jac/tests/sql/test_postgres.jac -j 1 -v
```

There are 60 native Jac test entries: 29 SQLite, the same 29 PostgreSQL cases,
and two static-check tests. Shared fixtures live in `sql_cases.jac` and use
standard-library assertion helpers.

The test account is `sql_test`, database `postgres`. Set up a dedicated cluster
with trust auth for local tests. SQL construction itself opens no connections.
Recorded commands, versions, test counts and source hashes accompany the validated
checkpoint under `validation/`.

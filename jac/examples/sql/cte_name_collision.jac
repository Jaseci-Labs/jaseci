"""Object-referenced CTEs preserve physical table reads.

Run with JAC_SQL_PG_SOCKET pointing to a disposable PostgreSQL test cluster.
The fixture is rolled back at exit.
"""
import os;
import from jaclang.data.pgwire { PgWireConnection }
import from jaclang.sql {
    Relation,
    field,
    int64_type,
    text_type,
    table,
    named,
    select,
    gt,
    int64,
    asc,
    cte,
    exists,
    compile_sql
}

def show[R, C](
    label: str, query: Relation[R, C], db: PgWireConnection
) -> list[tuple[any, ...]] {
    compiled = compile_sql(query);
    rows = db.run(compiled.sql, **compiled.params);
    print(label);
    print(compiled.sql);
    print(rows);
    return rows;
}

with entry {
    socket_path = os.environ.get('JAC_SQL_PG_SOCKET');
    if not socket_path {
        raise ValueError('Set JAC_SQL_PG_SOCKET to a disposable cluster socket');
    }
    db = PgWireConnection(user='sql_test', unix_sock=socket_path, database='postgres');
    db.run('BEGIN');
    try {
        db.run('CREATE TEMP TABLE people (id BIGINT, name TEXT, age BIGINT)');
        db.run("INSERT INTO people VALUES (1, 'Ann', 20), (2, 'Bob', 40)");
        person_id = field('id', int64_type());
        person_name = field('name', text_type());
        age = field('age', int64_type());
        people = table('people', [person_id, person_name, age]);
        kids = cte(
            select(
                [
                    named('id', people.col(person_id)),
                    named('name', people.col(person_name))
                ],
                source=people,
                where=gt(int64(30), people.col(age))
            )
        );
        requested = table('people', [person_id, person_name]);
        all_people = select(
            [named('name', requested.col(person_name))],
            source=requested,
            order_by=[asc(requested.col(person_id))]
        );
        assert show('A. Physical table', all_people, db) == [('Ann', ), ('Bob', )];
        kids_names = select([named('name', kids.col(person_name))], source=kids);
        assert show('B. CTE object', kids_names, db) == [('Ann', )];
        # Referencing kids in a nested query automatically includes its CTE definition.
        all_with_kids = select(
            [named('name', requested.col(person_name))],
            source=requested,
            where=exists(kids_names),
            order_by=[asc(requested.col(person_id))]
        );
        assert show('C. Physical table with referenced CTE', all_with_kids, db)
            == [('Ann', ), ('Bob', )];
    } finally {
        try {
            db.run('ROLLBACK');
        } finally {
            db.close();
        }
    }
}

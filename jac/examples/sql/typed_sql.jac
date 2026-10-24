"""Build a typed query; construction performs no database I/O."""
import from jaclang.sql {
    field,
    int64_type,
    text_type,
    table,
    named,
    select,
    gt,
    int64,
    inner_join,
    eq,
    desc,
    compile_sql,
    aggregate,
    count,
    scalar_one,
    cte
}

with entry {
    person_id = field('id', int64_type());
    person_name = field('name', text_type());
    person_age = field('age', int64_type());
    people = table('people', [person_id, person_name, person_age]);
    owner = field('owner_id', int64_type());
    pets = table('pets', [owner]);
    result = select(
        [named('name', people.col(person_name))],
        source=people,
        joins=[inner_join(pets, eq(people.col(person_id), pets.col(owner)))],
        where=gt(people.col(person_age), int64(30)),
        order_by=[desc(people.col(person_age))]
    );
    compiled = compile_sql(result);
    print(compiled.sql);
    print(compiled.params);
    total = named('total', count());
    total_query = aggregate([total], source=people);
    scalar_total = scalar_one(total_query, total.key());
    print(compile_sql(select([named('total', scalar_total)])).sql);
    adults = cte(
        select(
            [
                named('id', people.col(person_id)),
                named('name', people.col(person_name))
            ],
            source=people,
            where=gt(people.col(person_age), int64(30))
        )
    );
    names = select([named('name', adults.col(person_name))], source=adults);
    print(compile_sql(names).sql);
}

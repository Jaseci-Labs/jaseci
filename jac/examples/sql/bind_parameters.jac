"""Compile once; retain SQL and parameter metadata, then bind new values."""
import jaclang.sql as s;

with entry {
    age = s.field('age', s.int64_type());
    name = s.field('name', s.text_type());
    people = s.table('people', [age, name]);
    compiled = s.compile_sql(
        s.select(
            [s.named('name', people.col(name))],
            source=people,
            where=s.gt(people.col(age), s.slot('min_age', s.int64_type()))
        )
    );
    first = compiled.bind({'min_age': 18});
    second = compiled.bind({'min_age': 30});
    print(first.sql);
    print(first.params);
    print(second.params);
    # Pass each result's sql and params to the database driver.
}

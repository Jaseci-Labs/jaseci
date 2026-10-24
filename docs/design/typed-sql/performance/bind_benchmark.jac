"""Compare client-side rebuilding with binding an already compiled query."""
import jaclang.sql as s;
import json;
import from pathlib { Path }
import from time { perf_counter_ns }

with entry {
    age = s.field('age', s.int64_type());
    people = s.table('people', [age]);
    compiled = s.compile_sql(
        s.select(
            [s.named('age', people.col(age))],
            source=people,
            where=s.gt(people.col(age), s.slot('min_age', s.int64_type()))
        )
    );
    results: list[dict[str, float]] = [];
    for round_idx in range(8) {
        start = perf_counter_ns();
        for idx in range(500) {
            result = s.compile_sql(
                s.select(
                    [s.named('age', people.col(age))],
                    source=people,
                    where=s.gt(people.col(age), s.int64(idx))
                )
            );
        }
        rebuild_us = (perf_counter_ns() - start) / 500 / 1000;
        start = perf_counter_ns();
        for idx in range(10000) {
            result = compiled.bind({'min_age': idx});
        }
        bind_us = (perf_counter_ns() - start) / 10000 / 1000;
        if round_idx > 0 {
            results.append({'rebuild_us': rebuild_us, 'bind_us': bind_us});
        }
    }
    Path('docs/design/typed-sql/performance/bind-samples.json').write_text(
        json.dumps(results, indent=2)
    );
    print(results);
}

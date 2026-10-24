import from jaclang.sql {
    field,
    int64_type,
    nullable,
    select,
    named,
    int64,
    boolean,
    values,
    optional_source,
    left_join,
    compare_nullable,
    asc,
    array_param,
    unnest,
    sum_int64,
    over,
    rows_between,
    unbounded_preceding,
    preceding,
    coalesce,
    numeric,
    cte,
    cte_ref,
    define_cte,
    with_ctes,
    union_all,
    add,
    lt,
    compile_sql,
    case_nullable,
    is_not_null
}

with entry {
    id = field('id', int64_type());
    owner = field('owner', int64_type());
    nullable_owner = field('owner', nullable(int64_type()));
    people = values([id], [[int64(1)], [int64(2)]]).as_source();
    pets = optional_source(values([owner], [[int64(1)]]).as_source());
    joined = select(
        [
            named('id', people.col(id)),
            named(
                'owner',
                case_nullable(
                    [(is_not_null(pets.col(nullable_owner)), people.col(id))],
                    pets.col(nullable_owner)
                )
            )
        ],
        source=people,
        joins=[
            left_join(pets, compare_nullable(people.col(id), pets.col(nullable_owner)))
        ],
        order_by=[asc(people.col(id))]
    );
    print(compile_sql(joined).sql);

    ord = field('ord', int64_type());
    seeds = unnest(array_param(int64_type(), [1, 2, 3]), id, ord);
    prior = over(
        sum_int64(seeds.col(id)),
        order_by=[asc(seeds.col(ord))],
        frame=rows_between(unbounded_preceding(), preceding(1))
    );
    budget = select(
        [named('id', seeds.col(id)), named('prior', coalesce(prior, numeric(0)))],
        source=seeds,
        order_by=[asc(seeds.col(ord))]
    );
    print(compile_sql(budget).sql);

    walk = cte_ref([id]);
    frontier = cte(
        select(
            [named('id', walk.col(id))], source=walk, where=lt(walk.col(id), int64(4))
        ),
        materialized=True
    );
    step = with_ctes(
        select([named('id', add(frontier.col(id), int64(1)))], source=frontier),
        [frontier]
    );
    define_cte(walk, union_all(select([named('id', int64(1))]), step), recursive=True);
    result = select(
        [named('id', walk.col(id))], source=walk, order_by=[asc(walk.col(id))]
    );
    print(compile_sql(result).sql);
}

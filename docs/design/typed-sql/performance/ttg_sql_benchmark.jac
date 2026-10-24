"""Compare old SQL strings and typed AST construction on the same database."""
import os;
import json;
import from time { perf_counter_ns }
import from statistics { median }
import from tempfile { TemporaryDirectory }
import from pathlib { Path }
import from unittest.mock { patch }
import from jaclang.runtime.runtime { JacRuntime }
import from jaclang.runtime.ttg_sql { compile_specialized, compile_layered }
import from .test_topology_index { _ctx, _seed_overlap_budget, _sql_comparison_specs }
import from .fixtures.ttg_sql_legacy {
    _ttg_render_specialized_set_based_sql as legacy_specialized,
    layered_sql as legacy_layered
}

test "TTG SQL performance measurements" {
    measurements: list[dict] = [];
    with TemporaryDirectory() as td {
        previous = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            (alice, bobs, shared, tweets) = _seed_overlap_budget(ctx);
            ctx.mem.commit();
            store = ctx.mem.store;
            assert store is not None;
            origins = [alice, bobs[0]];
            with patch.dict(
                os.environ,
                {'JAC_TTG_PREFETCH_OWNER_ROOTS': '0', 'JAC_TTG_OPT_COMPLETE_HOPS': '1'}
            ) {
                for (case_idx, specs) in enumerate(_sql_comparison_specs()) {
                    for mode in ['specialized', 'layered'] {
                        queries: dict = {};
                        for version in ['legacy', 'ast'] {
                            samples: list[float] = [];
                            for iteration in range(55) {
                                start = perf_counter_ns();
                                if mode == 'specialized' {
                                    if version == 'legacy' {
                                        params: dict = {
                                            'origin_ids': [str(x) for x in origins],
                                            'limit': 12,
                                            'max_depth': 12
                                        };
                                        sql = legacy_specialized(specs, params);
                                    } else {
                                        compiled = compile_specialized(
                                            specs, origins, 12, 12
                                        );
                                        sql = compiled.sql;
                                        params = compiled.params;
                                    }
                                } else {
                                    if version == 'legacy' {
                                        (sql, params) = legacy_layered(
                                            specs, 12, False
                                        );
                                        params.update(
                                            {
                                                'frontier_ids': [
                                                    str(x) for x in origins
                                                ],
                                                'seen_ids': [
                                                    '00000000-0000-0000-0000-000000000000'
                                                ],
                                                'seen_count': 0,
                                                'limit': 12
                                            }
                                        );
                                    } else {
                                        compiled = compile_layered(
                                            specs, origins, [], 12, False
                                        );
                                        sql = compiled.sql;
                                        params = compiled.params;
                                    }
                                }
                                elapsed = (perf_counter_ns() - start) / 1000000;
                                if iteration >= 5 {
                                    samples.append(elapsed);
                                }
                            }
                            queries[version] = (sql, params);
                            measurements.append(
                                {
                                    'case': case_idx,
                                    'mode': mode,
                                    'version': version,
                                    'metric': 'build_ms',
                                    'samples': samples
                                }
                            );
                        }
                        assert store.rows(queries['legacy'][0], queries['legacy'][1])
                            == store.rows(queries['ast'][0], queries['ast'][1]);
                        timings: dict = {'legacy': [], 'ast': []};
                        for iteration in range(35) {
                            order = ['legacy', 'ast']
                                if iteration % 2 == 0
                                else ['ast', 'legacy'];
                            for version in order {
                                (sql, params) = queries[version];
                                start = perf_counter_ns();
                                rows = store.rows(sql, params);
                                elapsed = (perf_counter_ns() - start) / 1000000;
                                if iteration >= 5 {
                                    timings[version].append(elapsed);
                                }
                            }
                        }
                        for version in ['legacy', 'ast'] {
                            measurements.append(
                                {
                                    'case': case_idx,
                                    'mode': mode,
                                    'version': version,
                                    'metric': 'db_call_ms',
                                    'samples': timings[version]
                                }
                            );
                            print(
                                case_idx,
                                mode,
                                version,
                                'DB median ms',
                                median(timings[version])
                            );
                        }
                        for version in ['legacy', 'ast'] {
                            (sql, params) = queries[version];
                            plans = store.rows(
                                'EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) ' + sql, params
                            );
                            measurements.append(
                                {
                                    'case': case_idx,
                                    'mode': mode,
                                    'version': version,
                                    'metric': 'explain',
                                    'plan': plans
                                }
                            );
                        }
                        Path('benchmarks/ttg-sql/results.json').write_text(
                            json.dumps(measurements, indent=2, `default=str)
                        );
                    }
                }
            }
        } finally {
            JacRuntime.exec_ctx = previous;
            ctx.close();
        }
    }
}

import cProfile;
import pstats;
import io;
import from uuid { UUID }

test "TTG SQL construction profile" {
    profiler = cProfile.Profile();
    specs = _sql_comparison_specs()[3];
    origins = [UUID('00000000-0000-0000-0000-000000000001')];
    profiler.enable();
    for idx in range(20) {
        compile_specialized(specs, origins, 12, 12);
        compile_layered(specs, origins, [], 12, False);
    }
    profiler.disable();
    output = io.StringIO();
    stats_factory: any = pstats.Stats;
    stats_factory(profiler, stream=output).strip_dirs().sort_stats(
        'cumulative'
    ).print_stats(
        35
    );
    Path('benchmarks/ttg-sql/construction-profile.txt').write_text(output.getvalue());
}

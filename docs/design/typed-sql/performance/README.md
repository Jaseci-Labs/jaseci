# Scope-aware SQL validation caches

Measured 2026-10-24, Jac 0.36.1 / CPython 3.14.6 on the TTG port. Baseline SQL implementation corresponds to `d81664d57` with the existing Jac 0.36 syntax adaptations. The cached version applies the SQL cache changes to that same port. Compiler startup is excluded.

## Method

The TTG query adapter from `714e45988` builds six patterns through specialized and layered paths. Each query is rebuilt 55 times; the first five are warmups and the remaining 50 are timed. Parameters, query patterns and database fixture match the baseline. Each generated query is checked against the frozen legacy SQL result. The cache-correctness run additionally passes all 13 topology tests (including 145 query comparisons and 72 traversal comparisons).

Before and after are separate warm runs on the same machine, rather than paired samples in one process; differences include run-to-run noise. These are small-query construction measurements, not application throughput or database speedups.

## SQL construction time (median ms)

| Pattern | Path | Before | Cached | Reduction |
|---|---|---:|---:|---:|
| 0 | specialized | 15.528 | 10.362 | 33.3% |
| 1 | specialized | 15.515 | 10.277 | 33.8% |
| 2 | specialized | 16.087 | 11.054 | 31.3% |
| 3 | specialized | 16.500 | 10.870 | 34.1% |
| 4 | specialized | 17.996 | 11.775 | 34.6% |
| 5 | specialized | 16.239 | 11.077 | 31.8% |
| 0 | layered | 4.775 | 3.884 | 18.6% |
| 1 | layered | 4.776 | 3.815 | 20.1% |
| 2 | layered | 5.075 | 4.199 | 17.3% |
| 3 | layered | 4.849 | 3.885 | 19.9% |
| 4 | layered | 4.827 | 3.956 | 18.0% |
| 5 | layered | 5.057 | 4.232 | 16.3% |

## Profile evidence

For 20 specialized + 20 layered builds of pattern 3, total profiled calls fall from 5,152,321 to 3,465,661. Profiled wall time falls from 1.479 s to 1.080 s. Semantic analysis falls from 0.913 s to 0.700 s; schema derivation and immutable-value construction are reduced. Profiles add instrumentation overhead and cumulative times overlap. Raw profiles and uninstrumented construction samples are included.

## Implementation boundary

SELECT and set-operation schemas are derived lazily once on immutable nodes. The reserved internal cache cannot be assigned through the normal API. Analysis caches live on one validator and reset at every `analyze` call. Keys retain ordered source and CTE identities for each relevant scope. Failed validation results are not cached; cycle checks remain active. Query construction still runs for every request.

## Reproduce

Use the TTG checkout at `714e45988` with the SQL branch cache changes ported into its SQL module (retain its Jac 0.36 syntax adaptations). Copy `ttg_sql_benchmark.jac` from this directory to `jac/tests/runtimelib/bench_ttg_sql.jac` and create `benchmarks/ttg-sql/`. With the TTG Jac/PostgreSQL environment configured:

```sh
jac test jac/tests/runtimelib/bench_ttg_sql.jac --filter "SQL performance measurements" -v
jac test jac/tests/runtimelib/bench_ttg_sql.jac --filter "construction profile" -v
```

Run both commands before and after porting the cache changes, preserving the output files from each run. The benchmark writes raw timing samples and EXPLAIN plans under `benchmarks/ttg-sql/`. Source-only compatibility adaptations are described in the TTG migration document.

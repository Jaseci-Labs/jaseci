"""Kiwi differential oracle driver (LAYOUT-ENGINE-PLAN §8.2).

Reads JSONL batches on stdin, one solver scenario per line; writes one
JSON result line per batch on stdout. Imported and executed ONLY by
tests/oracle/test_constraints_oracle.py via `jac run`; never imported by
product or layout code.

Line protocol (schema 1):
  in : {"schema_version": 1, "seed": int, "vars": ["v0", ...],
        "ops": [{"op": "add",
                 "terms": [["v0", 2.0], ["v1", -1.0]],
                 "const": -4.0,
                 "rel": "eq" | "le" | "ge"}]}
  out: {"schema_version": 1, "seed": int,
        "ok": bool, "error": str, "values": {"v0": float, ...}}

Unknown schema versions abort before executing any batch. Stdlib
json/sys are the only non-constraints imports (process I/O for the
oracle boundary); no Kiwi, no ui.*, no app modules.
"""

import from .algebra {
    Constraint,
    Expression,
    Relation,
    StrengthTier,
    Term,
    Variable,
    add_expressions,
}
import from .results {
    SolveError,
}
import from .solver {
    Solver,
}
import from json {
    dumps,
    loads,
}
import from sys {
    stderr,
    stdin,
    stdout,
}


def _build_expression(terms: list[any], const: float) -> Expression {
    acc: Expression = Expression(constant=const);
    for pair in terms {
        plist: list[any] = pair as list[any];
        vid: int = int(plist[0] as int);
        coef: float = plist[1] as float;
        acc = add_expressions(
            acc,
            Expression(terms=[Term(variable=Variable(id=vid), coefficient=coef)]),
        );
    }
    return acc;
}


def _run_batch(batch: dict[str, any]) -> dict[str, any] {
    version = batch.get("schema_version");
    if version != 1 {
        return {
            "schema_version": -1,
            "seed": -1,
            "ok": False,
            "error": "unknown_schema_version",
            "values": {},
        };
    }
    seed = batch.get("seed", 0);
    s = Solver();
    # Variables are addressed by integer id directly (names map 1:1).
    rel_map = {
        "eq": Relation.EQ,
        "le": Relation.LEQ,
        "ge": Relation.GEQ,
    };
    ops_raw = batch.get("ops", []) as list[any];
    for op_any in ops_raw {
        op: dict[str, any] = op_any as dict[str, any];
        expr = _build_expression(op["terms"] as list[any], op["const"] as float);
        c = Constraint(
            expression=expr,
            relation=rel_map[op["rel"] as str],
            strength=StrengthTier.REQUIRED,
        );
        r = s.add_constraint(c);
        if not r.ok {
            return {
                "schema_version": 1,
                "seed": seed,
                "ok": False,
                "error": r.error.value,
                "values": {},
            };
        }
    }
    snap = s.snapshot();
    vals: dict[str, float] = {};
    for vid in sorted(snap.values.keys()) {
        vals[str(vid)] = snap.values[vid];
    }
    return {
        "schema_version": 1,
        "seed": seed,
        "ok": True,
        "error": "ok",
        "values": vals,
    };
}


with entry {
    for line in stdin {
        line = line.strip();
        if line == "" {
            continue;
        }
        try {
            batch = loads(line);
            out = _run_batch(batch);
        } except Exception as e {
            print("driver error:", e, file=stderr);
            out = {
                "schema_version": 1,
                "seed": -1,
                "ok": False,
                "error": "driver_exception",
                "values": {},
            };
        }
        stdout.write(dumps(out) + "\n");
    }
    stdout.flush();
}

"""A write that did not happen must not report success.

The optimistic-concurrency machinery was wired but inert: `read_versions` and
`note_traversal_reads` recorded, `WriteConflict` existed with a retry loop and a
409 behind it, and `AnchorRow.version` was populated from `xmin` -- but nothing
ever raised, nothing incremented a version, and `_materialize` dropped the
version it loaded. Concurrent read-modify-writes silently kept the last one and
told every loser it had succeeded.

`xmin` cannot serve as the token either: it is a 32-bit transaction id that
wraps, and VACUUM FREEZE rewrites it to a constant, so two genuinely different
row versions can report the same number on a long-lived table.

These pin a real version column that advances on write, a conflicting write
that reports rather than vanishing, and a long-lived session that sees other
sessions' commits once its own transaction ends (jac#10287).
"""

import from pathlib { Path }
import from tempfile { TemporaryDirectory }
import from uuid { UUID }
import from jaclang.runtime.runtime { JacRuntime }
import from jaclang.runtime.context { ExecutionContext }
import from jaclang.runtime.exceptions { WriteConflict }

node WCounter {
    has n: int = 0;
}


def _as_any(v: any) -> any {
    return v;
}


def _ctx(td: str) -> ExecutionContext {
    return ExecutionContext(
        base_path_dir=td, full_target_path=str(Path(td) / "wc_app.jac")
    );
}


test "a stored anchor carries a version that advances on write" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        cid: UUID;
        try {
            c = WCounter(n=1);
            root ++> c;
            ctx.mem.commit();
            cid = c.__jac__.id;
            store = ctx.mem.store;
            assert store is not None;
            first = store.rows(
                "SELECT version FROM anchors WHERE id = CAST(:i AS uuid)",
                {"i": str(cid)}
            )[0][0];
            c.n = 2;
            ctx.mem.mark_dirty(c.__jac__);
            ctx.mem.commit();
            second = store.rows(
                "SELECT version FROM anchors WHERE id = CAST(:i AS uuid)",
                {"i": str(cid)}
            )[0][0];
            assert int(second) > int(first) , (
                f"a write must advance the version: {first} -> {second}"
            );
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
    }
}


test "a write over a stale read reports instead of vanishing" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx1 = _ctx(td);
        JacRuntime.exec_ctx = ctx1;
        cid: UUID;
        try {
            c = WCounter(n=1);
            root ++> c;
            ctx1.mem.commit();
            cid = c.__jac__.id;
        } finally {
            JacRuntime.exec_ctx = old;
            ctx1.close();
        }
        # Reader A loads the counter and holds its version.
        ctxa = _ctx(td);
        JacRuntime.exec_ctx = ctxa;
        try {
            a = ctxa.mem.get(cid);
            assert a is not None;
            seen = _as_any(a).archetype.n;

            # Writer B advances it out of band and commits first.
            JacRuntime.exec_ctx = old;
            ctxb = _ctx(td);
            JacRuntime.exec_ctx = ctxb;
            try {
                b = ctxb.mem.get(cid);
                assert b is not None;
                _as_any(b).archetype.n = 99;
                ctxb.mem.mark_dirty(b);
                ctxb.mem.commit();
            } finally {
                ctxb.close();
            }

            # A now writes on top of a version that has moved.
            JacRuntime.exec_ctx = ctxa;
            _as_any(a).archetype.n = seen + 1;
            ctxa.mem.mark_dirty(a);
            raised = False;
            try {
                ctxa.mem.commit();
            } except WriteConflict {
                raised = True;
            }
            assert raised , (
                "a write over a version that moved must report a conflict, "
                "not silently overwrite the winner"
            );
            # Reported once, then gone: the next read must not flush the lost
            # write again, A sees the winner, and A can write on top of it.
            ctxa.mem.read_barrier();
            assert ctxa.mem.get(cid) is a and _as_any(a).archetype.n == 99;
            _as_any(a).archetype.n = 100;
            ctxa.mem.mark_dirty(a);
            ctxa.mem.commit();
        } finally {
            JacRuntime.exec_ctx = old;
            ctxa.close();
        }
    }
}


"""Session A reads the counter in one transaction and ends it with `end`, B
commits n=99, and A reads it again. Returns what A's held object shows."""
def _read_after_other_commit(td: str, end: str) -> int {
    old = JacRuntime.exec_ctx;
    ctx1 = _ctx(td);
    JacRuntime.exec_ctx = ctx1;
    cid: UUID;
    try {
        c = WCounter(n=1);
        root ++> c;
        ctx1.mem.commit();
        cid = c.__jac__.id;
    } finally {
        JacRuntime.exec_ctx = old;
        ctx1.close();
    }
    ctxa = _ctx(td);
    JacRuntime.exec_ctx = ctxa;
    try {
        a = ctxa.mem.get(cid);
        assert a is not None;
        fetched = ctxa.mem.get_fetch_count();
        assert ctxa.mem.get(cid) is a and ctxa.mem.get_fetch_count() == fetched , (
            "a second read in the same transaction must come from memory"
        );
        if end == "commit" {
            ctxa.mem.commit();
        } else {
            _as_any(ctxa.mem)._rollback_txn();
        }

        JacRuntime.exec_ctx = old;
        ctxb = _ctx(td);
        JacRuntime.exec_ctx = ctxb;
        try {
            b = ctxb.mem.get(cid);
            assert b is not None;
            _as_any(b).archetype.n = 99;
            ctxb.mem.mark_dirty(b);
            ctxb.mem.commit();
        } finally {
            ctxb.close();
        }

        # A's next transaction reads B's write into the object it already holds,
        # and a write through that object lands without a conflict.
        JacRuntime.exec_ctx = ctxa;
        assert ctxa.mem.get(cid) is a , "a held node was replaced by a second object";
        seen = _as_any(a).archetype.n;
        _as_any(a).archetype.n = 100;
        ctxa.mem.mark_dirty(a);
        ctxa.mem.commit();
        return seen;
    } finally {
        JacRuntime.exec_ctx = old;
        ctxa.close();
    }
}


test "a session sees what others committed once its own transaction ends" {
    for end in ["commit", "rollback"] {
        with TemporaryDirectory() as td {
            seen = _read_after_other_commit(td, end);
            assert seen == 99 , f"after a {end}, the session still reads its own copy: n={seen}";
        }
    }
}

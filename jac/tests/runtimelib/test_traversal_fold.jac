"""Object-space operations on a traversal fold back into the query.

`[a --> [?:T]]` returned a fully materialised list, so `len(...)`, `[0]`,
`[:50]` and a truthiness test each cost O(degree) no matter how little of the
answer was wanted. The result is now realised lazily: the shapes that have a
SQL equivalent push into the query, and anything else realises first and
behaves exactly as a list did.

The contract these pin is that laziness is invisible. The value is still a
list, still compares equal to one, still supports every list operation. What
changes is how much of the graph had to be read to answer the question --
measured here through the session's fetch counter, which counts anchors
materialised into Python.
"""

import from pathlib { Path }
import from tempfile { TemporaryDirectory }
import from jaclang.runtime.runtime { JacRuntime }
import from jaclang.runtime.context { ExecutionContext }

node FBoard {
    has name: str = "";
}

node FItem {
    has rank: int = 0;
}

edge FHas: FBoard --> FItem {}

node FSub {
    has rank: int = 0;
}

edge FSubOf: FItem --> FSub {}


def _as_any(v: any) -> any {
    return v;
}


def _ctx(td: str) -> ExecutionContext {
    return ExecutionContext(
        base_path_dir=td, full_target_path=str(Path(td) / "fold_app.jac")
    );
}


def _seed(n: int) -> FBoard {
    b = FBoard(name="b");
    root ++> b;
    for i in range(n) {
        b +>:FHas():+> FItem(rank=i);
    }
    return b;
}


test "the result is still a list and still equal to one" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = _seed(6);
            ctx.mem.commit();
            got = [b->:FHas:->[?:FItem]];
            assert isinstance(got, list) , type(got);
            assert len(got) == 6;
            ranks = sorted([_as_any(x).rank for x in got]);
            assert ranks == [0, 1, 2, 3, 4, 5] , ranks;
            assert got == list(got);
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
    }
}


test "len() answers without materialising the neighbourhood" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = _seed(40);
            ctx.mem.commit();
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
        ctx2 = _ctx(td);
        JacRuntime.exec_ctx = ctx2;
        try {
            boards = [root-->[?:FBoard]];
            b2 = boards[0];
            ctx2.mem.reset_fetch_count();
            n = len([b2->:FHas:->[?:FItem]]);
            fetched = ctx2.mem.get_fetch_count();
            assert n == 40 , n;
            assert fetched == 0 , (
                f"len() materialised {fetched} anchors; a count has a SQL "
                f"equivalent and must not read the neighbourhood"
            );
        } finally {
            JacRuntime.exec_ctx = old;
            ctx2.close();
        }
    }
}


test "a truthiness test stops at the first row" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = _seed(40);
            ctx.mem.commit();
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
        ctx2 = _ctx(td);
        JacRuntime.exec_ctx = ctx2;
        try {
            boards = [root-->[?:FBoard]];
            b2 = boards[0];
            ctx2.mem.reset_fetch_count();
            assert [b2->:FHas:->[?:FItem]];
            fetched = ctx2.mem.get_fetch_count();
            assert fetched <= 1 , (
                f"a truthiness test materialised {fetched} anchors; it needs "
                f"at most one row to answer"
            );
        } finally {
            JacRuntime.exec_ctx = old;
            ctx2.close();
        }
    }
}


test "a slice reads only the slice" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = _seed(40);
            ctx.mem.commit();
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
        ctx2 = _ctx(td);
        JacRuntime.exec_ctx = ctx2;
        try {
            boards = [root-->[?:FBoard]];
            b2 = boards[0];
            ctx2.mem.reset_fetch_count();
            head = [b2->:FHas:->[?:FItem]][:5];
            fetched = ctx2.mem.get_fetch_count();
            assert len(head) == 5 , len(head);
            assert fetched <= 5 , (
                f"a 5-row slice materialised {fetched} anchors out of 40"
            );
        } finally {
            JacRuntime.exec_ctx = old;
            ctx2.close();
        }
    }
}


test "an unfoldable operation realises and behaves exactly as a list" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = _seed(6);
            ctx.mem.commit();
            got = [b->:FHas:->[?:FItem]];
            got.reverse();
            assert len(got) == 6;
            first = _as_any(got)[0];
            got.append(first);
            assert len(got) == 7;
            counts = sorted([_as_any(x).rank for x in got]);
            assert len(counts) == 7 and len(set(counts)) == 6 , counts;
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
    }
}


test "an edges-only count counts edges, not their endpoints" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = FBoard(name="b");
            root ++> b;
            one = FItem(rank=0);
            b +>:FHas():+> one;
            b +>:FHas():+> one;
            ctx.mem.commit();
            assert len([edge b-->]) == 2 , (
                f"two edges to one node is two edges; got {len([edge b-->])}"
            );
            assert len([b-->[?:FItem]]) == 1 , (
                f"...but one distinct node; got {len([b-->[?:FItem]])}"
            );
            assert [edge b-->] , "an edges-only truthiness test must see them";
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
    }
}


test "a reference is evaluated where it appears, not where it is read" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = _seed(3);
            ctx.mem.commit();
            snapshot = [b->:FHas:->[?:FItem]];
            b +>:FHas():+> FItem(rank=99);
            assert len(snapshot) == 3 , (
                f"the reference must hold the graph as of the line it was "
                f"written on; got {len(snapshot)} after a later attach"
            );
            fresh = [b->:FHas:->[?:FItem]];
            assert len(fresh) == 4 , f"a later reference sees it; got {len(fresh)}";
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
    }
}


def _seed_nested(items: int, subs: int) -> FBoard {
    b = FBoard(name="nested");
    root ++> b;
    for i in range(items) {
        it = FItem(rank=i);
        b +>:FHas():+> it;
        for j in range(subs) {
            it +>:FSubOf():+> FSub(rank=i * 100 + j);
        }
    }
    return b;
}


def _anchor_scans(ctx: ExecutionContext) -> int {
    store = ctx.mem.store;
    assert store is not None , "these tests need the Postgres store";
    rows = store.rows(
        "SELECT coalesce(idx_scan, 0) + coalesce(seq_scan, 0) "
            + "FROM pg_stat_xact_user_tables WHERE relname = 'anchors'",
        {}
    );
    return int(rows[0][0]) if rows else 0;
}


test "hops from nodes one query returned run once for all of them" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            _seed_nested(12, 3);
            ctx.mem.commit();
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
        ctx2 = _ctx(td);
        JacRuntime.exec_ctx = ctx2;
        try {
            board = [root-->[?:FBoard]][0];
            items = list([board->:FHas:->[?:FItem]]);
            assert len(items) == 12;
            first = sorted([_as_any(x).rank for x in [items[0]->:FSubOf:->[?:FSub]]]);
            before = _anchor_scans(ctx2);
            got: dict[int, list[int]] = {};
            for it in items {
                got[_as_any(it).rank] = sorted(
                    [_as_any(x).rank for x in [it->:FSubOf:->[?:FSub]]]
                );
            }
            scans = _anchor_scans(ctx2) - before;
            for (rank, ranks) in got.items() {
                assert ranks == [rank * 100, rank * 100 + 1, rank * 100 + 2] , (
                    rank,
                    ranks
                );
            }
            assert first == got[_as_any(items[0]).rank];
            assert scans < 4 , (
                f"hops from 12 nodes one query returned scanned anchors {scans} times "
                f"after the first; they run as one batched hop"
            );
        } finally {
            JacRuntime.exec_ctx = old;
            ctx2.close();
        }
    }
}


test "a write between batched hops reaches the next hop" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            _seed_nested(6, 2);
            ctx.mem.commit();
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
        ctx2 = _ctx(td);
        JacRuntime.exec_ctx = ctx2;
        try {
            board = [root-->[?:FBoard]][0];
            items = list([board->:FHas:->[?:FItem]]);
            [items[0]->:FSubOf:->[?:FSub]];
            target = items[4];
            target +>:FSubOf():+> FSub(rank=999);
            ranks = sorted([_as_any(x).rank for x in [target->:FSubOf:->[?:FSub]]]);
            assert 999 in ranks , f"a sub-node connected before the hop was missed: {ranks}";
            assert len(ranks) == 3 , ranks;
        } finally {
            JacRuntime.exec_ctx = old;
            ctx2.close();
        }
    }
}


test "a bounded hop from sibling nodes keeps each node's own bound" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            _seed_nested(5, 4);
            ctx.mem.commit();
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
        ctx2 = _ctx(td);
        JacRuntime.exec_ctx = ctx2;
        try {
            board = [root-->[?:FBoard]][0];
            items = list([board->:FHas:->[?:FItem]]);
            for it in items {
                head = [it->:FSubOf:->[?:FSub]][:2];
                assert len(head) == 2 , (_as_any(it).rank, head);
                base = _as_any(it).rank * 100;
                assert all(base <= _as_any(x).rank < base + 4 for x in head) , head;
            }
        } finally {
            JacRuntime.exec_ctx = old;
            ctx2.close();
        }
    }
}

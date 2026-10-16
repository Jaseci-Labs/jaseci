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
import from uuid { UUID }
import from jaclang.runtime.runtime { JacRuntime }
import from jaclang.runtime.context { ExecutionContext }

node FBoard {
    has name: str = "";
}

node FItem {
    has rank: int = 0;
}

edge FHas: FBoard --> FItem {}

node FNoise {}

edge FNote: FBoard --> FItem {
    has note: str = "";
}


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


def _edge_types(ctx: ExecutionContext, where: str) -> list[tuple[str, str]] {
    store = ctx.mem.store;
    assert store is not None , "these tests need the Postgres store";
    rows = store.rows(
        "SELECT src_type, dst_type FROM anchors WHERE kind = 'EdgeAnchor' AND " + where,
        {}
    );
    return [(str(r[0]), str(r[1])) for r in rows];
}


test "typed hops in every direction reach their nodes through recorded endpoint types" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = FBoard(name="dirs");
            root ++> b;
            b ++> FItem(rank=0);
            FItem(rank=10) ++> b;
            b <++> FItem(rank=20);
            FItem(rank=21) <++> b;
            for _ in range(5) {
                b ++> FNoise();
                FNoise() ++> b;
                b <++> FNoise();
                FNoise() <++> b;
            }
            ctx.mem.commit();
            untyped = [
                t
                for t in _edge_types(ctx, "TRUE")
                if "" in t
            ];
            assert untyped == [] , f"edges written without endpoint types: {untyped}";
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
        ctx2 = _ctx(td);
        JacRuntime.exec_ctx = ctx2;
        try {
            b2 = [root-->[?:FBoard]][0];
            out = sorted([_as_any(x).rank for x in [b2-->[?:FItem]]]);
            inc = sorted([_as_any(x).rank for x in [b2<--[?:FItem]]]);
            both = sorted([_as_any(x).rank for x in [b2<-->[?:FItem]]]);
            assert out == [0, 20, 21] , out;
            assert inc == [10, 20, 21] , inc;
            assert both == [0, 10, 20, 21] , both;
            assert len([b2<-->[?:FNoise]]) == 20;
        } finally {
            JacRuntime.exec_ctx = old;
            ctx2.close();
        }
    }
}


test "an edge write takes its endpoint type from the stored node, not a stale copy" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = FBoard(name="stale");
            root ++> b;
            b +>:FNote(note="a"):+> FItem(rank=1);
            ctx.mem.commit();
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
        ctx2 = _ctx(td);
        JacRuntime.exec_ctx = ctx2;
        try {
            b2 = [root-->[?:FBoard]][0];
            items = [b2->:FNote:->[?:FItem]];
            notes = [edge b2->:FNote:->];
            assert len(items) == 1 and len(notes) == 1;
            iid = str(_as_any(items[0]).__jac__.id);
            other = _ctx(td);
            try {
                ostore = other.mem.store;
                assert ostore is not None;
                ostore.rows(
                    "UPDATE anchors SET arch_type = 'renamed.FItem' "
                        + "WHERE id = CAST(:i AS uuid)",
                    {"i": iid}
                );
                ostore.retype_edges([UUID(iid)]);
            } finally {
                other.close();
            }
            _as_any(notes[0]).note = "b";
            ctx2.mem.commit();
            assert _edge_types(ctx2, "props::text LIKE '%FNote%'")[0][1]
                == "renamed.FItem" , _edge_types(ctx2, "props::text LIKE '%FNote%'");
        } finally {
            JacRuntime.exec_ctx = old;
            ctx2.close();
        }
    }
}


test "an edge rewritten without loading its endpoints keeps their types" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = FBoard(name="noted");
            root ++> b;
            b +>:FNote(note="a"):+> FItem(rank=1);
            ctx.mem.commit();
            typed = _edge_types(ctx, "props::text LIKE '%FNote%'");
            assert len(typed) == 1 and "" not in typed[0] , typed;
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
        ctx2 = _ctx(td);
        JacRuntime.exec_ctx = ctx2;
        try {
            b2 = [root-->[?:FBoard]][0];
            for e in [edge b2->:FNote:->] {
                assert not _as_any(e).__jac__.target.is_populated() , (
                    "the edge's target must stay a stub for this test"
                );
                _as_any(e).note = "b";
            }
            ctx2.mem.commit();
            assert _edge_types(ctx2, "props::text LIKE '%FNote%'") == typed;
        } finally {
            JacRuntime.exec_ctx = old;
            ctx2.close();
        }
        ctx3 = _ctx(td);
        JacRuntime.exec_ctx = ctx3;
        try {
            b3 = [root-->[?:FBoard]][0];
            notes = [_as_any(e).note for e in [edge b3->:FNote:->]];
            assert notes == ["b"] , notes;
            assert [_as_any(x).rank for x in [b3->:FNote:->[?:FItem]]] == [1];
        } finally {
            JacRuntime.exec_ctx = old;
            ctx3.close();
        }
    }
}


test "a node whose stored type changed is still reached by typed hops" {
    with TemporaryDirectory() as td {
        old = JacRuntime.exec_ctx;
        ctx = _ctx(td);
        JacRuntime.exec_ctx = ctx;
        try {
            b = FBoard(name="moved");
            root ++> b;
            item = FItem(rank=7);
            b ++> item;
            ctx.mem.commit();
            store = ctx.mem.store;
            assert store is not None;
            iid = str(_as_any(item).__jac__.id);
            store.rows(
                "UPDATE anchors SET arch_type = 'moved.FItem' "
                    + "WHERE id = CAST(:i AS uuid)",
                {"i": iid}
            );
            store.rows(
                "UPDATE anchors SET dst_type = 'moved.FItem' "
                    + "WHERE dst = CAST(:i AS uuid)",
                {"i": iid}
            );
        } finally {
            JacRuntime.exec_ctx = old;
            ctx.close();
        }
        ctx2 = _ctx(td);
        JacRuntime.exec_ctx = ctx2;
        try {
            b2 = [root-->[?:FBoard]][0];
            for x in [b2-->] {
                _as_any(x).rank = 8;
            }
            ctx2.mem.commit();
        } finally {
            JacRuntime.exec_ctx = old;
            ctx2.close();
        }
        ctx3 = _ctx(td);
        JacRuntime.exec_ctx = ctx3;
        try {
            b3 = [root-->[?:FBoard]][0];
            ranks = [_as_any(x).rank for x in [b3-->[?:FItem]]];
            assert ranks == [8] , (
                f"a node rewritten under its current type was missed by a typed hop: {ranks}"
            );
        } finally {
            JacRuntime.exec_ctx = old;
            ctx3.close();
        }
    }
}

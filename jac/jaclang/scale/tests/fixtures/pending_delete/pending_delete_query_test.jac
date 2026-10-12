"""Pinned-runtime regression: a query must not resurrect a pending deletion.
Run only in CI with the real Mongo/Redis services and JAC_TEST_NATIVE=1.
"""

import from contextlib { contextmanager }
import from uuid { uuid4 }
import from typing { Generator }
import from jaclang { JacRuntime as Jac }
import from jaclang.runtimelib.query_plan { QueryPlan }
import from jaclang.runtimelib.exceptions { MissingAnchorError }

node DeleteQueryOwner {
    has marker: str;
}

node DeleteQueryTarget {
    has marker: str;
}

node DeleteQueryChild {
    has marker: str;
}


"""Only identifiers and persistence metadata, never archetype fields."""
def _diagnose(ctx: any, anchor_id: any, stage: str) -> None {
    mem = ctx.mem;
    pending = mem.changes.intents.get(anchor_id);
    cached = mem.__mem__.get(anchor_id);
    stored = mem.l3.collection.find_one(
        {"_id": str(anchor_id)}, {"data.version": 1}
    );
    print({
        "stage": stage,
        "anchor_id": str(anchor_id),
        "pending_delete": pending is not None and pending.is_delete(),
        "cached": cached is not None,
        "cached_version": cached.version if cached is not None else None,
        "stored": stored is not None,
        "stored_version": stored.get("data", {}).get("version") if stored is not None else None
    });
}


"""Each case owns a request context and unique graph records."""
@contextmanager
def _fixture() -> Generator[any, None, None] {
    ctx: any = Jac.create_j_context(user_root=None);
    token: any = Jac.push_request_context(ctx);
    owner: DeleteQueryOwner | None = None;
    target: DeleteQueryTarget | None = None;
    child: DeleteQueryChild | None = None;
    try {
        mem = ctx.mem;
        assert getattr(mem.l3, "collection", None) is not None,
            "this regression requires the CI Mongo backend";
        marker = "delete-query-" + uuid4().hex;
        owner = root ++> DeleteQueryOwner(marker=marker);
        target = owner ++> DeleteQueryTarget(marker=marker);
        mem.commit();
        child = target ++> DeleteQueryChild(marker=marker);
        mem.commit();
        target_metadata: any = target;
        target_id = target_metadata.__jac__.id;
        plan = QueryPlan(field_predicates={
            "__type__": "DeleteQueryTarget", "marker": marker
        });
        assert target_metadata.__jac__.version >= 1,
            "the fixture needs an existing versioned target before deletion";
        _diagnose(ctx, target_id, "persisted");
        yield (ctx, owner, target, target_id, plan);
    } finally {
        # Abandon failed writes before cleanup, then restore the original
        # context before disposing the failed request's memory.
        try {
            ctx.mem.abort();
        } finally {
            try {
                ctx.close();
            } finally {
                Jac.reset_request_context(token);
            }
        }
        # Delete only this case's graph, from a fresh request context. The
        # children are explicit because deleting a node removes its edges,
        # not every child node connected to it.
        cleanup: any = Jac.create_j_context(user_root=None);
        cleanup_token: any = Jac.push_request_context(cleanup);
        try {
            for fixture_node in [child, target, owner] {
                if fixture_node is not None {
                    try {
                        metadata: any = fixture_node;
                        fresh = jobj(str(metadata.__jac__.id));
                    } except MissingAnchorError {
                        continue;
                    }
                    if fresh is not None { del fresh; }
                }
            }
            cleanup.mem.commit();
        } finally {
            try { cleanup.close(); }
            finally { Jac.reset_request_context(cleanup_token); }
        }
    }
}


test "a real Mongo query excludes a target pending deletion in this request" {
    with _fixture() as raw_fixture {
        fixture: any = raw_fixture;
        ctx: any = fixture[0];
        target: DeleteQueryTarget = fixture[2];
        target_id: any = fixture[3];
        plan: QueryPlan = fixture[4];
        del target;
        _diagnose(ctx, target_id, "pending-delete");
        intent = ctx.mem.changes.intents.get(target_id);
        assert intent is not None and intent.is_delete(),
            "the fixture must hold an uncommitted delete";
        assert ctx.mem.l3.collection.find_one({"_id": str(target_id)}) is not None,
            "the Mongo delete must still be deferred until commit";
        found = list(ctx.mem.execute_plan(plan));
        _diagnose(ctx, target_id, "queried-pending-delete");
        assert found == [],
            "a query in the deleting request must not return its deleted target";
        cached: dict = ctx.mem.__mem__;
        assert target_id not in cached,
            "a query must not rehydrate a pending deletion into request memory";
    }
}


test "a query and owner reconciliation cannot poison later commits with a deleted target" {
    with _fixture() as raw_fixture {
        fixture: any = raw_fixture;
        ctx: any = fixture[0];
        owner: DeleteQueryOwner = fixture[1];
        target: DeleteQueryTarget = fixture[2];
        target_id: any = fixture[3];
        plan: QueryPlan = fixture[4];
        del target;
        # Builder's owner reconciliation reconnects every returned orphan.
        # This loop is empty when the query correctly respects the deletion.
        for anchor in ctx.mem.execute_plan(plan) {
            returned: any = anchor;
            owner ++> (returned.archetype as DeleteQueryTarget);
        }
        _diagnose(ctx, target_id, "reconciled-pending-delete");
        ctx.mem.commit();
        _diagnose(ctx, target_id, "first-commit");
        assert ctx.mem.l3.collection.find_one({"_id": str(target_id)}) is None,
            "the first commit must durably remove the target";
        # Without the runtime repair this attempts an edge update against
        # the deleted document, producing expected v1 / found v-1.
        ctx.mem.commit();
        _diagnose(ctx, target_id, "second-commit");
        assert list(ctx.mem.execute_plan(plan)) == [],
            "the target must stay deleted after subsequent commits";
        cached: dict = ctx.mem.__mem__;
        assert target_id not in cached,
            "the deleted target must not remain in request memory";
    }
}

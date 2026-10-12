"""Request reads must respect an uncommitted deletion across real cache tiers.
Run only in CI with Mongo/Redis services and JAC_TEST_NATIVE=1.
"""

import from uuid { uuid4 }
import from jaclang { JacRuntime as Jac }
import from jaclang.runtimelib.query_plan { QueryPlan }

node ContextualDeleteOwner { has marker: str; }
node ContextualDeleteTarget { has marker: str; }

test "all request lookups hide a pending deletion with real Mongo and Redis" {
    ctx: any = Jac.create_j_context(user_root=None);
    token: any = Jac.push_request_context(ctx);
    try {
        mem: any = ctx.mem;
        assert getattr(mem.l3, "collection", None) is not None,
            "this regression requires the CI Mongo backend";
        assert mem.l2 is not None and getattr(mem.l2, "redis_client", None) is not None,
            "this regression requires the CI Redis backend";
        marker = "contextual-delete-" + uuid4().hex;
        owner = root ++> ContextualDeleteOwner(marker=marker);
        target = owner ++> ContextualDeleteTarget(marker=marker);
        mem.commit();
        metadata: any = target;
        target_id: any = metadata.__jac__.id;
        assert mem.l3.collection.find_one({"_id": str(target_id)}) is not None,
            "the fixture must be durable before deleting it";
        mem.l2.put(metadata.__jac__);
        assert mem.l2.exists(target_id), "the fixture must warm the real Redis cache";
        cached: any = mem.l2.get(target_id);
        assert cached is not None and cached.id == target_id,
            "the Redis cache must return the same fixture anchor";
        plan = QueryPlan(field_predicates={
            "__type__": "ContextualDeleteTarget", "marker": marker
        });
        del target;

        # Collect every outcome before asserting so the red evidence names
        # all request-facing lookup paths, including Scale's overrides.
        observed = {
            "get_absent": mem.get(target_id) is None,
            "has_absent": not mem.`has(target_id),
            "batch_absent": target_id not in mem.batch_get([target_id]),
            "query_absent": list(mem.execute_plan(plan)) == []
        };
        pending: any = mem.changes.intents.get(target_id);
        observed["delete_still_pending"] = pending is not None and pending.is_delete();
        observed["mongo_delete_still_deferred"] = (
            mem.l3.collection.find_one({"_id": str(target_id)}) is not None
        );
        observed["l1_absent"] = target_id not in mem.__mem__;
        print({"stage": "pending-delete-contextual-reads",
            "anchor_id": str(target_id), "observed": observed});
        assert all(observed.values()),
            "pending deletion leaked through request lookups: " + str(observed);
    } finally {
        # Unique records live only in the ephemeral CI database. Teardown
        # abandons the request rather than committing a failed assertion.
        try { ctx.mem.abort(); }
        finally {
            try { ctx.close(); }
            finally { Jac.reset_request_context(token); }
        }
    }
}

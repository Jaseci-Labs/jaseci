"""The project-cleanup ordering: traverse children before deleting their owner."""

import from uuid { uuid4 }
import from jaclang { JacRuntime as Jac }
import from jaclang.runtimelib.query_plan { QueryPlan }

node TraversedDeleteOwner { has marker: str; }
node TraversedDeleteTarget { has marker: str; }
node TraversedDeleteChild { has marker: str; }

test "a traversed deletion cannot poison later commits after owner reconciliation" {
    ctx: any = Jac.create_j_context(user_root=None);
    token: any = Jac.push_request_context(ctx);
    try {
        mem: any = ctx.mem;
        assert getattr(mem.l3, "collection", None) is not None,
            "this regression requires the CI Mongo backend";
        marker = "traversed-delete-" + uuid4().hex;
        owner = root ++> TraversedDeleteOwner(marker=marker);
        target = owner ++> TraversedDeleteTarget(marker=marker);
        mem.commit();
        target ++> TraversedDeleteChild(marker=marker);
        mem.commit();
        metadata: any = target;
        target_id = metadata.__jac__.id;
        children = [target -->[?:TraversedDeleteChild]];
        assert len(children) == 1;
        assert ctx.read_versions.get(target_id) == metadata.__jac__.version;
        assert int(ctx.read_versions[target_id]) >= 1,
            "the traversal must record a positive OCC version";
        plan = QueryPlan(field_predicates={
            "__type__": "TraversedDeleteTarget", "marker": marker
        });
        del target;
        for anchor in mem.execute_plan(plan) {
            returned: any = anchor;
            owner ++> (returned.archetype as TraversedDeleteTarget);
        }
        mem.commit();
        assert mem.l3.collection.find_one({"_id": str(target_id)}) is None;
        print({"stage": "deleted-after-traversal", "anchor_id": str(target_id),
            "read_version": ctx.read_versions.get(target_id)});
        try {
            mem.commit();
        } except Exception as error {
            assert False, "subsequent commit failed after traversed deletion: " + str(error);
        }
        assert mem.l3.collection.find_one({"_id": str(target_id)}) is None,
            "a later commit must not recreate the deleted target";
    } finally {
        # This standalone CI process uses unique fixtures in ephemeral Mongo.
        # Abandon failed writes; teardown must not commit them again.
        try { ctx.mem.abort(); }
        finally {
            try { ctx.close(); }
            finally { Jac.reset_request_context(token); }
        }
    }
}

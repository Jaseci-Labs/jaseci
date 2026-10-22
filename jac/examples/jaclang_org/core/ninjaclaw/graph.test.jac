def _job(job_id: str) -> ClawJob;

impl _job(job_id: str) -> ClawJob {
    found = jobj(job_id);
    assert isinstance(found, ClawJob);
    return found;
}

test "a removed post's job is hidden, never worked, and its gap is dropped" {
    ids = enqueue_asks(
        [
            AskInput(
                ask_key="k1", tweet_id="t1", asker="ann", question="how do walkers work"
            ),
            AskInput(
                ask_key="k2", tweet_id="t2", asker="bob", question="what is a node"
            )
        ]
    );
    hub = claw_hub();
    hub +>:HasGap():+> ClawGap(question="how do walkers work", job_id=ids[0]);
    assert forget_jobs([ids[0]]) == 1;
    assert forget_jobs([ids[0]]) == 0;
    gone = _job(ids[0]);
    assert gone.removed and gone.question == "" and gone.outcome == "removed";
    assert [hub->:HasGap:->[?:ClawGap]] == [];
    nxt = next_queued();
    assert nxt is not None and jid(nxt) == ids[1];
    record_outcome(gone, Outcome(status="failed", outcome="failed"));
    assert gone.status == "failed";
}

test "pruning keeps the newest finished jobs and any job that wrote a tutorial" {
    ids = enqueue_asks(
        [
            AskInput(ask_key="p" + str(n), asker="ann", question="question " + str(n))
            for n in range(4)
        ]
    );
    for (n, job_id) in enumerate(ids) {
        job = _job(job_id);
        job.status = "done";
        job.finished_at = "2026-01-0" + str(n + 1) + "T00:00:00Z";
    }
    claw_hub() +>:HasTutorial():+> ClawTutorial(slug="kept", job_id=ids[0]);
    before = len(claw_jobs());
    pruned = prune_jobs(
        len(
            [
                j
                for j in claw_jobs()
                if j.status not in ("queued", "working")
            ]
        )
            - 2
    );
    assert pruned == 1;
    assert len(claw_jobs()) == before - 1;
    assert jobj(ids[0]) is not None;
    assert ids[1] not in [jid(j) for j in claw_jobs()];
}

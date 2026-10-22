import from unittest.mock { patch }
import from core.ninjaclaw.index { index_doc }
import from core.ninjaclaw.brain { Pick }

def _catalog -> list[IndexDoc];

def _steps -> list[str];

test "replies stay inside the post limit" {
    long_title = "A very long tutorial title " * 20;
    reply = link_reply(long_title, "/jacyac/tutorials/x", "abc123");
    assert len(reply) <= REPLY_LIMIT;
    assert reply.endswith("/jacyac/ninjaclaw/abc123");
    gap = gap_reply([LinkView(title="W", href="/docs/latest/walkers")], "abc123");
    assert len(gap) <= REPLY_LIMIT and "/docs/latest/walkers" in gap;
}

test "an off-topic post is ignored without retrieval" {
    notes: list[str] = [];
    with patch(
        run_pipeline.__module__ + ".classify_ask", return_value=AskKind.OFF_TOPIC
    ) {
        out = run_pipeline(
            JobSpec(job_id="j1", question="what's your favorite pizza"),
            _catalog(),
            lambda (phase: str, text: str) { notes.append(phase); }
        );
    }
    assert out.status == "ignored" and out.reply == "";
    assert "retrieve" not in notes;
}

test "a confident pick links the matching page" {
    with patch(
        run_pipeline.__module__ + ".classify_ask", return_value=AskKind.JAC_QUESTION
    ), patch(
        run_pipeline.__module__ + ".pick_answer",
        return_value=Pick(index=0, confidence=0.9, why="covers spawning")
    ) {
        out = run_pipeline(
            JobSpec(job_id="j2", question="how do I spawn a walker"),
            _catalog(),
            lambda (phase: str, text: str) {}
        );
    }
    assert out.outcome == "linked_docs";
    assert out.links[0].href == "/docs/latest/walkers";
    assert "/docs/latest/walkers" in out.reply;
}

test "no confident pick records a gap" {
    with patch(
        run_pipeline.__module__ + ".classify_ask", return_value=AskKind.JAC_QUESTION
    ), patch(
        run_pipeline.__module__ + ".pick_answer",
        return_value=Pick(index=-1, confidence=0.1, why="none fit")
    ) {
        out = run_pipeline(
            JobSpec(job_id="j3", question="how do walkers persist nodes"),
            _catalog(),
            lambda (phase: str, text: str) {}
        );
    }
    assert out.outcome == "gap";
    assert "/jacyac/ninjaclaw/j3" in out.reply;
}

impl _catalog -> list[IndexDoc] {
    return [
        index_doc(
            "docs",
            "walkers.md",
            "Walkers",
            "/docs/latest/walkers",
            "Walkers visit nodes. Spawn a walker on root."
        ),
        index_doc(
            "docs",
            "persist.md",
            "Persistence",
            "/docs/latest/persist",
            "Nodes reachable from root persist."
        )
    ];
}

impl _steps -> list[str] {
    return [];
}

import time;

test "only tutorials not yet verified on this jac are swept" {
    items = sweep_items(
        [
            ("current", "a", "published", "0.38.0"),
            ("older", "b", "published", "0.37.0"),
            ("stale", "c", "stale", "0.37.0"),
            ("gone", "d", "removed", "0.37.0")
        ],
        "0.38.0"
    );
    assert [i.slug for i in items] == ["older", "stale"];
}

test "a tutorial passes only when every block passes" {
    assert sweep_passed([BlockView(ok=True), BlockView(ok=True)]);
    assert not sweep_passed([BlockView(ok=True), BlockView(ok=False)]);
    assert not sweep_passed([]);
}

test "a chore runs once, reports progress, and hands back its result" {
    chore = Chore();

    def work(note: Callable) -> int {
        note("sweep", "halfway");
        return 42;
    }
    assert chore.start("sweep", work);
    assert not chore.start("sweep", work);
    deadline = time.time() + 5;
    taken = chore.take();
    while taken is None and time.time() < deadline {
        time.sleep(0.01);
        taken = chore.take();
    }
    assert taken == ("sweep", 42, "");
    assert not chore.busy();
    assert chore.start("pr", lambda (note: Callable) { 1 / 0; });
    deadline = time.time() + 5;
    taken = chore.take();
    while taken is None and time.time() < deadline {
        time.sleep(0.01);
        taken = chore.take();
    }
    assert taken is not None and taken[0] == "pr" and "ZeroDivisionError" in taken[2];
}

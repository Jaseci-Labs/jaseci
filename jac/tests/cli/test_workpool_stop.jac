"""A job that raises an error marked `stops_command` (the unloadable-kernel
refusal) stops the whole pool, inline or in a forked worker, instead of
being recorded as one failed item while the rest go on."""

import from jaclang.cli.workpool { WorkPool, pool_available }
import from jaclang.compiler.backends.native.kernel_resolve { KernelLoadError }

glob _seen: list[int] = [];

def _job(request: dict[(str, any)]) -> any {
    raise KernelLoadError("jac: stop");
}

def _on_record(idx: int, record: dict[(str, any)]) {
    _seen.append(idx);
}

def _exit_job(request: dict[(str, any)]) -> any {
    raise SystemExit(3);
}

def _stopped(pool: WorkPool, inline: bool) -> (str | None) {
    try {
        if inline {
            pool.run_inline();
        } else {
            pool.run();
        }
    } except SystemExit as e {
        return str(e.code);
    }
    return None;
}

test "a command-stopping job error stops an inline pool" {
    _seen.clear();
    pool = WorkPool(items=["a", "b", "c"], job=_job, on_record=_on_record);
    assert _stopped(pool, True) == "jac: stop";
    assert _seen == [] , _seen;
}

test "a command-stopping job error in a worker stops the pool" {
    if not pool_available() {
        return;
    }
    _seen.clear();
    pool = WorkPool(
        items=[f"item-{i}" for i in range(6)],
        job=_job,
        on_record=_on_record,
        jobs=2,
        crash_prefix="jac-workpool-stop-test-"
    );
    assert _stopped(pool, False) == "jac: stop";
    assert _seen == [] , _seen;
}

test "any other SystemExit from a job is one failed item" {
    _seen.clear();
    pool = WorkPool(items=["a", "b"], job=_exit_job, on_record=_on_record);
    assert _stopped(pool, True) is None;
    assert _seen == [0, 1] , _seen;
}

"""`flow f(p)` must run `f` with the `p` it was launched with, even when the task only starts after the
loop that launched it has moved on (here: the pool is held busy until every task is queued)."""
import from threading { Event }

glob gate = Event();

def hold -> int {
    gate.wait();
    return 0;
}

def echo(p: str, suffix: str = "") -> str {
    return p + suffix;
}

def fan(items: list[str]) -> list[str] {
    holders = [flow hold()  for _ in range(64)];
    futures = [flow echo(p)  for p in items];
    keyed = [flow echo(p, suffix="!")  for p in items];
    gate.set();
    for h in holders {
        wait h ;
    }
    return [wait f  for f in futures] + [wait f  for f in keyed];
}

with entry {
    print(fan(["a", "b", "c"]));
}

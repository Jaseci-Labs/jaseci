import threading;

obj SweepItem {
    has slug: str = "",
        body: str = "";
}

obj Chore {
    has lock: threading.Lock = threading.Lock(),
        kind: str = "",
        progress: str = "",
        result: any = None,
        error: str = "",
        finished: bool = False;

    def busy -> bool;
    def start(kind: str, work: Callable) -> bool;
    def note(phase: str, text: str) -> None;
    def status -> tuple[str, str];
    def take -> tuple[str, any, str] | None;
}

glob CHORE: Chore = Chore();

def sweep_items(
    tutorials: list[tuple[str, str, str, str]], version: str
) -> list[SweepItem];

def sweep(items: list[SweepItem], note: Callable) -> dict[str, list[BlockView]];

def sweep_passed(blocks: list[BlockView]) -> bool;

impl Chore.busy -> bool {
    with self.lock {
        return bool(self.kind) and not self.finished;
    }
}

impl Chore.start(kind: str, work: Callable) -> bool {
    with self.lock {
        if self.kind {
            return False;
        }
        self.kind = kind;
        self.progress = "";
        self.result = None;
        self.error = "";
        self.finished = False;
    }

    def run {
        result: any = None;
        error = "";
        try {
            result = work(self.note);
        } except Exception as e {
            error = (type(e).__name__ + ": " + str(e))[:400];
        }
        with self.lock {
            self.result = result;
            self.error = error;
            self.finished = True;
        }
    }
    threading.Thread(target=run, name="ninjaclaw-" + kind, daemon=True).start();
    return True;
}

impl Chore.note(phase: str, text: str) -> None {
    with self.lock {
        self.progress = (text or phase)[:200];
    }
}

impl Chore.status -> tuple[str, str] {
    with self.lock {
        return ("" if self.finished else self.kind, self.progress);
    }
}

impl Chore.take -> tuple[str, any, str] | None {
    with self.lock {
        if not self.kind or not self.finished {
            return None;
        }
        out = (self.kind, self.result, self.error);
        self.kind = "";
        self.result = None;
        self.error = "";
        self.finished = False;
        return out;
    }
}

impl sweep_items(
    tutorials: list[tuple[str, str, str, str]], version: str
) -> list[SweepItem] {
    items: list[SweepItem] = [];
    for (slug, body, status, verified) in tutorials {
        if status == "removed" {
            continue;
        }
        if status == "published" and verified == version {
            continue;
        }
        items.append(SweepItem(slug=slug, body=body));
    }
    return items;
}

impl sweep(items: list[SweepItem], note: Callable) -> dict[str, list[BlockView]] {
    results: dict[str, list[BlockView]] = {};
    for (i, item) in enumerate(items) {
        note(
            "sweep",
            "re-verifying "
                + item.slug
                + " ("
                + str(i + 1)
                + " of "
                + str(len(items))
                + ")"
        );
        results[item.slug] = verify_markdown(
            item.body, lambda (p: str, t: str) { None; }
        );
    }
    return results;
}

impl sweep_passed(blocks: list[BlockView]) -> bool {
    return bool(blocks) and all([b.ok for b in blocks]);
}

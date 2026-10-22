import threading;
import from datetime { datetime, UTC }

obj JobSpec {
    has job_id: str = "",
        question: str = "",
        asker: str = "",
        source: str = "";
}

obj TutorialDraft {
    has slug: str = "",
        title: str = "",
        summary: str = "",
        body: str = "",
        blocks: list[BlockView] = [];
}

obj Outcome {
    has status: str = "done",
        outcome: str = "",
        reply: str = "",
        detail: str = "",
        links: list[LinkView] = [],
        consulted: list[str] = [],
        blocks: list[BlockView] = [],
        steps: list[StepView] = [],
        tutorial: TutorialDraft | None = None,
        tutorial_slug: str = "";
}

obj Runner {
    has lock: threading.Lock = threading.Lock(),
        spec: JobSpec | None = None,
        steps: list[StepView] = [],
        done: list[tuple[str, Outcome]] = [];

    def busy -> bool;
    def start(spec: JobSpec, catalog: list[IndexDoc], work: Callable) -> bool;
    def note(phase: str, text: str) -> None;
    def live -> tuple[JobSpec | None, list[StepView]];
    def drain -> list[tuple[str, Outcome]];
}

glob MIN_CONFIDENCE: float = 0.6,
     CANDIDATES: int = 12,
     REPLY_LIMIT: int = 280,
     RUNNER: Runner = Runner();

def stamp -> str;

def fit(text: str, limit: int) -> str;

def job_path(job_id: str) -> str;

def link_reply(title: str, href: str, job_id: str) -> str;

def gap_reply(links: list[LinkView], job_id: str) -> str;

def run_pipeline(spec: JobSpec, catalog: list[IndexDoc], note: Callable) -> Outcome;

impl stamp -> str {
    return datetime.now(UTC).replace(tzinfo=None).isoformat() + "Z";
}

impl fit(text: str, limit: int) -> str {
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…";
}

impl job_path(job_id: str) -> str {
    return "/jacyac/ninjaclaw/" + job_id;
}

impl link_reply(title: str, href: str, job_id: str) -> str {
    tail = " · how I found it: " + job_path(job_id);
    head = " covers this: " + href;
    room = REPLY_LIMIT - len(tail) - len(head);
    return fit(title, max(room, 12)) + head + tail;
}

impl gap_reply(links: list[LinkView], job_id: str) -> str {
    text = "I couldn't find a tutorial or docs page that answers this yet, so I logged it as a docs gap: "
        + job_path(job_id);
    for link in links {
        extra = " · closest: " + link.href;
        if len(text) + len(extra) <= REPLY_LIMIT {
            text = text + extra;
        }
    }
    return text;
}

impl Runner.busy -> bool {
    with self.lock {
        return self.spec is not None;
    }
}

impl Runner.start(spec: JobSpec, catalog: list[IndexDoc], work: Callable) -> bool {
    with self.lock {
        if self.spec is not None {
            return False;
        }
        self.spec = spec;
        self.steps = [];
    }

    def run {
        outcome: Outcome = Outcome(status="failed", outcome="failed");
        try {
            outcome = work(spec, catalog, self.note);
        } except Exception as e {
            outcome = Outcome(
                status="failed",
                outcome="failed",
                detail=(type(e).__name__ + ": " + str(e))[:400]
            );
            self.note("failed", outcome.detail);
        }
        with self.lock {
            outcome.steps = list(self.steps);
            self.done.append((spec.job_id, outcome));
            self.spec = None;
        }
    }
    threading.Thread(
        target=run, name="ninjaclaw-" + spec.job_id[:8], daemon=True
    ).start();
    return True;
}

impl Runner.note(phase: str, text: str) -> None {
    with self.lock {
        self.steps.append(StepView(at=stamp(), phase=phase, text=fit(text, 400)));
    }
}

impl Runner.live -> tuple[JobSpec | None, list[StepView]] {
    with self.lock {
        return (self.spec, list(self.steps));
    }
}

impl Runner.drain -> list[tuple[str, Outcome]] {
    with self.lock {
        finished = list(self.done);
        self.done = [];
        return finished;
    }
}

impl run_pipeline(spec: JobSpec, catalog: list[IndexDoc], note: Callable) -> Outcome {
    out = Outcome();
    note("classify", "reading the post");
    if classify_ask(spec.question) == AskKind.OFF_TOPIC {
        note("classify", "not a Jac question: ignoring it");
        out.status = "ignored";
        out.outcome = "ignored";
        return out;
    }
    note("retrieve", "searching the tutorials and the docs of the serving release");
    hits = search(catalog, spec.question, CANDIDATES);
    out.consulted = [h.doc.kind + ": " + h.doc.title for h in hits];
    if hits {
        note("retrieve", "candidates: " + ", ".join([h.doc.title for h in hits[:5]]));
        candidates = [
            Candidate(
                index=i,
                kind=h.doc.kind,
                title=h.doc.title,
                excerpt=excerpt(h.doc, spec.question)
            ) for (i, h) in enumerate(hits)
        ];
        note("judge", "checking whether a candidate answers it");
        pick = pick_answer(spec.question, candidates);
        if pick.index >= 0
            and pick.index < len(hits)
            and pick.confidence >= MIN_CONFIDENCE {
            doc = hits[pick.index].doc;
            note("judge", "matched " + doc.title + ": " + pick.why);
            out.outcome = "linked_tutorial"
                if doc.kind == "tutorial"
                else "linked_docs";
            out.links = [LinkView(title=doc.title, href=doc.href)];
            out.tutorial_slug = doc.key if doc.kind == "tutorial" else "";
            out.reply = link_reply(doc.title, doc.href, spec.job_id);
            return out;
        }
        note("judge", "no candidate answers it: " + pick.why);
    } else {
        note("retrieve", "nothing in the tutorials or docs matches");
    }
    out.outcome = "gap";
    out.detail = "no existing tutorial or docs page answers it";
    out.links = [LinkView(title=h.doc.title, href=h.doc.href) for h in hits[:2]];
    out.reply = gap_reply(out.links, spec.job_id);
    return out;
}

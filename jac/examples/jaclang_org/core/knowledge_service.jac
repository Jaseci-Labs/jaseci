import logging;
import os;
import from jaclang.cli.manifest_route { resolve_cli_version }

obj ReleaseDocsInfo {
    has label: str = "",
        tag: str = "",
        version: str = "",
        fingerprint: str = "";
}

obj ReleaseLines {
    has ready: bool = False,
        serving_label: str = "",
        lines: list[ReleaseDocsInfo] = [];
}

glob REPO_TICK_S: float = 60.0,
     WORK_TICK_S: float = 5.0,
     QUEUE_LIMIT: int = 20,
     _BUNDLES: dict[str, DocBundle] = {},
     _CATALOG: dict[str, list[IndexDoc]] = {},
     log: logging.Logger = logging.getLogger("knowledge");

def release_bundle(line: ReleaseLine) -> DocBundle;

@schedule(trigger=ScheduleTrigger.STATIC, interval=REPO_TICK_S)
def:priv knowledge_repo_tick;

def:pub knowledge_status -> RepoStatus;

def:pub release_doc_lines -> ReleaseLines;

def:pub release_docs(tag: str) -> DocBundle | None;

def ninjaclaw_enabled -> tuple[bool, str];

def docs_catalog -> list[IndexDoc];

def tutorial_catalog -> list[IndexDoc];

def public_view(job: ClawJob, live: list[StepView] | None = None) -> JobView;

@schedule(trigger=ScheduleTrigger.STATIC, interval=WORK_TICK_S)
def:priv ninjaclaw_work_tick;

def:pub ninjaclaw_submit(secret: str, asks: list[AskInput]) -> list[str];

def:pub ninjaclaw_results(secret: str, job_ids: list[str]) -> list[JobReply];

def:pub ninjaclaw_activity -> Activity;

def:pub ninjaclaw_job(job_id: str) -> JobView | None;

def:pub ninjaclaw_tutorials -> list[TutorialCard];

def:pub ninjaclaw_tutorial(slug: str) -> TutorialView | None;

impl release_bundle(line: ReleaseLine) -> DocBundle {
    cached = _BUNDLES.get(line.tag);
    if cached is None {
        cached = bundle_from(export_docs(line), line.version);
        _BUNDLES[line.tag] = cached;
    }
    return cached;
}

impl knowledge_repo_tick {
    status = ensure_repo(resolve_cli_version());
    if status.phase != "ready" {
        log.info("knowledge: repo " + status.phase + " " + status.detail);
    }
}

impl knowledge_status -> RepoStatus {
    return read_status();
}

impl release_doc_lines -> ReleaseLines {
    status = read_status();
    answer = ReleaseLines(
        ready=status.phase == "ready",
        serving_label=label_of(status.serving_version or resolve_cli_version())
    );
    if not answer.ready {
        return answer;
    }
    for line in status.lines {
        bundle = release_bundle(line);
        answer.lines.append(
            ReleaseDocsInfo(
                label=line.label,
                tag=line.tag,
                version=line.version,
                fingerprint=bundle.fingerprint
            )
        );
    }
    return answer;
}

impl release_docs(tag: str) -> DocBundle | None {
    for line in read_status().lines {
        if line.tag == tag {
            return release_bundle(line);
        }
    }
    return None;
}

impl ninjaclaw_enabled -> tuple[bool, str] {
    if os.environ.get("NINJACLAW_ENABLED", "1").strip().lower()
        in ("0", "false", "no", "off") {
        return (False, "turned off on this server (NINJACLAW_ENABLED=0)");
    }
    if not os.environ.get("ANTHROPIC_API_KEY", "").strip() {
        return (False, "no model key on this server (ANTHROPIC_API_KEY is unset)");
    }
    status = read_status();
    if status.phase != "ready" {
        return (
            False,
            "warming up: the jac repo is " + (status.phase or "not cloned yet")
        );
    }
    return (True, "");
}

impl docs_catalog -> list[IndexDoc] {
    status = read_status();
    root_dir = checkout_root();
    if root_dir is None {
        return [];
    }
    cached = _CATALOG.get(status.checked_out);
    if cached is None {
        cached = docs_from_tree(root_dir / DOCS_PATH);
        _CATALOG.clear();
        _CATALOG[status.checked_out] = cached;
    }
    return cached;
}

impl tutorial_catalog -> list[IndexDoc] {
    return [
        index_doc(
            "tutorial",
            t.slug,
            t.title,
            "/jacyac/tutorials/" + t.slug,
            t.summary + "\n\n" + t.body
        )
        for t in claw_tutorials()
        if t.status == "published"
    ];
}

impl public_view(job: ClawJob, live: list[StepView] | None = None) -> JobView {
    view = job_view(job, live);
    if job.outcome == "ignored" {
        view.question = "";
        view.detail = "ignored: not a Jac question";
    }
    return view;
}

impl ninjaclaw_work_tick {
    for (job_id, outcome) in RUNNER.drain() {
        job = jobj(job_id);
        if isinstance(job, ClawJob) {
            record_outcome(job, outcome);
        }
    }
    (spec, _steps) = RUNNER.live();
    requeue_stale(spec.job_id if spec is not None else "");
    (ok, _why) = ninjaclaw_enabled();
    if not ok or RUNNER.busy() {
        return;
    }
    job = next_queued();
    if job is None {
        return;
    }
    if not take_budget() {
        record_outcome(
            job,
            Outcome(
                outcome="throttled",
                reply="I've reached today's answer budget; ask me again tomorrow."
            )
        );
        return;
    }
    job.status = "working";
    job.started_at = stamp();
    RUNNER.start(
        JobSpec(
            job_id=jid(job),
            question=job.question,
            asker=job.asker,
            source=job.source,
            repo_root=str(checkout_root() or ""),
            version=resolve_cli_version()
        ),
        tutorial_catalog() + docs_catalog(),
        run_pipeline
    );
}

impl ninjaclaw_submit(secret: str, asks: list[AskInput]) -> list[str] {
    if not secret_ok(secret) {
        return [];
    }
    return enqueue_asks(asks);
}

impl ninjaclaw_results(secret: str, job_ids: list[str]) -> list[JobReply] {
    if not secret_ok(secret) {
        return [];
    }
    return replies_for(job_ids);
}

impl ninjaclaw_activity -> Activity {
    (ok, why) = ninjaclaw_enabled();
    status = read_status();
    hub = find_hub() or ClawHub();
    (spec, live) = RUNNER.live();
    jobs = claw_jobs();
    current: JobView | None = None;
    queue: list[JobView] = [];
    recent: list[JobView] = [];
    for j in jobs {
        if j.status == "working" {
            current = public_view(
                j, live if spec is not None and spec.job_id == jid(j) else []
            );
        } elif j.status == "queued" {
            if len(queue) < QUEUE_LIMIT {
                queue.append(public_view(j));
            }
        }
    }
    finished = [
        j
        for j in jobs
        if j.status not in ("queued", "working")
    ];
    finished.sort(key=lambda (j: ClawJob) { j.finished_at; }, reverse=True);
    for j in finished[:RECENT_LIMIT] {
        recent.append(public_view(j));
    }
    state = "off" if not ok else ("working" if current is not None else "idle");
    if not ok and status.phase != "ready" and "warming" in why {
        state = "warming";
    }
    return Activity(
        enabled=ok,
        state=state,
        detail=why,
        repo_phase=status.phase,
        serving_version=status.serving_version or resolve_cli_version(),
        current=current,
        queue=queue,
        recent=recent,
        upkeep=UpkeepView(
            last_sweep_at=hub.last_sweep_at,
            swept_version=hub.swept_version,
            passed=hub.sweep_passed,
            stale=hub.sweep_stale,
            pr_state=hub.pr_state,
            pr_url=hub.pr_url,
            pr_note=hub.pr_note
        ),
        tutorials=len(
            [
                t
                for t in claw_tutorials()
                if t.status == "published"
            ]
        ),
        gaps=claw_gaps()
    );
}

impl ninjaclaw_job(job_id: str) -> JobView | None {
    job = jobj(job_id);
    if not isinstance(job, ClawJob) {
        return None;
    }
    (spec, live) = RUNNER.live();
    return public_view(job, live if spec is not None and spec.job_id == job_id else []);
}

impl ninjaclaw_tutorials -> list[TutorialCard] {
    return [
        tutorial_card(t)
        for t in claw_tutorials()
        if t.status != "removed"
    ];
}

impl ninjaclaw_tutorial(slug: str) -> TutorialView | None {
    t = tutorial_by_slug(slug);
    if t is None or t.status == "removed" {
        return None;
    }
    return TutorialView(
        card=tutorial_card(t),
        body=t.body,
        blocks=t.blocks,
        job_id=t.job_id,
        pr_url=t.pr_url
    );
}

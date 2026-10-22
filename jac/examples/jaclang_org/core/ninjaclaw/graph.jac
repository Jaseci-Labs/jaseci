import os;
import re;
import from datetime { datetime, UTC, timedelta }
import from jaclang.cli.manifest_route { resolve_cli_version }

node ClawNode {
    def __jac_access__ -> AccessLevel;
}

edge ClawEdge: ClawNode --> ClawNode {
    def __jac_access__ -> AccessLevel;
}

node ClawHub(ClawNode) {
    has created_at: str = "",
        day: str = "",
        jobs_today: int = 0,
        last_sweep_at: str = "",
        swept_version: str = "",
        sweep_passed: int = 0,
        sweep_stale: int = 0,
        pr_state: str = "",
        pr_url: str = "",
        pr_note: str = "";
}

node ClawJob(ClawNode) {
    has ask_key: str = "",
        tweet_id: str = "",
        asker: str = "",
        question: str = "",
        source: str = "",
        status: str = "queued",
        attempts: int = 0,
        outcome: str = "",
        reply: str = "",
        detail: str = "",
        tutorial_slug: str = "",
        links: list[LinkView] = [],
        consulted: list[str] = [],
        blocks: list[BlockView] = [],
        steps: list[StepView] = [],
        created_at: str = "",
        started_at: str = "",
        finished_at: str = "";
}

node ClawTutorial(ClawNode) {
    has slug: str = "",
        title: str = "",
        summary: str = "",
        body: str = "",
        status: str = "published",
        verified_version: str = "",
        blocks: list[BlockView] = [],
        answered: int = 0,
        askers: list[str] = [],
        job_id: str = "",
        created_at: str = "",
        pr_state: str = "",
        pr_url: str = "";
}

node ClawGap(ClawNode) {
    has question: str = "",
        job_id: str = "",
        created_at: str = "";
}

edge HasClaw: Node --> ClawHub {
    def __jac_access__ -> AccessLevel;
}

edge HasJob(ClawEdge): ClawHub --> ClawJob {}

edge HasTutorial(ClawEdge): ClawHub --> ClawTutorial {}

edge HasGap(ClawEdge): ClawHub --> ClawGap {}

edge Answered(ClawEdge): ClawTutorial --> ClawJob {}

glob DAILY_JOBS: int = int(os.environ.get("NINJACLAW_DAILY_JOBS", "200") or 200),
     STALE_WORKING_S: float = 900.0,
     MAX_ATTEMPTS: int = 2,
     RECENT_LIMIT: int = 30;

def find_hub -> ClawHub | None;

def claw_hub -> ClawHub;

def claw_gaps -> int;

def claw_jobs -> list[ClawJob];

def claw_tutorials -> list[ClawTutorial];

def tutorial_by_slug(slug: str) -> ClawTutorial | None;

def enqueue_asks(asks: list[AskInput]) -> list[str];

def next_queued -> ClawJob | None;

def take_budget -> bool;

def requeue_stale(running: str);

def record_outcome(job: ClawJob, outcome: Outcome);

def slug_for(title: str) -> str;

def job_view(job: ClawJob, live: list[StepView] | None = None) -> JobView;

def tutorial_card(t: ClawTutorial) -> TutorialCard;

def replies_for(job_ids: list[str]) -> list[JobReply];

impl ClawNode.__jac_access__ -> AccessLevel {
    return AccessLevel.READ;
}

impl ClawEdge.__jac_access__ -> AccessLevel {
    return AccessLevel.READ;
}

impl HasClaw.__jac_access__ -> AccessLevel {
    return AccessLevel.READ;
}

impl find_hub -> ClawHub | None {
    hubs = [root.shared->:HasClaw:->[?:ClawHub]];
    return hubs[0] if hubs else None;
}

impl claw_gaps -> int {
    hub = find_hub();
    return len([hub->:HasGap:->[?:ClawGap]]) if hub is not None else 0;
}

impl claw_hub -> ClawHub {
    found = find_hub();
    if found is not None {
        return found;
    }
    hub = ClawHub(created_at=stamp());
    root.shared +>:HasClaw():+> hub;
    return hub;
}

impl claw_jobs -> list[ClawJob] {
    hub = find_hub();
    if hub is None {
        return [];
    }
    jobs = [hub->:HasJob:->[?:ClawJob]];
    jobs.sort(key=lambda (j: ClawJob) { j.created_at; });
    return jobs;
}

impl claw_tutorials -> list[ClawTutorial] {
    hub = find_hub();
    if hub is None {
        return [];
    }
    found = [hub->:HasTutorial:->[?:ClawTutorial]];
    found.sort(key=lambda (t: ClawTutorial) { t.created_at; }, reverse=True);
    return found;
}

impl tutorial_by_slug(slug: str) -> ClawTutorial | None {
    for t in claw_tutorials() {
        if t.slug == slug {
            return t;
        }
    }
    return None;
}

impl enqueue_asks(asks: list[AskInput]) -> list[str] {
    hub = claw_hub();
    known: dict[str, str] = {};
    for j in [hub->:HasJob:->[?:ClawJob]] {
        known[j.ask_key] = jid(j);
    }
    ids: list[str] = [];
    for ask in asks {
        if ask.ask_key in known {
            ids.append(known[ask.ask_key]);
            continue;
        }
        job = hub +>:HasJob():+> ClawJob(
            ask_key=ask.ask_key,
            tweet_id=ask.tweet_id,
            asker=ask.asker,
            question=ask.question[:2000],
            source=ask.source,
            created_at=stamp()
        );
        known[ask.ask_key] = jid(job);
        ids.append(jid(job));
    }
    return ids;
}

impl next_queued -> ClawJob | None {
    for j in claw_jobs() {
        if j.status == "queued" {
            return j;
        }
    }
    return None;
}

impl take_budget -> bool {
    hub = claw_hub();
    today = stamp()[:10];
    if hub.day != today {
        hub.day = today;
        hub.jobs_today = 0;
    }
    if hub.jobs_today >= DAILY_JOBS {
        return False;
    }
    hub.jobs_today = hub.jobs_today + 1;
    return True;
}

impl requeue_stale(running: str) {
    cutoff = (datetime.now(UTC) - timedelta(seconds=STALE_WORKING_S)).replace(
        tzinfo=None
    ).isoformat()
        + "Z";
    for j in claw_jobs() {
        if j.status == "working" and jid(j) != running and j.started_at < cutoff {
            j.status = "queued";
            j.steps = j.steps
                + [
                    StepView(
                        at=stamp(),
                        phase="requeue",
                        text="the worker restarted mid-job; queued again"
                    )
                ];
        }
    }
}

impl slug_for(title: str) -> str {
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] or "tutorial";
    taken = {t.slug for t in claw_tutorials()};
    slug = base;
    n = 2;
    while slug in taken {
        slug = base + "-" + str(n);
        n += 1;
    }
    return slug;
}

impl record_outcome(job: ClawJob, outcome: Outcome) {
    hub = claw_hub();
    job.attempts = job.attempts + 1;
    if outcome.status == "failed" and job.attempts < MAX_ATTEMPTS {
        job.status = "queued";
        job.detail = outcome.detail;
        job.steps = job.steps
            + outcome.steps
            + [
                StepView(
                    at=stamp(),
                    phase="retry",
                    text="that attempt failed; queued to try once more"
                )
            ];
        return;
    }
    job.status = outcome.status;
    job.outcome = outcome.outcome;
    job.reply = outcome.reply;
    job.detail = outcome.detail;
    job.links = outcome.links;
    job.consulted = outcome.consulted;
    job.blocks = outcome.blocks;
    job.steps = job.steps + outcome.steps;
    job.finished_at = stamp();
    slug = outcome.tutorial_slug;
    draft = outcome.tutorial;
    if draft is not None {
        slug = draft.slug or slug_for(draft.title);
        made = hub +>:HasTutorial():+> ClawTutorial(
            slug=slug,
            title=draft.title,
            summary=draft.summary,
            body=draft.body,
            blocks=draft.blocks,
            verified_version=resolve_cli_version(),
            job_id=jid(job),
            created_at=stamp()
        );
        job.reply = job.reply.replace("{tutorial}", "/jacyac/tutorials/" + slug);
    }
    job.tutorial_slug = slug;
    if slug {
        t = tutorial_by_slug(slug);
        if t is not None {
            t +>:Answered():+> job;
            if job.asker and job.asker not in t.askers {
                t.askers = t.askers + [job.asker];
            }
            t.answered = len(t.askers);
        }
    }
    if outcome.outcome == "gap" {
        hub +>:HasGap():+> ClawGap(
            question=job.question[:400], job_id=jid(job), created_at=stamp()
        );
    }
}

impl job_view(job: ClawJob, live: list[StepView] | None = None) -> JobView {
    return JobView(
        job_id=jid(job),
        asker=job.asker,
        question=job.question,
        source=job.source,
        status=job.status,
        outcome=job.outcome,
        reply=job.reply,
        detail=job.detail,
        tutorial_slug=job.tutorial_slug,
        links=job.links,
        consulted=job.consulted,
        blocks=job.blocks,
        steps=job.steps + (live or []),
        created_at=job.created_at,
        finished_at=job.finished_at
    );
}

impl tutorial_card(t: ClawTutorial) -> TutorialCard {
    return TutorialCard(
        slug=t.slug,
        title=t.title,
        summary=t.summary,
        status=t.status,
        verified_version=t.verified_version,
        answered=t.answered,
        created_at=t.created_at
    );
}

impl replies_for(job_ids: list[str]) -> list[JobReply] {
    wanted = set(job_ids);
    out: list[JobReply] = [];
    for j in claw_jobs() {
        if jid(j) in wanted {
            out.append(
                JobReply(
                    job_id=jid(j),
                    ask_key=j.ask_key,
                    tweet_id=j.tweet_id,
                    status=j.status,
                    reply=j.reply
                )
            );
        }
    }
    return out;
}

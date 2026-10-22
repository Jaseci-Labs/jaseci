import argparse;
import asyncio;
import json;
import re;
import sys;
import from jaclang.server.bridge {
    BridgeError,
    BridgeRejected,
    BridgeTimeout,
    BridgeUnavailable
}

glob EXIT_OK: int = 0,
     EXIT_FAILURE: int = 1,
     EXIT_USAGE: int = 2,
     EXIT_UNAVAILABLE: int = 3,
     EXIT_TIMEOUT: int = 4,
     EXIT_REJECTED: int = 5;

glob START_HINT: str = "hint: start the site with `jac run web`";

def warn(text: str);

def _suffix(detail: str) -> str;

def explain_bridge_error(e: BridgeError) -> int;

impl warn(text: str) {
    print(text, file=sys.stderr);
}

impl _suffix(detail: str) -> str {
    return " (" + detail + ")" if detail else "";
}

impl explain_bridge_error(e: BridgeError) -> int {
    where = e.app + "." + e.name;
    if isinstance(e, BridgeUnavailable) {
        warn("jacorg: " + where + " is not reachable" + _suffix(e.detail));
        warn(START_HINT);
        return EXIT_UNAVAILABLE;
    }
    if isinstance(e, BridgeTimeout) {
        warn("jacorg: " + where + " timed out" + _suffix(e.detail));
        return EXIT_TIMEOUT;
    }
    if isinstance(e, BridgeRejected) {
        warn("jacorg: " + where + " rejected the call" + _suffix(e.detail));
        warn("hint: the site wants a signed-in identity for this command");
        return EXIT_REJECTED;
    }
    warn("jacorg: " + where + " failed" + _suffix(e.detail));
    return EXIT_FAILURE;
}

def render_status(st: DocsStatus) -> str;

async def run_docs(action: str) -> int;

impl render_status(st: DocsStatus) -> str {
    if not st.ready {
        return "docs: the graph is empty, the web app has not ingested a corpus yet";
    }
    lines: list[str] = [
        "docs: ready · latest " + st.latest_label + " · built " + st.built_at
    ];
    for v in st.versions {
        lines.append(
            "  "
                + v.label
                + "  jac "
                + v.jac_version
                + "  "
                + str(v.pages)
                + " pages  fetched "
                + v.fetched_at
        );
    }
    return "\n".join(lines);
}

impl run_docs(action: str) -> int {
    try {
        if action == "sync" {
            await docs_sync_tick();
            print(
                "docs sync: the web app checked its graph against the bundled corpus"
            );
        }
        print(render_status(await docs_status()));
        return EXIT_OK;
    } except BridgeError as e {
        return explain_bridge_error(e);
    }
}

obj FeedLine {
    has author: str = "",
        content: str = "",
        created_at: str = "",
        likes: int = 0,
        comments: int = 0;
}


def render_line(line: FeedLine) -> str;

async def run_feed(limit: int, query: str) -> int;

async def run_post(text: str) -> int;

impl render_line(line: FeedLine) -> str {
    stamp = line.created_at[:19].replace("T", " ");
    head = "@" + (line.author or "someone") + "  " + stamp;
    tail = str(line.likes) + " likes · " + str(line.comments) + " comments";
    return head + "  ·  " + tail + "\n    " + line.content;
}

impl run_feed(limit: int, query: str) -> int {
    try {
        res = await load_feed(search_query=query);
        rows = res.reports[0] if res.reports else [];
        if not rows {
            scope = " for \"" + query + "\"" if query else "";
            print(
                "your feed is empty"
                    + scope
                    + "; post something: jacorg post \"hello from the cli\""
            );
            return EXIT_OK;
        }
        for raw in rows[:limit] {
            print(
                render_line(
                    FeedLine(
                        author=raw.author_username,
                        content=raw.content,
                        created_at=raw.created_at,
                        likes=len(raw.likes),
                        comments=len(raw.comments)
                    )
                )
            );
        }
        if len(rows) > limit {
            print("... " + str(len(rows) - limit) + " more; raise --limit to see them");
        }
        return EXIT_OK;
    } except BridgeError as e {
        return explain_bridge_error(e);
    }
}

impl run_post(text: str) -> int {
    body = text.strip();
    if not body {
        warn("jacorg post: nothing to post");
        return EXIT_USAGE;
    }
    try {
        made = await create_tweet(content=body);
        posted = made.reports;
        if posted {
            tweet = posted[0];
            if isinstance(tweet, PostingDenied) {
                warn(tweet.message);
                return EXIT_REJECTED;
            }
            print(
                "posted as @" + (tweet.author_username or "you") + ": " + tweet.content
            );
        } else {
            print(
                "posted nothing: the site found no profile for this identity "
                    + "(open /jacyac once to create one)"
            );
        }
        return EXIT_OK;
    } except BridgeError as e {
        return explain_bridge_error(e);
    }
}

glob USER_AGENT: str = "jaclang.org cli scorer",
     MAX_TAR_BYTES: int = 52428800,
     MAX_MEMBER_BYTES: int = 2097152;

glob ERROR_TEXT: dict[str, str] = {
         "bad_ref": "expected owner/name or a github.com URL",
         "not_found": "GitHub knows no such repo (a private repo and a rate limit look the same; set GITHUB_TOKEN)",
         "fetch_failed": "could not download the default-branch tarball (over 50 MB, or GitHub is unreachable)",
         "not_jac": "no .jac files on the default branch, so there is nothing to score"
     };

obj ScoreResult {
    has ok: bool = False,
        error: str = "",
        meta: RepoMeta = RepoMeta(),
        an: RepoAnalysis = RepoAnalysis(),
        breakdown: ScoreBreakdown = ScoreBreakdown(),
        sha: str = "";
}

def parse_repo_ref(text: str) -> tuple[str, str] | None;

def score_repo(owner: str, name: str, quiet: bool = False) -> ScoreResult;

def as_dict(res: ScoreResult) -> dict[str, object];

def render(res: ScoreResult) -> str;

def run_score(repo: str, as_json: bool) -> int;

impl parse_repo_ref(text: str) -> tuple[str, str] | None {
    u = text.strip().rstrip("/");
    m = re.`match(
        r"^(?:https?://)?(?:www\.)?github\.com/([\w.\-]+)/([\w.\-]+?)(?:\.git)?$", u
    );
    if m is None {
        m = re.`match(r"^([\w.\-]+)/([\w.\-]+)$", u);
    }
    if m is None {
        return None;
    }
    return (m.group(1) as str, m.group(2) as str);
}

impl score_repo(owner: str, name: str, quiet: bool = False) -> ScoreResult {
    def say(note: str) {
        if not quiet {
            warn(note);
        }
    }
    meta = repo_meta(owner + "/" + name, USER_AGENT);
    if meta is None {
        return ScoreResult(error="not_found");
    }
    full = (meta.owner or owner) + "/" + (meta.name or name);
    sha = head_sha(full, meta.default_branch, USER_AGENT);
    ref = sha if sha != "" else meta.default_branch;
    say("fetching " + full + " @ " + ref[:12]);
    blob = download_tarball(full, ref, USER_AGENT, max_bytes=MAX_TAR_BYTES);
    if blob is None {
        return ScoreResult(error="fetch_failed", meta=meta);
    }
    say("unpacked " + mb_of(len(blob)) + ", analyzing");
    members = untar(
        blob,
        prefixes=[".github/workflows/", "docs/"],
        suffixes=[".jac", "jac.toml"],
        names=["readme.md", "license", "license.md", "license.txt"],
        max_member_bytes=MAX_MEMBER_BYTES
    );
    files: dict[str, str] = {};
    for rel in members.keys() {
        files[rel] = text_of(members[rel]);
    }
    an = analyze(files);
    stats = code_breakdown(blob);
    an.jac_bytes = stats[0];
    an.other_code_bytes = stats[1];
    if an.jac_files == 0 {
        return ScoreResult(error="not_jac", meta=meta);
    }
    breakdown = score(meta, an);
    breakdown.ai_review = optional_review(files);
    return ScoreResult(ok=True, meta=meta, an=an, breakdown=breakdown, sha=sha);
}

impl as_dict(res: ScoreResult) -> dict[str, object] {
    sc = res.breakdown;
    an = res.an;
    meta = res.meta;
    return {
        "repo": meta.full_name,
        "url": meta.html_url,
        "sha": res.sha,
        "stars": meta.stars,
        "forks": meta.forks,
        "topics": meta.topics,
        "pushed_at": meta.pushed_at,
        "jac_files": an.jac_files,
        "jac_lines": an.jac_lines,
        "jac_pct": an.jac_pct(),
        "features": {
            "osp": an.features.osp,
            "ai": an.features.ai,
            "cl": an.features.cl,
            "sv": an.features.sv,
            "na": an.features.na,
            "tests": an.features.tests
        },
        "readme": an.readme,
        "toml": an.toml,
        "license": an.license,
        "ci": an.ci,
        "docs": an.docs,
        "total": sc.total,
        "belt": sc.belt,
        "substance": sc.substance,
        "breadth": sc.breadth,
        "craft": sc.craft,
        "community": sc.community,
        "ai_review": {
            "summary": sc.ai_review.summary,
            "strength": {
                "observation": sc.ai_review.strength.observation,
                "evidence": sc.ai_review.strength.evidence
            },
            "opportunity": {
                "action": sc.ai_review.opportunity.action,
                "reason": sc.ai_review.opportunity.reason
            }
        }
            if sc.ai_review
            else None,
        "details": [
            {
                "category": p.category,
                "label": p.label,
                "pts": p.pts,
                "max": p.max,
                "note": p.note
            } for p in sc.details
        ]
    };
}

impl render(res: ScoreResult) -> str {
    sc = res.breakdown;
    an = res.an;
    meta = res.meta;
    lines: list[str] = [
        meta.full_name + "  " + str(sc.total) + "/100  " + sc.belt + " belt",
        "  substance "
            + str(sc.substance)
            + "/30 · breadth "
            + str(sc.breadth)
            + "/30 · craft "
            + str(sc.craft)
            + "/20 · community "
            + str(sc.community)
            + "/20",
        "  "
            + str(an.jac_files)
            + " jac files · "
            + str(an.jac_lines)
            + " lines · "
            + str(an.jac_pct())
            + "% jac · "
            + str(meta.stars)
            + " stars · "
            + str(meta.forks)
            + " forks"
    ];
    if res.sha and meta.html_url {
        lines.append("  scored at " + meta.html_url + "/tree/" + res.sha);
    }
    lines.append("");
    for p in sc.details {
        lines.append(
            f"  {p.category:<10} {p.label:<26} {p.pts:>5.1f} / {p.max:<4.0f} {p.note}"
        );
    }
    if sc.ai_review {
        lines.append("\n  AI code review · sampled files");
        lines.append("  " + sc.ai_review.summary);
        lines.append("  Strength: " + sc.ai_review.strength.observation);
        lines.append("  Evidence: " + sc.ai_review.strength.evidence);
        lines.append("  Next step: " + sc.ai_review.opportunity.action);
        lines.append("  " + sc.ai_review.opportunity.reason);
    }
    return "\n".join(lines);
}

impl run_score(repo: str, as_json: bool) -> int {
    parsed = parse_repo_ref(repo);
    if parsed is None {
        warn("jacorg score: " + ERROR_TEXT["bad_ref"] + ": " + repo);
        return EXIT_USAGE;
    }
    res = score_repo(parsed[0], parsed[1], quiet=as_json);
    if not res.ok {
        hint = ERROR_TEXT.get(res.error, res.error);
        if as_json {
            print(json.dumps({"ok": False, "error": res.error, "hint": hint}));
        } else {
            warn("jacorg score: " + hint);
        }
        return EXIT_FAILURE;
    }
    if as_json {
        print(json.dumps(as_dict(res), indent=2));
    } else {
        print(render(res));
    }
    return EXIT_OK;
}

glob PROG: str = "jacorg",
     DEFAULT_LIMIT: int = 20;

obj Invocation {
    has command: str = "",
        action: str = "",
        repo: str = "",
        as_json: bool = False,
        limit: int = DEFAULT_LIMIT,
        query: str = "",
        text: str = "";
}

def build_parser -> argparse.ArgumentParser;

def parse_args(argv: list[str]) -> Invocation;

async def dispatch(inv: Invocation) -> int;

async def main(argv: list[str]) -> int;

with entry:__main__ {
    sys.`exit(asyncio.run(main(sys.argv[1:])));
}

impl build_parser -> argparse.ArgumentParser {
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="The command-line face of jaclang.org. "
        "`score` runs offline; the rest talk to a running site."
    );
    commands = parser.add_subparsers(
        dest="command", metavar="<command>", required=True
    );
    scorer = commands.add_parser(
        "score", help="score a GitHub repo against the ninja rubric, offline"
    );
    scorer.add_argument("repo", help="owner/name or a github.com URL");
    scorer.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="print the breakdown as JSON"
    );
    docs = commands.add_parser("docs", help="the docs graph of a running site");
    docs.add_argument(
        "action",
        choices=["sync", "status"],
        help="sync: ask the site to ingest its bundled docs; status: what the graph holds"
    );
    feed = commands.add_parser(
        "feed", help="read your JacYac feed from a running site"
    );
    feed.add_argument(
        "--limit",
        `type=int,
        `default=DEFAULT_LIMIT,
        help="how many tweets to show (default " + str(DEFAULT_LIMIT) + ")"
    );
    feed.add_argument(
        "--search", dest="query", `default="", help="only tweets containing this text"
    );
    post = commands.add_parser("post", help="post to JacYac through a running site");
    post.add_argument("text", help="what to say");
    return parser;
}

impl parse_args(argv: list[str]) -> Invocation {
    parser = build_parser();
    ns = parser.parse_args(argv);
    inv = Invocation(
        command=str(getattr(ns, "command", "") or ""),
        action=str(getattr(ns, "action", "") or ""),
        repo=str(getattr(ns, "repo", "") or ""),
        as_json=bool(getattr(ns, "as_json", False)),
        limit=int(getattr(ns, "limit", DEFAULT_LIMIT)),
        query=str(getattr(ns, "query", "") or ""),
        text=str(getattr(ns, "text", "") or "")
    );
    if inv.limit < 1 {
        parser.error("--limit must be at least 1");
    }
    return inv;
}

impl dispatch(inv: Invocation) -> int {
    if inv.command == "score" {
        return run_score(inv.repo, inv.as_json);
    }
    if inv.command == "docs" {
        return await run_docs(inv.action);
    }
    if inv.command == "feed" {
        return await run_feed(inv.limit, inv.query);
    }
    if inv.command == "post" {
        return await run_post(inv.text);
    }
    warn("jacorg: unknown command " + inv.command);
    return EXIT_USAGE;
}

impl main(argv: list[str]) -> int {
    return await dispatch(parse_args(argv));
}

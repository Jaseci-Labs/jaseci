import asyncio;
import io;
import json;
import from contextlib { redirect_stderr }
import from types { SimpleNamespace }
import from unittest.mock { AsyncMock, patch }
import from core.ai { CodeReview, CodeInsight, NextStep }
import from core.timefmt { now_iso }

test "bridge failures map to distinct exit codes and hints" {
    buf = io.StringIO();
    with redirect_stderr(buf) {
        assert explain_bridge_error(
            BridgeUnavailable(
                app="web", name="docs_status", detail="connection refused"
            )
        )
            == EXIT_UNAVAILABLE;
        assert explain_bridge_error(BridgeTimeout(app="social_graph", name="load_feed"))
            == EXIT_TIMEOUT;
        assert explain_bridge_error(
            BridgeRejected(app="social_graph", name="create_tweet", detail="401")
        )
            == EXIT_REJECTED;
        assert explain_bridge_error(
            BridgeError(app="web", name="docs_sync_tick", detail="500")
        )
            == EXIT_FAILURE;
    }
    text = buf.getvalue();
    assert "web.docs_status is not reachable (connection refused)" in text;
    assert START_HINT in text;
    assert "social_graph.load_feed timed out" in text;
    assert "signed-in identity" in text;
    assert "web.docs_sync_tick failed (500)" in text;
}

test "exit codes are distinct" {
    codes = [
        EXIT_OK,
        EXIT_FAILURE,
        EXIT_USAGE,
        EXIT_UNAVAILABLE,
        EXIT_TIMEOUT,
        EXIT_REJECTED
    ];
    assert len(set(codes)) == len(codes);
}

test "posting quota reports the retry message and returns a rejection exit code" {
    result = SimpleNamespace(reports=[PostingDenied("Try again in 10 seconds.", 10)]);
    with patch(
        run_post.__module__ + ".create_tweet", new=AsyncMock(return_value=result)
    ), patch(run_post.__module__ + ".warn") as warning {
        assert asyncio.run(run_post("hello")) == EXIT_REJECTED;
        warning.assert_called_once_with("Try again in 10 seconds.");
    }
}

test "AI review appears in text and JSON without changing score" {
    res = sample_result();
    total = res.breakdown.total;
    res.breakdown.ai_review = CodeReview(
        summary="A typed task graph.",
        strength=CodeInsight(observation="Typed state.", evidence="app.jac: Task"),
        opportunity=NextStep(action="Test traversal.", reason="Protect behavior.")
    );
    assert "A typed task graph." in render(res);
    assert as_dict(res)["ai_review"]["strength"]["evidence"] == "app.jac: Task";
    assert as_dict(res)["total"] == total;
}


glob SAMPLE: dict[str, str] = {
         "app.jac": "node Task { has title: str; }\nwalker:pub add { can go with Root entry { root ++> Task(); } }\n",
         "ui.jac": "def:pub app -> JsxElement { return <div>hi</div>; }\n",
         "app.test.jac": "test \"adds\" { assert True; }\n",
         "jac.toml": "[project]\nname = \"dojo\"\n",
         "readme.md": "# dojo\n\nA sample.\n",
         "license": "MIT\n"
     };

def sample_result -> ScoreResult;

test "parse repo ref accepts slugs and github urls" {
    assert parse_repo_ref("jaseci-labs/jac") == ("jaseci-labs", "jac");
    assert parse_repo_ref("https://github.com/jaseci-labs/jac.git")
        == ("jaseci-labs", "jac");
    assert parse_repo_ref("github.com/jaseci-labs/jac/") == ("jaseci-labs", "jac");
    assert parse_repo_ref("  Jaseci-Labs/jac  ") == ("Jaseci-Labs", "jac");
}

test "parse repo ref rejects everything else" {
    assert parse_repo_ref("jac") is None;
    assert parse_repo_ref("https://gitlab.com/a/b") is None;
    assert parse_repo_ref("a/b/c") is None;
    assert parse_repo_ref("") is None;
}

test "as dict is json and mirrors the breakdown row for row" {
    res = sample_result();
    back = json.loads(json.dumps(as_dict(res)));
    assert back["repo"] == "acme/dojo";
    assert back["sha"] == "abc123def456789";
    assert back["total"] == res.breakdown.total;
    assert back["belt"] == res.breakdown.belt;
    assert back["jac_pct"] == 80;
    assert back["jac_files"] == res.an.jac_files;
    assert back["features"]["osp"];
    assert back["features"]["cl"];
    assert not back["features"]["na"];
    assert len(back["details"]) == len(res.breakdown.details);
    assert back["details"][0]["label"] == res.breakdown.details[0].label;
}

test "render names the repo the total the belt and every rubric line" {
    res = sample_result();
    out = render(res);
    assert out.startswith("acme/dojo  " + str(res.breakdown.total) + "/100  ");
    assert res.breakdown.belt + " belt" in out;
    assert "https://github.com/acme/dojo/tree/abc123def456789" in out;
    for p in res.breakdown.details {
        assert p.label in out;
    }
}

test "run score refuses a bad ref before touching the network" {
    assert run_score("not a repo", False) == EXIT_USAGE;
    assert run_score("", True) == EXIT_USAGE;
}

test "every scorer failure has a human hint" {
    for key in ["bad_ref", "not_found", "fetch_failed", "not_jac"] {
        assert len(ERROR_TEXT[key]) > 20;
    }
}

impl sample_result -> ScoreResult {
    meta = RepoMeta(
        full_name="acme/dojo",
        owner="acme",
        name="dojo",
        html_url="https://github.com/acme/dojo",
        stars=12,
        forks=3,
        topics=["jac"],
        pushed_at=now_iso()
    );
    an = analyze(SAMPLE);
    an.jac_bytes = 4000;
    an.other_code_bytes = 1000;
    return ScoreResult(
        ok=True, meta=meta, an=an, breakdown=score(meta, an), sha="abc123def456789"
    );
}

def usage_error(argv: list[str]) -> bool;

test "score takes a repo and an optional json flag" {
    inv = parse_args(["score", "jaseci-labs/jac"]);
    assert inv.command == "score";
    assert inv.repo == "jaseci-labs/jac";
    assert not inv.as_json;
    assert parse_args(["score", "jaseci-labs/jac", "--json"]).as_json;
    assert usage_error(["score"]);
}

test "docs takes exactly sync or status" {
    assert parse_args(["docs", "sync"]).action == "sync";
    assert parse_args(["docs", "status"]).action == "status";
    assert usage_error(["docs", "purge"]);
    assert usage_error(["docs"]);
}

test "feed defaults its limit and accepts a search" {
    plain = parse_args(["feed"]);
    assert plain.command == "feed";
    assert plain.limit == DEFAULT_LIMIT;
    assert plain.query == "";
    narrowed = parse_args(["feed", "--limit", "5", "--search", "#jac"]);
    assert narrowed.limit == 5;
    assert narrowed.query == "#jac";
    assert usage_error(["feed", "--limit", "0"]);
    assert usage_error(["feed", "--limit", "five"]);
}

test "post keeps its text verbatim" {
    assert parse_args(["post", "hello  from the cli"]).text == "hello  from the cli";
    assert usage_error(["post"]);
}

test "a missing or unknown command is a usage error" {
    assert usage_error([]);
    assert usage_error(["dance"]);
}

test "the parser names itself jacorg and lists every command" {
    buf = io.StringIO();
    with redirect_stderr(buf) {
        try {
            parse_args(["dance"]);
        } except SystemExit {}
    }
    text = buf.getvalue();
    assert text.startswith("usage: jacorg");
    for name in ["score", "docs", "feed", "post"] {
        assert name in text;
    }
}

impl usage_error(argv: list[str]) -> bool {
    buf = io.StringIO();
    exited = False;
    with redirect_stderr(buf) {
        try {
            parse_args(argv);
        } except SystemExit {
            exited = True;
        }
    }
    return exited and "usage:" in buf.getvalue();
}

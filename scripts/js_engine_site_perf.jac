"""Hold the js_engine's speed on the jaclang.org site build to its ratio to node's.

`measure` runs the site's vite build (the client bundle `jac build --as client
web` makes) under node with its optimizing tiers off (an interpreter, like the
engine), under the engine, and under plain node, the three interleaved `runs`
times on one runner. Each side keeps its fastest run: noise on a runner only
ever adds time. The engine's bundle must match node's file for file, or the
ratio would compare two different builds.

`gate` divides the engine's time by no-JIT node's, which cancels most of the
runner's own speed, and holds that ratio to the baseline in
.github/js-engine-site-perf.json. Above `fail_ratio` times the baseline it
fails. Below `record_ratio` times the baseline it writes the measured ratio as
the new baseline for CI to commit, as it does when there is no baseline yet or
node's version changed. In between it passes and leaves the baseline alone, so
noise neither fails a run nor ratchets the baseline down; several small
regressions still fail once together they cross `fail_ratio`. Plain node's
ratio and the peak RSS of each side are recorded, not gated.
"""

import argparse;
import hashlib;
import json;
import math;
import os;
import shutil;
import subprocess;
import sys;
import threading;
import time;
import from pathlib { Path }

glob NO_JIT_FLAGS: list[str] = ["--no-opt", "--no-sparkplug", "--no-maglev"],
     SIDES: list[str] = ["node-nojit", "engine", "node"],
     VITE_CONFIG: str = "configs/vite.config.js",
     RUN_TIMEOUT_SECONDS: float = 1800.0;

def finite_positive(value: any) -> bool {
    return isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value > 0;
}

obj Policy {
    has runs: int = 3,
        fail_ratio: float = 1.05,
        record_ratio: float = 0.95,
        baseline: dict[str, any] | None = None;

    def postinit {
        if not isinstance(self.runs, int) or self.runs < 1 {
            raise ValueError("runs must be a positive integer");
        }
        if not finite_positive(self.fail_ratio) or self.fail_ratio <= 1 {
            raise ValueError("fail_ratio must be a finite number above 1");
        }
        if not finite_positive(self.record_ratio) or self.record_ratio >= 1 {
            raise ValueError("record_ratio must be a positive number below 1");
        }
        if self.baseline is not None
            and not finite_positive(self.baseline.get("ratio")) {
            raise ValueError("the baseline needs a finite positive ratio");
        }
    }
}

def load_policy(path: Path) -> Policy {
    raw = json.loads(path.read_text());
    return Policy(
        runs=raw.get("runs", 3),
        fail_ratio=raw.get("fail_ratio", 1.05),
        record_ratio=raw.get("record_ratio", 0.95),
        baseline=raw.get("baseline")
    );
}

def write_json(path: Path, value: any) {
    path.parent.mkdir(parents=True, exist_ok=True);
    temporary = path.with_suffix(".tmp");
    temporary.write_text(json.dumps(value, indent=2) + "\n");
    temporary.replace(path);
}

"""A digest of every file under `top`, by relative path and content."""
def tree_digest(top: Path) -> str {
    digest = hashlib.sha256();
    for path in sorted([p for p in top.rglob("*") if p.is_file()]) {
        digest.update(str(path.relative_to(top)).encode());
        digest.update(b"\0");
        digest.update(path.read_bytes());
        digest.update(b"\0");
    }
    return digest.hexdigest();
}

"""Run `command`; return its wall seconds, peak RSS in MiB and exit status.

A command still running after `timeout` seconds is killed, which shows as a
negative status.
"""
def timed_run(
    command: list[str], cwd: Path, env: dict[str, str], log: Path, timeout: float
) -> tuple[float, float, int] {
    log.parent.mkdir(parents=True, exist_ok=True);
    with open(log, "wb") as out {
        start = time.monotonic();
        proc = subprocess.Popen(
            command, cwd=cwd, env=env, stdout=out, stderr=subprocess.STDOUT
        );
        killer = threading.Timer(timeout, proc.kill);
        killer.start();
        try {
            # The rusage wait4 returns is this child's own; the checker's
            # typeshed does not resolve the POSIX-only stub.
            waited: any = getattr(os, "wait4")(proc.pid, 0);
        } finally {
            killer.cancel();
        }
        seconds = time.monotonic() - start;
    }
    status: int = waited[1];
    peak_kib: int = waited[2].ru_maxrss;
    proc.returncode = os.waitstatus_to_exitcode(status);
    return (seconds, peak_kib / 1024.0, proc.returncode);
}

def engine_executable -> str {
    import from jaclang.artifacts.router { resolve }
    if resolve("js-engine").found is None {
        raise ValueError("no js_engine is installed (jac native build js-engine)");
    }
    import from jaclang.client.js_engine { node_executable }
    return node_executable();
}

def runtime_version(executable: str) -> str {
    done = subprocess.run(
        [executable, "--version"], capture_output=True, text=True, timeout=60
    );
    return done.stdout.strip();
}

def side_command(side: str, node_bin: str, engine_bin: str, vite: Path) -> list[str] {
    tail = [str(vite), "build", "--config", VITE_CONFIG];
    if side == "node-nojit" {
        return [node_bin] + NO_JIT_FLAGS + tail;
    }
    if side == "node" {
        return [node_bin] + tail;
    }
    return [engine_bin] + tail;
}

def side_env(executable: str) -> dict[str, str] {
    env = dict(os.environ);
    env["PATH"] = os.path.dirname(executable) + os.pathsep + env.get("PATH", "");
    return env;
}

def run_url -> (str | None) {
    server = os.environ.get("GITHUB_SERVER_URL");
    repo = os.environ.get("GITHUB_REPOSITORY");
    run_id = os.environ.get("GITHUB_RUN_ID");
    if not (server and repo and run_id) {
        return None;
    }
    return f"{server}/{repo}/actions/runs/{run_id}";
}

"""Time the site build on every side `runs` times; write and return the runs."""
def measure(
    client: Path,
    node_bin: str,
    engine_bin: str,
    runs: int,
    dist: str,
    output: Path,
    timeout: float = RUN_TIMEOUT_SECONDS
) -> dict[str, any] {
    vite = client / "node_modules" / "vite" / "bin" / "vite.js";
    if not vite.is_file() {
        raise ValueError(f"no vite under {client / 'node_modules'}");
    }
    if not (client / VITE_CONFIG).is_file() {
        raise ValueError(f"no {VITE_CONFIG} under {client}; build the client first");
    }
    if os.path.realpath(node_bin) == os.path.realpath(engine_bin) {
        raise ValueError("node and the engine resolve to the same executable");
    }
    samples: list[dict[str, any]] = [];
    digests: dict[str, str] = {};
    for index in range(runs) {
        for side in SIDES {
            label = f"{side} run {index + 1}";
            executable = engine_bin if side == "engine" else node_bin;
            (seconds, rss_mib, code) = timed_run(
                side_command(side, node_bin, engine_bin, vite),
                client,
                side_env(executable),
                output / "logs" / f"{side}-{index + 1}.log",
                timeout
            );
            print(f"{label}: {seconds:.2f}s, {rss_mib:.0f} MiB, exit {code}", flush=True);
            if code != 0 {
                raise ValueError(f"{label} exited {code}; see logs/{side}-{index + 1}.log");
            }
            out_dir = client / dist;
            if not out_dir.is_dir() {
                raise ValueError(f"{label} left no {dist} under {client}");
            }
            digest = tree_digest(out_dir);
            if side in digests and digests[side] != digest {
                raise ValueError(f"{label} built a different bundle than its first run");
            }
            digests[side] = digest;
            samples.append(
                {
                    "side": side,
                    "run": index + 1,
                    "seconds": round(seconds, 3),
                    "rss_mib": round(rss_mib, 1)
                }
            );
        }
    }
    if len(set(digests.values())) != 1 {
        raise ValueError(
            "the engine's bundle differs from node's; the times compare different builds"
        );
    }
    results: dict[str, any] = {
        "node": runtime_version(node_bin),
        "engine": engine_bin,
        "samples": samples,
        "commit": os.environ.get("GITHUB_SHA"),
        "run_url": run_url(),
        "runner": os.environ.get("RUNNER_NAME")
    };
    write_json(output / "results.json", results);
    return results;
}

"""Each side's fastest run and largest peak RSS, and the engine's ratios."""
def summarize(results: dict[str, any]) -> dict[str, any] {
    best: dict[str, float] = {};
    peak: dict[str, float] = {};
    for sample in results["samples"] {
        side = sample["side"];
        best[side] = min(best.get(side, math.inf), float(sample["seconds"]));
        peak[side] = max(peak.get(side, 0.0), float(sample["rss_mib"]));
    }
    for side in SIDES {
        if not finite_positive(best.get(side)) {
            raise ValueError(f"the results carry no {side} run");
        }
    }
    return {
        "runs": len([s for s in results["samples"] if s["side"] == "engine"]),
        "ratio": round(best["engine"] / best["node-nojit"], 4),
        "jit_ratio": round(best["engine"] / best["node"], 4),
        "engine_seconds": best["engine"],
        "node_nojit_seconds": best["node-nojit"],
        "node_seconds": best["node"],
        "engine_rss_mib": peak["engine"],
        "node_nojit_rss_mib": peak["node-nojit"],
        "node_rss_mib": peak["node"],
        "node": results.get("node"),
        "commit": results.get("commit"),
        "run_url": results.get("run_url"),
        "runner": results.get("runner")
    };
}

obj Verdict {
    has status: str,
        message: str,
        record: bool;

    def failed -> bool {
        return self.status == "regressed";
    }
}

def judge(policy: Policy, summary: dict[str, any]) -> Verdict {
    ratio = float(summary["ratio"]);
    held = policy.baseline;
    if held is None {
        return Verdict(
            status="recorded",
            message=f"no baseline yet; recording {ratio:.3f}",
            record=True
        );
    }
    was = float(held["ratio"]);
    if held.get("node") != summary.get("node") {
        return Verdict(
            status="recorded",
            message=(
                f"node changed from {held.get('node')} to {summary.get('node')}; "
                f"recording {ratio:.3f} without comparing it to {was:.3f}"
            ),
            record=True
        );
    }
    change = f"{ratio:.3f} against the baseline's {was:.3f} ({ratio / was - 1:+.1%})";
    if ratio > was * policy.fail_ratio {
        return Verdict(
            status="regressed",
            message=f"the engine got slower relative to node: {change}",
            record=False
        );
    }
    if ratio < was * policy.record_ratio {
        return Verdict(
            status="improved", message=f"recording the faster {change}", record=True
        );
    }
    return Verdict(status="pass", message=f"within the band: {change}", record=False);
}

def _cell(value: any, fmt: str) -> str {
    return "" if value is None else format(value, fmt);
}

def summary_markdown(
    policy: Policy, summary: dict[str, any], verdict: Verdict
) -> str {
    held = policy.baseline or {};
    rows: list[tuple[str, str, str]] = [
        ("engine / node no-JIT (gated)", "ratio", ".3f"),
        ("engine / node", "jit_ratio", ".3f"),
        ("engine (s)", "engine_seconds", ".2f"),
        ("node no-JIT (s)", "node_nojit_seconds", ".2f"),
        ("node (s)", "node_seconds", ".2f"),
        ("engine peak RSS (MiB)", "engine_rss_mib", ".0f"),
        ("node no-JIT peak RSS (MiB)", "node_nojit_rss_mib", ".0f")
    ];
    lines = [
        "## js_engine site build vs node",
        "",
        f"**{verdict.status}**: {verdict.message}. Fails above "
        f"{policy.fail_ratio:g}x the baseline ratio, records below "
        f"{policy.record_ratio:g}x. Fastest of {summary.get('runs')} runs per side, "
        f"node {summary.get('node')}.",
        "",
        "| | Now | Baseline |",
        "| --- | ---: | ---: |"
    ];
    for (title, key, fmt) in rows {
        lines.append(
            f"| {title} | {_cell(summary.get(key), fmt)} | {_cell(held.get(key), fmt)} |"
        );
    }
    if held.get("commit") {
        lines.append("");
        lines.append(f"Baseline recorded at {held.get('commit')}.");
    }
    return "\n".join(lines) + "\n";
}

def append_env_file(variable: str, text: str) {
    target = os.environ.get(variable);
    if target {
        with open(target, "a") as stream {
            stream.write(text);
        }
    }
}

"""Judge the measured runs against the policy's baseline; 1 when it regressed.

The table goes to `output`/summary.md and the step summary, and a recording
verdict writes the new baseline object to `output`/baseline.json; the verdict
lands in GITHUB_OUTPUT (`status`, `record`) for the workflow.
"""
def gate(policy_path: Path, results_path: Path, output: Path) -> int {
    policy = load_policy(policy_path);
    summary = summarize(json.loads(results_path.read_text()));
    verdict = judge(policy, summary);
    if verdict.record {
        write_json(output / "baseline.json", summary);
    }
    markdown = summary_markdown(policy, summary, verdict);
    output.mkdir(parents=True, exist_ok=True);
    (output / "summary.md").write_text(markdown);
    print(markdown, flush=True);
    append_env_file("GITHUB_STEP_SUMMARY", markdown);
    append_env_file(
        "GITHUB_OUTPUT",
        f"status={verdict.status}\nrecord={'true' if verdict.record else 'false'}\n"
    );
    if verdict.failed() {
        print(f"::error title=js_engine site perf::{verdict.message}", flush=True);
        return 1;
    }
    if verdict.record {
        print(f"::notice title=js_engine site perf::{verdict.message}", flush=True);
    }
    return 0;
}

def main(argv: list[str] | None = None) -> int {
    repo = Path(__file__).resolve().parent.parent;
    parser = argparse.ArgumentParser(description=__doc__);
    commands = parser.add_subparsers(dest="command", required=True);
    timing = commands.add_parser("measure", help="time the site build on each side");
    timing.add_argument("--client", type=Path, required=True, help="the site's .jac/client");
    timing.add_argument(
        "--dist", `default="web/dist", help="the bundle vite writes, under --client"
    );
    timing.add_argument(
        "--node", `default=None, help="node to compare with (default: node on PATH)"
    );
    timing.add_argument(
        "--engine",
        `default=None,
        help="the engine run as node (default: the installed one)"
    );
    timing.add_argument(
        "--runs", type=int, `default=None, help="runs per side (default: the policy's)"
    );
    timing.add_argument("--timeout", type=float, `default=RUN_TIMEOUT_SECONDS);
    judging = commands.add_parser("gate", help="hold the measured ratio to the baseline");
    judging.add_argument(
        "--results", type=Path, `default=None, help="default: --output/results.json"
    );
    for sub in [timing, judging] {
        sub.add_argument(
            "--policy", type=Path, `default=repo / ".github" / "js-engine-site-perf.json"
        );
        sub.add_argument(
            "--output",
            type=Path,
            `default=Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "js-engine-site-perf"
        );
    }
    args = parser.parse_args(argv);
    try {
        if args.command == "measure" {
            node_bin = args.node or shutil.which("node");
            if not node_bin {
                raise ValueError("no node on PATH; pass --node");
            }
            measure(
                args.client.resolve(),
                node_bin,
                args.engine or engine_executable(),
                args.runs or load_policy(args.policy).runs,
                args.dist,
                args.output.resolve(),
                args.timeout
            );
            return 0;
        }
        return gate(
            args.policy, args.results or args.output / "results.json", args.output
        );
    } except (OSError, ValueError, KeyError, TypeError) as error {
        print(f"::error title=js_engine site perf::{error}", flush=True);
        return 1;
    }
}

with entry:__main__ {
    sys.`exit(main());
}

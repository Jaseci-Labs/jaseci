import os;
import re;
import shutil;
import subprocess;
import sys;
import tempfile;
import from pathlib { Path }
import from jaclang.jac0core.handoff { handoff }
import from jaclang.jac0core.cache_paths { get_cache_home }

glob CHECK_TIMEOUT_S: int = 180,
     RUN_TIMEOUT_S: int = 60,
     CPU_LIMIT_S: int = 90,
     DETAIL_LIMIT: int = 600,
     SERVER_MARKERS: list[str] = [
         "walker:pub",
         "walker:priv",
         "walker:protect",
         "def:pub",
         "def:priv",
         "def:protect",
         "by llm",
         "JsxElement",
         "jac start",
         "@schedule"
     ];

def code_blocks(markdown: str) -> list[str];

def block_mode(code: str) -> str;

def jac_binary -> str;

def sandbox_env(home: str) -> dict[str, str];

def sandbox_prefix -> list[str];

def limit_resources -> None;

def run_jac(args: list[str], cwd: Path, timeout: int) -> tuple[bool, str];

def verify_block(index: int, code: str) -> BlockView;

def verify_markdown(markdown: str, note: Callable) -> list[BlockView];

impl code_blocks(markdown: str) -> list[str] {
    return [
        (m.group(1) as str).strip("\n")
        for m in re.finditer(r"```jac[^\n]*\n(.*?)```", markdown, re.DOTALL)
    ];
}

impl block_mode(code: str) -> str {
    for marker in SERVER_MARKERS {
        if marker in code {
            return "check";
        }
    }
    return "run" if "with entry" in code else "check";
}

impl jac_binary -> str {
    return shutil.which("jac") or "jac";
}

impl sandbox_env(home: str) -> dict[str, str] {
    keep = ["PATH", "LANG", "LC_ALL", "TMPDIR", "SYSTEMROOT"];
    env: dict[str, str] = {
        k: os.environ[k]
        for k in keep
        if k in os.environ
    };
    env["HOME"] = home;
    env["JAC_CACHE_HOME"] = str(get_cache_home());
    env["JAC_TEST_JOBS"] = "0";
    env["NO_COLOR"] = "1";
    return env;
}

impl sandbox_prefix -> list[str] {
    unshare = shutil.which("unshare");
    if sys.platform.startswith("linux") and unshare {
        probe = subprocess.run(
            [unshare, "-rn", "true"], capture_output=True, timeout=10
        );
        if probe.returncode == 0 {
            return [unshare, "-rn"];
        }
    }
    return [];
}

impl limit_resources -> None {
    import resource;
    try {
        resource.setrlimit(resource.RLIMIT_CPU, (CPU_LIMIT_S, CPU_LIMIT_S));
    } except Exception {}
    if sys.platform.startswith("linux") {
        try {
            gib = 2 * 1024 * 1024 * 1024;
            resource.setrlimit(resource.RLIMIT_AS, (gib, gib));
        } except Exception {}
    }
}

impl run_jac(args: list[str], cwd: Path, timeout: int) -> tuple[bool, str] {
    try {
        done = subprocess.run(
            sandbox_prefix() + [jac_binary()] + args,
            cwd=str(cwd),
            env=sandbox_env(str(cwd / ".home")),
            capture_output=True,
            text=True,
            timeout=timeout,
            preexec_fn=limit_resources
        );
    } except subprocess.TimeoutExpired {
        return (False, "timed out after " + str(timeout) + " s");
    }
    output = (done.stdout or "") + (done.stderr or "");
    lines = [
        ln
        for ln in output.splitlines()
        if "jac dev mode" not in ln and ln.strip()
    ];
    if done.returncode != 0 {
        errors = [
            ln
            for ln in lines
            if "rror" in ln or "-->" in ln
        ]
            or lines;
        return (False, "\n".join(errors[-8:])[:DETAIL_LIMIT]);
    }
    return (True, "\n".join(lines[-3:])[:DETAIL_LIMIT]);
}

impl verify_block(index: int, code: str) -> BlockView {
    mode = block_mode(code);
    with tempfile.TemporaryDirectory(prefix="ninjaclaw-") as tmp {
        work = Path(tmp);
        (work / ".home").mkdir();
        toml = '[project]\nname = "ninjaclaw_check"\n';
        source = str(handoff().get("compiler_source") or "");
        if source {
            toml = toml + '\n[dev]\njaclang_source = "' + source + '"\n';
        }
        (work / "jac.toml").write_text(toml, encoding="utf-8");
        (work / "main.jac").write_text(code + "\n", encoding="utf-8");
        (ok, detail) = run_jac(
            ["check", "main.jac", "--nowarn"], work, CHECK_TIMEOUT_S
        );
        if not ok or mode == "check" {
            return BlockView(
                index=index, mode=mode, ok=ok, detail="" if ok else detail
            );
        }
        (ok, detail) = run_jac(["run", "main.jac"], work, RUN_TIMEOUT_S);
        return BlockView(index=index, mode=mode, ok=ok, detail="" if ok else detail);
    }
}

impl verify_markdown(markdown: str, note: Callable) -> list[BlockView] {
    results: list[BlockView] = [];
    blocks = code_blocks(markdown);
    for (i, code) in enumerate(blocks) {
        note(
            "verify",
            "block " + str(i + 1) + " of " + str(len(blocks)) + ": " + block_mode(code)
        );
        result = verify_block(i, code);
        note(
            "verify",
            "block "
                + str(i + 1)
                + (" passed" if result.ok else " failed: " + result.detail[:160])
        );
        results.append(result);
    }
    return results;
}

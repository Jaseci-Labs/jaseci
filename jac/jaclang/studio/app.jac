import os;
import sys;
import json;
import time;

glob ACTIONS: list[str] = ["model", "ask", "agents", "sessions", "mcp"];

def out(text: str);

def err(text: str);

def run_studio(
    action: str,
    args: list[str],
    agent: str,
    session: str,
    as_json: bool,
    directory: str
) -> int;

def cmd_model(root_dir: str, args: list[str], as_json: bool) -> int;

def format_summary(model: ProjectModel) -> str;

def cmd_intel(directory: str, args: list[str]) -> int;

def paint_line(text: str, spans: list[Span]) -> str;

def wait_ready(ci: CodeIntel, path: str, timeout: float = 600.0) -> str;

def wait_tickets(
    ci: CodeIntel, tickets: list[int], timeout: float = 120.0
) -> dict[int, any];

def format_module(model: ProjectModel, key: str) -> str;

impl out(text: str) {
    sys.stdout.write(text + "\n");
    sys.stdout.flush();
}

impl err(text: str) {
    sys.stderr.write(text + "\n");
    sys.stderr.flush();
}

impl run_studio(
    action: str,
    args: list[str],
    agent: str,
    session: str,
    as_json: bool,
    directory: str
) -> int {
    rest: list[str] = [];
    i = 0;
    while i < len(args) {
        a = args[i];
        nxt = args[i + 1] if i + 1 < len(args) else "";
        if a in ["-a", "--agent"] and nxt {
            agent = nxt;
            i += 2;
        } elif a in ["-s", "--session"] and nxt {
            session = nxt;
            i += 2;
        } elif a in ["-d", "--dir"] and nxt {
            directory = nxt;
            i += 2;
        } elif a == "--json" {
            as_json = True;
            i += 1;
        } elif a.startswith("--agent=") {
            agent = a.split("=", 1)[1];
            i += 1;
        } elif a.startswith("--session=") {
            session = a.split("=", 1)[1];
            i += 1;
        } elif a.startswith("--dir=") {
            directory = a.split("=", 1)[1];
            i += 1;
        } else {
            rest.append(a);
            i += 1;
        }
    }
    args = rest;
    if action == "intel" {
        return cmd_intel(directory, args);
    }
    root_dir = find_project_root(directory or os.getcwd());
    if action == "model" {
        return cmd_model(root_dir, args, as_json);
    }
    if action == "" {
        err("jac studio: the workspace UI is not built yet; try `jac studio model`.");
        return 1;
    }
    err(
        f"jac studio: unknown action '{action}'. Expected one of: " + ", ".join(ACTIONS)
    );
    return 2;
}

impl cmd_model(root_dir: str, args: list[str], as_json: bool) -> int {
    model = ProjectModel(root_dir=root_dir);
    show = sys.stderr.isatty();
    def progress(n: int, total: int, key: str) {
        if show and (n % 25 == 0 or n == total) {
            sys.stderr.write(f"\r  indexing {n}/{total} modules");
            sys.stderr.flush();
        }
    }
    model.build(on_progress=progress);
    if show {
        sys.stderr.write("\r" + " " * 40 + "\r");
    }
    target = args[0] if args else "";
    if target and target not in model.modules {
        hits = model.search(target, limit=1, kinds=["module"]);
        if hits {
            target = hits[0].key;
        }
    }
    if as_json {
        out(json.dumps(model.to_dict(target), indent=2));
        return 0;
    }
    if target {
        if target not in model.modules {
            err(f"jac studio model: no module matches '{args[0]}'");
            return 1;
        }
        out(format_module(model, target));
        return 0;
    }
    out(format_summary(model));
    return 0;
}

impl format_summary(model: ProjectModel) -> str {
    st = model.stats();
    lines = [
        f"{model.root_dir}",
        f"  {st['modules']} modules in {st['packages']} packages, {st[
            'external'
        ]} external providers",
        f"  {st['wires']} wires, {st['rules']} rules, {len(
            model.archwires
        )} archwire.jac files",
        "  symbols: "
            + ", ".join([f"{v} {k}" for (k, v) in sorted(st["symbols"].items())]),
        f"  discovered in {st['discover_secs']}s, indexed in {st['index_secs']}s"
    ];
    if st["errors"] {
        lines.append(f"  {st['errors']} modules failed to parse");
    }
    tops = [
        k
        for k in model.packages
        if "." not in k
    ];
    if tops {
        lines.append("  top-level packages: " + ", ".join(sorted(tops)));
    }
    return "\n".join(lines);
}

impl format_module(model: ProjectModel, key: str) -> str {
    mod = model.modules[key];
    lines = [f"{key}  ({mod.file})"];
    rules = model.rules_for(key);
    if rules {
        lines.append("  governed by: " + ", ".join([r.name for r in rules]));
    }
    provs = model.providers(key);
    if provs {
        lines.append("  feeds this:");
        for w in provs {
            scope = f" -> {w.scope}" if w.scope else "";
            names = ", ".join(w.names) if w.names else "(module)";
            lines.append(f"    {w.provider}{scope}  {{ {names} }}");
        }
    }
    cons = model.consumers(key);
    if cons {
        lines.append("  consumed by:");
        for w in cons {
            names = ", ".join(w.names) if w.names else "(module)";
            lines.append(f"    {w.consumer}  {{ {names} }}");
        }
    }
    lines.append("  symbols:");
    def walk(nd: any, depth: int) {
        sig = getattr(nd, "signature", "") or getattr(nd, "type_str", "");
        loc = f"{os.path.basename(nd.file)}:{nd.line}" if nd.file else "";
        idef = "";
        if getattr(nd, "impl_file", "") {
            idef = f"  impl {os.path.basename(nd.impl_file)}:{nd.impl_line}";
        }
        lines.append(
            "    "
                + "  " * depth
                + f"{nd.kind} {nd.name} {sig}".rstrip()
                + f"  [{loc}]{idef}"
        );
        for kid in model.children(nd.key) {
            walk(kid, depth + 1);
        }
    }
    for kid in model.children(key) {
        walk(kid, 0);
    }
    return "\n".join(lines);
}

glob STYLE_COLORS: dict[str, int] = {
         "keyword": 170,
         "builtin": 168,
         "builtin_type": 38,
         "constant": 208,
         "number": 179,
         "string": 114,
         "docstring": 108,
         "comment": 244,
         "operator": 110,
         "punct": 248,
         "name": 252,
         "function": 75,
         "method": 81,
         "macro": 75,
         "class": 221,
         "struct": 221,
         "interface": 221,
         "type": 38,
         "type_parameter": 38,
         "enum": 215,
         "enum_member": 215,
         "namespace": 147,
         "parameter": 216,
         "variable": 252,
         "property": 117,
         "event": 117,
         "decorator": 180,
         "embedded": 139,
         "tag": 167,
         "text": 252,
         "error": 196
     };

impl paint_line(text: str, spans: list[Span]) -> str {
    out: list[str] = [];
    cursor = 0;
    for sp in spans {
        if sp.start < cursor or sp.start >= len(text) {
            continue;
        }
        if sp.start > cursor {
            out.append(text[cursor:sp.start]);
        }
        parts = sp.style.split(".");
        color = STYLE_COLORS.get(parts[0], 252);
        bold = "1;" if "declaration" in parts or "definition" in parts else "";
        italic = "3;" if parts[0] in ["comment", "docstring"] else "";
        out.append(
            f"\x1b[{bold}{italic}38;5;{color}m" + text[sp.start:sp.end] + "\x1b[0m"
        );
        cursor = min(sp.end, len(text));
    }
    out.append(text[cursor:]);
    return "".join(out);
}

impl wait_ready(ci: CodeIntel, path: str, timeout: float = 600.0) -> str {
    deadline = time.time() + timeout;
    st = ci.status(path);
    while time.time() < deadline {
        st = ci.status(path);
        if st == "ready" or st.startswith("error") {
            return st;
        }
        time.sleep(0.02);
    }
    return st;
}

impl wait_tickets(
    ci: CodeIntel, tickets: list[int], timeout: float = 120.0
) -> dict[int, any] {
    got: dict[int, any] = {};
    deadline = time.time() + timeout;
    while len(got) < len(tickets) and time.time() < deadline {
        for (t, res) in ci.poll() {
            got[t] = res;
        }
        if len(got) < len(tickets) {
            time.sleep(0.02);
        }
    }
    return got;
}

impl cmd_intel(directory: str, args: list[str]) -> int {
    max_apps = 1;
    if "--apps" in args {
        at = args.index("--apps");
        max_apps = int(args[at + 1]) if at + 1 < len(args) else 1;
        args = args[:at] + args[at + 2:];
    }
    if not args {
        err(
            "usage: jac studio intel <file.jac> [line col] [--apps N]   (line and col are 1-based)"
        );
        return 2;
    }
    path = os.path.realpath(args[0]);
    if not os.path.isfile(path) {
        err(f"jac studio intel: no such file: {args[0]}");
        return 1;
    }
    line = int(args[1]) if len(args) > 1 else 0;
    col = int(args[2]) - 1 if len(args) > 2 else 0;
    root_dir = find_project_root(directory or os.path.dirname(path));
    ci = CodeIntel(max_apps=max_apps);
    t0 = time.perf_counter();
    lexed = ci.highlight(path);
    hl_secs = time.perf_counter() - t0;
    t0 = time.perf_counter();
    ci.highlight(path);
    hl_cached = time.perf_counter() - t0;
    t_start = time.perf_counter();
    ci.start(root_dir);
    try {
        ci.request_check(path);
        with open(path, "r", encoding="utf-8", errors="replace") as f {
            edited = f.read() + "\n";
        }
        time.sleep(0.3);
        t0 = time.perf_counter();
        ci.highlight(path, edited);
        hl_busy = time.perf_counter() - t0;
        st = wait_ready(ci, path);
        first_sem = time.perf_counter() - t_start;
        check_cold = ci.check_secs(path);
        styles = ci.line_styles(path);
        with open(path, "r", encoding="utf-8", errors="replace") as f {
            lines = f.read().split("\n");
        }
        lo = max(0, line - 20) if line else 0;
        hi = min(len(lines), lo + 40);
        out(f"== {path}  [{st}]  lines {lo + 1}-{hi} of {len(lines)}");
        for i in range(lo, hi) {
            mark = ">" if i + 1 == line else " ";
            out(
                f"{mark}{i + 1:5d} "
                    + paint_line(lines[i], styles[i] if i < len(styles) else [])
            );
        }
        sem_rows = ci.semantic(path);
        nsem = sum([len(r) for r in sem_rows]) if sem_rows else 0;
        diags = ci.diagnostics(path);
        out(f"== diagnostics ({len(diags)})");
        for d in diags {
            out(
                f"  {d.severity} {d.code} {d.line}:{d.col + 1}-{d.end_line}:{d.end_col
                    + 1}  {d.message}"
            );
            if d.help {
                out(f"      help: {d.help.splitlines()[0]}");
            }
        }
        if line {
            snippet = lines[line - 1] if 0 < line <= len(lines) else "";
            out(f"== position {line}:{col + 1}  {snippet.strip()}");
            out(f"  symbol_at: {ci.symbol_at(path, line, col)}");
            th = ci.request_hover(path, line, col);
            td = ci.request_definition(path, line, col);
            tr = ci.request_references(path, line, col);
            got = wait_tickets(ci, [th, td, tr]);
            hover = got.get(th);
            out("  hover:");
            for hl in (str(hover) if hover else "(none)").splitlines() {
                out(f"    {hl}");
            }
            out(f"  definition: {got.get(td)}");
            refs = got.get(tr) or [];
            out(f"  references ({len(refs)}):");
            for r in refs[:30] {
                out(
                    f"    {os.path.relpath(r['path'], root_dir)}:{r['line']}:{r['col']
                        + 1}  {r.get('text', '')}"
                );
            }
        }
        ci.invalidate(path);
        wait_ready(ci, path);
        check_warm = ci.check_secs(path);
        out(
            f"== timings: highlight {hl_secs * 1000:.1f} ms for {len(
                lexed
            )} lines (cached {hl_cached * 1000:.2f} ms, while the worker compiles {hl_busy
                * 1000:.1f} ms), "
                + f"first semantic tokens {first_sem:.2f} s (cold check {check_cold:.2f} s), "
                + f"warm re-check {check_warm:.2f} s, {nsem} semantic tokens"
        );
        out(f"== log: {ci.log_path}");
    } finally {
        ci.stop();
    }
    return 0;
}

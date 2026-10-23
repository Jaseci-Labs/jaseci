import os;
import sys;
import json;
import queue;
import shutil;
import difflib;
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

def cmd_agents(root_dir: str, as_json: bool) -> int;

def cmd_sessions(root_dir: str, as_json: bool) -> int;

def cmd_ask(
    root_dir: str,
    args: list[str],
    agent: str,
    session_id: str,
    assume_yes: bool,
    as_json: bool
) -> int;

def build_model(root_dir: str) -> ProjectModel;

obj AskView {
    has root_dir: str,
        in_text: bool = False,
        titles: dict[str, str] = {},
        kinds: dict[str, str] = {},
        order: list[str] = [],
        calls: dict[str, dict[str, any]] = {},
        shown: list[str] = [];

    def chunk(text: str) -> None;
    def line(text: str) -> None;
    def tool(d: dict[str, any]) -> None;
    def show_tool(tid: str, failed: bool) -> None;
    def flush_tools -> None;
}

def jac_executable -> str;

def jac_mcp_server -> dict[str, any];

def unified_diff(path: str, old: str, new: str, root_dir: str) -> str;

def permission_diffs(
    tool_call: dict[str, any], root_dir: str, known: (dict[str, any] | None) = None
) -> list[str];

def read_or_empty(path: str) -> str;

def choose_permission(
    data: dict[str, any],
    assume_yes: bool,
    root_dir: str,
    known: (dict[str, any] | None) = None
) -> (str | None);

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
    assume_yes = False;
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
        } elif a in ["-y", "--yes"] {
            assume_yes = True;
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
    root_dir = find_project_root(directory or os.getcwd());
    if action == "model" {
        return cmd_model(root_dir, args, as_json);
    }
    if action == "agents" {
        return cmd_agents(root_dir, as_json);
    }
    if action == "sessions" {
        return cmd_sessions(root_dir, as_json);
    }
    if action == "ask" {
        return cmd_ask(root_dir, args, agent, session, assume_yes, as_json);
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

impl cmd_agents(root_dir: str, as_json: bool) -> int {
    reg = AgentRegistry(root_dir=root_dir);
    rows = reg.describe();
    if as_json {
        out(json.dumps({"default": reg.default_name(), "agents": rows}, indent=2));
        return 0;
    }
    width = max([len(r["name"]) for r in rows] + [4]);
    for r in rows {
        mark = "*" if r["default"] else " ";
        state = "ready" if r["runnable"] else "unavailable";
        if r["kind"] == "builtin" {
            what = f"built-in byllm agent (model: {r.get('model', '')})";
        } else {
            what = " ".join([r["command"], *r["args"]]);
        }
        line = f"{mark} {r['name'].ljust(width)}  {state.ljust(11)}  {what}";
        if not r["runnable"] and r["reason"] {
            line += f"  ({r['reason']})";
        }
        if r["source"] != "builtin" {
            line += f"  [{r['source']} config]";
        }
        out(line);
    }
    out(f"default: {reg.default_name()}  (set [studio] default_agent in jac.toml)");
    return 0;
}

impl cmd_sessions(root_dir: str, as_json: bool) -> int {
    rows = list_sessions(root_dir);
    if as_json {
        out(json.dumps(rows, indent=2));
        return 0;
    }
    if not rows {
        out(f"no saved sessions under {sessions_dir(root_dir)}");
        return 0;
    }
    for r in rows {
        when = time.strftime("%Y-%m-%d %H:%M", time.localtime(float(r["updated"])));
        fork = f"  (fork of {r['parent']})" if r.get("parent") else "";
        out(
            f"{r['id']}  {when}  {r['agent'] or '?':8}  {r['entries']:3} entries  {r[
                'title'
            ]}{fork}"
        );
    }
    return 0;
}

impl build_model(root_dir: str) -> ProjectModel {
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
    return model;
}

impl jac_executable -> str {
    argv0 = sys.argv[0] if sys.argv else "";
    cand = "";
    if argv0 {
        cand = argv0 if os.sep in argv0 else (shutil.which(argv0) or "");
    }
    if cand
        and os.path.isfile(cand)
        and os.access(cand, os.X_OK)
        and not cand.endswith((".py", ".jac")) {
        return os.path.realpath(cand);
    }
    return shutil.which("jac") or "jac";
}

impl jac_mcp_server -> dict[str, any] {
    return {"name": "jac", "command": jac_executable(), "args": ["mcp"], "env": []};
}

impl unified_diff(path: str, old: str, new: str, root_dir: str) -> str {
    name = os.path.relpath(path, root_dir) if os.path.isabs(path) else path;
    lines = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile=f"a/{name}",
        tofile=f"b/{name}"
    );
    text = "".join(lines);
    if text and not text.endswith("\n") {
        text += "\n";
    }
    return text or f"(no change to {name})\n";
}

impl permission_diffs(
    tool_call: dict[str, any], root_dir: str, known: (dict[str, any] | None) = None
) -> list[str] {
    diffs: list[str] = [];
    prior = known or {};
    contents = tool_call.get("content") or prior.get("content") or [];
    for c in contents {
        if isinstance(c, dict) and c.get("type") == "diff" {
            path = str(c.get("path", ""));
            old = str(c.get("oldText") or "");
            new = str(c.get("newText") or "");
            whole = read_or_empty(path);
            if whole and old and old != whole and old in whole {
                (old, new) = (whole, whole.replace(old, new, 1));
            }
            diffs.append(unified_diff(path, old, new, root_dir));
        }
    }
    raw = tool_call.get("rawInput") or prior.get("raw_input") or {};
    path = str(raw.get("file_path") or raw.get("path") or "")
        if isinstance(raw, dict)
        else "";
    if diffs or not path {
        return diffs;
    }
    old = read_or_empty(path);
    if "old_string" in raw and "new_string" in raw {
        count = -1 if raw.get("replace_all") else 1;
        new = old.replace(str(raw["old_string"]), str(raw["new_string"]), count);
        diffs.append(unified_diff(path, old, new, root_dir));
    } elif "content" in raw {
        diffs.append(unified_diff(path, old, str(raw["content"]), root_dir));
    }
    return diffs;
}

impl read_or_empty(path: str) -> str {
    try {
        with open(path, encoding="utf-8", errors="replace") as f {
            return f.read();
        }
    } except OSError {
        return "";
    }
}

impl choose_permission(
    data: dict[str, any],
    assume_yes: bool,
    root_dir: str,
    known: (dict[str, any] | None) = None
) -> (str | None) {
    tc = data.get("tool_call") or {};
    options = data.get("options") or [];
    title = tc.get("title") or tc.get("toolCallId") or "a tool call";
    out(f"\n  ? permission requested: {title}");
    for d in permission_diffs(tc, root_dir, known) {
        sys.stdout.write(d);
    }
    def first_of(kinds: list[str]) -> (str | None) {
        for k in kinds {
            for o in options {
                if o.get("kind") == k {
                    return o.get("optionId");
                }
            }
        }
        return None;
    }
    if assume_yes {
        pick = first_of(["allow_once", "allow_always"]);
        out(f"  -> allowed (--yes)");
        return pick;
    }
    if sys.stdin.isatty() {
        for (i, o) in enumerate(options) {
            out(f"    {i + 1}. {o.get('name', o.get('optionId'))}");
        }
        sys.stdout.write("    choose a number (enter to reject): ");
        sys.stdout.flush();
        try {
            ans = sys.stdin.readline().strip();
        } except (OSError, KeyboardInterrupt) {
            ans = "";
        }
        if ans.isdigit() and 1 <= int(ans) <= len(options) {
            return options[int(ans) - 1].get("optionId");
        }
    } else {
        out("  -> rejected (stdin is not a terminal; pass --yes to allow)");
    }
    return first_of(["reject_once", "reject_always"]);
}

impl cmd_ask(
    root_dir: str,
    args: list[str],
    agent: str,
    session_id: str,
    assume_yes: bool,
    as_json: bool
) -> int {
    if len(args) < 2 {
        err(
            "usage: jac studio ask <symbol-or-module> \"<instruction>\" [--agent NAME] [--session ID] [--yes]"
        );
        return 2;
    }
    target = args[0];
    instruction = " ".join(args[1:]).strip();
    reg = AgentRegistry(root_dir=root_dir);
    st: (StudioSession | None) = None;
    if session_id {
        st = load_session(root_dir, session_id);
        if st is None {
            err(
                f"jac studio ask: no saved session '{session_id}' (see `jac studio sessions`)"
            );
            return 1;
        }
    }
    name = agent
        or (st.agent if st is not None and st.agent else "")
        or reg.default_name();
    spec = reg.get(name);
    if spec is None {
        err(f"jac studio ask: unknown agent '{name}'. Known: {', '.join(reg.names())}");
        return 1;
    }
    if not spec.runnable() {
        err(f"jac studio ask: agent '{name}' cannot run: {spec.reason()}");
        return 1;
    }
    model = build_model(root_dir);
    key = resolve_key(model, target);
    if not key {
        err(f"jac studio ask: nothing in the project model matches '{target}'");
        return 1;
    }
    if key != target {
        err(f"  using {key}");
    }
    if st is None {
        st = new_session(root_dir, agent=name);
    }
    resume_id = st.agent_session_id if st.agent == name else "";
    st.agent = name;
    if key not in st.tray {
        st.tray.append(key);
    }
    st.add("user", f"[{key}] {instruction}");
    def gate(path: str, content: str) -> (str | None) {
        old = "";
        try {
            with open(path, encoding="utf-8", errors="replace") as f {
                old = f.read();
            }
        } except OSError {}
        out(f"\n  ~ write requested: {os.path.relpath(path, root_dir)}");
        sys.stdout.write(unified_diff(path, old, content, root_dir));
        if assume_yes {
            out("  -> applied (--yes)");
            st.decide("write", True, path=path);
            return None;
        }
        out("  -> not applied (rerun with --yes to apply)");
        st.decide("write", False, path=path, message="needs --yes");
        return (
            "The user did not approve this write: `jac studio ask` applies edits only "
            + "with --yes. The proposed change was shown to the user as a diff; do not retry it."
        );
    }
    try {
        sess = reg.create_session(
            name, project_model=model, load_session_id=resume_id, write_gate=gate
        );
    } except Exception as e {
        err(f"jac studio ask: {e}");
        return 1;
    }
    err(f"  starting {name} ...");
    try {
        sess.start(root_dir, [jac_mcp_server()]);
    } except Exception as e {
        err(f"jac studio ask: could not start agent '{name}': {e}");
        sess.stop();
        return 1;
    }
    blocks = context_blocks(model, [key]) + [{"type": "text", "text": instruction}];
    rc = 0;
    view = AskView(root_dir=root_dir);
    try {
        sess.prompt(blocks);
        while True {
            try {
                ev = sess.events.get(timeout=0.5);
            } except queue.Empty {
                continue;
            }
            d = ev.data;
            if d.get("replay") {
                continue;
            }
            st.record(ev);
            if ev.kind == "message_chunk" {
                view.chunk(str(d.get("text", "")));
            } elif ev.kind in ["tool_call", "tool_call_update"] {
                view.tool(d);
            } elif ev.kind == "plan" {
                view.line("  plan:");
                for p in (d.get("entries") or []) {
                    view.line(f"    [{p.get('status', '')}] {p.get('content', '')}");
                }
            } elif ev.kind == "terminal" {
                if d.get("exit_code") is not None or d.get("signal") {
                    view.line(
                        f"  $ {d.get('command', '')}  (exit {d.get('exit_code')})"
                    );
                }
            } elif ev.kind == "permission" {
                view.line("");
                tcid = str((d.get("tool_call") or {}).get("toolCallId", ""));
                choice = choose_permission(
                    d, assume_yes, root_dir, view.calls.get(tcid)
                );
                st.decide(
                    "permission",
                    choice is not None and "reject" not in str(choice),
                    message=str(choice),
                    detail=str((d.get("tool_call") or {}).get("title", ""))
                );
                sess.respond_permission(d.get("request_id"), choice);
            } elif ev.kind == "write" {
                verdict = gate(str(d.get("path", "")), str(d.get("content", "")));
                sess.resolve_write(d.get("request_id"), verdict is None, verdict or "");
            } elif ev.kind == "error" {
                view.line("");
                err(f"error: {d.get('message', '')}");
                rc = 1;
            } elif ev.kind == "turn_end" {
                view.flush_tools();
                view.line("");
                reason = str(d.get("stop_reason", ""));
                if reason != "end_turn" {
                    err(f"(turn ended: {reason})");
                    if reason == "error" {
                        rc = 1;
                    }
                }
                break;
            }
        }
    } except KeyboardInterrupt {
        err("\ncancelling ...");
        sess.cancel();
        deadline = time.time() + 20;
        while time.time() < deadline {
            try {
                ev = sess.events.get(timeout=0.5);
            } except queue.Empty {
                if not sess.busy() {
                    break;
                }
                continue;
            }
            st.record(ev);
            if ev.kind == "turn_end" {
                break;
            }
        }
        rc = 130;
    } except Exception as e {
        err(f"jac studio ask: {e}");
        rc = 1;
    } finally {
        sess.stop();
    }
    if sess.agent_session_id {
        st.agent_session_id = sess.agent_session_id;
    }
    st.save();
    out(f"\nsession: {st.id}");
    return rc;
}

impl AskView.chunk(text: str) -> None {
    if not text {
        return;
    }
    sys.stdout.write(text);
    sys.stdout.flush();
    self.in_text = not text.endswith("\n");
}

impl AskView.line(text: str) -> None {
    if self.in_text {
        sys.stdout.write("\n");
        self.in_text = False;
    }
    if text {
        out(text);
    }
}

impl AskView.tool(d: dict[str, any]) -> None {
    tid = str(d.get("id", ""));
    if tid not in self.order {
        self.order.append(tid);
    }
    if d.get("title") {
        self.titles[tid] = str(d["title"]);
    }
    if d.get("kind") {
        self.kinds[tid] = str(d["kind"]);
    }
    rec = self.calls.setdefault(tid, {});
    for k in ["content", "raw_input"] {
        if d.get(k) {
            rec[k] = d[k];
        }
    }
    status = str(d.get("status") or "");
    if status in ["in_progress", "completed", "failed"] and tid not in self.shown {
        self.show_tool(tid, status == "failed");
    } elif status == "failed" {
        self.line(f"  ! failed: {self.titles.get(tid, tid)}");
    }
}

impl AskView.show_tool(tid: str, failed: bool) -> None {
    self.shown.append(tid);
    title = self.titles.get(tid, tid).replace(self.root_dir + os.sep, "");
    mark = "!" if failed else ">";
    tail = "  (failed)" if failed else "";
    self.line(f"  {mark} {title}  [{self.kinds.get(tid, 'other')}]{tail}");
}

impl AskView.flush_tools -> None {
    for tid in self.order {
        if tid not in self.shown {
            self.show_tool(tid, False);
        }
    }
}

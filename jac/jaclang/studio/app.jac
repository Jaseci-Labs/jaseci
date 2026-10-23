import os;
import sys;
import json;

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

def cmd_mcp(root_dir: str, args: list[str]) -> int;

def format_summary(model: ProjectModel) -> str;

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
    root_dir = find_project_root(directory or os.getcwd());
    if action == "model" {
        return cmd_model(root_dir, args, as_json);
    }
    if action == "mcp" {
        return cmd_mcp(root_dir, args);
    }
    if action == "" {
        return run_tui(root_dir, agent, session);
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

impl cmd_mcp(root_dir: str, args: list[str]) -> int {
    sock = "";
    i = 0;
    while i < len(args) {
        a = args[i];
        if a == "--socket" and i + 1 < len(args) {
            sock = args[i + 1];
            i += 2;
        } elif a.startswith("--socket=") {
            sock = a.split("=", 1)[1];
            i += 1;
        } else {
            err(
                f"jac studio mcp: unexpected argument '{a}' (usage: jac studio mcp [--socket PATH])"
            );
            return 2;
        }
    }
    return serve_studio_mcp(sock, root_dir);
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

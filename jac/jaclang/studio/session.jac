import os;
import json;
import secrets;
import time;

glob SESSION_ROLES: list[str] = ["user", "agent", "tool", "plan", "system"],
     SESSION_FORMAT: int = 1;

obj StudioSession {
    has id: str = "",
        root_dir: str = "",
        created: float = 0.0,
        updated: float = 0.0,
        agent: str = "",
        agent_session_id: str = "",
        title: str = "",
        parent: str = "",
        entries: list[dict[str, any]] = [],
        tray: list[str] = [],
        decisions: list[dict[str, any]] = [],
        _streaming: bool = False;

    def postinit;
    def path -> str;
    def add(
        role: str, text: str, tool_call: (dict[str, any] | None) = None
    ) -> dict[str, any];

    def append_text(role: str, text: str) -> dict[str, any];
    def record(ev: AgentEvent) -> None;
    def tool_entry(tool_id: str) -> (dict[str, any] | None);
    def decide(
        kind: str, accepted: bool, path: str = "", message: str = "", detail: str = ""
    ) -> dict[str, any];

    def save -> str;
    def to_dict -> dict[str, any];
    def summary -> dict[str, any];
    def fork -> StudioSession;
}

def new_session_id -> str;

def sessions_dir(root_dir: str) -> str;

def new_session(root_dir: str, agent: str = "", title: str = "") -> StudioSession;

def session_from_dict(root_dir: str, d: dict[str, any]) -> StudioSession;

def load_session(root_dir: str, session_id: str) -> (StudioSession | None);

def list_sessions(root_dir: str) -> list[dict[str, any]];

def fork_session(root_dir: str, session_id: str) -> (StudioSession | None);

impl StudioSession.postinit {
    if not self.id {
        self.id = new_session_id();
    }
    now = time.time();
    if not self.created {
        self.created = now;
    }
    if not self.updated {
        self.updated = self.created;
    }
}

impl StudioSession.path -> str {
    return os.path.join(sessions_dir(self.root_dir), f"{self.id}.json");
}

impl StudioSession.add(
    role: str, text: str, tool_call: (dict[str, any] | None) = None
) -> dict[str, any] {
    if role not in SESSION_ROLES {
        role = "system";
    }
    ent: dict[str, any] = {"role": role, "text": text, "time": time.time()};
    if tool_call is not None {
        ent["tool_call"] = tool_call;
    }
    self.entries.append(ent);
    self._streaming = False;
    self.updated = ent["time"];
    if role == "user" and not self.title {
        self.title = " ".join(text.split())[:80];
    }
    return ent;
}

impl StudioSession.append_text(role: str, text: str) -> dict[str, any] {
    last = self.entries[-1] if self.entries else None;
    if self._streaming
        and last is not None
        and last.get("role") == role
        and "tool_call" not in last {
        last["text"] = last.get("text", "") + text;
        self.updated = time.time();
        return last;
    }
    ent = self.add(role, text);
    self._streaming = True;
    return ent;
}

impl StudioSession.record(ev: AgentEvent) -> None {
    d = ev.data;
    if ev.kind == "message_chunk" {
        self.append_text("agent", str(d.get("text", "")));
    } elif ev.kind == "tool_call" and self.tool_entry(str(d.get("id", ""))) is None {
        tc = {
            "id": d.get("id", ""),
            "title": d.get("title", ""),
            "kind": d.get("kind", ""),
            "status": d.get("status", ""),
            "locations": d.get("locations") or []
        };
        if "raw_input" in d {
            tc["raw_input"] = d["raw_input"];
        }
        self.add("tool", str(d.get("title", "")), tc);
    } elif ev.kind in ["tool_call", "tool_call_update"] {
        e = self.tool_entry(str(d.get("id", "")));
        if e is not None {
            prev: any = e.get("tool_call");
            for k in ["title", "kind", "status", "locations", "raw_input"] {
                if d.get(k) is not None {
                    prev[k] = d[k];
                }
            }
            if d.get("title") {
                e["text"] = str(d["title"]);
            }
        }
        self.updated = time.time();
    } elif ev.kind == "plan" {
        entries = d.get("entries") or [];
        text = "\n".join(
            [f"[{p.get('status', '')}] {p.get('content', '')}" for p in entries]
        );
        last = self.entries[-1] if self.entries else None;
        if last is not None and last.get("role") == "plan" {
            last["text"] = text;
            last["plan"] = entries;
        } else {
            self.add("plan", text)["plan"] = entries;
        }
    } elif ev.kind == "error" {
        self.add("system", "error: " + str(d.get("message", "")));
    } elif ev.kind == "turn_end" {
        self._streaming = False;
        reason = str(d.get("stop_reason", ""));
        if reason and reason != "end_turn" {
            self.add("system", f"turn ended: {reason}");
        }
    } elif ev.kind == "ready" {
        if d.get("session_id") {
            self.agent_session_id = str(d["session_id"]);
        }
    }
}

impl StudioSession.decide(
    kind: str, accepted: bool, path: str = "", message: str = "", detail: str = ""
) -> dict[str, any] {
    dec: dict[str, any] = {
        "kind": kind,
        "accepted": accepted,
        "path": path,
        "message": message,
        "time": time.time()
    };
    if detail {
        dec["detail"] = detail;
    }
    self.decisions.append(dec);
    self.updated = dec["time"];
    return dec;
}

impl StudioSession.save -> str {
    p = self.path();
    os.makedirs(os.path.dirname(p), exist_ok=True);
    tmp = p + ".tmp";
    with open(tmp, "w", encoding="utf-8") as f {
        json.dump(self.to_dict(), f, indent=1, `default=str);
    }
    os.replace(tmp, p);
    return p;
}

impl StudioSession.to_dict -> dict[str, any] {
    return {
        "format": SESSION_FORMAT,
        "id": self.id,
        "title": self.title,
        "created": self.created,
        "updated": self.updated,
        "agent": self.agent,
        "agent_session_id": self.agent_session_id,
        "parent": self.parent,
        "tray": self.tray,
        "entries": self.entries,
        "decisions": self.decisions
    };
}

impl StudioSession.summary -> dict[str, any] {
    return {
        "id": self.id,
        "title": self.title,
        "agent": self.agent,
        "created": self.created,
        "updated": self.updated,
        "entries": len(self.entries),
        "tray": self.tray,
        "parent": self.parent
    };
}

impl StudioSession.fork -> StudioSession {
    data = json.loads(json.dumps(self.to_dict(), `default=str));
    child = session_from_dict(self.root_dir, data);
    child.id = new_session_id();
    child.parent = self.id;
    child.agent_session_id = "";
    child.created = time.time();
    child.updated = child.created;
    return child;
}

impl new_session_id -> str {
    return time.strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(2);
}

impl sessions_dir(root_dir: str) -> str {
    return os.path.join(root_dir, ".jac", "studio", "sessions");
}

impl new_session(root_dir: str, agent: str = "", title: str = "") -> StudioSession {
    return StudioSession(root_dir=os.path.realpath(root_dir), agent=agent, title=title);
}

impl session_from_dict(root_dir: str, d: dict[str, any]) -> StudioSession {
    return StudioSession(
        id=str(d.get("id", "")),
        root_dir=os.path.realpath(root_dir),
        created=float(d.get("created", 0.0) or 0.0),
        updated=float(d.get("updated", 0.0) or 0.0),
        agent=str(d.get("agent", "")),
        agent_session_id=str(d.get("agent_session_id", "")),
        title=str(d.get("title", "")),
        parent=str(d.get("parent", "")),
        entries=list(d.get("entries") or []),
        tray=[str(k) for k in (d.get("tray") or [])],
        decisions=list(d.get("decisions") or [])
    );
}

impl load_session(root_dir: str, session_id: str) -> (StudioSession | None) {
    d = sessions_dir(root_dir);
    if not os.path.isdir(d) or not session_id {
        return None;
    }
    exact = os.path.join(d, f"{session_id}.json");
    path = exact if os.path.isfile(exact) else "";
    if not path {
        hits = sorted(
            [
                f
                for f in os.listdir(d)
                if f.endswith(".json") and f.startswith(session_id)
            ]
        );
        if len(hits) != 1 {
            return None;
        }
        path = os.path.join(d, hits[0]);
    }
    try {
        with open(path, encoding="utf-8") as f {
            data = json.load(f);
        }
    } except (OSError, ValueError) {
        return None;
    }
    if not isinstance(data, dict) {
        return None;
    }
    return session_from_dict(root_dir, data);
}

impl list_sessions(root_dir: str) -> list[dict[str, any]] {
    d = sessions_dir(root_dir);
    if not os.path.isdir(d) {
        return [];
    }
    out: list[dict[str, any]] = [];
    for f in os.listdir(d) {
        if not f.endswith(".json") {
            continue;
        }
        s = load_session(root_dir, f[:-5]);
        if s is not None {
            out.append(s.summary());
        }
    }
    out.sort(key=lambda (x: dict[str, any]) -> float { -float(x.get("updated", 0.0)) });
    return out;
}

impl fork_session(root_dir: str, session_id: str) -> (StudioSession | None) {
    src = load_session(root_dir, session_id);
    if src is None {
        return None;
    }
    child = src.fork();
    child.save();
    return child;
}

impl StudioSession.tool_entry(tool_id: str) -> (dict[str, any] | None) {
    for e in reversed(self.entries) {
        tc = e.get("tool_call");
        if isinstance(tc, dict) and str(tc.get("id", "")) == tool_id {
            return e;
        }
    }
    return None;
}

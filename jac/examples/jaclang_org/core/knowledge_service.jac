import logging;
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
     _BUNDLES: dict[str, DocBundle] = {},
     log: logging.Logger = logging.getLogger("knowledge");

def release_bundle(line: ReleaseLine) -> DocBundle;

@schedule(trigger=ScheduleTrigger.STATIC, interval=REPO_TICK_S)
def:priv knowledge_repo_tick;

def:pub knowledge_status -> RepoStatus;

def:pub release_doc_lines -> ReleaseLines;

def:pub release_docs(tag: str) -> DocBundle | None;

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

"""Gate harness entry points for OSPUI architecture validation (Unit 13).

Each gate returns success / a metrics report. Companion tests in gates.test.jac
define acceptance.
"""

import from time { perf_counter }

import from .model {
    MainScreen,
    ordered_child_keys,
}

import from .runtime {
    create_session,
    dispose_session,
}

import from .persistence_probe {
    ui_jids_reachable_from_persistent_root,
}

import from .bindings {
    is_empty,
}

import from .events {
    InsertText,
    dispatch_event,
}

import from .screen {
    build_main_shell,
    configure_main_shell_layout,
    install_shell_contracts,
    shell_insert_text,
    shell_open_approval,
    shell_close_approval,
    shell_resize,
}

import from .renderer {
    create_renderer,
    render_frame,
    set_node_content,
}

import from .virtual_terminal {
    VirtualTerminal,
}

import from .markup {
    lower_markup,
    default_shell_registry,
    register_tag,
    create_tag_registry,
}

import from .progress_bar {
    ProgressBar,
    SetProgress,
    render_progress,
    register_progress_markup,
}

import from .inspect {
    validate_invariants,
}


obj Gate4Report {
    has nodes_queried: int = 0,
        cells_written: int = 0,
        latency_ms: float = 0.0,
        full_frame_cells: int = 0,
        retained_cells: int = 0;
}


"""Gate 1 — Detached graph lifecycle: no UI jids from persistent root; dispose cleans."""
def run_gate1_detached_lifecycle() -> bool {
    handle = create_session();
    session = handle.session;
    shell = build_main_shell(session);
    install_shell_contracts(session, shell, "session.events");
    # Spawn a semantic walker on the prompt (process-local only).
    event = InsertText(text="gate1");
    dispatch_event(session, event, shell.prompt);

    ui_ids = set(session.tracked_node_ids);
    leaked = ui_jids_reachable_from_persistent_root(ui_ids);
    if leaked {
        return False;
    }

    dispose_session(session);
    if not session.disposed {
        return False;
    }
    if not is_empty(session.bindings) {
        return False;
    }
    if session.renderer.layout or session.renderer.damage {
        return False;
    }
    if session.capabilities.by_node {
        return False;
    }
    if session.tracked_node_ids {
        return False;
    }
    if session.ui_root is not None {
        return False;
    }
    return True;
}


"""Gate 3 — Real layout and damage across shell scenarios."""
def run_gate3_layout_damage() -> bool {
    handle = create_session();
    session = handle.session;
    shell = build_main_shell(session);
    shell_insert_text(session, shell, "hello");
    shell_resize(session, shell, 80, 24);
    open_res = shell_open_approval(session, shell);
    if not open_res.overlay_id {
        dispose_session(session);
        return False;
    }
    term = VirtualTerminal(columns=80, rows=24);
    renderer = create_renderer(80, 24);
    failures = configure_main_shell_layout(renderer.layout, shell);
    if failures {
        dispose_session(session);
        return False;
    }
    frame = render_frame(renderer, shell.screen, term);
    close_res = shell_close_approval(session, shell);
    _ = (frame, close_res);
    findings = validate_invariants(session);
    dispose_session(session);
    return findings == [];
}


"""Gate 4 — Invalidation benchmark numbers (nodes, cells, latency)."""
def run_gate4_invalidation_bench() -> Gate4Report {
    handle = create_session();
    session = handle.session;
    shell = build_main_shell(session);
    term = VirtualTerminal(columns=80, rows=24);
    renderer = create_renderer(80, 24);
    if configure_main_shell_layout(renderer.layout, shell) {
        dispose_session(session);
        return Gate4Report();
    }
    set_node_content(renderer, shell.header, ["Osprey"]);
    set_node_content(renderer, shell.transcript, ["hello retained stream"]);
    set_node_content(renderer, shell.status, ["ready"]);
    set_node_content(renderer, shell.prompt, ["> "]);

    t0 = perf_counter();
    frame1 = render_frame(renderer, shell.screen, term);
    set_node_content(renderer, shell.transcript, ["hello retained stream!"]);
    frame2 = render_frame(renderer, shell.screen, term);
    t1 = perf_counter();

    full_cells = 80 * 24;
    retained = frame2.cells_written;
    if retained > full_cells {
        retained = full_cells;
    }
    nodes_q = len(session.tracked_node_ids);
    metrics = Gate4Report(
        nodes_queried=nodes_q,
        cells_written=frame1.cells_written + frame2.cells_written,
        latency_ms=(t1 - t0) * 1000.0,
        full_frame_cells=full_cells,
        retained_cells=retained,
    );
    dispose_session(session);
    return metrics;
}


"""Gate 5 — External ProgressBar package without framework-source edits."""
def run_gate5_external_widget() -> bool {
    bar = ProgressBar(key="p", value=0.0);
    event = SetProgress(value=0.4);
    bar spawn event;
    if not event.handled {
        return False;
    }
    if bar.value != 0.4 {
        return False;
    }
    painted = render_progress(bar.value, 12);
    if len(painted) != 12 {
        return False;
    }
    tags: dict[str, object] = {};
    register_progress_markup(tags);
    if "ProgressBar" not in tags {
        return False;
    }
    # Markup registration into a framework registry without editing markup.jac.
    reg = create_tag_registry();
    register_tag(reg, "ProgressBar", ProgressBar);
    result = lower_markup('<ProgressBar key="pb" value="0.5" />', reg);
    if result.errors {
        return False;
    }
    if result.graph_root is None {
        return False;
    }
    return isinstance(result.graph_root, ProgressBar);
}


"""Gate 6 — Authoring scale: dozens of regions via markup, no manual ranks."""
def run_gate6_authoring_scale() -> bool {
    parts: list[str] = ['<MainScreen key="main">'];
    parts.append('  <Header key="header" title="Osprey" />');
    parts.append('  <TranscriptView key="transcript" />');
    for i in range(40) {
        parts.append('  <Status key="region_' + str(i) + '" phase="ready" />');
    }
    parts.append('  <Prompt key="prompt" />');
    parts.append('  <ApprovalOverlay key="approval" />');
    parts.append("</MainScreen>");
    source = "\n".join(parts);
    result = lower_markup(source, default_shell_registry());
    if result.errors {
        return False;
    }
    if result.graph_root is None {
        return False;
    }
    if not isinstance(result.graph_root, MainScreen) {
        return False;
    }
    keys = ordered_child_keys(result.graph_root);
    if len(keys) < 40 {
        return False;
    }
    if "header" not in keys or "prompt" not in keys {
        return False;
    }
    # Generated Jac mentions append_child and never asks authors for ranks.
    gen = result.generated_jac;
    if "append_child" not in gen {
        return False;
    }
    if "rank=" in gen {
        return False;
    }
    return True;
}

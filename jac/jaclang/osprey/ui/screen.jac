"""Osprey shell topology: durable MainScreen under UiSessionRoot.

Builds the representative shell once and keeps semantic node IDs stable
across typing, streaming, resize, focus, and overlay cycles (OSPUI.md §17–18,
OSPUI-P0-PLAN Unit 8).
"""

import from .model {
    MainScreen,
    Header,
    TranscriptView,
    Status,
    Prompt,
    ApprovalOverlay,
    UiNode,
    node_id,
}

import from .runtime {
    UiSession,
    SessionEventRecord,
    OverlayOpenResult,
    OverlayCloseResult,
    OverlayBounds,
    append_child_session,
    set_current_screen,
    set_focus,
    open_modal_overlay,
    close_overlay,
    track_node,
    register_capability,
}

import from .bindings {
    subscribe,
}

import from .events {
    SendPrompt,
    InsertText,
    Submit,
    Cancel,
    dispatch_event,
}

import from .editor {
    editor_insert,
    editor_submit,
    AblePrompt,
}

import from .layout_types {
    AxisSize,
    SizeMode,
    LayoutSpec,
    LayoutDiagnostic,
    LayoutState,
    fixed_axis,
    set_spec,
}


obj ShellScreen {
    has screen: MainScreen,
        header: Header,
        transcript: TranscriptView,
        status: Status,
        prompt: Prompt,
        approval: ApprovalOverlay | None = None;
}


obj ShellIdSnapshot {
    has screen_id: str,
        header_id: str,
        transcript_id: str,
        status_id: str,
        prompt_id: str;
}


glob _SHELL_BY_SESSION: dict[str, ShellScreen] = {};


"""Build MainScreen(Header, TranscriptView, Status, Prompt) under ui_root once."""
def build_main_shell(session: UiSession) -> ShellScreen {
    if session.disposed or session.ui_root is None {
        raise ValueError("UiSession is disposed or missing ui_root");
    }
    root_id = node_id(session.ui_root);
    if root_id in _SHELL_BY_SESSION {
        existing = _SHELL_BY_SESSION[root_id];
        if session.current_screen is existing.screen {
            return existing;
        }
        raise ValueError("main shell already built for this session");
    }
    screen = MainScreen(key="main");
    header = Header(key="header", title="Osprey");
    transcript = TranscriptView(key="transcript");
    status = Status(key="status", phase="ready");
    prompt = AblePrompt(key="prompt");

    append_child_session(session, session.ui_root, screen);
    append_child_session(session, screen, header);
    append_child_session(session, screen, transcript);
    append_child_session(session, screen, status);
    append_child_session(session, screen, prompt);
    set_current_screen(session, screen);
    set_focus(session, prompt);

    shell = ShellScreen(
        screen=screen,
        header=header,
        transcript=transcript,
        status=status,
        prompt=prompt,
    );
    _SHELL_BY_SESSION[root_id] = shell;
    return shell;
}


"""Wire default shell contracts: transcript binding + prompt cursor capability."""
def install_shell_contracts(session: UiSession, shell: ShellScreen, binding_name: str) {
    subscribe(
        session.bindings,
        binding_name,
        node_id(shell.transcript),
        "TranscriptChanged",
    );
    register_capability(session, node_id(shell.prompt), "cursor");
}


"""Snapshot stable jids for shell regions (for stability assertions)."""
def shell_ids(shell: ShellScreen) -> ShellIdSnapshot {
    return ShellIdSnapshot(
        screen_id=node_id(shell.screen),
        header_id=node_id(shell.header),
        transcript_id=node_id(shell.transcript),
        status_id=node_id(shell.status),
        prompt_id=node_id(shell.prompt),
    );
}


"""Insert text into the focused prompt draft (walker ability path)."""
def shell_insert_text(session: UiSession, shell: ShellScreen, text: str) {
    event = InsertText(text=text);
    dispatch_event(session, event, shell.prompt);
    if not event.handled {
        editor_insert(shell.prompt, text);
    }
}


"""Submit the prompt draft; returns host effects (e.g. SendPrompt)."""
def shell_submit(session: UiSession, shell: ShellScreen) -> list[any] {
    event = Submit();
    dispatch_event(session, event, shell.prompt);
    if event.effects {
        return event.effects;
    }
    text = editor_submit(shell.prompt);
    return [SendPrompt(text=text)];
}


"""Cancel in-progress edit / turn from the shell."""
def shell_cancel(session: UiSession, shell: ShellScreen) {
    event = Cancel();
    dispatch_event(session, event, shell.prompt);
    if not event.handled {
        shell.prompt.draft = "";
        shell.prompt.caret = 0;
        shell.prompt.sel_anchor = -1;
        shell.prompt.sel_end = -1;
    }
}


"""Open the modal ApprovalOverlay for the shell."""
def shell_open_approval(
    session: UiSession,
    shell: ShellScreen,
) -> OverlayOpenResult {
    if shell.approval is not None {
        return open_modal_overlay(
            session, shell.screen, shell.approval, initial_focus=shell.approval
        );
    }
    approval = ApprovalOverlay(key="approval");
    append_child_session(session, shell.screen, approval);
    track_node(session, approval);
    shell.approval = approval;
    return open_modal_overlay(
        session, shell.screen, approval, initial_focus=approval, z_index=10
    );
}


"""Close the approval overlay and restore shell focus."""
def shell_close_approval(
    session: UiSession,
    shell: ShellScreen,
) -> OverlayCloseResult {
    if shell.approval is None {
        return OverlayCloseResult(
            restored_focus_id=session.focus_id,
            damage=OverlayBounds(),
            overlay_id="",
        );
    }
    approval = shell.approval;
    shell.approval = None;
    return close_overlay(session, approval);
}


"""Apply a terminal resize to shell layout contracts / content wrap."""
def shell_resize(
    session: UiSession,
    shell: ShellScreen,
    columns: int,
    rows: int,
) {
    _ = shell;
    if columns < 1 or rows < 1 {
        raise ValueError("resize requires positive columns and rows");
    }
    session.graph_revision += 1;
    session.event_queue.append(
        SessionEventRecord(
            kind="resize",
            payload={"columns": columns, "rows": rows},
        )
    );
}


# ----------------------------------------------------------------------
# Permanent layout configuration (LAYOUT-ENGINE-PLAN §4 invariant 9).
# ----------------------------------------------------------------------

def _fill() -> AxisSize {
    return AxisSize(mode=SizeMode.FILL);
}


def _fixed(n: float) -> AxisSize {
    return AxisSize(mode=SizeMode.FIXED, preferred=n);
}


def _grow(weight: float) -> AxisSize {
    return AxisSize(mode=SizeMode.GROW, grow_weight=weight);
}


def _spec(width: AxisSize, height: AxisSize) -> LayoutSpec {
    return LayoutSpec(width=width, height=height);
}


"""Install the permanent layout specs for the main shell (plan §4
invariant 9): screen fills the root viewport; header/status/prompt keep
the legacy fixed heights (1/1/2); transcript grows with scroll enabled.
Mirrors the contracts gates.jac sets on the legacy engine so parity is
testable at the M6 cutover.

Returns the diagnostics of every failed set_spec; empty means success."""
def configure_main_shell_layout(
    state: LayoutState,
    shell: ShellScreen,
) -> list[LayoutDiagnostic] {
    failures: list[LayoutDiagnostic] = [];

    targets: list[UiNode] = [
        shell.screen,
        shell.header,
        shell.transcript,
        shell.status,
        shell.prompt,
    ];
    specs: list[LayoutSpec] = [
        _spec(_fill(), _fill()),
        _spec(_fill(), _fixed(1.0)),
        LayoutSpec(width=_fill(), height=_grow(1.0), scroll_vertical=True),
        _spec(_fill(), _fixed(1.0)),
        _spec(_fill(), _fixed(2.0)),
    ];
    for i in range(len(targets)) {
        r = set_spec(state, targets[i], specs[i]);
        if not r.ok {
            for d in r.diagnostics {
                failures.append(d);
            }
        }
    }

    # An open approval overlay is part of the compute scope (Layer-reached
    # nodes need registered specs); mirror the legacy overlay_contract
    # 20x4 fixed box.
    if shell.approval is not None {
        r = set_spec(
            state,
            shell.approval,
            LayoutSpec(width=fixed_axis(20.0), height=fixed_axis(4.0)),
        );
        if not r.ok {
            for d in r.diagnostics {
                failures.append(d);
            }
        }
    }
    return failures;
}

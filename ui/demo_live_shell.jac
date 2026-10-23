"""Interactive Osprey OSP shell — live ProcessTerminal session.

Crafted for presence: brand chrome, typewriter stream, visible caret,
Unicode progress, history, and a centered approval modal.

Keys:
  type / paste   edit draft
  enter          submit → stream → tool approval
  up / down      prompt history
  backspace      delete char
  ctrl+u         clear draft
  ctrl+l         redraw
  a / y          accept approval
  r / n          reject approval
  esc            dismiss approval, else quit
  ctrl+c         quit (terminal restored)

  JACPATH=. jac run ui/demo_entry.jac
"""

import from .runtime {
    UiSession,
    create_session,
    dispose_session,
}

import from .screen {
    ShellScreen,
    build_main_shell,
    install_shell_contracts,
    shell_insert_text,
    shell_submit,
    shell_cancel,
    shell_open_approval,
    shell_close_approval,
    shell_resize,
}

import from .editor {
    editor_backspace,
    editor_history_prev,
    editor_history_next,
}

import from .transcript {
    TranscriptMessage,
    TranscriptProjection,
    bind_transcript,
    apply_transcript_revision,
    materialize_visible,
    set_follow_tail,
}

import from .layout_types {
    LayoutSpec,
    fill_axis,
    fixed_axis,
    grow_axis,
}

import from .renderer {
    Renderer,
    create_renderer,
    render_frame,
    set_node_content,
    set_node_contract,
    mark_semantic_dirty,
    mark_layout_dirty,
    request_cursor,
}

import from .terminal {
    ProcessTerminal,
    read_terminal_size,
}

import from .input {
    HostEvent,
    InputNormalizer,
    TextEvent,
    KeyEvent,
    PasteEvent,
    coalesce_events,
}

import from .progress_bar {
    ProgressBar,
    SetProgress,
}

import from .width {
    display_width,
    truncate_text,
}

import from .demo_live_shell_model { LiveShell }

import from .demo_live_shell_messages {
    _push_turn,
    _rewrite_turn,
}

import from .demo_live_shell_render {
    _install_layout,
    _render,
}


def _apply_resize(app: LiveShell, columns: int, rows: int) {
    if columns < 40 {
        columns = 40;
    }
    if rows < 12 {
        rows = 12;
    }
    if columns == app.columns and rows == app.rows {
        return;
    }
    app.columns = columns;
    app.rows = rows;
    shell_resize(app.session, app.shell, columns, rows);
    app.renderer = create_renderer(columns, rows);
    _install_layout(app);
    app.proj.viewport_width = max(12, columns - 2);
    app.proj.viewport_height = max(4, rows - 7);
    app.dirty = True;
}


def _begin_assistant_reply(app: LiveShell, user_text: str) {
    _push_turn(app, "user", user_text);
    app.phase = "streaming";
    app.shell.status.phase = "streaming";
    app.progress_value = 0.08;
    app.progress spawn SetProgress(value=app.progress_value);
    # Typewriter source — paced in _tick_stream.
    clipped = user_text if len(user_text) < 48 else user_text[:45] + "…";
    app.stream_full = (
        "looking at «"
        + clipped
        + "». walking Child ranks, measuring layout, "
        + "unioning damage rectangles — then a verify pass."
    );
    app.stream_shown = 0;
    app.stream_tick = 0;
    app.stream_msg_id = _push_turn(app, "assistant", "▍");
    app.status_hint = "streaming";
}


def _tick_stream(app: LiveShell) {
    if app.phase != "streaming" {
        return;
    }
    app.stream_tick += 1;
    app.spin_i += 1;
    step = 3;
    if app.stream_shown >= len(app.stream_full) {
        app.phase = "approval";
        app.shell.status.phase = "approval";
        app.progress_value = 0.72;
        app.progress spawn SetProgress(value=app.progress_value);
        shell_open_approval(app.session, app.shell);
        app.status_hint = "a accept · r reject";
        app.dirty = True;
        return;
    }
    app.stream_shown = min(len(app.stream_full), app.stream_shown + step);
    body = app.stream_full[:app.stream_shown];
    if app.stream_shown < len(app.stream_full) {
        body = body + "█";
    }
    _rewrite_turn(app, app.stream_msg_id, "assistant", body);
    frac = float(app.stream_shown) / float(max(1, len(app.stream_full)));
    app.progress_value = 0.08 + 0.55 * frac;
    app.progress spawn SetProgress(value=app.progress_value);
}


def _accept_approval(app: LiveShell) {
    if app.shell.approval is None {
        return;
    }
    shell_close_approval(app.session, app.shell);
    # Drop the block caret from the finished assistant line.
    _rewrite_turn(app, app.stream_msg_id, "assistant", app.stream_full);
    _push_turn(app, "tool", "jac check  ✓  clean (demo — no subprocess)");
    app.phase = "ready";
    app.shell.status.phase = "ready";
    app.progress_value = 1.0;
    app.progress spawn SetProgress(value=1.0);
    app.status_hint = "enter · ↑↓ history · esc quit";
    app.dirty = True;
}


def _reject_approval(app: LiveShell) {
    if app.shell.approval is None {
        return;
    }
    shell_close_approval(app.session, app.shell);
    _rewrite_turn(app, app.stream_msg_id, "assistant", app.stream_full);
    _push_turn(app, "tool", "jac check  ✗  cancelled");
    app.phase = "ready";
    app.shell.status.phase = "ready";
    app.progress_value = 0.0;
    app.progress spawn SetProgress(value=0.0);
    app.status_hint = "enter · ↑↓ history · esc quit";
    app.dirty = True;
}


"""Prompt history via the shared editor API (ui/editor.jac)."""
def _history_up(app: LiveShell) {
    editor_history_prev(app.shell.prompt);
    app.dirty = True;
}


def _history_down(app: LiveShell) {
    editor_history_next(app.shell.prompt);
    app.dirty = True;
}


def _handle_key(app: LiveShell, key: str) {
    if key == "ctrl+c" {
        app.running = False;
        return;
    }
    if key == "ctrl+l" {
        app.dirty = True;
        return;
    }
    if app.shell.approval is not None {
        if key == "a" or key == "y" or key == "enter" {
            _accept_approval(app);
            return;
        }
        if key == "r" or key == "n" {
            _reject_approval(app);
            return;
        }
        if key == "escape" {
            _reject_approval(app);
            return;
        }
        return;
    }
    if key == "escape" {
        app.running = False;
        return;
    }
    if key == "up" {
        if app.phase != "streaming" {
            _history_up(app);
        }
        return;
    }
    if key == "down" {
        if app.phase != "streaming" {
            _history_down(app);
        }
        return;
    }
    if key == "enter" {
        if app.phase == "streaming" {
            return;
        }
        text = app.shell.prompt.draft.strip();
        if not text {
            return;
        }
        shell_submit(app.session, app.shell);
        _begin_assistant_reply(app, text);
        return;
    }
    if key == "backspace" {
        if app.shell.prompt.draft {
            editor_backspace(app.shell.prompt);
            # Leave history-browse mode on manual edits (matches editor_insert).
            app.shell.prompt.history_index = -1;
            app.dirty = True;
        }
        return;
    }
    if key == "ctrl+u" {
        shell_cancel(app.session, app.shell);
        # Gap: neither AblePrompt.on_cancel nor shell_cancel resets history
        # state — no editor API op covers "clear draft + exit browse mode".
        app.shell.prompt.history_index = -1;
        app.dirty = True;
        return;
    }
    if key == "ctrl+d" {
        if not app.shell.prompt.draft {
            app.running = False;
        }
        return;
    }
}


def _handle_host_events(app: LiveShell, events: list[HostEvent]) {
    for event in coalesce_events(events) {
        if isinstance(event, TextEvent) {
            if app.shell.approval is not None {
                if event.text in ["a", "y", "r", "n"] {
                    _handle_key(app, event.text);
                }
                continue;
            }
            if app.phase == "streaming" {
                continue;
            }
            shell_insert_text(app.session, app.shell, event.text);
            app.dirty = True;
        } elif isinstance(event, KeyEvent) {
            _handle_key(app, event.key);
        } elif isinstance(event, PasteEvent) {
            if app.shell.approval is None and app.phase != "streaming" {
                shell_insert_text(app.session, app.shell, event.text);
                app.dirty = True;
            }
        }
    }
}


def create_live_shell() -> LiveShell {
    (cols, rows) = read_terminal_size(80, 24);
    handle = create_session();
    session = handle.session;
    shell = build_main_shell(session);
    shell.header.title = "Osprey";
    install_shell_contracts(session, shell, "live.transcript");
    proj = bind_transcript(
        shell.transcript,
        "live.transcript",
        width=max(12, cols - 2),
        height=max(4, rows - 7),
    );
    set_follow_tail(proj, True);
    term = ProcessTerminal();
    term.columns = cols;
    term.rows = rows;
    renderer = create_renderer(cols, rows);
    progress = ProgressBar(key="live_progress", value=0.0);
    app = LiveShell(
        session=session,
        shell=shell,
        proj=proj,
        renderer=renderer,
        term=term,
        normalizer=InputNormalizer(),
        progress=progress,
        columns=cols,
        rows=rows,
    );
    _install_layout(app);
    _push_turn(
        app,
        "system",
        "session attached · detached graph · retained paint\n"
        + "say something — watch the stream, then the approval modal",
    );
    return app;
}


def run_live_shell_demo() {
    app = create_live_shell();
    app.term.start();
    app.term.set_title("Osprey");
    try {
        app.dirty = True;
        _render(app);
        while app.running {
            (cols, rows) = app.term.size();
            if cols != app.columns or rows != app.rows {
                _apply_resize(app, cols, rows);
            }
            raw = app.term.poll_input(0.04);
            if app.term.eof {
                app.running = False;
                break;
            }
            if raw {
                events = app.normalizer.feed(raw);
                _handle_host_events(app, events);
            } elif app.normalizer.buffer == "\x1b" {
                events = app.normalizer.flush_buffer();
                _handle_host_events(app, events);
            }
            if app.phase == "streaming" {
                _tick_stream(app);
            } elif app.phase == "approval" {
                # Keep the status meter alive while the modal sits.
                app.spin_i += 1;
                if app.spin_i % 4 == 0 {
                    app.dirty = True;
                }
            }
            _render(app);
        }
    } except KeyboardInterrupt {
        app.running = False;
    } finally {
        try {
            app.term.hide_cursor();
            app.term.stop();
        } except Exception {
        }
        dispose_session(app.session);
    }
}




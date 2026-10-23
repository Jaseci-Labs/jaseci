"""Terminal host tick: poll → decode → ESC timeout → coalesced HostEvents.

Maps process/virtual terminal bytes to semantic HostEvents for the shell.
Does not construct UiEvent walkers (that stays with the product host loop).
"""

import time;

import from .terminal {
    Terminal,
}

import from .input {
    HostEvent,
    InputNormalizer,
    KeyEvent,
    EofEvent,
    InterruptEvent,
    coalesce_events,
}


obj HostLoop {
    has normalizer: InputNormalizer,
        last_now_ms: float = 0.0,
        saw_eof: bool = False,
        interrupt_pending: bool = False;
}


def create_host_loop(esc_timeout_ms: int = 50) -> HostLoop {
    norm = InputNormalizer();
    norm.esc_timeout_ms = esc_timeout_ms;
    return HostLoop(normalizer=norm);
}


def note_interrupt(loop: HostLoop) {
    loop.interrupt_pending = True;
}


def note_resize(loop: HostLoop, width: int, height: int) {
    loop.normalizer.feed_resize(width, height);
}


"""One host tick: poll terminal, decode, apply ESC timeout, coalesce."""
def run_host_tick(
    loop: HostLoop,
    term: Terminal,
    timeout_s: float = 0.0,
    now_ms: float | None = None,
) -> list[HostEvent] {
    clock = now_ms if now_ms is not None else (time.monotonic() * 1000.0);
    loop.last_now_ms = clock;
    out: list[HostEvent] = [];

    if loop.interrupt_pending {
        loop.interrupt_pending = False;
        out.append(InterruptEvent());
    }

    # poll_input/eof live on ProcessTerminal/VirtualTerminal, not the base
    # Terminal type; resolve them dynamically so the native checker lowers.
    raw = "";
    try {
        poll_fn = getattr(term, "poll_input");
        raw = str(poll_fn(timeout_s));
    } except Exception {
        raw = "";
    }
    if raw {
        fed = loop.normalizer.feed(raw);
        out.extend(fed);
        if loop.normalizer.buffer == "\x1b" {
            loop.normalizer.arm_esc(clock);
        }
    } else {
        # Still allow ESC timeout to fire when idle.
        if loop.normalizer.buffer == "\x1b" and loop.normalizer.esc_armed_at_ms < 0.0 {
            loop.normalizer.arm_esc(clock);
        }
    }

    esc_events = loop.normalizer.flush_esc_timeout(clock);
    out.extend(esc_events);

    if hasattr(term, "eof") and getattr(term, "eof") and not loop.saw_eof {
        loop.saw_eof = True;
        out.append(EofEvent());
    }

    out.extend(loop.normalizer.flush_coalesced());
    return coalesce_events(out);
}


"""Thin mapping of common host keys to effect-like dicts for demos/tests."""
def host_events_to_effects(events: list[HostEvent]) -> list[dict[str, any]] {
    effects: list[dict[str, any]] = [];
    for event in events {
        if isinstance(event, InterruptEvent) {
            effects.append({"kind": "cancel"});
        } elif isinstance(event, EofEvent) {
            effects.append({"kind": "exit"});
        } elif isinstance(event, KeyEvent) {
            if event.key == "ctrl+c" {
                effects.append({"kind": "cancel"});
            } elif event.key == "enter" {
                effects.append({"kind": "submit"});
            } elif event.key == "escape" {
                effects.append({"kind": "escape"});
            } else {
                effects.append({"kind": "key", "key": event.key});
            }
        } else {
            effects.append({"kind": event.kind});
        }
    }
    return effects;
}

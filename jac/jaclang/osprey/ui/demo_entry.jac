"""Live-shell demo entry point — the composition root for the demo binary.

Runs server-placed on purpose: the live loop sits on the terminal/FFI
frontier (`ProcessTerminal` methods, renderer path) that still demotes, so
the entry block must reach a Python-only callee — a native `with entry`
cannot call a demoted function (E5092 hard failure, not a seam note).

  JACPATH=. jac run ui/demo_entry.jac
"""

import os;

import from .demo_live_shell { run_live_shell_demo }


with entry {
    if not os.isatty(0) or not os.isatty(1) {
        print("demo_live_shell needs a real TTY.");
        raise SystemExit(1);
    }
    run_live_shell_demo();
}

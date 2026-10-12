"""The record a jac process hands its own jac children (pure Python, boot-safe).

Internal plumbing, never a user setting: only jac writes it. It carries the
decisions a child must not make on its own, because a child spawned in another
directory cannot see the parent's ``jac.toml``: which compiler the process
tree runs (``compiler_source``, empty for the bundled one), whether its
products must be exact (``exact``), which artifacts it is building
(``building``) and how it treats its caches (``rebuild``, ``no_precompile``).

``_jac_finder`` (the boot module, which runs before any ``jaclang`` can be
imported) writes the compiler decision through a deliberate mirror of
``update_handoff``; everything inside ``jaclang`` uses this module.
"""

from __future__ import annotations

import json
import os
import sys

HANDOFF_ENV = "JAC_HANDOFF"


def handoff() -> dict[str, object]:
    raw = os.environ.get(HANDOFF_ENV, "")
    if not raw:
        return {}
    try:
        record = json.loads(raw)
    except ValueError:
        return {}
    return record if isinstance(record, dict) else {}


def update_handoff(**fields: object) -> None:
    """Record decisions for this process's children; ``None`` clears a field."""
    record = handoff()
    for key, value in fields.items():
        if value is None:
            record.pop(key, None)
        else:
            record[key] = value
    if record:
        os.environ[HANDOFF_ENV] = json.dumps(record, sort_keys=True)
    else:
        os.environ.pop(HANDOFF_ENV, None)


def process_executable() -> str:
    """The file this process is executing, from the OS rather than argv.

    In a fused jac binary libpython is dlopen'd into the jac executable, so
    this is the jac binary itself -- in CLI mode, worker re-spawns and ``jac
    -c`` alike -- without the launcher having to export it.
    """
    try:
        if sys.platform.startswith("linux"):
            return os.path.realpath("/proc/self/exe")
        import ctypes

        if sys.platform == "darwin":
            size = ctypes.c_uint32(0)
            libc = ctypes.CDLL(None)
            libc._NSGetExecutablePath(None, ctypes.byref(size))
            buf = ctypes.create_string_buffer(size.value)
            if libc._NSGetExecutablePath(buf, ctypes.byref(size)) == 0:
                return os.path.realpath(buf.value.decode())
        elif sys.platform == "win32":
            wide = ctypes.create_unicode_buffer(32768)
            if ctypes.windll.kernel32.GetModuleFileNameW(None, wide, 32768):  # type: ignore[attr-defined]
                return wide.value
    except (OSError, AttributeError, ValueError):
        pass
    return os.path.realpath(sys.executable)

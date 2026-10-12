"""The process environment as it is now: the C `environ` array, which setenv
and putenv update. /proc/self/environ holds only the environment the process
started with, so it misses what the launcher sets before running the engine
(the engine's own `bin` on PATH, SSL_CERT_FILE) and anything set since."""

import from engine.src.runtime.mem { read_ptr, str_from_foreign_cstr }

import from c {
    glob environ: int;
}

"""Every KEY=VALUE entry of the live environment, in order."""
def:pub environ_entries -> list[str] {
    out: list[str] = [];
    i: int = 0;
    while True {
        item: int = read_ptr(environ, 8 * i);
        if item == 0 {
            return out;
        }
        out.append(str_from_foreign_cstr(item));
        i = i + 1;
    }
}

import ctypes;
import os;
import signal;
import sys;
import tempfile;
import threading;
import from functools { cache }

def engine_dir -> str {
    import from jaclang.artifacts.router { require }
    found = require("js-engine").found;
    assert found is not None;
    return found.path;
}

def node_executable -> str {
    import from jaclang.client.js_runtime { ensure_node_link }
    return ensure_node_link(engine_dir());
}

@cache
def _library(engine: str) -> ctypes.CDLL {
    lib = ctypes.CDLL(os.path.join(engine, "libjs_engine.so"));
    lib.js_pm.argtypes = [ctypes.c_int64, ctypes.POINTER(ctypes.c_char_p)];
    lib.js_pm.restype = ctypes.c_int64;
    return lib;
}

def run_pm(args: list[str], cwd: str, capture: bool = False) -> tuple[int, str] {
    lib = _library(engine_dir());
    argv = (ctypes.c_char_p * (len(args) + 1))(b"node", *[a.encode() for a in args]);
    sys.stdout.flush();
    sys.stderr.flush();
    saved_cwd = os.getcwd();
    saved_umask = os.umask(0);
    os.umask(saved_umask);
    main_thread = threading.current_thread() is threading.main_thread();
    saved_sigint = signal.signal(signal.SIGINT, signal.SIG_DFL)
        if main_thread
        else None;
    out = tempfile.TemporaryFile() if capture else None;
    saved_fds: list[int] = [];
    try {
        if out is not None {
            saved_fds = [os.dup(1), os.dup(2)];
            os.dup2(out.fileno(), 1);
            os.dup2(out.fileno(), 2);
        }
        os.chdir(cwd);
        rc = int(lib.js_pm(len(args) + 1, argv));
    } finally {
        os.chdir(saved_cwd);
        os.umask(saved_umask);
        if saved_fds {
            os.dup2(saved_fds[0], 1);
            os.dup2(saved_fds[1], 2);
            for fd in saved_fds {
                os.close(fd);
            }
        }
        if saved_sigint is not None {
            signal.signal(signal.SIGINT, saved_sigint);
        }
    }
    if out is None {
        return (rc, "");
    }
    out.seek(0);
    text = out.read().decode("utf-8", "replace");
    out.close();
    return (rc, text);
}

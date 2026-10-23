"""Python/remote_debugging.c for a build without remote debugging.

JacPython is configured `--without-remote-debug`, so `sys.remote_exec()`
reports the feature as not compiled in, as the C file does in that
configuration. See ../LICENSE.cpython.
"""

import from c {
    def _PySysRemoteDebug_SendExec(pid: i32, tid: i32, path: ptr[u8]) -> i32 {
        PyErr_SetString(
            PyExc_RuntimeError, "Remote debugging support has not been compiled in"
        );
        return i32(-1);
    }
}

"""Python/perf_trampoline.c for a build without perf trampolines.

JacPython does not support `-X perf` or `sys.activate_stack_trampoline()`:
configure leaves PY_HAVE_PERF_TRAMPOLINE undefined, so the interpreter only
reaches these entry points, each the C file's branch for that configuration.
See ../LICENSE.cpython.
"""

import from c {
    def PyUnstable_PerfTrampoline_CompileCode(co: ptr[PyObject]) -> i32 {
        return i32(0);
    }  def _PyIsPerfTrampolineActive -> i32 {
        return i32(0);
    }  def _PyPerfTrampoline_GetCallbacks(callbacks: ptr) -> None {
        return;
    }  def _PyPerfTrampoline_SetCallbacks(callbacks: ptr) -> i32 {
        if not callbacks {
            return i32(-1);
        }
        return i32(0);
    }  def _PyPerfTrampoline_Init(activate: i32) -> i32 {
        return i32(0);
    }  def _PyPerfTrampoline_Fini -> i32 {
        return i32(0);
    }  def PyUnstable_PerfTrampoline_SetPersistAfterFork(enable: i32) -> i32 {
        return i32(0);
    }  def _PyPerfTrampoline_AfterFork_Child -> PyStatus {
        return PyStatus(
            _type=_PyStatus_TYPE_OK, func=ptr[u8](), err_msg=ptr[u8](), exitcode=0
        );
    }
}

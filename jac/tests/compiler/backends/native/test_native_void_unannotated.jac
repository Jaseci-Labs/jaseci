"""A callable with no `-> T` returns None under native, as it does on the server (#7139).

The frontend types a missing return annotation as `NoneType`, but native
lowered it to `i64`, so `v = f(); v is None` was False and every
`if result is None` guard silently stopped firing. Method calls also replaced
a `void` result with an integer zero, so even `-> None` methods were wrong.
Such callables now lower to `void`; a statement call stays native, and a call
whose None result is used as a value refuses with E5092 in the caller, which
then runs on the server.
"""

import ctypes;
import os;
import from tests.support {
    NATIVE_FIXTURES,
    compile_native,
    native_address,
    names_function,
    source_spelled
}
import from jaclang.compiler.backends.py.codegen_shim { generated_python }
import from jaclang.compiler.driver.compile_options { CompileOptions }
import from jaclang.compiler.driver.na_coverage { na_coverage_begin, na_coverage_end }
import from jaclang.compiler.driver.program { JacProgram }

glob _MEMO: dict[str, any] = {};

"""Compile `fixture` once under forced native; return (errors, seams)."""
def refusals(fixture: str) -> tuple[(list[str], list[str])] {
    if fixture in _MEMO {
        return _MEMO[fixture];
    }
    path = os.path.join(NATIVE_FIXTURES, fixture);
    prog = JacProgram();
    na_coverage_begin();
    try {
        prog.compile(file_path=path, options=CompileOptions(force_codespace='native'));
    } finally {
        coverage = na_coverage_end();
    }
    rec = coverage.get(os.path.realpath(path));
    seams = [str(s) for s in ((rec.get("seams") or []) if rec is not None else [])];
    out = ([str(e) for e in prog.errors_had], seams);
    _MEMO[fixture] = out;
    return out;
}

"""Compile the bridge fixture with its native pins, the rest on the server."""
def bridged -> any {
    if "bridge" not in _MEMO {
        prog = JacProgram();
        ir = prog.compile(
            os.path.join(NATIVE_FIXTURES, "na_py_void_interop.jac"),
            options=CompileOptions(default_codespace='server')
        );
        errors = [str(e) for e in prog.errors_had];
        assert not errors , f"Compilation errors: {errors}";
        _MEMO["bridge"] = ir;
    }
    return _MEMO["bridge"];
}


test "a callable without a return annotation lowers to void" {
    (_eng, ir) = compile_native("void_unannotated.jac");
    defines = [
        line
        for line in source_spelled(str(ir.gen.llvm_ir)).splitlines()
        if line.startswith("define")
    ];
    for name in ("bump", "free_fn", "Box.touch", "Box.touch_twice") {
        owned = [
            line
            for line in defines
            if names_function(line, name)
        ];
        assert owned and all(line.startswith("define void") for line in owned) , (
            f"'{name}' has no `-> T` and must return void, got: {owned}"
        );
    }
    assert any(
        line.startswith("define private void") and "__jac_nested_inner" in line
        for line in defines
    ) , "a nested def without `-> T` must return void";
}


test "statement calls of None-returning callables stay native" {
    (eng, _ir) = compile_native("void_unannotated.jac");
    addr = native_address(eng, "run");
    assert addr != 0 , "'run' not found in the JIT engine";
    run = ctypes.CFUNCTYPE(ctypes.c_int64)(addr);
    assert run() == 304 , (
        "three `touch` calls and four `bump` calls: n == 3 and COUNTER == 4"
    );
}


test "using a None call result as a value refuses in the caller" {
    (errors, seams) = refusals("void_binding.jac");
    assert not errors , (
        f"a refused caller must not fail the module (E5020), got: {errors}"
    );
    for caller in (
        "caller",
        "bare_caller",
        "method_caller",
        "bare_method_caller",
        "nested_caller",
        "str_caller"
    ) {
        owned = [
            s
            for s in seams
            if s.startswith(f"{caller}: ")
        ];
        assert len(owned) == 1
            and "[E5092]" in owned[0]
            and "call returning None" in owned[0] , (
            f"{caller} must refuse the None result it uses, got: {seams}"
        );
    }
}


test "the bridge declares a None return in both directions" {
    ir = bridged();
    text = source_spelled(str(ir.gen.llvm_ir));
    assert 'declare void @"py_note"' in text , (
        "native must call the Python `py_note` (no `-> T`) as void"
    );
    for name in ("native_note", "native_ack") {
        assert any(
            line.startswith("define void") and names_function(line, name)
            for line in text.splitlines()
        ) , f"'{name}' must be defined returning void";
    }
    py_src = generated_python(ir.gen);
    assert py_src.count("ctypes.CFUNCTYPE(None, ctypes.c_int64)") == 2 , (
        "both native stubs must declare a None restype instead of reading an int"
    );
    bindings = ir.gen.interop_manifest.bindings;
    for name in ("py_note", "native_note", "native_ack") {
        assert bindings[name].ret_type == "None" , (
            f"'{name}' returns None, got ret_type {bindings[name].ret_type!r}"
        );
    }
}

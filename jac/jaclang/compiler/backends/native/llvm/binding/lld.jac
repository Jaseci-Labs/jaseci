import from ctypes { c_int, c_uint, c_char_p, c_size_t, POINTER }
import from jaclang.compiler.backends.native.llvm.binding { ffi }

glob _LLD_SPENT: list[bool] = [];

def lld_link(args: list[str]) -> tuple[int, str] {
    if _LLD_SPENT {
        raise RuntimeError(
            "LLD crashed earlier in this process and cannot link again; rerun the build"
        );
    }
    argv = (c_char_p * len(args))(*[a.encode("utf-8") for a in args]);
    can_run_again = c_int(1);
    with ffi.OutputString() as out {
        code = ffi.lib.LLVMPY_LldLink(argv, len(args), out, can_run_again);
        text = str(out);
    }
    if not can_run_again.value {
        _LLD_SPENT.append(True);
    }
    return (int(code), text);
}

def write_import_library(
    dll_name: str, path: str, machine: int, names: list[str], data: list[bool]
) {
    c_names = (c_char_p * len(names))(*[n.encode("utf-8") for n in names]);
    c_data = (c_int * len(names))(*[1 if d else 0 for d in data]);
    with ffi.OutputString() as err {
        failed = ffi.lib.LLVMPY_WriteImportLibrary(
            dll_name.encode("utf-8"),
            path.encode("utf-8"),
            machine,
            c_names,
            c_data,
            len(names),
            err
        );
        if failed {
            raise RuntimeError(f"cannot write the import library for {dll_name}: {err}");
        }
    }
}

with entry {
    ffi.lib.LLVMPY_LldLink.argtypes = [
        POINTER(c_char_p),
        c_size_t,
        POINTER(c_char_p),
        POINTER(c_int)
    ];
    ffi.lib.LLVMPY_LldLink.restype = c_int;
    ffi.lib.LLVMPY_WriteImportLibrary.argtypes = [
        c_char_p,
        c_char_p,
        c_uint,
        POINTER(c_char_p),
        POINTER(c_int),
        c_size_t,
        POINTER(c_char_p)
    ];
    ffi.lib.LLVMPY_WriteImportLibrary.restype = c_int;
}

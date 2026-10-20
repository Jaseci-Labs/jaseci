"""posix_floor_ir.jac is generated from the posix_floor.c in the tree.

The floor reaches an artifact as IR text, so the C source and its IR must not
drift apart: editing posix_floor.c means running
`jac run scripts/gen_posix_floor.jac`, which records the source it compiled.
"""
import hashlib;
import from pathlib { Path }
import from jaclang.compiler.backends.native.posix_floor_ir {
    POSIX_FLOOR_SOURCE_SHA256
}
import from jaclang.compiler.backends.native.posix_floor { posix_floor_ir }

test "the floor's IR was generated from the floor's source" {
    import jaclang;
    source = Path(jaclang.__file__).resolve().parent
        / "compiler"
        / "backends"
        / "native"
        / "posix_floor.c";
    digest = hashlib.sha256(source.read_bytes()).hexdigest();
    assert digest == POSIX_FLOOR_SOURCE_SHA256 , (
        "posix_floor.c changed since posix_floor_ir.jac was generated; "
        "run `jac run scripts/gen_posix_floor.jac`"
    );
}

test "every release target has a floor that defines the whole API" {
    for osarch in ["linux-x86_64", "linux-aarch64", "macos-aarch64", "macos-x86_64"] {
        ir = posix_floor_ir(osarch);
        for name in [
            "__jac_errno",
            "__jac_stdio",
            "__jac_platform_id",
            "__jac_stat",
            "__jac_opendir",
            "__jac_readdir",
            "__jac_closedir",
            "__jac_dirent_name",
            "__jac_at_fdcwd",
            "__jac_home_dir",
            "__jac_clock_id",
            "__jac_sleep_ns",
            "__jac_malloc_size",
            "__jac_fmadd",
            "__jac_va_list",
            "__jac_va_i64",
            "__jac_va_f64"
        ] {
            assert f"@{name}(" in ir , f"{osarch} floor lacks {name}";
        }
    }
    assert posix_floor_ir("wasm32") == "";
}

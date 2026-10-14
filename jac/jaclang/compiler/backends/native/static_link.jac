import from jaclang.compiler.backends.native.linker_common {
    object_undefined_symbols,
    select_ar_members,
    ArMember
}

def floor_lib_dir(triple: str) -> (str | None) {
    import from jaclang.artifacts.router { resolve }
    import from jaclang.artifacts.kit { osarch }
    found = resolve(f"c-floor@{osarch(triple)}").found;
    return found.path if found is not None else None;
}

def clib_to_archive_name(clib_path: str) -> str {
    import os;
    return os.path.basename(clib_path).split(".")[0] + ".a";
}

def collect_floor_archives(
    clib_paths: list[str], clib_symbol_lib: dict[str, str], triple: str, is_macos: bool
) -> tuple[list[bytes], set[str]] {
    import os;
    member_bytes: list[bytes] = [];
    handled: set[str] = set();

    tl = triple.lower();
    is_pe = ("windows" in tl) or ("win32" in tl) or ("msvc" in tl) or ("mingw" in tl);
    if is_pe or not clib_paths {
        return (member_bytes, handled);
    }
    lib_dir = floor_lib_dir(triple);
    if lib_dir is None {
        return (member_bytes, handled);
    }

    syms_by_lib: dict[str, list[str]] = {};
    for (sym, raw) in clib_symbol_lib.items() {
        syms_by_lib.setdefault(raw, []).append(sym);
    }

    archives: dict[str, bytes] = {};
    paths_by_archive: dict[str, list[str]] = {};
    roots: list[str] = [];
    for clib_path in clib_paths {
        arch_file = os.path.join(lib_dir, clib_to_archive_name(clib_path));
        if not os.path.isfile(arch_file) {
            continue;
        }
        paths_by_archive.setdefault(arch_file, []).append(clib_path);
        if arch_file not in archives {
            with open(arch_file, "rb") as _f {
                archives[arch_file] = _f.read();
            }
        }
        for s in syms_by_lib.get(clib_path, []) {
            roots.append(("_" + s) if is_macos else s);
        }
    }
    """Select to a fixpoint across the archives: a member one archive
    contributes can call into another (libssl's members need libcrypto's).""";
    known: set[str] = set(roots);
    selected: dict[str, list[ArMember]] = {};
    while True {
        selected = {
            arch_file: select_ar_members(data, roots)
            for (arch_file, data) in archives.items()
        };
        added = False;
        for members in selected.values() {
            for m in members {
                for u in object_undefined_symbols(m.data) {
                    if u not in known {
                        known.add(u);
                        roots.append(u);
                        added = True;
                    }
                }
            }
        }
        if not added {
            break;
        }
    }
    for (arch_file, members) in selected.items() {
        if not members {
            continue;
        }
        for m in members {
            member_bytes.append(m.data);
        }
        for p in paths_by_archive[arch_file] {
            handled.add(p);
        }
    }
    return (member_bytes, handled);
}


def elf_runtime_soname(name: str) -> str {
    import ctypes.util;
    import re;
    matched = re.fullmatch(r"lib([^/]+)\.so", name);
    if matched is None {
        return name;
    }
    try {
        found = ctypes.util.find_library(matched.group(1));
    } except Exception {
        return name;
    }
    if found and "/" not in found and found.startswith(name + ".") {
        return found;
    }
    return name;
}

def clib_needed_libs(
    needed_libs: list[str],
    clib_paths: list[str],
    floor_handled: set[str],
    host_elf: bool = False
) -> dict[str, str] {
    import os;
    lib_norm: dict[str, str] = {};
    for lib_path in clib_paths {
        if lib_path in floor_handled {
            continue;
        }
        needed = lib_path;
        if (not os.path.isabs(lib_path))
            and (not lib_path.startswith("$"))
            and (not lib_path.startswith("@"))
            and ("/" in lib_path or "\\" in lib_path) {
            needed = os.path.basename(lib_path);
        }
        base = os.path.basename(needed);
        if base == "libc.so" {
            needed = "libc.so.6";
        } elif base == "libm.so" {
            needed = "libm.so.6";
        } elif base in ["libc.dylib", "libm.dylib"] {
            needed = "/usr/lib/libSystem.B.dylib";
        } elif host_elf and needed == base {
            needed = elf_runtime_soname(base);
        }
        if needed not in needed_libs {
            needed_libs.append(needed);
        }
        lib_norm[lib_path] = needed;
    }
    return lib_norm;
}


def clib_symbol_lib_map(
    clib_symbol_lib: dict[str, str],
    floor_handled: set[str],
    lib_norm: dict[str, str],
    shared: bool,
    is_macos: bool
) -> dict[str, str] {
    symbol_lib_map: dict[str, str] = {};
    for (sym, raw) in clib_symbol_lib.items() {
        if raw in floor_handled {
            continue;
        }
        if shared and is_macos {
            symbol_lib_map[sym] = "@process";
        } else {
            symbol_lib_map[sym] = lib_norm.get(raw, raw);
        }
    }
    return symbol_lib_map;
}

def musl_lib_dir(triple: str) -> (str | None) {
    import from jaclang.artifacts.router { resolve }
    import from jaclang.artifacts.kit { osarch }
    found = resolve(f"musl@{osarch(triple)}").found;
    return found.path if found is not None else None;
}

obj StaticRuntime {
    has archives: list[bytes],
        crt_objects: list[bytes];

    def select(objects: list[bytes]) -> list[bytes] {
        import hashlib;
        work_roots: list[str] = [];
        known: set[str] = set();
        for blob in list(objects) + self.crt_objects {
            for u in object_undefined_symbols(blob) {
                if u not in known {
                    known.add(u);
                    work_roots.append(u);
                }
            }
        }

        member_bytes: list[bytes] = [];
        seen_members: set[bytes] = set();
        changed = True;
        while changed {
            changed = False;
            for data in self.archives {
                for m in select_ar_members(data, work_roots) {
                    key = hashlib.sha256(m.data).digest();
                    if key in seen_members {
                        continue;
                    }
                    seen_members.add(key);
                    member_bytes.append(m.data);
                    changed = True;
                    for u in object_undefined_symbols(m.data) {
                        if u not in known {
                            known.add(u);
                            work_roots.append(u);
                        }
                    }
                }
            }
        }
        return member_bytes;
    }
}

def load_outline_atomics(triple: str) -> (StaticRuntime | None) {
    import os;
    import from jaclang.runtime.graph_utils { triple_arch }
    if triple_arch(triple) != "aarch64" or "linux" not in triple {
        return None;
    }
    lib_dir = musl_lib_dir(triple);
    if lib_dir is None {
        return None;
    }
    path = os.path.join(lib_dir, "libclang_rt.atomics.a");
    if not os.path.isfile(path) {
        return None;
    }
    with open(path, "rb") as archive {
        return StaticRuntime(archives=[archive.read()], crt_objects=[]);
    }
}

def load_musl_static(triple: str) -> (StaticRuntime | None) {
    import os;
    lib_dir = musl_lib_dir(triple);
    if lib_dir is None {
        return None;
    }
    libc_a = os.path.join(lib_dir, "libc.a");
    if not os.path.isfile(libc_a) {
        return None;
    }

    crt_objects: list[bytes] = [];
    have_crt1 = False;
    for crt_name in ["crt1.o", "crti.o", "crtn.o"] {
        p = os.path.join(lib_dir, crt_name);
        if os.path.isfile(p) {
            with open(p, "rb") as cf {
                crt_objects.append(cf.read());
            }
            if crt_name == "crt1.o" {
                have_crt1 = True;
            }
        }
    }
    if not have_crt1 {
        return None;
    }

    archives_data: list[bytes] = [];
    for af in ["libc.a", "libzigc.a", "libcompiler_rt.a", "libmusl_compat.a"] {
        p = os.path.join(lib_dir, af);
        if os.path.isfile(p) {
            with open(p, "rb") as archive {
                archives_data.append(archive.read());
            }
        }
    }

    return StaticRuntime(archives=archives_data, crt_objects=crt_objects);
}

def collect_musl_static(
    objects: list[bytes], triple: str
) -> (tuple[list[bytes], list[bytes]] | None) {
    runtime = load_musl_static(triple);
    if runtime is None {
        return None;
    }
    return (runtime.select(objects), runtime.crt_objects);
}

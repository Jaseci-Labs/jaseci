"""Metadata refreshes must not make obsolete executable sections look fresh.

The Python lane's products (bytecode, interop manifest, module IR, client
artifact) are judged by the interop manifest a writer brings. Native unit
products are stamped with the native ABI and their codegen, so a Python-lane
refresh never disturbs them, and a native unit persisting its products never
disturbs the Python lane's manifest.
"""
import from pathlib { Path }
import from tempfile { TemporaryDirectory }
import from jaclang.compiler.driver.jir {
    SEC_BYTECODE,
    SEC_NBITCODE,
    SEC_NOBJ,
    SEC_INTEROP,
    SEC_IFACE,
    NativeStamp,
    write_module_cache,
    get_module_cache_path,
    native_section_payload,
    read_section_bytes
}

glob STAMP: NativeStamp = NativeStamp(
         abi="c" * 64, codegen_identity="gc=rc", triple="x86_64-linux"
     );

obj CacheFixture {
    has source: Path,
        dep: Path;

    def seed(interop: (bytes | None) = b"old interop") {
        self.source.write_text("import from .dep { value }\n");
        self.dep.write_text("def value() -> int { return 1; }\n");
        sections: dict[int, bytes] = {
            SEC_IFACE: b"valid interface",
            SEC_NBITCODE: STAMP.pack(b"old native bitcode"),
            SEC_NOBJ: STAMP.pack(b"old native object")
        };
        if interop is not None {
            sections[SEC_INTEROP] = interop;
        }
        write_module_cache(str(self.source), b"old bytecode", extra_sections=sections);
    }

    def data -> bytes {
        return get_module_cache_path(str(self.source)).read_bytes();
    }

    def native(kind: int) -> (bytes | None) {
        return native_section_payload(read_section_bytes(self.data(), kind), STAMP);
    }
}

def fixture_in(directory: str) -> CacheFixture {
    fixture = CacheFixture(
        source=Path(directory) / "main.jac", dep=Path(directory) / "dep.jac"
    );
    fixture.seed();
    return fixture;
}

test "metadata refresh cannot pair bytecode with a different library manifest" {
    with TemporaryDirectory() as directory {
        fixture = fixture_in(directory);
        write_module_cache(
            str(fixture.source),
            None,
            extra_sections={SEC_INTEROP: b"empty interop"}
        );
        assert read_section_bytes(fixture.data(), SEC_BYTECODE) is None;
        assert read_section_bytes(fixture.data(), SEC_INTEROP) == b"empty interop";
        assert read_section_bytes(fixture.data(), SEC_IFACE) == b"valid interface";
        assert fixture.native(SEC_NBITCODE) == b"old native bitcode";
    }
}

test "unchanged library manifest preserves executable sections without rewriting" {
    with TemporaryDirectory() as directory {
        fixture = fixture_in(directory);
        before = fixture.data();
        assert not write_module_cache(
            str(fixture.source), None, extra_sections={SEC_INTEROP: b"old interop"}
        );
        assert fixture.data() == before;
    }
}

test "replacing a unit's bitcode drops the object emitted from the old bitcode" {
    with TemporaryDirectory() as directory {
        fixture = fixture_in(directory);
        write_module_cache(
            str(fixture.source),
            None,
            extra_sections={SEC_NBITCODE: STAMP.pack(b"new bitcode")}
        );
        assert fixture.native(SEC_NOBJ) is None;
        assert fixture.native(SEC_NBITCODE) == b"new bitcode";
        assert read_section_bytes(fixture.data(), SEC_BYTECODE) == b"old bytecode";
        assert read_section_bytes(fixture.data(), SEC_INTEROP) == b"old interop";
        write_module_cache(
            str(fixture.source),
            None,
            extra_sections={SEC_NOBJ: STAMP.pack(b"new object")}
        );
        assert fixture.native(SEC_NOBJ) == b"new object";
        assert fixture.native(SEC_NBITCODE) == b"new bitcode";
    }
}

test "a native unit persisting its products leaves the bytecode lane's manifest alone" {
    with TemporaryDirectory() as directory {
        fixture = fixture_in(directory);
        write_module_cache(
            str(fixture.source),
            None,
            extra_sections={
                SEC_INTEROP: b"native interop",
                SEC_NBITCODE: STAMP.pack(b"new bitcode")
            }
        );
        assert read_section_bytes(fixture.data(), SEC_BYTECODE) == b"old bytecode";
        assert read_section_bytes(fixture.data(), SEC_INTEROP) == b"old interop";
        assert fixture.native(SEC_NBITCODE) == b"new bitcode";
    }
}

test "a native unit fills in the manifest when no bytecode compile wrote one" {
    with TemporaryDirectory() as directory {
        fixture = CacheFixture(
            source=Path(directory) / "main.jac", dep=Path(directory) / "dep.jac"
        );
        fixture.seed(interop=None);
        write_module_cache(
            str(fixture.source),
            None,
            extra_sections={
                SEC_INTEROP: b"native interop",
                SEC_NBITCODE: STAMP.pack(b"new bitcode")
            }
        );
        assert read_section_bytes(fixture.data(), SEC_BYTECODE) == b"old bytecode";
        assert read_section_bytes(fixture.data(), SEC_INTEROP) == b"native interop";
    }
}

glob OTHER_CODEGEN: NativeStamp = NativeStamp(
         abi="c" * 64, codegen_identity="gc=none", triple="x86_64-linux"
     ),
     OTHER_ABI: NativeStamp = NativeStamp(
         abi="d" * 64, codegen_identity="gc=rc", triple="x86_64-linux"
     );

test "stamped variants for another codegen identity coexist" {
    with TemporaryDirectory() as directory {
        fixture = fixture_in(directory);
        write_module_cache(
            str(fixture.source),
            None,
            extra_sections={SEC_NBITCODE: OTHER_CODEGEN.pack(b"nogc bitcode")}
        );
        raw = read_section_bytes(fixture.data(), SEC_NBITCODE);
        assert native_section_payload(raw, STAMP) == b"old native bitcode";
        assert native_section_payload(raw, OTHER_CODEGEN) == b"nogc bitcode";
        assert fixture.native(SEC_NOBJ) == b"old native object";
    }
}

test "a native write prunes every section's variants from another native ABI" {
    with TemporaryDirectory() as directory {
        fixture = fixture_in(directory);
        write_module_cache(
            str(fixture.source),
            None,
            extra_sections={SEC_NBITCODE: OTHER_ABI.pack(b"upgraded bitcode")}
        );
        raw = read_section_bytes(fixture.data(), SEC_NBITCODE);
        assert native_section_payload(raw, OTHER_ABI) == b"upgraded bitcode";
        assert native_section_payload(raw, STAMP) is None;
        assert fixture.native(SEC_NOBJ) is None;
        assert read_section_bytes(fixture.data(), SEC_BYTECODE) == b"old bytecode";
    }
}

test "module cache writes lock through a pool instead of a sibling per entry" {
    with TemporaryDirectory() as directory {
        fixture = fixture_in(directory);
        cache_path = get_module_cache_path(str(fixture.source));
        assert cache_path.is_file();
        assert not cache_path.with_suffix(".lock").exists();
        pool = cache_path.parent / ".locks";
        assert pool.is_dir();
        assert all(lock_file.suffix == ".lock" for lock_file in pool.iterdir());
    }
}

"""What a compiler identity covers, and where a module's cache entry lives.

Module caches are keyed on each module's own source, so the compiler identity
no longer reaches them. It still names whole artifacts (sealed images and
release payloads), and these tests pin which inputs it covers. A module has
exactly one cache entry, directly under its cache root.
"""

import os;
import tempfile;
import from pathlib { Path }
import from jaclang.compiler.driver.jir { get_module_cache_path, get_native_debug_dir }

def _seeded_module -> str {
    tmp = tempfile.mkdtemp();
    src = os.path.join(tmp, "mod.jac");
    with open(src, "w") as f {
        f.write("with entry { print('x'); }\n");
    }
    return src;
}

test "a module has one cache entry, directly under its cache root" {
    src = _seeded_module();
    entry = get_module_cache_path(src);
    assert entry == get_module_cache_path(src);
    assert entry.suffix == ".jir";
    assert entry.parent == get_native_debug_dir(src).parent , (
        "a module entry sits below another directory than its cache root"
    );
}

test "native debug output sits beside the module entries" {
    src = _seeded_module();
    assert get_native_debug_dir(src).name == "native-debug";
}

test "JacPython sources participate in the producing compiler identity" {
    import from jaclang.compiler.driver.jir { compiler_source_digest }
    prefixes = (
        "compiler/frontend/python/",
        "compiler/backends/py/jacpython/",
        "runtime/python/"
    );
    with tempfile.TemporaryDirectory() as pkg {
        for prefix in prefixes {
            src = Path(pkg) / prefix / "module.jac";
            src.parent.mkdir(parents=True, exist_ok=True);
            src.write_text("def f() -> int { return 1; }\n");
            before = compiler_source_digest(pkg);
            src.write_text("def f() -> int { return 2; }\n");
            assert compiler_source_digest(pkg) != before;
        }
    }
}

test "a pruned staging resolves compiler identity from its recorded hashes" {
    # The payload drops the natively lowered trees (they live in JacPython's
    # native object, not as source), so a staged jaclang holds fewer files than
    # the checkout it was built from. Identity must still describe the SAME
    # compiler: the staging records what it dropped and the digest resolves
    # those inputs from the record. Without the record it must refuse to report
    # an identity at all -- silently reporting a smaller one is how a payload
    # and its own checkout came to disagree.
    import from jaclang.compiler.driver.jir {
        compiler_source_digest,
        write_compiler_identity
    }
    import shutil;
    with tempfile.TemporaryDirectory() as tmp {
        full = Path(tmp) / "full";
        full.mkdir();
        (full / "compiler_inputs.txt").write_text("compiler\nruntime\n");
        for rel in (
            "compiler/pass.jac",
            "compiler/frontend/python/ast_input.jac",
            "compiler/backends/py/jacpython/assembler.jac",
            "runtime/python/bindings/heapq.jac"
        ) {
            f = full / rel;
            f.parent.mkdir(parents=True, exist_ok=True);
            f.write_text("def f -> int { return 1; }\n");
        }
        expected = compiler_source_digest(str(full));
        pruned = Path(tmp) / "pruned";
        shutil.copytree(full, pruned);
        for prefix in (
            "compiler/frontend/python",
            "compiler/backends/py/jacpython",
            "runtime/python"
        ) {
            shutil.rmtree(pruned / prefix);
        }
        raised = False;
        try {
            compiler_source_digest(str(pruned));
        } except RuntimeError {
            raised = True;
        }
        assert raised , "a pruned staging with no record reported an identity";
        write_compiler_identity(str(full), str(pruned));
        assert compiler_source_digest(str(pruned)) == expected;
        # The record completes identity; it never overrides a present source.
        (pruned / "compiler/pass.jac").write_text("def f -> int { return 2; }\n");
        assert compiler_source_digest(str(pruned)) != expected;
    }
}

test "compiler identity excludes applications tests and generated artifacts" {
    import from jaclang.compiler.driver.jir { compiler_source_digest }
    with tempfile.TemporaryDirectory() as pkg {
        src = Path(pkg) / "compiler/pass.jac";
        src.parent.mkdir(parents=True);
        src.write_text("def f -> int { return 1; }\n");
        before = compiler_source_digest(pkg);
        for rel in (
            "scale/app.jac",
            "byllm/app.jac",
            "compiler/tests/fixture.jac",
            "compiler/pass.test.jac",
            "runtime/test/fixture.py",
            "compiler/.generated/input.py",
            "compiler/libjacllvm.so"
        ) {
            unrelated = Path(pkg) / rel;
            unrelated.parent.mkdir(parents=True, exist_ok=True);
            unrelated.write_text("unrelated");
            assert compiler_source_digest(pkg) == before , rel;
        }
        src.rename(src.with_name("renamed.jac"));
        renamed = compiler_source_digest(pkg);
        assert renamed != before;
        src.with_name("renamed.jac").unlink();
        assert compiler_source_digest(pkg) != renamed;
    }
}

test "native-only units join the compiler identity by path, not by content" {
    import from jaclang.compiler.driver.jir { compiler_source_digest }
    with tempfile.TemporaryDirectory() as pkg {
        unit = Path(pkg) / "runtime/na_stdlib/fnmatch.jac";
        unit.parent.mkdir(parents=True);
        unit.write_text("def f -> int { return 1; }\n");
        compiler = Path(pkg) / "compiler/pass.jac";
        compiler.parent.mkdir(parents=True);
        compiler.write_text("def f -> int { return 1; }\n");
        before = compiler_source_digest(pkg);
        unit.write_text("def f -> int { return 2; }\n");
        assert compiler_source_digest(pkg) == before , (
            "an edit to a native-only unit changed the compiler identity"
        );
        added = Path(pkg) / "runtime/na_stdlib/glob.jac";
        added.write_text("def g -> int { return 1; }\n");
        assert compiler_source_digest(pkg) != before , (
            "adding a native-only unit left the compiler identity unchanged"
        );
        added.unlink();
        assert compiler_source_digest(pkg) == before;
        compiler.write_text("def f -> int { return 2; }\n");
        assert compiler_source_digest(pkg) != before;
    }
}

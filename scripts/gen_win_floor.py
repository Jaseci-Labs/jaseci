#!/usr/bin/env python3
"""Regenerate win_floor_ir.jac from win_floor.c.

The Windows floor (jac/jaclang/compiler/backends/native/win_floor.c) reaches a
PE image as LLVM IR text carried by the link glue, so building a Windows image
needs no C toolchain. This script is the one place a C compiler is involved:
it compiles the floor with `zig cc` (any clang that targets
x86_64-windows-msvc will do, via CC), strips what is specific to that
compiler's build, and writes the IR and the table of the floor's kernel32
imports as a Jac module.

    python3 scripts/gen_win_floor.py
"""

import os
import re
import shlex
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NATIVE = os.path.join(ROOT, "jac", "jaclang", "compiler", "backends", "native")
SOURCE = os.path.join(NATIVE, "win_floor.c")
OUTPUT = os.path.join(NATIVE, "win_floor_ir.jac")

DROPPED_ATTRIBUTES = (
    "target-cpu",
    "target-features",
    "tune-cpu",
    "stack-protector-buffer-size",
    "min-legal-vector-width",
    "no-trapping-math",
    "frame-pointer",
)


def compile_ir() -> str:
    compiler = shlex.split(os.environ.get("CC", "zig cc"))
    with tempfile.TemporaryDirectory() as scratch:
        out = os.path.join(scratch, "win_floor.ll")
        command = compiler + [
            "-target", "x86_64-windows-msvc",
            "-ffreestanding", "-nostdinc", "-fno-stack-protector",
            "-O2", "-g0", "-Wall", "-Wextra",
            "-S", "-emit-llvm", "-o", out, SOURCE,
        ]
        done = subprocess.run(command, capture_output=True, text=True)
        if done.returncode != 0:
            sys.exit(done.stderr)
        for line in done.stderr.splitlines():
            if "argument unused" not in line:
                print(line, file=sys.stderr)
        with open(out, encoding="utf-8") as handle:
            return handle.read()


def clean(ir: str) -> str:
    lines = []
    for line in ir.splitlines():
        if line.startswith(("; ModuleID", "source_filename", "target ", "!")):
            continue
        if line.startswith("; Function Attrs"):
            continue
        line = re.sub(r", ![A-Za-z_.]+ !\d+", "", line)
        if line.startswith("attributes #"):
            for name in DROPPED_ATTRIBUTES:
                line = re.sub(r' "%s"="[^"]*"' % re.escape(name), "", line)
        lines.append(line.rstrip())
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def kernel32_names(source: str) -> list[str]:
    start = source.index("/* ---- kernel32.dll ---- */")
    end = source.index("#define CP_UTF8")
    return re.findall(r"\b([A-Za-z_]\w*)\(", source[start:end])


def main() -> None:
    with open(SOURCE, encoding="utf-8") as handle:
        source = handle.read()
    ir = clean(compile_ir())
    if '"""' in ir:
        sys.exit("the floor's IR holds a triple quote; it cannot be a raw string")
    declared = set(re.findall(r"^declare [^@]*@(\w+)\(", ir, re.M))
    imports = [name for name in kernel32_names(source) if name in declared]
    out = [
        '"""The Windows floor as LLVM IR. Generated from win_floor.c by',
        'scripts/gen_win_floor.py; edit that file and regenerate, not this one."""',
        "",
        '"""The kernel32 functions the floor imports."""',
        "glob WIN_FLOOR_KERNEL32: list[str] = [",
    ]
    # Laid out as `jac fmt` lays a glob's list out, so the formatter leaves it alone.
    out += ['         "%s"%s' % (name, "," if i + 1 < len(imports) else "") for i, name in enumerate(imports)]
    out += ["     ];", "", 'glob WIN_FLOOR_IR: str = r"""', ir.rstrip("\n"), '""";', ""]
    with open(OUTPUT, "w", encoding="utf-8") as handle:
        handle.write("\n".join(out))
    print(f"wrote {os.path.relpath(OUTPUT, ROOT)}: {len(ir.splitlines())} lines of IR, {len(imports)} kernel32 imports")


if __name__ == "__main__":
    main()

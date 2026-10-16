"""The repository's own archwire.jac files hold true facts in canonical form.

The payload drops the natively lowered subtrees whole, so an archwire.jac that
ships must not wire a module the payload drops; and every archwire.jac in the
tree must already be in the layout `jac fmt` renders.
"""

import os;
import jaclang;
import from jaclang.compiler.driver.program { JacProgram }
import from jaclang.compiler.driver.wiring { ARCH_FILE_NAME, wiring_for_path }
import from jaclang.dist.payload.fsutil { skip_jaclang }

glob _PKG: str = os.path.dirname(os.path.realpath(jaclang.__file__));


def _arch_files(top: str) -> list[str] {
    found: list[str] = [];
    for (dirpath, dirnames, filenames) in os.walk(top) {
        dirnames[:] = sorted(
            [
                d
                for d in dirnames
                if not d.startswith(".") and d not in ("node_modules", "__pycache__")
            ]
        );
        if ARCH_FILE_NAME in filenames {
            found.append(os.path.join(dirpath, ARCH_FILE_NAME));
        }
    }
    return found;
}


def _dropped(path: str) -> bool {
    return skip_jaclang(os.path.relpath(os.path.realpath(path), _PKG).replace(os.sep, "/"));
}


test "no archwire.jac the payload ships wires a module the payload drops" {
    shipped = [
        path
        for path in _arch_files(_PKG)
        if not _dropped(path)
    ];
    assert shipped;
    stray: list[str] = [];
    for arch in shipped {
        spec = wiring_for_path(arch);
        assert spec is not None , arch;
        for wire in spec.wires {
            heads = [wire.provider];
            for consumer in wire.consumers {
                split = spec.split_consumer(consumer);
                heads.append(split[0] if split is not None else consumer);
            }
            for head in heads {
                found = spec.module_file(head);
                if found is not None and _dropped(found) {
                    stray.append(f"{os.path.relpath(arch, _PKG)}:{wire.line} {head}");
                }
            }
        }
    }
    assert not stray , f"{len(stray)} wires reach dropped modules, e.g. {stray[:5]}";
}


test "every archwire.jac in the tree is in canonical layout" {
    tops = [_PKG, os.path.join(os.path.dirname(_PKG), "examples")];
    files = [
        path for top in tops
        if os.path.isdir(top)
        for path in _arch_files(top)
    ];
    assert files;
    drifted: list[str] = [];
    for path in files {
        with open(path) as f {
            text = f.read();
        }
        prog = JacProgram.jac_file_formatter(path);
        assert not prog.errors_had , (path, [str(e) for e in prog.errors_had[:3]]);
        if prog.mod.main.gen.jac != text {
            drifted.append(path);
        }
    }
    assert not drifted , drifted;
}

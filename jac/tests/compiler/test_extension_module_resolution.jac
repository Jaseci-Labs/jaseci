"""Python extension modules are valid providers for relative imports."""

import from importlib.machinery { EXTENSION_SUFFIXES }
import from pathlib { Path }
import from tempfile { TemporaryDirectory }
import from jaclang.compiler.driver.compile_options { CompileOptions }
import from jaclang.compiler.driver.program { JacProgram }
import from jaclang.project.modresolver { resolve_local_module, resolve_module }


test "relative imports resolve the host's Python extension suffixes" {
    with TemporaryDirectory() as directory {
        workspace = Path(directory);
        importer = workspace / '__init__.py';
        importer.write_text('');
        for suffix in EXTENSION_SUFFIXES {
            extension = workspace / f'_compiled{suffix}';
            extension.write_bytes(b'');
            try {
                assert resolve_local_module(directory, ['_compiled'])
                    == (str(extension), 'py');
                assert resolve_module('._compiled', str(importer))
                    == (str(extension), 'py');
            } finally {
                extension.unlink();
            }
        }
    }
}


test "a Python library's relative extension import is not a missing-module error" {
    with TemporaryDirectory() as directory {
        workspace = Path(directory);
        package = workspace / 'extension_pkg';
        package.mkdir();
        (package / '__init__.py').write_text('');
        (package / f'_compiled{EXTENSION_SUFFIXES[0]}').write_bytes(b'');
        (package / 'api.py').write_text(
            'from ._compiled import Marker\n\n'
            'def marker() -> Marker:\n'
            '    raise NotImplementedError\n'
        );
        entry_file = workspace / 'main.jac';
        entry_file.write_text(
            'import from extension_pkg.api { marker }\n\n'
            'def read_marker -> any { return marker(); }\n'
        );
        program = JacProgram();
        program.compile(str(entry_file), options=CompileOptions(no_cgen=True));
        assert program.errors_had == [] , [str(e) for e in program.errors_had];
    }
}


test "source modules keep their precedence over Python extensions" {
    with TemporaryDirectory() as directory {
        workspace = Path(directory);
        (workspace / f'provider{EXTENSION_SUFFIXES[0]}').write_bytes(b'');
        sources = [('.jac', 'jac'), ('.py', 'py'), ('.pyi', 'pyi'), ('.js', 'js')];
        for (suffix, language) in sources {
            (workspace / f'provider{suffix}').write_text('');
        }
        for (suffix, language) in sources {
            source = workspace / f'provider{suffix}';
            assert resolve_local_module(directory, ['provider'])
                == (str(source), language);
            source.unlink();
        }
    }
}


test "package initializers keep their precedence over Python extensions" {
    with TemporaryDirectory() as directory {
        workspace = Path(directory);
        package = workspace / 'provider';
        package.mkdir();
        initializer = package / '__init__.py';
        initializer.write_text('');
        (workspace / f'provider{EXTENSION_SUFFIXES[0]}').write_bytes(b'');
        assert resolve_local_module(directory, ['provider'])
            == (str(initializer), 'py');
    }
}


test "Jac namespace packages still resolve without a Python initializer" {
    with TemporaryDirectory() as directory {
        workspace = Path(directory);
        package = workspace / 'namespace_pkg';
        package.mkdir();
        (package / 'child.jac').write_text('');
        entry_file = workspace / 'main.jac';
        entry_file.write_text('');
        assert resolve_module('namespace_pkg', str(entry_file))
            == (str(package), 'jac');
    }
}


test "absent extension modules remain unresolved" {
    with TemporaryDirectory() as directory {
        workspace = Path(directory);
        (workspace / f'_other{EXTENSION_SUFFIXES[0]}').write_bytes(b'');
        assert resolve_local_module(directory, ['_missing']) is None;
        assert resolve_local_module(directory, ['_other_extra']) is None;
    }
}

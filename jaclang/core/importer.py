"""Special Imports for Jac Code."""

import marshal
import sys
import types
from os import path
from typing import Optional

from jaclang.compiler.absyntree import Module
from jaclang.compiler.compile import compile_jac
from jaclang.compiler.constant import Constants as Con
from jaclang.utils.log import logging


def jac_importer(
    target: str,
    base_path: str,
    cachable: bool = True,
    override_name: Optional[str] = None,
    mod_bundle: Optional[Module] = None,
) -> Optional[types.ModuleType]:
    """Core Import Process."""
    dir_path, file_name = path.split(path.join(*(target.split("."))) + ".jac")

    module_name = path.splitext(file_name)[0]
    package_path = dir_path.replace(path.sep, ".")

    if package_path and f"{package_path}.{module_name}" in sys.modules:
        return sys.modules[f"{package_path}.{module_name}"]
    elif not package_path and module_name in sys.modules:
        return sys.modules[module_name]

    caller_dir = path.dirname(base_path) if not path.isdir(base_path) else base_path
    caller_dir = path.dirname(caller_dir) if target.startswith("..") else caller_dir
    caller_dir = path.join(caller_dir, dir_path)

    full_target = path.normpath(path.join(caller_dir, file_name))

    if mod_bundle:
        codeobj = (
            mod_bundle.gen.py_bytecode
            if full_target == mod_bundle.loc.mod_path
            else mod_bundle.mod_deps[full_target].gen.py_bytecode
        )
        if isinstance(codeobj, bytes):
            codeobj = marshal.loads(codeobj)
    else:
        gen_dir = path.join(caller_dir, Con.JAC_GEN_DIR)
        pyc_file_path = path.join(gen_dir, module_name + ".jbc")
        if (
            cachable
            and path.exists(pyc_file_path)
            and path.getmtime(pyc_file_path) > path.getmtime(full_target)
        ):
            with open(pyc_file_path, "rb") as f:
                codeobj = marshal.load(f)
        else:
            result = compile_jac(full_target, cache_result=cachable)
            if result.errors_had or not result.ir.gen.py_bytecode:
                for e in result.errors_had:
                    print(e)
                    logging.error(e)
                return None
            else:
                codeobj = marshal.loads(result.ir.gen.py_bytecode)

    module_name = override_name if override_name else module_name
    module = types.ModuleType(module_name)
    module.__file__ = full_target
    module.__name__ = module_name
    module.__dict__["__jac_mod_bundle__"] = mod_bundle

    if package_path:
        parts = package_path.split(".")
        for i in range(len(parts)):
            package_name = ".".join(parts[: i + 1])
            if package_name not in sys.modules:
                sys.modules[package_name] = types.ModuleType(package_name)

        setattr(sys.modules[package_path], module_name, module)
        sys.modules[f"{package_path}.{module_name}"] = module
    sys.modules[module_name] = module

    path_added = False
    if caller_dir not in sys.path:
        sys.path.append(caller_dir)
        path_added = True
    if not codeobj:
        raise ImportError(f"No bytecode found for {full_target}")
    exec(codeobj, module.__dict__)
    if path_added:
        sys.path.remove(caller_dir)

    return module

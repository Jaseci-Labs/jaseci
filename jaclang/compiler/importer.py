"""Special Imports for Jac Code."""
import inspect
import marshal
import sys
import types
from os import path
from typing import Optional

from jaclang.compiler.constant import Constants as Con
from jaclang.compiler.transpiler import transpile_jac
from jaclang.utils.log import logging


def jac_import(
    target: str,
    base_path: Optional[str] = None,
    cachable: bool = True,
    override_name: Optional[str] = None,
) -> Optional[types.ModuleType]:
    """Core Import Process."""
    dir_path, file_name = path.split(path.join(*(target.split("."))) + ".jac")

    module_name = path.splitext(file_name)[0]
    package_path = dir_path.replace(path.sep, ".")

    if package_path and f"{package_path}.{module_name}" in sys.modules:
        return sys.modules[f"{package_path}.{module_name}"]
    elif not package_path and module_name in sys.modules:
        return sys.modules[module_name]

    if base_path:
        caller_dir = path.dirname(base_path) if not path.isdir(base_path) else base_path
    else:
        frame = inspect.stack()[1]
        caller_dir = path.dirname(path.abspath(frame[0].f_code.co_filename))
    caller_dir = path.dirname(caller_dir) if target.startswith("..") else caller_dir
    caller_dir = path.join(caller_dir, dir_path)

    gen_dir = path.join(caller_dir, Con.JAC_GEN_DIR)
    full_target = path.normpath(path.join(caller_dir, file_name))

    py_file_path = path.join(gen_dir, module_name + ".py")
    pyc_file_path = path.join(gen_dir, module_name + ".jbc")
    if (
        cachable
        and path.exists(py_file_path)
        and path.getmtime(py_file_path) > path.getmtime(full_target)
    ):
        with open(pyc_file_path, "rb") as f:
            codeobj = marshal.load(f)
    else:
        if error := transpile_jac(full_target):
            if error:
                for e in error:
                    print(e)
                    logging.error(e)
            return None
        with open(pyc_file_path, "rb") as f:
            codeobj = marshal.load(f)

    module_name = override_name if override_name else module_name
    module = types.ModuleType(module_name)
    module.__file__ = full_target
    module.__name__ = module_name

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
    exec(codeobj, module.__dict__)
    if path_added:
        sys.path.remove(caller_dir)

    return module

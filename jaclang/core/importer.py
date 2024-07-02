"""Special Imports for Jac Code."""

import importlib
import marshal
import sys
import types
from os import getcwd, path
from typing import Optional, Union

from jaclang.compiler.absyntree import Module
from jaclang.compiler.compile import compile_jac
from jaclang.compiler.constant import Constants as Con
from jaclang.core.utils import sys_path_context


def jac_importer(
    target: str,
    base_path: str,
    absorb: bool = False,
    cachable: bool = True,
    mdl_alias: Optional[str] = None,
    override_name: Optional[str] = None,
    mod_bundle: Optional[Module | str] = None,
    lng: Optional[str] = "jac",
    items: Optional[dict[str, Union[str, bool]]] = None,
) -> Optional[types.ModuleType]:
    """Core Import Process."""
    dir_path, file_name = path.split(
        path.join(*(target.split("."))) + (".jac" if lng == "jac" else ".py")
    )
    module_name = path.splitext(file_name)[0]
    package_path = dir_path.replace(path.sep, ".")

    if (
        not override_name
        and package_path
        and f"{package_path}.{module_name}" in sys.modules
    ):
        return sys.modules[f"{package_path}.{module_name}"]
    elif not override_name and not package_path and module_name in sys.modules:
        return sys.modules[module_name]

    valid_mod_bundle = (
        sys.modules[mod_bundle].__jac_mod_bundle__
        if isinstance(mod_bundle, str)
        and mod_bundle in sys.modules
        and "__jac_mod_bundle__" in sys.modules[mod_bundle].__dict__
        else None
    )

    caller_dir = get_caller_dir(target, base_path, dir_path)
    full_target = path.normpath(path.join(caller_dir, file_name))

    if lng == "py":
        module = py_import(
            target=target, items=items, absorb=absorb, mdl_alias=mdl_alias
        )
    else:
        module_name = override_name if override_name else module_name
        module = create_jac_py_module(
            valid_mod_bundle, module_name, package_path, full_target
        )
        if valid_mod_bundle:
            codeobj = valid_mod_bundle.mod_deps[full_target].gen.py_bytecode
            codeobj = marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
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
                    # for e in result.errors_had:
                    #     print(e)
                    return None
                else:
                    codeobj = marshal.loads(result.ir.gen.py_bytecode)
        if not codeobj:
            raise ImportError(f"No bytecode found for {full_target}")
        with sys_path_context(caller_dir):
            exec(codeobj, module.__dict__)

    return module


def create_jac_py_module(
    mod_bundle: Optional[Module | str],
    module_name: str,
    package_path: str,
    full_target: str,
) -> types.ModuleType:
    """Create a module."""
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
    return module


def get_caller_dir(target: str, base_path: str, dir_path: str) -> str:
    """Get the directory of the caller."""
    caller_dir = base_path if path.isdir(base_path) else path.dirname(base_path)
    caller_dir = caller_dir if caller_dir else getcwd()
    chomp_target = target
    if chomp_target.startswith("."):
        chomp_target = chomp_target[1:]
        while chomp_target.startswith("."):
            caller_dir = path.dirname(caller_dir)
            chomp_target = chomp_target[1:]
    caller_dir = path.join(caller_dir, dir_path)
    return caller_dir


def py_import(
    target: str,
    items: Optional[dict[str, Union[str, bool]]] = None,
    absorb: bool = False,
    mdl_alias: Optional[str] = None,
) -> types.ModuleType:
    """Import a Python module."""
    try:
        target = target.lstrip(".") if target.startswith("..") else target
        imported_module = importlib.import_module(name=target)
        main_module = __import__("__main__")
        if absorb:
            for name in dir(imported_module):
                if not name.startswith("_"):
                    setattr(main_module, name, getattr(imported_module, name))

        elif items:
            for name, alias in items.items():
                try:
                    setattr(
                        main_module,
                        alias if isinstance(alias, str) else name,
                        getattr(imported_module, name),
                    )
                except AttributeError as e:
                    if hasattr(imported_module, "__path__"):
                        setattr(
                            main_module,
                            alias if isinstance(alias, str) else name,
                            importlib.import_module(f"{target}.{name}"),
                        )
                    else:
                        raise e

        else:
            setattr(
                __import__("__main__"),
                mdl_alias if isinstance(mdl_alias, str) else target,
                imported_module,
            )
        return imported_module
    except ImportError as e:
        print(f"Failed to import module {target}")
        raise e

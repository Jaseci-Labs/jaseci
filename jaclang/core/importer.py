"""Special Imports for Jac Code."""

import importlib
import marshal
import os
import sys
import types
from os import getcwd, path
from typing import Optional, Union

from jaclang.compiler.absyntree import Module
from jaclang.compiler.compile import compile_jac
from jaclang.compiler.constant import Constants as Con
from jaclang.core.utils import sys_path_context


def handle_directory(
    module_name: str, full_mod_path: str, mod_bundle: Module
) -> types.ModuleType:
    """Import from a directory that potentially contains multiple Jac modules."""
    module = types.ModuleType(module_name)
    module.__name__ = module_name
    module.__path__ = [full_mod_path]
    module.__dict__["__jac_mod_bundle__"] = mod_bundle
    if module not in sys.modules:
        sys.modules[module_name] = module
    return module


def process_items(
    module: types.ModuleType,
    items: dict[str, Union[str, Optional[str]]],
    caller_dir: str,
    lang: Optional[str],
    mod_bundle: Optional[Module] = None,
    cachable: bool = True,
) -> list:
    """Process items within a module by handling renaming and potentially loading missing attributes."""
    unique_loaded_items = []

    def handle_item_loading(item: str, alias: Union[str, Optional[str]]) -> None:
        if item:
            unique_loaded_items.append(item)
            setattr(module, name, item)
            if alias and alias != name and not isinstance(alias, bool):
                setattr(module, alias, item)

    for name, alias in items.items():
        try:
            item = getattr(module, name)
            handle_item_loading(item, alias)
        except AttributeError:
            if lang == "jac":
                jac_file_path = (
                    os.path.join(module.__path__[0], f"{name}.jac")
                    if hasattr(module, "__path__")
                    else module.__file__
                )

                if jac_file_path and os.path.isfile(jac_file_path):
                    item = load_jac_file(
                        module=module,
                        name=name,
                        jac_file_path=jac_file_path,
                        mod_bundle=mod_bundle,
                        cachable=cachable,
                        caller_dir=caller_dir,
                    )
                    handle_item_loading(item, alias)
            else:
                if hasattr(module, "__path__"):
                    full_module_name = f"{module.__name__}.{name}"
                    item = importlib.import_module(full_module_name)
                    handle_item_loading(item, alias)
    return unique_loaded_items


def load_jac_file(
    module: types.ModuleType,
    name: str,
    jac_file_path: str,
    mod_bundle: Optional[Module],
    cachable: bool,
    caller_dir: str,
) -> Optional[types.ModuleType]:
    """Load a single .jac file into the specified module component."""
    try:
        package_name = (
            f"{module.__name__}.{name}"
            if hasattr(module, "__path__")
            else module.__name__
        )
        new_module = sys.modules.get(
            package_name,
            create_jac_py_module(mod_bundle, name, module.__name__, jac_file_path),
        )

        codeobj = get_codeobj(
            full_target=jac_file_path,
            module_name=name,
            mod_bundle=mod_bundle,
            cachable=cachable,
            caller_dir=caller_dir,
        )
        if not codeobj:
            raise ImportError(f"No bytecode found for {jac_file_path}")

        exec(codeobj, new_module.__dict__)
        return getattr(new_module, name, new_module)
    except ImportError as e:
        print(
            f"Failed to load {name} from {jac_file_path} in {module.__name__}: {str(e)}"
        )
        return None


def get_codeobj(
    full_target: str,
    module_name: str,
    mod_bundle: Optional[Module],
    cachable: bool,
    caller_dir: str,
) -> Optional[types.CodeType]:
    """Execcutes the code for a given module."""
    if mod_bundle:
        codeobj = mod_bundle.mod_deps[full_target].gen.py_bytecode
        return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
    gen_dir = os.path.join(caller_dir, Con.JAC_GEN_DIR)
    pyc_file_path = os.path.join(gen_dir, module_name + ".jbc")
    if cachable and os.path.exists(pyc_file_path):
        with open(pyc_file_path, "rb") as f:
            return marshal.load(f)

    result = compile_jac(full_target, cache_result=cachable)
    if result.errors_had or not result.ir.gen.py_bytecode:
        for e in result.errors_had:
            print(e)
            return None
    if result.ir.gen.py_bytecode is not None:
        return marshal.loads(result.ir.gen.py_bytecode)
    else:
        return None


def jac_importer(
    target: str,
    base_path: str,
    absorb: bool = False,
    cachable: bool = True,
    mdl_alias: Optional[str] = None,
    override_name: Optional[str] = None,
    mod_bundle: Optional[Module | str] = None,
    lng: Optional[str] = "jac",
    items: Optional[dict[str, Union[str, Optional[str]]]] = None,
) -> tuple[types.ModuleType, ...]:
    """Core Import Process."""
    unique_loaded_items = []
    dir_path, file_name = path.split(path.join(*(target.split("."))))
    module_name = path.splitext(file_name)[0]
    package_path = dir_path.replace(path.sep, ".")
    if (
        not override_name
        and package_path
        and f"{package_path}.{module_name}" in sys.modules
    ):
        module = sys.modules[f"{package_path}.{module_name}"]
    elif not override_name and not package_path and module_name in sys.modules:
        module = sys.modules[module_name]
    else:
        module = None
    valid_mod_bundle = (
        sys.modules[mod_bundle].__jac_mod_bundle__
        if isinstance(mod_bundle, str)
        and mod_bundle in sys.modules
        and "__jac_mod_bundle__" in sys.modules[mod_bundle].__dict__
        else None
    )

    caller_dir = get_caller_dir(target, base_path, dir_path)
    full_target = path.normpath(path.join(caller_dir, file_name))
    if not module:
        if os.path.isdir(full_target):
            module = handle_directory(module_name, full_target, valid_mod_bundle)
        else:
            full_target += ".jac" if lng == "jac" else ".py"
            module_name = path.splitext(file_name)[0]
            package_path = dir_path.replace(path.sep, ".")

            if lng == "py":
                module, *unique_loaded_items = py_import(
                    target=target,
                    items=items,
                    absorb=absorb,
                    mdl_alias=mdl_alias,
                    caller_dir=caller_dir,
                )
            else:
                module_name = override_name if override_name else module_name
                module = create_jac_py_module(
                    valid_mod_bundle,
                    module_name,
                    package_path,
                    full_target,
                )
                codeobj = get_codeobj(
                    full_target,
                    module_name,
                    valid_mod_bundle,
                    cachable,
                    caller_dir=caller_dir,
                )
                try:
                    if not codeobj:
                        raise ImportError(f"No bytecode found for {full_target}")
                    with sys_path_context(caller_dir):
                        exec(codeobj, module.__dict__)
                except Exception as e:
                    raise ImportError(f"Error importing {full_target}: {str(e)}")
    unique_loaded_items = (
        process_items(
            module=module,
            items=items,
            caller_dir=caller_dir,
            mod_bundle=valid_mod_bundle,
            cachable=cachable,
            lang=lng,
        )
        if items
        else []
    )
    return (module,) if absorb or not items else tuple(unique_loaded_items)


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
    caller_dir: str,
    items: Optional[dict[str, Union[str, Optional[str]]]] = None,
    absorb: bool = False,
    mdl_alias: Optional[str] = None,
) -> tuple[types.ModuleType, ...]:
    """Import a Python module."""
    try:
        loaded_items: list = []
        if target.startswith("."):
            target = target.lstrip(".")
            full_target = path.normpath(path.join(caller_dir, target))
            spec = importlib.util.spec_from_file_location(target, full_target + ".py")
            if spec and spec.loader:
                imported_module = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = imported_module
                spec.loader.exec_module(imported_module)
            else:
                raise ImportError(f"Cannot find module {target} at {full_target}")
        else:
            imported_module = importlib.import_module(name=target)
        main_module = __import__("__main__")
        if absorb:
            for name in dir(imported_module):
                if not name.startswith("_"):
                    setattr(main_module, name, getattr(imported_module, name))

        elif items:
            for name, alias in items.items():
                if isinstance(alias, bool):
                    alias = name
                try:
                    item = getattr(imported_module, name)
                    if item not in loaded_items:
                        setattr(
                            main_module, alias if isinstance(alias, str) else name, item
                        )
                        loaded_items.append(item)
                except AttributeError as e:
                    if hasattr(imported_module, "__path__"):
                        item = importlib.import_module(f"{target}.{name}")
                        if item not in loaded_items:
                            setattr(
                                main_module,
                                alias if isinstance(alias, str) else name,
                                item,
                            )
                            loaded_items.append(item)
                    else:
                        raise e

        else:
            setattr(
                __import__("__main__"),
                mdl_alias if isinstance(mdl_alias, str) else target,
                imported_module,
            )
        return (imported_module, *loaded_items)

    except ImportError as e:
        raise e

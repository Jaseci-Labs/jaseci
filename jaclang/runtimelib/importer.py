"""Special Imports for Jac Code."""

from __future__ import annotations

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
from jaclang.runtimelib.machine import JacMachine
from jaclang.runtimelib.utils import sys_path_context
from jaclang.utils.log import logging

logger = logging.getLogger(__name__)


class ImportPathSpec:
    """Import Specification."""

    def __init__(
        self,
        target: str,
        base_path: str,
        absorb: bool,
        cachable: bool,
        mdl_alias: Optional[str],
        override_name: Optional[str],
        mod_bundle: Optional[Module | str],
        lng: Optional[str],
        items: Optional[dict[str, Union[str, Optional[str]]]],
    ) -> None:
        """Initialize the ImportPathSpec object."""
        self.target = target
        self.base_path = base_path
        self.absorb = absorb
        self.cachable = cachable
        self.mdl_alias = mdl_alias
        self.override_name = override_name
        self.mod_bundle = mod_bundle
        self.language = lng
        self.items = items
        self.dir_path, self.file_name = path.split(path.join(*(target.split("."))))
        self.module_name = path.splitext(self.file_name)[0]
        self.package_path = self.dir_path.replace(path.sep, ".")
        self.caller_dir = self.get_caller_dir()
        self.full_target = path.abspath(path.join(self.caller_dir, self.file_name))

    def get_caller_dir(self) -> str:
        """Get the directory of the caller."""
        caller_dir = (
            self.base_path
            if path.isdir(self.base_path)
            else path.dirname(self.base_path)
        )
        caller_dir = caller_dir if caller_dir else getcwd()
        chomp_target = self.target
        if chomp_target.startswith("."):
            chomp_target = chomp_target[1:]
            while chomp_target.startswith("."):
                caller_dir = path.dirname(caller_dir)
                chomp_target = chomp_target[1:]
        return path.join(caller_dir, self.dir_path)


class ImportReturn:
    """Import Return Object."""

    def __init__(
        self,
        ret_mod: types.ModuleType,
        ret_items: list[types.ModuleType],
        importer: Importer,
    ) -> None:
        """Initialize the ImportReturn object."""
        self.ret_mod = ret_mod
        self.ret_items = ret_items
        self.importer = importer

    def process_items(
        self,
        module: types.ModuleType,
        items: dict[str, Union[str, Optional[str]]],
        caller_dir: str,
        lang: Optional[str],
        mod_bundle: Optional[Module] = None,
        cachable: bool = True,
    ) -> None:
        """Process items within a module by handling renaming and potentially loading missing attributes."""

        def handle_item_loading(
            item: types.ModuleType, alias: Union[str, Optional[str]]
        ) -> None:
            if item:
                self.ret_items.append(item)
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
                        item = self.load_jac_file(
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

    def load_jac_file(
        self,
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
            if isinstance(self.importer, JacImporter):
                new_module = sys.modules.get(
                    package_name,
                    self.importer.create_jac_py_module(
                        mod_bundle, name, module.__name__, jac_file_path
                    ),
                )
            codeobj = self.importer.get_codeobj(
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
            logger.error(
                f"Failed to load {name} from {jac_file_path} in {module.__name__}: {str(e)}"
            )
            return None


class Importer:
    """Abstract base class for all importers."""

    def __init__(self, jac_machine: JacMachine) -> None:
        """Initialize the Importer object."""
        self.jac_machine = jac_machine
        self.result: Optional[ImportReturn] = None

    def run_import(self, spec: ImportPathSpec) -> ImportReturn:
        """Run the import process."""
        raise NotImplementedError

    def update_sys(self, module: types.ModuleType, spec: ImportPathSpec) -> None:
        """Update sys.modules with the newly imported module."""
        if spec.module_name not in sys.modules:
            sys.modules[spec.module_name] = module

    def get_codeobj(
        self,
        full_target: str,
        module_name: str,
        mod_bundle: Optional[Module],
        cachable: bool,
        caller_dir: str,
    ) -> Optional[types.CodeType]:
        """Get the code object for a given module."""
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
            logger.error(
                f"While importing {len(result.errors_had)} errors"
                f" found in {full_target}"
            )
            return None
        if result.ir.gen.py_bytecode is not None:
            return marshal.loads(result.ir.gen.py_bytecode)
        else:
            return None


class PythonImporter(Importer):
    """Importer for Python modules."""

    def __init__(self, jac_machine: JacMachine) -> None:
        """Initialize the PythonImporter object."""
        self.jac_machine = jac_machine

    def run_import(self, spec: ImportPathSpec) -> ImportReturn:
        """Run the import process for Python modules."""
        try:
            loaded_items: list = []
            if spec.target.startswith("."):
                spec.target = spec.target.lstrip(".")
                full_target = path.normpath(path.join(spec.caller_dir, spec.target))
                imp_spec = importlib.util.spec_from_file_location(
                    spec.target, full_target + ".py"
                )
                if imp_spec and imp_spec.loader:
                    imported_module = importlib.util.module_from_spec(imp_spec)
                    sys.modules[imp_spec.name] = imported_module
                    imp_spec.loader.exec_module(imported_module)
                else:
                    raise ImportError(
                        f"Cannot find module {spec.target} at {full_target}"
                    )
            else:
                imported_module = importlib.import_module(name=spec.target)

            main_module = __import__("__main__")
            if spec.absorb:
                for name in dir(imported_module):
                    if not name.startswith("_"):
                        setattr(main_module, name, getattr(imported_module, name))

            elif spec.items:
                for name, alias in spec.items.items():
                    if isinstance(alias, bool):
                        alias = name
                    try:
                        item = getattr(imported_module, name)
                        if item not in loaded_items:
                            setattr(
                                main_module,
                                alias if isinstance(alias, str) else name,
                                item,
                            )
                            loaded_items.append(item)
                    except AttributeError as e:
                        if hasattr(imported_module, "__path__"):
                            item = importlib.import_module(f"{spec.target}.{name}")
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
                    spec.mdl_alias if isinstance(spec.mdl_alias, str) else spec.target,
                    imported_module,
                )
            self.result = ImportReturn(imported_module, loaded_items, self)
            return self.result

        except ImportError as e:
            raise e


class JacImporter(Importer):
    """Importer for Jac modules."""

    def __init__(self, jac_machine: JacMachine) -> None:
        """Initialize the JacImporter object."""
        self.jac_machine = jac_machine

    def get_sys_mod_name(self, full_target: str) -> str:
        """Generate the system module name based on full target path and package path."""
        if full_target == self.jac_machine.base_path_dir:
            return path.basename(self.jac_machine.base_path_dir)
        relative_path = path.relpath(full_target, start=self.jac_machine.base_path_dir)
        base_name = path.splitext(relative_path)[0]
        sys_mod_name = base_name.replace(os.sep, ".").strip(".")
        return sys_mod_name

    def handle_directory(
        self, module_name: str, full_mod_path: str, mod_bundle: Optional[Module | str]
    ) -> types.ModuleType:
        """Import from a directory that potentially contains multiple Jac modules."""
        module_name = self.get_sys_mod_name(full_mod_path)
        module = types.ModuleType(module_name)
        module.__name__ = module_name
        module.__path__ = [full_mod_path]
        module.__file__ = None
        module.__dict__["__jac_mod_bundle__"] = mod_bundle

        if module_name not in sys.modules:
            sys.modules[module_name] = module
        return module

    def create_jac_py_module(
        self,
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
        sys.modules[module_name] = module
        if package_path:
            base_path = full_target.split(package_path.replace(".", path.sep))[0]
            parts = package_path.split(".")
            for i in range(len(parts)):
                package_name = ".".join(parts[: i + 1])
                if package_name not in sys.modules:
                    full_mod_path = path.join(
                        base_path, package_name.replace(".", path.sep)
                    )
                    self.handle_directory(
                        module_name=package_name,
                        full_mod_path=full_mod_path,
                        mod_bundle=mod_bundle,
                    )
            setattr(sys.modules[package_path], module_name, module)
            sys.modules[f"{package_path}.{module_name}"] = module

        return module

    def run_import(self, spec: ImportPathSpec) -> ImportReturn:
        """Run the import process for Jac modules."""
        unique_loaded_items: list[types.ModuleType] = []
        module = None
        valid_mod_bundle = (
            sys.modules[spec.mod_bundle].__jac_mod_bundle__
            if isinstance(spec.mod_bundle, str)
            and spec.mod_bundle in sys.modules
            and "__jac_mod_bundle__" in sys.modules[spec.mod_bundle].__dict__
            else None
        )

        if not module:
            if os.path.isdir(spec.full_target):
                module = self.handle_directory(
                    spec.module_name, spec.full_target, valid_mod_bundle
                )
            else:
                spec.full_target += ".jac" if spec.language == "jac" else ".py"
                module_name = self.get_sys_mod_name(spec.full_target)
                module_name = (
                    spec.override_name if spec.override_name else spec.module_name
                )
                module = self.create_jac_py_module(
                    valid_mod_bundle,
                    module_name,
                    spec.package_path,
                    spec.full_target,
                )
                codeobj = self.get_codeobj(
                    spec.full_target,
                    module_name,
                    valid_mod_bundle,
                    spec.cachable,
                    caller_dir=spec.caller_dir,
                )
                try:
                    if not codeobj:
                        raise ImportError(f"No bytecode found for {spec.full_target}")
                    with sys_path_context(spec.caller_dir):
                        exec(codeobj, module.__dict__)
                except Exception as e:
                    raise ImportError(f"Error importing {spec.full_target}: {str(e)}")

        import_return = ImportReturn(module, unique_loaded_items, self)
        if spec.items:
            import_return.process_items(
                module=module,
                items=spec.items,
                caller_dir=spec.caller_dir,
                mod_bundle=valid_mod_bundle,
                cachable=spec.cachable,
                lang=spec.language,
            )
        self.result = import_return
        return self.result

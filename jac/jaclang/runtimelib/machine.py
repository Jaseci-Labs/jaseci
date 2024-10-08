"""Jac Machine module."""

import inspect
import marshal
import os
import sys
import tempfile
import types
from contextvars import ContextVar
from typing import Optional, Union

from jaclang.compiler.absyntree import Module
from jaclang.compiler.compile import compile_jac
from jaclang.compiler.constant import Constants as Con
from jaclang.runtimelib.architype import (
    Architype,
    EdgeArchitype,
    NodeArchitype,
    WalkerArchitype,
)
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


JACMACHINE_CONTEXT = ContextVar["JacMachine | None"]("JacMachine")


class JacMachine:
    """JacMachine to handle the VM-related functionalities and loaded programs."""

    def __init__(self, base_path: str = "") -> None:
        """Initialize the JacMachine object."""
        self.loaded_modules: dict[str, types.ModuleType] = {}
        if not base_path:
            base_path = os.getcwd()
        self.base_path = base_path
        self.base_path_dir = (
            os.path.dirname(base_path)
            if not os.path.isdir(base_path)
            else os.path.abspath(base_path)
        )
        self.jac_program: Optional[JacProgram] = None

        JACMACHINE_CONTEXT.set(self)

    def attach_program(self, jac_program: "JacProgram") -> None:
        """Attach a JacProgram to the machine."""
        self.jac_program = jac_program

    def get_mod_bundle(self) -> Optional[Module]:
        """Retrieve the mod_bundle from the attached JacProgram."""
        if self.jac_program:
            return self.jac_program.mod_bundle
        return None

    def get_bytecode(
        self,
        module_name: str,
        full_target: str,
        caller_dir: str,
        cachable: bool = True,
        reload: bool = False,
    ) -> Optional[types.CodeType]:
        """Retrieve bytecode from the attached JacProgram."""
        if self.jac_program:
            return self.jac_program.get_bytecode(
                module_name, full_target, caller_dir, cachable, reload=reload
            )
        return None

    def load_module(self, module_name: str, module: types.ModuleType) -> None:
        """Load a module into the machine."""
        self.loaded_modules[module_name] = module
        sys.modules[module_name] = module

    def list_modules(self) -> list[str]:
        """List all loaded modules."""
        return list(self.loaded_modules.keys())

    def list_walkers(self, module_name: str) -> list[str]:
        """List all walkers in a specific module."""
        module = self.loaded_modules.get(module_name)
        if module:
            walkers = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, WalkerArchitype):
                    walkers.append(name)
            return walkers
        return []

    def list_nodes(self, module_name: str) -> list[str]:
        """List all nodes in a specific module."""
        module = self.loaded_modules.get(module_name)
        if module:
            nodes = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, NodeArchitype):
                    nodes.append(name)
            return nodes
        return []

    def list_edges(self, module_name: str) -> list[str]:
        """List all edges in a specific module."""
        module = self.loaded_modules.get(module_name)
        if module:
            nodes = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, EdgeArchitype):
                    nodes.append(name)
            return nodes
        return []

    def create_architype_from_source(
        self,
        source_code: str,
        module_name: Optional[str] = None,
        base_path: Optional[str] = None,
        cachable: bool = False,
        keep_temporary_files: bool = False,
    ) -> Optional[types.ModuleType]:
        """Dynamically creates architypes (nodes, walkers, etc.) from Jac source code."""
        from jaclang.runtimelib.importer import JacImporter, ImportPathSpec

        if not base_path:
            base_path = self.base_path or os.getcwd()

        if base_path and not os.path.exists(base_path):
            os.makedirs(base_path)
        if not module_name:
            module_name = f"_dynamic_module_{len(self.loaded_modules)}"
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".jac",
            prefix=module_name + "_",
            dir=base_path,
            delete=False,
        ) as tmp_file:
            tmp_file_path = tmp_file.name
            tmp_file.write(source_code)

        try:
            importer = JacImporter(self)
            tmp_file_basename = os.path.basename(tmp_file_path)
            tmp_module_name, _ = os.path.splitext(tmp_file_basename)

            spec = ImportPathSpec(
                target=tmp_module_name,
                base_path=base_path,
                absorb=False,
                cachable=cachable,
                mdl_alias=None,
                override_name=module_name,
                lng="jac",
                items=None,
            )

            import_result = importer.run_import(spec, reload=False)
            module = import_result.ret_mod

            self.loaded_modules[module_name] = module
            return module
        except Exception as e:
            logger.error(f"Error importing dynamic module '{module_name}': {e}")
            return None
        finally:
            if not keep_temporary_files and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def update_walker(
        self, module_name: str, items: Optional[dict[str, Union[str, Optional[str]]]]
    ) -> tuple[types.ModuleType, ...]:
        """Reimport the module."""
        from .importer import JacImporter, ImportPathSpec

        if module_name in self.loaded_modules:
            try:
                old_module = self.loaded_modules[module_name]
                importer = JacImporter(self)
                spec = ImportPathSpec(
                    target=module_name,
                    base_path=self.base_path,
                    absorb=False,
                    cachable=True,
                    mdl_alias=None,
                    override_name=None,
                    lng="jac",
                    items=items,
                )
                import_result = importer.run_import(spec, reload=True)
                ret_items = []
                if items:
                    for item_name in items:
                        if hasattr(old_module, item_name):
                            new_attr = getattr(import_result.ret_mod, item_name, None)
                            if new_attr:
                                ret_items.append(new_attr)
                                setattr(
                                    old_module,
                                    item_name,
                                    new_attr,
                                )
                return (old_module,) if not items else tuple(ret_items)
            except Exception as e:
                logger.error(f"Failed to update module {module_name}: {e}")
        else:
            logger.warning(f"Module {module_name} not found in loaded modules.")
        return ()

    def spawn_node(
        self,
        node_name: str,
        attributes: Optional[dict] = None,
        module_name: str = "__main__",
    ) -> NodeArchitype:
        """Spawn a node instance of the given node_name with attributes."""
        node_class = self.get_architype(module_name, node_name)
        if isinstance(node_class, type) and issubclass(node_class, NodeArchitype):
            if attributes is None:
                attributes = {}
            node_instance = node_class(**attributes)
            return node_instance
        else:
            raise ValueError(f"Node {node_name} not found.")

    def spawn_walker(
        self,
        walker_name: str,
        attributes: Optional[dict] = None,
        module_name: str = "__main__",
    ) -> WalkerArchitype:
        """Spawn a walker instance of the given walker_name."""
        walker_class = self.get_architype(module_name, walker_name)
        if isinstance(walker_class, type) and issubclass(walker_class, WalkerArchitype):
            if attributes is None:
                attributes = {}
            walker_instance = walker_class(**attributes)
            return walker_instance
        else:
            raise ValueError(f"Walker {walker_name} not found.")

    def get_architype(
        self, module_name: str, architype_name: str
    ) -> Optional[Architype]:
        """Retrieve an architype class from a module."""
        module = self.loaded_modules.get(module_name)
        if module:
            return getattr(module, architype_name, None)
        return None

    @staticmethod
    def get(base_path: str = "") -> "JacMachine":
        """Get current jac machine."""
        if (jac_machine := JACMACHINE_CONTEXT.get(None)) is None:
            jac_machine = JacMachine(base_path)
        return jac_machine

    @staticmethod
    def detach() -> None:
        """Detach current jac machine."""
        JACMACHINE_CONTEXT.set(None)


class JacProgram:
    """Class to hold the mod_bundle and bytecode for Jac modules."""

    def __init__(
        self, mod_bundle: Optional[Module], bytecode: Optional[dict[str, bytes]]
    ) -> None:
        """Initialize the JacProgram object."""
        self.mod_bundle = mod_bundle
        self.bytecode = bytecode or {}

    def get_bytecode(
        self,
        module_name: str,
        full_target: str,
        caller_dir: str,
        cachable: bool = True,
        reload: bool = False,
    ) -> Optional[types.CodeType]:
        """Get the bytecode for a specific module."""
        if self.mod_bundle and isinstance(self.mod_bundle, Module):
            codeobj = self.mod_bundle.mod_deps[full_target].gen.py_bytecode
            return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
        gen_dir = os.path.join(caller_dir, Con.JAC_GEN_DIR)
        pyc_file_path = os.path.join(gen_dir, module_name + ".jbc")
        if cachable and os.path.exists(pyc_file_path) and not reload:
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

"""Module Import Resolution Pass for the Jac compiler.

This pass handles the static resolution and loading of imported modules by:

1. Identifying import statements in the source code
2. Resolving module paths (both relative and absolute)
3. Loading and parsing the imported modules
4. Handling both Jac and Python imports with appropriate strategies
5. Managing import dependencies and preventing circular imports
6. Supporting various import styles:
   - Direct imports (import x)
   - From imports (from x import y)
   - Star imports (from x import *)
   - Aliased imports (import x as y)

The pass runs early in the compilation pipeline to ensure all symbols from imported
modules are available for subsequent passes like symbol table building and type checking.
"""

import ast as py_ast
import os
from typing import Optional


import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import Transform, UniPass
from jaclang.compiler.passes.main import SymTabBuildPass
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


# TODO: This pass finds imports dependencies, parses them, and adds them to
# JacProgram's table, then table calls again if needed, should rename
class JacImportDepsPass(Transform[uni.Module, uni.Module]):
    """Jac statically imports Jac modules."""

    def pre_transform(self) -> None:
        """Initialize the JacImportPass."""
        super().pre_transform()
        self.last_imported: list[uni.Module] = []

    def transform(self, ir_in: uni.Module) -> uni.Module:
        """Run Importer."""
        # Add the current module to last_imported to start the import process
        self.last_imported.append(ir_in)

        # Process imports until no more imported modules to process
        while self.last_imported:
            current_module = self.last_imported.pop(0)
            all_imports = UniPass.get_all_sub_nodes(current_module, uni.ModulePath)
            for i in all_imports:
                self.process_import(i)

        return ir_in

    def process_import(self, i: uni.ModulePath) -> None:
        """Process an import."""
        imp_node = i.parent_of_type(uni.Import)
        if imp_node.is_jac:
            self.import_jac_module(node=i)

    def import_jac_module(self, node: uni.ModulePath) -> None:
        """Import a module."""
        from jaclang.compiler.passes.main import CompilerMode as CMode

        target = node.resolve_relative_path()
        # If the module is a package (dir)
        if os.path.isdir(target):
            self.load_mod(self.import_jac_mod_from_dir(target))
            import_node = node.parent_of_type(uni.Import)
            # And the import is a from import and I am the from module
            if node == import_node.from_loc:
                # Import all from items as modules or packages
                for i in import_node.items.items:
                    if isinstance(i, uni.ModuleItem):
                        from_mod_target = node.resolve_relative_path(i.name.value)
                        # If package
                        if os.path.isdir(from_mod_target):
                            self.load_mod(self.import_jac_mod_from_dir(from_mod_target))
                        # Else module
                        else:
                            if from_mod_target in self.prog.mod.hub:
                                return
                            self.load_mod(
                                self.prog.compile(
                                    file_path=from_mod_target, mode=CMode.PARSE
                                )
                            )
        else:
            if target in self.prog.mod.hub:
                return
            self.load_mod(self.prog.compile(file_path=target, mode=CMode.PARSE))

    def load_mod(self, mod: uni.Module) -> None:
        """Attach a module to a node."""
        self.prog.mod.hub[mod.loc.mod_path] = mod
        self.last_imported.append(mod)

    # TODO: Refactor this to a function for impl and function for test

    def import_jac_mod_from_dir(self, target: str) -> uni.Module:
        """Import a module from a directory."""
        from jaclang.compiler.passes.main import CompilerMode as CMode

        jac_init_path = os.path.join(target, "__init__.jac")
        if os.path.exists(jac_init_path):
            if jac_init_path in self.prog.mod.hub:
                return self.prog.mod.hub[jac_init_path]
            return self.prog.compile(file_path=jac_init_path, mode=CMode.PARSE)
        elif os.path.exists(py_init_path := os.path.join(target, "__init__.py")):
            with open(py_init_path, "r") as f:
                file_source = f.read()
                mod = uni.Module.make_stub(
                    inject_name=target.split(os.path.sep)[-1],
                    inject_src=uni.Source(file_source, py_init_path),
                )
                self.prog.mod.hub[py_init_path] = mod
                return mod
        else:
            return uni.Module.make_stub(
                inject_name=target.split(os.path.sep)[-1],
                inject_src=uni.Source("", target),
            )


class PyImportDepsPass(JacImportDepsPass):
    """Jac statically imports Python modules."""

    def pre_transform(self) -> None:
        """Initialize the PyImportPass."""
        self.import_from_build_list: list[tuple[uni.Import, uni.Module]] = []

    def transform(self, ir_in: uni.Module) -> uni.Module:
        """Run Importer."""
        self.__load_builtins()
        self.import_from_build_list = []

        # Add all modules from the program hub to last_imported to process their imports
        self.last_imported = list(self.prog.mod.hub.values())

        # Process imports until no more imported modules to process
        while self.last_imported:
            current_module = self.last_imported.pop(0)
            all_imports = UniPass.get_all_sub_nodes(current_module, uni.ModulePath)
            for i in all_imports:
                self.process_import(i)

        return ir_in

    def process_import(self, i: uni.ModulePath) -> None:
        """Process an import."""
        # Process import is orginally implemented to handle ModulePath in Jaclang
        # This won't work with py imports as this will fail to import stuff in form of
        #      from a import b
        #      from a import (c, d, e)
        # Solution to that is to get the import node and check the from loc `then`
        # handle it based on if there a from loc or not
        imp_node = i.parent_of_type(uni.Import)

        if imp_node.is_py:
            if imp_node.from_loc:
                msg = "Processing import from node at href="
                msg += uni.Module.get_href_path(imp_node)
                msg += f' path="{imp_node.loc.mod_path}, {imp_node.loc}"'
                self.__process_import_from(imp_node)
            else:
                msg = "Processing import node at href="
                msg += uni.Module.get_href_path(imp_node)
                msg += f' path="{imp_node.loc.mod_path}, {imp_node.loc}"'
                self.__process_import(imp_node)

    def __process_import_from(self, imp_node: uni.Import) -> None:
        """Process imports in the form of `from X import I`."""
        assert isinstance(imp_node.from_loc, uni.ModulePath)

        # Attempt to import the Python module X and process it
        imported_mod = self.__import_py_module(
            parent_node_path=uni.Module.get_href_path(imp_node),
            mod_path=imp_node.from_loc.dot_path_str,
        )

        if imported_mod:
            # Cyclic imports will happen in case of import sys
            # sys stub file imports sys module which means that we need
            # to import sys stub file again in the sys stub file and so on
            # This can be detected by iterating over all the parents and make sure
            # that the parent is in another file than the imported module
            if self.__check_cyclic_imports(imp_node, imported_mod):
                return

            if imported_mod.name == "builtins":
                return

            msg = f"\tRegistering module:{imported_mod.name} to "
            msg += f"import_from handling with {imp_node.loc.mod_path}:{imp_node.loc}"

            self.load_mod(imported_mod)
            self.import_from_build_list.append((imp_node, imported_mod))
            SymTabBuildPass(ir_in=imported_mod, prog=self.prog)

    def __process_import(self, imp_node: uni.Import) -> None:
        """Process the imports in form of `import X`."""
        # Expected that each ImportStatement will import one item
        # In case of this assertion fired then we need to revisit this item
        assert len(imp_node.items.items) == 1
        imported_item = imp_node.items.items[0]
        assert isinstance(imported_item, uni.ModulePath)

        imported_mod = self.__import_py_module(
            parent_node_path=uni.Module.get_href_path(imported_item),
            mod_path=imported_item.dot_path_str,
            imported_mod_name=(
                # TODO: Check this replace
                imported_item.dot_path_str.replace(".", "")
                if not imported_item.alias
                else imported_item.alias.sym_name
            ),
        )
        if imported_mod:
            if (
                self.__check_cyclic_imports(imp_node, imported_mod)
                or imported_mod.name == "builtins"
            ):
                return
            self.load_mod(imported_mod)

            if imp_node.is_absorb:
                msg = f"\tRegistering module:{imported_mod.name} to "
                msg += f"import_from (import all) handling with {imp_node.loc.mod_path}:{imp_node.loc}"

                self.import_from_build_list.append((imp_node, imported_mod))
            SymTabBuildPass(ir_in=imported_mod, prog=self.prog)

    def __import_py_module(
        self,
        parent_node_path: str,
        mod_path: str,
        imported_mod_name: Optional[str] = None,
    ) -> Optional[uni.Module]:
        """Import a python module."""
        from jaclang.compiler.passes.main import PyastBuildPass

        python_raise_map = self.prog.py_raise_map
        file_to_raise: Optional[str] = None

        if mod_path in python_raise_map:
            file_to_raise = python_raise_map[mod_path]
        else:
            # TODO: Is it fine to use imported_mod_name or get it from mod_path?
            resolved_mod_path = f"{parent_node_path}.{mod_path}"
            resolved_mod_path = resolved_mod_path.replace("..", ".")
            resolved_mod_path = resolved_mod_path.replace(
                f"{list(self.prog.mod.hub.values())[0]}.", ""
            )
            file_to_raise = python_raise_map.get(resolved_mod_path)

        if file_to_raise is None:
            return None

        try:
            if file_to_raise in {None, "built-in", "frozen"}:
                return None

            with open(file_to_raise, "r", encoding="utf-8") as f:
                file_source = f.read()
                mod = PyastBuildPass(
                    ir_in=uni.PythonModuleAst(
                        py_ast.parse(file_source),
                        orig_src=uni.Source(file_source, file_to_raise),
                    ),
                    prog=self.prog,
                ).ir_out

            if mod:
                mod.name = imported_mod_name if imported_mod_name else mod.name
                if mod.name == "__init__":
                    # (thakee): This needs to be re-done after implementing path handling properly.
                    mod_name = mod.loc.mod_path.split(os.path.sep)[-2]
                    mod.name = mod_name
                    mod.scope_name = mod_name
                mod.is_raised_from_py = True
                return mod
            else:
                raise self.ice(f"\tFailed to import python module {mod_path}")

        except Exception as e:
            self.log_error(f"\tFailed to import python module {mod_path}")
            raise e

    def __load_builtins(self) -> None:
        """Load Python builtins using introspection."""
        import builtins
        import inspect
        from jaclang.compiler.passes.main import PyastBuildPass

        # Python constants that cannot be assigned to
        constants = {"True", "False", "None", "NotImplemented", "Ellipsis", "..."}

        # Create a synthetic source with all builtins
        builtin_items = []
        for name in dir(builtins):
            if name in constants:
                # Skip constants as they're built into Python
                continue

            if not name.startswith("_") or name in ("__import__", "__build_class__"):
                obj = getattr(builtins, name)
                # Generate appropriate stub definitions based on obj type
                if inspect.isclass(obj):
                    builtin_items.append(f"class {name}: ...")
                elif inspect.isfunction(obj) or inspect.isbuiltin(obj):
                    # Try to get signature safely, use generic signature if it fails
                    try:
                        sig = inspect.signature(obj) if callable(obj) else "()"
                        builtin_items.append(f"def {name}{sig}: ...")
                    except (ValueError, TypeError):
                        builtin_items.append(f"def {name}(*args, **kwargs): ...")
                else:
                    # For variables that are not constants
                    builtin_items.append(f"{name} = None")

        file_source = "\n".join(builtin_items)
        mod = PyastBuildPass(
            ir_in=uni.PythonModuleAst(
                py_ast.parse(file_source),
                orig_src=uni.Source(file_source, "builtins"),
            ),
            prog=self.prog,
        ).ir_out
        SymTabBuildPass(ir_in=mod, prog=self.prog)
        self.prog.mod.hub["builtins"] = mod
        mod.is_raised_from_py = True

    def annex_impl(self, node: uni.Module) -> None:
        """Annex impl and test modules."""
        return None

    def __handle_different_site_packages(self, mod_path: str) -> str:
        if "site-packages" in mod_path:
            mod_path = mod_path[mod_path.index("site-packages") :]
        return mod_path

    def __check_cyclic_imports(
        self, imp_node: uni.UniNode, imported_module: uni.Module
    ) -> bool:
        """Check cyclic imports that might happen."""
        # Example of cyclic imports is import os
        # In the os stub file it imports the real os module which will cause os
        # stub to be raised again and so on
        # Another example is numpy. numpy init file imports multidim array file
        # which imports again more items from numpy and so on.
        imp_node_file = self.__handle_different_site_packages(imp_node.loc.mod_path)
        imported_module_file = self.__handle_different_site_packages(
            imported_module.loc.mod_path
        )
        if imp_node_file == imported_module_file:
            return True

        parent: Optional[uni.UniNode] = imp_node.parent
        while parent is not None:
            parent_file = self.__handle_different_site_packages(parent.loc.mod_path)
            if parent_file == imported_module_file:
                return True
            else:
                parent = parent.find_parent_of_type(uni.Module)

        return False

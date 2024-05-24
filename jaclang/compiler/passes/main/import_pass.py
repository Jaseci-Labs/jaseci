"""Static Import Pass.

This pass statically imports all modules used in import statements in the
current module. This pass is run before the def/decl pass to ensure that all
symbols are available for matching.
"""

import ast as py_ast
import importlib.util
import sys
from os import path
from typing import Optional


import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main import SubNodeTabPass
from jaclang.settings import settings
from jaclang.utils.helpers import import_target_to_relative_path


class JacImportPass(Pass):
    """Jac statically imports Jac modules."""

    x = 0

    def before_pass(self) -> None:
        """Run once before pass."""
        self.import_table: dict[str, ast.Module] = {}

    def enter_module(self, node: ast.Module) -> None:
        """Run Importer."""
        self.cur_node = node
        self.import_table[node.loc.mod_path] = node
        self.annex_impl(node)
        self.terminate()  # Turns off auto traversal for deliberate traversal
        self.run_again = True
        new_modpaths = self.get_all_sub_nodes(node, ast.ModulePath)
        breakk = None
        while self.run_again:
            self.x += 1
            self.run_again = False
            # print('\n\nwhiel loop starts over !! over !!!')  #uncomment me
            # all_imports = self.get_all_sub_nodes(node, ast.ModulePath)
            # print(all_imports)
            # all_imports = list(set(all_imports))
            # print(f"beofre for loop --)))) all_imports: {[i.path_str for i in all_imports]}")
            # for i in all_imports:
            new_modpaths_dummy = []
            for i in new_modpaths:
                # print(1)
                # print(self.x, '.',all_imports.index(i))
                # print(f"Importing  {i.path_str}")
                modds = self.process_import(node, i)
                if modds:
                    for md in modds:
                        # if md.path_str == 'types':
                        #     print('mayiruuu i am daa')
                        #     breakk=8989
                        #     break
                        if md.path_str in ["re", "math", "_decimal", "binascii"]:
                            continue
                        try:

                            spec = importlib.util.find_spec(md.path_str)
                        except:
                            continue
                        if (
                            spec
                            and spec.origin
                            and spec.origin not in {None, "built-in", "frozen"}
                        ):
                            if spec.origin in self.import_table:
                                md.sub_module = self.import_table[spec.origin]
                                continue
                        # print(self.import_table)
                        # print(f"Importing  {md.path_str}")
                        # print(f"Importing  {md}")
                    # if breakk:
                    #     self.run_again = False
                    new_modpaths_dummy.extend(modds)
                # self.process_import(node, i)
                self.enter_module_path(i)
            new_modpaths = new_modpaths_dummy
            # if breakk:
            #     self.run_again = False
            # break
            # SubNodeTabPass(prior=self, input_ir=node)
        self.annex_impl(node)
        node.mod_deps = self.import_table

    def process_import(self, node: ast.Module, i: ast.ModulePath) -> None:
        """Process an import."""
        lang = i.parent_of_type(ast.Import).hint.tag.value
        if lang == "jac" and not i.sub_module:
            mod = self.import_module(
                node=i,
                mod_path=node.loc.mod_path,
            )
            if mod:
                self.run_again = True
                self.annex_impl(mod)
                i.sub_module = mod
                i.add_kids_right([mod], pos_update=False)

    def annex_impl(self, node: ast.Module) -> None:
        """Annex impl and test modules."""
        if not node.loc.mod_path:
            self.error("Module has no path")
        if node.loc.mod_path.endswith(".jac") and path.exists(
            f"{node.loc.mod_path[:-4]}.impl.jac"
        ):
            mod = self.import_mod_from_file(f"{node.loc.mod_path[:-4]}.impl.jac")
            if mod:
                node.impl_mod = mod
                node.add_kids_left([mod], pos_update=False)
                mod.parent = node
        if node.loc.mod_path.endswith(".jac") and path.exists(
            f"{node.loc.mod_path[:-4]}.test.jac"
        ):
            mod = self.import_mod_from_file(f"{node.loc.mod_path[:-4]}.test.jac")
            if mod:
                node.test_mod = mod
                node.add_kids_right([mod], pos_update=False)
                mod.parent = node

    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: Sequence[Token],
        alias: Optional[Name],
        sub_module: Optional[Module] = None,
        """
        if node.alias and node.sub_module:
            node.sub_module.name = node.alias.value
        # Items matched during def/decl pass

    # Utility functions
    # -----------------

    def import_module(self, node: ast.ModulePath, mod_path: str) -> ast.Module | None:
        """Import a module."""
        self.cur_node = node  # impacts error reporting
        target = import_target_to_relative_path(
            node.level, node.path_str, path.dirname(node.loc.mod_path)
        )
        return self.import_mod_from_file(target)

    def import_mod_from_file(self, target: str) -> ast.Module | None:
        """Import a module from a file."""
        from jaclang.compiler.compile import jac_file_to_pass
        from jaclang.compiler.passes.main import SubNodeTabPass

        if not path.exists(target):
            self.error(f"Could not find module {target}")
            return None
        if target in self.import_table:
            return self.import_table[target]
        try:
            mod_pass = jac_file_to_pass(file_path=target, target=SubNodeTabPass)
            self.errors_had += mod_pass.errors_had
            self.warnings_had += mod_pass.warnings_had
            mod = mod_pass.ir
        except Exception as e:
            print(e)
            mod = None
        if isinstance(mod, ast.Module):
            self.import_table[target] = mod
            mod.is_imported = True
            mod.body = [x for x in mod.body if not isinstance(x, ast.AstImplOnlyNode)]
            return mod
        else:
            self.error(f"Module {target} is not a valid Jac module.")
            return None

    def import_py_module(
        self, node: ast.ModulePath, mod_path: str
    ) -> Optional[ast.Module]:
        """Import a module."""
        from jaclang.compiler.passes.main import PyastBuildPass

        base_dir = path.dirname(mod_path)
        sys.path.append(base_dir)
        # print('mod_path:---> ',node.alias)
        # print(node.alias)
        try:
            # Dynamically import the module
            spec = importlib.util.find_spec(node.path_str)
            sys.path.remove(base_dir)
            if spec and spec.origin and spec.origin not in {None, "built-in", "frozen"}:
                if spec.origin in self.import_table:
                    return self.import_table[spec.origin]
                with open(spec.origin, "r", encoding="utf-8") as f:
                    # print(f"\nImporting python module {node.path_str}")
                    # print('\nia m here  ))))---',node.path_str)  #uncomment me
                    mod = PyastBuildPass(
                        input_ir=ast.PythonModuleAst(
                            py_ast.parse(f.read()), mod_path=spec.origin
                        ),
                    ).ir
                if mod:
                    self.import_table[spec.origin] = mod
                    # print(f"Importing python module {node.path_str}")
                    # print(self.import_table[spec.origin])
                    # print(mod.name)
                    # print(mod.source.value)
                    # print(self.import_table)
                    # exit()
                    return mod
                else:
                    raise self.ice(
                        f"Failed to import python module {node.path_str}: {spec.origin}"
                    )
        except Exception as e:
            self.warning(f"Failed to import python module {node.path_str}: {e}")
            if "Empty kid for Token ModulePath" in str(e) or "utf-8" in str(e):
                return None
            self.error(
                f"Failed to import python module {node.path_str}: {e}",
                node_override=node,
            )
            raise e
        return None


class PyImportPass(JacImportPass):
    """Jac statically imports Python modules."""

    def process_import(self, node: ast.Module, i: ast.ModulePath) -> None:
        """Process an import."""
        # print(i)
        # print(7)
        lang = i.parent_of_type(ast.Import).hint.tag.value
        if lang == "py" and not i.sub_module and settings.py_raise:
            # if lang == "py" and not i.sub_module :
            # print(f"Importing python module {i.path_str}")
            # print(2)
            # base_dir = path.dirname(node.loc.mod_path)
            # sys.path.append(base_dir)
            # print('mod_path:---> ',node.alias)
            # print(node.alias)
            # Dynamically import the module
            try:
                spec = importlib.util.find_spec(i.path_str)
            except:
                return None
            # sys.path.remove(base_dir)
            if spec and spec.origin and spec.origin not in {None, "built-in", "frozen"}:
                if spec.origin in self.import_table:
                    return None
            mod = self.import_py_module(node=i, mod_path=node.loc.mod_path)
            # print(3)
            if mod:

                # if mod
                # print('ppppppppp==>',mod.name)
                # if mod.name =='typing':
                #     print(node.pp())
                #     exit()
                # print(f"Importing python module {i.path_str}\n") #uncomment me
                self.run_again = True
                i.sub_module = mod
                i.add_kids_right([mod], pos_update=False)
                # return self.get_all_sub_nodes(mod, ast.ModulePath, brute_force=True)
                xxx = self.get_all_sub_nodes(mod, ast.ModulePath, 89)
                return [
                    yyy
                    for yyy in xxx
                    if yyy.path_str
                    not in [
                        "grp",
                        "_contextvars",
                        "_bisect",
                        "_bz2",
                        "_lzma",
                        "termios",
                        "_socket",
                        "array",
                        "_random",
                        "fcntl",
                        "_posixsubprocess",
                        "_hashlib",
                        "_sha3",
                        "_md5",
                        "pyexpat",
                        "_datetime",
                        "_sha1",
                        "_sha2",
                        "_blake2",
                        "_statistics",
                        "_ssl",
                        "_struct",
                        "select",
                        "encodings",
                        "encodings",
                        "zlib",
                        "_opcode",
                        "readline",
                        "_pickle",
                        "unicodedata",
                        "importlib",
                        "_heapq",
                        "re",
                        "math",
                        "_decimal",
                        "binascii",
                    ]
                ]

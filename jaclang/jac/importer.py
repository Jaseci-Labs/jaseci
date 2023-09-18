"""Special Imports for Jac Code."""
import inspect
import marshal
import sys
import traceback
import types
from os import makedirs, path
from typing import Callable, Optional

from jaclang.jac.constant import Constants as Con, Values as Val
from jaclang.jac.transpiler import transpile_jac_blue, transpile_jac_purple
from jaclang.utils.helpers import add_line_numbers, clip_code_section


def import_jac_module(
    transpiler_func: Callable,
    target: str,
    base_path: Optional[str] = None,
    cachable: bool = True,
    override_name: Optional[str] = None,
) -> Optional[types.ModuleType]:
    """Core Import Process."""
    target = path.join(*(target.split("."))) + ".jac"

    dir_path, file_name = path.split(target)
    module_name = path.splitext(file_name)[0]
    package_path = dir_path.replace(path.sep, ".")

    if package_path and f"{package_path}.{module_name}" in sys.modules:
        return sys.modules[f"{package_path}.{module_name}"]
    elif not package_path and module_name in sys.modules:
        return sys.modules[module_name]

    if base_path:
        caller_dir = path.dirname(base_path) if not path.isdir(base_path) else base_path
    else:
        frame = inspect.stack()[2]
        caller_dir = path.dirname(path.abspath(frame[0].f_code.co_filename))
    full_target = path.normpath(path.join(caller_dir, target))

    dev_dir = path.join(caller_dir, "__jac_gen__")
    makedirs(dev_dir, exist_ok=True)
    py_file_path = path.join(dev_dir, module_name + ".py")
    if (
        cachable
        and path.exists(py_file_path)
        and path.getmtime(py_file_path) > path.getmtime(full_target)
    ):
        with open(py_file_path, "r") as f:
            code_string = f.read()
    else:
        code_string = transpiler_func(file_path=full_target, base_dir=caller_dir)
        with open(py_file_path, "w") as f:
            f.write(code_string)

    module = types.ModuleType(module_name)
    module.__file__ = full_target
    module.__name__ = override_name if override_name else module_name
    module.__dict__["_jac_pycodestring_"] = code_string

    if (
        cachable
        and path.exists(py_file_path + "c")
        and path.getmtime(py_file_path + "c") > path.getmtime(full_target)
    ):
        with open(py_file_path + "c", "rb") as f:
            codeobj = marshal.load(f)
    else:
        try:
            codeobj = compile(code_string, f"_jac_py_gen ({module.__file__})", "exec")
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            err = handle_jac_error(code_string, e, tb)
            raise type(e)(str(e) + "\n" + err)
        with open(py_file_path + "c", "wb") as f:
            marshal.dump(codeobj, f)

    try:
        exec(codeobj, module.__dict__)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        err = handle_jac_error(code_string, e, tb)
        raise type(e)(str(e) + "\n" + err)

    if package_path:
        parts = package_path.split(".")
        for i in range(len(parts)):
            package_name = ".".join(parts[: i + 1])
            if package_name not in sys.modules:
                sys.modules[package_name] = types.ModuleType(package_name)

        setattr(sys.modules[package_path], module_name, module)
        sys.modules[f"{package_path}.{module_name}"] = module
    else:
        sys.modules[module_name] = module
    return module


def handle_jac_error(code_string: str, e: Exception, tb: traceback.StackSummary) -> str:
    """Handle Jac Error."""
    except_line = e.end_lineno if isinstance(e, SyntaxError) else list(tb)[-1].lineno
    if not isinstance(except_line, int) or except_line == 0:
        return ""
    py_error_region = clip_code_section(
        add_line_numbers(code_string), except_line, Val.JAC_ERROR_LINE_RANGE
    )
    try:
        jac_err_line = int(code_string.splitlines()[except_line - 1].split()[-1])
        mod_index = int(code_string.splitlines()[except_line - 1].split()[-2])
        mod_paths = code_string.split(Con.JAC_DEBUG_SPLITTER)[1].strip().splitlines()
        target_mod = mod_paths[mod_index]
        with open(target_mod, "r") as file:
            jac_code_string = file.read()
        jac_error_region = clip_code_section(
            add_line_numbers(jac_code_string), jac_err_line, Val.JAC_ERROR_LINE_RANGE
        )
    except Exception as e:
        jac_error_region = str(e)
        target_mod = ""
    snippet = (
        f"{Con.JAC_ERROR_PREAMBLE}\n"
        f"{target_mod}\n"
        f"JacCode Snippet:\n{jac_error_region}\n"
        f"PyCode Snippet:\n{py_error_region}\n"
    )
    return snippet


def jac_blue_import(
    target: str,
    base_path: Optional[str] = None,
    cachable: bool = True,
    override_name: Optional[str] = None,
) -> Optional[types.ModuleType]:
    """Jac Blue Imports."""
    return import_jac_module(
        transpile_jac_blue, target, base_path, cachable, override_name
    )


def jac_purple_import(
    target: str,
    base_path: Optional[str] = None,
    cachable: bool = True,
    override_name: Optional[str] = None,
) -> Optional[types.ModuleType]:
    """Jac Purple Imports."""
    return import_jac_module(
        transpile_jac_purple, target, base_path, cachable, override_name
    )

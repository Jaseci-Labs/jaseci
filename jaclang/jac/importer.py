"""Special importer for Jac files."""
import inspect
import sys
import types
from os import path

from jaclang.jac.transpiler import transpile_jac_file


def import_jac(target: str) -> types.ModuleType:
    """Import a module from a path."""
    # Convert python import paths to directory paths
    target = path.join(*(target.split("."))) + ".jac"

    # Get module name and package path
    dir_path, file_name = path.split(target)
    module_name = path.splitext(file_name)[0]
    package_path = dir_path.replace(path.sep, ".")

    # Get the directory of the calling module
    frame = inspect.stack()[1]
    caller_dir = path.dirname(path.abspath(frame[0].f_code.co_filename))
    target = path.normpath(path.join(caller_dir, target))

    # Transpile the Jac file
    code_string = transpile_jac_file(target)

    # Create a module object
    module = types.ModuleType(module_name)

    # Set __file__ attribute
    module.__file__ = target

    # Execute the code in the context of the module's namespace
    exec(code_string, module.__dict__)

    # Register the module in sys.modules
    if package_path:
        # Register the package and all subpackages
        parts = package_path.split(".")
        for i in range(len(parts)):
            package_name = ".".join(parts[: i + 1])
            if package_name not in sys.modules:
                sys.modules[package_name] = types.ModuleType(package_name)

        # Set the module as an attribute of the package
        setattr(sys.modules[package_path], module_name, module)

    sys.modules[package_path + "." + module_name] = module

    # Add the module to the calling context's global variables
    return module

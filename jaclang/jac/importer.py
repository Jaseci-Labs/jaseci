"""Special importer for Jac files."""
import inspect
import os
import sys
import types


def import_jac(path: str) -> None:
    """Import a module from a path."""
    with open(path, "r") as file:
        code_string = file.read()

    # Get the absolute path and normalize it
    full_path = os.path.normpath(os.path.abspath(path))

    # Split the path into directory and file
    dir_path, file_name = os.path.split(full_path)

    # Get the module name from the file name by removing the .py extension
    module_name = os.path.splitext(file_name)[0]

    # Get the package path from the directory by replacing path separators with dots
    package_path = dir_path.replace(os.path.sep, ".")

    # Create a module object
    module = types.ModuleType(module_name)

    # Set __file__ attribute
    module.__file__ = full_path

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
    frame = inspect.stack()[1]
    frame[0].f_globals[module_name] = module

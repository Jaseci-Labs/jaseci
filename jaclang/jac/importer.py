"""Special importer for Jac files."""
import inspect
import sys
import types
from os import path


from jaclang.jac.parser import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.jac.passes.ast_build_pass import AstBuildPass
from jaclang.jac.passes.blue_pygen_pass import BluePygenPass
from jaclang.jac.passes.ir_pass import parse_tree_to_ast as ptoa


def import_jac(target: str) -> types.ModuleType:
    """Import a module from a path."""
    # Convert python import paths to directory paths
    target = path.join(*(target.split("."))) + ".jac"

    # Get the directory of the calling module
    frame = inspect.stack()[1]
    caller_dir = path.dirname(path.abspath(frame[0].f_code.co_filename))

    # Get the absolute path to the target module
    target = path.join(caller_dir, target)

    code_string = transpile_jac(target)

    # Get the absolute path and normalize it
    full_path = path.normpath(path.abspath(target))

    # Split the path into directory and file
    dir_path, file_name = path.split(full_path)

    # Get the module name from the file name by removing the .py extension
    module_name = path.splitext(file_name)[0]

    # Get the package path from the directory by replacing path separators with dots
    package_path = dir_path.replace(path.sep, ".")

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
    return module


def transpile_jac(file_path: str) -> str:
    """Convert a Jac file to an AST."""
    lex = JacLexer()
    prse = JacParser(cur_filename=file_path)
    builder = AstBuildPass(mod_name=file_path)
    pygen = BluePygenPass(mod_name=file_path)

    with open(file_path) as file:
        ptree = prse.parse(lex.tokenize(file.read()), filename=file_path)
        ast = builder.run(node=ptoa(ptree if ptree else ()))
        code = pygen.run(node=ast).meta["py_code"]
        return code

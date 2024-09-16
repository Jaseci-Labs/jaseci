"""Command line interface tool for the Jac language."""

import ast as ast3
import importlib
import marshal
import os
import pickle
import shutil
import types
from typing import Optional

import jaclang.compiler.absyntree as ast
from jaclang import jac_import
from jaclang.cli.cmdreg import CommandShell, cmd_registry
from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.constant import Constants
from jaclang.compiler.passes.main.pyast_load_pass import PyastBuildPass
from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.compiler.passes.tool.schedules import format_pass
from jaclang.plugin.builtin import dotgen
from jaclang.plugin.feature import JacCmd as Cmd
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.runtimelib.constructs import WalkerArchitype
from jaclang.runtimelib.context import ExecutionContext
from jaclang.runtimelib.machine import JacMachine, JacProgram
from jaclang.utils.helpers import debugger as db
from jaclang.utils.lang_tools import AstTool


Cmd.create_cmd()
Jac.setup()


@cmd_registry.register
def format(path: str, outfile: str = "", debug: bool = False) -> None:
    """Run the specified .jac file or format all .jac files in a given directory."""

    def format_file(filename: str) -> None:
        code_gen_format = jac_file_to_pass(filename, schedule=format_pass)
        if code_gen_format.errors_had:
            print(f"Errors occurred while formatting the file {filename}.")
        elif debug:
            print(code_gen_format.ir.gen.jac)
        elif outfile:
            with open(outfile, "w") as f:
                f.write(code_gen_format.ir.gen.jac)
        else:
            with open(filename, "w") as f:
                f.write(code_gen_format.ir.gen.jac)

    if path.endswith(".jac"):
        if os.path.exists(path):
            format_file(path)
        else:
            print("File does not exist.")
    elif os.path.isdir(path):
        count = 0
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".jac"):
                    file_path = os.path.join(root, file)
                    format_file(file_path)
                    count += 1
        print(f"Formatted {count} '.jac' files.")
    else:
        print("Not a .jac file or directory.")


@cmd_registry.register
def run(
    filename: str, session: str = "", main: bool = True, cache: bool = True
) -> None:
    """Run the specified .jac file."""
    # if no session specified, check if it was defined when starting the command shell
    # otherwise default to jaclang.session
    if session == "":
        session = (
            cmd_registry.args.session
            if hasattr(cmd_registry, "args")
            and hasattr(cmd_registry.args, "session")
            and cmd_registry.args.session
            else ""
        )

    base, mod = os.path.split(filename)
    base = base if base else "./"
    mod = mod[:-4]

    jctx = ExecutionContext.create(session=session)

    if filename.endswith(".jac"):
        jac_import(
            target=mod,
            base_path=base,
            cachable=cache,
            override_name="__main__" if main else None,
        )
    elif filename.endswith(".jir"):
        with open(filename, "rb") as f:
            JacMachine(base).attach_program(
                JacProgram(mod_bundle=pickle.load(f), bytecode=None)
            )
            jac_import(
                target=mod,
                base_path=base,
                cachable=cache,
                override_name="__main__" if main else None,
            )
    else:
        jctx.close()
        JacMachine.detach()
        raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

    jctx.close()
    JacMachine.detach()


@cmd_registry.register
def get_object(
    filename: str, id: str, session: str = "", main: bool = True, cache: bool = True
) -> dict:
    """Get the object with the specified id."""
    if session == "":
        session = (
            cmd_registry.args.session
            if hasattr(cmd_registry, "args")
            and hasattr(cmd_registry.args, "session")
            and cmd_registry.args.session
            else ""
        )

    base, mod = os.path.split(filename)
    base = base if base else "./"
    mod = mod[:-4]

    jctx = ExecutionContext.create(session=session)

    if filename.endswith(".jac"):
        jac_import(
            target=mod,
            base_path=base,
            cachable=cache,
            override_name="__main__" if main else None,
        )
    elif filename.endswith(".jir"):
        with open(filename, "rb") as f:
            JacMachine(base).attach_program(
                JacProgram(mod_bundle=pickle.load(f), bytecode=None)
            )
            jac_import(
                target=mod,
                base_path=base,
                cachable=cache,
                override_name="__main__" if main else None,
            )
    else:
        jctx.close()
        JacMachine.detach()
        raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

    data = {}
    obj = Jac.get_object(id)
    if obj:
        data = obj.__jac__.__getstate__()
    else:
        print(f"Object with id {id} not found.")

    jctx.close()
    JacMachine.detach()
    return data


@cmd_registry.register
def build(filename: str) -> None:
    """Build the specified .jac file."""
    if filename.endswith(".jac"):
        out = jac_file_to_pass(file_path=filename, schedule=py_code_gen_typed)
        errs = len(out.errors_had)
        warnings = len(out.warnings_had)
        print(f"Errors: {errs}, Warnings: {warnings}")
        for i in out.ir.flatten():
            i.gen.clean()
        with open(filename[:-4] + ".jir", "wb") as f:
            pickle.dump(out.ir, f)
    else:
        print("Not a .jac file.")


@cmd_registry.register
def check(filename: str, print_errs: bool = True) -> None:
    """Run type checker for a specified .jac file.

    :param filename: The path to the .jac file.
    """
    if filename.endswith(".jac"):
        out = jac_file_to_pass(
            file_path=filename,
            schedule=py_code_gen_typed,
        )

        errs = len(out.errors_had)
        warnings = len(out.warnings_had)
        if print_errs:
            for e in out.errors_had:
                print("Error:", e)
        print(f"Errors: {errs}, Warnings: {warnings}")
    else:
        print("Not a .jac file.")


@cmd_registry.register
def lsp() -> None:
    """Run Jac Language Server Protocol."""
    from jaclang.langserve.server import run_lang_server

    run_lang_server()


@cmd_registry.register
def enter(
    filename: str,
    entrypoint: str,
    args: list,
    session: str = "",
    main: bool = True,
    cache: bool = True,
    root: str = "",
    node: str = "",
) -> None:
    """
    Run the specified entrypoint function in the given .jac file.

    :param filename: The path to the .jac file.
    :param entrypoint: The name of the entrypoint function.
    :param args: Arguments to pass to the entrypoint function.
    :param session: shelve.Shelf file path.
    :param root: root executor.
    :param node: starting node.
    """
    if session == "":
        session = (
            cmd_registry.args.session
            if hasattr(cmd_registry, "args")
            and hasattr(cmd_registry.args, "session")
            and cmd_registry.args.session
            else ""
        )

    base, mod = os.path.split(filename)
    base = base if base else "./"
    mod = mod[:-4]

    jctx = ExecutionContext.create(session=session, root=root)

    if filename.endswith(".jac"):
        ret_module = jac_import(
            target=mod,
            base_path=base,
            cachable=cache,
            override_name="__main__" if main else None,
        )
    elif filename.endswith(".jir"):
        with open(filename, "rb") as f:
            JacMachine(base).attach_program(
                JacProgram(mod_bundle=pickle.load(f), bytecode=None)
            )
            ret_module = jac_import(
                target=mod,
                base_path=base,
                cachable=cache,
                override_name="__main__" if main else None,
            )
    else:
        jctx.close()
        JacMachine.detach()
        raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

    if ret_module:
        (loaded_mod,) = ret_module
        if not loaded_mod:
            print("Errors occurred while importing the module.")
        else:
            architype = getattr(loaded_mod, entrypoint)(*args)

            jctx.set_entry_node(node)

            if isinstance(architype, WalkerArchitype) and Jac.check_read_access(
                jctx.entry_node
            ):
                Jac.spawn_call(jctx.entry_node.architype, architype)

    jctx.close()
    JacMachine.detach()


@cmd_registry.register
def test(
    filepath: str,
    filter: str = "",
    xit: bool = False,
    maxfail: int = None,  # type:ignore
    directory: str = "",
    verbose: bool = False,
) -> None:
    """Run the test suite in the specified .jac file.

    :param filepath: Path/to/file.jac
    :param filter: Filter the files using Unix shell style conventions.
    :param xit(exit): Stop(exit) running tests as soon as finds an error.
    :param maxfail: Stop running tests after n failures.
    :param directory: Run tests from the specified directory.
    :param verbose: Show more info.

    jac test => jac test -d .
    """
    jctx = ExecutionContext.create()

    failcount = Jac.run_test(
        filepath=filepath,
        filter=filter,
        xit=xit,
        maxfail=maxfail,
        directory=directory,
        verbose=verbose,
    )

    jctx.close()

    if failcount:
        raise SystemExit(f"Tests failed: {failcount}")


@cmd_registry.register
def tool(tool: str, args: Optional[list] = None) -> None:
    """Run the specified AST tool with optional arguments.

    :param tool: The name of the AST tool to run.
    :param args: Optional arguments for the AST tool.
    """
    if hasattr(AstTool, tool):
        try:
            if args and len(args):
                print(getattr(AstTool(), tool)(args))
            else:
                print(getattr(AstTool(), tool)())
        except Exception as e:
            print(f"Error while running ast tool {tool}, check args: {e}")
            raise e
    else:
        print(f"Ast tool {tool} not found.")


@cmd_registry.register
def clean() -> None:
    """Remove the __jac_gen__ , __pycache__ folders.

    from the current directory recursively.
    """
    current_dir = os.getcwd()
    for root, dirs, _files in os.walk(current_dir, topdown=True):
        for folder_name in dirs[:]:
            if folder_name in [Constants.JAC_GEN_DIR, Constants.JAC_MYPY_CACHE]:
                folder_to_remove = os.path.join(root, folder_name)
                shutil.rmtree(folder_to_remove)
                print(f"Removed folder: {folder_to_remove}")
    print("Done cleaning.")


@cmd_registry.register
def debug(filename: str, main: bool = True, cache: bool = False) -> None:
    """Debug the specified .jac file using pdb."""
    base, mod = os.path.split(filename)
    base = base if base else "./"
    mod = mod[:-4]
    if filename.endswith(".jac"):
        bytecode = jac_file_to_pass(filename).ir.gen.py_bytecode
        if bytecode:
            code = marshal.loads(bytecode)
            if db.has_breakpoint(bytecode):
                run(filename, main, cache)
            else:
                func = types.FunctionType(code, globals())

                print("Debugging with Jac debugger.\n")
                db.runcall(func)
                print("Done debugging.")
        else:
            print(f"Error while generating bytecode in {filename}.")
    else:
        print("Not a .jac file.")


@cmd_registry.register
def dot(
    filename: str,
    session: str = "",
    initial: str = "",
    depth: int = -1,
    traverse: bool = False,
    connection: list[str] = [],  # noqa: B006
    bfs: bool = False,
    edge_limit: int = 512,
    node_limit: int = 512,
    saveto: str = "",
) -> None:
    """Generate and Visualize a graph based on the specified .jac file contents and parameters.

    :param filename: The name of the file to generate the graph from.
    :param initial: The initial node for graph traversal (default is root node).
    :param depth: The maximum depth for graph traversal (-1 for unlimited depth, default is -1).
    :param traverse: Flag to indicate whether to traverse the graph (default is False).
    :param connection: List of node connections(edge type) to include in the graph (default is an empty list).
    :param bfs: Flag to indicate whether to use breadth-first search for traversal (default is False).
    :param edge_limit: The maximum number of edges allowed in the graph.
    :param node_limit: The maximum number of nodes allowed in the graph.
    :param saveto: Path to save the generated graph.
    """
    if session == "":
        session = (
            cmd_registry.args.session
            if hasattr(cmd_registry, "args")
            and hasattr(cmd_registry.args, "session")
            and cmd_registry.args.session
            else ""
        )

    base, mod = os.path.split(filename)
    base = base if base else "./"
    mod = mod[:-4]

    jctx = ExecutionContext.create(session=session)

    if filename.endswith(".jac"):
        jac_machine = JacMachine(base)
        jac_import(target=mod, base_path=base, override_name="__main__")
        module = jac_machine.loaded_modules.get("__main__")
        globals().update(vars(module))
        try:
            node = globals().get(initial, eval(initial)) if initial else None
            graph = dotgen(
                node=node,
                depth=depth,
                traverse=traverse,
                edge_type=connection,
                bfs=bfs,
                edge_limit=edge_limit,
                node_limit=node_limit,
            )
        except Exception as e:
            print(f"Error while generating graph: {e}")
            import traceback

            traceback.print_exc()
            jctx.close()
            return
        file_name = saveto if saveto else f"{mod}.dot"
        with open(file_name, "w") as file:
            file.write(graph)
        print(f">>> Graph content saved to {os.path.join(os.getcwd(), file_name)}")
    else:
        print("Not a .jac file.")

    jctx.close()


@cmd_registry.register
def py2jac(filename: str) -> None:
    """Convert a Python file to Jac.

    :param filename: The path to the .py file.
    """
    if filename.endswith(".py"):
        with open(filename, "r") as f:
            code = PyastBuildPass(
                input_ir=ast.PythonModuleAst(ast3.parse(f.read()), mod_path=filename),
            ).ir.unparse()
        print(code)
    else:
        print("Not a .py file.")


@cmd_registry.register
def jac2py(filename: str) -> None:
    """Convert a Jac file to Python.

    :param filename: The path to the .jac file.
    """
    if filename.endswith(".jac"):
        with open(filename, "r"):
            code = jac_file_to_pass(file_path=filename).ir.gen.py
        print(code)
    else:
        print("Not a .jac file.")


def start_cli() -> None:
    """
    Start the command line interface.

    Returns:
    - None
    """
    parser = cmd_registry.parser
    args = parser.parse_args()
    cmd_registry.args = args

    if args.version:
        version = importlib.metadata.version("jaclang")
        print(f"Jac version {version}")
        return

    command = cmd_registry.get(args.command)
    if command:
        args_dict = vars(args)
        args_dict.pop("command")
        args_dict.pop("version", None)
        ret = command.call(**args_dict)
        if ret:
            print(ret)
    else:
        CommandShell(cmd_registry).cmdloop()


if __name__ == "__main__":
    start_cli()

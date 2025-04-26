"""Command line interface tool for the Jac language."""

import ast as ast3
import importlib
import marshal
import os
import pickle
import shutil
import sys
import types
from typing import Optional

import jaclang.compiler.unitree as uni
from jaclang.cli.cmdreg import CommandShell, cmd_registry
from jaclang.compiler.constant import Constants
from jaclang.compiler.passes.main.pyast_load_pass import PyastBuildPass
from jaclang.compiler.passes.main.schedules import py_code_gen_build, py_code_gen_typed
from jaclang.compiler.program import JacProgram
from jaclang.runtimelib.builtin import dotgen
from jaclang.runtimelib.constructs import WalkerArchitype
from jaclang.runtimelib.machine import JacMachine as Jac
from jaclang.runtimelib.machinestate import JacMachineState, call_jac_func_with_machine
from jaclang.utils.helpers import debugger as db
from jaclang.utils.lang_tools import AstTool


Jac.create_cmd()
Jac.setup()


@cmd_registry.register
def format(path: str, outfile: str = "", to_screen: bool = False) -> None:
    """Run the specified .jac file or format all .jac files in a given directory."""

    def format_file(filename: str) -> None:
        code_gen_format = JacProgram.jac_file_formatter(filename)
        if to_screen:
            print(code_gen_format)
        elif outfile:
            with open(outfile, "w") as f:
                f.write(code_gen_format)
        else:
            with open(filename, "w") as f:
                f.write(code_gen_format)

    if path.endswith(".jac"):
        if os.path.exists(path):
            format_file(path)
        else:
            print("File does not exist.", file=sys.stderr)
    elif os.path.isdir(path):
        count = 0
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".jac"):
                    file_path = os.path.join(root, file)
                    format_file(file_path)
                    count += 1
        print(f"Formatted {count} '.jac' files.", file=sys.stderr)
    else:
        print("Not a .jac file or directory.", file=sys.stderr)


def proc_file_sess(
    filename: str, session: str, root: Optional[str] = None, interp: bool = False
) -> tuple[str, str, JacMachineState]:
    """Create JacMachineState and return the base path, module name, and machine state."""
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
    mach = JacMachineState(base, session=session, root=root, interp_mode=interp)
    return base, mod, mach


@cmd_registry.register
def run(
    filename: str,
    session: str = "",
    main: bool = True,
    cache: bool = True,
    interp: bool = False,
) -> None:
    """Run the specified .jac file."""
    # if no session specified, check if it was defined when starting the command shell
    # otherwise default to jaclang.session
    base, mod, mach = proc_file_sess(filename, session, interp=interp)

    if filename.endswith(".jac"):
        try:
            Jac.jac_import(
                mach=mach,
                target=mod,
                base_path=base,
                override_name="__main__" if main else None,
            )
        except Exception as e:
            print(e, file=sys.stderr)
    elif filename.endswith(".jir"):
        try:
            with open(filename, "rb") as f:
                Jac.attach_program(mach, pickle.load(f))
                Jac.jac_import(
                    mach=mach,
                    target=mod,
                    base_path=base,
                    override_name="__main__" if main else None,
                )
        except Exception as e:
            print(e, file=sys.stderr)

    else:
        print("Not a valid file!\nOnly supports `.jac` and `.jir`")
    mach.exec_ctx.close()


@cmd_registry.register
def get_object(
    filename: str, id: str, session: str = "", main: bool = True, cache: bool = True
) -> dict:
    """Get the object with the specified id."""
    base, mod, mach = proc_file_sess(filename, session)

    if filename.endswith(".jac"):
        Jac.jac_import(
            mach=mach,
            target=mod,
            base_path=base,
            override_name="__main__" if main else None,
        )
    elif filename.endswith(".jir"):
        with open(filename, "rb") as f:
            Jac.attach_program(
                mach,
                pickle.load(f),
            )
            Jac.jac_import(
                mach=mach,
                target=mod,
                base_path=base,
                override_name="__main__" if main else None,
            )
    else:
        mach.exec_ctx.close()
        raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

    data = {}
    obj = call_jac_func_with_machine(mach, Jac.get_object, id)
    if obj:
        data = obj.__jac__.__getstate__()
    else:
        print(f"Object with id {id} not found.", file=sys.stderr)

    mach.exec_ctx.close()
    return data


@cmd_registry.register
def build(filename: str, pybuild: bool = False) -> None:
    """Build the specified .jac file."""
    if filename.endswith(".jac"):
        (out := JacProgram()).compile(
            file_path=filename,
            schedule=py_code_gen_typed if pybuild else py_code_gen_build,
        )
        errs = len(out.errors_had)
        warnings = len(out.warnings_had)
        print(f"Errors: {errs}, Warnings: {warnings}")
        with open(filename[:-4] + ".jir", "wb") as f:
            pickle.dump(out, f)
    else:
        print("Not a .jac file.", file=sys.stderr)


@cmd_registry.register
def check(filename: str, print_errs: bool = True) -> None:
    """Run type checker for a specified .jac file.

    :param filename: The path to the .jac file.
    """
    if filename.endswith(".jac"):
        (prog := JacProgram()).compile(
            file_path=filename,
            schedule=py_code_gen_typed,
        )

        errs = len(prog.errors_had)
        warnings = len(prog.warnings_had)
        if print_errs:
            for e in prog.errors_had:
                print("Error:", e, file=sys.stderr)
        print(f"Errors: {errs}, Warnings: {warnings}")
    else:
        print("Not a .jac file.", file=sys.stderr)


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
    base, mod, mach = proc_file_sess(filename, session, root)

    if filename.endswith(".jac"):
        ret_module = Jac.jac_import(
            mach=mach,
            target=mod,
            base_path=base,
            override_name="__main__" if main else None,
        )
    elif filename.endswith(".jir"):
        with open(filename, "rb") as f:
            Jac.attach_program(
                mach,
                pickle.load(f),
            )
            ret_module = Jac.jac_import(
                mach=mach,
                target=mod,
                base_path=base,
                override_name="__main__" if main else None,
            )
    else:
        mach.exec_ctx.close()
        raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

    if ret_module:
        (loaded_mod,) = ret_module
        if not loaded_mod:
            print("Errors occurred while importing the module.", file=sys.stderr)
        else:
            architype = getattr(loaded_mod, entrypoint)(*args)

            mach.exec_ctx.set_entry_node(node)
            if isinstance(architype, WalkerArchitype) and call_jac_func_with_machine(
                mach, Jac.check_read_access, mach.exec_ctx.entry_node
            ):
                Jac.spawn(mach.exec_ctx.entry_node.architype, architype)

    mach.exec_ctx.close()


@cmd_registry.register
def test(
    filepath: str,
    test_name: str = "",
    filter: str = "",
    xit: bool = False,
    maxfail: int = None,  # type:ignore
    directory: str = "",
    verbose: bool = False,
) -> None:
    """Run the test suite in the specified .jac file.

    :param filepath: Path/to/file.jac
    :param test_name: Run a specific test.
    :param filter: Filter the files using Unix shell style conventions.
    :param xit(exit): Stop(exit) running tests as soon as finds an error.
    :param maxfail: Stop running tests after n failures.
    :param directory: Run tests from the specified directory.
    :param verbose: Show more info.

    jac test => jac test -d .
    """
    mach = JacMachineState()

    failcount = Jac.run_test(
        mach=mach,
        filepath=filepath,
        func_name=("test_" + test_name) if test_name else None,
        filter=filter,
        xit=xit,
        maxfail=maxfail,
        directory=directory,
        verbose=verbose,
    )

    mach.exec_ctx.close()

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
            print(
                f"Error while running ast tool {tool}, check args: {e}", file=sys.stderr
            )
            raise e
    else:
        print(f"Ast tool {tool} not found.", file=sys.stderr)


@cmd_registry.register
def clean() -> None:
    """Remove the __jac_gen__ , __pycache__ folders.

    from the current directory recursively.
    """
    current_dir = os.getcwd()
    for root, dirs, _files in os.walk(current_dir, topdown=True):
        for folder_name in dirs[:]:
            if folder_name in [Constants.JAC_MYPY_CACHE]:
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
        bytecode = JacProgram().compile(filename).gen.py_bytecode
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
            print(f"Error while generating bytecode in {filename}.", file=sys.stderr)
    else:
        print("Not a .jac file.", file=sys.stderr)


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
    base, mod, jac_machine = proc_file_sess(filename, session)

    if filename.endswith(".jac"):
        Jac.jac_import(
            mach=jac_machine, target=mod, base_path=base, override_name="__main__"
        )
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
            jac_machine.exec_ctx.close()
            return
        file_name = saveto if saveto else f"{mod}.dot"
        with open(file_name, "w") as file:
            file.write(graph)
        print(f">>> Graph content saved to {os.path.join(os.getcwd(), file_name)}")
        jac_machine.exec_ctx.close()
    else:
        print("Not a .jac file.", file=sys.stderr)


@cmd_registry.register
def py2jac(filename: str) -> None:
    """Convert a Python file to Jac.

    :param filename: The path to the .py file.
    """
    if filename.endswith(".py"):
        with open(filename, "r") as f:
            file_source = f.read()
            code = PyastBuildPass(
                ir_in=uni.PythonModuleAst(
                    ast3.parse(file_source),
                    orig_src=uni.Source(file_source, filename),
                ),
                prog=JacProgram(),
            ).ir_out.unparse()
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
            code = JacProgram().compile(file_path=filename).gen.py
        print(code)
    else:
        print("Not a .jac file.", file=sys.stderr)


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
        print("Jac path:", __file__)
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

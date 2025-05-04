"""Common code for command line interface tool for the Jac language."""

from __future__ import annotations

import argparse
import cmd
import inspect
import pprint
import re
from typing import Callable, Dict, Optional


class Command:
    """Represents a command in the command line interface."""

    func: Callable
    sig: inspect.Signature

    def __init__(self, func: Callable) -> None:
        """Initialize a Command instance."""
        self.func = func
        self.sig = inspect.signature(func)

    def call(self, *args: list, **kwargs: dict) -> str:
        """Call the associated function with the specified arguments and keyword arguments."""
        return self.func(*args, **kwargs)


def extract_param_descriptions(docstring: str) -> Dict[str, str]:
    """Extract parameter descriptions from a function's docstring.

    Args:
        docstring: The function's docstring

    Returns:
        A dictionary mapping parameter names to their descriptions
    """
    param_descriptions: dict[str, str] = {}

    # Check if the docstring has an Args section
    args_match = re.search(r"Args:(.*?)(?:\n\n|\Z)", docstring, re.DOTALL)
    if not args_match:
        return param_descriptions

    args_section = args_match.group(1)

    # Extract parameter descriptions from the Args section
    # Looking for patterns like "param_name: Description" or "param_name (type): Description"
    current_param = None
    current_desc = []

    for line in args_section.strip().split("\n"):
        line = line.strip()
        if not line:
            continue

        # Match parameter name at the beginning of the line
        param_match = re.match(r"\s*([a-zA-Z0-9_]+)(?:\s*\([^)]*\))?:\s*(.*)", line)
        if param_match:
            # Save the previous parameter if there was one
            if current_param and current_desc:
                param_descriptions[current_param] = " ".join(current_desc)
                current_desc = []

            # Start a new parameter
            current_param = param_match.group(1)
            if param_match.group(2):
                current_desc.append(param_match.group(2))
        elif current_param and line:
            # Continue the description for the current parameter
            current_desc.append(line)

    # Save the last parameter
    if current_param and current_desc:
        param_descriptions[current_param] = " ".join(current_desc)

    return param_descriptions


class CommandRegistry:
    """Registry for managing commands in the command line interface."""

    registry: dict[str, Command]
    sub_parsers: argparse._SubParsersAction
    parser: argparse.ArgumentParser
    args: argparse.Namespace

    def __init__(self) -> None:
        """Initialize a CommandRegistry instance."""
        self.registry = {}
        self.parser = argparse.ArgumentParser(
            prog="jac",
            description="Jac Programming Language CLI - A tool for working with Jac programs",
            epilog="For more information, visit: https://github.com/Jaseci-Labs/jaseci",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        self.parser.add_argument(
            "-V",
            "--version",
            action="store_true",
            help="Show the Jac version and installation path",
        )
        self.sub_parsers = self.parser.add_subparsers(
            title="commands",
            dest="command",
            description="The following commands are available:",
            metavar="COMMAND",
        )
        self.args = argparse.Namespace()

    def register(self, func: Callable) -> Callable:
        """Register a command in the registry."""
        name = func.__name__
        cmd = Command(func)
        self.registry[name] = cmd
        # Extract the first paragraph from the docstring for brief description
        doc = func.__doc__ or ""
        brief_desc = doc.split("\n\n")[0].strip()

        # Use the full docstring for the detailed description
        cmd_parser: argparse.ArgumentParser = self.sub_parsers.add_parser(
            name,
            description=func.__doc__,
            help=brief_desc,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        first = True
        for param_name, param in cmd.sig.parameters.items():
            # Get parameter type name
            type_name = (
                param.annotation.__name__
                if hasattr(param.annotation, "__name__")
                else str(param.annotation)
            )

            # Extract parameter descriptions from the docstring
            docstring_param_descriptions = extract_param_descriptions(doc)

            # Use docstring description if available, otherwise fallback to predefined or just type
            if param_name in docstring_param_descriptions:
                arg_msg = f"{type_name} - {docstring_param_descriptions[param_name]}"
            else:
                arg_msg = f"{type_name}"
            # shorthand is first character by default,
            # If already taken, use the first 2 characters
            shorthand = param_name[:1]
            if f"-{shorthand}" in cmd_parser._option_string_actions:
                shorthand = param_name[:2]
            if param_name == "args":
                cmd_parser.add_argument("args", nargs=argparse.REMAINDER, help=arg_msg)
            elif param_name == "filepath":
                first = False
                cmd_parser.add_argument(
                    f"{param_name}",
                    type=(
                        eval(param.annotation)
                        if isinstance(param.annotation, str)
                        else param.annotation
                    ),
                    help=arg_msg,
                    nargs="?",
                )
            elif param.default is param.empty:
                if first:
                    first = False
                    cmd_parser.add_argument(
                        f"{param_name}",
                        type=(
                            eval(param.annotation)
                            if isinstance(param.annotation, str)
                            else param.annotation
                        ),
                        help=arg_msg,
                    )
                else:
                    cmd_parser.add_argument(
                        f"-{shorthand}",
                        f"--{param_name}",
                        required=True,
                        type=(
                            eval(param.annotation)
                            if isinstance(param.annotation, str)
                            else param.annotation
                        ),
                        help=arg_msg,
                    )
            elif first:
                arg_msg += f", default: {param.default}"
                first = False
                cmd_parser.add_argument(
                    f"{param_name}",
                    default=param.default,
                    type=eval(param.annotation),
                    help=arg_msg,
                )
            else:
                arg_msg += f", default: {param.default}"
                if param.annotation == bool:
                    cmd_parser.add_argument(
                        f"-{shorthand}",
                        f"--{param_name}",
                        default=param.default,
                        action="store_true",
                        help=arg_msg,
                    )
                    cmd_parser.add_argument(
                        f"-n{shorthand}",
                        f"--no-{param_name}",
                        dest=param_name,
                        action="store_false",
                        help=f"Compliment of {arg_msg}",
                    )
                else:
                    cmd_parser.add_argument(
                        f"-{shorthand}",
                        f"--{param_name}",
                        default=param.default,
                        help=arg_msg,
                        type=(
                            eval(param.annotation)
                            if isinstance(param.annotation, str)
                            else param.annotation
                        ),
                    )
        return func

    def get(self, name: str) -> Optional[Command]:
        """Get the Command instance for a given command name."""
        return self.registry.get(name)

    def get_all_commands(self) -> dict:
        """Get all registered commands along with their details."""
        all_commands = {}
        for name, comd in self.registry.items():
            doc = comd.func.__doc__ or "No help available."
            args = comd.sig.parameters
            all_commands[name] = (doc, args)
        return all_commands


cmd_registry = CommandRegistry()


class CommandShell(cmd.Cmd):
    """Command shell for the command line interface."""

    intro = "Welcome to the Jac CLI!"
    prompt = "jac> "
    cmd_reg: CommandRegistry

    def __init__(self, cmd_reg: CommandRegistry) -> None:
        """Initialize a CommandShell instance."""
        self.cmd_reg = cmd_reg
        super().__init__()

    def do_exit(self, arg: list) -> bool:
        """Exit the command shell."""
        return True

    def default(self, line: str) -> None:
        """Process the command line input."""
        args = vars(self.cmd_reg.parser.parse_args(line.split()))
        command = self.cmd_reg.get(args["command"])
        if command:
            args.pop("command")
            ret = command.call(**args)
            if ret:
                ret_str = pprint.pformat(ret, indent=2)
                self.stdout.write(f"{ret_str}\n")

    def do_help(self, arg: str) -> None:
        """Jac CLI help implementation."""

        def get_info(name: str, doc: str, args: dict[str, inspect.Parameter]) -> None:
            """Format and display detailed command information."""
            # Format the command header
            self.stdout.write(f"\n{'=' * 80}\n")
            self.stdout.write(f"COMMAND: {name}\n")
            self.stdout.write(f"{'=' * 80}\n\n")

            # Format the command description
            doc_lines = doc.strip().split("\n")
            for line in doc_lines:
                self.stdout.write(f"{line}\n")

            # Format the command arguments
            if args:
                self.stdout.write("\nARGUMENTS:\n")
                for param_name, param in args.items():
                    # Get parameter type
                    type_name = (
                        param.annotation.__name__
                        if hasattr(param.annotation, "__name__")
                        else str(param.annotation)
                    )

                    # Format default value if present
                    default_str = ""
                    if param.default is not param.empty:
                        default_str = f" (default: {param.default})"

                    # Format required/optional status
                    req_str = (
                        " [required]"
                        if param.default is param.empty and param_name != "args"
                        else " [optional]"
                    )

                    self.stdout.write(
                        f"  {param_name}: {type_name}{default_str}{req_str}\n"
                    )
            else:
                self.stdout.write("\nNo arguments\n")

            # Format usage examples
            command_parser = self.cmd_reg.sub_parsers.choices[name]
            self.stdout.write(f"\nUSAGE:\n  {command_parser.format_usage()[7:]}\n")

            # Extract and format examples from docstring if present
            if "Examples:" in doc:
                examples_section = doc.split("Examples:")[1].strip()
                example_lines = examples_section.split("\n")
                self.stdout.write("\nEXAMPLES:\n")
                for example in example_lines:
                    if example.strip():
                        self.stdout.write(f"  {example.strip()}\n")

            self.stdout.write("\n")

        if arg == "all":
            # Display all commands with their details
            command_details = self.cmd_reg.get_all_commands()
            for name, (doc, args) in sorted(command_details.items()):
                get_info(name, doc, args)

        elif arg:
            # Display help for a specific command
            command = self.cmd_reg.get(arg)
            if command:
                doc = command.func.__doc__ or "No help available."
                args = command.sig.parameters
                get_info(arg, doc, args)
            else:
                self.stdout.write(f"\nUnknown command: '{arg}'\n")
                self.stdout.write("Type 'help' to see available commands.\n")
        else:
            # Display general help information
            self.stdout.write("\n")
            self.stdout.write("JAC PROGRAMMING LANGUAGE COMMAND LINE INTERFACE\n")
            self.stdout.write("=" * 50 + "\n\n")

            self.stdout.write("AVAILABLE COMMANDS:\n")

            # Get all command names and sort them alphabetically
            command_names = sorted(self.cmd_reg.registry.keys())

            # Get brief descriptions for each command
            command_descriptions: dict[str, str] = {}
            for name in command_names:
                command = self.cmd_reg.get(name)
                if command and command.func.__doc__:
                    # Extract the first line of the docstring as a brief description
                    brief = command.func.__doc__.split("\n")[0].strip()
                    command_descriptions[name] = brief
                else:
                    command_descriptions[name] = "No description available"

            # Display commands with their brief descriptions
            for name in command_names:
                self.stdout.write(
                    f"  {name.ljust(15)} - {command_descriptions[name]}\n"
                )

            self.stdout.write("\nFor detailed information on a specific command:\n")
            self.stdout.write("  help <command>\n")

            self.stdout.write("\nTo see detailed information for all commands:\n")
            self.stdout.write("  help all\n")

            self.stdout.write("\nTo exit the Jac CLI:\n")
            self.stdout.write("  exit\n\n")

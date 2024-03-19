"""Common code for command line interface tool for the Jac language."""

from __future__ import annotations

import argparse
import cmd
import inspect
from typing import Callable, Optional


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


class CommandRegistry:
    """Registry for managing commands in the command line interface."""

    registry: dict[str, Command]
    sub_parsers: argparse._SubParsersAction
    parser: argparse.ArgumentParser

    def __init__(self) -> None:
        """Initialize a CommandRegistry instance."""
        self.registry = {}
        self.parser = argparse.ArgumentParser(prog="CLI")
        self.sub_parsers = self.parser.add_subparsers(title="commands", dest="command")

    def register(self, func: Callable) -> Callable:
        """Register a command in the registry."""
        name = func.__name__
        cmd = Command(func)
        self.registry[name] = cmd
        cmd_parser: argparse.ArgumentParser = self.sub_parsers.add_parser(
            name, description=func.__doc__
        )
        first = True
        for param_name, param in cmd.sig.parameters.items():
            arg_msg = f"type: {param.annotation.__name__}"
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
                        f"-{param_name[:1]}",
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
                        f"-{param_name[:1]}",
                        f"--{param_name}",
                        default=param.default,
                        action="store_true",
                        help=arg_msg,
                    )
                    cmd_parser.add_argument(
                        f"-n{param_name[:1]}",
                        f"--no-{param_name}",
                        dest=param_name,
                        action="store_false",
                        help=f"Compliment of {arg_msg}",
                    )
                else:
                    cmd_parser.add_argument(
                        f"-{param_name[:1]}",
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
        try:
            args = vars(self.cmd_reg.parser.parse_args(line.split()))
            command = self.cmd_reg.get(args["command"])
            if command:
                args.pop("command")
                ret = command.call(**args)
                if ret:
                    self.stdout.write(ret + "\n")
        except Exception as e:
            print(e)

    def do_help(self, arg: str) -> None:
        """Jac CLI 'help' implementaion."""

        def get_info(name: str, doc: str, args: dict[str, inspect.Parameter]) -> None:
            """Details to display."""
            arg_details = ", ".join(
                [
                    f"{param.name}: {param.annotation.__name__}"
                    for param in args.values()
                ]
            )
            self.stdout.write(f"{name}: {doc}\n")
            self.stdout.write(
                f"\tArguments: {arg_details}\n" if arg_details else "\tNo arguments\n"
            )
            command_parser = self.cmd_reg.sub_parsers.choices[name]
            self.stdout.write(f"\tUsage: {command_parser.format_usage()[7:]}\n")

        if arg == "all":
            commands = self.cmd_reg.get_all_commands()
            for name, (doc, args) in commands.items():
                get_info(name, doc, args)

        elif arg:
            command = self.cmd_reg.get(arg)
            if command:
                doc = command.func.__doc__ or "No help available."
                args = command.sig.parameters
                get_info(arg, doc, args)
            else:
                self.stdout.write(f"\tUnknown command: {arg}; Type 'help'\n")
        else:
            self.stdout.write("\tWelcome to Jaseci's help utility!\n")
            self.stdout.write(
                "\tType 'help all' to see all available commands with details. or,\n"
            )
            self.stdout.write(
                f"\tType 'help <choose on of ({', '.join(self.cmd_reg.registry.keys())})>'"
                " to see details of a specific command.\n"
            )
            self.stdout.write("\tType 'exit' to exit the Jac CLI.\n\n")

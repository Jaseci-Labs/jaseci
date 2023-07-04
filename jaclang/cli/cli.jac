"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such production Jac program.
"""

import:py inspect;
import:py argparse;
import:py cmd;

include:jac cli_imp;


object Command {
    has func: callable,
        sig: inspect.Signature;

    can:priv init(func: callable);
    can call(*args: list, **kwargs: dict);
}


object CommandRegistry {
    has:priv registry: dict[str, Command],
             sub_parsers: argparse._SubParsersActionp;
    has:pub parser: argparse.ArgumentParser;

    can init;
    can register(func: callable);
    can get(name: str) -> Command;
    can items -> dict[str, Command];
}

object CommandShell:cmd.Cmd {
    static has intro: str = "Welcome to the Jac CLI!",
               prompt: str = "jac> ";
    has cmd_reg: CommandRegistry;

    can init (cmd_reg: CommandRegistry);
    can do_exit(arg: list) -> bool;
    can default(line: str);
}

global command_registry = |> CommandRegistry;

can run {
    parser = command_registry.parser;
    args = |> parser.parse_args;
    command = args.command |> command_registry.get;
    if command {
        args = args |> vars;
        "command" |> args.pop;
        **args |> command.call |> print;
    }
    else {
        shell = |> CommandShell(command_registry).cmdloop;
    }
}

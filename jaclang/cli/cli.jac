"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such complete Jac program.
"""

import:py inspect;
import:py argparse;
import:py cmd;
include:jac impl.cli_impl;


object Command {
    has func: callable,
        sig: inspect.Signature;

    can:private <init>(func: callable);
    can call(*args: list, **kwargs: dict);
}


object CommandRegistry {
    has:private registry: dict[str, Command],
             sub_parsers: argparse._SubParsersActionp;
    has:public parser: argparse.ArgumentParser;

    can <init>;
    can register(func: callable);
    can get(name: str) -> Command;
    can items -> dict[str, Command];
}


object CommandShell:cmd.Cmd: {
    static has intro: str = "Welcome to the Jac CLI!",
               prompt: str = "jac> ";
    has cmd_reg: CommandRegistry;

    can <init>(cmd_reg: CommandRegistry);
    can do_exit(arg: list) -> bool;
    can default(line: str);
}


global cmd_registry = |> CommandRegistry;
can start_cli;
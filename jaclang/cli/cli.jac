"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such production Jac program.
"""

import:py inspect;
import:py argparse;
import:py cmd;


object Command {
    has func: callable,
        sig: inspect.Signature;

    can:priv init(func: callable) {
        <h>.func = func;
        <h>.sig = func |> inspect.signature;
    }

    can call(*args: list, **kwargs: dict) {
        return {*args, **kwargs} |> <h>.func;
    }
}


object CommandRegistry {
    has:priv registry: dict[str, Command],
        sub_parsers: argparse._SubParsersActionp;
    has:pub parser: argparse.ArgumentParser;

    can init {
        <h>.registry = {};
        <h>.parser = {prog="CLI"} |> argparse.ArgumentParser;
        <h>.sub_parsers = {title="commands", dest="command"}
            |> <h>.parser.add_subparsers;
    }

    can register(func: callable) {
        name = func.__name__;
        cmd = func |> Command;
        <h>.registry[name] = cmd;
        cmd_parser = name |> <h>.sub_parsers.add_parser;
        for param_name, param in |> cmd.sig.parameters.items {
            if param.default is param.empty {
                {f"-{param_name}", required=True, type=param.annotation}
                    |> cmd_parser.add_argument;
            }
            else {
                {f"-{param_name}", default=param.default, type=param.annotation}
                    |> cmd_parser.add_argument;
            }
        }
    }

    can get(name: str) -> Command {
        return name |> <h>.registry.get;
    }

    can items -> dict[str, Command] {
        return |> <h>.registry.items;
    }
}

object CommandShell:cmd.Cmd {
    static has intro: str = "Welcome to the Jac CLI!",
               prompt: str = "jac> ";
    has cmd_reg: CommandRegistry;

    can init (cmd_reg: CommandRegistry) {
        <h>.cmd_reg = cmd_reg;
        <h> |> cmd.Cmd.__init__;
    }

    can do_exit(arg: list) -> bool {
        return True;
    }

    can default(line: str) {
        try {
            args = |> line.split |> <h>.cmd_reg.parser.parse_args |> vars;
            command = args["command"] |> <h>.cmd_reg.get;
            if command {
                args.pop("command");
                **args |> command.call |> print;
            }
        }
        except Exception as e {
            e |> print;
        }
    }


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

@command_registry.register
can foo(a: int = 4, b: str = "hello") -> str {
    return f"Foo result: {a}, {b}";
}


@command_registry.register
can bar(a: float = 4, b: int = 3, c: str = "hello") -> str {
    return f"Bar result: {a}, {b}, {c}";
}

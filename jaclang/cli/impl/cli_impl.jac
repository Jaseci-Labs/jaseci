"""Implemenation for Jac's command line interface."""

:o:Command:a:init(func: callable) {
    <h>.func = func;
    <h>.sig = func |> inspect.signature;
}

:o:Command:a:call(*args: list, **kwargs: dict) {
    return {*args, **kwargs} |> <h>.func;
}

:o:CommandRegistry:a:init {
    <h>.registry = {};
    <h>.parser = {prog="CLI"} |> argparse.ArgumentParser;
    <h>.sub_parsers = {title="commands", dest="command"}
        |> <h>.parser.add_subparsers;
}

:o:CommandRegistry:a:register(func: callable) {
    name = func.__name__;
    cmd = func |> Command;
    <h>.registry[name] = cmd;
    cmd_parser = name |> <h>.sub_parsers.add_parser;
    for param_name, param in |> cmd.sig.parameters.items {
        if param.default is param.empty {
            {f"-{param_name[:1]}", f"--{param_name}",
            required=True, type=param.annotation|>eval}
                |> cmd_parser.add_argument;
        }
        else {
            {f"-{param_name[:1]}", f"--{param_name}",
            default=param.default, type=param.annotation|>eval}
                |> cmd_parser.add_argument;
        }
    }
}

:o:CommandRegistry:a:get(name: str) -> Command {
    return name |> <h>.registry.get;
}

:o:CommandRegistry:a:items -> dict[str, Command] {
    return |> <h>.registry.items;
}


:o:CommandShell:a:init (cmd_reg: CommandRegistry) {
    <h>.cmd_reg = cmd_reg;
    <h> |> cmd.Cmd.__init__;
}

:o:CommandShell:a:do_exit(arg: list) -> bool {
    return True;
}

:o:CommandShell:a:default(line: str) {
    try {
        args = |> line.split |> <h>.cmd_reg.parser.parse_args |> vars;
        command = args["command"] |> <h>.cmd_reg.get;
        if command {
            args.pop("command");
            ret = **args |> command.call;
            if ret {
                ret |> print;
            }
        }
    }
    except Exception as e {
        e |> print;
    }
}

:a:start_cli {
    parser = cmd_registry.parser;
    args = |> parser.parse_args;
    command = args.command |> cmd_registry.get;
    if command {
        args = args |> vars;
        "command" |> args.pop;
        ret = **args |> command.call;
        if ret {
            ret |> print;
        }
    }
    else {
        shell = |> CommandShell(cmd_registry).cmdloop;
    }
}

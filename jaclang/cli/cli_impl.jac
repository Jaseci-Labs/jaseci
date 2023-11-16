"""Implemenation for Jac's command line interface."""

:o:Command:c:<init>(func: callable) {
    <s>.func = func;
    <s>.sig = func |> inspect.signature;
}

:o:Command:c:call(*args: list, **kwargs: dict) {
    return (*args, **kwargs) |> <s>.func;
}

:o:CommandRegistry:c:<init> {
    <s>.registry = {};
    <s>.parser = (prog="CLI") |> argparse.ArgumentParser;
    <s>.sub_parsers =
        (title="commands", dest="command") |> <s>.parser.add_subparsers;
}

:o:CommandRegistry:c:register(func: callable) {
    name = func.__name__;
    cmd = func |> Command;
    <s>.registry[name] = cmd;
    cmd_parser = name |> <s>.sub_parsers.add_parser;
    param_items = cmd.sig.parameters.items;
    first = True;
    for (param_name, param) in |> cmd.sig.parameters.items {
        if param_name == "args" {
            ('args', nargs=argparse.REMAINDER)
                |> cmd_parser.add_argument;
        }
        elif param.default is param.empty {
            if first {
                first = False;
                (f"{param_name}", <>type=param.annotation|>eval)
                    |> cmd_parser.add_argument;
            }
            else {
                (f"-{param_name[:1]}", f"--{param_name}",
                required=True, <>type=param.annotation|>eval)
                    |> cmd_parser.add_argument;
            }

        }
        else {
            if first {
                first = False;
                (f"{param_name}", default=param.default, <>type=param.annotation|>eval)
                    |> cmd_parser.add_argument;
            }
            else {
                (f"-{param_name[:1]}", f"--{param_name}",
                default=param.default, <>type=param.annotation|>eval)
                    |> cmd_parser.add_argument;
            }
        }
    }
    return func;
}

:o:CommandRegistry:c:get(name: str) -> Command {
    return name |> <s>.registry.get;
}

:o:CommandRegistry:c:items -> dict[str, Command] {
    return |> <s>.registry.items;
}


:o:CommandShell:c:<init>(cmd_reg: CommandRegistry) {
    <s>.cmd_reg = cmd_reg;
    <s> |> cmd.Cmd.<init>;
}

:o:CommandShell:c:do_exit(arg: list) -> bool {
    return True;
}

:o:CommandShell:c:default(line: str) {
    try {
        args = |> line.split |> <s>.cmd_reg.parser.parse_args |> vars;
        command = args["command"] |> <s>.cmd_reg.get;
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

:c:start_cli {
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

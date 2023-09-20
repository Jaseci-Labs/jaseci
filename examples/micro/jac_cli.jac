"""
This is the implementation of the command line interface tool for the
Jac languages. It's built with the Jac language V2 via bootstraping and
represents the first such production Jac program.
"""

import:py inspect;
import:py from argparse, ArgumentParser, ArgumentError;
import:py cmd;
import:py from typing, Any, Callable;


object Interface {
    has functions: list[callable] = [];

    can register(func: callable) -> callable;
    can create_parser -> ArgumentParser;
    can run_from_cli;
    can run_shell;
}

object ShellCmd:cmd.Cmd {
    has prompt: str = "> ",
        reg: Interface;

    can init(registry: Interface, *args: list, **kwargs: dict);
    can default(line: str);
    can do_quit(arg: str) -> bool;
}

with entry {
    interface = Interface();

    @interface.register
    can function_one(a: int, b: str, c: bool = False) {
        print(f"Function One -> a: {a}, b: {b}, c: {c}");
    }

    @interface.register
    can function_two(x: float, y: float) {
        print(f"Function Two -> x: {x}, y: {y}");
    }

    @interface.register
    can function_three(name: str, age: int, country: str = 'Unknown') {
        print(f"Function Three -> name: {name}, age: {age}, country: {country}");
    }

    # Run CLI or Shell mode
    # interface.run_from_cli()
    interface.run_shell();
}



#***Implementation***#

:object:Interface:ability:register
(func: callable) -> callable {
    <h>.functions.append(func);
    return func;
}

:object:Interface:ability:create_parser
() -> ArgumentParser {
    parser = ArgumentParser();
    parser.add_argument("base",
                        choices = [f.__name__ for f in functions],
                        help = "The function to run");

    for func in <h>.functions {
        sig = inspect.signature(func);
        for name, param in sig.parameters.items() {
            kwargs = {};
            if param.default == inspect.Parameter.empty {
                kwargs = {'required': True};
            } else {
                kwargs = {'default': param.default};
            }
            parser.add_argument(f"--{func.__name__}.{name}", **kwargs);
        }
    }

    return parser;
}

:object:Interface:ability:run_from_cli {
    parser = <h>.create_parser();
    args = parser.parse_args();
    for f in <h>.functions {
        if f.__name__ == args.base {
            func = f; break;
        }
    }
    func_args = {k.split('.')[1]: v for k, v in vars(args).items() if k.startswith(func.__name__)};
    func(**func_args);
}

:object:Interface:ability:run_shell {
    ShellCmd(<self>).cmdloop();
}

:object:ShellCmd:ability:init
(registry: Interface, *args: list, **kwargs: dict) {
    <h>.cmd.Cmd.__init__(*args, **kwargs);
    <h>.reg = registry;
}

:object:ShellCmd:ability:default
(line: str) {
    args = line.split();
    parser = <h>.reg.create_parser();
    try {
        parsed_args = parser.parse_args(args);
        for f in <h>.reg.functions {
            if f.__name__ == parsed_args.base {
                func = f; break;
            }
        }
        func_args = {k.split('.')[1]: v for k, v in vars(parsed_args).items()
                    if k.startswith(func.__name__)};
        func(**func_args);
    } except ArgumentError as e {
        print(f"Error: {str(e)}");
    }
}

:object:ShellCmd:ability:do_quit
(arg: str) -> bool {
    return True;
}

# type: ignore
# flake8: noqa
import argparse
import inspect
import cmd


class Command:
    def __init__(self, func):
        self.func = func
        self.sig: inspect.Signature = inspect.signature(func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class CommandRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, func):
        command = Command(func)
        self._registry[func.__name__] = command
        return command

    def get(self, name):
        return self._registry.get(name)

    def items(self):
        return self._registry.items()


command_registry = CommandRegistry()


@command_registry.register
def foo(a: int = 4, b: str = "hello") -> str:
    return f"Foo result: {a}, {b}"


@command_registry.register
def bar(a: float = 4, b: int = 3, c: str = "hello") -> str:
    return f"Bar result: {a}, {b}, {c}"


class ArgumentParserFactory:
    @staticmethod
    def create():
        parser = argparse.ArgumentParser(prog="CLI")
        subparsers = parser.add_subparsers(title="commands", dest="command")

        for name, command in command_registry.items():
            command_parser = subparsers.add_parser(name)
            for param_name, param in command.sig.parameters.items():
                if param.default is param.empty:
                    command_parser.add_argument(
                        f"--{param_name}", required=True, type=param.annotation
                    )
                else:
                    command_parser.add_argument(
                        f"--{param_name}", default=param.default, type=param.annotation
                    )

        return parser


class CommandShell(cmd.Cmd):
    intro = "Welcome to the shell. Type help or ? to list commands.\n"
    prompt = "(command) "

    def do_exit(self, arg):
        "Exit the shell."
        return True

    def default(self, line):
        try:
            args = vars(ArgumentParserFactory.create().parse_args(line.split()))
            command = command_registry.get(args["command"])
            if command:
                args.pop("command")
                result = command(**args)
                print(result)
        except Exception as e:
            print(str(e))


def main():
    parser = ArgumentParserFactory.create()
    args = parser.parse_args()
    command = command_registry.get(args.command)
    if command:
        kwargs = vars(args)
        kwargs.pop("command")
        result = command(**kwargs)
        print(result)
    else:
        CommandShell().cmdloop()


if __name__ == "__main__":
    main()

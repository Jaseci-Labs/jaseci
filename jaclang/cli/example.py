# flake8: noqa
import inspect
from argparse import ArgumentParser, ArgumentError
import cmd
from typing import Callable, List


class Interface:
    def __init__(self):
        self.functions: List[Callable] = []

    def register(self, func: Callable) -> Callable:
        self.functions.append(func)
        return func

    def create_parser(self) -> ArgumentParser:
        parser = ArgumentParser()
        parser.add_argument(
            "base",
            choices=[f.__name__ for f in self.functions],
            help="The function to run",
        )
        for func in self.functions:
            sig = inspect.signature(func)
            for name, param in sig.parameters.items():
                kwargs = {}
                if param.default == inspect.Parameter.empty:
                    kwargs = {"required": True}
                else:
                    kwargs = {"default": param.default}
                parser.add_argument(f"--{func.__name__}.{name}", **kwargs)
        return parser

    def run_from_cli(self):
        parser = self.create_parser()
        args = parser.parse_args()
        func = None
        for f in self.functions:
            if f.__name__ == args.base:
                func = f
                break
        if func is not None:
            func_args = {
                k.split(".")[1]: v
                for k, v in vars(args).items()
                if k.startswith(func.__name__)
            }
            func(**func_args)

    def run_shell(self):
        ShellCmd(self).cmdloop()


class ShellCmd(cmd.Cmd):
    def __init__(self, registry: Interface):
        super().__init__()
        self.prompt: str = "> "
        self.reg: Interface = registry

    def default(self, line: str):
        args = line.split()
        parser = self.reg.create_parser()
        try:
            parsed_args = parser.parse_args(args)
            func = None
            for f in self.reg.functions:
                if f.__name__ == parsed_args.base:
                    func = f
                    break
            if func is not None:
                func_args = {
                    k.split(".")[1]: v
                    for k, v in vars(parsed_args).items()
                    if k.startswith(func.__name__)
                }
                func(**func_args)
        except ArgumentError as e:
            print(f"Error: {str(e)}")

    def do_quit(self, arg: str) -> bool:
        return True


interface = Interface()


@interface.register
def function_one(a: int, b: str, c: bool = False):
    print(f"Function One -> a: {a}, b: {b}, c: {c}")


@interface.register
def function_two(x: float, y: float):
    print(f"Function Two -> x: {x}, y: {y}")


@interface.register
def function_three(name: str, age: int, country: str = "Unknown"):
    print(f"Function Three -> name: {name}, age: {age}, country: {country}")


interface.run_shell()

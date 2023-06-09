"""Utility functions and classes for Jac compilation toolchain."""
import re

from jaclang.jac.parser import JacLexer


def get_prism_highight_info() -> str:
    """Get prism highlight info from JacLexer."""
    ret = ""
    for k in JacLexer._remapping["NAME"].keys():
        ret += f"{k}|"
    return ret[:-1]


if __name__ == "__main__":
    print(get_prism_highight_info())


def pascal_to_snake(pascal_string: str) -> str:
    """Convert pascal case to snake case."""
    snake_string = re.sub(r"(?<!^)(?=[A-Z])", "_", pascal_string).lower()
    return snake_string

"""Utility functions and classes for Jac compilation toolchain."""
import re

from jaclang.jac.parser import JacLexer


def get_all_jac_keywords() -> str:
    """Get all Jac keywords as an or string."""
    ret = ""
    for k in JacLexer._remapping["NAME"].keys():
        ret += f"{k}|"
    return ret[:-1]


if __name__ == "__main__":
    print(get_all_jac_keywords())


def pascal_to_snake(pascal_string: str) -> str:
    """Convert pascal case to snake case."""
    snake_string = re.sub(r"(?<!^)(?=[A-Z])", "_", pascal_string).lower()
    return snake_string

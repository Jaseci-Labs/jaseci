"""Utility functions and classes for Jac compilation toolchain."""

from jaclang.jac.parser import JacLexer


def get_prism_highight_info() -> str:
    """Get prism highlight info from JacLexer."""
    ret = ""
    for k in JacLexer._remapping["NAME"].keys():
        ret += f"{k}|"
    return ret[:-1]


if __name__ == "__main__":
    print(get_prism_highight_info())

"""Math tools for the MTLLM project."""

from jaclang.compiler.semtable import SemInfo

from mtllm.types import Tool


def solve_math_expression(expr: str) -> float:
    """Solves the given math expression."""
    return eval(expr)


math_tool = Tool(
    solve_math_expression,
    SemInfo(
        None,
        "math_tool",
        "ability",
        "Solves the given math expression",
    ),
    [SemInfo(None, "expr", "str", "Math expression to solve eg- 2+2")],
)

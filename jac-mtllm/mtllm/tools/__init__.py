"""Pre-made tools for the mtllm package."""

from mtllm.semtable import SemInfo

from mtllm.types import Tool


def finish(output: str) -> str:
    """Finishes the prompt with the given output."""
    return output


finish_tool = Tool(
    finish,
    SemInfo(
        None,
        "finish_tool",
        "ability",
        "Finishes the Thought process by providing the output",
    ),
    [SemInfo(None, "output", "Any", "Final Output")],
)

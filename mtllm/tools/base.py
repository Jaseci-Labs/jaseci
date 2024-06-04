"""Tools for the MTLLM framework."""

from typing import Callable

import wikipedia as wikipedia_utils


class Tool:
    """Base class for tools."""

    description: str = "Description of the tool"
    inputs: list[tuple[str, str, str]] = [("input1", "str", "Input 1 description")]
    output: tuple[str, str] = ("str", "Output description")

    def forward(self, *args, **kwargs) -> str:  # noqa
        """Forward function of the tool."""
        raise NotImplementedError

    def get_function(self) -> Callable:
        """Return the forward function of the tool."""
        return self.forward


class wikipedia(Tool):  # noqa
    """Wikipedia tool."""

    description: str = "Get the summary of a Wikipedia article"
    inputs: list[tuple[str, str, str]] = [
        ("title", "str", "Title of the Wikipedia article")
    ]
    output: tuple[str, str] = ("str", "Summary of the Wikipedia article")

    def forward(self, title: str) -> str:
        """Get the summary of a Wikipedia article."""
        return wikipedia_utils.summary(title)

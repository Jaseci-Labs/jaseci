"""LLM implementations for MTLLM."""

import re

from .anthropic import (
    Anthropic,
    PROMPT_TEMPLATE,
    WITHOUT_REASON_SUFFIX,
    WITH_REASON_SUFFIX,
)
from .groq import Groq
from .huggingface import Huggingface
from .ollama import Ollama


class BaseLLM:
    """Base Large Language Model (LLM) class."""

    MTLLM_PROMPT: str = PROMPT_TEMPLATE
    MTLLM_REASON_SUFFIX: str = WITH_REASON_SUFFIX
    MTLLM_WO_REASON_SUFFIX: str = WITHOUT_REASON_SUFFIX

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the Large Language Model (LLM) client."""
        raise NotImplementedError

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        raise NotImplementedError

    def __call__(self, input_text: str, **kwargs: dict) -> str:
        """Infer a response from the input text."""
        return self.__infer__(input_text, **kwargs)

    def resolve_output(self, meaning_out: str, did_reason: bool) -> dict:
        """Resolve the output string to return the reasoning and output."""
        reasoning_match = (
            re.search(r"\[Reasoning\](.*)\[Output\]", meaning_out)
            if did_reason
            else None
        )
        output_match = re.search(r"\[Output\](.*)", meaning_out)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else None
        output = output_match.group(1).strip() if output_match else None
        return {"reasoning": reasoning, "output": output}


__all__ = ["Anthropic", "Ollama", "Huggingface", "Groq", "BaseLLM"]

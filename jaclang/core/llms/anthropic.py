"""Anthropic API client for MTLLM."""

import re

PROMPT_TEMPLATE = """
[System Prompt]
This is an operation you must perform and return the output values. Neither, the methodology, extra sentences nor the code are not needed.
Input/Type formatting: Explanation of the Input (variable_name) (type) = value

[Information]
{information}

[Context]
{context}

[Inputs Information]
{inputs_information}

[Output Information]
{output_information}

[Type Explanations]
{type_explanations}

[Action]
{action}

{reason_suffix}
"""  # noqa E501

WITH_REASON_SUFFIX = """
Reason and return the output result(s) only, adhering to the provided Type in the following format

[Reasoning] <Reason>
[Output] <Result>
"""

WITHOUT_REASON_SUFFIX = """Generate and return the output result(s) only, adhering to the provided Type in the following format

[Output] <result>
"""  # noqa E501


class Anthropic:
    """Anthropic API client for MTLLM."""

    MTLLM_PROMPT: str = PROMPT_TEMPLATE
    MTLLM_REASON_SUFFIX: str = WITH_REASON_SUFFIX
    MTLLM_WO_REASON_SUFFIX: str = WITHOUT_REASON_SUFFIX

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the Anthropic API client."""
        import anthropic  # type: ignore

        self.client = anthropic.Anthropic()
        self.model_name = kwargs.get("model_name", "claude-3-sonnet-20240229")
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 1024)

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        messages = [{"role": "user", "content": meaning_in}]
        output = self.client.messages.create(
            model=kwargs.get("model_name", self.model_name),
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            messages=messages,
        )
        return output.content[0].text

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

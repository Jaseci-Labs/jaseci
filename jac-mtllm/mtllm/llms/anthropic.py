"""Anthropic API client for MTLLM."""

from mtllm.llms.base import BaseLLM


REASON_SUFFIX = """
Reason and return the output result(s) only, adhering to the provided Type in the following format

[Reasoning] <Reason>
[Output] <Result>
"""

NORMAL_SUFFIX = """Generate and return the output result(s) only, adhering to the provided Type in the following format

[Output] <result>
"""  # noqa E501

CHAIN_OF_THOUGHT_SUFFIX = """
Generate and return the output result(s) only, adhering to the provided Type in the following format. Perform the operation in a chain of thoughts.(Think Step by Step)

[Chain of Thoughts] <Chain of Thoughts>
[Output] <Result>
"""  # noqa E501

REACT_SUFFIX = """
You are given with a list of tools you can use to do different things. To achieve the given [Action], incrementally think and provide tool_usage necessary to achieve what is thought.
Provide your answer adhering in the following format. tool_usage is a function call with the necessary arguments. Only provide one [THOUGHT] and [TOOL USAGE] at a time.

[Thought] <Thought>
[Tool Usage] <tool_usage>
"""  # noqa E501


class Anthropic(BaseLLM):
    """Anthropic API client for MTLLM."""

    MTLLM_METHOD_PROMPTS: dict[str, str] = {
        "Normal": NORMAL_SUFFIX,
        "Reason": REASON_SUFFIX,
        "Chain-of-Thoughts": CHAIN_OF_THOUGHT_SUFFIX,
        "ReAct": REACT_SUFFIX,
    }

    def __init__(
        self,
        verbose: bool = False,
        max_tries: int = 10,
        type_check: bool = False,
        **kwargs: dict,
    ) -> None:
        """Initialize the Anthropic API client."""
        import anthropic  # type: ignore

        super().__init__(verbose, max_tries, type_check)
        self.client = anthropic.Anthropic()
        self.model_name = str(kwargs.get("model_name", "claude-3-sonnet-20240229"))
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 1024)

    def __infer__(self, meaning_in: str | list[dict], **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        if not isinstance(meaning_in, str):
            assert self.model_name.startswith(
                ("claude-3-opus", "claude-3-sonnet", "claude-3-haiku")
            ), f"Model {self.model_name} is not multimodal, use a multimodal model instead."

            import re

            formatted_meaning_in = []
            for item in meaning_in:
                if item["type"] == "image_url":
                    # item["source"] = "data:image/jpeg;base64,base64_string"
                    img_match = re.match(
                        r"data:(image/[a-zA-Z]*);base64,(.*)", item["source"]
                    )
                    if img_match:
                        media_type, base64_string = img_match.groups()
                    formatted_meaning_in.append(
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64_string,
                            },
                        }
                    )
                    continue
                formatted_meaning_in.append(item)
            meaning_in = formatted_meaning_in
        messages = [{"role": "user", "content": meaning_in}]
        output = self.client.messages.create(
            model=kwargs.get("model_name", self.model_name),
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            messages=messages,
        )
        return output.content[0].text

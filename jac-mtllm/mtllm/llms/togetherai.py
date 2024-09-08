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


class TogetherAI(BaseLLM):
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
        **kwargs: dict
    ) -> None:
        """Initialize the Anthropic API client."""
        import together  # type: ignore

        super().__init__(verbose, max_tries, type_check)
        self.client = together.Together()
        self.model_name = kwargs.get("model_name", "mistralai/Mistral-7B-Instruct-v0.3")
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 1024)

    def __infer__(self, meaning_in: str | list[dict], **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        assert isinstance(
            meaning_in, str
        ), "Currently Multimodal models are not supported. Please provide a string input."
        messages = [{"role": "user", "content": meaning_in}]
        output = self.client.chat.completions.create(
            model=kwargs.get("model_name", self.model_name),
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            messages=messages,
        )
        return output.choices[0].message.content

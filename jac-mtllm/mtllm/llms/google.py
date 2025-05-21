"""Gemini API client for MTLLM."""

from mtllm.llms.base import BaseLLM


REASON_SUFFIX = """
Reason and return the output result(s) only, adhering to the provided Type in the following format.

[Reasoning] <Reason>
[Output] <result>
"""

NORMAL_SUFFIX = """Generate and return the output result(s) only, adhering to the provided Type in the following format without using markdown formatting.

[Output] <results>
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


class Gemini(BaseLLM):
    """Google API client for MTLLM."""

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
        """Initialize the Google API client."""
        from google import genai  # type: ignore
        import os  # type: ignore

        super().__init__(verbose, max_tries, type_check)
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.model_name = str(kwargs.get("model_name", "gemini-1.5-flash"))
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 1024)

    def __infer__(self, meaning_in: str | list[dict], **kwargs: dict) -> str:
        """Infer the output from the input meaning."""
        if not isinstance(meaning_in, str):
            assert self.model_name.startswith(
                ("gemini-1.0", "aqa, text")
            ), f"Model {self.model_name} does not support input of type {type(meaning_in)}. Choose a Multi-Modal model."
        # messages = [{"role": "user", "content": meaning_in}]
        # messages = 'What is the earth\'s circumference'
        config = {
            "temperature": kwargs.get("temperature", self.temperature),
            # "max_tokens": kwargs.get("max_tokens", self.max_tokens),
        }
        output = self.client.models.generate_content(
            model=kwargs.get("model_name", self.model_name),
            contents=meaning_in,
            config=config,
        )
        return output.text

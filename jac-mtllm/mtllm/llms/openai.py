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


class OpenAI(BaseLLM):
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
        import openai  # type: ignore

        super().__init__(verbose, max_tries, type_check)
        self.client = openai.OpenAI()
        self.model_name = str(kwargs.get("model_name", "gpt-4o-mini"))
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 1024)

    def __infer__(self, meaning_in: str | list[dict], **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        if not isinstance(meaning_in, str):
            assert self.model_name.startswith(
                ("gpt-4o", "gpt-4-turbo")
            ), f"Model {self.model_name} is not multimodal, use a multimodal model instead."
        messages = [{"role": "user", "content": meaning_in}]
        output = self.client.chat.completions.create(
            model=kwargs.get("model_name", self.model_name),
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            messages=messages,
        )
        return output.choices[0].message.content


COMPLETION_REASON_SUFFIX = """
Reason and return the output result(s) only, adhering to the provided Type in the following format

[Reasoning] <Reason>
[Output] <Result>

---

[Reasoning] """

COMPLETION_NORMAL_SUFFIX = """Generate and return the output result(s) only, adhering to the provided Type in the following format

[Output] <result>

---

[Output] """  # noqa E501

COMPLETION_CHAIN_OF_THOUGHT_SUFFIX = """
Generate and return the output result(s) only, adhering to the provided Type in the following format. Perform the operation in a chain of thoughts.(Think Step by Step)

[Chain of Thoughts] <Chain of Thoughts>
[Output] <Result>

---

[Chain of Thoughts] Lets Think Step by Step,
1. """  # noqa E501

COMPLETION_REACT_SUFFIX = """
"""  # noqa E501


class OpenAICompletion(OpenAI):
    """OpenAI Completion API client for MTLLM."""

    MTLLM_METHOD_PROMPTS: dict[str, str] = {
        "Normal": COMPLETION_NORMAL_SUFFIX,
        "Reason": COMPLETION_REASON_SUFFIX,
        "Chain-of-Thoughts": COMPLETION_CHAIN_OF_THOUGHT_SUFFIX,
        "ReAct": COMPLETION_REACT_SUFFIX,
    }

    def __infer__(self, meaning_in: str | list[dict], **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        assert "instruct" in self.model_name or self.model_name in [
            "babbage-002",
            "davinci-002",
        ], f"Model {self.model_name} is not a instruction model. Please use an instruction model."
        assert isinstance(
            meaning_in, str
        ), "Completion models are not supported with multimodal inputs. Please provide a string input."

        model_params = {
            k: v
            for k, v in kwargs.items()
            if k not in ["model_name", "temperature", "max_tokens"]
        }
        model_output = self.client.completions.create(
            model=kwargs.get("model_name", self.model_name),
            prompt=meaning_in,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            **model_params,
        )
        output = model_output.choices[0].text.strip()
        output = f"[Output] {output}" if "[Output]" not in output else output
        return output

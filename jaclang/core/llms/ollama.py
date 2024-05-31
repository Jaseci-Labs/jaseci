"""Ollama client for MTLLM."""

from .base import BaseLLM

REASON_SUFFIX = """
Reason and return the output results(s) only such that <Output> should be eval(<Output>) Compatible and reflects the
expected output type, Follow the format below to provide the reasoning for the output result(s).

[Reasoning] <Reasoning>
[Output] <Output>
"""

NORMAL_SUFFIX = """Return the output result(s) only such that <Output> should be eval(<Output>) Compatible and
reflects the expected output type, Follow the format below to provide the output result(s).

[Output] <Output>
"""  # noqa E501

CHAIN_OF_THOUGHT_SUFFIX = """
Generate and return the output result(s) only, adhering to the provided Type in the following format. Perform the operation in a chain of thoughts.(Think Step by Step)

[Chain of Thoughts] <Chain of Thoughts>
[Output] <Result>
"""  # noqa E501

REACT_SUFFIX = """
"""  # noqa E501


class Ollama(BaseLLM):
    """Ollama API client for Large Language Models (LLMs)."""

    MTLLM_METHOD_PROMPTS: dict[str, str] = {
        "Normal": NORMAL_SUFFIX,
        "Reason": REASON_SUFFIX,
        "Chain-of-Thoughts": CHAIN_OF_THOUGHT_SUFFIX,
        "ReAct": REACT_SUFFIX,
    }

    def __init__(
        self, verbose: bool = False, max_tries: int = 10, **kwargs: dict
    ) -> None:
        """Initialize the Ollama API client."""
        import ollama  # type: ignore

        self.client = ollama.Client(host=kwargs.get("host", "http://localhost:11434"))
        self.verbose = verbose
        self.max_tries = max_tries
        self.model_name = kwargs.get("model_name", "phi3")
        self.default_model_params = {
            k: v for k, v in kwargs.items() if k not in ["model_name", "host"]
        }

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        model = str(kwargs.get("model_name", self.model_name))
        if not self.check_model(model):
            self.download_model(model)
        model_params = {k: v for k, v in kwargs.items() if k not in ["model_name"]}
        messages = [{"role": "user", "content": meaning_in}]
        output = self.client.chat(
            model=model,
            messages=messages,
            options={**self.default_model_params, **model_params},
        )
        return output["message"]["content"]

    def check_model(self, model_name: str) -> bool:
        """Check if the model is available."""
        try:
            self.client.show(model_name)
            return True
        except Exception:
            return False

    def download_model(self, model_name: str) -> None:
        """Download the model."""
        self.client.pull(model_name)

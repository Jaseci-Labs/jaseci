"""Ollama client for MTLLM."""

from .base import BaseLLM
from .utils import logger

PROMPT_TEMPLATE = """
[System Prompt]
This is an operation you must perform and return the output values. Neither, the methodology, extra sentences nor the
code are not needed.
Input/Type formatting: Explanation of the Input (variable_name) (type) = value

[Type Explanations]
{type_explanations}

[Information]
{information}

[Context]
{context}

[Inputs Information]
{inputs_information}

[Output Information]
{output_information}

[Action]
{action}

{reason_suffix}
"""  # noqa E501

WITH_REASON_SUFFIX = """
Reason and return the output results(s) only such that <Output> should be eval(<Output>) Compatible and reflects the
expected output type, Follow the format below to provide the reasoning for the output result(s).

[Reasoning] <Reasoning>
[Output] <Output>
"""

WITHOUT_REASON_SUFFIX = """Return the output result(s) only such that <Output> should be eval(<Output>) Compatible and
reflects the expected output type, Follow the format below to provide the output result(s).

[Output] <Output>
"""  # noqa E501


class Ollama(BaseLLM):
    """Ollama API client for Large Language Models (LLMs)."""

    MTLLM_PROMPT: str = PROMPT_TEMPLATE
    MTLLM_REASON_SUFFIX: str = WITH_REASON_SUFFIX
    MTLLM_WO_REASON_SUFFIX: str = WITHOUT_REASON_SUFFIX

    def __init__(self, verbose: bool = False, **kwargs: dict) -> None:
        """Initialize the Ollama API client."""
        import ollama  # type: ignore

        self.client = ollama.Client(host=kwargs.get("host", "http://localhost:11434"))
        self.verbose = verbose
        self.model_name = kwargs.get("model_name", "phi3")
        self.default_model_params = {
            k: v for k, v in kwargs.items() if k not in ["model_name", "host"]
        }

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        if self.verbose:
            logger.info(f"Meaning In\n{meaning_in}")
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

    def __call__(self, input_text: str, **kwargs: dict) -> str:
        """Infer a response from the input text."""
        return self.__infer__(input_text, **kwargs)

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

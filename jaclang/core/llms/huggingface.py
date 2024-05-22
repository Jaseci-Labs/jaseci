"""Huggingface client for MTLLM."""

import re

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


class Huggingface:
    """Huggingface API client for Large Language Models (LLMs)."""

    MTLLM_PROMPT: str = PROMPT_TEMPLATE
    MTLLM_REASON_SUFFIX: str = WITH_REASON_SUFFIX
    MTLLM_WO_REASON_SUFFIX: str = WITHOUT_REASON_SUFFIX

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the Huggingface API client."""
        import torch  # type: ignore
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline  # type: ignore

        torch.random.manual_seed(0)
        model = AutoModelForCausalLM.from_pretrained(
            kwargs.get("model_name", "microsoft/Phi-3-mini-128k-instruct"),
            device_map=kwargs.get("device_map", "cuda"),
            torch_dtype="auto",
            trust_remote_code=True,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            kwargs.get("model_name", "microsoft/Phi-3-mini-128k-instruct")
        )
        self.pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_new_tokens", 1024)

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        messages = [{"role": "user", "content": meaning_in}]
        output = self.pipe(
            messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_length=kwargs.get("max_new_tokens", self.max_tokens),
            **kwargs
        )
        return output[0]["generated_text"][-1]["content"]

    def __call__(self, input_text: str, **kwargs: dict) -> str:
        """Infer a response from the input text."""
        return self.__infer__(input_text, **kwargs)

    def resolve_output(self, meaning_out: str, did_reason: bool) -> dict:
        """Resolve the output string to return the reasoning and output."""
        print(meaning_out)
        reasoning_match = (
            re.search(r"\[Reasoning\](.*)\[Output\]", meaning_out)
            if did_reason
            else None
        )
        output_match = re.search(r"\[Output\](.*)", meaning_out)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else None
        output = output_match.group(1).strip() if output_match else None
        if not output and not reasoning:
            output = meaning_out.strip()
        return {"reasoning": reasoning, "output": output}

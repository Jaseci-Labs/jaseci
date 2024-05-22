"""Groq API client for MTLLM."""

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

WITH_REASON_OUTPUT_FIX = """
[Output]
{model_output}

[Previous Result You Provided]
{previous_output}

[Error]
{error}

Provide the given Output as dict with "output" and "reasoning" keys. Such that the "output"'s value should be
eval("output"'s value) Compatible. Important: Only provide the dict object.
"""  # noqa E501

WITHOUT_REASON_OUTPUT_FIX = """
[Output]
{model_output}

[Previous Result You Provided]
{previous_output}

[Error]
{error}

Provide the given Output as dict with "output" key. Such that the "output"'s value should be
eval("output"'s value) Compatible. Important: Only provide the dict object.
"""  # noqa E501


class Groq:
    """Groq API client for MTLLM."""

    MTLLM_PROMPT: str = PROMPT_TEMPLATE
    MTLLM_REASON_SUFFIX: str = WITH_REASON_SUFFIX
    MTLLM_WO_REASON_SUFFIX: str = WITHOUT_REASON_SUFFIX

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the Groq API client."""
        import groq  # type: ignore

        self.client = groq.Groq()
        self.model_name = kwargs.get("model_name", "mixtral-8x7b-32768")
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 1024)

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        # print("Meaning In\n", meaning_in)
        messages = [{"role": "user", "content": meaning_in}]
        model_params = {
            k: v
            for k, v in kwargs.items()
            if k not in ["model_name", "temperature", "max_tokens"]
        }
        output = self.client.chat.completions.create(
            model=kwargs.get("model_name", self.model_name),
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            messages=messages,
            **model_params
        )
        return output.choices[0].message.content

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
        if not output_match:
            reasoning, output = self._extract_output(meaning_out, did_reason)
            return {"reasoning": reasoning, "output": output}
        return {"reasoning": reasoning, "output": output}

    def _extract_output(
        self,
        meaning_out: str,
        did_reason: bool,
        previous_output: str = "None",
        error: str = "None",
        max_tries: int = 10,
    ) -> tuple[str, str]:
        """Extract the output from the meaning out string."""
        if max_tries == 0:
            raise ValueError(
                "Failed to extract output. Try Changing the Semstrings and provide examples."
            )
        output_fix_prompt_template = (
            WITH_REASON_OUTPUT_FIX if did_reason else WITHOUT_REASON_OUTPUT_FIX
        )
        output_fix_prompt = output_fix_prompt_template.format(
            model_output=meaning_out, previous_output=previous_output, error=error
        )
        llm_output = self.__infer__(output_fix_prompt)
        try:
            eval_output = eval(llm_output)
            return eval_output.get("reasoning", ""), eval_output["output"]
        except Exception as e:
            return self._extract_output(
                meaning_out, did_reason, llm_output, str(e), max_tries - 1
            )

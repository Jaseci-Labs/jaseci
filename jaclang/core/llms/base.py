"""Base Large Language Model (LLM) class."""

import re

from .utils import logger


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


class BaseLLM:
    """Base Large Language Model (LLM) class."""

    MTLLM_PROMPT: str = PROMPT_TEMPLATE
    MTLLM_REASON_SUFFIX: str = WITH_REASON_SUFFIX
    MTLLM_WO_REASON_SUFFIX: str = WITHOUT_REASON_SUFFIX

    def __init__(self, verbose: bool = False, **kwargs: dict) -> None:
        """Initialize the Large Language Model (LLM) client."""
        self.verbose = verbose
        raise NotImplementedError

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        if self.verbose:
            logger.info(f"Meaning In\n{meaning_in}")
        raise NotImplementedError

    def __call__(self, input_text: str, **kwargs: dict) -> str:
        """Infer a response from the input text."""
        return self.__infer__(input_text, **kwargs)

    def resolve_output(self, meaning_out: str, did_reason: bool) -> dict:
        """Resolve the output string to return the reasoning and output."""
        if self.verbose:
            logger.info(f"Meaning Out\n{meaning_out}")
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
            logger.error("Failed to extract output. Max tries reached.")
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
        if self.verbose:
            if error != "None":
                logger.info(
                    f"Ran into an error: {error}. Trying to extract output again. Max tries left: {max_tries}"
                )
            else:
                logger.info(
                    f"Trying to extract output again. Max tries left: {max_tries}"
                )
        try:
            eval_output = eval(llm_output)
            return eval_output.get("reasoning", ""), eval_output["output"]
        except Exception as e:
            if self.verbose:
                logger.error(
                    f"Failed to extract output. Error: {e}. Trying again. Given Output: {llm_output}"
                )
            return self._extract_output(
                meaning_out, did_reason, llm_output, str(e), max_tries - 1
            )

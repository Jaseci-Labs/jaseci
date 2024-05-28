"""Base Large Language Model (LLM) class."""

import re

from .utils import logger

SYSTEM_PROMPT = """
[System Prompt]
This is an operation you must perform and return the output values. Neither, the methodology, extra sentences nor the code are not needed.
Input/Type formatting: Explanation of the Input (variable_name) (type) = value
"""  # noqa E501


PROMPT_TEMPLATE = """
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
"""  # noqa E501

NORMAL_SUFFIX = """Generate and return the output result(s) only, adhering to the provided Type in the following format

[Output] <result>
"""  # noqa E501

REASON_SUFFIX = """
Reason and return the output result(s) only, adhering to the provided Type in the following format

[Reasoning] <Reason>
[Output] <Result>
"""

CHAIN_OF_THOUGHT_SUFFIX = """
Generate and return the output result(s) only, adhering to the provided Type in the following format. Perform the operation in a chain of thoughts.(Think Step by Step)

[Chain of Thoughts] <Chain of Thoughts>
[Output] <Result>
"""  # noqa E501

REACT_SUFFIX = """
"""  # noqa E501

MTLLM_OUTPUT_FIX_PROMPT = """
[Output]
{model_output}

[Previous Result You Provided]
{previous_output}

[Desired Output Type]
{output_info}

[Type Explanations]
{output_type_info}

[Error Encountered]
{error}

Provide the given Output as dict with "output" key. Such that the "output"'s value is in the desired output type and should be
eval("output"'s value) Compatible. Important: Only provide the dict object. Do not include any other information.
"""  # noqa E501


class BaseLLM:
    """Base Large Language Model (LLM) class."""

    MTLLM_SYSTEM_PROMPT: str = SYSTEM_PROMPT
    MTLLM_PROMPT: str = PROMPT_TEMPLATE
    MTLLM_METHOD_PROMPTS: dict[str, str] = {
        "Normal": NORMAL_SUFFIX,
        "Reason": REASON_SUFFIX,
        "Chain-of-Thoughts": CHAIN_OF_THOUGHT_SUFFIX,
        "ReAct": REACT_SUFFIX,
    }
    OUTPUT_FIX_PROMPT: str = MTLLM_OUTPUT_FIX_PROMPT

    def __init__(
        self, verbose: bool = False, max_tries: int = 10, **kwargs: dict
    ) -> None:
        """Initialize the Large Language Model (LLM) client."""
        self.verbose = verbose
        self.max_tries = max_tries
        raise NotImplementedError

    def __infer__(self, meaning_in: str, **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        if self.verbose:
            logger.info(f"Meaning In\n{meaning_in}")
        raise NotImplementedError

    def __call__(self, input_text: str, **kwargs: dict) -> str:
        """Infer a response from the input text."""
        return self.__infer__(input_text, **kwargs)

    def resolve_output(
        self, meaning_out: str, output_info: str, output_type_info: str
    ) -> str:
        """Resolve the output string to return the reasoning and output."""
        output_match = re.search(r"\[Output\](.*)", meaning_out)
        output = output_match.group(1).strip() if output_match else None
        if not output_match:
            output = self._extract_output(
                meaning_out, output_info, output_type_info, self.max_tries
            )
        return output

    def _extract_output(
        self,
        meaning_out: str,
        output_info: str,
        output_type_info: str,
        max_tries: int,
        previous_output: str = "None",
        error: str = "None",
    ) -> str:
        """Extract the output from the meaning out string."""
        if max_tries == 0:
            logger.error("Failed to extract output. Max tries reached.")
            raise ValueError(
                "Failed to extract output. Try Changing the Semstrings and provide examples."
            )

        if self.verbose:
            if error != "None":
                logger.info(
                    f"Ran into an error: {error}. Trying to extract output again. Max tries left: {max_tries}"
                )
            else:
                logger.info(
                    f"Trying to extract output again. Max tries left: {max_tries}"
                )
        output_fix_prompt = self.OUTPUT_FIX_PROMPT.format(
            model_output=meaning_out,
            previous_output=previous_output,
            output_info=output_info,
            output_type_info=output_type_info,
            error=error,
        )
        llm_output = self.__infer__(output_fix_prompt)
        try:
            eval_output = eval(llm_output)
            return eval_output["output"]
        except Exception as e:
            if self.verbose:
                logger.error(
                    f"Failed to extract output. Error: {e}. Trying again. Given Output: {llm_output}"
                )
            return self._extract_output(
                meaning_out,
                output_info,
                output_type_info,
                max_tries - 1,
                llm_output,
                str(e),
            )

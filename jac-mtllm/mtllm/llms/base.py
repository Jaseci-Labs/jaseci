"""Base Large Language Model (LLM) class."""

import logging
import re
from typing import Any, Mapping, Optional

from loguru import logger

from mtllm.types import InputInformation, OutputHint, ReActOutput, TypeExplanation
from mtllm.utils import format_template_section


httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

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
You are given with a list of tools you can use to do different things. To achieve the given [Action], incrementally think and provide tool_usage necessary to achieve what is thought.
Provide your answer adhering in the following format. tool_usage is a function call with the necessary arguments. Only provide one [THOUGHT] and [TOOL USAGE] at a time.

[Thought] <Thought>
[Tool Usage] <tool_usage>
"""  # noqa E501

MTLLM_OUTPUT_EXTRACT_PROMPT = """
[Output]
{model_output}

[Previous Result You Provided]
{previous_output}

[Desired Output Type]
{output_info}

[Type Explanations]
{output_type_info}

Above output is not in the desired Output Format/Type. Please provide the output in the desired type. Do not repeat the previously provided output.
Important: Do not provide the code or the methodology. Only provide the output in the desired format.
"""  # noqa E501

OUTPUT_CHECK_PROMPT = """
[Output]
{model_output}

[Desired Output Type]
{output_type}

[Type Explanations]
{output_type_info}

Check if the output is exactly in the desired Output Type. Important: Just say 'Yes' or 'No'.
"""  # noqa E501

OUTPUT_FIX_PROMPT = """
[Previous Output]
{model_output}

[Desired Output Type]
{output_type}

[Type Explanations]
{output_type_info}

[Error]
{error}

Above output is not in the desired Output Format/Type. Please provide the output in the desired type. Do not repeat the previously provided output.
Important: Do not provide the code or the methodology. Only provide the output in the desired format.
"""  # noqa E501

REACT_OUTPUT_FIX_PROMPT = """
[Previous Output]
{model_output}

[Error]
{error}

[Tool Explanations]
{tool_explanations}

[Type Explanations]
{type_explanations}

Above output is not in the desired Output Format/Type. Please provide the output in the desired type. Do not repeat the previously provided output.
Provide the output in the below format. Where tool_usage is a function call with the necessary arguments. Only provide one [THOUGHT] and [TOOL USAGE] at a time.

[Thought] <Thought>
[Tool Usage] <tool_usage>
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
    OUTPUT_EXTRACT_PROMPT: str = MTLLM_OUTPUT_EXTRACT_PROMPT
    OUTPUT_CHECK_PROMPT: str = OUTPUT_CHECK_PROMPT
    OUTPUT_FIX_PROMPT: str = OUTPUT_FIX_PROMPT
    REACT_OUTPUT_FIX_PROMPT: str = REACT_OUTPUT_FIX_PROMPT

    def __init__(
        self, verbose: bool = False, max_tries: int = 10, type_check: bool = False
    ) -> None:
        """Initialize the Large Language Model (LLM) client."""
        self.verbose = verbose
        self.max_tries = max_tries
        self.type_check = type_check

    def __infer__(self, meaning_in: str | list[dict], **kwargs: dict) -> str:
        """Infer a response from the input meaning."""
        raise NotImplementedError

    def __call__(
        self,
        input_text: str | list[dict],
        media: list[Optional[InputInformation]],
        **kwargs: dict,
    ) -> str:
        """Infer a response from the input text."""
        if self.verbose:
            logger.info(f"Meaning In\n{input_text}")
        return self.__infer__(input_text, **kwargs)

    def resolve_output(
        self,
        meaning_out: str,
        output_hint: OutputHint,
        output_type_explanations: list[TypeExplanation],
        _globals: dict,
        _locals: Mapping,
    ) -> Any:  # noqa: ANN401
        """Resolve the output string to return the reasoning and output."""
        if self.verbose:
            logger.info(f"Meaning Out\n{meaning_out}")
            logger.info(f"Output Hint\n{output_hint.type}")
        primary_types = [
            "str",
            "int",
            "float",
            "bool",
            "list",
            "dict",
            "tuple",
            "set",
            "Any",
            "None",
        ]
        if re.search(r"\[Output\]", meaning_out, re.IGNORECASE):
            output_match = re.search(r"\[Output\](.*)", meaning_out, re.DOTALL)
            if output_match:
                output = output_match.group(1).strip()
        else:
            # if output_hint.type.startswith("(") and output_hint.type.endswith(")"):
            #     tuple_pattern = re.compile(r"\(\s*(.*?)\s*\)", re.DOTALL)
            #     tuple_match = tuple_pattern.search(meaning_out)
            #     if tuple_match:
            #         # extracted_tuple = f"({tuple_match.group(0).strip()})"
            #         output_match = tuple_match
            #     else:
            #         output_match = None
            #     if self.verbose:
            #         logger.info(f"Tuple Output: {output_match}")
            if output_hint.type.split("[")[0] in primary_types:
                primary_patterns = {
                    "int": r"[-+]?\d+",
                    "float": r"[-+]?\d*\.\d+",
                    "bool": r"True|False",
                    "str": r"'([^']*)'",
                    "list": r"\[.*?\]",
                    "dict": r"\{.*?\}",
                    "tuple": r"\(.*?\)",
                    "set": r"\{.*?\}",
                    "Any": r".+",
                    "None": r"None",
                }
                single_pattern = re.compile(
                    primary_patterns[output_hint.type.split("[")[0]], re.DOTALL
                )
                single_match = single_pattern.search(meaning_out)
                if not single_match and output_hint.type.split("[")[0] == "str":
                    meaning_out = meaning_out.rstrip()
                    single_match = re.match(r".*", meaning_out)
                output_match = single_match
                if self.verbose:
                    logger.info(f"Single Output: {single_match}")
            else:
                custom_type_pattern = re.compile(
                    rf"{output_hint.type}\s*\((.*)\)", re.DOTALL
                )

                custom_match = custom_type_pattern.search(meaning_out)
                if custom_match:
                    extracted_output = (
                        f"{output_hint.type}({custom_match.group(1).strip()})"
                    )
                    if self.verbose:
                        logger.info(f"Custom Type Output: {extracted_output}")
                    output_match = custom_match
                else:
                    output_match = None
            if output_match:
                output = output_match.group(0).strip()
        if not output_match:
            output = self._extract_output(
                meaning_out,
                output_hint,
                output_type_explanations,
                self.max_tries,
            )

        if self.type_check:
            is_in_desired_format = self._check_output(
                output, output_hint.type, output_type_explanations
            )
            if not is_in_desired_format:
                output = self._extract_output(
                    meaning_out,
                    output_hint,
                    output_type_explanations,
                    self.max_tries,
                    output,
                )

        return self.to_object(
            output, output_hint, output_type_explanations, _globals, _locals
        )

    def resolve_react_output(
        self,
        meaning_out: str,
        _globals: dict,
        _locals: Mapping,
        tool_explanations: str,
        type_explanations: str,
    ) -> ReActOutput:
        """Resolve the output string to return the reasoning and output."""
        if self.verbose:
            logger.info(f"Meaning Out\n{meaning_out}")
        try:
            thought_match = re.search(
                r"\[Thought\](.*)\[Tool Usage\]", meaning_out, re.DOTALL
            )
            tool_usage_match = re.search(r"\[Tool Usage\](.*)", meaning_out, re.DOTALL)
            if not thought_match or not tool_usage_match:
                raise ValueError("Failed to find Thought or Tool Usage in the output.")
            thought = thought_match.group(1).strip()
            tool_usage = tool_usage_match.group(1).strip()
            try:
                output = eval(tool_usage, _globals, _locals)
            except Exception as e:
                return ReActOutput(
                    thought=thought, action=tool_usage, observation=str(e)
                )
            return ReActOutput(thought=thought, action=tool_usage, observation=output)
        except Exception as e:
            print(e)
            new_meaning_out = self._fix_react_output(
                meaning_out, e, tool_explanations, type_explanations
            )
            return self.resolve_react_output(
                new_meaning_out, _globals, _locals, tool_explanations, type_explanations
            )

    def _fix_react_output(
        self,
        meaning_out: str,
        error: Exception,
        tool_explanations: str,
        type_explanations: str,
    ) -> str:
        """Fix the output string."""
        if self.verbose:
            logger.info(f"Error: {error}, Fixing the output.")
        react_output_fix_values = {
            "model_output": meaning_out,
            "error": str(error),
            "tool_explanations": tool_explanations,
            "type_explanations": type_explanations,
        }
        react_output_fix_prompt = format_template_section(
            self.REACT_OUTPUT_FIX_PROMPT, react_output_fix_values
        )
        return self.__infer__(react_output_fix_prompt)

    def _check_output(
        self,
        output: str,
        output_type: str,
        output_type_explanations: list[TypeExplanation],
    ) -> bool:
        """Check if the output is in the desired format."""
        react_values = {
            "model_output": output,
            "output_type": output_type,
            "output_type_info": "\n".join(
                [str(info) for info in output_type_explanations]
            ),
        }
        output_check_prompt = format_template_section(
            self.OUTPUT_CHECK_PROMPT, react_values
        )
        llm_output = self.__infer__(output_check_prompt)
        return "yes" in llm_output.lower()

    def _extract_output(
        self,
        meaning_out: str,
        output_hint: OutputHint,
        output_type_explanations: list[TypeExplanation],
        max_tries: int,
        previous_output: str = "None",
    ) -> str:
        """Extract the output from the meaning out string."""
        if max_tries == 0:
            logger.error("Failed to extract output. Max tries reached.")
            raise ValueError(
                "Failed to extract output. Try Changing the Semstrings, provide examples or change the method."
            )

        if self.verbose:
            if max_tries < self.max_tries:
                logger.info(
                    f"Failed to extract output. Trying to extract output again. Max tries left: {max_tries}"
                )
            else:
                logger.info("Extracting output from the meaning out string.")
        output_check_values = {
            "model_output": meaning_out,
            "previous_output": previous_output,
            "output_info": str(output_hint),
            "output_type_info": "\n".join(
                [str(info) for info in output_type_explanations]
            ),
        }
        output_extract_prompt = format_template_section(
            self.OUTPUT_EXTRACT_PROMPT, output_check_values
        )
        llm_output = self.__infer__(output_extract_prompt)
        is_in_desired_format = self._check_output(
            llm_output, output_hint.type, output_type_explanations
        )
        if self.verbose:
            logger.info(
                f"Extracted Output: {llm_output}. Is in Desired Format: {is_in_desired_format}"
            )
        if is_in_desired_format:
            return llm_output
        return self._extract_output(
            meaning_out,
            output_hint,
            output_type_explanations,
            max_tries - 1,
            llm_output,
        )

    def to_object(
        self,
        output: str,
        output_hint: OutputHint,
        output_type_explanations: list[TypeExplanation],
        _globals: dict,
        _locals: Mapping,
        error: Optional[Exception] = None,
        num_retries: int = 0,
    ) -> Any:  # noqa: ANN401
        """Convert the output string to an object."""
        if num_retries >= self.max_tries:
            raise ValueError("Failed to convert output to object. Max tries reached.")
        if output_hint.type == "str":
            return output
        if error:
            fixed_output = self._fix_output(
                output, output_hint, output_type_explanations, error
            )
            return self.to_object(
                fixed_output,
                output_hint,
                output_type_explanations,
                _globals,
                _locals,
                num_retries=num_retries + 1,
            )

        try:
            return eval(output, _globals, _locals)
        except Exception as e:
            return self.to_object(
                output,
                output_hint,
                output_type_explanations,
                _globals,
                _locals,
                error=e,
                num_retries=num_retries + 1,
            )

    def _fix_output(
        self,
        output: str,
        output_hint: OutputHint,
        output_type_explanations: list[TypeExplanation],
        error: Exception,
    ) -> str:
        """Fix the output string."""
        if self.verbose:
            logger.info(f"Error: {error}, Fixing the output.")
        output_fix_values = {
            "model_output": output,
            "output_type": output_hint.type,
            "output_type_info": "\n".join(
                [str(info) for info in output_type_explanations]
            ),
            "error": str(error),
        }
        output_fix_prompt = format_template_section(
            self.OUTPUT_FIX_PROMPT, output_fix_values
        )
        return self.__infer__(output_fix_prompt)

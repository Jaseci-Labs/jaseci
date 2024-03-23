"""
AOTT: Automated Operational Type Transformation.

This has all the necessary functions to perform the AOTT operations.
"""

import re
from typing import Any


def get_reasoning_output(s: str) -> tuple:
    """Get the reasoning and output from the meaning out string."""
    reasoning_match = re.search(r"\[Reasoning\](.*)\[Output\]", s)
    output_match = re.search(r"\[Output\](.*)", s)

    if reasoning_match and output_match:
        reasoning = reasoning_match.group(1)
        output = output_match.group(1)
        return (reasoning.strip(), output.strip())
    elif output_match:
        output = output_match.group(1)
        return (None, output.strip())
    else:
        return (None, None)


prompt_template = """
[System Prompt]
This is an operation you must perform and return the output values. Neither, the methodology, extra sentences nor the code are not needed.
Input/Type formatting: Explanation of the Input (variable_name) (type) = value

[Information]
{information}

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

with_reason_suffix = """
Reason and return the output result(s) only, adhering to the provided Type in the following format

[Reasoning] <Reason>
[Output] <Result>
"""

without_reason_suffix = """Generate and return the output result(s) only, adhering to the provided Type in the following format

[Output] <result>
"""  # noqa E501


def aott_raise(
    information: str,
    inputs_information: str,
    output_information: str,
    type_explanations: str,
    action: str,
    reason: bool,
) -> str:
    """AOTT Raise uses the information (Meanings types values) provided to generate a prompt(meaning in)."""
    return prompt_template.format(
        information=information,
        inputs_information=inputs_information,
        output_information=output_information,
        type_explanations=type_explanations,
        action=action,
        reason_suffix=with_reason_suffix if reason else without_reason_suffix,
    )


def aott_lower(meaning_out: str) -> Any:  # noqa: ANN401
    """AOTT Lower uses the meaning out provided by the language model and return the result in the desired type."""
    reasoning, output = get_reasoning_output(meaning_out)
    try:
        return (reasoning, eval(output))
    except Exception as e:
        print(e)
        return (reasoning, output)

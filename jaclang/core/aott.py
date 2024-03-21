"""
AOTT: Automated Operational Type Transformation.

This has all the necessary functions to perform the AOTT operations.
"""

from typing import Any


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
"""

with_reason_suffix = """
Reason and return the output result(s) only, adhering to the provided Type in the following format

[Reasoning] <Reason>
[Output] <Result>
"""

without_reason_suffix = """Generate and return the output result(s) only, adhering to the provided Type in the following format

[Output] <result>
"""


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


def aott_lower(meaning_out: str, output_type_info: tuple) -> Any:  # noqa: ANN401
    """AOTT Lower uses the meaning out provided by the language model and return the result in the desired type."""
    return meaning_out

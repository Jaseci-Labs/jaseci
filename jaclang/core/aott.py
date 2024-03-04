"""
AOTT: Automated Operational Type Transformation.

This has all the necessary functions to perform the AOTT operations.
"""

from typing import Any


prompt_template = """
[System Prompt]
This is an operation you must perform and return the output values. Neither, the methodology,
extra sentences nor the code are not needed.

[Information]
{information_str}

[Inputs and Input Type Information]
{input_types_n_information_str}

[Output Type]
{output_type_str}

[Output Type Explanations]
{output_type_info_str}

[Action]
{action}

{reason_suffix}
"""

with_reason_suffix = """
Reason and return the output result(s) only, adhering to the provided Type in the following format

[Reasoning] <Reason>
[Output] <Result>
"""

without_reason_suffix = """Generate and return the output result(s) only, adhering to the provided Type in the
 following format

[Output] <result>
"""


def aott_raise(
    information_str: str,
    input_types_n_information_str: str,
    output_type_str: str,
    output_type_info_str: str,
    action: str,
    reason: bool,
) -> str:
    """AOTT Raise uses the information (Meanings types values) provided to generate a prompt(meaning in)."""
    return prompt_template.format(
        information_str=information_str,
        input_types_n_information_str=input_types_n_information_str,
        output_type_str=output_type_str,
        output_type_info_str=output_type_info_str,
        action=action,
        reason_suffix=with_reason_suffix if reason else without_reason_suffix,
    )


def aott_lower(meaning_out: str, output_type_info: tuple) -> Any:  # noqa: ANN401
    """AOTT Lower uses the meaning out provided by the language model and return the result in the desired type."""
    return meaning_out

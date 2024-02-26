from typing import Any

prompt_template = """
[System Prompt]
This is an operation you must perform and return the output values. Neither, the methodology, extra sentences nor the code are not needed. 

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

without_reason_suffix = """
Generate and return the output result(s) only, adhering to the provided Type in the following format

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
    return prompt_template.format(
        information_str=information_str,
        input_types_n_information_str=input_types_n_information_str,
        output_type_str=output_type_str,
        output_type_info_str=output_type_info_str,
        action=action,
        reason_suffix=with_reason_suffix if reason else without_reason_suffix,
    )

def aott_lower(meaning_out:str, output_type_info: tuple) -> Any:
    return meaning_out
"""
AOTT: Automated Operational Type Transformation.

This has all the necessary functions to perform the AOTT operations.
"""

import re
from enum import Enum
from typing import Any

from jaclang.core.registry import SemInfo, SemRegistry, SemScope


PROMPT_TEMPLATE = """
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

WITH_REASON_SUFFIX = """
Reason and return the output result(s) only, adhering to the provided Type in the following format

[Reasoning] <Reason>
[Output] <Result>
"""

WITHOUT_REASON_SUFFIX = """Generate and return the output result(s) only, adhering to the provided Type in the following format

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
    return PROMPT_TEMPLATE.format(
        information=information,
        inputs_information=inputs_information,
        output_information=output_information,
        type_explanations=type_explanations,
        action=action,
        reason_suffix=WITH_REASON_SUFFIX if reason else WITHOUT_REASON_SUFFIX,
    )


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


def get_info_types(
    scope: SemScope, mod_registry: SemRegistry, incl_info: list[tuple[str, str]]
) -> tuple[str, list[str]]:
    """Filter the registry data based on the scope and return the info string."""
    collected_types = []
    avail_scopes = []
    while True:
        avail_scopes.append(str(scope))
        if not scope.parent:
            break
        scope = scope.parent

    filtered_registry = SemRegistry()
    for _scope, sem_info_list in mod_registry.registry.items():
        if str(_scope) in avail_scopes:
            filtered_registry.registry[_scope] = sem_info_list

    info_str = []
    for incl in incl_info:
        _, sem_info = filtered_registry.lookup(name=incl[0])
        if sem_info and isinstance(sem_info, SemInfo):
            (
                collected_types.extend(extract_non_primary_type(sem_info.type))
                if sem_info.type
                else None
            )
            info_str.append(
                f"{sem_info.semstr} ({sem_info.name}) ({sem_info.type}) = {get_object_string(incl[1])}"
            )
    return ("\n".join(info_str), collected_types)


def get_object_string(obj: Any) -> Any:  # noqa: ANN401
    """Get the string representation of the input object."""
    if isinstance(obj, str):
        return f'"{obj}"'
    elif isinstance(obj, (int, float, bool)):
        return str(obj)
    elif isinstance(obj, list):
        return "[" + ", ".join(get_object_string(item) for item in obj) + "]"
    elif isinstance(obj, tuple):
        return "(" + ", ".join(get_object_string(item) for item in obj) + ")"
    elif isinstance(obj, dict):
        return (
            "{"
            + ", ".join(
                f"{get_object_string(key)}: {get_object_string(value)}"
                for key, value in obj.items()
            )
            + "}"
        )
    elif isinstance(obj, Enum):
        return f"{obj.__class__.__name__}.{obj.name}"
    elif hasattr(obj, "__dict__"):
        args = ", ".join(
            f"{key}={get_object_string(value)}"
            for key, value in vars(obj).items()
            if key != "_jac_"
        )
        return f"{obj.__class__.__name__}({args})"
    else:
        return str(obj)


def get_all_type_explanations(type_list: list, mod_registry: SemRegistry) -> dict:
    """Get all type explanations from the input type list."""
    collected_type_explanations = {}
    for type_item in type_list:
        type_explanation_str, nested_types = get_type_explanation(
            type_item, mod_registry
        )
        if type_explanation_str is not None:
            if type_item not in collected_type_explanations:
                collected_type_explanations[type_item] = type_explanation_str
            if nested_types:
                nested_collected_type_explanations = get_all_type_explanations(
                    list(nested_types), mod_registry
                )
                for k, v in nested_collected_type_explanations.items():
                    if k not in collected_type_explanations:
                        collected_type_explanations[k] = v
    return collected_type_explanations


def get_type_explanation(
    type_str: str, mod_registry: SemRegistry
) -> tuple[str | None, set[str] | None]:
    """Get the type explanation of the input type string."""
    scope, sem_info = mod_registry.lookup(name=type_str)
    if isinstance(sem_info, SemInfo) and sem_info.type:
        sem_info_scope = SemScope(sem_info.name, sem_info.type, scope)
        _, type_info = mod_registry.lookup(scope=sem_info_scope)
        type_info_str = []
        type_info_types = []
        if sem_info.type == "Enum" and isinstance(type_info, list):
            for enum_item in type_info:
                type_info_str.append(
                    f"{enum_item.semstr} (EnumItem) ({enum_item.name})"
                )
        elif sem_info.type in ["obj", "class", "node", "edge"] and isinstance(
            type_info, list
        ):
            for arch_item in type_info:
                type_info_str.append(
                    f"{arch_item.semstr} ({arch_item.type}) ({arch_item.name})"
                )
                if arch_item.type and extract_non_primary_type(arch_item.type):
                    type_info_types.extend(extract_non_primary_type(arch_item.type))
        return (
            f"{sem_info.semstr} ({sem_info.type}) ({sem_info.name}) = {', '.join(type_info_str)}",
            set(type_info_types),
        )
    return None, None


def extract_non_primary_type(type_str: str) -> list:
    """Extract non-primary types from the type string."""
    if not type_str:
        return []
    pattern = r"(?:\[|,\s*|\|)([a-zA-Z_][a-zA-Z0-9_]*)|([a-zA-Z_][a-zA-Z0-9_]*)"
    matches = re.findall(pattern, type_str)
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
    non_primary_types = [m for t in matches for m in t if m and m not in primary_types]
    return non_primary_types


def get_type_annotation(data: Any) -> str:  # noqa: ANN401
    """Get the type annotation of the input data."""
    if isinstance(data, dict):
        class_name = next(
            (value.__class__.__name__ for value in data.values() if value is not None),
            None,
        )
        if class_name:
            return f"dict[str, {class_name}]"
        else:
            return "dict[str, Any]"
    else:
        return str(type(data).__name__)

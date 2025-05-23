"""Utility Functions for the MTLLM."""

import re
from enum import Enum
from typing import Any

from mtllm.semtable import SemRegistry, SemScope


def get_object_string(obj: Any) -> str:  # noqa: ANN401
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
            if key != "__jac__"
        )
        return f"{obj.__class__.__name__}({args})"
    else:
        return str(obj)


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
    elif isinstance(data, list):
        if data:
            class_name = data[0].__class__.__name__
            return f"list[{class_name}]"
        else:
            return "list"
    else:
        return str(type(data).__name__)


def get_filtered_registry(mod_registry: SemRegistry, scope: SemScope) -> SemRegistry:
    """Get the filtered registry based on the scope."""
    avail_scopes = []
    while True:
        avail_scopes.append(str(scope))
        if not scope.parent:
            break
        scope = scope.parent

    print(f"Available scopes: {avail_scopes}")

    filtered_registry = SemRegistry()
    for _scope, sem_info_list in mod_registry.registry.items():
        if str(_scope) in avail_scopes:
            filtered_registry.registry[_scope] = sem_info_list

    return filtered_registry


def extract_template_placeholders(template: str) -> list:
    """Extract placeholders from the template."""
    return re.findall(r"{(.*?)}", template)


def format_template_section(template_section: str, values_dict: dict) -> str:
    """Format a template section with given values."""
    placeholders = extract_template_placeholders(template_section)
    formatted_sections = []
    for placeholder in placeholders:
        if placeholder in values_dict and values_dict[placeholder]:
            section_template = f"[{placeholder.title()}]\n{values_dict[placeholder]}"
            formatted_sections.append(section_template)
    return "\n\n".join(formatted_sections).strip()

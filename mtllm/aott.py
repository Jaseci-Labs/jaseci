"""
AOTT: Automated Operational Type Transformation.

This has all the necessary functions to perform the AOTT operations.
"""

from jaclang.compiler.semtable import SemRegistry

from mtllm.llms.base import BaseLLM
from mtllm.tools.base import Tool
from mtllm.types import (
    Image,
    Information,
    InputInformation,
    OutputHint,
    TypeExplanation,
    Video,
)


def aott_raise(
    model: BaseLLM,
    informations: list[Information],
    inputs_information: list[InputInformation],
    output_hint: OutputHint,
    type_explanations: list[TypeExplanation],
    action: str,
    context: str,
    method: str,
    tools: list[Tool],
    model_params: dict,
) -> str:
    """AOTT Raise uses the information (Meanings types values) provided to generate a prompt(meaning in)."""
    contains_media: bool = any(
        isinstance(x.value, (Image, Video)) for x in inputs_information
    )
    informations_str = "\n".join([str(x) for x in informations])
    inputs_information_repr: list[dict] | str
    if contains_media:
        inputs_information_repr = []
        for x in inputs_information:
            inputs_information_repr.extend(x.to_list_dict())
    else:
        inputs_information_repr = "\n".join([str(x) for x in inputs_information])

    type_explanations_str = "\n".join([str(x) for x in type_explanations])

    system_prompt = model.MTLLM_SYSTEM_PROMPT
    meaning_typed_input: str | list[dict]
    if method != "ReAct":
        method_prompt = model.MTLLM_METHOD_PROMPTS[method]
        if isinstance(inputs_information_repr, str):
            mtllm_prompt = model.MTLLM_PROMPT.format(
                information=informations_str,
                inputs_information=inputs_information_repr,
                output_information=str(output_hint),
                type_explanations=type_explanations_str,
                action=action,
                context=context,
            ).strip()
            meaning_typed_input = (
                f"{system_prompt}\n{mtllm_prompt}\n{method_prompt}".strip()
            )
        else:
            upper_half = model.MTLLM_PROMPT.split("{inputs_information}")[0]
            lower_half = model.MTLLM_PROMPT.split("{inputs_information}")[1]
            upper_half = upper_half.format(
                information=informations_str,
                context=context,
            )
            lower_half = lower_half.format(
                output_information=str(output_hint),
                type_explanations=type_explanations_str,
                action=action,
            )
            meaning_typed_input = [
                {"type": "text", "text": system_prompt},
                {"type": "text", "text": upper_half},
            ]
            meaning_typed_input.extend(inputs_information_repr)
            meaning_typed_input.extend(
                [
                    {"type": "text", "text": lower_half},
                    {"type": "text", "text": method_prompt},
                ]
            )
        return model(meaning_typed_input, **model_params)
    else:
        assert tools, "Tools must be provided for the ReAct method."
        # TODO: Implement ReAct method
        return ""


def get_all_type_explanations(
    type_list: list, mod_registry: SemRegistry
) -> list[TypeExplanation]:
    """Get all type explanations from the input type list."""
    collected_type_explanations = {}
    for type_item in type_list:
        type_explanation = TypeExplanation(type_item, mod_registry)
        if str(type_explanation) and type_item not in collected_type_explanations:
            collected_type_explanations[type_item] = type_explanation
        if type_explanation.nested_types:
            nested_collected_type_explanations = get_all_type_explanations(
                list(type_explanation.nested_types), mod_registry
            )
            for nested_type_explanation in nested_collected_type_explanations:
                if nested_type_explanation.type_item not in collected_type_explanations:
                    collected_type_explanations[nested_type_explanation.type_item] = (
                        nested_type_explanation
                    )
    return list(collected_type_explanations.values())

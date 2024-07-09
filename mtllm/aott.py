"""
AOTT: Automated Operational Type Transformation.

This has all the necessary functions to perform the AOTT operations.
"""

from typing import Any

from jaclang.compiler.semtable import SemInfo, SemRegistry, SemScope

from mtllm.llms.base import BaseLLM
from mtllm.tools.base import Tool
from mtllm.types import Image, TypeExplanation, Video
from mtllm.utils import extract_non_primary_type, get_object_string, get_type_annotation


def aott_raise(
    model: BaseLLM,
    information: str,
    inputs_information: str | list[dict],
    output_information: str,
    type_explanations: list["TypeExplanation"],
    action: str,
    context: str,
    method: str,
    tools: list[Tool],
    model_params: dict,
) -> str:
    """AOTT Raise uses the information (Meanings types values) provided to generate a prompt(meaning in)."""
    type_explanations_str = "\n".join([str(x) for x in type_explanations])
    system_prompt = model.MTLLM_SYSTEM_PROMPT
    meaning_in: str | list[dict]
    if method != "ReAct":
        method_prompt = model.MTLLM_METHOD_PROMPTS[method]
        if isinstance(inputs_information, str):
            mtllm_prompt = model.MTLLM_PROMPT.format(
                information=information,
                inputs_information=inputs_information,
                output_information=output_information,
                type_explanations=type_explanations_str,
                action=action,
                context=context,
            ).strip()
            meaning_in = f"{system_prompt}\n{mtllm_prompt}\n{method_prompt}".strip()
        else:
            upper_half = model.MTLLM_PROMPT.split("{inputs_information}")[0]
            lower_half = model.MTLLM_PROMPT.split("{inputs_information}")[1]
            upper_half = upper_half.format(
                information=information,
                context=context,
            )
            lower_half = lower_half.format(
                output_information=output_information,
                type_explanations=type_explanations_str,
                action=action,
            )
            meaning_in = (
                [
                    {"type": "text", "text": system_prompt},
                    {"type": "text", "text": upper_half},
                ]
                + inputs_information
                + [
                    {"type": "text", "text": lower_half},
                    {"type": "text", "text": method_prompt},
                ]
            )
        return model(meaning_in, **model_params)
    else:
        assert tools, "Tools must be provided for the ReAct method."
        # TODO: Implement ReAct method
        return ""


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
                f"{sem_info.semstr} ({sem_info.name}) ({sem_info.type}) = {get_object_string(incl[1])}".strip()
            )
    return ("\n".join(info_str), collected_types)


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


def get_input_information(
    inputs: list[tuple[str, str, str, Any]], type_collector: list
) -> str | list[dict]:
    """
    Get the input information for the AOTT operation.

    Returns:
        str | list[dict]: If the input does not contain images, returns a string with the input information.
            If the input contains images, returns a list of dictionaries representing the input information,
            where each dictionary contains either text or image_url.

    """
    contains_media = any(isinstance(i[3], (Image, Video)) for i in inputs)
    if not contains_media:
        inputs_information_list = []
        for i in inputs:
            typ_anno = get_type_annotation(i[3])
            type_collector.extend(extract_non_primary_type(typ_anno))
            inputs_information_list.append(
                f"{i[0] if i[0] else ''} ({i[2]}) ({typ_anno}) = {get_object_string(i[3])}".strip()
            )
        return "\n".join(inputs_information_list)
    else:
        inputs_information_dict_list: list[dict] = []
        for i in inputs:
            input_type = get_type_annotation(i[3])
            if input_type == "Image":
                img_base64, img_type = i[3].process()
                image_repr: list[dict] = [
                    {
                        "type": "text",
                        "text": f"{i[0] if i[0] else ''} ({i[2]}) (Image) = ".strip(),
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{img_type};base64,{img_base64}"
                        },
                    },
                ]
                inputs_information_dict_list.extend(image_repr)
                continue
            if input_type == "Video":
                video_frames = i[3].process()
                print(len(video_frames))
                video_repr: list[dict] = [
                    {
                        "type": "text",
                        "text": f"{i[0] if i[0] else ''} ({i[2]}) (Video) = Following are the frames of the video".strip(),  # noqa: E501
                    },
                    *(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpg;base64,{x}",
                                "detail": "low",
                            },
                        }
                        for x in video_frames
                    ),
                ]
                inputs_information_dict_list.extend(video_repr)
                continue
            type_collector.extend(extract_non_primary_type(input_type))
            inputs_information_dict_list.append(
                {
                    "type": "text",
                    "text": f"{i[0] if i[0] else ''} ({i[2]}) ({input_type}) = {get_object_string(i[3])}".strip(),
                }
            )
        return inputs_information_dict_list

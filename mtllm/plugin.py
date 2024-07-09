"""Plugin for Jac's with_llm feature."""

import os
import pickle
from typing import Any

from jaclang.compiler.semtable import SemScope
from jaclang.plugin.default import hookimpl

from mtllm.aott import (
    aott_raise,
    get_all_type_explanations,
)
from mtllm.llms.base import BaseLLM
from mtllm.types import Information, InputInformation, OutputHint
from mtllm.utils import get_filtered_registry


class JacFeature:
    """Jac's with_llm feature."""

    @staticmethod
    @hookimpl
    def with_llm(
        file_loc: str,
        model: BaseLLM,
        model_params: dict[str, Any],
        scope: str,
        incl_info: list[tuple[str, str]],
        excl_info: list[tuple[str, str]],
        inputs: list[
            tuple[str, str, str, Any]
        ],  # TODO: Need to change this in the jaclang pyast_build_pass
        outputs: tuple,
        action: str,
    ) -> Any:  # noqa: ANN401
        """Jac's with_llm feature."""
        with open(
            os.path.join(
                os.path.dirname(file_loc),
                "__jac_gen__",
                os.path.basename(file_loc).replace(".jac", ".registry.pkl"),
            ),
            "rb",
        ) as f:
            mod_registry = pickle.load(f)

        _scope = SemScope.get_scope_from_str(scope)
        assert _scope is not None, f"Invalid scope: {scope}"

        method = model_params.pop("method") if "method" in model_params else "Normal"
        available_methods = model.MTLLM_METHOD_PROMPTS.keys()
        assert (
            method in available_methods
        ), f"Invalid method: {method}. Select from {available_methods}"

        context = (
            "\n".join(model_params.pop("context")) if "context" in model_params else ""
        )

        type_collector: list = []

        filtered_registry = get_filtered_registry(mod_registry, _scope)
        incl_info = [x for x in incl_info if not isinstance(x[1], type)]
        informations = [Information(filtered_registry, x[0], x[1]) for x in incl_info]
        type_collector.extend([x.get_types() for x in informations])

        inputs_information = []
        for input_item in inputs:
            _input = InputInformation(input_item[0], input_item[2], input_item[3])
            type_collector.extend(_input.get_types())
            inputs_information.append(_input)

        output = outputs[0] if isinstance(outputs, list) else outputs
        output_hint = OutputHint(output[0], output[1])
        type_collector.extend(output_hint.get_types())
        output_type_explanations = get_all_type_explanations(
            output_hint.get_types(), mod_registry
        )

        type_explanations = get_all_type_explanations(type_collector, mod_registry)

        meaning_out = aott_raise(
            model,
            informations,
            inputs_information,
            output_hint,
            type_explanations,
            action,
            context,
            method,
            [],
            model_params,
        )
        _output = model.resolve_output(
            meaning_out, output_hint, output_type_explanations
        )
        return _output

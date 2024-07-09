"""Plugin for Jac's with_llm feature."""

import os
import pickle
from typing import Any

from jaclang.compiler.semtable import SemScope
from jaclang.plugin.default import hookimpl

from mtllm.aott import (
    aott_raise,
    extract_non_primary_type,
    get_all_type_explanations,
    get_info_types,
    get_input_information,
)
from mtllm.llms.base import BaseLLM


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
        inputs: list[tuple[str, str, str, Any]],
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

        outputs = outputs[0] if isinstance(outputs, list) else outputs
        _scope = SemScope.get_scope_from_str(scope)
        assert _scope is not None

        method = model_params.pop("method") if "method" in model_params else "Normal"
        available_methods = model.MTLLM_METHOD_PROMPTS.keys()
        assert (
            method in available_methods
        ), f"Invalid method: {method}. Select from {available_methods}"

        context = (
            "\n".join(model_params.pop("context")) if "context" in model_params else ""
        )

        type_collector: list = []
        incl_info = [x for x in incl_info if not isinstance(x[1], type)]
        information, collected_types = get_info_types(_scope, mod_registry, incl_info)
        type_collector.extend(collected_types)

        inputs_information = get_input_information(inputs, type_collector)

        output_information = f"{outputs[0]} ({outputs[1]})".strip()
        type_collector.extend(extract_non_primary_type(outputs[1]))
        output_type_explanations = "\n".join(
            [
                str(x)
                for x in get_all_type_explanations(
                    extract_non_primary_type(outputs[1]), mod_registry
                )
            ]
        )

        meaning_out = aott_raise(
            model=model,
            information=information,
            inputs_information=inputs_information,
            output_information=output_information,
            type_explanations=get_all_type_explanations(type_collector, mod_registry),
            action=action,
            context=context,
            method=method,
            tools=[],
            model_params=model_params,
        )
        output = model.resolve_output(
            meaning_out, outputs[0], outputs[1], output_type_explanations
        )
        return output

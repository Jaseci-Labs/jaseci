"""Plugin for Jac's with_llm feature."""

import ast as ast3
from typing import Any, Callable, Mapping, Optional, Sequence

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import Constants as Con
from jaclang.compiler.passes.main.pyast_gen_pass import PyastGenPass
from jaclang.compiler.semtable import SemInfo, SemRegistry, SemScope
from jaclang.plugin.default import hookimpl
from jaclang.runtimelib.utils import extract_params, extract_type, get_sem_scope

from mtllm.aott import (
    aott_raise,
    get_all_type_explanations,
)
from mtllm.llms.base import BaseLLM
from mtllm.types import Information, InputInformation, OutputHint, Tool
from mtllm.utils import get_filtered_registry


def callable_to_tool(tool: Callable, mod_registry: SemRegistry) -> Tool:
    """Convert a callable to a Tool."""
    assert callable(tool), f"{tool} cannot be used as a tool"
    tool_name = tool.__name__
    _, tool_info = mod_registry.lookup(name=tool_name)
    assert tool_info and isinstance(
        tool_info, SemInfo
    ), f"Tool {tool_name} not found in the registry"
    return Tool(tool, tool_info, tool_info.get_children(mod_registry, ast.ParamVar))


class JacFeature:
    """Jac's with_llm feature."""

    @staticmethod
    @hookimpl
    def with_llm(
        file_loc: str,
        model: BaseLLM,
        model_params: dict[str, Any],
        scope: str,
        incl_info: list[tuple[str, Any]],  # noqa: ANN401
        excl_info: list[tuple[str, str]],
        inputs: list[
            tuple[str, str, str, Any]
        ],  # TODO: Need to change this in the jaclang pyast_build_pass
        outputs: tuple,
        action: str,
        _globals: dict,
        _locals: Mapping,
    ) -> Any:  # noqa: ANN401
        """Jac's with_llm feature."""
        from jaclang.runtimelib.machine import JacMachine

        mod_registry = JacMachine.get().jac_program.sem_ir

        _scope = SemScope.get_scope_from_str(scope)
        assert _scope is not None, f"Invalid scope: {scope}"

        method = model_params.pop("method") if "method" in model_params else "Normal"
        is_custom = (
            model_params.pop("is_custom") if "is_custom" in model_params else False
        )
        raw_output = (
            model_params.pop("raw_output") if "raw_output" in model_params else False
        )
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

        tools = model_params.pop("tools") if "tools" in model_params else None
        if method == "ReAct":
            assert tools, "Tools must be provided for the ReAct method."
            _tools = [
                tool if isinstance(tool, Tool) else callable_to_tool(tool, mod_registry)
                for tool in tools
            ]
        else:
            _tools = []

        meaning_out = aott_raise(
            model,
            informations,
            inputs_information,
            output_hint,
            type_explanations,
            action,
            context,
            method,
            is_custom,
            _tools,
            model_params,
            _globals,
            _locals,
        )
        _output = (
            model.resolve_output(
                meaning_out, output_hint, output_type_explanations, _globals, _locals
            )
            if not raw_output
            else meaning_out
        )
        return _output

    @staticmethod
    @hookimpl
    def gen_llm_body(_pass: PyastGenPass, node: ast.Ability) -> list[ast3.AST]:
        """Generate the by LLM body."""
        _pass.needs_jac_feature()
        if isinstance(node.body, ast.FuncCall):
            model = node.body.target.gen.py_ast[0]
            extracted_type = (
                "".join(extract_type(node.signature.return_type))
                if isinstance(node.signature, ast.FuncSignature)
                and node.signature.return_type
                else None
            )
            scope = _pass.sync(ast3.Constant(value=str(get_sem_scope(node))))
            model_params, include_info, exclude_info = extract_params(node.body)
            inputs = (
                [
                    _pass.sync(
                        ast3.Tuple(
                            elts=[
                                (
                                    _pass.sync(
                                        ast3.Constant(
                                            value=(
                                                param.semstr.lit_value
                                                if param.semstr
                                                else None
                                            )
                                        )
                                    )
                                ),
                                (
                                    param.type_tag.tag.gen.py_ast[0]
                                    if param.type_tag
                                    else None
                                ),
                                _pass.sync(ast3.Constant(value=param.name.value)),
                                _pass.sync(
                                    ast3.Name(
                                        id=param.name.value,
                                        ctx=ast3.Load(),
                                    )
                                ),
                            ],
                            ctx=ast3.Load(),
                        )
                    )
                    for param in node.signature.params.items
                ]
                if isinstance(node.signature, ast.FuncSignature)
                and node.signature.params
                else []
            )
            outputs = (
                [
                    (
                        _pass.sync(
                            ast3.Constant(
                                value=(
                                    node.signature.semstr.lit_value
                                    if node.signature.semstr
                                    else ""
                                )
                            )
                        )
                    ),
                    (_pass.sync(ast3.Constant(value=(extracted_type)))),
                ]
                if isinstance(node.signature, ast.FuncSignature)
                else []
            )
            action = (
                node.semstr.gen.py_ast[0]
                if node.semstr
                else _pass.sync(ast3.Constant(value=node.name_ref.sym_name))
            )
            return [
                _pass.sync(
                    ast3.Return(
                        value=_pass.sync(
                            _pass.by_llm_call(
                                model,
                                model_params,
                                scope,
                                inputs,
                                outputs,
                                action,
                                include_info,
                                exclude_info,
                            )
                        )
                    )
                )
            ]
        else:
            return []

    @staticmethod
    @hookimpl
    def by_llm_call(
        _pass: PyastGenPass,
        model: ast3.AST,
        model_params: dict[str, ast.Expr],
        scope: ast3.AST,
        inputs: Sequence[Optional[ast3.AST]],
        outputs: Sequence[Optional[ast3.AST]] | ast3.Call,
        action: Optional[ast3.AST],
        include_info: list[tuple[str, ast3.AST]],
        exclude_info: list[tuple[str, ast3.AST]],
    ) -> ast3.Call:
        """Return the LLM Call, e.g. _Jac.with_llm()."""
        return _pass.sync(
            ast3.Call(
                func=_pass.sync(
                    ast3.Attribute(
                        value=_pass.sync(
                            ast3.Name(
                                id=Con.JAC_FEATURE.value,
                                ctx=ast3.Load(),
                            )
                        ),
                        attr="with_llm",
                        ctx=ast3.Load(),
                    )
                ),
                args=[],
                keywords=[
                    _pass.sync(
                        ast3.keyword(
                            arg="file_loc",
                            value=_pass.sync(ast3.Name(id="__file__", ctx=ast3.Load())),
                        )
                    ),
                    _pass.sync(
                        ast3.keyword(
                            arg="model",
                            value=model,
                        )
                    ),
                    _pass.sync(
                        ast3.keyword(
                            arg="model_params",
                            value=_pass.sync(
                                ast3.Dict(
                                    keys=[
                                        _pass.sync(ast3.Constant(value=key))
                                        for key in model_params.keys()
                                    ],
                                    values=[
                                        value.gen.py_ast[0]
                                        for value in model_params.values()
                                    ],
                                )
                            ),
                        )
                    ),
                    _pass.sync(
                        ast3.keyword(
                            arg="scope",
                            value=scope,
                        )
                    ),
                    _pass.sync(
                        ast3.keyword(
                            arg="incl_info",
                            value=_pass.sync(
                                ast3.List(
                                    elts=[
                                        _pass.sync(
                                            ast3.Tuple(
                                                elts=[
                                                    _pass.sync(
                                                        ast3.Constant(value=key)
                                                    ),
                                                    value,
                                                ],
                                                ctx=ast3.Load(),
                                            )
                                        )
                                        for key, value in include_info
                                    ],
                                    ctx=ast3.Load(),
                                )
                            ),
                        )
                    ),
                    _pass.sync(
                        ast3.keyword(
                            arg="excl_info",
                            value=_pass.sync(
                                ast3.List(
                                    elts=[
                                        _pass.sync(
                                            ast3.Tuple(
                                                elts=[
                                                    _pass.sync(
                                                        ast3.Constant(value=key)
                                                    ),
                                                    value,
                                                ],
                                                ctx=ast3.Load(),
                                            )
                                        )
                                        for key, value in exclude_info
                                    ],
                                    ctx=ast3.Load(),
                                )
                            ),
                        ),
                    ),
                    _pass.sync(
                        ast3.keyword(
                            arg="inputs",
                            value=_pass.sync(
                                ast3.List(
                                    elts=inputs,
                                    ctx=ast3.Load(),
                                )
                            ),
                        )
                    ),
                    _pass.sync(
                        ast3.keyword(
                            arg="outputs",
                            value=(
                                _pass.sync(
                                    ast3.Tuple(
                                        elts=outputs,
                                        ctx=ast3.Load(),
                                    )
                                )
                                if not isinstance(outputs, ast3.Call)
                                else outputs
                            ),
                        )
                    ),
                    _pass.sync(
                        ast3.keyword(
                            arg="action",
                            value=action,
                        )
                    ),
                    _pass.sync(
                        ast3.keyword(
                            arg="_globals",
                            value=_pass.sync(
                                ast3.Call(
                                    func=_pass.sync(
                                        ast3.Name(
                                            id="globals",
                                            ctx=ast3.Load(),
                                        )
                                    ),
                                    args=[],
                                    keywords=[],
                                )
                            ),
                        )
                    ),
                    _pass.sync(
                        ast3.keyword(
                            arg="_locals",
                            value=_pass.sync(
                                ast3.Call(
                                    func=_pass.sync(
                                        ast3.Name(
                                            id="locals",
                                            ctx=ast3.Load(),
                                        )
                                    ),
                                    args=[],
                                    keywords=[],
                                )
                            ),
                        )
                    ),
                ],
            )
        )

    @staticmethod
    @hookimpl
    def get_by_llm_call_args(_pass: PyastGenPass, node: ast.FuncCall) -> dict:
        """Get the by LLM call args."""
        if node.genai_call is None:
            raise _pass.ice("No genai_call")

        model = node.genai_call.target.gen.py_ast[0]
        model_params, include_info, exclude_info = extract_params(node.genai_call)
        action = _pass.sync(
            ast3.Constant(
                value="Create an object of the specified type, using the specifically "
                " provided input value(s) and look up any missing attributes from reliable"
                " online sources to fill them in accurately."
            )
        )
        _output_ = "".join(extract_type(node.target))
        include_info.append(
            (
                _output_.split(".")[0],
                _pass.sync(ast3.Name(id=_output_.split(".")[0], ctx=ast3.Load())),
            )
        )
        scope = _pass.sync(
            ast3.Call(
                func=_pass.sync(
                    ast3.Attribute(
                        value=_pass.sync(
                            ast3.Name(
                                id=Con.JAC_FEATURE.value,
                                ctx=ast3.Load(),
                            )
                        ),
                        attr="obj_scope",
                        ctx=ast3.Load(),
                    )
                ),
                args=[
                    _pass.sync(
                        ast3.Name(
                            id="__file__",
                            ctx=ast3.Load(),
                        )
                    ),
                    _pass.sync(ast3.Constant(value=_output_)),
                ],
                keywords=[],
            )
        )
        outputs = _pass.sync(
            ast3.Call(
                func=_pass.sync(
                    ast3.Attribute(
                        value=_pass.sync(
                            ast3.Name(
                                id=Con.JAC_FEATURE.value,
                                ctx=ast3.Load(),
                            )
                        ),
                        attr="get_sem_type",
                        ctx=ast3.Load(),
                    )
                ),
                args=[
                    _pass.sync(
                        ast3.Name(
                            id="__file__",
                            ctx=ast3.Load(),
                        )
                    ),
                    _pass.sync(ast3.Constant(value=str(_output_))),
                ],
                keywords=[],
            )
        )
        if node.params and node.params.items:
            inputs = [
                _pass.sync(
                    ast3.Tuple(
                        elts=[
                            _pass.sync(
                                ast3.Call(
                                    func=_pass.sync(
                                        ast3.Attribute(
                                            value=_pass.sync(
                                                ast3.Name(
                                                    id=Con.JAC_FEATURE.value,
                                                    ctx=ast3.Load(),
                                                )
                                            ),
                                            attr="get_semstr_type",
                                            ctx=ast3.Load(),
                                        )
                                    ),
                                    args=[
                                        _pass.sync(
                                            ast3.Name(id="__file__", ctx=ast3.Load())
                                        ),
                                        scope,
                                        _pass.sync(
                                            ast3.Constant(
                                                value=(
                                                    kw_pair.key.value
                                                    if isinstance(kw_pair.key, ast.Name)
                                                    else None
                                                )
                                            )
                                        ),
                                        _pass.sync(ast3.Constant(value=True)),
                                    ],
                                    keywords=[],
                                )
                            ),
                            _pass.sync(
                                ast3.Call(
                                    func=_pass.sync(
                                        ast3.Attribute(
                                            value=_pass.sync(
                                                ast3.Name(
                                                    id=Con.JAC_FEATURE.value,
                                                    ctx=ast3.Load(),
                                                )
                                            ),
                                            attr="get_semstr_type",
                                            ctx=ast3.Load(),
                                        )
                                    ),
                                    args=[
                                        _pass.sync(
                                            ast3.Name(id="__file__", ctx=ast3.Load())
                                        ),
                                        scope,
                                        _pass.sync(
                                            ast3.Constant(
                                                value=(
                                                    kw_pair.key.value
                                                    if isinstance(kw_pair.key, ast.Name)
                                                    else None
                                                )
                                            )
                                        ),
                                        _pass.sync(ast3.Constant(value=False)),
                                    ],
                                    keywords=[],
                                )
                            ),
                            _pass.sync(
                                ast3.Constant(
                                    value=(
                                        kw_pair.key.value
                                        if isinstance(kw_pair.key, ast.Name)
                                        else None
                                    )
                                )
                            ),
                            kw_pair.value.gen.py_ast[0],
                        ],
                        ctx=ast3.Load(),
                    )
                )
                for kw_pair in node.params.items
                if isinstance(kw_pair, ast.KWPair)
            ]
        else:
            inputs = []

        return {
            "model": model,
            "model_params": model_params,
            "scope": scope,
            "inputs": inputs,
            "outputs": outputs,
            "action": action,
            "include_info": include_info,
            "exclude_info": exclude_info,
        }

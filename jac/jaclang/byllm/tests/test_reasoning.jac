"""A model's reasoning, and any other field a provider puts on its reply: kept, sent
back, counted and reported to an llm call hook, streamed or not (backport of #10229)."""

import json;
import os;
import from pathlib { Path }
import from unittest { mock }
import from litellm.types.utils {
    Delta,
    Message as LiteLLMMessage,
    ModelResponse,
    ModelResponseStream,
    StreamingChoices,
    Usage
}
import jaclang.byllm.llm as _byllm_llm_mod;
import from jaclang.byllm.lib {
    Model,
    register_llm_call_hook,
    unregister_llm_call_hook
}
import from jaclang.byllm.llm { _estimate_tokens }
import from jaclang.byllm.tool_protocol { coerce_message_dict }
import from jaclang.byllm.config_loader { get_byllm_config, reset_byllm_config }

glob THINK: str = "REASONING " + ("step by step " * 20),
     CALL: tuple[str, str, dict[str, any]] = ("c1", "get_weather", {"city": "Paris"});


def get_weather(city: str) -> str {
    return f"sunny in {city}";
}


def usage(prompt: int = 10) -> Usage {
    return Usage(
        prompt_tokens=prompt,
        completion_tokens=9,
        total_tokens=19,
        completion_tokens_details={"reasoning_tokens": 7}
    );
}


def tool_calls(call: tuple | None) -> list[dict[str, any]] | None {
    if call is None {
        return None;
    }
    fn = {"name": call[1], "arguments": json.dumps(call[2])};
    return [{"index": 0, "id": call[0], "type": "function", "function": fn}];
}


"""A whole reply carrying THINK, as litellm returns it."""
def whole(content: str, call: tuple | None = None, prompt: int = 10) -> ModelResponse {
    msg = LiteLLMMessage(
        role="assistant",
        content=content,
        reasoning_content=THINK,
        tool_calls=tool_calls(call)
    );
    reason = "tool_calls" if call else "stop";
    return ModelResponse(
        model="gpt-4o",
        choices=[{"index": 0, "message": msg, "finish_reason": reason}],
        usage=usage(prompt)
    );
}


"""The same reply as stream chunks: reasoning first, then the text or the call."""
def streamed(content: str, call: tuple | None = None) -> list[any] {
    def chunk(delta: Delta, reason: str | None = None) -> any {
        return ModelResponseStream(
            model="gpt-4o",
            choices=[StreamingChoices(index=0, delta=delta, finish_reason=reason)]
        );
    }
    out = [chunk(Delta(role="assistant", reasoning_content=THINK))];
    if content {
        out.append(chunk(Delta(content=content)));
    }
    if call {
        out.append(chunk(Delta(tool_calls=tool_calls(call))));
    }
    last = chunk(Delta(), "tool_calls" if call else "stop");
    last.usage = usage();
    out.append(last);
    return out;
}


"""Run `ask` with the model's network calls answered from `replies` in order,
recording every request and hook record."""
def drive(
    ask: any, question: str | None, replies: list[any]
) -> tuple[list[any], list[any]] {
    sent: list[any] = [];
    records: list[any] = [];
    def answer(params: dict) -> any {
        sent.append(params);
        reply = replies.pop(0);
        return iter(reply) if isinstance(reply, list) else reply;
    }
    def broken(record: dict) {
        raise RuntimeError("a hook that raises must not break the call");
    }
    register_llm_call_hook(broken);
    register_llm_call_hook(records.append);
    try {
        with mock.patch.object(Model, "model_call_with_stream", side_effect=answer) {
            with mock.patch.object(Model, "model_call_no_stream", side_effect=answer) {
                out: any = ask(question) if question is not None else ask();
                if hasattr(out, "__next__") {
                    list(out);
                }
            }
        }
    } finally {
        unregister_llm_call_hook(broken);
        unregister_llm_call_hook(records.append);
    }
    return (sent, records);
}


"""Each message as (role, content), from a dict or a litellm object."""
def wire(msgs: list[any]) -> list[tuple[str, str]] {
    return [(str(m.get("role")), str(m.get("content"))) for m in msgs];
}


"""Each record's new_messages is what its request sent past the previous call's reply."""
def assert_records_match(label: str, records: list[any], sent: list[any]) {
    for (i, rec) in enumerate(records) {
        start = 0 if i == 0 else len(sent[i - 1]["messages"]) + 1;
        want = sent[i]["messages"][start:];
        assert wire(rec["new_messages"]) == wire(want) , (
            f"{label}: record {i} has {wire(rec['new_messages'])}, the request sent {wire(
                want
            )}"
        );
    }
}


test "reasoning is kept, sent back and reported on every tool-loop path" {
    llm = Model(model_name="gpt-4o");
    for (label, stream, logging, replies) in [
        ("whole replies", False, False, whole),
        ("stream with events", True, True, streamed),
        ("stream, final-answer restream", True, False, None)
    ] {
        history: list[any] = [];
        def ask(q: str) -> str by llm(
            tools=[get_weather], conversation=history, stream=stream, logging=logging
        );
        for (turn, question) in enumerate(["How is Paris?", "Still sunny?"]) {
            if replies is None {
                # Tool loop on whole replies, then the answer streamed again.
                script = [
                    whole("", CALL),
                    whole("", ("c2", "finish_tool", {"final_output": "ok"})),
                    streamed("Paris is sunny.")
                ];
            } else {
                script = [replies("", CALL), replies("Paris is sunny.")];
            }
            calls = len(script);
            before = [dict(m) for m in history];
            (sent, records) = drive(ask, question, script);
            if turn == 1 {
                resent = [
                    m
                    for m in sent[0]["messages"]
                    if not (isinstance(m, dict) and m.get("role") == "system")
                ];
                assert [dict(m) for m in resent[:len(before)]] == before , (
                    f"{label}: turn 2 changed what turn 1 left in the history"
                );
            }
            replies_kept = [
                m
                for m in history
                if m.get("role") == "assistant"
            ];
            assert replies_kept
            and all(m.get("reasoning_content") == THINK for m in replies_kept) , (
                f"{label}: stored replies {replies_kept}"
            );
            assert len(records) == calls , f"{label}: {calls} calls, {len(
                records
            )} records";
            assert_records_match(label, records, sent);
            for rec in records {
                assert rec["reply"].get("reasoning_content") == THINK , f"{label}: {rec[
                    'reply'
                ]}";
                assert rec["usage"].get("reasoning_tokens") == 7 , f"{label}: {rec[
                    'usage'
                ]}";
            }
            first = records[0]["new_messages"];
            assert turn == 1
            or [m.get("role") for m in first[:2]] == ["system", "user"] , (
                f"{label}: the first record carries the prompt: {first}"
            );
        }
    }
}


test "a reply litellm cannot rebuild still keeps its reasoning" {
    llm = Model(model_name="gpt-4o");
    no_builder = RuntimeError("no builder");
    for (label, logging, script) in [
        ("tool-loop stream", True, [streamed("Paris is sunny.")]),
        (
            "final-answer restream",
            False,
            [
                whole("", ("c2", "finish_tool", {"final_output": "ok"})),
                streamed("Paris is sunny.")
            ]
        )
    ] {
        history: list[any] = [];
        def ask(q: str) -> str by llm(
            tools=[get_weather], conversation=history, stream=True, logging=logging
        );
        with mock.patch.object(
            _byllm_llm_mod.litellm, "stream_chunk_builder", side_effect=no_builder
        ) {
            drive(ask, "How is Paris?", script);
        }
        reply = history[-1];
        assert (reply.get("content"), reply.get("reasoning_content")) == (
            "Paris is sunny.",
            THINK
        ) , (f"{label}: the streamed text and reasoning are both the reply: {reply}");
    }
}


obj Place {
    has city: str;
}


test "hook records show the request as sent: the parallel hint, and a typed-output retry" {
    llm = Model(model_name="gpt-4o");
    def ask(q: str) -> str by llm(tools=[get_weather], parallelize=True);
    (_, records) = drive(ask, "hi", [whole("ok")]);
    system = records[0]["new_messages"][0];
    assert "scheduling rules" in str(system.get("content")) , f"system prompt recorded as {system}";
    def place -> Place by llm();
    retry = [whole('{"city": '), whole('{"schema_object_wrapper": {"city": "Galle"}}')];
    (sent, records) = drive(place, None, retry);
    last = records[-1];
    assert wire(last["new_messages"]) == wire(sent[-1]["messages"]) , (
        "after a typed-output retry the record carries the whole request, schema hint included"
    );
    assert last["after_compaction"]
    and "output parser reported" in str(last["new_messages"]) , (
        f"the retry record misses its feedback: {last}"
    );
}


test "reasoning params reach the model only when set, from by llm() or jac.toml" {
    enabled = {"type": "enabled"};
    keys = ("reasoning_effort", "thinking", "extra_body");
    for given in [
        ("low", None, None),
        (None, enabled, None),
        (None, None, {"thinking": enabled}),
        (None, None, None)
    ] {
        llm = Model(model_name="gpt-4o");
        def answer(q: str) -> str by llm(
            reasoning_effort=given[0], thinking=given[1], extra_body=given[2]
        );
        (sent, _) = drive(answer, "hi", [whole("ok")]);
        for (key, want) in zip(keys, given) {
            assert sent[0].get(key) == want
            and (want is not None or key not in sent[0]) , (
                f"{given}: {key} sent as {sent[0].get(key)!r}"
            );
        }
    }
    reset_byllm_config();
    try {
        fixture = os.path.join(
            os.path.dirname(__file__), "fixtures", "reasoning_config"
        );
        params = get_byllm_config(Path(fixture)).get_call_params_config();
        assert tuple(params.get(k) for k in keys) == ("low", enabled, None) , f"jac.toml: {params}";
    } finally {
        reset_byllm_config();
    }
}


test "provider fields are lifted, and compaction counts the reasoning it sends back" {
    msg = LiteLLMMessage(
        role="assistant",
        content="hi",
        provider_specific_fields={"reasoning_details": [{"text": THINK}]}
    );
    lifted = coerce_message_dict(msg);
    assert lifted.get("reasoning_details") == [{"text": THINK}]
    and "provider_specific_fields" not in lifted , (
        f"provider fields stay nested: {lifted}"
    );
    plain = {"role": "assistant", "content": "hi"};
    assert _estimate_tokens([plain | {"reasoning_content": "x" * 400}]) == _estimate_tokens(
        [plain]
    ) + 100 , ("reasoning sent back must count toward the context estimate");
}


test "after compaction the hook reports the whole rebuilt request" {
    llm = Model(model_name="gpt-4o");
    def drop_reasoning(msgs: list[any], keep_recent: int) -> list[any] {
        return [coerce_message_dict(m) | {"reasoning_content": None} for m in msgs];
    }
    def ask(q: str) -> str by llm(
        tools=[get_weather],
        ctx_window=1000,
        threshold_ratio=0.80,
        on_compaction=drop_reasoning
    );
    (_, records) = drive(
        ask, "How is Paris?", [whole("", CALL, prompt=900), whole("done")]
    );
    flags = [r["after_compaction"] for r in records];
    assert flags.count(True) == 1 , f"after_compaction flags {flags}";
    rebuilt = records[flags.index(True)]["new_messages"];
    assert rebuilt[0].get("role") == "system" , f"the rebuilt request is reported whole: {rebuilt}";
}


test "a streamed reply that fails to parse is still counted and reported" {
    llm = Model(model_name="gpt-4o");
    def on_event(event: any) { }
    # A typed answer streams only through a stream_handler.
    def place(q: str) -> Place by llm(
        tools=[get_weather], stream=True, stream_handler=on_event
    );
    records: list[any] = [];
    replies = [streamed('{"city": '), streamed('{"city": ')];
    def answer(params: dict) -> any {
        return iter(replies.pop(0));
    }
    register_llm_call_hook(records.append);
    try {
        with mock.patch.object(Model, "model_call_with_stream", side_effect=answer) {
            place("Where?");
        }
    } except Exception { } finally {
        unregister_llm_call_hook(records.append);
    }
    assert records and records[0]["reply"].get("reasoning_content") == THINK , (
        f"the unparsable reply is missing from the records: {records}"
    );
}

"""A model's reasoning, and any other field a provider puts on its reply: kept, sent
back, streamed, counted and reported, whatever path the tool loop takes."""

import json;
import litellm;
import from pathlib { Path }
import from unittest { mock }
import jaclang.byllm.llm as _byllm_llm_mod;
import from jaclang.byllm._optdeps.loguru { logger }
import from jaclang.byllm.lib { Model }
import from jaclang.byllm.config_loader { get_byllm_config, reset_byllm_config }
import from jaclang.byllm.telemetry { register_llm_call_hook, unregister_llm_call_hook }
import from jaclang.byllm.types { StreamEvent }


def get_weather(city: str) -> str {
    return f"sunny in {city}";
}


def say(
    content: str,
    usage: dict[str, any] | None = None,
    finish_reason: str = "",
    fields: dict[str, any] | None = None
) -> dict[str, any] {
    return {
        "content": content,
        "tool_calls": [],
        "usage": usage,
        "finish_reason": finish_reason,
        "fields": fields or {}
    };
}


def call(
    name: str,
    args: dict[str, any],
    call_id: str = "",
    usage: dict[str, any] | None = None,
    fields: dict[str, any] | None = None
) -> dict[str, any] {
    return {
        "content": "",
        "tool_calls": [(call_id or f"call_{name}", name, json.dumps(args))],
        "usage": usage,
        "finish_reason": "",
        "fields": fields or {}
    };
}


def finish(
    output: object,
    usage: dict[str, any] | None = None,
    fields: dict[str, any] | None = None
) -> dict[str, any] {
    return call(
        "finish_tool",
        {"final_output": output},
        call_id="call_finish",
        usage=usage,
        fields=fields
    );
}


"""A stream that sends all of `reply` and then raises `error`."""
def fail(error: Exception, reply: dict[str, any]) -> dict[str, any] {
    return {"error": error, "reply": reply};
}


def _finish_reason(reply: dict[str, any]) -> str {
    return reply["finish_reason"] or ("tool_calls" if reply["tool_calls"] else "stop");
}


def _response(reply: dict[str, any]) -> any {
    tool_calls = [
        {"id": cid, "type": "function", "function": {"name": name, "arguments": args}}
        for (cid, name, args) in reply["tool_calls"]
    ];
    payload: dict[str, any] = {
        "model": "gpt-4o",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": reply["content"],
                    "tool_calls": tool_calls or None,
                    ** reply["fields"]
                },
                "finish_reason": _finish_reason(reply)
            }
        ]
    };
    if reply["usage"] {
        payload["usage"] = dict(reply["usage"]);
    }
    return litellm.ModelResponse(**payload);
}


def _chunk(
    delta: dict[str, any],
    finish_reason: str | None = None,
    usage: dict[str, any] | None = None
) -> any {
    payload: dict[str, any] = {
        "id": "chunk",
        "object": "chat.completion.chunk",
        "created": 1,
        "model": "gpt-4o",
        "choices": []
            if usage
            else [{"index": 0, "delta": delta, "finish_reason": finish_reason}]
    };
    if usage {
        payload["usage"] = usage;
    }
    return litellm.ModelResponseStream(**payload);
}


def _chunks(reply: dict[str, any], size: int) -> list[any] {
    out: list[any] = [];
    first = True;
    for (key, value) in reply["fields"].items() {
        pieces = [value[i:i + size] for i in range(0, len(value), size)]
            if isinstance(value, str)
            else [value];
        for piece in pieces {
            delta: dict[str, any] = {key: piece};
            if first {
                delta["role"] = "assistant";
            }
            out.append(_chunk(delta));
            first = False;
        }
    }
    text = reply["content"];
    for i in range(0, len(text), size) {
        delta = {"content": text[i:i + size]};
        if first {
            delta["role"] = "assistant";
        }
        out.append(_chunk(delta));
        first = False;
    }
    for (index, (cid, name, args)) in enumerate(reply["tool_calls"]) {
        frag = {
            "index": index,
            "id": cid,
            "type": "function",
            "function": {"name": name, "arguments": args}
        };
        delta = {"tool_calls": [frag]};
        if first {
            delta["role"] = "assistant";
        }
        out.append(_chunk(delta));
        first = False;
    }
    out.append(_chunk({}, _finish_reason(reply)));
    if reply["usage"] {
        out.append(_chunk({}, usage=dict(reply["usage"])));
    }
    return out;
}


"""A real `Model` whose network calls serve `replies` and record what was sent."""
obj Fake {
    has llm: Model,
        replies: list[dict[str, any]],
        seen: list[dict[str, any]] = [],
        size: int = 40;

    def _next(params: dict) -> dict[str, any] {
        self.seen.append(
            dict(params) | {"messages": list(params.get("messages") or [])}
        );
        return self.replies.pop(0);
    }

    def no_stream(params: dict) -> any {
        reply = self._next(params);
        if "error" in reply {
            raise reply["error"];
        }
        return _response(reply);
    }

    async def ano_stream(params: dict) -> any {
        return self.no_stream(params);
    }

    def with_stream(params: dict) -> any {
        reply = self._next(params);
        if "error" in reply {
            return self._failing(reply);
        }
        return iter(_chunks(reply, self.size));
    }

    def _failing(reply: dict[str, any]) -> any {
        for c in _chunks(reply["reply"], self.size) {
            yield c;
        }
        raise reply["error"];
    }

    def sent(key: str) -> list[any] {
        return [p.get(key) for p in self.seen];
    }

    def patch -> any {
        return mock.patch.multiple(
            self.llm,
            model_call_no_stream=self.no_stream,
            model_call_no_stream_async=self.ano_stream,
            model_call_with_stream=self.with_stream
        );
    }
}


def fake(replies: list[dict[str, any]], ctx_window: int = 0) -> Fake {
    return Fake(
        llm=Model(model_name="gpt-4o", ctx_window=ctx_window), replies=list(replies)
    );
}


def events_of(events: list[any], kind: str) -> list[any] {
    return [
        e
        for e in events
        if e.event_type == kind
    ];
}


def chunk_text(events: list[any]) -> str {
    return "".join([e.data.get("content", "") for e in events_of(events, "chunk")]);
}


# Not a multiple of the 200-char merge size, so a short tail is left to flush.
glob THINK: str = "REASONING " + ("step by step " * 20),
     USAGE: dict[str, any] = {
         "prompt_tokens": 10,
         "completion_tokens": 9,
         "total_tokens": 19,
         "completion_tokens_details": {"reasoning_tokens": 7}
     },
     SIGNED: dict[str, any] = {
         "type": "thinking",
         "thinking": THINK,
         "signature": "SIG"
     },
     # (label, fields, kept when streamed). litellm's stream builder drops a thinking
     # block with no text, and provider_specific_fields.
     KINDS: list[tuple[str, dict[str, any], bool]] = [
         ("reasoning text", {"reasoning_content": THINK}, True),
         (
             "signed thinking",
             {"reasoning_content": THINK, "thinking_blocks": [SIGNED]},
             True
         ),
         ("encrypted only", {"thinking_blocks": [SIGNED | {"thinking": ""}]}, False),
         (
             "provider specific",
             {"provider_specific_fields": {"reasoning_details": [{"text": THINK}]}},
             False
         ),
         ("nothing", {}, True)
     ],
     # (label, stream, logging, tools, restream after finish_tool)
     PATHS: list[tuple[str, bool, bool, bool, bool]] = [
         ("whole replies", False, False, True, False),
         ("stream", True, False, True, False),
         ("stream, finish_tool restream", True, False, True, True),
         ("stream with events", True, True, True, False),
         ("stream with events, no tools", True, True, False, False)
     ],
     FIELDS: list[str] = [
         "reasoning_content",
         "thinking_blocks",
         "reasoning_details",
         "provider_specific_fields"
     ];


"""One turn; returns the StreamEvents of a logging stream, else []."""
def turn(
    f: Fake, history: list[any], path: tuple[str, bool, bool, bool, bool], message: str
) -> list[any] {
    (_, stream, logging, tools, _) = path;
    llm = f.llm;
    def ask(msg: str) -> str by llm(
        tools=[get_weather] if tools else [],
        conversation=history,
        stream=stream,
        logging=logging
    );
    with f.patch() {
        out: any = ask(message);
        return list(out) if stream else [];
    }
}


"""The provider fields of `m`, missing ones as None."""
def pick(m: dict[str, any]) -> dict[str, any] {
    return {k: m.get(k) for k in FIELDS};
}


test "a reply's own fields are kept, sent back, streamed, counted and reported on every path" {
    def broken(record: dict[str, any]) {
        raise RuntimeError("a hook that raises must not break the call");
    }
    for path in PATHS {
        (path_name, stream, logging, tools, restream) = path;
        for (kind, fields, streams) in KINDS {
            if stream and not streams {
                continue;
            }
            label = f"{path_name}, {kind}";
            # provider_specific_fields arrive lifted onto the reply itself.
            want = dict(fields);
            want.update(want.pop("provider_specific_fields", None) or {});
            replies: list[any] = [];
            for answer in ["Paris is sunny.", "Still sunny."] {
                if tools {
                    replies.append(
                        call(
                            "get_weather", {"city": "Paris"}, fields=fields, usage=USAGE
                        )
                    );
                }
                if restream {
                    replies.append(finish(answer, fields=fields, usage=USAGE));
                }
                replies.append(say(answer, fields=fields, usage=USAGE));
            }
            calls = len(replies);
            f = fake(replies);
            records: list[dict[str, any]] = [];
            register_llm_call_hook(broken);
            register_llm_call_hook(records.append);
            history: list[any] = [];
            try {
                first = turn(f, history, path, "How is Paris?");
                held = [dict(m) for m in history];
                second = turn(f, history, path, "Still sunny?");
            } finally {
                unregister_llm_call_hook(broken);
                unregister_llm_call_hook(records.append);
            }
            # The tool really ran: a kept reply still carries a usable tool call.
            assert not tools
            or any(
                "sunny in Paris" in str(m.get("content"))
                for m in held
                if m.get("role") == "tool"
            ) , f"{label}: get_weather never ran: {held}";
            # Kept, and nothing invented.
            for m in held {
                assert m.get("role") != "assistant" or pick(m) == pick(want) , (
                    f"{label}: kept {pick(m)}, sent {want}"
                );
            }
            # Turn 2 resends turn 1 unchanged, so the provider's prompt cache matches.
            assert list(f.sent("messages")[-1])[1:1 + len(held)] == held , (
                f"{label}: turn 2 changed what turn 1 left in the history"
            );
            # One hook record per model call, with the full reply and its usage. A
            # streamed call without tools stores no reply and reports no call.
            assert len(records) == (calls if tools else 0) , f"{label}: {len(
                records
            )} records";
            assert not tools
            or [m["role"] for m in records[0]["new_messages"][:2]] == [
                "system",
                "user"
            ] , (f"{label}: the first record carries the prompt");
            for rec in records {
                usage = rec["usage"];
                got = (
                    rec["reply"].get("reasoning_content"),
                    rec["call_kind"],
                    usage.get("reasoning_tokens")
                );
                assert got == (
                    want.get("reasoning_content"),
                    usage.get("call_kind"),
                    7
                ) , (f"{label}: hook record {rec}");
            }
            if not logging {
                continue;
            }
            # Reasoning streams on its own channel, merged, before the answer.
            for evs in (first, second) {
                types_ = [e.event_type for e in evs];
                answering = False;
                for kind_ in types_ {
                    answering = answering or kind_ in ("thought", "chunk");
                    assert not (answering and kind_ == "reasoning") , (
                        f"{label}: reasoning after the answer began: {types_}"
                    );
                }
            }
            events = first + second;
            texts = [str(e.data["content"]) for e in events_of(events, "reasoning")];
            visible = chunk_text(events) + str(
                [e.data for e in events_of(events, "thought")]
            );
            assert "REASONING" not in visible , f"{label}: reasoning leaked into the answer";
            assert "".join(texts) == want.get("reasoning_content", "") * calls
            and len(texts) <= 2 * calls , f"{label}: reasoning events {texts}";
        }
    }
    before = len(records);
    turn(fake([say("ok")]), [], PATHS[0], "hi");
    assert len(records) == before , "an unregistered hook must not fire";
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
        f = fake([say("ok")]);
        llm = f.llm;
        def answer(q: str) -> str by llm(
            reasoning_effort=given[0], thinking=given[1], extra_body=given[2]
        );
        with f.patch() {
            answer("hi");
        }
        sent = f.seen[0];
        for (key, want) in zip(keys, given) {
            assert sent.get(key) == want and (want is not None or key not in sent) , (
                f"{given}: {key} sent as {sent.get(key)!r}"
            );
        }
    }
    reset_byllm_config();
    try {
        params = get_byllm_config(
            Path(__file__).parent / "fixtures" / "reasoning_config"
        ).get_call_params_config();
        assert tuple(params.get(k) for k in keys) == ("low", enabled, None) , f"jac.toml: {params}";
    } finally {
        reset_byllm_config();
    }
}


test "compaction counts reasoning, and the hook then reports the rebuilt request" {
    records: list[dict[str, any]] = [];
    def drop_reasoning(msgs: list[any], keep_recent: int) -> list[any] {
        return [
            m | {"reasoning_content": None} if isinstance(m, dict) else m for m in msgs
        ];
    }
    big = {"reasoning_content": THINK * 10};
    f = fake(
        [
            call(
                "get_weather",
                {"city": "Galle"},
                fields=big,
                usage={"prompt_tokens": 900}
            ),
            say("done")
        ],
        ctx_window=1000
    );
    llm = f.llm;
    def ask(q: str) -> str by llm(
        tools=[get_weather], threshold_ratio=0.80, on_compaction=drop_reasoning
    );
    register_llm_call_hook(records.append);
    lines: list[str] = [];
    sink = logger.add(lines.append, level="DEBUG");
    try {
        with f.patch() {
            assert ask("Find Galle") == "done";
        }
    } finally {
        logger.remove(sink);
        unregister_llm_call_hook(records.append);
    }
    text = "".join(str(x) for x in lines);
    assert "reduced message list" in text , f"dropping only reasoning is a reduction:\n{text}";
    flags = [r["after_compaction"] for r in records];
    assert flags.count(True) == 1 , f"after_compaction flags {flags}";
    rebuilt = records[flags.index(True)]["new_messages"];
    assert rebuilt[0]["role"] == "system" , f"the call after compaction reports the whole rebuilt request: {rebuilt}";
}


test "a stream litellm cannot rebuild still keeps the reasoning it carried" {
    think = {"reasoning_content": THINK};
    no_builder = RuntimeError("no builder");
    for (path, replies) in [
        (PATHS[3], [say("Paris is sunny.", fields=think)]),
        (
            PATHS[2],
            [
                finish("Paris is sunny.", fields=think),
                say("Paris is sunny.", fields=think)
            ]
        )
    ] {
        history: list[any] = [];
        with mock.patch.object(
            _byllm_llm_mod.litellm, "stream_chunk_builder", side_effect=no_builder
        ) {
            turn(fake(replies), history, path, "How is Paris?");
        }
        reply = history[-1];
        assert (reply.get("content"), reply.get("reasoning_content")) == (
            "Paris is sunny.",
            THINK
        ) , f"{path[0]}: {reply}";
    }
}


test "reasoning streams while the model is still thinking" {
    f = fake(
        [fail(ValueError("dropped"), say("", fields={"reasoning_content": THINK}))]
    );
    llm = f.llm;
    def ask(q: str) -> str by llm(stream=True, logging=True);
    seen: list[str] = [];
    with f.patch() {
        try {
            events: any = ask("hi");
            for ev in events {
                seen.append(ev.event_type);
            }
        } except ValueError { }
    }
    assert "reasoning" in seen , f"no reasoning before the stream ended: {seen}";
}


obj Place {
    has city: str;
}


test "hook records show the request as sent: the parallel hint, and a typed-output retry" {
    records: list[dict[str, any]] = [];
    hinted = fake([say("ok")]);
    hinted_llm = hinted.llm;
    def ask(q: str) -> str by hinted_llm(tools=[get_weather], parallelize=True);
    retried = fake(
        [say('{"city": '), say('{"schema_object_wrapper": {"city": "Galle"}}')]
    );
    retried_llm = retried.llm;
    def place -> Place by retried_llm();
    register_llm_call_hook(records.append);
    try {
        with hinted.patch() {
            ask("hi");
        }
        with retried.patch() {
            assert place().city == "Galle";
        }
    } finally {
        unregister_llm_call_hook(records.append);
    }
    system = records[0]["new_messages"][0];
    assert "scheduling rules" in str(system["content"]) , f"system prompt recorded as {system}";
    retry = records[-1];
    assert retry["after_compaction"]
    and "output parser reported" in str(retry["new_messages"]) , (
        f"the retry record misses its feedback: {retry}"
    );
}

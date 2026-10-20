"""A model's reasoning, and any other field a provider puts on its reply: kept, sent
back, streamed, counted and reported, whatever path the tool loop takes."""

import from pathlib { Path }
import from unittest { mock }
import jaclang.byllm.llm as _byllm_llm_mod;
import from jaclang.byllm.lib { MockLLM }
import from jaclang.byllm.config_loader { get_byllm_config, reset_byllm_config }
import from jaclang.byllm.telemetry { register_llm_call_hook, unregister_llm_call_hook }
import from support {
    call,
    capture_loguru,
    chunk_text,
    events_of,
    finish,
    fixture_path,
    say
}


def get_weather(city: str) -> str {
    return f"sunny in {city}";
}


# Not a multiple of the 200-char merge size, so a short tail is left to flush.
glob THINK: str = "REASONING " + ("step by step " * 20),
     USAGE: dict[str, any] = {
         "prompt_tokens": 10,
         "completion_tokens": 9,
         "total_tokens": 19,
         "completion_tokens_details": {"reasoning_tokens": 7}
     },
     # (label, fields, kept when streamed). litellm's stream builder drops a thinking
     # block with no text, and provider_specific_fields.
     KINDS: list[tuple[str, dict[str, any], bool]] = [
         ("reasoning text", {"reasoning_content": THINK}, True),
         (
             "signed thinking",
             {
                 "reasoning_content": THINK,
                 "thinking_blocks": [
                     {"type": "thinking", "thinking": THINK, "signature": "SIG"}
                 ]
             },
             True
         ),
         (
             "encrypted only",
             {
                 "thinking_blocks": [
                     {"type": "thinking", "thinking": "", "signature": "SIG"}
                 ]
             },
             False
         ),
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
     ];


"""One turn; returns the StreamEvents of a logging stream, else []."""
def turn(llm: MockLLM, history: list[any], path: tuple, message: str) -> list[any] {
    (_, stream, logging, tools, _) = path;
    def ask(msg: str) -> str by llm(
        tools=[get_weather] if tools else [],
        conversation=history,
        stream=stream,
        logging=logging
    );
    out: any = ask(message);
    return list(out) if stream else [];
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
            want = {
                k: v
                for (k, v) in fields.items()
                if k != "provider_specific_fields"
            }
                | (fields.get("provider_specific_fields") or {});
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
            llm = MockLLM(outputs=replies, chunk_size=40);
            records: list[dict[str, any]] = [];
            register_llm_call_hook(broken);
            register_llm_call_hook(records.append);
            history: list[any] = [];
            try {
                first = turn(llm, history, path, "How is Paris?");
                held = [dict(m) for m in history];
                second = turn(llm, history, path, "Still sunny?");
            } finally {
                unregister_llm_call_hook(broken);
                unregister_llm_call_hook(records.append);
            }
            # A streamed call without tools stores no reply and reports no call.
            if not tools {
                assert not records , f"{label}: unexpected records";
            }
            # Kept, and nothing invented.
            for reply in [
                m
                for m in held
                if m.get("role") == "assistant"
            ] {
                got = {
                    k: reply.get(k)
                    for k in set(want)
                        | {
                            "reasoning_content",
                            "thinking_blocks",
                            "provider_specific_fields"
                        }
                };
                assert got
                    == want
                        | {
                            k: None
                            for k in got
                            if k not in want
                        } , (f"{label}: kept {got}, sent {want}");
            }
            # Turn 2 resends turn 1 unchanged, so the provider's prompt cache matches.
            assert list(llm.sent("messages")[-1])[1:1 + len(held)] == held , (
                f"{label}: turn 2 changed what turn 1 left in the history"
            );
            # One hook record per model call, with the full reply and its usage.
            assert len(records) == (calls if tools else 0) , (
                f"{label}: {calls} calls, {len(records)} records"
            );
            assert not tools
                or [m.get("role") for m in records[0]["new_messages"]][:2]
                    == ["system", "user"] , (
                f"{label}: the first record carries the prompt"
            );
            for rec in records {
                assert rec["reply"].get("reasoning_content")
                    == want.get("reasoning_content") , (
                    f"{label}: hook reply {rec['reply']}"
                );
                assert rec["call_kind"] == rec["usage"].get("call_kind") , (
                    f"{label}: hook says {rec['call_kind']}, usage says {rec[
                        'usage'
                    ].get(
                        'call_kind'
                    )}"
                );
                assert rec["usage"].get("reasoning_tokens") == 7 , f"{label}: usage {rec[
                    'usage'
                ]}";
            }
            # Reasoning streams on its own channel, merged, never in the answer.
            if logging {
                for evs in (first, second) {
                    kinds = [e.event_type for e in evs];
                    shown = [
                        i
                        for (i, k) in enumerate(kinds)
                        if k in ("thought", "chunk")
                    ];
                    thought_at = [
                        i
                        for (i, k) in enumerate(kinds)
                        if k == "reasoning"
                    ];
                    assert not shown or not thought_at or max(thought_at) < shown[0] , (
                        f"{label}: reasoning arrived after the answer began: {kinds}"
                    );
                }
                events = first + second;
                texts = [
                    str(e.data["content"]) for e in events_of(events, "reasoning")
                ];
                visible = chunk_text(events)
                    + str([e.data for e in events_of(events, "thought")]);
                assert "REASONING" not in visible , f"{label}: reasoning leaked into the answer";
                assert "".join(texts) == want.get("reasoning_content", "") * calls , (
                    f"{label}: reasoning events {texts}"
                );
                assert len(texts) <= 2 * calls , f"{label}: {len(
                    texts
                )} events, not merged";
            }
        }
    }
    before = len(records);
    turn(MockLLM(outputs=[say("ok")]), [], PATHS[0], "hi");
    assert len(records) == before , "an unregistered hook must not fire";
}


test "reasoning params reach the model only when set, from by llm() or jac.toml" {
    enabled = {"type": "enabled"};
    for (label, effort, thinking, extra) in [
        ("effort", "low", None, None),
        ("thinking", None, enabled, None),
        ("extra_body", None, None, {"thinking": enabled}),
        ("none set", None, None, None)
    ] {
        llm = MockLLM(outputs=[say("ok")]);
        def answer(q: str) -> str by llm(
            reasoning_effort=effort, thinking=thinking, extra_body=extra
        );
        answer("hi");
        sent = llm.seen[0];
        for (key, want) in [
            ("reasoning_effort", effort),
            ("thinking", thinking),
            ("extra_body", extra)
        ] {
            assert sent.get(key) == want and (want is not None or key not in sent) , (
                f"{label}: {key} sent as {sent.get(key)!r}"
            );
        }
    }
    reset_byllm_config();
    try {
        params = get_byllm_config(
            Path(fixture_path("reasoning_config"))
        ).get_call_params_config();
        assert (
            params.get("reasoning_effort"),
            params.get("thinking"),
            params.get("extra_body")
        )
            == ("low", enabled, None) , f"jac.toml: {params}";
    } finally {
        reset_byllm_config();
    }
}


test "compaction counts reasoning, and the hook then reports the rebuilt request" {
    records: list[dict[str, any]] = [];
    def drop_reasoning(msgs: list[any], keep_recent: int) -> list[any] {
        return [
            {
                k: v
                for (k, v) in m.items()
                if k != "reasoning_content"
            }
                if isinstance(m, dict)
                else m for m in msgs
        ];
    }
    llm = MockLLM(
        ctx_window=1000,
        outputs=[
            call(
                "get_weather",
                {"city": "Galle"},
                fields={"reasoning_content": THINK * 10},
                usage={"prompt_tokens": 900}
            ),
            say("done")
        ]
    );
    def ask(q: str) -> str by llm(
        tools=[get_weather], threshold_ratio=0.80, on_compaction=drop_reasoning
    );
    register_llm_call_hook(records.append);
    try {
        with capture_loguru() as logs {
            assert ask("Find Galle") == "done";
        }
    } finally {
        unregister_llm_call_hook(records.append);
    }
    assert "reduced message list" in logs.text() , f"dropping only reasoning is a reduction:\n{logs.text()}";
    after = [
        r
        for r in records
        if r["after_compaction"]
    ];
    assert len(after) == 1 and after[0]["new_messages"][0].get("role") == "system" , (
        f"the call after compaction reports the whole rebuilt request: {after}"
    );
}


test "a stream litellm cannot rebuild still keeps the reasoning it carried" {
    history: list[any] = [];
    llm = MockLLM(
        outputs=[say("Paris is sunny.", fields={"reasoning_content": THINK})]
    );
    with mock.patch.object(
        _byllm_llm_mod.litellm,
        "stream_chunk_builder",
        side_effect=RuntimeError("no builder")
    ) {
        turn(llm, history, PATHS[3], "How is Paris?");
    }
    reply = [
        m
        for m in history
        if m.get("role") == "assistant"
    ][-1];
    assert (reply.get("content"), reply.get("reasoning_content"))
        == ("Paris is sunny.", THINK) , (
        f"the streamed text and reasoning are both the reply: {reply}"
    );
}

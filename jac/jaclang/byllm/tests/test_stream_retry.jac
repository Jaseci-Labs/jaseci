"""A streamed answer that drops mid-stream and is retried: what the caller ends up with."""

import asyncio;
import from litellm.exceptions { InternalServerError }
import from jaclang.byllm.types { IterationAction, IterationContext, StreamEvent }
import from jaclang.byllm.lib { MockLLM }
import from support { call, event_types, fail, finish, mk_run, say }


def save_data(name: str) -> str {
    return name;
}


def _dropped -> Exception {
    return InternalServerError(message="boom", llm_provider="openai", model="gpt-4o");
}


def _summarize_after_first(ctx: IterationContext) -> IterationAction {
    return IterationAction.ABORT_WITH_SUMMARY;
}


def _reply_text(msg: any) -> str {
    return str(msg.get("content", "") if isinstance(msg, dict) else msg.content);
}


"""The events of one `logging=True` turn, and the runtime whose conversation it wrote."""
def _events_turn(ending: str, retry: any) -> tuple[list[StreamEvent], any] {
    attempts = [fail(_dropped(), content="partial text here", after=1), retry];
    resp_type = int if ending == "recovery" else str;
    tools = [] if ending == "none" else [save_data];
    params: dict[str, any] = {};
    if ending == "cutoff" {
        params["max_react_iterations"] = 1;
    } elif ending == "abort" {
        params["on_iteration"] = _summarize_after_first;
    }
    lead = {
        "finish": [finish("COMMITTED")],
        "cutoff": [call("save_data", {"name": "x"})],
        "abort": [call("save_data", {"name": "x"})],
        "recovery": [say("seven"), finish(7)],
        "none": []
    };
    llm = MockLLM(outputs=lead[ending] + attempts);
    mt = mk_run(resp_type=resp_type, tools=tools, stream=True, call_params=params);
    return (list(llm._invoke_streaming(mt)), mt);
}


test "a retried answer replaces the attempt that failed" {
    rows = [
        ("after finish_tool", "finish", say("full answer"), "full answer"),
        ("after finish_tool, retry empty", "finish", say(""), "COMMITTED"),
        (
            "after finish_tool, retry cut off",
            "finish",
            say("", finish_reason="length"),
            "COMMITTED"
        ),
        ("at max_react_iterations", "cutoff", say("full answer"), "full answer"),
        ("on ABORT_WITH_SUMMARY", "abort", say("full answer"), "full answer"),
        ("after recovery", "recovery", say("full answer"), "full answer"),
        ("with no tools", "none", say("full answer"), "full answer"),
        ("with no tools, retry empty", "none", say(""), "")
    ];
    for (label, ending, retry, expected) in rows {
        (events, mt) = _events_turn(ending, retry);
        shown = "";
        discarded = "";
        for ev in events {
            if ev.event_type == "stream_reset" {
                discarded += shown;
                shown = "";
            } elif ev.event_type == "chunk" {
                shown += ev.data.get("content", "");
            }
        }
        assert discarded == "partial text" , (
            f"{label}: the failed attempt must be shown, then reset, got {discarded!r}"
        );
        assert shown == expected , f"{label}: the caller ends with {shown!r}";
        if ending != "none" {
            stored = _reply_text(mt.messages[-1]);
            assert stored == expected , f"{label}: the conversation stored {stored!r}";
        }
    }
}


"""What a plain `stream=True` call delivered before it ended, and the error that ended it."""
def _plain_turn(ending: str, attempts: list[any]) -> tuple[str, any] {
    lead = [finish("COMMITTED")] if ending == "finish" else [];
    tools = [save_data] if ending == "finish" else [];
    llm = MockLLM(outputs=lead + attempts);
    parts: list[str] = [];
    if ending == "async" {
        async def ask(task: str) -> str by llm(stream=True);

        async def drain -> any {
            try {
                stream: any = await ask("go");
                async for token in stream {
                    parts.append(token);
                }
            } except Exception as e {
                return e;
            }
            return None;
        }
        error = asyncio.run(drain());
        return ("".join(parts), error);
    }

    def ask(task: str) -> str by llm(tools=tools, stream=True);

    try {
        for token in ask("go") {
            parts.append(token);
        }
    } except Exception as e {
        return ("".join(parts), e);
    }
    return ("".join(parts), None);
}


test "a plain stream never replays text it has already delivered" {
    rows = [
        (
            "dropped before any text",
            [fail(_dropped()), say("full answer")],
            "full answer",
            False
        ),
        (
            "dropped after text",
            [
                fail(_dropped(), content="partial text here", after=1),
                say("full answer")
            ],
            "partial text",
            True
        )
    ];
    for ending in ["none", "finish", "async"] {
        for (label, attempts, expected, fails) in rows {
            (text, error) = _plain_turn(ending, attempts);
            where = f"{ending} / {label}";
            assert text == expected , f"{where}: the caller received {text!r}";
            if fails {
                assert isinstance(error, InternalServerError) , (
                    f"{where}: the drop must reach the caller, got {error!r}"
                );
            } else {
                assert error is None , f"{where}: unexpected {error!r}";
            }
        }
    }
}


test "a typed call with a stream_handler parses only the retried attempt" {
    seen: list[StreamEvent] = [];
    llm = MockLLM(
        outputs=[fail(_dropped(), content="[9, 9, 9, 9, 9, 9", after=1), [1, 2]]
    );

    def pick(options: str) -> list[int] by llm(
        stream=True, stream_handler=seen.append
    );

    assert pick("go") == [1, 2];
    kinds = event_types(seen);
    assert "stream_reset" in kinds , f"the handler was never told to discard: {kinds}";
    assert kinds.index("stream_reset") > kinds.index("chunk") , (
        f"the failed attempt must reach the handler before the reset: {kinds}"
    );
}

"""A finish_tool batched with other tools never leaves a tool call without its result."""

import from jaclang.byllm.exceptions { FinishToolError }
import from jaclang.byllm.types { ToolCallResultMsg }
import from litellm.types.utils {
    ChatCompletionMessageToolCall,
    Function,
    Message as LiteLLMMessage
}
import from jaclang.byllm.lib { MockLLM }
import from support {
    calls,
    chunk_text,
    finish,
    mk_run,
    say,
    sent_messages,
    stream_events
}

glob RAN: list[str] = [],
     MODES: list[str] = ["plain", "stream", "events", "handler"];


def mul(a: int, b: int) -> int {
    RAN.append(f"mul({a},{b})");
    return a * b;
}


def _call(a: int, b: int, call_id: str) -> tuple[any, ...] {
    return ("mul", {"a": a, "b": b}, call_id);
}


def _finish_entry(call_id: str = "cf") -> tuple[any, ...] {
    return ("finish_tool", {"final_output": "6"}, call_id);
}


"""The ids of tool calls that no tool message in `messages` answers."""
def unanswered(messages: list[any]) -> list[str] {
    asked = [str(tc["id"]) for m in messages for tc in (m.get("tool_calls") or [])];
    answered = [
        str(m.get("tool_call_id"))
        for m in messages
        if m.get("role") == "tool"
    ];
    return [
        a
        for a in asked
        if a not in answered
    ];
}


def tool_results(messages: list[any]) -> dict[str, str] {
    return {
        str(m.get("tool_call_id")): str(m.get("content"))
        for m in messages
        if m.get("role") == "tool"
    };
}


def tool_names(messages: list[any]) -> list[str] {
    calls_made = [
        str(tc["function"]["name"]) for m in messages
        for tc in (m.get("tool_calls") or [])
    ];
    return calls_made
        + [
            str(m.get("name"))
            for m in messages
            if m.get("role") == "tool"
        ];
}


"""The text the caller gets from one call, in whichever way it consumes the reply."""
def _answer(out: any, mode: str) -> str {
    if mode == "stream" {
        return "".join(out);
    }
    if mode == "events" {
        return chunk_text(stream_events(out));
    }
    return out;
}


"""Two turns over one conversation: `entries` as the model sent them, then a lone finish.

`events` and `handler` run the event loop, `plain` and `stream` the other one.
"""
def two_turns(entries: list[any], mode: str, parallel: bool) -> tuple[any, ...] {
    RAN.clear();
    history: list[dict[str, any]] = [];
    streaming = mode != "plain";
    replies = [calls(entries)]
        + ([say("FINAL")] if streaming else [])
        + [finish("two")]
        + ([say("TWO")] if streaming else []);
    llm = MockLLM(outputs=replies);

    def ask(q: str) -> str by llm(
        tools=[mul],
        conversation=history,
        stream=streaming,
        logging=(mode == "events"),
        stream_handler=([].append if mode == "handler" else None),
        parallelize=parallel
    );

    first = _answer(ask("first"), mode);
    ran = list(RAN);
    second = _answer(ask("second"), mode);
    return (llm, history, first, second, ran);
}


glob LAYOUTS: list[tuple[any, ...]] = [
         ("alone", [_finish_entry()], [], []),
         ("last", [_call(2, 3, "c1"), _finish_entry()], ["mul(2,3)"], []),
         (
             "middle",
             [_call(2, 3, "c1"), _finish_entry(), _call(4, 5, "c2")],
             ["mul(2,3)"],
             ["c2"]
         ),
         (
             "first",
             [_finish_entry(), _call(2, 3, "c1"), _call(4, 5, "c2")],
             [],
             ["c1", "c2"]
         ),
         (
             "two finishes",
             [_call(2, 3, "c1"), _finish_entry(), _finish_entry("cf2")],
             ["mul(2,3)"],
             []
         ),

     ];


test "no call is left unanswered, wherever finish_tool sits in the batch" {
    for (label, entries, ran_expected, skipped) in LAYOUTS {
        for mode in MODES {
            for parallel in [False, True] {
                where = f"{label} mode={mode} parallelize={parallel}";
                (llm, history, first, second, ran) = two_turns(entries, mode, parallel);

                assert ran == ran_expected , f"{where}: ran {ran}, expected {ran_expected}";
                expected = ("6", "two") if mode == "plain" else ("FINAL", "TWO");
                assert (first, second) == expected , f"{where}: got {(
                    first,
                    second
                )!r}";

                for n in range(len(llm.seen)) {
                    dangling = unanswered(sent_messages(llm, n));
                    assert dangling == [] , f"{where}: request {n} leaves {dangling} unanswered";
                }
                assert unanswered(history) == [] , (
                    f"{where}: the saved conversation leaves {unanswered(
                        history
                    )} unanswered"
                );
                assert "finish_tool" not in tool_names(history) , (
                    f"{where}: finish_tool is plumbing and leaked into the saved conversation"
                );
                saved = tool_results(history);
                for call_id in skipped {
                    assert "not executed" in saved.get(call_id, "").lower() , (
                        f"{where}: {call_id} needs a not-executed result, saved {saved}"
                    );
                }
            }
        }
    }
}


def _tool_call_dict(call_id: str) -> dict[str, any] {
    return {
        "id": call_id,
        "type": "function",
        "function": {"name": "mul", "arguments": "{}"}
    };
}


"""An assistant message calling every id in `call_ids`, then a result for each in `answered`."""
def _turn_messages(
    call_ids: list[str], answered: list[str], content: str = ""
) -> list[any] {
    asked = {
        "role": "assistant",
        "content": content,
        "tool_calls": [_tool_call_dict(cid) for cid in call_ids]
    };
    results = [
        ToolCallResultMsg(content="r", tool_call_id=cid, name="mul") for cid in answered
    ];
    return [{"role": "user", "content": "go"}, asked] + results;
}


"""The history byLLM would save for `messages`, as the dicts that land in the list."""
def _persisted(messages: list[any]) -> list[dict[str, any]] {
    run = mk_run(tools=[mul], messages=messages);
    return [
        m if isinstance(m, dict) else m.to_dict() for m in run.get_history_for_persist()
    ];
}


test "a turn cut short before its results arrived does not save the dangling call" {
    for (label, call_ids, answered, content, kept_ids, kept_msgs) in [
        ("half answered", ["a", "b"], ["a"], "", ["a"], 3),
        ("none answered, no text", ["a"], [], "", [], 1),
        ("none answered, with text", ["a"], [], "thinking", [], 2),
        ("all answered", ["a", "b"], ["a", "b"], "", ["a", "b"], 4)
    ] {
        messages = _turn_messages(call_ids, answered, content);
        persisted = _persisted(messages);

        assert unanswered(persisted) == [] , (
            f"{label}: saved {unanswered(persisted)} without a result"
        );
        assert len(persisted) == kept_msgs , f"{label}: expected {kept_msgs} messages, got {persisted}";
        saved_ids = [
            str(tc["id"]) for m in persisted for tc in (m.get("tool_calls") or [])
        ];
        assert saved_ids == kept_ids , f"{label}: kept calls {saved_ids}, expected {kept_ids}";
        assert [tc["id"] for tc in messages[1]["tool_calls"]] == call_ids , (
            f"{label}: the run's own assistant message was edited"
        );
    }
}


test "an earlier turn's result does not answer a call that reuses its id" {
    cut_short = {
        "role": "assistant",
        "content": "",
        "tool_calls": [_tool_call_dict("c1")]
    };
    persisted = _persisted(
        _turn_messages(["c1"], ["c1"])
            + [{"role": "user", "content": "again"}, cut_short]
    );

    assert unanswered(persisted) == [] , f"a reused id was taken as answered: {persisted}";
    assert [m["role"] for m in persisted] == ["user", "assistant", "tool", "user"] , (
        f"only the cut-short call should be gone, got {persisted}"
    );
}


test "a call with no id is left alone, since no result can be matched to it" {
    anonymous = _turn_messages([""], [""]);
    assert len(_persisted(anonymous)) == len(anonymous) , "an id-less call was dropped";
}


test "a message object is edited on a copy, like a dict" {
    asked = [
        ChatCompletionMessageToolCall(
            id=cid, function=Function(name=name, arguments="{}")
        ) for (cid, name) in [("a", "mul"), ("f1", "finish_tool"), ("z", "mul")]
    ];
    live = LiteLLMMessage(role="assistant", content="", tool_calls=asked);
    run = mk_run(
        tools=[mul],
        messages=[
            live,
            ToolCallResultMsg(content="r", tool_call_id="a", name="mul"),
            ToolCallResultMsg(content="r", tool_call_id="f1", name="finish_tool")
        ]
    );
    persisted = run.get_history_for_persist();

    assert [tc.id for tc in persisted[0].tool_calls] == ["a"] , (
        f"expected only the answered real call, got {persisted[0].tool_calls}"
    );
    assert [tc.id for tc in live.tool_calls] == ["a", "f1", "z"] , (
        f"the run's own message was edited: {live.tool_calls}"
    );
}


test "a failed finish_tool retries with the call after it answered" {
    for mode in MODES {
        RAN.clear();
        attempts = [0];

        def finish_tool(final_output: str) -> str {
            attempts[0] += 1;
            if attempts[0] == 1 {
                raise FinishToolError("simulated finish invocation failure");
            }
            return final_output;
        }

        streaming = mode != "plain";
        llm = MockLLM(
            outputs=[calls([_finish_entry(), _call(4, 5, "c2")]), finish("second try")]
                + ([say("FINAL")] if streaming else [])
        );

        def ask(q: str) -> str by llm(
            tools=[mul, finish_tool],
            stream=streaming,
            logging=(mode == "events"),
            stream_handler=([].append if mode == "handler" else None)
        );

        answer = _answer(ask("go"), mode);
        retry = sent_messages(llm, 1);
        results = tool_results(retry);

        assert unanswered(retry) == [] , f"mode={mode}: the retry leaves {unanswered(
            retry
        )} unanswered";
        assert "not executed" in results.get("c2", "").lower() , (
            f"mode={mode}: the trailing call needs its not-executed result: {results}"
        );
        assert "simulated finish invocation failure" in results.get("cf", "") , (
            f"mode={mode}: the failed finish call needs its error result: {results}"
        );
        assert RAN == [] , f"mode={mode}: a call after finish_tool ran: {RAN}";
        assert answer == ("second try" if mode == "plain" else "FINAL") , (
            f"mode={mode}: got {answer!r}"
        );
    }
}

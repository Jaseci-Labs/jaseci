"""A finish_tool batched with other tools never leaves a tool call without its result.

A model may put finish_tool anywhere in a batch. The calls before it run, the calls
after it are answered as not executed, finish_tool itself is plumbing and is not
persisted, and every other call keeps its result in the saved conversation.
"""

import from jaclang.byllm.exceptions { FinishToolError }
import from jaclang.byllm.types { ToolCallResultMsg }
import from litellm.types.utils {
    ChatCompletionMessageToolCall,
    Function,
    Message as LiteLLMMessage
}
import from jaclang.byllm.lib { MockLLM }
import from support { calls, finish, mk_run, say, sent_messages }

glob RAN: list[str] = [];


def mul(a: int, b: int) -> int {
    RAN.append(f"mul({a},{b})");
    return a * b;
}


"""A tool call with the given id."""
def _call(a: int, b: int, call_id: str) -> tuple[any, ...] {
    return ("mul", {"a": a, "b": b}, call_id);
}


def _finish_entry(call_id: str = "cf") -> tuple[any, ...] {
    return ("finish_tool", {"final_output": "6"}, call_id);
}


"""The ids of tool calls that no tool message in `messages` answers."""
def unanswered(messages: list[any]) -> list[str] {
    asked: list[str] = [];
    answered: list[str] = [];
    for m in messages {
        for tc in (m.get("tool_calls") or []) {
            asked.append(str(tc["id"]));
        }
        if m.get("role") == "tool" {
            answered.append(str(m.get("tool_call_id")));
        }
    }
    return [
        a
        for a in asked
        if a not in answered
    ];
}


"""Every tool name that appears in `messages`, as a call or as a result."""
def tool_names(messages: list[any]) -> list[str] {
    names: list[str] = [];
    for m in messages {
        for tc in (m.get("tool_calls") or []) {
            names.append(str(tc["function"]["name"]));
        }
        if m.get("role") == "tool" {
            names.append(str(m.get("name")));
        }
    }
    return names;
}


"""Two turns over one conversation. Turn one is `entries`, turn two a lone finish."""
def two_turns(entries: list[any], stream: bool, parallel: bool) -> tuple[any, ...] {
    RAN.clear();
    history: list[dict[str, any]] = [];
    replies = [calls(entries)]
        + ([say("FINAL")] if stream else [])
        + [finish("two")]
        + ([say("TWO")] if stream else []);
    llm = MockLLM(outputs=replies);

    def ask(q: str) -> str by llm(
        tools=[mul], conversation=history, stream=stream, parallelize=parallel
    );

    first = ask("first");
    first_text = "".join(first) if stream else first;
    ran = list(RAN);
    turn_two_request = len(llm.seen);
    second = ask("second");
    second_text = "".join(second) if stream else second;
    return (llm, history, first_text, second_text, ran, turn_two_request);
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
             ["cf2"]
         ),

     ];


test "no call is left unanswered, wherever finish_tool sits in the batch" {
    for (label, entries, ran_expected, skipped) in LAYOUTS {
        for stream in [False, True] {
            for parallel in [False, True] {
                where = f"{label} stream={stream} parallelize={parallel}";
                (llm, history, first, second, ran, _next) = two_turns(
                    entries, stream, parallel
                );

                assert ran == ran_expected , f"{where}: ran {ran}, expected {ran_expected}";
                assert first == ("FINAL" if stream else "6") , f"{where}: got {first!r}";
                assert second == ("TWO" if stream else "two") , f"{where}: got {second!r}";

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
                    f"{where}: finish_tool is plumbing and leaked into {tool_names(
                        history
                    )}"
                );
            }
        }
    }
}


test "a call after finish_tool is answered as not executed, and kept that way" {
    for stream in [False, True] {
        for parallel in [False, True] {
            where = f"stream={stream} parallelize={parallel}";
            (llm, history, _first, _second, ran, turn_two) = two_turns(
                [_call(2, 3, "c1"), _finish_entry(), _call(4, 5, "c2")],
                stream,
                parallel
            );
            assert "mul(4,5)" not in ran , f"{where}: a call after finish_tool ran: {ran}";

            results = {
                str(m.get("tool_call_id")): str(m.get("content"))
                for m in sent_messages(llm, turn_two)
                if m.get("role") == "tool"
            };
            assert results.get("c1") == "6" , f"{where}: the real result changed: {results}";
            assert "not executed" in results.get("c2", "").lower() , (
                f"{where}: the skipped call needs an explicit answer, got {results}"
            );
            saved = {
                str(m.get("tool_call_id")): str(m.get("content"))
                for m in history
                if m.get("role") == "tool"
            };
            assert saved == results , f"{where}: saved {saved} differs from sent {results}";
        }
    }
}


"""One assistant message with a call per id, then a result for each id in `answered`."""
def _turn_messages(
    call_ids: list[str], answered: list[str], content: str = ""
) -> list[any] {
    msgs: list[any] = [
        {"role": "user", "content": "go"},
        {
            "role": "assistant",
            "content": content,
            "tool_calls": [
                {
                    "id": cid,
                    "type": "function",
                    "function": {
                        "name": "finish_tool" if cid.startswith("f") else "mul",
                        "arguments": "{}"
                    }
                } for cid in call_ids
            ]
        }
    ];
    for cid in answered {
        msgs.append(
            ToolCallResultMsg(
                content="r",
                tool_call_id=cid,
                name="finish_tool" if cid.startswith("f") else "mul"
            )
        );
    }
    return msgs;
}


test "a turn that ended before its results arrived does not persist the dangling call" {
    for (label, call_ids, answered, content, kept_ids, kept_msgs) in [
        ("half answered", ["a", "b"], ["a"], "", ["a"], 3),
        ("none answered, no text", ["a"], [], "", [], 1),
        ("none answered, with text", ["a"], [], "thinking", [], 2),
        ("all answered", ["a", "b"], ["a", "b"], "", ["a", "b"], 4),
        ("finish and a real call", ["a", "f1"], ["a"], "", ["a"], 3)
    ] {
        run = mk_run(tools=[mul], messages=_turn_messages(call_ids, answered, content));
        persisted = [
            m.to_dict() if m?.to_dict else m for m in run.get_history_for_persist()
        ];
        assert unanswered(persisted) == [] , (
            f"{label}: persisted {unanswered(persisted)} without a result"
        );
        assert len(persisted) == kept_msgs , (
            f"{label}: expected {kept_msgs} messages, got {persisted}"
        );
        kept = [str(tc["id"]) for m in persisted for tc in (m.get("tool_calls") or [])];
        assert kept == kept_ids , f"{label}: kept calls {kept}, expected {kept_ids}";
    }
}


"""A tool call, as an assistant message carries it."""
def _tool_call_dict(call_id: str, name: str = "mul") -> dict[str, any] {
    return {
        "id": call_id,
        "type": "function",
        "function": {"name": name, "arguments": "{}"}
    };
}


"""The persisted history of `messages`, as the dicts that land in the caller's list."""
def _persisted(messages: list[any]) -> list[dict[str, any]] {
    run = mk_run(tools=[mul], messages=messages);
    return [
        m if isinstance(m, dict) else m.to_dict() for m in run.get_history_for_persist()
    ];
}


test "an earlier turn's result does not answer a call that reuses its id" {
    answered_turn = _turn_messages(["c1"], ["c1"]);
    cut_short = {
        "role": "assistant",
        "content": "",
        "tool_calls": [_tool_call_dict("c1")]
    };
    persisted = _persisted(
        answered_turn + [{"role": "user", "content": "again"}, cut_short]
    );

    assert unanswered(persisted) == [] , (
        f"a reused id was taken as answered: {unanswered(persisted)}"
    );
    assert [m["role"] for m in persisted] == ["user", "assistant", "tool", "user"] , (
        f"only the cut-short call should be gone, got {persisted}"
    );
}


test "a call with no id is left alone, since no result can be matched to it" {
    anonymous = _turn_messages([""], [""]);
    persisted = _persisted(anonymous);
    assert len(persisted) == len(anonymous) , f"an id-less call was dropped: {persisted}";
}


"""One turn in which finish_tool fails once while a call follows it, then succeeds."""
def _failed_finish_turn(stream: bool) -> tuple[any, ...] {
    RAN.clear();
    attempts = [0];

    def finish_tool(final_output: str) -> str {
        attempts[0] += 1;
        if attempts[0] == 1 {
            raise FinishToolError("simulated finish invocation failure");
        }
        return final_output;
    }

    replies = [calls([_finish_entry(), _call(4, 5, "c2")]), finish("second try")]
        + ([say("FINAL")] if stream else []);
    llm = MockLLM(outputs=replies);

    def ask(q: str) -> str by llm(tools=[mul, finish_tool], stream=stream);

    answer = ask("go");
    answer_text = "".join(answer) if stream else answer;
    return (llm, answer_text, list(RAN));
}


test "a failed finish_tool retries with the call after it answered" {
    for stream in [False, True] {
        (llm, answer, ran) = _failed_finish_turn(stream);
        retry = sent_messages(llm, 1);

        assert unanswered(retry) == [] , (
            f"stream={stream}: the retry request leaves {unanswered(retry)} unanswered"
        );
        results = {
            str(m.get("tool_call_id")): str(m.get("content"))
            for m in retry
            if m.get("role") == "tool"
        };
        assert "not executed" in results.get("c2", "").lower() , (
            f"stream={stream}: the trailing call needs its not-executed result: {results}"
        );
        assert "simulated finish invocation failure" in results.get("cf", "") , (
            f"stream={stream}: the failed finish call needs its error result: {results}"
        );
        assert ran == [] , f"stream={stream}: a call after finish_tool ran: {ran}";
        assert answer == ("FINAL" if stream else "second try") , (
            f"stream={stream}: got {answer!r}"
        );
    }
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


test "persisting does not edit the live messages of the run" {
    msgs = _turn_messages(["a", "f1"], ["a", "f1"]);
    run = mk_run(tools=[mul], messages=msgs);
    run.get_history_for_persist();
    live = run.messages[1];
    assert [tc["id"] for tc in live["tool_calls"]] == ["a", "f1"] , (
        f"the run's own assistant message was edited: {live}"
    );
}

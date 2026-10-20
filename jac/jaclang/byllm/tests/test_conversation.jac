"""The `conversation=<list>` kwarg: what byLLM writes back into the caller's list.

byLLM appends to the caller's list in place. The system prompt and finish_tool
plumbing are filtered out on the way; a real tool result is not.
"""

import jaclang.byllm.llm as _byllm_llm_mod;
import from unittest { mock }
import from jaclang.byllm.types { Message, MessageRole }
import from jaclang.byllm.lib { MockLLM }
import from support { call, finish, say }


def get_weather(city: str) -> str {
    return f"sunny in {city}";
}


"""Every message in `history` with the given role."""
def by_role(history: list[dict[str, any]], role: str) -> list[dict[str, any]] {
    return [
        m
        for m in history
        if m.get("role") == role
    ];
}


"""One conversation carried across two turns, sharing the caller's list."""
def ask_twice(history: list[dict[str, any]]) -> tuple[any, ...] {
    llm = MockLLM(
        outputs=[
            call("get_weather", {"city": "Paris"}),
            finish("Paris is sunny."),
            finish("Yes, still sunny in Paris.")
        ]
    );

    def ask(message: str) -> str by llm(tools=[get_weather], conversation=history);

    first = ask("How is Paris?");
    turn1_len = len(history);
    second = ask("And again?");
    return (llm, first, second, turn1_len);
}


test "the caller's list is mutated in place, not replaced" {
    history: list[dict[str, any]] = [
        {"role": "user", "content": "PRIOR_SESSION_USER_TURN"}
    ];
    before = id(history);

    ask_twice(history);

    assert id(history) == before , "write_back_conversation must mutate the caller's list";
    assert any(
        "PRIOR_SESSION_USER_TURN" in str(m.get("content", ""))
        for m in by_role(history, "user")
    ) , f"a pre-seeded dict must survive the round trip: {history}";
}


test "scaffolding and finish_tool are filtered out, a real tool result is not" {
    history: list[dict[str, any]] = [
        {"role": "user", "content": "PRIOR_SESSION_USER_TURN"}
    ];
    ask_twice(history);

    roles = [m.get("role") for m in history];
    assert "system" not in roles , f"the system prompt is scaffolding, not conversation: {roles}";

    tool_msgs = by_role(history, "tool");
    assert len(tool_msgs) == 1 , f"expected the one real tool result, got {len(
        tool_msgs
    )}";
    assert tool_msgs[0].get("name") == "get_weather" , (
        f"only finish_tool should be filtered, got name={tool_msgs[0].get('name')!r}"
    );
    assert "tool_call_id" in tool_msgs[0] , (
        f"a tool result needs its call id to be replayable: {tool_msgs[0]}"
    );
    for m in history {
        assert m.get("name") != "finish_tool" , f"finish_tool is plumbing and leaked: {m}";
    }
}


test "a second turn grows the same list and keeps every earlier message" {
    history: list[dict[str, any]] = [
        {"role": "user", "content": "PRIOR_SESSION_USER_TURN"}
    ];
    (llm, first, second, turn1_len) = ask_twice(history);

    assert first == "Paris is sunny." , f"got {first!r}";
    assert second == "Yes, still sunny in Paris." , f"got {second!r}";
    assert len(history) > turn1_len , "the second turn must append, not overwrite";

    users = by_role(history, "user");
    assert len(users) == 3 , (
        f"expected the pre-seeded turn plus two asked turns, got {len(users)}"
    );
    contents = [str(m.get("content", "")) for m in users];
    assert any("PRIOR_SESSION_USER_TURN" in c for c in contents) , (
        f"the pre-seeded message was dropped on turn 2: {contents}"
    );
    assert any("Paris" in c for c in contents) , f"turn 1's message was dropped: {contents}";
}


"""Drive one streamed turn and return what the caller saw."""
def stream_turn(llm: MockLLM, history: list[dict[str, any]], message: str) -> str {
    def ask(msg: str) -> str by llm(
        tools=[get_weather], conversation=history, stream=True
    );

    text = "";
    for tok in ask(message) {
        text += tok;
    }
    return text;
}


"""Every entry must be a dict, and the streamed answer must be among them."""
def assert_written_back(label: str, history: list[dict[str, any]], answer: str) {
    for m in history {
        assert isinstance(m, dict) , (
            f"{label}: history holds dicts, got {type(m).__name__}"
        );
    }
    assistants = [
        str(m.get("content", ""))
        for m in history
        if m.get("role") == "assistant"
    ];
    assert assistants , f"{label}: the streamed assistant message is missing";
    assert any(answer in c for c in assistants) , (
        f"{label}: the streamed answer is not in history: {assistants}"
    );
}


"""One streamed turn: a tool call, the finish call, then the answer."""
def _stream_replies(answer: str = "Paris is sunny right now.") -> list[any] {
    return [call("get_weather", {"city": "Paris"}), finish(answer), say(answer)];
}


test "a streamed answer is written back as dicts, whatever the history was seeded with" {
    # write_back has to run after the generator exhausts, and every entry is
    # persisted as a dict no matter what the caller seeded the list with.
    for (label, seed) in [
        ("empty", []),
        ("dict", [{"role": "user", "content": "PRIOR_DICT"}]),
        ("Message", [Message(role=MessageRole.USER, content="PRIOR_MESSAGE")])
    ] {
        history = list(seed);
        llm = MockLLM(outputs=_stream_replies());
        answer = stream_turn(llm, history, "How is Paris?");
        assert answer , f"{label}: the stream produced nothing";
        assert_written_back(label, history, answer);
    }
}


test "a second streamed turn grows the same history and keeps the first answer" {
    history: list[dict[str, any]] = [];
    # Distinct answers per turn: identical ones would let the second overwrite
    # the first with both assertions below still passing.
    llm = MockLLM(
        outputs=_stream_replies("Paris is sunny right now.")
            + _stream_replies("Paris is still sunny.")
    );

    first = stream_turn(llm, history, "How is Paris?");
    assert_written_back("turn 1", history, first);
    after_first = len(history);

    second = stream_turn(llm, history, "Still sunny?");
    assert second != first , f"the two turns must differ, both gave {first!r}";
    assert len(history) > after_first , (
        f"history did not grow: was {after_first}, now {len(history)}"
    );
    assert_written_back("turn 2, first answer", history, first);
    assert_written_back("turn 2, second answer", history, second);

    # Two per turn: the assistant turn that called the tool, then the answer.
    assert len(by_role(history, "assistant")) == 4 , (
        f"expected four assistant messages, got {len(by_role(history, 'assistant'))}"
    );
    assert len(by_role(history, "user")) == 2 , (
        f"expected two user messages, got {len(by_role(history, 'user'))}"
    );
}


"""Reply fields per kind of model: (label, fields, kept when streamed). litellm's stream
builder drops a thinking block with no text and `provider_specific_fields`."""
glob REPLY_FIELDS: list[tuple[str, dict[str, any], bool]] = [
         ("reasoning text", {"reasoning_content": "THINK"}, True),
         (
             "signed thinking",
             {
                 "reasoning_content": "THINK",
                 "thinking_blocks": [
                     {"type": "thinking", "thinking": "THINK", "signature": "SIG"}
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
             {"provider_specific_fields": {"reasoning_details": [{"text": "THINK"}]}},
             False
         ),
         ("nothing", {}, True)
     ];


"""One turn of a tool loop over `history`; `stream` and `logging` pick the path."""
def run_turn(
    llm: MockLLM, history: list[any], message: str, stream: bool, logging: bool
) {
    def ask(msg: str) -> str by llm(
        tools=[get_weather], conversation=history, stream=stream, logging=logging
    );
    reply: any = ask(message);
    if stream {
        for _ in reply {}
    }
}


test "the provider's own fields on a reply are kept and sent back, on every loop path" {
    for (path, stream, logging, finishes) in [
        ("whole replies", False, False, False),
        ("stream", True, False, False),
        ("stream, answer restreamed after finish_tool", True, False, True),
        ("stream with events", True, True, False)
    ] {
        for (kind, fields, streams) in REPLY_FIELDS {
            if stream and not streams {
                continue;
            }
            label = f"{path}, {kind}";
            want = {
                k: v
                for (k, v) in fields.items()
                if k != "provider_specific_fields"
            }
                | (fields.get("provider_specific_fields") or {});
            replies: list[any] = [
                call("get_weather", {"city": "Paris"}, fields=fields)
            ];
            for answer in ["Paris is sunny.", "Still sunny."] {
                if finishes {
                    replies.append(finish(answer, fields=fields));
                }
                replies.append(say(answer, fields=fields));
            }
            llm = MockLLM(outputs=replies);
            history: list[any] = [];
            run_turn(llm, history, "How is Paris?", stream, logging);
            turn1 = [dict(m) for m in history];
            assistants = by_role(turn1, "assistant");
            assert len(assistants) == 2 , f"{label}: the call and the answer: {turn1}";
            for reply in assistants {
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
            run_turn(llm, history, "Still sunny?", stream, logging);
            sent = list(llm.sent("messages")[-1]);
            assert sent[1:1 + len(turn1)] == turn1 , (
                f"{label}: turn 2 must resend turn 1 unchanged, for prompt caching"
            );
        }
    }
}


test "a stream litellm cannot rebuild still keeps the reasoning it carried" {
    history: list[any] = [];
    thought = {"reasoning_content": "THINK_RAW"};
    llm = MockLLM(outputs=[say("Paris is sunny.", fields=thought)]);
    with mock.patch.object(
        _byllm_llm_mod.litellm,
        "stream_chunk_builder",
        side_effect=RuntimeError("no builder")
    ) {
        run_turn(llm, history, "How is Paris?", True, True);
    }
    replies = by_role(history, "assistant");
    assert [r.get("content") for r in replies] == ["Paris is sunny."] , (
        f"the streamed text is the reply: {replies}"
    );
    assert replies[0].get("reasoning_content") == "THINK_RAW" , (
        f"the streamed reasoning must be kept too: {replies[0]}"
    );
}

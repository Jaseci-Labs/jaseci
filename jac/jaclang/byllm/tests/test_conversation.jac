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


"""Provider fields a reply can carry, per kind of model. `stream` is False where
litellm's stream builder does not carry the field, so only whole replies are checked."""
def reply_field_rows -> list[tuple[str, dict[str, any], bool]] {
    signed = {"type": "thinking", "thinking": "THINK_SIGNED", "signature": "SIG_A"};
    sealed = {"type": "thinking", "thinking": "", "signature": "SIG_SEALED"};
    return [
        ("reasoning text", {"reasoning_content": "THINK_TEXT"}, True),
        (
            "signed thinking",
            {"reasoning_content": "THINK_SIGNED", "thinking_blocks": [signed]},
            True
        ),
        # litellm's stream builder keeps a thinking block only when it has text.
        ("encrypted only", {"thinking_blocks": [sealed]}, False),
        # Fields litellm parks under provider_specific_fields, such as OpenRouter's.
        (
            "provider specific",
            {"provider_specific_fields": {"reasoning_details": [{"text": "THINK_PS"}]}},
            False
        ),
        ("nothing", {}, True)
    ];
}


"""The ways a caller drives a tool loop, as `by llm()` kwargs."""
def loop_path_rows -> list[tuple[str, dict[str, any]]] {
    return [
        ("whole replies", {}),
        ("stream", {"stream": True}),
        (
            "stream, answer restreamed after finish_tool",
            {"stream": True, "finish": True}
        ),
        ("stream with events", {"stream": True, "logging": True})
    ];
}


"""One turn of a tool loop over `history`, whatever the path returns."""
def run_turn(llm: MockLLM, history: list[any], kwargs: dict[str, any], message: str) {
    stream = kwargs.get("stream", False);
    logging = kwargs.get("logging", False);
    if stream and logging {
        def ask_events(msg: str) -> str by llm(
            tools=[get_weather], conversation=history, stream=True, logging=True
        );
        for _ in ask_events(message) {}
    } elif stream {
        def ask_stream(msg: str) -> str by llm(
            tools=[get_weather], conversation=history, stream=True
        );
        for _ in ask_stream(message) {}
    } else {
        def ask(msg: str) -> str by llm(tools=[get_weather], conversation=history);
        ask(message);
    }
}


test "the provider's own fields on a reply are kept and sent back, on every loop path" {
    for (path, kwargs) in loop_path_rows() {
        for (kind, fields, streams) in reply_field_rows() {
            if kwargs.get("stream", False) and not streams {
                continue;
            }
            label = f"{path}, {kind}";
            history: list[any] = [];
            answers = [
                say("Paris is sunny.", fields=fields),
                say("Still sunny.", fields=fields)
            ];
            if kwargs.get("finish", False) {
                answers = [
                    finish("Paris is sunny.", fields=fields),
                    answers[0],
                    finish("Still sunny.", fields=fields),
                    answers[1]
                ];
            }
            llm = MockLLM(
                outputs=[call("get_weather", {"city": "Paris"}, fields=fields)]
                    + answers
            );
            run_turn(llm, history, kwargs, "How is Paris?");
            turn1 = [dict(m) for m in history];
            replies = by_role(turn1, "assistant");
            assert len(replies) == 2 , f"{label}: expected the call and the answer: {turn1}";
            for reply in replies {
                lifted = dict(fields.get("provider_specific_fields") or {});
                for (key, value) in (
                    {
                        k: v
                        for (k, v) in fields.items()
                        if k != "provider_specific_fields"
                    }
                    | lifted
                ).items() {
                    assert reply.get(key) == value , (
                        f"{label}: {key} was not kept on {reply}"
                    );
                }
                assert "provider_specific_fields" not in reply , (
                    f"{label}: litellm's own wrapper must not be sent back: {reply}"
                );
                for key in ("reasoning_content", "thinking_blocks") {
                    if key not in fields {
                        assert not reply.get(key) , (
                            f"{label}: {key} appeared from nowhere on {reply}"
                        );
                    }
                }
            }
            run_turn(llm, history, kwargs, "Still sunny?");
            sent = list(llm.sent("messages")[-1]);
            assert sent[1:1 + len(turn1)] == turn1 , (
                f"{label}: turn 2 must resend turn 1 unchanged, for prompt caching:\n"
                f"sent {sent[1:1 + len(turn1)]}\nheld {turn1}"
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
        run_turn(llm, history, {"stream": True, "logging": True}, "How is Paris?");
    }
    replies = by_role(history, "assistant");
    assert [r.get("content") for r in replies] == ["Paris is sunny."] , (
        f"the streamed text is the reply: {replies}"
    );
    assert replies[0].get("reasoning_content") == "THINK_RAW" , (
        f"the streamed reasoning must be kept too: {replies[0]}"
    );
}

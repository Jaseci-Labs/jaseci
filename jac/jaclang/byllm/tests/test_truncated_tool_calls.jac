"""A reply cut off at max_tokens never passes as a finished answer."""

import asyncio;
import json;
import litellm;
import types;
import from unittest { mock }
import from jaclang.byllm.lib { Model, OutputTruncatedError }
import from jaclang.byllm.types { StreamEvent }


def save_data(name: str, payload: str) -> str {
    return f"saved {name} ({len(payload)} bytes)";
}


def say(content: str, finish_reason: str = "stop") -> dict[str, any] {
    return {"content": content, "tool_calls": [], "finish_reason": finish_reason};
}


def call(
    name: str, args: dict[str, any], finish_reason: str = "tool_calls"
) -> dict[str, any] {
    return {
        "content": "",
        "tool_calls": [(name, json.dumps(args))],
        "finish_reason": finish_reason
    };
}


def finish(output: str) -> dict[str, any] {
    return call("finish_tool", {"final_output": output});
}


def _response(reply: dict[str, any]) -> dict[str, any] {
    tool_calls = [
        types.SimpleNamespace(
            id=f"call_{i}",
            type="function",
            function=types.SimpleNamespace(name=name, arguments=args)
        ) for (i, (name, args)) in enumerate(reply["tool_calls"])
    ];
    msg = {"role": "assistant", "content": reply["content"], "tool_calls": tool_calls};
    return {
        "choices": [{"message": msg, "finish_reason": reply["finish_reason"]}],
        "model": "gpt-4o",
        "usage": {}
    };
}


def _chunk(delta: dict[str, any], finish_reason: str | None = None) -> any {
    return litellm.ModelResponseStream(
        id="chunk",
        object="chat.completion.chunk",
        created=1,
        model="gpt-4o",
        choices=[{"index": 0, "delta": delta, "finish_reason": finish_reason}]
    );
}


def _chunks(reply: dict[str, any]) -> list[any] {
    out: list[any] = [];
    if reply["content"] {
        out.append(_chunk({"role": "assistant", "content": reply["content"]}));
    }
    for (i, (name, args)) in enumerate(reply["tool_calls"]) {
        frag = {
            "index": i,
            "id": f"call_{i}",
            "type": "function",
            "function": {"name": name, "arguments": args}
        };
        out.append(_chunk({"role": "assistant", "tool_calls": [frag]}));
    }
    out.append(_chunk({}, reply["finish_reason"]));
    return out;
}


"""Serve `replies` from `llm`'s network calls, so its own dispatch stays real."""
def _scripted(llm: Model, replies: list[dict[str, any]]) -> mock._patch {
    queue = list(replies);

    def no_stream(params: dict) -> dict[str, any] {
        return _response(queue.pop(0));
    }

    async def ano_stream(params: dict) -> dict[str, any] {
        return _response(queue.pop(0));
    }

    def with_stream(params: dict) -> any {
        return iter(_chunks(queue.pop(0)));
    }

    return mock.patch.multiple(
        llm,
        model_call_no_stream=no_stream,
        model_call_no_stream_async=ano_stream,
        model_call_with_stream=with_stream
    );
}


def _chunk_text(stream: any) -> str {
    text = "";
    for e in stream {
        assert isinstance(e, StreamEvent) , f"got {type(e).__name__}";
        if e.event_type == "chunk" {
            text += e.data.get("content", "");
        }
    }
    return text;
}


"""One scripted turn in `mode`: (answer or raised error, conversation)."""
def _turn(
    replies: list[dict[str, any]], mode: str, iters: int
) -> tuple[any, list[dict[str, any]]] {
    conv: list[dict[str, any]] = [];
    llm = Model(model_name="gpt-4o");

    def run(task: str) -> str by llm(
        tools=[save_data],
        conversation=conv,
        stream=(mode != "plain"),
        logging=(mode == "events"),
        max_react_iterations=iters
    );

    async def arun(task: str) -> str by llm(conversation=conv);

    with _scripted(llm, replies) {
        try {
            if mode == "async" {
                return (asyncio.run(arun("save a big payload")), conv);
            }
            out = run("save a big payload");
            if mode == "streamed" {
                out = "".join(out);
            } elif mode == "events" {
                out = _chunk_text(out);
            }
            return (out, conv);
        } except OutputTruncatedError as e {
            return (e, conv);
        }
    }
}


test "a reply cut off at max_tokens never passes as a finished answer" {
    rows: list[tuple[str, list[dict[str, any]], any, int]] = [
        (
            "cut-off tool call",
            [call("save_data", {"name": "x"}, finish_reason="length"), say("done")],
            "done",
            0
        ),
        (
            "empty cut-off reply",
            [say("", finish_reason="length")],
            OutputTruncatedError,
            0
        ),
        (
            "committed answer, empty cut-off restatement",
            [finish("saved it"), say("", finish_reason="length")],
            "saved it",
            0
        ),
        (
            "empty committed answer, empty cut-off restatement",
            [finish(""), say("", finish_reason="length")],
            "",
            0
        ),
        (
            "empty cut-off forced final answer",
            [
                call("save_data", {"name": "x", "payload": "y"}),
                say("", finish_reason="length")
            ],
            OutputTruncatedError,
            1
        ),
        (
            "cut-off text",
            [say("partial answer", finish_reason="length")],
            "partial answer",
            0
        ),
        ("empty stop", [say("", finish_reason="stop")], "", 0)
    ];
    for (label, replies, expected, iters) in rows {
        modes = ["plain", "streamed", "events"];
        if not any(r["tool_calls"] for r in replies) {
            modes.append("async");
        }
        for mode in modes {
            (answer, conv) = _turn(replies, mode, iters);
            where = f"{label} / {mode}";
            assert conv , f"{where}: conversation was not written back";
            if expected is OutputTruncatedError {
                assert isinstance(answer, OutputTruncatedError)
                and "max_tokens" in str(answer) , f"{where}: got {answer!r}";
            } else {
                assert answer == expected , f"{where}: got {answer!r}";
            }
            if replies[0]["tool_calls"] and replies[0]["finish_reason"] == "length" {
                results = [
                    str(m.get("content"))
                    for m in conv
                    if isinstance(m, dict) and m.get("role") == "tool"
                ];
                assert results
                and "max_tokens" in results[0]
                and "missing" not in results[0] , f"{where}: {results}";
            }
        }
    }
}

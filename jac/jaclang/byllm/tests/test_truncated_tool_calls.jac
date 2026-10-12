"""A reply truncated at max_tokens (finish_reason == "length") must never pass as a
finished answer: a cut-off tool call surfaces a max_tokens error instead of running
with partial arguments, and a reply with no text and no tool call raises
OutputTruncatedError instead of returning an empty answer."""

import asyncio;
import from jaclang.byllm.lib { Model, OutputTruncatedError }
import from support { call, chunk_text, finish, say, scripted, stream_events }


def save_data(name: str, payload: str) -> str {
    return f"saved {name} ({len(payload)} bytes)";
}


"""Run one scripted turn in `mode` and return (answer or raised error, conversation).
`iters` caps the tool loop, so the next call is the forced final answer."""
def _turn(
    replies: list[any], mode: str, iters: int
) -> tuple[any, list[dict[str, any]]] {
    conv: list[dict[str, any]] = [];
    llm = Model(model_name="gpt-4o");

    """In "events" mode this is built the way a streaming agent is: tools, streamed,
    with logging."""
    def run(task: str) -> str by llm(
        tools=[save_data],
        conversation=conv,
        stream=(mode != "plain"),
        logging=(mode == "events"),
        max_react_iterations=iters
    );

    async def arun(task: str) -> str by llm(conversation=conv);

    with scripted(llm, replies) {
        try {
            if mode == "async" {
                return (asyncio.run(arun("save a big payload")), conv);
            }
            out = run("save a big payload");
            if mode == "streamed" {
                out = "".join(out);
            } elif mode == "events" {
                out = chunk_text(stream_events(out));
            }
            return (out, conv);
        } except OutputTruncatedError as e {
            return (e, conv);
        }
    }
}


test "a reply cut off at max_tokens never passes as a finished answer" {
    # (label, replies, answer, max_react_iterations). Rows with a tool call skip the
    # async mode, which is only its own path without tools.
    rows: list[tuple[str, list[any], any, int]] = [
        # Valid JSON cut off before `payload`: the tool must not run.
        (
            "cut-off tool call",
            [call("save_data", {"name": "x"}, finish_reason="length"), say("done")],
            "done",
            0
        ),
        # The whole budget went to reasoning: no answer exists.
        (
            "empty cut-off reply",
            [say("", finish_reason="length")],
            OutputTruncatedError,
            0
        ),
        # The answer is committed; only the streamed restatement of it is empty.
        (
            "empty cut-off narration",
            [finish("saved it"), say("", finish_reason="length")],
            "saved it",
            0
        ),
        # An empty committed answer is still an answer.
        (
            "empty committed answer, empty cut-off narration",
            [finish(""), say("", finish_reason="length")],
            "",
            0
        ),
        # The tool loop hit its cap and the forced final answer came back empty.
        (
            "empty cut-off final answer",
            [
                call("save_data", {"name": "x", "payload": "y"}),
                say("", finish_reason="length")
            ],
            OutputTruncatedError,
            1
        ),
        # Cut-off text is still the model's text.
        (
            "cut-off text",
            [say("partial answer", finish_reason="length")],
            "partial answer",
            0
        ),
        # An empty reply that stopped normally is the model's choice.
        ("empty stop", [say("", finish_reason="stop")], "", 0)
    ];
    for (label, replies, expected, iters) in rows {
        modes = ["plain", "streamed", "events"];
        if not any(r.tool_calls for r in replies) {
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
            # A cut-off tool call is answered with a max_tokens error, not run.
            if replies[0].tool_calls and replies[0].finish_reason == "length" {
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

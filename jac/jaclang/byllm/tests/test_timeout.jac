"""The call timeout (#9622, #9760): one deadline for a whole `by llm()` call.

The bound starts when the call does. Every request gets what is left of it, a retry
happens only if its backoff fits in what is left, and no transport retries underneath.
"""

import asyncio;
import socket;
import threading;
import time;
import from jaclang.byllm._optdeps.litellm { litellm }
import from jaclang.byllm.deadline { CallDeadline }
import from jaclang.byllm.exceptions { LLMTimeout, RateLimitError }
import from jaclang.byllm.lib { MockLLM, Model, ModelPool }
import from jaclang.byllm.llm { _is_timeout_error, _is_transient_error }
import from jaclang.testing.requires { require_module }
import from support { call, fail, mk_run, say }


"""A local endpoint that accepts every request and never finishes one. `stall` sends
nothing; `trickle` sends headers, then one byte a second, so no read ever times out."""
obj _Endpoint {
    has mode: str = "stall",
        requests: int = 0,
        _srv: any = None,
        _conns: list[any] = [],
        _closed: bool = False,
        _thread: any = None;

    def __enter__ -> _Endpoint {
        self._srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self._srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        self._srv.bind(("127.0.0.1", 0));
        self._srv.listen(8);
        self._srv.settimeout(0.2);
        self._thread = threading.Thread(target=self._serve, daemon=True);
        self._thread.start();
        return self;
    }

    def url -> str {
        return f"http://127.0.0.1:{self._srv.getsockname()[1]}";
    }

    def _serve {
        while not self._closed {
            try {
                (conn, _addr) = self._srv.accept();
            } except Exception {
                continue;
            }
            self.requests += 1;
            self._conns.append(conn);
            threading.Thread(target=self._answer, args=(conn, ), daemon=True).start();
        }
    }

    def _answer(conn: any) -> None {
        try {
            conn.recv(65536);
            if self.mode == "trickle" {
                conn.sendall(
                    b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                    b"Content-Length: 100000\r\n\r\n"
                );
                while not self._closed {
                    time.sleep(0.5);
                    conn.sendall(b" ");
                }
            }
        } except Exception {
            return;
        }
    }

    def __exit__(*_exc: any) -> bool {
        self._closed = True;
        for conn in self._conns {
            try {
                conn.close();
            } except Exception {}
        }
        self._srv.close();
        self._thread.join(timeout=2.0);
        return False;
    }
}


def _timed(work: Callable) -> tuple[any, float] {
    raised: any = None;
    started = time.monotonic();
    try {
        work();
    } except Exception as e {
        raised = e;
    }
    return (raised, time.monotonic() - started);
}


test "a call deadline counts down from when the call starts" {
    open_ended = CallDeadline(budget=None, model="m");
    assert open_ended.remaining() is None , "no budget leaves nothing to count";
    assert open_ended.bound(90.0) == 90.0 , "no budget leaves a phase timeout alone";
    assert open_ended.allows(10.0) , "no budget allows any backoff";
    open_ended.check();

    running = CallDeadline(budget=5.0, model="m");
    assert 4.0 < running.remaining() <= 5.0 , f"got {running.remaining()}";
    assert running.bound(90.0) <= 5.0 , "a phase timeout is capped at what is left";
    assert running.bound(1.0) == 1.0 , "a shorter phase timeout is kept";
    assert running.allows(1.0) and not running.allows(10.0) , (
        "a backoff fits only inside what is left"
    );

    spent = CallDeadline(budget=5.0, model="m", started_at=time.monotonic() - 10.0);
    assert spent.bound(3.0) == 0.0 , f"got {spent.bound(3.0)}";
    assert not spent.allows(0.0) , "a spent deadline allows no retry";
    raised: any = None;
    try {
        spent.check();
    } except LLMTimeout as e {
        raised = e;
    }
    assert raised is not None , "a spent deadline must raise LLMTimeout";
    assert "within its 5s timeout" in str(raised) , f"got {str(raised)!r}";
    assert raised.model == "m" , f"got {raised.model!r}";
}


test "the bound resolves through its precedence chain" {
    via_call_params = Model(model_name="gpt-4o-mini", timeout=45.0);
    via_call_params(timeout=30.0);

    # (label, model, call-site params, expected budget) -- None means no bound at all.
    cases: list[any] = [
        ("the configured default", Model(model_name="gpt-4o-mini"), {}, 600.0),
        ("the model field", Model(model_name="gpt-4o-mini", timeout=45.0), {}, 45.0),
        ("model call_params over the field", via_call_params, {}, 30.0),
        (
            "the call site over everything",
            Model(model_name="gpt-4o-mini", timeout=45.0),
            {"timeout": 15.0},
            15.0
        ),
        ("zero drops the bound", Model(model_name="gpt-4o-mini", timeout=0.0), {}, None)
    ];
    for (label, model, call_params, expected) in cases {
        run = mk_run(stream=False, call_params=call_params);
        params = model.make_model_params(run);
        assert model._call_deadline(run).budget == expected , (
            f"{label}: got {model._call_deadline(run).budget!r}"
        );
        got = params.get("timeout");
        if expected is None {
            assert "timeout" not in params , f"{label}: got {got!r}";
        } else {
            # A request gets what is left of the call's budget, not a fresh one.
            assert expected - 1.0 < got <= expected , f"{label}: got {got!r}";
        }
    }
}


test "a stalled endpoint raises LLMTimeout at the configured bound" {
    require_module("litellm");
    with _Endpoint() as ep {
        model = Model(
            model_name="openai/gpt-4o-mini",
            api_key="sk-test",
            config={"base_url": ep.url()}
        );
        (raised, elapsed) = _timed(
            lambda { model.dispatch_no_streaming(
                mk_run(call_params={"timeout": 3.0, "stream_num_retries": 0})
            ); }
        );
        requests = ep.requests;
    }
    assert isinstance(raised, LLMTimeout) , f"got {type(raised).__name__}: {raised}";
    assert elapsed >= 3.0 , f"gave up before the bound: {elapsed:.1f}s";
    # One request, not three: litellm's own retries would land near 11s.
    assert requests == 1 , f"litellm retried underneath: {requests} requests";
    # Headroom for litellm's first-call setup; three requests would land near 11s.
    assert elapsed < 9.0 , f"the bound covered more than one request: {elapsed:.1f}s";
}


test "retries share the call's budget instead of each taking a fresh one" {
    require_module("litellm");
    with _Endpoint() as ep {
        model = Model(
            model_name="openai/gpt-4o-mini",
            api_key="sk-test",
            config={"base_url": ep.url()}
        );
        # Default retries are on; each with a fresh bound would take 2+1+2+2+2 = 9s.
        (raised, elapsed) = _timed(
            lambda { model.dispatch_no_streaming(
                mk_run(call_params={"timeout": 2.0})
            ); }
        );
        requests = ep.requests;
    }
    assert isinstance(raised, LLMTimeout) , f"got {type(raised).__name__}: {raised}";
    assert requests == 1 , f"a stall spent the budget, yet {requests} requests went out";
    assert elapsed < 7.0 , f"the call outlived its 2s bound: {elapsed:.1f}s";
}


test "no transport retries a stalled request underneath byLLM" {
    require_module("litellm");
    require_module("openai");
    # (label, model config beyond base_url, streaming)
    for (label, extra, streaming) in [
        ("litellm, streaming", {}, True),
        ("proxy, non-streaming", {"proxy": True}, False),
        ("proxy, streaming", {"proxy": True}, True)
    ] {
        with _Endpoint() as ep {
            model = Model(
                model_name="openai/gpt-4o-mini",
                api_key="sk-test",
                config={"base_url": ep.url()} | extra
            );
            run = mk_run(
                stream=streaming, call_params={"timeout": 2.0, "stream_num_retries": 0}
            );
            (raised, elapsed) = _timed(
                lambda { list(model.dispatch_streaming(run))
                    if streaming
                    else model.dispatch_no_streaming(run); }
            );
            requests = ep.requests;
        }
        assert _is_timeout_error(raised) , (
            f"{label}: got {type(raised).__name__}: {raised}"
        );
        assert requests == 1 , f"{label}: the client retried underneath, {requests} requests";
        assert elapsed < 6.0 , f"{label}: the call outlived its 2s bound: {elapsed:.1f}s";
    }
}


test "an async call stops at its deadline even while bytes keep arriving" {
    require_module("litellm");
    with _Endpoint(mode="trickle") as ep {
        model = Model(
            model_name="openai/gpt-4o-mini",
            api_key="sk-test",
            config={"base_url": ep.url()}
        );
        run = mk_run(call_params={"timeout": 2.0, "stream_num_retries": 0});
        (raised, elapsed) = _timed(
            lambda { asyncio.run(model.adispatch_no_streaming(run)); }
        );
    }
    # A read timeout alone never fires here: a byte lands every half second.
    assert isinstance(raised, LLMTimeout) , f"got {type(raised).__name__}: {raised}";
    assert "did not finish within its 2s timeout" in str(raised) , f"got {raised}";
    assert elapsed < 6.0 , f"the call outlived its 2s bound: {elapsed:.1f}s";
}


test "a retry happens only when its backoff fits in what is left" {
    transient = litellm.APIConnectionError(
        message="connection reset", llm_provider="openai", model="gpt-4o-mini"
    );
    # (label, call budget, expected requests, expected answer or error type)
    for (label, budget, requests, outcome) in [
        ("a backoff past the deadline is not taken", 0.5, 1, "APIConnectionError"),
        ("a backoff inside the deadline is taken", 30.0, 2, "recovered")
    ] {
        llm = MockLLM(outputs=[fail(transient), say("recovered")], timeout=budget);
        got = "";
        try {
            got = str(llm.dispatch_no_streaming(mk_run()).output);
        } except Exception as e {
            got = type(e).__name__;
        }
        assert got == outcome , f"{label}: got {got!r}";
        assert len(llm.seen) == requests , f"{label}: {len(llm.seen)} requests";
    }
}


test "the deadline covers every turn of a tool loop, tool time included" {
    def nap -> str {
        time.sleep(0.6);
        return "rested";
    }
    # (label, call budget, expected answer or error type, expected requests)
    for (label, budget, outcome, requests) in [
        ("a tool that runs past the deadline ends the call", 0.4, "LLMTimeout", 1),
        ("a tool loop inside the deadline finishes", 30.0, "done", 2)
    ] {
        llm = MockLLM(outputs=[call("nap"), say("done")], timeout=budget);

        """Rest, then report."""
        def rest(note: str) -> str by llm(tools=[nap]);

        got = "";
        try {
            got = str(rest("go"));
        } except Exception as e {
            got = type(e).__name__;
        }
        assert got == outcome , f"{label}: got {got!r}";
        assert len(llm.seen) == requests , f"{label}: {len(llm.seen)} requests";
    }
}


test "a stream stops at the deadline even while chunks keep arriving" {
    text = "one two three four five six seven eight nine ten eleven twelve";
    llm = MockLLM(outputs=[say(text)], chunk_size=4, timeout=0.5);

    """Recite."""
    def recite(topic: str) -> str by llm(stream=True);

    received: list[str] = [];
    raised: any = None;
    try {
        for piece in recite("numbers") {
            received.append(piece);
            time.sleep(0.2);
        }
    } except LLMTimeout as e {
        raised = e;
    }
    got = "".join(received);
    assert raised is not None , f"the stream outlived its deadline: {got!r}";
    assert got , "the stream should deliver what arrived before the deadline";
    assert got != text , "the whole answer arrived after the deadline";
}


test "a pool leaves the bound to its router" {
    # The Router already gets [byllm.fallback] timeout.
    pool = ModelPool(models=[Model(model_name="gpt-4o-mini")]);
    run = mk_run(stream=False);
    assert pool._resolve_timeout(run) is None;
    assert "timeout" not in pool.make_model_params(run);
    assert pool._call_deadline(run).remaining() is None , "a pool sets no deadline";
}


test "LLMTimeout and RateLimitError stay retryable" {
    err = LLMTimeout(message="provider stalled", model="gpt-4o-mini");
    assert isinstance(err, litellm.Timeout) , "LLMTimeout must remain a litellm.Timeout";
    assert _is_transient_error(err) , "LLMTimeout must stay transient";
    assert str(err) == "provider stalled" , f"got {str(err)!r}";
    assert err.model == "gpt-4o-mini" , f"got {err.model!r}";
    assert err.status_code == 408 , f"got {err.status_code!r}";
    # litellm's own 429 retry is off (num_retries=0), so byLLM must retry it.
    assert _is_transient_error(RateLimitError("429")) , "RateLimitError must stay transient";
}


test "the proxy transport's dropped connections and 5xx replies stay retryable" {
    require_module("openai");
    import httpx;
    import openai;
    # The OpenAI client no longer retries these itself, so byLLM has to.
    request = httpx.Request("POST", "http://127.0.0.1/v1/chat/completions");
    # (label, error, transient)
    for (label, error, transient) in [
        ("a dropped connection", openai.APIConnectionError(request=request), True),
        ("a client-side timeout", openai.APITimeoutError(request=request), True),
        (
            "a 5xx reply",
            openai.InternalServerError(
                "upstream failed",
                response=httpx.Response(502, request=request),
                body=None
            ),
            True
        ),
        (
            "a rejected request",
            openai.BadRequestError(
                "bad input", response=httpx.Response(400, request=request), body=None
            ),
            False
        )
    ] {
        assert _is_transient_error(error) == transient , (
            f"{label}: expected transient={transient}"
        );
    }
}


test "every transport's timeout type is recognised" {
    require_module("litellm");
    import httpx;
    assert _is_timeout_error(
        litellm.Timeout(message="stalled", model="gpt-4o-mini", llm_provider="openai")
    ) , "the litellm transport";
    assert _is_timeout_error(httpx.ReadTimeout("stalled")) , "the http_client transport";
    assert not _is_timeout_error(ValueError("not a timeout"));
}

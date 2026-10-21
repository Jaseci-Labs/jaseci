"""In-process WebSocket tests for function endpoints and canonical walker paths.

Uses the Starlette TestClient transport (no subprocess / uvicorn / dev server),
so it exercises the FastAPI WebSocket routes directly.
"""
import threading;
import from jaclang.runtimelib.context { ExecutionContext }
import from jaclang.scale.memory.memory_hierarchy { ScaleTieredMemory }
import from jaclang.scale.tests.scale_test_client { make_client }


"""Build a test client and register WebSocket routes on its app.

The "test" endpoint profile does not register WebSocket routes, so opt in
explicitly against the already-built app.
"""
def _ws_client -> any {
    client = make_client("test_api.jac");
    client.server.register_websocket_endpoints();
    return client;
}


test "ws function echo returns the function result envelope" {
    client = _ws_client();
    try {
        tc = client.raw_client;
        with tc.websocket_connect("/ws/function/ws_echo") as ws {
            ws.send_json({"message": "hi", "client_id": "c1"});
            resp = ws.receive_json();
            assert resp["ok"] == True , f"expected ok, got {resp}";
            data = resp["data"];
            body = data["result"]
                if isinstance(data, dict) and "result" in data
                else data;
            assert body["echo"] == "hi" , f"got {body}";
            assert body["client_id"] == "c1" , f"got {body}";
            assert body["protocol"] == "websocket" , f"got {body}";
        }
    } finally {
        client.close();
    }
}


test "ws function streaming yields chunk frames then a done frame" {
    client = _ws_client();
    try {
        tc = client.raw_client;
        with tc.websocket_connect("/ws/function/ws_stream") as ws {
            ws.send_json({"count": 3});
            frames = [];
            for _ in range(20) {
                frame = ws.receive_json();
                frames.append(frame);
                if frame.get("type") == "done" {
                    break;
                }
            }
            chunks = [
                f
                for f in frames
                if f.get("type") == "chunk"
            ];
            assert len(chunks) == 3 , f"expected 3 chunks, got {frames}";
            assert frames[-1] == {"ok": True, "type": "done"} , f"got {frames}";
        }
    } finally {
        client.close();
    }
}


test "ws walker canonical path gives each message its own memory and commits off the loop" {
    client = _ws_client();
    request_mems: list[object] = [];
    loop_threads: set[int] = set();
    commit_threads: list[int] = [];
    original_aset = ExecutionContext.aset_user_root;
    original_commit = ScaleTieredMemory.commit;

    async def tracking_aset(self: ExecutionContext, root_id: str) {
        if self._parent is not None {
            request_mems.append(self.mem);
            loop_threads.add(threading.get_ident());
        }
        await original_aset(self, root_id);
    }

    def tracking_commit(self: ScaleTieredMemory, anchor: object = None) {
        commit_threads.append(threading.get_ident());
        original_commit(self, anchor);
    }

    ExecutionContext.aset_user_root = tracking_aset;
    ScaleTieredMemory.commit = tracking_commit;
    try {
        tc = client.raw_client;
        with tc.websocket_connect("/ws/walker/EchoMessage") as ws {
            for msg in ["cw1", "cw2"] {
                ws.send_json({"message": msg, "client_id": "c2"});
                resp = ws.receive_json();
                assert resp["ok"] == True , f"expected ok, got {resp}";
            }
        }
        with tc.websocket_connect("/ws/walker/EchoMessage") as ws {
            ws.send_json({"message": "cw3", "client_id": "c2"});
            resp = ws.receive_json();
            assert resp["ok"] == True , f"expected ok, got {resp}";
        }
    } finally {
        ExecutionContext.aset_user_root = original_aset;
        ScaleTieredMemory.commit = original_commit;
        client.close();
    }

    assert len(request_mems) == 3 , f"expected 3 walker calls, got {len(request_mems)}";
    distinct = len({id(mem) for mem in request_mems});
    assert distinct == 3 , f"messages shared an L1: {distinct} memories for 3 messages";
    assert commit_threads , "the walker never committed";
    on_loop = len(
        [
            t
            for t in commit_threads
            if t in loop_threads
        ]
    );
    assert on_loop == 0 , f"{on_loop} commits ran on the event loop";
}


test "ws private function rejects a message with no token" {
    client = _ws_client();
    try {
        tc = client.raw_client;
        with tc.websocket_connect("/ws/function/ws_private_echo") as ws {
            ws.send_json({"message": "secret"});
            resp = ws.receive_json();
            assert resp["ok"] == False , f"expected rejection, got {resp}";
            assert resp["error"]["code"] == "UNAUTHORIZED" , f"got {resp}";
        }
    } finally {
        client.close();
    }
}


test "ws walker legacy path /ws/{name} still works" {
    client = _ws_client();
    try {
        tc = client.raw_client;
        with tc.websocket_connect("/ws/EchoMessage") as ws {
            ws.send_json({"message": "lw", "client_id": "c3"});
            resp = ws.receive_json();
            assert resp["ok"] == True , f"expected ok, got {resp}";
        }
    } finally {
        client.close();
    }
}

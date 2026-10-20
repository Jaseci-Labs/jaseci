"""A program hosted by the one server assembly, outside the CLI.

A desktop host, a test harness, an embedding process: each wants the same
server `jac run --serve` assembles, without the CLI around it. Three things the
assembly must offer for that, pinned here against a two-app workspace:

- `serve_background()` runs the transport on a background thread, binding
  127.0.0.1 with an ephemeral port and reporting the bound port, and the
  returned callable stops it;
- `client_dist` in the serve settings names the client bundle the server
  serves, so a host that built its own bundle serves it from wherever it put
  it, index and assets, with the SPA fallback;
- `prepare_inprocess_runtime` colocates the workspace's service apps the way
  the CLI serve flow does, so an in-process server answers `/api/<service>/...`.
"""

import json;
import os;
import shutil;
import socket;
import sys;
import tempfile;
import threading;
import time;
import urllib.request;
import from pathlib { Path }
import from unittest.mock { AsyncMock, Mock, patch }
import from jaclang { JacRuntime as Jac }
import from jaclang.compiler.driver.application { prepare_application }
import from jaclang.project.config { set_config }
import from jaclang.server { sv_client }
import from jaclang.server.net { PortInUseError }
import from jaclang.server.server { JacAPIServer }
import from jaclang.server.settings { ServeSettings }
import from jaclang.server.serving.app { ServingApp }
import from jaclang.server.serving.server { ServingServer }
import jaclang.server.serving.server as serving_module;
import jaclang.server.server as api_module;


glob _TOML: str = (
         '[project]\nname = "hosted"\ndefault-app = "web"\n\n[apps.web]\nkind = "web-app"\nentry-point = "web.main"\n\n[apps.feed]\nkind = "service"\nentry-point = "core.feed"\n'
     ),
     _WEB_SRC: str = (
         "walker:pub Hello {\n"
         "    has who: str = \"world\";\n"
         "\n"
         "    can run with Root entry {\n"
         "        report \"hello \" + self.who;\n"
         "    }\n"
         "}\n"
     ),
     _FEED_SRC: str = (
         "walker:pub Latest {\n"
         "    can run with Root entry {\n"
         "        report [\"a\", \"b\"];\n"
         "    }\n"
         "}\n"
     );


def _workspace -> str {
    tmp = tempfile.mkdtemp(prefix="jac_host_serving_");
    os.makedirs(os.path.join(tmp, "web"), exist_ok=True);
    os.makedirs(os.path.join(tmp, "core"), exist_ok=True);
    (Path(tmp) / "jac.toml").write_text(_TOML);
    (Path(tmp) / "web" / "main.jac").write_text(_WEB_SRC);
    (Path(tmp) / "core" / "feed.jac").write_text(_FEED_SRC);
    return tmp;
}


def _dist(tmp: str) -> str {
    dist = os.path.join(tmp, "bundle");
    os.makedirs(os.path.join(dist, "assets"), exist_ok=True);
    (Path(dist) / "index.html").write_text("<!doctype html><title>hosted</title>ok");
    (Path(dist) / "assets" / "app.js").write_text("console.log('hosted');");
    return dist;
}


def _get(url: str) -> tuple[int, str] {
    try {
        with urllib.request.urlopen(url, timeout=10) as r {
            return (int(r.status), r.read().decode("utf-8"));
        }
    } except urllib.error.HTTPError as e {
        return (int(e.code), e.read().decode("utf-8"));
    }
}


def _post(url: str, body: dict[str, any]) -> tuple[int, str] {
    data = json.dumps(body).encode("utf-8");
    req = urllib.request.Request(
        url, data=data, method="POST", headers={"Content-Type": "application/json"}
    );
    try {
        with urllib.request.urlopen(req, timeout=10) as r {
            return (int(r.status), r.read().decode("utf-8"));
        }
    } except urllib.error.HTTPError as e {
        return (int(e.code), e.read().decode("utf-8"));
    }
}


def _load(tmp: str, mod: str, base: str) {
    if mod in Jac.loaded_modules {
        del Jac.loaded_modules[mod];
    }
    if mod in sys.modules {
        del sys.modules[mod];
    }
    prepare_application(str(Path(base) / (mod + '.jac')), Jac.get_program(), base);
    Jac.jac_import(target=mod, base_path=base, lng="jac");
}


def _reset(tmp: str) {
    sv_client.set_consumer_app("");
    sv_client.clear_local_providers();
    set_config(None);
    Jac.set_full_target_path("");
    shutil.rmtree(tmp, ignore_errors=True);
}


glob _EVENT_WAIT: any = threading.Event.wait;


"""Bound the broken baseline's wait without changing worker startup behavior."""
def _short_startup_wait(event: any, timeout: any = None) -> bool {
    return _EVENT_WAIT(event, 2 if timeout == 30 else timeout);
}


test "serve_background propagates an occupied port immediately" {
    occupied = socket.socket();
    occupied.bind(('127.0.0.1', 0));
    occupied.listen();
    port = int(occupied.getsockname()[1]);
    srv = ServingServer(app=ServingApp(), host='127.0.0.1', port=port);
    seen: list[int] = [];
    caught: any = None;
    stop: any = None;
    try {
        started = time.monotonic();
        with patch.object(threading.Event, 'wait', _short_startup_wait) {
            try {
                stop = srv.serve_background(
                    on_ready=lambda (p: int) { seen.append(p); }, port_retries=0
                );
            } except Exception as e {
                caught = e;
            }
        }
        assert isinstance(caught, PortInUseError) , caught;
        assert caught.port == port , caught;
        assert time.monotonic() - started < 1.0 , "a known bind failure must wake the caller";
        assert seen == [] , seen;
        assert srv._executor is not None and srv._executor._pool is None;
    } finally {
        if stop is not None {
            try {
                stop();
            } except RuntimeError {}
        }
        if srv._executor is not None {
            srv._executor.shutdown();
        }
        occupied.close();
    }
}


test "serve_background preserves startup errors and releases partial resources" {
    for stage in ('tls', 'server') {
        srv = ServingServer(app=ServingApp(), host='127.0.0.1', port=0);
        failure = ValueError(f"{stage} startup failed");
        listeners: list[any] = [];
        bind = serving_module.bind_listener;
        stop: any = None;
        caught: any = None;
        def _bind(*args: any, **kwargs: any) -> any {
            listener = bind(*args, **kwargs);
            listeners.append(listener);
            return listener;
        }
        failing = patch.object(srv.settings.tls, 'build_context', side_effect=failure)
            if stage == 'tls'
            else patch.object(
                serving_module.asyncio,
                'start_server',
                new=AsyncMock(side_effect=failure)
            );
        try {
            with patch.object(threading.Event, 'wait', _short_startup_wait), patch.object(
                serving_module, 'bind_listener', _bind
            ), failing {
                try {
                    stop = srv.serve_background(port_retries=0);
                } except Exception as e {
                    caught = e;
                }
            }
            assert caught is failure , (stage, caught);
            assert len(listeners) == 1 and listeners[0].fileno() == -1 , stage;
            assert srv._executor is not None and srv._executor._pool is None , stage;
        } finally {
            if stop is not None {
                try {
                    stop();
                } except RuntimeError {}
            }
            for listener in listeners {
                listener.close();
            }
            if srv._executor is not None {
                srv._executor.shutdown();
            }
        }
    }
}


test "serve_background waits for on_ready and propagates its failure" {
    srv = ServingServer(app=ServingApp(), host='127.0.0.1', port=0);
    entered = threading.Event();
    release = threading.Event();
    returned = threading.Event();
    failure = ValueError('ready callback failed');
    errors: list[any] = [];
    stops: list[any] = [];
    def _ready(port: int) {
        entered.set();
        assert release.`wait(timeout=2) , "callback was not released";
        raise failure;
    }
    def _call {
        try {
            stops.append(srv.serve_background(on_ready=_ready));
        } except Exception as e {
            errors.append(e);
        } finally {
            returned.set();
        }
    }
    caller = threading.Thread(target=_call, daemon=True);
    try {
        caller.start();
        assert entered.`wait(timeout=2) , "callback was not reached";
        assert not returned.`wait(timeout=0.05) , "success preceded the callback result";
        release.set();
        assert returned.`wait(timeout=2) , "callback failure did not wake the caller";
        caller.join(timeout=2);
        assert not caller.is_alive();
        assert errors == [failure] , errors;
        assert stops == [] , "a failed callback cannot return a stop handle";
        assert srv._server is not None and not srv._server.is_serving();
        assert srv._executor is not None and srv._executor._pool is None;
    } finally {
        release.set();
        caller.join(timeout=2);
        for stop in stops {
            try {
                stop();
            } except RuntimeError {}
        }
        if srv._server is not None {
            srv._server.close();
        }
        if srv._executor is not None {
            srv._executor.shutdown();
        }
    }
}


test "serve_background timeout suppresses late readiness and stops a delayed worker" {
    srv = ServingServer(app=ServingApp(), host='127.0.0.1', port=0);
    entered = threading.Event();
    release = threading.Event();
    finished = threading.Event();
    seen: list[int] = [];
    run = srv.run;
    caught: any = None;
    def _delayed_run(on_ready: any = None, port_retries: int = 0) -> int {
        entered.set();
        try {
            assert release.`wait(timeout=2) , "worker was not released";
            return run(on_ready=on_ready, port_retries=port_retries);
        } finally {
            finished.set();
        }
    }
    def _timeout(event: any, timeout: any = None) -> bool {
        if timeout == 30 {
            assert entered.`wait(timeout=2) , "worker did not enter startup";
            return False;
        }
        return _EVENT_WAIT(event, timeout);
    }
    with patch.object(srv, 'run', side_effect=_delayed_run), patch.object(
        threading.Event, 'wait', _timeout
    ), patch.object(srv, 'request_stop', wraps=srv.request_stop) as request_stop {
        try {
            try {
                srv.serve_background(on_ready=lambda (p: int) { seen.append(p); });
            } except Exception as e {
                caught = e;
            }
            assert isinstance(caught, TimeoutError) , caught;
            assert request_stop.call_count >= 1 , "timeout must request shutdown";
            release.set();
            assert finished.`wait(timeout=2) , "the late worker kept serving";
            assert seen == [] , "abandoned startup must not notify its host";
            assert request_stop.call_count >= 2 , "late readiness must retry the early stop";
            assert srv._server is not None and not srv._server.is_serving();
            assert srv._executor is not None and srv._executor._pool is None;
        } finally {
            release.set();
            cleanup_deadline = time.monotonic() + 2;
            while not finished.is_set()
                and srv._stop_event is None
                and time.monotonic() < cleanup_deadline {
                time.sleep(0.01);
            }
            if not finished.is_set() and srv._stop_event is not None {
                srv.request_stop();
            }
            assert finished.`wait(timeout=2) , "worker cleanup did not complete";
        }
    }
}


test "serve_background rejects worker exit before readiness" {
    srv = ServingServer(app=ServingApp());
    caught: any = None;
    stop: any = None;
    try {
        with patch.object(srv, 'run', return_value=0), patch.object(
            threading.Event, 'wait', _short_startup_wait
        ) {
            try {
                stop = srv.serve_background();
            } except Exception as e {
                caught = e;
            }
        }
        assert isinstance(caught, RuntimeError) , caught;
    } finally {
        if stop is not None {
            stop();
        }
    }
}


test "API background startup unwinds scheduler and bridge preserving the original error" {
    tmp = _workspace();
    Jac.set_base_path(tmp);
    Jac.set_context(Jac.create_j_context(user_root=None));
    try {
        for stage in ('transport', 'extension') {
            settings = ServeSettings.load(tmp, {'host': '127.0.0.1', 'port': 0});
            failure = ValueError(f"{stage} startup failed");
            scheduler = Mock();
            scheduler.stop.side_effect = RuntimeError('scheduler cleanup failed');
            ext = Mock();
            if stage == 'extension' {
                ext.on_worker_start.side_effect = failure;
            }
            srv = JacAPIServer(
                module_name='main', base_path=tmp, settings=settings, extensions=[ext]
            );
            srv.scheduler = scheduler;
            srv.app = ServingApp();
            caught: any = None;
            with patch.object(srv, '_prepare_to_serve', return_value=settings), patch.object(
                ServingServer, 'serve_background', side_effect=failure
            ), patch.object(api_module, 'start_worker_if_bridging') as start_bridge, patch.object(
                api_module, 'stop_worker'
            ) as stop_bridge {
                try {
                    srv.serve_background();
                } except Exception as e {
                    caught = e;
                }
                assert caught is failure , (stage, caught);
                scheduler.start_if_pending.assert_called_once();
                start_bridge.assert_called_once();
                scheduler.stop.assert_called_once();
                stop_bridge.assert_called_once();
            }
        }
    } finally {
        _reset(tmp);
    }
}


test "serve_background binds loopback on an ephemeral port and serves a client_dist" {
    os.environ["JAC_SCALE_RUNTIME"] = "1";
    tmp = _workspace();
    Jac.set_base_path(tmp);
    Jac.set_context(Jac.create_j_context(user_root=None));
    stop: any = None;
    try {
        set_config(None);
        Jac.set_full_target_path(os.path.join(tmp, "web", "main.jac"));
        sv_client.set_consumer_app("web");
        base = os.path.join(tmp, "web");
        _load(tmp, "main", base);
        settings = ServeSettings.load(
            base, {"host": "127.0.0.1", "port": 0, "client_dist": _dist(tmp)}
        );
        assert settings.port == 0 , "an explicit port 0 means ephemeral, not the config port";
        srv = JacAPIServer(
            module_name="main", port=0, base_path=base, settings=settings, extensions=[]
        );
        seen: list[int] = [];
        stop = srv.serve_background(on_ready=lambda (p: int) { seen.append(p); });
        assert seen and seen[0] > 0 , seen;
        assert srv.port == seen[0] , (srv.port, seen);
        origin = f"http://127.0.0.1:{seen[0]}";

        (code, body) = _get(f"{origin}/healthz/live");
        assert code == 200 , (code, body);

        (code, body) = _get(f"{origin}/");
        assert code == 200 and "hosted" in body , (code, body);
        (code, body) = _get(f"{origin}/assets/app.js");
        assert code == 200 and "hosted" in body , (code, body);
        (code, body) = _get(f"{origin}/some/client/route");
        assert code == 200 and "hosted" in body , (
            f"the SPA fallback must serve the client_dist index: {code} {body}"
        );

        (code, body) = _post(f"{origin}/walker/Hello", {"who": "loopback"});
        assert code == 200 and "hello loopback" in body , (code, body);
        (code, body) = _post(f"{origin}/api/web/walker/Hello", {"who": "routed"});
        assert code == 200 and "hello routed" in body , (code, body);
    } finally {
        if stop is not None {
            stop();
        }
        _reset(tmp);
    }
}


test "prepare_inprocess_runtime colocates the workspace's service apps" {
    os.environ["JAC_SCALE_RUNTIME"] = "1";
    tmp = _workspace();
    Jac.set_base_path(tmp);
    Jac.set_context(Jac.create_j_context(user_root=None));
    runtime: any = None;
    try {
        set_config(None);
        Jac.set_full_target_path(os.path.join(tmp, "web", "main.jac"));
        import from jaclang.scale.server.inprocess { prepare_inprocess_runtime }
        runtime = prepare_inprocess_runtime(
            os.path.join(tmp, "web", "main.jac"),
            os.path.join(tmp, "data"),
            endpoint_profile="desktop",
            setup_background_services=False
        );
        client = runtime.client;
        listing = client.get("/api/feed/walkers");
        assert listing.status_code == 200 , (
            f"the colocated service must be mounted: {listing.status_code} {listing.text}"
        );
        assert "Latest" in listing.text , listing.text;
        spawned = client.post("/api/feed/walker/Latest", json={});
        assert spawned.status_code == 200 and "\"a\"" in spawned.text , spawned.text;
        mine = client.post("/api/web/walker/Hello", json={"who": "self"});
        assert mine.status_code == 200 and "hello self" in mine.text , mine.text;
    } finally {
        if runtime is not None {
            runtime.close();
        }
        _reset(tmp);
    }
}

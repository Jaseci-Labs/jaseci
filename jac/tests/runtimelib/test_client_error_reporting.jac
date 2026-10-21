"""Tests for client-side error reporting endpoint.

The /cl/__error__ endpoint allows client-side JavaScript to report
errors back to the server for logging and observability.
"""

import io;
import json;
import logging;
import uuid;
import from pathlib { Path }
import from tempfile { TemporaryDirectory }
import from jaclang.testing.testing { JacTestClient }

def _as_any(v: any) -> any {
    return v;
}

glob FIXTURES = str(Path(__file__).parent / "fixtures");

def fixture_abs_path(filename: str) -> str {
    return str((Path(FIXTURES) / filename).resolve());
}

def make_client(base_path: str) -> JacTestClient {
    return JacTestClient.from_file(
        fixture_abs_path("serve_api.jac"), base_path=base_path
    );
}

"""Attach a StringIO handler to logger and return (buf, handler, old_level)."""
def capture_log_start(
    logger: logging.Logger, level: int = logging.DEBUG
) -> tuple[any, ...] {
    buf = io.StringIO();
    handler = logging.StreamHandler(buf);
    handler.setLevel(level);
    logger.addHandler(handler);
    old_level = logger.level;
    logger.setLevel(level);
    return (buf, handler, old_level);
}

"""Remove handler and restore logger level."""
def capture_log_stop(
    logger: logging.Logger, handler: logging.StreamHandler, old_level: int
) {
    logger.removeHandler(handler);
    logger.setLevel(old_level);
}

# =============================================================================
# Client Error Reporting Tests
# =============================================================================
test "client error endpoint exists and accepts error reports" {
    with TemporaryDirectory() as tmpdir {
        client = make_client(tmpdir);
        response = client.post(
            "/cl/__error__",
            json={
                "message": "Cannot use 'in' operator to search for '@' in undefined",
                "stack": "TypeError: Cannot use 'in' operator\n    at LoginPage (login.jac:42)",
                "url": "http://localhost:8001/",
                "source": "window.onerror",
                "timestamp": "2026-03-14T12:00:00Z"
            }
        );
        assert response.status_code == 200;
        client.close();
    }
}

test "client error is logged to server console" {
    with TemporaryDirectory() as tmpdir {
        client = make_client(tmpdir);
        logger = logging.getLogger("jaclang.client_errors");
        (buf, handler, old_level) = capture_log_start(logger);
        try {
            # Use unique message to avoid rate limiter dedup across test runs
            error_msg = f"Test error {uuid.uuid4().hex}";
            client.post(
                "/cl/__error__",
                json={
                    "message": error_msg,
                    "stack": "TypeError: test\n    at TestFunc (test.jac:1)",
                    "url": "http://localhost:8001/",
                    "source": "window.onerror",
                    "timestamp": "2026-03-14T12:00:00Z"
                }
            );
            log_output = buf.getvalue();
            assert error_msg in log_output , f"Expected client error in log output, got: {log_output}";
        } finally {
            capture_log_stop(logger, handler, old_level);
        }
        client.close();
    }
}

test "client error componentStack is logged when provided" {
    with TemporaryDirectory() as tmpdir {
        client = make_client(tmpdir);
        logger = logging.getLogger("jaclang.client_errors");
        (buf, handler, old_level) = capture_log_start(logger);
        try {
            error_msg = f"Render error {uuid.uuid4().hex}";
            comp_stack = "    in Toolbar\n    in App\n    in JacClientErrorBoundary";
            client.post(
                "/cl/__error__",
                json={
                    "message": error_msg,
                    "stack": "TypeError: d is not a function\n    at hs (/static/client.js:1:100)",
                    "componentStack": comp_stack,
                    "url": "http://localhost:8001/",
                    "source": "ErrorBoundary"
                }
            );
            log_output = buf.getvalue();
            assert error_msg in log_output;
            assert "Component stack:" in log_output , f"Expected component stack section in log, got: {log_output}";
            assert "in Toolbar" in log_output;
            assert "in App" in log_output;
        } finally {
            capture_log_stop(logger, handler, old_level);
        }
        client.close();
    }
}

test "client error endpoint handles missing fields gracefully" {
    with TemporaryDirectory() as tmpdir {
        client = make_client(tmpdir);
        # Minimal payload - just a message
        response = client.post("/cl/__error__", json={"message": "Something broke"});
        assert response.status_code == 200;
        client.close();
    }
}

test "client error endpoint rejects empty payload" {
    with TemporaryDirectory() as tmpdir {
        client = make_client(tmpdir);
        response = client.post("/cl/__error__", json={});
        assert response.status_code == 400;
        client.close();
    }
}

# =============================================================================
# Prod page error handler setup
# =============================================================================
"""Render a prod page for a stub client module and return its HTML."""
def render_stub_page -> str {
    import types;
    import from jaclang.client.serving { JacClient }
    module = types.ModuleType('stub');
    module.__file__ = __file__;
    introspector = types.SimpleNamespace(
        _client_manifest={'exports': ['app'], 'endpoint_effects': {}},
        _bundle=None,
        _module=module,
        module_name='stub',
        load=lambda { None; },
        get_client_functions=lambda { {'app': None}; },
        ensure_bundle=lambda { 'abc123'; }
    );
    result = JacClient.render_page(_as_any(introspector), 'app', {}, 'guest');
    return result['html'];
}

test "prod render_page injects early error handler before module bundle script" {
    html = render_stub_page();
    assert 'window.__jacErrorHandlersInstalled' in html;
    assert '/cl/__error__' in html;
    # Handler script must appear before the bundle so it catches errors during evaluation
    assert html.index('window.__jacErrorHandlersInstalled') < html.index('client.js');
}

# =============================================================================
# Client-side report budget
# =============================================================================
"""Run the budget harness against one reporter and return its per-scenario results."""
def run_error_budget_harness(mode: str, target: Path) -> dict[str, any] {
    import subprocess;
    result = subprocess.run(
        [
            "node",
            fixture_abs_path("client_error_budget_harness.mjs"),
            mode,
            str(target)
        ],
        capture_output=True,
        text=True,
        timeout=120
    );
    assert result.returncode == 0 , f"harness failed:\n{result.stdout}\n{result.stderr}";
    return json.loads(result.stdout.strip().splitlines()[-1]);
}

test "runtime reporter drops extension errors and caps reports per page" {
    import from jaclang.testing.requires { require_tool }
    import from jaclang.client.runtime_source { resolve_client_runtime_cl_path }
    import from .react_jsdom_harness {
        compile_react,
        wire_jac_runtime,
        write_runtime_support
    }
    require_tool("node");
    with TemporaryDirectory() as tmp {
        work = Path(tmp);
        runtime_path = resolve_client_runtime_cl_path("react");
        write_runtime_support(work, runtime_path);
        core_js = compile_react(
            str(Path(runtime_path).parent / "client_runtime_core.jac")
        );
        (work / "client_runtime_core.js").write_text(
            wire_jac_runtime(core_js), encoding="utf-8"
        );
        (work / "jac_runtime.js").write_text(
            "export function __jacJsx() { return null; }\n", encoding="utf-8"
        );
        (work / "package.json").write_text('{"type": "module"}', encoding="utf-8");
        results = run_error_budget_harness("runtime", work / "client_runtime_core.js");
    }
    assert results["extensionRejections"]["sent"] == 0 , results;
    assert results["firefoxExtensionRejections"]["sent"] == 0 , results;
    assert results["extensionScriptWithoutStack"]["sent"] == 0 , results;
    # One report per distinct error, however often it is thrown.
    assert results["identicalAppErrors"]["sent"] == 1 , results;
    first = results["identicalAppErrors"]["first"];
    assert first["endpoint"] == "/cl/__error__";
    assert first["message"] == "boom";
    assert first["source"] == "unhandledrejection";
    # A stack that passes through app code is ours to see.
    assert results["mixedStack"]["sent"] == 1 , results;
    assert results["appWindowError"]["sent"] == 1 , results;
    # At most 10 reports a minute, and the budget refills the next minute.
    assert results["distinctAppErrors"]["sent"] == 10 , results;
    assert results["distinctAppErrorsOverTwoMinutes"]["sent"] == 20 , results;
}

test "prod early error handler drops extension errors and caps reports per page" {
    import re;
    import from jaclang.testing.requires { require_tool }
    require_tool("node");
    scripts = re.findall(r"<script>(.*?)</script>", render_stub_page(), re.S);
    handlers = [
        s
        for s in scripts
        if "/cl/__error__" in s
    ];
    assert len(handlers) == 1 , scripts;
    with TemporaryDirectory() as tmp {
        script = Path(tmp) / "early_error_handler.js";
        script.write_text(handlers[0], encoding="utf-8");
        results = run_error_budget_harness("inline", script);
    }
    assert results["extensionRejections"]["sent"] == 0 , results;
    assert results["firefoxExtensionRejections"]["sent"] == 0 , results;
    assert results["extensionScriptWithoutStack"]["sent"] == 0 , results;
    assert results["mixedStack"]["sent"] == 1 , results;
    assert results["appWindowError"]["sent"] == 1 , results;
    # The early handler only covers the moments before the bundle loads, so it
    # has a flat budget of 10 per page rather than a per-minute one.
    assert results["identicalAppErrors"]["sent"] == 10 , results;
    assert results["distinctAppErrorsOverTwoMinutes"]["sent"] == 10 , results;
    # Once the runtime has installed its own handlers, the early one stands down.
    assert results["afterRuntimeHandlersInstalled"]["sent"] == 0 , results;
}

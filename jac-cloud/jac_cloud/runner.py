"""BCSAI runner scripts."""

from multiprocessing import cpu_count
from os import getenv
from ssl import CERT_NONE

from uvicorn import run as _run
from uvicorn.config import (
    HTTPProtocolType,
    InterfaceType,
    LOGGING_CONFIG,
    LifespanType,
    LoopSetupType,
    SSL_PROTOCOL_VERSION,
    WSProtocolType,
)


def run() -> None:
    """Run dev BCSAI BE."""
    workers = int(workers) if (workers := getenv("WORKER")) else ((cpu_count() * 2) + 1)

    _run(
        "jac_cloud.standalone:app",
        host=getenv("UV_HOST") or "127.0.0.1",
        port=int(getenv("UV_PORT") or "8000"),
        uds=getenv("UV_UDS"),
        fd=int(v) if (v := getenv("UV_FD")) else None,
        loop=(
            v  # type: ignore[arg-type]
            if (v := getenv("UV_LOOP")) and v in LoopSetupType.__args__  # type: ignore[attr-defined]
            else "auto"
        ),
        http=(
            v  # type: ignore[arg-type]
            if (v := getenv("UV_HTTP")) and v in HTTPProtocolType.__args__  # type: ignore[attr-defined]
            else "auto"
        ),
        ws=(
            v  # type: ignore[arg-type]
            if (v := getenv("UV_WS")) and v in WSProtocolType.__args__  # type: ignore[attr-defined]
            else "auto"
        ),
        ws_max_size=int(v) if (v := getenv("UV_WS_MAX_SIZE")) else 16777216,
        ws_max_queue=int(v) if (v := getenv("UV_WS_MAX_QUEUE")) else 32,
        ws_ping_interval=float(v) if (v := getenv("UV_WS_PING_INTERVAL")) else 20.0,
        ws_ping_timeout=float(v) if (v := getenv("UV_WS_PING_TIMEOUT")) else 20.0,
        ws_per_message_deflate=getenv("UV_WS_PER_MESSAGE_DEFLATE", "true").lower()
        != "false",
        lifespan=(
            v  # type: ignore[arg-type]
            if (v := getenv("UV_LIFESPAN")) and v in LifespanType.__args__  # type: ignore[attr-defined]
            else "auto"
        ),
        interface=(
            v  # type: ignore[arg-type]
            if (v := getenv("UV_INTERFACE")) and v in InterfaceType.__args__  # type: ignore[attr-defined]
            else "auto"
        ),
        reload=getenv("UV_RELOAD", "false").lower() != "false",
        reload_dirs=(
            vl if (v := getenv("UV_RELOAD_DIRS")) and (vl := v.split(",")) else None
        ),
        reload_includes=(
            vl if (v := getenv("UV_RELOAD_INCLUDES")) and (vl := v.split(",")) else None
        ),
        reload_excludes=(
            vl if (v := getenv("UV_RELOAD_EXCLUDES")) and (vl := v.split(",")) else None
        ),
        reload_delay=float(v) if (v := getenv("UV_RELOAD_DELAY")) else 0.25,
        workers=int(v) if (v := getenv("UV_WORKERS")) else None,
        env_file=getenv("UV_ENV_FILE"),
        log_config=getenv("UV_LOG_CONFIG") or LOGGING_CONFIG,
        log_level=getenv("UV_LOG_LEVEL"),
        access_log=getenv("UV_ACCESS_LOG", "true").lower() != "false",
        proxy_headers=getenv("UV_PROXY_HEADERS", "true").lower() != "false",
        server_header=getenv("UV_SERVER_HEADER", "true").lower() != "false",
        date_header=getenv("UV_DATE_HEADER", "true").lower() != "false",
        forwarded_allow_ips=(
            vl
            if (v := getenv("UV_FORWARDED_ALLOW_IPS")) and (vl := v.split(","))
            else None
        ),
        root_path=v if (v := getenv("UV_ROOT_PATH")) is not None else "",
        limit_concurrency=int(v) if (v := getenv("UV_LIMIT_CONCURRENCY")) else None,
        backlog=int(v) if (v := getenv("UV_BACKLOG")) else 2048,
        limit_max_requests=(int(v) if (v := getenv("UV_LIMIT_MAX_REQUESTS")) else None),
        timeout_keep_alive=int(v) if (v := getenv("UV_TIMEOUT_KEEP_ALIVE")) else 5,
        timeout_graceful_shutdown=(
            int(v) if (v := getenv("UV_TIMEOUT_GRACEFUL_SHUTDOWN")) else None
        ),
        ssl_keyfile=getenv("UV_SSL_KEYFILE"),
        ssl_certfile=getenv("UV_SSL_CERTFILE"),
        ssl_keyfile_password=getenv("UV_SSL_KEYFILE_PASSWORD"),
        ssl_version=(
            int(v) if (v := getenv("UV_SSL_VERSION")) else SSL_PROTOCOL_VERSION
        ),
        ssl_cert_reqs=(int(v) if (v := getenv("UV_SSL_CERT_REQS")) else CERT_NONE),
        ssl_ca_certs=getenv("UV_SSL_CA_CERTS"),
        ssl_ciphers=getenv("UV_SSL_CIPHERS") or "TLSv1",
        headers=(
            [tuple(_v.split(":", maxsplit=1)) for _v in vl if _v]  # type: ignore[misc]
            if (v := getenv("UV_HEADERS")) and (vl := v.split(","))
            else None
        ),
        use_colors=v != "false" if (v := getenv("UV_USE_COLORS")) else None,
        app_dir=getenv("UV_APP_DIR"),
        factory=getenv("UV_FACTORY", "false").lower() != "false",
        h11_max_incomplete_event_size=(
            int(v) if (v := getenv("UV_H11_MAX_INCOMPLETE_EVENT_SIZE")) else None
        ),
    )

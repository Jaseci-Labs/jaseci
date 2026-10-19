import os;
import sys;
import json;
import hashlib;
import importlib;
import platform;
import from pathlib { Path }


glob PLUGIN_BOOTSTRAP_MODULES: list[str] = [
         "manifest",
         "desktop_plugin",
         "webview_lib",
         "plugin_host",
         "registry"
     ],
     EMBEDDED: str = "embedded",
     PORT_RETRIES: int = 64;

glob _EMBEDDED_LOCKS: dict[str, any] = {},
     _EMBEDDED_STOPPED: set[str] = set();


obj HostContext {
    has port: int = 0,
        dev_port: int = 0,
        host: any = None,
        runtime: any = None,
        library_dir: str = "",
        pg_home: str = "",
        _stop: any = None;

    def setup_webview(wv_handle: int) {
        self.host.setup(wv_handle, self.library_dir);
    }

    def shutdown {
        stop = self._stop;
        self._stop = None;
        if stop is not None {
            try {
                stop();
            } except Exception as e {
                sys.stderr.write("host_boot: server stop failed: " + str(e) + "\n");
            }
        }
        runtime = self.runtime;
        self.runtime = None;
        if runtime is not None {
            try {
                runtime.close();
            } except Exception as e {
                sys.stderr.write("host_boot: runtime close failed: " + str(e) + "\n");
            }
        }
        _stop_embedded_store(self.pg_home);
    }
}


def preferred_port(app_name: str) -> int {
    return 49152 + (int(hashlib.sha1(app_name.encode()).hexdigest(), 16) % 16000);
}


def host_executable -> str {
    return process_executable();
}


def default_data_dir(system: str, identifier: str, app_name: str) -> str {
    """The per-user, per-app data directory on this platform.

    Scoped by the app `identifier` (falling back to its name), so two desktop
    apps never share state, and placed under the OS per-user data location, so
    the state survives cache clears and never lands in a read-only bundle.
    """;
    scope = identifier or app_name;
    if system == "Darwin" {
        return os.path.join(os.path.expanduser("~/Library/Application Support"), scope);
    }
    if system == "Windows" {
        base = os.environ.get("LOCALAPPDATA")
            or os.path.join(os.path.expanduser("~"), "AppData", "Local");
        return os.path.join(base, scope);
    }
    base = os.environ.get("XDG_DATA_HOME")
        or os.path.join(os.path.expanduser("~"), ".local", "share");
    return os.path.join(base, scope);
}


def _migrate_legacy_data_dir(data_dir: str, app_dir: str) -> None {
    """Carry pre-existing app state into the per-user data dir, on upgrade.

    Before this, a Linux app kept its graph and session beside the app image
    (`<app_dir>/.jac/desktop`). Copy that once into the new per-user dir so an
    upgrade keeps its state instead of starting empty. macOS and Windows were
    already per-user, so their old and new dirs are equal and this is a no-op.
    A missing legacy dir, or a new dir that already has state, is left alone.
    """;
    if not app_dir or os.path.realpath(data_dir) == os.path.realpath(app_dir) {
        return;
    }
    legacy = os.path.join(app_dir, ".jac", "desktop");
    current = os.path.join(data_dir, ".jac", "desktop");
    if not os.path.isdir(legacy) or os.path.exists(current) {
        return;
    }
    try {
        import shutil;
        os.makedirs(os.path.dirname(current), exist_ok=True);
        shutil.copytree(legacy, current);
    } except Exception as e {
        sys.stderr.write(
            "host_boot: could not migrate desktop state: " + str(e) + "\n"
        );
    }
}


def embedded_store_env(app_dir: str, data_dir: str, pg_dist: str) -> dict[str, str] {
    """The environment that gives the embedded store a per-app cluster and the
    distribution baked beside the app image.

    `JAC_PG_HOME` relocates the whole `pg` cache bucket (cluster and dist cache)
    under the app's per-user data dir, so two apps never share a cluster and the
    state is not the machine-wide `<cache>/pg/main`. `JAC_PG_DIST` points at the
    tree the build vendored, or at the cached tree a dev session passes instead,
    so the app starts with no network and no system Postgres.
    """;
    env = {"JAC_PG_HOME": data_dir};
    if pg_dist {
        env["JAC_PG_DIST"] = os.path.join(app_dir, pg_dist);
    }
    return env;
}


def _embedded_cluster_dir(home: str) -> str {
    """The per-app embedded cluster dir under an app's `JAC_PG_HOME` data dir.

    Mirrors the `pg` cache bucket layout (`<root>/pg`) and the cluster name
    (`main`) that `shared_pg_data_dir` resolves, so the path this app stops is
    the cluster it started. A test pins the two together.
    """;
    return os.path.join(home, "pg", "main");
}


def _embedded_user_lock_path(home: str) -> str {
    """The advisory lock file whose shared holders are the app's running instances.""";
    return os.path.join(home, "pg", ".desktop-users.lock");
}


def _join_embedded_store(home: str) -> None {
    """Hold a shared lock for as long as this process uses the app's cluster.

    Two instances of one app share one cluster, so only the last may stop it.
    The OS drops the lock when the process exits, even on a crash, so the lock
    is the shared count of live instances.
    """;
    if not home or home in _EMBEDDED_LOCKS {
        return;
    }
    try {
        import fcntl;
        path = _embedded_user_lock_path(home);
        os.makedirs(os.path.dirname(path), exist_ok=True);
        handle = open(path, "a");
        fcntl.flock(handle.fileno(), fcntl.LOCK_SH);
        _EMBEDDED_LOCKS[home] = handle;
    } except Exception as e {
        sys.stderr.write("host_boot: embedded postgres lock failed: " + str(e) + "\n");
    }
}


def _holds_last_embedded_user(handle: any) -> bool {
    """True when no other process holds a shared lock on `handle`.

    Converting the shared lock to an exclusive one succeeds only for the sole
    holder; a peer still using the cluster keeps the lock shared and this
    fails.
    """;
    try {
        import fcntl;
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB);
    } except Exception {
        return False;
    }
    return True;
}


def _stop_embedded_store(home: str) -> None {
    """Stop this app's embedded cluster once the last instance exits.

    The shutdown hook and the atexit backstop both call this, so a second call
    is a no-op. When this process holds no lock (a platform without `fcntl`),
    stop directly, as before.
    """;
    if not home or home in _EMBEDDED_STOPPED {
        return;
    }
    _EMBEDDED_STOPPED.add(home);
    handle = _EMBEDDED_LOCKS.pop(home, None);
    if handle is not None {
        last = _holds_last_embedded_user(handle);
        handle.close();
        if not last {
            # A peer instance still uses the cluster; it stops the cluster on
            # its own exit.
            return;
        }
    }
    try {
        import from jaclang.data.pgembed { stop_cluster }
        stop_cluster(_embedded_cluster_dir(home));
    } except Exception as e {
        sys.stderr.write("host_boot: embedded postgres stop failed: " + str(e) + "\n");
    }
}


def _apply_extra_deps {
    extra = os.environ.get("JAC_DESKTOP_DEPS", "");
    if not extra {
        return;
    }
    for d in extra.split(os.pathsep) {
        if d and d not in sys.path {
            sys.path.append(d);
        }
    }
}


def _bootstrap_plugin_host(plugin_configs: dict[str, any]) -> any {
    import jaclang;
    pdir = os.path.join(
        os.path.dirname(str(jaclang.__file__)), "client", "targets", "desktop", "plugin"
    );
    if pdir not in sys.path {
        sys.path.insert(0, pdir);
    }
    for name in PLUGIN_BOOTSTRAP_MODULES {
        importlib.import_module(str(name));
    }
    return sys.modules["registry"].bootstrap_plugins(plugin_configs, sys.modules);
}


def _ensure_jac_meta_importer {
    if not any(isinstance(f, JacMetaImporter) for f in sys.meta_path) {
        sys.meta_path.insert(0, JacMetaImporter());
    }
}


def resolve_program(program: dict[str, any], app_dir: str) -> str {
    jab = str(program.get("jab") or "");
    if jab {
        import from jaclang.dist.jab { jab_app_meta, materialize_jab }
        jab_path = jab if os.path.isabs(jab) else os.path.join(app_dir, jab);
        img = materialize_jab(jab_path);
        entry_rel = str((jab_app_meta(img).get("entry") or {}).get("path") or "");
        if not entry_rel {
            raise RuntimeError(f"the app image {jab_path} has no entry to serve");
        }
        return str(img / entry_rel);
    }
    entry_path = str(program.get("entry") or "");
    if not entry_path {
        raise RuntimeError("the host config names neither an app image nor an entry");
    }
    return entry_path
        if os.path.isabs(entry_path)
        else os.path.join(app_dir, entry_path);
}


def _pinned_port -> int {
    raw = os.environ.get("JAC_DESKTOP_BROKER_PORT", "");
    if not raw {
        return 0;
    }
    try {
        return int(raw);
    } except ValueError {
        raise RuntimeError(
            "JAC_DESKTOP_BROKER_PORT must be a port number, got '" + raw + "'"
        );
    }
}


def serve_program(
    entry_file: str,
    data_dir: str,
    dist_dir: str,
    app_name: str,
    backend: str,
    host: any,
    store: any
) -> tuple[any, int, any] {
    _ensure_jac_meta_importer();
    broker = DesktopBrokerExtension(store=store, host=host);
    remote = backend != EMBEDDED;
    pinned = _pinned_port();
    attempts = [(pinned, 0)]
        if pinned
        else [(preferred_port(app_name), PORT_RETRIES), (0, 0)];
    last_error: (Exception | None) = None;
    for (port, retries) in attempts {
        runtime = prepare_inprocess_runtime(
            entry_file,
            os.path.join(data_dir, ".jac", "desktop", "graph"),
            endpoint_profile="desktop",
            setup_background_services=False,
            transport_kind="listener",
            extensions=[broker],
            overrides={
                "host": "127.0.0.1",
                "port": port,
                "strict_port": retries == 0,
                "no_client": False,
                "client_dist": dist_dir,
                "static_only": remote
            }
        );
        bound: list[int] = [];
        try {
            stop = runtime.server.serve_background(
                on_ready=bound.append, port_retries=retries
            );
        } except OSError as e {
            last_error = e;
            runtime.close();
            continue;
        }
        if not bound {
            stop();
            runtime.close();
            last_error = RuntimeError("the server did not report a bound port");
            continue;
        }
        return (runtime, bound[0], stop);
    }
    raise RuntimeError(
        "the desktop host could not bind a loopback port"
            + (f": {last_error}" if last_error is not None else "")
    );
}


def boot(config_json: str) -> HostContext {
    cfg = json.loads(config_json);
    app_name = str(cfg.get("app_name") or "app");
    mode = str(cfg.get("mode") or "webview");
    program = (cfg.get("program") or {}) as dict[str, any];
    backend = str(cfg.get("backend") or EMBEDDED);
    plugin_configs = (cfg.get("plugins") or {}) as dict[str, any];
    identifier = str(cfg.get("identifier") or "");

    layout = AppLayout.from_executable(Path(host_executable()));
    app_dir = str(cfg.get("app_dir") or "") or str(layout.resources);
    chosen_data_dir = os.environ.get("JAC_DATA_PATH", "");
    data_dir = chosen_data_dir
        or default_data_dir(platform.system(), identifier, app_name);
    if not chosen_data_dir {
        # Only the default path changed; a user-chosen JAC_DATA_PATH is already
        # the user's own location and keeps its state.
        _migrate_legacy_data_dir(data_dir, app_dir);
    }

    if backend == EMBEDDED {
        for (key, value) in embedded_store_env(
            app_dir, data_dir, str(cfg.get("pg_dist") or "")
        ).items() {
            os.environ[key] = value;
        }
        _join_embedded_store(data_dir);
        import atexit;
        atexit.register(_stop_embedded_store, data_dir);
    }

    _apply_extra_deps();

    host = _bootstrap_plugin_host(plugin_configs);
    if mode == "cef" {
        host.setup_cef(str(layout.library_dir()));
    }

    entry_file = resolve_program(program, app_dir) if backend == EMBEDDED else "";
    store = SessionStore(os.path.join(data_dir, ".jac", "desktop", "session.json"));
    (runtime, port, stop) = serve_program(
        entry_file,
        data_dir,
        os.path.join(app_dir, "dist"),
        app_name,
        backend,
        host,
        store
    );

    ctx = HostContext(
        host=host,
        runtime=runtime,
        port=port,
        library_dir=str(layout.library_dir()),
        pg_home=(data_dir if backend == EMBEDDED else ""),
        _stop=stop
    );
    try {
        ctx.dev_port = int(os.environ.get("JAC_DESKTOP_DEV_PORT", "0") or "0");
    } except (TypeError, ValueError) {
        ctx.dev_port = 0;
    }
    sys.stdout.write("JAC_DESKTOP_SERVING http://127.0.0.1:" + str(port) + "/\n");
    sys.stdout.flush();
    return ctx;
}

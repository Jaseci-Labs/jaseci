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


obj HostContext {
    has port: int = 0,
        dev_port: int = 0,
        host: any = None,
        runtime: any = None,
        library_dir: str = "",
        _stop: any = None;

    def setup_webview(wv_handle: int);
    def shutdown;
}


def preferred_port(app_name: str) -> int;


def host_executable -> str;


def default_data_dir(system: str, identifier: str, app_name: str, app_dir: str) -> str;


def _apply_extra_deps;


def _bootstrap_plugin_host(plugin_configs: dict[str, any]) -> any;


def _ensure_jac_meta_importer;


def resolve_program(program: dict[str, any], app_dir: str) -> str;


def _pinned_port -> int;


def serve_program(
    entry_file: str,
    data_dir: str,
    dist_dir: str,
    app_name: str,
    backend: str,
    host: any,
    store: any
) -> tuple[any, int, any];


def boot(config_json: str) -> HostContext;

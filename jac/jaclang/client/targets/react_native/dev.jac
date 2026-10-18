import json;
import os;
import subprocess;
import from pathlib { Path }
import from typing { Optional }

glob JAC_RN_METRO_PORT_ENV: str = "JAC_RN_METRO_PORT",
     JAC_RN_DEV_HOST_ENV: str = "JAC_RN_DEV_HOST",
     DEFAULT_METRO_PORT: int = 8081;

def resolve_metro_port(cli_port: int = DEFAULT_METRO_PORT) -> int;

def setup_android_port_reverse(metro_port: int, api_port: int);

def inject_dev_api_base_url(rn_dir: Path, api_url: str) -> Optional[str];

def restore_app_json(rn_dir: Path, original: Optional[str]) -> None;

def rn_hmr_on_jac_changed(
    event: FileChangeEvent,
    compiler: any,
    entry_file: Path,
    project_dir: Path,
    rn_dir: Path,
    entry_module: str
) -> None;

def build_expo_start_argv(
    rn_dir: Path, metro_port: int, clear_cache: bool = True
) -> list[str];

def run_expo_start(rn_dir: Path, metro_port: int, clear_cache: bool = True) -> int;

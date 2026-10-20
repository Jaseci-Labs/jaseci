import os;
import sys;
import json;
import logging;
import from pathlib { Path }

glob _logger: logging.Logger = logging.getLogger("byllm.model_cache");

def _is_interactive -> bool;

def _emit(msg: str);

def get_cache_dir -> Path;

def alias_dir(alias: str) -> Path;

def gguf_path(alias: str, spec: dict[str, any]) -> Path;

def _consent_marker(alias: str) -> Path;

def is_downloaded(alias: str, spec: dict[str, any]) -> bool;

def _fmt_size(mb: int) -> str;

def _resolve_consent(alias: str, spec: dict[str, any], auto_download: bool) -> bool;

def _download(alias: str, spec: dict[str, any]) -> Path;

def ensure_model(alias: str, spec: dict[str, any], auto_download: bool = False) -> str;

def force_pull(alias: str, spec: dict[str, any]) -> str;

def remove_alias(alias: str) -> bool;

def list_downloaded -> list[dict[str, any]];

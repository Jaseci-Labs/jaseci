import json;
import os;

import from pathlib { Path }

glob SERVE_MANIFEST_REL: str = os.path.join(".jac", "serve_manifest.json"),
     CLIENT_DIST_REL: str = os.path.join(".jac", "client", "dist"),
     NATIVE_DIR_REL: str = os.path.join(".jac", "native"),
     _MODULE_KEYS_CACHE: dict[str, tuple[float, set]] = {};


def _image_module_keys(img_root: str) -> set;


def _image_key(abs_path: str, img_root: str) -> str;


def _image_roots(abs_path: str) -> Iterator[tuple[str, bool]];


def sealed_root_for(path: str) -> (str | None);


def unlisted_image_root(path: str) -> (str | None);


def serve_manifest_for(path: str) -> (dict[str, any] | None);


def client_dist_for(path: str) -> (Path | None);

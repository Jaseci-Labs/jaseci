import os;
import sys;

glob _KIT: list[tuple[str, (SealedImage | None)]] = [],
     PR_KIT_EVENT: str = "pull_request",
     PR_KIT_LABEL_PREFIX: str = "native:";

def kit_image -> (tuple[str, SealedImage] | None);

def pr_kit_omits(name: str) -> bool;

def _pr_labels -> set[str];

def kit_path(rel: str) -> str;

def _find_kit -> tuple[str, (SealedImage | None)];

def runtime_floor_root(sealed: bool) -> str;

def osarch(triple: str = "") -> str;

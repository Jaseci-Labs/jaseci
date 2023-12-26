"""The Jac Programming Language."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))

from jaclang.compiler.importer import jac_import  # noqa: E402
from jaclang.plugin.feature import JacFeature  # noqa: E402
from jaclang.vendor import lark  # noqa: E402
from jaclang.vendor import mypy  # noqa: E402
from jaclang.vendor import pluggy  # noqa: E402

__all__ = [
    "jac_import",
    "lark",
    "mypy",
    "pluggy",
]

JacFeature.pm.load_setuptools_entrypoints("jac")

"""The Jac Programming Language."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))


from jaclang.jac.importer import jac_import  # noqa: E402
from jaclang.utils.helpers import handle_jac_error  # noqa: E402
import jaclang.core  # noqa: F401, E402, I100

__all__ = [
    "jac_import",
    "handle_jac_error",
]

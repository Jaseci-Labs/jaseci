"""The Jac Programming Language."""
import os
import sys

from jaclang.jac.importer import jac_blue_import, jac_purple_import
from jaclang.utils.helpers import handle_jac_error


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
__all__ = ["jac_blue_import", "jac_purple_import", "handle_jac_error"]

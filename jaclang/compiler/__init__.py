# type: ignore
"""Jac compiler tools."""
import contextlib
import logging
import os
import sys

cur_dir = os.path.dirname(__file__)
if not os.path.exists(os.path.join(cur_dir, "__jac_gen__", "jac_parser.py")):
    from jaclang.vendor.lark.tools import standalone

    os.makedirs(os.path.join(cur_dir, "__jac_gen__"), exist_ok=True)
    with open(os.path.join(cur_dir, "__jac_gen__", "__init__.py"), "w"):
        pass
    save_argv = sys.argv
    sys.argv = [
        "lark",
        os.path.join(cur_dir, "jac.lark"),
        "-o",
        os.path.join(cur_dir, "__jac_gen__", "jac_parser.py"),
        "-c",
    ]
    standalone.main()  # type: ignore
    sys.argv = save_argv

from .__jac_gen__ import jac_parser as jac_lark  # noqa: E402


jac_lark.logger.setLevel(logging.DEBUG)
contextlib.suppress(AttributeError)

__all__ = ["jac_lark"]

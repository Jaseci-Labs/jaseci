"""Jac compiler tools."""

import contextlib
import logging
import os
import shutil
import sys


def generate_static_parser(force: bool = False) -> None:
    """Generate static parser."""
    from jaclang.utils.helpers import auto_generate_refs
    from jaclang.vendor.lark.tools import standalone

    cur_dir = os.path.dirname(__file__)
    if force or not os.path.exists(os.path.join(cur_dir, "generated", "jac_parser.py")):
        if os.path.exists(os.path.join(cur_dir, "generated")):
            shutil.rmtree(os.path.join(cur_dir, "generated"))
        os.makedirs(os.path.join(cur_dir, "generated"), exist_ok=True)
        with open(os.path.join(cur_dir, "generated", "__init__.py"), "w"):
            pass
        save_argv = sys.argv
        sys.argv = [
            "lark",
            os.path.join(cur_dir, "jac.lark"),
            "-o",
            os.path.join(cur_dir, "generated", "jac_parser.py"),
            "-c",
        ]
        standalone.main()  # type: ignore
        sys.argv = save_argv
        try:
            auto_generate_refs()
        except Exception as e:
            print(f"Error generating reference files: {e}")


generate_static_parser()
try:
    from jaclang.compiler.generated import jac_parser as jac_lark  # noqa: E402

    jac_lark.logger.setLevel(logging.DEBUG)
except AttributeError:
    generate_static_parser(force=True)
    from jaclang.compiler.generated import jac_parser as jac_lark  # noqa: E402

    jac_lark.logger.setLevel(logging.DEBUG)
contextlib.suppress(AttributeError)
TOKEN_MAP = {
    x.name: x.pattern.value
    for x in jac_lark.Lark_StandAlone().parser.lexer_conf.terminals
}

TOKEN_MAP.update(
    {
        "CARROW_L": "<++",
        "CARROW_R": "++>",
        "GLOBAL_OP": ":global:",
        "NONLOCAL_OP": ":nonlocal:",
        "WALKER_OP": ":walker:",
        "NODE_OP": ":node:",
        "EDGE_OP": ":edge:",
        "CLASS_OP": ":class:",
        "OBJECT_OP": ":obj:",
        "TYPE_OP": "`",
        "ABILITY_OP": ":can:",
        "ELVIS_OP": "?:",
        "NULL_OK": "?",
        "KW_OR": "|",
        "ARROW_BI": "<-->",
        "ARROW_L": "<--",
        "ARROW_R": "-->",
        "ARROW_L_P1": "<-:",
        "ARROW_R_P2": ":->",
        "ARROW_L_P2": ":-",
        "ARROW_R_P1": "-:",
        "CARROW_BI": "<++>",
        "CARROW_L": "<++",
        "CARROW_R": "++>",
        "CARROW_L_P1": "<+:",
        "CARROW_R_P2": ":+>",
        "CARROW_L_P2": ":+",
        "CARROW_R_P1": "+:",
        "PIPE_FWD": "|>",
        "PIPE_BKWD": "<|",
        "A_PIPE_FWD": ":>",
        "A_PIPE_BKWD": "<:",
        "DOT_FWD": ".>",
        "STAR_POW_EQ": "**=",
        "MUL_EQ": "*=",
        "FLOOR_DIV_EQ": "//=",
        "DIV_EQ": "/=",
        "BW_OR_EQ": "|=",
        "BW_XOR_EQ": "^=",
        "STAR_POW": "**",
        "STAR_MUL": "*",
        "FLOOR_DIV": "//",
        "DIV": "/",
        "PYNLINE": "::py::",
    }
)


__all__ = ["jac_lark", "TOKEN_MAP"]

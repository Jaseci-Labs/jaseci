import io
import os
import sys

import contextlib
from collections.abc import Iterable

# If these variables are not set by the pyodide this will raise an exception.
SAFE_CODE = globals()["SAFE_CODE"]
JAC_PATH  = globals()["JAC_PATH"]
CB_STDOUT = globals()["CB_STDOUT"]
CB_STDERR = globals()["CB_STDERR"]

debugger  = globals()["debugger"]

# Redirect stdout and stderr to javascript callback.
class JsIO(io.StringIO):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        super().__init__(*args, **kwargs)

    def write(self, s: str, /) -> int:
        self.callback(s)
        super().write(s)

    def writelines(self, lines: Iterable[str], /) -> None:
        for line in lines:
            self.callback(line)
        super().writelines(lines)


with open(JAC_PATH, "w") as f:
    f.write(SAFE_CODE)


with contextlib.redirect_stdout(JsIO(CB_STDOUT)), \
        contextlib.redirect_stderr(JsIO(CB_STDERR)):

    try:
        code = \
        "from jaclang.cli.cli import run\n" \
        f"run('{JAC_PATH}')\n"
        debugger.set_code(code=code, filepath=JAC_PATH)
        debugger.do_run()

    except Exception:
        import traceback
        traceback.print_exc()

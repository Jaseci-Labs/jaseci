import bdb
from typing import Callable


class Debugger(bdb.Bdb):

    def __init__(self):
        super().__init__()
        self.filepath: str = ""
        self.code: str = ""
        self.curframe = None
        self.breakpoint_buff = []

        self.cb_break: Callable[[Debugger, int], None] = lambda dbg, lineno: None
        self.cb_graph: Callable[[str], None] = lambda graph: None

    def set_code(self, code: str, filepath: str) -> None:
        self.filepath = filepath
        self.code = code
        self.curframe = None
        self.clear_breakpoints()

    def user_line(self, frame):
        """Called when we stop or break at a line."""

        if self.curframe is None:
            self.curframe = frame
            self.set_continue()
        elif frame.f_code.co_filename == self.filepath:
            self._send_graph()
            self.curframe = frame
            self.cb_break(self, frame.f_lineno)
        else:
            self.do_step_into()  # Just step till we reach the file again.

    def _send_graph(self) -> None:
        try:
            graph_str = self.runeval("dotgen(as_json=True)")
            self.cb_graph(graph_str)
        except Exception as e:
            pass
        self.set_trace()

    # -------------------------------------------------------------------------
    # Public API.
    # -------------------------------------------------------------------------

    def set_breakpoint(self, lineno: int) -> None:
        if not self.filepath:
            self.breakpoint_buff.append(lineno)
        else:
            self.set_break(self.filepath, lineno)

    def clear_breakpoints(self) -> None:
        self.clear_all_breaks()

    def do_run(self) -> None:
        for lineno in self.breakpoint_buff:
            self.set_break(self.filepath, lineno)
        self.breakpoint_buff.clear()
        self.run(self.code)

    def do_continue(self) -> None:
        self.set_continue()

    def do_step_over(self) -> None:
        self.set_next(self.curframe)

    def do_step_into(self) -> None:
        self.set_step()

    def do_step_out(self) -> None:
        self.set_return(self.curframe)

    def do_terminate(self) -> None:
        self.set_quit()

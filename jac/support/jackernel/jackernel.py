"""Jupyter notebook kernel for jaclang."""

from io import BytesIO

from ipykernel.kernelapp import IPKernelApp
from ipykernel.kernelbase import Kernel

from jaclang.cli.jacrunner import JacMachine, JacRunner
from jaclang.runtimelib.builtin import dotgen


class JaclangKernel(Kernel):
    """Jupyter kernel for Jaclang."""

    implementation = "Jaclang"
    implementation_version = "0.1"
    language = "jaclang"
    language_version = "0.1"
    language_info = {
        "name": "jaclang",
        "mimetype": "text/x-jaclang",
        "file_extension": ".jac",
    }
    banner = "Jaclang kernel - execute Jaclang code via a custom ipykernel wrapper"

    def __init__(self, *args, **kwargs) -> None:  # noqa
        super().__init__(*args, **kwargs)
        self.silent = False
        self.runner = JacRunner()
        self.runner.notebook_repr_fn = self._notebook_repr_fn

        self._override_matplotlib_show()

    def do_execute(
        self,
        code: str,
        silent: bool,
        store_history: bool = True,
        user_expressions=None,  # noqa: ANN001
        allow_stdin: bool = False,
    ) -> None:
        """Execute code in Jaclang and return the output."""
        self.silent = silent

        # Trim or preprocess code if needed
        if not code.strip():
            return self._done_exec()

        try:
            code = "with entry {\n%s;\n}" % code
            bytecode = self.runner.compile(code)
            if not bytecode:
                return self._done_exec()

            self.runner.execute(bytecode)
        except Exception:
            pass

        return self._done_exec()

    # --------------------------------------------------------------------------
    # Internal methods.
    # --------------------------------------------------------------------------

    def _override_matplotlib_show(self) -> None:
        try:
            import matplotlib.pyplot as plt

            def show() -> None:
                buf = BytesIO()
                plt.savefig(buf, format="png")
                buf.seek(0)
                self._image_output(buf)

            plt.show = show
        except ImportError:
            pass

    def _notebook_repr_fn(self, val) -> bool:  # noqa
        """If this is handled, return True."""
        if isinstance(val, (JacMachine.Root, JacMachine.Node)):
            try:
                import graphviz
            except ImportError:
                self.runner.add_stderr(
                    "'graphviz' is not installed. Please install it to visualize jac graph.\n"
                    "    graphviz      : https://graphviz.org/\n"
                    "    python wrapper: https://pypi.org/project/graphviz/"
                )
                return False
            dotgraph_str = dotgen(val)
            dotgraph = graphviz.Source(dotgraph_str)
            graph_bytes = dotgraph.pipe(format="png")
            buf = BytesIO(graph_bytes)
            buf.seek(0)
            self._image_output(buf)
            return True

        return False

    def _image_output(self, buf: BytesIO) -> None:
        self.send_response(
            self.iopub_socket,
            "display_data",
            {
                "data": {
                    "image/png": buf.read(),
                },
                "metadata": {},
            },
        )

    def _done_exec(self) -> dict:
        if not self.silent:
            if self.runner.stdout:
                self.send_response(
                    self.iopub_socket,
                    "stream",
                    {
                        "name": "stdout",
                        "text": self.runner.stdout,
                    },
                )
            if self.runner.stderr:
                self.send_response(
                    self.iopub_socket,
                    "stream",
                    {
                        "name": "stderr",
                        "text": self.runner.stderr,
                    },
                )
        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }


if __name__ == "__main__":
    IPKernelApp.launch_instance(kernel_class=JaclangKernel)

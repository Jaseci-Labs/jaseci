let pyodide = null;

self.onmessage = async (event) => {
    const { type, code } = event.data;

    if (type === "init") {
        importScripts("https://cdn.jsdelivr.net/pyodide/v0.27.0/full/pyodide.js");
        pyodide = await loadPyodide();
        await pyodide.loadPackage("micropip");
        await pyodide.runPythonAsync(`
import micropip
await micropip.install("jaclang==0.7.0")
        `);
        self.postMessage({ type: "ready" });
    }

    if (pyodide) {
        try {
            const jacCode = JSON.stringify(code);
            const output = await pyodide.runPythonAsync(`
from jaclang.cli.cli import run
import sys
from io import StringIO

captured_output = StringIO()
sys.stdout = captured_output
sys.stderr = captured_output

jac_code = ${jacCode}
with open("/tmp/temp.jac", "w") as f:
    f.write(jac_code)
run("/tmp/temp.jac")

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
captured_output.getvalue()
            `);
            self.postMessage({ type: "result", output });
        } catch (error) {
            self.postMessage({ type: "error", error: error.toString() });
        }
    }
};

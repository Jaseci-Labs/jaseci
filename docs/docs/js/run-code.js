let pyodideWorker = null;
let pyodideReady = false;
let pyodideInitPromise = null;

function initPyodideWorker() {
    if (pyodideWorker) return pyodideInitPromise;
    pyodideWorker = new Worker("/js/pyodide-worker.js");
    pyodideInitPromise = new Promise((resolve, reject) => {
        pyodideWorker.onmessage = (event) => {
            if (event.data.type === "ready") {
                pyodideReady = true;
                resolve();
            }
        };
        pyodideWorker.onerror = (e) => reject(e);
    });
    pyodideWorker.postMessage({ type: "init" });
    return pyodideInitPromise;
}

function runJacCodeInWorker(code) {
    return new Promise(async (resolve, reject) => {
        await initPyodideWorker();
        const handleMessage = (event) => {
            if (event.data.type === "result") {
                pyodideWorker.removeEventListener("message", handleMessage);
                resolve(event.data.output);
            } else if (event.data.type === "error") {
                pyodideWorker.removeEventListener("message", handleMessage);
                reject(event.data.error);
            }
        };
        pyodideWorker.addEventListener("message", handleMessage);
        pyodideWorker.postMessage({ type: "run", code });
    });
}

class CodeBlock extends HTMLElement {
    constructor() {
        super();

        const shadow = this.attachShadow({ mode: "open" });
        const container = document.createElement("div");
        container.className = "code-container";

        // Inject external CSS from extra.css
        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = "/extra.css";
        shadow.appendChild(link);

        const code = this.textContent.trim() || "with entry{\n    print('Hello, Jac!');\n}";

        container.innerHTML = `
            <pre><code class="jac-code" contenteditable="true" spellcheck="false" style="display:block; min-height:80px; padding: 5px;">${code}</code></pre>
            <button class="md-button md-button--primary run-code-btn">Run</button>
            <pre class="code-output" style="display:none;"></pre>
        `;

        shadow.appendChild(container);

        container.querySelector(".run-code-btn").addEventListener("click", async () => {
            const outputBlock = container.querySelector(".code-output");
            const codeElem = container.querySelector(".jac-code");
            outputBlock.style.display = "block";
            if (!pyodideReady) {
                outputBlock.textContent = "Loading Jac runner (Pyodide)...";
                await initPyodideWorker();
            }
            outputBlock.textContent = "Running...";
            try {
                const codeToRun = codeElem.textContent.trim();
                const result = await runJacCodeInWorker(codeToRun, outputBlock);
                outputBlock.textContent = `Output:\n${result}`;
            } catch (error) {
                outputBlock.textContent = `Error:\n${error}`;
            }
        });
    }
}

// Define the custom element
customElements.define("code-block", CodeBlock);


document.addEventListener("DOMContentLoaded", () => {
    initPyodideWorker();
});

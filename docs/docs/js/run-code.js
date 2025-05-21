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

function setupCodeBlock(div) {
    if (div.shadowRoot) return;

    const shadow = div.attachShadow({ mode: 'open' });

    const container = document.createElement('div');
    container.className = 'code-container';

    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/extra.css';
    shadow.appendChild(link);
    shadow.appendChild(container);

    const setupBlock = (code) => {
        container.innerHTML = `
            <pre><code class="jac-code" contenteditable="true" spellcheck="false" style="display:block; min-height:80px; padding: 5px;">${code}</code></pre>
            <button class="md-button md-button--primary run-code-btn">Run</button>
            <pre class="code-output" style="display:none;"></pre>
        `;

        const runButton = container.querySelector(".run-code-btn");
        runButton.addEventListener("click", async () => {
            
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
                const result = await runJacCodeInWorker(codeToRun);
                outputBlock.textContent = `Output:\n${result}`;
            } catch (error) {
                outputBlock.textContent = `Error:\n${error}`;
            }
        });
    };

    const inlineCode = div.textContent.trim();
    setupBlock(inlineCode);
}

// Observe and apply when .code-blocks are added
const observer = new MutationObserver(() => {
    document.querySelectorAll('.code-block').forEach(setupCodeBlock);
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});

// Initial loading
document.querySelectorAll('.code-block').forEach(setupCodeBlock);

// Loading Pyodide worker
document.addEventListener("DOMContentLoaded", () => {
    initPyodideWorker();
});

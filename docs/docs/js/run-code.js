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
    if (div._monacoInitialized) return;
    div._monacoInitialized = true;

    const originalCode = div.textContent.trim();

    div.innerHTML = `
        <div class="jac-code" style="border: 1px solid #ccc;"></div>
        <button class="md-button md-button--primary run-code-btn">Run</button>
        <pre class="code-output" style="display:none; white-space: pre-wrap; background: #1e1e1e; color: #d4d4d4; padding: 10px;"></pre>
    `;

    const container = div.querySelector(".jac-code");
    const runButton = div.querySelector(".run-code-btn");
    const outputBlock = div.querySelector(".code-output");

    // Initialize Monaco editor on container
    require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.52.2/min/vs' } });
    require(['vs/editor/editor.main'], function () {
        const editor = monaco.editor.create(container, {
            value: originalCode || '# Write your Jac code here',
            language: 'python',
            theme: 'vs-dark',
            scrollBeyondLastLine: false,
            scrollbar: {
                vertical: 'hidden',
                handleMouseWheel: false,
            },
            automaticLayout: true,
        });

        function updateEditorHeight() {
            const lineCount = editor.getModel().getLineCount();
            const lineHeight = editor.getOption(monaco.editor.EditorOption.lineHeight);
            const height = lineCount * lineHeight + 20;
            container.style.height = `${height}px`;
            editor.layout();
        }

        updateEditorHeight();
        editor.onDidChangeModelContent(updateEditorHeight);

        // On Run button click, get code from editor and run
        runButton.addEventListener("click", async () => {
            outputBlock.style.display = "block";

            if (!pyodideReady) {
                outputBlock.textContent = "Loading Jac runner...";
                await initPyodideWorker();
            }

            outputBlock.textContent = "Running...";
            try {
                const codeToRun = editor.getValue();
                const result = await runJacCodeInWorker(codeToRun);
                outputBlock.textContent = `Output:\n${result}`;
            } catch (error) {
                outputBlock.textContent = `Error:\n${error}`;
            }
        });
    });
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

import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions
} from 'vscode-languageclient/node';
import * as path from 'path';
import * as fs from 'fs';

import {
    makeWebView,
    getDebugGraphData
} from './visual_debugger/visdbg';

let client: LanguageClient;

function getCondaEnvironment(): string | undefined {
    const condaPath = process.env.CONDA_PREFIX;
    if (condaPath) {
        const jacPath = (process.platform === 'win32')
            ? path.join(condaPath, 'Scripts', 'jac.exe')
            : path.join(condaPath, 'bin', 'jac');
        if (fs.existsSync(jacPath)) {
            return jacPath;
        }
    }
    return undefined;
}

function getVenvEnvironment(): string | undefined {
    const venvPath = process.env.VIRTUAL_ENV;
    if (venvPath) {
        const jacPath = (process.platform === 'win32')
            ? path.join(venvPath, 'Scripts', 'jac.exe')
            : path.join(venvPath, 'bin', 'jac');

        if (fs.existsSync(jacPath)) {
            return jacPath;
        }
    }
    return undefined;
}

function getJacInterpreterPath(): string {
    const possiblePath = getCondaEnvironment() || getVenvEnvironment();

    if (possiblePath) {
        return possiblePath;
    }

    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (workspaceFolders) {
        for (const folder of workspaceFolders) {
            const venvJac = (process.platform === 'win32')
                ? path.join(folder.uri.fsPath, 'Scripts', 'jac.exe')
                : path.join(folder.uri.fsPath, 'bin', 'jac');

            if (fs.existsSync(venvJac)) {
                return venvJac;
            }
        }
    }

    return (process.platform === 'win32') ? 'jac.exe' : 'jac';
}

export function activate(context: vscode.ExtensionContext) {
    const jacCommand = getJacInterpreterPath();

    let serverOptions: ServerOptions = {
        run: { command: jacCommand, args: ["lsp"] },
        debug: { command: jacCommand, args: ["lsp"] }
    };

    let clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'jac' }],
    };

    client = new LanguageClient(
        'JacLanguageServer',
        'Jac Language Server',
        serverOptions,
        clientOptions
    );

    client.start().then(() => {
        vscode.window.showInformationMessage('Jac Language Server has started successfully!');
        console.log('Jac Language Server has started successfully!');
    }).catch((error) => {
        vscode.window.showErrorMessage('Failed to start Jac Language Server: ' + error.message);
        console.error('Failed to start Jac Language Server: ', error);
    });

    // Find and return the jac executable's absolute path.
    context.subscriptions.push(vscode.commands.registerCommand('extension.jaclang-extension.getJacPath', config => {

        const programName = (process.platform === 'win32') ? "jac.exe" : "jac";

        const paths = process.env.PATH.split(path.delimiter);
        for (const dir of paths) {
            console.log(dir);
            const fullPath = path.join(dir, programName);
            try {
                fs.accessSync(fullPath, fs.constants.X_OK); // Check if file exists and is executable
                console.log(`Found ${programName} at: ${fullPath}`);
                return fullPath;
            } catch (err) {
                // File doesn't exist or isn't executable in this directory
            }
        }

        const err_msg = `Couldn't find ${programName} in the PATH.`;
        console.error(err_msg);
        vscode.window.showErrorMessage(err_msg);
        return null;
	}));

    // Debugger Visualize Plugin.
	let webviewPanel: vscode.WebviewPanel | undefined;
    let graphData: JSON = JSON.parse('{}');

    context.subscriptions.push(
        vscode.commands.registerCommand('jac.visualize', async () => {
            if (webviewPanel) {
                webviewPanel.reveal();
            } else {
                webviewPanel = makeWebView();
                webviewPanel.onDidDispose(() => { webviewPanel = undefined; });
            }
        })
    );

    vscode.debug.onDidStartDebugSession(async (event) => {
        if (webviewPanel) {
            graphData = await getDebugGraphData();
            if (graphData != null) {
                webviewPanel.webview.postMessage({
                    "command": "init",
                    "data": graphData,
                });
            }
        }
    });

	vscode.debug.onDidChangeActiveStackItem(async (event) => {
		if (webviewPanel) {
			graphData = await getDebugGraphData();
			if (graphData != null) {
				webviewPanel.webview.postMessage({
                    "command": "update",
                    "data": graphData,
                });
			}
		}
	});

    vscode.debug.onDidTerminateDebugSession(async (event) => {
        if (webviewPanel) {
            webviewPanel.webview.postMessage({
                "command": "clear",
            });
        }
    });
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

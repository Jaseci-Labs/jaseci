import * as vscode from 'vscode';
import { makeWebView, getDebugGraphData } from '../visual_debugger/visdbg';

export let webviewPanel: vscode.WebviewPanel | undefined;

export function setupVisualDebuggerWebview(context: vscode.ExtensionContext, envManager: any) {
    vscode.debug.onDidStartDebugSession(async () => {
        if (webviewPanel) {
            const graphData = await getDebugGraphData();
            if (graphData != null) {
                webviewPanel.webview.postMessage({
                    "command": "init",
                    "data": graphData,
                });
            }
        }
    });

    vscode.debug.onDidChangeActiveStackItem(async () => {
        if (webviewPanel) {
            const graphData = await getDebugGraphData();
            if (graphData != null) {
                webviewPanel.webview.postMessage({
                    "command": "update",
                    "data": graphData,
                });
            }
        }
    });

    vscode.debug.onDidTerminateDebugSession(() => {
        if (webviewPanel) {
            webviewPanel.webview.postMessage({
                "command": "clear",
            });
        }
    });
}

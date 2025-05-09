import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions
} from 'vscode-languageclient/node';

export let client: LanguageClient;

export function setupLspClient(envManager: { getJacPath(): string }) {
    const jacPath = envManager.getJacPath();
    const serverOptions: ServerOptions = {
        run: { command: jacPath, args: ['lsp'] },
        debug: { command: jacPath, args: ['lsp'] }
    };
    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'jac' }],
    };
    client = new LanguageClient(
        'JacLanguageServer',
        'Jac Language Server',
        serverOptions,
        clientOptions
    );
    client.start().then(() => {
        vscode.window.showInformationMessage('Jac Language Server started!');
    }).catch((error) => {
        vscode.window.showErrorMessage('Failed to start Jac Language Server: ' + error.message);
    });
    return client;
}

export function stopLspClient(): Thenable<void> | undefined {
    if (!client) return undefined;
    return client.stop();
}

import * as path from 'path';
import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind
} from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
    vscode.window.showInformationMessage('Starting Extension');
    let serverModule = context.asAbsolutePath(
        path.join('src', 'server.py')
    );

    let serverOptions: ServerOptions = {
        run: { command: 'python3', args: [serverModule] },
        debug: { command: 'python3', args: [serverModule] }
    };

    let clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'jac' }],
    };

    client = new LanguageClient(
        'myLanguageServer',
        'Jac Language Server',
        serverOptions,
        clientOptions
    );

    client.start();
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

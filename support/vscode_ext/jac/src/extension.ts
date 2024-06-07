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
    vscode.window.showInformationMessage('Jac Language Extension is activated!');
    console.log('Jac Language Extension is activated!');
    let serverModule = context.asAbsolutePath(
        path.join('src', 'server.jac')
    );

    let serverOptions: ServerOptions = {
        run: { command: 'jac', args: ["run", serverModule] },
        debug: { command: 'jac', args: ["run", serverModule] }
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

}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

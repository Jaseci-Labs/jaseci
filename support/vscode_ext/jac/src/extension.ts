import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions
} from 'vscode-languageclient/node';
import * as path from 'path';

let client: LanguageClient;

function getCondaEnvironment(): string | undefined {
    const condaPath = process.env.CONDA_PREFIX;
    if (condaPath) {
        return path.join(condaPath, 'bin', 'jac');
    }
    return undefined;
}

export function activate(context: vscode.ExtensionContext) {
    const condaJac = getCondaEnvironment();
    const jacCommand = condaJac ? condaJac : 'jac';

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
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

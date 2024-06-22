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
        const jacPath = path.join(condaPath, 'bin', 'jac');
        if (fs.existsSync(jacPath)) {
            return jacPath;
        }
    }
    return undefined;
}

function getVenvEnvironment(): string | undefined {
    const venvPath = process.env.VIRTUAL_ENV;
    if (venvPath) {
        const jacPath = path.join(venvPath, 'bin', 'jac');
        if (fs.existsSync(jacPath)) {
            return jacPath;
        }
    }
    return undefined;
}

export function activate(context: vscode.ExtensionContext) {
    const condaJac = getCondaEnvironment();
    const venvJac = getVenvEnvironment();
    const jacCommand = condaJac ? condaJac : (venvJac ? venvJac : 'jac');

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

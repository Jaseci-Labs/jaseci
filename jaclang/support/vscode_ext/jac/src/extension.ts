import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions
} from 'vscode-languageclient/node';
import * as path from 'path';
import * as fs from 'fs';

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
    const jacCommand = condaJac || venvJac || 'jac';

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
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

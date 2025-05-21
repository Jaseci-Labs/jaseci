import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { runJacCommandForCurrentFile } from '../utils';
import { COMMANDS } from '../constants';

export function registerAllCommands(context: vscode.ExtensionContext, envManager: any) {
    context.subscriptions.push(
        vscode.commands.registerCommand(COMMANDS.SELECT_ENV, () => {
            envManager.promptEnvironmentSelection();
        })
    );
    context.subscriptions.push(
        vscode.commands.registerCommand(COMMANDS.RUN_FILE, () => {
            runJacCommandForCurrentFile('run');
        })
    );
    context.subscriptions.push(
        vscode.commands.registerCommand(COMMANDS.CHECK_FILE, () => {
            runJacCommandForCurrentFile('check');
        })
    );
    context.subscriptions.push(
        vscode.commands.registerCommand(COMMANDS.SERVE_FILE, () => {
            runJacCommandForCurrentFile('serve');
        })
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('extension.jaclang-extension.getJacPath', config => {
            const programName = (process.platform === 'win32') ? "jac.exe" : "jac";
            const paths = process.env.PATH.split(path.delimiter);
            for (const dir of paths) {
                const fullPath = path.join(dir, programName);
                try {
                    fs.accessSync(fullPath, fs.constants.X_OK);
                    return fullPath;
                } catch (err) {
                    // Not found or not executable
                    // Ignore and continue searching
                }
            }
            const err_msg = `Couldn't find ${programName} in the PATH.`;
            vscode.window.showErrorMessage(err_msg);
            return null;
        })
    );
}

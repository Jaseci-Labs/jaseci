import * as vscode from 'vscode';
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
}

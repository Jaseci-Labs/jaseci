import * as vscode from 'vscode';
import { TERMINAL_NAME } from '../constants';

export function runJacCommandForCurrentFile(command: string) {
    const filePath = vscode.window.activeTextEditor?.document.uri.fsPath;
    if (filePath) {
        let terminal = vscode.window.terminals.find(t => t.name === TERMINAL_NAME);
        if (!terminal) {
            terminal = vscode.window.createTerminal(TERMINAL_NAME);
        }
        terminal.show();
        terminal.sendText(`jac ${command} "${filePath}"`);
    }
}

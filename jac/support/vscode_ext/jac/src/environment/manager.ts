import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { findPythonEnvsWithJac } from '../utils/envDetection';

export class EnvManager {
    private context: vscode.ExtensionContext;
    private statusBar: vscode.StatusBarItem;
    private jacPath: string | undefined;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
        this.statusBar.command = 'jaclang-extension.selectEnv';
        context.subscriptions.push(this.statusBar);
    }

    async init() {
        this.jacPath = this.context.globalState.get<string>('jacEnvPath');
        if (!this.jacPath) {
            await this.promptEnvironmentSelection();
        }
        this.updateStatusBar();
    }

    getJacPath(): string {
        if (this.jacPath) return this.jacPath;
        // Fallback: try to find jac in PATH
        return process.platform === 'win32' ? 'jac.exe' : 'jac';
    }

    async promptEnvironmentSelection() {
        const envs = await findPythonEnvsWithJac();
        if (envs.length === 0) {
            vscode.window.showWarningMessage("No environments with 'jac' executable found.");
            return;
        }
        const choice = await vscode.window.showQuickPick(envs, {
            placeHolder: "Select the environment containing 'jac'"
        });
        if (choice) {
            this.jacPath = choice;
            await this.context.globalState.update('jacEnvPath', choice);
            this.updateStatusBar();
            vscode.window.showInformationMessage(`Jac environment set to: ${choice}`);
            vscode.commands.executeCommand("workbench.action.reloadWindow");
        }
    }

    updateStatusBar() {
        const label = this.jacPath ? path.basename(this.jacPath) : 'No Env';
        this.statusBar.text = `Jac Env: ${label}`;
        this.statusBar.tooltip = this.jacPath || 'No Jac environment selected';
        this.statusBar.show();
    }
}

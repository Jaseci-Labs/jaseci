import * as assert from 'assert';
import * as vscode from 'vscode';
import * as sinon from 'sinon';

suite('Extension Tests', () => {
    test('Extension activates', async () => {
        const ext = vscode.extensions.getExtension('jaclang.jaclang-extension');
        assert.ok(ext, 'Extension not found');
        await ext!.activate();
        assert.ok(ext!.isActive, 'Extension did not activate');
    });

    test('Commands are registered', async () => {
        const commands = await vscode.commands.getCommands(true);
        assert.ok(commands.includes('jaclang-extension.selectEnv'), 'selectEnv not registered');
        assert.ok(commands.includes('jaclang-extension.runFile'), 'runFile not registered');
        assert.ok(commands.includes('jaclang-extension.checkFile'), 'checkFile not registered');
        assert.ok(commands.includes('jaclang-extension.serveFile'), 'serveFile not registered');
    });

    test('Visual Debugger WebView command opens panel', async () => {
        const spy = sinon.spy(vscode.window, 'createWebviewPanel');
        await vscode.commands.executeCommand('jac.visualize');
        assert.ok(spy.called, 'Webview panel was not created');
        spy.restore();
    });
});

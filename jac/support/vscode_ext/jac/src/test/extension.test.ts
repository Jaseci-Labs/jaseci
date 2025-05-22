import * as assert from 'assert';
import * as vscode from 'vscode';
import * as sinon from 'sinon';

suite('Extension Tests', () => {
    suiteSetup(async function() {
        this.timeout(10000);
        const ext = vscode.extensions.getExtension('jaseci-labs.jaclang-extension');
            await ext.activate();
    });

    test('Commands are registered', async () => {
        const commands = await vscode.commands.getCommands(true);
        console.log('Registered commands:', commands);
        // print all commands start in 'jaclang-extension'
        const jacCommands = commands.filter(cmd => cmd.startsWith('jaclang-extension.'));
        console.log('Jac commands:', jacCommands);
        assert.ok(commands.includes('jaclang-extension.selectEnv'), 'jaclang-extension.selectEnv not registered');
        assert.ok(commands.includes('jaclang-extension.runCurrentFile'), 'runCurrentFile not registered');
        assert.ok(commands.includes('jaclang-extension.checkCurrentFile'), 'checkCurrentFile not registered');
        assert.ok(commands.includes('jaclang-extension.serveCurrentFile'), 'serveCurrentFile not registered');
    });

    test('Visual Debugger WebView command opens panel', async () => {
        const spy = sinon.spy(vscode.window, 'createWebviewPanel');
        await vscode.commands.executeCommand('jac.visualize');
        assert.ok(spy.called, 'Webview panel was not created');
        spy.restore();
    });
});
import * as assert from 'assert';
import * as vscode from 'vscode';
import * as sinon from 'sinon';

suite('Extension Tests', () => {
    test('Extension activates', async () => {
        console.log('Activating extension...');
        const ext = vscode.extensions.getExtension('jaseci-labs.jaclang-extension');
        console.log('Extension found:', ext);
        
        assert.ok(ext, 'Extension not found');

        const pythonExt = vscode.extensions.getExtension('ms-python.python');
        assert.ok(pythonExt, 'Dependency extension "ms-python.python" not found. Check test setup and installation of dependencies.');

        await ext!.activate();
        console.log('Extension activated:', ext!.isActive);
        assert.ok(ext!.isActive, 'Extension did not activate');
    });

    test('Commands are registered', async () => {
        const commands = await vscode.commands.getCommands(true);
        assert.ok(commands.includes('jaclang-extension.selectEnv'), 'selectEnv not registered');
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

import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Command Execution', () => {
    suiteSetup(async () => {
        const ext = vscode.extensions.getExtension('jaseci-labs.jaclang-extension');
        if (ext) {
            await ext.activate();
        }
    });

    test('jaclang-extension.getJacPath returns path or null', async () => {
        const result = await vscode.commands.executeCommand('extension.jaclang-extension.getJacPath');
        assert.ok(typeof result === 'string' || result === null, 'getJacPath did not return string or null');
    });
});

import * as assert from 'assert';
import * as sinon from 'sinon';
import * as lspClientModule from '../lsp/client';

suite('LSP Client', () => {
    test('setupLspClient initializes client', () => {
        const envManager = { getJacPath: () => 'jac' };
        const stub = sinon.stub(lspClientModule, 'setupLspClient').returns({ start: () => {}, stop: () => {} } as any);
        const client = lspClientModule.setupLspClient(envManager);
        assert.ok(client, 'LSP client not initialized');
        stub.restore();
    });
});
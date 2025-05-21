import mock = require('mock-require');
// Mock EnvManager for tests
mock('../../env/manager', {
    EnvManager: class {
        constructor() {}
        async init() {}
    }
});

import * as path from 'path';
import * as Mocha from 'mocha';

export function run(): Promise<void> {
    // Create the mocha test
    const mocha = new Mocha({
        ui: 'tdd',
        color: true
    });

    const testDir = __dirname;

    // Add files to the test suite (use .js, not .ts)
    mocha.addFile(path.join(testDir, '../extension.test.js'));
    mocha.addFile(path.join(testDir, '../commands.test.js'));
    mocha.addFile(path.join(testDir, '../lspClient.test.js'));

    return new Promise((resolve, reject) => {
        mocha.run(failures => {
            if (failures > 0) {
                reject(new Error(`${failures} tests failed.`));
            } else {
                resolve();
            }
        });
    });
}

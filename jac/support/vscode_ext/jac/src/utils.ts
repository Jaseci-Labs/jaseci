import * as fs from 'fs';
import * as path from 'path';
import * as cp from 'child_process';

export async function findPythonEnvsWithJac(): Promise<string[]> {
    const envs: string[] = [];

    // 1. Check PATH
    const searchDirs = process.env.PATH?.split(path.delimiter) || [];
    for (const dir of searchDirs) {
        const jacPath = path.join(dir, process.platform === 'win32' ? 'jac.exe' : 'jac');
        if (fs.existsSync(jacPath)) {
            envs.push(jacPath);
        }
    }

    // 2. Check Conda environments
    try {
        const condaInfo = cp.execSync('conda env list', { encoding: 'utf8' });
        const condaLines = condaInfo.split('\n');
        for (const line of condaLines) {
            const match = line.match(/^(.*?)\s+(\S+)/);
            if (match) {
                const envPath = match[2];
                const jacPath = path.join(envPath, 'bin', 'jac');
                const jacPathWin = path.join(envPath, 'Scripts', 'jac.exe');
                if (fs.existsSync(jacPath)) envs.push(jacPath);
                if (fs.existsSync(jacPathWin)) envs.push(jacPathWin);
            }
        }
    } catch (err) {
        console.warn('conda env list failed:', err);
    }

    // 3. Check WSL Conda environments
    try {
        const wslCondaInfo = cp.execSync('wsl conda env list', { encoding: 'utf8' });
        const wslCondaLines = wslCondaInfo.split('\n');
        for (const line of wslCondaLines) {
            const match = line.match(/^(.*?)\s+(\S+)/);
            if (match) {
                const envPath = match[2];
                const jacPath = `/mnt/${envPath.replace(/^\/mnt\//, '').replace(/\\/g, '/')}/bin/jac`;
                try {
                    const wslCheck = cp.execSync(`wsl test -f ${jacPath} && echo exists || echo missing`, { encoding: 'utf8' }).trim();
                    if (wslCheck === 'exists') envs.push(`wsl:${jacPath}`);
                } catch {}
            }
        }
    } catch (err) {
        console.warn('wsl conda env list failed:', err);
    }

    // 4. Deduplicate
    const uniqueEnvs = [...new Set(envs)];
    return uniqueEnvs;
}

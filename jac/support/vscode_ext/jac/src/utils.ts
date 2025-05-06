import * as fs from 'fs';
import * as path from 'path';
import * as cp from 'child_process';

function isJacInVenv(venvPath: string): string | null {
    const jacPath = path.join(venvPath, 'bin', 'jac');
    const jacPathWin = path.join(venvPath, 'Scripts', 'jac.exe');
    if (fs.existsSync(jacPath)) return jacPath;
    if (fs.existsSync(jacPathWin)) return jacPathWin;
    return null;
}

function walkForVenvs(baseDir: string, depth = 3): string[] {
    const found: string[] = [];
    if (depth === 0) return found;

    const entries = fs.readdirSync(baseDir, { withFileTypes: true });
    for (const entry of entries) {
        if (entry.isDirectory()) {
            const fullPath = path.join(baseDir, entry.name);

            const jacPath = isJacInVenv(fullPath);
            if (jacPath) {
                found.push(jacPath);
            }

            // Continue walking deeper
            try {
                found.push(...walkForVenvs(fullPath, depth - 1));
            } catch {}
        }
    }
    return found;
}


export async function findPythonEnvsWithJac(workspaceRoot: string = process.cwd()): Promise<string[]> {
    const envs: string[] = [];

    // 1. Check PATH
    const searchDirs = process.env.PATH?.split(path.delimiter) || [];
    for (const dir of searchDirs) {
        const jacPath = path.join(dir, process.platform === 'win32' ? 'jac.exe' : 'jac');
        if (fs.existsSync(jacPath)) {
            envs.push(jacPath);
        }
    }

    // 2. Conda environments
    try {
        const condaInfo = cp.execSync('conda env list', { encoding: 'utf8' });
        const condaLines = condaInfo.split('\n');
        for (const line of condaLines) {
            const match = line.match(/^(.*?)\s+(\S+)/);
            if (match) {
                const envPath = match[2];
                const jacPath = isJacInVenv(envPath);
                if (jacPath) envs.push(jacPath);
            }
        }
    } catch (err) {
        console.warn('conda env list failed:', err);
    }

    // 3. WSL Conda environments (skip if already inside WSL)
    if (!process.env.WSL_DISTRO_NAME) {
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
        } catch {
            console.warn('Skipping WSL conda env list (likely inside WSL or no permission)');
        }
    }

    // 4. Local venvs in workspace
    const localVenvDirs = ['.venv', 'venv', 'env'];
    for (const dirName of localVenvDirs) {
        const jacPath = isJacInVenv(path.join(workspaceRoot, dirName));
        if (jacPath) envs.push(jacPath);
    }

    // 5. Walk home directory (or workspace) to find other venvs
    const homeDir = process.env.HOME || process.env.USERPROFILE || workspaceRoot;
    envs.push(...walkForVenvs(homeDir, 6));  // limit search to depth 3
    const venvWrapperDir = path.join(homeDir, '.virtualenvs');
    if (fs.existsSync(venvWrapperDir)) {
        envs.push(...walkForVenvs(venvWrapperDir, 2));
    }

    // 6. Deduplicate
    // const uniqueEnvs = [...new Set(envs)];
    const uniqueEnvs = Array.from(new Set(envs));

    return uniqueEnvs;
}

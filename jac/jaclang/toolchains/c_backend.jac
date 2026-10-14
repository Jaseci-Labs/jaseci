import os;
import shutil;
import subprocess;
import tempfile;
import from pathlib { Path }

glob LLVM_MAJOR: int = 22,
     C_BACKEND: Artifact = Artifact(
         'llvm-cbe',
         'a13fcf3b27079f4989902594b7c72f81f75c5357',
         'source',
         'https://codeload.github.com/JuliaHubOSS/llvm-cbe/tar.gz/a13fcf3b27079f4989902594b7c72f81f75c5357',
         'd425227fe3bd6a69299b188754403e20b0c840cf1609955c0ccbb68827e34ab9'
     );

def _c_backend_slot -> Path {
    patch = Path(__file__).parent / 'patches' / 'llvm-cbe-runtime-semantics.patch';
    return build_slot(
        C_BACKEND.name,
        host_platform(),
        f"{C_BACKEND.version[:16]}-{file_digest(patch)[:16]}"
    );
}

def _c_backend_binary -> Path {
    return _c_backend_slot() / 'bin' / executable('llvm-cbe');
}

def _llvm_config -> (str | None) {
    return shutil.which(f'llvm-config-{LLVM_MAJOR}') or shutil.which('llvm-config');
}

obj CBackendArtifact(ArtifactBase) {
    has name: str = 'llvm-cbe',
        kind: ArtifactKind = ArtifactKind.CAPABILITY,
        release: ReleasePolicy = ReleasePolicy.ON_DEMAND,
        summary: str = 'the LLVM C backend (C source export)';

    override def probe_checkout -> Probe {
        directory = _c_backend_slot();
        binary = _c_backend_binary();
        if slot_ready(directory) and binary.is_file() {
            return Probe.hit(Source.CHECKOUT, str(binary), {});
        }
        return Probe.missing();
    }

    override def checkout_path -> str {
        return str(_c_backend_binary());
    }

    override def build_blocker -> str {
        if not _llvm_config() or not shutil.which('cmake') {
            return f'C source export needs CMake and the LLVM {LLVM_MAJOR} development toolchain (llvm-config)';
        }
        return '';
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        _build_c_backend();
    }
}

def ensure_c_backend -> Path {
    found = require('llvm-cbe').found;
    assert found is not None;
    return Path(found.path);
}

def _build_c_backend {
    patch = Path(__file__).parent / 'patches' / 'llvm-cbe-runtime-semantics.patch';
    directory = _c_backend_slot();
    with FileLock(directory.with_suffix('.lock')) {
        llvm_config = _llvm_config();
        if not llvm_config {
            raise RuntimeError(
                f'the LLVM {LLVM_MAJOR} development toolchain (llvm-config) is missing'
            );
        }
        version = subprocess.check_output(
            [llvm_config, '--version'], text=True
        ).strip();
        if int(version.split('.')[0]) != LLVM_MAJOR {
            raise RuntimeError(
                f'LLVM C backend requires LLVM {LLVM_MAJOR}, found {version}'
            );
        }
        cmake_dir = subprocess.check_output(
            [llvm_config, '--cmakedir'], text=True
        ).strip();
        archive = fetch(C_BACKEND);
        directory.parent.mkdir(parents=True, exist_ok=True);
        with tempfile.TemporaryDirectory(
            prefix=f".tmp.{os.getpid()}.", dir=directory.parent
        ) as temporary {
            staging = Path(temporary);
            extract(archive, staging / 'source');
            source = next((staging / 'source').iterdir());
            subprocess.run(['git', 'apply', str(patch)], cwd=source, check=True);
            build = staging / 'build';
            env = dict(os.environ);
            run_step(
                'Configuring the LLVM C backend',
                [
                    'cmake',
                    '-S',
                    str(source),
                    '-B',
                    str(build),
                    '-DCMAKE_BUILD_TYPE=Release',
                    f'-DLLVM_DIR={cmake_dir}'
                ],
                staging,
                env
            );
            run_step(
                'Building the LLVM C backend',
                [
                    'cmake',
                    '--build',
                    str(build),
                    '--parallel',
                    str(min(os.cpu_count() or 1, 4))
                ],
                staging,
                env
            );
            ready = staging / 'ready';
            (ready / 'bin').mkdir(parents=True);
            shutil.copy2(
                build / 'tools' / 'llvm-cbe' / executable('llvm-cbe'), ready / 'bin'
            );
            shutil.copy2(source / 'LICENSE', ready / 'LICENSE');
            publish_build_slot(ready, directory);
        }
    }
}


def c_backend_provenance -> dict[str, str | int] {
    patch = Path(__file__).parent / 'patches' / 'llvm-cbe-runtime-semantics.patch';
    return {
        'name': C_BACKEND.name,
        'revision': C_BACKEND.version,
        'source': C_BACKEND.url,
        'source_sha256': C_BACKEND.digest,
        'patch_sha256': file_digest(patch),
        'llvm_major': LLVM_MAJOR
    };
}

def c_backend_license -> Path {
    return Path(__file__).parent / 'patches' / 'llvm-cbe-LICENSE';
}

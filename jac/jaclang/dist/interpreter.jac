import ctypes;
import os;
import sys;

def running_jacpython -> bool {
    return hasattr(ctypes.pythonapi, "_PyJac_CompilerRequired");
}

def _repo_root -> str {
    return os.path.dirname(jaclang_pkg_root());
}

def jacpython_binary -> str {
    return os.path.join(_repo_root(), "zig-out", "jacpython", "bin", "jac");
}

def _this_process(source: Source) -> Probe {
    if running_jacpython() {
        return Probe.hit(source, sys.executable, {});
    }
    built = jacpython_binary();
    return Probe.missing(
        f"this jac bundles CPython; the JacPython build is {built}"
            if os.path.isfile(built)
            else "this jac bundles CPython; `jac native build jacpython` builds a jac on JacPython"
    );
}

obj JacPythonArtifact(Artifact) {
    has name: str = "jacpython",
        kind: ArtifactKind = ArtifactKind.ACCELERATOR,
        release: ReleasePolicy = ReleasePolicy.FLOOR,
        summary: str = "JacPython (the interpreter whose compiler is native Jac)",
        floor: str = "CPython",
        hosts: list[str] = ["linux", "darwin"];

    override def probe_sealed -> (Probe | None) {
        if sealed._jaclang_image() is None {
            return None;
        }
        return Probe.hit(Source.SEALED, sys.executable, {})
            if running_jacpython()
            else Probe.by_design();
    }

    override def probe_checkout -> Probe {
        return _this_process(Source.CHECKOUT);
    }

    override def probe_kit -> Probe {
        if kit_image() is None {
            return Probe.missing("this process runs on no kit");
        }
        return _this_process(Source.KIT);
    }

    override def checkout_path -> str {
        return jacpython_binary();
    }

    override def built -> Probe {
        path = jacpython_binary();
        return Probe.hit(Source.CHECKOUT, path, {})
            if os.path.isfile(path)
            else Probe.missing();
    }

    override def build_blocker -> str {
        import shutil;
        return "" if shutil.which("zig") else "zig is not on PATH";
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        import subprocess;
        prefix = os.path.dirname(os.path.dirname(jacpython_binary()));
        argv = ["zig", "build", "-Dpython=jacpython", "--prefix", prefix];
        if not exact {
            argv.append("-Dreuse-python=true");
        }
        log("  " + " ".join(argv));
        subprocess.run(argv, cwd=_repo_root(), check=True);
        log(f"  run JacPython with {jacpython_binary()}");
    }
}

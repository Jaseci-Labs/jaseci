import ctypes;
import os;
import sys;
import from jaclang.artifacts.model {
    Artifact,
    ArtifactKind,
    Probe,
    ReleasePolicy,
    Source
}

def running_jacpython -> bool {
    return hasattr(ctypes.pythonapi, "_PyJac_CompilerRequired");
}

def _repo_root -> str {
    import from jaclang.compiler.frontend.codeinfo { jaclang_pkg_root }
    return os.path.dirname(jaclang_pkg_root());
}

obj JacPythonArtifact(Artifact) {
    has name: str = "jacpython",
        kind: ArtifactKind = ArtifactKind.ACCELERATOR,
        release: ReleasePolicy = ReleasePolicy.FLOOR,
        summary: str = "JacPython (the interpreter whose compiler is native Jac)",
        floor: str = "CPython",
        hosts: list[str] = ["linux", "darwin"];

    override def probe_sealed -> (Probe | None) {
        import from jaclang.jac0core { sealed }
        if sealed._jaclang_image() is None {
            return None;
        }
        return Probe.hit(Source.SEALED, sys.executable, {})
            if running_jacpython()
            else Probe.by_design();
    }

    override def probe_checkout -> Probe {
        tree = self.checkout_path();
        stamp = os.path.join(tree, "build-key");
        return Probe.hit(Source.CHECKOUT, tree, {})
            if os.path.isfile(stamp)
            else Probe.missing();
    }

    override def probe_kit -> Probe {
        import from jaclang.artifacts.kit { kit_image }
        if kit_image() is None {
            return Probe.missing("this process runs on no kit");
        }
        return Probe.hit(Source.KIT, sys.executable, {})
            if running_jacpython()
            else Probe.by_design();
    }

    override def checkout_path -> str {
        import from jaclang.artifacts.kit { osarch }
        return os.path.join(_repo_root(), ".python-build", "jacpython", osarch());
    }

    override def build_blocker -> str {
        import shutil;
        return "" if shutil.which("zig") else "zig is not on PATH";
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        import subprocess;
        argv = ["zig", "build", "build-python", "-Dpython=jacpython"];
        if not exact {
            argv.append("-Dreuse-python=true");
        }
        log("  " + " ".join(argv));
        subprocess.run(argv, cwd=_repo_root(), check=True);
    }
}

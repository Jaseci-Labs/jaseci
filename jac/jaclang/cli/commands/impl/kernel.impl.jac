import os;
import time;
import from jaclang.cli.console { console }
import from jaclang.compiler.backends.native.kernel_resolve {
    build_kernel,
    kit_kernel,
    resolve_kernel,
    source_tree_kernel_path,
    tree_kernel
}


def _is_sealed -> bool {
    import from jaclang.jac0core { sealed }
    return sealed._jaclang_image() is not None;
}


def _toolchain_refusal -> str {
    import from jaclang.compiler.driver.toolchain { native_pipeline_available }
    (ok, why) = native_pipeline_available();
    return "" if ok else (why or "the native toolchain is unavailable");
}


def _log(message: str) {
    console.print(message);
}


def _print_drift(drift: list[str]) {
    for reason in drift[:20] {
        console.print(f"    - {reason}");
    }
    if len(drift) > 20 {
        console.print(f"    ... and {len(drift) - 20} more");
    }
}


def _kernel_status -> int {
    if _is_sealed() {
        found = resolve_kernel();
        if found is None {
            console.print("kernel: none (this kit runs the compiler from bytecode)");
        } else {
            console.print(f"kernel: sealed, {found.lib_path}");
        }
        return 0;
    }
    (tree, drift) = tree_kernel();
    console.print(f"checkout kernel: {source_tree_kernel_path()}");
    if tree is not None {
        console.print("  current: built from these sources");
    } else {
        console.print("  not usable:");
        _print_drift(drift);
    }
    (kit, kit_drift) = kit_kernel();
    if kit is not None {
        console.print(f"kit kernel: {kit.lib_path}");
        console.print("  current: the kit was built from these sources");
    } elif kit_drift and kit_drift[0] != "this process runs on no kit" {
        console.print("kit kernel: not usable");
        _print_drift(kit_drift[:1]);
    }
    found = resolve_kernel();
    if found is not None {
        console.print(
            f"running: the {'checkout'
                if found.source == 'tree'
                else found.source} kernel"
        );
    } else {
        refusal = _toolchain_refusal();
        console.print(
            f"running from bytecode: {refusal
                or 'run `jac kernel build` for full speed'}"
        );
    }
    return 0;
}


def _kernel_build(force: bool) -> int {
    if _is_sealed() {
        console.error(
            "this jac is a sealed image and runs the kernel it ships with",
            hint="build the kernel from a source checkout"
        );
        return 1;
    }
    refusal = _toolchain_refusal();
    if refusal {
        console.error(f"cannot build the kernel: {refusal}");
        return 1;
    }
    destination = source_tree_kernel_path();
    (tree, drift) = tree_kernel();
    if tree is not None and not force {
        console.success(f"kernel is current: {destination}");
        return 0;
    }
    if drift {
        console.print("Building the native compiler kernel:");
        _print_drift(drift);
    } else {
        console.print("Relinking the native compiler kernel");
    }
    started = time.monotonic();
    build_kernel(destination, log=_log);
    (built, left) = tree_kernel();
    if built is None {
        console.error("the kernel was built but does not match the sources");
        _print_drift(left);
        return 1;
    }
    console.success(
        f"kernel built in {time.monotonic() - started:.1f}s: {destination} "
        f"({os.path.getsize(destination) >> 20} MB)"
    );
    return 0;
}


impl kernel(action: str = "status", force: bool = False) -> int {
    if action == "status" {
        return _kernel_status();
    }
    if action == "build" {
        return _kernel_build(force);
    }
    console.error(f"unknown action: {action} (expected status or build)");
    return 1;
}

import os;
import from .embed { CStrArray, export_ca_bundle }
import from .report { die }
import from _dl_native { dlopen, dlsym, dl_error, RTLD_NOW, RTLD_GLOBAL }

import from c {
    def readlink(path: str, buf: bytes, bufsiz: int) -> int;  def symlink(
        target: str, linkpath: str
    ) -> i32;  obj EngineApi {
        has jac_main: Callable[[i32, int], i32] = 0;
    }
}

def:pub node_path(rt: str) -> str {
    return rt + "/js/bin/node";
}

def:pub is_node_name(argv0: str) -> bool {
    return os.path.basename(argv0) == "node";
}

def link_target(path: str) -> str {
    buf = b"\x00" * 4096;
    n = readlink(path, buf, 4095);
    if n <= 0 {
        return "";
    }
    return buf[0:n].decode();
}

def:pub link_node(rt: str, exe_path: str) {
    """Keep `<rt>/js/bin/node` pointing at this binary: it is the engine's
    `process.execPath` and the `node` its child processes exec, so a binary
    that runs from this runtime re-points a link another copy left behind.""";
    if not os.path.isdir(rt + "/js") {
        return;
    }
    link = node_path(rt);
    if link_target(link) == exe_path {
        return;
    }
    os.makedirs(os.path.dirname(link), exist_ok=True);
    tmp = f"{link}.{os.getpid()}";
    if symlink(exe_path, tmp) == i32(0) {
        os.rename(tmp, link);
    }
}

def:pub run_node(rt: str, argv: list[str]) -> int {
    """Run the JavaScript engine as `node` in this process: load the engine
    library from the runtime tree and hand it argv, with argv[0] the runtime's
    `node` so the engine's execPath names an executable that runs it again,
    and that `node` first on PATH so a tool that spawns `node` by name does too.""";
    export_ca_bundle(rt);
    node_dir = os.path.dirname(node_path(rt));
    os.environ["PATH"] = node_dir + ":" + os.environ.get("PATH", "");
    lib = rt + "/js/libjs_engine.so";
    handle = dlopen(lib, i32(RTLD_NOW | RTLD_GLOBAL));
    if handle == 0 {
        die(f"cannot load the JavaScript engine {lib}: {dl_error()}");
    }
    main_fn = dlsym(handle, "jac_main");
    if main_fn == 0 {
        die(f"{lib} has no jac_main entry");
    }
    api = EngineApi(jac_main=main_fn);
    args = CStrArray([node_path(rt)] + argv[1:]);
    return int(api.jac_main(i32(args.count), args.ptrs));
}

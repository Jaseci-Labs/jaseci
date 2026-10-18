import from jaclang.runtime.build_services { BuildServices }
import type from jaclang.compiler.driver.compiler { JacCompiler }
import type from jaclang.compiler.driver.program { JacProgram }
import type from jaclang.compiler.driver.selfhost { SelfHostCache }
import type from jaclang.client.client_bundle { ClientBundleBuilder }
import type from jaclang.runtime.prepared { PreparedApplication }
import type from jaclang.server.hmr { HotReloader }

obj CompilerBuildServices(BuildServices) {
    def compiler -> JacCompiler;
    def program -> JacProgram;
    def selfhost -> SelfHostCache;
    def client_builder -> ClientBundleBuilder;
    def prepare_application(
        entry_path: str,
        program: JacProgram,
        project_root: str,
        default_codespace: str = ''
    ) -> PreparedApplication;

    def prepare_dynamic_module(
        path: str, program: JacProgram, application: PreparedApplication
    ) -> PreparedApplication;

    def hot_reloader(base_path: str, module_name: str) -> HotReloader;
    def client_runtime_basename(framework: str) -> str;
    def application_edges(
        entry_path: str, app_name: str, app_kind: str, project_root: str
    ) -> list[tuple[str, str]];

    def run_test(
        filepath: str,
        func_name: str | None,
        filter: str | None,
        xit: bool,
        maxfail: int | None,
        directory: str | None,
        verbose: bool
    ) -> int;
}

impl CompilerBuildServices.compiler -> JacCompiler {
    import from jaclang.compiler.driver.compiler { JacCompiler }
    return JacCompiler();
}

impl CompilerBuildServices.program -> JacProgram {
    import from jaclang.compiler.driver.program { JacProgram }
    return JacProgram();
}

impl CompilerBuildServices.selfhost -> SelfHostCache {
    import from jaclang.compiler.driver.selfhost { SelfHostCache }
    return SelfHostCache();
}

impl CompilerBuildServices.client_builder -> ClientBundleBuilder {
    import from jaclang.client.vite_client_bundle { make_client_bundle_builder }
    return make_client_bundle_builder();
}

impl CompilerBuildServices.prepare_application(
    entry_path: str, program: JacProgram, project_root: str, default_codespace: str = ''
) -> PreparedApplication {
    import from jaclang.compiler.driver.application { prepare_application }
    import from jaclang.compiler.frontend.codeinfo { set_effective_default_codespace }
    if default_codespace {
        set_effective_default_codespace(default_codespace);
    }
    return prepare_application(entry_path, program, project_root);
}

impl CompilerBuildServices.prepare_dynamic_module(
    path: str, program: JacProgram, application: PreparedApplication
) -> PreparedApplication {
    import from jaclang.compiler.driver.application { prepare_dynamic_module }
    return prepare_dynamic_module(path, program, application);
}

impl CompilerBuildServices.hot_reloader(
    base_path: str, module_name: str
) -> HotReloader {
    import from jaclang.server.hmr { HotReloader }
    import from jaclang.server.watcher { JacFileWatcher }
    return HotReloader(
        base_path=base_path,
        module_name=module_name,
        watcher=JacFileWatcher(watch_paths=[base_path])
    );
}

impl CompilerBuildServices.client_runtime_basename(framework: str) -> str {
    import from jaclang.compiler.backends.es.backends.registry {
        resolve_framework_backend,
        resolve_active_backend
    }
    backend = resolve_framework_backend(framework)
        if framework
        else resolve_active_backend();
    return backend.runtime_source_basename();
}

impl CompilerBuildServices.application_edges(
    entry_path: str, app_name: str, app_kind: str, project_root: str
) -> list[tuple[str, str]] {
    import from jaclang.compiler.driver.application_edges { application_edges }
    return application_edges(entry_path, app_name, app_kind, project_root);
}

impl CompilerBuildServices.run_test(
    filepath: str,
    func_name: str | None,
    filter: str | None,
    xit: bool,
    maxfail: int | None,
    directory: str | None,
    verbose: bool
) -> int {
    import from jaclang.testing.runner { run_test }
    return run_test(filepath, func_name, filter, xit, maxfail, directory, verbose);
}

import from jaclang.compiler.frontend.unitree { Module }
import from jaclang.compiler.driver.pipeline_types { PassContract }
import from jaclang.compiler.passes.context { CompileContext, CompilerPass }


walker AppContextPass(CompilerPass) {
    static has contract: PassContract = PassContract();

    can run_walk with Module entry;
}

walker AbsorbImportsPass(CompilerPass) {
    static has contract: PassContract = PassContract();

    can run_walk with Module entry;
}

walker BoundaryFactsPass(CompilerPass) {
    static has contract: PassContract = PassContract();

    can run_walk with Module entry;
}

walker NativeImportFactsPass(CompilerPass) {
    static has contract: PassContract = PassContract();

    can run_walk with Module entry;
}

impl AppContextPass.run_walk with Module entry {
    self.prog.stamp_app_facts(here);
    self.prog.stamp_access_check_facts(here);
}

impl AbsorbImportsPass.run_walk with Module entry {
    self.prog.resolve_absorb_imports(here);
}

impl BoundaryFactsPass.run_walk with Module entry {
    self.prog.stamp_boundary_facts(here);
}

impl NativeImportFactsPass.run_walk with Module entry {
    self.prog.stamp_native_import_facts(here);
}

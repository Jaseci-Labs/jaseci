import from jaclang.compiler.frontend.unitree { Module, SemDef, Symbol, UniScopeNode }
import from jaclang.compiler.driver.pipeline_types { PassContract }
import from jaclang.compiler.passes.context { CompileContext, CompilerPass }

walker SemDefMatchPass(CompilerPass) {
    static has contract: PassContract = PassContract(kernel_safe=True);

    def _run_impl(ir_in: Module) -> Module;
    can run_walk with Module entry;
    def resolve_sem_target(
        semdef: SemDef, target_sym_tab: UniScopeNode
    ) -> (Symbol | None);

    def connect_sems(
        source_sym_tab: UniScopeNode, target_sym_tab: UniScopeNode
    ) -> None;
}

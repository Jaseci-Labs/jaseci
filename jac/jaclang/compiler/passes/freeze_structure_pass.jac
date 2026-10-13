import from jaclang.compiler.passes.context { CompileContext, CompilerPass }
import from jaclang.compiler.driver.pipeline_types { AnalysisFact, PassContract }
import jaclang.compiler.frontend.unitree as uni;

walker FreezeStructurePass(CompilerPass) {
    static has contract: PassContract = PassContract(provides=(AnalysisFact.FROZEN, ));
    can freeze with uni.Module entry;
}

impl FreezeStructurePass.freeze with uni.Module entry {
    here.freeze_structure();
}

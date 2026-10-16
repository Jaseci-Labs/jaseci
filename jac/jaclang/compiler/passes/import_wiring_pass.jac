import os;
import from jaclang.compiler.driver.pipeline_types { AnalysisFact, PassContract }
import from jaclang.compiler.passes.context { CompileContext, CompilerPass }
import from jaclang.compiler.frontend.constant { ExprCtx }
import from jaclang.compiler.frontend.unitree {
    Ability,
    AtomTrailer,
    EmptyToken,
    ImplDef,
    GraphImport,
    Import,
    ImportRule,
    ImportWire,
    JsxElementName,
    KWPair,
    Module,
    ModuleItem,
    ModulePath,
    Name,
    String,
    UniNode,
    WireTarget
}
import from jaclang.compiler.frontend.module_facts { ModuleFacts }
import from jaclang.compiler.driver.wiring {
    RuleRec,
    WireBinding,
    WireRec,
    WiringSpec,
    rule_record,
    scope_owners,
    is_arch_file,
    scope_path_of,
    wiring_for_path
}
import from jaclang.project.source { pascal_to_snake }
import from jaclang.compiler.passes.annex_weave { import_form }
import from jaclang.compiler.frontend.diagnostics {
    E1141,
    E1142,
    E1143,
    E1144,
    E1146,
    E2088,
    E2089,
    E2090,
    E2091,
    E2092,
    E2093,
    E2094,
    E2097,
    E2098
}

walker ImportWiringPass(CompilerPass) {
    static has contract: PassContract = PassContract(requires=(AnalysisFact.SYM_OF, ));

    can run_walk with Module entry;
    def _check_arch_module(mod: Module) -> None;
    def _check_scope(spec: WiringSpec, block: GraphImport, seen: set[int]) -> None;
    def _check_wire(spec: WiringSpec, wire: ImportWire) -> None;
    def _check_target(
        spec: WiringSpec, provider: str, provider_ok: bool, target: WireTarget
    ) -> None;
    def _check_rule_liveness(spec: WiringSpec, rule: ImportRule) -> None;
    def _check_edge(
        spec: WiringSpec,
        provider: str,
        consumer: str,
        names: (list[tuple[str, UniNode]] | None),
        at: UniNode
    ) -> None;

    def _check_module(mod: Module, spec: WiringSpec) -> None;
    def _check_import(
        spec: WiringSpec,
        imp: Import,
        consumer: str,
        provided: dict[tuple[str, str, str, str], WireRec],
        enforce: bool,
        nested: bool = False,
        scope: (list[str] | None) = None
    ) -> None;

    def _emit_nested(
        spec: WiringSpec,
        binding: WireBinding,
        at: UniNode,
        consumer: str,
        scope: (list[str] | None)
    ) -> None;

    static def _rule_names(rules: list[RuleRec]) -> str;
}

obj UnusedBinding {
    has consumer: str,
        wire: WireRec,
        binding: WireBinding,
        at: UniNode;
}

def report_unused_wires(reporter: CompilerPass, mod: Module) -> None;
def unused_wire_bindings(mod: Module) -> list[UnusedBinding];
def names_read_in(body: UniNode) -> set[str];

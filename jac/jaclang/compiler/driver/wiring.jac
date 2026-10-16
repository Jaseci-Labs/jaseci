import hashlib;
import os;
import from collections.abc { Iterator }
import from contextlib { contextmanager }
import from contextvars { ContextVar }
import from jaclang.compiler.frontend.unitree {
    Ability,
    Archetype,
    EmptyToken,
    Enum,
    ImplDef,
    GraphImport,
    Import,
    ImportRule,
    ImportWire,
    Module,
    ModuleItem,
    ModulePath,
    ModulePattern,
    Token,
    UniNode
}
import from jaclang.compiler.frontend.constant { Tokens as Tok }
import from jaclang.compiler.frontend.roles { BodyRole, Kid }
import from jaclang.compiler.frontend.host {
    HOST_FACT_GIT_IGNORED,
    HOST_FACT_SEP,
    HOST_FACT_STDLIB_MODULES,
    active_host
}
import from jaclang.compiler.passes.annex_weave {
    WovenAnnex,
    import_form,
    import_items,
    import_keys,
    relative_twin
}

glob ARCH_FILE_NAME: str = "archwire.jac",
     SKIPPED_PROJECT_DIRS: tuple[str, ...] = ("node_modules", "__pycache__"),
     RECORDS_FORMAT: int = 2;

obj WireBinding {
    has provider: str,
        form: str,
        name: str = "",
        alias: str = "";

    def key -> tuple[str, str, str, str] {
        return (self.provider, self.form, self.name, self.alias);
    }

    def wire_text(consumer: str) -> str;
}

obj PatternRec {
    has dotted: str,
        is_glob: bool = False,
        text: str = "";

    def matches(module: str, prefix: str = "") -> bool;
}

obj RuleRec {
    has name: str,
        scope: str,
        sources: list[PatternRec] = [],
        targets: list[PatternRec] = [],
        item_names: set[str] = set(),
        is_open: bool = False;
}

obj WireRec {
    has provider: str,
        consumers: list[str] = [],
        is_module_form: bool = False,
        is_absorb: bool = False,
        is_typed: bool = False,
        is_comptime: bool = False,
        alias: str = "",
        items: list[tuple[str, str]] = [],
        line: int = 0,
        col: int = 0,
        lb_line: int = 0,
        lb_col: int = 0,
        payload: str = "",
        index: int = 0;

    def bindings -> list[WireBinding];
}

obj WiringSpec {
    has root_dir: str,
        path: str,
        parse_failed: bool = False,
        wires: list[WireRec] = [],
        rules: list[RuleRec] = [],
        _raw: dict[str, list[WireRec]] = {},
        _by_consumer: dict[str, list[WireRec]] = {},
        _splits: dict[str, (tuple[str, list[str]] | None)] = {},
        _annex_cache: dict[str, str] = {},
        _policy_digest: str = "",
        _project_modules: (list[str] | None) = None,
        _prefix: (str | None) = None,
        _owned_dirs: dict[str, bool] = {},
        _scopes: dict[tuple[str, int], list[str]] = {},
        _wire_lines: dict[int, WireRec] = {},
        package_prefix: str = "";

    def postinit -> None;
    def module_name(path: str) -> (str | None);
    def _local_name(name: str) -> (str | None);
    def import_prefix -> str;
    def import_name(name: str) -> str;
    def module_file(name: str) -> (str | None);
    def owns(path: str) -> bool;
    def split_consumer(path: str) -> (tuple[str, list[str]] | None);
    def consumer_scope(consumer: str, wire: WireRec) -> list[str];
    def wire_at_line(line: int) -> (WireRec | None);
    def is_package_dir(name: str) -> bool;
    def project_modules -> list[str];
    def _scan_modules(directory: str, found: list[str], seen: set[str]) -> None;
    def consumer_wires(consumer: str) -> list[WireRec];
    def is_covered(consumer: str) -> bool;
    def is_project_module(module: str) -> bool;
    def _wire_pieces(wire: WireRec) -> list[tuple[int, int, str]];
    def annex_source(consumer: str) -> (str | None);
    def digest_for(consumer: str) -> str;
    def consumer_bindings(
        consumer: str, scope: (list[str] | None) = None
    ) -> dict[tuple[str, str, str, str], WireRec];

    def import_provider(path_node: ModulePath) -> (str | None);
    def rules_for_provider(provider: str) -> list[RuleRec];
    def rules_admitting(provider: str, consumer: str) -> list[RuleRec];
    static def admitted_names(rules: list[RuleRec]) -> (set[str] | None);
}

glob _spec_cache: dict[str, tuple[tuple[float, int], WiringSpec]] = {},
     _resolution: ContextVar[dict[str, WiringSpec | None] | None] = ContextVar(
         'jac_wiring_resolution', `default=None
     ),
     _building: set[str] = set(),
     _STDLIB_NAMES: list[set[str]] = [];

@contextmanager
def wiring_scope -> Iterator[None] {
    if _resolution.get() is not None {
        yield ;
        return;
    }
    token = _resolution.set({});
    try {
        yield ;
    } finally {
        _resolution.reset(token);
    }
}

def is_arch_file(path: str) -> bool;
def arch_file_for(path: str) -> (str | None);
def wiring_for_path(path: str) -> (WiringSpec | None);
def wiring_annex_for(file_path: str) -> (WovenAnnex | None);
def wiring_digest_for(file_path: str) -> str;
def dedupe_generated_imports(mod: Module) -> None;
def compiled_by_seed(path: str) -> bool;
def is_kernel_abi_contract(path: str) -> bool;
def is_native_stdlib_source(path: str) -> bool;
def pattern_text(pattern: ModulePattern) -> str;
def pattern_record(pattern: ModulePattern) -> PatternRec;
def rule_record(rule: ImportRule) -> RuleRec;
def wire_record(wire: ImportWire, source: str = "") -> WireRec;
def parse_records(source: str, path: str) -> tuple[bool, list[WireRec], list[RuleRec]];
def encode_records(
    parse_failed: bool, wires: list[WireRec], rules: list[RuleRec]
) -> str;

def decode_records(text: str) -> (tuple[bool, list[WireRec], list[RuleRec]] | None);
def _split_list(text: str) -> list[str];
def _encode_patterns(patterns: list[PatternRec]) -> str;
def _decode_patterns(text: str) -> (list[PatternRec] | None);
def import_prefix_for(root_dir: str) -> str;
def is_stdlib_module(name: str) -> bool;

def _load_spec(root_dir: str, arch_path: str) -> WiringSpec;
def scope_path_of(nd: UniNode) -> (list[str] | None);
def scope_owners(mod: Module) -> dict[str, (Ability | ImplDef)];
def inject_into_scope(owner: (Ability | ImplDef), stmt: UniNode) -> None;
def local_module_name(root_dir: str, path: str) -> (str | None);

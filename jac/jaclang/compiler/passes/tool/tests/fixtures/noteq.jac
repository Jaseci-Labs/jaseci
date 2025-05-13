with entry {
    sym_tabs = [sym_tab] if not isinstance(sym_tab, uni.Module) and sym_tab.loc.mod_path != file_path else [];
}
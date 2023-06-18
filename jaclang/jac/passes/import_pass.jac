"""Import Pass written in Jac bootstrapped with Python strategy."""

import:py jaclang.jac.ast;
import:py os;
import:py from jaclang.jac.ast, AstNode, is_blank;
import:py from jaclang.jac.passes.ir_pass, Pass;
import:py from jaclang.jac.utils, jac_file_to_ast;


object ImportPass:Pass {
    has symbol_table: dict[str, any];

    can exit_import(nd:AstNode) {
        alias = None;
        if nd.lang == 'jac' {
            if not is_blank(nd.alias) {
                alias = nd.alias.value;
                alias |> print;
            }

        }
    }
}

can import_path_to_dir(import_path:str) -> str {
    parts = '.' |> import_path.split;
    directory = *parts |> os.path.join;
    return directory;
}

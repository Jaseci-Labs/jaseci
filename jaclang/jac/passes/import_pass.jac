"""Import Pass written in Jac bootstrapped with Python strategy."""

import:py jaclang.jac.absyntree as ast;
import:py os;
import:py from jaclang.jac.absyntree, AstNode;
import:py from jaclang.jac.passes.ir_pass, Pass;
import:py from jaclang.jac.utils, jac_file_to_ast;

"""
ImportPass is a pass that handles import statements.
It is responsible for:
    - Resolving the import path to a directory
    - Loading the AST from the directory
    - Adding the AST to the symbol table
"""
object ImportPass:Pass {
    has symbol_table: dict[str, any];

    can exit_import(nd:AstNode) {
        alias = None;
        if nd.lang == 'jac' {
            if not nd.alias {
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


with entry {
  print("hello world");
}
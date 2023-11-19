"""Implementations for the jac command line interface."""
import:py os;
import:py shutil;
import:py unittest;
import:py from jaclang.jac.constant, Constants as C;

"""Load a .jac file and return the entrypoint function."""
:c:run
(filename: str, main: bool = True) {
    if filename.endswith(".jac"){
        [base, mod] = os.path.split(filename);
        base = './' if not base else base;
        mod=mod[:-4];
        __jac_import__(
            target=mod, base_path=base,
            override_name=("__main__" if main else None)
        );
    } else {
        "Not a .jac file." :> print;
    }
}

"""Run the entrypoint of the given .jac file."""
:c:enter
(filename: str, entrypoint: str, args: list) {
    if filename.endswith(".jac") {
        [base, mod] = os.path.split(filename);
        base = './' if not base else base;
        mod=mod[:-4];
        mod = __jac_import__(target=mod, base_path=base);
        if not mod {
            print('Errors occured while importing the module.');
            return;
        }
        else {
            :> ((mod, entrypoint) :> getattr );
        }
    } else {
        "Not a .jac file." :> print;
    }
}

"""Load a .jac file and return the entrypoint function."""
:c:<>test
(filename: str) {
    if filename.endswith(".jac"){
        [base, mod] = os.path.split(filename);
        base = './' if not base else base;
        mod=mod[:-4];
        mod = __jac_import__(target=mod, base_path=base);
        unittest.TextTestRunner().run(mod.__jac_suite__);
    } else {
        "Not a .jac file." :> print;
    }
}

:c:ast_tool
(tool: str, args: list) {
    import:py from jaclang.utils.lang_tools, AstTool;
    if(hasattr(AstTool, tool)) {
        try {
            if(len(args)) { print(getattr(AstTool(), tool)(args)); }
            else { print(getattr(AstTool(), tool)()); }
        } except Exception {
            print(f"Error while running ast tool {tool}, check args.");
        }
    } else {
        print(f"Ast tool {tool} not found.");
    }
}

"""Remove the __jac_gen__ , __pycache__ folders from the current directory recursevely."""
:c:clean {
    current_dir = os.getcwd();
    py_cache = "__pycache__";
    for (root, dirs, files) in os.walk(current_dir, topdown=True) {
        for folder_name in dirs[:] {
            if folder_name == C.JAC_GEN_DIR or folder_name == py_cache {
                folder_to_remove = os.path.join(root, folder_name);
                shutil.rmtree(folder_to_remove);
                print(f"Removed folder: {folder_to_remove}");
            }
        }
    }
    print("Done cleaning.");
}


"""Implementations for the jac command line interface."""
import:py from os, path, shutil;

:a:load(filename: str) {
    #* Load a .jac file and return the entrypoint function. *#
    if filename.endswith(".jac"){
        [base, mod] = path.split(filename);
        base = './' if not base else base;
        mod=mod[:-4];
        __jac_import__(target=mod, base_path=base);
    } else {
        "Not a .jac file." :> print;
    }
}


:a:run(filename: str, entrypoint: str, args: list) {
    #* Run the entrypoint of the given .jac file. *#
    if filename.endswith(".jac"){
        [base, mod] = path.split(filename);
        base = './' if not base else base;
        mod=mod[:-4];
        mod = __jac_import__(target=mod, base_path=base);
        :> ((mod, entrypoint) :> getattr );
    } else {
        "Not a .jac file." :> print;
    }
}

:a:clean() {
    #* Remove the __jac_gen__ , __pycache__ folders from the current directory recursevely. *#
    current_dir = os.getcwd();
    jac_gen = "__jac_gen__";
    py_cache = "__pycache__"
    for root,dirs, files in os.walk(current_directory, topdown=True){
        for folder_name in dirs[:]{
            if folder_name == target_dir or folder_name == py_cache{
                shutil.rmtree(os.path.join(root, folder_name));
                dirs.remove(folder_name);
            }
        }
    }   
}
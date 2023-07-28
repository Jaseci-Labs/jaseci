"""Implementations for the jac command line interface."""
import:py from os, path;

:a:load(filename: str) {
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
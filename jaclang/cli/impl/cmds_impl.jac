"""Implementations for the jac command line interface."""
import:py from os, path;

:a:load(filename: str) {
    if filename.endswith(".jac"){
        [base, mod] = path.split(filename);
        mod=mod[:-4];
        __jac_import__(target=mod, base_path=base);
    }
}
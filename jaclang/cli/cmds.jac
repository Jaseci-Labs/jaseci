"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such production Jac program.
"""
import:py from os, path;
import:jac from cli, command_registry as cmd_reg;

# include:jac impl.cmds_imp;

@cmd_reg.register
can load(filename: str) {
    if filename.endswith(".jac"){
        [base, mod] = path.split(filename);
        mod=mod[:-4];
        __jac_import__(target=mod, base_path=base);
    }
}

@cmd_reg.register
can build() {
    return f"Bar result: {a}, {b}, {c}";
}


"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such production Jac program.
"""
import:jac from cli, cmd_registry as cmd_reg;

include:jac cmds_impl;

@cmd_reg.register
can run(filename: str, main: bool = True);

@cmd_reg.register
can enter(filename: str, entrypoint: str, args: list);

@cmd_reg.register
can <>test(filename: str);

@cmd_reg.register
can ast_tool(tool: str, args: list = []);

@cmd_reg.register
can clean;

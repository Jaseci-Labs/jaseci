"""
This is the implementation of the command line interface tool for the
Jac languages. It's built with the Jac language V2 via bootstraping and
represents the first such production Jac program.
"""

import:py from argparse, ArgumentParser as ArgParser;

global version="0.0.1";

"""
Object representing a command line flag to be
attached to any command group.
"""
object CmdFlag {
    has flag: str, full_flag: str, help: str,
        typ: type, action: str, default: any;

    can init(full_flag: str, flag: str = None, help: str = "No Help Here!",
             typ: type = None, action: str = None, default: any = None) {
        :h:flag = flag ?: f"-{full_flag[2]}";
        :h:full_flag = full_flag;
        :h:help = help;
        :h:typ = typ;
        :h:action = action;
        :h:default = default;
    }
}

"""
Object representing a command line argument to be
attached to any command group.
"""
object CmdArg {
    has name: str, help: str, typ: type, default: any;

    can init(name: str, help: str = "No Help Here!", typ: type = None,
             default: any = None) {
        :h:name = name;
        :h:help = help;
        :h:typ = typ;
        :h:default = default;
    }
}

"""
Represents a higher level command, each command
can take one Argument and any number of flags.
"""
object Command {
    has name: str, description: str, flags: list[CmdFlag], arg: CmdArg;

    can init(name: str, description: str, flags: list[CmdFlag] = [],
             arg: CmdArg = None) {
        :h:name = name;
        :h:description = description;
        :h:flags = flags;
        :h:arg = arg;
    }

    can add_flag(flag: CmdFlag) {
        flag |> :h:flags.append;
    }

    can set_arg(arg: CmdArg) {
        :h:arg = arg;
    }
}

"""
The main CLI object, this is the entry point for the
CLI tool.
"""
object JacCli {
    has parser:ArgParser = ArgParser(prog="jac", description="Jac CLI Tool");

    can init() {
        :h:parser.add_argument("-v", "--version", action="version",
                               version=f"Jac CLI Tool {version}");
        |> :h:setup;
    }

    can setup() {
        run_cmd = Command(name="run", description="Run a Jac program");
        run_cmd.set_arg <| spawn CmdArg(name="file",
                           help="The Jac file to run",  typ=str);
        run_cmd.add_flag <| spawn CmdFlag(full_flag="--debug",
                            help="Run the program in debug mode",
                            action="store_true");

        build_cmd = Command(name="build", description="Build a Jac program");
        build_cmd.set_arg <| spawn CmdArg(name="file",
                             help="The Jac file to build",  typ=str);
        build_cmd.add_flag <| spawn CmdFlag(full_flag="--debug",
                              help="Build the program in debug mode",
                              action="store_true");
    }

    can cli() {
        args = :h:parser.parse_args;
        if args.run {
            {args.file, args.debug} |> :h:run;
        } elif args.build {
            {args.file, args.debug} |> :h:build;
        } else {
            |> :h:parser.print_help;
        }
    }
}

with entry {
    |> (:+: JacCli).cli;
}
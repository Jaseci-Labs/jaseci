# Red Pill: Concepts, Semantics, and Features for Realizing Data Spatial Programming

This section of the Jac language specification dives into the composition of how the data spatial programming model is achieved through Jac's four primary architypes: objects, nodes, edges, and walkers. These architypes represent various categories of the notion of a traditional class, each with its unique traits and functionalities.
### Main Components of an Architype in Jac

Across all architypes in Jac, there are three main types of fields: has variables, data spatial abilities, and method abilities.

#### Has Variables

Has variables stand for the variable fields of the architype. Unlike other elements of the Jac language, these fields are strongly typed, thereby requiring explicit type declaration. This ensures that each has variable adheres to a specific type, promoting a sense of robustness and predictability within the language, even while other areas of code allow for dynamic type inference.

#### Data Spatial Abilities

Data spatial abilities, on the other hand, are akin to methods in other languages but imbued with the distinct semantics of data spatial programming. These abilities do not operate on traditional parameter passing or value returning paradigms. Instead, all data access is facilitated exclusively through two references: `here` and `visitor`.

- The `here` reference allows access to the has fields of the node or object that a walker is currently visiting. This visitation-based data access highlights the unique traversal mechanics of Jac's data spatial model.

- The `visitor` reference only provides access to the has variables of the walker itself. It is through this constraint that data sharing between the visited node or object (`here`) and the walker (`visitor`) is permitted.

This spatial ability to access and manipulate data, unique to Jac, aligns with the spatial model of data programming, thus strengthening its differentiating edge.

#### Method Abilities

Method abilities are reminiscent of traditional class methods in other programming languages. They accept parameters and return values, providing a more conventional programming mechanism within Jac. However, just like has variables, these parameters and return types must also be explicitly defined. This requirement ensures type safety during method invocation, helping to prevent runtime errors.


### The Node Architype
### The Edge Architype
### The Walker Architype
### The Object Architype
### Computation via Traversing Graphs
### Data In-Situ Programming
### Report
### Yield
### Cross Invocation Persistence
### The Sentinel

### Notes

* Introduce root along with here and <visitor>, here is root for all non ds code points
## Real World Examples

### Jac's own command line tool written in Jac

```jac
"""
This is the implementation of the command line interface tool for the
Jac languages. It's built with the Jac language V2 via bootstraping and
represents the first such production Jac program.
"""
#* This is
A Multiline
Comment *#

# This is a single line comment

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
            :h:run(args.file, args.debug);
        } elif args.build {
            :h:build(args.file, args.debug);
        } else {
            :h:parser.print_help;
        }
    }
}

with entry {
    |> (:+: JacCli).cli;
}
```
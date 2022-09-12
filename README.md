[![jaseci_core Unit Tests](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_test.yml/badge.svg?branch=main&event=push)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_test.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci/)](https://pypi.org/project/jaseci)
[![jaseci_serv](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci-serv/)](https://pypi.org/project/jaseci-serv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Jaseci can be installed on a single machine or on a Kubernetes cluster.

## Introduction

The setup section is split into two parts: 
- a standalone local setup
- a cloud and kubernetes setup *(Coming Soon)*

### Setup (Local)

We've built a command line tool to help you effectively work with Jaseci from your terminal. This tool gives you complete control over jaseci and makes working with instances even better. Let's get started!

### Requirements

1. Python 3
2. pip3

### Installation (for Users of Jaseci and Jac coders)

1. Install Jaseci by running: `pip3 install jaseci`
2. Install Jaseci Server by running: `pip3 install jaseci-serv`
3. (for AI) Install Jaseci Kit by running: `pip3 install jaseci-ai-kit`

### Installation (for Contributors of Jaseci)

1. Install black: `pip3 install black`
2. Install pre-commit: `pip3 install pre-commit; pre-commit install`
3. Install Jaseci from main branch: `cd jaseci_core; source install.sh; cd -`
4. Install Jaseci Server from main branch: `cd jaseci_serv; source install.sh; cd -`
5. (for AI) Install Jaseci Kit from main branch: `cd jaseci_ai_kit; source install.sh; cd -`

Note: You'll have to add `--max-line-length=88 --extend-ignore=E203` args to flake8 for linting. If you use VSCode, you should update it there too. 

### Quickstart (Hello, World!)

In this section, we'll take a look at how easy it is to get started with a simple Hello World program in Jac.
*Ensure that jaseci is installed before proceeding with the quickstart guide.*

1.  Create a new directory for your project called `hello_jac`
2.  Create a file called `hello.jac` within the directory created in the previous step.
3.  Give `hello.jac` the following contents:

```jac
walker init {
    std.out("Hello, World!");
}
```

4.  Navigate to the `hello_jac` directory using your terminal.
5.  Run the program with the following command: `jsctl jac run hello.jac`
6.  This should print the following string to the console: `Hello World`

Let's get into the details. `walker` is the keyword used to define a **Walker**. `init` is a reserved word; in this case, it provides the entry point to the jac program. Therefore, once the compiler encounters `walker init {}` it starts the program execution. Line 2 contains the `std` library for standard operation and `out()` is a module for printing. Simply put, the command `std.out()` displays the string `Hello World` as an output in your terminal.

### Workflow

In the quickstart section, the `run` command was used to prompt the execution of the hello.jac program. We only recommend doing this for very small programs. Using the `run` command on larger programs may increase run time.

#### How the `run` command works

When you use the `run` command on a .jac file, the program is sent to Jaseci to be compiled (larger programs take longer to compile). After compilation, Jaseci then runs the program.

#### Using the `build` command

To ensure that our Jac programs runs fast, it's recommended that you build programs first using the `jac build` command and then run them.

To build the `hello.jac` program from the **Quickstart** section, run the following command:

`jsctl jac build hello.jac`

Running the above command will build the program and output a file called `hello.jir`. This is our compiled jac program.

You can then run the compiled hello.jac program with:

`jsctl jac run hello.jir`

You'll notice how fast it runs. Instantly!

### The Jaseci shell

You hate the idea of typing `jsctl` every time you want to do something... There is a shell for this. Let's learn more.

1. To access the shell, type `jsctl` in your terminal and hit Enter.

You'll get the following output:

```
Starting Jaseci Shell...
jaseci >
```

If you're still in the hello_jac directory, try building or running the hello.jac program, this time without typing `jsctl` in front of the commands:

run: `jac run hello.jac`

build: `jac build hello.jac`

#### Getting help

1.  To see a list of commands you can run with the jaseci shell, type `help` and press Enter. You'll see the following output:

```
jaseci > help

Documented commands (type help <topic>):
========================================
actions    clear   global  logger  master  sentinel  walker
alias      config  graph   login   object  stripe
architype  edit    jac     ls      reset   tool

Undocumented commands:
======================
exit  help  quit
```

To get help on a particular command, type: `help NAME_OF_COMMAND`

For example, to see all the commands for `jac`, type: `help jac`

You should see an output like:

```
Usage: jac [OPTIONS] COMMAND [ARGS]...

Group of `jac` commands

Options:
--help  Show this message and exit.

Commands:
build  Command line tooling for building executable jac ir
run    Command line tooling for running all test in both .jac code files...
test   Command line tooling for running all test in both .jac code files...
```

### Visualizing a graph

As you get to know Jaseci and Jac, you'll want to try things and tinker a bit. In this section, we'll get to know how jsctl can be used as the main platform for this play. A typical flow will involve jumping into shell-mode, writing some code, running that code to observe its output, visualizing the state of the graph, and rendering that graph in dot to see its visualization.

#### Installing Graphiz

Graphiz is a software package that comes with a tool called `dot`. Dot is a standardized and open graph description language that is a key primitive of Graphiz. The dot tool takes in dot code and renders it nicely.

##### Windows (WSL)

Run the following command to install `Graphiz` on Linux:

`sudo apt install graphiz`

##### MacOS

Run the following command to install `Graphiz` on MacOS:

`brew install graphiz`

That's it!

#### Using Graphiz

Now that we have Graphiz installed, let's use it.

1.  In the `hello_jac` directory that you created earlier, create a file called `fam.jac` and give it the following content:

```
node man;
node woman;

edge mom;
edge dad;
edge married;

walker create_fam {
    root {
        spawn here --> node::man;
        spawn here --> node::woman;
        --> node::man <-[married]-> --> node::woman;
        take -->;
    }
    woman {
        son = spawn here <-[mom]- node::man;
        son -[dad]-> <-[married]->;
    }
    man {
        std.out("I didn't do any of the hard work.");
    }
}
```

Don't worry if that looks confusing. As you learn the Jac language, this will become clearer.

2. Let's "register" a sentinel based on our Jac program. A sentinel is the abstraction Jaseci uses to encapsulate compiled walkers and architype nodes and edges. You can think of registering a sentinel as compiling your jac program. The walkers of a given sentinel can then be invoked and run on arbitrary nodes of any graph. Let's register `fam.jac`

3. Open the jaseci shell by typing `jsctl`
4. Run the following command to register a sentinel:
   `sentinel register -name fam -code fam.jac -set_active true`

You should see the following output:

```
jaseci > sentinel register -name fam -code fam.jac -set_active true
2022-03-21 13:56:29,443 - INFO - parse_jac: fam: Processing Jac code...
2022-03-21 13:56:29,558 - INFO - register: fam: Successfully registered code
[
{
    "version": null,
    "name": "fam",
    "kind": "generic",
    "jid": "urn:uuid:04385141-7d65-4467-bf51-d251bb9e5a84",
    "j_timestamp": "2022-03-21T17:56:29.443318",
    "j_type": "sentinel"
},
{
    "context": {},
    "anchor": null,
    "name": "root",
    "kind": "generic",
    "jid": "urn:uuid:9df56101-f831-4791-8326-ca6657b4b23c",
    "j_timestamp": "2022-03-21T17:56:29.443427",
    "j_type": "graph"
}
]
```

This output shows that the sentinel was created. Note that we've also made this the "active" sentinel that will be used as the default setting for any calls to the Jaseci Core APIs that require a sentinel be specified.

At this point, Jasei has registered our code and we are ready to run walkers!

4. Now let's run our walker on the root node of the graph we created and see what happens!

Run the following command:

`walker run -name create_fam`

You should see the following output:

```
walker run -name create_fam
I didn't do any of the hard work.
[]
```

But how do we visualize that the graph produced by the program is right? If you've guessed it, we can use the Jaseci dot feature to take a look at our graph!!

Run the following command:

`graph get -mode dot -o fam.dot`

You should see the following output:

```
jaseci > graph get -mode dot -o fam.dot
strict digraph root {
    "n0" [ id="9df56101f83147918326ca6657b4b23c", label="n0:root"  ]
    "n1" [ id="011d88ae58744e5a87ca27fd6875ce3e", label="n1:man"  ]
    "n2" [ id="2099b359f4024a94bc167dead2b8d15d", label="n2:woman"  ]
    "n3" [ id="efa326feadc94b2fad2399e787907885", label="n3:man"  ]
    "n0" -> "n1" [ id="10b075a1b3714ff986f9cbb37160f601", label="e0" ]
    "n1" -> "n2" [ id="a7bae4f6c8ae4a3496cd8f942bb40aa8", label="e1:married", dir="both" ]
    "n3" -> "n1" [ id="35a76964f7144e9aba04200368cdab29", label="e2:dad" ]
    "n3" -> "n2" [ id="285d4f89f6144b2ca208807d8471fa54", label="e3:mom" ]
    "n0" -> "n2" [ id="4caffc3f14884965b48d64a005d57427", label="e4" ]
}
[saved to fam.dot]
```

To see a pretty visual of the graph itself, we can use the dot command from Graphiz. Exit the shell by typing `exit` and then run the following command:

`dot -Tpdf fam.dot -o fam.pdf`

A new file called `fam.pdf` will now appear in the `hello_jac` directory. Open this file to see your graph!

## References

- Official Documentation: https://docs.jaseci.org/
- Jaseci Bible: https://github.com/Jaseci-Labs/jaseci_bible

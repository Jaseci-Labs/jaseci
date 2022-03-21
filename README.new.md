[![jaseci_core](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_build.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_build.yml)
[![jaseci_serv](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml)


Jaseci can be installed on a single machine or on a Kubernetes cluster.

## Introduction
The Setup section is split into two parts. The first of which contains information pertaining to a standalone local setup and the second contains setup instructions for cloud and kubernetes setup. 

### Setup (Local)

We've built a command line tool to help you effectively work with Jaseci from your terminal. This tool gives you complete control over jaseci and makes working with instances even better. Lets get started!

### Requirements
1. Python 3
2. pip3

### Installation
1. Install Jaseci by running: `pip3 install jaseci`

### Quickstart (Hello, World!)
In this section we'll take a look at how easy it is to get up and running with a simple Hello World program in Jac.
1. To get started created a new folder (on your desktop or anywhere else) called `hello_jac`
2. Inside that folder, create a file called `hello.jac`
3. Give `hello.jac` the following contents:  
   
        walker init {
            std.out("Hello, World!");
        }
4. Open a terminal in `hello_jac` folder.
5. Assuming that you have jaseci installed, run the program with the following command: `jsctl jac run hello.jac`
6. This should print to the console: `Hello World`

### Workflow
In the quickstart section, you saw that we instantly ran the code in hello.jac program. The `run` command runs a jac programs on the fly. We only recommend doing this for very small programs. Using the `run` command on larger programs may take sometime.

#### How the `run` command works
When you use the `run` command on a .jac file, the program is sent to Jaseci to be compiled (Larger programs takes a longer time to compile). After compilation completes, Jaseci then runs the program.

#### Using the `build` command
To ensure that our Jac programs runs fast enough its recommended that you build programs first using the `jac build` command and then run them.

To build the `hello.jac` program from the **Quickstart** section, run the following command:
`jsctl jac build hello.jac`

running the above command will build the program and output a file called `hello.jir`, and this is our compiled jac program.

you can then run the compiled hello.jac program by running:

`jsctl jac run hello.jir`

You'll notice how fast it runs, instantly!.

### The Jaseci shell
You hate the idea of typing jsctl everytime you want to do something... There is a shell for this. Lets learn more.

1. To acccess the shell type `jsctl` in your terminal and hit enter.

You'll get the following output:  

    Starting Jaseci Shell...  
    jaseci >

if you're still in the hello_jac folder/directory, try building or running the hello.jac program, this time without typing `jsctl` infront of the commands:

run:   `jac run hello.jac`

build: `jac build hello.jac`

#### Getting help
1. To see a list of commands you can run with the jaseci shell type `help` and press enter. You'll see the following output:

        jaseci > help

        Documented commands (type help <topic>):
        ========================================
        actions    clear   global  logger  master  sentinel  walker
        alias      config  graph   login   object  stripe  
        architype  edit    jac     ls      reset   tool    

        Undocumented commands:
        ======================
        exit  help  quit

To get help on a particular command type:

`help NAME_OF_COMMAND` 

for example to see all the commands for `jac` type:

`help jac` You should see an output like:

    Usage: jac [OPTIONS] COMMAND [ARGS]...

    Group of `jac` commands

    Options:
    --help  Show this message and exit.

    Commands:
    build  Command line tooling for building executable jac ir
    run    Command line tooling for running all test in both .jac code files...
    test   Command line tooling for running all test in both .jac code files...

### Visualizing a graph

## References
- Official Documentation: https://docs.jaseci.org/
- Jaseci Bible: https://github.com/Jaseci-Labs/jaseci_bible

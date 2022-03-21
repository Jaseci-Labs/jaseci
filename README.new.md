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
5. Assuming that you have jaseci installed, run the program with the following command: `jsctl jac run hello.jac `
6. This should print to the console: `Hello World`

### Workflow
In the quickstart section, you saw that we instantly ran the code in hello.jac program. The `run` command runs a jac programs on the fly. We only recommend doing this for very small programs. Using the `run` command on larger programs may take sometime.

#### How the `run` command works
When you use the `run` command on a .jac file, the program is sent to Jaseci to be compiled (Larger programs takes a longer time to compile). After compilation completes, Jaseci then runs the program.

#### Using the `build` command
To ensure that our Jac programs


### Getting help


## References
- Official Documentation: https://docs.jaseci.org/
- Jaseci Bible: https://github.com/Jaseci-Labs/jaseci_bible

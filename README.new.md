[![jaseci_core](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_build.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_build.yml)
[![jaseci_serv](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml)


Jaseci can be installed on a single machine or on a Kubernetes cluster.

## Introduction
The Setup section is split into two parts. The first of which contains information pertaining to a standalone local setup and the second contains setup instructions for both cloud and kubernetes setup. 

### Setup (Local)

We've built a command line tool to help you effectively work with Jaseci from your terminal. Lets get started!

### Requirements
1. Python 3
2. pip3
3. 

### Installation
1. Install Jaseci by running: `pip3 install jaseci`

### Quickstart (Hello, World!)
1. To get started created a folder (on your desktop or anywhere else) called `hello_jac`
2. Create a file called `hello.jac`
3. Give `hello.jac` the following contents:  
   
        walker init {
            std.out("Hello, World!");
        }
4. Open a terminal in hello_jac folder.
5. Run the program: `jsctl jac run hello.jac `
6. This should print to the console: `Hello World`

### Workflow
In the quickstart section, you saw that we instantly ran the hello jac program. This runs a jac programs on the fly. We only recommend 


### Getting help


## References
- Official Documentation: https://docs.jaseci.org/
- Jaseci Bible: https://github.com/Jaseci-Labs/jaseci_bible

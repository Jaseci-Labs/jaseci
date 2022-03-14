[![jaseci_core](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_build.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_build.yml)
[![jaseci_serv](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml)


## Setup

### Prerequisites
1. Python 3
2. Virtualenv
3. pip3
4. Docker Desktop with Kubernetes Enabled
5. OS - Windows (WSL) or Linux
6. Visual Studio Code (Recommeded) - https://code.visualstudio.com/

### Installations

1. Clone this repo
2. Create a virtual python environment: `virtualenv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install JSCTL (Jaseci Command line tool): `cd jaseci_core && source install.sh`
5.  Install the VSCode Extension for Jaseci (Only if using VSCode): `cd support/vscode_extension/ && source install.sh`

### Write some code (Hello, World!)
1. To get started created a folder in this repo called `hello_jac`
2. Create a file called `hello.jac`
3. Give `hello.jac` the following contents:  
   
        walker init {
            std.out("Hello, World!");
        }
4. Change directory to `hello_jac`: `cd hello_jac`
4. Start the jaseci shell: `jsctl`
5. Run the program: `jac run hello.jac`
6. This should print to the console: `Hello World`

## References
- Official Documentation: https://docs.jaseci.org/
- Jaseci Bible: https://github.com/Jaseci-Labs/jaseci_bible

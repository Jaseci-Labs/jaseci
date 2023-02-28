# JSCTL: The Jaseci Command Line Interface

JSCTL or jsctl is a command line tool that provides full access to Jaseci. This tool is installed alongside the installation of the Jaseci Core package and should be accessible from the command line from anywhere.  At this point we can issue a call to say jsctl --help for any working directory. This command line tool provides full access to the Jaseci core APIs via the command line, or a shell mode.

```
haxor@linux:~/jaseci# pip3 install ./jaseci_core
Processing ./jaseci_core
...
Successfully installed jaseci-0.1.0
haxor@linux:~/jaseci# jsctl --help
Usage: jsctl [OPTIONS] COMMAND [ARGS]...
The Jaseci Command Line Interface
Options:
-f, --filename TEXT Specify filename for session state.
-m, --mem-only Set true to not save file for session.
--help Show this message and exit.
Commands:
alias Group of `alias` commands
architype Group of `architype` commands
check Group of `check` commands
config Group of `config` commands
dev Internal dev operations
edit Edit a file
graph Group of `graph` commands
login Command to log into live Jaseci server
ls List relevant files
object Group of `object` commands
sentinel Group of `sentinel` commands
walker Group of `walker` commands
haxor@linux:~/jaseci#
```

**Python below shows the implementation of setup.py that is responsible for deploying the jsctl tool upon pip3 installation of Jaseci Core.**

```py
from setuptools import setup, find_packages

 setup(
    name="jaseci",
    version="0.1.0",
    packages=find_packages(include=["jaseci", "jaseci.*"]),
    install_requires=[
        "click>=7.1.0,<7.2.0",
        "click-shell>=2.0,<3.0",
        "numpy >= 1.21.0, < 1.22.0",
        "antlr4-python3-runtime>=4.9.0,<4.10.0",
        "requests",
        "flake8",
    ],
    package_data={
        "": ["*.ini"],
    },
    entry_points={"console_scripts": ["jsctl = jaseci.jsctl.jsctl:main"→ ]},
 )
```
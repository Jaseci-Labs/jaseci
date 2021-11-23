---
sidebar_position: 1
---

# Overview

JSCTL or `jsctl` is a command line tool that provides full access to **Jaseci**. This tool is installed alongside the installation of the **Jaseci** Core package and should be accessible from the command line from anywhere.

In this section, well walk through how to access it and use it.

## Setup

To get up and running with `jsctl`, you must be within the main repo folder in your terminal (You'll need to clone the repo, if you haven't already)

The `jsctl` command line tool is installed automatically when we install the Jaseci python package.

1. Run the following command to install the `Jaseci` python package:

```
pip3 install ./jaseci_core
```

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
  alias Group of ‘alias‘ commands
architype Group of ‘architype‘ commands
check Group of ‘check‘ commands
config Group of ‘config‘ commands
dev Internal dev operations
edit Edit a file
graph Group of ‘graph‘ commands
login Command to log into live Jaseci server
ls List relevant files
object Group of ‘object‘ commands
sentinel Group of ‘sentinel‘ commands
walker Group of ‘walker‘ commands
haxor@linux:~/jaseci#

```

At this point we can check if `jsctl` is ready by running the following command from any working directory:

```
jsctl --help
```




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

At this point we can check if `jsctl` is ready by running the following command from any working directory:

```
jsctl --help
```


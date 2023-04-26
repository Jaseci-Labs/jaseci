---
sidebar_position: 1
---

# Jaseci Installation Guide

Welcome to the Jaseci installation guide! We are excited that you have decided to explore the world of Jaseci, and we are here to assist you in the installation process.

Jaseci offers a range of packages that can enhance the production of bleeding edge AI, including the Jaseci NLP library, Jaseci Speech library, Jaseci Miscellaneous library, and JAC Vision. Additionally, the Jaseci VS Code Extension provides syntax highlighting and auto-complete features, while Jaseci Studio allows Jaseci hackers to develop programs and visualize the graph output seamlessly. Furthermore, Jaseci Studio includes features that enable you to test and develop JAC programs, which we will cover in later sections.

Let's get started with the installation process and unlock the full potential of Jaseci!

Jaseci is tested and supported on the following systems:
* Ubuntu 18.04 or later
* Windows WSL2
* macOS* (see note below for compatibility with Apple silicon)

## Windows setup

To run commands for Jaseci we need a terminal that accepts bash arguments. We recommend using the Ubuntu terminal that comes as the default with WSL.

**Step 1:**

Check if WSL is installed by running the following the Windows powershell terminal :

 ```python
 wsl -l -v
 ```
 This will return  the flavour of the distribution used for WSL. The version column will show the version of WSL.

**Step 2:**

If no version is specified open windows powershell in  adminstrator mode and install WSL by running :

```
wsl --install
```

**Step 3:**

Restart your Computer

**Step 4:**

Open the Ubuntu terminal. for more information on installation see [here.](https://docs.microsoft.com/en-us/windows/wsl/install)


## Install Jaseci in Debian or WSL2

**Step 1:**

Install Jaseci Dependencies

Jaseci requires the following dependencies:
* python3.10-dev
* g++
* build-essential
* pkg-config
* cmake

To install in Debian (or WSL2),

```bash
apt-get install python3.10-dev python3-pip git g++ build-essential pkg-config cmake
```

**Step 2:**

Install `pip` python paackage manager

```bash
# Upgrade pip to the latest
pip install --upgrade pip
```

**Step 3:**

Once all the dependencies are installed. Now to install Jaseci

```bash
pip install jaseci
```

**Step 4:**

To ensure our installation is working run :

```
jsctl
```

Once it shows a list of options and commands, you're installation is complete.

## Install Jaseci on MacOS


**Step 1:**

For macOS, install the following dependencies using one of macOS package manager such as [Homebrew](https://brew.sh/) and [MacPorts](https://www.macports.org/).
- python3.10-dev
- g++
- build-essential
- pkg-config
- cmake

**Step 2:**

Install Jaseci

```bash
pip install jaseci
```

**Step 3:**
To ensure our installation is working run :

```
jsctl
```

Once it shows a list of options and commands, you're installation is complete.

>
> **Note**
>
> For macOS, there is currently a [known compatibility issue](https://developer.apple.com/forums/thread/700906) between `tensorflow-text` and Apple custom ARM-based silicon (M1, M2, etc.). If you are on a Mac machine with an Apple chip, you can still use `jaseci` and `jaseci-serv` and majority of the AI modules come with Jaseci, with the exception of those depending on `tensorflow-text`, which includes `use_enc` and `use_qa` in the `jac-nlp` package.
>
> Alternatively, you can build `tensorflow-text` from source following solutions provided by the [community](https://github.com/Jaseci-Labs/jaseci.git).




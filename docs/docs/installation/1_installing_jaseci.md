# Jaseci Installation Guide

Jaseci is tested and supported on the following systems:
* Ubuntu 18.04 or later
* Windows WSL2
* macOS* (see note below for compatibility with Apple silicon)


- [Jaseci Installation Guide](#jaseci-installation-guide)
  - [Installation for Jaseci Users](#installation-for-jaseci-users)
    - [Windows Set up](#windows-set-up)
    - [Install Jaseci in Debian or WSL2](#install-jaseci-in-debian-or-wsl2)
    - [Install Jaseci on MacOS](#install-jaseci-on-macos)
  - [Installation for Jaseci Contributors](#installation-for-jaseci-contributors)
    - [Build from source](#build-from-source)
    - [Setting up your Code Editor](#setting-up-your-code-editor)
    - [Setting up Development Environment](#setting-up-development-environment)
  - [Running a Jaseci Container](#running-a-jaseci-container)


Welcome to the Jaseci installation guide! We are excited that you have decided to explore the world of Jaseci, and we are here to assist you in the installation process.

Jaseci offers a range of packages that can enhance the production of bleeding edge AI, including the Jaseci NLP library, Jaseci Speech library, Jaseci Miscellaneous library, and JAC Vision. Additionally, the Jaseci VS Code Extension provides syntax highlighting and auto-complete features, while Jaseci Studio allows Jaseci hackers to develop programs and visualize the graph output seamlessly. Furthermore, Jaseci Studio includes features that enable you to test and develop JAC programs, which we will cover in later sections.

If you prefer to use Graphviz to visualize your graph, Jaseci also provides an option to do so. In this guide, we will walk you through the installation of all these packages and the complete setup of your development environment.

Let's get started with the installation process and unlock the full potential of Jaseci!

## Installation for Jaseci Users

### Windows Set up

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


### Install Jaseci in Debian or WSL2

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

Once it shows a list of options and commands, you're installation is complete

### Install Jaseci on MacOS

**Step 1:**

For macOS, install the above dependencies using one of macOS package manager such as [Homebrew](https://brew.sh/) and [MacPorts](https://www.macports.org/). and install Jaseci and verify the installation as per the instructions in step 3 and step 4.

>
> **Note**
>
> For macOS, there is currently a [known compatibility issue](https://developer.apple.com/forums/thread/700906) between `tensorflow-text` and Apple custom ARM-based silicon (M1, M2, etc.). If you are on a Mac machine with an Apple chip, you can still use `jaseci` and `jaseci-serv` and majority of the AI modules come with Jaseci, with the exception of those depending on `tensorflow-text`, which includes `use_enc` and `use_qa` in the `jac-nlp` package.
>
> Alternatively, you can build `tensorflow-text` from source following solutions provided by the [community](https://github.com/Jaseci-Labs/jaseci.git).


## Installation for Jaseci Contributors

### Build from source

If you wish to use the development version of Jaseci, you can download the source code from Github and build from source.

**Step 1.**

Cloning the repository.

```
git clone https://github.com/Jaseci-Labs/jaseci.git
```

**Step 2.**

Installing from source.

```
cd jaseci/jaseci_core/ && source install_everything.sh
```


### Setting up your Code Editor

Visual Studio code is a popular IDE used by developers of all operating systems. This IDE comes with a Jac extension to aid in your coding Journey.

**Step 1.**

If you already have VS code installed move to step 3. Download Visual Studio code from their website [here](https://code.visualstudio.com/)

**Step 2.**

Once download is completed . Open and follow the installation instructions.

**Step 3.**

Once Installation is completed open VS code and install the JAC extension.

**Step 4.**

Go to View > Command Palette . Type Install and select extensions.

**Step 5.**

Search JAC and select it then install.


### Setting up Development Environment

If you'd like to make contribution to Jaseci Open Source, you should build from source. In addition, you should set up the following in your development environment to follow the Jaseci Open Source Code Standards.

**Step 1.**

Install black
```bash
pip install black
```

**Step 2.**

Install pre-commit
```bash
pip install pre-commit

# goto root directory of Jaseci

pre-commit install
```

You'll need to add `--max-line-length=88 --extend-ignore=E203` arguments to flake8 for linting. We recommend setting it up in your preferred code editor or IDE, e.g. VSCode.

## Running a Jaseci Container

The [Jaseci Docker images](https://hub.docker.com/r/jaseci/jaseci) are built with the dependencies and the Jaseci package installed.

A Docker container runs in a virtual environment.

```bash
docker pull jaseci/jaseci:latest # Download the latest Jaseci image
docker run -it jaseci/jaseci:latest /bin/bash # Start the container and launch an interactive terminal inside it
```
This will open up a terminal inside the running container.

We also provide several other [Docker images](https://hub.docker.com/u/jaseci/starred).
These images include the core jaseci installation as well as one of the jaseci AI kit package.
For example, [jaseci/jac-nlp](https://hub.docker.com/r/jaseci/jac-nlp) have all modules in `jac_nlp` installed.
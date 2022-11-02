## Installing Jaseci

Jaseci can be installed on a single machine or on a Kubernetes cluster.

The setup section is split into two parts:
- a standalone local setup
- a cloud and kubernetes setup *(Coming Soon)*

### Setup (Local)

We've built a command line tool to help you effectively work with Jaseci from your terminal. This tool gives you complete control over jaseci and makes working with instances even better. Let's get started!

### Requirements

1. Python 3
2. pip3

### Installation (for Users of Jaseci and Jac coders)

Generally, installing Jaseci requires the following commands:

1. Install Jaseci by running: `pip3 install jaseci`
2. Install Jaseci Server by running: `pip3 install jaseci-serv`
3. (for AI) Install Jaseci Kit by running: `pip3 install jaseci-ai-kit`

Here are step-by-step guides on getting Jaseci Installed on different platforms:

- [Installing on Windows](#installing-on-windows)
- [Installing on Mac](#installing-on-mac)
- [Installing on Linux](#installing-on-linux)

#### Installing on Windows

To run commands for Jaseci we need a terminal that accepts bash arguments. We recommend using the Ubuntu terminal that comes as the default with WSL.

1. Check if WSL is installed by running the following the Windows powershell terminal :

 ```python
 wsl -l -v
 ```
 This will return  the flavour of the distribution used for WSL. The version column will show the version of WSL.

2. If no version is specified open windows powershell in  adminstrator mode and install WSL by running :

```bash
  wsl --install
````

3. Restart your Computer

4.Open the Ubuntu terminal. for more information on installation see [here.](https://docs.microsoft.com/en-us/windows/wsl/install)

 Install Python and Pip packet Manager

5. Check version of Python and Pip by running :
```
python3 --version
pip3 --version
```
If these packages are installed they will return a version number. Move to step 7 if a version number is present.

6.Install Python3 and pip3 by running the following:
```
sudo apt update
sudo apt install python3-dev python3-pip
```
7.Once the Python and pip packages are installed. Now to install Jaseci and Jaseci Kit
```
pip install jaseci
```
```
pip install jaseci-ai-kit
```

8. To ensure our installation is working run :
```
jsctl
```
The Jsctl terminal will be activated. It will look like this :
```
>jsctl
```

#### Installing on Mac

Install Python and Pip packet Manager

1. Check the version of Python and Pip by running :
```
python3 --version
pip3 --version
```
If these packages are installed they will return a version number. Move to step 3 if a version number is present.

2. Install Python3 and pip3 by running the following:
```
brew update
brew install python
```
3. Once the Python and pip packages are installed. Now to install Jaseci and Jaseci Kit
```
pip install jaseci
```
```
pip install jaseci-ai-kit
```

4. To ensure our installation is working run :
```
jsctl
```
Once it shows a list of options and commands, you're installation is complete.

#### Installing on Linux

Install Python and Pip packet Manager

1. Check the version of Python and Pip by running :
```
python3 --version
pip3 --version
```
If these packages are installed they will return a version number. Move to step x if a version number is present.

2. Install Python3 and pip3 by running the following:
```
sudo apt update
sudo apt install python3-dev python3-pip
```
3. Once the Python and pip packages are installed. Now to install Jaseci and Jaseci Kit
```
pip install jaseci
```
```
pip install jaseci-kit
```

4. To ensure our installation is working run :
```
jsctl
```
Once it shows a list of options and commands, your installation is complete.


### Installation (for Contributors of Jaseci)

1. Install black: `pip3 install black`
2. Install pre-commit: `pip3 install pre-commit; pre-commit install`
3. Install Jaseci from main branch: `cd jaseci_core; source install.sh; cd -`
4. Install Jaseci Server from main branch: `cd jaseci_serv; source install.sh; cd -`
5. (for AI) Install Jaseci Kit from main branch: `cd jaseci_ai_kit; source install.sh; cd -`

Note: You'll have to add `--max-line-length=88 --extend-ignore=E203` args to flake8 for linting. If you use VSCode, you should update it there too.

# Install Jaseci
Jaseci is tested and supported on the following systems:
* python 3.10 or higher
* Ubuntu 18.04 or later
* Windows WSL2
* macOS* (see note below)

## Pre-requiste
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
> **Note**
>
> For macOS, install the above dependencies using one of macOS package manager such as [Homebrew](https://brew.sh/) and [MacPorts](https://www.macports.org/).

## Install via `pip`
Install Jaseci with Python's `pip` package manager
```bash
# Upgrade pip to the latest
pip install --upgrade pip

# Core Jaseci
pip install jaseci

# Jaseci server
pip install jaseci-serv
```
To check for succesfull installation, execute in terminal
```bash
jsctl info
```
The following output should show.
```bash
{
  "Version": "1.4.0.8",
  "Creator": "Jason Mars and friends",
  "URL": "https://jaseci.org"
}
```

### Additional Pacakges for AI Modules
`jaseci` and `jaseci-serv` packages provide the core of the Jaseci framework.
To build jaseci program with AI modules, you need to install additional pacakges.
```bash
# Jaseci AI modules for Natural Language Processing (NLP)
pip install jac_nlp[all]

# Jaseci AI modules for Speech
pip install jac_speech[all]

# Jaseci AI modules for Computer Vision
pip install jac_vision[all]

# Other Jaseci AI modules
pip install jac_misc[all]
```
You do not need to install all of the above packages or even everything in a specific `jac_*` package.
You can cherry-pick specific modules to install based on what is needed for your application.
Details on which module is included in each package and how to install selectively can be found [here](../../..//jaseci_ai_kit/README.md#Installation)

> **Note**
>
> For macOS, there is currently a [known compatibility issue](https://developer.apple.com/forums/thread/700906) between `tensorflow-text` and Apple custom ARM-based silicon (M1, M2, etc.). If you are on a Mac machine with an Apple chip, you can still use `jaseci` and `jaseci-serv` and majority of the AI modules come with Jaseci, with the exception of those depending on `tensorflow-text`, which includes `use_enc` and `use_qa` in the `jac-nlp` packages.
>
> Alternatively, you can build `tensorflow-text` from source following solutions provided by the [community](https://github.com/Jaseci-Labs/jaseci.git).

## Upgrade Versions
To upgrade installed version of Jaseci core packages to the latest version from Pypi
```bash
pip install --upgrade jaseci, jaseci_serv
```
Similarly, to upgrade the jaseci AI kit packages from Pypi
```bash
pip install --upgrade jac_nlp[all]
pip install --upgrade jac_speech[all]
pip install --upgrade jac_vision[all]
pip install --upgrade jac_misc[all]
```

To install specific version of Jaseci
```bash
pip install jaseci==1.4.0.0
```

## Build from Source
If you wish to use the development version of Jaseci, you can download the source code from Github and build from source.
```bash
git clone https://github.com/Jaseci-Labs/jaseci.git
cd jaseci/jaseci/ && source install.sh
cd jaseci/jaseci_serv && source install.sh
cd jaseci/jaseci_ai_kit && source install.sh all
```

## For Contributors
If you'd like to make contribution to Jaseci Open Source, you should build from source.
In addition, you should set up the following in your development environment to follow the Jaseci Open Source Code Standards.
```bash
# Install black
pip install black
# Install pre-commit
pip install pre-commit
pre-commit install
```
You'll need to add `--max-line-length=88 --extend-ignore=E203` arguments to `flake8` for linting.
We recommend setting it up in your preferred code editor or IDE, e.g. VSCode.

The Jaseci Open Source Contribution Guidelines can be found [here](../../../CONTRIBUTING.md).

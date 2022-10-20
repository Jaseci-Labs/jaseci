---
sidebar_position: 2
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Installation

<Tabs>
<TabItem value="windows" label="Windows" default>

## Windows Set up

### Software Requirements
- Ubuntu 20+
- python 2.8 +
- pip package manager

To run commands for Jaseci we need a terminal that accepts bash arguments. We recommend using the Ubuntu terminal that comes as the default with WSL.

1. Check if WSL is installed by running the following the Windows powershell terminal :

 ```python
 wsl -l -v
 ```
 This will return  the flavour of the distribution used for WSL. The version column will show the version of WSL.

2. If no version is specified open windows powershell in  adminstrator mode and install WSL by running :
    ```
    wsl --install
    ````

3. Restart your Computer

4.Open the Ubuntu terminal. for more information on installation see [here.](https://docs.microsoft.com/en-us/windows/wsl/install)

### Install Python and Pip packet Manager

5. Check version of Python and Pip by running :
```
python3 --version
pip3 --version
```
If these packages are installed they will return a version number. Move to step x if a version number is present.

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
Once it shows a list of options and commands, you're installation is complete
</TabItem>
<TabItem value="Macos" label="MACOS" default>

## Mac OS Set up

### Install Python and Pip packet Manager

5. Check the version of Python and Pip by running :
```
python3 --version
pip3 --version
```
If these packages are installed they will return a version number. Move to step x if a version number is present.

6.Install Python3 and pip3 by running the following:
```
brew update
brew install python
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
Once it shows a list of options and commands, you're installation is complete.
</TabItem>
<TabItem value="linux" label="Linux" default>

## Linux Installation



### Install Python and Pip packet Manager

5. Check the version of Python and Pip by running :
```
python3 --version
pip3 --version
```
If these packages are installed they will return a version number. Move to step x if a version number is present.

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
Once it shows a list of options and commands, your installation is complete.

</TabItem>

</Tabs>

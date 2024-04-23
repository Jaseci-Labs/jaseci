<div style="display: flex; justify-content: center; align-items: center;">
  <img src="https://www.jaseci.org/wp-content/uploads/2022/02/jaseki-logo-inverted-rgb.svg" alt="Jaseci" width="50%" />
</div>


[![jaseci_core Unit Tests](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-core-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-core-test.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci/)](https://pypi.org/project/jaseci)
[![jaseci_serv Tests](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-serv-test.yml/badge.svg)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-serv-test.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci-serv/)](https://pypi.org/project/jaseci-serv)
[![Jac NLP](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-nlp-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-nlp-test.yml)  [![PyPi version](https://badgen.net/pypi/v/jac_nlp/)](https://pypi.org/project/jac-nlp)
[![Jac Vision](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-vision-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-vision-test.yml)  [![PyPi version](https://badgen.net/pypi/v/jac_vision/)](https://pypi.org/project/jac-vision)
[![Jac Speech](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-speech-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-speech-test.yml)  [![PyPi version](https://badgen.net/pypi/v/jac_speech/)](https://pypi.org/project/jac-speech)
[![Jac Misc](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-misc-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-misc-test.yml)  [![PyPi version](https://badgen.net/pypi/v/jac_misc/)](https://pypi.org/project/jac-misc)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# [Maintenance] Jaseci: Build the Next Generation of AI Products at Scale

## Note to our community
We appreciate all the interests in Jaseci since its launch! We have been hard at work on developing the next evolution of Jaseci and the Jac Programming Language.

This next evolution embodies all the learnings from jaseci1.0 and represents the true form of data spatial programming and a modern programming language that serves the ever changing needs of developing production-grade AI applications.

Learn more:
* [jaclang (a.k.a jac2.0)](https://github.com/Jaseci-Labs/jaclang)
* [jaclang-jaseci](https://github.com/Jaseci-Labs/jaclang-jaseci)

This repo is now under maintenance mode, meaning moving forward there will be minimal features introduced. We will continue to resolve issues and push bugfixes as needed.

# The Jaseci Ecosystem

The [Jaseci](https://www.jaseci.org/) ecosystem, is an open-source technology stack composed of three components:
**Jaseci Core**, the fundamental execution engine,
**Jaseci Serv**, a cloud-scale runtime engine with diffuse capabilities,
and **Jaseci AI Kit**, a collection of state-of-the-art AI engines and pre-trained models contributed by the Jaseci team and the open source community. Additionally, **Jaseci Studio**, is a comprehensive IDE for programming and debugging Jaseci programs.

Jaseci presents a groundbreaking computational model that aims to simplify the process of developing AI applications. Through its exclusive data-spacial programming approach and diffuse execution environment, Jaseci has accomplished remarkable feats, such as decreasing development time by tenfold and almost completely removing standard backend code. Jaseci is invented by professors and researchers from the University of Michigan and has been open-source since 2021. Jaseci has been used by dozens of developers to create commercial products in various domains serving tens of thousands requests per day.

# Getting Started

To install Jaseci and all its packages, refer to the comprehensive Jaseci [Installation Guide](https://docs.jaseci.org/docs/docs/getting_started/installation).

For a quick start, install the `jaseci` python package via `pip`:

```bash
pip install jaseci
```

To set up a Jaseci server, please follow the steps outlined in the [Jaseci Server Setup guide](https://docs.jaseci.org/docs/docs/getting_started/setup_jaseci_serv).
To set up Jaseci Studio, please follow the instructions outlined in the [following guide](https://docs.jaseci.org/docs/docs/getting_started/setting_up_jaseci_studio).

A quick hello world example:
```jac
walker init{
  std.out("Hello World");
}
```

To run this example, save the code in a file named `main.jac` file and run with `jac run` command in `jsctl` shell;

```bash
jsctl
```
This will execute the Jaseci command line environment `jsctl`.

```bash
jaseci> jac run hello.jac
```

# Write Your First Jaseci Application
Follow these links to access more tutorials:

- [(Optional) VSCode Extension](https://docs.jaseci.org/docs/docs/getting_started/writing_first_app/setting_up_code_editor)
- [Building a Graph](https://docs.jaseci.org/docs/docs/getting_started/writing_first_app/building_graph)
- [Develop Walkers and Abilities](https://docs.jaseci.org/docs/docs/getting_started/writing_first_app/playing_with_walkers_and_abilities)

# Advanced Tutorials
  - [Building a Conversational AI](https://docs.jaseci.org/docs/category/build-a-conversational-ai-system-with-jaseci)
  - [Building a Text Analytics System](https://docs.jaseci.org/docs/category/text-analitics-with-jaseci)

# Resources
- [Documentation](https://docs.jaseci.org/)
- [Glossary](docs/docs/docs/glossary.md)
- [API Reference](https://api.jaseci.org/docs/)
- [Pypi Index](https://pypi.org/project/jaseci/)
- [Dockerhub Repository](https://hub.docker.com/u/jaseci)

# Community
- [Join our Discord!](https://discord.gg/zDYe3dKd)
- [StackOverflow](https://stackoverflow.com/questions/tagged/jaseci)
- [Contributing to Jaseci Open Source](CONTRIBUTING.md)
  - [How to be a Jaseci Contributor](CONTRIBUTING.md#how-to-be-a-jaseci-contributor)
  - [How to contribute code](CONTRIBUTING.md#how-to-contribute-code)
  - [How to Update the Official Documentation](CONTRIBUTING.md#how-to-update-the-official-documentation)
- [Contributors](CONTRIBUTORS.md)
---
sidebar_position: 0
title: Introduction
description: Introduction to Langchain and Langflow
---

## What is Langchain?

LangChain is a framework for developing applications powered by language models.

It enables applications that are:

- **Data-aware**: connect a language model to other sources of data
- **Agentic**: allow a language model to interact with its environment

The main value props of LangChain are:

- **Components**: abstractions for working with language models, along with a collection of implementations for each abstraction. Components are modular and easy-to-use, whether you are using the rest of the LangChain framework or not
- **Off-the-shelf chains**: a structured assembly of components for accomplishing specific higher-level tasks
Off-the-shelf chains make it easy to get started. For more complex applications and nuanced use-cases, components make it easy to customize existing chains or build new ones.

We have integrate langchain to jaseci as part of the jaseci ai kit's Jac Miscellaneous Package. You can install it by running:

```shell
pip install jac_misc[langchain]
```

The module comes with few off the shelf chains that you can use to build your own chatbot and also the ability to use langflow output JSON to build your own custom chains.

## What is Langflow?

Langflow is a UI for LangChain, designed with react-flow to provide an effortless way to experiment and prototype flows.

<img width="100%" src="https://github.com/logspace-ai/langflow/blob/main/img/langflow-demo.gif?raw=true"></img>

## 📦 Installation

### <b>Locally</b>

You can install Langflow from pip:

```shell
# This installs the package without dependencies for local models
pip install langflow
```

To use local models (e.g llama-cpp-python) run:

```shell
pip install langflow[local]
```

This will install the following dependencies:

- [CTransformers](https://github.com/marella/ctransformers)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [sentence-transformers](https://github.com/UKPLab/sentence-transformers)

You can still use models from projects like LocalAI

Next, run:

```shell
python -m langflow
```

or

```shell
langflow # or langflow --help
```

### HuggingFace Spaces

You can also check it out on [HuggingFace Spaces](https://huggingface.co/spaces/Logspace/Langflow) and run it in your browser! You can even clone it and have your own copy of Langflow to play with.

## Creating a Chatbot using Langchain and Langflow

In this tutorial, we will be creating a chatbot that can answer questions about the a given website. We will be using Langflow to create the flow and Langchain to create the chatbot.

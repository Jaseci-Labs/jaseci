---
sidebar_position: 1
title: Using Langflow to Create the Website Chatbot Flow
description: Using Langflow to Create the Website Chatbot Flow
---

# Using Langflow to Create the Website Chatbot Flow

If you haven't already installed Langflow, follow the instructions [here](#installation).

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

## Creating a Simple Chatbot

### Step 1
Go to your langflow platform and click `community examples`. Then click the  `Fork Example` button under the `Basic Chat` card. This will create a copy of the example in your own workspace. and forward you to the editor.

<img width="100%" src="https://i.ibb.co/zFV7Gk0/Screen-Recording-2023-08-02-at-18-02-33.gif"></img>

### Step 2
Create a `OpenAI API key` by visiting your [API Keys](https://platform.openai.com/account/api-keys) page in OpenAI website to retrieve the API key you'll use in your requests. Remember that your API key is a secret! Do not share it with others or expose it in any client-side code (browsers, apps). Then Paste it to the `OpenAI API key` field ChatOpenAI component.

<img width="100%" src="https://i.ibb.co/0VvvC0S/Screen-Recording-2023-08-02-at-18-13-12.gif"></img>
### Step 3
Then Click the `Lighting button` on the bottom right corner of the editor to compile the the flow. This will enable the `Chat button` on the bottom right corner of the editor. Click the `Chat button` to open the chat window. Now you have a working chatbot!

<img width="100%" src="https://i.ibb.co/K2QpVG3/Screen-Recording-2023-08-02-at-18-10-27.gif"></img>

## Creating a Website Chatbot

Similar to the previous example, we will create the following chain using the Langflow. Use the drag and drop interface to create the following flow.

<img width="100%" src="https://i.ibb.co/LhGp4Vv/Screenshot-2023-08-02-at-20-23-20.png"></img>

In the Above flow we have used `WebBaseLoader` to get the information from the website you have mentioned and `RecursiveCharacterTextSplitter` to split the text into sentences and we used the `OpenAIEmbedding` to convert the sentences into embeddings to store in the `Chroma` vector database. Then we used `VectorStoreAgent` to combine the Vector Database and the `ChatOpenAI` to create a chatbot.

Lets try it out!

<img width="100%" src="https://i.ibb.co/brr8FmM/Screen-Recording-2023-08-02-at-18-55-08.gif"></img>

> **Note**
> This is not a tutorial on how to use langchain. If you want to learn more about langchain, please visit the [Langchain Documentation](https://python.langchain.com/).

Click Export and you will end up with a JSON file. Makesure to tick the include secrets or you might need to do an additional step in the next section.
<img width="100%" src="https://i.ibb.co/cCLJwg4/Screen-Recording-2023-08-02-at-18-56-01.gif"></img>

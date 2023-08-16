---
sidebar_position: 2
title: Connecting Jaseci to the Langchain Flow
description: Connecting Jaseci to the Langchain Flow for the Website Chatbot
---

# Connecting Jaseci to the Langchain Flow
If you havent already installed Jaseci and langchain module follow the following instructions:

## Installation

Install Jaseci from pip:

```shell
pip install jaseci jaseci-serv
```
Follow the [Getting Started Guide](https://docs.jaseci.org/docs/category/getting-started) on setting up a jaseci server and running it with the help of JSCTL.

Install langchain module from pip:

```shell
pip install jac_misc[langchain] langflow # langflow is not required if you have ran it locally in the previous step
```
## Loading the Langchain Module and Testing it
Load the langchain module in the jaseci server by running the following command in the JSCTL shell:

```shell
jaseci> actions load module jac_misc.langchain
```
First lets step up the module with the JSON file we have downloaded now. You can do this by running the following command in the JSCTL shell:

```shell
jaseci> actions call langchain.setup -ctx '{"flow_type":"json", "json_file": <path-to-json-file>}'
```

Generate a random sentence by running the following command in the JSCTL shell:

```shell
jaseci> actions call langchain.generate -ctx '{"input": {"inputs":"What is Jaseci?"}}'
```

Output would be something like this:

```shell
> Entering new AgentExecutor chain...
I should use the Website tool to find information about Jaseci.
Action: Website
Action Input: Jaseci
Observation: Jaseci is an end-to-end open-source and Open Computational Model, Technology Stack, and Methodology for bleeding edge AI. It enables developers to rapidly build robust products with sophisticated AI capabilities at scale. Jaseci provides bleeding-edge AI models ready to use out of the box and eliminates the need for devops, simplifying and accelerating backend development.
Thought:I now know the final answer.
Final Answer: Jaseci is an end-to-end open-source and Open Computational Model, Technology Stack, and Methodology for bleeding edge AI. It enables developers to rapidly build robust products with sophisticated AI capabilities at scale. Jaseci provides bleeding-edge AI models ready to use out of the box and eliminates the need for devops, simplifying and accelerating backend development.

> Finished chain.
{
  "success": true,
  "result": {
    "input": "What is Jaseci?",
    "output": "Jaseci is an end-to-end open-source and Open Computational Model, Technology Stack, and Methodology for bleeding edge AI. It enables developers to rapidly build robust products with sophisticated AI capabilities at scale. Jaseci provides bleeding-edge AI models ready to use out of the box and eliminates the need for devops, simplifying and accelerating backend development."
  }
}
```

## Lets create the walkers we need for the website chatbot
We need only one walker for the website chatbot. You can start by creating a jac file (I will name it website_chatbot.jac) and adding the following code to it:

```python
# Path: website_chatbot.jac

walker ask_jaseci_bot {
    has input;
    can langchain.generate;
    report langchain.generate(input={"inputs":input});
}
```
Lets build the jac file and Sentinel register this walker by running the following command in the JSCTL shell:

```shell
jaseci> jac build website_chatbot.jac
jaseci> sentinel register website_chatbot.jir -mode jir -set_active true
```
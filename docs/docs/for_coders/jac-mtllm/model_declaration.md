# GenAI Models

<!-- - Remote model APIs
- Local model APIs
- Creating your own model interface -->

To incorporate a Large Language Model (LLM) into code, initialize it by importing from the ```mtllm.llms``` module built into the langauge.

To download jac-lang with all required python dependencies to use llms:
    ```bash
    pip install jaclang[llms]
    ```

Here are the list of models/ model providers which are available to use out of the box with jac-lang.

## Cloud Hosted LLMs (API Clients)

 - [OpenAI](https://openai.com/index/openai-api/)
 - [Anthropic (Claud models)](https://www.anthropic.com/)
 - [Groq](https://groq.com/)
 - [Together AI](https://www.together.ai/)

> Note:
>
> - Theses LLMs require an API Key and the relevent python libraries to be installed. -->

=== "OpenAI"
    ```bash
    pip install openai
    ```
=== "Anthropic"
    ```bash
    pip install anthropic
    ```
=== "Groq"
    ```bash
    pip install groq
    ```
=== "Together AI"
    ```bash
    pip install together
    ```

## Running Local LLMs

 - [Ollama](https://ollama.com/library)

    Downlad Ollama from their website, install and run the server by running ```ollama serve```. Pull and install your model of choice by bashing ```ollama run <model_name>``` on a new terminal.

 - [Hugging Face](https://huggingface.co/)

    Download and run opensource LLMs from the plethora of models available on the Hugging Face website.

> **Note:**
>
> - Running Local LLMs would be demanding for your PC setup where it will either simply not run the model or inference performance will take a hit. Check whether you have sufficient system requirements to run local LLMs.

In the jac program that you require to inference an LLM, please code as following template code snippets.

=== "OpenAI"
    ```jac linenums="1"
    import:py from mtllm.llms, OpenAI;

    glob llm = OpenAI(
                model_name = "gpt-4"
                );
    ```
=== "Anthropic"
    ```jac linenums="1"
    import:py from mtllm.llms, Anthropic;

    glob llm = Anthropic(
                model_name = "claude-3-sonnet-20240229"
                );
    ```
=== "Groq"
    ```jac linenums="1"
    import:py from mtllm.llms, Groq;

    glob llm = Groq(
                model_name = "llama3-8b-8192", # Go through available models in website
                );
    ```
=== "Together AI"
    ```jac linenums="1"
    import:py from mtllm.llms, TogetherAI;

    glob llm = TogetherAI(
                model_name = "meta-llama/Llama-2-70b-chat-hf" # Go through available models in website
                );
    ```
=== "Ollama"
    ```jac linenums="1"
    import:py from mtllm.llms, Ollama;

    glob llm = Ollama(
                model_name = "llama3:8b" # Will pull model if does not exists
                );
    ```
=== "Hugging Face"
    ```jac linenums="1"
    import:py from mtllm.llms, Huggingface;

    glob llm = Huggingface(
                model_name = "mistralai/Mistral-7B-v0.3" # Will pull model if does not exists
                );
    ```

The llm model is defined in these examples which can be intialized with specific attributes.

> **Note:**
>
> - If the coder wants to visualize the prompts during inference, enable verbose by adding ```verbose = True``` as an argument when defining the LLM.

This approach allows for the initialization of the desired model as a model code construct with a specific name (in this case, `llm`), facilitating its integration into code. -->
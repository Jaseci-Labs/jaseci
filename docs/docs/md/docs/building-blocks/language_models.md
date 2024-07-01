# Language Models

Language models is the most important building block of MTLLM. Without it we can't achieve neuro-symbolic programming.

Let's first make sure you can set up your language model. MTLLM support clients for many remote and local LMs. You can even create your own as well very easily if you want to.

## Setting up a LM client

In this section, we will go through the process of setting up a OpenAI's `GPT-4o` language model client. For that first makesure that you have installed the necessary dependancies by running `pip install mtllm[openai]`.

```python
import:py from mtllm.llms.openai, OpenAI;

my_llm = OpenAI(model_name="gpt-4o");
```

Makesure to set the `OPENAI_API_KEY` environment variable with your OpenAI API key.

## Directly calling the LM

You can directly call the LM by giving the raw prompts as well.

```python
my_llm("What is the capital of France?");
```

You can also pass the `max_tokens`, `temperature` and other parameters to the LM.

```python
my_llm("What is the capital of France?", max_tokens=10, temperature=0.5);
```

## Using the LM with MTLLM

Intented use of MTLLM's LMs is to use them with the `jaclang`'s `BY_LLM` Feature.

### With Abilities and Methods

```python
can function(arg1: str, arg2: str) -> str by llm();
```

### With Classes

```python
new_object = MyClass(arg1: str by llm());
```

### You can parse following attributes to the `by llm()` feature:

- `method` (default: `Normal`): Reasoning method to use. Can be `Normal`, `Reason` or `Chain-of-Thoughts`.
- `tools` (default: `None`): Tools to use. This is a list of abilities to use with ReAct Prompting method.
- `model specific parameters`: You can pass the model specific parameters as well. for example, `max_tokens`, `temperature` etc.

## Enabling Verbose Mode

You can enable the verbose mode to see the internal workings of the LM.

```python
import:py from mtllm.llms, OpenAI;

my_llm = OpenAI(model_name="gpt-4o", verbose=True);
```

## Remote LMs

These language models are provided as managed services. To access them, simply sign up and obtain an API key. Before calling any of the remote language models listed below, make sure to set the corresponding environment variable with your API key. Use Chat models for better performance.

```python
llm = mtllm.llms.{provider_listed_below}(model_name="your model", verbose=True/False);
```

1. `OpenAI` - OpenAI's gpt-3.5-turbo, gpt-4, gpt-4-turbo, gpt-4o [model zoo](https://platform.openai.com/docs/models)
2. `Anthropic` - Anthropic's Claude 3 & Claude 3.5 - Haiku ,Sonnet, Opus [model zoo](https://docs.anthropic.com/en/docs/about-claude/models)
3. `Groq` - Groq's Fast Inference Models [model zoo](https://console.groq.com/docs/models)
4. `Together` - Together's hosted OpenSource Models [model zoo](https://docs.together.ai/docs/inference-models)

## Local LMs

### Ollama

Initiate a ollama server by following this tutorial [here](https://github.com/ollama/ollama). Then you can use it as follows:

```python
import:py from mtllm.llms.ollama, Ollama;

llm = Ollama(host="ip:port of the ollama server", model_name="llama3", verbose=True/False);
```

### HuggingFace

You can use any of the HuggingFace's language models as well. [models](https://huggingface.co/models?pipeline_tag=text-generation)

```python
import:py from mtllm.llms.huggingface, HuggingFace;

llm = HuggingFace(model_name="microsoft/Phi-3-mini-4k-instruct", verbose=True/False);
```
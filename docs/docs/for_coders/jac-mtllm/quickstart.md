# Quick Start Guide

## Installation

To install MTLLM run,

```bash
pip install mtllm
```

By default, MTLLM will not install any llm integrations, to install the available integrations, include the extra(s) below:

=== "OpenAI"
    ```bash
    pip install mtllm[openai]
    ```
=== "Anthropic"
    ```bash
    pip install mtllm[anthropic]
    ```
=== "Together"
    ```bash
    pip install mtllm[together]
    ```
=== "Ollama"
    ```bash
    pip install mtllm[ollama]
    ```
=== "Huggingface"
    ```bash
    pip install mtllm[huggingface]
    ```
=== "Groq"
    ```bash
    pip install mtllm[groq]
    ```

MTLLM Supports MultiModal LLMs. To Support Images and Videos, you need to install the following extra(s):

=== "Image Support"
    ```bash
    pip install mtllm[image]
    ```
=== "Video Support"
    ```bash
    pip install mtllm[video]
    ```

Currently, only multimodal LLMs from OpenAI and Anthropic are supported. In the future, we plan to support multimodal LLMs from other providers as well.

## Minimal Working Example

Here we will walk you through a minimal working example of using MTLLM to generate translate a sentence from English to a target language.

### Setup

Before we start, make sure you have installed MTLLM & Jaclang.
Following code snippet will be our starting point:

```jac
can translate(eng_sentence: str, target_lang: str) -> str {
    """Normally this would include the translation logic such as calling an API.
    For the sake of this example, we will return a dummy translated sentence."""

    return "Hola Mundo";
}

with entry {
    print(translate("Hello World", "es"));
}
```

Assuming we went with API based translation, `target_lang` would be the language code of the target language. For example, `es` for Spanish, `fr` for French, etc. But Assume that you don't know the language code for the target language, or you would like to provide a context to `target_lang` instead of a language code. for example `Spanish` instead of `es` or `Language spoken in Somalia`. This is where you need the help of LLMs.

### Using MTLLM

#### Import the LLM You Want to Use

For this example, we will use OpenAI's GPT-3.5-turbo (default).

```jac
import from mtllm.llms, OpenAI;

llm = OpenAI();

# Rest of the code
```

#### Remove the Ability Body and Add `by LLM` keyword

```jac
import from mtllm.llms, OpenAI;

llm = OpenAI();

can translate(eng_sentence: str, target_lang: str) -> str by llm;

with entry {
    print(translate("Hello World", "Language spoken in Somalia"));
}
    ```

Thats it! 🎊

Now you can run the code and see the translated sentence by running the following command:
Makesure to export your OpenAI API key as an environment variable `OPENAI_API_KEY` before running the code.

```bash
jac run translator.jac
```

### Adding Additional Support to the LLMs

In this example, we dont need to add any additional support to the LLMs. But if you want to add additional support, you can do so by adding `SemStrings` to variables, output type hint and abilities the following code snippet:

```jac
import from mtllm.llms, OpenAI;

llm = OpenAI();

can 'Translate the given english sentence to the target language'
translate(eng_sentence: str, target_lang: str) -> 'Translation': str by llm;

with entry {
    print(translate("Hello World", "Language spoken in Somalia"));
}
```

You've successfully created a working example using the Jaclang and MTLLM.

Feel free to adapt and expand upon this example to suit your specific use case while exploring the extensive capabilities of MTLLM.

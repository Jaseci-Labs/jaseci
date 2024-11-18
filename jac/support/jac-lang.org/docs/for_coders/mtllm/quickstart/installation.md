# <span style="color: orange; font-weight: bold">MTLLM Documentation</span>

## <span style="color: orange">Installation</span>

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

Currently, only multimodal LLMs from OpenAI and Anthropic are supported. In the future, we plan to support multimodal LLMs from other providers as well
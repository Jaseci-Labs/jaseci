# **Langchain (`langchain`)**

Module `langchain` provides a set of actions to interact with OpenAI API with. You can use the actions to generate text,

## **1. Setup**
You have to set the OpenAI API key before using the module. You can get the API key from [here](https://platform.openai.com/account/api-keys). You can set the API key using the `setup` action or by setting the environment variable `OPENAI_API_KEY`.

### Setting the Environment Variable
if you are using one of the given langchain flows that prebuit into this module, you have to set the environment variable `OPENAI_API_KEY` using the following command. You can get the API key from [here](https://platform.openai.com/account/api-keys).
```bash
export OPENAI_API_KEY=<your-api-key>
```
Then you can load the module as usual as follows.
```bash
jaseci> actions load module jac_misc.langchain
```
### Using the `setup` Action to Initialize the Langchain Flow
If you have already loaded the module, you can use the `setup` action to set the langchain flow and also pass the required parameters.
Below example shows how to set the json langchain flow with the generated JSON file you got from the langflow platform.
Refer [Langchain Flows](https://python.langchain.com/en/latest/) for the available flows.
```bash
jaseci> actions call langchain.setup -ctx '{"flow_type":"json", "json_file": <path-to-json-file>}'
```
If you want to do the setup and load the module at the same time, you can parse the `ctx` as follows.
```bash
jaseci> action load module jac_misc.langchain -ctx '{"flow_type":"json", "json_file": <path-to-json-file>}'
```

#### Parameters:
- `flow_type`: str, optional (default="json")
    The type of the langchain flow to use. Available options are `json`, `qa-flow`, `document-chat-flow` more will be added soon.
- `uid`: str, optional (default='default')
    The unique identifier for the langchain flow. This is used to identify the flow when you are using multiple flows.

## **2. Generate**
This action is common for all the langchain flows. You can use the `generate` action to generate the desired output using the langchain flow you have set.
#### Parameters:

- `input`: dict
    The input to the langchain flow. for example if you are using the `qa-flow` flow, you have to pass the the following as the input.
    ```json
    {
        "query": "What is the capital of India?"
    }
    ```
- `flow`: str, optional (default="default")
    The name of the langchain flow to use for generating the output.

#### Example:
```jac
walker find_answer {
    has query;
    can langchain.generate;
    report langchain.generate(input={"query": query});
}
```

## Chains Available
### **`json`** - JSON Langchain Flow
This chain is used to load the langchain flow from a json file. You can get the json file from the langflow platform. Follow the following tutorial to get the json file. Use **[this link](https://jaseci-langflow.hf.space/)** to go to the langflow platform.

<iframe width="1280" height="665" src="https://www.youtube.com/embed/KJ-ux3hre4s?start=0?end=740" title="⛓️ LangFlow: Build Chatbots without Writing Code - LangChain" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

### **`qa-flow`** - Question Answering Flow
This chain is used to generate the answer for the given question using the giving context. You can use the `generate` action to generate the answer.

#### Setup Parameters:
- `text`: str
    The context for the question answering flow. This is the text that the model will use to answer the questions. You can provide a text file too.
- `prefix`: str, optional (default=DEFAULT_PREFIX)
    The prefix to use for the question. This is explains how the question should be answered. You can use the default prefix or you can use your own prefix. If you are using your own prefix, make sure to include the following in your prefix.
    ```python
    DEFAULT_PREFIX = "Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer."
    ```
- `openai_api_key`: str, optional (default=will use the OPENAI_API_KEY environment variable)
    The OpenAI API key to use for the question answering flow. You can get the API key from [here](https://platform.openai.com/account/api-keys).
- `chunk_size`: int, optional (default=1000)
    This is the number of characters to chunk the text into.
- `chunk_overlap`: int, optional (default=0)
    This is the number of characters to overlap the chunks.
- `embedding_kwargs`: dict, optional
    The keyword arguments to use for the embedding model. You can find the available keyword arguments [here](https://python.langchain.com/en/latest/reference/modules/embeddings.html#langchain.embeddings.OpenAIEmbeddings).
- `llm_kwargs`: dict, optional
    The keyword arguments to use for the language model. You can find the available keyword arguments [here](https://python.langchain.com/en/latest/reference/modules/llms.html#langchain.llms.OpenAI).

#### Example:
```bash
jaseci> actions call langchain.setup -ctx '{"flow_type":"qa-flow", "text": "The capital of India is New Delhi."}'
```

#### Input Format for `generate` Action:
```json
{"query": "What is the capital of India?"}
```
#### Output Format of `generate` Action:
```json
{"answer": "The capital of India is New Delhi."}
```

### **`document-chat-flow`** - Document Retrieval Chat Flow
This chain is used to generate the answer for the given question using the giving context but you can maintain a conversation with the model. You can use the `generate` action to generate the answer.

#### Setup Parameters:
- `text`: str
    The context for the question answering flow. This is the text that the model will use to answer the questions. You can provide a text file too.
- `openai_api_key`: str, optional (default=will use the OPENAI_API_KEY environment variable)
    The OpenAI API key to use for the question answering flow. You can get the API key from [here](https://platform.openai.com/account/api-keys).
- `chunk_size`: int, optional (default=1000)
    This is the number of characters to chunk the text into.
- `chunk_overlap`: int, optional (default=0)
    This is the number of characters to overlap the chunks.
- `embedding_kwargs`: dict, optional
    The keyword arguments to use for the embedding model. You can find the available keyword arguments [here](https://python.langchain.com/en/latest/reference/modules/embeddings.html#langchain.embeddings.OpenAIEmbeddings).
- `llm_kwargs`: dict, optional
    The keyword arguments to use for the language model. You can find the available keyword arguments [here](https://python.langchain.com/en/latest/reference/modules/llms.html#langchain.llms.OpenAI).

#### Example:
```bash
jaseci> actions call langchain.setup -ctx '{"flow_type":"document-chat-flow", "text": "The capital of India is New Delhi."}'
```

#### Input Format for `generate` Action:
```json
{"query": "What is the capital of India?", "chat_history"=[["Hello", "Hi"]]}
```
```bash
jaseci > actions call langchain.generate -ctx '{"input":{"query": "What is the capital of India?"}}'
```
#### Output Format of `generate` Action:
```json
{"answer": "New Delhi"}
```

## Examples
- [Document Retrieval Chatbot with Streamlit UI](https://github.com/Jaseci-Labs/jaseci/tree/feature/langchain/examples/langchain_example/chatbot)

## References
- [Jaseci Hosted LangFlow Platform](https://jaseci-langflow.hf.space/)
- [LangFlow Platform Tutorial](https://www.youtube.com/watch?v=KJ-ux3hre4s)
- [Langchain Documentation](https://python.langchain.com/en/latest/)

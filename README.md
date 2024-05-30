# MTLLM API library

[![PyPI version](https://img.shields.io/pypi/v/mtllm.svg)](https://pypi.org/project/mtllm/)

The MTLLM Python library provides convenient access to a large number of easy to use and customizable APIs to be used in Jaseci's [Jaclang](https://github.com/Jaseci-Labs/jaclang) by llm feature.
The Library provides automatic output fixing, output type validation, different prompting techniques, and more.

## Documentation

The documentation on how to use this library with Jaseci's Jaclang can be found [here]().

## Installation

> [!IMPORTANT]
> Though this is can be used with python projects, it is primarily intended to be used with Jaseci's Jaclang.

```sh
# install from PyPI
pip install mtllm
```

## Usage

The full API of this library can be found [here](docs/api.md).

### Using Different LLMs
```py
import:py from mtllm.llms, OpenAI;

glob llm = OpenAI();

can "Translate English to French"
translate(word: "English Word": str) -> "French Word": str by llm();
```

Based on your LLM of choice, make sure to set the `API Key` in the environment variable. For example, for OpenAI:

```sh
export OPENAI_API_KEY="your-api-key"
```
### Using Tools
```py
import:py from mtllm.llms, OpenAI;
import:py from mtllm.tools, wikipedia;

glob llm = OpenAI();

can "Answer History Questions"
history_qa(question: "History Question": str) -> "Detailed Answer": str by llm(tools=[wikipedia]);
```
## Supported LLMs and Tools
TBA

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
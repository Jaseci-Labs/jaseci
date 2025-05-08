# <span style="color: orange">Create Your Own Language Model

This guide will help you to bring your own language model to be used with MTLLM. This is helpful if you have a self-hosted Language Model or you are using a different service that is not currently supported by MTLLM.

> <span style="color: orange"> **IMPORTANT**
>
> This assumes that you have a proper understanding on how to inference with your language model. If you are not sure about this, please refer to the documentation of your language model.

## <span style="color: orange">Steps

- Create a new class that inherits from `BaseLLM` class.

In Python,
```python
from mtllm.llms.base import BaseLLM

class MyLLM(BaseLLM):
    def __init__(self, verbose: bool = False, max_tries: int = 10, **kwargs):
        self.verbose = verbose
        self.max_tries = max_tries
        # Your model initialization code here

    def __infer__(self, meaning_in: str | list[dict], **kwargs) -> str:
        # Your inference code here
        # If you are using a Multimodal (VLLM) model, use the list of dict -> openai format input with encoded images
        #  kwargs are the model specific parameters
        return 'Your response'
```

In Jaclang,
```jac
import from mtlm.llms.base, BaseLLM;

class MyLLM:BaseLLM: {
    can init(verbose:bool=false, max_tries:int=10, **kwargs: dict) -> None {
        self.verbose = verbose;
        self.max_tries = max_tries;
        # Your model initialization code here
    }

    can __infer__(meaning_in:str|list[dict], **kwargs: dict) -> str {
        # Your inference code here
        # If you are using a Multimodal (VLLM) model, use the list of dict -> openai format input with encoded images
        # kwargs are the model specific parameters
        return 'Your response';
    }
}
```

- Initialize your model with the required parameters.

```jac
import from my_llm, MyLLM; # For Jaclang
import from my_llm, MyLLM; # For Python

llm = MyLLM();
```

## <span style="color: orange">Changing the Prompting Techniques

You can change the prompting techniques overriding the the following parameters in your class.

```python
from mtllm.llms.base import BaseLLM

class MyLLM(BaseLLM):
    MTLLM_SYSTEM_PROMPT = 'Your System Prompt'
    MTLLM_PROMPT = 'Your Prompt' # Not Recommended to change this
    MTLLM_METHOD_PROMPTS = {
        "Normal": 'Your Normal Prompt',
        "Reason": 'Your Reason Prompt',
        "Chain-of-Thoughts": 'Your Chain-of-Thought Prompt',
        "ReAct": 'Your ReAct Prompt',
    }
    OUTPUT_FIX_PROMPT = 'Your Output Fix Prompt'
    OUTPUT_CHECK_PROMPT = 'Your Output Check Prompt'

    # Rest of the code
```

Thats it! You have successfully created your own Language Model to be used with MTLLM.

>  <span style="color: orange">**NOTICE**
>
> We are constantly adding new LMs to the library. If you want to add a new LM, please open an issue [here](https://github.com/Jaseci-Labs/mtllm/issues).
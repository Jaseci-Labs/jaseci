# Semstrings

The core idea behind MT-LLM is that if the program has been written in a readable manner, with type-safety, an LLM would be able to understand the task required to be performed using _meaning_ embedded within the code.

However, there are instanced where this is not the case for all instances. Hence, a new _meaning_ insertion code abstraction called "**semstrings**" has been introduced in MT-LLM.

## Where code is not meaningful enough!

Lets look into an instance where the existing code constructs are not sufficient to describe the meaning of the code for an LLM.

```python | apple.jac
import:py from mtllm.llms, OpenAI;

glob llm = OpenAI();

obj item


```


- Recap the core idea behind MTLLM.
- Show an example where existing code abstractions are not sufficient for embedding meaning in code.
- Introduce semstrings
- Show same example with semstrings
- Show possible semstring insertion points
- where not to use semstring
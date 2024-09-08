---
sidebar_position: 1
title: GPT2
description: Text Generation with GPT2
---

Module `gp2` uses the OpenAI's `GPT-2-medium` to perform text generation on a given text.

## Actions

The `generate` action allows you to generate text based on the input text you provide.

Inputs:
- text: input text, either a string or a list of strings
- max_length: maximum length of the generated text (default: 30)
- min_length: minimum length of the generated text (default: 10)
- num_return_sequences: number of sequences to return (default: 3)

Output: a list of generated text sequences

The `gtp2.get_embeddings` action allows you to get the embeddings for the input text.

Inputs:
- text: input text, either a string or a list of strings

Output: a list of embeddings for the input text

## Example Jac Usage:
Given a text or a list of texts, it will return the generated text.

```
walker test_generate {
    can gpt2.generate;
    report gpt2.generate(text= "Hello, my name is", num_return_sequences= 5);
}
```

Given a text or a list of texts, it will return the embeddings of the text.

```
walker test_get_embeddings {
    can gpt2.get_embeddings;
    report gpt2.get_embeddings(text= ["Hello, my name is GPT2", "GPT2 is an Text-to-Text Generation Model" ]);
}
```
For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/gpt2)


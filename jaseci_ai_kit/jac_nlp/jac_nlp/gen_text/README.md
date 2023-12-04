---
title: Text Generation
---

# **Text Generation (`gen_text`)**

Module `gen_text` uses various models to generate text based on the input prompt.

1. Import [`gen_text`](#1-import-gen_text-text-generation-module-in-jac) module in jac
2. [Text Generation](#2-text-generation)

# **Walkthrough**

## **1. Import `gen_text` Text Generation Module in jac**
1. To execute Jaseci, open a terminal and run the following command:
    ```
        jsctl -m
    ```
2. Load `gen_text` module in jac:
    ```
    actions load module jac_nlp.gen_text
    ```

## **2. Text Generation**
There are multiple ways to use the `gen_text` module to generate text:

1. Given a prompt, it will generate text.
2. Given a prompt and other optional parameters, it will generate text.

Following example will generate text based on a prompt:
```jac
walker test_generate_text {
 can gen_text.generate;
 report gen_text.generate("This is a test prompt.", 30, 10, 3);
}
```
## **3. Setup Parameters**

* `model` - Model to be used for text generation.
  Type: `str`
  Default: `gpt2`

# **References**

* [Text Generation](https://huggingface.co/transformers/model_doc/gpt2.html)
* [Text Generation Paper](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)


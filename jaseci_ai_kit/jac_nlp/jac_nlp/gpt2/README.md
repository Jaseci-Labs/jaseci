# **GPT2 (`gpt2`)**

Module `gp2` uses the OpenAI's `GPT-2-medium` to perform text genreation on a given text.
## **Actions**
### generate
The `generate` action allows you to generate text based on the input text you provide.

Inputs:
- text: input text, either a string or a list of strings
- max_length: maximum length of the generated text (default: 30)
- min_length: minimum length of the generated text (default: 10)
- num_return_sequences: number of sequences to return (default: 3)

Output: a list of generated text sequences

### get_embeddings
The `get_embeddings` action allows you to get the embeddings for the input text.

Inputs:
- text: input text, either a string or a list of strings

# **Walk through**

## **1. Import GPT2 (`gpt2`) module in jac**
1. For executing jaseci Open terminal and run follow command.
    ```
    jsctl -m
    ```
2.  Load gpt2 module in jac
    ```
    actions load module jac_nlp.gpt2
    ```

## **2. Generate**
Given a text or a list of texts, it will return the generated text.

walker test_generate {
    can gpt2.generate;
    report gpt2.generate(text= "Hello, my name is", num_return_sequences= 5);
}

## **3. Get Embeddings**
Given a text or a list of texts, it will return the embeddings of the text.

walker test_get_embeddings {
    can gpt2.get_embeddings;
    report gpt2.get_embeddings(text= ["Hello, my name is GPT2", "GPT2 is an Text-to-Text Generation Model" ]);
}

# **References**
- [GPT-2](https://openai.com/blog/better-language-models/)
- [HuggingFace](https://huggingface.co/transformers/model_doc/gpt2.html)
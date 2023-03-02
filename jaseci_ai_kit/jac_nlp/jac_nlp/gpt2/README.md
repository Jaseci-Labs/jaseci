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

Output: a list of embeddings

### train
The `train` action allows you to train the model on a given dataset.

Inputs:
- text: input text, either a string or a list of strings
- epochs: number of epochs to train the model (default: 1)
- use_prev_trained: whether to use the previously trained model weights (default: True)
- freeze: whether to freeze the model weights and only train the last layer (default: True)

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
```jac
walker test_generate {
    can gpt2.generate;
    report gpt2.generate(text= "Hello, my name is", num_return_sequences= 5);
}
```

## **3. Get Embeddings**
Given a text or a list of texts, it will return the embeddings of the text.

```jac
walker test_get_embeddings {
    can gpt2.get_embeddings;
    report gpt2.get_embeddings(text= ["Hello, my name is GPT2", "GPT2 is an Text-to-Text Generation Model" ]);
}
```

## **4. Train**
Given a text or a list of texts, it will train the model on the given dataset.

```jac
walker test_train {
    can gpt2.train;
    can file.load_str;
    text= file.load_str("jac_nlp/jac_nlp/gpt2/tests/german_recipes.txt");
    gpt2.train(text, 1);
}
```

# **References**
- [GPT-2](https://openai.com/blog/better-language-models/)
- [HuggingFace](https://huggingface.co/transformers/model_doc/gpt2.html)
# **OpenAI's GPT3 (`gpt3`)**

Module `gp3` uses the OpenAI's `GPT-3` api to perform text genreation on a given text.
## **Actions**
### generate
The `generate` action allows you to generate text based on the input text you provide.

Inputs:
- text: input text, string
- args: arguments to pass to the api (default: {
    "model": "text-davinci-003",
    "temperature": 0,
    "max_tokens": 100,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
})

Output: list of dictionaries, each dictionary contains the generated text and the score
```
[
    {
        "text": "This is some generated text.",
        "index": 0,
        "logprobs": null,
        "finish_reason": "stop"
    }
]
```

Refer to [OpenAI's GPT3 api](https://platform.openai.com/examples) for more details on the arguments.

# **Walk through**

## **1. Import GPT3 (`gpt3`) module in jac**
1. For executing jaseci Open terminal and run follow command.
    ```
    jsctl -m
    ```
2.  Load gpt2 module in jac
    ```
    actions load module jac_nlp.gpt3
    ```

## **2. Generate**
Given a text or a list of texts, it will return the generated text.
```jac
walker test_generate {
    can gpt3.generate;
    report gpt3.generate(text= "Hello, my name is", args= {
        "model": "text-davinci-003",
        "temperature": 0,
        "max_tokens": 100,
        "top_p": 1,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    });
}
```
# **References**
- [GPT-3](https://openai.com/blog/gpt-3-apps/)
- [GPT-3 API](https://beta.openai.com/docs/api-reference/introduction)
- [GPT-3 Examples](https://beta.openai.com/docs/api-reference/examples)
- [GPT-3 Documentation](https://beta.openai.com/docs/api-reference/introduction)
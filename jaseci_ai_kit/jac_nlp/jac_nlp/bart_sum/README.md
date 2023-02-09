# **Bart Summarizer (`bart_sum`)**

Module `bart_sum` uses the `bart-large-cnn` to get the abstractive summary of a text.

1. Import [`bart_sum`](#1-import-summarizer-bart_sum-module-in-jac) module in jac
2. [Summarizer](#2-summarizer)

# **Walk through**

## **1. Import Summarizer (`bart_sum`) module in jac**
1. For executing jaseci Open terminal and run follow command.
    ```
    jsctl -m
    ```
2.  Load bart_sum module in jac
    ```
    actions load module jac_nlp.bart_sum
    ```


## **2. Summarizer**
There are 2 ways to use `bart_sum` module.
1. Given a text, it will return the summary of the text.
2. Given a web page url, it will return the summary of the web page.

Both the methods uses a single action `summarize` to get the summary. Following are the parameters of the function.
* `text` - Text to be summarized. Type: `Union[List[str], str]` (Optional)
* `url` - Url of the web page to be summarized. Type: `str` (Optional)
* `max_length` - Maximum character length of the summary. Type: `int` Default: `100`
* `min_length` - Minimum character length of the summary. Type: `int` Default: `10`

Return type of the action is `List[str]`.

### **2.1. Given a text, it will return the summary of the text.**
Following example will return the summary of the a single text.

```jac
walker test_summarize_single {
    can bart_sum.summarize;
    report bart_sum.summarize("There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.", 10);
}
```
You can also pass a list of texts to get the summary of all the texts.
```jac
walker test_summarize_batch {
    can bart_sum.summarize;
    report bart_sum.summarize(
        ["There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.",
        "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.",
        "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude."],
        10
    );
}
```

### **2.2. Given a web page url, it will return the summary of the web page.**
Following example will return the summary of the web page.

```jac
walker test_summarize_url {
    can bart_sum.summarize;
    report bart_sum.summarize(null, "https://in.mashable.com/");
}
```

# **References**
* [Bart Summarizer](https://huggingface.co/transformers/model_doc/bart.html)
* [Bart Summarizer Paper](https://arxiv.org/abs/1910.13461)
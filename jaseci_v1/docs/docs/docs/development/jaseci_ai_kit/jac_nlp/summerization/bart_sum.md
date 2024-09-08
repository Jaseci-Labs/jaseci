---
sidebar_position: 3
title: BART Summarizer
description: Text Summerization with BART Summerizer
---

# Bart Summarization (`bart_sum`)

`bart_sum` uses the BART transformer model to perform abstractive summary on a body of text.

## Actions

There are 2 ways to use `bart_sum` module.
1. Given a text, it will return the summary of the text.
2. Given a web page url, it will return the summary of the web page.

Both the methods uses a single action `summarize` to get the summary. Following are the parameters of the function.
* `text` - Text to be summarized. Type: `Union[List[str], str]` (Optional)
* `url` - Url of the web page to be summarized. Type: `str` (Optional)
* `max_length` - Maximum character length of the summary. Type: `int` Default: `100`
* `min_length` - Minimum character length of the summary. Type: `int` Default: `10`

Return type of the action is `List[str]`.

## Example Jac Usage:

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
Following example will return the summary of the web page.

```jac
walker test_summarize_url {
    can bart_sum.summarize;
    report bart_sum.summarize(null, "https://in.mashable.com/");
}
```

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/bart_sum)

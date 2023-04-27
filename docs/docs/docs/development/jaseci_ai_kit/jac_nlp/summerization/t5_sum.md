---
sidebar_position: 2
title: T5 Summarizer
description: Text Summarization with T5 Summarizer
---

#  T5 Summarizer (`t5_sum`)

`t5_sum` uses the T5 transformer model to perform abstractive summary on a body of text.

#### Actions

* `classify_text`: use the T5 model to summarize a body of text
    * **Input**:
        * `text` (string): text to summarize
        * `min_length` (integer): the least amount of words you want returned from the model
        * `max_length` (integer): the most amount of words you want returned from the model
    * **Input datafile**
    `**data.json**`
        ```
        {
            "text": "The US has passed the peak on new coronavirus cases, President Donald Trump said and predicted that some states would reopen this month. The US has over 637,000 confirmed Covid-19 cases and over 30,826 deaths, the highest for any country in the world. At the daily White House coronavirus briefing on Wednesday, Trump said new guidelines to reopen the country would be announced on Thursday after he speaks to governors. We'll be the comeback kids, all of us, he said. We want to get our country back. The Trump administration has  previously fixed May 1 as a possible date to reopen the world's largest economy, but the president said some states may be able to return to normalcy earlier than that.",
            "min_length": 30,
            "max_length": 100
        }
        ```

#### Example Jac Usage:
```jac
# Use the T5 model to summarize a given piece of text
walker summarization {
    can t5_sum.classify_text;
    has data = "data.json";
    data = file.load_json(data);
    summarized_text = t5_sum.classify_text(
        text = data["text"],
        min_length = data["min_length"],
        max_length = data["max_length"]
        );
    report summarized_text;
}
```

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/t5_sum)
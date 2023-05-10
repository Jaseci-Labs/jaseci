---
sidebar_position: 1
title: CL Summarizer
description: Text Summarization with CL Summarizer
---

# CL Summarizer (`cl_summer`)

`cl_summer` uses the sumy summarizer to create extractive summary.

#### Actions

* `summarize`: to get the extractive summary in provided sentences count.
    * Input
        * `text`(String): text the contain the entire context
        * `url`(String): the link to the webpage
        * `sent_count`(int): number of sentence you want in the summary
        * `summarizer_type`(String): name of the summarizer type, available options are:
            * `LsaSummarizer`
            * `LexRankSummarizer`
            * `LuhnSummarizer`
    * Returns: List of Sentences that best summarizes the context

  * **Input text file `summarize.json`**
        ```
        {
            "text": "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and   rude. The King of England was at war with him and had led a great army into Scotland to drive him out of the land. Battle after battle had been fought. Six times Bruce had led his brave little army against his foes and six times his men had been beaten and driven into flight. At last his army was scattered, and he was forced to hide in the woods and in lonely places among the mountains. One rainy day, Bruce lay on the ground under a crude shed listening to the patter of the drops on the roof above him. He was tired and unhappy. He was ready to give up all hope. It seemed to him that there was no use for him to try to do anything more. As he lay thinking, he saw a spider over his head making ready to weave her web. He watched her as she toiled slowly and with great care. Six times she tried to throw her frail thread from one beam to another, and six times it fell short. 'Poor thing,' said Bruce: 'you, too, know what it is to fail.', But the spider did not lose hope with the sixth failure. With still more care, she made ready to try for the seventh time. Bruce almost forgot his own troubles as, he watched her swing herself out upon the slender line. Would she fail again? No! The thread was carried safely to the beam and fastened there."
        }
        ```
#### Example Jac Usage
```jac
# Use the summarizer to summarize a given text blob
walker cl_summer_example {
    has text_file = "summarize.json";
    has sent_count = 5;
    has summarizer_type = "LsaSummarizer";
    can cl_summer.summarize;

    # Getting Extractive summary from text
    train_data = file.load_json(text_file);
    resp_data = cl_summer.summarize(
        text=train_data.text,
        url="none",
        sent_count=sent_count,
        summarizer_type=summarizer_type
    );
    report resp_data;
}
```
```jac
# Use the summarizer to summarize a given URL
walker cl_summer_example {
    has sent_count = 5;
    has summarizer_type = "LsaSummarizer";
    has url="https://in.mashable.com/";
    can cl_summer.summarize;

    # Getting Extractive summary from URL
    resp_data_url = cl_summer.summarize(
        text="none",
        url=url,
        sent_count=sent_count,
        summarizer_type=summarizer_type
    );
    report resp_data_url;
}
```

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/cl_summer)
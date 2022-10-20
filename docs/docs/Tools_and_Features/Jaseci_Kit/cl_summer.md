
# Summarizer 
`cl_summer` uses the sumy summarizer to create extractive summary.

To load the Summarizer run :

```
actions load module jaseci_ai_kit.cl_summer
```

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
#### Example Jac Usage:
```jac
# Use the summarizer to summarize a given text blob or from a URL
walker cl_summer_example {
    has text_file = "summarize.json";
    has sent_count = 5;
    has summarizer_type = "LsaSummarizer";
    has url="https://in.mashable.com/";
    can cl_summer.summarize;

    # Getting Extractive summary from text
    train_data = file.load_json(text_file);
    resp_data = cl_summer.summarize(
        text=train_data.text,
        url="none",
        sent_count=sent_count,
        summarizer_type=summarizer_type
    );

    # Getting Extractive summary from URL
    resp_data_url = cl_summer.summarize(
        text="none",
        url=url,
        sent_count=sent_count,
        summarizer_type=summarizer_type
    );
}
```
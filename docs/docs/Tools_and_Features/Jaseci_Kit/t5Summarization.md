# T5 Summarization
`t5_sum` uses the T5 transformer model to perform abstractive summary on a body of text.

To load the T5 Summarizer run :

```
actions load module jaseci_ai_kit.t5_sum
```

* `classify_text`: use the T5 model to summarize a body of text
    * Input:
        * `text` (string): text to summarize
        * `min_length` (integer): the least amount of words you want returned from the model
        * `max_length` (integer): the most amount of words you want returned from the model

#### Example Jac Usage:
```jac
# Use the T5 model to summarize a given piece of text
walker summarization {
    can t5_sum.classify_text;
    
    has text;
    has min_length = 30;
    has max_length = 100;
    
    summarized_text = t5_sum.classify_text(text=text, min_length=min_length, max_length=max_length);
    
    report summarized_text;
}
```
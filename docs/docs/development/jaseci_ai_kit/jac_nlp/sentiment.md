---
sidebar_position: 7
title: Sentiment Analysis Model
---

# Sentiment Analysis Model (`sentiment`)

## Actions

Module `sentiment` implemented for analysing the sentiment in a given list of text. This module accepts as input a set of sentences.

- `texts` - (list of strings) list of input text documents.

## Example Jac Usage:

```jac
walker test_predict{
    can sentiment.predict;

    has texts = ["I love you", "I hate you"];

    report sentiment.predict(texts);
}
```

For a complete example visit [here](https://github.com/Jaseci-Labs/jaseci/tree/main/jaseci_ai_kit/jac_nlp/jac_nlp/sentiment)

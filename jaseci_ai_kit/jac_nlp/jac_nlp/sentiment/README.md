# Sentiment Analysis Model (sentiment)

Sentiment analysis is a technique used in natural language processing and machine learning to automatically identify and extract subjective information from text, such as opinions, emotions, and attitudes. It involves analyzing large volumes of text data to determine whether the overall sentiment expressed is positive, negative, or neutral.

Sentiment analysis is useful in a variety of applications, such as social media monitoring, customer feedback analysis, market research, and political analysis. It can help businesses and organizations understand how their customers or stakeholders feel about their products or services, and can provide insights into trends and patterns in public opinion.

There are different approaches to sentiment analysis, ranging from rule-based methods to machine learning-based methods. Rule-based methods use predefined rules and lexicons to identify sentiment, while machine learning-based methods train models on labeled data to predict sentiment.

Despite its potential benefits, sentiment analysis is not always accurate, as it can be influenced by factors such as sarcasm, irony, and cultural differences. Therefore, it is important to carefully evaluate the results and incorporate human judgment in the analysis process.

Module `sentiment` implemented for analysing the sentiment in a given list of text. This module accepts as input a set of sentences. This is an example program using Jaseci `sentiment` module.

# **Walk through**

## **1. Import text cluster (`sentiment`) module in jac**
1. For executing jaseci open terminal and run following command.
    ```
    jsctl -m
    ```
2.  Load `sentiment` module in jac shell session
    ```
    actions load module jac_nlp.sentiment
    ```

## **2. Predict sentiment of given list of texts**


Use `sentiment.predict` action to predict the sentiment for the given list of texts.

- `texts` - (list of strings) list of input text documents.

```jac
walker test_predict{
    can sentiment.predict;

    has texts = ["I love you", "I hate you"];

    report sentiment.predict(texts);
}
```

Expected output:

```
{
  "success": true,
  "report": [
    [
      {
        "label": "POS",
        "score": 0.9916695356369019
      },
      {
        "label": "NEG",
        "score": 0.9806600213050842
      }
    ]
  ],
  "final_node": "urn:uuid:cb853eb8-cb7d-45be-ace3-71d65d300f79",
  "yielded": false
}
```


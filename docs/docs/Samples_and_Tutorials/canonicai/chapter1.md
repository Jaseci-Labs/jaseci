---
title: Chapter 1
---

### What are we building?
We are building a Conversational AI.

### What is a Conversational AI agent?
Conversational AI is a type of artificial intelligence that enables consumers to interact with computer applications the way they would with other humans.

### Real world examples of conversational AI
* Amazon Alexa (Voice) 

![Amazon Alexa (Voice) ](https://imageio.forbes.com/specials-images/imageserve/6022e0a7644b9ab003f0dcb7/iPhone-screenshots-of-the-Alexa-app-s-new-Light-and-Dark-modes/960x0.jpg?format=jpg&width=700)

* Example of a text-based chatbot ( Website )

![Example of a text-based chatbot](https://cdn2.hubspot.net/hubfs/4056626/BotHomePage.png)

## What AI models  will be used

### Intent Classification

Intent classification (Text classification) is the process of assigning tags or categories to text according to its content. It's one of the fundamental tasks in Natural Language Processing (NLP) with broad applications such as sentiment analysis, topic labeling, spam detection, and intent detection.

**A (simple) diagram illustrating the input and output of Intent Classification**
![Alt text](/img/tutorial/images/intent_classification.png?raw=true "Title")

**A new version of the diagram with the real example**
![Alt text](/img/tutorial/images/intent_classification_example.png?raw=true "Title")

**Real example**
![Real Example For Intent Classification](/img/tutorial/images/real_example_ic.png "Title")

### Entity extraction

Entity extraction is a text analysis technique that uses Natural Language Processing (NLP) to automatically pull out specific data from unstructured text, and classifies it according to predefined categories. Entity extraction, also known as named entity extraction (NER), enables machines to automatically identify or extract entities, like product name, event, and location. It’s used by search engines to understand queries, chatbots to interact with humans, and teams to automate tedious tasks like data entry.

#### A (simple) diagram illustrating the input and output of Entity extraction
![Alt text](/img/tutorial/images/entity_extraction.png?raw=true "Title")

#### A new version of the diagram with the real example
![Alt text](/img/tutorial/images/entity_extraction_example.png?raw=true "Title")

**Real example**
![Real Example For Entity extraction](/img/tutorial/images/real_example_er.png "Title")

### Sentence Encoding

The Sentence Encoder encodes text into high dimensional vectors that can be used for text classification, semantic similarity, clustering, and other natural language tasks. The sentence embeddings can then be trivially used to compute sentence-level meaning similarity as well as to enable better performance on downstream classification tasks using less supervised training data.

**A (simple) diagram illustrating the input and output of Sentence Encoding**
![Sentence Encoding Example](/img/tutorial/images/sentence_encoding.png?raw=true "Title")

**A new version of the diagram with the real example**
![Sentence Encoding Example](/img/tutorial/images/sentence_encoding_example.png?raw=true "Title")

#### Real example
![Real Example For Sentence Encoder](/img/tutorial/images/real_example_se.png "Title")

**The AI models we will use in this tutorial**

| Name                  | AI Model                                        | Links                                                                                            |
| --------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Intent classification | biencoder                                       | [link](https://arxiv.org/abs/2103.06523)                                                         |
| Entity extraction     | Transformer-based token classification          | [link](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) |
| Sentence encoding     | Universal Sentence Encoder (USE_ENC and USE_QA) | [link](https://arxiv.org/abs/1803.11175)                                                         |
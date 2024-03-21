---
sidebar_position: 1
title: Introduction
description: An Overview of Jaseci AI Kit.
---

# Jaseci AI Kit

Jaseci AI Kit is a collection of state-of-the-art machine learning models from different domains (NLP, Computer Vision, Speech etc.) that are readily available to load into jaseci. Jaseci AI Kit consist of 4 Main Python Packages

## Jac NLP Modules

The `jac_nlp` package contains a collection of state-of-the-art NLP models that can be used to perform various nlp tasks such as named entity recognition, text summarization, embedding generation, topic extraction etc. following is a list of all the models available in the `jac_nlp` package.

### Available Modules in Jac NLP

#### Text Encoders

Text encoders are a type of encoder used in natural language processing (NLP) that transform raw text into a numerical representation that can be used by machine learning algorithms. Text encoders are designed to capture the semantic and syntactic information of the input text and convert it into a vectorized format that is suitable for further processing. Text encoders are essential components in many NLP applications such as language translation, sentiment analysis, and text classification.

Jaseci provides a selection of pre-built text encoders that are available for use without any training.


| Module      | Model Description | Docs                                       | Type                    | Status | Description                                                 | Resources                                 |
| ----------- | ----------------- | ------------------------------------------ | ----------------------- | ------ | ----------------------------------------------------------- | ----------------------------------------- |
| `use_enc`   | USE Encoder       | [Link](jac_nlp/text_encoders/use_enc.md)   | Zero-shot               | Ready  | Sentence-level embedding pre-trained on general text corpus | [Paper](https://arxiv.org/abs/1803.11175) |
| `use_qa`    | USE QA            | [Link](jac_nlp/text_encoders/use_qa.md)    | Zero-shot               | Ready  | Sentence-level embedding pre-trained on Q&A data corpus     | [Paper](https://arxiv.org/abs/1803.11175) |
| `fast_enc`  | FastText          |   | Training req.           | Deprecated  | FastText Text Classifier                                    | [Paper](https://arxiv.org/abs/1712.09405) |
| `bi_enc`    | Bi-Encoder        | [Link](jac_nlp/text_encoders/bi_enc.md)    | Training req./Zero-shot | Ready  | Dual sentence-level encoders                                | [Paper](https://arxiv.org/abs/1803.11175) |
| `sbert_sim` | SBert Similarity  | [Link](jac_nlp/text_encoders/sbert_sim.md) | Training req./Zero-shot | Ready  | SBert Encoders for Sentence Similarity                      | [Paper](https://arxiv.org/abs/1908.10084) |

#### Named Entity Recognition Models

Named Entity Recognition (NER) is a subtask of natural language processing (NLP) that involves identifying and classifying named entities in unstructured text. Named entities are words or phrases that refer to specific people, places, organizations, products, and other entities. The goal of NER is to identify and classify these entities into predefined categories such as person, location, organization, date, time, and others. NER is a crucial step in many NLP applications such as information retrieval, sentiment analysis, and question answering systems. NER can be achieved using various machine learning approaches such as rule-based systems, statistical models, and deep learning models. Deep learning models such as recurrent neural networks (RNNs) and transformers have achieved state-of-the-art performance in NER tasks.

Jaseci offers pre-built NER models that can be utilized immediately without any need for training.

| Module                | Model Description | Docs                           | Type          | Status | Description                                                     | Resources                                                                                               |
| --------------------- | ----------------- | ------------------------------ | ------------- | ------ | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `tfm_ner`             | Transformer NER   | [Link](jac_nlp/ner/tfm_ner.md) | Training req. | Ready  | Token classification on Transformer models, can be used for NER | [Huggingface](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) |
| `ent_ext`/ `lstm_ner` | Flair NER         |  | Training req. | Deprecated  | Entity extraction using the FLAIR NER framework                 |

#### Text Segmentation Modules

Text segmentation refers to the process of dividing a large chunk of text into smaller, meaningful segments. This can be useful for a variety of natural language processing tasks, such as sentiment analysis, topic modeling, and text summarization. Text segmentation can be performed using various techniques, including rule-based approaches, statistical models, and machine learning algorithms. The goal is to break down the text into meaningful units that can be analyzed and processed more effectively.

Jaseci offers a pre-built Text Segmentation model that can be utilized immediately without any need for training.

| Module     | Model Description | Docs                        | Type             | Status       | Description                           | Resources                                                           |
| ---------- | ----------------- | --------------------------- | ---------------- | ------------ | ------------------------------------- | ------------------------------------------------------------------- |
| `text_seg` | Text Segmenter    | [Link](jac_nlp/text_seg.md) | No Training req. | Experimental | Topical Change Detection in Documents | [Huggingface](https://huggingface.co/dennlinger/roberta-cls-consec) |

#### Summarization Models

Summarization in Natural Language Processing (NLP) refers to the process of creating a shorter, condensed version of a longer piece of text while retaining its key information and meaning. This can be done through various techniques such as extraction, where the most important sentences or phrases are identified and used to create a summary, or abstraction, where the summary is generated by synthesizing new sentences that capture the essence of the original text. Summarization can be applied to a wide range of tasks, such as summarizing news articles, scientific papers, legal documents, or social media posts, and can be used for various purposes, such as aiding in decision-making, information retrieval, or providing quick overviews.

Jaseci AI kit contains pre-built SOTA Summarization models that can be utilized immediately without any need for training.

| Module      | Model Description | Docs                                       | Type             | Status | Description                                          | Resources                                                                                                         |
| ----------- | ----------------- | ------------------------------------------ | ---------------- | ------ | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `cl_summer` | Summarizer        | [Link](jac_nlp/summerization/cl_summer.md) | No Training req. | Ready  | Extractive Summarization using Sumy                  | [Doc.](https://miso-belica.github.io/sumy/)                                                                       |
| `t5_sum`    | Summarizer        |     | No Training req. | Deprecated | Abstractive Summarization using the T5 Model         | [Doc.](https://huggingface.co/docs/transformers/model_doc/t5), [Paper](https://arxiv.org/pdf/1910.10683.pdf)      |
| `bart_sum`  | Summarizer        | [Link](jac_nlp/summerization/bart_sum.md)  | No Training req. | Ready  | Abstractive Summarization using the Bart Large Model | [Huggingface](https://huggingface.co/transformers/model_doc/bart.html), [Paper](https://arxiv.org/abs/1910.13461) |

#### Topic Modeling Models

Topic modeling is a technique used in natural language processing and machine learning to identify the topics present in a large corpus of text data. It involves analyzing the words and phrases in the text and grouping them together based on their similarity, in order to identify underlying themes or topics.

This process usually involves using algorithms such as Latent Dirichlet Allocation (LDA) or Non-negative Matrix Factorization (NMF) to identify the most likely topics present in the text, based on the frequency and co-occurrence of words.

Once the topics are identified, they can be used for a variety of purposes, such as understanding the main themes present in a corpus of documents, identifying patterns and trends in a particular field, or even for recommending related content to users.

Jaseci AI Kit NLP package comes with a ready to use topic modeling model with SOTA performance.


| Module      | Model Description | Docs                         | Type             | Status       | Description                                                  | Resources |
| ----------- | ----------------- | ---------------------------- | ---------------- | ------------ | ------------------------------------------------------------ | --------- |
| `topic_ext` | Topic Extraction  | [Link](jac_nlp/topic_ext.md) | No Training req. | Experimental | Indentifying most relevent topics for given set of documents |


#### Sentiment Analysis Models

Sentiment analysis is a technique used to automatically identify the sentiment or opinion expressed in a piece of text, such as a review or social media post. It involves using natural language processing and machine learning algorithms to analyze the text and classify it as positive, negative, or neutral.

The process usually involves preprocessing the text to remove stop words and other irrelevant information, then using techniques such as bag-of-words or word embeddings to represent the text in a way that can be analyzed by a machine learning algorithm.

Once the text is represented, a classification algorithm such as a Naive Bayes classifier or a neural network can be trained to predict the sentiment of the text. The output of the sentiment analysis can be used for a variety of purposes, such as understanding customer feedback, monitoring brand reputation, or even for predicting stock market trends.

Jaseci AI Kit NLP package comes with a ready to use sentiment analysis model with SOTA performance.

| Module      | Model Description  | Docs                         | Type             | Status       | Description                                                                           | Resources |
| ----------- | ------------------ | ---------------------------- | ---------------- | ------------ | ------------------------------------------------------------------------------------- | --------- |
| `sentiment` | Sentiment Analysis | [Link](jac_nlp/sentiment.md) | No Training req. | Experimental | Determining the overall sentiment expressed is text as positive, negative, or neutral |

#### Paraphraser Model

Paraphrasing is the process of restating or rephrasing a piece of text in your own words, while retaining the original meaning and intent of the text. It involves carefully analyzing the original text and using synonyms, alternative phrasing, and other linguistic techniques to express the same information in a different way.

Paraphrasing is often used to avoid plagiarism, as it allows you to use ideas and information from another source without directly copying their words. It can also be used to simplify complex text or to adapt text for a different audience or purpose.

Effective paraphrasing requires a strong understanding of the original text and the ability to express its meaning accurately and clearly in your own words. It is an important skill for writers, researchers, and anyone who needs to communicate complex ideas in a clear and concise manner.

| Module        | Model Description | Docs                           | Type             | Status       | Description                                                 | Resources |
| ------------- | ----------------- | ------------------------------ | ---------------- | ------------ | ----------------------------------------------------------- | --------- |
| `paraphraser` | Text Paraphrasing | [Link](jac_nlp/paraphraser.md) | No Training req. | Experimental | Returning list of paraphrased text of the given input text. |           |


#### Text Generation Model

Text generation is a technology that uses algorithms and machine learning models to generate written text autonomously. It involves the use of natural language processing techniques to analyze existing text and create new content based on patterns and structures found in the data. Text generation can be used for a variety of applications, such as content creation, language translation, and chat-bots. It has the potential to increase efficiency and productivity by reducing the amount of time and effort required to create new content. However, it also raises concerns about the potential for the technology to be used maliciously, such as for the creation of fake news or propaganda.

| Module | Model Description | Docs                                    | Type             | Status       | Description                                        | Resources                                                              |
| ------ | ----------------- | --------------------------------------- | ---------------- | ------------ | -------------------------------------------------- | ---------------------------------------------------------------------- |
| `gpt2` | GPT-2             | [Link](jac_nlp/text_generation/gpt2.md) | No Training req. | Experimental | Predicting the next sentence in a sequence of text | [Huggingface](https://huggingface.co/transformers/model_doc/gpt2.html) |

### Installation

Each module can be installed individually or all at once. To install all modules at once.
```bash
pip install jac_nlp[all] # Installs all the modules present in the jac_nlp package
pip install jac_nlp[use_enc] # Installs the use_enc module present in the jac_nlp package
pip install jac_nlp[use_qa,ent_ext] # Installs the use_qa and ent_ext modules present in the jac_nlp package
```

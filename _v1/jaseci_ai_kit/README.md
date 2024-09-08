# Jaseci AI Kit
Jaseci AI Kit is a collection of state-of-the-art machine learning models from different domains (NLP, Computer Vision, Speech etc.) that are readily available to load into jaseci. Jaseci AI Kit consist of 4 Main Python Packages

- [Jaseci AI Kit](#jaseci-ai-kit)
  - [**Jac NLP Modules**](#jac-nlp-modules)
    - [Available Modules in Jac NLP](#available-modules-in-jac-nlp)
      - [Text Encoders](#text-encoders)
      - [Named Entity Recognition Models](#named-entity-recognition-models)
      - [Text Segmentation Modules](#text-segmentation-modules)
      - [Summarization Models](#summarization-models)
      - [Topic Modeling Models](#topic-modeling-models)
      - [Sentiment Analysis Models](#sentiment-analysis-models)
      - [Paraphraser Model](#paraphraser-model)
      - [Text Generation Model](#text-generation-model)
    - [Installation](#installation)
  - [**Jac Speech Modules**](#jac-speech-modules)
    - [Available Modules in Jac Speech](#available-modules-in-jac-speech)
      - [Speech to Text](#speech-to-text)
      - [Text to Speech Synthesizing](#text-to-speech-synthesizing)
    - [Installation](#installation-1)
  - [**Jac Vision Modules**](#jac-vision-modules)
    - [Available Modules in Jac Speech](#available-modules-in-jac-speech-1)
  - [**Jac Miscellaneous Modules**](#jac-miscellaneous-modules)
    - [Available Modules in Jac Speech](#available-modules-in-jac-speech-2)
      - [Clustering](#clustering)
      - [Translator Module](#translator-module)
      - [PDF Extractor Module](#pdf-extractor-module)
      - [Personalized Head](#personalized-head)
    - [Installation](#installation-2)

## **Jac NLP Modules**

The `jac_nlp` package contains a collection of state-of-the-art NLP models that can be used to perform various nlp tasks such as named entity recongnition, text summerization, embedding generation, topic extraction etc. following is a list of all the models available in the `jac_nlp` package.

### Available Modules in Jac NLP

#### Text Encoders

Text encoders are a type of encoder used in natural language processing (NLP) that transform raw text into a numerical representation that can be used by machine learning algorithms. Text encoders are designed to capture the semantic and syntactic information of the input text and convert it into a vectorized format that is suitable for further processing. Text encoders are essential components in many NLP applications such as language translation, sentiment analysis, and text classification.

Jaseci provides a selection of pre-built text encoders that are available for use without any training.


| Module      | Model Description | Docs                                                       | Type                    | Status | Description                                                 | Resources                                 |
| ----------- | ----------------- | ---------------------------------------------------------- | ----------------------- | ------ | ----------------------------------------------------------- | ----------------------------------------- |
| `use_enc`   | USE Encoder       | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/use_enc/README.md)   | Zero-shot               | Ready  | Sentence-level embedding pre-trained on general text corpus | [Paper](https://arxiv.org/abs/1803.11175) |
| `use_qa`    | USE QA            | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/use_qa/README.md)    | Zero-shot               | Ready  | Sentence-level embedding pre-trained on Q&A data corpus     | [Paper](https://arxiv.org/abs/1803.11175) |
| `fast_enc`  | FastText          | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/fast_enc/README.md)  | Training req.           | Ready  | FastText Text Classifier                                    | [Paper](https://arxiv.org/abs/1712.09405) |
| `bi_enc`    | Bi-Encoder        | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/bi_enc/README.md)    | Training req./Zero-shot | Ready  | Dual sentence-level encoders                                | [Paper](https://arxiv.org/abs/1803.11175) |
| `sbert_sim` | SBert Similarity  | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/sbert_sim/README.md) | Training req./Zero-shot | Ready  | SBert Encoders for Sentence Similarity                      | [Paper](https://arxiv.org/abs/1908.10084) |

#### Named Entity Recognition Models

Named Entity Recognition (NER) is a subtask of natural language processing (NLP) that involves identifying and classifying named entities in unstructured text. Named entities are words or phrases that refer to specific people, places, organizations, products, and other entities. The goal of NER is to identify and classify these entities into predefined categories such as person, location, organization, date, time, and others. NER is a crucial step in many NLP applications such as information retrieval, sentiment analysis, and question answering systems. NER can be achieved using various machine learning approaches such as rule-based systems, statistical models, and deep learning models. Deep learning models such as recurrent neural networks (RNNs) and transformers have achieved state-of-the-art performance in NER tasks.

Jaseci offers pre-built NER models that can be utilized immediately without any need for training.

| Module                | Model Description | Docs                                                     | Type          | Status | Description                                                     | Resources                                                                                               |
| --------------------- | ----------------- | -------------------------------------------------------- | ------------- | ------ | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ent_ext`/ `lstm_ner` | Flair NER         | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/ent_ext/README.md) | Training req. | Ready  | Entity extraction using the FLAIR NER framework                 |
| `tfm_ner`             | Transformer NER   | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/tfm_ner/README.md) | Training req. | Ready  | Token classification on Transformer models, can be used for NER | [Huggingface](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) |

#### Text Segmentation Modules

Text segmentation refers to the process of dividing a large chunk of text into smaller, meaningful segments. This can be useful for a variety of natural language processing tasks, such as sentiment analysis, topic modeling, and text summarization. Text segmentation can be performed using various techniques, including rule-based approaches, statistical models, and machine learning algorithms. The goal is to break down the text into meaningful units that can be analyzed and processed more effectively.

Jaseci offers a pre-built Text Segmentation model that can be utilized immediately without any need for training.

| Module     | Model Description | Docs                                                      | Type             | Status      | Description                           | Resources                                                           |
| ---------- | ----------------- | --------------------------------------------------------- | ---------------- | ----------- | ------------------------------------- | ------------------------------------------------------------------- |
| `text_seg` | Text Segmenter    | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/text_seg/README.md) | No Training req. | Experimetal | Topical Change Detection in Documents | [Huggingface](https://huggingface.co/dennlinger/roberta-cls-consec) |


#### Summarization Models

Summarization in Natural Language Processing (NLP) refers to the process of creating a shorter, condensed version of a longer piece of text while retaining its key information and meaning. This can be done through various techniques such as extraction, where the most important sentences or phrases are identified and used to create a summary, or abstraction, where the summary is generated by synthesizing new sentences that capture the essence of the original text. Summarization can be applied to a wide range of tasks, such as summarizing news articles, scientific papers, legal documents, or social media posts, and can be used for various purposes, such as aiding in decision-making, information retrieval, or providing quick overviews.

Jaseci AI kit contains pre-built SOTA Summerization models that can be utilized immediately without any need for training.

| Module      | Model Description | Docs                                                       | Type             | Status | Description                                          | Resources                                                                                                         |
| ----------- | ----------------- | ---------------------------------------------------------- | ---------------- | ------ | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `cl_summer` | Summarizer        | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/cl_summer/README.md) | No Training req. | Ready  | Extractive Summarization using Sumy                  | [Doc.](https://miso-belica.github.io/sumy/)                                                                       |
| `t5_sum`    | Summarizer        | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/t5_sum/README.md)    | No Training req. | Ready  | Abstractive Summarization using the T5 Model         | [Doc.](https://huggingface.co/docs/transformers/model_doc/t5), [Paper](https://arxiv.org/pdf/1910.10683.pdf)      |
| `bart_sum`  | Summarizer        | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/bart_sum/README.md)  | No Training req. | Ready  | Abstractive Summarization using the Bart Large Model | [Huggingface](https://huggingface.co/transformers/model_doc/bart.html), [Paper](https://arxiv.org/abs/1910.13461) |

#### Topic Modeling Models

Topic modeling is a technique used in natural language processing and machine learning to identify the topics present in a large corpus of text data. It involves analyzing the words and phrases in the text and grouping them together based on their similarity, in order to identify underlying themes or topics.

This process usually involves using algorithms such as Latent Dirichlet Allocation (LDA) or Non-negative Matrix Factorization (NMF) to identify the most likely topics present in the text, based on the frequency and co-occurrence of words.

Once the topics are identified, they can be used for a variety of purposes, such as understanding the main themes present in a corpus of documents, identifying patterns and trends in a particular field, or even for recommending related content to users.

Jaseci AI Kit NLP package comes with a ready to use topic modeling model with SOTA performance.


| Module      | Model Description | Docs                                                       | Type             | Status      | Description                                                  | Resources |
| ----------- | ----------------- | ---------------------------------------------------------- | ---------------- | ----------- | ------------------------------------------------------------ | --------- |
| `topic_ext` | Topic Extraction  | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/topic_ext/README.md) | No Training req. | Experimetal | Indentifying most relevent topics for given set of documents |


#### Sentiment Analysis Models

Sentiment analysis is a technique used to automatically identify the sentiment or opinion expressed in a piece of text, such as a review or social media post. It involves using natural language processing and machine learning algorithms to analyze the text and classify it as positive, negative, or neutral.

The process usually involves preprocessing the text to remove stop words and other irrelevant information, then using techniques such as bag-of-words or word embeddings to represent the text in a way that can be analyzed by a machine learning algorithm.

Once the text is represented, a classification algorithm such as a Naive Bayes classifier or a neural network can be trained to predict the sentiment of the text. The output of the sentiment analysis can be used for a variety of purposes, such as understanding customer feedback, monitoring brand reputation, or even for predicting stock market trends.

Jaseci AI Kit NLP package comes with a ready to use sentiment analysis model with SOTA performance.

| Module      | Model Description  | Docs                                                       | Type             | Status      | Description                                                                           | Resources |
| ----------- | ------------------ | ---------------------------------------------------------- | ---------------- | ----------- | ------------------------------------------------------------------------------------- | --------- |
| `sentiment` | Sentiment Analysis | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/sentiment/README.md) | No Training req. | Experimetal | Determining the overall sentiment expressed is text as positive, negative, or neutral |

#### Paraphraser Model

Paraphrasing is the process of restating or rephrasing a piece of text in your own words, while retaining the original meaning and intent of the text. It involves carefully analyzing the original text and using synonyms, alternative phrasing, and other linguistic techniques to express the same information in a different way.

Paraphrasing is often used to avoid plagiarism, as it allows you to use ideas and information from another source without directly copying their words. It can also be used to simplify complex text or to adapt text for a different audience or purpose.

Effective paraphrasing requires a strong understanding of the original text and the ability to express its meaning accurately and clearly in your own words. It is an important skill for writers, researchers, and anyone who needs to communicate complex ideas in a clear and concise manner.

| Module        | Model Description | Docs                                                         | Type             | Status      | Description                                                 | Resources |
| ------------- | ----------------- | ------------------------------------------------------------ | ---------------- | ----------- | ----------------------------------------------------------- | --------- |
| `paraphraser` | Text Paraphrasing | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/paraphraser/README.md) | No Training req. | Experimetal | Returning list of paraphrased text of the given input text. |           |


#### Text Generation Model

Text generation is a technology that uses algorithms and machine learning models to generate written text autonomously. It involves the use of natural language processing techniques to analyze existing text and create new content based on patterns and structures found in the data. Text generation can be used for a variety of applications, such as content creation, language translation, and chatbots. It has the potential to increase efficiency and productivity by reducing the amount of time and effort required to create new content. However, it also raises concerns about the potential for the technology to be used maliciously, such as for the creation of fake news or propaganda.

| Module | Model Description | Docs                                                  | Type             | Status      | Description                                        | Resources                                                              |
| ------ | ----------------- | ----------------------------------------------------- | ---------------- | ----------- | -------------------------------------------------- | ---------------------------------------------------------------------- |
| `gpt2` | GPT-2             | [Link](/jaseci_ai_kit/jac_nlp/jac_nlp/gpt2/README.md) | No Training req. | Experimetal | Predicting the next sentence in a sequence of text | [Huggingface](https://huggingface.co/transformers/model_doc/gpt2.html) |

### Installation

Each module can be installed individually or all at once. To install all modules at once.
```bash
pip install jac_nlp[all] # Installs all the modules present in the jac_nlp package
pip install jac_nlp[use_enc] # Installs the use_enc module present in the jac_nlp package
pip install jac_nlp[use_qa,ent_ext] # Installs the use_qa and ent_ext modules present in the jac_nlp package
```

## **Jac Speech Modules**

The `jac_speech` package contains a collection of state-of-the-art Speech models that can be used to perform various speech tasks such as speech to text, text to speech etc. following is a list of all the models available in the `jac_speech` package.

### Available Modules in Jac Speech

#### Speech to Text

Speech to text is a technology that allows users to convert spoken words into written text. It involves the use of speech recognition software that analyzes audio input, identifies the words spoken, and transcribes them into text. Speech to text technology has many practical applications, including dictation, transcription of meetings or lectures, and captioning of videos or live events for the deaf or hard of hearing. It has the potential to increase accessibility for individuals who have difficulty typing or writing, as well as improve productivity in many industries.

| Module | Model Description        | Docs                                                       | Type             | Status | Description                                            | Resources                                                                                                                                                   |
| ------ | ------------------------ | ---------------------------------------------------------- | ---------------- | ------ | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stt`  | Speech to Text - Whisper | [Link](/jaseci_ai_kit/jac_speech/jac_speech/stt/README.md) | No Training req. | Ready  | transcription or translation of a give audio sequence. | [Robust Speech Recognition via Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf), [OpenAI Whisper](https://openai.com/blog/whisper/) |


#### Text to Speech Synthesizing

Text to speech is a technology that converts written text into spoken words. It involves the use of software that analyzes written input, synthesizes the text into a spoken format, and outputs the audio through speakers or headphones. Text to speech technology has many practical applications, including assistive technology for individuals with visual impairments, language learning tools, and automated customer service systems. It has the potential to increase accessibility for individuals who have difficulty reading or comprehending written text, as well as improve efficiency in many industries by providing a faster and more natural way to convey information.

| Module   | Model Description                  | Docs                                                          | Type             | Status | Description                                      | Resources                                                                                                                                                                                                                                                                 |
| -------- | ---------------------------------- | ------------------------------------------------------------- | ---------------- | ------ | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `vc_tts` | Text to Speech with voice cloning. | [Link](/jaseci_ai_kit/jac_speech/jac_speech/vc_tts/README.md) | No Training req. | Ready  | List of Amplitudes of the synthesized audio wav. | [Tacotron2](https://arxiv.org/abs/1712.05884), [Waveglow](https://arxiv.org/abs/1811.00002), [Hifigan](https://arxiv.org/abs/2010.05646), [Nvidia Tacotron2 implementation](https://github.com/NVIDIA/tacotron2), [SpeechBrain](https://speechbrain.github.io/index.html) |


### Installation

Each module can be installed individually or all at once. To install all modules at once.

```bash
pip install jac_speech[all] # Installs all the modules present in the jac_nlp package
pip install jac_speech[tts] # Installs the use_enc module present in the jac_nlp package
pip install jac_speech[tts,vc_tts] # Installs the use_qa and ent_ext modules present in the jac_nlp package
```

> **Note**
>
> After installing the `jac speech[vc tts]` module, if you see a numba version failure, upgrade to `numba==0.56.4` to fix the issue.
>
>


## **Jac Vision Modules**

The `jac_vision` package contains a collection of state-of-the-art Computer Vision models that can be used to perform various computer vision tasks such as image classification, object detection, image segmentation etc. following is a list of all the models available in the `jac_vision` package.

### Available Modules in Jac Speech

## **Jac Miscellaneous Modules**

The `jac_misc` package contains a collection of miscellaneous models that can be used to perform various tasks such as translation, pdf extraction, personalized head etc. following is a list of all the models available in the `jac_misc` package.

### Available Modules in Jac Speech

#### Clustering

Clustering is a technique used in data analysis and machine learning to group a set of objects in such a way that objects in the same group, called a cluster, are more similar to each other than to those in other groups. Clustering can be used for a variety of tasks, such as customer segmentation, image recognition, anomaly detection, and more. Clustering algorithms typically rely on mathematical measures of similarity or distance between objects, and the goal is to partition the data into groups that are internally homogeneous and externally heterogeneous. The choice of clustering algorithm depends on the nature of the data, the desired number of clusters, and the computational resources available.

| Module    | Model Description                                         | Docs                                                       | Type             | Status      | Description                                                                                                                       | Resources |
| --------- | --------------------------------------------------------- | ---------------------------------------------------------- | ---------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------- | --------- |
| `cluster` | Indentifying Posible Similar Clusters in Set of Documents | [Link](/jaseci_ai_kit/jac_misc/jac_misc/cluster/README.md) | No Training req. | Experimetal | [UMAP](https://umap-learn.readthedocs.io/en/latest/) , [HBDSCAN](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html) |


#### Translator Module

A translator is a program or a person that converts text or speech from one language into another. Translators are used to bridge the language barrier between people who speak different languages and are essential in fields such as international business, diplomacy, tourism, and education. Machine translation, performed by computer programs, uses algorithms and statistical models to analyze and translate text or speech from one language to another. Human translators, on the other hand, use their language skills and cultural knowledge to produce accurate and idiomatic translations. While machine translation is faster and more cost-effective, it often lacks the nuances and context-specific knowledge that human translators bring to the task. Therefore, the choice of using a machine translator or a human translator depends on the requirements and goals of the task at hand.

| Module       | Model Description                                 | Docs                                                          | Type             | Status | Description                                                                                                                                                                                | Resources |
| ------------ | ------------------------------------------------- | ------------------------------------------------------------- | ---------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- |
| `translator` | Text Translation for 50 languages to 50 languages | [Link](/jaseci_ai_kit/jac_misc/jac_misc/translator/README.md) | No Training req. | Ready  | [Multilingual Denoising Pre-training for Neural Machine Translation](https://arxiv.org/abs/2001.08210), [Huggingface MBart Docs](https://huggingface.co/transformers/model_doc/mbart.html) |


#### PDF Extractor Module

| Module    | Model Description                           | Docs                                                       | Type             | Status | Description                                      | Resources |
| --------- | ------------------------------------------- | ---------------------------------------------------------- | ---------------- | ------ | ------------------------------------------------ | --------- |
| `pdf_ext` | Extract content from a PDF file via PyPDF2. | [Link](/jaseci_ai_kit/jac_misc/jac_misc/pdf_ext/README.md) | No Training req. | Ready  | [Doc.](https://pypdf2.readthedocs.io/en/latest/) |

#### Personalized Head

| Module | Model Description                          | Docs                                                  | Type          | Status | Description  | Resources |
| ------ | ------------------------------------------ | ----------------------------------------------------- | ------------- | ------ | ------------ | --------- |
| `ph`   | Extract content from a PDF file via PyPDF2 | [Link](/jaseci_ai_kit/jac_misc/jac_misc/ph/README.md) | Training Req. | Ready  | Experimental |           |


### Installation

Each module can be installed individually or all at once. To install all modules at once.
```bash
pip install jac_misc[all] # Installs all the modules present in the jac_misc package
pip install jac_misc[translator] # Installs the translator module present in the jac_misc package
pip install jac_misc[cluster,pdf_ext] # Installs the cluster and pdf_ext module present in the jac_misc package
```


:zap: For Contributors
| Use the `install.sh` to install the modules you need. `bash install.sh all` will install all the modules. `bash install.sh stt use_enc` will install only the stt and use_enc modules. |


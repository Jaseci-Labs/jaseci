# Jaseci AI Kit
Jaseci AI Kit is a collection of state-of-the-art machine learning models from different domains (NLP, Computer Vision, Speech etc.) that are readily available to load into jaseci. Jaseci AI Kit consist of 4 Main Python Packages

- [Jaseci AI Kit](#jaseci-ai-kit)
  - [Jac NLP Modules](#jac-nlp-modules)
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
  - [Jac Vision Modules](#jac-vision-modules)
  - [Jac Speech Modules](#jac-speech-modules)
  - [Jac Miscellaneous Modules](#jac-miscellaneous-modules)
- [Jaseci Vision Package `(jac_vision)`](#jaseci-vision-package-jac_vision)
- [Jaseci Speech Package `(jac_speech)`](#jaseci-speech-package-jac_speech)
- [Jaseci Misc Package `(jac_misc)`](#jaseci-misc-package-jac_misc)
- [Examples](#examples)
  - [Speech](#speech)
    - [Speech2Text (`stt`)](#speech2text-stt)
      - [Example Jac Usage:](#example-jac-usage)
      - [Example Jac Usage:](#example-jac-usage-1)
    - [Text2Speech (`tts`)](#text2speech-tts)
      - [Example Jac Usage:](#example-jac-usage-2)
  - [Text Processing](#text-processing)
    - [](#)
    - [Text Generation (`gpt2`)](#text-generation-gpt2)
      - [Example Jac Usage:](#example-jac-usage-3)
    - [Text Translation (`translator`)](#text-translation-translator)
      - [Example Jac Usage:](#example-jac-usage-4)
    - [Text Cluster (`cluster`)](#text-cluster-cluster)

## Jac NLP Modules

The `jac_nlp` package contains a collection of state-of-the-art NLP models that can be used to perform various nlp tasks such as named entity recongnition, text summerization, embedding generation, topic extraction etc. following is a list of all the models available in the `jac_nlp` package.

### Available Modules in Jac NLP

#### Text Encoders

Text encoders are a type of encoder used in natural language processing (NLP) that transform raw text into a numerical representation that can be used by machine learning algorithms. Text encoders are designed to capture the semantic and syntactic information of the input text and convert it into a vectorized format that is suitable for further processing. Text encoders are essential components in many NLP applications such as language translation, sentiment analysis, and text classification.

Jaseci provides a selection of pre-built text encoders that are available for use without any training.


| Module      | Model Description | Docs                                | Type                    | Status | Description                                                 | Resources                                 |
| ----------- | ----------------- | ----------------------------------- | ----------------------- | ------ | ----------------------------------------------------------- | ----------------------------------------- |
| `use_enc`   | USE Encoder       | [Link](jac_nlp/use_enc/README.md)   | Zero-shot               | Ready  | Sentence-level embedding pre-trained on general text corpus | [Paper](https://arxiv.org/abs/1803.11175) |
| `use_qa`    | USE QA            | [Link](jac_nlp/use_qa/README.md)    | Zero-shot               | Ready  | Sentence-level embedding pre-trained on Q&A data corpus     | [Paper](https://arxiv.org/abs/1803.11175) |
| `fast_enc`  | FastText          | [Link](jac_nlp/fast_enc/README.md)  | Training req.           | Ready  | FastText Text Classifier                                    | [Paper](https://arxiv.org/abs/1712.09405) |
| `bi_enc`    | Bi-Encoder        | [Link](jac_nlp/bi_enc/README.md)    | Training req./Zero-shot | Ready  | Dual sentence-level encoders                                | [Paper](https://arxiv.org/abs/1803.11175) |
| `sbert_sim` | SBert Similarity  | [Link](jac_nlp/sbert_sim/README.md) | Training req./Zero-shot | Ready  | SBert Encoders for Sentence Similarity                      | [Paper](https://arxiv.org/abs/1908.10084) |

#### Named Entity Recognition Models

Named Entity Recognition (NER) is a subtask of natural language processing (NLP) that involves identifying and classifying named entities in unstructured text. Named entities are words or phrases that refer to specific people, places, organizations, products, and other entities. The goal of NER is to identify and classify these entities into predefined categories such as person, location, organization, date, time, and others. NER is a crucial step in many NLP applications such as information retrieval, sentiment analysis, and question answering systems. NER can be achieved using various machine learning approaches such as rule-based systems, statistical models, and deep learning models. Deep learning models such as recurrent neural networks (RNNs) and transformers have achieved state-of-the-art performance in NER tasks.

Jaseci offers pre-built NER models that can be utilized immediately without any need for training.

| Module                | Model Description | Docs                              | Type          | Status | Description                                                     | Resources                                                                                               |
| --------------------- | ----------------- | --------------------------------- | ------------- | ------ | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ent_ext`/ `lstm_ner` | Flair NER         | [Link](jac_nlp/ent_ext/README.md) | Training req. | Ready  | Entity extraction using the FLAIR NER framework                 |
| `tfm_ner`             | Transformer NER   | [Link](jac_nlp/tfm_ner/README.md) | Training req. | Ready  | Token classification on Transformer models, can be used for NER | [Huggingface](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) |

#### Text Segmentation Modules

Text segmentation refers to the process of dividing a large chunk of text into smaller, meaningful segments. This can be useful for a variety of natural language processing tasks, such as sentiment analysis, topic modeling, and text summarization. Text segmentation can be performed using various techniques, including rule-based approaches, statistical models, and machine learning algorithms. The goal is to break down the text into meaningful units that can be analyzed and processed more effectively.

Jaseci offers a pre-built Text Segmentation model that can be utilized immediately without any need for training.

| Module     | Model Description | Docs                               | Type             | Status      | Description                           | Resources                                                           |
| ---------- | ----------------- | ---------------------------------- | ---------------- | ----------- | ------------------------------------- | ------------------------------------------------------------------- |
| `text_seg` | Text Segmenter    | [Link](jac_nlp/text_seg/README.md) | No Training req. | Experimetal | Topical Change Detection in Documents | [Huggingface](https://huggingface.co/dennlinger/roberta-cls-consec) |


#### Summarization Models

Summarization in Natural Language Processing (NLP) refers to the process of creating a shorter, condensed version of a longer piece of text while retaining its key information and meaning. This can be done through various techniques such as extraction, where the most important sentences or phrases are identified and used to create a summary, or abstraction, where the summary is generated by synthesizing new sentences that capture the essence of the original text. Summarization can be applied to a wide range of tasks, such as summarizing news articles, scientific papers, legal documents, or social media posts, and can be used for various purposes, such as aiding in decision-making, information retrieval, or providing quick overviews.

Jaseci AI kit contains pre-built SOTA Summerization models that can be utilized immediately without any need for training.

| Module      | Model Description | Docs                                | Type             | Status | Description                                          | Resources                                                                                                         |
| ----------- | ----------------- | ----------------------------------- | ---------------- | ------ | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `cl_summer` | Summarizer        | [Link](jac_nlp/cl_summer/README.md) | No Training req. | Ready  | Extractive Summarization using Sumy                  | [Doc.](https://miso-belica.github.io/sumy/)                                                                       |
| `t5_sum`    | Summarizer        | [Link](jac_nlp/t5_sum/README.md)    | No Training req. | Ready  | Abstractive Summarization using the T5 Model         | [Doc.](https://huggingface.co/docs/transformers/model_doc/t5), [Paper](https://arxiv.org/pdf/1910.10683.pdf)      |
| `bart_sum`  | Summarizer        | [Link](jac_nlp/bart_sum/README.md)  | No Training req. | Ready  | Abstractive Summarization using the Bart Large Model | [Huggingface](https://huggingface.co/transformers/model_doc/bart.html), [Paper](https://arxiv.org/abs/1910.13461) |

#### Topic Modeling Models

Topic modeling is a technique used in natural language processing and machine learning to identify the topics present in a large corpus of text data. It involves analyzing the words and phrases in the text and grouping them together based on their similarity, in order to identify underlying themes or topics.

This process usually involves using algorithms such as Latent Dirichlet Allocation (LDA) or Non-negative Matrix Factorization (NMF) to identify the most likely topics present in the text, based on the frequency and co-occurrence of words.

Once the topics are identified, they can be used for a variety of purposes, such as understanding the main themes present in a corpus of documents, identifying patterns and trends in a particular field, or even for recommending related content to users.

Jaseci AI Kit NLP package comes with a ready to use topic modeling model with SOTA performance.


| Module      | Model Description | Docs                                | Type             | Status      | Description                                                  | Resources |
| ----------- | ----------------- | ----------------------------------- | ---------------- | ----------- | ------------------------------------------------------------ | --------- |
| `topic_ext` | Topic Extraction  | [Link](jac_nlp/topic_ext/README.md) | No Training req. | Experimetal | Indentifying most relevent topics for given set of documents |


#### Sentiment Analysis Models

Sentiment analysis is a technique used to automatically identify the sentiment or opinion expressed in a piece of text, such as a review or social media post. It involves using natural language processing and machine learning algorithms to analyze the text and classify it as positive, negative, or neutral.

The process usually involves preprocessing the text to remove stop words and other irrelevant information, then using techniques such as bag-of-words or word embeddings to represent the text in a way that can be analyzed by a machine learning algorithm.

Once the text is represented, a classification algorithm such as a Naive Bayes classifier or a neural network can be trained to predict the sentiment of the text. The output of the sentiment analysis can be used for a variety of purposes, such as understanding customer feedback, monitoring brand reputation, or even for predicting stock market trends.

Jaseci AI Kit NLP package comes with a ready to use sentiment analysis model with SOTA performance.

| Module      | Model Description  | Docs                                | Type             | Status      | Description                                                                           | Resources |
| ----------- | ------------------ | ----------------------------------- | ---------------- | ----------- | ------------------------------------------------------------------------------------- | --------- |
| `sentiment` | Sentiment Analysis | [Link](jac_nlp/sentiment/README.md) | No Training req. | Experimetal | Determining the overall sentiment expressed is text as positive, negative, or neutral |

#### Paraphraser Model

Paraphrasing is the process of restating or rephrasing a piece of text in your own words, while retaining the original meaning and intent of the text. It involves carefully analyzing the original text and using synonyms, alternative phrasing, and other linguistic techniques to express the same information in a different way.

Paraphrasing is often used to avoid plagiarism, as it allows you to use ideas and information from another source without directly copying their words. It can also be used to simplify complex text or to adapt text for a different audience or purpose.

Effective paraphrasing requires a strong understanding of the original text and the ability to express its meaning accurately and clearly in your own words. It is an important skill for writers, researchers, and anyone who needs to communicate complex ideas in a clear and concise manner.

| Module        | Model Description | Docs                                  | Type             | Status      | Description                                                 | Resources |
| ------------- | ----------------- | ------------------------------------- | ---------------- | ----------- | ----------------------------------------------------------- | --------- |
| `paraphraser` | Text Paraphrasing | [Link](jac_nlp/paraphraser/README.md) | No Training req. | Experimetal | Returning list of paraphrased text of the given input text. |           |


#### Text Generation Model

| Module | Model Description | Docs                          | Type             | Status      | Description                                        | Resources                                                              |
| ------ | ----------------- | ----------------------------- | ---------------- | ----------- | -------------------------------------------------- | ---------------------------------------------------------------------- |
| `gpt2` | GPT-2             | [Link](#text-generation-gpt2) | No Training req. | Experimetal | Predicting the next sentence in a sequence of text | [Huggingface](https://huggingface.co/transformers/model_doc/gpt2.html) |

### Installation

Each module can be installed individually or all at once. To install all modules at once.
```bash
pip install jac_nlp[all] # Installs all the modules present in the jac_nlp package
pip install jac_nlp[use_enc] # Installs the use_enc module present in the jac_nlp package
pip install jac_nlp[use_qa,ent_ext] # Installs the use_qa and ent_ext modules present in the jac_nlp package
```

## Jac Vision Modules

## Jac Speech Modules

## Jac Miscellaneous Modules



> **Note**
>
> After installing the `jac speech[vc tts]` module, if you see a numba version failure, upgrade to `numba==0.56.4` to fix the issue.
>
>

| :zap: For Contributors                                                                                                                                                                 |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Use the `install.sh` to install the modules you need. `bash install.sh all` will install all the modules. `bash install.sh stt use_enc` will install only the stt and use_enc modules. |



# Jaseci Vision Package `(jac_vision)`
The `jac_vision` package contains a collection of state-of-the-art Computer Vision models that can be used to perform various computer vision tasks such as image classification, object detection, image segmentation etc. following is a list of all the models available in the `jac_vision` package.

# Jaseci Speech Package `(jac_speech)`
The `jac_speech` package contains a collection of state-of-the-art Speech models that can be used to perform various speech tasks such as speech to text, text to speech etc. following is a list of all the models available in the `jac_speech` package.

| Module | Model Type     | Model Name | Example                  | Type             | Status | Description                                            | Resources                                                                                                                                                                                                                                                                 |
| ------ | -------------- | ---------- | ------------------------ | ---------------- | ------ | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stt`  | Speech to Text | Whisper    | [Link](#speech2text-stt) | No Training req. | Ready  | transcription or translation of a give audio sequence. | [Robust Speech Recognition via Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf), [OpenAI Whisper](https://openai.com/blog/whisper/)                                                                                                               |
| `tts`  | Text to Speech | Tacotron   | [Link](#)                | No Training req. | Ready  | List of Amplitudes of the synthesized audio wav.       | [Tacotron2](https://arxiv.org/abs/1712.05884), [Waveglow](https://arxiv.org/abs/1811.00002), [Hifigan](https://arxiv.org/abs/2010.05646), [Nvidia Tacotron2 implementation](https://github.com/NVIDIA/tacotron2), [SpeechBrain](https://speechbrain.github.io/index.html) |

To load the `jac_speech.stt` package into jaseci in local environment, run the following command in the jsctl console.
```bash
jsctl > actions load module jac_speech.stt
```

# Jaseci Misc Package `(jac_misc)`
The `jac_misc` package contains a collection of miscellaneous models that can be used to perform various tasks such as translation, pdf extraction, personalized head etc. following is a list of all the models available in the `jac_misc` package.

| Module       | Model Name        | Example                                | Type             | Status       | Description                                               | Resources                                                                                                                                                                                  |
| ------------ | ----------------- | -------------------------------------- | ---------------- | ------------ | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `translator` | Text Translation  | [Link](#text-translation-translator)   | No Training req. | Ready        | Text Translation for 50 languages to 50 languages         | [Multilingual Denoising Pre-training for Neural Machine Translation](https://arxiv.org/abs/2001.08210), [Huggingface MBart Docs](https://huggingface.co/transformers/model_doc/mbart.html) |
| `cluster`    | Text Cluster      | [Link](#text-cluster-cluster)          | No Training req. | Experimetal  | Indentifying Posible Similar Clusters in Set of Documents | [UMAP](https://umap-learn.readthedocs.io/en/latest/) , [HBDSCAN](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html)                                                          |
| `pdf_ext`    | PDF Extractor     | [Link](#pdf-extractor-pdf_ext)         | No Training req. | Ready        | Extract content from a PDF file via PyPDF2                | [Doc.](https://pypdf2.readthedocs.io/en/latest/)                                                                                                                                           |
| `ph`         | Personalized Head | [Link](jac_misc/jac_misc/ph/README.md) | Training Req.    | Experimental | Extract content from a PDF file via PyPDF2                |                                                                                                                                                                                            |


To load the `jac_misc.translator` package into jaseci in local environment, run the following command in the jsctl console.
```bash
jsctl > actions load module jac_misc.translator
```

# Examples

## Speech
### Speech2Text (`stt`)
`stt` uses the `whisper-tiny` to get the transcription or translation of a give audio sequence.

`stt.transcribe` to get the transcription. Following are the parameters of the action.
* `language` - Spoken Language in the Audio. Type: Type: `str` Default: `en`
* `array` - Audio Array (should be sampled at 16kHz). Type: `list[float]` (Optional)
* `audio_file` - Location to a Audio file. Type: `str` (Optional) - Works only in local mode
* `url` - Web URL to a Audio file. Type: `str` (Optional)

Return type of the action is `str`.

#### Example Jac Usage:
```jac
walker transribe_array {
    can stt.transcribe, stt.audio_to_array;
    audio_array = stt.audio_to_array("test.mp3");
    report stt.transcribe("en", audio_array);
}

walker transribe_file {
    can stt.transcribe;
    report stt.transcribe("en", null, "test.mp3");
}

walker transribe_url {
    can stt.transcribe;
    report stt.transcribe("fr", null, null, "https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}
```

`stt.translate` to get the english translation of a audio sequence of different language. Following are the parameters of the action.
* `language` - Spoken Language in the Audio. Type: Type: `str` Default: `en`
* `array` - Audio Array (should be sampled at 16kHz). Type: `list[float]` (Optional)
* `audio_file` - Location to a Audio file. Type: `str` (Optional) - Works only in local mode
* `url` - Web URL to a Audio file. Type: `str` (Optional)

Return type of the action is `str`.

#### Example Jac Usage:
```jac
walker translate {
    can stt.translate;
    report stt.translate("fr", null, null, "https://www.audio-lingua.eu/IMG/mp3/les_sports.mp3");
}
```
### Text2Speech (`tts`)
Implementation of the `tts` module produces audio wavs from the input text sequence.

* `synthesize`: Synthesize audio wavs for the input text sequence and will return the list of amlitude values of the audio wav. provide an option to save the audio wav in a prefered file location if the correct file path is passed as a parameter.
  * Input
    * `text` : (String) Input text sequence. This input text sequence will undergo with text preprocessing steps, such as expanding abrivations, converting numbers into ordinal format and removing unnessary white spaces.
    * `base64_val`: (Boolean). Set this to true if you need the return value in base64.
    * `path` : (String) Set the path correctly if you need to save the audio in a prefered location. ignore if you don't wanna save.
    * `rate` : The bitrate of the audio. This is not mandotory field.
  * Return
    * Dictionary
* `save_audio` : This action will save the audio amplitude as a wav file in a prefered location.
  * Input
    * `audio_data`: (List) a list of amplitude(float) values
    * `path` : (String) The location path to save the audio.
    * `rate`: (Int) The audio bitrate.
  * Return
    * Dictionary
* `load_seq2seqmodel` : This action will load the sequence to sequence model given in the input.
  * Input
    * `model_name` : String, model name. possible names {`tacotron2_v1`, `tacotron2_v2`}
    * `force_reload` : Boolean.
  * Return
    * String, status and of name of the loaded model.
* `load_vocorder` : This action will load the vocorder model given in the input.
  * Input
    * `model_name` : String, model name. possible names {`waveglow`, `hifigan`}
    * `force_reload` : Boolean.
  * Return
    * String, status and of name of the loaded model.

#### Example Jac Usage:

```
walker init{
    has text_input = "Hello world!, This is a test run";
    can tts.synthesize;
    can tts.save_audio;
    can tts.load_seq2seqmodel;
    can tts.load_vocorder;

    has seq2seq = tts.load_seq2seqmodel("tacotron2_v1");
    has vocorder = tts.load_vocorder("hifigan");

    has result = tts.synthesize(text = text_input);
    report tts.save_audio(result.audio_wave , "./");
}
```

## Text Processing
###
### Text Generation (`gpt2`)
Module `gp2` uses the OpenAI's `GPT-2-medium` to perform text genreation on a given text.

The `gpt2.generate` action allows you to generate text based on the input text you provide.

Inputs:
- text: input text, either a string or a list of strings
- max_length: maximum length of the generated text (default: 30)
- min_length: minimum length of the generated text (default: 10)
- num_return_sequences: number of sequences to return (default: 3)

Output: a list of generated text sequences

The `gtp2.get_embeddings` action allows you to get the embeddings for the input text.

Inputs:
- text: input text, either a string or a list of strings

Output: a list of embeddings for the input text

#### Example Jac Usage:
Given a text or a list of texts, it will return the generated text.

walker test_generate {
    can gpt2.generate;
    report gpt2.generate(text= "Hello, my name is", num_return_sequences= 5);
}

Given a text or a list of texts, it will return the embeddings of the text.

walker test_get_embeddings {
    can gpt2.get_embeddings;
    report gpt2.get_embeddings(text= ["Hello, my name is GPT2", "GPT2 is an Text-to-Text Generation Model" ]);
}


### Text Translation (`translator`)
Module `translator` uses the `mbart-large-50-many-to-many` to perform multilingual translation. It can translate from 50 languages to 50 languages.

Following are the parameters for the action `translator.translate`:
* `text` - Text to be translated. Type: `Union[List[str], str]`
* `src_lang` - Source language of the text. Type: `str`
* `tgt_lang` - Target language of the text. Type: `str`

Return type of the action is `List[str]`.

#### Example Jac Usage:
Example JAC Code to translate text from Hindi to English:
```jac
walker test_translate_hindi_eng {
    can translator.translate;
    report translator.translate("नमस्ते, आप कैसे हैं?", "hi_IN", "en_XX"); # Returns ["Hello, how are you?"]
}
```
Example JAC Code to translate text from English to German:
```jac
walker test_translate_eng_german {
    can translator.translate;
    report translator.translate("Hello, how are you?", "en_XX", "de_DE"); # Returns ["Hallo, wie geht es dir?"]
}
```

### Text Cluster (`cluster`)

Module `cluster` implemented for clustering text document into similar clusters. This is a example program to cluster documents with jaseci `cluster` module. We will use input as list of raw text documents and will produce cluster labels for each text documents.

* `get_umap`: Redusing the dimention of data while preseving the relationship beween data points to identify clusters easier.
    * Input
        * `text_embeddings` (list): list of text embeddings should pass here.
        * `n_neighbors` (int): number of neighbors to consider.
        * `min_dist` (float): minimum distance between clusters.
        * `n_components` (int): the dimensionality of the reduced data.
        * `random_state`(int): preproducability of the algorithm.

    * Returns: multidimentional array of reduced features.

* `get_cluster_labels`: To get list of possible cluster labels
    * Input
        * `embeddings`(list): This accept list of embedded text features.
        * `algorithm` (String): Algorithm for clustering.
        * `min_samples` (int): The minimum number of data points in a cluster is represented here. Increasing this will reduces number of clusters
        * `min_cluster_size` (int): This represents how conservative you want your clustering should be. Larger values more data points will be considered as noise

    * Returns: list of labels.
* **Input data file `text_cluster.json`**
  ```json
  [
    "still waiting card",
    "countries supporting",
    "card still arrived weeks",
    "countries accounts suppor",
    "provide support countries",
    "waiting week card still coming",
    "track card process delivery",
    "countries getting support",
    "know get card lost",
    "send new card",
    "still received new card",
    "info card delivery",
    "new card still come",
    "way track delivery card",
    "countries currently support"]
    ```

* #### Example Jac Usage:

```
walker text_cluster_example{
    can file.load_json;
    can use.encode;
    can cluster.get_umap;
    can cluster.get_cluster_labels;

    has text, encode, final_features, labels;

    text = file.load_json("text_cluster.json");
    encode = use.encode(text);
    final_features = cluster.get_umap(encode,2);

    labels = cluster.get_cluster_labels(final_features,"hbdscan",2,2);
    std.out(labels);

}
```


## Non-AI Tools
### PDF Extractor (`pdf_ext`)
`pdf_ext` module implemented for the Topical Change Detection in Documents via Embeddings of Long Sequences.
* `extract_pdf`: gets different topics in the context provided, given a threshold
    * Input
        * `url`(String): gets the pdf from URL
        * `path`(Float): gets the pdf from local path
        * `metadata`(Bool): to display available metadata of PDF
    * Returns: a json with number of pages the pdf had and content

#### Example Jac Usage:
```jac
walker pdf_ext_example {
    has url = "http://www.africau.edu/images/default/sample.pdf";
    has metadata = true;
    can pdf_ext.extract_pdf;

    # Getting the dat from PDF
    resp_data = pdf_ext.extract_pdf(url=url,
    metadata=metadata);
    std.out(resp_data);
}
```

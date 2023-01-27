# Jaseci NLP Package `(jac_nlp)`
The `jac_nlp` package contains a collection of state-of-the-art NLP models that can be used to perform various nlp tasks such as named entity recongnition, text summerization, embedding generation, topic extraction etc. following is a list of all the models available in the `jac_nlp` package.

## Installation
Each module can be installed individually or all at once. To install all modules at once.
```bash
pip install jac_nlp[all] # Installs all the modules present in the jac_nlp package
pip install jac_nlp[use_enc] # Installs the use_enc module present in the jac_nlp package
pip install jac_nlp[use_qa,ent_ext] # Installs the use_qa and ent_ext modules present in the jac_nlp package
```

## List of Models


| Module      | Model Type       |Model Name       | Docs                             | Type                    | Status       | Description                                                 | Resources                                 |
| ----------- | ---------------- | ---------------- | ----------------------------------- | ----------------------- | ------------ | ----------------------------------------------------------- | ----------------------------------------- |
| `use_enc`   | Text Encoder      |USE Encoder      | [Link](jac_nlp/use_enc/README.md)        | Zero-shot               | Ready        | Sentence-level embedding pre-trained on general text corpus | [Paper](https://arxiv.org/abs/1803.11175) |
| `use_qa`    | Text Encoder      |USE QA           | [Link](jac_nlp/use_qa/README.md)              | Zero-shot               | Ready        | Sentence-level embedding pre-trained on Q&A data corpus     | [Paper](https://arxiv.org/abs/1803.11175) |
| `fast_enc`  | Text Encoder      |FastText         | [Link](jac_nlp/fast_enc/README.md)  | Training req.           | Ready        | FastText Text Classifier                                    | [Paper](https://arxiv.org/abs/1712.09405) |
| `bi_enc`    | Text Encoder      |Bi-encoder       | [Link](jac_nlp/bi_enc/README.md)          | Training req./Zero-shot | Ready        | Dual sentence-level encoders                                | [Paper](https://arxiv.org/abs/1803.11175) |
| `sbert_sim` | Text Encoder      |SBert Similarity | [Link](jac_nlp/sbert_sim/README.md) | Training req./Zero-shot | Ready        | SBert Encoders for Sentence Similarity                      | [Paper](https://arxiv.org/abs/1908.10084) |
| `ent_ext`/ `lstm_ner` | Named Entity Recognition      |Flair NER       | [Link](jac_nlp/ent_ext/README.md)                    | Training req.  | Ready        | Entity extraction using the FLAIR NER framework                   |                                                                                                         |
| `tfm_ner`             | Named Entity Recognition      |Transformer NER | [Link](jac_nlp/tfm_ner/README.md) | Training req.  | Ready        | Token classification on Transformer models, can be used for NER   | [Huggingface](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) |
| `cl_summer` | Summarization      |Summarizer | [Link](jac_nlp/cl_summer/README.md)         | No Training req. | Ready  | Extractive Summarization using Sumy                  | [Doc.](https://miso-belica.github.io/sumy/)                                                                       |
| `t5_sum`    | Summarization      |Summarizer | [Link](jac_nlp/t5_sum/README.md)      | No Training req. | Ready  | Abstractive Summarization using the T5 Model         | [Doc.](https://huggingface.co/docs/transformers/model_doc/t5), [Paper](https://arxiv.org/pdf/1910.10683.pdf)      |
| `bart_sum`  | Summarization      |Summarizer | [Link](jac_nlp/bart_sum/README.md) | No Training req. | Ready  | Abstractive Summarization using the Bart Large Model | [Huggingface](https://huggingface.co/transformers/model_doc/bart.html), [Paper](https://arxiv.org/abs/1910.13461) |
| `text_seg`   | Text Processing      |Text Segmenter   | [Link](jac_nlp/text_seg/README.md)     | No Training req. | Experimetal | Topical Change Detection in Documents             | [Huggingface](https://huggingface.co/dennlinger/roberta-cls-consec)                                                                                                                        |
| `topic_ext` | Text Analysis      |Topic Extraction | [Link](jac_nlp/topic_ext/README.md) | No Training req. | Experimetal | Indentifying most relevent topics for given set of documents |           |


## Usage

To load the `jac_nlp.use_enc` package into jaseci in local environment, run the following command in the jsctl console.
```bash
jsctl > actions load module jac_nlp.use_enc
```
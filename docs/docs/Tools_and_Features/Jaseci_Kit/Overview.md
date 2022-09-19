# Overview
Jaseci Kit is a collection of state-of-the-art machine learning models that are readily available to load into jaseci.

# Model Directory

## Encoders
| Module      | Model Name    | Example                            | Type                    | Status       | Description                                                 | Resources                                 |
| ----------- | ------------- | ---------------------------------- | ----------------------- | ------------ | ----------------------------------------------------------- | ----------------------------------------- |
| `use_enc`   | USE Encoder   | [Link](#use-encoder-use_enc)       | Zero-shot               | Ready        | Sentence-level embedding pre-trained on general text corpus | [Paper](https://arxiv.org/abs/1803.11175) |
| `use_qa`    | USE QA        | [Link](#use-qa-use_qa)             | Zero-shot               | Ready        | Sentence-level embedding pre-trained on Q&A data corpus     | [Paper](https://arxiv.org/abs/1803.11175) |
| `fast_enc`  | FastText      | [Link](#fasttext-encoder-fast_enc) | Training req.           | Ready        | FastText Text Classifier                                    | [Paper](https://arxiv.org/abs/1712.09405) |
| `bi_enc`    | Bi-encoder    | [Link](#bi-encoder-bi_enc)         | Training req./Zero-shot | Ready        | Dual sentence-level encoders                                | [Paper](https://arxiv.org/abs/1803.11175) |
| `poly_enc`  | Poly-encoder  |                                    | Training req./Zero-shot | Experimental | Poly Encoder                                                | [Paper](https://arxiv.org/abs/1905.01969) |
| `cross_enc` | Cross-encoder |                                    | Training req./Zero-shot | Experimental | Cross Encoder                                               | [Paper](https://arxiv.org/abs/1905.01969) |

## Entity
| Module                | Model Name      | Example                                               | Type           | Status       | Description                                                       | Resources                                                                                               |
| --------------------- | --------------- | ----------------------------------------------------- | -------------- | ------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ent_ext`/ `lstm_ner` | Flair NER       | [Link](#entity-extraction-ent_ext)                    | Training req.  | Ready        | Entity extraction using the FLAIR NER framework                   |                                                                                                         |
| `tfm_ner`             | Transformer NER | [Link](#entity-extraction-using-transformers-tfm_ner) | Training req.  | Ready        | Token classification on Transformer models, can be used for NER   | [Huggingface](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) |
| `lstm_ner`            | LSTM NER        |                                                       | Traininig req. | Experimental | Entity extraction/Slot filling via Long-short Term Memory Network |                                                                                                         |

## Summarization
| Module      | Model Name | Example                         | Type             | Status | Description                                  | Resources                                                                                                    |
| ----------- | ---------- | ------------------------------- | ---------------- | ------ | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `cl_summer` | Summarizer | [Link](#summarizer-clsummer)    | No Training req. | Ready  | Extractive Summarization using Sumy          | [Doc.](https://miso-belica.github.io/sumy/)                                                                  |
| `t5_sum`    | Summarizer | [Link](#t5-summarization-t5sum) | No Training req. | Ready  | Abstractive Summarization using the T5 Model | [Doc.](https://huggingface.co/docs/transformers/model_doc/t5), [Paper](https://arxiv.org/pdf/1910.10683.pdf) |


## Text Processing
| Module     | Model Name     | Example                          | Type             | Status      | Description                           | Resources                                                           |
| ---------- | -------------- | -------------------------------- | ---------------- | ----------- | ------------------------------------- | ------------------------------------------------------------------- |
| `text_seg` | Text Segmenter | [Link](#text-segmenter-text_seg) | No Training req. | Experimetal | Topical Change Detection in Documents | [Huggingface](https://huggingface.co/dennlinger/roberta-cls-consec) |


## Non-AI Tools
| Module    | Model Name    | Example                        | Status | Description                                | Resources                                        |
| --------- | ------------- | ------------------------------ | ------ | ------------------------------------------ | ------------------------------------------------ |
| `pdf_ext` | PDF Extractor | [Link](#pdf-extractor-pdf_ext) | Ready  | Extract content from a PDF file via PyPDF2 | [Doc.](https://pypdf2.readthedocs.io/en/latest/) |

## Install Jaseci Kit 

Run :


```
pip install jaseci-ai-kit --upgrade

```
Activate the Jaseci terminal by running:
```
jsctl
```
Jaseci default libraries can be seen by running :

```
actions list 
```

We can load additional models by running <strong>actions load module</strong> in the terminal followed by the name of the model we want to use.
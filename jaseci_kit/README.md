# Jaseci Kit
Jaseci Kit is a collection of state-of-the-art machine learning models and useful tools that may be used in your application development.

## Encoders
| Module      | Model Name    | Example                            | Type                    | Status       | Description                                                 | Resources                                 |
| ----------- | ------------- | ---------------------------------- | ----------------------- | ------------ | ----------------------------------------------------------- | ----------------------------------------- |
| `use_enc`   | USE Encoder   | [Link](modules/encoders/use_enc/README.md)       | Zero-shot               | Ready        | Sentence-level embedding pre-trained on general text corpus | [Paper](https://arxiv.org/abs/1803.11175) |
| `use_qa`    | USE QA        | [Link](modules/encoders/use_qa/README.md)             | Zero-shot               | Ready        | Sentence-level embedding pre-trained on Q&A data corpus     | [Paper](https://arxiv.org/abs/1803.11175) |
| `fast_enc`  | FastText      | [Link](modules/encoders/fast_enc/README.md) | Training req.           | Ready        | FastText Text Classifier                                    | [Paper](https://arxiv.org/abs/1712.09405) |
| `bi_enc`    | Bi-encoder    | [Link](modules/encoders/bi_enc/README.md)         | Training req./Zero-shot | Ready        | Dual sentence-level encoders                                | [Paper](https://arxiv.org/abs/1803.11175) |
| `poly_enc`  | Poly-encoder  |                                    | Training req./Zero-shot | Experimental | Poly Encoder                                                | [Paper](https://arxiv.org/abs/1905.01969) |
| `cross_enc` | Cross-encoder |                                    | Training req./Zero-shot | Experimental | Cross Encoder                                               | [Paper](https://arxiv.org/abs/1905.01969) |

## Entity 
| Module                | Model Name      | Example                                               | Type           | Status       | Description                                                       | Resources                                                                                               |
| --------------------- | --------------- | ----------------------------------------------------- | -------------- | ------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ent_ext`/ `lstm_ner` | Flair NER       | [Link](modules/entity_utils/flair_ner/README.md)                    | Training req.  | Ready        | Entity extraction using the FLAIR NER framework                   |                                                                                                         |
| `tfm_ner`             | Transformer NER | [Link](modules/entity_utils/tfm_ner/README.md) | Training req.  | Ready        | Token classification on Transformer models, can be used for NER   | [Huggingface](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) |
| `lstm_ner`            | LSTM NER        |                                                       | Traininig req. | Experimental | Entity extraction/Slot filling via Long-short Term Memory Network |                                                                                                         |

## Summarization
| Module      | Model Name | Example                         | Type             | Status | Description                                  | Resources                                                                                                    |
| ----------- | ---------- | ------------------------------- | ---------------- | ------ | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `cl_summer` | Summarizer | [Link](modules/summarization/cl_summer/README.md)    | No Training req. | Ready  | Extractive Summarization using Sumy          | [Doc.](https://miso-belica.github.io/sumy/)                                                                  |
| `t5_sum`    | Summarizer | [Link](modules/summarization/t5_sum/README.md) | No Training req. | Ready  | Abstractive Summarization using the T5 Model | [Doc.](https://huggingface.co/docs/transformers/model_doc/t5), [Paper](https://arxiv.org/pdf/1910.10683.pdf) |


## Text Processing
| Module     | Model Name     | Example                          | Type             | Status      | Description                           | Resources                                                           |
| ---------- | -------------- | -------------------------------- | ---------------- | ----------- | ------------------------------------- | ------------------------------------------------------------------- |
| `text_seg` | Text Segmenter | [Link](modules/text_processing/text_seg/README.md) | No Training req. | Experimetal | Topical Change Detection in Documents | [Huggingface](https://huggingface.co/dennlinger/roberta-cls-consec) |


## Object Detection
| Module     | Model Name     | Example                          | Type             | Status      | Description                           | Resources                                                           |
| ---------- | -------------- | -------------------------------- | ---------------- | ----------- | ------------------------------------- | ------------------------------------------------------------------- |
| `yolo_v5` | Object Recognition | [Link](modules/object_detection/yolo_v5/README.md) | Training req. | Ready | 'You only look once', is an object detection algorithm that divides images into a grid system | [Documentation](https://docs.ultralytics.com/) |


## Non-AI Tools
| Module    | Model Name    | Example                        | Status | Description                                | Resources                                        |
| --------- | ------------- | ------------------------------ | ------ | ------------------------------------------ | ------------------------------------------------ |
| `pdf_ext` | PDF Extractor | [Link](modules/non_ai/pdf_ext/README.md) | Ready  | Extract content from a PDF file via PyPDF2 | [Doc.](https://pypdf2.readthedocs.io/en/latest/) |


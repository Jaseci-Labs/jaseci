---
sidebar_position: 2
---

# Jaseci Kit


Jaseci Kit is a collection of state-of-the-art machine learning models that are readily available to load into jaseci.

## Model Directory
## Encoders
| Module      | Model Name    | Example                     | Type                    | Status       | Description                                                 | Resources                                 |
| ----------- | ------------- | --------------------------- | ----------------------- | ------------ | ----------------------------------------------------------- | ----------------------------------------- |
| `use_enc`   | USE Encoder   | [Link](#use-encoder-useenc) | Zero-shot               | Ready        | Sentence-level embedding pre-trained on general text corpus | [Paper](https://arxiv.org/abs/1803.11175) |
| `use_qa`    | USE QA        | [Link](#5-useqa)            | Zero-shot               | Ready        | Sentence-level embedding pre-trained on Q&A data corpus     | [Paper](https://arxiv.org/abs/1803.11175) |
| `fast_enc`  | FastText      | [Link](#4-fasttext)         | Training req.           | Ready        | FastText Text Classifier                                    | [Paper](https://arxiv.org/abs/1712.09405) |
| `bi_enc`    | Bi-encoder    | [Link](#1-encoders)         | Training req./Zero-shot | Ready        | Dual sentence-level encoders                                | [Paper](https://arxiv.org/abs/1803.11175) |
| `poly_enc`  | Poly-encoder  |                             | Training req./Zero-shot | Experimental | Poly Encoder                                                | [Paper](https://arxiv.org/abs/1905.01969) |
| `cross_enc` | Cross-encoder |                             | Training req./Zero-shot | Experimental | Cross Encoder                                               | [Paper](https://arxiv.org/abs/1905.01969) |

## Entity
| Module     | Model Name      | Example                      | Type           | Status       | Description                                                       | Resources                                                                                               |
| ---------- | --------------- | ---------------------------- | -------------- | ------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ent_ext`  | Flair NER       | [Link](#2-entity-extraction) | Training req.  | Ready        | Entity extraction using the FLAIR NER framework                   |                                                                                                         |
| `tfm_ner`  | Transformer NER |                              | Training req.  | Ready        | Token classification on Transformer models, can be used for NER   | [Huggingface](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) |
| `lstm_ner` | LSTM NER        |                              | Traininig req. | Experimental | Entity extraction/Slot filling via Long-short Term Memory Network |                                                                                                         |

## Summarization
| Module      | Model Name | Example | Type             | Status | Description                         | Resources                                   |
| ----------- | ---------- | ------- | ---------------- | ------ | ----------------------------------- | ------------------------------------------- |
| `cl_summer` | Summarizer |         | No Training req. | Ready  | Extractive Summarization using Sumy | [Doc.](https://miso-belica.github.io/sumy/) |

## Non-AI Tools
| Module    | Model Name    | Example | Status | Description                                | Resources                                        |
| --------- | ------------- | ------- | ------ | ------------------------------------------ | ------------------------------------------------ |
| `pdf_ext` | PDF Extractor |         | Ready  | Extract content from a PDF file via PyPDF2 | [Doc.](https://pypdf2.readthedocs.io/en/latest/) |



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

## Using QA model

use_qa module uses the universal sentence encoder and distance metric to evaluate the distance between question and and probable answers.
To load the Question and Answer Model run in the jsctl terminal :



To load the Question and Answer Module run :

```
actions load module jaseci_ai_kit.use_qa
```
Running ``` actions list ```  will show the new modules loaded.

Lets test the Module out by copying and pasting the following code .

```jac
walker init {
        # when using external libraries we use the (can) keyword to load them in to the program.
        can use.enc_question , use.enc_answer;


        answers = ['I am 20 years old' , 'My dog is hungry','My TV is broken'];
        question = "If i wanted to fix something what should i fix ?";


        q_enc = use.enc_question(question);
        a_enc  = use.enc_answer(answers); # can take list or single strings

        a_scores = [];

        for i in a_enc:

            a_scores.l::append(vector.cosine_sim(q_enc,i));

            report a_scores;


}

```

The above code takes in a list of answers and a question and then returns a report with the probability of each answer. The probability represents how likely each answer is to answer the question. The higher the probability the more likely it is to answer the question.

To run the code  :


```jac

jac run main.jac

```





## Using the Encode Model

`use_enc` module uses the universal sentence encoder to generate sentence level embeddings.
The sentence level embeddings can then be used to calculate the similarity between two given text via cosine similarity and/or dot product.


```
actions load module jaseci_ai_kit.use_enc
```
Running ``` actions list ```  will show the new modules loaded.

Lets test the Module out by copying and pasting the following code .

```jac
walker use_enc_example {
    can use.encode, use.cos_sim_score;
    has text = "What is the weather tomorrow?";
    has candidates = [
        "weather forecast",
        "ask for direction",
        "order food"
    ];
    text_emb = use.encode(text)[0];
    cand_embs = use.encode(candidates); # use.encode handles string/list

    max_score = 0;
    max_cand = 0;
    cand_idx = 0;
    for cand_emb in cand_embs {
        cos_score = use.cos_sim_score()
        if (cos_score > max_score) {
            max_score = cos_score
            max_cand = cand_idx;
        }
        cand_idx += 1;
    }

    predicted_cand = candidates[max_cand];
}
```

The above code takes in a list of answers and a question and then returns a report with the probability of each answer. The probability represents how likely each answer is to answer the question. The higher the probability the more likely it is to answer the question.


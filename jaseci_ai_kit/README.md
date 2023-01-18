# Jaseci AI Kit
Jaseci AI Kit is a collection of state-of-the-art machine learning models from different domains (NLP, Computer Vision, Speech etc.) that are readily available to load into jaseci. Jaseci AI Kit consist of 4 Main Python Packages
- `jac_nlp` - Natural Language Processing
- `jac_vision` - Computer Vision
- `jac_speech` - Speech
- `jac_misc` - Miscellaneous

## Installation
Each module can be installed individually or all at once. To install all modules at once.
```bash
pip install jac_nlp[all] #Installs all the modules present in the jac_nlp package
pip install jac_misc[translator] #Installs the translator module present in the jac_misc package
pip install jac_speech[stt, tts] #Installs the stt and tts modules present in the jac_speech package
```

# Jaseci NLP Package `(jac_nlp)`
The `jac_nlp` package contains a collection of state-of-the-art NLP models that can be used to perform various nlp tasks such as named entity recongnition, text summerization, embedding generation, topic extraction etc. following is a list of all the models available in the `jac_nlp` package.


| Module      | Model Type       |Model Name       | Example                             | Type                    | Status       | Description                                                 | Resources                                 |
| ----------- | ---------------- | ---------------- | ----------------------------------- | ----------------------- | ------------ | ----------------------------------------------------------- | ----------------------------------------- |
| `use_enc`   | Text Encoder      |USE Encoder      | [Link](#use-encoder-use_enc)        | Zero-shot               | Ready        | Sentence-level embedding pre-trained on general text corpus | [Paper](https://arxiv.org/abs/1803.11175) |
| `use_qa`    | Text Encoder      |USE QA           | [Link](#use-qa-use_qa)              | Zero-shot               | Ready        | Sentence-level embedding pre-trained on Q&A data corpus     | [Paper](https://arxiv.org/abs/1803.11175) |
| `fast_enc`  | Text Encoder      |FastText         | [Link](#fasttext-encoder-fast_enc)  | Training req.           | Ready        | FastText Text Classifier                                    | [Paper](https://arxiv.org/abs/1712.09405) |
| `bi_enc`    | Text Encoder      |Bi-encoder       | [Link](#bi-encoder-bi_enc)          | Training req./Zero-shot | Ready        | Dual sentence-level encoders                                | [Paper](https://arxiv.org/abs/1803.11175) |
| `sbert_sim` | Text Encoder      |SBert Similarity | [Link](#sbert-similarity-sbert_sim) | Training req./Zero-shot | Ready        | SBert Encoders for Sentence Similarity                      | [Paper](https://arxiv.org/abs/1908.10084) |
| `ent_ext`/ `lstm_ner` | Named Entity Recognition      |Flair NER       | [Link](#entity-extraction-ent_ext)                    | Training req.  | Ready        | Entity extraction using the FLAIR NER framework                   |                                                                                                         |
| `tfm_ner`             | Named Entity Recognition      |Transformer NER | [Link](#entity-extraction-using-transformers-tfm_ner) | Training req.  | Ready        | Token classification on Transformer models, can be used for NER   | [Huggingface](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) |
| `cl_summer` | Summarization      |Summarizer | [Link](#summarizer-clsummer)         | No Training req. | Ready  | Extractive Summarization using Sumy                  | [Doc.](https://miso-belica.github.io/sumy/)                                                                       |
| `t5_sum`    | Summarization      |Summarizer | [Link](#t5-summarization-t5sum)      | No Training req. | Ready  | Abstractive Summarization using the T5 Model         | [Doc.](https://huggingface.co/docs/transformers/model_doc/t5), [Paper](https://arxiv.org/pdf/1910.10683.pdf)      |
| `bart_sum`  | Summarization      |Summarizer | [Link](#bart-summarization-bart_sum) | No Training req. | Ready  | Abstractive Summarization using the Bart Large Model | [Huggingface](https://huggingface.co/transformers/model_doc/bart.html), [Paper](https://arxiv.org/abs/1910.13461) |
| `text_seg`   | Text Processing      |Text Segmenter   | [Link](#text-segmenter-text_seg)     | No Training req. | Experimetal | Topical Change Detection in Documents             | [Huggingface](https://huggingface.co/dennlinger/roberta-cls-consec)                                                                                                                        |
| `topic_ext` | Text Analysis      |Topic Extraction | [Link](#topic-extraction-topic_ext) | No Training req. | Experimetal | Indentifying most relevent topics for given set of documents |           |



To load the `jac_nlp.use_enc` package into jaseci in local environment, run the following command in the jsctl console.
```bash
jsctl > actions load module jac_nlp.use_enc
```
# Jaseci Vision Package `(jac_vision)`
The `jac_vision` package contains a collection of state-of-the-art Computer Vision models that can be used to perform various computer vision tasks such as image classification, object detection, image segmentation etc. following is a list of all the models available in the `jac_vision` package.

# Jaseci Speech Package `(jac_speech)`
The `jac_speech` package contains a collection of state-of-the-art Speech models that can be used to perform various speech tasks such as speech to text, text to speech etc. following is a list of all the models available in the `jac_speech` package.

| Module      | Model Type       | Model Name       | Example                             | Type                    | Status       | Description                                                 | Resources                                 |
| ----------- | ---------------- |---------------- | ----------------------------------- | ----------------------- | ------------ | ----------------------------------------------------------- | ----------------------------------------- |
| `stt`  | Speech to Text | Whisper |  [Link](#speech2text-stt) | No Training req. | Ready  | transcription or translation of a give audio sequence. | [Robust Speech Recognition via Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf), [OpenAI Whisper](https://openai.com/blog/whisper/)                                                                                                               |
| `tts`  | Text to Speech | Tacotron | [Link](#)                | No Training req. | Ready  | List of Amplitudes of the synthesized audio wav.       | [Tacotron2](https://arxiv.org/abs/1712.05884), [Waveglow](https://arxiv.org/abs/1811.00002), [Hifigan](https://arxiv.org/abs/2010.05646), [Nvidia Tacotron2 implementation](https://github.com/NVIDIA/tacotron2), [SpeechBrain](https://speechbrain.github.io/index.html) |

To load the `jac_speech.stt` package into jaseci in local environment, run the following command in the jsctl console.
```bash
jsctl > actions load module jac_speech.stt
```

# Jaseci Misc Package `(jac_misc)`
The `jac_misc` package contains a collection of miscellaneous models that can be used to perform various tasks such as translation, pdf extraction, personalized head etc. following is a list of all the models available in the `jac_misc` package.

| Module      | Model Name       | Example                             | Type                    | Status       | Description                                                 | Resources                                 |
| ----------- | ---------------- | ----------------------------------- | ----------------------- | ------------ | ----------------------------------------------------------- | ----------------------------------------- |
| `translator` | Text Translation | [Link](#text-translation-translator) | No Training req. | Ready       | Text Translation for 50 languages to 50 languages | [Multilingual Denoising Pre-training for Neural Machine Translation](https://arxiv.org/abs/2001.08210), [Huggingface MBart Docs](https://huggingface.co/transformers/model_doc/mbart.html) |
| `cluster` | Text Cluster | [Link](#text-cluster-cluster) | No Training req. | Experimetal | Indentifying Posible Similar Clusters in Set of Documents | [UMAP](https://umap-learn.readthedocs.io/en/latest/) , [HBDSCAN](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html) |
| `pdf_ext` | PDF Extractor | [Link](#pdf-extractor-pdf_ext) | No Training req.| Ready  | Extract content from a PDF file via PyPDF2 | [Doc.](https://pypdf2.readthedocs.io/en/latest/) |

To load the `jac_misc.translator` package into jaseci in local environment, run the following command in the jsctl console.
```bash
jsctl > actions load module jac_misc.translator
```

# Examples

## Encoders

###  USE Encoder (`use_enc`)
`use_enc` module uses the universal sentence encoder to generate sentence level embeddings.
The sentence level embeddings can then be used to calculate the similarity between two given text via cosine similarity and/or dot product.

* `encode`: encodes the text and returns a embedding of 512 length
    * Alternate name: `get_embedding`
    * Input:
        * `text` (string or list of strings): text to be encoded
    * Return: Encoded embeddings
* `cos_sim_score`:
    * Input:
        * `q_emb` (string or list of strings): first text to be embeded
        * `a_emb` (string or list of strings): second text to be embedded
    * Return: cosine similarity score
* `text_simliarity`: calculate the simlarity score between given texts
    * Input:
        * `text1` (string): first text
        * `text2` (string): second text
    * Return: cosine similarity score
* `text_classify`: use USE encoder as a classifier
    * Input:
        * `text` (string): text to classify
        * `classes` (list of strings): candidate classification classes

#### Example Jac Usage:
```jac
# Use USE encoder for zero-shot intent classification
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
        cos_score = use.cos_sim_score(cand_emb, text_emb);
        if (cos_score > max_score) {
            max_score = cos_score;
            max_cand = cand_idx;
        }
        cand_idx += 1;
    }

    predicted_cand = candidates[max_cand];
}
```

###  USE QA (`use_qa`)
`use_qa` module uses the multilingual-qa to generate sentence level embeddings.
The sentence level embeddings can then be used to calculate best match between question and available answers via cosine similarity and/or dist_score.

* `question_encode`: encodes question and returns a embedding of 512 length
    * Alternate name: `enc_question`
    * Input:
        * `text` (string or list of strings): question to be encoded
    * Return: Encoded embeddings
* `answer_encode`: encodes answers and returns a embedding of 512 length
    * Alternate name: `enc_answer`
    * Input:
        * `text` (string or list of strings): question to be encoded
        * `context` (string or list of strings): usually the text around the answer text, for example it could be 2 sentences before plus 2 sentences after.
    * Return: Encoded embeddings
* `cos_sim_score`:
    * Input:
        * `q_emb` (string or list of strings): first embeded text
        * `a_emb` (string or list of strings): second embeded text
    * Return: cosine similarity score

* `dist_score`:
    * Input:
        * `q_emb` (string or list of strings): first embeded text
        * `a_emb` (string or list of strings): second embeded text
    * Return: inner product score
* `question_similarity`: calculate the simlarity score between given questions
    * Input:
        * `text1` (string): first text
        * `text2` (string): second text
    * Return: cosine similarity score
* `question_classify`: use USE QA as question classifier
    * Input:
        * `text` (string): text to classify
        * `classes` (list of strings): candidate classification classes
* `answer_similarity`: calculate the simlarity score between given answer
    * Input:
        * `text1` (string): first text
        * `text2` (string): second text
    * Return: cosine similarity score
* `answer_classify`: use USE encoder as answer classifier
    * Input:
        * `text` (string): text to classify
        * `classes` (list of strings): candidate classification classes
* `qa_similarity`: calculate the simlarity score between question and answer
    * Input:
        * `text1` (string): first text
        * `text2` (string): second text
    * Return: cosine similarity score
* `qa_classify`: use USE encoder as a QA classifier
    * Input:
        * `text` (string): text to classify
        * `classes` (list of strings): candidate classification classes
    * Returns:
#### Example Jac Usage:
```jac
# Use USE_QA model for zero-shot text classification
walker use_qa_example {
    can use.qa_similarity;
    has questions = "What is your age?";
    has responses = ["I am 20 years old.", "good morning"];
    has response_contexts = ["I will be 21 next year.", "great day."];

    max_score = 0;
    max_cand = 0;
    cand_idx = 0;
    for response in responses {
        cos_score = use.qa_similarity(text1=questions,text2=response);
        std.out(cos_score);
        if (cos_score > max_score) {
            max_score = cos_score;
            max_cand = cand_idx;
        }
        cand_idx += 1;
    }

    predicted_cand = responses[max_cand];
}
```

###  BI-Encoder (`bi_enc`)
`bi_enc`  module can be used for intent classification, it takes contexts and candidates, to predict the best suitable candidate for each context. You can train the module on custom data to behave accordingly.

* `dot_prod`:
    * Input:
        * `vec_a` (list of float): first embeded text
        * `vec_b` (list of float): second embeded text
    * Return: dot product score
* `cos_sim_score`:
    * Input:
        * `vec_a` (list of float): first embeded text
        * `vec_b` (list of float): second embeded text
    * Return: cosine similarity score
* `infer`: predits the most suitable candidate for a provided context, takes text or embedding
    * Input:
        * `contexts` (string or list of strings): context which needs to be classified
        * `candidates` (string or list of strings): list of candidates for the context
        * `context_type` (string): can be text or embedding type
        * `candidate_type` (string): can be text or embedding type
    * Return: a dictionary of similarity score for each candidate and context
* `train`: used to train the Bi-Encoder for custom input
    * Input:
        * `dataset` (Dict): dictionary of candidates and suportting contexts for each candidate
        * `from_scratch` (bool): if set to true train the model from scratch otherwise trains incrementally
        * `training_parameters` (Dict): dictionary of training parameters
    * Returns: text when model training is completed
* `get_context_emb`:
    * Alternate name: `encode_context`
    * Input:
        * `contexts` (string or list of strings): context which needs to be encoded
    * Returns a list of embedding of 128 length for tiny bert
* `get_candidate_emb`:
    * Alternate name: `encode_candidate`
    * Input:
        * `candidates` (string or list of strings): candidates which needs to be encoded
    * Returns: list of embedding of 128 length for tiny bert
* `get_train_config`:
    * Input: None
    * Returns: json of all the current training configuration
     ```
     {
        "max_contexts_length": 128,
        "max_candidate_length": 64,
        "train_batch_size": 8,
        "eval_batch_size": 2,
        "max_history": 4,
        "learning_rate": 0.001,
        "weight_decay": 0.01,
        "warmup_steps": 100,
        "adam_epsilon": 1e-06,
        "max_grad_norm": 1,
        "num_train_epochs": 10,
        "gradient_accumulation_steps": 1,
        "fp16": false,
        "fp16_opt_level": "O1",
        "gpu": 0,
        "basepath": "logoutput",
        "seed": 12345,
        "device": "cuda"
    }
    ```
* `set_train_config`:
    * Input
        * `train_parameters` (Dict): dictionary of training parameters. See the json example above under `get_train_config` for the list of available training parameters.
    * Returns: "Config setup is complete." if train configuration is completed successfully
* `get_model_config`:
    * Input: None
    * Returns: json of all the current model configuration
    ```
    {
        "shared": false,
        "model_name": "prajjwal1/bert-tiny",
        "model_save_path": "modeloutput",
        "loss_function": "mse",
        "loss_type": "dot"
    }
    ```
* `set_model_config`:
    * Input
        * `model_parameters`(Dict): dictionary of model parameters. See the json example above under `get_model_config` for the list of available training parameters.
    * Returns: "Config setup is complete." if model configuration is completed successfully
* `save_model`:
    * Input
        * `model_path` (string): the path to save model
    * Returns: "[Saved model at] : <model_path>" if model successfully saved
* `load_model`:
    * Input
        * `model_path` (string): the path to save model
    * Returns: "[loaded model from] : <model_path>" if model successfully loaded


#### Example Jac Usage:
```jac
# Train an bi-encoder model for intent classification
walker bi_enc_example{
    has train_file = "train_bi.json";
    has from_scratch = true;
    has num_train_epochs = 20;
    has contexts= ["Share my location with Hillary's sister"];
    has candidates=[
        "searchplace",
        "getplacedetails",
        "bookrestaurant",
        "gettrafficinformation",
        "compareplaces",
        "sharecurrentlocation",
        "requestride",
        "getdirections",
        "shareeta",
        "getweather"
    ];

    can bi_enc.train,bi_enc.infer;

    train_data = file.load_json(train_file);

    # Train the model
    bi_enc.train(
        dataset=train_data,
        from_scratch=from_scratch,
        training_parameters={
            "num_train_epochs": num_train_epochs
        }
    );

    # Use the model to perform inference
    # returns the list of context with the suitable candidates
    resp_data = bi_enc.infer(
        contexts=contexts,
        candidates=candidates,
        context_type="text",
        candidate_type="text"
    );

    # Iterate through the candidate labels and their predicted scores
    max_score = 0;
    max_intent = "";
    pred=resp_data[0];
    for j=0 to j<pred["candidate"].length by j+=1 {
        if (pred["score"][j] > max_score){
            max_intent = pred["candidate"][j];
            max_score = pred["score"][j];
        }
    }
    std.out("predicted intent : ",max_intent ," Conf_Score:", max_score);
}
```

###  Sbert Similarity (`sbert_sim`)
`sbert_sim` is a implementation of SentenceBert for scoring similarity between sentence pairs, it uses bi-encoder in a saimese setup to encode the sentences followed by the cosine similarity to score the similarity.

* `get_dot_score` : Caculate the dot product of two given vectors
    * Input:
        * `vec_a` (list of float): first embeded text
        * `vec_b` (list of float): second embeded text
    * Return: dot product score
* `get_cos_score` : Caculate the cosine similarity score of two given vectors
    * Input:
        * `vec_a` (list of float): first embeded text
        * `vec_b` (list of float): second embeded text
    * Return: cosine similarity score
* `get_text_sim`: gets the similarity score between `query` with all the sentences in `corpus` and return the top_k similar sentences with `sim_score`
    * Input:
        * `query` (string or list of strings): context which needs to be classified
        * `corpus` (string or list of strings): list of candidates for the context
        * `top_k` (string): can be text or embedding type
    * Return: list of top_k similar sentences with `sim_score`
* `train`: used to train the Bi-Encoder for custom input
    * Input:
        * `dataset` (List): List of List, each list contains a pair of sentence and similarity score.
        * `training_parameters` (Dict): dictionary of training parameters
    * Returns: text when model training is completed
* `getembeddings`:
    * Input:
        * `texts` (string or list of strings): take text and returns a encoded embeddings
    * Returns a list of embeddings
* `get_train_config`:
    * Input: None
    * Returns: json of all the current training configuration
     ```
     {
        "device": "cpu",
        "num_epochs": 2,
        "model_save_path": "output/sent_model-2022-11-04_17-43-18",
        "model_name": "bert-base-uncased",
        "max_seq_length": 256
    }
    ```
* `load_model`:
    * Input
        * `model_type` (string): can be `default` or `tfm_model`
          * `default` : loads model from the [sbert](https://www.sbert.net/docs/pretrained_models.html) model zoo
          * `tfm_model` : load tranformer model from the [huggingface hub](https://huggingface.co/models)
        * `model_name` (string): this is name of the model to be loaded
      *  ```
          {
          "model_name": "all-MiniLM-L12-v2",
          "model_type": "default"
          }
          ```

    * Returns: "[loaded model from] : <model_type> <model_name>" if model successfully loaded
      * ```
        [loaded model from] SBERT Hub : all-MiniLM-L12-v2
        ```

#### Example Jac Usage:
```jac
## Train and evalute a sbert model for senetence similarity
walker sbert_sim_example{
    has train_file = "train_sbert.json";
    has num_epochs = 2;
    has query= ["A girl is on a sandy beach."];
    has corpus=["A girl dancing on a sandy beach."];
    has top_k=1;

    can sbert_sim.train,sbert_sim.get_text_sim;

    train_data = file.load_json(train_file);

    # Train the model
    sbert_sim.train(
        dataset=train_data['train_data'],
        training_parameters={
            "num_epochs": num_epochs
        }
    );

    # returns the top_k of simlar test in the corpus
    resp_data = sbert_sim.get_text_sim(query=query,corpus=corpus,top_k=top_k);
    std.out(resp_data);
}
```


###  FastText Encoder (`fast_enc`)
`fast_enc` module uses the facebook's fasttext -- efficient learning of word representations and sentence classification.

* `train`: used to train the Bi-Encoder for custom input
    * Input:
        * `traindata` (Dict): dictionary of candidates and suportting contexts for each candidate
        * `train_with_existing` (bool): if set to true train the model from scratch otherwise trains incrementally
* `predict`: predits the most suitable candidate for a provided context, takes text or embedding
    * Input:
        * `sentences` (list of strings): list of sentences the needs to be classified
    * Return: a dictionary of sentence, predicted intent and probability
* `save_model`:
    * Input
        * `model_path` (string): the path to save model
    * Returns: "[Saved model at] : <model_path>" if model successfully saved
* `load_model`:
    * Input
        * `model_path` (string): the path to save model
    * Returns: "[loaded model from] : <model_path>" if model successfully loaded
#### Example Jac Usage:
```jac
# Train and inference with a fasttext classifier
walker fast_enc_example {
    has train_file = "fast_enc_train.json";
    has train_with_existing = false;
    has test_sentence=  ["what's going on ?"];
    can fast_enc.train,fast_enc.predict;

    # Training the model
    train_data = file.load_json(train_file);
    fast_enc.train(traindata=train_data,train_with_existing=false);

    # Getting inference from the model
    resp_data=fast_enc.predict(sentences=test_sentence);
    std.out(resp_data);
}
```

## Entity
###  Entity Extraction (`ent_ext`)
`ent_ext` module uses Flair named entity recognition architecture. Can either be used zero-shot or trained.

* `train`: used to train the Flair-based NER model
    * Input:
        * `train_data`: (List(Dict)): a list of dictionaries containing contexts and list of entities in each context.
        ```
        [
            {
                "context": "EU rejects German call to boycott British lamb",
                "entities": [
                    {
                        "entity_value": "EU",
                        "entity_type": "ORG",
                        "start_index": 0,
                        "end_index": 2
                    },
                    {
                        "entity_value": "German",
                        "entity_type": "MISC",
                        "start_index": 11,
                        "end_index": 17
                    },
                    {
                        "entity_value": "British",
                        "entity_type": "MISC",
                        "start_index": 34,
                        "end_index": 41
                    }
                ]
            }
        ]
        ```
        * `val_data`: (List(Dict)): a list of dictionaries containing contexts and list of entities in each context
        ```
        [
            {
                "context": "CRICKET LEICESTERSHIRE TAKE OVER AT TOP AFTER INNINGS VICTORY",
                "entities": [
                    {
                        "entity_value": "LEICESTERSHIRE",
                        "entity_type": "ORG",
                        "start_index": 8,
                        "end_index": 22
                    }
                ]
            }
        ]
        ```
        * `test_data`: (List(Dict)): a list of dictionaries containing contexts and list of entities in each context
        ```
        [
            {
                "context": "The former Soviet republic was playing in an Asian Cup finals tie for the first time",
                "entities": [
                    {
                        "entity_value": "Soviet",
                        "entity_type": "MISC",
                        "start_index": 11,
                        "end_index": 17
                    },
                    {
                        "entity_value": "Asian",
                        "entity_type": "MISC",
                        "start_index": 45,
                        "end_index": 50
                    },
                    {
                        "entity_value": "Asian",
                        "entity_type": "MISC",
                        "start_index": 45,
                        "end_index": 50
                    }
                ]
            }
        ]
        ```
        * `train_params`: (Dict): dictionary of training parameters to modify the training behaviour
        ```
        {
            "num_epoch": 20,
            "batch_size": 16,
            "LR": 0.01
        }
        ```
* `entity_detection`: detects all availabe entities from the provided context
    * Input:
        * `text` (string): context to detect entities.
        * `ner_labels`(list of strings): List of entities, e.g. ["LOC","PER"]
    * Return: a list of dictionary entities containing entity_text, entity_value, conf_score and index
* `save_model`:
    * Input
        * `model_path` (string): the path to save model
    * Returns: "[Saved model at] : <model_path>" if model successfully saved
* `load_model`:
    * Input
        * `model_path` (string): the path to save model
    * Returns: "[loaded model from] : <model_path>" if model successfully loaded
* `set_config`:
    * Input
        * `ner_model`: pretrained or basic model to be loaded, provide the exact name of the model, available options are:
            * `Pre-trained LSTM / GRU` : ["ner", "ner-fast","ner-large"]
            * `Huggingface model` : all available models that can be intialized with AutoModel
            * `None` : for load a RNN model from scratch
        * `model_type`: type of model to be loaded, available options are :
            * `TRFMODEL` : for huggingface models
            * `LSTM` or `GRU` : RNN models
    * Returns: "Config setup is complete." if model successfully loaded
#### Example Jac Usage:
```jac
# Train and inference with an entity extraction model
walker ent_ext_example {

    has train_file = "train_data.json";
    has val_file = "val_data.json";
    has test_file = "test_data.json";
    has from_scratch = true;
    has num_train_epochs = 20;
    has batch_size = 8;
    has learning_rate = 0.02;
    can ent_ext.entity_detection, ent_ext.train;
    train_data = file.load_json(train_file);
    val_data = file.load_json(val_file);
    test_data = file.load_json(test_file);

    # Training the model
    ent_ext.train(
        train_data = train_data,
        val_data = val_data,
        test_data = test_data,
        train_params = {
            "num_epoch": num_train_epochs,
            "batch_size": batch_size,
            "LR": learning_rate
            });

    # Getting inference from the model
    resp_data = ent_ext.entity_detection(text="book a flight from kolkata to delhi",ner_labels= ["LOC"]);
    std.out(resp_data);
}
```

###  Entity Extraction Using Transformers (`tfm_ner`)
`tfm_ner` module uses transformers to identify and extract entities. It uses TokenClassification method from Huggingface.

* `train`: used to train transformer NER model
    * Input:
        * `train_data`: (List(Dict)): a list dictionary containing contexts and list of entities in each context
        ```
        [
            {
                "context": "MINNETONKA , Minn .",
                "entities": [
                            {
                                "entity_value": "MINNETONKA",
                                "entity_type": "LOC",
                                "start_index": 0,
                                "end_index": 10
                            },
                            {
                                "entity_value": "Minn",
                                "entity_type": "LOC",
                                "start_index": 13,
                                "end_index": 17
                            }
                ]
            }
        ]
        ```
        * `mode`: (String): mode for training the model, available options are :
            * `default`: train the model from scratch
            * `incremental`: providing more training data for current set of entities
            * `append`: changing the number of entities (model is restarted and trained with all of traindata)
        * `epochs `: (int): Number of epoch you want model to train.
* `extract_entity`: detects all availabe entities from the provided context
    * Input:
        * `text` (string): context to detect entities.
    * Return: a list of dictionary entities containing entity_text, entity_value, conf_score and index
* `save_model`:
    * Input
        * `model_path` (string): the path to save model
    * Returns: "[Saved model at] : <model_path>" if model successfully saved
* `load_model`:
    * Input
        * `model_path` (string): the path to save model
    * Returns: "[loaded model from] : <model_path>" if model successfully loaded
* `get_train_config`:
    * Input: None
    * Returns: json of all the current training configuration
     ```
        {
            "MAX_LEN": 128,
            "TRAIN_BATCH_SIZE": 4,
            "VALID_BATCH_SIZE": 2,
            "EPOCHS": 50,
            "LEARNING_RATE": 2e-05,
            "MAX_GRAD_NORM": 10,
            "MODE": "default"
        }
    ```
* `set_train_config`:
    * Input
        * `train_parameters` (Dict): dictionary of training parameters. See the json example above for available configuration parameters.
    * Returns: "Config setup is complete." if train configuration is completed successfully
* `get_model_config`:
    * Input: None
    * Returns: json of all the current model configuration
    ```
        {
            "model_name": "prajjwal1/bert-tiny",
            "model_save_path": "modeloutput"
        }
    ```
* `set_model_config`:
    * Input
        * `model_parameters`(Dict): dictionary of model parameters. See the json example above for available configuration parameters.
    * Returns: "Config setup is complete." if model configuration is completed successfully

#### Example Jac Usage:
```jac
# Train and inference with a transformer-based NER model
walker tfm_ner_example {

    has train_file = "train_ner.json";
    has num_train_epochs = 10;
    has mode = "default";
    can tfm_ner.extract_entity, tfm_ner.train;
    train_data = file.load_json(train_file);

    # Training the model
    tfm_ner.train(
        mode = mode,
        epochs = num_train_epochs,
        train_data=train_data
    );

    # Infer using the model
    resp_data = tfm_ner.extract_entity(
        text="book a flight from kolkata to delhi,Can you explain to me,please,what Homeowners Warranty Program means,what it applies to,what is its purpose? Thank you. The Humboldt University of Berlin is situated in Berlin, Germany"
    );
    std.out(resp_data);
}
```
## Summarization
### Summarizer (`cl_summer`)
`cl_summer` uses the sumy summarizer to create extractive summary.

* `summarize`: to get the extractive summary in provided sentences count.
    * Input
        * `text`(String): text the contain the entire context
        * `url`(String): the link to the webpage
        * `sent_count`(int): number of sentence you want in the summary
        * `summarizer_type`(String): name of the summarizer type, available options are:
            * `LsaSummarizer`
            * `LexRankSummarizer`
            * `LuhnSummarizer`
    * Returns: List of Sentences that best summarizes the context
    * **Input text file `summarize.json`**
        ```
        {
            "text": "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and   rude. The King of England was at war with him and had led a great army into Scotland to drive him out of the land. Battle after battle had been fought. Six times Bruce had led his brave little army against his foes and six times his men had been beaten and driven into flight. At last his army was scattered, and he was forced to hide in the woods and in lonely places among the mountains. One rainy day, Bruce lay on the ground under a crude shed listening to the patter of the drops on the roof above him. He was tired and unhappy. He was ready to give up all hope. It seemed to him that there was no use for him to try to do anything more. As he lay thinking, he saw a spider over his head making ready to weave her web. He watched her as she toiled slowly and with great care. Six times she tried to throw her frail thread from one beam to another, and six times it fell short. 'Poor thing,' said Bruce: 'you, too, know what it is to fail.', But the spider did not lose hope with the sixth failure. With still more care, she made ready to try for the seventh time. Bruce almost forgot his own troubles as, he watched her swing herself out upon the slender line. Would she fail again? No! The thread was carried safely to the beam and fastened there."
        }
        ```
#### Example Jac Usage for given text blob:
```jac
# Use the summarizer to summarize a given text blob
walker cl_summer_example {
    has text_file = "summarize.json";
    has sent_count = 5;
    has summarizer_type = "LsaSummarizer";
    can cl_summer.summarize;

    # Getting Extractive summary from text
    train_data = file.load_json(text_file);
    resp_data = cl_summer.summarize(
        text=train_data.text,
        url="none",
        sent_count=sent_count,
        summarizer_type=summarizer_type
    );
    report resp_data;
}
```

#### Example Jac Usage for given URL
```jac
# Use the summarizer to summarize a given URL
walker cl_summer_example {
    has sent_count = 5;
    has summarizer_type = "LsaSummarizer";
    has url="https://in.mashable.com/";
    can cl_summer.summarize;

    # Getting Extractive summary from URL
    resp_data_url = cl_summer.summarize(
        text="none",
        url=url,
        sent_count=sent_count,
        summarizer_type=summarizer_type
    );
    report resp_data_url;
}
```

###  T5 Summarization (`t5_sum`)
`t5_sum` uses the T5 transformer model to perform abstractive summary on a body of text.

* `classify_text`: use the T5 model to summarize a body of text
    * **Input**:
        * `text` (string): text to summarize
        * `min_length` (integer): the least amount of words you want returned from the model
        * `max_length` (integer): the most amount of words you want returned from the model
    * **Input datafile**
    `**data.json**`
        ```
        {
            "text": "The US has passed the peak on new coronavirus cases, President Donald Trump said and predicted that some states would reopen this month. The US has over 637,000 confirmed Covid-19 cases and over 30,826 deaths, the highest for any country in the world. At the daily White House coronavirus briefing on Wednesday, Trump said new guidelines to reopen the country would be announced on Thursday after he speaks to governors. We'll be the comeback kids, all of us, he said. We want to get our country back. The Trump administration has  previously fixed May 1 as a possible date to reopen the world's largest economy, but the president said some states may be able to return to normalcy earlier than that.",
            "min_length": 30,
            "max_length": 100
        }
        ```

#### Example Jac Usage:
```jac
# Use the T5 model to summarize a given piece of text
walker summarization {
    can t5_sum.classify_text;
    has data = "data.json";
    data = file.load_json(data);
    summarized_text = t5_sum.classify_text(
        text = data["text"],
        min_length = data["min_length"],
        max_length = data["max_length"]
        );
    report summarized_text;
}
```

###  Bart Summarization (`bart_sum`)
`bart_sum` uses the BART transformer model to perform abstractive summary on a body of text.

There are 2 ways to use `bart_sum` module.
1. Given a text, it will return the summary of the text.
2. Given a web page url, it will return the summary of the web page.

Both the methods uses a single action `summarize` to get the summary. Following are the parameters of the function.
* `text` - Text to be summarized. Type: `Union[List[str], str]` (Optional)
* `url` - Url of the web page to be summarized. Type: `str` (Optional)
* `max_length` - Maximum character length of the summary. Type: `int` Default: `100`
* `min_length` - Minimum character length of the summary. Type: `int` Default: `10`

Return type of the action is `List[str]`.

#### Example Jac Usage:
Following example will return the summary of the a single text.

```jac
walker test_summarize_single {
    can bart_sum.summarize;
    report bart_sum.summarize("There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.", 10);
}
```
You can also pass a list of texts to get the summary of all the texts.
```jac
walker test_summarize_batch {
    can bart_sum.summarize;
    report bart_sum.summarize(
        ["There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.",
        "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.",
        "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude."],
        10
    );
}
```
Following example will return the summary of the web page.

```jac
walker test_summarize_url {
    can bart_sum.summarize;
    report bart_sum.summarize(null, "https://in.mashable.com/");
}
```

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
### Text Segmenter (`text_seg`)
`text_seg` Text segmentation is a method of splitting a document into smaller parts, which is usually called segments. It is widely used in text processing. Each segment has its relevant meaning. Those segments categorized as word, sentence, topic, phrase etc. module implemented for the Topical Change Detection in Documents via Embeddings of Long Sequences.
* `get_segements`: gets different topics in the context provided, given a threshold
    * Input
        * `text`(String): text the contain the entire context
        * `threshold`(Float): range is between 0-1, make each sentence as segment if, threshold is 1.
    * Returns: List of Sentences that best summarizes the context

* `load_model`: to load the available model for text segmentation
    * Input
        * `model_name`(String): name of the transformer model to load, options are:
            * `wiki`: trained on wikipedia data
            * `legal`: trained on legal documents
    * Returns: "[Model Loaded] : <model_name>"

* **Input data file `text_seg.json`**
    ```json
    {
        "text": "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude. The King of England was at war with him and had led a great army into Scotland to drive him out of the land. Battle after battle had been fought. Six times Bruce had led his brave little army against his foes and six times his men had been beaten and driven into flight. At last his army was scattered, and he was forced to hide in the woods and in lonely places among the mountains. One rainy day, Bruce lay on the ground under a crude shed listening to the patter of the drops on the roof above him. He was tired and unhappy. He was ready to give up all hope. It seemed to him that there was no use for him to try to do anything more. As he lay thinking, he saw a spider over his head making ready to weave her web. He watched her as she toiled slowly and with great care. Six times she tried to throw her frail thread from one beam to another, and six times it fell short. 'Poor thing,' said Bruce: 'you, too, know what it is to fail. But the spider did not lose hope with the sixth failure. With still more care, she made ready to try for the seventh time. Bruce almost forgot his own troubles as he watched her swing herself out upon the slender line. Would she fail again? No! The thread was carried safely to the beam and fastened there."
    }
    ```
#### Example Jac Usage:
```jac
walker text_seg_example {
    has data_file = "text_seg.json";
    has threshold = 0.85;
    can text_seg.get_segments, text_seg.load_model;

    # loading the desired model
    resp_data = text_seg.load_model(model_name='wiki');
    std.out(resp_data);

    # Getting Segments of different topic from text
    data = file.load_json(data_file);
    resp_data = text_seg.get_segments(
        text=data.text,
        threshold=threshold
        );
    std.out(resp_data);
}
```

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

### Topic Extraction (`topic_ext`)

Module `topic_ext` implemented for producing most relevant and possible set of topics for given set of text documents. Following is an example usage of the `topic_ext` module.

* `topic_ext.topic_extraction`: This action extracts top n number of topics from each cluster. The the text along with cluster label for the text cluster should be provided here as an input.
  * Input
    * `texts` - (list of strings) list of input text documents.
    * `labels` - (list of int) list of labels associated with each text documents.
    * `n_topics` - (int) number of topics to extract from each cluster.
  * Returns
    * A dictionary which contains relevant topics for each clusters.

* **Input data file `topic_extraction.json`**
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

```jac
walker init{
    can file.load_json;
    has text = file.load_json("topic_extraction.json");

    can use.encode;
    has encode = use.encode(visitor.text);

    can cluster.get_umap;
    final_features = cluster.get_umap(encode,2);

    can cluster.get_cluster_labels;
    labels = cluster.get_cluster_labels(final_features,"hbdscan",2,2);

    can topic_ext.topic_extraction;
    topic_dict = topic_ext.topic_extraction(texts=text,classes=labels,n_topics=5);
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

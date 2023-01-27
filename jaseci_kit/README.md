# Jaseci Kit
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
    ```
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
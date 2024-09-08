# Jaseci NLP Package `jac_nlp`

The `jac_nlp` package contains a collection of state-of-the-art NLP models that can be used to perform various nlp tasks such as named entity recongnition, text summerization, embedding generation, topic extraction etc. following is a list of all the models available in the `jac_nlp` package.

- [Jaseci NLP Package `jac_nlp`](#jaseci-nlp-package-jac_nlp)
  - [Text Encoders](#text-encoders)
    - [USE Encoder (`use_enc`)](#use-encoder-use_enc)
      - [Actions](#actions)
      - [Example Jac Usage:](#example-jac-usage)
    - [USE QA (`use_qa`)](#use-qa-use_qa)
      - [Actions](#actions-1)
      - [Example Jac Usage:](#example-jac-usage-1)
    - [BI-Encoder (`bi_enc`)](#bi-encoder-bi_enc)
      - [Actions](#actions-3)
      - [Example Jac Usage:](#example-jac-usage-3)
    - [Sbert Similarity (`sbert_sim`)](#sbert-similarity-sbert_sim)
      - [Actions](#actions-4)
      - [Example Jac Usage:](#example-jac-usage-4)
  - [Named Entity Recognition Models](#named-entity-recognition-models)
    - [Entity Extraction Using Transformers (`tfm_ner`)](#entity-extraction-using-transformers-tfm_ner)
      - [Actions](#actions-6)
      - [Example Jac Usage:](#example-jac-usage-6)
  - [Text Segmentation Modules](#text-segmentation-modules)
    - [Text Segmenter (`text_seg`)](#text-segmenter-text_seg)
      - [Actions](#actions-7)
      - [Example Jac Usage:](#example-jac-usage-7)
  - [Summarization Modules](#summarization-modules)
    - [Summarizer (`cl_summer`)](#summarizer-cl_summer)
      - [Actions](#actions-8)
      - [Example Jac Usage](#example-jac-usage-8)
    - [Summarization (`summarization`)](#summarization-summarization)
      - [Actions](#actions-10)
      - [Example Jac Usage:](#example-jac-usage-10)
  - [Topic Modeling Modules](#topic-modeling-modules)
    - [Topic Extraction](#topic-extraction)
      - [Actions](#actions-11)
  - [Sentiment Analysis Modules](#sentiment-analysis-modules)
    - [Sentiment Analysis](#sentiment-analysis)
      - [Actions](#actions-12)
      - [Example Jac Usage:](#example-jac-usage-11)
  - [Paraphraser Modules](#paraphraser-modules)
    - [Paraphraser](#paraphraser)
      - [Actions](#actions-13)
      - [Example Jac Usage:](#example-jac-usage-12)
  - [Text Generation Modules](#text-generation-modules)
    - [ChatGPT](#chatgpt)
      - [Actions](#actions-14)
      - [Example Jac Usage:](#example-jac-usage-13)

## Text Encoders

###  USE Encoder (`use_enc`)
`use_enc` module uses the universal sentence encoder to generate sentence level embeddings.
The sentence level embeddings can then be used to calculate the similarity between two given text via cosine similarity and/or dot product.

#### Actions

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
For a complete example visit [here](jac_nlp/use_enc/README.md)

###  USE QA (`use_qa`)

#### Actions

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

For a complete example visit [here](jac_nlp/use_qa/README.md)


### BI-Encoder (`bi_enc`)
`bi_enc`  module can be used for intent classification, it takes contexts and candidates, to predict the best suitable candidate for each context. You can train the module on custom data to behave accordingly.

#### Actions

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

For a complete example visit [here](jac_nlp/bi_enc/README.md)

### Sbert Similarity (`sbert_sim`)
`sbert_sim` is a implementation of SentenceBert for scoring similarity between sentence pairs, it uses bi-encoder in a saimese setup to encode the sentences followed by the cosine similarity to score the similarity.

#### Actions

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

For a complete example visit [here](jac_nlp/sbert_sim/README.md)

## Named Entity Recognition Models


### Entity Extraction Using Transformers (`tfm_ner`)

`tfm_ner` module uses transformers to identify and extract entities. It uses TokenClassification method from Huggingface.

#### Actions

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

For a complete example visit [here](jac_nlp/tfm_ner/README.md)

## Text Segmentation Modules

### Text Segmenter (`text_seg`)

`text_seg` Text segmentation is a method of splitting a document into smaller parts, which is usually called segments. It is widely used in text processing. Each segment has its relevant meaning. Those segments categorized as word, sentence, topic, phrase etc. module implemented for the Topical Change Detection in Documents via Embeddings of Long Sequences.

#### Actions

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

For a complete example visit [here](jac_nlp/text_seg/README.md)

## Summarization Modules
### Summarizer (`cl_summer`)

`cl_summer` uses the sumy summarizer to create extractive summary.

#### Actions

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
#### Example Jac Usage
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

For a complete example visit [here](jac_nlp/cl_summer/README.md)


### Summarization (`summarization`)

`summarization` uses the BART transformer model to perform abstractive summary on a body of text.

#### Actions

There are 2 ways to use `summarization` module.
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
    can summarization.summarize;
    report summarization.summarize("There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude.", 10);
}
```
You can also pass a list of texts to get the summary of all the texts.
```jac
walker test_summarize_batch {
    can summarization.summarize;
    report summarization.summarize(
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
    can summarization.summarize;
    report summarization.summarize(null, "https://in.mashable.com/");
}
```

For a complete example visit [here](jac_nlp/summarization/README.md)

## Topic Modeling Modules

### Topic Extraction

Topic Extraction (`topic_ext`)

Module `topic_ext` implemented for producing most relevant and possible set of topics for given set of text documents. Following is an example usage of the `topic_ext` module.

#### Actions

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

#### Example Jac Usage:

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

For a complete example visit [here](jac_nlp/topic_ext/README.md)

## Sentiment Analysis Modules

### Sentiment Analysis

#### Actions

Module `sentiment` implemented for analysing the sentiment in a given list of text. This module accepts as input a set of sentences.

- `texts` - (list of strings) list of input text documents.

#### Example Jac Usage:

```jac
walker test_predict{
    can sentiment.predict;

    has texts = ["I love you", "I hate you"];

    report sentiment.predict(texts);
}
```
For a complete example visit [here](jac_nlp/sentiment/README.md)

## Paraphraser Modules

### Paraphraser

#### Actions

Module `paraphraser` implemented for paraphrasing the given input text.

- `text` - (Strings) Input text phrases.

#### Example Jac Usage:

```jac
walker init{
    can paraphraser.paraphrase;

    has text = "Yiping Kang is inviting you to a scheduled Zoom meeting";

    report paraphraser.paraphrase(text=text);
}
```

For a complete example visit [here](jac_nlp/paraphraser/README.md)

## Text Generation Modules

### ChatGPT

Module `gp2` uses the OpenAI's `GPT-2-medium` to perform text genreation on a given text.

#### Actions

The `generate` action allows you to generate text based on the input text you provide.

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

```
walker test_generate {
    can gpt2.generate;
    report gpt2.generate(text= "Hello, my name is", num_return_sequences= 5);
}
```

Given a text or a list of texts, it will return the embeddings of the text.

```
walker test_get_embeddings {
    can gpt2.get_embeddings;
    report gpt2.get_embeddings(text= ["Hello, my name is GPT2", "GPT2 is an Text-to-Text Generation Model" ]);
}
```
For a complete example visit [here](jac_nlp/gpt2/README.md)


---
sidebar_position: 1
title: Flair NER
description: NER with Flair NER
---

# Entity Extraction (`ent_ext` and `lstm_ner`)

`ent_ext` module uses Flair named entity recognition architecture. Can either be used zero-shot or trained.

## Actions

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
* `entity_detection`: detects all available entities from the provided context
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
        * `ner_model`: pre-trained or basic model to be loaded, provide the exact name of the model, available options are:
            * `Pre-trained LSTM / GRU` : ["ner", "ner-fast","ner-large"]
            * `Huggingface model` : all available models that can be initialized with AutoModel
            * `None` : for load a RNN model from scratch
        * `model_type`: type of model to be loaded, available options are :
            * `TRFMODEL` : for huggingface models
            * `LSTM` or `GRU` : RNN models
    * Returns: "Config setup is complete." if model successfully loaded
    *
## Example Jac Usage:

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

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/ent_ext)
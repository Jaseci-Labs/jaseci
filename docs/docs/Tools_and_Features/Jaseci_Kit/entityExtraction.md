# Entity Extraction

`ent_ext` module uses Flair named entity recognition architecture. Can either be used zero-shot or trained.


To load the Entity Extraction Module run :

```
actions load module jaseci_ai_kit.ent_ext
```

* `train`: used to train the Flair-based NER model
    * Input:
        * `traindata`: (List(Dict)): a list of dictionaries containing contexts and list of entities in each context
        ```
        [
            {
                "context": "I used to live at London, UK",
                "entities": [
                    {
                        "entity_value": "London",
                        "entity_type": "LOC",
                        "start_index": 13,
                        "end_index": 18
                    },
                    {
                        "entity_value": "Minn",
                        "entity_type": "LOC",
                        "start_index": 19,
                        "end_index": 20
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

    has train_file = "train_ner.json";
    has from_scratch = true;
    has num_train_epochs = 20;
    has batch_size = 8;
    has learning_rate = 0.02;
    can ent_ext.entity_detection,ent_ext.train;
    train_data = file.load_json(train_file);

    # Training the model
    ent_ext.train(
    train_data=train_data,
    train_params={
        "num_epoch": num_train_epochs,
        "batch_size": batch_size,
        "LR": learning_rate
    }
    );

    # Getting inference from the model
    resp_data = ent_ext.entity_detection(text="book a flight from kolkata to delhi",ner_labels= ["LOC"]);
    std.out(resp_data);
}
```

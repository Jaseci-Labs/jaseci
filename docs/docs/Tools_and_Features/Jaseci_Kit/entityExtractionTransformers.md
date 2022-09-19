# Entity Extraction Using Transformers 


`tfm_ner` module uses transformers to identify and extract entities. It uses TokenClassification method from Huggingface.


To load the Entity Extraction Transformer Module run :

```
actions load module jaseci_ai_kit.ent_ext
```


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
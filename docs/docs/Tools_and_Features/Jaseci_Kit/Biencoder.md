
#  BI-Encoder 
`bi_enc`  module can be used for intent classification, it takes contexts and candidates, to predict the best suitable candidate for each context. You can train the module on custom data to behave accordingly.

To load the Bi-encoder  Module run :

```
actions load module jaseci_ai_kit.bi_enc
```
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

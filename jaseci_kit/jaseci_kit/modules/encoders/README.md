##  Bi-Encoder (`bi_enc`)
`bi_enc` is a arrangement of two encoder modules from BERT, it represents context and candidate separately using twin-structured encoders, it takes contexts and candidates, to predict the best suitable candidate for each context. You can train the module on custom data to behave accordingly. Let's take a deep dive into the trainning culture.

### List of APIs required 
* `train`: will be used to train the Bi-Encoder on custom data
    * Input:
        * `dataset` (Dict): dictionary of candidates and suportting contexts for each candidate
        * `from_scratch` (bool): if set to true train the model from scratch otherwise trains incrementally 
        * `training_parameters` (Dict): dictionary of training parameters
    * Returns: text when model training is completed
* `infer`: will be used to predits the most suitable candidate for a provided context, takes text or embedding 
    * Input:
        * `contexts` (string or list of strings): context which needs to be classified
        * `candidates` (string or list of strings): list of candidates for the context 
        * `context_type` (string): can be text or embedding type
        * `candidate_type` (string): can be text or embedding type
    * Return: a dictionary of similarity score for each candidate and context 

* `get_train_config`: used to get the model's current training configuration
    * Input: None
    * Returns: json of all the current training configuration
     ```
     {
        "max_contexts_length": 128,
        "max_candidate_length": 64,
        "train_batch_size": 8,
        "eval_batch_size": 2,
        "max_history": 4,
        "learning_rate": 0.0001,
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
* `get_model_config`: used to get the model's current configuration
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
* `set_model_config`: used to setup the model's configuration
    * Input 
        * `model_parameters`(Dict): dictionary of model parameters. See the json example above under `get_model_config` for the list of available training parameters.
    * Returns: "Config setup is complete." if model configuration is completed successfully


### Let's Jump into the coding Section 

Declaring the walker: 
```jac
walker bi_enc_example{
    # the parameters required for training
    
    has train_file = "train_bi.json";
    has from_scratch = true;
    has num_train_epochs = 20;
    has test_file = "test_bi.json";

    # the actions that would be supported by the walker
    can bi_enc.train;
    can bi_enc.infer;
}
```
Code snippet for training the model
```
    train_data = file.load_json(train_file);
    
    # Train the model 
    bi_enc.train(
        dataset=train_data["dataset"],
        from_scratch=from_scratch,
        training_parameters={
            "num_train_epochs": num_train_epochs
        }
    );
```
Code snippet that can be used to infer the data
```
    test_data = file.load_json(test_file);
    
    # Use the model to perform inference
    # returns the list of context with the suitable candidates
    resp_data = bi_enc.infer(
        contexts=test_data["contexts"],
        candidates=test_data["candidates"],
        context_type=test_data["context_type"],
        candidate_type=test_data["candidate_type"]
    );
    # the infer action returns all the candidate with the confidence scores
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
```
#### Sample train_bi.json
```
{
	"dataset": {
		"PlayMusic": [
			"listen to westbam alumb allergic on google music"
		],
		"AddToPlaylist": [
			"add step to me to the 50 classic playlist "
		],
		"RateBook": [
			"i give this current textbook a rating value of 1 and a best rating of 6"
		],
		"SearchCreativeWork": [
			"can you look up the molecular oncology saga"
		]
	}
}
```

#### Sample test_bi.json
```
{
	"contexts": [
		"add this artist to showstopper being mary jane",
		"what is the weather here"
	],
	"candidates": [
		"PlayMusic",
		"GetWeather",
		"BookRestaurant",
		"SearchScreeningEvent",
		"RateBook",
		"SearchCreativeWork",
		"AddToPlaylist"
	],
	"context_type": "text",
	"candidate_type": "text"
}
```
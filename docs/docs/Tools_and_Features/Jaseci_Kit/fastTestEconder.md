
# Fast Text Encoder 
`fast_enc` module uses the facebook's fasttext -- efficient learning of word representations and sentence classification.



To load the Fast text Encoder run :

```
actions load module jaseci_ai_kit.fast_enc
```

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



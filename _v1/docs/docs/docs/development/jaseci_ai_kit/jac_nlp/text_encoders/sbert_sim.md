---
sidebar_position: 5
title: Sbert Similarity
description: Text Encoding with Sbert
---

# Sbert Similarity (`sbert_sim`)
`sbert_sim` is a implementation of SentenceBert for scoring similarity between sentence pairs, it uses bi-encoder in a saimese setup to encode the sentences followed by the cosine similarity to score the similarity.

## Actions

* `get_dot_score` : Calculate the dot product of two given vectors
    * Input:
        * `vec_a` (list of float): first embedded text
        * `vec_b` (list of float): second embedded text
    * Return: dot product score
* `get_cos_score` : Calculate the cosine similarity score of two given vectors
    * Input:
        * `vec_a` (list of float): first embedded text
        * `vec_b` (list of float): second embedded text
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
          * `tfm_model` : load transformer model from the [huggingface hub](https://huggingface.co/models)
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

## Example Jac Usage:

```jac
## Train and evaluate a sbert model for sentence similarity
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

    # returns the top_k of similar test in the corpus
    resp_data = sbert_sim.get_text_sim(query=query,corpus=corpus,top_k=top_k);
    std.out(resp_data);
}
```

For a complete example visit [here](../../../../../tutorials/jaseci_ai_kit/jac_nlp/sbert_sim)
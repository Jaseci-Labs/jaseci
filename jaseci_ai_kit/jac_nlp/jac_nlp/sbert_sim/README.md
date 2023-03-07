#  **SBert Similarity (`sbert_sim`)**
**`sbert_sim`** is a implementation of SentenceBert for scoring similarity among sentences, it uses bi-encoder in a saimese setup to encode the sentence followed by the cosine similarity to score the similarity.

This tutorial guide you through the usage of api's available for sbert_sim though jac codes.


1. Preparing [dataset](#1-praparing-dataset)
2. Import [Sbert Similarity(sbert_sim)](#2-import-sbert-similaritysbertsim-module-in-jac) module in jac
3. [Train and Predict](#3-train-and-predict)


## **Walk through**

### **1. Praparing dataset**
The training dataset format contain a list of sentence pair and the similarity score among them. Let's consider the folowing sample for example:
```
["A person is on a baseball team.","A person is playing basketball on a team.",0.99]
```

### **2. Import `Sbert Similarity(sbert_sim)` module in jac**
1. Open terminal and run jaseci by cmd
    > jsctl -m
2. Load `sbert_sim` module in jac by cmd
    > actions load module jac_nlp.sbert_sim

### **3. Train and Predict**
For this tutorial, we would walk you though the process to `train` and use the `get_sim_score` from `sbert_sim` to get similarty score.

* **Creating Jac Program (sbert_sim)**
    1. Create a file by name `sbert_sim.jac`

    2. Initialize walker `train_sbert_sim` and `get_sim_score`
        ```jac
        walker train_module{
            can sbert_sim.train;
            has train_data= [
                            ["A person is on a baseball team.","A person is playing basketball on a team.",0.99],
                            ["Our current vehicles will be in museums when everyone has their own aircraft.","The car needs to some work",0.99],
                            ["A woman supervisor is instructing the male workers.","A woman is working as a nurse.",0.99]
                        ];
            report sbert_sim.train(train_data,{'num_epochs':2});
            }
        walker get_sim_score{
            can sbert_sim.get_text_sim;
            report sbert_sim.get_text_sim("A girl dancing on a sandy beach.","A girl is on a sandy beach.",1);
            }
        ```
        **Parameter details**
        * `train`: will be used to train the Sbert Similarity on custom data
            * Input:
                * `dataset` (Dict): dictionary of candidates and suportting contexts for each candidate
                * `training_parameters` (Dict): dictionary of training parameters
            * Returns: text when model training is completed
        * `get_sim_score`: will be used to predits the most suitable candidate from corpus for a provided query, takes text or embedding
            * Input:
                * `query` (string or list of strings): contains a list of queries that is scored against the list of corpus
                * `corpus` (string or list of strings): contain a list of entries that is evaluated with each query
                * `top_k` (int): returns k number of top similar entries in corpus
            * Return: a dictionary of similarity score for each candidate and context


    **Steps for running `sbert_sim.jac` programm**
    1. Build `sbert_sim.jac` by run cmd
        > jac build sbert_sim.jac
    2. Activate sentinal by run cmd
        > sentinel set -snt active:sentinel -mode ir sbert_sim.jir

    3. Calling walker `train_sbert_sim` with `default parameter` for training `sbert_sim` module by cmd
        > walker run train_sbert_sim </br>
    4. Calling walker `get_sim_score` with `default parameter` for predicting `sbert_sim` module by cmd
        > walker run get_sim_score </br>
#  **Bi-NER (`bi_ner`)**
**`bi_ner`** is a arrangement of two encoder modules from BERT, it represents context and candidate separately using twin-structured encoders. You can train the module on custom data to behave accordingly. Let's take a deep dive into the training culture.


This tutorial shows you how to train a Bi-NER with a custom training loop to extracts entities from contexts. In this you use jaseci(jac) and python.


1. Import [Bi-NER (bi_ner)](#1-import-bi-nerbi_ner-module-in-jac) module in jac
2. [Train](#2-train-the-model) the model
3. Use the trained model to make [predictions](#3-use-the-trained-model-to-make-predictions-)


## **Walk through**

### **1. Import `Bi-NER(bi_ner)` module in jac**
1. Open terminal and run jaseci by cmd
    > jsctl -m
2. Load `bi_ner` module in jac by cmd
    > actions load module jaseci_ai_kit.bi_ner

### **2. Train and Predict **
For this tutorial, we are going to `train and Predict` the `bi-ner` for `Named Entity Recognition`.

* **Creating Jac Program (`train and infer` bi_ner)**
    1. Create a file by name `bi_ner.jac`
    2. Create  `train` walker
        ```
        walker train{
            # import train ability
            can bi_ner.train;
            # the parameters required for training
            has train_file = "train_bi.json";
            has from_scratch = true;
            has num_train_epochs = 20;
            # load the file
            train_data = file.load_json(train_file);
            # Train the model
            report bi_ner.train(
                dataset=train_data,
                from_scratch=from_scratch,
                training_parameters={
                    "num_train_epochs": num_train_epochs.int
                    }
                );
            }
        ```

    3. Declaring Predict walker for extracting entities
        ```
        #
        walker predict{
            # passing input data for prediction
            has test_data_file = "test_dataset.json";
            test_data = file.load_json(test_data_file);
            report bi_ner.infer(
                            contexts=test_data,
                            );
        }
        ```

        **Parameter details**
        * `train`: will be used to train the Bi-NER on custom data
            * Input:
                * `dataset` (Dict): dictionary of candidates and suportting contexts for each candidate
                * `from_scratch` (bool): if set to true train the model from scratch otherwise trains incrementally
                * `training_parameters` (Dict): dictionary of training parameters
            * Returns: text when model training is completed
        * `infer`: will be used to predits the most suitable candidate for a provided context, takes text or embedding
            * Input:
                * `contexts` (string or list of strings): context which needs to be classified
            * Return: a dictionary of entities type and value with start and end index

    **Steps for running `bi_ner.jac` programm**

    4. Build `bi_ner.jac` by run cmd
        > jac build bi_ner.jac
    5. Activate sentinal by run cmd
        > sentinel set -snt active:sentinel -mode ir bi_ner.jir

    6. Calling walker `train` with `default parameter` for training `bi_ner` module by cmd
        > walker run train </br>
    7. Calling walker `predict` with `default parameter`  to get evalution
        > walker run predict </br>


    **Sample Input Data for Training**
    ```
   {
        "text": [
            "IL-2 gene expression and NF-kappa B activation through CD28 requires reactive oxygen production by 5-lipoxygenase.",
            "Activation of the CD28 surface receptor provides a major costimulatory signal for T cell activation resulting in enhanced production of interleukin-2 (IL-2) and cell proliferation."
        ],
        "annotations": [
            [
                {
                    "start_index": 0,
                    "end_index": 9,
                    "entity_type": "G#DNA"
                },
                {
                    "start_index": 25,
                    "end_index": 35,
                    "entity_type": "G#protein"
                },
                {
                    "start_index": 55,
                    "end_index": 59,
                    "entity_type": "G#protein"
                },
                {
                    "start_index": 99,
                    "end_index": 113,
                    "entity_type": "G#protein"
                }
            ],
            [
                {
                    "start_index": 18,
                    "end_index": 22,
                    "entity_type": "G#protein"
                },
                {
                    "start_index": 18,
                    "end_index": 39,
                    "entity_type": "G#protein"
                },
                {
                    "start_index": 136,
                    "end_index": 149,
                    "entity_type": "G#protein"
                },
                {
                    "start_index": 151,
                    "end_index": 155,
                    "entity_type": "G#protein"
                }
            ]
        ]
    }
    ```



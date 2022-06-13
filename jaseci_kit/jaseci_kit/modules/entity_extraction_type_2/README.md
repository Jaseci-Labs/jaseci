#  Entity Extraction Using Transformers (`tfm_ner`)

**What is NER:** named entity recognition (NER) — sometimes referred to as entity chunking, extraction, or identification — is the task of identifying and categorizing key information (entities) in text. An entity can be any word or series of words that consistently refers to the same thing. Every detected entity is classified into a predetermined category.

**`tfm_ner`**: module based on transformers to identify and extract entities. It uses TokenClassification method from Huggingface.

This tutorial show you how to train test and validate **tfm_ner** module.

# Transformer NER
1. Preparing [Dataset](#1-preparing-dataset)
2. Import [tfm_ner](#2-import-tfmner-module-in-jaseci) module
3. Model [training and validation](#3-model-training-and-validation)

## **1. Preparing Dataset**
For train, test and validation dataset, we are going to creating list of dict and storing in json file by name `train.json`, `validation.json` and `test.json` and storing dataset file in directory name dataset and put all required file in this.

* **`train_data`:**: (List(Dict)): a list dictionary containing contexts and list of entities in each context.

    ```
    [{
        "context": "However a loophole in the law allowed Buddharakkita and Jayewardene evade the death penalty as the Capital Punishment Repeal Act allowed for a sentence of death to a person convicted for murder committed prior to December 2 1959 and not for the offence of conspiracy to commit murder",
        "entities": [
            {
                "entity_value": "Buddharakkita",
                "entity_type": "person",
                "start_index": 38,
                "end_index": 51
            },
            {
                "entity_value": "Jayewardene",
                "entity_type": "person",
                "start_index": 56,
                "end_index": 67
            },
            {
                "entity_value": "Capital Punishment Repeal Act",
                "entity_type": "event",
                "start_index": 99,
                "end_index": 128
            }
        ]
        }
    ]
    ```
* **`val_data`:** (List(Dict)): a list dictionary containing contexts and list of entities in each context
    ```
    [
        {
            "context": "The Stavros Niarchos Foundation Cultural Center inaugurated in 2016 will house the National Library of Greece and the Greek National Opera",
            "entities": [
                {
                    "entity_value": "Stavros Niarchos Foundation Cultural Center",
                    "entity_type": "building",
                    "start_index": 4,
                    "end_index": 47
                },
                {
                    "entity_value": "National Library of Greece",
                    "entity_type": "building",
                    "start_index": 83,
                    "end_index": 109
                },
                {
                    "entity_value": "Greek National Opera",
                    "entity_type": "building",
                    "start_index": 118,
                    "end_index": 138
                }
            ]
        }
    ]
    ```
* **`test_data`:** (List(Dict)): a list dictionary containing contexts and list of entities in each context
    ```
    [
        {
            "context": "The project proponents told the Australian Financial Review in December that year that they had been able to demonstrate that the market for backpacker tourism was less affected by these events and that they intended to apply for an air operator 's certificate in January 2004",
            "entities": [
                {
                    "entity_value": "Australian Financial Review",
                    "entity_type": "organization",
                    "start_index": 32,
                    "end_index": 59
                }
            ]
        }
    ]
    ```

## **2. Import `tfm_ner` module in jaseci**
1. Open terminal and run jaseci by cmd
    ```
    jsctl -m
    ```
2. Load module tfm_ner in jac by cmd
    ```
    actions load module 
    ```

## **3. Model training and validation**
For this tutorial we are going to train the model on train dataset and validate the model on validation dataset and finaly we test model on the test dataset.

**1. Creating Jac Program**
1. `Create a file (main.jac)`

2. Create node `model_dir` and  `tfm_ner` in `main.jac`

    ```
    node model_dir;
    node tfm_ner {}
    ```
3. Initializing `node tfm_ner` and adding abilty:- `train`, `infer`

    here we are importing ability to train and infer model.
    ```
    node tfm_ner {
        # train, infer
        can tfm_ner.train, tfm_ner.extract_entity, tfm_ner.load_model, tfm_ner.save_model, tfm_ner.get_train_config, tfm_ner.set_train_config;
    }

    ```

4. Initializing module for `train and validation` inside `node tfm_ner`
    In this step we are initializing `training` and `validation` of tfm_ner model. It will take 5 parameter train, test, val (file contain `list of dict`) and mode and epochs
    
    ```
    # train and validation model 
    can train_and_val with train_and_val_tfm entry {
        train_data = file.load_json(visitor.train_file);
        val_data = file.load_json(visitor.val_file);
        test_data = file.load_json(visitor.test_file);
        std.out("corpus : ",train_data.length," train + ",val_data.length," val +",test_data.length," test sentences");
        tfm_ner.train(
            mode = visitor.mode,
            epochs = visitor.num_train_epochs.int,
            train_data = train_data,
            dev_data = val_data,
            test_data = test_data
            );
        std.out("training and validation done ");
        }
    ```
5. adding module for `infer entity` inside node `tfm_ner`

    `Infer` module will take text input and return entities list.
    ```
    # infer entity from text
    can infer with predict_entity_from_tfm entry {
        report tfm_ner.extract_entity(
            text = visitor.text
        );
    }
    ```
6. Adding `edge` name of  `ner_model` in `main.jac` file for connecting nodes inside graph.
    ```
    # adding edge
    edge ner_model {
        has model_type;
    }
    ``` 

7. Adding `graph` name of `ner_val_graph` for initializing node . 
    ```
    # Adding Graph
    graph ner_val_graph {
        has anchor ner_model_dir;
        spawn {
            ner_model_dir = spawn node::model_dir;
            tfm_ner_node = spawn node::tfm_ner;
            ner_model_dir -[ner_model(model_type="tfm_ner")]-> tfm_ner_node;
        }
    }
    ``` 

8. Initializing `walker init` for calling graph
    ```
    walker init {
        root {
        spawn here --> graph::ner_val_graph; 
        }
    }
    ```
9. Creating `walker` name of `train_and_val_tfm` for getting parameter from context and calling ability `training and validation` model.
    ```
    # creating walker 
    walker train_and_val_tfm {
        has train_file;
        has val_file;
        has test_file;
        has num_train_epochs;
        has mode;

        # Train NER models on the train set
        # and validate them on the val set (Optional)
        # and test them on the test set (Optional)

        # report accuracy performance of NER model on inside dir creating on place of current path `main.jac` file "train/logs/"
        root {
            take --> node::model_dir;
        }
        model_dir {
            take -->;
        }
    }
    ```
10. Creating a walker name of `predict_entity_from_tfm` for getting new text as input from context and infer entities.

    ```
    walker predict_entity_from_tfm{
        has text;

        root {
            take --> node::model_dir;
        }
        model_dir {
            take -->;
        }
    }
    ```
* **Now we are adding all `steps(from 2 to 10)` inside `main.jac` file**

* **Final jac programm `(main.jac)`**

    ```
    node model_dir;
    node tfm_ner {
        # train,infer
        can tfm_ner.extract_entity, tfm_ner.train;

        # extracting entities
        can infer with predict_entity_from_tfm entry {
            report tfm_ner.extract_entity(
                text = visitor.text
            );
        }

        ## train and validate
        can train_and_val with train_and_val_tfm entry {

            train_data = file.load_json(visitor.train_file);
            val_data = file.load_json(visitor.val_file);
            test_data = file.load_json(visitor.test_file);
            std.out("corpus : ",train_data.length," train + ",val_data.length," dev +",test_data.length," test sentences");
            tfm_ner.train(
                mode = visitor.mode,
                epochs = visitor.num_train_epochs.int,
                train_data = train_data,
                dev_data = val_data,
                test_data = test_data
                );
            std.out("training and validation done ");
            }
    }


    edge ner_model {
        has model_type;
    }

    graph ner_val_graph {
        has anchor ner_model_dir;
        spawn {
            ner_model_dir = spawn node::model_dir;
            tfm_ner_node = spawn node::tfm_ner;
            ner_model_dir -[ner_model(model_type="tfm_ner")]-> tfm_ner_node;
        }
    }


    walker init {
        root {
        spawn here --> graph::ner_val_graph; 
        }
    }

    ## creating walker 
    walker train_and_val_tfm {
        has train_file;
        has val_file;
        has test_file;
        has num_train_epochs;
        has mode;

        # Train all NER models on the train set
        # and validate them on the val set
        # report accuracy performance across all NER models
        root {
            take --> node::model_dir;
        }
        model_dir {
            take -->;
        }
    }

    walker predict_entity_from_tfm{
        has text;

        root {
            take --> node::model_dir;
        }
        model_dir {
            take -->;
        }
    }

**2. Steps for running `main.jac` file** and `train` and `validate` tfm_ner model

1. Build main.jac by run:
    ```
    jac build main.jac
    ```

2. Activate sentinal by run cmd:
    ```
    sentinel set -snt active:sentinel -mode ir main.jir
    ```

3.  ### Create **`Training Input`**
    * `mode`: (String): mode for training the model, available options are :
            * `default`: train the model from scratch.
            * `incremental`: providing more training data for current set of entities.
            * `append`: changing the number of entities (model is restarted and trained with all of traindata).
    * `epochs `: (int): Number of epoch you want model to train.
    * `train_file`: `list[dict]` train data file name.
    * `val_file`: `list[dict]` validation data file name.
    * `test_file`: `list[dict]` test data file name.

    

6. for train model run walker `train_and_val_tfm` with jac by run cmd
    ```
    walker run train_and_val_tfm -ctx "{\"train_file\":\"dataset/train.json\",\"val_file\":\"dataset/dev.json\",\"test_file\":\"dataset/test.json\",\"num_train_epochs\":\"10\",\"mode\":\"default\"}"
    ```

7. `Result` : after running `train_and_val_tfm` walker you will get logs on console below format

    ```
    2022-06-06 11:23:46.832007    Training epoch: 1/50
    2022-06-06 11:23:46.847969    Training loss per 100 training steps: 0.9243220090866089
    2022-06-06 11:23:47.186904    Training loss epoch: 0.8817697350795453
    2022-06-06 11:23:47.191905    Training accuracy epoch: 0.11538461538461539
    2022-06-06 11:23:47.330845    Validation loss epoch: 0.7973677378434402
    2022-06-06 11:23:47.336076    Validation accuracy epoch: 0.038461538461538464
    2022-06-06 11:23:47.442199    Epoch 1 total time taken : 0:00:00.610192
    2022-06-06 11:23:47.448885    ------------------------------------------------------------
    2022-06-06 11:23:47.456886    Training epoch: 2/50
    2022-06-06 11:23:47.474848    Training loss per 100 training steps: 0.8383979797363281
    2022-06-06 11:23:47.814906    Training loss epoch: 0.7714704366830679
    2022-06-06 11:23:47.820939    Training accuracy epoch: 0.023076923076923078
    2022-06-06 11:23:47.969910    Validation loss epoch: 0.70741940003175
    2022-06-06 11:23:47.976287    Validation accuracy epoch: 0.0
    2022-06-06 11:23:48.075297    Epoch 2 total time taken : 0:00:00.618411
    2022-06-06 11:23:48.081293    ------------------------------------------------------------
    
    ```

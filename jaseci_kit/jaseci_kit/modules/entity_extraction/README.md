### Entity Extraction Using `FLAIR NER(ent_ext)`

`ent_ext`: module uses Flair named entity recognition architecture. Can either be used zero-shot or trained.


### `Use Case 1 : Zero-Shot entity detection` Classify entity Without Training NER Data:

Starting write jac code for classifying entities from text:

1. create a file by name `zero_shot_ner.jac`

2. Create node `model_dir` and `flair_ner` in `zero_shot_ner.jac` file
    ```
    node model_dir;
    node flair_ner {};
    ```
3. Initializing node flair_ner and adding abilty `set_config` and `entity_detection`
    ```
    node flair_ner{
        # set model configuration and infer entity
        ent_ext.set_config, can ent_ext.entity_detection;
        }
    ```
4. initializing module for `set_config` inside node `flair_ner`
    ```
    can set_config with infer_zero_shot entry{
        report ent_ext.set_config(
            ner_model = visitor.model_name,
            model_type = visitor.model_type
        );
    }
    ```
    its take two argument `model_name(str)` an `model_type(str)`.

5. Initializing module for `zero_shot tokenclassification` inside `flair_ner`
    ```
    can infer_zero_shot with infer_zero_shot entry{
        text = visitor.text;
        labels = visitor.labels.list;
        result =  ent_ext.entity_detection(
            text=text,
            ner_labels= labels
            );
        fn = "result.json";
        result = {"text":text,"entities":result["entities"]};
        file.dump_json(fn, result);
    }
    ```
    `infer_zero_shot` module take two arguments `text` and `labels list` for infer entity.

6. Adding edge name of `ner_model` in `zero_shot_ner.jac` file for connecting nodes inside graph.
    ```
    # adding edge
    edge ner_model {
        has model_type;
    }
    ```

7. Adding graph name of `ner_val_graph` for initializing node .
    ```
    graph ner_eval_graph {
        has anchor ner_model_dir;
        spawn {
            ner_model_dir = spawn node::model_dir;
            flair_ner_node = spawn node::flair_ner;
            ner_model_dir -[ner_model(model_type="flair_ner")]-> flair_ner_node;
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

9. Creating `walker` name of `infer_zero_shot` for getting parameter from context and calling ability `set_config` and `infer_zero_shot` entity detection.

    ```
    # creating walker for entity predictions
    walker infer_zero_shot{
        has model_name;
        has model_type;
        has text;
        has labels;

        root {
            take --> node::model_dir;
        }
        model_dir {
            take -->;
        }
    }
    ```
    it take arguments from context and call ability to set model configuration `set_config` and `infer_zero_shot` for detecting entity from text and store `result` in `result.json file`

    Now we commbining all the steps from `2 to 9` in single file `zero_shot_ner.jac`
    ### final Jac Program `zero_shot_ner.jac`

    ```
    node model_dir;
    node flair_ner {
        # load the model actions here
        can ent_ext.entity_detection, ent_ext.set_config;

        can set_config with infer_zero_shot entry{
            report ent_ext.set_config(
                ner_model = visitor.model_name,
                model_type = visitor.model_type
            );
        }

        can infer_zero_shot with infer_zero_shot entry{
            text = visitor.text;
            labels = visitor.labels.list;
            result =  ent_ext.entity_detection(
                text=text,
                ner_labels= labels
                );
            fn = "result.json";
            result = {"text":text,"entities":result["entities"]};
            file.dump_json(fn, result);
        }
    }



    edge ner_model {
        has model_type;
    }

    graph ner_eval_graph {
        has anchor ner_model_dir;
        spawn {
            ner_model_dir = spawn node::model_dir;
            flair_ner_node = spawn node::flair_ner;
            ner_model_dir -[ner_model(model_type="flair_ner")]-> flair_ner_node;
        }
    }



    walker init {
        root {
        spawn here --> graph::ner_eval_graph; 
        }
    }

    # creating walker for entity predictions
    walker infer_zero_shot{
        has model_name;
        has model_type;
        has text;
        has labels;

        root {
            take --> node::model_dir;
        }
        model_dir {
            take -->;
        }
    }
    ```
    ### steps for calling jac program `use case 1` and `infer entity` from new text.
    1. Open terminal and run jaseci by command
        ```
        jsctl -m
        ```
    2. Load the `flair entity_detection` Module by run cmd :
        ```
        actions load module jaseci_kit.ent_ext
        ```
    3. Build `zero_shot_ner.jac` by run cmd :
        ```
        jac build zero_shot_ner.jac
        ```
    4. Activate `sentinal` by run cmd:
        ```
        sentinel set -snt active:sentinel -mode ir zero_shot_ner.jir
        ```
    5. `entity_detection`: detects all availabe entities from the provided context
        * ### Input:
            * `model_name`: name of model which we are using for zero-shot entity detection e.g. `tars-ner`
            * `model_type : type of model using in entity detection e.g. `tars` 
            * `text (string)`: context to detect entities.
            * `ner_labels(list of strings)`: List of entities, e.g. `["LOC","PER"]`
            
        * ### output
            * `Result`: Created a json file that stored `input text` and `predicted entities` in result.json file`

    6. Calling walker for `entity_detection` and pass `input data` in context by cmd:
        * `Create Input Data`:-

            * `model_name` : `prajjwal1/bert-tiny` or `tars-ner`
            * `model_type` : `trfmodel` or `tars`
            * `text`: "They had a record of five wins and two losses in Opening Day games at Bennett Park 19 wins and 22 losses at Tiger Stadium and three wins and four losses at Comerica Park for a total home record in Opening Day games of 26 wins and 28 losses"
            * `labels` : ["building", "organization"]

        * `calling walker by cmd:`
            ```
            walker run infer_zero_shot -ctx "{\"model_name\":\"prajjwal1/bert-tiny\",\"model_type\":\"trfmodel\",\"text\":\"They had a record of five wins and two losses in Opening Day games at Bennett Park 19 wins and 22 losses at Tiger Stadium and three wins and four losses at Comerica Park for a total home record in Opening Day games of 26 wins and 28 losses\",\"labels\":[\"building\", \"organization\"]}"
            ```

    7. After calligg step 6 entity outpu will be stored in `result.json` file 
        ```
        ```


### `Use Case 2 : Train model, validate and test on new datasets(train, val, test)`: Classify entity after Training on some ner dataset and then detect entity on new test ner dataset

Starting write jac code for training flair ner model and then classifying entities from text data:
1. create a file by name `flair_ner.jac`

2. Create node `model_dir` and `flair_ner` in `flair_ner.jac` file
    ```
    node model_dir;
    node flair_ner {};
    ```
3. Initializing node flair_ner and adding abilty `set_config` and `entity_detection`
    ```
    node flair_ner{
        # set ability model configuration and train model
        ent_ext.set_config, can ent_ext.train;
        }
    ```
4. initializing module for `set_config` inside node `flair_ner`
    ```
    can set_config with infer_zero_shot entry{
        report ent_ext.set_config(
            ner_model = visitor.model_name,
            model_type = visitor.model_type
        );
    }
    ```
    its take two argument `model_name(str)` an `model_type(str)`.

5. initializing module for `train` inside node `flair_ner`
    ```
    can train with train_and_val_flair entry{
        # train the model with a given dataset
        train_data = file.load_json(visitor.train_file);
        val_data = file.load_json(visitor.val_file);
        test_data = file.load_json(visitor.test_file);

        # training model
        ent_ext.train(
            train_data = train_data,
            val_data = val_data,
            test_data = test_data,
            train_params = {
                "num_epoch": visitor.num_train_epochs.int,
                "batch_size": visitor.batch_size.int,
                "LR": visitor.learning_rate.float
                });
    }
    ```
6. Adding edge name of `ner_model` in `flair_ner.jac` file for connecting nodes inside graph.
    ```
    # adding edge
    edge ner_model {
        has model_type;
    }
    ```

7. Adding graph name of `ner_val_graph` for initializing node .
    ```
    graph ner_eval_graph {
        has anchor ner_model_dir;
        spawn {
            ner_model_dir = spawn node::model_dir;
            flair_ner_node = spawn node::flair_ner;
            ner_model_dir -[ner_model(model_type="flair_ner")]-> flair_ner_node;
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

9. Creating `walker` name of `train_and_val_flair` for getting parameter from context and calling ability `set_config` and `train` and start training model on new dataset, validate and test

    ```
    ## creating walker 
    walker train_and_val_flair {
        # Take in a training and eval dataset
        has train_file;
        has val_file;
        has test_file;
        has model_name="prajjwal1/bert-tiny";
        has model_type="trfmodel";
        has num_train_epochs=3;
        has batch_size=8;
        has learning_rate=0.02;

        # Train all NER models on the train set
        # and validate them on the val set
        # report accuracy performance on flair NER models
        root {
            take --> node::model_dir;
        }
        model_dir {
            take -->;
        }
    }
    ```
    here we are initialize some default argument and also we are providing all argument from context. it take arguments from context and call ability to set model configuration `set_config` and `train` is for training, val and test model on new datasets.


    Now we commbining all the steps from `2 to 9` in single file `flair_ner.jac`
    ### final Jac Program `flair_ner.jac`

    ```
    node model_dir;
    node flair_ner {
        # load the model actions here
        can ent_ext.set_config, ent_ext.train;


        can set_config with train_and_val_flair entry{
            ent_ext.set_config(
                ner_model = visitor.model_name,
                model_type = visitor.model_type
            );
        }


        can train with train_and_val_flair entry{
            # train the model with a given dataset
            train_data = file.load_json(visitor.train_file);
            val_data = file.load_json(visitor.val_file);
            test_data = file.load_json(visitor.test_file);

            # training model
            ent_ext.train(
                train_data = train_data,
                val_data = val_data,
                test_data = test_data,
                train_params = {
                    "num_epoch": visitor.num_train_epochs.int,
                    "batch_size": visitor.batch_size.int,
                    "LR": visitor.learning_rate.float
                    });
        }
    }


    edge ner_model {
        has model_type;
    }

    graph ner_eval_graph {
        has anchor ner_model_dir;
        spawn {
            ner_model_dir = spawn node::model_dir;
            flair_ner_node = spawn node::flair_ner;
            ner_model_dir -[ner_model(model_type="flair_ner")]-> flair_ner_node;
        }
    }


    walker init {
        root {
        spawn here --> graph::ner_eval_graph; 
        }
    }

    ## creating walker for:
    # Train all NER models on the train set
    # and validate them on the val set
    # and test on test set
    # report accuracy performance on flair NER models

    walker train_and_val_flair {
        # Take in a training and eval dataset
        has train_file;
        has val_file;
        has test_file;
        has model_name="prajjwal1/bert-tiny";
        has model_type="trfmodel";
        has num_train_epochs=3;
        has batch_size=8;
        has learning_rate=0.02;

        root {
            take --> node::model_dir;
        }
        model_dir {
            take -->;
        }
    }
    ```

    ### steps for calling jac program `use case 2` and `train, validate and test entity` on new datasets(train, val, test datasets).
    1. Open terminal and run jaseci by command
        ```
        jsctl -m
        ```
    2. Load the `flair train and entity_detection` Module by run cmd :
        ```
        actions load module jaseci_kit.ent_ext
        ```
    3. Build `flair_ner.jac` by run cmd :
        ```
        jac build flair_ner.jac
        ```
    4. Activate `sentinal` by run cmd:
        ```
        sentinel set -snt active:sentinel -mode ir flair_ner.jir
        ```
    5. `train and validation`: train model on train dataset file and validate and test on validate and test dataset file.
        * ### Input data:
            * `train_file(List(Dict))` : training dataset file
            * `val_file(List(Dict))`: validation datase file
            * `test_file(List(Dict))`: test dataset file
            * `model_name(str)` : `prajjwal1/bert-tiny` or `tars-ner`
            * `model_type(str)` : `trfmodel` or `tars`
            * `num_train_epochs(int)` : `3` (default)
            * `batch_size(int)`: `8`
            * `learning_rate(float)`:`0.02`

        ### Creating Input Datasets
        storing dataset file in directory name `dataset` and put all required file in this

            * train_file : `dataset/train.json`
            ```
            [
                {
                    "context": "He sang a broad repertoire at that house including appearances in the world premieres Ildebrando Pizzetti 's Lo straniero 1930 King Hanóch Ermanno Wolf-Ferrari 's La vedova scaltra 1931 Innkeeper Licinio Refice 's Cecilia 1934 Bishop Urbano and Franco Alfano 's Cyrano de Bergerac 1936 Carbon",
                    "entities": [
                        {
                            "entity_value": "Hanóch",
                            "entity_type": "person-politician",
                            "start_index": 132,
                            "end_index": 138
                        }
                    ]
                },
                {
                    "context": "The show was revived for a reunion of the 63rd Division held at the Statler Hilton Hotel in New York City in July 1965",
                    "entities": [
                        {
                            "entity_value": "Statler Hilton Hotel",
                            "entity_type": "building-hotel",
                            "start_index": 68,
                            "end_index": 88
                        },
                        {
                            "entity_value": "New York City",
                            "entity_type": "location-GPE",
                            "start_index": 92,
                            "end_index": 105
                        }
                    ]
                }
            ]
            ```
            * val_file : `dataset/val.json`
            ```
            [
                {
                    "context": "When reconstruction of the building was complete the rear half of the building was named Budig Hall for then KU Chancellor Gene Budig",
                    "entities": [
                        {
                            "entity_value": "KU",
                            "entity_type": "organization-education",
                            "start_index": 109,
                            "end_index": 111
                        }
                    ]
                },
                {
                    "context": "Nannu 's younger brother Shamsul Haq Monju played as a right-back for the Mohammedan Sporting Club",
                    "entities": [
                        {
                            "entity_value": "Mohammedan Sporting Club",
                            "entity_type": "organization-sportsteam",
                            "start_index": 74,
                            "end_index": 98
                        }
                    ]
                }
            ]
            ```
            * test_file : `dataset/test.json`
            ```
            [
                {
                    "context": "The City of Bradenton talked A 's owner Charlie Finley into staying at McKechnie until",
                    "entities": [
                        {
                            "entity_value": "City of Bradenton",
                            "entity_type": "location-GPE",
                            "start_index": 4,
                            "end_index": 21
                        },
                        {
                            "entity_value": "McKechnie",
                            "entity_type": "organization-sportsleague",
                            "start_index": 71,
                            "end_index": 80
                        }
                    ]
                },
                {
                    "context": "When reconstruction of the building was complete the rear half of the building was named Budig Hall for then KU Chancellor Gene Budig",
                    "entities": [
                        {
                            "entity_value": "KU",
                            "entity_type": "organization-education",
                            "start_index": 109,
                            "end_index": 111
                        }
                    ]
                }
            ]
            ```

    6. Calling walker for `model train and validation` and pass `input data` in context from step 5 by cmd:
        ```
        walker run train_and_val_flair -ctx "{\"train_file\":\"dataset/train.json\",\"val_file\":\"dataset/dev.json\",\"test_file\":\"dataset/test.json\",\"model_name\":\"prajjwal1/bert-tiny\",\"model_type\":\"trfmodel\",\"num_train_epochs\":\"10\",\"batch_size\":\"8\",\"learning_rate\":\"0.02\"}"
        ```

    7. After calling step model training will be started and you will get results on console.
        `Console logs`
        ```
        2022-06-07 19:15:48,039 ----------------------------------------------------------------------------------------------------
        2022-06-07 19:15:48,039 Corpus: "Corpus: 80 train + 20 dev + 20 test sentences"
        2022-06-07 19:15:48,039 ----------------------------------------------------------------------------------------------------
        2022-06-07 19:15:48,040 Parameters:
        2022-06-07 19:15:48,040  - learning_rate: "0.02"
        2022-06-07 19:15:48,041  - mini_batch_size: "8"
        2022-06-07 19:15:48,042  - patience: "3"
        2022-06-07 19:15:48,047  - anneal_factor: "0.5"
        2022-06-07 19:15:48,050  - max_epochs: "10"
        2022-06-07 19:15:48,050  - shuffle: "True"
        2022-06-07 19:15:48,052  - train_with_dev: "False"
        2022-06-07 19:15:48,052  - batch_growth_annealing: "False"
        2022-06-07 19:15:48,053 ----------------------------------------------------------------------------------------------------
        2022-06-07 19:15:48,053 Model training base path: "train\prajjwal1\bert-tiny"
        2022-06-07 19:15:48,054 ----------------------------------------------------------------------------------------------------
        2022-06-07 19:15:48,054 Device: cuda:0
        2022-06-07 19:15:48,058 ----------------------------------------------------------------------------------------------------
        2022-06-07 19:15:48,060 Embeddings storage mode: cpu
        2022-06-07 19:15:48,067 ----------------------------------------------------------------------------------------------------
        2022-06-07 19:15:48,416 epoch 1 - iter 1/10 - loss 1.85155192 - samples/sec: 24.19 - lr: 0.020000
        2022-06-07 19:15:48,730 epoch 1 - iter 2/10 - loss 1.30620119 - samples/sec: 25.56 - lr: 0.020000
        2022-06-07 19:15:49,248 epoch 1 - iter 3/10 - loss 1.06608053 - samples/sec: 15.49 - lr: 0.020000
        2022-06-07 19:15:49,529 epoch 1 - iter 4/10 - loss 0.88059333 - samples/sec: 28.41 - lr: 0.020000
        2022-06-07 19:15:49,823 epoch 1 - iter 5/10 - loss 0.74124464 - samples/sec: 27.23 - lr: 0.020000
        2022-06-07 19:15:50,032 epoch 1 - iter 6/10 - loss 0.68382501 - samples/sec: 38.25 - lr: 0.020000
        2022-06-07 19:15:50,309 epoch 1 - iter 7/10 - loss 0.61733453 - samples/sec: 29.02 - lr: 0.020000
        2022-06-07 19:15:50,566 epoch 1 - iter 8/10 - loss 0.59231687 - samples/sec: 31.28 - lr: 0.020000
        2022-06-07 19:15:50,810 epoch 1 - iter 9/10 - loss 0.56157529 - samples/sec: 32.82 - lr: 0.020000
        2022-06-07 19:15:51,117 epoch 1 - iter 10/10 - loss 0.52164928 - samples/sec: 26.10 - lr: 0.020000
        2022-06-07 19:15:51,118 ----------------------------------------------------------------------------------------------------
        2022-06-07 19:15:51,120 EPOCH 1 done: loss 0.5216 - lr 0.0200000
        2022-06-07 19:15:54,183 DEV : loss 0.07136827294948334 - f1-score (micro avg)  0.0
        2022-06-07 19:15:54,185 BAD EPOCHS (no improvement): 0
        ``` 


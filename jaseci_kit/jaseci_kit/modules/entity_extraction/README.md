### Entity Extraction Using `FLAIR NER(ent_ext)`

### **FLAIR NER**`(ent_ext)` module uses flair named entity recognition architecture. It can either be used zero-shot or few-shot entity recognition.

For this tutorial we are going to leaverage the flair ner `Zero-shot classification` and `Few-shot classification` Use Case

**USE CASE I : [Zero-Shot entity detection](#use-case-i--zero-shot-entity-detection-classify-entity-without-training-ner-data)**
1. Import [flair ner(ent_ext)](#1-import-flair-ner-module-in-jac) module
2. [Classify Entity](#2-classify-entity-)


**USE CASE II : [Few-shot classification(`ent_ext`)](#use-case-ii--few-shot-classification)**
1. Preparing [dataset](#1-creating-input-datasets)
2. Import [flair ner(ent_ext)](#2-import-flair-nerent_ext-module-in-jac) module
3. [Few-shot classification](#3-few-shot-classification-train-test-and-validate-model)


# **Walk through** 
## **USE CASE I** : `Zero-Shot entity detection` Classify entity without training `NER Data`:
### **1. Import Flair Ner Module in jac**
1. Open terminal an run jaseci by cmd
    ```
    jsctl -m
    ```  
2. Load module `ent_ext` in jac by cmd
    ```
    actions load module jaseci_kit.ent_ext
    ```
### **2. Classify Entity** : 
for this tutorial we are going to classify entity text with `flair ner(ent_ext)` module on `tars-ner` pretrained model.

* Creating jac program for **zero-shot(ent_ext)**
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

        `set_config` will get parameter from context and load model in module. its take two argument `model_name(str)` an `model_type(str)`.
        ```
        can set_config with infer_zero_shot entry{
            report ent_ext.set_config(
                ner_model = visitor.model_name,
                model_type = visitor.model_type
            );
        }
        ```

    5. Initializing module `infer_zero_shot` for **zero_shot tokenclassification** inside **flair_ner node**

        `infer_zero_shot` module take two arguments `text` and `labels list` for infer entity.
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

* After combining all the steps from **2 to 9** in single file `zero_shot_ner.jac`
    * **File zero_shot_ner.jac**

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

* steps for calling jac program `use case 1` and `infer_zero_shot entity` from new text.
        
    1. Build `zero_shot_ner.jac` by run cmd
        ```
        jac build zero_shot_ner.jac
        ```
    2. Activate `sentinal` by run cmd:
        ```
        sentinel set -snt active:sentinel -mode ir zero_shot_ner.jir
        ```
    3. `entity_detection`: detects all availabe entities from the provided context
        * ### Input:
            * `model_name`: name of model which we are using for zero-shot entity detection e.g. `tars-ner`
            * `model_type : type of model using in entity detection e.g. `tars` 
            * `text (string)`: context to detect entities.
            * `ner_labels(list of strings)`: List of entities, e.g. `["LOC","PER"]`
            
        * ### output
            * `Result`: Created a json file that stored `input text` and `predicted entities` in result.json file`

    6. Calling walker for `entity_detection` and pass `input data` in context by cmd:
        * `Create Input Data`:-

            * `model_name` : `tars-ner`
            * `model_type` : `tars`
            * `text`: "They had a record of five wins and two losses in Opening Day games at Bennett Park 19 wins and 22 losses at Tiger Stadium and three wins and four losses at Comerica Park for a total home record in Opening Day games of 26 wins and 28 losses"
            * `labels` : ["building", "organization"]

        * `calling walker by cmd:`
            ```
            walker run infer_zero_shot -ctx "{\"model_name\":\"tars-ner\",\"model_type\":\"tars\",\"text\":\"They had a record of five wins and two losses in Opening Day games at Bennett Park 19 wins and 22 losses at Tiger Stadium and three wins and four losses at Comerica Park for a total home record in Opening Day games of 26 wins and 28 losses\",\"labels\":[\"building\", \"organization\"]}"
            ```

    7. After calligg step 6 entity outpu will be stored in `result.json` file 
        ```
        {
            "text": "They had a record of five wins and two losses in Opening Day games at Bennett Park 19 wins and 22 losses at Tiger Stadium and three wins and four losses at Comerica Park for a total home record in Opening Day games of 26 wins and 28 losses",
            "entities": [
                {
                    "entity_text": "Bennett Park",
                    "entity_value": "building",
                    "conf_score": 0.9999510645866394,
                    "start_pos": 70,
                    "end_pos": 82
                },
                {
                    "entity_text": "Tiger Stadium",
                    "entity_value": "building",
                    "conf_score": 0.9999762773513794,
                    "start_pos": 108,
                    "end_pos": 121
                },
                {
                    "entity_text": "Comerica Park",
                    "entity_value": "building",
                    "conf_score": 0.999976634979248,
                    "start_pos": 156,
                    "end_pos": 169
                }
            ]
        }
        ```



## **Use Case II : Few-shot classification**
In Few shot classification we are going train, test and validate `ent_ext` module

### 1. Creating Input Datasets
For `train` `test` and `validation` we are going to prepare dataset we are creating list of dict and storing in json file by name `train.json, validation.json and test.json`
and storing dataset file in directory name `dataset` and put all required file in this.

* **train_file : `dataset/train.json`**
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
* **val_file : `dataset/val.json`**
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
* **test_file : `dataset/test.json`**
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

### **2. Import Flair ner(ent_ext) Module in jac**
1. Open terminal an run jaseci by cmd
    ```
    jsctl -m
    ```  
2. Load module `ent_ext` in jac by cmd
    ```
    actions load module jaseci_kit.ent_ext
    ```
### **3. Few-shot classification `(Train, Test and Validate model)`**

For this tutorial we are going to train the model on train dataset and validate the model on validation dataset and final test model on the test dataset.

* **Creating Jac Program**
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
        **set_config** will take two argument `model_name(str)` an `model_type(str)`.
        and load model for training and validation.

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
        **train** will take 4 parameter describing in upcoming steps [parameter_description](#input-data-for-train-and-validation)

        
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

* **final Jac Program**
    * `flair_ner.jac`
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

* **Steps for calling jac program(`flair_ner.jac`)**
    1. Build `flair_ner.jac` by run cmd :
        ```
        jac build flair_ner.jac
        ```
    2. Activate `sentinal` by run cmd:
        ```
        sentinel set -snt active:sentinel -mode ir flair_ner.jir
        ```
    3. `Create train and validation context`: train model on train dataset file and validate and test on validate and test dataset file.
        * ### Input data for train and validation:
            * `train_file(List(Dict))` : training dataset file
            * `val_file(List(Dict))`: validation datase file
            * `test_file(List(Dict))`: test dataset file
            * `model_name(str)` : `prajjwal1/bert-tiny` or `tars-ner`
            * `model_type(str)` : `trfmodel` or `tars`
            * `num_train_epochs(int)` : `3` (default)
            * `batch_size(int)`: `8`
            * `learning_rate(float)`:`0.02`
    
    4. Calling walker for `model train and validation` and pass `input data` in context from step 3 by cmd:
        ```
        walker run train_and_val_flair -ctx "{\"train_file\":\"dataset/train.json\",\"val_file\":\"dataset/dev.json\",\"test_file\":\"dataset/test.json\",\"model_name\":\"tars-ner\",\"model_type\":\"tars\",\"num_train_epochs\":\"2\",\"batch_size\":\"8\",\"learning_rate\":\"0.02\"}"
    
    5. After calling step 4 model training will be started and you will get results on console.
        `Console logs`
        ```
        2022-06-08 12:00:21,453 ----------------------------------------------------------------------------------------------------
        2022-06-08 12:00:21,453 Corpus: "Corpus: 80 train + 20 dev + 20 test sentences"
        2022-06-08 12:00:21,453 ----------------------------------------------------------------------------------------------------
        2022-06-08 12:00:21,453 Parameters:
        2022-06-08 12:00:21,453  - learning_rate: "0.02"
        2022-06-08 12:00:21,453  - mini_batch_size: "8"
        2022-06-08 12:00:21,453  - patience: "3"
        2022-06-08 12:00:21,453  - anneal_factor: "0.5"
        2022-06-08 12:00:21,453  - max_epochs: "2"
        2022-06-08 12:00:21,453  - shuffle: "True"
        2022-06-08 12:00:21,453  - train_with_dev: "False"
        2022-06-08 12:00:21,453  - batch_growth_annealing: "False"
        2022-06-08 12:00:21,453 ----------------------------------------------------------------------------------------------------
        2022-06-08 12:00:21,453 Model training base path: "train/tars-ner"
        2022-06-08 12:00:21,453 ----------------------------------------------------------------------------------------------------
        2022-06-08 12:00:21,453 Device: cuda:0
        2022-06-08 12:00:21,453 ----------------------------------------------------------------------------------------------------
        2022-06-08 12:00:21,453 Embeddings storage mode: cpu
        2022-06-08 12:00:21,455 ----------------------------------------------------------------------------------------------------
        2022-06-08 12:00:22,631 epoch 1 - iter 1/10 - loss 0.60523161 - samples/sec: 7.19 - lr: 0.020000
        2022-06-08 12:00:23,408 epoch 1 - iter 2/10 - loss 0.51332167 - samples/sec: 10.30 - lr: 0.020000
        2022-06-08 12:00:24,033 epoch 1 - iter 3/10 - loss 0.62513998 - samples/sec: 12.79 - lr: 0.020000
        2022-06-08 12:00:25,106 epoch 1 - iter 4/10 - loss 0.57849901 - samples/sec: 7.46 - lr: 0.020000
        2022-06-08 12:00:26,077 epoch 1 - iter 5/10 - loss 0.54225198 - samples/sec: 8.24 - lr: 0.020000
        2022-06-08 12:00:26,688 epoch 1 - iter 6/10 - loss 0.50653757 - samples/sec: 13.10 - lr: 0.020000
        2022-06-08 12:00:27,573 epoch 1 - iter 7/10 - loss 0.47263640 - samples/sec: 9.04 - lr: 0.020000
        2022-06-08 12:00:28,070 epoch 1 - iter 8/10 - loss 0.45762492 - samples/sec: 16.10 - lr: 0.020000
        2022-06-08 12:00:28,931 epoch 1 - iter 9/10 - loss 0.45796768 - samples/sec: 9.29 - lr: 0.020000
        2022-06-08 12:00:29,892 epoch 1 - iter 10/10 - loss 0.43133600 - samples/sec: 8.33 - lr: 0.020000
        2022-06-08 12:00:29,893 ----------------------------------------------------------------------------------------------------
        2022-06-08 12:00:29,893 EPOCH 1 done: loss 0.4313 - lr 0.0200000
        2022-06-08 12:00:38,203 DEV : loss 0.10980782216621005 - f1-score (micro avg)  0.069
        2022-06-08 12:00:38,203 BAD EPOCHS (no improvement): 0
        2022-06-08 12:00:40,378 saving best model
        2022-06-08 12:00:42,539 ----------------------------------------------------------------------------------------------------
        2022-06-08 12:00:43,461 epoch 2 - iter 1/10 - loss 0.18578914 - samples/sec: 9.71 - lr: 0.020000
        2022-06-08 12:00:44,440 epoch 2 - iter 2/10 - loss 0.24499737 - samples/sec: 8.17 - lr: 0.020000
        2022-06-08 12:00:45,482 epoch 2 - iter 3/10 - loss 0.23535200 - samples/sec: 7.67 - lr: 0.020000
        2022-06-08 12:00:46,256 epoch 2 - iter 4/10 - loss 0.23531097 - samples/sec: 10.34 - lr: 0.020000
        2022-06-08 12:00:46,948 epoch 2 - iter 5/10 - loss 0.23616702 - samples/sec: 11.56 - lr: 0.020000
        2022-06-08 12:00:47,570 epoch 2 - iter 6/10 - loss 0.28713835 - samples/sec: 12.88 - lr: 0.020000
        2022-06-08 12:00:48,801 epoch 2 - iter 7/10 - loss 0.27177298 - samples/sec: 6.50 - lr: 0.020000
        2022-06-08 12:00:49,622 epoch 2 - iter 8/10 - loss 0.25330073 - samples/sec: 9.75 - lr: 0.020000
        2022-06-08 12:00:50,855 epoch 2 - iter 9/10 - loss 0.23808518 - samples/sec: 6.49 - lr: 0.020000
        2022-06-08 12:00:51,468 epoch 2 - iter 10/10 - loss 0.24134582 - samples/sec: 13.05 - lr: 0.020000
        2022-06-08 12:00:51,470 ----------------------------------------------------------------------------------------------------
        2022-06-08 12:00:51,470 EPOCH 2 done: loss 0.2413 - lr 0.0200000
        2022-06-08 12:00:59,574 DEV : loss 0.06216340040996651 - f1-score (micro avg)  0.075
        2022-06-08 12:00:59,574 BAD EPOCHS (no improvement): 0
        2022-06-08 12:01:06,280 saving best model
        2022-06-08 12:01:15,103 ----------------------------------------------------------------------------------------------------
        2022-06-08 12:01:15,104 loading file train/tars-ner/best-model.pt
        2022-06-08 12:01:31,248 0.0698	0.0811	0.075	0.0417
        2022-06-08 12:01:31,248 
        Results:
        - F-score (micro) 0.075
        - F-score (macro) 0.0368
        - Accuracy 0.0417
        By class:
                                       precision    recall  f1-score   support

                 person-artist/author     0.2857    0.4000    0.3333         5
                   organization-other     0.2000    0.1667    0.1818         6
                    person-politician     0.0000    0.0000    0.0000         0
              building-sportsfacility     0.0000    0.0000    0.0000         4
                         location-GPE     0.0000    0.0000    0.0000         5
            organization-sportsleague     0.0000    0.0000    0.0000         2
              organization-sportsteam     0.0000    0.0000    0.0000         4
                 organization-company     0.0000    0.0000    0.0000         1
                        product-other     0.0000    0.0000    0.0000         2
                     building-airport     0.0000    0.0000    0.0000         3
               organization-education     0.0000    0.0000    0.0000         2
                       person-soldier     0.0000    0.0000    0.0000         2
                     product-airplane     0.0000    0.0000    0.0000         1
                        location-road     0.0000    0.0000    0.0000         0

                            micro avg     0.0698    0.0811    0.0750        37
                            macro avg     0.0347    0.0405    0.0368        37
                         weighted avg     0.0710    0.0811    0.0745        37
                          samples avg     0.0417    0.0417    0.0417        37

        2022-06-08 12:01:31,248 ----------------------------------------------------------------------------------------------------

        ```
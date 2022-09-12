### Entity Extraction Using `FLAIR NER(ent_ext)`

### **FLAIR NER**`(ent_ext)` module uses flair named entity recognition architecture. It can either be used `zero-shot` or `few-shot` entity recognition.

For this tutorial we are going to leaverage the flair ner `Zero-shot classification` and `Few-shot classification` Use Case

**USE CASE I : [Zero-Shot entity detection](#use-case-i--zero-shot-entity-detection-classify-entity-without-training-ner-data)**
1. Import [flair ner(ent_ext)](#1-import-flair-ner-module-in-jac) module
2. [Classify Entity](#2-classify-entity-)


**USE CASE II : [Few-shot classification](#use-case-ii--few-shot-classification)**
1. Preparing [dataset](#1-creating-input-datasets)
2. Import [flair ner(ent_ext)](#2-import-flair-nerent_ext-module-in-jac) module
3. [Few-shot classification](#3-few-shot-classification-train-test-and-validate-model)

**[Eperiment and methodology](#experiment-and-methodology)**

# **Walk through** 
## **USE CASE I** : `Zero-Shot entity detection` Classify entity without training `NER Data`:
### **1. Import Flair Ner Module in jac**
1. Open terminal an run jaseci by cmd
    ```
    jsctl -m
    ```  
2. Load module `ent_ext` in jac by cmd
    ```
    actions load module jaseci_ai_kit.ent_ext
    ```
### **2. Classify Entity** : 
For this tutorial we are going to classify entity text with `flair ner(ent_ext)` module on `tars-ner` pretrained model.

* Creating jac program for **zero-shot(ent_ext)**
    1. Create a file by name `zero_shot_ner.jac`

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

    4. Initializing module for `set_config` inside node `flair_ner`

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
        It take arguments from context and call ability to set model configuration `set_config` and `infer_zero_shot` for detecting entity from text and store `result` in `result.json file`


    * **Final jac program `zero_shot_ner.jac`**

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

* Steps for calling jac program `use case 1` and `infer_zero_shot entity` from new text.
        
    1. Build `zero_shot_ner.jac` by run cmd
        ```
        jac build zero_shot_ner.jac
        ```
    2. Activate `sentinal` by run cmd:
        ```
        sentinel set -snt active:sentinel -mode ir zero_shot_ner.jir
        ```
        **Note**: If getting error **`ValueError: badly formed hexadecimal UUID string`** execute only once
        > sentinel register -set_active true -mode ir zero_shot_ner.jir
    3. Module `entity_detection`: detects all availabe entities from the provided context
        * ### Input Data:
            * `model_name`: name of model which we are using for zero-shot entity detection e.g. `tars-ner`
            * `model_type` : type of model using in entity detection e.g. `tars` 
            * `text (string)`: context to detect entities. e.g. "They had a record of five wins and two losses in Opening Day games at Bennett Park 19 wins and 22 losses at Tiger Stadium and three wins and four losses at Comerica Park for a total home record in Opening Day games of 26 wins and 28 losses"
            * `ner_labels(list of strings)`: List of entities, e.g. `["LOC","PER"]`
            
        * ### Output
            * `Result`: Created a json file that stored `input text` and `predicted entities` in result.json file`

    6. Run the following command to execute walker for `entity_detection` and pass [`Input Data`](#input-data) in context.
        ```
        walker run infer_zero_shot -ctx "{\"model_name\":\"tars-ner\",\"model_type\":\"tars\",\"text\":\"They had a record of five wins and two losses in Opening Day games at Bennett Park 19 wins and 22 losses at Tiger Stadium and three wins and four losses at Comerica Park for a total home record in Opening Day games of 26 wins and 28 losses\",\"labels\":[\"building\", \"organization\"]}"
        ```

    7. After executing step 6 entity output will be stored in `result.json` file 
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

For `train` `test` and `validation` we are going to prepare dataset from [Conll2003](https://huggingface.co/datasets/conll2003) dataset, we are creating list of dict and storing in json file by name `train.json, validation.json and test.json`, 
and storing dataset file in directory name `dataset` and put all required file in this.


* **train_file : `dataset/train.json`**
    ```
    [
        {
            "context": "EU rejects German call to boycott British lamb",
            "entities": [
                {
                    "entity_value": "EU",
                    "entity_type": "ORG",
                    "start_index": 0,
                    "end_index": 2
                },
                {
                    "entity_value": "German",
                    "entity_type": "MISC",
                    "start_index": 11,
                    "end_index": 17
                },
                {
                    "entity_value": "British",
                    "entity_type": "MISC",
                    "start_index": 34,
                    "end_index": 41
                }
            ]
        }
    ]
    ```
* **val_file : `dataset/val.json`**
    ```
    [
        {
            "context": "CRICKET LEICESTERSHIRE TAKE OVER AT TOP AFTER INNINGS VICTORY",
            "entities": [
                {
                    "entity_value": "LEICESTERSHIRE",
                    "entity_type": "ORG",
                    "start_index": 8,
                    "end_index": 22
                }
            ]
        }
    ]
    ```
* **test_file : `dataset/test.json`**
    ```
    [
        {
            "context": "The former Soviet republic was playing in an Asian Cup finals tie for the first time",
            "entities": [
                {
                    "entity_value": "Soviet",
                    "entity_type": "MISC",
                    "start_index": 11,
                    "end_index": 17
                },
                {
                    "entity_value": "Asian",
                    "entity_type": "MISC",
                    "start_index": 45,
                    "end_index": 50
                },
                {
                    "entity_value": "Asian",
                    "entity_type": "MISC",
                    "start_index": 45,
                    "end_index": 50
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
    actions load module jaseci_ai_kit.ent_ext
    ```
### **3. Few-shot classification `(Train, Test and Validate model)`**

For this tutorial we are going to train the model on train dataset and validate the model on validation dataset and final test model on the test dataset.

* **Creating Jac Program**
    1. Create a file by name `flair_ner.jac`

    2. Create node `model_dir` and `flair_ner` in `flair_ner.jac` file
        ```
        node model_dir;
        node flair_ner {};
        ```
    3. Initializing node flair_ner and adding abilty `set_config` and `entity_detection`
        ```
        node flair_ner{
            # set ability model configuration and train model
            ent_ext.set_config, can ent_ext.train, ent_ext.entity_detection;
            }
        ```
    4. Initializing module for `set_config` inside node `flair_ner`
        ```
        can set_config with infer_zero_shot entry{
            report ent_ext.set_config(
                ner_model = visitor.model_name,
                model_type = visitor.model_type
            );
        }
        ```
        **set_config** will take two argument `model_name(str)` and `model_type(str)`.
        and load model for training and validation.

    5. Initializing module for `train` and `infer` inside node `flair_ner`
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

        can infer with predict_flair entry{
            report ent_ext.entity_detection(
                text = visitor.text,
                ner_labels = visitor.ner_labels.list
            );
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
        Here we are initialize some default argument and also we are providing all argument from context. it take arguments from context and call ability to set model configuration `set_config` and `train` is for training, val and test model on new datasets.

    10. Creating walker for `predicting` `entities` from trained flair model.
        ```
        # infer
        walker predict_flair{
            has text;
            #declare default labels
            has ner_labels = ["PER","ORG", "LOC", "MISC"];

            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }

        }
        ```


* **Final Jac Program**
    * `flair_ner.jac`
        ```
        node model_dir;
        node flair_ner {
            # load the model actions here
            can ent_ext.set_config, ent_ext.train, ent_ext.entity_detection;


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

            can infer with predict_flair entry{
                report ent_ext.entity_detection(
                    text = visitor.text,
                    ner_labels = visitor.ner_labels.list
                );
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

        # infer
        walker predict_flair{
            has text;
            #declare default labels
            has ner_labels = ["PER","ORG", "LOC", "MISC"];

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
        **Note**: If getting error **`ValueError: badly formed hexadecimal UUID string`** execute only once
        > sentinel register -set_active true -mode ir flair_ner.jir
    3. Create `train and validation context`: train model on train dataset file and validate and test on validate and test dataset file.
        * ### Input data for train and validation:
            * `train_file(List(Dict))` : training dataset file
            * `val_file(List(Dict))`: validation datase file
            * `test_file(List(Dict))`: test dataset file
            * `model_name(str)` : `prajjwal1/bert-tiny` or `tars-ner`
            * `model_type(str)` : `trfmodel` or `tars`
            * `num_train_epochs(int)` : `3` (default)
            * `batch_size(int)`: `8`
            * `learning_rate(float)`:`0.02`
    
    4. Run the following command to execute walker for `model train and validation` and pass [`input data`](#input-data-for-train-and-validation) in context.
        ```
        walker run train_and_val_flair -ctx "{\"train_file\":\"dataset/train.json\",\"val_file\":\"dataset/val.json\",\"test_file\":\"dataset/test.json\",\"model_name\":\"prajjwal1/bert-tiny\",\"model_type\":\"trfmodel\",\"num_train_epochs\":\"10\",\"batch_size\":\"8\",\"learning_rate\":\"0.02\"}"
    
    5. You'll find the following logs in train folder inside model name.
        `Console logs`
        ```
        2022-06-14 10:58:47,583 ----------------------------------------------------------------------------------------------------
        2022-06-14 10:58:47,583 Corpus: "Corpus: 14041 train + 3250 dev + 3453 test sentences"
        2022-06-14 10:58:47,583 ----------------------------------------------------------------------------------------------------
        2022-06-14 10:58:47,583 Parameters:
        2022-06-14 10:58:47,584  - learning_rate: "0.02"
        2022-06-14 10:58:47,584  - mini_batch_size: "128"
        2022-06-14 10:58:47,584  - patience: "3"
        2022-06-14 10:58:47,584  - anneal_factor: "0.5"
        2022-06-14 10:58:47,584  - max_epochs: "10"
        2022-06-14 10:58:47,584  - shuffle: "True"
        2022-06-14 10:58:47,584  - train_with_dev: "False"
        2022-06-14 10:58:47,584  - batch_growth_annealing: "False"
        2022-06-14 10:58:47,584 ----------------------------------------------------------------------------------------------------
        2022-06-14 10:58:47,584 Model training base path: "train/prajjwal1/bert-tiny"
        2022-06-14 10:58:47,584 ----------------------------------------------------------------------------------------------------
        2022-06-14 10:58:47,584 Device: cuda:0
        2022-06-14 10:58:47,584 ----------------------------------------------------------------------------------------------------
        2022-06-14 10:58:47,584 Embeddings storage mode: cpu
        2022-06-14 10:58:47,585 ----------------------------------------------------------------------------------------------------
        2022-06-14 10:59:11,725 epoch 1 - iter 11/110 - loss 0.46690662 - samples/sec: 58.35 - lr: 0.020000
        2022-06-14 10:59:36,854 epoch 1 - iter 22/110 - loss 0.35627199 - samples/sec: 56.04 - lr: 0.020000
        2022-06-14 10:59:56,318 epoch 1 - iter 33/110 - loss 0.32018351 - samples/sec: 72.35 - lr: 0.020000
        2022-06-14 11:00:16,082 epoch 1 - iter 44/110 - loss 0.30274213 - samples/sec: 71.25 - lr: 0.020000
        2022-06-14 11:00:35,760 epoch 1 - iter 55/110 - loss 0.28451030 - samples/sec: 71.56 - lr: 0.020000
        2022-06-14 11:00:58,241 epoch 1 - iter 66/110 - loss 0.26581275 - samples/sec: 62.64 - lr: 0.020000
        2022-06-14 11:01:24,133 epoch 1 - iter 77/110 - loss 0.25145255 - samples/sec: 54.39 - lr: 0.020000
        2022-06-14 11:01:48,914 epoch 1 - iter 88/110 - loss 0.24174765 - samples/sec: 56.82 - lr: 0.020000
        2022-06-14 11:02:15,320 epoch 1 - iter 99/110 - loss 0.23233378 - samples/sec: 53.33 - lr: 0.020000
        2022-06-14 11:02:40,455 epoch 1 - iter 110/110 - loss 0.22324374 - samples/sec: 56.03 - lr: 0.020000
        2022-06-14 11:02:40,455 ----------------------------------------------------------------------------------------------------
        2022-06-14 11:02:40,456 EPOCH 1 done: loss 0.2232 - lr 0.0200000
        2022-06-14 11:04:15,844 DEV : loss 0.08416544854674485 - f1-score (micro avg)  0.1417
        2022-06-14 11:04:15,876 BAD EPOCHS (no improvement): 0
        2022-06-14 11:04:15,922 saving best model
        ..............
        ..............
        ..............

        2022-06-14 11:48:43,609 epoch 10 - iter 11/110 - loss 0.05611527 - samples/sec: 61.04 - lr: 0.020000
        2022-06-14 11:49:06,084 epoch 10 - iter 22/110 - loss 0.05563375 - samples/sec: 62.66 - lr: 0.020000
        2022-06-14 11:49:29,709 epoch 10 - iter 33/110 - loss 0.05567900 - samples/sec: 59.61 - lr: 0.020000
        2022-06-14 11:49:52,993 epoch 10 - iter 44/110 - loss 0.05584901 - samples/sec: 60.48 - lr: 0.020000
        2022-06-14 11:50:16,497 epoch 10 - iter 55/110 - loss 0.05558204 - samples/sec: 59.91 - lr: 0.020000
        2022-06-14 11:50:39,222 epoch 10 - iter 66/110 - loss 0.05536536 - samples/sec: 61.97 - lr: 0.020000
        2022-06-14 11:51:03,463 epoch 10 - iter 77/110 - loss 0.05519602 - samples/sec: 58.09 - lr: 0.020000
        2022-06-14 11:51:27,246 epoch 10 - iter 88/110 - loss 0.05550491 - samples/sec: 59.21 - lr: 0.020000
        2022-06-14 11:51:50,920 epoch 10 - iter 99/110 - loss 0.05559963 - samples/sec: 59.48 - lr: 0.020000
        2022-06-14 11:52:13,645 epoch 10 - iter 110/110 - loss 0.05556217 - samples/sec: 61.97 - lr: 0.020000
        2022-06-14 11:52:13,646 ----------------------------------------------------------------------------------------------------
        2022-06-14 11:52:13,646 EPOCH 10 done: loss 0.0556 - lr 0.0200000
        2022-06-14 11:53:51,555 DEV : loss 0.03640907264452083 - f1-score (micro avg)  0.7614
        2022-06-14 11:53:51,587 BAD EPOCHS (no improvement): 0
        2022-06-14 11:53:51,634 saving best model
        2022-06-14 11:53:51,725 ----------------------------------------------------------------------------------------------------
        2022-06-14 11:53:51,726 loading file train/prajjwal1/bert-tiny/best-model.pt
        2022-06-14 11:53:54,423 No model_max_length in Tokenizer's config.json - setting it to 512. Specify desired model_max_length by passing it as attribute to embedding instance.
        2022-06-14 11:55:30,534 0.7138	0.7305	0.7221	0.6166
        2022-06-14 11:55:30,534 
        Results:
        - F-score (micro) 0.7221
        - F-score (macro) 0.5625
        - Accuracy 0.6166

        By class:
                    precision    recall  f1-score   support

                PER     0.7186    0.8751    0.7892      1617
                LOC     0.7645    0.8118    0.7874      1668
                ORG     0.6902    0.5527    0.6138      1661
                MISC    0.6192    0.6254    0.6223       702
             <STOP>     0.0000    0.0000    0.0000         0

          micro avg     0.7138    0.7305    0.7221      5648
          macro avg     0.5585    0.5730    0.5625      5648
        weighted avg    0.7115    0.7305    0.7164      5648
        samples avg     0.6166    0.6166    0.6166      5648

        ```

    10. Run the following command to execute walker `predict_flair` for predicting entities.
        ```
        walker run predict_flair -ctx "{\"text\":\"Two goals from defensive errors in the last six minutes allowed Japan to come from behind and collect all three points from their opening meeting against Syria\"}"
        ```
        After executing walker `predict_flair` will get output e.g.
        ```
        [
            {
                "entities": [
                    {
                        "entity_text": "Japan",
                        "entity_value": "LOC",
                        "conf_score": 0.9944729208946228,
                        "start_pos": 64,
                        "end_pos": 69
                    },
                    {
                        "entity_text": "Syria",
                        "entity_value": "LOC",
                        "conf_score": 0.9952408075332642,
                        "start_pos": 154,
                        "end_pos": 159
                    }
                ]
            }
        ]
        ```
## **Experiment and methodology**
* **Zero-Shot entity detection**

    Let us further look our `zero-shot entity` detection on [Few-Nerd Dataset](https://ningding97.github.io/fewnerd/), Few-NERD is a large-scale, fine-grained manually annotated named entity recognition dataset, which contains `8 coarse-grained(Major)` types, `66 fine-grained(All)` labels types. Three benchmark tasks are built, one is supervised (Few-NERD (SUP)) and the other two are few-shot (Few-NERD (INTRA) and Few-NERD (INTER)).

    ### **Dataset details**
    | Dataset Name   | train dataset | validation dataset | test dataset |
    | -------------- | ------------- | ------------------ | ------------ |
    | FEW-NERD (SUP) | 131767        | 18824              | 37648        |

    For zero-shot entity-detection we are using flair **tars-ner** model.

    **Results**

    ## Zero-shot performance on FEW-NERD(INTER) test Dataset.
    | Labels | Accuracy    | F1_Score    |
    | ------ | ----------- | ----------- |
    | All    | 0.32053081  | 0.305329825 |
    | Major  | 0.475163372 | 0.447818008 |


    ## Zero-shot performance on FEW-NERD(INTRA) test Dataset.
    | Labels | Accuracy    | F1_Score    |
    | ------ | ----------- | ----------- |
    | All    | 0.143001171 | 0.171142318 |
    | Major  | 0.540210805 | 0.462717092 |


    ## Zero-shot performance on FEW-NERD(SUP) test Dataset.
    | Labels | Accuracy    | F1_Score    |
    | ------ | ----------- | ----------- |
    | All    | 0.105859864 | 0.128166615 |
    | Major  | 0.475106014 | 0.431429256 |

    From this results we will get following insight, if we have number of labels is less, we will get higher accuracy and f1_score.

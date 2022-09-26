# **Fasttext Classifier**

`fast_enc` module uses the facebook's fasttext -- efficient learning of word representations and sentence classification.

This tutorial shows you how to train a `fasttext Classifier` with a custom training loop to categorize sentences.

1. Preparing [dataset](#1-praparing-dataset)
2. Import [fasttext(`fast_enc`)](#2-import-fasttextfastenc-module-in-jac) module in jac
3. [Train](#3-train-the-model) the model
4. [Evaluate](#4-evaluation-of-the-model-effectiveness-) the model's effectiveness
5. Use the trained model to make [predictions](#5-use-the-trained-model-to-make-predictions-br)

# **Walk through** 

### **1. Praparing dataset**
For this tutorial, we are going to leverage the `fasttext Classifier` for sentence classification, which is categorizing an incoming text into a one of predefined intents. for demonstration purpose, we are going to use the SNIPS dataset as an example here. [snips dataset](https://huggingface.co/datasets/snips_built_in_intents).

SNIPS is a popular intent classificawtion datasets that covers intents such as ``
[
    "BookRestaurant",
    "ComparePlaces",
    "GetDirections",
    "GetPlaceDetails",
    "GetTrafficInformation",
    "GetWeather",
    "RequestRide",
    "SearchPlace",
    "ShareCurrentLocation",
    "ShareETA"
]
    ``
We need to do a little data format conversion to create a version of SNIPS that work with our `fasttext Classifier` implemenation.
For this part, we are going to use Python. First, 

1. `Import the dataset` from huggingface [dataset library](https://huggingface.co/datasets/snips_built_in_intents).
    ```python
    # import library
    from datasets import load_dataset
    # load dataset
    dataset = load_dataset("snips_built_in_intents")
    print(dataset["train"][:2])
    ```
    If imported successsfuly, you should see the data format to be something like this
    > {"text": ["Share my location with Hillary's sister", "Send my current location to my father"], "label": [5, 5]}


2. `Converting the format` from the SNIPS out of the box to the format that can be ingested by biencoder.
    ```python
    import pandas as pd
    from sklearn.model_selection import train_test_split
    import json

    # get labels names
    lab = dataset["train"].features["label"].names
    # create labels dictionary
    label_dict = {v: k for v, k in enumerate(lab)}
    # dataset
    dataset = dataset["train"]

    # create dataset function
    def CreateData(data):
        # Create dataframe
        df = pd.DataFrame(data)
        # Map labels dict on label column
        df["label"] = df["label"].apply(lambda x : label_dict[x])
        # grouping text on basis of label
        df = df.groupby("label").agg({"text": "\t".join, "label": "\t".join})
        df["label"] = df["label"].apply(lambda x: x.split("\t")[0])

        # Create data dictionary
        data_dict = {}
        for i in range(len(df)):
            data_dict[df["label"][i]] = df["text"][i].split("\t")
        return data_dict
    # Split dataset: Create train and test dataset and store in json file `train_bi.json` and `test_bi.json` and save to disk.
    # Split dataset in train and test set
    train, test = train_test_split(dataset, test_size=0.2, random_state=42)

    # Create train dataset
    train_data = CreateData(train)
    # write data in json file 'train.json'
    with open("train.json", "w", encoding="utf8") as f:
        f.write(json.dumps(train_data, indent = 4))
        

    # Create test dataset
    test_data = CreateData(test)
    data = {
        "contexts": [],
        "labels": []
        }
    for itm in test_data:
        data["labels"].append(itm)
        data["contexts"].extend(test_data[itm])
    # write data in json file 'test.json'
    with open("test.json", "w", encoding="utf8") as f:
            f.write(json.dumps(data, indent = 4))
    ```
    **The example result format should look something like this.**
    * **train.json**
        ```
        "BookRestaurant": [
            "Book me a table for 2 people at the sushi place next to the show tomorrow night","Find me a table for four for dinner tonight"
            ],
        "ComparePlaces": [
            "What's the cheapest between the two restaurants the closest to my hotel?"
            ]
        ```
    
    * **test.json**
        ```
        {
            {
                "contexts": [
                    "We are a party of 4 people and we want to book a table at Seven Hills for sunset",
                    "Book a table at Saddle Peak Lodge for my diner with friends tonight",
                    "How do I go to Montauk avoiding tolls?",
                    "What's happening this week at Smalls Jazz Club?",
                    "Will it rain tomorrow near my all day event?",
                    "Send my current location to Anna",
                    "Share my ETA with Jo",
                    "Share my ETA with the Snips team"
                ],
                "labels": [
                    "BookRestaurant",
                    "ComparePlaces",
                    "GetDirections",
                    "GetPlaceDetails",
                    "GetTrafficInformation",
                    "GetWeather",
                    "RequestRide",
                    "SearchPlace",
                    "ShareCurrentLocation",
                    "ShareETA"
                ]
            }
        }
        ```
### **2. Import `Fasttext(fast_enc)` module in jac**
1. Open terminal and run jaseci by cmd
    > jsctl -m
2. Load `fast_enc` module in jac by cmd
    > actions load module jaseci_ai_kit.fast_enc

### **3. Train the model**  
For this tutorial, we are going to `train and test` the `fast_enc` for `intent classification` its `train` on snips `train datasets` and `test` on `test dataset`, which is categorizing an incoming text into a one of predefined intents.

* **Creating Jac Program (`train and test` fast_enc)**
    1. Create a file by name `fasttext.jac`
    2. Create node `model_dir` and `fasttext` in `fasttext.jac` file        
        ```
        node model_dir;
        node fasttext {};
        ```
    3. Initializing `node fasttext` and import `train` and `infer` ability inside node.
        ```python
        # import train and infer ability
        can fast_enc.train, fast_enc.predict;
        ```
    4. Initialize module `train` and `test` inside `fatstext node`
        `fast_enc.train` take training argument and start traing `fast_enc` module
        ```python
            can train_fasttext with train_and_test_fasttext entry{
            #Code snippet for training the model
            train_data = file.load_json(visitor.train_file);
            std.out("fasttext training started...",train_data.type, visitor.train_with_existing.bool);
            report fast_enc.train(
                traindata = train_data,
                train_with_existing = visitor.train_with_existing
            );
        }

        can tests with train_and_test_fasttext exit{
            std.out("fasttext validation started...");
            # Use the model to perform inference
            # returns the list of context with the suitable intents
            test_data = file.load_json(visitor.test_file);
            
            resp_data = fast_enc.predict(
                sentences=test_data["contexts"]
            );

            fn = "fasttext_val_result.json";
            file.dump_json(fn, resp_data);
        }
        ```
    5. Initialize module for predict intent on new text
        ```python
        can predict with predict_fasttext entry{        
        # Use the model to perform inference
        resp_data = fast_enc.predict(
            sentences=file.load_json(visitor.test_file)["text"]
            );
        # the infer action returns all the labels with the probability scores
        report [resp_data];
        }
        ```
        **Parameter details**
        * `train`: will be used to train the `fasttext module` on custom dataset
            * Input:
                * `traindata` (Dict): dictionary of candidates and suportting contexts for each candidate
                * `train_with_existing` (bool): if set to `false` train the model from `scratch` otherwise trains `incrementally` 

        * `infer`: will be used to predits the most suitable candidate for a provided context, takes text or embedding 
            * Input:
                * `contexts` (list of strings): context which needs to be classified
            * Return: a dictionary of probability score for each candidate and context 

    
    5. Adding edge name of `enc_model` in `fasttext.jac` file for connecting nodes inside graph.
        ```
        # adding edge
        edge enc_model {
            has model_type;
        }
        ```
    6. Adding graph name of `encoder_graph` for initializing node .
        ```
        graph encoder_graph {
            has anchor enc_model_dir;
            spawn {
                enc_model_dir = spawn node::model_dir;
                fasttext_node = spawn node::fasttext;
                enc_model_dir -[enc_model(model_type="fasttext")]-> fasttext_node;
            }
        }
        ```
    7. Initializing `walker init` for calling graph
        ```
        walker init {
            root {
            spawn here --> graph::encoder_graph; 
            }
        }
        ```
    8. Creating walker name of `train_and_evaluate_fasttext` for getting parameter from **context or default** and calling ability `train and test`.
        ```python
        # Declaring the walker: 
        walker train_and_evaluate_fasttext{
            # the parameters required for training  
            has train_with_existing=false;
            has train_file="train.json";
            has test_file="test.json";    
            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }
        ```
        **Default parameter for train and test fasttext** </br>
        `train_file` : local path of **train.json** file </br>
        `train_with_existing` : **false** </br>
        `test_file` : local path of **test.json** file </br>
    
    9. Declaring walker for `predicting intents` on new text
       
        ``` python
        # Declaring walker for predicting intents on new text
        walker predict_fasttext{
            has test_file = "test_dataset.json";    

            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }            
        ```

        **Final fasttext.jac** program
        ```python
        node model_dir;
        node fasttext{
            # import train and infer ability
            can fast_enc.train, fast_enc.predict;

            can train_fasttext with train_and_test_fasttext entry{
                #Code snippet for training the model
                train_data = file.load_json(visitor.train_file);
                std.out("fasttext training started...",train_data.type, visitor.train_with_existing.bool);
                report fast_enc.train(
                    traindata = train_data,
                    train_with_existing = visitor.train_with_existing
                );
            }
                

            can tests with train_and_test_fasttext exit{
                std.out("fasttext validation started...");
                # Use the model to perform inference
                # returns the list of context with the suitable candidates
                test_data = file.load_json(visitor.test_file);
                
                resp_data = fast_enc.predict(
                    sentences=test_data["contexts"]
                );
                # the infer action returns all the candidate with the confidence scores
                # Iterate through the candidate labels and their predicted scores

                fn = "fasttext_val_result.json";
                file.dump_json(fn, resp_data);
            }

            can predict with predict_fasttext entry{        
            # Use the model to perform inference
            resp_data = fast_enc.predict(
                sentences=file.load_json(visitor.test_file)["text"]
                );
            # the infer action returns all the labels with the probability scores
            report [resp_data];
            }
        }


        # adding edge
        edge enc_model {
            has model_type;
        }

        graph encoder_graph {
            has anchor enc_model_dir;
            spawn {
                enc_model_dir = spawn node::model_dir;
                fasttext_node = spawn node::fasttext;
                enc_model_dir -[enc_model(model_type="fasttext")]-> fasttext_node;
            }
        }

        walker init {
            root {
            spawn here --> graph::encoder_graph; 
            }
        }


        # Declaring the walker: 
        walker train_and_test_fasttext{
            # the parameters required for training  
            has train_with_existing=false;
            has train_file="train.json";
            has test_file="test.json";    
            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }

        # declaring walker for predicting intents on new text
        walker predict_fasttext{
            has test_file = "test_dataset.json";    

            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }
        ```
* **Steps for running `fasttext.jac` programm**
    1. Run the following command to Build `fasttext.jac`
        > jac build fasttext.jac
    2. Run the following command to Activate sentinal
        > sentinel set -snt active:sentinel -mode ir fasttext.jir
    
        **Note**: If getting error **`ValueError: badly formed hexadecimal UUID string`** execute only once
        > sentinel register -set_active true -mode ir fasttext.jir
    3. Run the following command to execute  walker `train_and_test_fasttext` with `default parameter` for training `fast_enc` module.
        > walker run train_and_test_fasttext </br>
    
    4. You'll find the following logs on console

        **training logs**
        ```
        jaseci > walker run train_and_evaluate_fasttext -ctx "{\"train_file\":\"train.json\",\"test_file\":\"test.json\",\"train_with_existing\":\"false\"}"
        Training...
        Wrote 261 sentences to C:\Users\satyam.singh\anaconda3\envs\pytorch\lib\site-packages\jaseci_ai_kit\modules\fasttext\pretrained_model\train.txt
        Read 0M words
        Number of words:  577
        Number of labels: 10
        Progress: 100.0% words/sec/thread:  105638 lr:  0.000000 avg.loss:  1.230422 ETA:   0h 0m 0s
        Saving...

        Model saved to C:\Users\satyam.singh\anaconda3\envs\pytorch\lib\site-packages\jaseci_ai_kit\modules\fasttext\pretrained_model\model.ftz.

        LABELS (10):
        - BookRestaurant
        - GetPlaceDetails
        - GetWeather
        - GetDirections
        - SearchPlace
        - RequestRide
        - ShareETA
        - GetTrafficInformation
        - ComparePlaces
        - ShareCurrentLocation
        fasttext validation started...
        {
        "success": true,
        "report": [
            "Model training Completed"
        ]
        }
        ```
### **4. Evaluation of the model effectiveness** </br>
* Performing model effectiveness on `test.json` dataset

    ```
    Model testing Accuracy :  0.82
    Model testing F1_Score :  0.76

    Model classification Report

                            precision    recall  f1-score   support

            BookRestaurant       1.00      1.00      1.00        14
             ComparePlaces       1.00      0.25      0.40         4
             GetDirections       0.70      1.00      0.82         7
           GetPlaceDetails       0.56      0.90      0.69        10
     GetTrafficInformation       0.80      1.00      0.89         4
                GetWeather       0.88      0.78      0.82         9
               RequestRide       1.00      1.00      1.00         5
               SearchPlace       0.00      0.00      0.00         6
      ShareCurrentLocation       1.00      1.00      1.00         3
                  ShareETA       1.00      1.00      1.00         4

                  accuracy                           0.82        66
                 macro avg       0.79      0.79      0.76        66
              weighted avg       0.78      0.82      0.78        66
    ```

    **Sample Result Data**
    ```
    {
        "I want a table for friday 8pm for 2 people at Katz's Delicatessen": [
            {
                "sentence": "I want a table for friday 8pm for 2 people at Katz's Delicatessen",
                "intent": "BookRestaurant",
                "probability": 0.9759947061538696
            }
        ],
        "I want a table in a good japanese restaurant near Trump tower": [
            {
                "sentence": "I want a table in a good japanese restaurant near Trump tower",
                "intent": "BookRestaurant",
                "probability": 0.830787181854248
            }
        ],
        "Book a table at a restaurant near Times Square for 2 people tomorrow night": [
            {
                "sentence": "Book a table at a restaurant near Times Square for 2 people tomorrow night",
                "intent": "BookRestaurant",
                "probability": 0.9866142272949219
            }
        ],
        "Book a table for today's lunch at Eggy's Diner for 3 people": [
            {
                "sentence": "Book a table for today's lunch at Eggy's Diner for 3 people",
                "intent": "BookRestaurant",
                "probability": 0.9936538934707642
            }
        ]
    }
    ```

### **5. Use the trained model to make predictions** </br>
* Create new input data for prdiction stored in a file for example - `test_dataset.json`</br>
**Input data**
    ```
    {
        "text": [
            "We are a party of 4 people and we want to book a table at Seven Hills for sunset",
            "Is Waldorf Astoria more luxurious than the Four Seasons?"
        ]
    }
    ```

* Run the following command to Executing walker `predict_fasttext`
    ```
    walker run predict_fasttext
    ```
    **Output Result**
    ```
    {
        "We are a party of 4 people and we want to book a table at Seven Hills for sunset": [
            {
                "sentence": "We are a party of 4 people and we want to book a table at Seven Hills for sunset",
                "intent": "BookRestaurant",
                "probability": 0.9151427149772644
            }
        ],
        "Is Waldorf Astoria more luxurious than the Four Seasons?": [
            {
                "sentence": "Is Waldorf Astoria more luxurious than the Four Seasons?",
                "intent": "GetPlaceDetails",
                "probability": 0.34331175684928896
            }
        ]
    }
    ```

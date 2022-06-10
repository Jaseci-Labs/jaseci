#  **Bi-Encoder (`bi_enc`)**
**`bi_enc`** is a arrangement of two encoder modules from BERT, it represents context and candidate separately using twin-structured encoders, it takes contexts and candidates, to predict the best suitable candidate for each context. You can train the module on custom data to behave accordingly. Let's take a deep dive into the trainning culture.


This tutorial shows you how to train a Bi-Encoder with a custom training loop to categorize contexts by candidates. In this you use jaseci(jac) and python.


1. Preparing dataset 
2. Import `Bi-Encoder(bi_enc)` module in jac
3. Train the model
4. Evaluate the model's effectiveness
5. Use the trained model to make predictions


## **Walk through** 

### **1. Praparing dataset**
For this tutorial, we are going to leverage the biencoder for intent classification, which is categorizing an incoming text into a one of predefined intents. for demonstration purpose, we are going to use the SNIPS dataset as an example here. [snips dataset](https://huggingface.co/datasets/snips_built_in_intents).

SNIPS is a popular intent classificawtion datasets that covers intents such as `
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
    `
We need to do a little data format conversion to create a version of SNIPS that work with our biencoder implemenation.
For this part, we are going to use Python. First, 

1. `import the dataset` from huggingface [dataset](https://huggingface.co/datasets/snips_built_in_intents).
    ```python
    # import library
    from datasets import load_dataset
    # load dataset
    dataset = load_dataset("snips_built_in_intents")
    ```
    If imported successsfuly, you should see the data format to be something like this
    > {"text": ["Share my location with Hillary's sister", "Send my current location to my father"], "label": [5, 5]}

2. `Converting the format`: Now are converting the format from the SNIPS out of the box to the format that can be ingested by biencoder.
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
    # write data in json file 'train_bi.json'
    with open("train_bi.json", "w", encoding="utf8") as f:
        f.write(json.dumps(train_data, indent = 4))
        

    # Create test dataset
    test_data = CreateData(test)
    data = {
        "contexts": [],
        "candidates": [],
        "context_type": "text",
        "candidate_type": "text"
        }
    for itm in test_data:
        data["candidates"].append(itm)
        data["contexts"].extend(test_data[itm])
    # write data in json file 'test_bi.json'
    with open("test_bi.json", "w", encoding="utf8") as f:
            f.write(json.dumps(data, indent = 4))
    ```
    **The resulting format should look something like this.**
    * **train_bi.json**
        ```
        "BookRestaurant": [
            "Book me a table for 2 people at the sushi place next to the show tomorrow night","Find me a table for four for dinner tonight"
            ],
        "ComparePlaces": [
            "What's the cheapest between the two restaurants the closest to my hotel?"
            ]
        ```
    
    * **test_bi.json**
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
                "candidates": [
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
                ],
                "context_type": "text",
                "candidate_type": "text"
            }
        }
        ```
### **2. Import `Bi-Encoder(bi_enc)` module in jac**
1. Open terminal and run jaseci by cmd
    > jsctl -m
2. Load `bi_enc` module in jac by cmd
    > actions load module jaseci_kit.bi_enc

### **3. Train the model**  
For this tutorial, we are going to `train and infer` the `biencoder` for `intent classification` its `train` on snips `train datasets` and `infer` on `test dataset`, which is categorizing an incoming text into a one of predefined intents.

**Let's Jump into the coding Section**
* **Creating Jac Program (`train and infer` bi_enc)**
    1. Create a file by name `bi_encoder.jac`
    2. Create node `model_dir` and `bi_encoder` in `bi_encoder.jac` file        
        ```
        node model_dir;
        node bi_encoder {};
        ```
    3. Initializing `node bi_encoder` and import `train` and `infer` ability inside node.
        ```
        # import train and infer ability
        can bi_enc.train, bi_enc.infer;
        ```
    4. Initialize module `train` and `infer` inside `bi_encoder node`
        `bi_enc.train` take training argument and start traing `bi_enc` module
        ```
        can train_bi_enc with train_bi_enc entry{
        #Code snippet for training the model
        train_data = file.load_json(visitor.train_file);
        
        # Train the model 
        report bi_enc.train(
            dataset=train_data,
            from_scratch=visitor.from_scratch,
            training_parameters={
                "num_train_epochs": visitor.num_train_epochs.int
                }
            );
        }

        can infer with train_bi_enc exit{
            # Use the model to perform inference
            # returns the list of context with the suitable candidates
            test_data = file.load_json(visitor.test_file);
            resp_data = bi_enc.infer(
                contexts=test_data["contexts"],
                candidates=test_data["candidates"],
                context_type=test_data["context_type"],
                candidate_type=test_data["candidate_type"]
            );
            # the infer action returns all the candidate with the confidence scores
            # Iterate through the candidate labels and their predicted scores
            result = [];
            for pred in resp_data.list{
                // pred=resp_data[0];
                text = pred["context"];
                max_score = 0;
                max_intent = "";
                for j=0 to j<pred["candidate"].length by j+=1 {
                    if (pred["score"][j] > max_score){
                        max_intent = pred["candidate"][j];
                        max_score = pred["score"][j];
                    }
                }
                result.list::append({
                    "context":text,
                    "predicted intent":max_intent,
                    "Conf_Score":max_score
                    });
            }
            report [result];
        }
        ```
        **Parameter details**
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

    
    5. Adding edge name of `bi_model` in `bi_encoder.jac` file for connecting nodes inside graph.
        ```
        # adding edge
        edge bi_model {
            has model_type;
        }
        ```
    6. Adding graph name of `bi_encoder_graph` for initializing node .
        ```
        graph bi_encoder_graph {
            has anchor bi_model_dir;
            spawn {
                bi_model_dir = spawn node::model_dir;
                bi_encoder_node = spawn node::bi_encoder;
                bi_model_dir -[bi_model(model_type="bi_encoder")]-> bi_encoder_node;
            }
        }
        ```
    7. Initializing `walker init` for calling graph
        ```
        walker init {
            root {
            spawn here --> graph::bi_encoder_graph; 
            }
        }
        ```
    8. Creating walker name of `train_bi_enc` for getting parameter from **context or default** and calling ability `train and infer` bi_encoder.
        ```
        # Declaring the walker: 
        walker train_bi_enc{
            # the parameters required for training    
            has train_file = "train_bi.json";
            has from_scratch = true;
            has num_train_epochs = 20;
            has test_file = "test_bi.json";    

            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }
        ```
        **Default parameter for train and test biencoder** </br>
        `train_file` : local path of **train_bi.json** file </br>
        `from_scratch` : **true** </br>
        `num_train_epochs` : **20** </br>
        `test_file` : local path of **test_bi.json** file </br>
    
        **Final bi_encoder.jac** program
        we are conmbining all steps from **2 to 8** inside **bi_encoder.jac**
        ```python
        node model_dir;
        node bi_encoder{
            # import train and infer ability
            can bi_enc.train, bi_enc.infer;

            can train_bi_enc with train_bi_enc entry{
                #Code snippet for training the model
                train_data = file.load_json(visitor.train_file);
                
                # Train the model 
                report bi_enc.train(
                    dataset=train_data,
                    from_scratch=visitor.from_scratch,
                    training_parameters={
                        "num_train_epochs": visitor.num_train_epochs.int
                        }
                    );
                }

            can infer with train_bi_enc exit{
                # Use the model to perform inference
                # returns the list of context with the suitable candidates
                test_data = file.load_json(visitor.test_file);
                resp_data = bi_enc.infer(
                    contexts=test_data["contexts"],
                    candidates=test_data["candidates"],
                    context_type=test_data["context_type"],
                    candidate_type=test_data["candidate_type"]
                );
                # the infer action returns all the candidate with the confidence scores
                # Iterate through the candidate labels and their predicted scores

                result = [];
                for pred in resp_data.list{
                    // pred=resp_data[0];
                    text = pred["context"];
                    max_score = 0;
                    max_intent = "";
                    for j=0 to j<pred["candidate"].length by j+=1 {
                        if (pred["score"][j] > max_score){
                            max_intent = pred["candidate"][j];
                            max_score = pred["score"][j];
                        }
                    }
                    result.list::append({
                        "context":text,
                        "predicted intent":max_intent,
                        "Conf_Score":max_score
                        });
                }
                report [result];
            }
        }


        # adding edge
        edge bi_model {
            has model_type;
        }

        graph bi_encoder_graph {
            has anchor bi_model_dir;
            spawn {
                bi_model_dir = spawn node::model_dir;
                bi_encoder_node = spawn node::bi_encoder;
                bi_model_dir -[bi_model(model_type="bi_encoder")]-> bi_encoder_node;
            }
        }

        walker init {
            root {
            spawn here --> graph::bi_encoder_graph; 
            }
        }


        # Declaring the walker: 
        walker train_bi_enc{
            # the parameters required for training    
            has train_file = "train_bi.json";
            has from_scratch = true;
            has num_train_epochs = 20;
            has test_file = "test_bi.json";    

            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }
        ```
    **Steps for running `bi_encoder.jac` programm**
    1. Build `bi_encoder.jac` by run cmd
        > jac build bi_encoder.jac
    2. Activate sentinal by run cmd
        > sentinel set -snt active:sentinel -mode ir bi_encoder.jir
    3. Calling walker `train_bi_enc` with `default parameter` for training `bi_enc` module by cmd
        > walker run train_bi_enc </br>
    
    After `3 step` running logging will shown on console </br>
    **`training logs`**
    ```
    jaseci > walker run train_bi_enc
    Saving non-shared model to : modeloutput
    non shared model created
    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 33/33 [00:13<00:00,  2.42it/s]
    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 33/33 [00:13<00:00, 14.12it/s]

                Epoch : 1
                loss : 0.11524221436543898
                LR : 0.000891891891891892

    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 33/33 [00:01<00:00, 21.54it/s]
    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 33/33 [00:01<00:00, 21.42it/s]

                Epoch : 2
                loss : 0.030822114031197445
                LR : 0.0006689189189189189

    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 33/33 [00:01<00:00, 20.99it/s]
    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 33/33 [00:01<00:00, 20.67it/s]

                Epoch : 3
                loss : 0.016803985327538667
                LR : 0.000445945945945946

    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 33/33 [00:01<00:00, 19.98it/s]
    97%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊     | 32/33 [00:01<00:00, 19.59it/s]

                Epoch : 4
                loss : 0.011880970348350027
                LR : 0.000222972972972973

    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 33/33 [00:04<00:00,  8.16it/s]
    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 33/33 [00:04<00:00,  6.06it/s]

                Epoch : 5
                loss : 0.010109249611780273
                LR : 0.0

    Epoch: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:22<00:00,  4.49s/batch]
    
    ```

    **Inference `result` on `test_bi.json`**
    ```
     [
        {
          "context": "We are a party of 4 people and we want to book a table at Seven Hills for sunset",
          "predicted intent": "BookRestaurant",
          "Conf_Score": 6.875568016339256
        },
        {
          "context": "Book a table at Saddle Peak Lodge for my diner with friends tonight",
          "predicted intent": "BookRestaurant",
          "Conf_Score": 8.29900637832673
        },
        {
          "context": "How do I go to Montauk avoiding tolls?",
          "predicted intent": "GetDirections",
          "Conf_Score": 2.9064500455793087
        },
        {
          "context": "What's happening this week at Smalls Jazz Club?",
          "predicted intent": "GetWeather",
          "Conf_Score": 5.134972962952694
        },
        {
          "context": "Will it rain tomorrow near my all day event?",
          "predicted intent": "GetWeather",
          "Conf_Score": 13.8709731523643
        },
        {
          "context": "Send my current location to Anna",
          "predicted intent": "ShareCurrentLocation",
          "Conf_Score": 13.069706572586623
        },
        {
          "context": "Share my ETA with Jo",
          "predicted intent": "ShareETA",
          "Conf_Score": 13.607459699093246
        },
        {
          "context": "Share my ETA with the Snips team",
          "predicted intent": "ShareETA",
          "Conf_Score": 10.038374795126789
        }
      ]
    ```
    
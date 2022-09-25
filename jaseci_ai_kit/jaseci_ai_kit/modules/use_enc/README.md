# **USE Encoder (`use_enc`)**

Module **`use_enc`** uses the universal sentence encoder to generate sentence level embeddings. The sentence level embeddings can then be used to calculate the similarity between two given text via cosine similarity and/or dot product.

For this tutorial we are going to leverage the `Use encoder` for **Zero-shot text classification**.



1. Preparing [dataset](#1-praparing-dataset) for evaluation
2. Import [Use-Encoder(use_enc)](#2-import-use-encoderuse_enc-module-in-jac) module in jac
3. Evaluate the models [effectiveness](#3-evaluate-the-models-effectiveness)

# **Walk through**

## **1. Praparing dataset**
For this tutorial, we are going to leverage the `use_encoder` for text classification, which is categorizing an incoming text into a one of predefined class. for demonstration purpose, we are going to use the SNIPS dataset as an example here. [snips dataset](https://huggingface.co/datasets/snips_built_in_intents).

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
We need to do a little data format conversion to create a version of SNIPS that work with our `use_encoder` implemenation.
For this part, we are going to use Python. First, 

1. `Import the dataset` from huggingface [dataset library](https://huggingface.co/datasets/snips_built_in_intents).
    ```python
    # import library
    from datasets import load_dataset
    # load dataset
    dataset = load_dataset("snips_built_in_intents")
    print(dataset["train"][:2])
    ```
    If imported successsfuly, you should see the data format to be something like this in output

    > {"text": ["Share my location with Hillary's sister", "Send my current location to my father"], "label": [5, 5]}

2. `Converting the format` from the SNIPS out of the box to the format that can be ingested by use_encoder.
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
    # Split dataset: Create test dataset and store in json file `test.json` and save to disk.
    _, test = train_test_split(dataset, test_size=0.2, random_state=42)

    # Create test dataset
    test_data = CreateData(test)

    data = []
    classes = []
    for itms in test_data:
        if itms not in classes:
            classes.append(itms)
        for text in test_data[itms]:
            data.append({
                "text": text,
                "class":itms
                })
    test_dataset = {"text":data, "classes":classes}
    # write data in json file 'test.json'
    with open("test.json", "w", encoding="utf8") as f:
            f.write(json.dumps(test_dataset, indent = 4))
    ```
    **The resulting format should look something like this.**
   * **test.json**

        ```
		{
			"text": [
				{
					"text": "Book a table at Galli for 6 people tonight",
					"class": "BookRestaurant"
				},
				{
					"text": "What's the best hotel between Soho Grand and Paramount Hotel?",
					"class": "ComparePlaces"
				},
				{
					"text": "Give me transit directions from Grand Central to Brooklyn bridge",
					"class": "GetDirections"
				},
				{
					"text": "What's today's menu at The Water Club?",
					"class": "GetPlaceDetails"
				},
				{
					"text": "Should I expect traffic from here to Kennedy international airport?",
					"class": "GetTrafficInformation"
				},
				{
					"text": "What will the weather be like tomorrow morning?",
					"class": "GetWeather"
				},
				{
					"text": "I need an Uber right now",
					"class": "RequestRide"
				},
				{
					"text": "Find me the closest theatre for tonight",
					"class": "SearchPlace"
				},
				{
					"text": "Share my location to mum until I get to school",
					"class": "ShareCurrentLocation"
				},
				{
					"text": "Send my time of arrival to Nina",
					"class": "ShareETA"
				}
			],
			"classes": [
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
        ```

##  **2. Import USE-Encoder(use_enc) module in jac**
1. Open terminal and run jaseci by follow command.
   ```
   jsctl -m
   ```

2. Load `use_enc` module in jac by command
    ```
    actions load module jaseci_ai_kit.use_enc
    ```

## **3. Evaluate the models effectiveness**
For this tutorial, we are going to `evaluation of text classification` with `use_encoder` for intent classification its tested on snips test dataset, which is categorizing an incoming text into a one of predefined class.

* **Creating Jac Program (evaluation use_enc)**
    1. Create a file by name use_enc.jac

    2. Create node model_dir and use_encoder in use_enc.jac file
        ```
        node model_dir;
        node use_encoder {};
        ```

    3. Initializing node use_encoder and import text classify train and infer ability inside node.
        ```python
        # import ability
        can use.text_similarity, use.text_classify;
        ```
    4. Initialize module eval_text_classification inside use_encoder node.
        ```python
        # classify text amd evaluate text classification
        can eval_text_classification with eval_text_classification entry{
            test_data = file.load_json(visitor.test_file);
            classes = test_data["classes"];
            result = [];
            for itm in test_data["text"]{
                text = itm["text"];
                class_true = itm["class"];
                resp = use.text_classify(
                    text = text,
                    classes = classes.list
                    );
                result.list::append({"text":text,"class_true":class_true,"class_pred":resp["match"]});
            }
            fn = "result_use_enc.json";
            file.dump_json(fn, result);        
        }
        ```
        **Parameter details**

        * Input:
            * `text` (string): text to classify
            * `classes` (list of strings): candidate classification classes
        * output:
            * `dict` will contain `matching class` ,`match index` and `score`

        for the evaluation we are passing here test data file e.g. `test.json` for evaluation.

    5. Adding edge name of `use_model` in `use_enc.jac` file for connecting nodes inside graph.

        ```
        # adding edge
        edge use_model {
            has model_type;
        }        
        ```
    
    6. Adding graph name of `use_encoder_graph` for initializing node .
        ```
        graph use_encoder_graph {
            has anchor use_model_dir;
            spawn {
                use_model_dir = spawn node::model_dir;
                use_encoder_node = spawn node::use_encoder;
                use_model_dir -[use_model(model_type="use_encoder")]-> use_encoder_node;
            }
        }
        ```

    7. Initializing walker init for calling graph
        ```
        walker init {
            root {
            spawn here --> graph::use_encoder_graph; 
            }
        }
        ```
    8. Creating walker name of `eval_text_classification` for getting parameter from context or default and calling ability `text_classify`.
        ```
        # Declaring the walker: 
        walker eval_text_classification{ 
            has test_file="test.json";
            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }
        ```

        **Final use_enc.jac program**
        ```python
        node model_dir;
        node use_encoder{
            # import all module ability
            can use.text_classify;

            # evaluate text classification
            can eval_text_classification with eval_text_classification entry{
                test_data = file.load_json(visitor.test_file);
                classes = test_data["classes"];
                result = [];
                for itm in test_data["text"]{
                    text = itm["text"];
                    class_true = itm["class"];
                    resp = use.text_classify(
                        text = text,
                        classes = classes.list
                        );
                    result.list::append({"text":text,"class_true":class_true,"class_pred":resp["match"]});
                }
                fn = "result_use_enc.json";
                file.dump_json(fn, result);        
            }
        }

        # adding edge
        edge use_model {
            has model_type;
        }

        # creating graph
        graph use_encoder_graph {
            has anchor use_model_dir;
            spawn {
                use_model_dir = spawn node::model_dir;
                use_encoder_node = spawn node::use_encoder;
                use_model_dir -[use_model(model_type="use_encoder")]-> use_encoder_node;
            }
        }

        # initialize init walker
        walker init {
            root {
            spawn here --> graph::use_encoder_graph; 
            }
        }


        # Declaring the walker fro calling : 
        walker eval_text_classification{ 
            has test_file="test.json";
            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }
        ```
    **Steps for running use_enc.jac program**
    * Execute the follow command for Build `use_enc.jac`
        ```
        jac build use_enc.jac
        ```

    * Execute the follow command to Activate sentinal
        ```
        sentinel set -snt active:sentinel -mode ir use_enc.jir
        ```
        **Note**: If getting error **`ValueError: badly formed hexadecimal UUID string`** execute only once
        > sentinel register -set_active true -mode ir use_enc.jir
    * Execute the walker `eval_text_classification` with default parameter for evaluation `use_enc` module by following command
        ```
        walker run eval_text_classification
        ```
    After executing walker `eval_text_classification` result data will store in file `result_use_enc.json` in your current local path.

    **Evaluation Result**
    ```
    Evaluation accuracy score        :  0.0303
    Evaluation F1_score              :  0.0495

    Evaluation classification_report : 
    
                            precision    recall  f1-score   support

            BookRestaurant       0.00      0.00      0.00        17
             ComparePlaces       0.50      0.33      0.40         3
             GetDirections       0.06      0.33      0.10         3
           GetPlaceDetails       0.00      0.00      0.00        13
     GetTrafficInformation       0.00      0.00      0.00         1
                GetWeather       0.00      0.00      0.00        13
               RequestRide       0.00      0.00      0.00         2
               SearchPlace       0.00      0.00      0.00         5
      ShareCurrentLocation       0.00      0.00      0.00         4
                  ShareETA       0.00      0.00      0.00         5

                  accuracy                           0.03        66
                 macro avg       0.06      0.07      0.05        66
              weighted avg       0.03      0.03      0.02        66
    ```
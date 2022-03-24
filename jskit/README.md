
# What is JSKit ? 
JSKit contains the SOTA models that's made readily available for production usage. Let's look at the available models and there usage.

## 1. Encoders
Encoders module can be used for intent classification, it contains the Bi-Encoder and Poly-Encoder(coming soon) models.

### 1.1. List of API's  available
 #### **cosine_sim** - to calculate the similarity between two List of embeddings
 Request :
 
    requests.post(
            "/cosine_sim/",
            json={
                    "vec_a":  [-0.1938219964504242,..........],
                    "vec_b": [-0.18731489777565002,,..........],
                    "meta": "default"
                }
            )
Response:

    0.90

 #### **train** - for training the model in production environment
 Request : 
    
    requests.post(
                "/train/",
                json={
                    "contexts":[
                        "add godmusic to my latin dance cardio playlist",
                        "add godmusic to my latin dance cardio playlist"
                    ],
                    "candidates":[
                        "addtoplaylist",
                        "getweather"
                    ],
                    "labels ":[
                        1,
                        0
                    ]
                }
            )
Response :

    "Model Training is complete."

 #### **infer** - to get the best matching candidate from the list provided 
 Request :

    requests.post(
                "/infer/",
                json={
                    "contexts":[
                        "What is the cheapest restaurant between Balthazar and Lombardi's?"
                    ],
                    "candidates":[
                        'searchplace',
                        'getplacedetails',
                        'bookrestaurant',
                        'gettrafficinformation',
                        'compareplaces',
                        'sharecurrentlocation',
                        'requestride',
                        'getdirections',
                        'shareeta',
                        'getweather'
                    ]
                }
            )
    
Response: 

    "bookrestaurant" 

 #### **get_context_emb** - to get the embedding for contexts data
 Request :

    requests.post(
                "/get_context_emb/",
                json={
                    "contexts": ["i give this current textbook a rating value of 1 and a best rating of 6"]
                    }
                )
Response : 

    [-0.1938219964504242,..........]

 #### **get_candidate_emb** - for getting the embedding for candidates data
 Request :
    
    requests.post(
                "/get_candidate_emb/",
                json={
                    "candidates": ["RateBook"]
                    }
                )
Response :

    [-0.18731489777565002,,..........]

 #### **set_config** - for setting the model and training parameters
Request : 

     requests.post(
                "/set_config/",
                json={
                    "training_parameters": {
                        "MAX_CONTEXTS_LENGTH": "128",
                        "MAX_CANDIDATE_LENGTH": "64",
                        "TRAIN_BATCH_SIZE": "8",
                        "LEARNING_RATE": "0.00005",
                        "WEIGHT_DECAY": "0.1",
                        "WARMUP_STEPS": "2000",
                        "ADAM_EPSILON": "0.00000008",
                        "MAX_GRAD_NORM": "1",
                        "NUM_TRAIN_EPOCHS": "20",
                        "SEED": "12345",
                        "GRADIENT_ACCUMULATION_STEPS": "1"
                    },
                    "model_parameters": {
                        "SHARED": "False", // if shared is false we use Siamese Model
                        "MODEL_NAME": "bert-base-uncased" 
                    }
                }

            )
Response :
    
    "Config setup is complete."

 #### **save_model** - for saving the model to a provided path
Request : 
    
    requests.post(
                "/save_model/",
                json={
                    "model_path": "mypath"
                    }
                )
Response : 
    
    "[Saved model at] : mypath" 

 #### **load_model** - for loading the model from the provided path
Request :
    
    requests.post(
                "/load_model/",
                json={
                    "model_path": "mypath"
                    }
                )
Response: 
    
    "[loaded model from] : mypath" 

### 1.2. Addtional Instructions

1. You can set the use all model that are available on huggingface.co model library,that can be used with AutoModel
2. Load and save models only take alphanumeric text
3. cosine_sim API expects both embedding provided should be of same length 
4.  Resetting the model parameter through set_config api stores the live model in default location and reloads the fresh pretrainted model from Library  

## 2. Entity Extraction
Entity Extraction module can be used to detect entities from the given context, it has two models one based on transformers and another on RNN architecture. These models will be used for extracting entities from the context.


### 2.1. List of API's  available

 1. #### **entity_detection** - used to detect provided entities in the context 
 Request :
 
    requests.post(
            "/entity_detection/",
            json={
                    "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
                    "ner_labels": ["University", "City", "Country"]
                }
            )
Response:

    {
    "input_text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "entities": [
        {
            "entity_text": "Humboldt University of Berlin",
            "entity_value": "University",
            "conf_score": 0.9708927571773529,
            "start_pos": 4,
            "end_pos": 33
        },
        {
            "entity_text": "Berlin",
            "entity_value": "City",
            "conf_score": 0.9977847933769226,
            "start_pos": 49,
            "end_pos": 55
        },
        {
            "entity_text": "Germany",
            "entity_value": "Country",
            "conf_score": 0.9997479319572449,
            "start_pos": 57,
            "end_pos": 64
        }
    ]
}

 #### **train** - used to train the model on new entities
 Request :
 
    requests.post(
            "/train/",
            json= {
                    "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
                    "entity": [
                        {
                            "entity_value": "Humboldt University of Berlin",
                            "entity_name": "University",
                            "start_index": 4,
                            "end_index": 33
                        },
                        {
                            "entity_value": "Berlin",
                            "entity_name": "City",
                            "start_index": 49,
                            "end_index": 55
                        },
                        {
                            "entity_value": "Germany",
                            "entity_name": "Country",
                            "start_index": 57,
                            "end_index": 64
                        }
                    ]
                }
            )
Response:

    "Model Training is Completed"

 #### **set_config** - Updates the configuration file with new model parameters
Request : 
    
    requests.post(
                "/set_config/",
                json={
                    "ner_model": "ner",
                    "model_type": "LSTM"
                    }
                )
Response :
    
    "Config setup is complete."

 #### **save_model** - for saving the model to the provided path
Request : 
    
    requests.post(
                "/save_model/",
                json={
                    "model_path": "mypath"
                    }
                )
Response : 
    
    "[Saved model at] : mypath" 

 #### **load_model** - for loading the model from the provided path
Request :
    
    requests.post(
                "/load_model/",
                json={
                    "model_path": "mypath"
                    }
                )
Response: 
    
    "[loaded model from] : mypath" 


### 2.2. Addtional Instructions
Parameter available for config setup

    ner_model types:
        1. Pre-trained LSTM / GRU : ["ner", "ner-fast","ner-large"]
        2. Huggingface model : all available models that can be intialized with AutoModel
        3. None : for load a RNN model from scratch
   
    model_type :
        1. "TRFMODEL" : for huggingface models
        2. "LSTM" or "GRU" : RNN models


## 3. Text Segmenter
Text Segmenter module has the ability to split text in multiple pragraph  depending on semantics similarity. 


### 3.1. List of API's  available
 #### **get_segements** - splits the text into mutiple segements as per the threshold provided, the value of thresold can be [ 0 - 1 ] where `0` would return entire text as it is and `1` would split text in sentences. 
Request : 
    
    requests.post(
                "/get_segements/",
                json={
                    "text": "Both men lowered the temperature of air until it liquefied and then distilled the component gases by boiling them off one at a time and capturing them. Later, in 1901, oxyacetylene welding was demonstrated for the first time by burning a mixture of acetylene and compressed O2. This method of welding and cutting metal later became common.Highly combustible materials that leave little residue, such as wood or coal, were thought to be made mostly of phlogiston; whereas non-combustible substances that corrode, such as iron, contained very little. Air did not play a role in phlogiston theory, nor were any initial quantitative experiments conducted to test the idea; instead, it was based on observations of what happens when something burns, that most common objects appear to become lighter and seem to lose something in the process. The fact that a substance like wood gains overall weight in burning was hidden by the buoyancy of the gaseous combustion products. Indeed, one of the first clues that the phlogiston theory was incorrect was that metals, too, gain weight in rusting (when they were supposedly losing phlogiston).",
                    "threshold": 0.95
                    }
                )
Response : 
    
    [
    "Both men lowered the temperature of air until it liquefied and then distilled the component gases by boiling them off one at a time and capturing them. Later, in 1901, oxyacetylene welding was demonstrated for the first time by burning a mixture of acetylene and compressed O2.",
    "This method of welding and cutting metal later became common. Highly combustible materials that leave little residue, such as wood or coal, were thought to be made mostly of phlogiston; whereas non-combustible substances that corrode, such as iron, contained very little. Air did not play a role in phlogiston theory, nor were any initial quantitative experiments conducted to test the idea; instead, it was based on observations of what happens when something burns, that most common objects appear to become lighter and seem to lose something in the process.",
    "The fact that a substance like wood gains overall weight in burning was hidden by the buoyancy of the gaseous combustion products. Indeed, one of the first clues that the phlogiston theory was incorrect was that metals, too, gain weight in rusting (when they were supposedly losing phlogiston)."
    ]

 #### **load_model** - for loading the model from options : [ `wiki`, `legal` ]
Request :
    
    requests.post(
                "/load_model/",
                json={
                        "model_name": "wiki"
                    }
                )
Response: 
    
    "[Model Loaded] : wiki"

### 3. 2. Addtional Instructions
1. Available Parameter for load_model api

        model_name options for Pre-trained LM:
           1. wiki : trained for 3 epochs on wiki727 dataset
           2. legal : trained on legal documents (provides better performace for official docs)
### Unfinished TODOs

1. convert poly encoders to new interface
2. convert flair intent extraction to new interface
3. Get Myca to stop using infer.py (and use date standard actions) then delete

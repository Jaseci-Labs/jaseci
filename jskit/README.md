
# What is JSKit ? 
JSKit contains the SOTA models that's made readily available for production usage. Let's look at the available models and there usage.

## 1. Encoders
Encoders contains the Bi-Encoder and Poly-Encoder(coming soon) models.

### 1.1. List of API's  available
 #### **cosine_sim** - to calculate the similarity between two List of embeddings
    Usage: requests.post(
            "/cosine_sim/",
            json={
                    "vec_a": [<list of embedding vec>],
                    "vec_b": [<list of embedding vec>],
                    "meta": "default"
                }
                )
    Response: < 0.90 >
 #### **train** - for training the model in production environment
    Usage: requests.post(
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
    Response: < "Model Training is complete." >
 #### **get_context_emb** - getting the . 
     Usage: requests.post(
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
    Response: < "bookrestaurant" >

 #### **get_context_emb** - for getting the embedding for contexts data
     Usage: requests.post(
                "/get_context_emb/",
                json={
                    "contexts": ["i give this current textbook a rating value of 1 and a best rating of 6"]
                    }
                )
    Response: < [-0.1938219964504242,..........]>

 #### **get_candidate_emb** - for getting the embedding for candidates data
     Usage: requests.post(
                "/get_candidate_emb/",
                json={
                    "candidates": ["RateBook"]
                    }
                )
    Response: < [-0.18731489777565002,,..........]>

 #### **set_config** - for setting the model and training parameters
     Usage: requests.post(
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
    Response: < "Config setup is complete." >

 #### **save_model** - for saving the model provided a path
     Usage: requests.post(
                "/save_model/",
                json={
                    "model_path": "mypath"
                    }
                )
    Response: < "[Saved model at] : mypath" >

 #### **load_model** - for saving the model provided a path
     Usage: requests.post(
                "/load_model/",
                json={
                    "model_path": "mypath"
                    }
                )
    Response: < "[loaded model from] : mypath" >

### 1.2. Addtional Instructions

1. You can set the use all model that are available on huggingface.co model library,that can be used with AutoModel
2. Load and save models only take alphanumeric text
3. cosine_sim API expects both embedding provided should be of same length 
4.  Resetting the model parameter through set_config api stores the live model in default location and reloads the fresh pretrainted model from Library  

## 2. Entity Extraction

###  


### Unfinished TODOs

1. convert poly encoders to new interface
2. convert flair intent extraction to new interface
3. Get Myca to stop using infer.py (and use date standard actions) then delete

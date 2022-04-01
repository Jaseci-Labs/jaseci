
# What is JSKit ? 
JSKit contains the SOTA models that's made readily available for production usage. Let's look at the available models and there usage.

## 1. Encoders
Encoders module can be used for intent classification, it contains the Bi-Encoder and Poly-Encoder(coming soon) models.

### 1.1. List of API's  available
 #### **cosine_sim** - to calculate the similarity between two List of embeddings
 Request :
``` 
requests.post(
        "/cosine_sim/",
        json={
                "vec_a":  [-0.1938219964504242,..........],
                "vec_b": [-0.18731489777565002,,..........],
                "meta": "default"
            }
        )
```
Response:

```
0.90
```

 #### **dot_prod** - to calculate the dot-product between two List of embeddings
 Request :

 ```
requests.post(
        "/dot_prod/",
        json={
                "vec_a":  [-0.1938219964504242,..........],
                "vec_b": [-0.18731489777565002,,..........]
            }
        )
```
Response:
```
48.023
```
 #### **train** - for training the model in production environment
 Request : 
```
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
```
Response :
```
"Model Training is complete."
```
 #### **infer** - to get the best matching candidate from the list provided 
 Request :
```
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
 ```   
Response: 
```
"bookrestaurant" 
```
 #### **get_context_emb** - to get the embedding for contexts data
 Request :
```
requests.post(
            "/get_context_emb/",
            json={
                "contexts": ["i give this current textbook a rating value of 1 and a best rating of 6"]
                }
            )
```
Response : 
```
[-0.1938219964504242,..........]
```
 #### **get_candidate_emb** - for getting the embedding for candidates data
 Request :
```    
requests.post(
            "/get_candidate_emb/",
            json={
                "candidates": ["RateBook"]
                }
            )
```
Response :
```
[-0.18731489777565002,,..........]
```
 #### **set_train_config** - for setting the training parameters
Request : 

```
requests.post
(
"/set_train_config/",
    json={
        training_parameters:{
            "max_contexts_length": 128,
            "max_candidate_length": 64,
            "train_batch_size": 8,
            "eval_batch_size": 2,
            "max_history": 4,
            "learning_rate": 0.01,
            "weight_decay": 0.1,
            "warmup_steps": 2000,
            "adam_epsilon": 8e-08,
            "max_grad_norm": 1,
            "num_train_epochs": 10,
            "gradient_accumulation_steps": 1,
            "fp16": false,
            "fp16_opt_level": "O1",
            "gpu": 0,
            "basepath": "logoutput",
            "seed": 12345,
            "device": "cuda"
        }
    }   
)
```
Response :
    
``` 
"Config setup is complete." 
```

 #### **get_train_config** - for getting active training parameters
Request : 

```
requests.post
(
"/get_train_config/",
    json={}   
)
```
Response :
    
``` 
{
  "max_contexts_length": 128,
  "max_candidate_length": 64,
  "train_batch_size": 8,
  "eval_batch_size": 2,
  "max_history": 4,
  "learning_rate": 0.01,
  "weight_decay": 0.1,
  "warmup_steps": 2000,
  "adam_epsilon": 8e-8,
  "max_grad_norm": 1,
  "num_train_epochs": 10,
  "gradient_accumulation_steps": 1,
  "fp16": false,
  "fp16_opt_level": "O1",
  "gpu": 0,
  "basepath": "logoutput",
  "seed": 12345,
  "device": "cuda"
}
```


 #### **get_model_config** - for getting active model parameters
Request : 

```
requests.post
(
"/get_model_config/",
    json={}   
)
```
Response :
    
``` 
{
  "shared": false,
  "model_name": "prajjwal1/bert-tiny",
  "model_save_path": "modeloutput"
}
```


 #### **set_model_config** - for setting the model parameters
Request : 

```
requests.post
(
"/set_train_config/",
    json= {
        "model_parameters : {
            "shared": false,
            "model_name": "prajjwal1/bert-tiny",
            "model_save_path": "modeloutput" 
        }        
    }
)
```
Response :
    
``` 
"Config setup is complete." 
```

 #### **save_model** - for saving the model to a provided path
Request : 
```
requests.post
(
    "/save_model/",
    json={
        "model_path": "mypath"
        }
)
```
Response : 
    
```
"[Saved model at] : mypath"
``` 

 #### **load_model** - for loading the model from the provided path
Request :
```
requests.post
(
    "/load_model/",
        json={
            "model_path": "mypath"
            }
)
```
Response: 
    
    "[loaded model from] : mypath" 

### 1.2. Addtional Instructions

1. You can use all model that are available on huggingface.co model library which is compatible with AutoModel
2. Load and save models only accepts alphanumeric and '_' characters
3. cosine_sim API expects both embedding provided should be of same length 
4.  Resetting the model parameter through set_config api stores the live model in default location and reloads the default pretrainted model from huggingface Library  

## 2. Entity Extraction
Entity Extraction module can be used to detect entities from the given context, it has two models one based on transformers and another on RNN architecture. These models will be used for extracting entities from the context.


### 2.1. List of API's  available

#### **entity_detection** - used to detect provided entities in the context 
 Request :
 ```
requests.post(
        "/entity_detection/",
        json={
                "text": "The Humboldt University of Berlin is situated in Berlin, Germany",
                "ner_labels": ["University", "City", "Country"]
            }
        )
```
Response:
```
{
    "input_text": "The Humboldt University of Berlin is situated in Berlin, Germany",
    "entities": 
    [
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
```
#### **train** - used to train the model on new entities
 Request :
 ```
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
```
Response:
```
"Model Training is Completed"
```
 #### **set_config** - Updates the configuration file with new model parameters
Request : 
```    
requests.post(
            "/set_config/",
            json={
                "ner_model": "ner",
                "model_type": "LSTM"
                }
            )
```
Response :
```    
"Config setup is complete."
```
 #### **save_model** - for saving the model to the provided path
Request : 
```    
requests.post(
            "/save_model/",
            json={
                "model_path": "mypath"
                }
            )
```
Response : 
```    
"[Saved model at] : mypath" 
```
 #### **load_model** - for loading the model from the provided path
Request :
```
requests.post(
            "/load_model/",
            json={
                "model_path": "mypath"
                }
            )
```
Response: 
```    
"[loaded model from] : mypath" 
```

### 2.2. Addtional Instructions
Parameter available for config setup
```
    ner_model types:
        1. Pre-trained LSTM / GRU : ["ner", "ner-fast","ner-large"]
        2. Huggingface model : all available models that can be intialized with AutoModel
        3. None : for load a RNN model from scratch
   
    model_type :
        1. "TRFMODEL" : for huggingface models
        2. "LSTM" or "GRU" : RNN models

```
## 3. Text Segmenter
Text Segmenter module has the ability to split text in multiple pragraph  depending on semantics similarity. 


### 3.1. List of API's  available
 #### **get_segements** - splits the text into mutiple segements as per the threshold provided, the value of thresold can be [ 0 - 1 ] where `0` would return entire text as it is and `1` would split text in sentences. 
Request : 
```    
requests.post(
    "/get_segements/",
    json=
    {
        "text": "Labor statistics do reveal trends initially supportive of Bernard's thesis. From 1950 to 1990, the proportion of men in the labor forced decreased 9.4%, couples with a 28.8% increase of women who were in the labor force, suggesting a challenge to the traditional ideal of men working outside the home and women being relegated to domestic duties only. 200 years ago, having a fever or a cut can become life-threatening very quickly. Vaccines or treatments for many diseases did not exist as well. On the industrial front, progress was slow and time-consuming. Transportation was rather primitive and prohibitively expensive, ensuring that only the rich and famous could use it. The bright inexplicable pink of the tender flaky salmon, with golden olive oil-crisped edges. The deep green of the roasted asparagus calling us towards springtime. The pale yellow of the creamy leek drenched potatoes, speckled with bright pops of chives. I want to know how to use the NTXentLoss as in CPC model. I mean, I have a positive sample and N-1 negative samples. Many people dream about traveling the world for a living; and there are people that are actually able to do so that aren’t pilots, flight attendants, or businessmen. These people are known as travel bloggers and they get paid to visit and write about their major passion in life that is travel.", 
        
        "threshold": 0.85
    }
)
```
Response : 
``` 
[
  "Labor statistics do reveal trends initially supportive of Bernard's thesis. From 1950 to 1990, the proportion of men in the labor forced decreased 9.4%, couples with a 28.8% increase of women who were in the labor force, suggesting a challenge to the traditional ideal of men working outside the home and women being relegated to domestic duties only.",
  "200 years ago, having a fever or a cut can become life-threatening very quickly. Vaccines or treatments for many diseases did not exist as well. On the industrial front, progress was slow and time-consuming. Transportation was rather primitive and prohibitively expensive, ensuring that only the rich and famous could use it.",
  "The bright inexplicable pink of the tender flaky salmon, with golden olive oil-crisped edges. The deep green of the roasted asparagus calling us towards springtime. The pale yellow of the creamy leek drenched potatoes, speckled with bright pops of chives.",
  "I want to know how to use the NTXentLoss as in CPC model. I mean, I have a positive sample and N-1 negative samples.",
  "Many people dream about traveling the world for a living; and there are people that are actually able to do so that aren’t pilots, flight attendants, or businessmen. These people are known as travel bloggers and they get paid to visit and write about their major passion in life that is travel."
]
```
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
   

## 4. Fasttext
FastText is an implentation of the open-source library that allows users to learn text representations and text classifiers. 
### 4.1. List of API's available

#### **train** - used to train the model for new classifiers

Request :
```
requests.post(
    "/train/",
    json={
        "traindata":{
            "travel_time": [
                "do i need to fly a long time from london",
                "Do I need to fly for a long time to arrive in Guyana as a London citizen?"
                ],
            "fees_and_taxes": [
                "I would like to know the taxes due at the departure.",
                "Does this vacation have any fees?"
                ]

        },
        "train_with_existing": false
    }
)
```
Response :
```
"Model training Completed"
```
#### **predict** - used to predict the intent of the sentences.
Request :
```
requests.post(
    "/predict/",
    json={
        "sentences": [
            "how much time it takes to travel from Michigan to Sydney"
        ]
    }
)
```
Response :
```
{
  "how much time it takes to travel to Michigan from Sydney": [
    {
      "sentence": "how much time it takes to travel from Michigan to Sydney",
      "intent": "travel-time",
      "probability": 1.0000100135803223
    }
  ]
}
```
 #### **save_model** - for saving the model to the provided path
Request : 
```    
requests.post(
            "/save_model/",
            json={
                "model_path": "mypath"
                }
            )
```
Response : 
```    
"Model saved to mypath."
```
 #### **load_model** - for loading the model from the provided path
Request :
```
requests.post(
            "/load_model/",
            json={
                "model_path": "mypath"
                }
            )
```
Response: 
```    
"Model Loaded From : mypath" 
```
### 4. 2. Addtional Instructions
1. Training parameter :
```
train_with_existing :
    True : appends the data to the active training set 
    False : creates a new training set with the data provided
```
### 5. USE_QA
use_qa module uses the universal sentence encoder and distance metric to evaluate the distance between question and and probable answers
### 5.1. List of API's available 
#### **question_encode** - encodes the question text and return a embedding of 512 length
Request :
```
requests.post(
    "/question_encode/",
    json={
        "question": "Which city is capital of India?"
    }
)
```
Response: 
```    
[
  [
    0.015976766124367714,
    0.05355389043688774,
    -0.02080559730529785,
    -0.09500843286514282,
    ....,
    ....,
    ....
  ]
]
```
#### **answer_encode** - encodes the answer, context and return a embedding of 512 length
Request :
```
requests.post(         
    "/answer_encode/",
    json={
            "answer": "New Delhi",
            "context": "New Delhi is the capital of India and a part of the National Capital Territory of Delhi (NCT)."
        }
)
```
Response: 
```    
[
  [
    -0.02469351328909397,
    0.018782570958137512,
    -0.030687350779771805,
    -0.03719259053468704,
    ....,
    ....,
    ....
  ]
]
```

#### **cos_sim_score** - calculates the cosine similarity between encodings
Request :
```
requests.post(         
    "/cos_sim_score/",
    json={
        "q_emb":[
            0.015976766124367714,
            0.05355389043688774,
            -0.02080559730529785,
            -0.09500843286514282,
            ....,
            ....,
            ....
        ],
        "a_emb": [
            -0.02469351328909397,
            0.018782570958137512,
            -0.030687350779771805,
            -0.03719259053468704,
            ....,
            ....,
            ....
        ]
    }
)
```
Response: 
```
0.5570200427361625 
```
#### **qa_score** - calculates the inner product between encodings
Request :
```
requests.post(         
    "/qa_score/",
    json={
        "q_emb":[
            0.015976766124367714,
            0.05355389043688774,
            -0.02080559730529785,
            -0.09500843286514282,
            ....,
            ....,
            ....
        ],
        "a_emb": [
            -0.02469351328909397,
            0.018782570958137512,
            -0.030687350779771805,
            -0.03719259053468704,
            ....,
            ....,
            ....
        ]
    }
)
```
Response: 
```   
0.5570200627571644
```

### Unfinished TODOs

1. convert poly encoders to new interface
2. convert flair intent extraction to new interface
3. Get Myca to stop using infer.py (and use date standard actions) then delete

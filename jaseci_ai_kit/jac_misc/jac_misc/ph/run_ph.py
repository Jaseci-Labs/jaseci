import requests
import json
import traceback
try:
    with open("custom.py","r") as fp:
        model_data=fp.read()
    req_json={
        "config":{
            "Model":{
                "args":{
                    "model_args":{
                        "context_bert_model":"distilbert-base-uncased",
                        "candidate_bert_model":"distilbert-base-uncased",
                        "hidden_size":128,
                        "max_sequence_length":128,
                        "max_entity_length":30,
                        "loss_beta":0.6,
                        "start_coef":0.3,
                        "end_coef":0.1,
                        "span_coef":0.6,
                        "unk_entity_type_id":-1,
                        "unk_category":"<UNK>",
                        "descriptions":[
                            "LOC",
                            "PER"
                            ]
                    }
                },
         "type":"CustomModel"
        },
        "Inference":{
            "postprocess": {
                "type": "CustomProcessor",
                "args": {}
            },  
            "preprocess": {
                "type": "CustomProcessor",
                "args": {}
            }
        }
      },
    "python": model_data
    }
    response = requests.post('http://localhost:8000/create_head_list/',json=req_json)
    print(response.status_code)
    if response.status_code==200:
        response = requests.post('http://localhost:8000/create_head/',json={"uuid": "sample","config": {}})
        print(response.status_code)
        print(response.text)
        if response.status_code==200:
            train_json={"uuid":"sample",
            "config":{
                "Trainer":{
                    "name": "CustomTrainer",
                    "trainer":{
                        "epochs": 3
                    },
                    "dataloader": {
                        "args":{
                            "train_args":{
                                "context_bert_model":"distilbert-base-uncased",
                                "hidden_size":128,
                                "max_sequence_length":128,
                                "max_entity_length":30,
                                "unk_entity_type_id":-1,
                                "unk_category":"<UNK>",
                                "descriptions":[
                                    "LOC",
                                    "PER"
                                    ]
                                }
                            },
                        "type": "CustomDataLoader"
                    },
                    "loss":{
                        "args":{
                            "loss_args":{
                                "n_classes":2
                            }
                        },
                    "type": "Loss"
                    }
                }
            }
            }
            response = requests.post('http://localhost:8000/train_head/',json=train_json)
            print(response.status_code)
            print(response.text)
except Exception as e:
    print(f"Exceptions : {e}")
    print(traceback.print_exc())
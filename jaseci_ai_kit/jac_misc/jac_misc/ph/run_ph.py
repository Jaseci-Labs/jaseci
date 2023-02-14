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
                            "Fin_Corp"
                            ]
                    }
                },
         "type":"CustomModel"
        },
        "Inference":{
            "type":"CustomInference"
            # "postprocess": {
            #     "type": "CustomProcessor",
            #     "args": {
                    
            #     }
            # },  
            # "preprocess": {
            #     "type": "CustomProcessor",
            #     "args": {"inf_args":{
            #                     "unk_entity_type_id":-1,
            #                     "unk_category":"<UNK>",
            #                     "max_sequence_length":128,
            #                     "descriptions":[
            #                         "Fin_Corp",
            #                         "PER"
            #                         ]
            #                     }}
            # }
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
                        "epochs": 10,
                        "tensorboard":False
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
                                       "Fin_Corp"
                                    ]
                                }
                            },
                        "type": "CustomDataLoader"
                    },
                    "loss":"custom_loss",
                    "loss_args":{
                        "n_classes":1
                    },
                    "metrics":[]
            }
            }
            }
            response = requests.post('http://localhost:8000/train_head/',json=train_json)
            print(response.status_code)
            print(response.text)
            if response.status_code==200:
                pred_json={"uuid":"sample","data":"What does Site-Built Housing mean?"}
                response = requests.post('http://localhost:8000/predict/',json=pred_json)
                print(response.status_code)
                print(response.text)
except Exception as e:
    print(f"Exceptions : {e}")
    print(traceback.print_exc())
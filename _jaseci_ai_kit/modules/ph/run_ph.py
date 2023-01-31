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
                        "G#protein",
                        "G#DNA"
                        ]
                },
         "type":"CustomModel"
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
except Exception as e:
    print(f"Exceptions : {e}")
    print(traceback.print_exc())
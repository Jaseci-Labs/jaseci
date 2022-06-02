### Example Jac Usage:(model training)
#### Create jac programm (main.jac)


```
node model_dir;
node tfm_ner {
    # train,infer, eval
    can tfm_ner.extract_entity, tfm_ner.train;

    # extracting entities
    can infer with predict_entity_from_tfm entry {
        report tfm_ner.extract_entity(
            text = visitor.text
        );
    }

    ## train and evaluate
    can train_and_eval with train_and_eval_tfm entry {

        train_data = file.load_json(visitor.train_file);
        eval_data = file.load_json(visitor.eval_file);
        test_data = file.load_json(visitor.test_file);
        std.out("corpus : ",train_data.length," train + ",eval_data.length," dev +",test_data.length," test sentences");
        tfm_ner.train(
            mode = visitor.mode,
            epochs = visitor.num_train_epochs.int,
            train_data = train_data,
            dev_data = eval_data,
            test_data = test_data
            );
        std.out("training and evaluation done ");
        }
}




edge ner_model {
    has model_type;
}

graph ner_eval_graph {
    has anchor ner_model_dir;
    spawn {
        ner_model_dir = spawn node::model_dir;
        tfm_ner_node = spawn node::tfm_ner;
        ner_model_dir -[ner_model(model_type="tfm_ner")]-> tfm_ner_node;
    }
}


walker init {
    root {
       spawn here --> graph::ner_eval_graph; 
    }
}

## creating walker 
walker train_and_eval_tfm {
    has train_file;
    has eval_file;
    has test_file;
    has num_train_epochs;
    has mode;

    # Train all NER models on the train set
    # and evaluate them on the eval set
    # report accuracy performance across all NER models
    root {
        take --> node::model_dir;
    }
    model_dir {
        take -->;
    }
}

walker predict_entity_from_tfm{
    has text;

    root {
        take --> node::model_dir;
    }
    model_dir {
        take -->;
    }
}

```
Run jaseci 

```
jsctl
```

To load the Transformer Entity Extraction Module run :
```
actions load module jaseci_kit.tfm_ner
```

Build main.jac by run:

```
jac build main.jac
```

Activate sentinal by run :
```
sentinel set -snt active:sentinel -mode ir main.jir
```

Create train test and dev dataset in this from example format :
### train_file
dataset/train.json 
```
[{
    "context": "However a loophole in the law allowed Buddharakkita and Jayewardene evade the death penalty as the Capital Punishment Repeal Act allowed for a sentence of death to a person convicted for murder committed prior to December 2 1959 and not for the offence of conspiracy to commit murder",
    "entities": [
        {
            "entity_value": "Buddharakkita",
            "entity_type": "person",
            "start_index": 38,
            "end_index": 51
        },
        {
            "entity_value": "Jayewardene",
            "entity_type": "person",
            "start_index": 56,
            "end_index": 67
        },
        {
            "entity_value": "Capital Punishment Repeal Act",
            "entity_type": "event",
            "start_index": 99,
            "end_index": 128
        }
    ]
},
{
    "context": "In 2012 penguin researchers observed that penguins feeding trips were much longer than those taken by the population on Bowen Island in the Jervis Bay Territory",
    "entities": [
        {
            "entity_value": "Bowen Island",
            "entity_type": "location",
            "start_index": 120,
            "end_index": 132
        },
        {
            "entity_value": "Jervis Bay Territory",
            "entity_type": "location",
            "start_index": 140,
            "end_index": 160
        }
    ]
}]
```

### eval_file
dataset/dev.json 

```
[
    {
        "context": "The Stavros Niarchos Foundation Cultural Center inaugurated in 2016 will house the National Library of Greece and the Greek National Opera",
        "entities": [
            {
                "entity_value": "Stavros Niarchos Foundation Cultural Center",
                "entity_type": "building",
                "start_index": 4,
                "end_index": 47
            },
            {
                "entity_value": "National Library of Greece",
                "entity_type": "building",
                "start_index": 83,
                "end_index": 109
            },
            {
                "entity_value": "Greek National Opera",
                "entity_type": "building",
                "start_index": 118,
                "end_index": 138
            }
        ]
    },
    {
        "context": "He was highly critical of Donald Trump during the 2016 Republican Party primaries",
        "entities": [
            {
                "entity_value": "Donald Trump",
                "entity_type": "person",
                "start_index": 26,
                "end_index": 38
            },
            {
                "entity_value": "2016 Republican Party primaries",
                "entity_type": "event",
                "start_index": 50,
                "end_index": 81
            }
        ]
    }
]
```

### test_file
dataset/test.json
```
[
    {
        "context": "The project proponents told the Australian Financial Review in December that year that they had been able to demonstrate that the market for backpacker tourism was less affected by these events and that they intended to apply for an air operator 's certificate in January 2004",
        "entities": [
            {
                "entity_value": "Australian Financial Review",
                "entity_type": "organization",
                "start_index": 32,
                "end_index": 59
            }
        ]
    },
    {
        "context": "German forces attempted to organise a defense using rear-area support units and several divisions hurriedly transferred from Army Group North",
        "entities": [
            {
                "entity_value": "German",
                "entity_type": "location",
                "start_index": 0,
                "end_index": 6
            },
            {
                "entity_value": "Army Group North",
                "entity_type": "organization",
                "start_index": 125,
                "end_index": 141
            }
        ]
    }
]
```

train model with jac by run:
```
walker run train_and_eval_models -ctx "{\"train_file\":\"dataset/train.json\",\"eval_file\":\"dataset/dev.json\",\"test_file\":\"dataset/test.json\",\"num_train_epochs\":\"10\",\"mode\":\"default\"}"
```

### after calling walker will get result on console below format

```
2022-06-01 10:53:21.033712     Training epoch: 1/15
2022-06-01 10:53:21.550641     Training loss per 100 training steps: 2.237579345703125
2022-06-01 10:55:22.277295     Training loss per 100 training steps: 0.5347430409476308
2022-06-01 10:58:01.659007     Training loss epoch: 0.3391421662278511
2022-06-01 10:58:01.659043     Training accuracy epoch: 0.9104983621756423
2022-06-01 10:58:01.659056     Training accuracy epochexcept('O') : 0.5919401402227067
2022-06-01 10:58:01.659079     evaluation loss epoch: 0.09548642354396482
2022-06-01 10:58:01.659088     evaluation accuracy epoch: 0.9743775487732153
2022-06-01 10:58:01.659097     evaluation accuracy epoch except('O') : 0.8941230627589382
2022-06-01 10:58:02.322026     model saved successful to : train/model_save_checkpoint
2022-06-01 10:58:02.322090     Epoch 1 total time taken : 0:04:41.288424
2022-06-01 10:58:02.322105     ------------------------------------------------------------
2022-06-01 10:58:02.322119     Training epoch: 2/15
2022-06-01 10:58:02.866552     Training loss per 100 training steps: 0.09209490567445755
2022-06-01 11:00:13.298555     Training loss per 100 training steps: 0.07785731317973373
2022-06-01 11:02:53.564629     Training loss epoch: 0.07312824366492542
2022-06-01 11:02:53.564664     Training accuracy epoch: 0.9799573343351519
2022-06-01 11:02:53.564679     Training accuracy epochexcept('O') : 0.9126455743435653
2022-06-01 11:02:53.564700     evaluation loss epoch: 0.07342989133515705
2022-06-01 11:02:53.564710     evaluation accuracy epoch: 0.9794031554630792
2022-06-01 11:02:53.564718     evaluation accuracy epoch except('O') : 0.9315636028847629
2022-06-01 11:02:56.476696     model saved successful to : train/model_save_checkpoint
2022-06-01 11:02:56.476761     Epoch 2 total time taken : 0:04:54.154651
2022-06-01 11:02:56.476776     ------------------------------------------------------------
2022-06-01 11:02:56.476791     Training epoch: 3/15
2022-06-01 11:02:57.038975     Training loss per 100 training steps: 0.031212003901600838
2022-06-01 11:05:07.675648     Training loss per 100 training steps: 0.045618000633940836
2022-06-01 11:07:40.095328     Training loss epoch: 0.04381770853552237
2022-06-01 11:07:40.095367     Training accuracy epoch: 0.9882465879142729
2022-06-01 11:07:40.095379     Training accuracy epochexcept('O') : 0.9512166381900665
2022-06-01 11:07:40.095410     evaluation loss epoch: 0.06000439737302562
2022-06-01 11:07:40.095423     evaluation accuracy epoch: 0.9843478724432414
2022-06-01 11:07:40.095437     evaluation accuracy epoch except('O') : 0.9360902255639098
2022-06-01 11:07:43.036175     model saved successful to : train/model_save_checkpoint
2022-06-01 11:07:43.036236     Epoch 3 total time taken : 0:04:46.559454
```

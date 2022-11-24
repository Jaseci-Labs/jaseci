
walker test_train_ner{
    can ent_ext.train;
    train_data=[
        {
            "context": "EU rejects German call to boycott British lamb",
            "entities": [
                {
                    "entity_value": "EU",
                    "entity_type": "ORG",
                    "start_index": 0,
                    "end_index": 2
                },
                {
                    "entity_value": "German",
                    "entity_type": "MISC",
                    "start_index": 11,
                    "end_index": 17
                },
                {
                    "entity_value": "British",
                    "entity_type": "MISC",
                    "start_index": 34,
                    "end_index": 41
                }
            ]
        }
    ];
    train_params={
        "num_epoch": 2,
        "batch_size": 1,
        "LR": 0.02
        };
    report ent_ext.train(train_data=train_data,[],[],train_params=train_params);
}

walker test_extract_entity{
    can ent_ext.entity_detection;
     report ent_ext.entity_detection(text="cricket leicestershire take over at top after innings victory",ner_labels=["PER", "LOC", "ORG"]);
}

walker test_ent_ext_set_config{
    can ent_ext.set_config;
    report ent_ext.set_config(ner_model="prajjwal1/bert-tiny",model_type="TRFMODEL");
}

walker test_ent_ext_load_model{
    can ent_ext.load_model;
    report ent_ext.load_model("modeloutput");
}

walker test_ent_ext_save_model{
    can ent_ext.save_model;
    report ent_ext.save_model("modeloutput");
}
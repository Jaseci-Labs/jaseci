import {*} with "./ai.jac";

node ent_ext:ai_model {
    can ent_ext.entity_detection, ent_ext.train, ent_ext.save_model, ent_ext.load_model;

    can train {
        train_data = file.load_json(visitor.train_file);

        if(visitor.from_scratch) {
            ent_ext.load_model({"default": true});
            here.labels = [];
        }
        for item in train_data {
            for ent in item["entities"] {
                ent_label = ent["entity_type"];
                if (ent_label not in here.labels): here.labels.l::append(ent_label);
            }
        }
        ent_ext.train(
            train_data=train_data,
            val_data=val_data,
            test_data=test_data,
            train_params={
                "num_epoch": (visitor.num_train_epochs).int,
                "batch_size": (visitor.batch_size).int,
                "LR": (visitor.learning_rate).float
            }
        );
        if (visitor.model_name):
            ent_ext.save_model(model_path=visitor.model_name);
    }
    can infer {
        report ent_ext.entity_detection(
            text=input["text"],
            ner_labels=input["labels"]
        );
    }
    # TODO: test ability
    can test_model {

    }
}
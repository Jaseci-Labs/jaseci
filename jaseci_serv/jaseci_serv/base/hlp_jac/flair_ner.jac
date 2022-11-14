node flair_ner {
    has pretrained = {
        "tinybert": "prajjwal1/bert-tiny",
        "distillbert": "distilbert-base-uncased"
    };
    has labels = [];
    can ent_ext.entity_detection, ent_ext.train, ent_ext.save_model, ent_ext.load_model;
    can load_model with init entry {
        if (visitor.load_model and "flair_ner" in visitor.models_to_load) {
            ent_ext.load_model(visitor.models_to_load["flair_ner"]);
        }
    }
    can train_model with train_flair_ner activity {
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
            train_params={
                "num_epoch": visitor.num_train_epochs,
                "batch_size": visitor.batch_size,
                "LR": visitor.learning_rate
            }
        );
    }

    can save_model with save_flair_ner entry {
        ent_ext.save_model(model_path=visitor.model);
    }

    can set_pretrained_model with set_flair_ner_pretrained_model entry {
        ent_ext.set_config({
            "ner_model": here.pretrained[visitor.model_type]
        });
    }

    can infer with infer_flair_ner entry {
        # TODO: remove this
        if (here.labels == []) {
            here.labels = ["Fin_Corp"];
        }
        report ent_ext.entity_detection(
            text=visitor.query,
            ner_labels=here.labels
        );
    }
}

walker train_flair_ner {
    has train_file = "data/flair_ner_train.json";
    has from_scratch = false;
    has num_train_epochs = 20;
    has batch_size = 8;
    has learning_rate = 0.02;

    root: take --> node::cai_root;
    cai_root: take --> node::flair_ner;
    flair_ner {
        here::train_model;
    }
}

walker set_flair_ner_pretrained_model {
    has model_type;
    root: take --> node::cai_root;
    cai_root: take --> node::flair_ner;
}

walker save_flair_ner {
    has model_name;
    root: take --> node::cai_root;
    cai_root: take --> node::flair_ner;
}

walker infer_flair_ner {
    has query;
    root: take --> node::cai_root;
    cai_root: take --> node::flair_ner;
}
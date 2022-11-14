node tfm_ner {
    can extract_entity.train, extract_entity.load_model, extract_entity.save_model;
    can extract_entity.set_model_config;

    can load_model with init entry {
        if (visitor.load_model) {
            extract_entity.load_model(visitor.models["tfm_ner"]);
        }
    }

    can train with train_ent_ext entry {
        extract_entity.set_model_config();
        train_data = file.load_json(visitor.train_file);
        ent_ext.train(train_data);
    }

    can save_model with save_tfm_ner entry {
        extract_entity.save_model(visitor.model_name);
    }
}

walker train_tfm_ner {
    has train_file;
    root: take --> node::cai_root;
    cai_root: take --> node::tfm_ner;
}

walker save_tfm_ner {
    has model_name;
}
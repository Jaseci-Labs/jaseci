node tfm_ner {
    can tfm_ner.train, tfm_ner.extract_entity;

    can train {
        train_data = file.load_json(visitor.train_file);
        std.out(train_data);
        tfm_ner.train(
            mode = "default",
            epochs = visitor.num_train_epochs,
            train_data = train_data,
            val_data = train_data
        );
    }

    can infer {
        res = tfm_ner.extract_entity(
            text = visitor.query
        );
        visitor.prediction = res;
    }
}

walker train {
    has train_file;
    has num_train_epochs = 50, from_scratch = true;
    root {
        spawn here --> node::tfm_ner;
        take --> node::tfm_ner;
    }
    tfm_ner: here::train;
}

walker infer {
    has query, interactive = true;
    has labels, prediction;
    root {
        spawn here --> node::tfm_ner;
        take --> node::tfm_ner;
    }
    tfm_ner {
        if (interactive) {
            while true {
                query = std.input("Enter input text (Ctrl-C to exit)> ");
                here::infer;
                std.out(prediction);
            }
        } else {
            here::infer;
            report prediction;
        }
    }
}

walker save_model {
    has model_path;
    can tfm_ner.save_model;
    tfm_ner.save_model(model_path=model_path);
}

walker load_model {
    has model_path;
    can tfm_ner.load_model;
    tfm_ner.load_model(model_path=model_path);
}